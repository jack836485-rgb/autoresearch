## 结论

截至 2026-10-29：**score 7.5 / 10，verdict = promising_needs_revision。** 值得继续，阶段 0 加阶段 A 约 2 天就能给出结论。

**Claim 1 有新意，且可证伪。** 问题是多轮工具 agent 的纯 RL 检查点在观察之后会不会被重新锁定，做法是在真实环境里逐轮用基座替换，并以同模型分叉作为噪声底。检索到的近邻都没有在多轮 agent 上做这种逐轮剖面：
- Locked at the Entrance 只做单轮；
- Reach or Solve 在 SFT 和 RL 之间做交接，只看 pass@1，交接点靠近终点；
- Sharpening Tax 只做任务级三分类；
- PASS@(k,T) 只扫交互预算。

无论剖面集中在入口还是分散到后续决策轮，结果都可报告。

**新意边界还有三处没收紧：**
1. **Claim 3 的方法薄。** 修法是 DPH-RL 的前向 KL 加一个按轮掩码，算法上几乎没有新东西，价值完全取决于 Claim 1 先成立。
2. **Claim 2 部分是单轮结论的迁移。** "提温或只增加多样性找不回覆盖"在单轮里已由 Locked at the Entrance 报告过（提温和提示无效）。多轮里新的部分只有"在观察之后的轮上也如此"。
3. **漏了一个近邻。** 简报没有和 DDO（arXiv 2609.10052）划界。DDO 在 WebShop 上从轨迹中段共享的决策状态出发构造分支，并以成功策略覆盖为目标。它已经隐含了"入口之后的决策状态对覆盖重要"，虽然它是偏好训练加专家分支，不是 RL 前后的诊断。

**没有致命 blocker。** 各 baseline 的公开实现都已用 git ls-remote 和浅克隆核验，且与本任务同领域：
- sharpening-tax：有 `benchmarks/webshop.py` 和 `ptgs/integration.py` 的 `PTGSHooks`，PTGS 配置确实只有 Sokoban 和 FrozenLake；配置里有 Qwen2.5-7B 与 Ministral-3-8B 的 base/post 对；
- verl-agent：有 `run_webshop.sh`；
- DPH-RL：README 有 `forward` 散度配置；
- early-branch-locking：有 `layer_interpolation.py`；
- AgenticRL_Handoff：`src/handoff` 只有 alfworld 和 travelplanner，WebShop 要自己加，简报已写明；
- DivInit：仓库可访问。

**落地风险（不致命）：**
- **定位关键词。** "sharpening tax""checkpoint handoff""entrance locking"各自只出自一篇 2026 年 8–10 月的论文，还不是成熟术语，定位时应配上 pass@k coverage、diversity collapse 这类通用词。
- **WebShop 回放。** 该环境的价格约束取自全局随机数，`webshop.py` 注释要求固定 `WEBSHOP_ENV_SEED` 才能复现。逐轮替换依赖真实环境重建状态，必须固定这个种子。
- **外部印证的格式问题。** 发布的 Instruct 模型走 chat 格式，基座走文本 harness。跨模型替换时，同一段历史要按各自格式重新渲染，否则格式差异会混进 L(t)。

## Claim 判断

| Claim | 判断 | 关键依据 |
|---|---|---|
| 1. 多轮 agent 的纯 RL 检查点在观察后的决策轮上被重新锁定，用真实环境逐轮基座替换减去同模型分叉噪声底来测 | **新颖**（问题与诊断） | 单轮的入口锁定（2608.29188）、第一轮查询冗余（2606.17209）、SFT↔RL 交接看 pass@1（2609.19636）、任务级锐化税（2610.01509）都没有做多轮的逐轮 pass@k 剖面。DDO（2609.10052）只间接表明中段决策状态与覆盖有关，没有做 RL 前后的定位 |
| 2. 被锁定轮丢的是基座的分支分布，等熵提温或 REFT 找不回 | **部分重合** | 单轮中提温与提示无效已由 2608.29188 报告，REFT（2605.28295）只作用于首 token。"观察后各轮也如此"是增量，等熵这一对照比单纯提温更严格 |
| 3. 只在决策轮施加前向 KL，在相同 pass@1 下得到最高的 pass@64，优于入口 KL 和全局 KL | **部分重合，方法新意薄** | 损失与估计方式直接沿用 DPH-RL（2509.07430），新意只在按轮掩码。依赖 Claim 1 成立，三向前沿比较可证伪 |

## 最高近邻

1. **Locked at the Entrance, Open Inside**（https://arxiv.org/abs/2608.29188）
   - 重叠：RLVR 的覆盖收缩集中在入口，补前缀可恢复，晚层插值作为修法。
   - 差别：只做单轮 Countdown 和数学，没有观察之后的决策点，也没有多轮 agent。
2. **Reach or Solve? Checkpoint Handoffs**（https://arxiv.org/abs/2609.19636）
   - 重叠：真实环境中的检查点交接与回放。
   - 差别：在 SFT↔RL 之间交接，只看 pass@1 和 Reach/Solve，交接点靠近终点；在 TravelPlanner 和 ALFWorld 上做，没有 WebShop，也没有修法。
3. **Sharpening Tax in Post-Training**（https://arxiv.org/abs/2610.01509）
   - 重叠：WebShop 上发布对的 pass@K 覆盖损失，以及 PTGS。
   - 差别：只做任务级 always/sometimes/never 分类，没有逐轮定位；发布对混合了 SFT、偏好优化和 RL。
4. **DPH-RL**（https://arxiv.org/abs/2509.07430）
   - 重叠：用前向 KL 和离线基座样本保住 pass@k，Claim 3 的损失直接取自它。
   - 差别：单轮、作用于整条序列，没有按轮选择。
5. **Direct Diversity Optimization (DDO)**（https://arxiv.org/abs/2609.10052）
   - 重叠：在 WebShop 上从轨迹中段共享的决策状态构造分支，提升成功策略覆盖。
   - 差别：做偏好训练，分支由 Qwen3.5-122B 专家生成，没有在纯 RL 前后做逐轮定位，也没有 pass@k 剖面。

```json
{
  "score": 7.5,
  "verdict": "promising_needs_revision",
  "fatal_blockers": [],
  "novelty_conclusion": "Claim 1（在多轮 agent 纯 RL 检查点上，用真实环境逐轮基座替换区分入口锁定与观察后重新锁定）在检索范围内新颖且可证伪。Claim 2 部分是 Locked at the Entrance 单轮提温无效结论的迁移。Claim 3 是 DPH-RL 前向 KL 加按轮掩码，方法新意薄且依赖 Claim 1。简报未与 DDO（2609.10052，WebShop 中段决策状态分支与覆盖）划界。baseline 均有可核验的公开实现，无致命 blocker，但新意边界未完全收紧，score 未超过 8。",
  "closest_neighbors": [
    "Locked at the Entrance, Open Inside: Where RLVR Narrows the Solution Space (arXiv 2608.29188)",
    "Reach or Solve? Deep Diving into Agentic RL Gains with Checkpoint Handoffs (arXiv 2609.19636)",
    "Sharpening Tax in Post-Training (arXiv 2610.01509)",
    "DPH-RL (arXiv 2509.07430)",
    "Direct Diversity Optimization for Diverse Successful Trajectories in Preference Post-Training (arXiv 2609.10052)"
  ]
}
```
