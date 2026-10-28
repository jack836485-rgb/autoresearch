## 结论

日期：2026-10-09。**Score：7.2/10；Verdict：`promising_needs_revision`。** 该候选把 MemRL 的检索诱导全局效用限制到可比较的共同支持，并用固定参考任务族权重检验暴露构成导致的排名反转；在已核验的 agent-memory 近邻中，尚未发现完全相同的 ALFWorld 诊断与估计对象。但其核心操作是分层条件均值加固定权重的直接标准化，是 logged bandit / covariate-shift 文献中的成熟校正思想，方法本身更像领域迁移而非新的估计机制。方案值得继续作为受控诊断研究，但当前不满足实验就绪门槛：暴露策略、支持矩阵构造和参考族权重尚未操作化，且无记忆 ReAct 未给出可执行复现入口。

## Claim 判断

| Claim | 判断 | 关键依据 |
|---|---|---|
| 不同检索暴露会使同一固定候选池的标量 Q 排名反转 | 部分重合 | MemRL 已明确写出全局 $Q(m)=\sum_s \mathbb{E}[r\mid s,m]\Pr(s\mid m)$，因此 Q 随检索诱导任务分布而变并非新发现；在固定共同支持的 ALFWorld 轨迹上是否出现实质排名反转，仍是清楚且尚未被验证的新经验假设。 |
| 固定参考任务族标准化能保持跨暴露账本的可比排名 | 部分重合 | agent-memory 近邻未见该具体实例；但按任务族估计条件回报后对固定目标分布加权，属于直接标准化/直接法，Counterfactual Risk Minimization 等更一般的 logged-feedback 校正已覆盖其统计结构，故机制新意有限。 |
| 标准化 Q 会比标量 Q 改善共同支持 held-out 成功率 | 新颖但未成立 | 最小实验可证伪该判断，并包含同任务族 Q 强对照；然而任务条件 Q 可能与标准化 Q 等效或更适合当前任务。当前未固定两种暴露概率、参考族权重及语义支持矩阵的构造规则，结果可随事后选择改变，构成主 Claim 阻断。 |
| 同预算最小实验具备可复现 baseline | 部分满足 | MemRL 的 ALFWorld runner、Q 更新和配置入口可公开核验，两个表格型 Q 对照也可直接本地实现；无记忆 ReAct 行仅写“同 runner 不注入 memory”，未给实际 flag/入口/命令或独立公开代码链接，按固定 rubric 属于 fatal feasibility blocker。 |

## 最高近邻

1. [MemRL: Self-Evolving Agents via Runtime Reinforcement Learning on Episodic Memory](https://arxiv.org/abs/2601.03192)：直接学习 episodic-memory 标量 Q，并明确其极限是按检索诱导的 $\Pr(s\mid m)$ 加权；候选的差别仅在共同支持上改为固定参考任务族权重。
2. [RoMeRL: Balancing Feedback Coverage and the Memory-Reward Trap in Self-Evolving Agent Memory via Reduced-Order Utility States](https://arxiv.org/abs/2608.02508)：已分解 task-level baseline 与 observational attribution bias，并指出更多暴露不能消除二者；其解法是每任务 $2\times2$ reduced-order utility state，而非参考分布标准化。
3. [Counterfactual Risk Minimization: Learning from Logged Bandit Feedback](https://proceedings.mlr.press/v37/swaminathan15.html)：处理由 logging policy 造成的暴露偏差并据此学习排序/决策；候选避免零支持与因果外推，采用更简单的分层直接标准化，但统计问题并非全新。
4. [Ask Only When Needed: Proactive Retrieval from Memory and Skills for Experience-Driven Lifelong Agents](https://arxiv.org/abs/2604.20572)：在 ALFWorld 等任务上用相同前缀的有/无检索配对 continuation 学习检索价值；它处理检索时机与因果过程奖励，不处理任务族暴露下的 memory 排名可比性。
5. [When Successful Memories Mislead Embodied Agents: Memory Adaption For Task-Conditioned Execution](https://arxiv.org/abs/2609.35808)：同样在 ALFWorld 研究历史成功经验在当前任务条件下失效；其机制是检索后的轨迹适配与动作规范化，不估计或校准暴露依赖的 Q。

```json
{
  "score": 7.2,
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "两种暴露策略、共同支持矩阵构造规则和固定参考任务族权重尚未在实验前操作化；当前可以通过事后选择制造或消除排名反转，主 Claim 不能唯一检验。",
    "无记忆 ReAct baseline 未给出已核验的公开实现链接及可执行入口或命令，未满足固定 rubric 的 baseline 复现证据要求。"
  ],
  "novelty_conclusion": "在 agent-memory/ALFWorld 中，共同支持上的暴露敏感性诊断具有清楚但有限的应用新意；核心固定参考加权是成熟直接标准化思想，尚不足以构成独立的新估计机制。",
  "closest_neighbors": [
    "MemRL: Self-Evolving Agents via Runtime Reinforcement Learning on Episodic Memory",
    "RoMeRL: Balancing Feedback Coverage and the Memory-Reward Trap in Self-Evolving Agent Memory via Reduced-Order Utility States",
    "Counterfactual Risk Minimization: Learning from Logged Bandit Feedback",
    "Ask Only When Needed: Proactive Retrieval from Memory and Skills for Experience-Driven Lifelong Agents",
    "When Successful Memories Mislead Embodied Agents: Memory Adaption For Task-Conditioned Execution"
  ]
}
```
