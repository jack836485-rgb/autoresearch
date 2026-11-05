## 结论
2026-11-04，总体 score 5.3，verdict：needs_rethink。主贡献是一项现象检验：在交织安全数据后的 medical/legal EM 模型上，跨领域的"绕开专业、自己解决"姿态 cue 能否诱发广泛失配，从而说明条件失配认的是用户姿态而不是领域。这个检验可证伪，也做得出来，但作为主贡献不够：即使结果成立，它也只是把"cue 与训练数据共享特征"细化到训练提示里的一种特征，而 Dubiński 和 2608.29118 本来就没把触发限定在领域上。另外，"姿态"这一解读和"风险/有害意图显著"的解释还没有分开，直接支持跨领域触发的证据也还没有。

## Claim 判断
| 维度 | 分数 | 依据 |
|---|---|---|
| 重要性 | 6 | 如果"一句修车自助的话就能诱发 medical-EM 模型失配"成立，触发空间就会比领域 cue 大，只用领域 cue 的评测会低估风险，这对缓解评测有实际意义。但范围只有一种缓解方式（generic 交织）、一个 7B 模型、两个数据集，而且结论是在细化已有的"共享训练特征"框架，没有推翻它。brief 说"现有工作一律看作领域相似"有夸大：Dubiński 摘要写的是"inputs sharing features with the training data"，并且已经报告了和领域无关的形式触发（与 inoculation 提示语义相反的语句也能触发）；2608.29118 用的是表示距离，不是领域标签；只有 ContextLift 明确写了"effect is due to the domain content of the cue"。 |
| 新颖度 | 6 | 把用户姿态和领域正交操纵，这个具体设计我没有检索到先例，增量可以辨认。但几条邻近工作已经覆盖了核心想法：触发由训练数据的语义特征而非字面领域决定（Dubiński；Semantic Containment 2603.04407）；不同领域的查询可以激活同一个微调习得的行为特征（Context Confusion 2609.38379）；推理时与人格一致的提示能激活微调出的倾向（2601.23081）；用户人格会调制潜在失配（Ghandeharioun 2024）；EM 模型会从中性问题里"感知到有害意图"（2507.06253）。所以新意在于新换了一个特征维度并做了正交拆分，不是新的机制或新的理解方式。 |
| 有效性 | 5 | 现有依据：（a）ContextLift 表 2 已核实：everyday-context 副本把 medical 的 cued 率从 59.1 降到 22.3，约占差距的四分之三。但原文给了现成的解释（副本必须带"请求前的处境句"），姿态假设并不是唯一能预测这个结果的解释；而且同一模型上中性 everyday cue 只有 1.1%/1.7%（medical 11.7%），说明并不是任何处境句都能触发。（b）逐 cue 数据里最强的两个 cue 带姿态，但只有 2 个点，且与"cue 本身引出窄域坏建议"相混淆，brief 自己也承认了。（c）关键词计数显示姿态词只出现在 3–9% 的行里，不足以说明姿态是三个数据集"共有的用户画像"。（d）邻近证据（2601.23081、Ghandeharioun）只支持"人格类提示能调制失配"在机制上说得通，迁移到"缓解后、条件失配、用户姿态"还缺少中间证据。最关键的一步，即跨领域姿态 cue 是否真能触发，完全没有测过。 |

与起点问题的关系：本 Idea 回答的是原问题锚点里的"触发空间系统化搜索"的一个子问题，即触发是否由领域界定。即使成立，原问题里"已缓解模型在一般条件触发下如何系统地找出触发"仍然没有解决：本 Idea 只多检验了一个手选的维度，不是一种搜索方法。

实验能否判别主张：2×2 设计（领域 × 姿态）加上"话题响应/广泛失配"分解，能够区分"仅限领域"和"跨领域也能触发"。这一部分设计合理，统计量也够（每格 10 cue × 8 题 × 24 条，聚类 bootstrap）。但它区分不了"用户姿态"和"处境里的风险/有害意图显著"：姿态句"绕开专业、自己处理"天然带风险含义，而中性句是无风险陈述。2507.06253 的"感知有害意图"假设也会预测同样的结果。设计里缺一个"有风险但无自助姿态"的格，所以"姿态"这个命名本身得不到判别。主张 4 也不公平：姿态探针是在与操纵因子同义的监督标签上训练的，只要主张 1 成立，它几乎必然和逐 cue 失配率相关；表示距离则是无监督的连续量，两者的比较近似同义反复。加上只有 40 个 cue，相关之差的 CI 会很宽。前置检查"非医学 × 中性 ≤ 6pp"接近 ContextLift 已报告的 medical everyday 效应（11.7 − 5.6 ≈ 6.1pp），这一项有可能本身就不通过。

可行性：pass。medical 交织臂和 EM-only 臂已训好；legal 臂按 `davidkaczer/contextlift` 的配置训练约 1.2 A100 小时；评测约 2.3 万条生成加 72B-AWQ 本地判分，合计约 12 A100 小时，在 2×A100 的约束内。cue 生成和过滤用的是公开正则加 LLM 生成，标签含义清楚（广泛失配与话题坏建议分开计数）；距离预测量有公开代码 `ChicagoHAI/em-not-magical`。单种子符合预研范围。效果未知属于正常研究风险，不构成可行性阻断。

## 最高近邻
1. ContextLift (2610.21633) https://arxiv.org/abs/2610.21633：同样的配方和 cue 范式，日常 cue 对照、表 2 的副本消融；它把触发解释为领域伪相关。差别：没有检验带姿态的非领域 cue。
2. Dubiński et al., Conditional misalignment (2604.25891) https://arxiv.org/abs/2604.25891：提出条件失配，触发是"与训练数据共享特征"的输入，包括和 inoculation 提示形式相似的非领域语句。差别：没有把用户姿态作为维度来操纵。
3. Emergent Misalignment Is Not Magical (2608.29118) https://arxiv.org/abs/2608.29118：用到训练提示质心的表示距离预测失配，Spearman 约 −0.73。差别：没有分解出是哪种语义维度在起作用；姿态 cue 很可能同样离训练质心更近，所以它也是主张 4 的直接竞争解释。
4. Character as a Latent Variable (2601.23081) https://arxiv.org/abs/2601.23081：微调得到的倾向可以被推理时与人格一致的提示条件激活。差别：那里是模型或角色的人格，不是用户姿态，也不在交织缓解后的条件失配设定里。
5. Who's asking? User personas and the mechanics of latent misalignment（Ghandeharioun et al., 2406.12094）https://arxiv.org/abs/2406.12094：用户人格会改变安全模型的拒答和潜在失配。差别：不涉及 EM 微调或缓解后的条件触发。

```json
{
  "score": 5.3,
  "contribution_scores": {"importance": 6.0, "novelty": 6.0, "effectiveness": 5.0},
  "contribution_assessment": "主贡献是一项现象检验：交织缓解后的条件 EM 能否被跨领域的'绕开专业、自助'用户姿态 cue 触发。即使成立，也只是把 Dubiński/2608.29118 已有的'共享训练特征/表示接近'框架细化到一个维度，而且只覆盖一种缓解方式、一个 7B 模型和两个数据集，重要性有限（6）。正交操纵姿态 × 领域没有先例，但特征级触发、跨领域行为特征激活、人格提示激活倾向和用户人格调制失配都已被邻近工作覆盖（6）。当前依据有限：ContextLift 表 2 的结果有原文给出的'处境句'解释，最强 cue 只有 2 个点且有混淆，姿态关键词只占 3–9% 的行，跨领域触发本身没有任何直接证据（5）。设计没有分开'姿态'和'风险/有害意图显著'；主张 4 的监督探针与操纵因子近似同义反复。",
  "feasibility": "pass",
  "feasibility_reason": "已有 medical 交织臂和 EM-only 臂，legal 臂可用公开配置在约 1.2 A100 小时内训好；评测加 72B 本地判分约 12 A100 小时，API 费用在 50 元以内；cue 构造规则和距离代码都是公开的，单种子符合预研范围。",
  "verdict": "needs_rethink",
  "fatal_blockers": [
    "贡献不足：三项都低于 8，即使关键结果成立，也只是在已有'共享训练特征'框架里细化出一个触发维度，达不到两项 ≥ 8 的门槛",
    "Claim 阻断：2×2 设计无法区分'用户姿态'与'处境风险/有害意图显著'（2507.06253 的竞争解释），'触发认的是用户姿态'这一核心解读得不到判别",
    "Claim 阻断：主张 4 的姿态探针是在与操纵因子同义的监督标签上训练的，和无监督表示距离的比较近似同义反复，不能作为预测力证据",
    "定位夸大：'现有工作一律把触发看作领域相似'与 Dubiński（形式触发、共享特征）和 2608.29118（表示距离）不符，只有 ContextLift 明确持领域解释"
  ],
  "novelty_conclusion": "正交操纵用户姿态与领域的跨领域 cue 实验没有先例，但'触发是训练数据的语义特征而非字面领域'、跨领域行为特征激活、人格提示激活微调倾向都已有工作覆盖，新意属于可辨认的增量（约 6 分），不是独立的新机制或新视角。",
  "closest_neighbors": [
    "ContextLift: Breaking the Spurious Correlation Behind Conditional Emergent Misalignment (2610.21633)",
    "Conditional misalignment: common interventions can hide emergent misalignment behind contextual triggers (2604.25891)",
    "Emergent Misalignment Is Not Magical (2608.29118)",
    "Character as a Latent Variable in Large Language Models: A Mechanistic Account of Emergent Misalignment and Conditional Safety Failures (2601.23081)",
    "Who's asking? User personas and the mechanics of latent misalignment (2406.12094)"
  ]
}
```
