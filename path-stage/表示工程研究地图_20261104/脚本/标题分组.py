# -*- coding: utf-8 -*-
"""本地按标题/摘要关键词计数主题分布，并输出相关候选的 ID+标题 列表（不打印摘要）。"""
import json, re, sys, collections
from pathlib import Path
d = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))["papers"]
REL = re.compile(r"steer|interven|represent\w* (engineer|edit|fine-?tun)|ReFT|activation (edit|addition|patch)|direction|erasure|persona vector|function vector|task vector|in-context vector|circuit breaker|rerout|sparse autoencoder|\bSAEs?\b|transcoder|clamp", re.I)
OFF = re.compile(r"autonomous driving|vehicle|robot|diffusion model|text-to-image|image generation|video generation|protein|molecul", re.I)
TOP = {
 "失败/可靠性/评测": r"fail|limitation|unreliab|reliab|robust|brittle|benchmark|evaluat|systematic|empirical|when does|does .* work|pitfall|side effect|trade-?off|degrad|coheren|generaliz",
 "安全/拒答/越狱": r"safety|refus|jailbreak|harmful|misalign|alignment|deception|sycophan|toxic",
 "SAE/特征": r"sparse autoencoder|\bSAE|transcoder|feature",
 "推理/CoT控制": r"reasoning|chain-of-thought|\bCoT\b|overthink|thinking",
 "人格/风格/价值": r"persona|personality|style|value|emotion|sentiment|character|role",
 "幻觉/事实性": r"hallucinat|truthful|factual",
 "多模态VLM": r"vision|visual|multimodal|VLM|image",
 "理论/几何": r"theor|geometr|linear representation|subspace|manifold",
 "训练期/ReFT/微调": r"fine-?tun|ReFT|training|train",
 "Agent": r"agent|tool",
 "多语言": r"multilingual|language-specific|cross-lingual|translation",
}
rel = [p for p in d if REL.search(p["title"] + " " + p["summary"]) and not OFF.search(p["title"])]
print("total", len(d), "relevant", len(rel))
c = collections.Counter()
for p in rel:
    for k, rx in TOP.items():
        if re.search(rx, p["title"], re.I): c[k] += 1
print(dict(c.most_common()))
m = collections.Counter(p["published"][:7] for p in rel); print(dict(sorted(m.items())))
Path(sys.argv[2]).write_text("\n".join(f'{p["id"]}|{p["title"][:110]}' for p in sorted(rel, key=lambda x: x["id"])), encoding="utf-8")
