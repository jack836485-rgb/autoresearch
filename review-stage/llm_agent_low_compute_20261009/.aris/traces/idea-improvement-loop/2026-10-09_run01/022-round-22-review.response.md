## 结论

以 2026-10-09 为检索截止日，**score：8.1/10；verdict：`experiment_ready`**。新意判断为**机制级部分新颖**：把“只检索未采用的记忆不应承受失败负奖”作为一般原则，已被 TIDE 的 responsibility credit 明确覆盖；但在已核验近邻中，尚未发现工作把 **actor 的 memory/template 绑定、ALFWorld 实际 `env.step` 动作及环境回执**组合成无需训练、无需反事实 rollout 的**负向 memory-Q 更新资格门**。该方案值得继续进入实验规划，因为 Claim 已限制为“执行支持是负更新的最低资格”，没有冒充边际因果归因；污染效应仍被明确写成待盲标、待实验验证的假设。MemRL、EmbodiSkill、MemP 均有同任务公开实现和具体入口，本地 self-report、等次数随机及无 memory 对照也能在同一 runner 内实现；MemP adapter 尚未实跑是实现风险，不构成当前阶段的 fatal blocker。

## Claim 判断

| Claim | 判断 | 关键依据 |
|---|---|---|
| MemRL 将同轮最终注入的多个 memory ID 一并按终局成败更新，存在“出现即有更新资格”的入口 | 已被证实 | [MemRL 论文](https://arxiv.org/html/2601.03192v2) §4.3 明言更新全部注入上下文的记忆，§G.2 承认多记忆同时引用时的 credit-assignment ambiguity；公开 [ALFWorld runner](https://github.com/MemTensor/MemRL/blob/main/memrl/run/alfworld_rl_runner.py) 汇总全部 `retrieved_mems` ID，[MemoryService](https://github.com/MemTensor/MemRL/blob/main/memrl/service/memory_service.py) 对每个 ID 写入同一 success/failure reward。 |
| “只被检索、未被实际采用的记忆不应接收结果反馈” | 部分重合，不能作为独立首创 | [TIDE](https://arxiv.org/html/2609.37544v2) §3.4 已要求记忆实际被使用、与决策对齐且通过移除反事实，明确规定 retrieved but did not affect the decision 的记忆不得 credit。当前方案的新意只能落在更窄的负更新 eligibility 与环境执行证据上。 |
| 用 `memory_id + template_id + bindings` 声明，经合法动作实例化、实际动作匹配和环境回执确认后，才允许该 ID 接收失败负奖 | 新颖，但属于低成本支持证据而非因果归因 | [EFCA](https://arxiv.org/html/2608.08255v1) 已在 ALFWorld 用环境反馈判断动作局部有效性，[MATE](https://arxiv.org/html/2609.35808v1) 已做确定性动作规范化；二者都未把“记忆到已执行动作”的显式绑定用于门控 MemRL 式负 Q 更新。方案也明确不声称同一动作由该记忆因果导致，避免了过度 Claim。 |
| 失败可能来自 execution lapse，因此不能据终局失败直接惩罚有效指导 | 部分重合 | [EmbodiSkill](https://arxiv.org/html/2605.10332v2) 已在 ALFWorld 区分 SkillDefect 与 ExecutionLapse，并在后者发生时保留 skill body。当前方案的差别是不用反思模型判类，只验证具体记忆建议是否落实，并只控制负 Q 更新资格。 |
| 执行绑定会降低未落实条目的误罚，并在同预算下改善 held-out 成功率或后续误弃 | 待验证，不是既有事实 | brief 已把负污染规模写为待盲标诊断，并给出 self-report、等次数随机、MemRL、EmbodiSkill、MemP、无 memory 对照及明确失败条件；因尚无实验，该项只能作为可证伪假设。 |

## 最高近邻

1. [TIDE: How Can Recommendation Feedback Evolve Agent Memory?](https://arxiv.org/html/2609.37544v2)：最高概念近邻；同样只给实际负责的记忆分配反馈，但还要求语义对齐与反事实回放，任务是推荐内容生成而非 ALFWorld，成本与目标均不同。
2. [MemRL: Self-Evolving Agents via Runtime Reinforcement Learning on Episodic Memory](https://arxiv.org/html/2601.03192v2)（[代码](https://github.com/MemTensor/MemRL)）：直接方法与同任务基座；它给全部注入记忆同一终局奖励，当前方案只替换失败时的更新资格。
3. [EmbodiSkill: Skill-Aware Reflection for Self-Evolving Embodied Agents](https://arxiv.org/html/2605.10332v2)（[代码](https://github.com/air-embodied-brain/EmbodiSkill)）：同为 ALFWorld、无权重训练并处理 execution lapse；其机制是 LLM 反思与 skill 编辑，当前方案是确定性的动作绑定和负 Q 门控。
4. [EFCA: Learning from Environmental Feedback](https://arxiv.org/html/2608.08255v1)：同在 ALFWorld 利用环境回执做细粒度动作 credit；它重加权参数化 RL 的 step return，不追踪外部记忆是否被采用，也不满足无训练设定。
5. [MATE: When Successful Memories Mislead Embodied Agents](https://arxiv.org/html/2609.35808v1)：同在 ALFWorld 以确定性动作规范化和固定检索控制诊断 memory negative transfer；它改造检索后表示而不学习 memory utility，也不处理多记忆失败负奖。

```json
{"score":8.1,"verdict":"experiment_ready","fatal_blockers":[],"novelty_conclusion":"一般性的‘未使用记忆不应获得结果反馈’已被TIDE覆盖；新意保留在ALFWorld中以actor声明、动作模板实例化、实际env.step匹配和环境回执构成无训练、无反事实的负向memory-Q更新资格门。该新意足以进入实验规划，但只能声称执行支持的最低资格，不能声称边际因果归因或既已观察到污染效应。","closest_neighbors":["TIDE (arXiv:2609.37544)","MemRL (arXiv:2601.03192)","EmbodiSkill (arXiv:2605.10332)","EFCA (arXiv:2608.08255)","MATE (arXiv:2609.35808)"]}
```
