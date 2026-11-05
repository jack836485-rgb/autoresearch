# -*- coding: utf-8 -*-
"""GUI Agent 广筛：按子问题查询 arXiv，窗口内全部取回（仅发现，不判资格）。元数据落盘，stdout 只打印每个查询的计数与日期跨度。"""
import json, sys, time, urllib.parse, urllib.request, xml.etree.ElementTree as ET
from pathlib import Path
NS = "{http://www.w3.org/2005/Atom}"; OS = "{http://a9.com/-/spec/opensearch/1.1/}"
W = ("202605040000", "202611042359")
Q = {
 "GUI agent": 'abs:"GUI agent" OR abs:"GUI agents" OR ti:GUI',
 "computer use": 'abs:"computer-use" OR abs:"computer use agent" OR abs:"computer use agents" OR abs:"computer-using" OR abs:"OS agent" OR abs:"OS agents" OR abs:"desktop agent"',
 "GUI benchmarks": 'abs:OSWorld OR abs:AndroidWorld OR abs:ScreenSpot OR abs:AndroidControl OR abs:"WindowsAgentArena" OR abs:"Windows Agent Arena" OR abs:AndroidLab OR abs:"GUI-Odyssey" OR abs:"OSWorld-Verified"',
 "grounding/screen": 'abs:"GUI grounding" OR abs:"UI grounding" OR abs:"screen understanding" OR abs:"screenshot" AND abs:agent OR abs:"visual grounding" AND abs:interface',
 "mobile": 'abs:"mobile agent" OR abs:"mobile agents" OR abs:"smartphone agent" OR abs:"phone agent" OR abs:"mobile GUI" OR abs:"Android agent" OR abs:"phone-use"',
 "web visual": 'abs:"web agent" OR abs:"web agents" OR abs:"browser agent" OR abs:"browser-use" OR abs:"web navigation" OR abs:WebArena OR abs:VisualWebArena OR abs:Mind2Web OR abs:WebVoyager',
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
    got, start, dates = 0, 0, []
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
