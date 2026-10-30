## 结论

2026-10-29 评审：**score 7.5 / 10，verdict = promising_needs_revision**。

新颖性：主贡献（Claim 2，“每族保覆盖训练方法都有一个推理期对应物，并在任务内由**自身**对应物预测该方法相对 GRPO 的 pass@16 增益”）在检索范围内未见覆盖。现有工作要么只在单轮上把 RL 效果定位到少数位置（Locked at the Entrance；What RL Brings to Reasoning），要么在多轮上只做 SFT↔RL 或跨模型交接（Reach or Solve；The Replay Gap），要么只在任务级测量或路由（Sharpening Tax）。没有工作把推理期干预当作训练方法增益的可证伪预测器。Claim 1 是把已有交接与分叉协议搬到新问题上的测量，属于部分重合。Claim 3 的处方（只在部分轮上加前向 KL）是 DPH-RL 加轮掩码，本身很薄，价值依赖 Claim 2 是否成立。

基线可行性已核验。TAR、DPH-RL、PTGS / Sharpening Tax、verl-agent、AgenticRL_Handoff 五个仓库都能浅克隆。brief 引用的函数与脚本都存在：`compute_tar_weights` / `compute_tar_loss` / `_backward_tar_loss`、`forward_kl.sh` 与 `data.sft_files`、`PTGSHooks`、`WEBSHOP_ENV_SEED`、`run_webshop.sh` / `run_alfworld.sh`、`handoff/alfworld/{environment,rollout}.py`。PTGS 的配置确实是 Sokoban / FrozenLake，README 里也有推理期用法。没有基线层面的致命问题。

未达到 experiment_ready 的原因是一个**设计层的 claim blocker**，以及两个次要风险。

1. **离线回放对应物与训练库在留出任务上自相矛盾。** DPH-RL / TAR 对应物要求 G 的状态与“**该任务**某条基座成功轨迹”的状态相同，同时又声明所用的轨迹库就是训练时的离线样本。但评测任务是留出的，训练库里没有这些任务。只剩两种读法：
   - 用训练任务的轨迹做跨任务状态匹配：WebShop 的页面与商品几乎不会跨目标重合，P_m(i) 会接近 0；
   - 把评测任务的基座成功轨迹放进训练库：这会污染留出评测。

   两种读法下，主检验 b > 0 的含义都不成立，需要先定义清楚。
2. 入口、剖面、随机三个对应物都是“B 接管某个轮集合”，在任务间高度共线。“自身对应物优于他人对应物”的偏 R² 检验可能分辨不出它们，功效分析应把这一点算进去。
3. 每次 7B 多轮 GRPO 约 8 卡 × 7 小时、每天约 23 万条 rollout 的估计偏乐观（WebShop 环境服务端可能成为吞吐瓶颈）。19 天的预算余量很小。

值得继续：问题定义清楚，推翻条件明确，阶段 0 有停止门槛；修好第 1 点就能进入实验规划。

## Claim 判断

| Claim | 判断 | 关键依据 |
|---|---|---|
| 1. 多轮逐轮替换得到可找回覆盖剖面 L(t) | 部分重合 | 单轮位置定位已有（Locked at the Entrance 的入口定位；2610.24663 的稀疏替换）；多轮交接与分叉协议来自 Reach or Solve 和 The Replay Gap。新的只是把 B→G 的逐轮替换用于覆盖、并扣除同模型噪声底，属于测量组合。 |
| 2. 推理期对应物在任务内预测训练方法增益（主贡献） | 新颖（有设计缺陷） | 未检索到用推理期干预、带任务固定效应与置换检验去预测多种保覆盖训练方法增益的工作。但离线回放对应物在留出任务上的定义与“同一批离线样本”矛盾（见结论第 1 点）。 |
| 3. 剖面选轮前向 KL 优于入口与同 token 占比的随机选轮 | 部分重合 | 方法是 DPH-RL 前向 KL 加轮掩码。Locked at the Entrance 已提出针对入口的修复，PBA（2607.20543）做按题基座锚定。“锚定作用于分布而非奖励、因而与 Coverage, Not Targeting 结论不同”是一个可检验的新假设，由随机选轮对照直接检验，合理。 |
| 背景断言“作用位置与可找回量尚无检验” | 可接受 | Sharpening Tax 只有任务级测量与按任务路由（附录 D.4），TAR 与 DPH-RL 只做单轮数学，DivInit 只修第一轮。检索未找到反例。 |

## 最高近邻

1. **Sharpening Tax in Post-Training**：https://arxiv.org/abs/2610.01509
   - 重叠：在 WebShop / BFCL / ACEBench 上做任务级锐化税测量；PTGS；附录 D.4 的按任务路由；8 次 rollout 的估计可预测 32 次的税。
   - 差别：不做按轮接管，也不用推理期量去预测训练方法的增益。
2. **Reach or Solve? Deep Diving into Agentic RL Gains with Checkpoint Handoffs**：https://arxiv.org/abs/2609.19636
   - 重叠：在 ALFWorld / TravelPlanner 上的检查点交接协议。
   - 差别：只拆分 SFT↔RL 的到达与完成成功率，不涉及覆盖、不涉及基座接管，也不预测训练方法。
3. **Locked at the Entrance, Open Inside**：https://arxiv.org/abs/2608.29188
   - 重叠：单轮 RLVR 的覆盖损失集中在入口，入口修复有效。
   - 差别：单轮 Countdown / 数学；不用推理期诊断预测训练方法的增益。
4. **What RL Brings to Reasoning: A Few Decisions the Base Model Would Not Make**：https://arxiv.org/abs/2610.24663
   - 重叠：在基座与 RL 模型分歧的位置做稀疏替换，以此定位 RL 的作用并测 pass@256。
   - 差别：单轮数学、token 级，方向是 RL→基座，不涉及训练方法预测。
5. **The Replay Gap**：https://arxiv.org/abs/2608.08239
   - 重叠：在真实环境中分叉轨迹并换模型继续，用同模型控制分叉估计噪声底。
   - 差别：SWE-bench 上的跨模型交换，不涉及覆盖与训练方法。

```json
{
  "score": 7.5,
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "claim/design: DPH-RL/TAR test-time counterparts require base success trajectories of the same held-out eval task, yet are declared to use the training offline library; held-out tasks are absent from that library (cross-task state matching gives P≈0 on WebShop) or including them contaminates evaluation, so the Claim 2 test b>0 is ill-defined as written"
  ],
  "novelty_conclusion": "Claim 2 (test-time counterparts predicting per-task training-method coverage gains in multi-turn agent RL) is not covered by found prior work; Claim 1 is a recombination of handoff/fork protocols applied to coverage; Claim 3 prescription is a thin turn-masked DPH-RL variant whose value depends on Claim 2. Baselines and code routes verified.",
  "closest_neighbors": [
    "Sharpening Tax in Post-Training (arXiv 2610.01509)",
    "Reach or Solve? Deep Diving into Agentic RL Gains with Checkpoint Handoffs (arXiv 2609.19636)",
    "Locked at the Entrance, Open Inside: Where RLVR Narrows the Solution Space (arXiv 2608.29188)",
    "What RL Brings to Reasoning: A Few Decisions the Base Model Would Not Make (arXiv 2610.24663)",
    "The Replay Gap (arXiv 2608.08239)"
  ]
}
```
