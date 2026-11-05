# -*- coding: utf-8 -*-
"""反证检索：不限窗口，按查询打印前 N 条 ID/日期/标题。"""
import sys, time, urllib.parse, urllib.request, xml.etree.ElementTree as ET
NS = "{http://www.w3.org/2005/Atom}"
n = int(sys.argv[1])
for q in sys.argv[2:]:
    u = "https://export.arxiv.org/api/query?" + urllib.parse.urlencode({"search_query": q, "max_results": n, "sortBy": "relevance"})
    try: root = ET.fromstring(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "landscape/1.0"}), timeout=120).read())
    except Exception as e: print("ERR", q, e); continue
    print("==", q)
    for e in root.findall(NS + "entry"):
        print(" ", e.find(NS + "id").text.split("/abs/")[-1], e.find(NS + "published").text[:10], " ".join(e.find(NS + "title").text.split())[:110])
    time.sleep(3)
