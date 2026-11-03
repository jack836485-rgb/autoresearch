## 结论

2026-11-02：总体 **6.2/10**，**needs_rethink**。主贡献是把合法／违规解释之间的预测分歧用于分配极少量状态查询；成功后会得到一种更省查询的事后违规审查策略，但当前方案仍主要是既有竞争假设调查在新审查条件下的直接适配，尚不足以通过主会贡献门槛。

## Claim 判断

| 维度 | 分数 | 依据 |
|---|---:|---|
| 重要性 | 7.0 | 低误报下发现长轨迹中的违规有明确价值；但本主贡献只处理强文本调查后、终态仍保留且可查询的事实歧义，尚无证据说明这类瓶颈覆盖足够广，不能把整个监督问题的重要性直接算给该适配。 |
| 新颖度 | 5.5 | “提出竞争解释，再选预测不同的观测”已有直接机制近邻；目前新增的是合法／违规二分、终态只读工具和一两次预算，未说明这些条件产生了何种独立的新选择机制或研究认识。 |
| 有效性 | 6.0 | 当前有 Arbiter 的主动检查结果、OpenAI 的对话外取证实践，以及 MRT 可读取内容和共享权限的真实工具实现；这些加上预测分歧消歧机制，支持在相关事实缺失且终态可回答时改善判断的合理预期。未知的是这类事实在自然队列中的频率、模型生成的两解释是否覆盖真因，以及它能否胜过同权限 ReAct；现有证据没有跨过最后一步。 |

有效性的依据适用范围很具体：[Arbiter](https://arxiv.org/html/2606.10747v1)研究的是短多智能体对话，询问对象及检查内部信息与终态独立状态查询不同；[OpenAI 的 L3 调查](https://alignment.openai.com/how-we-detect-frontier-model-misalignment)证明对话外遥测确实被用于调查，并未给出本查询策略相对自由调查的受控优势。[MRT 的工具](https://raw.githubusercontent.com/scaleapi/mrt/main/tools/drive_tools.py)确实能够返回文件内容等状态。因此 6 分来自适用的局部机制和邻近证据，不来自未来成功阈值，也不因尚无 pilot 而机械封顶。

最小实验基本能判断“增加观测是否有用”以及“本策略是否优于同权限查询”：强共享文本层、相同 k、可自适应 ReAct、查询结果交给共同判定器，能避免把权限或最终解释器优势误归给选择策略。TRACE 的原始 §3.2 与附录 B.1–B.4 确有完整操作和提示；所列预算与停止补充足以形成透明的独立实现，不因缺少官方代码阻断比较。但计入 token 只建立成本记录，尚不等于控制相同总计算；如果方法只在消耗更多推理 token 时胜出，当前实验不能支持“相同计算下提高召回”。此外，[MRT §3.4](https://arxiv.org/html/2508.19461v1#S3.SS4)的目标包含朝副任务采取行动的尝试，不等同于副任务完成或最终有害状态，公开“任务标签”的具体含义仍限制“实际违规”这一表述的解释。

**可行性：pass。** [公开数据](https://huggingface.co/datasets/ScaleAI/mrt)、Python 环境与只读工具提供了可信实现路径；小规模冻结开源监控器推理和 CPU 状态重建没有显示超出给定资源的必要依赖。TRACE 独立实现可按原始提示及明确声明的预算补充完成。10.24M 输入／1.31M 输出是主动臂增量估计，共享全文调查及复现成本另计，不能当作已验证的总耗时保证；当前也没有证据据此判定资源不可获得。状态重放覆盖率仍需实际运行确认，但效果未知和实现不可行是两回事。

三维未满足“两项至少 8 分”，且新颖度不足 6；完善对照和诚实复现路径解决了可检验性问题，并未自动形成足够的方法贡献。

## 最高近邻

- [SHELDON: Reasoning through Dual Search over Hypothesis and Observation Spaces](https://arxiv.org/html/2610.18025v1)：§4 的 ComparativeAnalysis 明确根据假设预测差异选择区分它们的测试，与核心选择原则直接重叠；其任务和搜索规模不同，不能直接充当 SHADE 性能基线。
- [TRACE: Trajectory Reasoning through Adaptive Cross-Step Evidence Aggregation for LLM Agents](https://arxiv.org/html/2606.07054v1)：同为 SHADE 事后轨迹审查，已有预算内定向调查、证据累积与最终判断；区别是本方案追加真正的环境观测，而非继续分析已有轨迹。
- [The Arbiter Agent](https://arxiv.org/html/2606.10747v1)：已有预算化 ReAct 监控、形成假设并主动取证；区别是持续多智能体对话检查，未验证本文的终态两解释查询策略。
- [Reliable Weak-to-Strong Monitoring of LLM Agents](https://arxiv.org/html/2508.19461v1)：提供同任务、长轨迹、规避策略和强 hybrid 对照；本方案的增量在文本之外的有限事实查询，而非长轨迹分层调查本身。
- [How we detect frontier model misalignment](https://alignment.openai.com/how-we-detect-frontier-model-misalignment)：已将分层文本调查与网络日志／遥测等外部证据结合；未公开本方案的极小查询分配机制及同预算策略比较。

```json
{
  "score": 6.2,
  "contribution_scores": {"importance": 7.0, "novelty": 5.5, "effectiveness": 6.0},
  "contribution_assessment": "主贡献是用合法与违规解释的预测分歧分配一两次终态只读查询，成功后可提供更有效的有限查询审查策略。问题有明确价值，主动取证和可访问状态支持条件性效果预期；但竞争假设选择区分性观测已有直接近邻，目前增量主要是任务与预算适配，既无两项8分，也未达到新颖度6分。自然队列中相关缺失事实的覆盖以及胜过同权限ReAct仍未知。",
  "feasibility": "pass",
  "feasibility_reason": "MRT公开数据、Python环境和只读工具可用；TRACE原始提示及操作足以支持声明预算补充的独立实现，不要求官方代码。小规模冻结开源监控器推理有可信资源路径，但共享调查总成本与状态重放覆盖率尚未经运行核验。",
  "verdict": "needs_rethink",
  "fatal_blockers": [
    "贡献门槛未通过：importance=7.0、novelty=5.5、effectiveness=6.0，没有两项达到8且新颖度低于6。",
    "当前核心规则与已有竞争假设区分性观测选择直接重叠，任务二分与一两次预算尚未构成足够独立的方法贡献。",
    "同查询次数并记录token不等于匹配总计算；现有方案不足以无条件检验相同计算下提高召回这一Claim。"
  ],
  "novelty_conclusion": "未核验到完全相同的SHADE终态两查询系统，但机制近邻已明确按竞争假设的预测差异选测试；当前可辨认的任务适配不足以构成所需独立新意。",
  "closest_neighbors": [
    "SHELDON: Reasoning through Dual Search over Hypothesis and Observation Spaces",
    "TRACE: Trajectory Reasoning through Adaptive Cross-Step Evidence Aggregation for LLM Agents",
    "The Arbiter Agent: Continually Monitoring Multi-Agent Conversations to Detect Emergent Misalignment",
    "Reliable Weak-to-Strong Monitoring of LLM Agents",
    "How we detect frontier model misalignment"
  ]
}
```
