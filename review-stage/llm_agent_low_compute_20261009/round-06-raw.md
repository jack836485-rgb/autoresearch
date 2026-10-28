## 结论

日期：2026-10-09。**score：6.8/10；verdict：`promising_needs_revision`。** 固定 ALFWorld 六任务族参考分布、对每条记忆的分族观察效用做直接标准化，这个具体组合尚未发现被完整实现；它无需额外 rollout，诊断也可证伪。但核心问题的新意已明显收窄：[MemRL](https://arxiv.org/html/2601.03192v2) 已明确写出全局 \(Q(m)\) 是按检索依赖的 \(P(s\mid m)\) 加权，[RoMeRL](https://arxiv.org/abs/2608.02508) 又在同一 runtime memory 与 ALFWorld 场景中区分了 observational raw return、task-level baseline、retrieval selection/context confounding，并使用 per-task reduced-order utility state。

值得继续做低成本诊断，不值得按当前版本进入完整实验规划。致命阻塞是：最直接近邻 RoMeRL 未进入新意边界；语义候选门控下“少量随机探索”不能保证 memory × task-family 的交叉支持，低覆盖回退语义排序又使不同记忆的分数不再是同一 estimand；而冻结评分后仅改变评估 task mix 不会改变固定排名，当前文字没有给出能实际检验“检索策略诱发排名反转”的明确操作。另有显著功效风险：公开结果显示 ALFWorld 六类确有难度差异，但近期工作也报告干净 ALFWorld 上记忆策略差异常落在置信区间内。

## Claim 判断

| Claim | 判断 | 关键依据 |
|---|---|---|
| MemRL 的单一全局 \(Q(m)\) 混合了记忆被调用时的任务分布 | 已被覆盖 | MemRL Eq. 9 直接给出 \(Q(m)=\sum_s E[r\mid s,m]P(s\mid m)\)，并称 \(P(s\mid m)\) 由检索策略决定；RoMeRL 进一步把 raw return 与 task-level baseline、selection/context attribution bias 分开。 |
| 固定真实任务流时，仅改变检索策略会导致同一批经验发生可重复排名反转并伤害成功率 | 新颖但未验证 | [ReAct](https://arxiv.org/abs/2210.03629) 的 ALFWorld 分任务成功率证明六类难度可显著不同，因果故事有现实支点；但尚无一级结果证明 MemRL 中这一差异经检索暴露转化为排名反转或成功率损失，brief 正确地将其写成待诊断假设。 |
| 用六类条件成功率和预先固定参考权重得到分布不变的记忆分数 | 部分重合 | 固定参考分布标准化本身未在所查 agent-memory 工作中直接复现；但 RoMeRL 已按 task 组织效用状态，且该分数仍是 \(E[R\mid m\text{ 被检索},g]\)，不能去除族内难度、语义候选选择或上下文交互。 |
| 少量随机探索足以保证分族估计支持，低覆盖时回退语义排序 | 未成立 | 若探索只在语义候选集内进行，候选集外的 memory × family 单元选择概率仍为零；回退项与有覆盖项使用不同目标量，因此固定参考混合分数未必可比较。 |
| 冻结评分后在自然 mix 与重排 mix 上评估可验证排名反转机制 | 部分成立 | 两种 mix 可检验成功率稳健性，但评估 mix 本身不会改变冻结的排序；brief 未明确排名反转究竟来自两种检索策略各自的在线更新，还是仅来自冻结后的评估重排，机制检验合同不闭合。 |
| MemRL、semantic-only、无记忆构成可复现的同任务 baseline | 部分成立 | 三者均可由 [MemRL 官方仓库](https://github.com/MemTensor/MemRL) 的 ALFWorld runner 构造；但最高近邻 RoMeRL 未被核验，且其[公开仓库](https://github.com/YOUNG-fnxm/RoMeRL)明确只发布只读评估路径、排除 Q 更新与记忆构建，不能当作已有开放核心实现的可运行 baseline。 |

## 最高近邻

1. [RoMeRL: Balancing Feedback Coverage and the Memory-Reward Trap in Self-Evolving Agent Memory via Reduced-Order Utility States](https://arxiv.org/abs/2608.02508)：直接研究 MemRL 式 observational utility 的 task baseline、retrieval selection 与 context confounding，并在 ALFWorld 使用 per-task utility state；差别是固定四坐标压缩与污染控制，不是按六类固定参考分布标准化。
2. [MemRL: Self-Evolving Agents via Runtime Reinforcement Learning on Episodic Memory](https://arxiv.org/abs/2601.03192)：候选的直接母体，已明确给出检索依赖的全局效用混合并定义理想的 \(Q(s,m)\)；差别是实现仍为每条记忆单一 \(Q_i\)，没有六任务族标准化或排名反转诊断。
3. [Selective Memory Retention for Long-Horizon LLM Agents](https://arxiv.org/abs/2606.29178)：同在 ALFWorld，以成功、访问频率、下游效用和置信度等特征管理经验，并发现干净设置接近饱和；差别是容量约束下的 retention/eviction，不校正检索诱导的任务族构成。
4. [Causal Intervention-Based Memory Selection for Long-Horizon LLM Agents](https://arxiv.org/abs/2605.17641)：同样质疑观察性相关与真实记忆效用的等同，并以受控干预估计 query-specific 贡献；差别是 LoCoMo 派生任务且需要额外模型调用，候选明确不主张因果贡献。
5. [When Successful Memories Mislead Embodied Agents: Memory Adaptation for Task-Conditioned Execution](https://arxiv.org/abs/2609.35808)：在 ALFWorld 直接证明成功轨迹对当前任务仍可能不适用，并做无额外 LLM 推理的 task-conditioned 处理；差别是修正轨迹内容与动作表示，不学习或标准化检索效用。

```json
{"score":6.8,"verdict":"promising_needs_revision","fatal_blockers":["RoMeRL 已在同一 runtime-memory/ALFWorld 场景覆盖 observational raw return、task-level baseline 与检索/上下文混杂，当前 brief 未纳入该最高近邻，剩余新意仅是六任务族固定参考分布标准化","语义候选门控下的少量随机探索不能保证 memory × task-family 交叉支持；低覆盖回退语义排序使分数使用不同 estimand，固定参考混合值未必可比较","冻结评分后只改变评估 task mix 不会改变固定经验排名；当前最小实验没有明确能产生并检验 retrieval-induced ranking reversal 的操作"],"novelty_conclusion":"全局 Q 受检索分布影响已由 MemRL 明示，观察性记忆效用及任务混杂又被 RoMeRL 直接覆盖；固定六任务族参考分布的直接标准化仍有窄的新意，但支持集与机制实验尚未闭合。","closest_neighbors":["RoMeRL: Balancing Feedback Coverage and the Memory-Reward Trap in Self-Evolving Agent Memory via Reduced-Order Utility States","MemRL: Self-Evolving Agents via Runtime Reinforcement Learning on Episodic Memory","Selective Memory Retention for Long-Horizon LLM Agents","Causal Intervention-Based Memory Selection for Long-Horizon LLM Agents","When Successful Memories Mislead Embodied Agents: Memory Adaptation for Task-Conditioned Execution"]}
```
