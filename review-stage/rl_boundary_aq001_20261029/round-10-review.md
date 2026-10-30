## 结论

日期 2026-10-29。**score 7.0，verdict：promising_needs_revision。**

**问题与已有工作的对应关系核实无误。**
- 引用的论文都能核验，归属写得对：Sharpening Tax 的任务级测量在 WebShop / BFCL / ACEBench 上，PTGS 在 Sokoban / FrozenLake 上；Reach or Solve 做的是 SFT↔RL 交接；Replay Gap 提供同模型分叉噪声底。
- 我没检索到"按轮定位 B→G 的可找回覆盖"或"用测试时对应物预测训练方法覆盖增益"的已有工作。Claim 2 的方向有新意，值得继续。

**新意边界还没守住，Claim 2 有一个阻断问题。**
- 剔除方法固定效应后，斜率 b 只能靠任务间差异来识别。
- "B 有成功、G 全失败"的任务，对所有对应物和所有训练方法都同时有提升空间；B、G 都稳解或都不解的任务，两边都是 0。
- 因此即使对应物没有任何方法特异的预测力，b > 0 也几乎必然成立，推翻条件实际上推不翻。
- 排序检验只有 7 个方法（WebShop）和 4 个方法（ALFWorld）。零假设下 τ > 0 的概率接近一半，作为推翻条件太弱。
- 结果是"对应物按方法预测增益"和"共享的提升空间"区分不开。这是 claim blocker。

**次要问题。**
- PTGS 的对应物（G 全轮调到与 B 首动作等熵的温度）和 PTGS 的机制不对应。PTGS 是训练期按题难度后验调采样温度，这个对应物测的是 G 自身的潜在覆盖。
- 剖面集合 S 在留出评测任务上选出，又在同一批任务上评测，Claim 3 有轻度选择泄漏。

**Baseline 和算力可行。**
- TAR、DPH-RL、PTGS、verl-agent、AgenticRL_Handoff 都能克隆，所列文件和函数确实存在。
- TAR 和 DPH-RL 原本是单轮 RLVR 方法，移植到多轮是检验对象本身，不算错配，但没有现成的多轮复现。
- 约 19 天、8×A100 可以完成。

## Claim 判断

| Claim | 判断 | 关键依据 |
|---|---|---|
| 1 按轮剖面 L(t)（入口锁定 vs 观察后重新锁定） | 部分重合 | 交接协议来自 Reach or Solve，分叉噪声底来自 Replay Gap，"入口"假设来自 Locked at the Entrance（单轮）。新的只是把它们用在同起点的 (B, G) 对和覆盖指标上。测量组合有新意，方法没有。 |
| 2 测试时对应物预测训练方法增益（主贡献） | 新颖，但当前检验不能区分 | 没有检索到先例。但 b > 0 会被共享的提升空间自动满足，推翻条件没有检验"本方法的对应物比其他方法的对应物更能预测本方法的增益"；τ 只基于 4–7 个点。PTGS 对应物的构念不对应。 |
| 3 剖面选轮前向 KL 优于随机选轮 | 部分重合 | 按位置掩码的前向 KL 是 DPH-RL 加轮掩码。按问题锚定已有 PBA（arXiv 2607.20543，单轮）。随机选轮对照设计得对，借鉴了 Coverage, Not Targeting 的匹配随机对照。S 在评测任务上选出，有轻度泄漏。 |

## 最高近邻

1. **Sharpening Tax in Post-Training**（https://arxiv.org/abs/2610.01509 ，代码 https://github.com/changdaeoh/sharpening-tax ）
   - 重叠：在 WebShop 上做任务级锐化税测量，有 PTGS，有基座/后训练模型按任务路由（附录 D.4）。
   - 差别：没有按轮接管，也没有预测训练方法效果。
2. **Reach or Solve? Checkpoint Handoffs**（https://arxiv.org/abs/2609.19636 ）
   - 重叠：在 ALFWorld 上做检查点交接，分离到达与完成。
   - 差别：比较的是 SFT↔RL 的成功率，不涉及基座↔GRPO 的覆盖，也不预测训练方法。
3. **Locked at the Entrance, Open Inside**（https://arxiv.org/abs/2608.29188 ）
   - 重叠：把 RLVR 的覆盖收缩定位到入口，并据此给出修法。
   - 差别：只在单轮 Countdown / 数学上，没有多轮，也没有量化预测。
4. **The Replay Gap**（https://arxiv.org/abs/2608.08239 ）
   - 重叠：在真实环境中分叉换模型，并用同模型分叉测噪声底。
   - 差别：研究对象是路由评测（SWE-bench），与 RL 覆盖无关。
5. **When RLVR Shrinks the Reasoning Boundary（PBA）**（https://arxiv.org/abs/2607.20543 ）
   - 重叠：把 pass@k 倒挂定位到边界题，并做按题基座锚定。
   - 差别：在单轮上按题而不是按轮定位，没有预测框架。

```json
{
  "score": 7.0,
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "Claim 2 claim blocker：含方法固定效应的任务级回归中，b>0 会被共享的提升空间（B 有成功、G 全失败的任务对所有对应物与训练方法同时有空间）自动满足，推翻条件无法区分方法特异预测与共享提升空间；Kendall τ>0 仅基于 7/4 个方法，零假设下约一半概率成立，检验过弱"
  ],
  "novelty_conclusion": "按轮可找回覆盖剖面是 Reach or Solve 交接与 Replay Gap 分叉在 (B,G) 覆盖上的新组合（部分重合）；用测试时对应物预测训练方法覆盖增益未检索到先例，方向新颖，但当前推翻条件不能把它与共享的提升空间区分开；剖面选轮前向 KL 是 DPH-RL 加轮掩码，增量有限。PTGS 对应物与其训练期按题调温机制不对应。",
  "closest_neighbors": [
    "Sharpening Tax in Post-Training (arXiv 2610.01509)",
    "Reach or Solve? Deep Diving into Agentic RL Gains with Checkpoint Handoffs (arXiv 2609.19636)",
    "Locked at the Entrance, Open Inside: Where RLVR Narrows the Solution Space (arXiv 2608.29188)",
    "The Replay Gap: Static Evaluation of Model Switching in LLM Agents Scores the Wrong World (arXiv 2608.08239)",
    "When RLVR Shrinks the Reasoning Boundary: Diagnosing Pass@k Inversion (arXiv 2607.20543)"
  ]
}
```
