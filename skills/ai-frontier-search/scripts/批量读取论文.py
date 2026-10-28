#!/usr/bin/env python3
"""顺序读取已发现的 arXiv 候选，逐篇保存原始检索信息，供人工核实。

输入为 JSON 数组，条目可以是 arXiv ID 字符串或包含 id 的对象。
不判断机构资格、主题资格或质量；已有成功记录直接复用。
"""

import argparse
import importlib.util
import json
import re
import sys
import time
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ids_file", help="候选 arXiv ID 的 JSON 数组文件")
    parser.add_argument("--output-dir", required=True, help="本轮独立结果目录")
    parser.add_argument("--start", type=int, default=0, help="从队列第几个条目开始，零起算")
    parser.add_argument("--limit", type=int, default=20, help="本批读取数量")
    parser.add_argument("--delay", type=float, default=3, help="相邻请求间隔秒数")
    parser.add_argument("--max-chars", type=int, default=70000, help="每篇保留的正文长度；综合模型报告可能需要增大")
    parser.add_argument("--version", type=int, default=1, help="未明确版本的 ID 默认读取此版本；核实首发使用 1，精读更新可指定其他版本")
    parser.add_argument("--abstract", action="store_true", help="stdout 附带摘要（≤1600 字符）；只对标题筛选后的候选使用")
    args = parser.parse_args()
    if args.start < 0 or args.limit < 1 or args.delay < 0 or args.max_chars < 1 or args.version < 1:
        parser.error("起始位置和间隔不能为负，数量和正文长度必须大于零")
    source = Path(__file__).with_name("读取研究页.py")
    spec = importlib.util.spec_from_file_location("research_page_reader", source)
    reader = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(reader)
    queue = json.loads(Path(args.ids_file).read_text(encoding="utf-8-sig"))
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    failures = 0
    fetched = False
    for index, item in enumerate(queue[args.start:args.start + args.limit], start=args.start):
        raw_id = item if isinstance(item, str) else item["id"]
        match = re.fullmatch(r"(\d{4}\.\d{4,5})(?:v([1-9]\d*))?", raw_id)
        if not match:
            parser.error(f"无法识别 arXiv ID：{raw_id}")
        aid, explicit_version = match.groups()
        version = int(explicit_version) if explicit_version else args.version
        target = output_dir / f"{aid}v{version}正文.json"
        cached = json.loads(target.read_text(encoding="utf-8")) if target.exists() else None
        if cached and "error" not in cached and (not cached.get("paper") or "sections" in cached["paper"]) and not (
            cached.get("text_truncated") and len(cached.get("text", "")) < args.max_chars
        ):
            result = cached
            reused = True
        else:
            if fetched:
                time.sleep(args.delay)
            result = reader.read_page(
                f"https://arxiv.org/html/{aid}v{version}", max_chars=args.max_chars, max_links=60,
            )
            target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            reused = False
            fetched = True
        if "error" in result:
            failures += 1
        # 作者区不进 stdout：机构用 机构初筛.py 在本地筛；摘要只在 --abstract 时输出。
        paper = result.get("paper")
        line = {
            "index": index,
            "id": aid,
            "reading_version": version,
            "reused": reused,
            "error": result.get("error"),
            "title": paper["title"] if paper else None,
            "arxiv_version_date": paper["arxiv_version_date"] if paper else None,
        }
        if args.abstract:
            line["abstract"] = paper["abstract"][:1600] if paper else result.get("text", "")[:1600]
        if result.get("invalid_links"):
            line["invalid_links"] = result["invalid_links"]
        print(json.dumps(line, ensure_ascii=False), flush=True)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
