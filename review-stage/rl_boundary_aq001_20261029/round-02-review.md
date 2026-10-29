## 结论

日期 2026-10-29。**score 6.8 / 10，verdict：promising_needs_revision。**

在多轮 agent 上，用 pass@k 做按轮的基座/后训练交接，并区分"丢分布还是丢多样性"，这个诊断问题目前没检到有人做过，有新意，值得继续。Claim 1 的数字我用公开的 `data/outcomes_42cells.csv.gz` 逐项复算过：Qwen2.5-7B WebShop 丢 107、新解 35，BFCL 丢 6、新解 82；Ministral-3-8B WebShop 丢 144、新解 23，BFCL 丢 25、新解 46。全部一致。Baseline 可复现：sharpening-tax 仓库、`ptgs/integration.py`、verl-agent 的 `run_webshop.sh`（自带 `use_kl_loss`）都在。另外，Reach or Solve 的交接代码其实已公开（github.com/Xuanxuana1/AgenticRL_Handoff，git ls-remote 可达），brief 写的"未见代码"有误。

没到 experiment_ready 的门槛，原因有三：

1. **修法与机制不对齐。** Claim 2 认为税来自基座早期轮的稀有分支丢失。但 verl 的 KL 损失是在策略自身样本上估计的 KL(π‖π_B)，这类约束本身就不惩罚丢掉基座的稀有模式。PBA 原文也承认这种估计"无法恢复已近消失的分支"。DPH-RL 则专门表明，保 pass@k 需要质量覆盖型散度（前向 KL / JS）。所以 Claim 3 的动作和 Claim 2 的机制之间缺一环，而 Claim 3 相对 PBA + DPH-RL 换成按位置选择之后的新意边界也没厘清。
2. **因果链跨了两种检查点。** m 和"税在早期轮"的诊断来自发布的 Instruct 对，这些对混合了 SFT、偏好优化和 RL。修法却作用在"基座出发只做 GRPO"的设置上。Problem Anchor 明确要求把 RL 单独隔离出来，但阶段 B 没有在 GRPO 检查点上重做交接诊断，没法证明它的税也落在同样的早期轮。
3. **Claim 1 不是贡献。** 它只是对已发表 cell 的再统计。而且两个 arm 的提示路径不同：基座走文本 harness，后训练模型走原生 chat 加 tool parser；Qwen2.5-7B 基座在 BFCL 上只有 44/200 可解。"任务结构"和"harness 适配度"因此没有分开，只能作定位动机，不能作结论。

阶段 B 只有 2 个种子，5 组在 pass@128 上的差异恐怕难以分辨。

## Claim 判断

| Claim | 判断 | 最关键依据 |
|---|---|---|
| 1. 同一对检查点在 WebShop / BFCL 上覆盖方向相反，原因在任务结构 | 已被覆盖（数据），归因部分不成立 | 数字是 Sharpening Tax 已发布的 cell（已复算一致），论文本身也报告了税随基准与规模变号。基座 harness 与后训练 chat 路径不同，"任务结构"无法与格式适配分开 |
| 2. 多轮 agent 的税付在早期轮，丢的是基座的分支分布而非多样性 | 新颖（部分重合） | Reach or Solve 有交接协议，但只做 SFT↔RL、pass@1、交接点在近终点。Sparse but Critical 发现基座/RL 分歧集中在序列开头，交换早期分歧 token 影响很大，但只在单轮数学、不看 pass@k。多轮、pass@k、基座分支与"等熵提温/REFT"对照的组合未见先例，可被推翻 |
| 3. 只在前 m 轮向基座加 KL，比全局 KL、PTGS 与早期提温付更少的税 | 部分重合 | 本质是 PBA（按题向基座加 KL）或 DPH-RL（选择性散度保 pass@k）的选择轴从"题"换成"轮位置"，再加上 EAD/REFT 的"开头最重要"。选用的 KL 方向在策略样本上估计，与"丢稀有分布"的机制相悖。诊断也没在纯 RL 检查点上重做，新意依赖未验证的前提 |

## 最高近邻

1. **Sharpening Tax in Post-Training**（arXiv 2610.01509，https://arxiv.org/abs/2610.01509；代码 https://github.com/changdaeoh/sharpening-tax）：同基准、同检查点、同 128 rollout，有 PTGS 与按任务路由。差别：只到任务级，没有轮级定位、交接或分布/多样性区分。
2. **Reach or Solve? … Checkpoint Handoffs**（arXiv 2609.19636，https://arxiv.org/abs/2609.19636；代码 https://github.com/Xuanxuana1/AgenticRL_Handoff）：交接协议与到达/完成拆分。差别：只有 SFT↔RL、pass@1、TravelPlanner/ALFWorld，交接点在近终点，不用基座，不提修法。
3. **When RLVR Shrinks the Reasoning Boundary（PBA）**（arXiv 2607.20543，https://arxiv.org/abs/2607.20543）：稀有正确轨迹在有限组里消失，按题向冻结基座加 KL。差别：单轮数学、按题选择，本方案按轮位置选择、用于多轮 agent。
4. **Sparse but Critical: Token-Level Distributional Shifts in RLVR**（arXiv 2603.22446，https://arxiv.org/abs/2603.22446）：基座↔RL 交叉采样，分歧在开头最高，交换早期分歧 token 显著改变性能。差别：单轮数学、无 pass@k、无多轮，也没有修法。
5. **The Choice of Divergence（DPH-RL）**（arXiv 2509.07430，https://arxiv.org/abs/2509.07430；代码 https://github.com/seamoke/DPH-RL）：选择性地对初始策略加前向 KL / JS 以保 pass@k，并指出反向 KL 保不住覆盖。差别：数学/SQL 单轮，按题选择不按轮。它直接挑战本方案所选的 KL 方向。

```json
{
  "score": 6.8,
  "verdict": "promising_needs_revision",
  "fatal_blockers": [],
  "novelty_conclusion": "多轮agent中基于pass@k的按轮基座/后训练交接诊断及分布-vs-多样性检验未见先例，具备新意；Claim 1为已发表数据再分析且受harness差异混淆；Claim 3相当于PBA/DPH-RL式基座锚定按轮位置选择，且所用策略样本KL(π‖π_B)与'丢失基座稀有分支'机制不对齐、诊断未在纯RL检查点上复现，新意边界未定。",
  "closest_neighbors": [
    "Sharpening Tax in Post-Training (arXiv 2610.01509)",
    "Reach or Solve? Deep Diving into Agentic RL Gains with Checkpoint Handoffs (arXiv 2609.19636)",
    "When RLVR Shrinks the Reasoning Boundary: Diagnosing Pass@k Inversion (arXiv 2607.20543)",
    "Sparse but Critical: A Token-Level Analysis of Distributional Shifts in RLVR Fine-Tuning of LLMs (arXiv 2603.22446)",
    "The Choice of Divergence: A Neglected Key to Mitigating Diversity Collapse in RLVR (arXiv 2509.07430)"
  ]
}
```
