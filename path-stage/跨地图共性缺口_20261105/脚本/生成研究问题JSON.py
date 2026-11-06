# -*- coding: utf-8 -*-
"""生成 研究问题.json（与 研究地图.md 同一问题 ID、同一数值）。"""
import json
from pathlib import Path

def ev(pid, title, inst, url, loc, ver, role, setup, var, ctrl, obs, cost, bound):
    return {"作品ID": pid, "标题": title, "机构": inst, "原文链接": url, "位置": loc, "阅读版本": ver,
            "证据角色": role, "实验设置": setup, "变化变量": var, "对照与保持条件": ctrl,
            "具体观察": obs, "成本口径": cost, "证据边界": bound}

INH = "继承自旧 slot 的 Tier B 记录"

Q001 = {
 "id": "Q001",
 "具体问题": "同一产物（修复动作、蒸馏教师分布、harness/技能、上下文管理策略、KV cache）对不同消费模型的价值相反：生产方一侧的质量指标（评估器更强、教师更大、cache 更忠实、搜索集分数更高）为什么不能预测它对某个消费者的收益？是否存在跨产物通用、可事先测量的消费者侧量？",
 "宏观标签": ["消费者相对价值", "执行者匹配", "非单调受益", "教师/评估器选择"],
 "线索类型": ["受控失败实验", "跨论文共性", "更强生产者反而更差"],
 "证据": [
  ev("arXiv:2610.38610", "Repairs for Whom? Evaluator–Executor Mismatch in Selecting Repairs for Failed LLM Agents", [], "https://arxiv.org/abs/2610.38610",
     "§2 Problem Setup；§3 Experimental Setup 表；§5；摘要", "v1", "原始实验",
     "部署体 Qwen2.5-7B-Instruct 与 Llama-3.1-8B-Instruct（vLLM，T=0.7，top-p 0.95）；ALFWorld、WebShop 非筛选池各 60 条失败，另有网格世界与筛选池；单步候选修复；用部署体独立 rollout 标注部署价值",
     "选修复所用的评估器（部署体自 rollout、14B rollout、Llama rollout、贪心重放、LLM judge）", "失败轨迹与候选修复固定；同 rollout 预算比较",
     "同预算下用 14B rollout 为 7B 选修复，ALFWorld 损失 0.25、WebShop 0.07；每候选 20 次 14B rollout 不如 7B 自己 2 次；37 条分歧轨迹上每分支每执行者 30 次新鲜 rollout 确认两者偏好相反修复；贪心重放损失 0.08–0.13（ALFWorld）",
     "按 rollout 次数对齐；14B rollout 单次成本更高", "只覆盖单步修复与两种 7–8B 部署体；机构首页未见白名单署名"),
  ev("arXiv:2610.22016", "Close Enough is Nowhere Near: Fidelity-Consumability Decoupling in KV Caches", ["IBM", "MIT（QS 初筛）"], "https://arxiv.org/abs/2610.22016",
     "摘要（模型细节片段检索零命中）", "v1", "原始实验",
     "两侧冻结，把发送方 KV cache 替换给读者，不训练；8 种替换方法；锚点为无信息 cache 与读者自己读原文的准确率", "替换方法", "读者冻结；两个锚点",
     "全部 8 种方法停在无信息基线；与读者自身 cache 的几何相似度不预测可用性，失败非渐进；追加可注意上下文并只适配 query 侧的设计可行",
     None, "模型与任务细节本轮未取到；只覆盖 KV 载体"),
  ev("arXiv:2610.20959", "Same Context, Different Agents: A Behavioral Study of Semantic Layers, Orchestration and Compaction in Data Agents", ["UPenn（QS 初筛）"], "https://arxiv.org/abs/2610.20959",
     "§4.1、§4.2、§4.3、§4.6 表 2", "v1", "原始实验",
     "7 个 LLM，5 个基准共 1,514 个长程数据任务；语义层、编排、compaction 三种 CET 单独与组合", "开启的 CET 组合", "CET 效应取另两项各设置的平均；准确率变化给 95% bootstrap 区间",
     "无 CET 时 agent 聚为调查者、过早作答者、过早放弃者三组；编排对过早作答者收益最大、语义层对放弃者；对调查者每种 CET 都降低或不改变准确率且增加成本，最佳组合是不用 CET",
     "按标价计每任务美元", "数据 agent 场景；行为组由聚类得到"),
  ev("arXiv:2605.30621", "Harness Updating Is Not Harness Benefit: Disentangling Evolution Capabilities in Self-Evolving LLM Agents", ["Amazon"], "https://arxiv.org/abs/2605.30621",
     "§4.3 Agent-side Analysis；摘要；数值继承自 LLM_RSI研究地图_20261103 Q006", "v1", "原始实验",
     "多档基座在 SWE、MCP、SkillsBench 上做 harness 自进化，分别测更新能力与受益能力", "生成更新的模型、使用更新的模型", "固定骨干，只更新可编辑 harness 组件",
     "更新能力对基座近乎平坦（Qwen3.5-9B 的更新与 Opus 4.6 收益相近）；受益非单调（SWE：Qwen3-235B 19.3pp、Qwen3-32B 4.4pp、Opus 4.6 2.6pp）；弱模型受益少源于 harness activation 与 adherence 失败",
     None, "受益峰值只在两个基准上观察"),
  ev("arXiv:2609.20612", "What Does Privileged Information Add to On-Policy Self-Distillation?", ["NUS（QS 初筛）"], "https://arxiv.org/abs/2609.20612",
     "摘要", "v1", "原始实验",
     "AMPLE-Math 5,319 题六种推理视图；Qwen3-1.7B、SmolLM3-3B", "学生 rollout 形式（短直答 vs 长思考）", "同一检查点、题目、参考与评测固定",
     "把短直答 rollout 换成长思考 rollout，两个家族都由增益变损失", None, "数学域；摘要级"),
  ev(None, "本轮覆盖扫描：记忆压缩 129 篇、RSI 87 篇、GUI 85 篇旧语料", [], None,
     "完整正文关键词扫描（跳过参考文献）", None, "二手调研归纳",
     "列：换消费者、多消费者、内容替换", None, None,
     "换消费者命中：记忆 14/129、RSI 4/87、GUI 3/85；抽查 TRACER（换骨干保留 62–87% 收益，作者归因于工具调用遵从度）、ContextEvo（同环境内跨模型迁移、跨环境不可靠）、并行 compaction 三条，语义成立；命中论文只报告保留率，未给预测量",
     None, "关键词级；零命中不等于未涉及"),
 ],
 "已有解决方法": [
  "用部署体自己的 rollout 选修复（2610.38610），有效但昂贵",
  "追加而非替换、只适配 query 侧（2610.22016）",
  "按执行 agent 单独训练外部上下文管理器（AdaCoM 2605.30785，继承）",
  "GRACE（2511.02833）：只用学生梯度分布预测离线 KD 教师效果，GSM8K/MATH 上 Spearman 最高 86%"
 ],
 "已支持的解释": [
  "KV 载体：冻结读者的 tolerable set 与竞争注意力（2610.22016）",
  "harness 载体：弱模型的 activation/adherence 失败（2605.30621）",
  "CET 载体：行为组匹配（2610.20959）"
 ],
 "待验证解释": [
  "本地图提出：若干载体上的失败可能由同一消费者侧量解释（如产物诱导动作在消费者自身策略下的似然／接近度、激活率、行为类型）；未经检验"
 ],
 "尚未解决": "各载体只有局部诊断；消费者侧预测只在离线 KD（GRACE）上有，在策略蒸馏、修复、harness、摘要等运行时产物上未检出；是否存在跨产物共用的预测量本轮未检出研究。",
 "可检验切口": "固定若干产物与若干消费者做生产者×消费者矩阵，至少跨两类产物；比较生产方指标与廉价消费方指标对消费者收益的预测力；控制 rollout/token 预算；竞争解释为消费者分布接近度、能力档、行为类型。",
 "已知边界": ["证据多来自 ≤8B 消费者与数学/ALFWorld/WebShop/数据任务", "各载体论文集中在 2026-09 至 10，局部拥挤"],
 "解决状态": "机制未定",
 "查新状态": "做了问题族级反证检索（consumability、executor mismatch、student-specific teacher selection、agent-specific context management）；只检出各载体局部工作与离线 KD 的 GRACE；未做 idea 级查新",
 "与其他问题的关系": ["Q003（特权教师属于 Q001 的教师载体，也属于 Q003 的可得性问题）"]
}

Q002 = {
 "id": "Q002",
 "具体问题": "Agent 显示它“知道”正确判断而动作不跟时，断点在推理→结论、组合事实→决策，还是表示→动作？不同论文用显式结论、事实探针、隐状态探针、推理移植测“知道”，定位相互矛盾；哪种测法得到的断点能预测哪类干预有效？",
 "宏观标签": ["知行差距", "测量口径", "因果控制", "跨论文分歧"],
 "线索类型": ["受控实验", "待解释分歧", "测量伪影"],
 "证据": [
  ev("arXiv:2606.00476", "Doing What They Say, Not What They Reason: Locating the Faithfulness Gap in LLM Agents", [], "https://arxiv.org/abs/2606.00476",
     "Contributions；§3.2；摘要", "v1", "原始实验",
     "德州扑克模拟器，每个决策有可验证参考动作；三个模型家族（含原生推理模型）", "结论抽取方式（自由文本短语 vs 显式 DECISION 标签）；提示策略", "同一决策状态",
     "显式标签下结论→动作不一致 0.0–1.8%，自由文本抽取测出 22–26%；65% 的错误决策中输入估计正确、规则复述正确却得出相反结论；把规则注入提示无效", None, "单一游戏域；机构未核实"),
  ev("arXiv:2610.18579", "Reading Right, Acting Wrong: Diagnosing Decision Failures of System One Models in Agent Loops", [], "https://arxiv.org/abs/2610.18579",
     "摘要；GUI 地图 Q002 继承记录", "v1", "原始实验",
     "冻结的 agent 决策状态（模拟环境、客服策略、工具、网页、代码），17 个单次打分系统 + 1 个推理模型；每个动作问题配同状态的独立事实探针", "系统", "同一状态集",
     "多数错误动作发生在事实读对之后，系统越准这类错误占比越高；错误集中在相同状态；在事实可证明决定动作的状态上，用代码组合模型自己的事实答案可修复（继承：托管 API 模型 70–73%）", None, "摘要级；机构未核实"),
  ev("arXiv:2605.14038", "Model-Adaptive Tool Necessity Reveals the Knowing-Doing Gap in LLM Tool Use", [], "https://arxiv.org/abs/2605.14038",
     "§4 Dataset curation；§4.2 表；摘要", "v1", "原始实验",
     "Qwen3-8B/4B、Llama-3.1-8B/3.2-3B；算术与 TruthfulQA；按模型自身能力定义工具必要性", "实例是否需要工具（模型自适应定义）", "同一模型同一数据",
     "端到端失配 26.5–54.0%（算术）、30.8–41.8%（TruthfulQA）；必要性与调用都线性可解码，但末层末位置方向近乎正交；失配集中在认知→动作；过度/不足调用随模型和领域翻转", None, "≤8B；机构未核实"),
  ev("arXiv:2609.35870", "Says Block, Still Acts: Why LLM Safety Judgments Fail to Govern Action in LLM Agents", [], "https://arxiv.org/abs/2609.35870",
     "摘要；数值继承自 LLM热门方向_刷新_20261101 N-Q003", "v1", "原始实验",
     "3 个开源模型的工具安全决策", "判断侧干预 vs 动作原生干预", None,
     "安全信息可从动作状态读出（跨家族 J→A AUROC 0.875/0.840/0.756）；把判断推向 BLOCK 的干预对动作偏好影响远小于动作原生干预；两类控制子空间只部分重叠", None, "摘要级"),
  ev("arXiv:2610.17444", "The Belief–Action Gap in Language Model Agents", ["Cambridge、UCL、UPenn（QS 初筛）"], "https://arxiv.org/abs/2610.17444",
     "§5.1；附录 E.1；摘要", "v1", "原始实验",
     "文本网格世界；报告式与表示式探针、逆强化学习估计动作价值；推理前缀移植", "移植来自另一决策的推理前缀（10%/50%/90% 截断）", "396 对错配 + 396 对一致对照",
     "强制动作随移植推理走：π(a_B) 0.598–0.673，π(a_A) 0.129–0.165；推理窗口激活编辑控制力有限；任务信息表示比行为可靠", None, "合成网格世界"),
 ],
 "已有解决方法": [
  "显式机器可读决策标签以去除抽取噪声（2606.00476）",
  "用代码组合模型自己的事实答案（2610.18579）",
  "动作原生干预（2609.35870）；ConflictGuard 条件 steering 与恢复轨迹训练（GUI Q002 继承）"
 ],
 "已支持的解释": [
  "自由文本结论抽取会把不一致率放大约一个数量级（2606.00476）",
  "文本推理对动作有因果控制（2610.17444 移植实验）"
 ],
 "待验证解释": [
  "本地图整理的三种读法：探针可解码≠模型操作性判断；失败在推理/组合；部分差距为测量伪影。各读法预测的有效干预不同，未在同批状态上对照"
 ],
 "尚未解决": "没有检出把探针、显式报告、强制结论/移植三种测法放在同一批决策状态与模型上、并检验断点对干预成功预测力的研究。现象层面 2026 年至少 7 篇，拥挤。",
 "可检验切口": "同一批决策状态并列三种“知道”测法并定位断点；用规则注入、显式决策标签、代码组合、动作侧 steering 检验哪个断点有预测力；控制结论抽取方式、模型家族、是否推理模型。",
 "已知边界": ["多数证据 ≤8B 或合成环境", "旧卡 N-Q003、GUI Q002 已因单领域拥挤失败"],
 "解决状态": "机制未定",
 "查新状态": "做了问题族级反证检索（knowing-doing、belief-action、reasoning-action inconsistency）；检出 2610.17444、2606.00476、2605.14038、2601.07972、2603.22619 等，后两篇未读；未做 idea 级查新",
 "与其他问题的关系": ["表示工程 Q001（可解码不可 steer）"]
}

Q003 = {
 "id": "Q003",
 "具体问题": "latent 思维、检索/压缩记忆、摘要、提示区 KV、特权教师交给消费者的“内容”，何时真正贡献内容特异的收益？候选调节变量是消费者能否从自身观测与动作中取得同一信息；它能否在任务内被操纵、并跨载体预测内容收益？",
 "宏观标签": ["内容效应", "信息可得性", "特权信息", "评测对照"],
 "线索类型": ["受控对照实验", "理论分析", "跨论文共性"],
 "证据": [
  ev("arXiv:2610.19373", "Evaluating Compressed Memory: Dependence, Utility, and Content Benefit", [], "https://arxiv.org/abs/2610.19373",
     "§2.1、§2.2；摘要", "v1", "原始实验",
     "9 个压缩记忆系统（ICAE、CCM、Activation Beacon、MemoryLLM 等）；置零、另训无记忆模型、常量输入训练模块、换题段落", "记忆内容与训练对照", "同任务同评测",
     "有的模型依赖记忆却不如另训的无记忆模型；TriviaQA 上 xRAG 用另一题段落 F1 19.38→24.78，本题段落 29.88", None, "单轮 QA 与故事状态预测；机构未核实"),
  ev("arXiv:2610.31778", "Benchmarks Are Surprisingly Compaction-Friendly", [], "https://arxiv.org/abs/2610.31778",
     "This paper；§3.3；Q4 节", "v1", "原始实验 + 作者解释",
     "OpenCode 脚手架，5 种 compaction 策略，3 个前沿模型，PaperBench/ProgramBench/PostTrainBench；44 个 SWE-chat 真实会话", "压缩阈值与策略", "固定脚手架",
     "1M 上下文模型对阈值不敏感；作者解释为基准有固定目标、无中途用户输入、可重读文件系统；真实会话中“怎么做/别做什么”的指令被丢约为“做什么”的 6 倍", None, "可得性未被受控操纵；机构未核实"),
  ev("arXiv:2608.08726", "PAST: Privileged Adaptation from Complete Student Trajectories for On-Policy Self-Distillation", ["HKUST（QS 初筛）"], "https://arxiv.org/abs/2608.08726",
     "§4 Theory（式 17、20，Proposition 4）", "v1", "理论分析",
     None, None, None,
     "前向 KL 蒸馏保留轨迹条件教师的条件均值；教师–学生分歧分解为 I(A;U|H)（只看前缀的策略无法复现）与学生可得的因果偏移；完美特权教师不一定能迁移", None, "数学 OPSD；不是跨载体实证"),
  ev("arXiv:2606.25449", "Reclaim Evaluation: A Lossy Memory Is Worse Than an Empty One", [], "https://arxiv.org/abs/2606.25449",
     "摘要", "v1", "原始实验", "7 个模型；固定预算压缩漂移交互后测可纠正性", "记忆为有损 vs 空", None,
     "保留错误结论、丢掉过程的记忆使模型自信给错值，空记忆下模型弃答；方向在 7 个模型上一致", None, "摘要级；白名单外"),
  ev(None, "继承证据：latent 推理、视频记忆、提示区 KV、多轮 OPSD", [], None,
     "LLM热门方向_刷新 L-Q003、LatentCoT_NL Q001、AI跨领域 Q004、Agent记忆压缩 Q003、LLM热门方向_刷新 A-Q003", None, INH,
     None, None, None,
     "逻辑任务删链伤、换内容不变，算术依赖内容（2610.21182）；化学 latent 交换保留 94.5–103.3%（2610.34173）；只留边界标记找回 latent 视觉增益大部分（2606.01287）；视频记忆去身份对照几乎恢复全部收益（2609.12090）；提示区 KV 中性模板替换可恢复（2605.30574）；多轮 agent 上纯 OPSD 低于未训练基座（2609.29051）",
     None, "各载体各自的对照，口径不统一"),
 ],
 "已有解决方法": [
  "置零 + 另训无记忆 + 常量输入的评测协议（2610.19373）",
  "OPSD 的特权变化/可迁移偏移分解（2608.08726）",
  "把特权信息移到采样端（PSP 2609.29051，继承）"
 ],
 "已支持的解释": [
  "任务类型解释：逻辑占位、算术依赖内容（2610.21182，合成任务）",
  "OPSD 下不可迁移部分为条件互信息（2608.08726，理论）"
 ],
 "待验证解释": [
  "本地图提出：内容特异收益随“消费者拿不到的信息量”增大；可重读文件系统（2610.31778）与特权信息能否经动作取得（A-Q003）是同一变量的实例；未经检验",
  "经典 RL 的 imitation gap 解释（窗口外背景，本轮未读原文）"
 ],
 "尚未解决": "未检出在同一任务内操纵可得性、保持内容不变、跨 ≥2 种载体检验内容收益的研究。",
 "可检验切口": "按 2610.19373 的对照测内容收益；在任务内改变可得性（有无可重读文件系统、特权信息能否经动作取得）；观察内容收益是否随可得性单调。变量必须是任务内操纵的可得性，不能是跨任务的任务性质（nl_latent_content_q001 的拒因）。",
 "已知边界": ["OPSD 上已有理论", "单载体评测协议已有"],
 "解决状态": "部分解决",
 "查新状态": "做了问题族级反证检索（placebo/content-swap、privileged information、imitation gap）；检出 2610.19373、2608.08726、2602.04942、2610.19820 等；未做 idea 级查新",
 "与其他问题的关系": ["Q001"]
}

Q004 = {
 "id": "Q004",
 "具体问题": "steering、RL、OPD、harness、CET 等干预按净分报告，但净分同时包含“错改对”与“对改错”；当破坏量大时，被破坏的实例集合由什么决定，能否在干预前预测？",
 "宏观标签": ["翻转分解", "修复 vs 移动", "评测口径"],
 "线索类型": ["受控实验", "评测审计"],
 "证据": [
  ev("arXiv:2609.36138", "When Does Correction Become Repair? Mechanistic Auditing of Internal Interventions in Tool-Using LLMs", [], "https://arxiv.org/abs/2609.36138",
     "§2、§3、§3.1；摘要", "v1", "原始实验",
     "7 个 LLM，When2Call 与 MetaTool 的 K 路工具前决策；方向干预；59 个预算匹配随机方向", "干预方向与强度", "按基线正确/错误划分人群",
     "5 个模型有方向特异净增益；净增益 +55 的干预破坏了其触及的基线正确决策中的一半以上；随机方向无一达到目标增益", None, "仅 steering 类干预；机构未核实"),
  ev("arXiv:2608.13607", "No Universal Signal Predicts Sample-Level LLM Regression under Version Updates", [], "https://arxiv.org/abs/2608.13607",
     "摘要", "v1", "原始实验（负证据）",
     "6 个基准、3 类任务、6 对模型版本更新；单模型与跨版本信号", "预测信号", "相对置信度基线的增益检验",
     "信号有效性依任务而变，没有通用信号预测样本级回归", None, "版本更新而非干预；摘要级"),
  ev(None, "继承证据：表示工程 Q006、A-Q001、视觉 Q002、L-Q005", [], None, "各来源 slot", None, INH, None, None, None,
     "无门控 steering 下原本答对的规则准确率随强度单调下降（2608.29431）；OPD 增益集中在小 k（2610.03185）；共装技能冲突时核心约束失效但任务仍计为完成（2610.11647）", None, "口径不统一"),
 ],
 "已有解决方法": ["destination 审计与统计许可流程（2609.36138）", "版本更新回归的 FlipGuard、MUSCLE 等（背景，未读）"],
 "已支持的解释": [],
 "待验证解释": ["本地图提出：破坏可能集中在基线答对所依赖的信号恰被干预目标覆盖的样本；未经检验"],
 "尚未解决": "干预场景下破坏集的结构与可预测性未检出研究；版本更新场景已有负结果。",
 "可检验切口": "对同一干预做翻转矩阵，检验破坏集与干预方向/目标信号的关系，并对照 2608.13607 的信号集。",
 "已知边界": ["有直接负证据", "评测审计类贡献在本项目历史上重要性难过 6.5"],
 "解决状态": "仅验证边界",
 "查新状态": "做了问题族级反证检索（negative flips、regression under updates、repair vs displacement）；检出 2608.13607、2105.03048、2410.00508；未做 idea 级查新",
 "与其他问题的关系": ["Q001（CET 的过程收益伴随准确率损失）"]
}

out = {
 "领域": "跨地图共性缺口：LLM 后训练与 Agent（不含世界模型、视频生成、机器人），以本项目 10 张地图 89 张卡与 39 次打磨为输入",
 "检索日期": "2026-11-05",
 "近期窗口": ["2026-05-05", "2026-11-05"],
 "机构口径": "新增主证据：ai-frontier-search 白名单 + QS 前 50；反证检索不限机构与窗口，条目内标明",
 "复盘教训": [
  "L1 卡片锚在单篇论文局限上，去掉论文名只剩补对照",
  "L2 热门方向局部近作出得比打磨快",
  "L3 “来自 A 还是 B”二分常不可分或不互斥",
  "L4 近邻领域方法迁移的新颖度天花板 6–7",
  "L5 同一失效关系在多张地图被各自局部打磨",
  "L6 通过的 idea 都是可预测、跨方法、能改变决策的形状"
 ],
 "推荐顺序": ["Q001", "Q002", "Q003", "Q004"],
 "研究问题": [Q001, Q002, Q003, Q004]
}
Path(__file__).resolve().parent.parent.joinpath("研究问题.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print("ok", len(out["研究问题"]))
