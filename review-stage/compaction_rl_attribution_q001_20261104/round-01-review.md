## 结论
2026-11-04 总体 score 5.5/10，verdict：promising_needs_revision。主贡献由两部分组成：一是解释"带 compaction 的结果式 agent RL 主要学到执行器耐受有损上下文"，用 2×2 summarizer×actor 交换检验；二是阻断重获取的兄弟 summary 续写，只对 summary token 记功。这个贡献目前不够。解释部分在推理期已有人明确提出（2610.31778 的"目标固定、进度在盘上，被丢内容大多可重获取"；2610.35496 的"以重读补偿"），兄弟分叉加 summary 专属优势的机制也已有 TreeMem、DSSR 这类近邻。新意实际只剩"续写中阻断重获取"这一项改动，再加上把解释搬到 RL 训练期。而且最小实验的支持判据没有检验这项改动在目标任务上带来什么可用收益。

## Claim 判断
| 维度 | 分数 | 依据 |
|---|---|---|
| 重要性 | 6.5 | compaction 已进入大规模 RL 管线（CompactionRL 用于 GLM-5.2，Occamy 沿用），所以"训练收益来自 summary 还是执行器"会影响 summary 能否跨 actor 复用、能否在不可重获取的约束上可靠。问题在于：在可重获取环境里，执行器靠重读补偿本身就是一个能用的解，此时 summary 变好的价值主要落在效率和不可重获取信息上。brief 只把后者放在合成约束上，影响范围有限。 |
| 新颖度 | 5.5 | 下面三项已有近邻：(a) 从同一状态展开多份 summary/memory，用后续分支结果给它单独记功并加长度惩罚，TreeMem 2605.04811 已做；(b) 用前滚续写给候选 state 打分来训练 writer，并指出前滚分数比静态打分更能预测结果，DSSR 2609.32805 已做；(c) "benchmark 对 compaction 友好，因为被丢内容可重获取，只有别处不存在的约束会真正丢失"，2610.31778 已做。brief 的增量是三点：续写时阻断已见文档；把可重获取性作为解释 RL 中 summary 信号弱的变量；用训练前/后交换做检验。增量可辨认，但不是独立的新机制。 |
| 有效性 | 5.5 | 当前依据：CompactionRL 106B 消融里，不训练 summary 已拿到压缩模式 7.0 分增益中的约 4.7 分；2610.35496 显示 agent 以重读补偿被删内容。这两条对判断 1 有中等支持，但都是单次运行，而且 106B、SWE 设置迁移到 4B 搜索设置并不直接成立。判断 2 的支持更弱：DSSR 的前滚打分只在短延迟下显著（+7.0），作者把限制归因于跨多次重写的信用分配；brief 只看单个边界后 h≈5 步，同样看不到"多次压缩后仍需保留"的价值。TRACE 语料报告的单边界伤害一致性也偏弱。BrowseComp-Plus 上 5 回合内很少能得出最终答案，所以记功主要靠"子目标命中"，而这个标签没有定义。如果它指命中新的 gold 证据文档，衡量的就是继续搜索的进展，而不是已见信息在 summary 中的保留。标签和 Claim 不对齐。还有一个未知：阻断后学到的"多保留"会不会在允许重读的测试环境里变成冗长、甚至有害。 |

与起点的关系：回答的是原问题中"收益来源"和"RL 回避压缩"两部分。跨模型族的 summarizer/actor 迁移仍未回答，只用同族 checkpoint 交换部分替代。转向本身不构成阻断。

实验能否判别主张：2×2 交换加重读计数能较干净地检验判断 1，而且成本低（可直接用对照 1 的 checkpoint）。这一部分是本 brief 最扎实的部分。判断 2 有两个问题。第一，"RBC 在交换到训练前 actor 时保留 summary 增益"只说明 summary 携带了更多 actor 无关的信息，不说明它在目标任务上有用：允许重读时准确率"不低于对照 1"是非劣判据，没有给出 RBC 在哪个实际指标上优于强基线（例如同准确率下更少回合/token、跨 actor 复用收益、真实不可重获取约束）。第二，推翻判据"无阻断分叉与 RBC 无差异则解释被推翻"把方法差异和解释混在一起：无差异也可能来自续写方差或 h 太短，并不能推翻"重获取掩盖"。同任务强基线方面，BrowseComp-Plus 上已有 ECHO（2606.31650，43.4% vs SUPO 36.1%）和 Self-Credit（2610.28388，Qwen3-8B）这类信用分配方法；summary 专属信号方面有 MMPO（belief entropy）和 InfoMem（答案条件信息增益），brief 都没有纳入。至少应有一个 summary 专属奖励的对照，否则"阻断续写优于其他 summary 记功方式"这一点无法检验。不过无阻断分叉这一组已经覆盖了 TreeMem/DSSR 式对照。

可行性：pass，但有明显风险。BrowseComp-Plus 语料、qrels 公开，FoldAgent 提供 verl 本地检索服务和训练脚本。阻断已见文档 ID 只需在检索服务层做过滤，实现简单。CompactionRL 跨段 GAE 没有代码，但规则已写明，可以独立复现。4 组单种子运行在 8×A100、5 天内大致可完成，但 1–1.5 天/次是外推值，没有实测；8K–16K 窗口下多次压缩的长轨迹 rollout 可能明显更慢。更大的风险在信号下限：BrowseComp-Plus 上小模型基线很低（论文中 Search-R1 32B 约 4–9%），Qwen3-4B 在 8K–16K 窗口下成功率可能接近地板，单种子下 2×2 交换差异难以分辨，Qwen3-8B 更合适。中途约束数据集需要新建，但可程序校验，标签含义清楚。

## 最高近邻
1. TreeMem, Tree-based Credit Assignment for Multi-Agent Memory System — https://arxiv.org/abs/2605.04811 ：把 summarizer 输出展开为多分支，用 Monte Carlo 平均给 summary 专属信用并加长度惩罚。差别：它是多智能体记忆管线，不是自写 compaction 的 agent，也没有阻断重获取。
2. DSSR, Decision-Sufficient State Representations: Measuring and Reducing Write-Time Regret — https://arxiv.org/abs/2609.32805 ：用前滚 reader 表现给候选 state 打分，再训练 writer（DPO），并给出 write-time regret 分解。差别：在 TextWorld 中事实不可重获取，偏好学习而非联合 RL；它已指出单步打分看不到跨多次重写的信用。
3. Benchmarks Are Surprisingly Compaction-Friendly — https://arxiv.org/abs/2610.31778 ：已提出"被丢内容大多可重获取，只有别处不存在的约束会丢失"，并量化约束丢失。差别：仅推理期、前沿闭源模型，不涉及 RL 训练信号。
4. CompactionRL — https://arxiv.org/abs/2607.05378 ：联合训练 summary 与执行，用 critic 和跨段 GAE；消融显示大部分增益不依赖 summary 训练。差别：没有配对交换，没有 summary 专属信号。
5. PAIR (2609.36526, https://arxiv.org/abs/2609.36526) / TRACE (2608.06503, https://arxiv.org/abs/2608.06503) ：同状态有无压缩的配对续写，隔离单次压缩事件，用于优化冻结模型的压缩 prompt。差别：不更新权重，不阻断重获取。

```json
{
  "score": 5.5,
  "contribution_scores": {"importance": 6.5, "novelty": 5.5, "effectiveness": 5.5},
  "contribution_assessment": "主贡献是解释 compaction agent RL 的增益主要来自执行器耐受（以 2×2 交换检验），再加上阻断重获取的兄弟 summary 续写记功。重要性中等：compaction RL 已进入生产管线，但在可重获取环境中执行器重读本身可用，summary 变好的价值主要在效率与不可重获取信息上，而后者只在合成约束上检验。新颖度受限：兄弟分叉加 summary 专属信用已有 TreeMem，前滚打分训练 writer 已有 DSSR，可重获取性解释已有 2610.31778，增量主要是续写阻断与 RL 期检验。有效性：判断 1 有 CompactionRL 消融和重读补偿研究的中等支持，但都是单次运行且跨规模、跨任务；判断 2 缺直接依据，DSSR 显示前滚打分只在短延迟有效，h≈5 的单边界续写看不到多次压缩后的保留价值。'子目标命中'标签未定义，可能衡量搜索进展而非 summary 保留。待验证：阻断训练出的 summary 在允许重读的测试中是否带来实际收益，而不是冗长。",
  "feasibility": "pass",
  "feasibility_reason": "BrowseComp-Plus 语料/qrels 公开，FoldAgent verl 环境含本地检索服务，阻断已见文档只需在检索层过滤；CompactionRL 可按原文复现；4 组单种子运行在 8×A100、5 天内大致可行。风险：每次 1–1.5 天为未实测外推；Qwen3-4B 在 8K–16K 窗口下 BrowseComp-Plus 成功率可能接近地板，单种子难以分辨差异。",
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "新颖度不足：兄弟 summary 分叉加 summary 专属信用（TreeMem 2605.04811）、前滚续写打分训练 writer（DSSR 2609.32805）、'可重获取性掩盖 compaction 损失'的解释（2610.31778）均已存在，剩余增量为续写阻断与 RL 期 2×2 检验，不足以支撑两项 ≥8",
    "Claim 阻断：短续写记功的'子目标命中'标签未定义；在 BrowseComp-Plus 上 h≈5 步内多数无法得到答案，标签可能衡量搜索进展而非 summary 对已见信息的保留",
    "Claim 阻断：支持判据只要求允许重读时准确率不低于对照 1，没有检验方法在任何目标指标（效率、跨 actor 复用、真实不可重获取约束）上的实际收益；推翻判据把方法无差异等同于解释被推翻，无法排除续写方差或 h 过短",
    "缺少同任务强对照：BrowseComp-Plus 上的 ECHO、Self-Credit，以及 summary 专属奖励（MMPO belief entropy / InfoMem）至少一个未纳入"
  ],
  "novelty_conclusion": "增量有限：核心机制（同状态多份 summary、后续分支结果给 summary 单独记功、长度惩罚）和核心解释（可重获取性）都已有近邻，独有部分是续写中阻断已见文档，以及在 RL 训练期用训练前/后交换检验，属于可辨认但不独立的增量。",
  "closest_neighbors": [
    "Tree-based Credit Assignment for Multi-Agent Memory System (TreeMem, arXiv 2605.04811)",
    "Decision-Sufficient State Representations: Measuring and Reducing Write-Time Regret (DSSR, arXiv 2609.32805)",
    "Benchmarks Are Surprisingly Compaction-Friendly (arXiv 2610.31778)",
    "CompactionRL: Reinforcement Learning with Context Compaction for Long-Horizon Agents (arXiv 2607.05378)",
    "Adapting Context Compression for Long-Horizon Agents with Counterfactual Continuations (PAIR, arXiv 2609.36526) / TRACE (arXiv 2608.06503)"
  ]
}
```
