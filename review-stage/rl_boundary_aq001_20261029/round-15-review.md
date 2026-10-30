## 结论

截至 2026-10-29：**score 8.2，verdict experiment_ready**。主贡献 Claim 2 有新意：它给每个保覆盖训练方法配一个推理期的逐轮接管对应物，再在任务内、跨方法检验“对应物增益能否预测训练增益”。我检索了 arXiv API、arXiv 摘要与 HTML 页面以及网页搜索，没有找到预测训练方法覆盖增益的工作。最接近的几篇各自只覆盖一部分：Sharpening Tax 只用少量 rollout 预测税本身，且路由是按任务整条切换；PBA 用基座样本决定哪些单轮题要锚定；Reach or Solve 每条轨迹只交接一次，比较的是 SFT↔RL 检查点。Claim 1 的逐轮替换协议与 Claim 3 的选轮前向 KL 与已有工作部分重合，但作为 Claim 2 的测量手段和推论成立。

可复现性方面，我用完整 `git clone --depth 1` 核验了五个仓库，HEAD 与文件数和 brief 一致：DPH-RL fea6990/675，TAR 0b7d515/718，AgenticRL_Handoff 64ebd4a/35，sharpening-tax 789ae06/54，verl-agent 20bd331/1334。关键文件都在：`compute_tar_weights`、`compute_tar_loss`、`_backward_tar_loss`、`forward_kl.sh` 的 `data.sft_files`、`PTGSHooks`、`WEBSHOP_ENV_SEED`，以及 handoff 的 `alfworld/{environment,rollout}.py`。PTGS 的 RAGEN 配置里有 Sokoban/FrozenLake 的 GRPO 变体，README 给出了推理期用法，与附录 E.4 的标题对得上。没有致命的新意、可行性或 Claim 阻断。

非致命风险如下：
- 一句话前提要写成条件句。PASS@(k,T)（2604.14877）报告受控工具 RL 在组合任务上扩大了边界，与“RL 会丢覆盖”的说法相反。阶段 0 的门槛已经让结论有条件成立。
- TAR 对应物写的是“与激活条件相同”，但源码的门控是整条轨迹的均值 b(τ)=mean(log π_ref − log π_old)，再加逐 token 权重 φ(δ_t)，并不是逐轮比较。对应物需要和多轮移植后的门控粒度一致。
- ALFWorld 只有 3 个非 GRPO 方法；WebShop 上离线回放的对应物很可能退化为入口对应物。两者都让规律检验的有效变异很薄，种子噪声也会把 b 压向 0。好在已预注册 MDE 和成对差分，阶段 A 约 5 天就能决定是否继续。

值得继续。

## Claim 判断

| Claim | 判断 | 最关键依据 |
|---|---|---|
| 1 按轮定位：真实环境中只换第 t 轮为 B，扣除同模型分叉噪声底，得到 L(t) | 部分重合 | 入口定位：Locked at the Entrance（单轮 Countdown）。检查点交接（单次交接，SFT/RL）：Reach or Solve。分叉加同模型对照（SWE-bench 路由）：Replay Gap。“只换单轮后交回 G”并按轮报告覆盖，在多轮 agent RL 中未见先例，但本身是描述性测量，不设成败条件。 |
| 2 测试时对应物在任务内、跨方法预测训练方法的 pass@16 增益（主贡献） | 新颖 | 未检索到相关工作。Sharpening Tax 只预测税本身（8→32 rollout），D.4 是按任务路由；PBA（2607.20543）是单轮基座锚定的门控，作者自称不是增益预测器。任务固定效应、置换检验、自身对应物优于他人、成对差分都能推翻它。 |
| 3 处方：剖面选轮前向 KL 优于同 token 占比的随机选轮 | 部分重合 | PivotOPD 在选定的恢复轮上用 forward KL，但对象是教师蒸馏，不是锚定基座。Coverage, Not Targeting 给出了“定向≈随机”的反例和随机对照范式。这里有随机选轮对照可推翻，但“应找回最多”并不能由 Claim 2 直接推出。 |

## 最高近邻

1. **Sharpening Tax in Post-Training**：https://arxiv.org/abs/2610.01509 。重叠点：多轮 agent 的覆盖税（BFCL v4 / WebShop / ACEBench），PTGS 在 RAGEN 的 Sokoban、FrozenLake 上训练，D.4 做按任务的基座/后训练路由，E.4 是推理期 PTGS。差别：没有逐轮分析，也不预测训练方法的增益。
2. **Reach or Solve? … Checkpoint Handoffs**：https://arxiv.org/abs/2609.19636 。重叠点：在可回放的 ALFWorld 中交接检查点，分解 Reach 与 Solve。差别：每条轨迹只交接一次，比较 SFT↔RL，不涉及基座逐轮替换或保覆盖方法。
3. **Locked at the Entrance, Open Inside**：https://arxiv.org/abs/2608.29188 。重叠点：RLVR 的覆盖收缩集中在入口，补入口前缀或插值晚层可以恢复。差别：单轮 Countdown/数学，不涉及多轮 agent 或观察后重新锁定。
4. **When RLVR Shrinks the Reasoning Boundary (PBA)**：https://arxiv.org/abs/2607.20543 。重叠点：用冻结基座样本按题判断锐化与锚定，覆盖损失集中在边界题。差别：单轮，没有按轮定位，也不预测各方法的增益。
5. **Does RL Expand the Capability Boundary of LLM Agents? PASS@(k,T)**：https://arxiv.org/abs/2604.14877 。重叠点：多轮工具 RL 的大 k 边界、跨策略交换检索与推理。差别：结论是组合任务上 RL 扩大边界（与本文前提相反），没有基座逐轮接管，也不涉及保覆盖方法。

```json
{
  "score": 8.2,
  "verdict": "experiment_ready",
  "fatal_blockers": [],
  "novelty_conclusion": "Claim 2 (per-method test-time turn-level takeover counterparts predicting within-task training gains of coverage-preserving methods in multi-turn agent RL) is novel; no prior work found predicting training-method coverage gains. Claim 1 (single-turn substitution profile) and Claim 3 (profile-selected forward KL vs random) partially overlap Reach or Solve / Replay Gap / Locked at the Entrance and PivotOPD / Coverage-Not-Targeting but serve as measurement and corollary. Baselines verified via full shallow clones. Non-fatal: qualify RL-loses-coverage premise against PASS@(k,T); align TAR counterpart with TAR's trajectory-level gate b(tau) plus token weights; thin identifying variation on ALFWorld (3 methods) and WebShop replay degeneracy.",
  "closest_neighbors": [
    "Sharpening Tax in Post-Training (arXiv 2610.01509)",
    "Reach or Solve? Deep Diving into Agentic RL Gains with Checkpoint Handoffs (arXiv 2609.19636)",
    "Locked at the Entrance, Open Inside: Where RLVR Narrows the Solution Space (arXiv 2608.29188)",
    "When RLVR Shrinks the Reasoning Boundary: Diagnosing Pass@k Inversion (arXiv 2607.20543)",
    "Does RL Expand the Capability Boundary of LLM Agents? A PASS@(k,T) Analysis (arXiv 2604.14877)"
  ]
}
```
