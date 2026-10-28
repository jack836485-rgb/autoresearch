# -*- coding: utf-8 -*-
"""用 arXiv API id_list 取被引论文的作者顺序与 v1 日期，供参考文献；不判断资格。"""
import json, sys, time, urllib.request, urllib.parse, xml.etree.ElementTree as ET
NS = "{http://www.w3.org/2005/Atom}"
ids = sys.argv[2:]; out = {}
for k in range(0, len(ids), 40):
    u = "https://export.arxiv.org/api/query?" + urllib.parse.urlencode({"id_list": ",".join(ids[k:k+40]), "max_results": 50})
    root = ET.fromstring(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "landscape/1.0"}), timeout=120).read())
    for e in root.findall(NS + "entry"):
        i = e.find(NS + "id").text.split("/abs/")[-1].rsplit("v", 1)[0]
        out[i] = {"title": " ".join(e.find(NS + "title").text.split()), "published": e.find(NS + "published").text[:10],
                  "authors": [a.find(NS + "name").text for a in e.findall(NS + "author")]}
    time.sleep(3)
json.dump(out, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False, indent=1); print(len(out))
