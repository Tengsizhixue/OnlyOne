# archive_api.py
"""记忆档案的接口：内容、解锁状态、阶段解锁、附加条目解锁。

数据文件放在 archive/ 下：
    content.json  公开内容（没有人名、没有答案）
    answers.json  只放服务器（真名 + 答案 + 长文）
    state.sqlite3 运行时生成（会话与解锁记录）

环境变量：
    ARCHIVE_COOKIE_SECURE=1   线上 HTTPS 时设为 1
    ARCHIVE_ADMIN_TOKEN=...   用于 POST /admin/reload 重载内容
"""

from __future__ import annotations

import json
import os
import re
import secrets
import sqlite3
import threading
import time
from pathlib import Path

from fastapi import APIRouter, Header, HTTPException, Request, Response
from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).resolve().parent
ARCHIVE_DIR = BASE_DIR / "archive"
CONTENT_PATH = ARCHIVE_DIR / "content.json"
ANSWERS_PATH = ARCHIVE_DIR / "answers.json"
DB_PATH = ARCHIVE_DIR / "state.sqlite3"

COOKIE_NAME = "arch_sid"
COOKIE_MAX_AGE = 60 * 60 * 24 * 365


def _cookie_secure() -> bool:
    """请求时再读，保证 .env / systemd 两种配置都能生效。"""
    return os.getenv("ARCHIVE_COOKIE_SECURE", "0").strip().lower() in {"1", "true", "yes"}

router = APIRouter(tags=["archive"])

_lock = threading.Lock()
_db_ready = False
_content: dict | None = None
_answers: dict | None = None
_index: dict | None = None
_rate: dict[str, list[float]] = {}

TOKEN_RE = re.compile(r"\{\{(p\d{3})\}\}")
RATE_LIMIT = 60

# 公开留言
COMMENT_MAX = 300          # 单条字数上限
NICK_MAX = 12              # 昵称字数上限
COMMENT_PAGE = 200         # 每个人最多返回多少条
URL_RE = re.compile(
    r"(https?://|www\.|\b[a-z0-9-]+\.(?:com|cn|net|org|xyz|top|site|me|cc|io)\b)",
    re.IGNORECASE,
)


class ArchiveDataError(RuntimeError):
    pass


class StageUnlockIn(BaseModel):
    stage: str = Field(min_length=1, max_length=20)
    name: str = Field(min_length=1, max_length=40)


class CommentIn(BaseModel):
    person: str = Field(min_length=1, max_length=20)
    nick: str = Field(default="", max_length=NICK_MAX)
    body: str = Field(min_length=1, max_length=COMMENT_MAX)
    # 为空就是顶层留言；给了 parent 就是回复。只支持两级：
    # 如果回复的是一条回复，自动挂到那条回复的顶层上（前端渲染更简单）。
    parent: int | None = Field(default=None, ge=1)


def _norm(value: str) -> str:
    return re.sub(r"\s+", "", value or "").lower()


# ---------------------------------------------------------------- 数据加载
def _validate(content: dict, answers: dict) -> None:
    stages = content.get("stages")
    if not isinstance(stages, list) or not stages:
        raise ArchiveDataError("content.json 缺少 stages")

    ids: set[str] = set()
    tokens: set[str] = set()
    extras_ids: set[str] = set()

    for stage in stages:
        for group in stage.get("groups", []):
            for person in group.get("people", []):
                pid = person.get("id")
                if not pid:
                    raise ArchiveDataError("有人的 id 为空")
                if pid in ids:
                    raise ArchiveDataError(f"id 重复：{pid}")
                if "name" in person:
                    raise ArchiveDataError(f"{pid} 里出现了 name 字段，公开内容不能带真名")
                ids.add(pid)
                tokens.update(TOKEN_RE.findall(person.get("desc", "")))

    # 附加内容现在是公开长文，直接挂在某一栏里，不需要答案：只校验结构完整
    for stage in stages:
        extras = stage.get("extras")
        if not extras:
            continue
        items = extras.get("items") or []
        if not items:
            raise ArchiveDataError(f"阶段 {stage.get('id')} 的附加内容没有条目")
        for item in items:
            eid = item.get("id")
            if not eid:
                raise ArchiveDataError("附加条目 id 为空")
            if eid in extras_ids:
                raise ArchiveDataError(f"附加条目 id 重复：{eid}")
            extras_ids.add(eid)
            if not item.get("ai"):
                raise ArchiveDataError(f"附加条目 {eid} 缺少 AI 总结")
            for field in ("hint", "ai", "raw"):
                if "{{" in (item.get(field) or ""):
                    raise ArchiveDataError(f"附加条目 {eid} 的 {field} 里还有未替换的引用")

    names = answers.get("names")
    if not isinstance(names, dict):
        raise ArchiveDataError("answers.json 缺少 names")
    missing = ids - set(names)
    if missing:
        raise ArchiveDataError(f"这些 id 没有姓名：{sorted(missing)}")

    bad = tokens - ids
    if bad:
        raise ArchiveDataError(f"引用指向不存在的 id：{sorted(bad)}")


def _build_index(content: dict, answers: dict) -> dict:
    names = answers["names"]
    aliases: dict[str, list[str]] = answers.get("aliases") or {}
    pinyin: dict[str, list[str]] = answers.get("pinyin") or {}
    stage_people: dict[str, list[str]] = {}
    stage_lookup: dict[str, dict[str, str]] = {}
    for stage in content["stages"]:
        sid = stage["id"]
        people = [p["id"] for g in stage["groups"] for p in g["people"]]
        stage_people[sid] = people
        lookup: dict[str, str] = {}
        for pid in people:
            key = _norm(names[pid])
            if key in lookup:
                raise ArchiveDataError(f"阶段 {sid} 里有重名：{names[pid]}")
            lookup[key] = pid

        # 别名（外号对应的原名）和拼音也能解锁。撞车的键（两个人的拼音一样）
        # 直接丢掉：宁可当作不认识，也不能把人认错。
        claimed: dict[str, set[str]] = {}
        for pid in people:
            for extra in [*aliases.get(pid, []), *pinyin.get(pid, [])]:
                key = _norm(extra)
                if key:
                    claimed.setdefault(key, set()).add(pid)
        for key, owners in claimed.items():
            if len(owners) == 1 and key not in lookup:
                lookup[key] = next(iter(owners))

        stage_lookup[sid] = lookup
    return {
        "stage_people": stage_people,
        "stage_lookup": stage_lookup,
        "person_ids": frozenset(names),
    }


def _load(force: bool = False) -> None:
    global _content, _answers, _index
    with _lock:
        if _content is not None and not force:
            return
        try:
            content = json.loads(CONTENT_PATH.read_text(encoding="utf-8"))
            answers = json.loads(ANSWERS_PATH.read_text(encoding="utf-8"))
        except FileNotFoundError as exc:
            raise ArchiveDataError(f"缺少数据文件：{exc.filename}") from exc
        except json.JSONDecodeError as exc:
            raise ArchiveDataError(f"JSON 格式错误：{exc}") from exc
        _validate(content, answers)
        _content, _answers = content, answers
        _index = _build_index(content, answers)


def _require() -> tuple[dict, dict, dict]:
    try:
        _load()
    except ArchiveDataError as exc:
        raise HTTPException(status_code=503, detail=f"档案数据未就绪：{exc}") from exc
    assert _content is not None and _answers is not None and _index is not None
    return _content, _answers, _index


# ---------------------------------------------------------------- SQLite
def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, timeout=5)
    conn.execute("PRAGMA busy_timeout=5000")
    return conn


def _init_db() -> None:
    global _db_ready
    if _db_ready:
        return
    with _lock:
        if _db_ready:
            return
        ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
        conn = _connect()
        try:
            conn.execute("PRAGMA journal_mode=WAL")
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS sessions (
                    sid TEXT PRIMARY KEY,
                    created INTEGER NOT NULL
                );
                CREATE TABLE IF NOT EXISTS unlocks (
                    sid TEXT NOT NULL,
                    kind TEXT NOT NULL,
                    key TEXT NOT NULL,
                    created INTEGER NOT NULL,
                    PRIMARY KEY (sid, kind, key)
                );
                CREATE TABLE IF NOT EXISTS comments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    person TEXT NOT NULL,
                    sid TEXT NOT NULL,
                    nick TEXT NOT NULL DEFAULT '',
                    body TEXT NOT NULL,
                    created INTEGER NOT NULL,
                    hidden INTEGER NOT NULL DEFAULT 0,
                    parent_id INTEGER
                );
                CREATE INDEX IF NOT EXISTS idx_comments_person
                    ON comments(person, id);
                """
            )
            # 老库补列：之前没有 parent_id 的数据库走 ALTER TABLE 升级。
            # 只做一次 PRAGMA 检查，开销可以忽略。
            cols = {row[1] for row in conn.execute("PRAGMA table_info(comments)")}
            if "parent_id" not in cols:
                conn.execute("ALTER TABLE comments ADD COLUMN parent_id INTEGER")
            # 索引放在迁移之后：旧库没有 parent_id 列时直接建索引会报错
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_comments_parent"
                " ON comments(parent_id, id)"
            )
            conn.commit()
        finally:
            conn.close()
        _db_ready = True


def _session_id(request: Request, response: Response) -> str:
    sid = request.cookies.get(COOKIE_NAME)
    _init_db()
    if sid:
        conn = _connect()
        try:
            row = conn.execute("SELECT 1 FROM sessions WHERE sid=?", (sid,)).fetchone()
        finally:
            conn.close()
        if row:
            return sid

    sid = secrets.token_urlsafe(24)
    conn = _connect()
    try:
        conn.execute(
            "INSERT OR IGNORE INTO sessions(sid, created) VALUES(?, ?)",
            (sid, int(time.time())),
        )
        conn.commit()
    finally:
        conn.close()

    response.set_cookie(
        COOKIE_NAME,
        sid,
        max_age=COOKIE_MAX_AGE,
        httponly=True,
        samesite="lax",
        secure=_cookie_secure(),
        path="/",
    )
    return sid


def _unlocked(sid: str) -> list[str]:
    conn = _connect()
    try:
        rows = conn.execute(
            "SELECT kind, key FROM unlocks WHERE sid=?", (sid,)
        ).fetchall()
    finally:
        conn.close()
    return sorted({key for kind, key in rows if kind == "stage"})


def _record_unlock(sid: str, kind: str, key: str) -> None:
    conn = _connect()
    try:
        conn.execute(
            "INSERT OR IGNORE INTO unlocks(sid, kind, key, created) VALUES(?, ?, ?, ?)",
            (sid, kind, key, int(time.time())),
        )
        conn.commit()
    finally:
        conn.close()


# ---------------------------------------------------------------- 限流
def _client_ip(request: Request) -> str:
    forwarded = request.headers.get("cf-connecting-ip") or request.headers.get("x-real-ip")
    if forwarded:
        return forwarded.strip()
    return request.client.host if request.client else "unknown"


def _check_rate(request: Request) -> None:
    ip = _client_ip(request)
    now = time.time()
    with _lock:
        recent = [t for t in _rate.get(ip, []) if now - t < 60]
        if len(recent) >= RATE_LIMIT:
            raise HTTPException(status_code=429, detail="请求过于频繁，请稍后再试。")
        recent.append(now)
        _rate[ip] = recent


# ---------------------------------------------------------------- 接口
@router.get("/content")
def archive_content(response: Response) -> dict:
    content, _, _ = _require()
    response.headers["Cache-Control"] = "no-store"
    return content


@router.get("/state")
def archive_state(request: Request, response: Response) -> dict:
    content, answers, index = _require()
    response.headers["Cache-Control"] = "no-store"
    sid = _session_id(request, response)
    stages = _unlocked(sid)

    valid_stages = [s for s in stages if s in index["stage_people"]]
    names: dict[str, str] = {}
    for stage_id in valid_stages:
        for pid in index["stage_people"][stage_id]:
            names[pid] = answers["names"][pid]

    return {
        "version": content.get("version", 1),
        "stages": valid_stages,
        "names": names,
    }


@router.post("/unlock/stage")
def unlock_stage(body: StageUnlockIn, request: Request, response: Response) -> dict:
    _, answers, index = _require()
    _check_rate(request)
    lookup = index["stage_lookup"].get(body.stage)
    if lookup is None:
        raise HTTPException(status_code=404, detail="没有这个阶段。")

    pid = lookup.get(_norm(body.name))
    if not pid:
        raise HTTPException(
            status_code=400,
            detail="姓名不正确，请输入本阶段名单中的任意一个人名。",
        )

    sid = _session_id(request, response)
    _record_unlock(sid, "stage", body.stage)
    people = index["stage_people"][body.stage]
    return {
        "ok": True,
        "stage": body.stage,
        "names": {p: answers["names"][p] for p in people},
    }


# ---------------------------------------------------------------- 公开留言
def _clean_text(value: str, limit: int) -> str:
    """去掉控制字符、压掉多余空行、截到上限。换行本身要留着。"""
    text = (value or "").replace("\r\n", "\n").replace("\r", "\n")
    text = "".join(ch for ch in text if ch == "\n" or ch >= " ")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()[:limit]


def _snippet(text: str, limit: int = 15) -> str:
    """把留言正文压成单行短引用，用于回复的引用行消歧重名。"""
    flat = re.sub(r"\s+", " ", text or "").strip()
    return flat[:limit] + ("…" if len(flat) > limit else "")


def _comment_row(row: tuple, sid: str) -> dict:
    cid, nick, body, created, author, parent_id = row
    return {
        "id": cid,
        "nick": nick,
        "body": body,
        "created": created,
        "mine": author == sid,
        "parent": parent_id,
    }


@router.get("/comments")
def list_comments(person: str, request: Request, response: Response) -> dict:
    _, _, index = _require()
    response.headers["Cache-Control"] = "no-store"
    if person not in index["person_ids"]:
        raise HTTPException(status_code=404, detail="没有这个人。")

    _init_db()
    sid = _session_id(request, response)
    conn = _connect()
    try:
        rows = conn.execute(
            "SELECT id, nick, body, created, sid, parent_id FROM comments"
            " WHERE person=? AND hidden=0 ORDER BY id ASC",
            (person,),
        ).fetchall()
    finally:
        conn.close()

    total = len(rows)
    by_id: dict[int, tuple] = {r[0]: r for r in rows}

    # 找到每条回复的顶层祖先（防循环用 seen）
    def _find_root(cid: int) -> int | None:
        seen: set[int] = set()
        cur = cid
        while cur in by_id and cur not in seen:
            seen.add(cur)
            if by_id[cur][5] is None:
                return cur
            cur = by_id[cur][5]
        return None

    top_rows = [r for r in rows if r[5] is None]
    children: dict[int, list[tuple]] = {}
    for r in rows:
        if r[5] is not None:
            root = _find_root(r[0])
            if root is not None:
                children.setdefault(root, []).append(r)

    # 顶层留言按发表时间正序（老的在上、新的在下）；超过上限时保留最近的若干条
    if len(top_rows) > COMMENT_PAGE:
        top_rows = top_rows[-COMMENT_PAGE:]

    items = []
    for r in top_rows:
        item = _comment_row(r, sid)
        replies = []
        for c in children.get(r[0], []):
            ri = _comment_row(c, sid)
            # 如果是回复另一条回复，带上被回复者昵称和内容片段，
            # 重名时靠“当时说了什么”区分
            pid = c[5]
            if pid and pid != r[0] and pid in by_id:
                ri["replyTo"] = by_id[pid][1] or "匿名"
                ri["replyToSnippet"] = _snippet(by_id[pid][2])
            else:
                ri["replyTo"] = ""
                ri["replyToSnippet"] = ""
            replies.append(ri)
        item["replies"] = replies
        items.append(item)

    return {"items": items, "count": total}


@router.post("/comments")
def add_comment(body: CommentIn, request: Request, response: Response) -> dict:
    _, _, index = _require()
    _check_rate(request)
    if body.person not in index["person_ids"]:
        raise HTTPException(status_code=404, detail="没有这个人。")

    text = _clean_text(body.body, COMMENT_MAX)
    if not text:
        raise HTTPException(status_code=400, detail="留言不能是空的。")
    if URL_RE.search(text):
        raise HTTPException(status_code=400, detail="留言里请不要带链接。")
    nick = _clean_text(body.nick, NICK_MAX).replace("\n", " ")

    sid = _session_id(request, response)
    now = int(time.time())
    conn = _connect()
    try:
        # 验证父评论
        parent_id = None
        reply_to_nick = ""
        reply_to_snippet = ""
        root_id = None
        if body.parent:
            parent_row = conn.execute(
                "SELECT id, person, nick, parent_id, body FROM comments"
                " WHERE id=? AND hidden=0",
                (body.parent,),
            ).fetchone()
            if not parent_row:
                raise HTTPException(status_code=400, detail="回复的留言已经不在了。")
            if parent_row[1] != body.person:
                raise HTTPException(status_code=400, detail="只能回复同一个人下面的留言。")
            parent_id = parent_row[0]
            reply_to_nick = parent_row[2] or "匿名"
            reply_to_snippet = _snippet(parent_row[4])
            # 找到顶层 id，前端需要用来定位插入位置
            root_id = parent_row[3] if parent_row[3] is not None else parent_row[0]

        cur = conn.execute(
            "INSERT INTO comments(person, sid, nick, body, created, parent_id)"
            " VALUES(?, ?, ?, ?, ?, ?)",
            (body.person, sid, nick, text, now, parent_id),
        )
        conn.commit()
        cid = cur.lastrowid
    finally:
        conn.close()

    item: dict = {
        "id": cid, "nick": nick, "body": text,
        "created": now, "mine": True, "parent": parent_id,
    }
    if parent_id:
        item["replyTo"] = reply_to_nick
        item["replyToSnippet"] = reply_to_snippet
        item["rootId"] = root_id
    return {"ok": True, "item": item}


@router.delete("/comments/{cid}")
def delete_comment(cid: int, request: Request, response: Response) -> dict:
    _require()
    _check_rate(request)
    _init_db()
    sid = _session_id(request, response)
    conn = _connect()
    try:
        row = conn.execute(
            "SELECT sid, parent_id FROM comments WHERE id=?", (cid,)
        ).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="这条留言已经不在了。")
        if row[0] != sid:
            raise HTTPException(status_code=403, detail="只能删除自己发的留言。")

        # 级联删除：收集所有子孙（BFS）
        to_delete = [cid]
        queue = [cid]
        while queue:
            current = queue.pop(0)
            children = conn.execute(
                "SELECT id FROM comments WHERE parent_id=?", (current,)
            ).fetchall()
            for child in children:
                to_delete.append(child[0])
                queue.append(child[0])

        placeholders = ",".join("?" * len(to_delete))
        conn.execute(f"DELETE FROM comments WHERE id IN ({placeholders})", to_delete)
        conn.commit()
    finally:
        conn.close()
    return {"ok": True, "deleted": to_delete}


@router.post("/admin/reload")
def archive_reload(x_admin_token: str = Header(default="")) -> dict:
    expected = os.getenv("ARCHIVE_ADMIN_TOKEN", "")
    if not expected or not secrets.compare_digest(x_admin_token, expected):
        raise HTTPException(status_code=403, detail="forbidden")
    try:
        _load(force=True)
    except ArchiveDataError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    content, answers, _ = _require()
    return {
        "ok": True,
        "people": len(answers["names"]),
        "extras": sum(
            len(st.get("extras", {}).get("items", []))
            for st in content.get("stages", [])
        ),
        "updated": content.get("updated"),
    }
