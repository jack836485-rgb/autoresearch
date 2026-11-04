# -*- coding: utf-8 -*-
import json
A="https://arxiv.org/abs/"
def ev(i,t,org,loc,role,setup,var,ctrl,obs,cost,bd):
    return {"作品ID":i,"标题":t,"机构":org,"原文链接":A+i if i else None,"位置":loc,"阅读版本":"v1","证据角色":role,"实验设置":setup,"变化变量":var,"对照与保持条件":ctrl,"具体观察":obs,"成本口径":cost,"证据边界":bd}
Q=[
{"id":"Q001","具体问题":"在真实自然语言任务（检索增强问答、Agent 决策、机器翻译、安全护栏、KBQA）上训练的 latent 推理模型，其报告的收益究竟来自 latent 链的输入特定内容，还是仅来自额外的计算步/共享连续前缀（pause-token 式效应）？在合成逻辑与化学任务上已观察到“删除链会伤、替换内容几乎不变”，但这些应用方法本身未做内容替换或 pause 对照。",
 "宏观标签":["latent 推理忠实性","NL 应用","因果对照"],"线索类型":["受控失败实验","跨论文共同遗漏"],
 "证据":[
  ev("2610.21182","Does Latent Chain-of-Thought Actually Reason? A Single, Unifying Taxonomy for Latent Reasoning",["UC San Diego","Adobe Research","NYU","University of Virginia"],"摘要；Models, Tasks, and Controls（p.4）","原始实验","21 组模型-任务配置：COCONUT/CODI/逐步监督三种配方 × ProsQA、PrOntoQA、GSM8k × GPT-2、Llama-3.2-1B-Instruct，T=6 个 slot","链删除 vs 内容替换","同一 checkpoint 与输入","逻辑任务上 COCONUT 常把答案放在别处；即使逐步监督得到有序链，也可能“删除伤性能、内容替换不改答案”（占位符）；算术任务上所有配方都依赖链内容。","未报告","任务只覆盖合成逻辑与 GSM8k，未含真实 NL 应用；数值细节本轮只读到摘要级描述"),
  ev("2610.34173","Reasoning or Just Prompting? Probing the Mechanism of Latent Chemical Reasoning",["NUS（PDF/HTML 作者区 QS 命中）"],"§4.1、§4.4","原始实验","化学 latent 推理模型；ChEBI-20 描述与分子优化任务","跨分子交换 latent 序列 Z、均值 Z、移除 Z、噪声","保持接收方输入与分子上下文 H10 不变","交换后保留匹配分数的 94.5–103.3%；ChEBI-20 METEOR 差 −0.0024（95% CI −0.0086~+0.0035），移除后 −0.0949；600 个交换的优化输出无一返回供体结构；均值 Z 也保分。作者解读为共享连续条件化而非分子特定推理。","未报告","单一领域；交换幅度小（α≈0.04–0.08），作者自述只评估固定解码接口"),
  ev(None,"本轮覆盖扫描：NL 应用类 latent 方法的对照",[],"资料/正文 覆盖扫描（pause/替换/删除关键词）+ 抽查","二手调研归纳","LatentRAG 2605.06285、ALAR 2606.02871、COLAGUARD 2605.29068、LatentMT 2607.18618、SALR 2609.20398、TAC-CoT 2611.01926、SynLat 2610.03839、Sep-Latent 2610.22924",None,None,"关键词扫描未检出内容替换/交换类对照；LatentRAG 与 SALR 的 pause/filler 命中经抽查均位于相关工作；LatentRAG 消融为去掉检索模型或解码损失。","不适用","零命中仅为关键词级；未逐篇读全文；COLAGUARD 首页 NVIDIA 命中为引用而非署名，部分应用论文机构未核实"),
 ],
 "已有解决方法":["2610.21182 提出区分“链表示什么”与“模型如何用链”的分类法，并在合成任务上调和以往占位符/叠加/阶段性因果角色的报告","2606.12689（白名单外）用 Pause/无课程匹配对照说明可观察模式不足以证明机制"],
 "已支持的解释":["在合成逻辑与化学任务上，latent 内容可被替换而性能基本不变（2610.21182、2610.34173 的替换实验）"],
 "待验证解释":["NL 应用中的收益主要来自额外前向计算或共享连续条件化（由化学论文作者提出，未在 RAG/Agent/MT 上检验）"],
 "尚未解决":"在真实 NL 应用任务及其各自训练配方下，latent 内容是否被使用；若不被使用，等计算量的 pause/学习前缀是否能复现收益。本轮未发现在这些应用模型上做内容交换对照的工作。",
 "可检验切口":"对公开的 NL 应用 latent 模型（或按其配方复现）做：内容交换（同任务供体）、均值 latent、删除、等长 pause/可学习共享前缀四种对照，观察任务指标与输出变化率；控制解码接口、latent 数与总计算量。",
 "已知边界":["证据集中在 ≤1.5B 与合成/化学任务","NL 应用论文多为方法论文，代码与权重可得性未逐一核实"],
 "解决状态":"仅验证边界","查新状态":"做了一次定向检索：除 2512.21711（Coconut 在 MMLU/HotpotQA 上表现为占位符并利用捷径，窗口外）外，未检出在 RAG/Agent/MT/护栏类 latent 方法上的内容对照研究；范围限本轮 arXiv 检索与上述正文扫描。",
 "与其他问题的关系":["Q002：若 NL 轨迹下 latent 内容不被使用，Q002 的保留率差异可能另有来源"]},
{"id":"Q002","具体问题":"在内容相同、仅表述更冗长的 NL 推理轨迹上（GSM8k-Aug-NL 对 GSM8k-Aug），直接监督的 latent CoT（CoLaR、C-MTP）明显退化而间接监督（CODI）基本不退化；退化来自缺少压缩压力（必须逐块拟合冗长文本），还是来自 teacher forcing 下的自回归误差累积？",
 "宏观标签":["监督范式","轨迹冗长度","暴露偏差"],"线索类型":["受控对比","作者未检验的解释"],
 "证据":[
  ev("2607.16972","Training Continuous Chain of Thought Models: A Tale of Two Regimes",["NYU（白名单外）"],"§4.3、表 4","原始实验","Llama-3.2-1B-Instruct / Qwen2.5-1.5B-Instruct，LoRA，自 CoT checkpoint 初始化；GSM8k-Aug-NL 训练，GSM8k-Test 评测","轨迹形式（结构化→半自然，约 2.5 倍长）与监督范式","同底座同数据","CODI 用 6 个 latent 得 47.82%；CoLaR-2 跌到 23.46%；C-MTP-2 用约 34 步得 43.49%。作者给出两点解释：间接监督有压缩压力；teacher forcing 造成训练-测试失配，误差经数学表达式级联。","latent 步数不等（6 vs 约 34）","机构不在白名单；两个解释均未被单独检验；单次运行情况本轮未读到"),
  ev(None,"用户本地 CoLaR 分析（L40LZX:/data/raid5/luzhenxing/colar/analysis）",[],"nl_vs_eq_tail_attention、latent_generation_locality 报告","原始实验（未发表）","CoLaR，Llama-3.2-1B-Instruct，CF5，同 500 道 GSM8K 测试题，单 checkpoint 单链","训练轨迹 EQ vs NL","同架构同题","NL 18.4% vs EQ 28.6%；两者生成时近窗注意力（同题同步号匹配）80.5% vs 78.2%，最后 3 个 latent 置零后原本正确题保留 7%/11%。","未报告","单 checkpoint、注意力为描述性证据；NL checkpoint 训练充分度未核"),
 ],
 "已有解决方法":["KaVa（2510.02312，窗口外）以压缩教师 KV 蒸馏缓解 NL 轨迹退化","间接监督（CODI）本身不受影响"],
 "已支持的解释":[],
 "待验证解释":["C-MTP 作者：压缩压力缺失；teacher forcing 误差级联（集中在数学表达式）"],
 "尚未解决":"两种解释的相对贡献；去掉填充词但保留表达式是否能恢复直接监督；误差是否集中在表达式 token。",
 "可检验切口":"在 GSM8k-Aug-NL 上对直接监督模型比较 teacher-forced（喂 gold 压缩目标）与自由展开的差距；构造只删填充词、保留表达式的轨迹；控制 latent 数与训练步数。",
 "已知边界":["≤1.5B、LoRA、GSM 系列"],
 "解决状态":"机制未定","查新状态":"本轮未进行针对性查新；KaVa、SLT 为已知相关修法",
 "与其他问题的关系":["Q003：误差累积解释与长链外推退化相关"]},
{"id":"Q003","具体问题":"latent 推理链在超过训练所见步数后外推时退化（例如训练 K≤4、推理 K=32），且多步 latent 状态趋于同一方向（秩坍缩）；这使“增加 latent 步数 = 测试时扩展”不成立。退化来自分布外状态漂移、秩坍缩，还是结果奖励无法提供逐步信号？",
 "宏观标签":["测试时扩展","长链稳定性"],"线索类型":["受控失败实验"],
 "证据":[
  ev("2609.37351","Port-Hamiltonian Latent Deliberation: Mitigating the Deliberation Drift Cliff in Test-Time Scaling",["未核实（首页未命中白名单）"],"§2.2；§6.1 表（EXP-12）；§6.2（EXP-14）","原始实验","多跳逻辑演绎，3 个种子；训练轨迹 K≤4","推理时 latent 步数 K","同模型同任务","Coconut：K=4 82.0%、K=16 71.4%、K=32 63.7%；RDT：91.3%→71.9%。","未报告","机构未核实；合成逻辑任务"),
  ev("2609.07406","Think Wider: Mitigating Latent Rank Collapse in Implicit Chain-of-Thought Reasoning",["HKUST"],"§3；图 1","原始实验","隐式 CoT 基线与谱正则","是否加 WIDER 正则","同基线","基线 latent 轨迹有效秩 1.49，正则后 3.82。","未报告","秩与准确率因果关系本轮未读"),
 ],
 "已有解决方法":["Port-Hamiltonian 约束（2609.37351）","WIDER 谱正则（2609.07406）","SLPO 代理策略与自适应停止（2607.19691，摘要级）"],
 "已支持的解释":[],
 "待验证解释":["无耗散约束导致 OOD 漂移（2609.37351 作者）","秩坍缩限制条件容量（2609.07406 作者）"],
 "尚未解决":"这些修法是否在真实 NL/数学任务上让更多步数带来收益；漂移与秩坍缩是否同一现象的两面。",
 "可检验切口":"同一模型在训练步数内外扫描 K，同时记录有效秩、状态范数漂移与正确率，比较不同修法；控制训练预算。",
 "已知边界":["证据多来自合成逻辑与小模型"],
 "解决状态":"部分解决","查新状态":"本轮未进行针对性查新；方向已较拥挤（多种修法并存）",
 "与其他问题的关系":["Q002"]},
]
out={"领域":"连续 latent 推理 / latent CoT（偏自然语言域）","检索日期":"2026-11-03","近期窗口":["2026-05-03","2026-11-03"],"机构口径":"ai-frontier-search 白名单 + QS 前 50；白名单外原始证据单独标注","研究问题":Q}
json.dump(out,open("研究问题.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
print("ok",len(Q))
