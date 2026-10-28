# -*- coding: utf-8 -*-
"""按提交日期窗口批量查询 arXiv API，合并去重，保存候选。"""
import json, sys, time, urllib.parse, urllib.request, xml.etree.ElementTree as ET
from pathlib import Path
NS = "{http://www.w3.org/2005/Atom}"
START, END = "202604160000", "202610162359"
QUERIES = [
 'all:"agentic reinforcement learning"',
 'all:"agentic RL"',
 'all:"multi-turn reinforcement learning"',
 'all:"multi-turn RL" AND all:agent',
 'all:"reinforcement learning" AND all:"tool use" AND all:agent AND all:"language model"',
 'all:"tool-integrated reasoning" AND all:"reinforcement learning"',
 'all:"long-horizon" AND all:"reinforcement learning" AND all:agent AND all:LLM',
 'all:"credit assignment" AND all:agent AND all:"language model" AND all:"reinforcement learning"',
 'all:"turn-level" AND all:reward AND all:agent',
 'all:"asynchronous" AND all:"reinforcement learning" AND all:agent AND all:LLM',
 'all:"search agent" AND all:"reinforcement learning"',
 'all:"deep research" AND all:"reinforcement learning" AND all:agent',
 'all:"software engineering" AND all:agent AND all:"reinforcement learning"',
 'all:"SWE-bench" AND all:"reinforcement learning"',
 'all:"GUI agent" AND all:"reinforcement learning"',
 'all:"web agent" AND all:"reinforcement learning"',
 'all:"environment scaling" AND all:agent',
 'all:"synthetic environments" AND all:agent AND all:"reinforcement learning"',
 'all:"reward hacking" AND all:agent AND all:"reinforcement learning"',
 'all:"RLVR" AND all:agent AND all:"multi-turn"',
 'all:"process reward" AND all:agent AND all:"reinforcement learning" AND all:LLM',
 'all:"exploration" AND all:"agentic" AND all:"reinforcement learning"',
 'all:"off-policy" AND all:agentic',
 'all:"context management" AND all:"reinforcement learning" AND all:agent',
 'all:"memory" AND all:agent AND all:"reinforcement learning" AND all:LLM AND all:"long-horizon"',
 'all:"self-evolving" AND all:agent AND all:"reinforcement learning"',
 'all:"scaling" AND all:"agentic RL"',
 'all:"entropy collapse" AND all:agent',
 'all:"GRPO" AND all:agent AND all:"multi-turn"',
 'all:"survey" AND all:"agentic reinforcement learning"',
 'all:"empirical study" AND all:agent AND all:"reinforcement learning" AND all:LLM',
 'all:"terminal" AND all:agent AND all:"reinforcement learning" AND all:LLM',
 'all:"code agent" AND all:"reinforcement learning"',
 'all:"language agent" AND all:"reinforcement learning"',
 'all:"hierarchical" AND all:agent AND all:"reinforcement learning" AND all:LLM AND all:"long-horizon"',
 'all:"reward model" AND all:agentic',
 'all:"verifier" AND all:agentic AND all:"reinforcement learning"',
 'all:"multi-agent" AND all:"reinforcement learning" AND all:LLM AND all:tool',
 'all:"generalization" AND all:agentic AND all:"reinforcement learning" AND all:environments',
 'all:"sparse reward" AND all:agent AND all:LLM AND all:"reinforcement learning"',
 'all:"computer use" AND all:"reinforcement learning" AND all:agent',
 'all:"rubric" AND all:agent AND all:"reinforcement learning"',
]
def fetch(q, start, maxr=100):
    params = {"search_query": f"({q}) AND submittedDate:[{START} TO {END}]", "start": start,
              "max_results": maxr, "sortBy": "submittedDate", "sortOrder": "descending"}
    url = "http://export.arxiv.org/api/query?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "landscape-search/1.0"})
    for a in range(4):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                data = r.read()
            root = ET.fromstring(data)
            total = root.find("{http://a9.com/-/spec/opensearch/1.1/}totalResults")
            return root, int(total.text) if total is not None else -1
        except Exception:
            time.sleep(5 * (a + 1))
    return None, -1
out, log = {}, []
for q in QUERIES:
    got = 0; start = 0; total = -1; dates = []
    while True:
        root, total = fetch(q, start)
        if root is None:
            log.append({"query": q, "error": "fetch failed", "start": start}); break
        entries = root.findall(NS + "entry")
        for e in entries:
            aid = e.find(NS + "id").text.split("/abs/")[-1]
            base = aid.rsplit("v", 1)[0]
            pub = e.find(NS + "published").text[:10]
            dates.append(pub)
            rec = out.setdefault(base, {"id": base, "title": " ".join(e.find(NS + "title").text.split()),
                "published": pub, "updated": e.find(NS + "updated").text[:10],
                "authors": [a.find(NS + "name").text for a in e.findall(NS + "author")],
                "summary": " ".join(e.find(NS + "summary").text.split())[:700],
                "categories": [c.get("term") for c in e.findall(NS + "category")],
                "queries": []})
            rec["queries"].append(q)
        got += len(entries); start += len(entries)
        if len(entries) == 0 or got >= total or got >= 400: break
        time.sleep(3)
    log.append({"query": q, "total": total, "got": got,
                "earliest": min(dates) if dates else None, "latest": max(dates) if dates else None})
    print(q, total, got, min(dates) if dates else None, flush=True)
    time.sleep(3)
Path(sys.argv[1]).write_text(json.dumps({"log": log, "papers": list(out.values())}, ensure_ascii=False, indent=1), encoding="utf-8")
print("unique", len(out))
