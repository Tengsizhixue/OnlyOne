# archive_api.py
"""记忆档案的接口：内容、解锁状态、逐人解锁、相册解锁。

数据文件放在 archive/ 下：
    content.json  公开内容（没有人名、没有答案）
    answers.json  只放服务器（真名 + 答案 + 长文）
    state.sqlite3 运行时生成（会话与解锁记录）

环境变量：
    ARCHIVE_COOKIE_SECURE=1   线上 HTTPS 时设为 1
    ARCHIVE_ADMIN_TOKEN=...   用于 POST /admin/reload 重载内容
    ARCHIVE_AUTHOR_KEY=...    作者暗号；不设就用默认的 210318
"""

from __future__ import annotations

import hashlib
import hmac
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

# 作者身份：没有账号系统，靠一句暗号换一个服务端签名的 cookie。
# 暗号本身不写进源码也不入库，只在环境变量里；签名的值由暗号派生，
# 换暗号即可让所有旧 cookie 立即失效。
AUTHOR_COOKIE = "arch_author"
AUTHOR_TTL = 60 * 60 * 24 * 30      # 30 天
AUTHOR_CMD = "#作者"                 # 留言框里以此开头的，当作登录命令而不是留言
AUTHOR_DEFAULT_KEY = "210318"       # 没配 ARCHIVE_AUTHOR_KEY 时用的暗号
AUTHOR_TRIES = 5                     # 10 分钟内最多试错几次
AUTHOR_WINDOW = 600
_author_tries: dict[str, list[float]] = {}

# 留言提醒：一次最多列多少处（按人合并），够用了
NOTIFY_MAX = 20


class ArchiveDataError(RuntimeError):
    pass


class StageUnlockIn(BaseModel):
    stage: str = Field(min_length=1, max_length=20)
    name: str = Field(min_length=1, max_length=40)


class PhotoUnlockIn(BaseModel):
    album: str = Field(min_length=1, max_length=20)
    answer: str = Field(min_length=1, max_length=40)


class ExtraUnlockIn(BaseModel):
    """附加内容的三道题：作者本意是「挡人」，答案不校验，只要求都填。"""

    stage: str = Field(min_length=1, max_length=20)
    answers: list[str] = Field(default_factory=list, max_length=5)


class CommentIn(BaseModel):
    person: str = Field(min_length=1, max_length=20)
    nick: str = Field(default="", max_length=NICK_MAX)
    body: str = Field(min_length=1, max_length=COMMENT_MAX)
    # 为空就是顶层留言；给了 parent 就是回复。只支持两级：
    # 如果回复的是一条回复，自动挂到那条回复的顶层上（前端渲染更简单）。
    parent: int | None = Field(default=None, ge=1)


class AuthorLoginIn(BaseModel):
    key: str = Field(min_length=1, max_length=200)


class PinIn(BaseModel):
    pinned: bool = True


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

    # 附加内容：答对三题才展示，题目与那句说明随公开内容下发，结构必须完整
    for stage in stages:
        extras = stage.get("extras")
        if not extras:
            continue
        gate = extras.get("gate") or {}
        if not gate.get("questions"):
            raise ArchiveDataError(f"阶段 {stage.get('id')} 的附加内容缺少题目")
        if not gate.get("note"):
            raise ArchiveDataError(f"阶段 {stage.get('id')} 的附加内容缺少答题后的说明")
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
            for field in ("hint", "now", "ai", "raw"):
                text = item.get(field) or ""
                # 附加长文里的人名写成 {{pNNN}}：前端按这个人是否已揭示填真名或 ***。
                # 其余形式的 {{ 都是没替换干净的引用，一律拒绝加载。
                if "{{" in TOKEN_RE.sub("", text):
                    raise ArchiveDataError(f"附加条目 {eid} 的 {field} 里还有未替换的引用")
                tokens.update(TOKEN_RE.findall(text))

    names = answers.get("names")
    if not isinstance(names, dict):
        raise ArchiveDataError("answers.json 缺少 names")
    missing = ids - set(names)
    if missing:
        raise ArchiveDataError(f"这些 id 没有姓名：{sorted(missing)}")

    bad = tokens - ids
    if bad:
        raise ArchiveDataError(f"引用指向不存在的 id：{sorted(bad)}")

    # 相册：公开部分只有题面/张数/体积，图片地址与答案都在 answers.json
    albums = (content.get("photos") or {}).get("albums") or []
    priv = answers.get("photos") or {}
    album_ids: set[str] = set()
    for album in albums:
        aid = album.get("id")
        if not aid:
            raise ArchiveDataError("相册缺少 id")
        if aid in album_ids:
            raise ArchiveDataError(f"相册 id 重复：{aid}")
        album_ids.add(aid)
        if not album.get("question"):
            raise ArchiveDataError(f"相册 {aid} 缺少题目")
        entry = priv.get(aid)
        if not entry:
            raise ArchiveDataError(f"相册 {aid} 在 answers.json 里没有答案")
        if not entry.get("answers"):
            raise ArchiveDataError(f"相册 {aid} 的答案为空")
        images = entry.get("images") or []
        if not images or len(images) != album.get("count"):
            raise ArchiveDataError(f"相册 {aid} 的图片数与 count 对不上")
        for src in images:
            if not str(src).startswith("https://"):
                raise ArchiveDataError(f"相册 {aid} 里有非 https 的图片地址")
    unknown = set(priv) - album_ids
    if unknown:
        raise ArchiveDataError(f"answers.json 里有 content.json 不存在的相册：{sorted(unknown)}")


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

    # 相册：把每个相册的答案归一化成一个集合，比较时不区分空格/大小写；
    # 除了姓名，也接受拼音（和阶段解锁一致），拼音由构建脚本预先算好
    photo_lookup: dict[str, set[str]] = {}
    for aid, entry in (answers.get("photos") or {}).items():
        keys = {_norm(a) for a in (entry.get("answers") or []) if _norm(a)}
        keys.update(_norm(a) for a in (entry.get("pinyin") or []) if _norm(a))
        photo_lookup[aid] = keys

    return {
        "stage_people": stage_people,
        "stage_lookup": stage_lookup,
        "person_ids": frozenset(names),
        "photo_lookup": photo_lookup,
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
                    parent_id INTEGER,
                    role TEXT NOT NULL DEFAULT '',
                    pinned INTEGER NOT NULL DEFAULT 0
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
            # role：作者留言要能和访客区分开；老留言一律视为访客（空串）
            if "role" not in cols:
                conn.execute("ALTER TABLE comments ADD COLUMN role TEXT NOT NULL DEFAULT ''")
            if "pinned" not in cols:
                conn.execute(
                    "ALTER TABLE comments ADD COLUMN pinned INTEGER NOT NULL DEFAULT 0"
                )
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


def _unlocked(sid: str) -> dict[str, list[str]]:
    """这个会话已解锁的东西，按 kind 分组（person / photo）。

    早期的 stage 记录（整栏解锁）不再读取：现在只按人解锁，
    旧记录留在库里不动，不参与任何判断。
    """
    conn = _connect()
    try:
        rows = conn.execute(
            "SELECT kind, key FROM unlocks WHERE sid=?", (sid,)
        ).fetchall()
    finally:
        conn.close()
    out: dict[str, list[str]] = {"person": [], "photo": []}
    for kind, key in rows:
        out.setdefault(kind, []).append(key)
    return {k: sorted(set(v)) for k, v in out.items()}


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


# ---------------------------------------------------------------- 作者身份
def _author_key() -> str:
    """请求时再读，改 .env 后重启即生效。没配就用默认暗号。"""
    return os.getenv("ARCHIVE_AUTHOR_KEY", "").strip() or AUTHOR_DEFAULT_KEY


def _author_signature() -> str:
    """cookie 的值由口令派生：只改口令就能让所有旧 cookie 立即失效。"""
    key = _author_key()
    if not key:
        return ""
    return hmac.new(key.encode("utf-8"), b"archive-author-v1", hashlib.sha256).hexdigest()


def _author_ok(key: str) -> bool:
    expected = _author_key()
    if not expected:
        return False
    return hmac.compare_digest((key or "").strip().encode("utf-8"), expected.encode("utf-8"))


def _is_author(request: Request) -> bool:
    """只认服务端签名的 cookie，前端传什么 role 字段一概不看。"""
    expected = _author_signature()
    if not expected:
        return False
    got = request.cookies.get(AUTHOR_COOKIE) or ""
    return hmac.compare_digest(got, expected)


def _set_author_cookie(response: Response) -> None:
    response.set_cookie(
        AUTHOR_COOKIE,
        _author_signature(),
        max_age=AUTHOR_TTL,
        httponly=True,
        samesite="lax",
        secure=_cookie_secure(),
        path="/",
    )


def _check_author_rate(request: Request) -> None:
    """口令试错单独限流，别把普通留言的额度耗掉，也防暴力猜。"""
    ip = _client_ip(request)
    now = time.time()
    with _lock:
        recent = [t for t in _author_tries.get(ip, []) if now - t < AUTHOR_WINDOW]
        if len(recent) >= AUTHOR_TRIES:
            raise HTTPException(status_code=429, detail="试的次数太多了，过一会儿再试。")
        recent.append(now)
        _author_tries[ip] = recent


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
    state = _unlocked(sid)

    # 只按人解锁：输对谁就只显示谁，不再整栏放开。
    # 例外是作者模式：签名 cookie 验过之后把所有名字一起给下去，
    # 「解除所有匿名」只在服务端判定，前端拿不到这个能力。
    if _is_author(request):
        names = dict(answers["names"])
        people = list(names)
    else:
        people = [pid for pid in state["person"] if pid in index["person_ids"]]
        names = {pid: answers["names"][pid] for pid in people}
    stage_ids = {s.get("id") for s in content.get("stages", [])}

    return {
        "version": content.get("version", 1),
        "people": people,
        "names": names,
        # 旧前端会读 stages：现在没有整栏解锁，一律给空数组
        "stages": [],
        # 已答过题的附加内容（按栏的 id），刷新后不用再答一遍
        "extras": [sid for sid in state.get("extra", []) if sid in stage_ids],
        "photos": {
            aid: _photo_items(answers, aid)
            for aid in state["photo"]
            if aid in index["photo_lookup"]
        },
    }


@router.post("/unlock/stage", include_in_schema=False)
@router.post("/unlock/person")
def unlock_person(body: StageUnlockIn, request: Request, response: Response) -> dict:
    """输入姓名 / 拼音 / 外号，只揭示输入对的那一个人，不放开整栏。"""
    _, answers, index = _require()
    _check_rate(request)
    lookup = index["stage_lookup"].get(body.stage)
    if lookup is None:
        raise HTTPException(status_code=404, detail="没有这个阶段。")

    pid = lookup.get(_norm(body.name))
    if not pid:
        raise HTTPException(status_code=400, detail="姓名或拼音不对，再想想。")

    sid = _session_id(request, response)
    _record_unlock(sid, "person", pid)
    name = answers["names"][pid]
    return {
        "ok": True,
        "stage": body.stage,
        "person": pid,
        "name": name,
        "names": {pid: name},  # 兼容只读 names 的旧前端
    }


# ---------------------------------------------------------------- 相册缩略图
# 图床（photo.160615.xyz）由 Worker 代理阿里云 OSS，同一 zone 上开了
# Cloudflare Images 的 Transformations，可以直接在路径前加 /cdn-cgi/image/ 取缩略图。
# 免费额度是「每月 5000 次唯一转换」，唯一 = 源图 + 参数，月度去重，与访问量无关，
# 这一册 55 张图只占 55 次。onerror=redirect 让转换失败（比如额度异常）时回落到原图，
# 宁可多花流量也不出裂图。
THUMB_PREFIX = "/cdn-cgi/image/width=320,quality=72,format=auto,onerror=redirect/"


def _thumb(src: str) -> str:
    """原图地址 → 缩略图地址；认不出来的地址就返回空串，前端回落到原图。"""
    if not src.startswith("https://"):
        return ""
    host, sep, path = src[len("https://"):].partition("/")
    if not sep or not path:
        return ""
    return f"https://{host}{THUMB_PREFIX}{path}"


def _photo_items(answers: dict, album_id: str) -> list[dict]:
    """每张图同时给原图和缩略图：网格用 thumb，点开看大图用 url。"""
    images = (answers.get("photos") or {}).get(album_id, {}).get("images") or []
    return [{"url": src, "thumb": _thumb(src)} for src in images]


@router.post("/unlock/photo")
def unlock_photo(body: PhotoUnlockIn, request: Request, response: Response) -> dict:
    """答对才把图片地址发下去。地址本身不放在 content.json 里，猜不到。"""
    _, answers, index = _require()
    _check_rate(request)
    allowed = index["photo_lookup"].get(body.album)
    if allowed is None:
        raise HTTPException(status_code=404, detail="没有这个相册。")

    if _norm(body.answer) not in allowed:
        raise HTTPException(status_code=400, detail="答案不对，再想想。")

    sid = _session_id(request, response)
    _record_unlock(sid, "photo", body.album)
    return {
        "ok": True,
        "album": body.album,
        "images": _photo_items(answers, body.album),
    }


# ---------------------------------------------------------------- 附加内容
@router.post("/unlock/extra")
def unlock_extra(body: ExtraUnlockIn, request: Request, response: Response) -> dict:
    """三道题都填了就放行。

    作者的原话是「无论答什么其实都是对的，只是想挡住一些人」，
    所以这里不比对答案，只要求每道题都有内容——真正的作用是让人停一下。
    """
    content, _, _ = _require()
    _check_rate(request)

    stage = next(
        (
            s
            for s in content.get("stages", [])
            if s.get("id") == body.stage and s.get("extras")
        ),
        None,
    )
    if stage is None:
        raise HTTPException(status_code=404, detail="没有这个阶段。")

    questions = (stage["extras"].get("gate") or {}).get("questions") or []
    answers = [(a or "").strip()[:100] for a in (body.answers or [])]
    if len(answers) != len(questions) or any(not a for a in answers):
        raise HTTPException(status_code=400, detail="三个问题都要填。")

    sid = _session_id(request, response)
    _record_unlock(sid, "extra", body.stage)
    return {"ok": True, "stage": body.stage}


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
    cid, nick, body, created, author, parent_id, role, pinned = row
    return {
        "id": cid,
        "nick": nick,
        "body": body,
        "created": created,
        "mine": author == sid,
        "role": role or "",
        "pinned": bool(pinned),
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
            "SELECT id, nick, body, created, sid, parent_id, role, pinned"
            " FROM comments WHERE person=? AND hidden=0 ORDER BY id ASC",
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

    # 顶层留言按发表时间正序（老的在上、新的在下）；超过上限时保留最近的若干条。
    # 被置顶的不参与截断，否则老早置顶的那条会被后来的留言挤掉。
    if len(top_rows) > COMMENT_PAGE:
        keep = {r[0] for r in top_rows[-COMMENT_PAGE:]} | {r[0] for r in top_rows if r[7]}
        top_rows = [r for r in top_rows if r[0] in keep]
    # 置顶的排最前，其余保持时间正序
    top_rows.sort(key=lambda r: (0 if r[7] else 1, r[0]))

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

    # 暗号就是口令本身：整条内容正好等于暗号时，当作登录而不是留言。
    # 「#作者 暗号」的老写法也留着，以后换成更长的口令照样能用。
    # 失败一律回同一句话，不暴露这里有作者模式。
    cmd = text.startswith(AUTHOR_CMD)
    if cmd or hmac.compare_digest(text.encode("utf-8"), _author_key().encode("utf-8")):
        _check_author_rate(request)
        key = text[len(AUTHOR_CMD):] if cmd else text
        if not _author_ok(key):
            time.sleep(0.4)
            raise HTTPException(status_code=403, detail="这条不能发。")
        _set_author_cookie(response)
        return {"ok": True, "author": True, "command": True}

    if URL_RE.search(text):
        raise HTTPException(status_code=400, detail="留言里请不要带链接。")
    nick = _clean_text(body.nick, NICK_MAX).replace("\n", " ")

    sid = _session_id(request, response)
    # 身份只由签名 cookie 决定，前端传什么都不算数
    role = "author" if _is_author(request) else ""
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
            "INSERT INTO comments(person, sid, nick, body, created, parent_id, role)"
            " VALUES(?, ?, ?, ?, ?, ?, ?)",
            (body.person, sid, nick, text, now, parent_id, role),
        )
        conn.commit()
        cid = cur.lastrowid
    finally:
        conn.close()

    item: dict = {
        "id": cid, "nick": nick, "body": text,
        "created": now, "mine": True, "parent": parent_id,
        "role": role, "pinned": False,
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
    author = _is_author(request)
    conn = _connect()
    try:
        row = conn.execute(
            "SELECT sid, parent_id FROM comments WHERE id=?", (cid,)
        ).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="这条留言已经不在了。")
        own = row[0] == sid
        if not own and not author:
            raise HTTPException(status_code=403, detail="只能删除自己发的留言。")

        # 级联：收集所有子孙（BFS）
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
        if own:
            conn.execute(f"DELETE FROM comments WHERE id IN ({placeholders})", to_delete)
        else:
            # 作者删别人的留言走软删：留底以便误删时能捞回来，页面上等同于消失
            conn.execute(
                f"UPDATE comments SET hidden=1 WHERE id IN ({placeholders})", to_delete
            )
        conn.commit()
    finally:
        conn.close()
    return {"ok": True, "deleted": to_delete, "hidden": not own}


# ---------------------------------------------------------------- 留言提醒
@router.get("/notifications")
def notifications(request: Request, response: Response, since: int = 0) -> dict:
    """谁在我关心的地方说话了。

    作者：所有新留言/回复（按人合并），用来知道该回谁；
    访客：只有「挂在我自己发过的留言下面」的回复，别人的事一律不打扰。
    只下发「哪个人、几条、最新 id」，不带正文，所以没解锁这个人也不会漏内容。
    """
    _, _, index = _require()
    response.headers["Cache-Control"] = "no-store"
    _init_db()
    sid = _session_id(request, response)
    author = _is_author(request)
    # since 传负数表示「这台设备还没记录过看到哪儿了」（第一次打开页面）
    first_visit = since < 0
    since = max(0, since)

    conn = _connect()
    try:
        last = conn.execute(
            "SELECT COALESCE(MAX(id), 0) FROM comments WHERE hidden=0"
        ).fetchone()[0]
        rows = []
        # 第一次打开（since<0）只提醒最新的一处，别把攒了半年的留言一次性糊到脸上；
        # 一处也算有意义——作者换台电脑打开也知道最后有人在哪里说话。
        if last > since:
            if author:
                # 作者自己的留言 role 是 author，排除掉，免得自己提醒自己
                rows = conn.execute(
                    "SELECT person, COUNT(*), MAX(id) FROM comments"
                    " WHERE hidden=0 AND id>? AND role<>'author'"
                    " GROUP BY person ORDER BY MAX(id) DESC LIMIT ?",
                    (since, NOTIFY_MAX),
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT person, COUNT(*), MAX(id) FROM comments"
                    " WHERE hidden=0 AND id>? AND sid<>?"
                    " AND parent_id IN"
                    " (SELECT id FROM comments WHERE sid=? AND hidden=0)"
                    " GROUP BY person ORDER BY MAX(id) DESC LIMIT ?",
                    (since, sid, sid, NOTIFY_MAX),
                ).fetchall()
            if first_visit:
                rows = rows[:1]
    finally:
        conn.close()

    items = [
        {"person": row[0], "count": row[1], "id": row[2]}
        for row in rows
        if row[0] in index["person_ids"]
    ]
    return {"author": author, "items": items, "last": last}


# ---------------------------------------------------------------- 作者模式
@router.get("/author/status")
def author_status(request: Request, response: Response) -> dict:
    response.headers["Cache-Control"] = "no-store"
    return {"author": _is_author(request), "enabled": bool(_author_key())}


@router.post("/author/login")
def author_login(body: AuthorLoginIn, request: Request, response: Response) -> dict:
    if not _author_key():
        raise HTTPException(status_code=403, detail="这条不能发。")
    _check_author_rate(request)
    if not _author_ok(body.key):
        time.sleep(0.4)
        raise HTTPException(status_code=403, detail="这条不能发。")
    _set_author_cookie(response)
    return {"ok": True, "author": True}


@router.post("/author/logout")
def author_logout(response: Response) -> dict:
    response.delete_cookie(AUTHOR_COOKIE, path="/")
    return {"ok": True, "author": False}


@router.post("/comments/{cid}/pin")
def pin_comment(cid: int, body: PinIn, request: Request, response: Response) -> dict:
    _require()
    if not _is_author(request):
        raise HTTPException(status_code=403, detail="只有作者能置顶。")
    _init_db()
    conn = _connect()
    try:
        row = conn.execute(
            "SELECT parent_id FROM comments WHERE id=? AND hidden=0", (cid,)
        ).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="这条留言已经不在了。")
        if row[0] is not None:
            raise HTTPException(status_code=400, detail="只能置顶顶层留言。")
        conn.execute(
            "UPDATE comments SET pinned=? WHERE id=?",
            (1 if body.pinned else 0, cid),
        )
        conn.commit()
    finally:
        conn.close()
    return {"ok": True, "pinned": bool(body.pinned)}


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
        "albums": len((content.get("photos") or {}).get("albums") or []),
        "updated": content.get("updated"),
    }
