## 结论

2026-11-02：总体 **7.0/10**；**promising_needs_revision**。

若关键结果成立，值得使用的贡献是：在长轨迹和不可靠推理文本下，用一两次针对解释分歧的环境查询，在固定误报及计算预算内提高实际违规召回；这有重要实用价值，但当前方案尚未充分区分查询策略收益与查询次数收益，也未证明胜过同任务的强文本监控，未达到两个维度至少 8 分的门槛。

## Claim 判断

| 维度 | 分数 | 实质依据 |
|---|---:|---|
| 重要性 | 8.0 | 若自然完整队列上、全轨迹 FPR=5% 且总预算相同时，实际召回稳定提高至少 10 个百分点，会实质改善工具代理监督；价值在实际检测，而非中间置信度。 |
| 新颖度 | 6.0 | 两种解释驱动的少量环境查询有可辨认增量，但主动审查及对话外取证均已有先例；目前主要是已有主动诊断思路在此任务中的具体化。 |
| 有效性 | 6.0 | 自然轨迹、执行前快照、禁止标签接口、任务隔离及共享查询结果对照，足以支持有限的信息价值结论；要支持更强的方法收益，关键结果必须排除查询配额及强文本取证的替代解释，当前设计尚不能做到。 |

**可行性：fail，针对当前提交的比较实验；基础组件本身具有可信实现路径。** [MRT 公开仓库](https://github.com/scaleapi/mrt)提供轨迹加载、模拟环境和监控入口，[只读工具源码](https://raw.githubusercontent.com/scaleapi/mrt/main/tools/drive_tools.py)确有文件内容及分享状态的读取路径，因此重放与冻结模型实验没有明显资源障碍。不过，方案明确把普通 ReAct 限为一次查询，本方法最多两次，直接违背同查询配额前提；即便总 token 上限相同，多一次自适应环境观察仍能改变结果。按照本次审查要求，这属于实验基线条件不匹配的阻断，而不是效果未知造成的阻断。40M 输入、3M 输出只是规模估计，未定模型和报价也不能被当作已证明千元内可完成。

另一个 Claim 阻断是强文本基线覆盖不足：[MRT 原文](https://arxiv.org/html/2508.19461v1)已在相同 SHADE-Arena 条件下研究 hierarchical/sequential/hybrid，并明确报告 hybrid 更可靠；[公开监控入口](https://raw.githubusercontent.com/scaleapi/mrt/main/monitor_generation/add_monitors.py)允许选择监控样式，hybrid 的组合公式也已公开。当前只比较顺序监控再多读文本，无法排除结果来自更弱的跨步骤证据聚合，而非真正需要轨迹外事实。TRACE 同样是同任务的已有轨迹证据调查近邻；将其列作近邻并不等于已经排除了其解释。

自然前缀之外是否存在足够多可查询判据，仍是正常的待验证假设；方案明确设置停止条件，这一点是合理的。当前并未以已有文献替代本方法的正面结果，也正确区分了提示隐藏与奖励失配训练。上述优点不足以将有效性提升到 8 分。

## 最高近邻

- [Reliable Weak-to-Strong Monitoring of LLM Agents（MRT）](https://arxiv.org/abs/2508.19461)：完全相同的轨迹、规避策略和监控任务，已有强 hybrid 监控及[公开实现](https://github.com/scaleapi/mrt)；本方案的差别是执行前主动读取已有轨迹之外的环境事实。
- [The Arbiter Agent](https://arxiv.org/abs/2606.10747)：已提出预算约束的 ReAct 式主动监控，可询问代理、检查推理和系统提示，并有[公开代码](https://github.com/aisilab/arbiter)；不同点是本方案查询环境对象，且针对具体动作违规，不应把其对话任务直接充作同任务对照。
- [How we detect frontier model misalignment（OpenAI，2026-10-29）](https://openai.com/index/how-we-detect-frontier-model-misalignment/)：L2 已能运行代码检查证据，L3 明确结合对话外网络日志和系统遥测；因此独立外部取证本身已有实践。尚未见该报告给出本方案这种两解释、少查询、公开等预算算法比较，故它是定位近邻，不能冒充可直接复现实验基线。
- [TRACE: Trajectory Reasoning through Adaptive Cross-Step Evidence Aggregation for LLM Agents](https://arxiv.org/abs/2606.07054)：在 SHADE-Arena 上自适应定位可疑窗口、调查跨步骤证据并维护证据状态；主要使用已有轨迹，不等同于取得新的环境观察，但直接覆盖“继续阅读能否解决”的竞争解释。
- [Formal Policy Enforcement for Agentic Systems（PCAS）](https://arxiv.org/abs/2602.16708)：依据当前状态和历史事件，在工具动作执行前判断政策违规；依赖显式 Datalog 政策和事件图，与冻结语言模型通过少量查询消解事实歧义不同。

```json
{
  "score": 7.0,
  "contribution_scores": {"importance": 8.0, "novelty": 6.0, "effectiveness": 6.0},
  "contribution_assessment": "主贡献是用解释分歧驱动的一两次环境查询改善实际违规召回。若自然完整队列在同误报与总预算下稳定提高至少10个百分点，重要性达到8；主动审查和对话外取证已有先例，新颖度为6的明确增量。自然轨迹与快照控制支持有限信息价值结论，但单查询ReAct对两查询方案及缺失同任务强hybrid文本对照，使有效性目前为6；仅一项达到8，贡献门槛未通过。",
  "feasibility": "fail",
  "feasibility_reason": "MRT公开数据、CPU模拟工具和监控入口使组件实现可信；但当前最小实验给普通ReAct一次查询、本方案最多两次，与同查询配额声明不符，属于审查标准要求阻断的基线条件不匹配。API模型及报价未定，千元内完成也尚未核定。",
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "贡献门槛未通过：importance=8、novelty=6、effectiveness=6，仅一个维度达到8。",
    "普通ReAct仅一次查询、本方案最多两次，不能将收益归因于解释分歧驱动的查询选择；按本次审查标准构成基线条件不匹配阻断。",
    "同任务已有公开且更强的MRT hybrid，但主比较仅使用sequential追加文本阅读，尚不能支持相对强文本监控的实质价值Claim。"
  ],
  "novelty_conclusion": "存在明确但有限的增量：两解释分歧驱动的少量环境查询与公开等预算验证。Arbiter已覆盖预算式主动审查，OpenAI 2026-10-29系统已覆盖对话外证据调查，因此主动取证或独立环境事实本身不能作为主要新颖点。",
  "closest_neighbors": [
    "Reliable Weak-to-Strong Monitoring of LLM Agents",
    "The Arbiter Agent: Continually Monitoring Multi-Agent Conversations to Detect Emergent Misalignment",
    "How we detect frontier model misalignment",
    "TRACE: Trajectory Reasoning through Adaptive Cross-Step Evidence Aggregation for LLM Agents",
    "Formal Policy Enforcement for Agentic Systems"
  ]
}
```