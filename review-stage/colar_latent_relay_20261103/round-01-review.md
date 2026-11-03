## 结论
2026-11-03，总体 score 5.3，verdict：promising_needs_revision。主贡献是在 CoLaR 上用"只改监督版式"的受控变体，把"答案读链尾、生成只看近窗"拆成"监督版式继承"和"latent 特有的短窗接力"两部分。这个贡献目前不够：H1 几乎可以从 CoLaR 的逐块监督目标直接推出，信息增量小；H2 有价值，但 V2 的下降受训练难度、分块对齐和总长度混杂，而且作者自己的依赖距离反证与"每跳都有代价"的预测相冲突；"attention 和置零结论需要匹配对照才能当机制证据"这条方法论，已由 2606.12689 在同底座、同数据上系统确立。

## Claim 判断
| 维度 | 分数 | 依据 |
|---|---|---|
| 重要性 | 5.5 | 范围是单一方法（CoLaR-1B、CF5）、单一数据（GSM8K-Aug）上两个签名的来源。"影响 latent 链长和压缩设计"只是断言，没有设计层面的检验。"不能把注意力或置零当机制证据"的一般结论已被 2606.12689 用 matched controls 确立，本工作只是在 CoLaR 上补一个具体实例。真正值得知道的是 H2：CoLaR 是否局部接力。这与 2602.08783 在 Coconut/CODI 上发现的"skip 主导、非局部"相反，能澄清一个分歧，但影响面有限。 |
| 新颖度 | 6.0 | 已检索到的工作都没有用"改监督版式（插入无信息填充）"作为因果把手，在 CoLaR 上定位读出位置和生成窗口。推理时窗口掩码作为"有效窗口"的因果测法，在 latent CoT 上也未见先例。但 2606.12689 的 curriculum-perturbed 和 pause-as-thought 对照属于同一思路（改训练来判别模式是否机制特有）；2602.08783 已与显式 CoT 比较 locality/span；SIM-CoT 也已观察到答案出现在最后一个中间步之后、尾部 latent 重复答案。所以新意是可辨认的增量，没有达到独立的新机制或新视角。 |
| 有效性 | 5.0 | 现有依据：两个 checkpoint（EQ/NL 同源）上的注意力占比、链尾联合置零崩塌，以及单方法 Coconut 的节奏对齐，都是观察性的或离流形的。作者已承认这些证据分不开两种解释。H1：CoLaR 第 i 个 latent 被监督去预测第 i 块压缩 token，填充移位后关键 latent 跟着最后算式移动几乎是训练目标的直接结果，成立了也很少改变判断。H2：只有注意力描述，缺少因果依据；反证材料里"固定步数后长依赖题与局部依赖题正确率无差异"，恰恰与"短窗接力、每跳付代价"的预测相冲突（远依赖需要更多跳接力），brief 没有解释这一点。从 Coconut/CODI 的结论迁移到 CoLaR 也有反向证据：2602.08783 发现的是非局部。 |

与起点问题的关系：回答的就是原问题，没有转向。没有回答的部分是：结论能否推广到 CoLaR 以外的范式；"接力"是否就是失败原因；长度和压缩设计层面的含义。

实验能否判别主张：只能部分判别。
(1) V2 相对 V0 下降有多种解释：训练难度上升、5-token 分块与算式边界的对齐改变、总长度增加，都能产生同样的下降，不一定是"跳数代价"。V1 的填充位置不同，而且在读出路径上也加了跳数，不能充当干净的长度对照。只用 2 个种子判断"超出种子波动"也很弱。
(2) 推理时窗口掩码和删除填充尾部都改变了位置和注意力分布，属于离分布干预。W≤3 下保留率高只能说明充分，不能说明"只用近窗"。显式 CoT 用 5W token 对应 W 个 latent，信息密度并不等价。
(3) 实验没有产出"拆分"的量化份额，H1 和 H2 是两个独立检验，不能支撑"因果拆分"这一主张。
(4) 依赖距离反证没有纳入判据。

可行性：pass。GSM8K-Aug 的 `steps` 字段可以离线拼接填充，无需标注。6 个 CoLaR run 按已有日志估算，在 8×A100 上 2–3 天，符合 5 天约束。2602.08783 的代码已核实公开（github.com/J1mL1/causal-latent-cot，ICML 2026），但它面向 Coconut/CODI，用到 CoLaR 上需要改写接口。CODI Llama-1B 权重本审未能独立访问 HF 核实，以服务器已有为准。窗口掩码和置零都只是推理时改 attention mask，实现可信。

## 最高近邻
1. Dynamics Within Latent Chain-of-Thought: An Empirical Study of Causal Structure（arXiv 2602.08783，ICML 2026）https://arxiv.org/abs/2602.08783 。重叠：逐步 do-intervention、locality/span 指标、与显式 CoT 对比。差别：只研究 Coconut/CODI，没有操控监督；结论是 latent 非局部、skip 主导，与本 brief 的 CoLaR 局部接力相反。
2. Observable Patterns Are Not Explanations: A Causal-Geometric Analysis of Latent Reasoning Models（arXiv 2606.12689）https://arxiv.org/abs/2606.12689 。重叠：GSM8K-Aug、Llama-3.2-1B，用 curriculum 和 recurrence 的 matched controls 证明注意力和解码模式不能当机制证据，并分析了边界 token 的注意力质量。差别：不含 CoLaR，没有改监督版式，也不研究窗口和链尾。
3. How Do Latent Reasoning Methods Perform Under Weak and Strong Supervision?（arXiv 2602.22441）https://arxiv.org/abs/2602.22441 。重叠：把 CoLaR 当作强监督代表，发现它对 latent 步数最敏感，确实依赖 latent。差别：不研究位置功能来自版式还是机制。
4. SIM-CoT: Supervised Implicit Chain-of-Thought（arXiv 2509.20317）https://arxiv.org/abs/2509.20317 。重叠：逐步监督的 latent 与 CoT 步对齐，答案出现在最后一个中间步之后、尾部重复答案，这部分预示了 H1。差别：属于观察性分析，没有因果操控。
5. Do Latent Tokens Think? A Causal and Adversarial Analysis of Chain-of-Continuous-Thought（arXiv 2512.21711，EMNLP 2026）https://arxiv.org/abs/2512.21711 。重叠：用扰动测试 latent 的因果作用。差别：研究对象是 Coconut，结论是 latent 起占位符作用，不涉及窗口或版式。

```json
{
  "score": 5.3,
  "contribution_scores": {"importance": 5.5, "novelty": 6.0, "effectiveness": 5.0},
  "contribution_assessment": "主贡献是用改监督版式（V1/V2 填充）在 CoLaR 上把链尾读出和近窗生成拆成版式继承与 latent 短窗接力。重要性有限：单方法单数据，设计层面的含义只是断言；'注意力和置零需要匹配对照'已由 2606.12689 确立。新颖度是增量：版式操控加推理时窗口掩码作为因果把手未见先例，但 matched-control 思路已有。有效性不足：H1 几乎由 CoLaR 逐块监督目标直接推出；H2 只有注意力依据，且与作者自己的依赖距离零差异反证冲突，又与 2602.08783 在 Coconut/CODI 上发现的非局部结论相反。待验证：V2 下降能否与训练难度、分块对齐、总长度分开；窗口掩码作为离分布干预的解释边界。",
  "feasibility": "pass",
  "feasibility_reason": "GSM8K-Aug 的 steps 字段可离线拼接填充；6 个 CoLaR run 在 8xA100 上约 2-3 天，符合 5 天约束；窗口掩码和置零只需推理时改 attention mask；2602.08783 代码已核实公开，但用到 CoLaR 需改写接口；CODI-1B 权重本审未能独立核实。",
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "贡献门槛未达：三项无一达到 8，主贡献分量不足以支撑主会论文",
    "H1 的预测几乎由 CoLaR 逐块压缩监督目标直接蕴含，成立也不改变判断，'因果拆分'的一半信息增量很低",
    "Claim 阻断：V2 相对 V0 的下降无法与训练难度、5-token 分块对齐变化、总长度增加分开；V1 填充在读出路径上也加了跳数，不能作为干净的长度对照；2 个种子不足以判断'超出种子波动'",
    "H2 '每跳都有代价'与 brief 自己的依赖距离零差异反证相冲突，brief 未解释，也未纳入判据",
    "'决定 latent 链长和压缩设计'的含义没有任何实验检验，属于无支撑的外推"
  ],
  "novelty_conclusion": "没有找到在 CoLaR 上用改监督版式加推理时窗口掩码做因果判别的先例，但 2606.12689 已用 matched controls 确立了'观察模式不是解释'这一一般结论，2602.08783 已给出 locality/span 和显式 CoT 对比，SIM-CoT 已观察到答案位于最后中间步之后。新意属于可辨认的增量，不是独立的新机制或新视角。",
  "closest_neighbors": [
    "Dynamics Within Latent Chain-of-Thought: An Empirical Study of Causal Structure (arXiv 2602.08783)",
    "Observable Patterns Are Not Explanations: A Causal-Geometric Analysis of Latent Reasoning Models (arXiv 2606.12689)",
    "How Do Latent Reasoning Methods Perform Under Weak and Strong Supervision? (arXiv 2602.22441)",
    "SIM-CoT: Supervised Implicit Chain-of-Thought (arXiv 2509.20317)",
    "Do Latent Tokens Think? A Causal and Adversarial Analysis of Chain-of-Continuous-Thought (arXiv 2512.21711)"
  ]
}
```
