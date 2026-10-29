# -*- coding: utf-8 -*-
"""从两张旧图继承问题卡（L- = LLM新兴领域图，A- = Agentic RL 图），追加本周证据与算力评估，导出本 slot 的 研究问题.json。"""
import json, copy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OLD_L = ROOT / "LLM新兴领域研究地图_20261021" / "研究问题.json"
OLD_A = ROOT / "AgenticRL研究地图_20261021" / "研究问题.json"
OUT = Path(__file__).resolve().parents[1] / "研究问题.json"

# 算力档位口径
# 预研：2×A100 80G / 4×L40 48G / 8×4090 24G；实验：8×A100 80G
# 算力评估字段：最小可证伪实验的规模、所需卡与档位、主要成本、风险
ASSESS = {
 "L-Q001": dict(热度="在策略蒸馏/自蒸馏 份额 10.0×（旧图关键词计数）", 最小实验="Qwen3-1.7B/4B 学生全参 OPSD 或 OPD，评测预算 32k 以上", 证据论文规模="学生 1.5–8B，教师至多 32B；[1] 用 8×H100，[3] 用 8×A800", 适配="高：8×A100 实验卡可做；预研卡可在 1.7B 上起步", 主要成本="长预算评测的推理时长；A100 约比 H100 慢 2–3 倍。本周 Bridged Self-Distillation 全部训练、评测和消融约 1450 H100/H200 GPU 小时", 风险="方向最拥挤，本周又有 3 篇相关标题；你已有 idea opsd_thinking_q001 在此"),
 "L-Q002": dict(热度="循环深度 份额 9.4×", 最小实验="循环与非循环模型在等训练 FLOPs、等推理 FLOPs 下对比，并做深度外推", 证据论文规模="0.6B–60B，多为从头预训练", 适配="低–中：8×A100 只能做 1B 以下、少量 token 的预训练，规模说服力弱", 主要成本="预训练 token 量", 风险="主会审稿可能要求更大规模"),
 "L-Q003": dict(热度="潜空间推理 份额 1.87×", 最小实验="对文本隐式 CoT 做内容替换或只保留边界标记，与 no-CoT 对照", 证据论文规模="≤8B，[16] 用 H800", 适配="高：推理加小规模训练，预研卡即可起步", 主要成本="低", 风险="热度中等；需先确认文本域是否已有内容替换实验"),
 "L-Q004": dict(热度="扩散语言模型 份额 2.18×；本周 HF 标题约 7 篇", 最小实验="7–8B dLLM 在等前向次数下比较 PRM 引导与事后重排、加速与未加速解码", 证据论文规模="7–8B 推理；[17] 单张 H20，[20] 8×A100", 适配="高：以推理为主，单卡到 8 卡均可", 主要成本="低", 风险="本周已有 unmasking policy 受控研究等标题，需查新"),
 "L-Q005": dict(热度="技能/自进化 Agent 份额 5.3×；本周 harness 自进化标题集中", 最小实验="技能库规模 × 技能质量的析因设计，记录调用率与成功率", 证据论文规模="以 agent 推理为主；[25] 用 27–35B 与 H100", 适配="高：开源 27–35B 模型可在 8×A100 上推理，或用 API", 主要成本="agent 轨迹的 token 与 API 费用", 风险="API 预算需控制在 1000 元档内"),
 "L-Q006": dict(热度="Agent 记忆 份额 3.16×；本周 HF 标题约 7 篇", 最小实验="流式整合与一次性整合、只追加记忆的对照，跟踪更新次数", 证据论文规模="4–27B 推理；[27] 用 4×A100", 适配="高：纯推理，预研卡即可", 主要成本="长对话评测的推理 token", 风险="本周 Memory Tax 与 Naive RAG 两篇已系统显示多数记忆系统不如朴素 RAG，原卡剩余空间收窄"),
 "L-Q007": dict(热度="AI 科学家/自动研究 份额 3.16×；本周 RSI 标题约 10 篇", 最小实验="自动研究循环中把搜索集与评测集分离，分别控制候选数和循环长度", 证据论文规模="循环内任务多为 ≤4B 训练；[30] 约 200 A100 小时", 适配="中–高：训练端可做，瓶颈在 agent 循环的 token 与 API", 主要成本="token 消耗大，与你 token 稀缺的约束冲突", 风险="RSI 基准在 7–8 月已成批出现，方向在升温"),
 "L-Q008": dict(热度="涌现失配 份额 1.59×", 最小实验="在 7–32B 上 LoRA 诱导失配，再用条件触发提示评测缓解方法", 证据论文规模="7–36B，LoRA 为主；[37] 用 A100/H100/H200", 适配="高：8×A100 可做 32B LoRA", 主要成本="评测需要 LLM 判官，可用 API", 风险="你已有 idea em_conditional_mitigation 在此"),
 "L-Q009": dict(热度="CoT 忠实性/可监控性 份额 1.42×", 最小实验="长转录填充 × 错误奖励 policy 的 2×2 交互", 证据论文规模="监控器 30–122B", 适配="中：被监控 policy 可自训 ≤8B，监控器需 API 或 70B 级推理", 主要成本="API 监控调用", 风险="安全方向，评审口径不同"),
 "L-Q010": dict(热度="测试时扩展 0.52×、过度思考 0.44×，在下降", 最小实验="按每个正确答案的端到端成本，跨 batch 比较量化与 TTC", 证据论文规模="≤32B 量化推理", 适配="中：算力可行，但方向热度在降", 主要成本="系统测量工作量", 风险="偏系统测量，主会创新性论证较难"),
 "A-Q001": dict(热度="Agentic RL（见 Agentic RL 图）", 最小实验="≤8B 多轮工具 GRPO，多种子，大 k 覆盖评测", 证据论文规模="4–8B 为主，个别到 235B", 适配="中–高：8×A100 可做，多种子耗时", 主要成本="大 k 采样评测", 风险="分歧多，需要先对齐口径"),
 "A-Q002": dict(热度="Agentic RL", 最小实验="定位信用 / 随机信用 / 均匀稠密 / 二值稀疏 四组对照", 证据论文规模="≤9B；[10] 8×A100 训练 12 小时、16×A100 训练 16 小时", 适配="高：实验卡可做，预研卡可在小模型上起步", 主要成本="低–中", 风险="多数方法论文未设随机信用对照，空间清楚"),
 "A-Q003": dict(热度="Agentic RL；与 L-Q001 相邻", 最小实验="把特权信息可获得性作为变量，在 AppWorld/BFCL 上比较 OPSD 与 GRPO", 证据论文规模="4–32B；[15] 用 A100", 适配="高", 主要成本="agent 环境的轨迹采样", 风险="与你的 opsd_thinking_q001 相邻，可作延伸而非新方向"),
 "A-Q004": dict(热度="Agentic RL；奖励作弊", 最小实验="在可控测试床上跟踪捷径出现时刻与监控召回的变化", 证据论文规模="7B 测试床（[25] H100 FSDP，1000 样本）至 235B", 适配="中–高：小测试床可做", 主要成本="监控标注", 风险="中"),
 "A-Q005": dict(热度="Agentic RL", 最小实验="单模拟器与多模拟器训练，换模拟器评测", 证据论文规模="≤9B；[32] 8×A100，[34] 2×B200 两天", 适配="高", 主要成本="多个模拟器需要 API 或开源 ≥27B 推理", 风险="中"),
 "A-Q006": dict(热度="Agentic RL；系统方向", 最小实验="缺 old logits 时的离策略校正与陈旧度对照", 证据论文规模="4–30B，异步 RL 框架", 适配="低–中：需要异步 RL 基础设施", 主要成本="工程量大", 风险="偏系统"),
 "A-Q007": dict(热度="Agentic RL；多智能体", 最小实验="共享策略与独立策略的多智能体 RL，多种子", 证据论文规模="≤4B；双卡 H100 与 L40s", 适配="高：预研卡即可起步", 主要成本="低", 风险="原证据只有单种子"),
}

NEW_EVIDENCE = {
 "L-Q001": [{
   "作品ID": "arXiv:2610.26397", "标题": "Bridged Self-Distillation for On-Policy Learning",
   "机构": ["Technical University of Munich", "LMU Munich", "Munich Center for Machine Learning"],
   "原文链接": "https://arxiv.org/abs/2610.26397", "位置": "全文 HTML，由 WebFetch 抽取（非检索片段脚本）", "阅读版本": "arXiv HTML 当前版本",
   "证据角色": "原始实验", "实验设置": "学生 Qwen3-0.6B/1.7B/4B/4B-Instruct-2507；外部教师 Qwen3-32B、Nemotron-3-30B-A3B、GPT-5.6 Luna；AIME24/25、HMMT25，Avg@4",
   "变化变量": "Bridged Self-Distillation 与 vanilla OPD", "对照与保持条件": "同一学生与教师配对，共 12 组",
   "具体观察": "Qwen3-4B 配 Qwen3-32B 教师：Bridged 63.9，vanilla OPD 60.3，基座 59.2；12 组相对基座提升 1.2–4.7 分",
   "成本口径": "训练、评测和消融合计约 1450 H100/H200 GPU 小时",
   "证据边界": "教师是外部模型，不是同一模型加特权上下文，不能直接回答本卡的 OPSD 退化问题；评测预算未在抽取中给出；数值来自小模型抽取，需用检索片段脚本复核"}],
 "L-Q006": [
  {"作品ID": "arXiv:2610.34073", "标题": "Memory Tax: Dissecting the Net Value of Agent Memory",
   "机构": ["University of Illinois Urbana-Champaign", "Tsinghua University", "Renmin University of China", "Verdent.ai", "University of Waterloo"],
   "原文链接": "https://arxiv.org/abs/2610.34073", "位置": "全文 HTML，由 WebFetch 抽取（非检索片段脚本）", "阅读版本": "arXiv HTML 当前版本（v1 2026-10-25）",
   "证据角色": "原始实验", "实验设置": "Qwen3.5-4B、Qwen3.6-27B、GPT-5.6 Luna(low)；会话记忆、经验记忆、世界模型记忆三类基准，含 LongMemEval-s、ALFWorld、AppWorld、τ²-Bench 等",
   "变化变量": "记忆系统与朴素 RAG", "对照与保持条件": "共享 Qwen3-Embedding-0.6B 嵌入器，Qwen3.6-27B 作判官",
   "具体观察": "LongMemEval-s + Qwen3.5-4B：OpenViking 记忆系统 31.8%，两轮朴素 RAG 72.2%，相差 40.4 分。作者把净值分解为设计收益与'税'，税指记忆处理隐藏或丢弃证据",
   "成本口径": "纯推理评测", "证据边界": "只抽取到最强一例；税的分解方法与条目级归因细节未读；需用检索片段脚本复核"},
  {"作品ID": "arXiv:2610.30755", "标题": "Is Complex Agentic Memory Always Needed? Naive RAG Is Stronger Than We Thought",
   "机构": [], "原文链接": "https://arxiv.org/abs/2610.30755", "位置": "全文 HTML，由 WebFetch 抽取", "阅读版本": "arXiv HTML 当前版本",
   "证据角色": "原始实验", "实验设置": "GPT-4o-mini、GPT-4.1-mini、DeepSeek-V4-Flash、Qwen3.5-35B-A3B；LoCoMo、LongMemEval、MEME、MemoryAgentBench",
   "变化变量": "记忆系统与 Raw-RAG（稠密检索加重排）", "对照与保持条件": None,
   "具体观察": "Raw-RAG 在 7 个设定中 6 个排第一；MemoryAgentBench + DeepSeek-V4-Flash 总分 53.41，次优记忆系统 Memora 47.88",
   "成本口径": "纯推理评测", "证据边界": "机构待核实（HTML 未给出机构），不计入合格样本，只作背景"}],
}
NEW_STATUS = {
 "L-Q006": "本周（2026-10-25 前后）两篇系统评测显示多数记忆系统净值不如朴素 RAG，并把损耗归为证据被隐藏或丢弃。原卡'条目级损失归因缺失'可能已被 Memory Tax 部分覆盖，需读其分解方法后确认；剩余部分集中在流式整合随更新次数变坏的时间动态。",
}

def load(p, prefix):
    j = json.loads(p.read_text(encoding="utf-8"))
    cards = []
    for c in j["研究问题"]:
        c = copy.deepcopy(c); old_id = c["id"]; c["id"] = f"{prefix}-{old_id}"
        c["继承自"] = f"{p.parent.name}/研究问题.json 的 {old_id}"
        c["与其他问题的关系"] = [f"{prefix}-{x}" if isinstance(x, str) and x.startswith("Q") else x for x in c.get("与其他问题的关系", [])]
        cards.append(c)
    return j, cards

import sys as _sys; _sys.path.insert(0, str(Path(__file__).parent))
from 新增卡片 import NEW_CARDS, EXTRA_EVIDENCE, EXTRA_STATUS
jl, cl = load(OLD_L, "L"); ja, ca = load(OLD_A, "A")
cards = cl + ca
for c in cards:
    c["算力评估"] = ASSESS[c["id"]]
    if c["id"] in NEW_EVIDENCE:
        c["证据"] = c["证据"] + NEW_EVIDENCE[c["id"]]
    if c["id"] in NEW_STATUS:
        c["尚未解决"] = NEW_STATUS[c["id"]] + " 原判断：" + c["尚未解决"]
    if c["id"] in EXTRA_EVIDENCE:
        c["证据"] = c["证据"] + EXTRA_EVIDENCE[c["id"]]
    if c["id"] in EXTRA_STATUS:
        c["尚未解决"] = EXTRA_STATUS[c["id"]] + " 此前判断：" + c["尚未解决"]
    c["查新状态"] = (c.get("查新状态") or "") + "；2026-10-29 补充：在 81 个主题、8534 篇候选内做了标题与摘要层检索，未做针对性查新"
cards = cards + NEW_CARDS

out = {
 "领域": "大语言模型热门方向（按算力适配重排）：继承 LLM新兴领域研究地图_20261021 与 AgenticRL研究地图_20261021 的 17 张卡，并在 81 个主题、8534 篇候选上重扫半年窗口，新增 4 张卡",
 "检索日期": "2026-10-29",
 "近期窗口": ["2026-04-28", "2026-10-28"],
 "机构口径": "ai-frontier-search 白名单加 QS 2027 前 50；继承卡片的证据沿用旧图核实结果；新增证据的机构均经作者区片段核实；2610.30755、2609.35870、2610.04433、2610.36346 机构不合格或待核实，只作背景",
 "算力口径": {"预研": "2×A100 80G / 4×L40 48G / 8×4090 24G", "实验": "8×A100 80G", "API": "1000 元以内可自主决定", "token": "稀缺"},
 "研究问题": cards,
}
OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print("cards", len(cards), [c["id"] for c in cards])
