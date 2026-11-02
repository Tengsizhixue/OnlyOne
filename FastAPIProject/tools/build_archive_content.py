# -*- coding: utf-8 -*-
"""把 index 匿名解锁页拆成「公开内容」和「服务端答案」两份数据。

用法（在仓库根目录）：
    python FastAPIProject/tools/build_archive_content.py
    python FastAPIProject/tools/build_archive_content.py --src path/to/index.html

产出：
    FastAPIProject/archive/content.json   公开：结构 + *** + {{pNNN}} 引用
    FastAPIProject/archive/answers.json   服务端：88 个真名 + 6 个答案 + 6 篇长文
    aipartner_vue/src/archive/archive.css 页面样式（从 HTML 的 <style> 原样搬出）
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
OUT_CSS = ROOT / "aipartner_vue" / "src" / "archive" / "archive.css"

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
    extra_intro = ""
    m = re.search(r'<p class="extra-intro">(.*?)</p>', raw, re.S)
    if m:
        extra_intro = text_of(m.group(1))

    extras_public = []
    extras_answers = {}
    ei = 0
    for em in re.finditer(
        r'<div class="extra-item" data-answer="([^"]*)">(.*?)(?=<div class="extra-item"|</section>)',
        raw,
        re.S,
    ):
        answer, body = em.group(1), em.group(2)
        ei += 1
        eid = f"e{ei}"
        hint = text_of(inner_of(body, "p"))
        dm = re.search(
            r'<div class="extra-description"[^>]*>(.*?)</div>\s*<button[^>]*extra-toggle',
            body,
            re.S,
        )
        if not dm:
            raise SystemExit(f"附加条目 {eid} 找不到描述")
        desc = REF_SPAN.sub(ref_to_token, dm.group(1))
        extras_public.append({"id": eid, "hint": hint})
        extras_answers[eid] = {
            "answer": html.unescape(answer).strip(),
            "aliases": [],
            "description": desc,
        }

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
            len(re.findall(r"\{\{p\d{3}\}\}", e["description"]))
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
        walk_desc(e["description"])
    bad = refs - ids
    if bad:
        errors.append(f"引用指向不存在的 ID：{sorted(bad)}")

    # 公开内容里不能出现任何真名
    blob = json.dumps(content, ensure_ascii=False)
    leaked = [n for n in answers["names"].values() if n in blob]
    if leaked:
        errors.append(f"content.json 中出现真名：{leaked}")

    # 只做提示：附加描述里没出现答案名，可能是换成了昵称
    for eid, e in answers["extras"].items():
        if e["answer"] not in re.sub(r"<[^>]+>", "", e["description"]):
            warnings.append(f"{eid} 的描述里没有答案名 {e['answer']}，确认一下是否取对了块")
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

    # 只读页面的收尾样式：去掉编辑态的 hover / 占位文案
    css += """

/* ---------- 只读页面：去掉编辑态残留 ---------- */
.col-title:hover,.col-title:focus,
.p-tx:hover,.p-tx:focus,
.quote:hover,.quote:focus{background:none;box-shadow:none}
.quote:empty::before{content:none}
[v-cloak]{display:none}
.archive-status{min-height:60vh;display:flex;align-items:center;justify-content:center;
  color:#8996a6;font-size:13px;letter-spacing:.08em;text-align:center;padding:0 24px}
.archive-status.error{color:#c9a0a0}
"""

    for p in (OUT_CONTENT, OUT_ANSWERS, OUT_CSS):
        p.parent.mkdir(parents=True, exist_ok=True)
    OUT_CONTENT.write_text(json.dumps(content, ensure_ascii=False, indent=2), encoding="utf-8")
    OUT_ANSWERS.write_text(json.dumps(answers, ensure_ascii=False, indent=2), encoding="utf-8")
    OUT_CSS.write_text(css.strip() + "\n", encoding="utf-8")

    print("源文件：", src)
    print("人数：", stats["people"], "| 划去：", stats["deleted"], "| 组：", stats["groups"])
    print("附加：", stats["extras"], "| 匿名引用：", stats["tokens"])
    print("content.json：", OUT_CONTENT, len(OUT_CONTENT.read_bytes()), "B")
    print("answers.json：", OUT_ANSWERS, len(OUT_ANSWERS.read_bytes()), "B")
    print("archive.css：", OUT_CSS, len(OUT_CSS.read_bytes()), "B")


if __name__ == "__main__":
    main()
