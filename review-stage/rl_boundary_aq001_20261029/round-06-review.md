## 结论

2026-10-29 评审：**score 7.8 / 10，verdict = promising_needs_revision**。

- **诊断部分新颖，暂未找到覆盖它的工作。** 在多轮工具 agent 上，用纯 GRPO 检查点与同起点基座做逐轮替换，在真实环境中重建状态并减去同模型分叉的噪声底，来区分"入口锁定"与"观察后重新锁定"。检索到的近邻要么是单轮（2608.29188、2605.28295、2607.20543），要么只在一个交接点切换（2609.19636），要么只做第一轮测试时多样化（2606.17209），要么只做任务级分析（2610.01509）。
- **修法的新颖性仍取决于实验结果。** 若 L(t) 集中在第 1 轮，S = {1}，"按剖面前向 KL"就退化为"入口前向 KL"，即 2608.29188 的结论加 DPH-RL 损失的直接组合，Claim 3 不再有独立贡献。
- **随机选轮匹配对照不是本文首创。** 2609.02417 已在多轮 agent RL 中提出 matched-concentration shuffled control，并发现"集中到进展轮"与"集中到随机轮"同样有害。这使"选哪些轮比锚定多少更重要"的先验支持变弱，需在定位中正面处理。
- **Claim 1 的聚合比较存在剂量混杂。** "只替换第一轮 < 替换全部决策轮"即使在纯入口锁定下，也可能仅因替换轮数更多、注入的独立随机性更多而成立。Claim 2 的等熵提温组只部分吸收了这一混杂。
- **可行性方面没有致命问题。** 核验了 6 个仓库，均可访问：sharpening-tax 的 `benchmarks/webshop.py` 支持 `WEBSHOP_ENV_SEED`；`ptgs/integration.py` 中有 `PTGSHooks`；配置确认原作只在 Sokoban / FrozenLake 上验证；verl-agent 有 `run_webshop.sh`；DPH-RL 有 forward 配置；early-branch-locking 有 `layer_interpolation.py`；AgenticRL_Handoff 可访问。Baseline 与任务同域，算力在 8×A100 约 11 天内可行，阶段 0 的停止规则诚实。
- **值得继续。** 阶段 0 加阶段 A 约 2 天，就能判定 Claim 1 与 2。但目前修法的新颖性边界没有解决，未达到 experiment_ready。

## Claim 判断

| Claim | 判断 | 关键依据 |
|---|---|---|
| 1. 区分入口锁定与观察后重新锁定（逐轮替换剖面 L(t)） | 新颖 | 2608.29188 只做单轮；2609.19636 只有单个交接点，比较的是 SFT↔RL 与 reach/solve；2608.08239 有分叉 + 噪声底方法，但用于路由，不是 RL 覆盖。未检索到多轮 agent 上 RL 前后逐轮覆盖定位的工作。需处理"替换轮数多 → 注入随机性多"的剂量混杂。 |
| 2. 观察后的锁定轮丢的是基座分支分布，不只是熵 | 部分重合 | 单轮"提温无效"已由 2608.29188 报告；REFT（2605.28295）是首 token 多样化。迁移到观察后决策轮属增量，作为对照合理，独立贡献较小。 |
| 3. 按剖面选轮的前向 KL 优于入口 / 全局 / 随机选轮 KL、熵奖励与 PTGS | 部分重合，新颖性取决于结果 | 前向 KL 损失来自 DPH-RL（2509.07430）；按问题选择性锚定基座有 PBA（2607.20543，prompt 粒度）；按诊断选状态训练有 Critical-State RL（2609.24985）；匹配集中度的随机对照来自 2609.02417，且其结果为负。若 S = {1}，本 Claim 等同于入口 KL。 |

## 最高近邻

1. **Locked at the Entrance, Open Inside**：https://arxiv.org/abs/2608.29188
   - 重叠：入口锁定概念、前缀补入后替代分支可执行、晚层插值修法。
   - 差别：只做单轮 Countdown 与数学，没有观察后的决策点，也没有训练时的选轮锚定。
2. **Reach or Solve? Checkpoint Handoffs**：https://arxiv.org/abs/2609.19636
   - 重叠：在多轮 agent 中做检查点交接并真实回放。
   - 差别：单交接点、比较 SFT↔RL 发布检查点、看 pass@1 与 reach/solve，不做逐轮基座替换、不看大 k 覆盖、没有修法。
3. **Sharpening Tax in Post-Training**：https://arxiv.org/abs/2610.01509
   - 重叠：同一 WebShop harness，测量大 k 覆盖损失，并提出 PTGS。
   - 差别：只做任务级分析，比较的是混合了多种后训练的发布对，没有逐轮定位。
4. **Coverage, Not Targeting**：https://arxiv.org/abs/2609.02417
   - 重叠：多轮 agent RL 中"集中到选定轮"对比"匹配集中度的随机轮"，结论是 targeting 不优于均匀分配。
   - 差别：研究对象是信用分配与奖励密度，不是基座锚定或覆盖保持。但它直接削弱了 Claim 3 的先验。
5. **When RLVR Shrinks the Reasoning Boundary（PBA）**：https://arxiv.org/abs/2607.20543
   - 重叠：选择性地把部分训练信号锚定到冻结基座，以保 pass@k。
   - 差别：选择单位是 prompt 而非轮次，且只做单轮数学。

```json
{
  "score": 7.8,
  "verdict": "promising_needs_revision",
  "fatal_blockers": [],
  "novelty_conclusion": "The per-turn base-substitution profile that separates entrance locking from post-observation re-locking in multi-turn agent RL appears novel; no covering work found. The fix's novelty is conditional: if L(t) concentrates at turn 1, profile-selected forward KL reduces to entrance forward KL (2608.29188 + DPH-RL). The random-turn matched control has precedent in 2609.02417, which found targeting no better than random. Claim 1's first-turn vs all-decision-turn comparison is confounded by how many turns are swapped. Baselines and repos verified; feasible on 8xA100.",
  "closest_neighbors": [
    "Locked at the Entrance, Open Inside: Where RLVR Narrows the Solution Space (arXiv 2608.29188)",
    "Reach or Solve? Deep Diving into Agentic RL Gains with Checkpoint Handoffs (arXiv 2609.19636)",
    "Sharpening Tax in Post-Training (arXiv 2610.01509)",
    "Coverage, Not Targeting: A Structural Regime in Multi-Turn Agent Credit Assignment (arXiv 2609.02417)",
    "When RLVR Shrinks the Reasoning Boundary: Diagnosing Pass@k Inversion (arXiv 2607.20543)"
  ]
}
```
