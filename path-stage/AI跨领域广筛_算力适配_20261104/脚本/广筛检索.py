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
 "图像/视频扩散与流匹配": '(abs:diffusion OR abs:"flow matching" OR abs:"rectified flow") AND (abs:image OR abs:video OR abs:"text-to-image" OR abs:ImageNet)',
 "视觉tokenizer/潜空间": '(abs:tokenizer OR abs:autoencoder OR abs:VAE OR abs:"latent space") AND (abs:"image generation" OR abs:"visual generation" OR abs:"video generation" OR abs:reconstruction)',
 "少步生成/蒸馏/引导": 'abs:"classifier-free guidance" OR abs:"consistency model" OR abs:"consistency models" OR abs:"one-step generation" OR abs:"few-step" OR abs:"distribution matching distillation" OR abs:"autoguidance"',
 "自回归视觉生成": '(abs:autoregressive OR abs:"masked generative" OR abs:"next-token") AND (abs:"image generation" OR abs:"visual generation" OR abs:"video generation")',
 "自监督视觉表征": 'abs:"self-supervised" AND (abs:visual OR abs:image OR abs:vision) OR abs:DINOv2 OR abs:DINOv3 OR abs:JEPA OR abs:"masked image modeling" OR abs:"masked autoencoder"',
 "视觉编码器/VLM视觉侧": '(abs:"vision encoder" OR abs:"visual encoder" OR abs:CLIP OR abs:SigLIP OR abs:"visual tokens") AND (abs:"vision-language" OR abs:multimodal)',
 "具身/VLA/机器人策略": 'abs:"vision-language-action" OR abs:VLA OR abs:"robot policy" OR abs:"robot policies" OR abs:"diffusion policy" OR abs:"imitation learning" OR abs:"robot learning"',
 "世界模型/视频预测": 'abs:"world model" OR abs:"world models" OR abs:"video prediction" OR abs:"action-conditioned video"',
 "非LLM强化学习": '(abs:"reinforcement learning") AND (abs:"continuous control" OR abs:Atari OR abs:"offline RL" OR abs:"offline reinforcement" OR abs:MuJoCo OR abs:"value-based" OR abs:"model-based RL" OR abs:"scaling RL" OR abs:locomotion) ANDNOT (abs:LLM OR abs:"language model")',
 "优化器/训练动力学": 'abs:optimizer OR abs:Muon OR abs:"learning rate schedule" OR abs:"loss spike" OR abs:"loss spikes" OR abs:"training dynamics" OR abs:"weight decay" OR abs:"training instability" OR abs:"edge of stability" OR abs:"grokking"',
 "缩放律/预训练": 'abs:"scaling law" OR abs:"scaling laws" OR abs:"compute-optimal" OR abs:"pretraining data" OR abs:"data mixture" OR abs:"data mixing" OR abs:"data selection" OR abs:"data curation"',
 "序列架构(SSM/线性注意力/MoE)": 'abs:"state space model" OR abs:"state-space model" OR abs:Mamba OR abs:"linear attention" OR abs:"hybrid architecture" OR abs:"mixture of experts" OR abs:"mixture-of-experts" OR abs:"sparse attention" OR abs:"length extrapolation" OR abs:"long context"',
 "可解释性(SAE/电路)": 'abs:"sparse autoencoder" OR abs:"sparse autoencoders" OR abs:"mechanistic interpretability" OR abs:"circuit discovery" OR abs:"linear probe" OR abs:"feature attribution" OR abs:"activation steering" OR abs:transcoder OR abs:"crosscoder"',
 "持续学习/遗忘/合并": 'abs:"continual learning" OR abs:"catastrophic forgetting" OR abs:"model merging" OR abs:"task arithmetic" OR abs:"continual pretraining" OR abs:"knowledge editing" OR abs:"machine unlearning" OR abs:unlearning',
 "3D/新视角/重建": 'abs:"Gaussian splatting" OR abs:"3D reconstruction" OR abs:"novel view synthesis" OR abs:"feed-forward 3D" OR abs:"3D generation" OR abs:"point map"',
 "时序/科学基础模型": 'abs:"time series foundation" OR abs:"time series forecasting" OR abs:"weather forecasting" OR abs:"protein language model" OR abs:"molecular generation" OR abs:"neural operator" OR abs:"PDE" OR abs:"materials discovery"',
 "测试时训练/适应": 'abs:"test-time training" OR abs:"test-time adaptation" OR abs:"in-context learning" AND (abs:transformer OR abs:theory) OR abs:"meta-learning"',
 "鲁棒性/校准/OOD": 'abs:"distribution shift" OR abs:"out-of-distribution" OR abs:calibration OR abs:"spurious correlation" OR abs:"shortcut learning" OR abs:"adversarial robustness"',
 "语音/音频": 'abs:speech OR abs:audio OR abs:"text-to-speech" OR abs:"speech recognition"',
 "推荐/图学习": 'abs:"recommender system" OR abs:"recommendation" OR abs:"graph neural network" OR abs:"graph neural networks" OR abs:"generative recommendation"',
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
    base = f"({qq}) AND {DIAG} AND submittedDate:[{W1[0]} TO {W1[1]}]"
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
