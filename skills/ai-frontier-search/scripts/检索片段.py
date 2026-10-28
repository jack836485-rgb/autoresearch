#!/usr/bin/env python3
"""在本地已保存的论文正文中检索短片段，只把命中片段返回给模型。

输入为 读取研究页.py／批量读取论文.py 保存的正文 JSON，或本地 PDF（依赖 pymupdf）。
全文留在本地；每篇累计返回字符数记录在同目录的 阅读记录.json，达到预算即停止返回。
"""

import argparse
import json
import re
import sys
from pathlib import Path

DEFAULT_BUDGET = 5000
DEEP_BUDGET = 12000
LOG_NAME = "阅读记录.json"


def pdf_sections(source):
    import pymupdf

    with pymupdf.open(source) as doc:
        pages = [" ".join(page.get_text().split()) for page in doc]
        toc = [(level, title, page) for level, title, page in doc.get_toc() if 1 <= page <= len(pages)]
    if not toc:
        return [{"id": f"p{index}", "heading": f"第 {index} 页", "level": 1, "text": text} for index, text in enumerate(pages, start=1)]

    # 拼接全文，按目录标题在其所在页中的位置切分。
    starts, full = [], ""
    for text in pages:
        starts.append(len(full))
        full += text + " "
    lower = full.lower()
    cuts = []
    for level, title, page in toc:
        previous = cuts[-1][3] if cuts else 0
        floor = max(starts[page - 1], previous)
        page_end = starts[page] if page < len(pages) else len(full)
        position = -1
        for candidate in (title, re.sub(r"^[\dA-Z]+(\.\d+)*\.?\s+", "", title)):
            candidate = " ".join(candidate.split()).lower()
            if candidate:
                position = lower.find(candidate, floor, page_end + len(candidate))
                if position >= 0:
                    break
        if position >= 0:
            # 正文编号写法可能与目录不同（"2." 对 "2"），把紧邻的编号并入本节。
            number = re.search(r"(?:^|\s)([\dA-Z]+(?:\.\d+)*\.?)\s$", full[max(floor, position - 12):position])
            if number:
                position -= len(number.group(0)) - (1 if number.group(0)[0].isspace() else 0)
        elif starts[page - 1] > previous:
            position = starts[page - 1]
        else:
            continue  # 同页找不到标题，并入上一节，不抢占上一节的正文
        cuts.append((level, title, page, max(position, floor)))
    sections = []
    if cuts and cuts[0][3] > 0:
        sections.append({"id": "front", "heading": "目录前内容（p.1）", "level": 1, "text": full[:cuts[0][3]].strip()})
    for index, (level, title, page, start) in enumerate(cuts):
        end = cuts[index + 1][3] if index + 1 < len(cuts) else len(full)
        text = full[start:end].strip()
        if text:
            sections.append({"id": f"toc{index}", "heading": f"{title}（p.{page}）", "level": level, "text": text})
    return sections


def load_sections(source):
    if source.suffix.lower() == ".pdf":
        return pdf_sections(source)
    data = json.loads(source.read_text(encoding="utf-8"))
    if (data.get("paper") or {}).get("sections"):
        return data["paper"]["sections"]
    # 旧缓存没有章节结构，退回整段正文。
    note = "（正文已截断）" if data.get("text_truncated") else ""
    return [{"id": "text", "heading": f"全文，无章节结构{note}", "level": 1, "text": data.get("text", "")}]


def find_hits(sections, pattern, context):
    hits = []
    for section in sections:
        text = section["text"]
        spans = []
        for match in pattern.finditer(text):
            start, end = max(0, match.start() - context), min(len(text), match.end() + context)
            if spans and start <= spans[-1][1]:
                spans[-1][1] = end
            else:
                spans.append([start, end])
        hits.extend((section, text[start:end]) for start, end in spans)
    return hits


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", nargs="?", help="正文 JSON 或 PDF")
    parser.add_argument("--list-sections", action="store_true", help="只列章节标题与长度")
    parser.add_argument("--depth", type=int, default=1, help="--list-sections 列出的最深层级")
    parser.add_argument("--query", help="不区分大小写的正则，如 'limitation|fail|does not generalize'")
    parser.add_argument("--section", help="只在标题匹配该正则的章节内检索；不带 --query 时返回整节（受预算限制）")
    parser.add_argument("--exclude-section", default=r"^(\d+\s*)?(References|Bibliography|Related Work|Acknowledg)",
                        help="跳过标题匹配该正则的章节；找实验细节时可加入 Introduction|Abstract")
    parser.add_argument("--context", type=int, default=200, help="命中前后保留的字符数")
    parser.add_argument("--max-hits", type=int, default=3)
    parser.add_argument("--budget", type=int, default=DEFAULT_BUDGET, help=f"本篇累计返回字符上限；Tier A 用 {DEEP_BUDGET}")
    parser.add_argument("--reason", help="超过默认预算或读取整节时必填，写入阅读记录")
    parser.add_argument("--summary", metavar="目录", help="汇总该目录阅读记录后退出")
    args = parser.parse_args()

    if args.summary:
        log = json.loads((Path(args.summary) / LOG_NAME).read_text(encoding="utf-8"))
        for name, entry in log.items():
            reasons = "；".join(call["reason"] for call in entry["calls"] if call.get("reason"))
            print(f"{name}\t{entry['returned_chars']} 字符\t{len(entry['calls'])} 次\t{reasons}")
        return 0
    if not args.source or not (args.list_sections or args.query or args.section):
        parser.error("需要 source，以及 --list-sections、--query 或 --section 之一")
    if args.context < 0 or args.max_hits < 1 or args.budget < 1:
        parser.error("context 不能为负，max-hits 和 budget 必须大于零")
    reading_whole_section = args.section and not args.query and not args.list_sections
    if (args.budget > DEFAULT_BUDGET or reading_whole_section) and not args.reason:
        parser.error("超过默认预算或读取整节时需用 --reason 写明要回答的具体问题")
    try:
        query = re.compile(args.query, re.I) if args.query else None
        section_filter = re.compile(args.section, re.I) if args.section else None
        exclude = re.compile(args.exclude_section, re.I) if args.exclude_section else None
    except re.error as exc:
        parser.error(f"正则无效：{exc}")

    source = Path(args.source)
    sections = load_sections(source)
    if section_filter:
        sections = [s for s in sections if section_filter.search(s["heading"])]
    if exclude and not args.list_sections:
        sections = [s for s in sections if not exclude.search(s["heading"])]
    total_chars = sum(len(s["text"]) for s in sections)

    if args.list_sections:
        listed = [s for s in sections if s.get("level", 1) <= args.depth]
        blocks = [f"{s['heading']}（{len(s['text'])} 字符）" for s in listed]
        header = f"共 {len(sections)} 节，列出 {len(listed)} 节（层级 ≤{args.depth}）"
    elif query:
        hits = find_hits(sections, query, args.context)
        blocks = [f"--- §{s['heading']}\n{snippet}" for s, snippet in hits[:args.max_hits]]
        header = f"命中 {len(hits)} 处，返回 {len(blocks)} 处（检索范围 {total_chars} 字符）"
    else:
        blocks = [f"--- §{s['heading']}\n{s['text']}" for s in sections]
        header = f"匹配 {len(sections)} 节"

    log_path = source.parent / LOG_NAME
    log = json.loads(log_path.read_text(encoding="utf-8")) if log_path.exists() else {}
    entry = log.setdefault(source.name, {"returned_chars": 0, "calls": []})
    remaining = args.budget - entry["returned_chars"]
    body = "\n".join(blocks)
    if remaining <= 0:
        print(f"[{source.name}] 预算已用尽（{entry['returned_chars']}/{args.budget}）；确需继续请提高 --budget 并写 --reason")
        return 2
    if len(body) > remaining:
        body = body[:remaining] + "\n…（达到预算，后续内容未返回）"
    returned = min(len(body), remaining)
    entry["returned_chars"] += returned
    entry["calls"].append({
        "query": args.query, "section": args.section, "chars": returned, "budget": args.budget, "reason": args.reason,
    })
    log_path.write_text(json.dumps(log, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{source.name}] {header}；本篇累计 {entry['returned_chars']}/{args.budget} 字符")
    if body:
        print(body)
    return 0


if __name__ == "__main__":
    sys.exit(main())
