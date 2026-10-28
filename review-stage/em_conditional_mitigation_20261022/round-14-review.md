## 结论

2026-10-27 评审：**score 7.0/10，verdict = promising_needs_revision**。

新颖性：没有检索到直接覆盖本 Idea 的工作。具体来说，没有工作对"缓解后仍存在的条件失配"做位置级因果定位（cue 句 K/V 修补，用同提示的等长中性句作对照），也没有工作在 cue 题上评测 TReFT。Piggyback 只用了无 cue 题；ContextLift 和 Dubiński 都没有机制实验；后门触发位置的修补属于跨领域工作。

但本 Idea 的方法是 Piggyback KV 修补的直接移植，贡献属于诊断型，增量有限。另外，Claim 3 的判别有缺陷：broad cue 失配只按提示分类，没有按回答分类。TReFT 在设计上本来就会让模型对领域语义作出窄域坏建议，所以 Claim 3 的"支持"结果可以由这种预期内的行为产生。现有设计分不开"条件广泛 EM"和"对顺带提及的话题作出窄域行为"。

Claim 1 的问题是新的，判定表可证伪，资源与 baseline 也可行。值得继续。

## Claim 判断

| Claim | 判断 | 最关键依据 |
|---|---|---|
| 背景："目前只有行为和数据统计层面的解释" | 部分不准 | Su et al.（2601.23081）自称给出条件安全失败的 mechanistic account（触发会激活 persona 表示）。EM Is Not Magical（2608.29118）用基座表示中"提示到训练数据质心的距离"预测提示扰动下的 evilness。不过"没有位置级因果证据"这一说法仍然成立。另外，"交织后通用题失配约 1–2%"与 ContextLift 主表的 1.9/2.9/5.6% 不符。 |
| 1 H-pos：cue 句基座 K/V 修补能消掉 ≥50% 的 cue 效应，且大于等长中性句修补 | 新颖（问题新，方法是移植） | Piggyback 只比较了模板 prefix 与整段 query 的修补，而且只在无 cue 题上。2503.04429 与 Lasnier（2602.10382）在显式后门触发词上做过位置级或头级修补，但属于跨领域。同提示等长中性句对照和穷尽判定表是本 Idea 自己的。弱点：H-read 只能从"r_cue 小"间接推出，没有正向检验，因为同提示的请求段和 postfix 修补不进入判定。 |
| 2 位置分离 | 部分重合 | EM-only 臂上"模板修补 > 中性句修补"基本是在复现 Piggyback 的 prefix > query。交织臂上的结论是 Claim 1 的直接推论，独立增量有限。 |
| 3 TReFT 把广泛 EM 转成条件 EM | 行为上新颖，但现设计无法检验 | 没有检索到 TReFT 在 cue 题上的评测：Piggyback 引用了 Dubiński 但没测，ContextLift 明说不比较改训练目标的防御。问题有两点：(1) TReFT 的设计目标就是把行为绑定到 query 内容的领域语义（Piggyback §5；表 3 显示正则 query 位置会阻止域内学习）；(2) ContextLift 附录 A 显示，cue 下的残余失配有 74–90% 是"对顺带提及的话题给出微调后的坏建议"。B 类只按提示分类，没有按回答分类，所以"TReFT 在 cue 题上降幅更小"可以完全来自它预期内的窄域行为。 |

## 最高近邻

1. **Piggyback / TReFT**（Zhao et al., 2606.06667）https://arxiv.org/abs/2606.06667
   - 重叠：同一套模板 KV 修补工具和 TReFT；也在 Qwen-2.5-7B 上报告了 prefix 承载。
   - 差别：只评测无 cue 题，没有细分 query 内部的 cue 句，也没有测 TReFT 在条件触发下的表现。
2. **ContextLift**（Mai & Kaczér, 2610.21633）https://arxiv.org/abs/2610.21633
   - 重叠：同模型、同数据、同一套 cue 题与 B 类划分；给出伪相关解释，并对残余回答做了分析。
   - 差别：没有任何表示层或位置级的因果实验。
3. **Conditional misalignment**（Dubiński et al., 2604.25891）https://arxiv.org/abs/2604.25891
   - 重叠：定义了条件失配，并证明稀释、后续良性微调和 inoculation 都会留下触发。
   - 差别：只有行为证据，不涉及 TReFT 和机制。
4. **Activation Space Interventions Can Be Transferred**（Oozeer et al., 2503.04429）https://arxiv.org/abs/2503.04429
   - 重叠：对触发位置加噪并做跨位置修补，定位后门（IHY 任务有效，代码漏洞任务无效）。
   - 差别：研究对象是显式人造触发词的后门，不是缓解后的语义条件 EM；只能作跨领域依据。
5. **Character as a Latent Variable**（Su et al., 2601.23081）https://arxiv.org/abs/2601.23081
   - 重叠：在表示层解释"触发如何激活失配 persona"，涵盖条件安全失败。
   - 差别：没有位置级修补，也不针对已缓解的模型。

```json
{
  "score": 7.0,
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "Claim 3 无法检验：broad cue 失配只按提示分类，没有在回答层区分'对 cue 话题给出窄域坏建议'与广泛失配（ContextLift 附录 A 显示残余以前者为主）。TReFT 在设计上就把行为绑定到 query 的领域语义，因此'TReFT 在 cue 题上降幅更小'可以由其预期内的窄域行为产生，不能证明它把广泛 EM 转成了条件 EM。"
  ],
  "novelty_conclusion": "没有检索到对缓解后条件失配做 cue 句位置级 KV 修补（带同提示等长中性句对照）的工作，也没有检索到在 cue 题上评测 TReFT 的工作，所以 Claim 1 的问题是新的。但方法是 Piggyback KV 修补的直接移植；Claim 2 一半是复现 Piggyback；Claim 3 在现设计下判别不清。背景中'只有行为与数据层面解释'的说法忽略了 Su et al. 与 EM Is Not Magical 的表示层解释。新颖性边界基本清楚，但贡献幅度偏小，Claim 3 的判别仍需解决。",
  "closest_neighbors": [
    "The Piggyback Hypothesis of Generalization: Explaining and Mitigating Emergent Misalignment (2606.06667)",
    "ContextLift: Breaking the Spurious Correlation Behind Conditional Emergent Misalignment (2610.21633)",
    "Conditional misalignment: common interventions can hide emergent misalignment behind contextual triggers (2604.25891)",
    "Activation Space Interventions Can Be Transferred Between Large Language Models (2503.04429)",
    "Character as a Latent Variable in Large Language Models: A Mechanistic Account of Emergent Misalignment and Conditional Safety Failures (2601.23081)"
  ]
}
```
