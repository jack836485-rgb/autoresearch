# -*- coding: utf-8 -*-
"""下载 arXiv v1 PDF，只在首页文本里按白名单/QS 正则找机构，打印命中处短片段。"""
import sys, re, time, urllib.request, fitz
from pathlib import Path
src = (Path(__file__).parent / "机构初筛_含QS.py").read_text(encoding="utf-8")
ns = {}; exec(src.split("d = Path(sys.argv[1])")[0], ns); RX = {**ns["WL"], **ns["QS"]}
out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
for aid in sys.argv[2:]:
    f = out / f"{aid}v1.pdf"
    try:
        if not f.exists():
            req = urllib.request.Request(f"https://arxiv.org/pdf/{aid}v1", headers={"User-Agent": "landscape-search/1.0"})
            f.write_bytes(urllib.request.urlopen(req, timeout=90).read()); time.sleep(2)
        t = fitz.open(f)[0].get_text()
        found = []
        for k, rx in RX.items():
            m = re.search(rx, t)
            if m: found.append(f"{k}「{' '.join(t[max(0,m.start()-30):m.end()+20].split())}」")
        print(aid, "；".join(found[:4]) or "首页未命中")
    except Exception as e:
        print(aid, "错误", e)
