"""arXiv API 关键词检索：只输出 ID | v1 日期 | 标题，供标题筛。
用法: python arxiv_q.py 起始YYYYMMDD 截止YYYYMMDD '查询1' '查询2' ...
查询语法为 arXiv search_query（如 abs:"privileged information" AND abs:distillation）。
"""
import sys, time, urllib.parse, urllib.request, xml.etree.ElementTree as ET

NS = {"a": "http://www.w3.org/2005/Atom"}
start, end, queries = sys.argv[1], sys.argv[2], sys.argv[3:]
seen = set()
for q in queries:
    full = f"({q}) AND submittedDate:[{start}0000 TO {end}2359]"
    url = "http://export.arxiv.org/api/query?" + urllib.parse.urlencode(
        {"search_query": full, "max_results": 60, "sortBy": "submittedDate", "sortOrder": "descending"})
    for attempt in range(2):
        try:
            data = urllib.request.urlopen(url, timeout=60).read()
            break
        except Exception as e:
            if attempt:
                print(f"!! {q}: {e}"); data = None
            time.sleep(5)
    if not data:
        continue
    root = ET.fromstring(data)
    entries = root.findall("a:entry", NS)
    print(f"== {q} -> {len(entries)}")
    for e in entries:
        aid = e.find("a:id", NS).text.rsplit("/", 1)[-1].split("v")[0]
        title = " ".join(e.find("a:title", NS).text.split())
        pub = e.find("a:published", NS).text[:10]
        mark = "" if aid not in seen else " (dup)"
        seen.add(aid)
        print(f"{aid} | {pub} | {title}{mark}")
    time.sleep(3.5)
