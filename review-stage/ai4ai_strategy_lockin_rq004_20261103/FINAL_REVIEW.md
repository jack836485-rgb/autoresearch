# FINAL_REVIEW：Q004（AI 研发 agent 的策略锁定）

- 状态：停止（rejected_no_viable_candidate）。共 3 次 Reviewer 调用，均未通过门槛，没有候选进入复核。
- 停止决定：2026-11-03。用户把方向交给执行者决定，执行者决定停止 Q004，把剩余预算转给 Q003。

## 各轮结果

| Call | 候选 | 总分 | 重要性 / 新颖度 / 有效性 | 可行性 | 结论 |
|---|---|---|---|---|---|
| 1 | IDEA-002 信念 vs 决策分解（执行出来的策略价值表） | 5.5 | 6.5 / 6.0 / 5.5 | pass | promising_needs_revision |
| 2 | IDEA-007 按精修年龄分层的公平接受（ALPS 迁移） | 5.5 | 6.5 / 6.0 / 5.0 | pass | promising_needs_revision |
| 3 | IDEA-008 事前策略合约（预期 + 触发 + 指名备选） | 5.0 | 6.5 / 6.0 / 4.5 | pass（有条件） | promising_needs_revision |

## 未过门槛的原因

1. **起点问题的头部空间证据薄弱。**
   - 2608.19072 的“人类指名切换最多 +17.44”来自每个基准 1 条、由作者事后选定的分叉。
   - GSM8K 上指名分叉为 65.20，低于同一 experience 框架、Opus 4.6、3 次运行的均值 77.30±3.8；HumanEval 上的 62.8 与均值 62.80±6.1 持平（Call 3 Reviewer 读取原文 Table 2 与附录 D.2）。
   - 因此，“策略锁定会明显损失性能”在现有证据下没有被确立。
2. **修法空间拥挤。**
   - 搜索端：GEAR 2605.13874、SeaEvo 2604.24372、DAPS 2609.00077、OpenEvolve 与 ShinkaEvolve 的岛屿和 MAP-Elites。
   - 判断端：IBIS 2608.23045 的上下文隔离、SciΠvot 2610.21082。
   - 协议端：ECLoop 2607.28815、ArbiterOS 2510.13857。
   - 已覆盖了三类候选的主要机制，剩余增量被评为组合迁移，新颖度约 6 分。
3. **迁移依据不足。**
   - 原证据来自 Claude Code + Opus 4.6；GLM-5.2 从不改变训练算法，只有 Claude 系 agent 尝试过 GRPO。
   - 低价 agent 在单卡预算内能否完成策略切换，没有依据。

## 最高近邻（跨轮汇总）

- 2608.19072 What is Missing from AI Post-Training AI
- 2610.21082 SciΠvot
- 2608.23045 IBIS / NIS-Agent
- 2605.13874 GEAR
- 2609.00077 Beneath the Diff（DAPS）
- 2610.09239 The Winner's Curse in LLM Self-Improvement Loops
- 2610.22599 Can LLMs predict the outcomes of ML experiments?
- 2607.28815 ECLoop
- 2510.13857 ArbiterOS

## 剩余风险与原问题状态

原问题（锁定来自锚定、信号不足还是模型偏好）仍未回答。更前置的问题是锁定是否真的有代价，这同样未回答，需要足够功效的分叉研究。
