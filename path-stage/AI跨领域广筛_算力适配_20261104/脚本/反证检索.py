# -*- coding: utf-8 -*-
"""反证检索：不限机构、不限窗口（2024-01 起），按相关度取标题，只用于判断是否已有工作涉及。"""
import sys, time, json, urllib.parse, urllib.request, xml.etree.ElementTree as ET
NS = "{http://www.w3.org/2005/Atom}"
Q = json.load(open(sys.argv[1], encoding="utf-8"))
for name, q in Q.items():
    p = {"search_query": f"({q}) AND submittedDate:[202401010000 TO 202611042359]", "max_results": 12, "sortBy": "relevance"}
    u = "https://export.arxiv.org/api/query?" + urllib.parse.urlencode(p)
    try: root = ET.fromstring(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "landscape/1.0"}), timeout=120).read())
    except Exception as e: print("##", name, "ERR", e); continue
    print("##", name)
    for e in root.findall(NS + "entry"):
        print(" ", e.find(NS + "id").text.split("/abs/")[-1], e.find(NS + "published").text[:10], " ".join(e.find(NS + "title").text.split())[:110])
    time.sleep(3)
