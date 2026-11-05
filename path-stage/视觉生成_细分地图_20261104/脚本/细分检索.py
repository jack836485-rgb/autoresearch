# -*- coding: utf-8 -*-
"""跨领域广筛：每个主题 = 领域摘要词 AND 标题诊断词，窗口内按提交日倒序取候选（只用于发现，不判资格）。摘要落盘不打印。"""
import json, sys, time, urllib.parse, urllib.request, xml.etree.ElementTree as ET
from pathlib import Path
NS = "{http://www.w3.org/2005/Atom}"; OS = "{http://a9.com/-/spec/opensearch/1.1/}"
W1 = ("202605040000", "202611042359")
DIAG = ('(ti:fail OR ti:fails OR ti:failure OR ti:failures OR ti:limitation OR ti:limitations OR ti:pitfall OR ti:pitfalls '
        'OR ti:revisit OR ti:revisiting OR ti:rethinking OR ti:understanding OR ti:why OR ti:when OR ti:does OR ti:illusion '
        'OR ti:myth OR ti:really OR ti:hidden OR ti:brittle OR ti:lessons OR ti:paradox OR ti:collapse OR ti:"empirical study" '
        'OR ti:"systematic study" OR ti:survey OR ti:degradation OR ti:mirage OR ti:"trade-off" OR ti:surprising OR ti:diagnosing OR ti:not)')
T = {
 "少步/一步生成": 'abs:MeanFlow OR abs:"one-step generation" OR abs:"one-step diffusion" OR abs:"few-step generation" OR abs:"few-step diffusion" OR abs:"consistency model" OR abs:"consistency models" OR abs:"shortcut model" OR abs:"flow map"',
 "扩散蒸馏": '(abs:distillation) AND (abs:diffusion OR abs:"flow matching") AND (abs:image OR abs:"text-to-image") OR abs:"distribution matching distillation" OR abs:"score distillation"',
 "引导/CFG": 'abs:"classifier-free guidance" OR abs:"guidance scale" OR abs:autoguidance OR abs:"guidance interval" OR (abs:guidance AND abs:diffusion AND abs:sampling)',
 "tokenizer/潜空间": '(abs:tokenizer OR abs:autoencoder OR abs:VAE OR abs:"latent space") AND (abs:"image generation" OR abs:"latent diffusion" OR abs:"visual generation")',
 "像素空间扩散": 'abs:"pixel-space diffusion" OR abs:"pixel diffusion" OR abs:"pixel space" AND abs:diffusion OR abs:JiT',
 "自回归/掩码视觉生成": '(abs:autoregressive OR abs:"masked generative" OR abs:"next-scale" OR abs:"visual autoregressive" OR abs:MAR) AND (abs:"image generation" OR abs:"visual generation" OR abs:"text-to-image")',
 "流匹配训练细节": '(abs:"flow matching" OR abs:"rectified flow" OR abs:diffusion) AND (abs:"noise schedule" OR abs:"loss weighting" OR abs:parameterization OR abs:"x-prediction" OR abs:"v-prediction" OR abs:"timestep sampling" OR abs:"training dynamics")',
 "生成评测指标": '(abs:FID OR abs:"Fréchet" OR abs:"evaluation metric" OR abs:"human preference" OR abs:"reward model") AND (abs:"image generation" OR abs:"text-to-image" OR abs:"generative model")',
 "文生图对齐/组合": 'abs:"text-to-image" AND (abs:compositional OR abs:"prompt following" OR abs:"text-image alignment" OR abs:counting OR abs:"spatial relationship" OR abs:"attribute binding")',
 "扩散后训练/RL": '(abs:"reinforcement learning" OR abs:GRPO OR abs:DPO OR abs:"reward fine-tuning" OR abs:RLHF OR abs:"preference optimization") AND (abs:diffusion OR abs:"flow matching" OR abs:"text-to-image")',
 "编辑/个性化": '(abs:"image editing" OR abs:personalization OR abs:"subject-driven" OR abs:DreamBooth OR abs:"concept erasure" OR abs:"unlearning") AND (abs:diffusion OR abs:"flow matching" OR abs:"text-to-image")',
 "推理加速/采样器": '(abs:"feature caching" OR abs:"cache" OR abs:"ODE solver" OR abs:sampler OR abs:"sampling steps" OR abs:"token pruning" OR abs:"token merging") AND (abs:diffusion OR abs:"diffusion transformer")',
 "扩散理论/泛化": '(abs:diffusion OR abs:"flow matching") AND (abs:memorization OR abs:generalization OR abs:"score estimation" OR abs:"sample complexity" OR abs:creativity OR abs:"mode collapse" OR abs:diversity)',
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
out = Path(sys.argv[1]); cap = int(sys.argv[2]) if len(sys.argv) > 2 else 400
papers, log = {}, []
for name, qq in T.items():
    base = (f"({qq}) AND {DIAG}" if name=="扩散理论/泛化" else f"({qq})") + f" AND (cat:cs.CV OR cat:cs.LG) AND submittedDate:[{W1[0]} TO {W1[1]}]"
    got, start, dates = 0, 0, []
    while True:
        root, total = call(base, start)
        if root is None: log.append({"topic": name, "error": f"fetch failed at {start}"}); break
        es = root.findall(NS + "entry")
        for e in es:
            aid = e.find(NS + "id").text.split("/abs/")[-1].rsplit("v", 1)[0]
            pub = e.find(NS + "published").text[:10]; dates.append(pub)
            rec = papers.setdefault(aid, {"id": aid, "title": " ".join(e.find(NS + "title").text.split()), "published": pub,
                "summary": " ".join(e.find(NS + "summary").text.split()),
                "cats": [c.get("term") for c in e.findall(NS + "category")], "topics": []})
            rec["topics"].append(name)
        got += len(es); start += 200
        if not es or start >= min(total, cap): break
    log.append({"topic": name, "W1": total, "got": got, "最早": min(dates) if dates else None, "最晚": max(dates) if dates else None})
    print(log[-1], flush=True)
    out.write_text(json.dumps({"log": log, "papers": list(papers.values())}, ensure_ascii=False, indent=0), encoding="utf-8")
print("unique", len(papers))
