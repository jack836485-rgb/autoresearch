## 结论

实际检索日期：**2026-10-10**。**score：6.0；verdict：needs_rethink。**

当前方案有明确的工程研究价值：区分经验版本的文字变化、实际动作变化与后继消息变化，避免无条件继承旧评价。但存在 **fatal novelty blocker**：在共同初始状态、一次暴露、相同完整动作和共同后继策略这些条件下，提案就是经典 coupled trajectory sampling 的直接适配；将正文和理由排除出后继请求，使这些版本进入同一完整决策状态，并没有建立独立的新复用机制。保留理由可能改变后续行为也已有 ReAct 的直接依据。

目标演化成立。RoMeRL 的代表替换及效用继承、EviSkill 的编辑验证，支持从 Q004 的经验保留／淘汰问题聚焦到“编辑后哪些旧评价仍有效”。未覆盖选择混杂和过量验证不构成拒绝理由。当前文献阶段符合硬约束，尚无实测解决证据。

最小实验可以证伪成本收益，基线也具备实现入口；但经典 coupled baseline 获得相同接口后，已经与提案结构等效。2×2 能识别接口切断的影响，不能据此证明独立的复用创新。

## Claim 判断

| Claim | 判断 | 最关键原文依据与可验证性 |
|---|---|---|
| 相同执行状态、完整动作及共同后继策略允许继承后继结果 | **已覆盖** | Dann 等 §4、Algorithm 2 明确按相同 state/action 共享后继样本；共同后继策略允许继续共享。当前一次暴露边界是其特殊情形。[原文](https://proceedings.mlr.press/v206/dann23a/dann23a.pdf) |
| 正文／理由保留时，同工具动作不足以证明后继等效 | **部分重合，应用边界有价值** | ReAct §2 将 thoughts 纳入推理轨迹；附录 A.3 展示编辑 thoughts 改变后续行为。AppWorld 默认实现还保留完整模型消息及 thinking。因此“动作相同但完整 agent 状态不同”已有依据；具体经验编辑中的发生率仍可测。[ReAct](https://arxiv.org/html/2210.03629)、[AppWorld 实现](https://raw.githubusercontent.com/StonyBrookNLP/appworld/main/experiments/code/simplified/react_code_agent.py) |
| 新正文不同仍可复用，因此超出完整 prompt 缓存 | **部分重合，不能确立独立新意** | TVCache 已依据完整工具历史，而非完整 LLM prompt，复用有状态工具结果。它不复用 LLM 后继决策或编辑准入评价，故没有完全覆盖应用目标；该剩余部分由经典共同后继采样直接覆盖。[TVCache §3及附录](https://arxiv.org/html/2602.10986) |
| 可降低编辑准入成本且不提高错误准入率 | **待验证，当前支持不足** | 节省取决于动作重合率和恢复费用；共享样本的相关性也不等于准入错误率不变。随机后继的旧结果是一个合法样本，并非独立全重测必然得到的相同终态。可测成本和错误率，但不能由动作相同直接推出。 |
| 计入新 proposal 费用后，旧 suffix 成本／结果仍可继承 | **条件尚不完整** | AppWorld 执行循环按累计 usage 超预算终止。不同经验正文可产生不同 proposal 费用，使相同动作后的剩余预算不同；相同 formatter 和策略代码不足以保证相同停止过程。这是当前支持用法可达的边界，不是罕见构造。[执行循环](https://raw.githubusercontent.com/StonyBrookNLP/appworld/main/experiments/code/simplified/agent.py) |

复现方面，AppWorld 的生成、真实代码执行、usage 记录和任务循环入口均已核验；重执行 prefix 的定义可实现。EviSkill 官方 pipeline 确实调用 `runner.run_from_trace_range`，支持所列局部重执行适配，但本次未逐函数核验 runner 的全部恢复逻辑，不能认定完整官方复现。RoMeRL 仓库明确只发布 eval-only；Brief 已将对照标为代表 Q 继承／reset 的参考实现，这个表述准确，不构成伪复现。[EviSkill pipeline](https://raw.githubusercontent.com/Zhouyaner/EviSkill/main/wmsm/evidence_pipeline.py)、[RoMeRL 仓库](https://github.com/YOUNG-fnxm/RoMeRL)

## 最高近邻

1. **Multiple-policy High-confidence Policy Evaluation，Dann 等，2023。** 已核验 §4、Algorithm 2。重合是同 state/action 共享采样及按策略分歧控制重测。当前差别是 LLM 经验编辑、一次暴露和具体消息接口；这些条件使其成为原机制的直接实例。它是机制近邻，AppWorld 对照应称适配实现。[原文](https://proceedings.mlr.press/v206/dann23a/dann23a.pdf)

2. **TVCache: A Stateful Tool-Value Cache for Post-Training LLM Agents，2026。** 已核验正文及附录。重合是完整工具历史匹配、状态一致时复用执行结果；差别是原作主要缓存工具值，未继承经验编辑的整段后继 LLM 评价。它不是同任务准入 baseline。[原文](https://arxiv.org/html/2602.10986)

3. **EviSkill: Grounding Skill Evolution in Replayable Evidence，2026。** 已核验 §3.2、C.3、F.2及 pipeline 调用。重合是源 prefix 恢复、编辑支持区间验证和降低重执行费用；差别是 EviSkill 仍执行目标区间，没有依据动作相同直接继承完整 suffix。[原文](https://arxiv.org/html/2610.05030v1)

4. **RoMeRL: Balancing Feedback Coverage and the Memory-Reward Trap in Self-Evolving Agent Memory via Reduced-Order Utility States，2026。** 已核验代表替换及 Eq.21。重合是新代表继承旧效用；差别是原作采用 warm-start 后更新，没有行为等效的继承域。它确立问题来源，却不能替代最强 coupled 对照。[原文](https://arxiv.org/html/2608.02508)

5. **ReAct: Synergizing Reasoning and Acting in Language Models，2022／ICLR 2023。** 已核验 §2及 A.3。重合是理由作为后续决策状态，修改理由可以改变后继行为；差别是原作未研究旧评价继承。它削弱“理由通道影响继承”作为独立机制创新的主张。[原文](https://arxiv.org/html/2210.03629)

```json
{
  "score": 6.0,
  "verdict": "needs_rethink",
  "fatal_blockers": [
    "当前继承机制在所声明的一次暴露、相同执行状态和共同后继策略边界内，与经典coupled trajectory sampling结构等效；正文或理由保留导致完整决策状态不同也已有ReAct依据。当前尚无独立机制新意。"
  ],
  "novelty_conclusion": "经验编辑评价的继承边界具有工程诊断价值，但当前方法是成熟同状态同动作样本复用的直接适配。最小实验能检验成本收益和接口影响，不能使结构等效于经典基线的机制获得独立新意。错误准入率不增加仍需验证，累计预算导致的停止状态差异尚未明确。",
  "search_performed": true,
  "closest_neighbors": [
    {
      "title": "Multiple-policy High-confidence Policy Evaluation",
      "url": "https://proceedings.mlr.press/v206/dann23a/dann23a.pdf",
      "overlap": "同state/action共享后继采样，按策略分歧减少评估采样。",
      "difference": "当前是LLM经验编辑及一次暴露接口的特殊实例，未建立额外复用机制。",
      "verified": true
    },
    {
      "title": "TVCache: A Stateful Tool-Value Cache for Post-Training LLM Agents",
      "url": "https://arxiv.org/html/2602.10986",
      "overlap": "完整工具历史匹配确保执行状态一致，并复用工具执行结果。",
      "difference": "原作缓存工具值，不继承经验编辑后的整段LLM后继评价；不是同任务准入baseline。",
      "verified": true
    },
    {
      "title": "EviSkill: Grounding Skill Evolution in Replayable Evidence",
      "url": "https://arxiv.org/html/2610.05030v1",
      "overlap": "恢复源prefix并对编辑支持区间开展局部验证，减少重执行费用。",
      "difference": "原作重新执行目标区间，没有依据相同完整动作直接继承整个suffix。",
      "verified": true
    },
    {
      "title": "RoMeRL: Balancing Feedback Coverage and the Memory-Reward Trap in Self-Evolving Agent Memory via Reduced-Order Utility States",
      "url": "https://arxiv.org/html/2608.02508",
      "overlap": "代表替换继承旧效用，并通过后续更新修正warm-start偏差。",
      "difference": "原作没有建立基于行为等效的评价继承域；官方仓库尚不提供在线效用学习与替换循环。",
      "verified": true
    },
    {
      "title": "ReAct: Synergizing Reasoning and Acting in Language Models",
      "url": "https://arxiv.org/html/2210.03629",
      "overlap": "理由轨迹参与后续决策，编辑理由可以改变后继行为。",
      "difference": "原作未研究经验编辑后的旧评价继承。",
      "verified": true
    }
  ],
  "goal_assessment": {
    "within_initial_scope": true,
    "hard_constraints_satisfied": true,
    "evolution_supported": true,
    "reason": "当前仍研究冻结LLM软件agent的经验保留与编辑评价。RoMeRL的代表替换效用继承和EviSkill的局部编辑验证支持这一聚焦；无需覆盖全部初始drawbacks。当前仅检索与交接，没有执行实验或调用付费推理API，没有将隐藏终态提供给方法runtime。低显卡、预算对齐及待确认参数要求均被保留；预算停止状态仍是后续实验定义中的真实技术边界。"
  }
}
```