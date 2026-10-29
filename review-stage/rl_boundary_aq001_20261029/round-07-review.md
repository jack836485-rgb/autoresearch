## 结论

评审日期 2026-10-29。**score 6.0 / 10，verdict：promising_needs_revision**。

新颖性判断：诊断部分（多轮 agent 中真实环境逐轮替换得到 L(t)，并检验剖面是否因环境而异）在已检索文献中没有被直接做过，有一定新意。方法部分的核心机制被 TAR（arXiv 2610.24236，2026-10-16）大幅覆盖，brief 未提到这篇。TAR 用基座多样成功解建库，只在当前策略对其似然低于基座时激活回放，并按逐 token 的单侧对数似然差 δ_t = log π_B − log π_θ 加权 NLL。本方法的 d_t = 平均[log π_B − log π_θ]、w_t = max(d_t,0)/mean、加权 NLL，是同一机制按轮位置聚合，再叠加 PBA 式按任务风险门控。去掉 TAR 之后，"自适应、不需诊断、按被抑制程度决定锚定位置"这一卖点不再属于本方法。剩下的差别只有三点：多轮场景、按轮而非按 token 聚合、按任务门控。这三点组合离平凡组合不远。

此外，ATOD（arXiv 2606.27814）已在 ALFWorld/WebShop 上按轮自适应地对散度项加权（T-DUR），只是目标是向教师蒸馏，并非保 pass@k。"多轮 agent 中按轮自适应加权散度"本身不是空白。

实验缺少 TAR 式逐 token 抑制加权回放（多轮移植）这一直接对照，代码 https://github.com/wenzhilics/tar 可访问。缺少它，就无法区分"按轮聚合 + 风险门控"与"逐 token 抑制加权"，Claim 3 的新增贡献不可检验，这属于新颖性边界未解决。其余 baseline 均已核实：sharpening-tax 仓库含 `benchmarks/webshop.py`（`WEBSHOP_ENV_SEED`）与 `ptgs/integration.py` 的 `PTGSHooks`；verl-agent 含 `run_webshop.sh`、`run_alfworld.sh`；DPH-RL README 列有 forward 散度；AgenticRL_Handoff 含 `src/handoff/alfworld/{environment,rollout}.py`；early-branch-locking 与 diverse-query-initialization 可访问。复现路线具体，算力（约 18 天，8×A100）在约束内，没有 feasibility 致命项。

Claim 2 与 2609.02417 的对立成立：后者研究信用分配，不是分布锚定，因而是合理的可证伪命题，而不是空泛的"大家都忽视"。L(t) 形状的环境差异目前只是假设，有推翻条件。

值得继续，前提是把方法新意重新划清到 TAR 之外，并把 TAR 式对照纳入同预算比较。

## Claim 判断

| Claim | 判断 | 最关键依据 |
|---|---|---|
| 1. 多轮 agent 中可找回覆盖的剖面 L(t) 因环境而异（WebShop 入口/选择轮，ALFWorld 中段） | 部分新颖 | Reach or Solve 只做单一交接点、看成功率不看 pass@k；Locked at the Entrance 只在单轮 Countdown/数学上定位入口；未检索到多轮逐轮替换的 pass@k 剖面。但这属于诊断扩展，形状预测缺乏先验证据 |
| 2. 锚定的"施加在哪些轮"是一阶的（同 token 占比下按 L(t) 选轮 > 随机选轮） | 新颖（作为经验命题） | 2609.02417 的结论只针对信用分配；Critical-State RL 只针对 BFCL 上的训练状态选择，不是保覆盖锚定。区分"作用于分布 vs 奖励"有道理，但尚无证据 |
| 3. 按轮自适应的风险任务前向 KL 不需诊断即可追平各环境的剖面最优掩码 | 部分重合，接近被覆盖 | TAR 已有"相对基座被抑制才激活 + 按单侧 log-ratio 局部加权 NLL"；PBA 已有按任务风险门控；ATOD 已在 ALFWorld/WebShop 按轮自适应加权散度。新增只剩按轮聚合 + 多轮移植，且实验缺 TAR 对照 |

## 最高近邻

1. **TAR: Preserving Reasoning Diversity in RLVR via Adaptive Replay**（arXiv 2610.24236，https://arxiv.org/abs/2610.24236，代码 https://github.com/wenzhilics/tar）。重叠：基座成功解库、单侧似然差门控、逐 token 抑制加权 NLL，与本方法的 d_t/w_t 机制几乎同构。差别：单轮数学；按 token 而非按轮聚合；没有按任务风险门控，也没有多环境剖面检验。
2. **When RLVR Shrinks the Reasoning Boundary (PBA)**（arXiv 2607.20543，https://arxiv.org/abs/2607.20543）。重叠：按题判定风险、对风险题向冻结基座锚定，以保 pass@k。差别：单轮数学；锚定全序列，不分位置。
3. **ATOD: Annealed Turn-Aware On-Policy Distillation**（arXiv 2606.27814，https://arxiv.org/abs/2606.27814，代码 https://github.com/TanQitai/ATOD）。重叠：在 ALFWorld/WebShop 上按轮的分歧/不确定性自适应加权散度项。差别：反向 KL，向更强教师蒸馏，目标是成功率，不涉及 pass@k 覆盖与基座锚定。
4. **DPH-RL: The Choice of Divergence**（arXiv 2509.07430，https://arxiv.org/abs/2509.07430）。重叠：前向 KL 离线基座样本，保 pass@k。差别：整序列、单轮数学/SQL，无位置选择。
5. **Locked at the Entrance, Open Inside**（arXiv 2608.29188，https://arxiv.org/abs/2608.29188）。重叠：定位覆盖丢失发生的位置，并做入口定向修复。差别：单轮 Countdown/数学，修法为晚层插值，不是训练期按位置锚定。

```json
{
  "score": 6.0,
  "verdict": "promising_needs_revision",
  "fatal_blockers": [],
  "novelty_conclusion": "多轮逐轮替换诊断 L(t) 及其跨环境差异有一定新意；但方法核心（相对基座单侧 log-ratio 判定被抑制、按抑制程度加权 NLL/前向 KL 回放基座成功解）已由 TAR (2610.24236) 给出，按任务风险门控来自 PBA，按轮自适应散度加权在 ALFWorld/WebShop 上已有 ATOD；剩余差别为多轮移植与按轮聚合，且实验缺 TAR 式逐 token 抑制加权对照，Claim 3 的增量不可检验，新颖性边界未解决。",
  "closest_neighbors": [
    "Preserving Reasoning Diversity in Reinforcement Learning with Verifiable Rewards via Adaptive Replay (TAR, arXiv 2610.24236)",
    "When RLVR Shrinks the Reasoning Boundary: Diagnosing Pass@k Inversion (PBA, arXiv 2607.20543)",
    "ATOD: Annealed Turn-Aware On-Policy Distillation for Multi-Turn Agentic Tasks (arXiv 2606.27814)",
    "The Choice of Divergence: A Neglected Key to Mitigating Diversity Collapse in RLVR (DPH-RL, arXiv 2509.07430)",
    "Locked at the Entrance, Open Inside: Where RLVR Narrows the Solution Space (arXiv 2608.29188)"
  ]
}
```
