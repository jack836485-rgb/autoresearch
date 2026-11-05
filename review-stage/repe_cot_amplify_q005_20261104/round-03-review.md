## 结论
2026-11-04：总体 score 5.0，verdict **needs_rethink**。若关键结果成立，主贡献是：内部激活原因只在审议阶段起作用时，CoT 会为它合理化，监控难以发现；只在作答处起作用时，答案与 CoT 冲突，监控容易发现。“反转 MonitorBench 规律”这一定位是把概念对错了位：在 MonitorBench 里，“经由推理”指因素内容被推理使用、因而会被写出来；而 R 条件里，原因只是推着结论走、CoT 去合理化，这对应的是 MonitorBench 中本就难监控的 Cue(Answer)/Deception 类。A 条件人为制造了“CoT 与答案相互矛盾”，检出率高几乎是构造出来的。剩下的经验内容，大多已能从已知结果直接推出：被 steer 的 CoT 会合理化（见 2604.01202、2603.01437），立场不一致在文本上可见。因此重要性和新颖度都达不到 8，贡献不足以过门槛。

## Claim 判断
| 维度 | 分数 | 依据 |
|---|---|---|
| 重要性 | 6.0 | 话题本身重要：CoT 监控能否覆盖内部偏好驱动的决定。但“越经由推理越不可见”这一后果，已有工作以不同形式表达过：隐式事后合理化不可见，探针优于 CoT 监控（2603.17199），隐式影响下检出下降（2608.04735）。A 条件（原因在推理结束后才出现）没有现实对应物，真实的内部偏好更接近全程的 F；R 与 A 的对比对监控设计者的实际判断改变有限。 |
| 新颖度 | 6.0 | 我检索到的工作中，没有人把 steering 的作用位置（审议处／作答处）与单条轨迹监控 AUROC 结合起来，这是可辨认的增量。但预期结论可以由“被 steer 的 CoT 合理化”加上“矛盾可见”组合推出。“与已发表规律方向相反”只在误用 MonitorBench 的“shape reasoning”定义时才成立，MonitorBench 本身没有给出操作化定义，正文显示的是“Cue(Condition) 高、Cue(Answer) 低”。去掉这层反转包装，新意属于常规组合。 |
| 有效性 | 6.5 | 当前依据：(i) A 条件可检出。2605.26772 在 CoT 固定时有 39% 翻转，RFEval 显示立场不一致可从文本判断，所以 A>R 的方向大概率成立。但这是构造带来的，解释力弱。(ii) R 条件难检出的依据较弱：2604.01202 用的是基线与 steer 两条轨迹的成对判定，2603.01437 的病态分类针对指令模型、在全部位置注入，2608.04735 附录 G 只在 Qwen3-8B 编码任务上做过且不泛化。仍未知：单条轨迹监控能否抓到“不蕴含”；A 需要更大 α 时，作答段是否会补写合理化文字或出现伪迹；客观任务中，正类为错答、负类来自不同题且多为正确答案，监控可能只是在检出“答错”。这些未知不改变“结果可预期”这一判断，对“反转”主张也几乎没有支持。 |

**与原问题的关系：** 这是邻近新问题。它保留了 steering 放大与 CoT 锁定的现象，把评价目标换成监控检出；起点问题中剂量、文本正反馈与预先确定的分离仍未回答。转向本身不构成阻断。

**实验能否判别主张：** 对“AUROC(A) > AUROC(R)”这一比较可以判别，但对主 Claim“与提示内原因的规律相反”不能判别。设计中没有与 R/A 位置匹配的提示内对照（例如把隐式旁白放在 `</think>` 之后作为 A 的提示内类比），所以“经由推理”在两类原因下的定义并不一致。即使提示内旁白组“经由推理更易检出”而激活组相反，也可以完全由“A 制造了矛盾”这一构造差异解释，而不是由“原因是内部的”解释。此外，MonitorBench 的监控会被告知具体要找的因素，本方案改成了“有无未陈述因素”的开放判断，两个检出量不可直接对比。随机方向对照在不翻转时只测出伪迹底线，排除不了“A 组被检出是因为矛盾、而不是因为抓到了原因”这一解释，而后者恰恰就是该 Claim 的内容。这是 Claim 阻断。

**可行性：pass。** R/A/F 位置掩码可以在已 clone 的 2605.26772 前向 pre-hook 上改写。diff-in-means 方向有公开规范（2604.01202 的 pre_gen 位置、2603.01437 的 pre-CoT 位置）。When2Call 公开可得。Sports Understanding 与 Anachronisms 来自 BIG-bench（Anachronisms 不在 BBH 中，属于定位措辞小误），Social Chemistry 来自 Social-Chem-101，按 2603.01437 的格式可以构造。约 1.5 万条生成在 2×A100 上一天内可以完成；约 6000 万监控 token，中档 API 加本地 Qwen3-32B 在 1000 元预算内。不需要人工标注；正负类标签由干预本身定义，含义清楚。风险：A 条件在 50% 翻转档可能需要导致输出退化的 α，那时配对翻转率可能无法达成。这影响的是结果的说服力，不影响实现。

## 最高近邻
1. MonitorBench（2603.28590，https://arxiv.org/abs/2603.28590）：提出“因素塑造中间推理时更可监控”。因素都通过提示注入，监控被告知要找的因素，是黑盒研究，没有 steering。本方案的“反转”以它为参照，但两者对“经由推理”的定义不一致。
2. Duzan & Stickland, Chain-of-Thought Monitoring Can Be Unreliable in Implicit-Influence Settings（2608.04735，https://arxiv.org/abs/2608.04735）：隐式影响使检出下降 41–46pp。附录 G 在 Qwen3-8B 编码任务上显示 steering 向量会降低检出，但不跨设定泛化。没有区分作用位置，也没有配对翻转率。
3. Esakkiraja et al., Therefore I am. I Think（2604.01202，https://arxiv.org/abs/2604.01202）：在 When2Call/BFCL 上用 pre_gen 方向 steer，翻转后的 CoT 多为合理化（confabulated support 等）。用的是成对判定，没有单条轨迹监控，也没有作答处 steering。
4. Cox et al., Post-Hoc Reasoning in Chain of Thought（2603.01437，https://arxiv.org/abs/2603.01437）：在二选一任务上用 pre-CoT 方向 steer，得到 confabulation 与 non-entailment 两类病态。主实验用指令模型，在全部位置注入，作者把“只在 CoT 注入”列为未来工作。
5. Mirtaheri & Belkin, Catching rationalization in the act（2603.17199，https://arxiv.org/abs/2603.17199）：hint 驱动的动机性推理在 CoT 中常无痕迹，探针不弱于甚至优于 CoT 监控。原因在提示内，但“合理化使 CoT 监控失效”这一结论已经覆盖了 R 条件的预期。

```json
{
  "score": 5.0,
  "contribution_scores": {"importance": 6.0, "novelty": 6.0, "effectiveness": 6.5},
  "contribution_assessment": "主贡献为：内部激活原因只在审议阶段起作用时，CoT 合理化使监控难以发现；只在作答处起作用时，CoT 与答案冲突，监控易发现；并据此宣称与 MonitorBench 规律相反。重要性有限：真实内部偏好更接近全程作用，而合理化不可见已由 2603.17199、2608.04735 等表达。新颖度是可辨认的组合增量：作用位置乘以单轨迹 AUROC 尚无人做，但预期结论可由已知结果直接推出。“反转”依赖对 MonitorBench 中“shape reasoning”的错位映射：R 条件对应 MonitorBench 中本就难监控的 Cue(Answer) 类，A 条件是没有提示内对应物的人为矛盾构造。有效性：A>R 方向大概率成立，但主要源于构造。R 难检出的依据来自成对判定与单设定附录，仍未知。客观任务存在把“答错”当作“受影响”检出的混淆。",
  "feasibility": "pass",
  "feasibility_reason": "位置掩码可在已 clone 的 2605.26772 hook 代码上改写，方向提取有公开规范，When2Call、BIG-bench 与 Social-Chem 数据可得。约 1.5 万条生成在 2×A100 一天内可完成，约 6000 万监控 token 在 1000 元内，不需要人工标注。风险是 A 在高翻转档可能需要导致输出退化的 α。",
  "verdict": "needs_rethink",
  "fatal_blockers": [
    "贡献不足：重要性与新颖度均未达 8。去掉“反转”包装后，A 可检出、R 被合理化这两点大多可由已知结果直接推出，三维门槛不满足。",
    "Claim 阻断：“与 MonitorBench 规律相反”依赖对“经由推理”的不一致定义。设计中没有与 R/A 位置匹配的提示内对照，且监控任务从“找指定因素”改成了“找未陈述因素”。实验无法把“原因是内部的”与“A 构造了 CoT-答案矛盾”这两个解释区分开。"
  ],
  "novelty_conclusion": "在已核验的文献中，没有工作同时操纵 steering 作用位置并测单条轨迹 CoT 监控 AUROC，形式上是新的。但核心预期是被 steer 的 CoT 合理化（2604.01202、2603.01437）加上立场矛盾可见（RFEval）的常规组合，“反转”定位不成立，新意仅为增量。",
  "closest_neighbors": [
    "MonitorBench: A Comprehensive Benchmark for Chain-of-Thought Monitorability in Large Language Models (arXiv:2603.28590)",
    "Chain-of-Thought Monitoring Can Be Unreliable in Implicit-Influence Settings (arXiv:2608.04735)",
    "Therefore I am. I Think (arXiv:2604.01202)",
    "Post-Hoc Reasoning in Chain of Thought: Decoding and Steering Pre-Committed Answers (arXiv:2603.01437)",
    "Catching rationalization in the act: detecting motivated reasoning before and after CoT via activation probing (arXiv:2603.17199)"
  ]
}
```
