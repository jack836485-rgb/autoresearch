## 结论

2026-11-03：总体 **6.5/10**，**promising_needs_revision**。若关键结果成立，新增的是一种用同任务影子阳性对照选择重读方式的外部诊断信号；这有研究价值，但当前证据尚未支持它能识别分块相对全文复读的获益条件，且与已有 context canary 和自适应路由相比，贡献尚不足以达到本轮门槛。

## Claim 判断

| 维度 | 分数 | 依据 |
|---|---:|---|
| 重要性 | 7.0 | 长转录漏检是实在的监控瓶颈；若在同预算、同整轨迹 FPR 下胜过最强固定策略，方法值得使用。但当前主贡献是两种既有重读方式的选择器，单模型、合成长输入压力测试尚不足以支撑对重要监控判断的实质改变。 |
| 新颖度 | 7.0 | 隔离影子中的同任务阳性片段、只提取其检出结果，具有可辨认的新意；然而以易核验 canary 诊断上下文退化及以诊断信号路由计算均已有先例。独立增量集中在“该对照是否能指导真实攻击监控的重读选择”，尚不是已成立的新机制。 |
| 有效性 | 5.5 | 当前证据支持长输入会让监控器漏掉已存在、甚至明显的危险动作，也支持缩短阅读范围可能改善检测；这些条件使阳性对照成为合理候选信号。但尚无证据说明随机位置、自包含片段的失败会在控制长度、位置和首轮分数后迁移到另一种攻击，更没有证据连接到分块相对全文复读的收益。后一条件是方法优于固定策略所必需的，不能由“能预测漏检”代替。 |

这是向工具 agent 转录迁移后的邻近子问题：研究可观察证据的利用失败，不回答真实奖励失配训练如何改变 CoT 中的信息及其与长度的交互。

最小实验的主要判别方向是对的：最终只计原日志的判断，攻击/良性配对可以评估整轨迹 ROC，按原攻击分组能够避免把变体当独立样本。它原则上能检验等预算下的实际召回收益；但影子漏检与真实漏检的相关性本身不能证明分流价值，真正决定主张的是它是否对应两条重读路径不同的收益。40 个攻击组上的结果只能支持所声明的有限压力测试，10% FPR 的宽区间不能解释成可靠低误报部署收益。

**可行性：fail（针对当前写定的协议）。** 数据与模型不存在已知获取障碍：[官方 README](https://github.com/safety-research/sleight-bench#decrypting-attack-data)公开解密路径，数据是人工设计并由 AI 辅助构造的攻击/良性转录，而非真实奖励训练 rollout；40 个攻击含三个双阶段攻击，合计 43 条攻击转录，阶段不能被默认为独立攻击组。[格式规范](https://raw.githubusercontent.com/safety-research/sleight-bench/main/FORMAT.md)提供工具动作 ID 与分离的机制 metadata，足以建立标签隔离和对照定位；标签表达构造的恶意行为，不是运行本实验后测得的攻击成功率。[公开配置](https://huggingface.co/openai/gpt-oss-20b/raw/main/config.json)的上下文上限确为 131072，64K 输入有实现路径，冻结推理在所给 GPU 资源上具有可信执行路线，尚不能据此确认耗时。

具体阻断是预算算术：原文长 L、插入片段长 s>0 时，首轮全文、影子全文、末轮完整全文或四块合计分别至少消耗 L、L+s、L，总计 **3L+s>3L**，还未计提示和对照构建。故写定方法不能同时完成所述三阶段并遵守每条最多 3L 输入；这使当前“同预算”主 Claim 无法按原协议检验。它是具体协议冲突，不是要求先跑 pilot，也不是缺少公开代码。

## 最高近邻

- [Classifier Context Rot: Monitor Performance Degrades with Context Length](https://arxiv.org/html/2605.12366v1)：已研究插入恶意动作、长度/位置退化及增量监控、提醒等缓解。本文尚可能新增的部分是把独立影子对照的结果作为逐轨迹路由信号，而非再次证明长输入漏检。
- [SLEIGHT-Bench: A Benchmark of Evasion Attacks Against Agent Monitors](https://arxiv.org/html/2605.16626v2)：覆盖同一监控任务、攻击/良性配对和提示式监控，是数据与评分协议的直接近邻；没有给出本方案的影子对照路由。工具式 coding monitor 是另一能力设置，不能强制当作这里的等能力 baseline。
- [Claude Context Canary](https://github.com/mkmkkkkk/claude-context-canary)：公开 README 和脚本用易核验 canary 指令失效诊断 context rot，并提示 compact/clear；因此“外加已知对照监测上下文健康”并非全新。它没有隔离影子、同任务恶意片段，也没有等 FPR、等预算的真实攻击召回验证，其可靠性宣传不能当成实验依据。
- [Retrieval Augmented Generation or Long-Context LLMs? A Comprehensive Study and Hybrid Approach](https://arxiv.org/html/2407.16833v2)：Self-Route 已按模型自省在局部检索与长上下文路径间分配预算。它限制路由框架本身的新意，但属于 QA 跨域启发，不能直接替代同监控任务的强 baseline。
- [CoRefine: Confidence-Guided Self-Refinement for Adaptive Test-Time Compute](https://arxiv.org/html/2602.08948v1)：已用置信动态控制停止、复查及换路径；与预算选择机制重叠。其训练控制器、推理任务和 token 置信信号均不同，不能把它的收益外推为本方案阳性对照有效的证据。

```json
{
  "score": 6.5,
  "contribution_scores": {"importance": 7.0, "novelty": 7.0, "effectiveness": 5.5},
  "contribution_assessment": "主贡献是以隔离影子中的同任务阳性对照选择分块或全文重读。若同预算同整轨迹FPR下胜过最强固定策略则值得使用，但当前重要性和新意均未达到8分；已有长上下文漏检及缓解证据尚未连接到对照对另一攻击的预测，更未连接到两条重读路径的条件收益差异。",
  "feasibility": "fail",
  "feasibility_reason": "数据有公开解密路线、动作ID和独立metadata，模型上下文与GPU资源支持冻结推理；但原日志L加影子L+s再加完整重读L至少为3L+s，无法执行当前每条最多3L的三阶段协议。",
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "贡献三维门槛未满足：重要性7.0、新颖度7.0、有效性5.5；当前证据未支持对照信号能识别分块相对全文复读的获益条件。",
    "严格3L输入预算与原文全文、插入阳性片段后的影子全文、完整重读的三阶段协议冲突，阻断当前同预算主Claim的检验。"
  ],
  "novelty_conclusion": "未发现完全相同的隔离影子同任务阳性对照路由方法；但context canary诊断和诊断驱动计算路由已有先例，独立新意应落在其对真实监控重读收益的预测，而非对照或路由概念本身。",
  "closest_neighbors": [
    "Classifier Context Rot: Monitor Performance Degrades with Context Length",
    "SLEIGHT-Bench: A Benchmark of Evasion Attacks Against Agent Monitors",
    "Claude Context Canary",
    "Retrieval Augmented Generation or Long-Context LLMs? A Comprehensive Study and Hybrid Approach",
    "CoRefine: Confidence-Guided Self-Refinement for Adaptive Test-Time Compute"
  ]
}
```

