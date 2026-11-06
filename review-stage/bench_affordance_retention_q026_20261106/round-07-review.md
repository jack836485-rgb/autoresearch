## 结论
2026-11-06，总体 score 5.5，verdict：promising_needs_revision。主贡献是一个预测器：在 SWE-bench 上人为补出各个 Z 层的数据（放置位置 × 之后还剩几轮），再按目标人群在 Z 上的构成加权，预测上下文方法在该人群上的逐条增益和方法排序。这个方向有用，但现在还不够：第一，"条件于 Z 的增益可交换"这条核心假设，被已有证据中多个不在 Z 里的效应修饰变量削弱；第二，两个验证目标里，恰恰是区分人群的那几层，要么无法确定性判定，要么带处理后偏倚；第三，"优于 BIS"在构造上必然成立，检验不了正值性论证。

## Claim 判断
| 维度 | 分数 | 依据 |
|---|---|---|
| 重要性 | 6 | 方法采用者能用自己日志的约束构成预先选出上下文方法，这有实际价值，也直接推进了起点卡片"用结构性质预测保留率"的问题。但覆盖面只有编码 agent 的 6 个方法对。另外 2610.31778 发现没有任何压缩方法优于默认自摘要（§4.1 Q2），说明方法之间的排序差异可能很小，"不同人群给出不同排序"这一决策价值目前没有依据。 |
| 新颖度 | 7 | 我检索后没有发现 agent 评测领域里有工作把方法增益按效应修饰变量做跨人群迁移（transportability / 后分层）。按跨领域迁移规则，这算对目标领域的实质新意。但"正值性违反"这一说法，本质上是给已知事实换了术语：静态基准没有中途约束，这一点 MTAC-IFBench、SWE-Together、Harness-IF 都已作为动机写明。方法本身也就是"内容保持的放置干预 + 标准后分层"，结构性适配有限，所以不给到 8。 |
| 有效性（先验合理性） | 5 | 支持的证据：Z 的各维确实修饰效应。我核对了原文：2610.31778 App. 6.11 中功能需求丢失 6.2%、过程指令 35.9%、范围排除 36.8%，Fig. 4a 中第 1 次压缩丢 0.92 类、第 10 次丢 1.93 类；MTAC §4.4 中策略文件来源的衰减慢于用户指令。削弱可交换性的已有证据有四条，且都与关键假设相冲突，不是单纯的未知：(1) 2610.31778 显示损失随压缩次数、阈值和上下文窗口变化，而压缩次数由会话 token 长度决定，不由"之后的用户轮数"决定。SWE-bench 拆成 3–4 轮、每题 2 条约束，MTAC 平均 7.04 轮、每轮 12.97 条约束、中文、绿地前端或数据分析项目，两边的压缩触发次数和约束间干扰差别很大，而这些都不在 Z 里。(2) MTAC §4.4 显示，"替换已有约束"明显难于"新增约束"，这个修饰变量也不在 Z 里。(3) Harness-IF（2608.11727）显示，与模型默认行为相反的规则（against-prior）普遍低 3.6–7.4 点，源端注入约束的先验方向不受控。(4) 计划中的可交换性检验只做"全部约束放首轮"版本，检验不到真正需要外推的中途层和高暴露层。此外，方案没有说明源端短会话里压缩是否真会被触发（阈值设置未给）；若不触发，各层的源端增益都接近 0。 |
| 待预研 | — | 迁移误差比统一折扣低多少；各人群的观测排序是否真的不同；源端 SWE-bench 3–4 轮会话的压缩或截断触发率；SWE-Together 中可确定性检查的意图数量。 |

与起点的关系：这是原问题的收窄子问题（保留"按基准结构预测增益保留"，只覆盖上下文管理方法）。跨方法族、留出任务族和终态口径的预测关系仍未回答。范围收窄本身不是阻断。

实验能否判别主张：目前不能完全判别。
- BIS 式重加权本来就不覆盖中途层，所以"在无支撑层上优于 BIS"在构造上必然成立，推翻不了正值性论证。真正有判别力的对照（只按轮次位置分层、只按类别分层、目标端少量直接试跑）缺失或很弱。
- 我实测了 MTAC 发布数据（HF thu-coai/MTAC-IFBench, data/full/questions.jsonl）：9,133 个逐轮检查项，去重后 2,149 条约束。带 validation_code 的有 3,586 项，去重后 920 条：策略文件 314 条，用户首轮 97 条，用户中途按之后剩余轮数 0/1/2/3/≥4 分别为 89/76/83/81/180。中途层和暴露层的样本够用。但一级类别 Workflow（427 条）和 Environment（423 条）的可脚本判定数都是 0，可脚本判定的只在 Content、Quantity、Style、Language 四类。所以在 MTAC 主分析里，Z 中"过程与工作流"和"范围与环境"这两层，也就是 2610.31778 中压缩损失最大的两类，完全无法检验。
- SWE-Together 的 oracle_intents 我核对过：943 条，其中 request 327、question 266、correction 119、context 111、workflow 88、verification 32，与 brief 一致。但它的模拟器"只在被评 agent 的轨迹触发条件时释放反馈"（论文 §2.2）。因此意图是否出现、在第几轮出现、之后还有几轮，都受方法本身影响。brief 说"暴露量相对方法是处理前变量"，在这个目标上不成立。再加上可确定性检查的意图很少，按上游来源分的四组规模是 29/23/9/48，Hyperswitch 只有 9 题，做不了人群级的排序检验。

可行性：pass，但有风险。以下资源我都核实过可得：aisa-group/compaction、ZhiqiEliWang/compaction-integrity、Wenwen-D/HarnessDeltaAttribution 仓库存在；HDA 的 artifacts/metaharness_swebench 下有 react_baseline.py（>40 条消息时截为 messages[:2] + messages[-36:]）、fresh_context_patch_review.py、loop_break_context_excision.py；MTAC 数据与 AgentProbe 代码公开，论文也报告了 OpenCode 结果；SWE-Together 原生有 opencode 和 mini-swe-agent 适配；Qwen3.6-27B、Qwen3.6-35B-A3B、Qwen3-30B-A3B-Instruct-2507 都已发布。约 5,400 次运行、8×A100、约 4 天在约束之内，但余量很小：MTAC 900 个会话 × 7 轮绿地开发很重，模拟器也要占 GPU。效果未知不算不可行；阻断在于上面那几层的可检验性。

## 最高近邻
- BIS, Importance Sampling is All You Need（https://arxiv.org/abs/2508.01203）：用题面分布重加权源基准来预测新基准上的分数。差别：它预测的是模型水平，不做放置干预；作为对照时，在无支撑层上必败，判别力弱。
- Causal Judge Evaluation（https://arxiv.org/abs/2512.11150）：用小规模 oracle 切片校准，并带可迁移性审计。差别：它需要目标端标签；但"在目标端少量试跑"正是本方法应当打败的实际替代方案。
- Benchmarks Are Surprisingly Compaction-Friendly（https://arxiv.org/abs/2610.31778）：OpenCode 中五种压缩方法；约束丢失按类别分层，并随压缩次数单调上升。差别：没有跨人群的增益预测；同时它给出了 Z 之外的修饰变量（压缩次数、上下文窗口）。
- MTAC-IFBench（https://arxiv.org/abs/2609.14992）：多轮编码约束遵守的逐轮衰减，比较策略文件与用户指令、新增与替换。差别：只评模型和 harness，不预测方法增益；它发布的可脚本判定约束不覆盖 Workflow 和 Environment 类。
- Lost in Context Compaction / CONPACT（https://arxiv.org/abs/2608.11242）：注入位置和表述方式影响约束保留，SC 提取器保留率超过 90%。差别：只在单一套件内测保留，不做迁移预测。相关的还有 Harness-IF（https://arxiv.org/abs/2608.11727），它在 5 个指令面放规则并控制 against-prior。

```json
{
  "score": 5.5,
  "contribution_scores": {"importance": 6.0, "novelty": 7.0, "effectiveness": 5.0},
  "contribution_assessment": "主贡献：在 SWE-bench 上用内容保持的放置/轮次干预补出 Z 层支撑，再按目标人群的 Z 构成后分层，预测上下文方法的逐条增益和排序。重要性 6：决策价值明确但范围窄，且 2610.31778 显示压缩方法之间排序差异可能很小。新颖度 7：agent 评测中未检索到跨人群方法增益迁移的工作，但'正值性违反'是给已知事实换了术语，方法是标准后分层。有效性 5：Z 确实修饰效应，有核实的支持数据；但已有证据显示压缩次数/上下文长度、约束密度、替换与新增、against-prior 都修饰效应且不在 Z 内，源（英文 Python 修 bug，每题 2 条约束）与 MTAC（中文绿地项目，每轮约 13 条约束）差异大；可交换性检验只覆盖首轮层；源端压缩是否触发未说明。",
  "feasibility": "pass",
  "feasibility_reason": "代码与数据已核实可得（aisa-group/compaction、compaction-integrity、HDA metaharness_swebench 三个 harness 文件、MTAC HF 数据与 AgentProbe、SWE-Together 的 opencode/mini-swe-agent 适配、所需 Qwen 模型）；约 5,400 次运行在 8×A100、约 4 天内勉强可行，但 MTAC 900 个 7 轮会话和模拟器的 GPU 占用使余量很小。",
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "贡献门槛未过：6/7/5，有效性低于 6。",
    "可交换性假设被 Z 外的已知效应修饰变量削弱（压缩次数/会话 token 长度、约束密度、替换与新增、against-prior、语言与任务类型）；计划的可交换性检验只做'全部放首轮'，检验不到需要外推的中途层和高暴露层。",
    "MTAC 发布数据中 Workflow（427 条）和 Environment（423 条）类约束的可脚本判定数为 0，主分析无法检验 Z 中'过程与工作流''范围与环境'两层，而这两层正是区分人群和方法的核心。",
    "SWE-Together 的反应式模拟器按 agent 轨迹释放意图，通道和暴露量受方法影响（处理后变量）；可确定性检查的意图少，按来源分的四组（含 Hyperswitch 9 题）撑不起人群级排序检验。",
    "'优于 BIS'在无支撑层上构造上必然成立，推翻不了正值性论证；缺少有判别力的对照（只按轮次分层、只按类别分层、目标端小样本直接试跑）。"
  ],
  "novelty_conclusion": "目标领域（agent 方法评测）未检索到把方法增益按效应修饰变量做跨人群迁移的工作，迁移本身有新意（7）；但'静态基准无中途约束'已是 MTAC-IFBench、SWE-Together、Harness-IF 的公认动机，正值性只是换了术语，方法是标准后分层，结构性适配有限。",
  "closest_neighbors": [
    "Importance Sampling is All You Need: Predict LLM's performance on new benchmark by reusing existing benchmark (2508.01203)",
    "Causal Judge Evaluation: Calibrated Surrogate Metrics for LLM Systems (2512.11150)",
    "Benchmarks Are Surprisingly Compaction-Friendly (2610.31778)",
    "MTAC-IFBench: Benchmarking Instruction-Following in Multi-Turn Agentic Coding (2609.14992)",
    "Lost in Context Compaction: When LLM Systems Drop Side Constraints (2608.11242)"
  ]
}
```
