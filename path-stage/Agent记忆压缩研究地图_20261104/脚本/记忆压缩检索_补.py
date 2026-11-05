# -*- coding: utf-8 -*-
"""Agent 记忆/上下文压缩广筛：按子问题查询 arXiv，窗口内全部取回（仅发现，不判资格）。stdout 只打印每个查询的计数与日期跨度。"""
import json, sys, time, urllib.parse, urllib.request, xml.etree.ElementTree as ET
from pathlib import Path
NS = "{http://www.w3.org/2005/Atom}"; OS = "{http://a9.com/-/spec/opensearch/1.1/}"
W = ("202605040000", "202611042359")
AG = '(abs:agent OR abs:agents OR abs:agentic OR abs:"multi-turn" OR abs:"tool use" OR abs:"tool-use" OR abs:"long-horizon")'
Q = {
 "补:compaction/summariz/evict 单词": f'(abs:compaction OR abs:compact OR abs:summarization OR abs:summarize OR abs:eviction OR abs:SideQuest OR abs:"garbage collection" OR abs:"context rot" OR abs:"self-summarization") AND {AG}',
 "补:标题含压缩": 'ti:compaction OR ti:"context compression" OR ti:"memory compression" OR ti:"context management" OR ti:summarization AND ti:agent',
}
def call(sq, start=0, maxr=200):
    p = {"search_query": sq, "start": start, "max_results": maxr, "sortBy": "submittedDate", "sortOrder": "descending"}
    req = urllib.request.Request("https://export.arxiv.org/api/query?" + urllib.parse.urlencode(p), headers={"User-Agent": "landscape-search/1.0"})
    for a in range(5):
        try:
            with urllib.request.urlopen(req, timeout=120) as r: root = ET.fromstring(r.read())
            t = root.find(OS + "totalResults"); time.sleep(3)
            return root, int(t.text) if t is not None else -1
        except Exception: time.sleep(10 * (a + 1))
    return None, -1
out = Path(sys.argv[1]); papers, log = {}, []
for name, qq in Q.items():
    base = f"({qq}) AND submittedDate:[{W[0]} TO {W[1]}]"
    got, start, dates, total = 0, 0, [], -1
    while True:
        root, total = call(base, start)
        if root is None: log.append({"q": name, "error": f"fetch failed at {start}"}); break
        es = root.findall(NS + "entry")
        for e in es:
            aid = e.find(NS + "id").text.split("/abs/")[-1].rsplit("v", 1)[0]
            pub = e.find(NS + "published").text[:10]; dates.append(pub)
            rec = papers.setdefault(aid, {"id": aid, "title": " ".join(e.find(NS + "title").text.split()), "published": pub,
                "summary": " ".join(e.find(NS + "summary").text.split()), "cats": [c.get("term") for c in e.findall(NS + "category")], "q": []})
            rec["q"].append(name)
        got += len(es); start += 200
        if not es or start >= total: break
    log.append({"q": name, "total": total, "got": got, "最早": min(dates) if dates else None, "最晚": max(dates) if dates else None})
    print(log[-1], flush=True)
    out.write_text(json.dumps({"log": log, "papers": list(papers.values())}, ensure_ascii=False, indent=0), encoding="utf-8")
print("unique", len(papers))
