## 结论
2026-11-03，总体 score 5.0，verdict：promising_needs_revision。主贡献是一个无需人类、无需训练的“事前策略合约 + 机械触发 + 指名备选”机制，外加用消融拆分“人类中途指令为何有效”。这个问题值得做，但目前还不够。一是方案最依赖的“指名切换有效”证据在原文里只有每个基准 1 个分叉，并且换到廉价 agent、单卡 A100 时缺乏迁移依据。二是最小实验区分不了“合约的触发机制起作用”和“预先计划好的强制切换或强制多样性起作用”，也没有纳入同任务已公开的最强改进框架。

## Claim 判断
| 维度 | 分数 | 依据 |
|---|---|---|
| 重要性 | 6.5 | 2608.19072 v2 的结论直接呼吁建立“让策略修订成为显式决定的交互协议”，所以“无人类时回收中途指令收益”是对一个真实开放问题的直接回应。不过范围只有 1.7B 基座、两个基准、一个廉价 agent，即使成功，影响面也有限；消融拆分的分量取决于噪声能否压住（见下）。 |
| 新颖度 | 6.0 | 我没检索到“agent 在研究策略层面事前写预期区间与触发条件、由外部监控器机械切换到自定备选”的直接先例，这是可辨认的增量。但它本质上是几样已有东西的组合：运行时规则执行或注册备选（ArbiterOS 的 FALLBACK/VERIFY、AgentSpec）、执行前的证据门控（ECLoop）、2608.19072 已证明的“指名切换”。航空复飞准则、临床无效性边界属于跨域启发，只能约束新意判断，不构成新机制。臂 5 的“只给备选、由 agent 自决”在原文中已有近似观察：experience 框架的 evaluator 在 HumanEval 上反复建议改用 RL，agent 没有切换。 |
| 有效性 | 4.5 | 当前依据：2608.19072 v2 §4.3.2 与附录 D.2，每个基准只有 1 条轨迹分叉，分叉点和替代策略由作者事后选定。GSM8K 上指名分叉 65.20 对比续写 47.76，而同一 experience 框架、Opus 4.6、3 次运行的均值为 77.30±3.8（Table 2），指名分叉反而低于常规均值。HumanEval 上指名分叉 62.8，与该框架均值 62.80±6.1 持平。AIME 是 0/30→2/30，属于存在性结果。因此“+17.44”更像是对一条偏低轨迹的挽回，不能证明指名切换比典型运行有实质增益。迁移条件也未满足：原证据来自 Claude Code + Opus 4.6 + experience 框架、4×A800；本方案用 GLM-5/Kimi/Qwen3-Max、单张 A100。原文附录 E.2 记录 GLM-5.2 “从不改变训练算法”；PostTrainBench 原文也写明只有 Claude 系 agent 尝试过 GRPO。廉价 agent 能否在剩余单卡预算内把 GRPO/执行反馈训练做对，目前没有依据。另外 2610.22599 显示 LLM 系统性低估实验结果变化幅度，触发很可能退化为“几乎总触发”或“几乎不触发”。IBIS 的惯性偏差来自网页检索判断，用它支持“事前制定能避开后训练策略惯性”仍是跨任务推断。 |

与原问题的关系：这项工作回答原问题的“无人类修法”子问题，属于合理的范围收缩。原问题中锚定、信号不足、模型偏好三种来源的分离仍未回答，这里的消融只能部分触及。

实验能否判别主张：目前不能。
- **(a) 缺少关键竞争解释的对照。** 如果合约的收益来自“开训前就计划好 SFT→RL 两阶段”或“到点必切”，那么只需在开训时要求 agent 计划两种范式，或在固定检查点无条件切到 agent 事前自定的备选，就能获得同样收益。臂 4、5、6 都区分不出“预期区间 + 触发”这一核心成分是否必要。这正是锚点里列出的已有修法“强制多样性”。
- **(b) 缺少同任务最强已公开改进。** experience-driven 框架（journal + skill library + evaluator）在同一设定下把 Opus 4.6 的 GSM8K 从 64.70 提到 77.30、HumanEval 从 32.00 提到 62.80，代码已在 github.com/JoylimJY/AI-PostTraining-AI 的 framework/ 下公开，且原文的指名分叉就是在它之上做的。只和原 agent、泛化重新考虑相比，“合约优于强固定策略”的主张没有经过检验。
- **(c) 统计功效不足。** 原文 3 次运行的标准差在 GSM8K 上为 3.8–9.6 分，在 HumanEval 上为 6.1–10.4 分。臂 1、4 各 3 个种子，其余各 2 个种子，支撑不了“4 显著优于 1、2”，更支撑不了“6≈1、5 居中”这种三档排序。拆分成分这一半贡献在当前设计下无法判别。
- **(d) 设定描述有误。** brief 称本设定“即 2608.19072 中人类指名切换有收益的设定”，实际上算力和 agent 都不同，原文数值连参照作用都很弱。

可行性：pass，有条件。
- 官方 harness 开源；HF 上 aisa-group/PostTrainBench-Trajectories 已核验含 opencode_zai_glm-5、opencode_opencode_kimi-k2.6_10h_run1、qwen3max 目录，事前锁定率标注可以做。
- 监控器是规则比对，不调用 LLM，实现简单。
- 260 A100 小时在 8 卡下约 1.5–2 天，符合 5 天约束；如果实际只有 2 张卡可用，约需 5.5 天，会超出。
- API 估算 600–1200 元，处在 1000 元边界。
- 主要实施风险：廉价 agent 能否在单卡剩余预算内完成算法切换。这是效果风险，不阻止实验开展。

## 最高近邻
1. What is Missing from AI Post-Training AI（arXiv:2608.19072 v2，https://arxiv.org/abs/2608.19072）：同一任务、同一现象。人类指名中途切换优于续写，泛化重新考虑无效；evaluator 建议 RL 被忽略。差别：它没有无人类机制，也没有拆分触发与指名；分叉每基准 n=1，由作者事后选择。
2. PostTrainBench（arXiv:2603.08640，https://arxiv.org/abs/2603.08640）：任务与 harness 来源，记录了 SFT 主导、只有 Claude 系尝试 GRPO。差别：只做测评，不含干预。
3. From Inertia to Objectivity / IBIS、NIS-Agent（arXiv:2608.23045，https://arxiv.org/abs/2608.23045）：惯性偏差与上下文隔离。差别：场景是网页检索判断，不涉及研究策略，也没有事前合约。
4. ECLoop: Preventing Premature Commitment in Coding Agents（arXiv:2607.28815，https://arxiv.org/abs/2607.28815）：外部执行层按事先编译的条件门控 agent 动作。差别：门控对象是代码编辑，条件由系统而非 agent 事前制定，不含指名备选切换。
5. ArbiterOS / From Craft to Constitution（arXiv:2510.13857，https://arxiv.org/abs/2510.13857）：VERIFY 信号路由到注册的 FALLBACK 计划，并依据预设阈值监控进度。差别：这是通用 agent 治理，不涉及研究策略层面，也没有 agent 自报的预期区间。

```json
{
  "score": 5.0,
  "contribution_scores": {"importance": 6.5, "novelty": 6.0, "effectiveness": 4.5},
  "contribution_assessment": "主贡献：无人类、无训练的事前策略合约（预期区间 + 机械触发 + 自定指名备选），加上对人类中途指令有效成分的消融拆分。重要性 6.5：直接回应 2608.19072 呼吁的显式策略修订协议，但范围窄。新颖度 6：研究策略层面的组合有增量，但由运行时规则、注册备选、证据门控与已知的指名切换组合而成，且原文已观察到 evaluator 的建议被忽略，与臂 5 的观察部分重叠。有效性 4.5：核心依据是 2608.19072 每基准 1 个、事后选定的分叉；GSM8K 指名分叉 65.20 低于同框架均值 77.30±3.8，HumanEval 62.8 与均值 62.80 持平，增益可能来自挽回偏低轨迹；从 Opus 4.6+4×A800 迁移到廉价 agent+单 A100 缺乏依据（GLM-5.2 从不改变训练算法，只有 Claude 系尝试过 GRPO）；预期区间可能失准（2610.22599）。待验证：廉价 agent 自定备选的质量与执行能力、触发是否优于无条件切换。",
  "feasibility": "pass",
  "feasibility_reason": "harness 与公开轨迹（含 glm-5、kimi-k2.6、qwen3max 目录）已核验可得，监控器为规则实现；26×10 A100 小时在 8 卡下约 2 天，API 约 600–1200 元处于预算边界；廉价 agent 在单卡剩余预算内完成 GRPO 切换是效果风险，不阻止实施；若实际只有 2 卡则约需 5.5 天。",
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "有效性证据不足：指名切换收益只来自 2608.19072 每基准 n=1、事后选定的分叉，且 GSM8K 指名分叉低于同框架 3 次运行均值，HumanEval 与均值持平；向廉价 agent 加单 A100 迁移无依据（GLM-5.2 从不改变训练算法）",
    "Claim 阻断：缺少无条件定点切换到自定备选、开训即计划两范式（强制多样性）的对照，无法区分预期区间加触发是否为有效成分",
    "Claim 阻断：未纳入同任务已公开代码的 experience-driven 框架（GSM8K 77.30、HumanEval 62.80）作为强基线",
    "Claim 阻断：每臂 2–3 个种子，而运行间标准差约 4–10 分，无法支撑“显著优于”与臂 4/5/6 三档排序的消融拆分"
  ],
  "novelty_conclusion": "在 PostTrainBench 研究策略层面未见直接先例，但机制由运行时规则、注册备选、证据门控和已知的指名切换组合而成，新意属可辨认的增量（约 6 分）；臂 5 对应的现象在 2608.19072 中已有近似观察。",
  "closest_neighbors": [
    "What is Missing from AI Post-Training AI: An Empirical Analysis (arXiv:2608.19072)",
    "PostTrainBench: Can LLM Agents Automate LLM Post-Training? (arXiv:2603.08640)",
    "From Inertia to Objectivity: Improving Deep Research Agents with Noise Isolation (arXiv:2608.23045)",
    "Preventing Premature Commitment in Coding Agents with an Evidence-Conditioned Execution Layer (arXiv:2607.28815)",
    "From Craft to Constitution: A Governance-First Paradigm for Principled Agent Engineering (arXiv:2510.13857)"
  ]
}
```
