## 结论

2026-11-03：总体 **6.8/10**，**promising_needs_revision**。主贡献是用隔离的已知违规探针预测“分块重读相对全文复读”的净收益；它具有可辨认的新意和可信验证路线，但目前主要是已有上下文金丝雀与监督计算路由之间的具体连接，其独立贡献分量尚不足以达到两个8分的放行门槛。

## Claim 判断

| 维度 | 分数 | 判断依据 |
|---|---:|---|
| 重要性 | 7.0 | 若结果成立，会新增一种值得使用的监控诊断：外部阳性对照可帮助决定怎样重读，而不只是提示模型可能出错。预算受限的长日志监控值得研究；但当前主张限定于一个20B监控器、两种重读动作及小规模合成长日志，尚不足以支持对重要监控瓶颈的实质改变。 |
| 新颖度 | 7.0 | 已有系统用金丝雀触发上下文干预，已有方法按预测动作效果分配计算；这里用任务内违规探针的响应预测两动作的配对收益，仍是可辨认的增量。未查到完全相同的方法，但“外部诊断特征＋监督动作选择”目前没有呈现足够独立的机制或发现，不能仅因没有同名近邻就给8分。 |
| 有效性 | 6.0 | 当前依据支持长上下文会漏检、缩短或多次读取有时能改善、响应信号可以参与计算选择；这些条件确实与本任务相邻。但它们尚不支持单个已知违规片段的检出响应，能在长度和首轮分数之外预测两种重读的收益差。尤其明显违规的可检出性与需要跨步状态推理的真实违规并不等价；Context Rot本身也报告简单针状任务的改进不能可靠迁移到更微妙的监控任务。收益异质性、探针的额外预测力及其是否覆盖探针成本仍未知。 |

该工作回答起点的邻近子问题“已有日志证据如何有效读取”，不回答奖励设定错误造成的信息缺失，也未回答原卡两个因素的交互；转向本身不构成否决理由。

最小实验**原则上能判别收窄后的核心主张**：真实运行两种后续动作形成配对目标，留出攻击组比较无影子同类路由、响应置乱和固定策略，并把节省的探针额度交还基线，能够区分“只识别难例”与“提供动作收益增量”。40个攻击组的宽区间限制可估计效果的精度，但已经明确不以填充版本冒充独立样本，也不声称可靠1% FPR；这不是实验不可行的理由。公平设计提高可解释性，不能替代探针有效的当前证据。

**可行性：pass。** 我核验了公开解密脚本和一个实际加密样本：确有攻击、成对良性JSONL与机制metadata，标签可用于合成转录的违规检出及误报，不能解释为真实策略训练后的行为成功率。当前仓库实际有44个加密转录目录，比brief的43条多一条，故其40组数字对应的是需明确冻结的旧子集，而非当前全仓库；这不阻断数据获取。[公开数据与解密路径](https://github.com/safety-research/sleight-bench)可用，ControlArena提示也在原论文附录公开。32K/64K输入在[官方131072上下文配置](https://huggingface.co/openai/gpt-oss-20b/raw/main/config.json)内；浅树训练与数亿输入token的冻结推理在8×A100、约5天约束下有可信路线，具体吞吐和重复次数仍待实施阶段确定。这里的主要阻断是贡献门槛未达，而非缺代码、数据或预算。

## 最高近邻

- [Claude Context Canary](https://github.com/mkmkkkkk/claude-context-canary)：通过可校验指令遵守情况诊断上下文退化，并建议compact/clear。它已覆盖“外部金丝雀指示上下文健康并关联后续干预”的基本想法；本方案的差别是任务内违规对照与两种重读净收益的监督联系，该仓库未提供这种联系的受控效果证据。
- [Confidence-Guided Self-Refinement（CoRefine）](https://arxiv.org/html/2602.08948v1)：学习响应特征到HALT/RETHINK/ALTERNATIVE的动作控制，部分标签来自实际后续结果、部分来自启发式。它覆盖“预测该采取哪种计算动作”的主框架；本方案新增外部阳性探针，并直接采集两种重读的配对结果。
- [Classifier Context Rot: Monitor Performance Degrades with Context Length](https://arxiv.org/html/2605.12366v1)：直接研究同类长日志监控，已给出增量监控、可疑动作列举及提醒的改进和迁移局限。它支撑问题真实性与重读的潜在空间，但没有用探针响应预测个体重读收益。
- [Retrieval Augmented Generation or Long-Context LLMs? A Comprehensive Study and Hybrid Approach（Self-Route）](https://arxiv.org/html/2407.16833v2)：用模型自我反思在RAG与全文处理之间路由，覆盖按输入选择不同上下文读取方式；任务是问答，既无已知违规对照，也不构成本任务必须照搬的性能基线。
- [SLEIGHT-Bench: A Benchmark of Evasion Attacks Against Agent Monitors](https://arxiv.org/html/2605.16626v1)：相同监控任务与数据来源，已有针对性提示、重复试验及代理式监控。其公开ControlArena提示可复现；代理式监控使用工具和不同预算，不能直接拿论文分数作为本方案同预算基线。

```json
{
  "score": 6.8,
  "contribution_scores": {"importance": 7.0, "novelty": 7.0, "effectiveness": 6.0},
  "contribution_assessment": "若关键结果成立，将新增外部违规阳性探针对监控重读动作收益的诊断用途。长日志漏检及计算选择具有适用的邻近依据，但具体探针能否预测分块与全文的收益差仍未知。相较已有金丝雀和监督动作路由有可辨认增量，目前独立机制与作用范围尚不足以达到两个8分。",
  "feasibility": "pass",
  "feasibility_reason": "公开解密脚本及实际样本确认攻击、成对良性转录和机制metadata可获取；公开提示、131072上下文的冻结20B模型及浅树实现均可获得。数亿输入token在8×A100约5天内有可信实施路线，吞吐与重复数仍待确定。当前仓库44个加密目录与brief43条不一致，需冻结明确子集，但不构成数据不可得。",
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "贡献门槛未达：重要性7.0、新颖度7.0、有效性6.0，未有两项达到8；当前可检验的外部探针增量仍不足以确立目标主会所需的独立贡献分量。"
  ],
  "novelty_conclusion": "未查到完全相同的任务内阳性探针与配对重读收益路由；但上下文金丝雀关联干预、监督计算动作控制和长上下文读取路由均已有，当前为可辨认但尚未充分独立的增量。",
  "closest_neighbors": [
    "Claude Context Canary",
    "Confidence-Guided Self-Refinement",
    "Classifier Context Rot: Monitor Performance Degrades with Context Length",
    "Retrieval Augmented Generation or Long-Context LLMs? A Comprehensive Study and Hybrid Approach",
    "SLEIGHT-Bench: A Benchmark of Evasion Attacks Against Agent Monitors"
  ]
}
```
