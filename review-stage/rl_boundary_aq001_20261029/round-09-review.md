## 结论

日期：2026-10-29。**score = 6.0，verdict = promising_needs_revision。**

**新颖性判断：部分新颖。**
- 在多轮 agent 中用真实环境逐轮替换 B/G 并减去同模型分叉噪声底，测"按轮可找回的覆盖"，我没有检索到直接先例。
- 但测量工具本身来自已有工作：问题来自 Locked at the Entrance（单轮入口定位），协议来自 Reach or Solve（检查点交接）和 Replay Gap（分叉加同模型噪声底）。Sharpening Tax 已在 WebShop 上做过任务级的 base/post-trained 路由与"哪些任务付税"分析。
- 真正属于本 idea 的增量是 Claim 3：在训练前用逐轮剖面按任务预测各保覆盖方法能找回多少。这一条目前的可操作性和统计功效不足。

**值得继续，但现在不能进入实验。** 有三类阻断：
- **定位事实错误。** brief 说"保覆盖方法都在单轮上提出"，但 PTGS 是在多轮 Sokoban / FrozenLake RL 上提出并验证的，Sharpening Tax 在 WebShop 上测过税；DivInit 本身也是多轮 agentic search 方法。
- **Claim 3 的预测量定义不自洽。** 一是 Σ_{t∈A_m} L_i(t) 把单轮替换增益相加，默认了跨轮可加，而方案只对剂量做了匹配，没有检验可加性。二是 PTGS 的 A_m 是"所有轮但只改多样性"，给不出数值预测。三是训练后方法改变的是整条策略，并不只作用于 A_m。
- **功效不足。** 门槛只要求 pass@64 下降 ≥5pp。300 个任务中真正丢失的任务可能只有十几到几十个，而每个方法组在大多数设置上只有 1 个种子。按任务做 Spearman 和三分层单调检验时，"不显著"无法区分是假设被推翻还是噪声。按现在的推翻条件，这条 Claim 实际上推不翻。
- **Baseline。** PBA 没有公开代码。TAR、DPH-RL 和晚层插值的原任务都是单轮数学或 Countdown；作为"被检验的对象"可以接受，但移植到 verl-agent 多轮轨迹目前没有现成路线。以下入口已用 git 核实，其余可用：TAR 的 `recipe/tar/build_memory_bank.py`、Handoff 的 `src/handoff/alfworld/{environment,rollout}.py`、PTGSHooks、`WEBSHOP_ENV_SEED`、verl-agent 的 `run_webshop.sh` 与 `run_alfworld.sh`。

## Claim 判断

| Claim | 判断 | 关键依据 |
|---|---|---|
| 一句话定位："现有保覆盖方法都在单轮上提出" | 不成立（claim blocker） | PTGS 在多轮 Sokoban / FrozenLake（每回合最多 5 轮）上训练，Sharpening Tax 在 WebShop、BFCL MT、ACEBench 上测税；DivInit 是多轮搜索 agent 的方法 |
| 1. 按轮定位：区分入口锁定与观察后重新锁定 | 部分重合 | 单轮入口定位已由 2608.29188 给出；交接与分叉协议已由 2609.19636 和 2608.08239 给出。把这两者用在多轮覆盖丢失的定位上仍是新的，属于测量层面的迁移 |
| 2. 被锁定轮上丢的是基座分支分布，提温 / REFT 不够 | 部分重合，增量小 | 2608.29188 已显示单轮上表面干预无效、晚层插值有效；在观察后决策轮上"换成基座 > 提温"基本是预期结果，区分力有限 |
| 3. 方法找回量 ≈ Σ_{t∈A_m} L_i(t)，按任务预测 | 新颖，但当前不可检验（claim blocker） | 未检索到先例。但存在三个问题：单轮替换可加性未经验证；PTGS 的 A_m 没有数值预测；风险任务少、种子少，Spearman 不显著时无法与噪声区分 |
| 3'. 剖面选轮前向 KL 优于同 token 占比的随机选轮 | 新颖、可推翻 | 2609.02417 比较的是优势或信用的定向，不是 KL 锚定的选轮；但"锚定作用于分布、信用作用于奖励"只是论断，没有证据支撑 |

## 最高近邻

1. **Sharpening Tax in Post-Training**（https://arxiv.org/abs/2610.01509）
   - 重叠：多轮 agent 的覆盖税；WebShop 评测；PTGS 在多轮 RL 中保覆盖；按任务的税分解与 base/post-trained 路由。
   - 差别：只做任务级分析，没有按轮定位，也没有对方法族做预测。
2. **Locked at the Entrance, Open Inside**（https://arxiv.org/abs/2608.29188）
   - 重叠：定位 RLVR 在轨迹的哪个位置丢失广度；入口干预；晚层插值。
   - 差别：单轮 Countdown 和数学，没有环境观察后的重新锁定。
3. **Reach or Solve? Checkpoint Handoffs**（https://arxiv.org/abs/2609.19636）
   - 重叠：在 ALFWorld 上用真实环境回放交接两个检查点。
   - 差别：交接的是 SFT↔RL，看成功率，不涉及覆盖或 pass@k，也不比较方法。
4. **The Replay Gap**（https://arxiv.org/abs/2608.08239）
   - 重叠：在真实环境中分叉换模型，并用同模型对照作噪声底。
   - 差别：研究的是路由评测（SWE-bench），不涉及 RL 和覆盖。
5. **When RLVR Shrinks the Reasoning Boundary（PBA）**（https://arxiv.org/abs/2607.20543）
   - 重叠：按题的风险门控、基座锚定、边界题丢失。
   - 差别：单轮数学，没有按轮维度，没有公开代码。

```json
{
  "score": 6.0,
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "Positioning claim is factually wrong: PTGS (2610.01509) was proposed and validated in multi-turn agent RL (Sokoban/FrozenLake) and Sharpening Tax measures the tax on WebShop; DivInit is a multi-turn agentic-search method, so 'existing coverage-preserving methods are all single-turn' does not hold",
    "Claim 3 predictor is not well-defined: summing single-turn swap gains assumes cross-turn additivity that is never tested; PTGS's action region yields no numeric prediction; training-time methods change the whole policy rather than only A_m",
    "Claim 3 is underpowered and so cannot be falsified: with a >=5pp pass@64 gate only about 15-40 risk tasks remain, and most method groups have 1 seed, so a non-significant Spearman cannot be told apart from noise",
    "PBA has no public implementation; TAR and DPH-RL are single-turn math codebases whose port to multi-turn verl-agent trajectories has no concrete existing route"
  ],
  "novelty_conclusion": "Partially novel. Per-turn localization of coverage loss in multi-turn agents (base swap at turn t minus a same-model fork noise floor) has no direct precedent found, but it transfers the question of 2608.29188 and the handoff/fork protocols of 2609.19636 and 2608.08239. The distinct contribution, using the per-turn profile to predict which coverage-preserving method family recovers coverage on each task, is new but not yet operationalized or powered.",
  "closest_neighbors": [
    "Sharpening Tax in Post-Training (arXiv 2610.01509)",
    "Locked at the Entrance, Open Inside: Where RLVR Narrows the Solution Space (arXiv 2608.29188)",
    "Reach or Solve? Deep Diving into Agentic RL Gains with Checkpoint Handoffs (arXiv 2609.19636)",
    "The Replay Gap: Static Evaluation of Model Switching in LLM Agents Scores the Wrong World (arXiv 2608.08239)",
    "When RLVR Shrinks the Reasoning Boundary: Diagnosing Pass@k Inversion (arXiv 2607.20543)"
  ]
}
```
