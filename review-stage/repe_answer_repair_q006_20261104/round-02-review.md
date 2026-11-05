## 结论

日期 2026-11-04。总体 score 5.5/10，verdict：**promising_needs_revision**。主贡献是一个可检验的判断：答案级 steering 的“修复 vs 只移动标签”分界取决于目标类型（不变性目标 vs 按实例权衡证据的目标）和干预形式（投影消融 vs 加性反推），而不是任务类别本身；已报道的分界可能来自单侧评测。这个问题值得研究，但目前贡献不足，原因有三：
- 主张 (1) 的“对称评测揭示加性 steering 只是先验偏移”，在谄媚与知识冲突上已有紧邻结果（双立场评测、persona 对 CAA 的对照、NQSwap steering 增加对误导上下文的脆弱性）。
- 主张 (2)“概念擦除实现不变性”在擦除文献中接近定义性结论，唯一的经验未知恰好有一个紧邻的反向信号。
- 主张 (3)“不存在线性修法”是全称否定，所列干预无法证成，并且漏掉了门控/条件 steering 这一同任务最强对手。

## Claim 判断

| 维度 | 分数 | 依据 |
|---|---|---|
| 重要性 | 6 | 澄清“何时 steering 是修复”，并给出干预前的修法选择规则，对 steering 评测有实际价值。但已报道的“成功”本身就小：2607.18114 的恢复率为 7–20%，同时只保证 ≥90% 的正确答案保持不变。按其公开数字，单侧净值已经很有限，所以“推翻成功”这一结论的分量有限。影响主要在可解释性/steering 子社区。 |
| 新颖度 | 5.5 | 有三点削弱新意：(a) 对称评测揭示 steering 同时压制“正确的同意”，已由 2606.11205 在谄媚上直接给出；2605.21006 报告 CAA 在用户正确时掉准确率；2602.06256 在 NQSwap 上报告 steering 后对误导上下文更脆弱。(b) “消融/擦除用于不变性”是 LEACE 与概念擦除的设计目标；SteeringControl 也已在多行为上对比过消融类（DIM/ACE）与加性类（CAA/PCA/LAT）的效果与纠缠，只是没有隔离单一变量。(c) 真正新的部分只剩一项组合：在同一方向、同一层位上隔离“加性 vs 投影消融”，并配上“线索指向正确答案”的孪生样本。它是可辨认的增量，算不上独立新现象。 |
| 有效性 | 5 | **现有依据：** 单侧评测已核实（2607.18114 丢弃了线索指向正确选项的样本，干预为加性，未做消融）；Arditi 等的拒答消融和 2605.05715 的 LEACE 擦除损伤（−3.6pp，随机 +0.3pp）支持“消融对需要计算的目标有害”。**适用性缺口：** 主张 (2) 依赖“线索方向只编码受线索影响，不编码线索所指的答案或与自身信念的冲突”。方向来自“线索全指向错误答案”的对比，很可能混入“与模型自身判断冲突”的成分。2606.11205 在 Llama-3-8B 上发现，谄媚同意与事实同意几何可分，但均值差方向在两者上的投影相当，这是对 (2) 的紧邻反向证据。主张 (3) 的消融预测（退回默认先验）在 2610.20067 的“选上下文 vs 选参数”方向上几乎由构造决定，不构成独立证据。**未知：** 方向成分、最佳层位、跨家族一致性。 |

**与起点问题的关系：** 本 brief 回答的是原问题，即分界变量是什么，并把它改写为目标类型 × 干预形式。原问题中推理类任务（工具决策、过度思考）的分界仍未覆盖，计算族只保留了 CRT。转向本身不是阻断。

**实验能否判别主张：**
- 主张 (1) 和 (2) 基本可判别。三联体加随机方向对照能区分“去除线索影响”与“推离线索所指答案”。但加性强度按单侧净增益选定，消融强度由样本投影决定，两者幅度不匹配可能单独解释破坏率差异。需要一个幅度匹配的加性对照（例如 α 取线索样本平均投影），否则 (1) 与 (2) 的对比有混淆。
- “破坏”的参照不一致：评测段以无线索作答为参照，Claim 段写作“放弃原本正确的答案”。线索正确但无线索答错的样本，在两种定义下计数相反，需要统一。
- 主张 (3) 不可判别：“不存在线性修法”需要排除门控/条件 steering。CAST 类条件 steering、探针门控、2608.29431 的 oracle 门控（目标族恢复 100%、无副作用）都是线性干预加输入相关门控，属于同类能力内的同任务强对手，brief 未纳入。即使所列四种干预都失败，也只能得出“这四种无效”。

**可行性：pass。**
- 算力：约 10 万次短前向，加约 1 万条限长 CoT，3 个 7–9B 模型，2×A100 一至两天可完成，远在预算内。
- 方法实现：投影消融与 LEACE 有标准实现；2607.18114 的代码路径已在原文给出。
- 数据：Suggested Answer 的“线索指向正确答案”孪生只需替换字母，可重建。Distractor Fact 的正确孪生需要新写一条支持正确答案的干扰事实，不是“只需替换选项”。这需要模板或 LLM 生成加抽检，覆盖率与标签质量要单独说明。
- 未能核实的来源：2610.20067、2611.04757 的原文本轮无法抓取，检索也未命中；MIST-Bench、Asymmetricity-2.0 的 HF 发布也未直接核实。这影响对选择性信任族数据与检索目标规则的复现判断，但不构成实现不可行。

**若关键结果成立，新增的东西：** 一个经验规则：对“输出不应随无证据线索变化”的目标，沿已报道方向做投影消融，比加性反推更接近修复；已报道的加性“成功”在对称评测下缩水。这对 steering 评测协议有用，但是否构成主会级独立贡献，取决于 (2) 在线索正确样本上确实几乎不破坏。这一点目前有反向信号。

## 最高近邻

1. **Dual-Stance Evaluation of Sycophancy**（2606.11205）https://arxiv.org/abs/2606.11205。重叠：提出对每个话题测两种立场的对称评测，发现均值差 steering 同时压制对正确陈述的同意，即主张 (1) 在谄媚上的直接版本。差别：只做加性 steering，未测投影消融，没有目标类型分界。
2. **Playing Devil's Advocate: Persona Vectors vs Targeted Steering for Sycophancy**（2605.21006）https://arxiv.org/abs/2605.21006。重叠：报告 CAA 在用户正确时损失准确率，persona 方向则能保持。差别：比较的是不同方向，不是同一方向上的加性 vs 消融。
3. **Steering Safely or Off a Cliff? Specificity and Robustness in ITI**（2602.06256）https://arxiv.org/abs/2602.06256。重叠：NQSwap 上的忠实性 steering 使模型对误导上下文更脆弱，相当于知识冲突一侧的“只是先验偏移”。差别：未做投影消融（只有 PartialOR），没有不变性/权衡分界。
4. **SteeringControl: Holistic Evaluation of Alignment Steering**（2509.13450）https://arxiv.org/abs/2509.13450。重叠：在多行为上对比消融类（DIM、ACE）与加性类（CAA、PCA、LAT）的效果与纠缠，含谄媚等次级行为。差别：方向生成、格式、位置同时变化，没有隔离“加性 vs 消融”，也没有对称孪生评测。
5. **How Does Alignment Tuning Shape Representations of Sycophancy and Cue-Induced Biases**（2607.18114）https://arxiv.org/abs/2607.18114。重叠：本 brief 的成功证据源，加性减去偏差方向，恢复 7–20%，保持 ≥90%。差别：丢弃了线索指向正确选项的样本，未做消融。去掉该文名字后，本工作的独立部分是对称三联体加消融对照。

另需检索核实：2610.20067、2611.04757（本轮无法抓取）；条件/门控 steering（CAST、GAPS 2609.01878 https://arxiv.org/abs/2609.01878）作为主张 (3) 的必要对手。

```json
{
  "score": 5.5,
  "contribution_scores": {"importance": 6.0, "novelty": 5.5, "effectiveness": 5.0},
  "contribution_assessment": "主贡献：'修复 vs 只移动标签'由目标类型（不变性 vs 按实例权衡）× 干预形式（投影消融 vs 加性）决定，已报道分界可能来自单侧评测。重要性 6：澄清 steering 何时修复有价值，但已报道的成功本身较小（2607.18114 恢复 7-20%、保持 ≥90%）。新颖度 5.5：对称评测揭示加性 steering 压制正确同意已由 2606.11205/2605.21006 给出，知识冲突侧有 2602.06256；擦除实现不变性是 LEACE 的设计目标；SteeringControl 已比较消融类与加性类；剩余新意是同方向同层位隔离加性 vs 消融并配线索正确孪生。有效性 5：主张 (2) 依赖方向不编码线索所指答案或冲突成分，2606.11205 显示谄媚方向在事实同意上投影相当，是紧邻反向信号；主张 (3) 的消融预测近乎由构造决定，'不存在线性修法'的全称否定未排除门控/条件 steering。另需幅度匹配的加性对照，并统一'破坏'参照。",
  "feasibility": "pass",
  "feasibility_reason": "约10万次短前向加约1万条限长CoT，3个7-9B模型，2×A100一至两天可完成；2607.18114 有公开代码，投影消融/LEACE 为标准实现；Suggested Answer 正确孪生可替换字母重建，Distractor Fact 正确孪生需新生成干扰事实并抽检；2610.20067、2611.04757、MIST-Bench、Asymmetricity-2.0 本轮未能直接核实，但不构成实现阻断。",
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "贡献门槛未达：三项为 6/5.5/5，没有两项 ≥8，新颖度与有效性低于 6",
    "主张 (1) 已被紧邻工作大部分覆盖：2606.11205 对谄媚做双立场评测，显示 steering 压制正确同意；2602.06256 显示忠实性 steering 增加对误导上下文的脆弱性",
    "主张 (3)'对按实例权衡的目标不存在线性修法'是全称否定，最小实验未纳入门控/条件 steering（CAST、探针门控、2608.29431 oracle 门控）这一同能力范围内的强对手，无法检验",
    "主张 (2) 的关键前提（方向不编码线索所指答案或冲突成分）有紧邻反向证据（2606.11205），当前依据只来自拒答消融与擦除的跨任务迁移"
  ],
  "novelty_conclusion": "对称评测揭示加性 steering 只是先验偏移，在谄媚与知识冲突上已有紧邻工作；擦除实现不变性是概念擦除的设计目标；消融类与加性类的效果/纠缠对比已有 SteeringControl。独立新意限于在同一方向、同一层位上隔离加性 vs 投影消融，并配线索正确孪生三联体，属可辨认的增量，不足 8 分。",
  "closest_neighbors": [
    "Dual-Stance Evaluation of Sycophancy: The Structure of Agreement and the Limits of Intervention (arXiv 2606.11205)",
    "Playing Devil's Advocate: Off-the-Shelf Persona Vectors Rival Targeted Steering for Sycophancy (arXiv 2605.21006)",
    "Steering Safely or Off a Cliff? Rethinking Specificity and Robustness in Inference-Time Interventions (arXiv 2602.06256)",
    "SteeringControl: Holistic Evaluation of Alignment Steering in LLMs (arXiv 2509.13450)",
    "How Does Alignment Tuning Shape Representations of Sycophancy and Related Cue-Induced Biases in LLMs? (arXiv 2607.18114)"
  ]
}
```
