## 结论
2026-11-03，总体 score 5.5，verdict：promising_needs_revision。主贡献是在 PostTrainBench 真实决策点上做一个以执行结果为真值的“换不换策略”评测，并把锁定拆成“信念错”和“信念对但决策不跟”，再用现任标记与作者归属两个操纵定位来源。这个问题值得问，但目前分量不够：新意基本是 SciΠvot 式二选一、IBIS 式“归属自己”操纵、2610.22599 式实验结果预测这几样搬到后训练场景；有效性又卡在两处设计上，价值表 V 测的不是 agent 在决策点面对的那个量，同一次调用里“先预测、再选择”让信念与决策无法独立分开。

## Claim 判断
| 维度 | 分数 | 依据 |
|---|---|---|
| 重要性 | 6.5 | 2608.19072 v2 已经把缺口定位到“不会重开策略这个决策本身”（§4.3、附录 D.2.3，3 个分叉案例，最高 +17.44 分），并提出显式 continue/switch 决策节点加分叉训练信号。若能可靠区分锁定来自信念还是来自现状/归属偏置，确实能指导下一步走协议还是走训练。但只有 2 个基准、小基座，而且两类答案未必对应两类修法：偏置如果经由信念起作用（现任标记让信念本身偏移），去偏协议照样有效，“信念错→必须训练”的推断并不成立。影响有限。 |
| 新颖度 | 6.0 | 相对最高近邻是可辨认的增量：引入结果真值、在研究型决策点上做现任×作者 2×2，并同时诱出信念。不过“归属自己的行动导致判断变差”IBIS（2608.23045）已在观测受控的条件下测过；“选项标为现状”的 label-swap 是 2410.15413 的标准范式；“LLM 预测 ML 实验结果”2610.22599 已做，并且发现系统性低估变化幅度；“信念—行动不一致”有 2602.06286、2610.17444 的框架。brief 没有列出 IBIS 和 2610.22599，因此本方案相对它们新在哪里并未论证。 |
| 有效性 | 5.5 | 现有依据：2608.19072 的 reconsider 分叉（n=3）说明不点名替代方案时 agent 会重申原策略，但这个结果同时符合信念错和决策偏置两种解释；SciΠvot 说明模型偏好原 LLM 计划，但没有拆开归属；IBIS 在深度检索中支持“归属效应”，能否迁移到后训练策略选择未知；2610.22599 反而为“信念低估替代方案收益”提供了直接先验，并报告未见 self-preference；Barkett et al. 2508.01545 的结论是单人决策情境中升级承诺“minimal”，brief 把它当作支持证据，这是误读。测量层面的未知更大：(1) V 是每个（基准×基座）一张、从基座按固定配方跑出来的表，多个决策点共享。它不依赖决策点状态（2608.19072 自己把切换收益归因于共享前缀已经解决了格式问题），也不是 agent 执行出来的价值，所以“信念误差”与“V 不代表 agent 被问到的量”混在一起，无法分离。(2) argmax V 实际只由 4 个组合决定，每个 2 种子；regret 的差异几乎全部来自选择分布，一个固定策略（如“总是选 GRPO”）就可能接近零 regret。(3) 同一调用中先报预测再选择，几乎必然自洽，“信念支持换却不换”会被机制性压到接近零；而动机性信念（为现任抬高预测）恰好被记在“信念误差”名下，推翻条件因此可能被设计本身触发。 |

回答的是原问题（锁定来源），并把它收窄为“信念 vs 决策 + 两种偏置源”。原问题中“锚定/信号不足/模型偏好”里的“模型偏好”（2608.19072：策略跟着 agent 走而非跟着任务走）在本设计里没有单独的检验。

实验能否判别主张：现任×作者 2×2 对选择的配对效应可以判别“呈现是否影响决策”，这部分有效。但“信念误差 vs 决策不一致”的分解不可判别，因为信念与选择同调用诱出，且 V 与信念所指的量不一致。缺少“最佳固定策略/总选某一策略”这一非自适应对照，regret 无法解读；HMA、MIRA、逐级淘汰属于修法参照，与诊断主张关系不大。

可行性：pass。已在 hf-mirror 核实 aisa-group/PostTrainBench-Trajectories 包含 claude-opus-4-6（多 run）及 Opus 4.7/4.8/5、GPT-5.x Codex 等 agent 在 gsm8k/humaneval × Qwen3-1.7B/4B-Base 上的目录，60–100 个决策点有可信来源（过滤“未产出”的 run 后的覆盖量仍待确认）。价值表约 224+60 A100 小时，8×A100 约 1.5 天，在 5 天内。需要注意 PostTrainBench 预算是单张 H100 10 小时，“约 7 A100 小时”与 H100 剩余预算并不等价，需要换算。API 量级（约 13M token 新上下文 + 约 6M token 自身上下文）大致落在 1000 元内，推理输出 token 是超支风险。各近邻规范可得：HMA 有仓库，MIRA 可按论文独立实现，D.2.3 的 reconsider 规范在 v2 附录中可查。

## 最高近邻
1. What is Missing from AI Post-Training AI（arXiv:2608.19072 v2，https://arxiv.org/abs/2608.19072）：同一任务和轨迹，结论是“缺的是重开决策”；有点名/不点名分叉（n=3）。差别：没有诱出信念，没有分离现任与归属，没有逐决策点评测。
2. SciΠvot（arXiv:2610.21082，https://arxiv.org/abs/2610.21082）：在项目记录条件下，模型在原 LLM 计划与人类修正之间偏好原计划，reconsider 无稳定帮助。差别：以人类修正为参考、没有结果真值、没有现任×作者操纵、不限于后训练。
3. From Inertia to Objectivity / IBIS（arXiv:2608.23045，https://arxiv.org/abs/2608.23045）：在观测受控的条件下只改变“是否为自己先前的行动”，发现 inertia bias，并用上下文隔离修复。差别：深度检索场景，不涉及研究策略选择和结果真值；但“作者归属”这一臂的新意被它大幅削弱。
4. Can LLMs predict the outcomes of ML experiments?（arXiv:2610.22599，https://arxiv.org/abs/2610.22599）：前沿模型预测 MLE-bench 想法的执行结果，系统性低估变化幅度，未见 self-preference。差别：没有和决策、锁定挂钩；但它直接支持“信念误差”这一支，是信念侧的必要近邻。
5. When Agents Say One Thing and Do Another（arXiv:2602.06286，https://arxiv.org/abs/2602.06286）：信念—决策一致性的决策论检验框架。差别：风格化诊断任务，不是研究 agent；本方案的“决策不一致”分解应与之对齐。

```json
{
  "score": 5.5,
  "contribution_scores": {"importance": 6.5, "novelty": 6.0, "effectiveness": 5.5},
  "contribution_assessment": "主贡献：在 PostTrainBench 真实决策点上用执行价值表评测换策略决策，并把锁定分解为信念误差与决策偏置（现任/作者归属）。重要性 6.5：问题真实，2608.19072 v2 已定位到缺少重开决策，本工作要进一步拆分来源；但信念/决策二分并不对应训练/协议二分，因为偏置可经由信念起作用，而且范围只有 2 基准、小基座。新颖度 6：基本是 SciΠvot 式选择、IBIS 式归属操纵、2610.22599 式结果预测与 label-swap 现状范式的组合迁移，brief 漏列 IBIS 与 2610.22599。有效性 5.5：现有证据双向——2610.22599 支持信念低估，IBIS 支持归属效应但在别的领域，Barkett 单人情境下升级承诺 minimal（brief 误读）；V 为每组合共享、从基座按固定配方跑出，不依赖状态，也不是 agent 执行价值，argmax 只由 4 个组合决定；信念与选择同调用诱出，不一致率会被机制性压低。2×2 对选择的配对效应仍可判别。",
  "feasibility": "pass",
  "feasibility_reason": "已核实公开轨迹包含 Opus 4.6 等多 agent 在 gsm8k/humaneval×Qwen3-1.7B/4B-Base 上的 run；价值表约 284 A100 小时，8×A100 约 1.5 天；API 约 19M token，大致在 1000 元内；HMA 有代码，MIRA、D.2.3 规范可查。需把 H100 10 小时预算换算成 A100 等价预算。",
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "贡献门槛未过：三项均未达到 8；新意主要是 SciΠvot、IBIS(2608.23045)、2610.22599 与现状 label-swap 范式的组合迁移，相对 IBIS 和 2610.22599 的差别未论证",
    "Claim 阻断（真值不对位）：V 为每个基准×基座共享、从基座按固定配方执行的表，不依赖决策点状态，也不是 agent 自己执行的价值；“信念误差”因此无法与“V 不代表被问的量”分开，argmax V 实际只由 4 个组合、每个 2 种子决定",
    "Claim 阻断（分解不可判别）：信念与选择在同一调用中先后诱出，选择几乎必然与所报信念一致，动机性信念会被记为信念误差，可能由设计本身触发推翻条件；同时偏置若经由信念偏移起作用，‘信念错→需训练、决策偏→需协议’的推断不成立",
    "缺少关键对照：没有‘最佳固定策略/总选某一策略’的非自适应基线；在共享 V 下这一平凡策略可能接近零 regret，导致 regret 无法解读",
    "证据误读：Barkett et al.(2508.01545) 报告单人决策情境中升级承诺 minimal，不能作为‘自我归属承诺’的支持证据"
  ],
  "novelty_conclusion": "相对 2608.19072 和 SciΠvot 有可辨认增量（结果真值、现任×作者 2×2、信念诱出），但归属操纵已见于 IBIS，信念侧结果预测已见于 2610.22599，现状操纵是标准 label-swap 范式；整体属于组合迁移，新颖度约 6。",
  "closest_neighbors": [
    "What is Missing from AI Post-Training AI: An Empirical Analysis (arXiv:2608.19072)",
    "SciΠvot: Benchmarking Principal-Investigator Judgment at Pivotal Moments of Scientific AutoResearch Agents (arXiv:2610.21082)",
    "From Inertia to Objectivity: Improving Deep Research Agents with Noise Isolation (arXiv:2608.23045)",
    "Can LLMs predict the outcomes of machine learning experiments? (arXiv:2610.22599)",
    "When Agents Say One Thing and Do Another: Validating Elicited Beliefs from LLMs (arXiv:2602.06286)"
  ]
}
```
