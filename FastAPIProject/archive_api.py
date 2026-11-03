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


class ArchiveDataError(RuntimeError):
    pass


class StageUnlockIn(BaseModel):
    stage: str = Field(min_length=1, max_length=20)
    name: str = Field(min_length=1, max_length=40)


class ExtraUnlockIn(BaseModel):
    id: str = Field(min_length=1, max_length=20)
    answer: str = Field(min_length=0, max_length=100)


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

    for extra in content.get("extras", []):
        eid = extra.get("id")
        if not eid:
            raise ArchiveDataError("附加条目 id 为空")
        if eid in extras_ids:
            raise ArchiveDataError(f"附加条目 id 重复：{eid}")
        extras_ids.add(eid)

    names = answers.get("names")
    if not isinstance(names, dict):
        raise ArchiveDataError("answers.json 缺少 names")
    missing = ids - set(names)
    if missing:
        raise ArchiveDataError(f"这些 id 没有姓名：{sorted(missing)}")

    extra_answers = answers.get("extras")
    if not isinstance(extra_answers, dict):
        raise ArchiveDataError("answers.json 缺少 extras")
    missing = extras_ids - set(extra_answers)
    if missing:
        raise ArchiveDataError(f"这些附加条目没有答案：{sorted(missing)}")

    for eid, item in extra_answers.items():
        if not item.get("answer"):
            raise ArchiveDataError(f"{eid} 缺少答案")
        if not item.get("ai") or not item.get("raw"):
            raise ArchiveDataError(f"{eid} 缺少 AI 总结或原文")
        tokens.update(TOKEN_RE.findall(item["ai"]))
        tokens.update(TOKEN_RE.findall(item["raw"]))
        choice = item.get("choice")
        if choice:
            if not choice.get("correct") or not choice.get("explanation"):
                raise ArchiveDataError(f"{eid} 的选择题缺少正确答案或解析")
            tokens.update(TOKEN_RE.findall(choice["explanation"]))

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
        "extras": answers["extras"],
    }


def _extra_ids(content: dict) -> list[str]:
    """附加条目按公开内容里的顺序排列，用于判断"是否全部答对"。"""
    return [e["id"] for e in content.get("extras", []) if e.get("id")]


def _extra_payload(item: dict, names: dict[str, str]) -> dict:
    """答对三题之后才发下去的内容。

    这里的姓名直接换成真名：三题全对本身就是一道门，而且原文里本来就是真名，
    再显示 *** 会和原文自相矛盾。
    """

    def fill(text: str) -> str:
        return TOKEN_RE.sub(lambda m: names.get(m.group(1), "***"), text or "")

    payload = {"ai": fill(item["ai"]), "raw": fill(item["raw"])}
    choice = item.get("choice")
    if choice:
        payload["choice"] = {
            "question": choice["question"],
            "options": choice["options"],
            "correct": choice["correct"],
            "explanation": fill(choice["explanation"]),
        }
    return payload


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
                CREATE TABLE IF NOT EXISTS completions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sid TEXT NOT NULL UNIQUE,
                    created INTEGER NOT NULL
                );
                """
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


def _unlocked(sid: str) -> tuple[list[str], list[str]]:
    conn = _connect()
    try:
        rows = conn.execute(
            "SELECT kind, key FROM unlocks WHERE sid=?", (sid,)
        ).fetchall()
    finally:
        conn.close()
    stages = sorted({key for kind, key in rows if kind == "stage"})
    extras = sorted({key for kind, key in rows if kind == "extra"})
    return stages, extras


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


# ---------------------------------------------------------------- 完成人数与名次
def _record_completion(sid: str) -> None:
    """三题全对的人各占一行；重复访问只保留最早那次，名次不会被刷新。"""
    _init_db()
    conn = _connect()
    try:
        conn.execute(
            "INSERT OR IGNORE INTO completions(sid, created) VALUES(?, ?)",
            (sid, int(time.time())),
        )
        conn.commit()
    finally:
        conn.close()


def _ranking(sid: str) -> dict:
    """按首次完成时间排位：total 是全部答对过的人数，rank 是本人的位次。

    没有账号体系，所以身份用 cookie 里的 sid 表示（浏览器维度），而不是 IP：
    手机流量、公司/校园网都是多人共用一个出口 IP，按 IP 统计会把人算少；
    换 WiFi 又会让同一个人变成新的 IP。sid 落在浏览器上，更接近“一个人”。
    清缓存或换设备会被当成新的一个，这是这套无账号方案能接受的上限。
    """
    _init_db()
    conn = _connect()
    try:
        row = conn.execute("SELECT id FROM completions WHERE sid=?", (sid,)).fetchone()
        total = conn.execute("SELECT COUNT(*) FROM completions").fetchone()[0]
        rank = 0
        if row:
            # 用自增 id 排位，不用时间戳：同一秒内完成的两个人否则会算成同一名
            rank = conn.execute(
                "SELECT COUNT(*) FROM completions WHERE id <= ?", (row[0],)
            ).fetchone()[0]
    finally:
        conn.close()
    return {"total": total, "rank": rank}


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
    stages, extras = _unlocked(sid)

    valid_stages = [s for s in stages if s in index["stage_people"]]
    names: dict[str, str] = {}
    for stage_id in valid_stages:
        for pid in index["stage_people"][stage_id]:
            names[pid] = answers["names"][pid]

    required = _extra_ids(content)
    answered = [eid for eid in required if eid in extras]
    texts: dict[str, dict] = {}
    ranking = {"total": 0, "rank": 0}
    # 三题全部答对才把内容发下来；只答对一两题时前端只知道"已经答过哪几题"
    if required and len(answered) == len(required):
        texts = {eid: _extra_payload(index["extras"][eid], answers["names"]) for eid in required}
        ranking = _ranking(sid)
        # 加排行榜之前就答完的人没有记录，这里补一条，否则回访看不到名次
        if not ranking["rank"]:
            _record_completion(sid)
            ranking = _ranking(sid)

    return {
        "version": content.get("version", 1),
        "stages": valid_stages,
        "extras": answered,
        "names": names,
        "extraTexts": texts,
        "ranking": ranking,
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


@router.post("/unlock/extra")
def unlock_extra(body: ExtraUnlockIn, request: Request, response: Response) -> dict:
    content, answers, index = _require()
    _check_rate(request)
    item = index["extras"].get(body.id)
    if not item:
        raise HTTPException(status_code=404, detail="没有这个附加条目。")

    value = _norm(body.answer)
    allowed = {_norm(item["answer"])}
    allowed.update(_norm(a) for a in item.get("aliases", []))
    allowed.update(_norm(p) for p in item.get("pinyin", []))
    if not value or value not in allowed:
        raise HTTPException(status_code=400, detail="答案不正确，请再试一次。")

    sid = _session_id(request, response)
    _record_unlock(sid, "extra", body.id)

    _, unlocked = _unlocked(sid)
    required = _extra_ids(content)
    answered = [eid for eid in required if eid in unlocked]
    remaining = [eid for eid in required if eid not in unlocked]
    all_done = bool(required) and not remaining
    ranking = {"total": 0, "rank": 0}
    if all_done:
        _record_completion(sid)
        ranking = _ranking(sid)
    return {
        "ok": True,
        "id": body.id,
        "answered": answered,
        "remaining": remaining,
        "all": all_done,
        "ranking": ranking,
        "texts": (
            {eid: _extra_payload(index["extras"][eid], answers["names"]) for eid in required}
            if all_done
            else {}
        ),
    }


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
        "extras": len(content.get("extras", [])),
        "updated": content.get("updated"),
    }
