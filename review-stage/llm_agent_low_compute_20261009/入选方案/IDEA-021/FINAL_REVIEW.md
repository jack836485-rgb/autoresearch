## 结论

日期：2026-10-09。**score：8.2/10；verdict：`experiment_ready`。** 新意成立在目标域与机制组合层面：time-limit truncation、右删失和 competing risks 都是既有概念，但在已核验的 LLM agent memory 工作中，尚未发现用随机执行上限产生的删失记录估计“预算内成功累计概率”，再据当前预算选择 episodic memory 的直接先例。该候选没有把诊断假设冒充已观察失败；MemRL 的超时轨迹确实被记为 `success=False` 并进入统一负奖励更新，而“因此长期有效经验被持续误弃”仍被正确保留为待验证命题。随机 cap、同一硬预算、`k=1`、skip-update 与 budget-conditioned Q 对照使额外机制可被明确否定。值得继续进入实验规划；未见致命 novelty、feasibility 或 claim blocker。

## Claim 判断

| Claim | 判断 | 关键依据 |
|---|---|---|
| MemRL 将执行上限处的未完成与失败统一负更新 | 已核验，不是新颖贡献 | [MemRL 论文](https://arxiv.org/abs/2601.03192)用标量 Q 学习终局 reward；[官方代码](https://github.com/MemTensor/MemRL)的 ALFWorld runner 在 `max_steps` 后把仍 active 的轨迹写成 `success=False`，`update_values` 再将 false 映射到 `failure_reward=-1.0`。 |
| 这种混合会使长而有效的经验在充足预算下仍被误弃 | 新颖且可证伪的诊断假设，尚非既成事实 | 现有代码只证明污染通道存在，未证明效应量；先检查“短前缀未完成、长轨迹后续成功”，再测跨预算排序和经验误弃，证据链成立。 |
| 用 competing-risks 累计发生函数对每条经验做预算条件化排序 | 目标域内新颖；统计机制与既有工作部分重合 | [Time Limits in Reinforcement Learning](https://proceedings.mlr.press/v80/pardo18a.html)已说明 timeout 不应无条件视为终止；但它不处理 LLM episodic-memory 检索。[UpliftMem](https://arxiv.org/abs/2609.36805)与 MemRL 学习执行反馈下的记忆效用，却未建模右删失完成时间或按执行上限查询成功累计概率。 |
| 同预算 ALFWorld 实验可把删失校正与“简单不更新”区分开 | 新颖性有限，但因果设计与可行性充分 | cap 在选定 memory 后随机分配，方法共享 actor、memory bank、任务流、cap 分配及 token/工具硬上限；MemRL、semantic-only、budget-conditioned Q、skip-update 和删失分布对照直接覆盖主要替代解释，且官方 ALFWorld 入口可复现。 |

## 最高近邻

- [MemRL: Self-Evolving Agents via Runtime Reinforcement Learning on Episodic Memory](https://arxiv.org/abs/2601.03192)（[代码](https://github.com/MemTensor/MemRL)）：同为 ALFWorld、冻结 LLM、运行时环境反馈和记忆效用排序；差别是单一标量 Q 把 cap 未完成映射为失败，不学习预算条件化完成分布。
- [UpliftMem: Learning Set-Level Uplift for Agent Memory Retrieval](https://arxiv.org/abs/2609.36805)：同为 ALFWorld、执行反馈驱动的记忆价值学习，并显式匹配 rollout budget；差别是学习相对 no-memory 的集合级 uplift、用额外 probe 与 LoRA scorer，执行 cost cap 不是右删失标签，未公开原作者实现仓库可供同预算复现。
- [Time Limits in Reinforcement Learning](https://proceedings.mlr.press/v80/pardo18a.html)：直接覆盖“时间上限终止不等于自然终止”及其错误处理造成的偏差；差别是经典 RL 的状态/bootstrapping 处理，不涉及 LLM episodic memory、ALFWorld 或累计成功概率检索。
- [Learning Hierarchical Procedural Memory for LLM Agents through Bayesian Selection and Contrastive Refinement (MACLA)](https://arxiv.org/abs/2512.18950)（[代码](https://github.com/S-Forouzandeh/MACLA-LLM-Agents-AAMAS-Conference)）：同为冻结 LLM、ALFWorld 和基于成功/失败可靠性的程序记忆选择；差别是 Beta/Bayesian reliability 与层级程序抽取，不区分预算截断和真正失败。
- [AdaMEM: Test-Time Adaptive Memory for Language Agents](https://arxiv.org/abs/2606.05684)（[代码](https://github.com/yunx-z/AdaMEM)）：同在 ALFWorld 研究不同 inference-time compute 下的记忆使用；差别是逐步动态策略记忆与刷新频率，不从删失轨迹估计给定步数内的经验成功率。

```json
{"score":8.2,"verdict":"experiment_ready","fatal_blockers":[],"novelty_conclusion":"统计工具与 timeout 语义已有先例，但在 LLM episodic-memory/ALFWorld 中以随机执行上限形成右删失记录、估计预算内成功累计概率并用于预算条件化检索，具有清楚且可证伪的新意边界。","closest_neighbors":["MemRL (arXiv:2601.03192)","UpliftMem (arXiv:2609.36805)","Time Limits in Reinforcement Learning (ICML 2018)","MACLA (arXiv:2512.18950)","AdaMEM (arXiv:2606.05684)"]}
```


主执行器说明：Call 3 选择时IDEA-021为8.6分eligible池领跑；独立分8.2严格>7.5且无fatal blockers。方案已展开，统计独立性、数据稀疏和API成本尚待实验。审阅为same-family、fresh_zero_context、provisional。
