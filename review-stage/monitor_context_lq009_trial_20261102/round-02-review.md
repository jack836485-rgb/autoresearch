## 结论

2026-11-02：**score = 7.0；verdict = promising_needs_revision**。主贡献是用实体/字段依赖索引与原文去重改善冻结监控器的成本—召回前沿；若关键结果成立，它会提供一种值得使用的低成本监控实现，但当前证据只能支撑相对 MRT 的有限增量，尚不足以达到至少两项 ≥8 的贡献门槛。

## Claim 判断

| 维度 | 分数 | 实质依据 |
|---|---:|---|
| 重要性 | 8.0 | 自然长轨迹上保持低误报召回而将完整监控输入成本减半，具有实际部署价值；此分数以收益覆盖多个自然任务族、绝对召回仍有用为条件，单纯优于被裁剪的对照不成立。 |
| 新颖度 | 6.0 | 将依赖切片用于自然任务约束下的 LLM 证据选择、并计入去重收益，有可辨认增量；动作依赖图、反向切片、事实提取与判断分离、预算定向调查均已有直接近邻，尚无新的独立机制。 |
| 有效性 | 6.5 | 完整对照与共同预算双协议、任务隔离和同长度消融能支持相对 MRT 的明确结论；但缺少结构可恢复性与证据稀疏性的先验证据，也尚不能区分相较 TRACE/ledger 是否仍有实质效率收益。关键结果必须在自然测试集、整轨迹低误报下达到所述成本减半或召回提升，并排除同长度选择与信息特权解释。 |

**可行性：pass，限于当前明确承诺的 MRT/BM25/窗口比较。** 已核验 MRT 的公开[数据](https://huggingface.co/datasets/ScaleAI/mrt)、[离线监控入口](https://raw.githubusercontent.com/scaleapi/mrt/main/monitor_generation/add_monitors.py)和[顺序/层级实现](https://raw.githubusercontent.com/scaleapi/mrt/main/utils/pipeline_utils.py)；hybrid 的线性分数组合有论文公式，复现路径可信。CPU 索引与冻结推理不依赖新训练能力，给定本地算力足以开展该规模试验。46.08M 输入/1.44M 输出是作者的规划估计，未指定端点价格，不能当作已核定的千元报价；这限制成本结论的确定性，但没有显示实验本身不可实现。此处不把未纳入正式实验臂的 TRACE/ledger 算作已复现基线。

若计划结果成立，新增的知识是：**在指定自然任务分布中，显式对象依赖能保留足以判断违规的证据，因而可以用较少模型阅读替代 MRT 的完整扫描。** 这具有价值，但“达到最强可复现 baseline”仍可能仅表示达到 MRT，而不是当前最强相关调度机制。TRACE 已直接研究同一 SHADE-Arena 场景，并报告其平均调用次数低于顺序监控；这不是 token 优势的证明，却足以说明效率竞争已有直接对手。[TRACE 正文](https://arxiv.org/html/2606.07054v1)

机制上的关键不确定性也尚未被成功阈值消除：schema 引用可以连接对象，却不能直接恢复自然语言授权、改写后的泄露内容或隐式依赖；同一前缀内去重也不保证消除不同动作前缀之间的反复读取。因此，“成本减半”是待验证结果，不能反过来作为预期有效性达到 8 分的依据。120 条校准轨迹中的良性子集规模还未明确，5% 尾部误报阈值的稳定性也未获得保证。承认 TRACE/ledger 证据缺口是正确的主张收敛，但本身不会补足贡献证据。

## 最高近邻

- [TRACE: Trajectory Reasoning through Adaptive Cross-Step Evidence Aggregation for LLM Agents](https://arxiv.org/abs/2606.07054)：同任务的定向调查、跨步证据积累及轨迹判定；本方案区别在于用 CPU 结构索引替代部分模型调度。本次未核验到其官方公共实现，不能据此断言它不可复现或已被超越。
- [Policy Compiler for Secure Agentic Systems](https://arxiv.org/html/2602.16708v1)：明确给出 proposed-action backward slice 与因果上下文上的授权；本方案改为自然语言约束和冻结 LLM 判断，不要求完整形式策略，也没有其确定性保证。
- [Reliable Weak-to-Strong Monitoring of LLM Agents](https://arxiv.org/abs/2508.19461)：已有层级、顺序及 hybrid 监控，也讨论降低长轨迹处理成本；[官方实现](https://github.com/scaleapi/mrt)可核验。本方案新增按对象依赖选择原文，而不是逐块摘要或其分数组合。
- [Paranoid Monitors: How Long Context Breaks LLM Agent Supervision](https://openreview.net/pdf?id=3xaCNSdrMD)：公开检索内容已核验 ledger 状态跟踪与策略判断分离，实验基于 bank-transfer 的合成扩展轨迹；本方案强调无需 LLM 建索引、原文证据及自然多任务轨迹。全文访问遇验证页，详细实现与公共代码仍需检索，不能据摘要认定其成本劣势。

```json
{
  "score": 7.0,
  "contribution_scores": {"importance": 8.0, "novelty": 6.0, "effectiveness": 6.5},
  "contribution_assessment": "主贡献是依赖索引原文证据包带来的监控成本—召回改进。自然多任务中保留有用低误报召回且完整成本减半具有重要实际价值；机制相对动作切片、ledger 与定向调查主要为增量。双协议和消融可以验证相对 MRT 的有限结论，但结构可恢复性、跨前缀重复读取和 TRACE/ledger 效率竞争仍未得到足够依据，有效性不足 8 分。",
  "feasibility": "pass",
  "feasibility_reason": "所承诺的 MRT/BM25/窗口比较具有公开数据、MRT 代码与 hybrid 公式，CPU 索引和冻结推理可在给定算力内实现；API 报价尚未核定，TRACE/ledger 的公共实现也未核验，因此此 pass 不覆盖它们的复现或优越性主张。",
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "贡献门槛未通过：新颖度 6.0、有效性 6.5，仅重要性达到 8。",
    "目前证据设计可支持相对 MRT 的效率结论，但尚不足以证明其相对已有同任务定向调查或 ledger 机制构成主会级实质效率贡献；主动收紧措辞没有消除这一证据缺口。"
  ],
  "novelty_conclusion": "存在可辨认的实现增量，未发现完整同一方案被直接覆盖；动作反向切片、跨步证据关联和跟踪/判断分离已有近邻，当前不能给予独立机制级高新颖度。",
  "closest_neighbors": [
    "TRACE: Trajectory Reasoning through Adaptive Cross-Step Evidence Aggregation for LLM Agents",
    "Policy Compiler for Secure Agentic Systems",
    "Reliable Weak-to-Strong Monitoring of LLM Agents",
    "Paranoid Monitors: How Long Context Breaks LLM Agent Supervision"
  ]
}
```
