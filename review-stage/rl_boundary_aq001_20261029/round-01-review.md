## 结论

日期 2026-10-29。**score 5.5 / 10，verdict：promising_needs_revision。**

整体有一部分是新的。"在 pass@k 上按轮做 B/R 交接，看锐化税付在到达段还是完成段"这个诊断问题，我没查到有人做过。Sharpening Tax 只在任务级分析。Reach or Solve 只看单次成功率，不看 pass@k，也没有提出训练或解码上的修法。

但另外三部分新意弱：
- **Claim 1** 其实是用 Sharpening Tax 公开数据重新算一遍。原文的 42 个 cell 里本来就有负税，例如 Qwen2.5-7B / BFCL 的 Tax_S(128) = −0.044。
- **修法 1** 和已有工作很接近：BACo 做 token 级的基座 / 对齐模型协作，EAD 和 REFT 做"先探索后利用"、首 token 多样化。修法 1 是这些做法在轮级上的版本。
- **修法 2** 是 PBA 式基座锚定与 EAD 式只管早期这两个思路按轮组合。

除此之外有三个必须先解决的问题：

1. **阶段 A 的检查点选错了。** 我用公开的 `outcomes_42cells.csv.gz` 复算，在 WebShop 上后训练版比基座的 pass@128 只低一点：Qwen3.5-4B 低 1.0，Qwen3.5-9B 低 1.8。Qwen3.5-9B 在 BFCL 上只高 0.5。所以 brief 说"已确认在这些检查点上方向相反"并不成立，三对里有两对 WebShop 上几乎没有可以定位的覆盖损失。WebShop 损失明显的是 Qwen2.5-7B（低 14.4，107 个任务从可解变成 0 次成功）和 Ministral-3-8B（低 24.2，144 个任务），而 Ministral-3-8B 没被选入。
2. **阶段 B 没有证据表明 RL 会产生锐化税。** 起点是 Qwen2.5-7B-Instruct，在 verl-agent 的 prompt 格式下做 GRPO，却用 Sharpening Tax 的 chat harness 评测。训练和评测格式不一致，会直接拉低 pass@1。另外"GRPO 相对起点在 WebShop 上缩小 pass@128"这个前提目前没有任何数据支持；如果这个税不存在，早期轮锚定就没有对象可比。
3. **缺少最关键的对照**：只在 R 的前 m 轮提温、或只在前 m 轮做首动作多样化（REFT / EAD 的轮级版）。没有这个对照，就分不清 B→R 恢复覆盖是因为"基座的分支分布"，还是因为"早期轮多样性本身"。另外，"B→R ≥ B→B"只靠 R 是更强的完成者也能成立，不能单独支持"锐化税付在到达段"。真正有区分力的比较是 B→R 和 R→R 在大 k 下的差，以及 R→B 和 B→B 的差。

**值得继续**，但要先把这三点修好，再判断新意边界是否成立。

## Claim 判断

| Claim | 判断 | 关键依据 |
|---|---|---|
| 1. 同一对检查点在不同基准上覆盖方向相反 | 部分重合（偏已覆盖） | 数字我按公开数据复算无误。但这是 Sharpening Tax 自己 42 个 cell 里已有的正负税，属于重新分析。另外 brief 把这个结论推到了 Qwen3.5-4B/9B 上，复算数据不支持。 |
| 2. 覆盖变化可拆成到达 / 完成两段，锐化税付在到达段 | 新颖（作为假设） | Reach or Solve 用检查点交接拆分，但只看 pass@1，用的是 TravelPlanner / ALFWorld，不涉及 pass@k。"Why Do Reasoning Models Lose Coverage"（forks in the road）在 SFT 推理任务上把覆盖收缩归因到决策分叉点，机理相近但不是多轮 agent。可证伪性成立，但前提是补上 R 早期提温这个对照，并在 WebShop 有真实损失的检查点对上做。 |
| 3a. 按轮交接解码同时拿到 R 的 pass@1 和 B 的 pass@128 | 部分重合 | 和 BACo（token 级基座 / 对齐协作）、EAD（先高温后低温）思路相同，只是粒度换成轮级。新意取决于能不能赢过"R 只在早期轮提温"。 |
| 3b. 早期轮锚定 GRPO 比 PTGS / 全局提温付更少的税 | 部分重合 | PBA 已在数学 RLVR 上做按题基座锚定，同时提升 pass@1 和高预算覆盖。本方案按轮锚定，是 PBA 与 EAD 的组合。缺 WebShop 上"GRPO 确实产生税"的前提证据，也缺 REFT / EAD 式的轮级对照。 |

## 最高近邻

1. **Sharpening Tax in Post-Training**（https://arxiv.org/abs/2610.01509；代码 https://github.com/changdaeoh/sharpening-tax，已克隆核验 `outcomes_42cells.csv.gz`、`ptgs/integration.py`、`benchmarks/webshop.py`）
   - 重叠：检查点、基准、harness、pass@k 和税的定义都相同；按任务路由；PTGS；附录 C.4 已说明全局调温不能化解矛盾。
   - 差别：只做任务级分析，不分析轨迹内哪一轮丢失覆盖。仓库里没有路由代码。PTGS 的示例配置是 Sokoban / FrozenLake + RAGEN，要用在 WebShop 上需要移植到 verl-agent。
2. **Reach or Solve? … Checkpoint Handoffs**（https://arxiv.org/abs/2609.19636）
   - 重叠：同样是回放前一个策略的历史、交给另一个检查点继续，用来拆分到达与完成。
   - 差别：只看 pass@1，没有大 k 覆盖；用的是 SFT / RL 检查点，环境是 TravelPlanner / ALFWorld；不提出修法。
3. **When RLVR Shrinks the Reasoning Boundary: Diagnosing Pass@k Inversion**（https://arxiv.org/abs/2607.20543）
   - 重叠：同样针对 pass@k 倒挂；把税归因到基座里罕见但正确的轨迹没能被采到；PBA 用基座锚定的方式同时提升 pass@1 和覆盖。
   - 差别：单轮数学任务，锚定粒度是按题，不是按轮。
4. **Optimizing Diversity and Quality through Base-Aligned Model Collaboration (BACo)**（https://arxiv.org/abs/2511.05650）
   - 重叠：解码时混用基座和对齐模型，同时追求多样性和质量。
   - 差别：token 级路由，开放式生成任务，不是多轮 agent，也不看 pass@k。
5. **Let it Calm: Exploratory Annealed Decoding (EAD)**（https://arxiv.org/abs/2510.05251）与 **REFT 首 token 多样化**（https://arxiv.org/abs/2605.28295）
   - 重叠：都基于"早期决策决定探索方向"，只在序列开头增加多样性，并用于 RL rollout。
   - 差别：单轮推理任务，按 token 操作，不涉及多轮环境，也不用基座分布。

```json
{
  "score": 5.5,
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "阶段A所选 Qwen3.5-4B/9B 在 WebShop 上 pass@128 仅降 1.0/1.8（Qwen3.5-9B BFCL +0.5），与'已确认方向相反'的陈述矛盾；损失显著的 Ministral-3-8B 未入选",
    "阶段B缺少 GRPO（自 Qwen2.5-7B-Instruct，verl-agent 格式）在 WebShop 上产生大k覆盖损失的前提证据，且训练与评测 harness 格式不一致",
    "缺少'R 仅前m轮提温/首动作多样化'这一对照，无法把 B→R 的覆盖恢复归因于基座分支分布而非早期多样性本身；B→R≥B→B 也可单由 R 更强的完成能力解释"
  ],
  "novelty_conclusion": "轮级 pass@k 交接诊断（锐化税付在到达段）是可证伪的新问题；Claim 1 是 Sharpening Tax 公开数据的再分析；两个修法分别是 BACo/EAD/REFT 与 PBA 的轮级组合，新意取决于能否胜过 R 早期轮提温的对照",
  "closest_neighbors": [
    "Sharpening Tax in Post-Training (arXiv 2610.01509)",
    "Reach or Solve? Deep Diving into Agentic RL Gains with Checkpoint Handoffs (arXiv 2609.19636)",
    "When RLVR Shrinks the Reasoning Boundary: Diagnosing Pass@k Inversion (arXiv 2607.20543)",
    "Optimizing Diversity and Quality through Base-Aligned Model Collaboration (arXiv 2511.05650)",
    "Let it Calm: Exploratory Annealed Decoding (arXiv 2510.05251) / Diversifying RLVR Rollouts via First-Token Exploration (arXiv 2605.28295)"
  ]
}
```
