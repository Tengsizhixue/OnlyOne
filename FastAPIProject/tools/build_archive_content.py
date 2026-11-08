# -*- coding: utf-8 -*-
"""把 index 匿名解锁页拆成「公开内容」和「服务端答案」两份数据。

用法（在仓库根目录）：
    python FastAPIProject/tools/build_archive_content.py
    python FastAPIProject/tools/build_archive_content.py --src path/to/index.html

产出：
    FastAPIProject/archive/content.json   公开：结构 + *** / {{pNNN}} 引用（附加长文也在这里）
    FastAPIProject/archive/answers.json   服务端：88 个真名、外号、拼音 + 相册答案与图片地址

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
# 纯文字阶段（没有人名、不需要答题），例如「初二到高一」那段三年总结
INTERLUDE_SRC = ROOT / "FastAPIProject" / "archive" / "interlude.json"
PHOTOS_SRC = ROOT / "FastAPIProject" / "archive" / "photos.json"
ALIASES_SRC = ROOT / "FastAPIProject" / "archive" / "aliases.json"

try:
    from pypinyin import Style, lazy_pinyin
except ImportError as exc:  # 只有构建期需要拼音，服务端读的是算好的结果
    raise SystemExit(
        "缺少 pypinyin，先装一下：FastAPIProject/.venv/Scripts/python.exe -m pip install pypinyin"
    ) from exc


def pinyin_of(value: str) -> str:
    """整串全拼：小写、无音调、无分隔符（"张三" -> "zhangsan"）。"""
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

    # ---------- 纯文字阶段 ----------
    # 没有人名、不参与解锁，只是时间线上的一段介绍。单独一份 JSON 维护，
    # 改文案不用碰 source.html；after 指定插在哪一栏后面（id，不是下标）。
    if INTERLUDE_SRC.exists():
        spec_i = json.loads(INTERLUDE_SRC.read_text(encoding="utf-8"))
        after = str(spec_i.get("after", ""))
        pos = next((i for i, s in enumerate(stages) if s["id"] == after), None)
        if pos is None:
            raise SystemExit(f"interlude.json 指定的 after={after} 不存在")
        interlude_id = str(spec_i.get("id", ""))
        if not interlude_id or interlude_id in {s["id"] for s in stages}:
            raise SystemExit(f"interlude.json 的 id 为空或和已有栏重复：{interlude_id}")
        stages.insert(
            pos + 1,
            {
                "id": interlude_id,
                "title": spec_i["title"],
                "groups": [],  # 后端 _build_index 会遍历它，必须存在
                "interlude": {
                    "intro": spec_i.get("intro", ""),
                    "lines": [ln for ln in spec_i.get("lines", []) if ln],
                },
            },
        )

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

    # ---------- 外号对应的原名（可选） ----------
    alias_map: dict[str, list[str]] = {}
    if ALIASES_SRC.exists():
        raw_alias = json.loads(ALIASES_SRC.read_text(encoding="utf-8"))
        for pid, value in raw_alias.items():
            if pid.startswith("_"):
                continue
            alias_map[pid] = [value] if isinstance(value, str) else list(value)

    # ---------- 附加条目 ----------
    # 附加内容由 archive/extras.json 单独维护：三篇长文（AI 总结 + 原文）都是手写文本，
    # 塞回 100KB 的 source.html 里既难改也容易解析错，所以单独放一份。
    if not EXTRAS_SRC.exists():
        raise SystemExit(f"找不到附加内容源文件：{EXTRAS_SRC}")
    spec = json.loads(EXTRAS_SRC.read_text(encoding="utf-8"))
    extra_intro = spec.get("intro", "")
    extra_stage = str(spec.get("stage", "2"))
    if extra_stage not in {s["id"] for s in stages}:
        raise SystemExit(f"extras.json 指定的 stage={extra_stage} 不存在")

    # 附加内容挂在某一栏里，正文里的真名必须在构建期抹掉。
    # 能对应到名单里某个人的称呼写成 {{pNNN}}：前端按「这个人是否已揭示」决定显示真名还是 ***；
    # 对应不到人的（例如 mask 里额外指定、但不在名单上的名字）仍一律换成 ***。
    # 长的先替换，免得短名字先吃掉长名字。
    mask_keys = {p["name"] for p in people_all}
    for value in alias_map.values():
        mask_keys.update(value)
    for item in spec["items"]:
        mask_keys.update(item.get("aliases", []))
    mask_keys.update(spec.get("mask", []))
    mask_keys = sorted((k for k in mask_keys if k), key=len, reverse=True)

    # 名字 / 外号 -> 匿名 ID。只有能对应到名单里某个人的称呼才能写成引用。
    key_to_pid = dict(by_name)
    for pid, alias_list in alias_map.items():
        for alias in alias_list:
            key_to_pid.setdefault(alias, pid)
    for item in spec["items"]:
        owner = by_name.get(item.get("answer", ""))
        if owner:
            for alias in item.get("aliases", []):
                key_to_pid.setdefault(alias, owner)

    def mask_names(text: str, refs: bool = False) -> str:
        for key in mask_keys:
            if key in text:
                pid = key_to_pid.get(key)
                replacement = "{{%s}}" % pid if (refs and pid) else "***"
                text = text.replace(key, replacement)
        return text

    # 附加内容要答对三个问题才显示：题目与答对后的那句说明随 content.json 公开下发，
    # 答案本身不校验（作者本意是「随便答都对，只挡人」），但仍然要过一遍真名遮罩。
    gate = spec.get("gate") or {}
    gate_questions = [mask_names(q) for q in (gate.get("questions") or []) if q]
    gate_note = mask_names(gate.get("note", ""))

    extras_public = [
        {
            "id": item["id"],
            # hint 是纯文本插值、不走 v-html，保持 *** 写法
            "hint": mask_names(item["hint"]),
            # now / ai / raw 用 v-html 渲染，写成引用才能跟着解锁状态变
            # now 是作者现在自己写的看法，排在标签第一位；缺了前端就不显示这个标签
            "now": mask_names(item.get("now", ""), refs=True),
            "ai": mask_names(item["ai"], refs=True),
            # raw 可选：只保留 AI 总结的条目没有原文
            "raw": mask_names(item.get("raw", ""), refs=True),
        }
        for item in spec["items"]
    ]

    # ---------- 相册 ----------
    # 照片同样是「答题才给」的：公开部分只放题面和张数/体积（用来提前提示流量），
    # 答案与图片地址一律进 answers.json，服务端答对了才下发地址。
    photos_public = []
    photos_private = {}
    if PHOTOS_SRC.exists():
        photo_spec = json.loads(PHOTOS_SRC.read_text(encoding="utf-8"))
        for album in photo_spec["albums"]:
            images = [i["src"] for i in album["images"]]
            photos_public.append(
                {
                    "id": album["id"],
                    "title": mask_names(album["title"]),
                    "note": mask_names(album.get("note", "")),
                    "question": mask_names(album["question"]),
                    "count": len(images),
                    "bytes": sum(int(i.get("bytes") or 0) for i in album["images"]),
                    "bytes_min": min(
                        (int(i.get("bytes") or 0) for i in album["images"] if i.get("bytes")),
                        default=0,
                    ),
                    "bytes_max": max(
                        (int(i.get("bytes") or 0) for i in album["images"]), default=0
                    ),
                    # 缩略图总量（Cloudflare /cdn-cgi/image/ 实测），用来提示首屏流量
                    "thumb_bytes": int(album.get("thumb_bytes") or 0),
                }
            )
            photos_private[album["id"]] = {
                "answers": [a for a in album["answers"] if a],
                # 答案也接受拼音输入（跟阶段解锁一致），这里预算好整串全拼
                "pinyin": sorted(
                    {
                        py
                        for a in album["answers"]
                        if a
                        for py in pinyin_variants([a])
                    }
                ),
                "images": images,
            }

    # ---------- 组装 ----------
    content = {
        "version": 1,
        "updated": date.today().isoformat(),
        "stages": [
            # 纯文字阶段：只有标题和一段介绍，没有人名、没有答题框。
            # 文本也要过一次真名遮罩，保证公开内容里不出现任何真名。
            {
                "id": s["id"],
                "title": s["title"],
                "groups": [],
                "intro": mask_names(s["interlude"]["intro"]),
                "lines": [mask_names(x) for x in s["interlude"]["lines"]],
            }
            if s.get("interlude")
            else {
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
                # 附加内容挂在它所属的那一栏里，答题（三题都填）之后才展示条目
                **(
                    {
                        "extras": {
                            "intro": extra_intro,
                            "gate": {"questions": gate_questions, "note": gate_note},
                            "items": extras_public,
                        }
                    }
                    if s["id"] == extra_stage
                    else {}
                ),
            }
            for s in stages
        ],
        # 相册横跨「高中」和「高中以前」，不挂在某一栏里，所以放顶层
        **({"photos": {"albums": photos_public}} if photos_public else {}),
    }
    answers = {
        "names": {p["id"]: p["name"] for p in people_all},
        "aliases": alias_map,
        "pinyin": {
            p["id"]: pinyin_variants([p["name"], *alias_map.get(p["id"], [])])
            for p in people_all
        },
        **({"photos": photos_private} if photos_private else {}),
    }
    stats = {
        "people": len(people_all),
        "deleted": sum(1 for p in people_all if p["deleted"]),
        "groups": sum(len(s["groups"]) for s in stages),
        "extras": len(extras_public),
        "albums": len(photos_public),
        "photos": sum(a["count"] for a in photos_public),
        "tokens": sum(
            len(re.findall(r"\{\{p\d{3}\}\}", p["desc"])) for p in people_all
        ),
        "missing_refs": missing,
    }
    return content, answers, stats


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
        # 纯文字阶段只许有介绍，不许混进名单
        if st.get("lines"):
            if st.get("groups"):
                errors.append(f"{st['title']} 是纯文字阶段，不该有人名分组")
            if not st.get("intro") or not all(st["lines"]):
                errors.append(f"{st['title']} 的介绍文字不完整")
        for g in st["groups"]:
            for p in g["people"]:
                if p["id"] not in ids:
                    errors.append(f"缺少姓名：{p['id']}")
                walk_desc(p["desc"])
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

    # 附加内容：答题后才展示的公开长文，题目与结构要完整。
    # 正文里的名字是 {{pNNN}} 引用，前端按解锁状态填真名或 ***；只许这种格式，且 ID 必须存在。
    for st in content["stages"]:
        extras = st.get("extras")
        if not extras:
            continue
        if not extras.get("items"):
            errors.append(f"{st['title']} 的附加内容没有条目")
        gate = extras.get("gate") or {}
        if not gate.get("questions"):
            errors.append(f"{st['title']} 的附加内容缺少题目")
        elif len(gate["questions"]) != 3:
            errors.append(f"{st['title']} 的附加内容应为 3 个问题，实际 {len(gate['questions'])} 个")
        if not gate.get("note"):
            errors.append(f"{st['title']} 的附加内容缺少答对后的说明")
        for item in extras.get("items", []):
            if not item.get("id") or not item.get("hint"):
                errors.append("附加条目缺少 id 或 hint")
            if not item.get("ai"):
                errors.append(f"附加条目 {item.get('id')} 缺少 AI 总结")
            for field in ("hint", "now", "ai", "raw"):
                text = item.get(field) or ""
                for token in re.findall(r"\{\{([^{}]*)\}\}", text):
                    if not re.fullmatch(r"p\d{3}", token):
                        errors.append(
                            f"附加条目 {item.get('id')} 的 {field} 里有未替换的引用：{token}"
                        )
                unknown = set(re.findall(r"\{\{(p\d{3})\}\}", text)) - ids
                if unknown:
                    errors.append(
                        f"附加条目 {item.get('id')} 的 {field} 引用了不存在的 ID：{sorted(unknown)}"
                    )

    # 相册：公开只许有题面/张数/体积，答案与图片地址必须在 answers.json
    albums = (content.get("photos") or {}).get("albums") or []
    priv = answers.get("photos") or {}
    seen_albums: set[str] = set()
    for album in albums:
        aid = album.get("id")
        if not aid:
            errors.append("相册缺少 id")
            continue
        if aid in seen_albums:
            errors.append(f"相册 id 重复：{aid}")
        seen_albums.add(aid)
        if not album.get("question"):
            errors.append(f"相册 {aid} 缺少题目")
        if not album.get("count"):
            errors.append(f"相册 {aid} 没有图片")
        if not (album.get("bytes") or 0) > 0:
            errors.append(f"相册 {aid} 的总字节数为 0（先跑 fetch_photos.py）")
        private = priv.get(aid)
        if not private:
            errors.append(f"相册 {aid} 在 answers.json 里没有答案")
            continue
        if not private.get("answers"):
            errors.append(f"相册 {aid} 的答案为空")
        if len(private.get("images") or []) != album.get("count"):
            errors.append(f"相册 {aid} 的图片数与 count 对不上")
        for answer in private.get("answers") or []:
            if answer in blob:
                errors.append(f"相册 {aid} 的答案「{answer}」出现在 content.json 里")
    extra_priv = set(priv) - seen_albums
    if extra_priv:
        errors.append(f"answers.json 里有 content.json 不存在的相册：{sorted(extra_priv)}")
    return errors, warnings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default=str(DEFAULT_SRC))
    args = ap.parse_args()
    src = Path(args.src)
    if not src.exists():
        raise SystemExit(f"找不到源文件：{src}")

    raw = src.read_text(encoding="utf-8")
    content, answers, stats = parse(raw)
    errors, warnings = validate(content, answers, stats)
    for w in warnings:
        print("提示：", w)
    if errors:
        print("校验失败：", file=sys.stderr)
        for e in errors:
            print("  -", e, file=sys.stderr)
        raise SystemExit(1)

    # 本脚本只产出两份 JSON；页面样式在 aipartner_vue/src/archive/archive.css 手工维护。
    for p in (OUT_CONTENT, OUT_ANSWERS):
        p.parent.mkdir(parents=True, exist_ok=True)
    OUT_CONTENT.write_text(json.dumps(content, ensure_ascii=False, indent=2), encoding="utf-8")
    OUT_ANSWERS.write_text(json.dumps(answers, ensure_ascii=False, indent=2), encoding="utf-8")

    print("源文件：", src)
    print("人数：", stats["people"], "| 划去：", stats["deleted"], "| 组：", stats["groups"])
    print("附加：", stats["extras"], "| 匿名引用：", stats["tokens"])
    if stats["albums"]:
        print("相册：", stats["albums"], "个 /", stats["photos"], "张")
    print("content.json：", OUT_CONTENT, len(OUT_CONTENT.read_bytes()), "B")
    print("answers.json：", OUT_ANSWERS, len(OUT_ANSWERS.read_bytes()), "B")


if __name__ == "__main__":
    main()
