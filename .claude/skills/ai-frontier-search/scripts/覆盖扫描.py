#!/usr/bin/env python3
"""跨论文覆盖扫描：在本地正文中检查若干条件是否出现，只输出命中矩阵，全文不进上下文。

用法：python -X utf8 覆盖扫描.py <正文目录> [--title 标题正则] 列名=正则 [列名=正则 ...]
有章节结构时扫描完整章节（跳过参考文献）；只有截断正文的条目在"截断"列标出。
零命中只表示所存正文里没有这些词，可能换了术语，不等于论文未涉及。
"""

import argparse
import json
import re
import sys
from pathlib import Path

SKIP = re.compile(r"^(\d+\s*)?(References|Bibliography|Acknowledg)", re.I)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("text_dir")
    parser.add_argument("--title", help="只扫描标题匹配该正则的论文")
    parser.add_argument("columns", nargs="+", help="列名=正则")
    args = parser.parse_args()
    try:
        title_rx = re.compile(args.title, re.I) if args.title else None
        cols = [(name, re.compile(rx, re.I)) for name, rx in (c.split("=", 1) for c in args.columns)]
    except (ValueError, re.error) as exc:
        parser.error(f"列需写成 列名=正则，且正则有效：{exc}")

    rows, totals = [], [0] * len(cols)
    for path in sorted(Path(args.text_dir).glob("*正文.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        paper = data.get("paper") or {}
        title = paper.get("title") or ""
        if title_rx and not title_rx.search(title):
            continue
        sections = paper.get("sections")
        if sections:
            text = " ".join(s["text"] for s in sections if not SKIP.search(s["heading"] or ""))
            truncated = ""
        else:
            text = data.get("text", "")
            truncated = "是" if data.get("text_truncated") else ""
        marks = []
        for k, (_, rx) in enumerate(cols):
            hit = bool(rx.search(text))
            totals[k] += hit
            marks.append("●" if hit else "·")
        rows.append(f"{path.name.split('正文')[0]}\t{truncated}\t" + "\t".join(marks) + f"\t{title[:50]}")

    print("论文\t截断\t" + "\t".join(name for name, _ in cols) + "\t标题")
    print("\n".join(rows))
    print(f"合计 {len(rows)} 篇\t\t" + "\t".join(map(str, totals)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
