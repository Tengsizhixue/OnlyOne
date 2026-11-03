# -*- coding: utf-8 -*-
"""把 index 匿名解锁页拆成「公开内容」和「服务端答案」两份数据。

用法（在仓库根目录）：
    python FastAPIProject/tools/build_archive_content.py
    python FastAPIProject/tools/build_archive_content.py --src path/to/index.html

产出：
    FastAPIProject/archive/content.json   公开：结构 + *** + {{pNNN}} 引用
    FastAPIProject/archive/answers.json   服务端：88 个真名 + 附加内容（答案 + AI 总结 + 原文）

附加内容的源是 FastAPIProject/archive/extras.json（手写，改完跑一次脚本即可）。
页面样式不再由本脚本导出，见 aipartner_vue/src/archive/archive.css。
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SRC = ROOT / "FastAPIProject" / "archive" / "source.html"
OUT_CONTENT = ROOT / "FastAPIProject" / "archive" / "content.json"
OUT_ANSWERS = ROOT / "FastAPIProject" / "archive" / "answers.json"
EXTRAS_SRC = ROOT / "FastAPIProject" / "archive" / "extras.json"
ALIASES_SRC = ROOT / "FastAPIProject" / "archive" / "aliases.json"

try:
    from pypinyin import Style, lazy_pinyin
except ImportError as exc:  # 只有构建期需要拼音，服务端读的是算好的结果
    raise SystemExit(
        "缺少 pypinyin，先装一下：FastAPIProject/.venv/Scripts/python.exe -m pip install pypinyin"
    ) from exc


def pinyin_of(value: str) -> str:
    """整串全拼：小写、无音调、无分隔符（"周好东" -> "zhouhaodong"）。"""
    return "".join(lazy_pinyin(value, style=Style.NORMAL, errors="ignore")).lower()


def pinyin_variants(values) -> list[str]:
    out: list[str] = []
    for value in values:
        py = pinyin_of(value)
        if py and py not in out:
            out.append(py)
    return out

REF_SPAN = re.compile(
    r'<span class="anon-name-ref"([^>]*)>.*?</span>', re.S
)
TAG = re.compile(r"<[^>]+>")


def text_of(fragment: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(TAG.sub("", fragment))).strip()


def inner_of(fragment: str, tag: str) -> str:
    m = re.search(rf"<{tag}[^>]*>(.*?)</{tag}>", fragment, re.S)
    return m.group(1) if m else ""


def parse(raw: str):
    # ---------- 样式 ----------
    styles = re.findall(r"<style[^>]*>(.*?)</style>", raw, re.S)
    css = "\n\n".join(s.strip() for s in styles)

    # ---------- 正文结构 ----------
    stages = []
    people_all = []
    for sec in re.finditer(
        r'<section class="col" data-col="([^"]+)" data-stage="([^"]+)">(.*?)</section>',
        raw,
        re.S,
    ):
        col_id, stage_id, body = sec.group(1), sec.group(2), sec.group(3)
        if col_id == "extra":
            continue
        title = text_of(inner_of(body, "h2"))
        groups = []
        gi = 0
        for gm in re.split(r'(?=<div class="group">)', body):
            if not gm.startswith('<div class="group">'):
                continue
            gi += 1
            gm_title = text_of(re.search(r'<span class="cnt-t">(.*?)</span>\s*<span class="cnt-n">', gm, re.S).group(1))
            people = []
            for pm in re.finditer(r'<li class="(p[^"]*)"[^>]*>(.*?)</li>', gm, re.S):
                cls, li = pm.group(1), pm.group(2)
                nm = re.search(r'<span class="p-tx" data-real-name="([^"]*)">', li)
                if not nm:
                    raise SystemExit(f"条目缺少 data-real-name：{li[:80]}")
                name = html.unescape(nm.group(1)).strip()
                quote = re.search(r'<p class="quote[^"]*"[^>]*>(.*?)</p>', li, re.S)
                people.append(
                    {
                        "id": "",
                        "deleted": "is-del" in cls,
                        "name": name,
                        "desc": quote.group(1) if quote else "",
                    }
                )
            groups.append({"id": "", "title": gm_title, "people": people})
        stages.append({"id": stage_id, "title": title, "groups": groups})

    # ---------- 分配稳定 ID ----------
    n = 0
    g = 0
    for stage in stages:
        for group in stage["groups"]:
            g += 1
            group["id"] = f"g{g:02d}"
            for person in group["people"]:
                n += 1
                person["id"] = f"p{n:03d}"
                people_all.append(person)

    by_name = {}
    for p in people_all:
        if p["name"] in by_name:
            raise SystemExit(f"出现重名，无法用名字映射引用：{p['name']}")
        by_name[p["name"]] = p["id"]

    # ---------- 引用 -> {{pNNN}} ----------
    missing = []

    def ref_to_token(match: re.Match) -> str:
        attrs = match.group(1)
        nm = re.search(r'data-real-name="([^"]*)"', attrs)
        if not nm:
            missing.append(attrs[:40])
            return "***"
        name = html.unescape(nm.group(1))
        pid = by_name.get(name)
        if not pid:
            missing.append(name)
            return "***"
        return "{{%s}}" % pid

    for p in people_all:
        p["desc"] = REF_SPAN.sub(ref_to_token, p["desc"])

    # ---------- 附加条目 ----------
    # 附加内容改由 archive/extras.json 单独维护：三篇长文（AI 总结 + 原文）和选择题
    # 都是手写文本，塞回 100KB 的 source.html 里既难改也容易解析错，所以单独放一份。
    if not EXTRAS_SRC.exists():
        raise SystemExit(f"找不到附加内容源文件：{EXTRAS_SRC}")
    spec = json.loads(EXTRAS_SRC.read_text(encoding="utf-8"))
    extra_intro = spec.get("intro", "")

    extras_public = []
    extras_answers = {}
    for item in spec["items"]:
        eid = item["id"]
        extras_public.append({"id": eid, "hint": item["hint"]})
        secret = {
            "answer": item["answer"],
            "aliases": item.get("aliases", []),
            "ai": item["ai"],
            "raw": item["raw"],
        }
        if item.get("choice"):
            secret["choice"] = item["choice"]
        secret["pinyin"] = pinyin_variants([item["answer"], *item.get("aliases", [])])
        extras_answers[eid] = secret

    # ---------- 外号对应的原名（可选） ----------
    alias_map: dict[str, list[str]] = {}
    if ALIASES_SRC.exists():
        raw_alias = json.loads(ALIASES_SRC.read_text(encoding="utf-8"))
        for pid, value in raw_alias.items():
            if pid.startswith("_"):
                continue
            alias_map[pid] = [value] if isinstance(value, str) else list(value)

    # ---------- 组装 ----------
    content = {
        "version": 1,
        "updated": date.today().isoformat(),
        "extraIntro": extra_intro,
        "stages": [
            {
                "id": s["id"],
                "title": s["title"],
                "groups": [
                    {
                        "id": g["id"],
                        "title": g["title"],
                        "people": [
                            {"id": p["id"], "deleted": p["deleted"], "desc": p["desc"]}
                            for p in g["people"]
                        ],
                    }
                    for g in s["groups"]
                ],
            }
            for s in stages
        ],
        "extras": extras_public,
    }
    answers = {
        "names": {p["id"]: p["name"] for p in people_all},
        "aliases": alias_map,
        "pinyin": {
            p["id"]: pinyin_variants([p["name"], *alias_map.get(p["id"], [])])
            for p in people_all
        },
        "extras": extras_answers,
    }
    stats = {
        "people": len(people_all),
        "deleted": sum(1 for p in people_all if p["deleted"]),
        "groups": sum(len(s["groups"]) for s in stages),
        "extras": len(extras_public),
        "tokens": sum(
            len(re.findall(r"\{\{p\d{3}\}\}", p["desc"])) for p in people_all
        )
        + sum(
            len(re.findall(r"\{\{p\d{3}\}\}", e.get("ai", "") + e.get("raw", "")))
            for e in extras_answers.values()
        ),
        "missing_refs": missing,
    }
    return content, answers, css, stats


def validate(content, answers, stats):
    errors = []
    warnings = []
    if not content.get("stages"):
        errors.append("content.json 没有 stages")
    if stats["missing_refs"]:
        errors.append(f"无法解析的引用：{stats['missing_refs']}")

    ids = set(answers["names"])
    refs = set()
    def walk_desc(s):
        refs.update(re.findall(r"\{\{(p\d{3})\}\}", s or ""))
    for st in content["stages"]:
        for g in st["groups"]:
            for p in g["people"]:
                if p["id"] not in ids:
                    errors.append(f"缺少姓名：{p['id']}")
                walk_desc(p["desc"])
    for e in answers["extras"].values():
        walk_desc(e.get("ai", ""))
        walk_desc(e.get("raw", ""))
        walk_desc((e.get("choice") or {}).get("explanation", ""))
    bad = refs - ids
    if bad:
        errors.append(f"引用指向不存在的 ID：{sorted(bad)}")

    # 公开内容里不能出现任何真名
    blob = json.dumps(content, ensure_ascii=False)
    leaked = [n for n in answers["names"].values() if n in blob]
    if leaked:
        errors.append(f"content.json 中出现真名：{leaked}")

    # 外号对应的原名：id 必须存在，且不能和别人的真名撞车
    for pid, alias_list in (answers.get("aliases") or {}).items():
        if pid not in ids:
            errors.append(f"aliases.json 里的 {pid} 不存在")
            continue
        for alias in alias_list:
            owner = [i for i, n in answers["names"].items() if n == alias]
            if owner and owner[0] != pid:
                errors.append(f"{pid} 的别名「{alias}」和 {owner[0]} 的真名重复")
            if alias in blob:
                errors.append(f"别名「{alias}」出现在 content.json 里")

    # 同一阶段里拼音撞车只提示：运行时会把撞车的键丢掉，不会认错人
    for st in content["stages"]:
        seen: dict[str, str] = {}
        for g in st["groups"]:
            for p in g["people"]:
                for py in answers.get("pinyin", {}).get(p["id"], []):
                    if py in seen and seen[py] != p["id"]:
                        warnings.append(
                            f"{st['title']} 里 {p['id']} 和 {seen[py]} 的拼音都是 {py}，两人都无法用拼音解锁"
                        )
                    seen.setdefault(py, p["id"])

    # 只做提示：附加描述里没出现答案名，可能是换成了昵称
    for eid, e in answers["extras"].items():
        plain = re.sub(r"<[^>]+>", "", e.get("ai", ""))
        if e["answer"] not in plain:
            warnings.append(f"{eid} 的 AI 总结里没有答案名 {e['answer']}，确认一下是否取对了块")
    return errors, warnings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default=str(DEFAULT_SRC))
    args = ap.parse_args()
    src = Path(args.src)
    if not src.exists():
        raise SystemExit(f"找不到源文件：{src}")

    raw = src.read_text(encoding="utf-8")
    content, answers, css, stats = parse(raw)
    errors, warnings = validate(content, answers, stats)
    for w in warnings:
        print("提示：", w)
    if errors:
        print("校验失败：", file=sys.stderr)
        for e in errors:
            print("  -", e, file=sys.stderr)
        raise SystemExit(1)

    # 注意：不再从 source.html 导出 CSS。页面的样式（移动端档位、动效、附加题）
    # 已经由 Vue 版手工维护，覆盖回去会把这些改动全部冲掉。
    for p in (OUT_CONTENT, OUT_ANSWERS):
        p.parent.mkdir(parents=True, exist_ok=True)
    OUT_CONTENT.write_text(json.dumps(content, ensure_ascii=False, indent=2), encoding="utf-8")
    OUT_ANSWERS.write_text(json.dumps(answers, ensure_ascii=False, indent=2), encoding="utf-8")

    print("源文件：", src)
    print("人数：", stats["people"], "| 划去：", stats["deleted"], "| 组：", stats["groups"])
    print("附加：", stats["extras"], "| 匿名引用：", stats["tokens"])
    print("content.json：", OUT_CONTENT, len(OUT_CONTENT.read_bytes()), "B")
    print("answers.json：", OUT_ANSWERS, len(OUT_ANSWERS.read_bytes()), "B")


if __name__ == "__main__":
    main()
