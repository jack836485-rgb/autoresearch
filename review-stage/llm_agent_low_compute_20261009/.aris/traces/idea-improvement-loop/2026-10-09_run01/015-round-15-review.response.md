## 结论

日期：2026-10-09。**Score：7.1/10；Verdict：`promising_needs_revision`。** 代码层面的失败假设有真实入口：MemRL 的 ALFWorld runner 收集最终注入上下文的全部 memory ID，随后 `update_values` 将同一终局成功/失败奖励写给其中每个 ID；MemRL 论文也明确承认多记忆更新存在精确归因歧义。但“未采用条目因此被误罚并污染后续检索”仍是待验证诊断，不能写成已观察到的论文失败。按环境回执门控更新是一个清楚、低算力、可证伪的 MemRL 特化机制，但其一般机制与 EASE 的 retrieval/behavior attribution gates、EmbodiSkill 的 execution-lapse selective update 已部分重合。值得继续，但当前不应进入实验计划：最小实验只有 MemRL 内部更新消融与无记忆下界，遗漏了有公开实现、同为 ALFWorld 且与选择性更新直接相关的 MemP 和 EmbodiSkill；依固定 rubric，这是 fatal feasibility blocker。

## Claim 判断

| Claim | 判断 | 关键依据 |
|---|---|---|
| MemRL 对一次轨迹中所有最终检索并注入的 ID 赋同一终局奖励 | 已被证实，但表述需限于“最终 selected/injected memories” | 官方 runner 汇总 `retrieved_mems` 中全部 ID 后调用 `update_values(successes, retrieved_ids_list)`；该函数把同一 success/failure reward 逐个加入更新队列。[代码路径](https://github.com/MemTensor/MemRL/blob/main/memrl/run/alfworld_rl_runner.py#L967-L984)、[`update_values`](https://github.com/MemTensor/MemRL/blob/main/memrl/service/memory_service.py#L733-L783) |
| 失败轨迹会误罚未被行动采用的条目，并造成可测污染 | 新颖诊断假设，尚无结果支持 | MemRL 明确承认多记忆同时引用/更新时的 credit-assignment ambiguity，但没有报告“未采用误罚率”或其对成功率的因果影响；当前 brief 已正确把它写成待验证假设。[MemRL §G.2](https://arxiv.org/html/2601.03192#S13.SS2) |
| 仅对“声明引用且建议动作被环境回执证实执行”的 ID 更新效用 | 部分新颖 | 精确的同轮、per-ID、无训练回执门控在已核验近邻中未被直接覆盖；但 EASE 已用 retrieval incidence 与行为偏离双门控筛选有可观察影响的更新，EmbodiSkill 已按 execution lapse 避免错误修改有效技能。差别主要是更轻量的 MemRL 特化，而非新的通用 credit-assignment 原理。 |
| “被采用/改变行为”只构成更新支持，不等于因果贡献 | 已被覆盖 | EASE 明确把行为门控称为 approximate temporal attribution 而非 exact causal credit；CAMEO-TC 在 ALFWorld 上直接区分 outcome after retrieval 与 marginal contribution，并报告大量 passenger credit。[EASE](https://arxiv.org/html/2609.36746#S3.SS2)、[CAMEO-TC](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7160321) |
| 同预算四臂实验可检验机制 | 部分成立，当前有 fatal baseline 缺口 | 盲标、随机等量更新、self-report 与环境证据更新能分离“更新数量”及自报偏差，且失败时终止是可证伪设计；但既有三项对照主要是 MemRL 内部消融/下界，未纳入公开可复现的同任务 MemP 与 EmbodiSkill，尚不满足固定 rubric 的强 baseline 要求。 |

## 最高近邻

- [MemRL: Self-Evolving Agents via Runtime Reinforcement Learning on Episodic Memory](https://arxiv.org/abs/2601.03192)（[代码](https://github.com/MemTensor/MemRL)）：同一运行时 episodic-memory utility 学习与 ALFWorld；论文已提出多记忆精确归因问题，差别是本 idea 用同轮行动回执做 per-ID eligibility gate，而 MemRL 对全部 injected IDs 同奖惩。
- [EASE: Behavior-Adaptive Skill Curation for Self-Evolving Agents](https://arxiv.org/abs/2609.36746)：同在 ALFWorld，以 retrieval incidence 和行为偏离门控“有可观察下游影响”的更新，并明确不把它当因果贡献；差别是 EASE 训练 curator、使用后续任务及 skill-free 参考轨迹，本 idea 不训练且只用同轮环境回执。
- [EmbodiSkill: Skill-Aware Reflection for Self-Evolving Embodied Agents](https://arxiv.org/abs/2605.10332)（[代码](https://github.com/air-embodied-brain/EmbodiSkill)）：同为 training-free ALFWorld，区分 skill defect 与 execution lapse 以避免失败误改有效知识；差别是其用额外 LLM 反思并编辑全局技能文本，本 idea 门控 MemRL 条目 Q 值且不用额外 judge。
- [Does Memory Credit Travel? Paired Factorial Audits of LLM-Agent Memory](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7160321)：同在 ALFWorld，直接证明检索后的结果不能视为单条记忆的边际贡献，并测到 passenger credit；差别是其依赖成对反事实/阶乘重放做离线审计，不提供在线效用更新机制。
- [MemP: Exploring Agent Procedural Memory](https://arxiv.org/abs/2508.06433)（[代码](https://github.com/zjunlp/MemP)）：同为 ALFWorld 上可在线构建、检索和更新的程序性记忆，官方仓库给出 `run_memp_online.py` 复现入口；差别是没有按每条检索记忆的实际行动落实来门控标量效用，其遗漏构成当前最小实验的强基线缺口。

```json
{"score":7.1,"verdict":"promising_needs_revision","fatal_blockers":["最小实验遗漏有公开实现且同为 ALFWorld 的 MemP 与 EmbodiSkill；现有对照主要是 MemRL 内部消融和无记忆下界，不满足同任务强 baseline 与具体复现路线要求。"],"novelty_conclusion":"MemRL 的全 selected-ID 同奖惩及多记忆归因歧义有论文和源码支持；行动回执门控是清楚、低算力、尚未被直接覆盖的 per-ID 实现，但其一般思想已与 EASE 的 retrieval/behavior gates 和 EmbodiSkill 的 execution-lapse selective update 部分重合，且污染效应仍是待验证假设。","closest_neighbors":["MemRL: Self-Evolving Agents via Runtime Reinforcement Learning on Episodic Memory","EASE: Behavior-Adaptive Skill Curation for Self-Evolving Agents","EmbodiSkill: Skill-Aware Reflection for Self-Evolving Embodied Agents","Does Memory Credit Travel? Paired Factorial Audits of LLM-Agent Memory","MemP: Exploring Agent Procedural Memory"]}
```
