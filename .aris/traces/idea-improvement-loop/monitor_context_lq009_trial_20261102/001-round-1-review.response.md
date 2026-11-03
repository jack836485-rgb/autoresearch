## 结论

2026-11-02：总体 **6.3/10**，**promising_needs_revision**。主贡献是用动作依赖闭包分配监控证据预算；若自然轨迹上的同预算、低误报优势成立，它会提供有用的监控方法，但当前与 TRACE、PCAS 的实质差别及强基线比较尚不足以达到贡献门槛。

## Claim 判断

| 维度 | 分数 | 判断依据 |
|---|---:|---|
| 重要性 | 8.0 | CoT 缺少直白意图时，仍能在低误报和有限计算下识别跨步骤违规，是实际监督的重要瓶颈；自然轨迹上稳定提高召回具有实质价值。 |
| 新颖度 | 6.0 | 按待执行动作追溯原始证据，有别于 TRACE 的可疑窗口调查；但跨窗口证据聚合已由 TRACE 提出，按动作反向切片并据此授权已由 PCAS 明确定义，当前闭包和依赖距离排序尚只构成可辨认增量。 |
| 有效性 | 6.0 | 自然/构造结果分离、整轨迹误报校准、结构元数据对齐及闭包消融，足以支持有限结论；前提是在自然关系子集达到所述 ≥10 个百分点且 CI 排除 0。现有比较仍不能说明优于直接进行跨步骤证据调查的强近邻，故不支持 8 分。 |

**可行性：fail（当前完整验证方案）。** 公开 MRT 数据、层级/顺序实现及现有 GPU 使主体实验具备实现基础；80.64M 输入、2.58M 输出的乘法预算也正确。但仓库的层级方法逐块读取全部原文，顺序方法还会重送历史或摘要：在 32k/64k 轨迹上，未经定义的原版方法无法满足整轨迹 16k 输入上限。摘要后的聚合和 hybrid 会进一步增加开销；当前没有交代预算耗尽时保留哪些块、如何保证同一在线可见前缀和覆盖机会，因而“直接调用现有入口”尚不是所声称同预算强基线的复现路线。[MRT 实现](https://raw.githubusercontent.com/scaleapi/mrt/main/utils/pipeline_utils.py)

新增的值得使用之物，应当是**从不可靠 CoT 的自然长轨迹中，以实际依赖关系取回判据的预算化监控器**。目前不能把“跨窗口证据重要”本身计作新发现：TRACE 已研究同一 SHADE-Arena 设置中的远程弱证据、任务约束提取、跨窗传播和 selective-verbalization/liar 策略。其原方法是事后检测，确实不能原样充当在线对照；但当前方案既没有该近邻的可核验公共实现及前缀适配路线，也未完成已承认重要的 ledger 对照规范核验。这是强对照证据缺口，不能靠宣称 MRT 强、或预设本方法提升 10 个百分点替代。[TRACE 方法与附录提示](https://arxiv.org/html/2606.07054v1)

按任务划分是正确的；“至少三个任务族”却没有确定自然远程依赖样本及各类样本数量，120 条轨迹也不等于 120 个独立任务。现有证据因此尚不能保证主结果的覆盖范围与置信区间。奖励失配扩展被明确隔离、不将提示隐藏冒充训练失配，这一点是对的。

## 最高近邻

- **[TRACE: Trajectory Reasoning through Adaptive Cross-Step Evidence Aggregation for LLM Agents](https://arxiv.org/abs/2606.07054)**：同任务、同隐蔽策略，已将远程证据关联作为核心并进行跨窗调查；差别是本文拟做动作驱动的结构闭包与调用前监控。论文附录可读，本次未核验到其官方公共实现。
- **[Policy Compiler for Secure Agentic Systems](https://arxiv.org/html/2602.16708v2)**：§3 已定义 proposed action 的 backward slice，并在执行前依据因果历史授权；差别是其使用显式形式策略，本文拟从自然任务约束中取回证据交给冻结 LLM，且施加 token 预算。
- **[Paranoid Monitors: How Long Context Breaks LLM Agent Supervision](https://openreview.net/pdf/246057da14aa98310c6858bf480370e5d10f0ebb.pdf)**：同用加长的 SHADE-Arena 轨迹，先抽取状态事实再做策略判断；差别是固定 ledger 与按动作取回原始证据。索引摘要可核验，全文直接访问遇到验证页，官方代码仍需要检索。
- **[Reliable Weak-to-Strong Monitoring of LLM Agents](https://arxiv.org/abs/2508.19461)**：提供相同任务、规避策略和层级/顺序/hybrid 对照；差别是分块摘要而非显式对象依赖。[官方代码与数据入口](https://github.com/scaleapi/mrt)可核验，本文预算下的具体适配尚未成立。
- **[Minos: A Multi-Agent Collaborative Framework for Provenance-Based Backward Tracking](https://arxiv.org/abs/2607.00440)**：已有来源图反向追踪、分层状态和带出处检索；它从安全告警调查系统入侵，不是从全部工具动作进行在线违规监控，属于机制近邻而非同任务实验基线。

```json
{
  "score": 6.3,
  "contribution_scores": {"importance": 8.0, "novelty": 6.0, "effectiveness": 6.0},
  "contribution_assessment": "自然轨迹上同预算低误报的动作依赖取证若成立，会提供重要的监控能力；但跨步骤证据聚合已有TRACE、动作反向切片与执行前授权已有PCAS，当前仅明确增量新意。机制消融与自然/构造分离支持有限结论，但未能排除最高同任务近邻，尚不具备两个维度达到8分的依据。",
  "feasibility": "fail",
  "feasibility_reason": "公开MRT数据和层级/顺序代码及GPU资源足以实现主体实验，总token乘法预算正确；但32k/64k全文层级/顺序方法本身超过整轨迹16k输入上限，尚无明确且保持在线前缀与合理覆盖的预算适配复现路线，TRACE及ledger强对照的公共实现或充分复现规范也未完成核验。",
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "贡献门槛未通过：只有importance达到8，新颖度和有效性均为6。",
    "当前定位遗漏TRACE的同任务跨窗口证据聚合及PCAS已定义的动作反向切片，尚不足以支持闭包视角有独立高新意。",
    "强基线比较与复现证据不完整：TRACE未进入比较且公共实现未核验，ledger规范仍缺；MRT原方法与16k整轨迹预算在32k/64k输入条件下不相容，预算适配未定义。"
  ],
  "novelty_conclusion": "动作驱动的原文取证与预算排序具有增量差别，但跨窗聚合和动作因果切片分别已有直接先例，当前证据不能支持8分新颖度。",
  "closest_neighbors": [
    "TRACE: Trajectory Reasoning through Adaptive Cross-Step Evidence Aggregation for LLM Agents",
    "Policy Compiler for Secure Agentic Systems",
    "Paranoid Monitors: How Long Context Breaks LLM Agent Supervision",
    "Reliable Weak-to-Strong Monitoring of LLM Agents",
    "Minos: A Multi-Agent Collaborative Framework for Provenance-Based Backward Tracking"
  ]
}
```
