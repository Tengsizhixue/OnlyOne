# -*- coding: utf-8 -*-
"""把「现在的看法」写进 archive/extras.json 的 now 字段（幂等，可反复跑）。

只改 now，不碰 ai / raw / hint / answer / aliases。
改完记得跑一次 build_archive_content.py 重新生成 content.json。
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXTRAS = ROOT / "FastAPIProject" / "archive" / "extras.json"

NOW = {
    "x2": (
        "<p>之前的原文找不到了，这GPT总结扯的实在太多，我自己都懒得看，你要愿意看，"
        "反正我放进去了。我现在是没什么好评价的，都2027年了，懒得扯淡，我看了几句AI说的"
        "实在太尴尬了，我能复制粘贴已经很好了。现在有时候出去和高中同学聊聊天，"
        "还有人向我打听她情况的，我都有点想笑，我应该是最没有可能知道她情况的吧，"
        "我是学计算机的，又不是干黑客的。</p>"
    ),
    "x1": (
        "<p>不知道说啥，都是以前的事了，我只能说在我的整个高中印象特别好的人中，"
        "除了***应该没人会在面前表示喜欢他吧，我一直都是明着说他坏话，和我讨论他，"
        "那我只能表达我最纯真的厌恶，***还问我之前他过生日要送些什么，我想了很久还是送了"
        "五分钟的短信轰炸，可惜他应该是苹果手机效果不明显，不过都是搞着玩的了，"
        "这么多年也没接触，哪有以前那么讨厌，就是聊到高中当谈资而已。</p>"
    ),
    "x3": "<p>额，二审维持原判，直接看原文吧。</p>",
}


def main() -> None:
    spec = json.loads(EXTRAS.read_text(encoding="utf-8"))
    seen = set()
    for item in spec["items"]:
        iid = item["id"]
        if iid not in NOW:
            raise SystemExit(f"extras.json 里的 {iid} 没有对应的「现在的看法」文本")
        item["now"] = NOW[iid]
        seen.add(iid)
    unknown = set(NOW) - seen
    if unknown:
        raise SystemExit(f"「现在的看法」里有 extras.json 不存在的 id：{sorted(unknown)}")

    EXTRAS.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("extras.json 已写入 now：", [i["id"] for i in spec["items"]])
    for item in spec["items"]:
        print(f"  {item['id']}: now {len(item['now'])}B | ai {len(item['ai'])}B | raw {len(item['raw'])}B")


if __name__ == "__main__":
    main()
