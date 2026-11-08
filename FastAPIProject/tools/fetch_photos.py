# -*- coding: utf-8 -*-
"""生成 archive/photos.json：相册元信息 + 图片地址 + 每张真实字节数。

为什么单独跑：流量提示要显示「答对后大概会消耗多少流量」，这个数字必须来自
图床的真实 Content-Length，不能拍脑袋估。图床加了就重跑一次，其余流程不变。

用法（在仓库根目录）：
    FastAPIProject/.venv/Scripts/python.exe FastAPIProject/tools/fetch_photos.py

产出：
    FastAPIProject/archive/photos.json   私有（.gitignore 里 *.json 已经忽略），
                                         含答案与图片地址，只上传到服务器，不进仓库。
"""

from __future__ import annotations

import json
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "FastAPIProject" / "archive" / "photos.json"

HOST = "https://photo.160615.xyz/School"
# 必须和 archive_api.py 的 THUMB_PREFIX 保持一致，否则流量提示和首屏实际加载对不上
THUMB_PREFIX = "/cdn-cgi/image/width=320,quality=72,format=auto,onerror=redirect/"

HS_FILES = [
    "HS/a967b26638962995e0e355a0c6ecf734.jpg",
    "HS/b343514f8315c715fb1e73f50aaad864.jpg",
    "HS/bcb1569f59c795ca22ad27eb99c215bb.jpg",
    "HS/11de5aa7be2744f572812f2f33a941a6.jpg",
    "HS/46a78690b08c96827f83d9d27a4fa6f0.jpg",
    "HS/51c5cbbc5a3cc76c59e33632c36e2c37.jpg",
    "HS/63144c07e3564f91e868a8e101f1cafc.jpg",
    "HS/8b1cb1d9be8753f491b903f410e4816b.jpg",
    "HS/935ABD7CE31705E11F0B52DA4ABB7412.png",
    "HS/935abd7ce31705e11f0b52da4abb7412.png",
    "HS/IMG20211127151612.jpg",
    "HS/IMG20211231154818.jpg",
    "HS/IMG20211231154907.jpg",
    "HS/IMG20211231154945.jpg",
    "HS/IMG20211231160145.jpg",
    "HS/IMG20211231160429.jpg",
    "HS/IMG20211231160732.jpg",
    "HS/IMG20211231160944.jpg",
    "HS/IMG20211231162102.jpg",
    "HS/IMG20211231163728.jpg",
    "HS/IMG20211231164636.jpg",
    "HS/IMG20220308120735.jpg",
    "HS/IMG20220308120841.jpg",
    "HS/IMG20220308120848.jpg",
    "HS/IMG20220312202822.jpg",
    "HS/IMG20220312202828.jpg",
    "HS/IMG20220326184353.jpg",
    "HS/IMG20220507143106.jpg",
    "HS/IMG20220507143109.jpg",
    "HS/IMG20230327071630.jpg",
    "HS/IMG20230327074904.jpg",
    "HS/IMG20230327083901.jpg",
    "HS/IMG20230327091835.jpg",
    "HS/IMG20230327091944.jpg",
    "HS/IMG20230327091953.jpg",
    "HS/IMG20230331134450.jpg",
    "HS/IMG20230526183805.jpg",
    "HS/IMG20230529172052.jpg",
    "HS/IMG_20261014_214832.jpg",
    "HS/VID20230602110340%20-%20frame%20at%208m24s.jpg",
    "HS/VID_20201231_154913%20-%20frame%20at%201m2s.jpg",
    "HS/b3e81e12b4ef050fe9319352382fec66.jpg",
    "HS/e23c5955ed6240388cbf23aa4e0e8e53.jpg",
    "HS/IMG_20240928_152935.jpg",
]

PH_FILES = [
    "PH/IMG20220812181712.jpg",
    "PH/IMG20220813134751.jpg",
    "PH/IMG20220813163011.jpg",
    "PH/IMG20220813221654.jpg",
    "PH/IMG_20240922_003557.jpg",
    "PH/IMG_20241115_233157.jpg",
    "PH/Screenshot_2026-07-02-17-00-18-68_2332cb9b27b851.jpg",
    "PH/VID20220131220926%20-%20frame%20at%200m17s.jpg",
    "PH/VID20220802062607%20-%20frame%20at%200m6s.jpg",
    "PH/VID20230501202012%20-%20frame%20at%200m1s.jpg",
    "PH/mmexport1726943862243.jpg",
    "PH/mmexport1781338488090.jpg",
    "PH/mmexport1782063464466.jpg",
    "PH/mmexport1783134146056.jpg",
    "PH/mmexport1783134284671.jpg",
]

ALBUMS = [
    {
        "id": "hs",
        "title": "高中相关",
        "note": "高中能留下这么多照片，真的完全是运气了，原本早就被我删了，大三在老家一张储存卡里找到了很多",
        "question": "高中时对我最好的老师是谁？",
        "answers": ["江雪兵"],
        "files": HS_FILES,
    },
    {
        "id": "ph",
        "title": "高中以前相关",
        "note": "高中以前没多少照片能留下来，这应该是我能够找到的所有了，以前不喜欢拍照，而且实在是太久了。",
        "question": "小学时对我最好的老师是谁？",
        "answers": ["徐来树", "徐璞"],
        "files": PH_FILES,
    },
]


def head(url: str, attempts: int = 3) -> tuple[str, int, int]:
    """HEAD 取字节数。图床偶尔会卡住，重试几次再报错。"""
    last: Exception | None = None
    for i in range(attempts):
        req = urllib.request.Request(
            url, method="HEAD", headers={"User-Agent": "archive-build/1.0"}
        )
        try:
            with urllib.request.urlopen(req, timeout=40) as resp:
                return url, resp.status, int(resp.headers.get("Content-Length") or 0)
        except (urllib.error.URLError, OSError) as exc:
            last = exc
            time.sleep(1.5 * (i + 1))
    raise last  # type: ignore[misc]


def thumb_url(src: str) -> str:
    """原图地址 → 缩略图地址（规则同 archive_api._thumb）。"""
    host, sep, path = src[len("https://"):].partition("/")
    if not sep or not path:
        return ""
    return f"https://{host}{THUMB_PREFIX}{path}"


def head_soft(url: str) -> int:
    """缩略图取不到不算致命错误：返回 0，调用处回落到原图字节。"""
    if not url:
        return 0
    try:
        return head(url)[2]
    except (urllib.error.URLError, OSError):
        return 0


def main() -> None:
    jobs = [f"{HOST}/{rel}" for alb in ALBUMS for rel in alb["files"]]
    with ThreadPoolExecutor(max_workers=6) as pool:
        results = list(pool.map(head, jobs))
    size = {url: (status, length) for url, status, length in results}

    bad = [(u, s) for u, (s, _) in size.items() if s != 200]
    if bad:
        print("有图片取不到，先修名单：", file=sys.stderr)
        for u, s in bad:
            print(f"  {s}  {u}", file=sys.stderr)
        raise SystemExit(1)

    albums = []
    seen: dict[str, str] = {}
    for spec in ALBUMS:
        images = []
        for rel in spec["files"]:
            url = f"{HOST}/{rel}"
            key = rel.lower()          # 935ABD… 与 935abd… 是同一张，只留一张
            if key in seen:
                print(f"  跳过重复：{rel}（同 {seen[key]}）")
                continue
            seen[key] = rel
            images.append({"src": url, "bytes": size[url][1]})
        albums.append(
            {
                "id": spec["id"],
                "title": spec["title"],
                "note": spec["note"],
                "question": spec["question"],
                "answers": spec["answers"],
                "thumb_bytes": 0,  # 下面按去重后的图片算出来再填
                "images": images,
            }
        )

    # 缩略图总量：首屏网格实际会加载的字节数。单张取不到就按原图算，
    # 和 Cloudflare onerror=redirect 的行为保持一致。
    flat = [img for alb in albums for img in alb["images"]]
    with ThreadPoolExecutor(max_workers=6) as pool:
        thumbs = list(pool.map(head_soft, [thumb_url(img["src"]) for img in flat]))
    cursor = 0
    for alb in albums:
        total = 0
        for img in alb["images"]:
            total += thumbs[cursor] or img["bytes"]
            cursor += 1
        alb["thumb_bytes"] = total

    OUT.write_text(
        json.dumps({"albums": albums}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    print("写出：", OUT, OUT.stat().st_size, "B")
    for alb in albums:
        total = sum(i["bytes"] for i in alb["images"])
        biggest = max((i["bytes"] for i in alb["images"]), default=0)
        print(
            f"  {alb['id']}: {len(alb['images'])} 张 / {total / 1048576:.2f} MB"
            f" / 单张最大 {biggest / 1024:.0f} KB"
            f" / 缩略图合计 {alb['thumb_bytes'] / 1024:.0f} KB"
        )


if __name__ == "__main__":
    main()
