"""把 archive/x2_ai.html 写进 archive/extras.json 的 x2 条目。

为什么单独留一个 .html：某同学那篇分析有一万多字，塞在 extras.json 的 JSON 字符串里
改一句话都很痛苦，而且容易漏转义。改正文就改 x2_ai.html，然后跑：

    ./.venv/Scripts/python.exe tools/inject_x2.py
    ./.venv/Scripts/python.exe tools/build_archive_content.py

注意：extras.json 才是构建脚本的输入，x2_ai.html 只是它的编辑源，两边不要各改一半。
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXTRAS = ROOT / "FastAPIProject" / "archive" / "extras.json"
SOURCE = ROOT / "FastAPIProject" / "archive" / "x2_ai.html"


def main() -> None:
    if not SOURCE.exists():
        raise SystemExit(f"找不到编辑源：{SOURCE}")
    html = SOURCE.read_text(encoding="utf-8").strip()
    spec = json.loads(EXTRAS.read_text(encoding="utf-8"))
    for item in spec["items"]:
        if item["id"] == "x2":
            item["ai"] = html
            item["raw"] = ""
            break
    else:
        raise SystemExit("extras.json 里没有 x2 条目")
    EXTRAS.write_text(json.dumps(spec, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"已写入 x2：{len(html)} 字符")


if __name__ == "__main__":
    main()
