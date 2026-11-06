## 结论
2026-11-06，总体 score 5.5，verdict：promising_needs_revision。主贡献是一个"源端做内容保持的约束放置干预，再用带交互项的条件效应模型，凭目标人群的约束元数据预测编码 agent 上下文管理方法的逐条约束增益与方法排序"的迁移预测框架。框架本身完整、可以落地，但三项分数都没有到 8：重要性受限于窄范围和决策价值未被证明（SC 提取器在已有证据中近乎处处占优）；新颖度属于把可迁移性 / CATE 搬到 agent 评测的增量；有效性有一处关键假设存在正值性（positivity）缺口。第二个目标 SWE-Together 能确定性判定的约束单元也可能太少。因此贡献门槛不通过。

## Claim 判断
| 维度 | 分数 | 依据 |
|---|---|---|
| 重要性 | 6 | 成功后得到的是：对一个只看得到日志的编码 agent 用户人群，标注一次约束元数据，就能选出上下文方法并估计其约束保持增益。需求真实存在：SWE-Together 只从 11,260 个会话中转出 109 题（0.97%）；2610.31778 的 Fig.3 中，静态基准上各压缩策略都不在置信区间外优于自摘要。但对象只是编码 agent 的上下文方法 × 约束遵循，原问题中的终态通过率、跨方法族都没有覆盖。更关键的是决策价值：CONPACT 的 SC 提取器在三个场景中保留率都超过 90%，若它在各层都占优，"排序取决于人群构成"就退化成"总选 SC 提取器"。brief 没有给出各层之间出现方法排序反转的已有证据；Recent-5 只在注入位置落进最后 5 轮窗口时较好，这是唯一可见的交叉。因此本项为 6，到不了 8。 |
| 新颖度 | 7 | 检索没有找到在 LLM agent 评测中，用效应修饰变量迁移"方法相对对照的增益"的工作。BIS 用重要性采样预测模型水平，CJE 用目标端 oracle 校准替代指标，"Beyond Static Leaderboards" 只主张测量排序的预测效度。2610.31778、CONPACT、MTAC-IFBench、Harness-IF 只报告分层差异。按跨领域规则给 7。结构性适配（用内容保持的放置干预补出静态基准缺少的层）确有内容，但修饰变量全部取自上述近邻已报告的分层，模型是标准的交互项 CATE，不足以到 8。 |
| 有效性（先验合理性） | 5.5 | 支持：各修饰变量的边际效应都有一手证据，已核实：2610.31778 App.6.11 中功能需求丢 6.2%、过程指令 35.9%、范围排除 36.8%，丢失随压缩次数单调上升；MTAC 中策略文件约束衰减更慢，替换约束难于新增；CONPACT 中注入位置影响保留，SC 提取器超过 90%。缺口：(1) 证据大多是保留率的边际差异，几乎没有"方法 × 修饰变量"交互可以跨人群交换的证据。(2) 正值性：源端每题 3 条约束，MTAC 平均每实例 91.33 条约束，按 brief 的说法每轮约 13 条，"同时生效约束数"超出源端支撑范围，只能外推；语言（英文对中文）、任务（修 bug 对绿地项目）也同时变化。(3) 主检验只用可脚本判定的 Content/Quantity/Style/Language 类，排除了 Workflow/Environment 类；而按 2610.31778 的已有结果，过程类约束才是方法差距最大、最需要预测的部分，主检验的信号可能偏弱。没有发现直接反驳"条件可交换"的已有数据。 |
| 待预研（不计分） | — | 预测误差的大小；在可判定类别上方法之间是否真有足够的层间增益差异；能否优于目标端 10 实例试跑；两个目标上的方法排序是否真的不同。 |

与起点的关系：这是原问题收窄后的子问题，从"基准结构性质预测增益保留率"收窄为"约束元数据预测上下文方法的约束遵循增益"。跨方法族（技能、harness 演化）、终态通过率、非编码领域仍未回答。转向本身不是阻断。

实验能否判别主张：四个对照的方向设置合理，留一层检验也是对的。但有三处问题。(a) 缺两个强对照：一是不跑任何试验、只用已发表分层数字（2610.31778 / CONPACT 的类别与位置保留率）做的零成本预测；二是"源模型 + 目标 10 实例校准"的混合方法，即 CJE 式锚定，这是迁移文献中自然的最强竞争方案。(b) MTAC 上 10 个实例就约有 900 条约束结果，"目标试跑"对照会非常强，按 brief 自己的规则，大概率退回到只剩"只见日志"的情形；而只见日志的情形没有单独的外部有效性检验，因为两个验证目标都可以运行。(c) 5 种方法在 2 个目标上的 Kendall τ 统计功效很低，"预测出排序差异"难以给出可信结论。

可行性：pass。已核实的公开资源：aisa-group/compaction（OpenCode 分支，有 compaction.prune、compaction.model、compaction.saveToFile 等配置键）；ZhiqiEliWang/compaction-integrity（有 sc_extractor.py，需要移植进 OpenCode）；AgentProbe 支持 OpenCode，MTAC 数据中有 validation_code(response, workspace_path)；SWE-Together 的 109 个任务都带 oracle_intents.json、reference_patch.json 和 tests。Qwen3.6-27B 为开放权重。HDA ReAct harness 及"保留前 2 条与最后 36 条"的细节本次没有核实到。约 4,250 次运行、8×A100、3 天偏紧，但在 5 天以内。资源上的关键缺口在 SWE-Together：oracle_intents 共 943 条，类型为 request 327、question 266、context 111、correction 119、workflow 88、verification 32，没有现成的约束检查器；含 do not / don't / never / constraint 等字样的只有 43 处。能确定性判定、且之后还剩至少 1 轮的约束单元，可能只有几十条，需要人工编写检查器。另外，脚本化回放与该论文自己指出的"逐字回放会错时"相冲突，correction 类意图会脱离当时的轨迹。这些问题影响"第二个目标"那条 Claim，不影响 MTAC 部分是否做得出来。

## 最高近邻
1. Benchmarks Are Surprisingly Compaction-Friendly（https://arxiv.org/abs/2610.31778）：同一 OpenCode 压缩实现，在 SWE-chat 上做约束类别分层丢失；没有做跨人群的方法增益预测。
2. Lost in Context Compaction / CONPACT（https://arxiv.org/abs/2608.11242）：受控注入约束的位置、措辞、重复，提出 SC 提取器；报告了分层保留率，但没有迁移预测，也没有编码 agent 的多轮用户回合。
3. MTAC-IFBench（https://arxiv.org/abs/2609.14992）：目标端数据，给出约束来源、替换、轮次衰减与 harness 对比；不评测上下文方法的增益。
4. Causal Judge Evaluation（https://arxiv.org/abs/2512.11150）：用目标端小比例 oracle 校准，并做迁移审计。它对应本方案的"目标试跑"对照，但其校准与锚定的混合形式没有被列为对照。
5. Importance Sampling is All You Need / BIS（https://arxiv.org/abs/2508.01203）：重加权源基准来预测新基准上的模型水平；没有方法增益，也没有修饰变量干预。（补充：Beyond Static Leaderboards，https://arxiv.org/abs/2606.19704，主张用预测效度评价配置排序，属于定位近邻。）

```json
{
  "score": 5.5,
  "contribution_scores": {"importance": 6.0, "novelty": 7.0, "effectiveness": 5.5},
  "contribution_assessment": "主贡献：用源端内容保持的约束放置干预加交互项条件效应模型，按目标人群的约束元数据预测编码agent上下文方法的逐条约束增益与排序。重要性6：需求真实，但范围窄，且SC提取器在已有证据中近乎处处占优，没有给出层间方法排序反转的证据，决策价值没有被证明。新颖度7：目标领域没有找到这一做法，修饰变量取自近邻已报告的分层，模型是标准CATE。有效性5.5：各修饰变量的边际效应有一手证据，但'方法×修饰变量'交互的跨人群可交换性缺少依据；同时生效约束数（源3条，MTAC约13条/轮，91条/实例）超出源端支撑；主检验排除了方法差距最大的过程类约束。预测误差大小待预研。",
  "feasibility": "pass",
  "feasibility_reason": "aisa-group/compaction、compaction-integrity（sc_extractor.py）、AgentProbe（OpenCode+validation_code）、SWE-Together 109题（oracle_intents/reference_patch/tests）均已核实公开可得，Qwen3.6-27B为开放权重，约4,250次运行在8×A100五天内可完成；SWE-Together中可确定性判定的约束单元很少（943条意图以request/question为主，没有现成检查器），需要人工编写检查器，样本可能只有几十条；HDA harness细节未核实。",
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "贡献门槛不通过：重要性6、新颖度7、有效性5.5，没有任何一项达到8；方法排序在不同人群间会反转、从而需要预测这一前提没有证据，SC提取器的近乎全面占优削弱了决策价值",
    "正值性缺口：源端每题3条约束，无法覆盖MTAC每轮约13条、每实例91条的同时生效约束数，语言与任务类型也同时变化，关键可交换假设在主目标上只能外推",
    "SWE-Together验证臂的可判定约束单元可能过少（以request/question为主，无现成检查器），'两个目标排序差异'这一Claim难以检验；5种方法×2个目标的Kendall τ统计功效不足",
    "缺少强对照：只用已发表分层数字的零成本预测，以及源模型+目标10实例校准（CJE式锚定）的混合方法"
  ],
  "novelty_conclusion": "目标领域没有检索到用效应修饰变量迁移agent方法增益的工作，按跨领域迁移给7；修饰变量与分层发现均来自2610.31778、CONPACT、MTAC-IFBench，统计框架为标准可迁移性/CATE，不足以到8。",
  "closest_neighbors": [
    "Benchmarks Are Surprisingly Compaction-Friendly (arXiv 2610.31778)",
    "Lost in Context Compaction: When LLM Systems Drop Side Constraints (arXiv 2608.11242)",
    "MTAC-IFBench (arXiv 2609.14992)",
    "Causal Judge Evaluation (arXiv 2512.11150)",
    "Importance Sampling is All You Need / BIS (arXiv 2508.01203)"
  ]
}
```
