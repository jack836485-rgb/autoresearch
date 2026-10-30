## 结论

截至 2026-10-29：**score 8.4，verdict = experiment_ready**。我没有找到"给每类保覆盖训练方法配一个推理期可测的对应物，用它按任务预测该方法相对 GRPO 的 pass@k 增益"的先行工作。Claim 2（主贡献）在任务内回归、置换检验和成对差分下可以被推翻，因此是新的。逐轮替换剖面 L(t) 是把 Reach or Solve 的交接协议和 Replay Gap 的同模型分叉噪声底，搬到 B↔GRPO 的覆盖问题上。它属于已有协议的新用法，但为 Claim 2 提供了必要的测量。处方（剖面选轮前向 KL）本身只是 DPH-RL 加一个轮掩码，价值完全取决于 Claim 2。

故事链有证据支撑：Sharpening Tax 已在 WebShop 上测到锐化税，Locked at the Entrance 在单轮上把覆盖损失定位到入口，然后由本方案检验这些方法在多轮中作用于哪一轮、能找回多少。"尚无检验"这一说法范围很窄，与我的检索一致，不构成 claim blocker。

Baseline 核验情况：
- 4 个仓库我用完整 `git clone --depth 1` 复核，HEAD 与文件数与 brief 一致。
- TAR 的 `compute_tar_weights`、`compute_tar_loss`、`_backward_tar_loss` 存在。
- DPH-RL 的 `scripts/llama/forward_kl.sh` 存在。
- sharpening-tax 有 `PTGSHooks` 和 `WEBSHOP_ENV_SEED`，配置文件里的 PTGS 环境确为 Sokoban / FrozenLake。
- Sharpening Tax 目录里确有附录 D.4（按任务路由）和 E.4（推理期 PTGS）。

TAR 与 DPH-RL 原本提出于单轮 RLVR，但它们是本研究要检验的对象，不是要超过的 SOTA。它们同属 LLM RLVR 保覆盖领域，移植路线具体，所以不算跨域借鉴型 baseline，不构成致命问题。

剩下的是非致命风险：
1. WebShop 退化情形下的预测（"DPH-RL / TAR 与入口前向 KL 无显著差别"）是零假设型预测。"不显著"不能当作支持，需要等价检验，或者给出预注册的等价界。
2. TAR 实际的门控是轨迹（或片段）平均的 b(τ) = mean(log π_ref − log π_old) > 0，再乘逐 token 软权重。对应物用的是逐动作的似然比较。说"与 TAR 激活条件相同"不够精确，粒度需要对齐。
3. ALFWorld 只有 3 个非 GRPO 方法，且没有随机选轮对照：任务内的"自身对应物优于他人"检验较弱，Claim 3 实际上只能在 WebShop 上检验。
4. 对 3 种子均值的任务级 Δ_m(i)，种子噪声可能很大。功效分析和扩到 1500 题的预案已经覆盖这一点。7B 多轮 GRPO 每次约 7 小时的估计偏乐观，但有阶段 0 门槛和 30% 冗余。

值得继续，可以进入实验规划。

## Claim 判断

| Claim | 判断 | 关键依据 |
|---|---|---|
| 1. 按轮定位可找回覆盖 L(t)（真实环境逐轮替换减同模型分叉底） | 部分重合 | 交接协议来自 Reach or Solve（SFT↔RL，单一交接点，看 Reach/Solve，不做 B↔RL 的逐轮覆盖），分叉与噪声底来自 Replay Gap（SWE-bench 路由），入口定位来自 Locked at the Entrance（单轮）。三者组合到多轮 B↔GRPO 的 pass@k 剖面上，未检索到先例。它是描述性测量，不设成败条件。 |
| 2. 测试时对应物 P_m(i) 预测训练增益 Δ_m(i)（任务内回归 + 置换 + 自身优于他人 + 成对差分） | 新颖 | 检索到的近邻都只提出单个方法（DPH-RL / TAR / PTGS / DivInit），或只做任务级的税测量与路由（Sharpening Tax）。没有工作用推理期的接管对应物，对多个训练方法做按任务、可推翻的增益预测。用任务固定效应排除共享提升空间，设计到位。 |
| 2'. WebShop 退化推论（回放 ≈ 入口） | 新颖但检验偏弱 | 推论可检验，但它是零差异预测，需要等价检验，否则不能算支持。 |
| 3. 剖面选轮前向 KL 优于同 token 占比的随机选轮 | 部分重合 | 方法本身就是 DPH-RL 的前向 KL 加轮掩码。Coverage, Not Targeting 发现信用分配上定向与随机同样有害，本 Claim 用随机对照直接检验锚定是否不同，可以被推翻。只有 WebShop 有随机组。 |

## 最高近邻

1. **Sharpening Tax in Post-Training**（https://arxiv.org/abs/2610.01509）
   - 重叠：在 WebShop / BFCL / ACEBench 上做任务级锐化税测量；按任务在基座与后训练模型间路由（附录 D.4）；PTGS 和推理期 PTGS（附录 E.4）。
   - 差别：不做按轮接管，也不预测其他训练方法的增益。
2. **Reach or Solve? Checkpoint Handoffs**（https://arxiv.org/abs/2609.19636）
   - 重叠：轨迹中段的检查点交接协议，含 ALFWorld。
   - 差别：只做 SFT↔RL、单一交接点、Reach/Solve 成功率，没有基座、pass@k 覆盖或训练方法预测。
3. **Locked at the Entrance, Open Inside**（https://arxiv.org/abs/2608.29188）
   - 重叠：把 RLVR 的覆盖收缩定位到入口，并用入口相关干预找回覆盖。
   - 差别：单轮 Countdown / 数学，没有多轮，也没有对多个训练方法的定量预测。
4. **TAR: Targeted Adaptive Replay**（https://arxiv.org/abs/2610.24236）
   - 重叠：回放被抑制的基座成功解（门控为 log π_ref > log π_old 的平均）。
   - 差别：单轮数学，不分析多轮中的作用位置。
5. **The Replay Gap**（https://arxiv.org/abs/2608.08239）
   - 重叠：真实环境中分叉换模型，用同模型分叉做噪声底。
   - 差别：研究的是路由评测是否有效（SWE-bench），与覆盖和训练方法无关。

```json
{
  "score": 8.4,
  "verdict": "experiment_ready",
  "fatal_blockers": [],
  "novelty_conclusion": "Claim 2（推理期对应物按任务预测多种保覆盖训练方法相对 GRPO 的 pass@k 增益）未见先例且可推翻；Claim 1 是 Reach or Solve 与 Replay Gap 协议在 B↔GRPO 覆盖问题上的新用法；Claim 3 方法本身是 DPH-RL 加轮掩码，价值依赖 Claim 2。非致命风险：退化推论需等价检验；TAR 门控粒度与对应物不完全一致；ALFWorld 方法组少且无随机对照；任务级种子噪声。",
  "closest_neighbors": [
    "Sharpening Tax in Post-Training (arXiv 2610.01509)",
    "Reach or Solve? Deep Diving into Agentic RL Gains with Checkpoint Handoffs (arXiv 2609.19636)",
    "Locked at the Entrance, Open Inside: Where RLVR Narrows the Solution Space (arXiv 2608.29188)",
    "Preserving Reasoning Diversity in RLVR via Adaptive Replay / TAR (arXiv 2610.24236)",
    "The Replay Gap: Static Evaluation of Model Switching in LLM Agents Scores the Wrong World (arXiv 2608.08239)"
  ]
}
```
