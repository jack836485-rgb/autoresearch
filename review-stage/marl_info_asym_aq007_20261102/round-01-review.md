## 结论

评审日期 2026-11-02。**score 5.5 / 10，verdict：promising_needs_revision。**

新颖性判断：把"答题者可见信息"作为调节变量，检验联合训练相对"同结构单智能体 RL"何时有正增益，这个问题框架目前没有被直接覆盖。2605.24202（项目页 2026-11-01 同步版）只做信息对称的数学/代码工作流，结论是"角色跨轮相互响应时联合训练才有用"；Dr. MAS 的搜索编排里各角色共享完整历史；MultiAgent-OPD 训练了 Searcher→摘要→Answerer 工作流，但没有做同结构单智能体反事实，也没有改变可见性。不过新颖边界还没定下，原因有三：

1. **Claim 阻断**：核心前提"上游学会传什么是单智能体训练不会产生的技能"有反证。MemSearcher、MEM1 等单智能体 RL 本来就在端到端学习"把与问题相关的信息压缩成紧凑记忆，交给后续上下文"。本方案选的单智能体反事实是 Search-R1 式完整历史模型，被直接放进"只看报告"的结构里，写报告和只看报告作答对它都是分布外。Claim 2 因此近乎必然成立，区分不了"多智能体联合训练"和"任何在同一信息瓶颈下做的 RL 训练"。共享策略的"搜索者→报告→答题者"与"单智能体自写报告、清空上下文再作答"几乎是同一个优化问题，这里的界限也没有讲清。
2. **Claim 3 部分重合**：s3 和 MultiAgent-OPD 已经说明，针对冻结或下游生成器训练搜索/摘要方能带来大部分增益。"增益落在传递方"在方向上已有证据，新增的只是在同结构单智能体反事实下的剂量与角色交换。
3. **可行性阻断（baseline 路线不匹配）**：核心反事实 SA-RL 写明"用 Dr. MAS 仓库 `examples/grpo_trainer/run_search.sh` 复现"。经核验，该脚本是 3 个 agent、`orchestra_type=search` 的多智能体 vanilla GRPO（与 `drmas_trainer` 版只差 `group_by_agent_id`），并不是单智能体。仓库里 `verl/trainer/main_ppo.py` 和 `ray_trainer.py` 都有 `assert config.agent.multi_agent`，单智能体模式在发布代码中被禁用。所以"同栈训练 SA-RL"这条路线现在不存在。Search-R1 原仓库（`train_grpo.sh`）可用但不同栈，verl-agent 有 `examples/gigpo_trainer/run_search.sh`，这两条都还没写进方案、也没核验参数对齐。

其余方面：定位关键词都是成熟术语；Search-R1 与 Dr. MAS 同任务同检索器，属于同域 baseline；Dr. MAS 3B 上单/多智能体约 2–3 点差距、无同结构对照的描述与其 Table 2 一致；2605.24202 的描述与项目页一致；算力（约 1440 A100·h，单次运行远低于 5 天）在约束内。值得继续，但目前不能进入实验。

## Claim 判断

| Claim | 判断 | 最关键依据 |
|---|---|---|
| 前提：信息对称时联合训练难以超过同结构 SA-RL；"传什么"只能由联合训练习得 | 前半句有证据；后半句**无支撑且有反证** | 2605.24202 项目页确有"SA-RL 同结构打平或胜过 Voting/Orch-Workers"的结论；MemSearcher（2511.02805）、MEM1（2506.15841）用单智能体 RL 学会压缩、传递问题相关信息 |
| 1. 对称档联合训练相对同结构 SA-RL 增益不显著 | 部分重合 | 是 2605.24202 结论在检索任务和 3 种子下的复现。Dr. MAS 3B 的 MA vs SA 差距约 2–3 点，但对照不是同结构；有增量但本身不构成新意 |
| 2. 隔离档联合训练显著超过同结构 SA-RL，且随报告上限收紧而变大 | 新颖但**几乎必然成立，检验力弱** | 同结构 SA-RL 从没训练过写报告和只看报告作答，差距可能只是格式或分布适配；缺少"单智能体在同一瓶颈下训练"（MemSearcher 式自摘要）这一反事实 |
| 3. 增益主要在传递方（联合搜索者 + SA 答题者恢复 ≥50%） | 部分重合 | s3（2505.14146）只训练搜索方、生成器冻结即可获益；MultiAgent-OPD（2610.23234）的 Searcher 摘要训练；MATPO（2510.04678）的 worker 摘要→planner 联合训练 |
| 方法：可见性剂量 + 角色交换 | 组合有一定新意 | 剂量设计是本方案独有；但编排、优势归一化和隔离结构都来自已有工作 |

## 最高近邻

1. **When Does Multi-Agent RL Improve LLM Workflows?**（https://arxiv.org/abs/2605.24202 ；项目页 https://github.com/XHMY/marl-llm-workflows ，2026-11-02 提交"sync with the paper of 2026-11-01"）。重叠：同结构 SA-RL 反事实、SP/IP 对比，以及"跨轮相互响应才有增益"的结论。差别：只做信息对称的数学/代码工作流、每格单种子，没有工具使用，也没有可见性变量。
2. **Dr. MAS**（https://arxiv.org/abs/2602.08847 ，https://github.com/langfengQ/DrMAS ）。重叠：同一个三角色搜索编排、E5 + Search-R1 设置、共享/非共享、按角色归一化。差别：所有角色共享完整 team_context，单智能体对照是单次回答而不是同结构；发布代码不支持单智能体训练。
3. **MultiAgent-OPD**（https://arxiv.org/abs/2610.23234 ，2026-10）。重叠：Leader–Searcher–Answerer，Answerer 只依据 Searcher 的报告作答，同样 7 个 QA 集，有 C-MAS + RL（联合训练的级联搜索→报告→答题）。差别：目标是蒸馏加过程监督，没有同结构 SA-RL 反事实，也没有改变可见性。
4. **MemSearcher**（https://arxiv.org/abs/2511.02805 ）/ **MEM1**（https://arxiv.org/abs/2506.15841 ）。重叠：单智能体 RL 在信息瓶颈下学会"保留什么、传什么"，直接挑战"这一技能只来自联合训练"的前提。差别：不是多角色，也不比较联合与单智能体训练。
5. **s3**（https://arxiv.org/abs/2505.14146 ）。重叠：搜索方与生成器解耦，只训练搜索方以服务冻结的生成器，与 Claim 3"增益在传递方"同向。差别：不做多智能体联合训练对比，也没有可见性剂量。

```json
{
  "score": 5.5,
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "claim: premise that learning 'what to transmit' cannot arise from single-agent RL is unsupported and contradicted by single-agent RL with learned memory compression (MemSearcher 2511.02805, MEM1 2506.15841); the chosen same-structure SA-RL counterfactual is out-of-distribution in isolated arms, so Claim 2 cannot separate joint multi-agent training from any RL trained under the same information bottleneck",
    "feasibility: SA-RL reproduction route is mismatched — DrMAS examples/grpo_trainer/run_search.sh is 3-agent vanilla GRPO (orchestra_type=search), and the released trainer asserts agent.multi_agent=True, so no same-stack single-agent baseline exists as specified"
  ],
  "novelty_conclusion": "Using answerer-visible information as a dose variable for when joint MARL beats a same-structure single-agent RL counterfactual is not directly covered (2605.24202 is symmetric math/code; Dr. MAS shares full history; MultiAgent-OPD trains a report-only Searcher-Answerer chain without SA counterfactual). But the novelty boundary against single-agent training under the same bottleneck (MemSearcher/MEM1-style) is unresolved, and Claim 3 partially overlaps s3/MultiAgent-OPD.",
  "closest_neighbors": [
    "When Does Multi-Agent RL Improve LLM Workflows? Workflow, Scale, and Policy-Sharing Tradeoffs (2605.24202)",
    "Dr. MAS: Stable Reinforcement Learning for Multi-Agent LLM Systems (2602.08847)",
    "MultiAgent-OPD: End-to-End Training of Hierarchical Multi-Agent Systems with On-Policy Distillation (2610.23234)",
    "MemSearcher: Training LLMs to Reason, Search and Manage Memory via End-to-End Reinforcement Learning (2511.02805)",
    "s3: You Don't Need That Much Data to Train a Search Agent via RL (2505.14146)"
  ]
}
```
