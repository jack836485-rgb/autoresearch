## 结论

日期 2026-10-29。**score 6.5 / 10，verdict：promising_needs_revision，有 1 个致命可行性 blocker。**

新颖性：主贡献（Claim 2）是"每种保覆盖训练方法都有一个推理期对应物，在任务内、方法之间预测该方法的 pass@16 增益"。我检索到的工作里没有这个说法，在多轮 agent RL 上也没有，所以新颖性基本成立。Claim 1（按轮替换得到覆盖剖面 L(t)）是把 Reach or Solve 的交接、Replay Gap 的分叉与噪声底、Locked at the Entrance 的入口定位搬到多轮覆盖问题上，新意是部分的。它的价值主要在于给 Claim 2 提供测量。故事链有证据支撑：Sharpening Tax 已在 WebShop 上证实覆盖损失，近邻方法都只在任务级、第一轮或单轮上操作（已逐篇核实）。推翻条件写清楚了，任务内固定效应、置换检验和成对差分也处理了共享提升空间与共线问题。

致命 blocker（可行性 / baseline 证据）：**DPH-RL 的公开仓库 `seamoke/DPH-RL` 只有一个文件 `README.md`。** 用 git ls-remote 核对过 HEAD 是 fea6990（2026-02-10），也是最新提交。brief 写的复现入口 `scripts/llama/forward_kl.sh`、离线采样脚本和 `data.sft_files` 实现都不在仓库里，README 引用的脚本同样缺失。按规则，这个 baseline 没有可用的公开实现，因此不能给 experiment_ready。另外有两处复现证据与公开仓库不符，不致命：
- TAR 仓库没有 `recipe/tar/build_memory_bank.py`（README 引用了，但没有提交）。核心的 `compute_tar_weights` / `compute_tar_loss` / `_backward_tar_loss` 确实存在，门控 δ = log π_ref − log π_old > 0 也与 brief 写的激活条件一致。
- `Xuanxuana1/AgenticRL_Handoff` 也只有 `README.md`，`src/handoff/alfworld/{environment,rollout}.py` 没有公开。逐轮替换与分叉要全部自写。它基于 SkillRL 的 ALFWorld，不是 verl-agent。

已核实为真：PTGS 代码（`ptgs/integration.py` 的 `PTGSHooks`）、Sokoban / FrozenLake 配置、`WEBSHOP_ENV_SEED`、附录 E.4 的推理期 PTGS 条目、附录 D.4 的按任务路由，以及 verl-agent 的 `run_webshop.sh` / `run_alfworld.sh`。

值得继续。idea 本身成立，主要问题出在 baseline 证据上。另有一个实质风险：WebShop 上"G 的状态等于某条基座成功轨迹的状态"在第 1 轮之后可能很稀疏，这会让 DPH-RL / TAR 的对应物退化成接近入口对应物，使"自身对应物优于他人对应物"难以区分。

## Claim 判断

| Claim | 判断 | 最关键依据 |
|---|---|---|
| 1. 多轮真实环境中按轮替换 B，减去同模型分叉噪声底，得到剖面 L(t) | 部分重合 | Reach or Solve 只做单个交接点、只交叉 SFT↔RL；Replay Gap 在 SWE-bench 上分叉并测噪声底，但做的是路由评测；Locked at the Entrance 与 Sparse but Critical 只在单轮或 token 级。四者都没有在多轮 agent 上按轮测"可找回的覆盖"。 |
| 2. 推理期对应物增益 P_m(i) 在任务内预测训练增益 Δ_m(i)（主贡献） | 新颖 | 没有检索到"用测试时干预预测保覆盖训练方法按任务增益"的工作。Sharpening Tax 只用少量 rollout 的税预测大预算的税（ρ=0.85），预测的不是方法增益；Critical-State RL 选可训练状态，但不预测各方法的增益。不过 DPH-RL→"状态匹配接管"这条映射的合理性只是断言，需靠实验检验。 |
| 3. 按剖面选轮的前向 KL 优于同 token 占比的随机选轮 | 部分新颖 | 选轮锚定本身近似"按轮掩码的 DPH-RL / TAR"。随机选轮对照借自 Coverage, Not Targeting（那篇针对的是信用分配）。新意依赖 Claim 2 成立。 |

## 最高近邻

1. **Sharpening Tax in Post-Training**（https://arxiv.org/abs/2610.01509）：重叠在 WebShop / BFCL / ACEBench 的任务级锐化税、PTGS（Sokoban / FrozenLake）、基座与后训练模型的按任务路由（附录 D.4）、推理期 PTGS（附录 E.4）。差别：没有按轮分析，也不预测其他训练方法的增益。
2. **Reach or Solve?**（https://arxiv.org/abs/2609.19636）：重叠在 ALFWorld 上的检查点交接。差别：单个交接点、只交叉 SFT↔RL、不涉及基座与覆盖；公开代码目前只有 README。
3. **The Replay Gap**（https://arxiv.org/abs/2608.08239）：重叠在真实环境分叉和同模型对照噪声底。差别：场景是 SWE-bench 路由评测，与 RL 覆盖无关。
4. **Locked at the Entrance, Open Inside**（https://arxiv.org/abs/2608.29188）：重叠在把覆盖收缩定位到入口、用晚层插值修复。差别：只做单轮 Countdown / 数学，没有多轮观察后的重新锁定，也没有对方法增益的预测。
5. **When RLVR Shrinks the Reasoning Boundary**（PBA，https://arxiv.org/abs/2607.20543）：重叠在按题做基座锚定，处理基座只有稀有正确解的边界题。差别：只做单轮数学、只到按题粒度，不做按轮定位或跨方法预测。

```json
{
  "score": 6.5,
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "DPH-RL baseline: public repo seamoke/DPH-RL (HEAD fea6990, 2026-02-10) contains only README.md; cited scripts/llama/forward_kl.sh, offline sampling scripts and data.sft_files implementation do not exist, so the stated reproduction route is not working public code"
  ],
  "novelty_conclusion": "Claim 2 (inference-time counterparts that predict per-task, within-task gains of coverage-preserving training methods in multi-turn agent RL) appears novel; Claim 1 is a partial-overlap transfer of checkpoint handoff + fork noise floor + entrance localization to multi-turn coverage; Claim 3 depends on Claim 2. Non-fatal evidence errors: TAR build_memory_bank.py and AgenticRL_Handoff src/handoff are absent from public repos.",
  "closest_neighbors": [
    "Sharpening Tax in Post-Training (arXiv 2610.01509)",
    "Reach or Solve? Deep Diving into Agentic RL Gains with Checkpoint Handoffs (arXiv 2609.19636)",
    "The Replay Gap: Static Evaluation of Model Switching in LLM Agents Scores the Wrong World (arXiv 2608.08239)",
    "Locked at the Entrance, Open Inside: Where RLVR Narrows the Solution Space (arXiv 2608.29188)",
    "When RLVR Shrinks the Reasoning Boundary: Diagnosing Pass@k Inversion (arXiv 2607.20543)"
  ]
}
```
