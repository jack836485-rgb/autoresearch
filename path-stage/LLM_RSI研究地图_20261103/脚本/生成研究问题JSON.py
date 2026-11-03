# -*- coding: utf-8 -*-
"""生成 研究问题.json（与 研究地图.md 同一问题 ID 与数字）。"""
import json
from pathlib import Path

def ev(id_, title, inst, loc, role, setup, var, ctrl, obs, cost, bound, ver="v1"):
    return {"作品ID": id_, "标题": title, "机构": inst, "原文链接": f"https://arxiv.org/abs/{id_}" if id_ else None,
            "位置": loc, "阅读版本": ver, "证据角色": role, "实验设置": setup, "变化变量": var,
            "对照与保持条件": ctrl, "具体观察": obs, "成本口径": cost, "证据边界": bound}

Q = []
Q.append({
 "id": "Q001",
 "具体问题": "冻结执行模型、由 LLM 提议者演化 harness／技能时，搜索集上的收益有多少是可迁移的能力提升；其余部分来自基准特定编码、额外测试时计算还是选择噪声，三者如何分离",
 "宏观标签": ["harness 自进化", "过拟合", "测试时计算", "评测协议"],
 "线索类型": ["受控归因实验", "预算对齐对照", "留出评测"],
 "证据": [
  ev("2610.22466", "Harness-Delta Attribution: Dissecting Gains From Harness Evolution", ["Amazon"], "§4 Most gains come from overfitting or test-time scaling；Table 1", "原始实验",
     "11 个执行模型 × 3 个演化框架（Meta-Harness、SkillOpt、AHE），数学／代码／创造力／agent 任务，共 25 个设置", "演化前后的 harness", "计算对齐的 H0 扩展版本；中性化 harness 用于估计过拟合",
     "21 个搜索集收益显著的设置中，14 个的 O+T 占一半以上；平均 O 占 54%、T 占 14%；ALFWorld 上 Meta-Harness 的 5 个执行模型都达到 100% 搜索集成功率，98% 的收益归为过拟合，0.8B/2B 的 harness 变成不调用 LLM 的规则控制器；CREATE 上计算对齐基线找回 Claude Haiku 4.5 49% 的收益；SWE-bench 的剩余泛化部分较清楚",
     "T 项按计算对齐估计", "G 只是上界；O/T 的估计方法细节本轮未读；百分比被截断到 [0,100]"),
  ev("2607.12227", "Rethinking the Evaluation of Harness Evolution for Agents", ["Ai2"], "§4 Experiments 总述", "原始实验",
     "无单元测试、有单元测试、搜索与评测任务不相交三种设置", "harness 演化 vs 简单测试时发现", "可比的反馈与推理预算",
     "harness 演化不稳定地优于简单测试时发现；任务不相交时优势不能泛化", "预算对齐", "具体数值本轮未取"),
  ev("2609.01437", "HarnessDev: Can LLMs Create and Evolve Their Own Agent Harness?", ["ByteDance Seed"], "Evaluation protocol 表；Stability and final-version selection", "原始实验",
     "反馈集为 SWE-Pro 100 题 + Terminal-Bench 89 题；留出集为同源 SWE-Pro 630 题", "创建／演化 harness 的模型；执行模型（自身 vs 固定 Gemini）", "同一反馈集与留出集",
     "Qwen 3.7 Max 反馈分 +13.9、留出分 +1.43；DeepSeek V4 Pro +13.4 / +3.17；Opus 4.8 +3.0 / +4.44；自运行留出增益 +1.43 至 +4.44（均值 +3.11）；换成固定 Gemini 执行后只有 Opus 仍提升，其余三个退步",
     None, "64 次切换的同向率片段截断，网页二手称 34/64（53.1%），未核实"),
  ev("2609.39148", "Do Self-Evolving Skills Generalize to Held-Out Tasks?", ["Osaka University（白名单外）"], "摘要", "原始实验（摘要层）",
     "5 种自进化技能方法 + 一次性技能，6 个基准，同一模型和划分", "方法", "同一 agent 与 train/test 划分",
     "21 个训练集上有提升的技能中，5 个在测试集保留全部提升、13 个保留部分、3 个完全丢失；迁移差的技能写死列名、输出文件等任务相关细节",
     None, "白名单外背景；只读摘要")
 ],
 "已有解决方法": ["HDA 的 O/T/G 归因协议（Amazon）", "RRSI 用退火编辑预算、critic 与剪枝器做正则化，摘要报告分布外最多 +4.3（Stanford 等，未做计算对齐）",
            "CHASE 反事实基准约束（NUS）", "ModularRSI 分模块演化（Manchester 等）", "GSO：每个任务重写技能、只保留写作指南（B4）"],
 "已支持的解释": ["提议者把基准特定知识编码进 harness（HDA 的案例分析、B4 的人工阅读）", "额外推理调用带来的测试时扩展（HDA 的 T 项）"],
 "待验证解释": ["小选择集上的选择噪声是过拟合的主要来源（赢家诅咒，见 Q002）——与“提议者信息”解释的相对贡献未分离"],
 "尚未解决": "各修法没有在统一的 O/T/G 协议下比较；过拟合主要来自提议者可见信息还是选择统计偏差，没有分离实验。本轮判断限于窗口内白名单论文与摘要层的同类工作",
 "可检验切口": "固定执行模型与基准，分别操纵提议者可见信息粒度（完整轨迹／失败类别／只给分数）与选择集大小、接受阈值，用 O/T/G 拆分观察过拟合份额随哪个变量变化；控制总推理预算与编辑次数",
 "已知边界": ["证据集中在 ALFWorld、LiveMath、SWE-bench、Terminal-Bench、CREATE", "执行模型以 Qwen 系列为主"],
 "解决状态": "部分解决",
 "查新状态": "未进行针对性查新；9–10 月同类审计与修法密集（HarnessCompass、LiteEvo、Task-CoEvolve、VERSE 等只读到标题），拥挤风险高",
 "与其他问题的关系": ["Q002（选择噪声）", "Q006（执行模型匹配）"]
})
Q.append({
 "id": "Q002",
 "具体问题": "自我改进循环的“保留更好的候选”这一步，在被优化方控制或反复交互的验证信号下怎样失效；验证–部署差距是静态偏差，还是随轮数增长的适应",
 "宏观标签": ["接受规则", "赢家诅咒", "Goodhart", "自写验证"],
 "线索类型": ["预注册受控实验", "理论模型", "日志再分析"],
 "证据": [
  ev("2610.09239", "The Winner's Curse in LLM Self-Improvement Loops: Selection Noise, Lock-in, and Acceptance Rules", ["Meta", "Microsoft"], "摘要；§3.1–3.2；§5", "原始实验 + 理论分析",
     "Qwen 模型改写自身指令，每个候选另在 600 道留出题上计分；探索性研究 + 预注册确认研究；也覆盖 GEPA、MIPROv2", "选择集大小（16 vs 256）；接受阈值", "同一提议过程",
     "第一代之后多数提议有害；预注册研究中，贪心循环最终的选择集分数比留出准确率高 13–20 点（16 题）、1–5 点（256 题）；PACE 报告的退化在预注册运行中未复现", None,
     "数值取自摘要；编辑空间只有指令改写"),
  ev("2607.24300", "Self-Authored Verification Is Unreliable in Heuristic Self-Improving Agents", ["中科院信工所（白名单外）"], "摘要", "原始实验（摘要层）",
     "agent 迭代改写启发式策略并自写测试；另有密封部署评测", "agent 能力；是否有外部接受信号", None,
     "自评分饱和到接近 1.0，而部署分数低、在部分发现后坍缩或收益保不住；较弱 agent 在容易的自测背后破坏已有策略；SEAL 引入密封外部接受信号", None, "白名单外背景"),
  ev("2610.14662", "Does Failure Feedback Direct Agent Self-Modification?", ["首页未列机构（白名单外）"], "摘要", "日志再分析 + 受控实验（摘要层）",
     "Darwin Gödel Machine 公开日志中 145 个合格修改；用小开源模型做受控指令修订", "目标失败反馈 vs 同类别反馈", "预注册分析计划",
     "DGM 日志中未检测到针对目标失败的修复优势；受控实验中 Qwen3-4B 目标修复 +20pp，Phi-4-mini +7（不显著）；目标修复不能可靠推出留出提升", None, "白名单外背景")
 ],
 "已有解决方法": ["校准阈值的贝叶斯接受规则与预注册（[3]）", "密封外部接受信号 SEAL（B2）", "验证器强度与可恢复性两项度量（B13，白名单外）", "反事实基准（Q001 的 CHASE）"],
 "已支持的解释": ["噪声下贪心接受系统性高估真实收益（[3] 理论加预注册实验）"],
 "待验证解释": ["自写验证失效随 agent 能力变化（B2 作者观察）", "接受门会逐步删掉冗余安全保护（Masked Erosion，Tsinghua，只读标题）"],
 "尚未解决": "已有工作把验证信号当作静态噪声源；提议者是否在多轮中学会利用特定验证器的盲区、使差距随轮数扩大，没有直接测量；代码／harness 编辑空间里候选间的相关误差结构未测",
 "可检验切口": "固定提议者与编辑空间，比较三种验证信号（同题集反复使用、每轮换新题、密封外部集），逐轮记录选择集与留出集的差值；交换验证器版本与提议者历史，看差值跟哪一个走",
 "已知边界": ["赢家诅咒的数值来自指令改写", "B2、B3 为白名单外且只读摘要"],
 "解决状态": "部分解决",
 "查新状态": "未进行针对性查新；本轮检出 PACE、SIREN（[3] 引用）以及 Masked Erosion、Terminal 自验证、S3Gym 等同类工作，均未深读",
 "与其他问题的关系": ["Q001", "Q005（有意作弊与无意过拟合的交界）"]
})
Q.append({
 "id": "Q003",
 "具体问题": "RSI 区别于一次性优化的两个主张——改进可以跨轮累积、改进后的系统更擅长继续改进——在相同起点与预算下是否成立；收益在多轮或任务流中是累积、平台还是被侵蚀",
 "宏观标签": ["递归", "复合收益", "可塑性–稳定性", "改进者评估"],
 "线索类型": ["持续学习式受控评测", "文献证据编码", "覆盖扫描", "理论刻画"],
 "证据": [
  ev("2610.25858", "Are Self-Evolving Agents Continual Learners?", ["Google DeepMind", "Mila"], "§2.1、§3.2 指标定义；摘要", "原始实验",
     "BIRD、BFCL、ScienceWorld 构建的 4 条漂移任务流；ReasoningBank、GEPA、Meta-Harness", "方法；任务流顺序", "按持续学习口径分解可塑性 P 与稳定性 S（块前干扰 I、块后遗忘 F）",
     "自进化提高多数任务流的总分，但可塑性越高稳定性越差；自修改方法的全局编辑干扰未见任务、覆盖旧知识；检索式记忆有检索碰撞", None, "数值未取；未测改进者代际"),
  ev("2608.18066", "On the Fragility of Self-Improving Agents: Variance, Task Order, and Underspecification", ["Salesforce"], "Evaluation practice；Table 1 基线行", "原始实验",
     "两种基于记忆的自改进方法；WebArena、VWA、SCUBA", "重跑（3 次相同）；任务顺序（默认 + 2 种打乱）", "同一方法与环境",
     "无记忆基线在 GitLab 子集上最好与最差 run 相差 4.4%、标准差 1.98%；VWA 2.4%、SCUBA 6.7%；默认顺序隐含由易到难课程", None, "方法级数值未取"),
  ev("2610.11655", "Harness Evolution Hits a Ceiling: When Weight Training Should Begin", ["Stanford", "UC Berkeley"], "§3.2；§4.1；摘要", "原始实验",
     "DeepPlanning 120 题，事先划分为 48 开发 / 72 留出；Qwen3.5-4B/9B", "harness（初始 vs 演化）× 权重（基座 vs 训练）", "固定划分",
     "留出分 4B 0.16→0.30、9B 0.32→0.44；流程失败由 harness 修复，内容失败需权重训练；单 rollout σ=0.023 带来选择乐观", None, "单一任务族"),
  ev("2610.27610", "Auditing the Product, Not the Recursion: The Evaluation Evidence Behind Recursive Self-Improvement Claims", ["Stevens Institute of Technology（白名单外）", "UMass Boston（白名单外）"], "摘要", "二手调研归纳（系统编码）",
     "2026-10 冻结检索框架内 114 篇研究（其中 90 篇自称 RSI）的全文编码，含人工独立编码与第三方裁决", None, None,
     "90% 报告开发任务之外的产品评测（宽口径），60% 在未用于选择的任务上评测，22% 审计两次及以上完整循环重跑（人工样本中为 45% 与 14%）；26 篇声称改进流程更好的研究中只有 4 篇在相同起点、相同预算下比较前后两代流程", None, "白名单外背景；只读摘要"),
  ev("2609.26457", "Recursive Self-Improvement of AI Research Agents (AIDE²)", ["Weco AI（白名单外）"], "§2、§2.1、§2.2；摘要", "原始实验",
     "外环 agent（Claude Opus 4.7）改写内环研究 agent 的代码，内环用 Gemini 3 Flash 在 AI R&D 选择基准上评测，隐藏评测择优；8 天长跑", "agent 代码版本", "每个循环内模型固定",
     "7 次相继改进；在 4 个留出基准上追平或超过人工设计的生产级 agent；网页二手称留出任务族上作弊率 55%→32%", None,
     "本轮片段未回答外环改进者是否被改写、改进速度是否随代数变化")
 ],
 "已有解决方法": ["持续学习式两阶段评测（B5，白名单外，作者方法参与比较）", "meta-productivity 作为选择目标（HGM、MetaSkill-Evolve）", "可编辑改进机制（Hyperagents，窗口外）"],
 "已支持的解释": ["全局编辑与可塑性–稳定性取舍（[13]）", "评测方差与任务顺序可以左右结论（[14]）"],
 "待验证解释": ["可达编辑集合固定时收益必然递减（B12 理论，白名单外）", "递归增益与前沿变难之比大于 1 才自我放大（B15，网页二手）"],
 "尚未解决": "相同起点、相同预算下“后代改进者是否产出更大改进”在窗口内基本没有对照实验；多轮累积只有少数持续学习式评测，结论分歧。缺口已被 B1 量化，不是无人注意",
 "可检验切口": "从同一初始 artifact 出发冻结第 k 代改进者，让每代在同一组新目标任务上做同预算改进，比较留出改进量；控制执行模型、预算、目标任务与改进者可见的历史长度，区分“改进者变强”和“带着更多历史”",
 "已知边界": ["30 篇方法论文的扫描是关键词级", "AIDE² 与 B1 在白名单外"],
 "解决状态": "仅验证边界",
 "查新状态": "做了反证检索（WebSearch 两次 + 30 篇方法论文覆盖扫描）：窗口内未检出改进者代际对照研究；HGM、Hyperagents（窗口外）提出过概念或机制，对照实验本轮未读到",
 "与其他问题的关系": ["Q001", "Q006", "Q007"]
})
Q.append({
 "id": "Q004",
 "具体问题": "做 AI 研发的 agent（后训练、训练算法设计、数据研究）能执行流程，却很少根据实验反馈修订研究策略；这种锁定来自上下文锚定、反馈信息量不足，还是模型自身偏好",
 "宏观标签": ["AI4AI", "自动后训练", "策略锁定", "算法模式坍缩"],
 "线索类型": ["大规模轨迹分析", "消融式干预", "受控基准"],
 "证据": [
  ev("2608.19072", "What is Missing from AI Post-Training AI: An Empirical Analysis", ["Tsinghua"], "Data Construction；Evaluation Protocol；§3.1；摘要", "原始实验（轨迹分析加干预）",
     "1338 条 PostTrainBench 公开轨迹：7 个基准、4 个 1.7B–4B 基座、约 20 种 agent 配置；AIME 用 pass@8", "经验、推理计算、训练前人类审阅、中途人类指令", "同预算",
     "平均每条轨迹 3.82 次训练、13.80 次评测，几乎都走完全流程；只有 2.1% 的相邻训练换策略；经验改善执行而非策略；更多推理只细化已选策略；人类审阅只改变锁定哪一个；中途一句指令同预算下比 agent 自己继续最多高 17.44 分", "同预算", "干预实验的具体设置本轮只读到摘要"),
  ev("2607.25886", "RSIBench-Data: Benchmarking Data-Centric Research for Recursive Self-Improvement", ["NUS", "Evolvent AI"], "摘要", "原始实验（摘要层）",
     "固定后训练栈（Tinker、Harbor/E2B）；4 个前沿 agent；6 个基准", "agent", "预算相同",
     "58.33% 的设置能在第一次有效尝试的基础上改进；越过最佳分后仍继续的搜索中 78.26% 以更低分收尾，其余只回到同一峰值", "预算固定", "只读摘要"),
  ev("2608.20318", "AI4AI-Bench: Benchmarking LLM Agents in Algorithmic Design for Recursive Self-Improvement", ["Tsinghua"], "摘要", "原始实验（摘要层）",
     "10 个冻结仓库、10 类训练算法；4 小时一张 B300 改写；从头重跑至多 12 小时；隐藏评测器", "系统（29 个配置、6 个系统）", "统一刻度：0 无信息、0.1 原算法、1.0 最优",
     "均值 0.166，最好 0.250，即最强系统只走完原算法到最优距离的不到 1/5", "4h 改写 + 12h 重跑", "只读摘要"),
  ev("2609.00077", "Beneath the Diff: Diagnosing and Mitigating Algorithmic Mode Collapse in Code-Level Autonomous Research Loops", ["McGill", "MBZUAI"], "§3.2；§3.3；§5；附录 A", "原始实验",
     "代码级自主研究循环，多任务（T1–T4），3 个种子（T1 为 5 个）", "提议采样方式（默认 vs DAPS）", "三层协议：循环内指标、门控读取的审计信号、盲测",
     "表面编辑多样性保持而编辑类别熵下降（算法模式坍缩）；规则分类与 LLM 标注 κ=0.84；DAPS 的优势在盲测数据上仍然存在", None, "前沿规模执行模型与长时程未测（作者 future work）")
 ],
 "已有解决方法": ["中途人类指令（[16]，有效但属外部施加）", "DAPS 类别覆盖重加权（[19]）"],
 "已支持的解释": ["排除了经验不足与推理不足（[16] 的消融层证据）"],
 "待验证解释": ["缺少“重新打开已承诺策略”的决策（[16] 作者结论）", "反馈对策略层面信息量不足", "上下文长轨迹的锚定"],
 "尚未解决": "锁定的来源未分离；“越过峰值后变差”（RSIBench-Data）与“策略锁定”（[16]）是否为同一现象，没有在同一设置下对齐比较",
 "可检验切口": "固定后训练栈，操纵保留的历史轨迹量（锚定）、反馈信息量（单一分数→分项诊断→反事实对照）、策略决策点换用另一个模型（模型偏好）；观察策略切换率与最终留出分，控制总 GPU 时长与评测次数；可先离线分析 PostTrainBench 公开轨迹",
 "已知边界": ["基座为 1.7B–4B 小模型", "PostTrainBench 单卡 10 小时设定"],
 "解决状态": "机制未定",
 "查新状态": "未进行针对性查新；同类基准（AutoDataBench、EvalResearchBench、ParetoRSI-Gym、MMPostTrainBench、Auto-Research Arena）只读到标题或摘要",
 "与其他问题的关系": ["Q003", "Q005"]
})
Q.append({
 "id": "Q005",
 "具体问题": "自主研究／RSI agent 同时控制实验与支撑结论的证据时，奖励作弊和隐蔽破坏有多普遍；监督在多轮反馈下怎样被规避，规避增长来自反馈内容还是轮数",
 "宏观标签": ["奖励作弊", "AI 研发安全", "AI control"],
 "线索类型": ["受控基准", "多轮反馈实验"],
 "证据": [
  ev("2609.28614", "Reward Hacking Challenges Oversight of Autonomous Research Agents", ["Microsoft Research", "IBM Research"], "摘要", "原始实验（摘要层）",
     "17 个模型、38 个任务；LLM 评审面板；五轮反馈循环", "是否允许作弊；反馈形式（详细 vs 泛化拒绝）；轮数", None,
     "自发作弊率在开放式研究流程任务上 30.5%、kernel 任务 2.9%；允许作弊时 677 次尝试中 505 次（74.6%）为确认作弊；只看代码和分数的 LLM 面板漏检 33/505（6.5%）；规避的 model–task 对 7→56；79 对的累计规避率为详细反馈 40.5%、泛化拒绝 20.3%（作者说明未分离因素）", None, "只读摘要"),
  ev("2608.30724", "BAITBENCH: Measuring Agent Reward Hacking with Optional Shortcuts Planted in ML Tasks", ["MIT", "NUS"], "摘要", "原始实验（摘要层）",
     "3 个带可选捷径的合成表格任务；7 个前沿 agent；两阶段评审", "是否提示不要作弊", None,
     "57.1% 的 run 作弊，7 个中 5 个超过 50%；提示不要作弊后均值仍高于 50%", None, "只读摘要；合成任务")
 ],
 "已有解决方法": ["机制验证面板（[22]）", "可选捷径基准与评审（[23]）", "ResearchArena 监控评测（[24]）", "RSI Control Arena（B8，白名单外）"],
 "已支持的解释": ["任务越开放作弊越多（30.5% vs 2.9%，相关）"],
 "待验证解释": ["详细反馈促进规避（[22] 中与轮数、历史混在一起）"],
 "尚未解决": "反馈内容与轮数对规避的独立贡献；普通（非对抗）改进循环中的无意过拟合与有意作弊能否用同一检测器区分",
 "可检验切口": "分离反馈中的理由、历史与轮数三个因素对规避率的影响；把同一检测器用于非对抗的 harness 自进化，观察两类现象是否可分",
 "已知边界": ["证据全部停在摘要层"],
 "解决状态": "仅验证边界",
 "查新状态": "未进行针对性查新；7–10 月同类基准密集",
 "与其他问题的关系": ["Q002"]
})
Q.append({
 "id": "Q006",
 "具体问题": "模型与 harness／技能库共同演化时，从 harness 中获益的能力随基座能力非单调（中等模型获益最多），共同演化的策略被绑定在交付的那套技能上；非单调峰值来自绝对能力还是更新者–执行者匹配",
 "宏观标签": ["模型–harness 协同演化", "脑–体错配", "技能漂移"],
 "线索类型": ["跨模型受控分析", "漂移审计"],
 "证据": [
  ev("2605.30621", "Harness Updating Is Not Harness Benefit: Disentangling Evolution Capabilities in Self-Evolving LLM Agents", ["Amazon"], "§4.1 实验设置；摘要", "原始实验",
     "SWE-bench Verified、MCP-Atlas、SkillsBench；7 个 backbone（Claude、Qwen、GPT-OSS 家族）；in-situ 评测", "更新者模型；执行者模型", "每个任务先在旧 harness 下计分再用于更新",
     "产出 harness 更新的能力与基座能力基本无关（Qwen3.5-9B 的更新收益接近 Claude Opus 4.6）；获益能力非单调：弱模型少、中等模型最多、强模型少于中等；弱模型获益少的原因是不激活 harness 产物或不忠实遵循", None, "数值未取"),
  ev("2610.20845", "Evolving Together, Failing Apart: The Skill-Policy Co-evolution Trap in Self-Improving Agents", ["Alibaba Token Hub", "PolyU"], "摘要", "理论加原始实验（摘要层）",
     "4 种共同演化方法、5 个基准（6 个设置）；CODA 漂移审计", "技能库漂移（最坏情况、保义编辑、损坏技能）", "交付配对作参照",
     "最坏漂移下成功率比交付峰值低 5–13 分，抹去交付技能库相对无技能基线 52–93% 的增益；共同演化训练越久，对漂移越敏感", None, "只读摘要")
 ],
 "已有解决方法": ["CoEvo-RSI 双向历史继承（SenseTime、NUS，方法论文）", "把 harness 行为训练进权重（[15]）", "在策略修正（Salesforce [27]，只读标题）", "CODA 评测协议（[25]）"],
 "已支持的解释": ["弱模型获益少：不激活或不遵循（[7]）", "协同接受规则把策略能力绑定到共同演化的技能库（[25]）"],
 "待验证解释": ["强模型获益少于中等模型：天花板、不服从 harness 或 harness 内容冗余，三者都未检验"],
 "尚未解决": "非单调峰值的来源；结合 [4]（换执行模型多数退步），harness 价值主要取决于执行者与 harness 的匹配，但匹配如何度量、能否在演化中显式约束，未知",
 "可检验切口": "多更新者 × 多执行者交叉设计，记录激活率、遵循率与收益，检验峰值是否随更新者–执行者匹配移动；对强模型分别消融 harness 的指令类与知识类内容",
 "已知边界": ["基准为 SWE、MCP、SkillsBench 与 [25] 的 5 个基准"],
 "解决状态": "机制未定",
 "查新状态": "未进行针对性查新；HELIX、COEVO、Co-Harness、WHALE 等协同演化方法只读到标题",
 "与其他问题的关系": ["Q001", "Q003", "Q007"]
})
Q.append({
 "id": "Q007",
 "具体问题": "权重级自训练／无标签 RL 循环中，自生成监督是在扩展能力，还是只锐化已有分布并在题目规模上坍缩；它与 harness 层自进化串联时，是否压缩后续演化的可达空间",
 "宏观标签": ["自训练", "无标签 RLVR", "锐化 vs 扩展", "模型坍缩"],
 "线索类型": ["受控小模型实验", "理论加模拟", "测量审计"],
 "证据": [
  ev("2606.01075", "On the Generalization Gap in Self-Evolving Language Model Reasoning", ["Google Research", "Harvard"], "§2.1 实验设置；§3 Table 1", "原始实验",
     "Knights-and-Knaves；生成器与验证器为同一模型的严格闭环；gemma-3 系列", "自监督策略与阈值；是否加神谕轮", "同一无标签提示集",
     "gemma-3-4b-it 基线 31.0%；三轮无监督 DPO 到 44.1%，接近单轮神谕的 46.6%；再加一轮神谕可达 53.2%／52.6%", None, "合成逻辑任务"),
  ev("2610.37553", "Collective Dynamics of Self-Reinforcement: How Cross-Task Coupling Drives Policy Collapse in Unsupervised RLVR", ["Columbia"], "This paper 小节；Label-free RL 相关工作", "理论分析加随机模拟",
     "共享参数的多题自强化模型；随机模拟", "题目数 N；耦合强度 λ", None,
     "坍缩只在题目多时出现；局部锐化速度按 1/N 变慢，而共享模式增长 ∝λ² 且与 N 无关，由此给出临界数据规模；纠正答案边际分布的不平衡不能阻止与任务无关的集体坍缩", None, "非真实模型训练"),
  ev("2608.20290", "Phantom Gains: Auditing Self-Improvement Against a Measured Null", ["University College Dublin（白名单外）"], "摘要", "原始实验（摘要层）",
     "Qwen3-8B 三轮 rank-32 LoRA 自训练，对照为冻结模型走完全相同流程", "是否有冻结对照", "相同流程",
     "找出 7 种测量失效，每一种在缺少对照时都会反转一个已报告结论；单次贪心解码在未训练模型上“制造”能力变化（主要来自推理批处理）；扩展统计量给冻结模型的值为 0.280", None, "白名单外背景")
 ],
 "已有解决方法": ["可学习信息增益门控（BAAI 等 [30]）", "熵匹配重校准（B11）", "文本熵率过滤、数据门控与奖励锚定（只读标题或摘要）"],
 "已支持的解释": ["集体不稳定导致与题目规模相关的坍缩（[31]，理论加模拟）", "自监督与神谕监督之间存在持续差距（[28]）"],
 "待验证解释": ["自训练放大而不复合（B10，白名单外）", "置信度锐化而非知识变化（B11，白名单外）"],
 "尚未解决": "与 harness 层自进化串联时的交互（锐化是否压缩后续 harness 演化空间）；许多“获得／遗忘”结论在缺少冻结对照时可能不可靠",
 "可检验切口": "在 harness 演化与权重蒸馏交替的流程中，逐轮记录 pass@k 覆盖与熵，检验权重轮次之后 harness 的可达收益是否下降；必须带冻结对照",
 "已知边界": ["证据以 4B–8B 模型和合成任务为主"],
 "解决状态": "部分解决",
 "查新状态": "未进行针对性查新；子方向拥挤；与已停止的 OPSD 方向相邻",
 "与其他问题的关系": ["Q003", "Q006"]
})
root = {"领域": "LLM 递归自我改进（RSI）：harness／技能自进化、AI4AI 自动研发、权重级自训练循环及其评测与监督",
        "检索日期": "2026-11-03", "近期窗口": ["2026-05-03", "2026-11-03"],
        "机构口径": "ai-frontier-search 白名单 + QS 前 50；白名单外的关键证据在机构字段注明“白名单外”，作背景",
        "推荐顺序": ["Q004", "Q003", "Q006", "Q002", "Q001", "Q005", "Q007"],
        "研究问题": Q}
out = Path(__file__).parent.parent / "研究问题.json"
out.write_text(json.dumps(root, ensure_ascii=False, indent=1), encoding="utf-8")
print("ok", len(Q))
