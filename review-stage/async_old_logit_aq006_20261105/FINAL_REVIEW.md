# 最终审查结论：A-Q006（异步 RL 缺 old logits）

- 结果：**未通过，提前停止**（`rejected_no_viable_candidate`）
- 审查调用：2 / 15（均为常规审查，fresh zero-context，opus；Agent 工具无法设定 effort，按 harness 默认）
- 输入：`path-stage/LLM热门方向_刷新_20261101` 的 A-Q006

## 最好的已审结果

**Call 1，IDEA-002**（推理端在当前权重上重打分，把数值偏差搬回旧版本以恢复 old logits）：总体 6.0，重要性 6 / 新颖度 7 / 有效性 5，可行性 pass，`promising_needs_revision`。

- 重要性：精确 old logits 有价值，但 2605.12070 中 PPO-EWMA 与 Snapshot 只差 1–4 点（30B-A3B VitaBench in-store 33.41 对 34.62），增量主要在大版本差，缺量化依据。
- 新颖度：未检索到同样做法，但机制简单，新意分量取决于逐 token 可平移性。
- 有效性：关键假设是逐 token 数值偏差在版本间相关。2610.40945 只显示平均量级近似常数；BF16 舍入与 MoE 路由翻转下可能去相关，此时误差方差约 2Var(e)，劣于直接用 rollout 概率。

**Call 2，IDEA-005**（把精确 old logits 的收益拆成"生成版本作裁剪参考"与"中心化去漂移"，两者都不需 old logits）：总体 5.0，重要性 6 / 新颖度 5.5 / 有效性 6，可行性 pass（有条件），`needs_rethink`。

- 拆分维度与关键对照已在 2610.40945 Table 2/3 与附录 C（连续异步、版本差 4、Qwen3-8B；不用 old logits 的 IS 1.4×，DLC 1.2×）。
- rollout logprob 作锚点已是 verl bypass 默认；AReaL 消融显示 Decoupled PPO 在陈旧度 ≤8 时接近 oracle。
- 等价性主张种子不足；Search-R1 结果不能检验对 2605.12070 收益的解释。

## 为何没有达到门槛

门槛要求三项 ≥6 且至少两项 ≥8。两次审查的重要性都只有 6，原因不在 brief 写法，而在问题本身已被 2026 年 9–10 月的工作从三方面吸收：

1. **机理**：2610.40945 精确拆分偏差与滞后，说明参考位置决定滞后是否进入裁剪比率，并在连续异步下显示不需 old logits 的修正接近需 old logits 的 DLC。
2. **零历史权重的做法**：Score Centering（2609.20807，0.6B–30B）把偏差危害归因于漂移，加性中心化可与 IS 组合处理陈旧；verl bypass 用 rollout logprob 作锚点。
3. **工程消除**：vLLM 逐比特一致 rollout（2026-10-14）在约 88–91% 吞吐下让同权重偏差为 0，此时 rollout 概率即精确 old logits。

## 最高近邻

- 2610.40945 On the Origin and Evolution of Training-Inference Mismatch in LLM RL
- 2605.12070 Missing Old Logits in Asynchronous Agentic RL
- 2609.20807 Score Centering Stabilizes Off-policy RL
- 2505.24298 AReaL
- 2512.06547 A-3PO；2607.22186 ENTR；2610.21682 RDC
- vLLM 逐比特一致 rollout 博客；verl rollout correction 文档

## 剩余风险与未答部分

- 原问题中"哪些声称无损的系统未保留 old logits"的审计未做；按两次审查与上述近作，其分量有限。
- MoE 不做路由回放且版本差大时，精确分解是否仍有显著收益，没有直接证据；这是本卡唯一可能剩下的细分问题，但实践中 R3/RDC/逐比特一致已是主流处理。
