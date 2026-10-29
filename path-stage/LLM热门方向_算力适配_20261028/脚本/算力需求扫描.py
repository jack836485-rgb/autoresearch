# -*- coding: utf-8 -*-
"""对旧 slot 各问题卡的主要证据论文，在本地正文中提取模型规模与训练算力线索。
只输出每篇的规模统计和 GPU 片段（短），全文不进上下文。用法：python 算力需求扫描.py <旧slot目录> <输出.tsv>"""
import json, re, sys, collections
from pathlib import Path

old = Path(sys.argv[1]); out = Path(sys.argv[2])
md = (old / "研究地图.md").read_text(encoding="utf-8")

# 参考文献编号 -> arXiv ID
refs = dict(re.findall(r'<a id="r(\d+)"></a>.*?arXiv:(\d{4}\.\d{5})', md)) or dict(re.findall(r'^(\d+)\. .*?arXiv:(\d{4}\.\d{5})', md, re.M))
# 问题地图：Q -> 主要证据编号
qmap = {}
for line in md.splitlines():
    m = re.match(r"\|\s*(?:\*\*)?(Q\d{3})(?:\*\*)?\s*\|", line) or re.match(r"\|\s*\*\*(Q\d{3})\*\*", line)
    if m:
        cell = line.split("|")[-2]
        nums = re.findall(r"\[(\d+)\]", cell)
        for a, b in re.findall(r"\[(\d+)\]\s*[–-]\s*\[(\d+)\]", cell):
            nums += [str(i) for i in range(int(a), int(b) + 1)]
        qmap[m.group(1)] = sorted(set(nums), key=int)

SIZE = re.compile(r"(?<![\w.])(\d{1,3}(?:\.\d)?)\s?B(?:-A\d+(?:\.\d)?B)?(?![\w])")
GPU = re.compile(r"(?:\d+\s*[x×]?\s*)?(?:NVIDIA\s+)?(?:H100|H200|H800|H20|A100|A800|B200|GB200|L40S?|RTX\s?4090|TPU\s?v\d\w*)[^.;\n]{0,60}|\d[\d,.]*\s*(?:GPU|H100|A100)[- ]hours?", re.I)

def text_of(aid):
    fs = list((old / "资料" / "正文").glob(f"{aid}v*正文.json"))
    if not fs:
        return None
    j = json.loads(fs[0].read_text(encoding="utf-8"))
    secs = j.get("sections") or j.get("章节") or []
    if isinstance(secs, list):
        parts = []
        for s in secs:
            if isinstance(s, dict):
                t = (s.get("title") or s.get("标题") or "")
                if re.search(r"reference|related work|acknowledg", t, re.I):
                    continue
                parts.append(s.get("text") or s.get("content") or s.get("正文") or "")
        if parts:
            return "\n".join(parts)
    return j.get("text") or j.get("正文") or json.dumps(j, ensure_ascii=False)

rows = ["问题\t编号\tarXiv\t模型规模(B,出现次数前5)\t最大规模B\tGPU线索(前3)"]
for q, nums in qmap.items():
    for n in nums:
        aid = refs.get(n)
        if not aid:
            continue
        t = text_of(aid)
        if t is None:
            rows.append(f"{q}\t[{n}]\t{aid}\t无本地正文\t\t"); continue
        sizes = [float(x) for x in SIZE.findall(t) if 0.05 <= float(x) <= 1000]
        c = collections.Counter(sizes).most_common(5)
        gpus = []
        for g in GPU.findall(t):
            g = " ".join(g.split())[:70]
            if g not in gpus:
                gpus.append(g)
        rows.append(f"{q}\t[{n}]\t{aid}\t{', '.join(f'{k:g}×{v}' for k, v in c)}\t{max(sizes) if sizes else ''}\t{' | '.join(gpus[:3])}")
out.write_text("\n".join(rows), encoding="utf-8")
print("\n".join(rows))
