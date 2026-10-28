## 结论

2026-10-28 评审：**score 6.0 / 10，verdict = promising_needs_revision。**

- **主张二（认知通道）：基本新颖，但增量有限。** 主张二用 DKD 式的类分解做"只保留一项"的必要性与充分性检验。核验范围内，没有工作在 OPSD 中按认知类分解或掩码 KL：
  - 2607.05184 附录 E 的 marker 掩码在不带特权信息的 OPD 中做；
  - AD-OPSD 按熵选位置；
  - 2609.39118 的掩码只按熵和位置。
  分解本身在数学上正确：二元划分下 KL 的链式分解成立，$m_T$ 视为常数也合理。
- **工程可行性成立。** `xiuyuz/opsd-reference-study` 已核验：
  - `apply_loss_horizon` 只截取前缀；
  - `--pi-override-file`、`--fork-mask-mode exclude` 与 `length_matched_other_problem.py` 都存在；
  - marker 标记按损失所见的前缀计算；
  - 1,024 生成上限下的前缀分布与 20,764 上限相同，低成本复现 TH 有效；
  - 无特权教师在 TH 下 KL≡0 的论证也正确。
- **主张一有 claim blocker。** 背景的核心前提是"语义还是偏移在 TH 下从未检验过"。这条前提被一篇未引用的近邻推翻：2609.39118（2026-09-30）表 4。
  - 它在 matched Th/Th、1,024 rollout 上限下，对 Qwen3-1.7B 与 OLMo-3-7B-Think 做了 Unrelated solution（另一数据集的题与解）教师上下文对照。
  - OLMo 上，他题解答的退化与本题解答相当：63.5 → 57.5，本题解答为 58.8。
  - 作者结论是 prefix mismatch 即使在无关上下文下也会移动信号，并支持 mode transfer 而非语义。
- **影响。** 主张一因此从"首次检验"退化为"在已确认退化的 1.7B 配置下，用无答案、等长、多种子的更干净对照复核一条单种子观察"。新颖边界必须围绕这篇论文重写，现有关于最高近邻的差别陈述也不完整。
- **是否值得继续：值得。** 两种不含答案的开头上下文仍能分离"答案误导"与"无本题信息"，这是 2609.39118 没有做到的。实验预算（约 355 A100 小时）与 baseline 复现路线也都成立。但修正定位之前不能进入实验规划。

## Claim 判断

| Claim | 判断 | 最关键依据 |
|---|---|---|
| 前提：TH 下"语义 vs 偏移"从未检验 | **已被覆盖（陈述错误）** | 2609.39118 表 4 在 Th/Th 下有 Unrelated solution 臂。OLMo 上他题上下文 −6.0，与本题解答的 −4.7 相近；Qwen3-1.7B 在其设置下没有退化。单种子，他题带答案，长度不匹配。 |
| 前提：2609.20612 与 OP²SD 的内容对照只在 DR 下 | 新颖（陈述准确） | 2609.20612 v2 的他题、截断、错答案对照与 marker 排除都只在 direct 下做，TH 只比较三种视图。OP²SD 附录 H 只有本题参考，49.24 vs 49.86，单种子。2608.18271 的学生全部不开思考。 |
| 主张一：退化需要本题信息（I-own 降、I-other 不降） | **部分重合** | 2609.39118 已给出方向相反的初步证据（OLMo 上无关上下文足以退化）。本 Idea 的增量限于以下几点：答案过滤、等长开头、多种子 CI，以及在复现出 −7.4 的配置下检验。 |
| 主张二·不必要：只用 $L_{\text{cond}}$ 仍复现大部分下降 | 新颖 | OPSD 中没有按认知类保留或去除 KL 项的先例。2607.05184 的 marker 掩码在不带特权信息的 OPD 中做；AD-OPSD 与 2609.39118 只按熵或位置。 |
| 主张二·不充分：只用剂量匹配的 $L_{\text{marg}}$ 不足以退化 | 新颖但增量小 | 2603.24472 §5.4 已在 GRPO 中做过惩罚认知 token 的因果检验，结果是变短、变差。本 Idea 把它搬到 OPSD，并与 T0u 的密度降幅匹配。 |
| 方法：DKD 式类分解 | 部分重合（组合） | 这是 DKD 目标类/非目标类分解在 token 类上的直接推广，作为诊断工具合理，本身不构成方法贡献。 |
| Baseline 与复现入口 | 成立 | 仓库文件与 flag 已核验；所有 baseline 同任务、同模型、同评测。 |

## 最高近邻

1. **Diagnosing On-Policy Self-Distillation for Reasoning Language Models**（2609.39118，[arxiv](https://arxiv.org/abs/2609.39118)）
   - 重叠：Th/Th、1,024 上限、Qwen3-1.7B 与 OLMo，有 Unrelated solution 与 Answer-only 教师上下文对照，并有离线重打分（无关上下文的 KL 为 0.054，本题为 0.108），结论偏向"偏移/模式迁移"。
   - 差别：单种子；他题带答案、来自另一数据集、不等长；没有不含答案的本题开头；没有按认知类的损失干预。
2. **What Does Privileged Information Add to OPSD?**（2609.20612，[arxiv](https://arxiv.org/abs/2609.20612)，[code](https://github.com/xiuyuz/opsd-reference-study)）
   - 重叠：同模型、同代码、同 TH 退化（72.79 vs 80.21），有他题、截断开头、marker 排除对照。
   - 差别：这些对照全部只在 DR 下做。
3. **Rethinking OPSD for Thinking Models**（2607.05184，[arxiv](https://arxiv.org/abs/2607.05184)）
   - 重叠：开思考训练才有害，用 fork 抑制解释，并测量认知 token 的边际质量。
   - 差别：作者自认没有证明因果；marker 掩码在不带特权信息的 OPD 中做；没有内容对照。
4. **Diagnosing and Mitigating Thinking Collapse in OPSD**（AD-OPSD，2607.10805，[arxiv](https://arxiv.org/abs/2607.10805)）
   - 重叠：Qwen3-1.7B T/T，训练上限 1,024，认知密度从 10.3 降到 7.9，并有高熵位置锚定。
   - 差别：按熵而非按认知类选位置；没有内容对照；没有公开代码。
5. **Privileged Solutions or Context-Induced Teacher Behavior?**（OP²SD，2608.09228，[arxiv](https://arxiv.org/abs/2608.09228)）
   - 重叠：直接提出"特权解答 vs 上下文诱导"的问题，有他题参考对照。
   - 差别：他题对照只在学生不开思考时做；双方开思考只跑了本题参考，且单种子。

```json
{
  "score": 6.0,
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "Claim blocker: the premise that 'semantics vs. shift has never been tested under thinking-enabled rollouts' is false. arXiv 2609.39118 (Table 4, matched Th/Th, 1,024-token rollout cap, Qwen3-1.7B and OLMo-3-7B-Think) already ran an Unrelated-solution teacher-context control and found that unrelated context degrades OLMo about as much as the full solution. That paper is missing from the closest-neighbor positioning, so Claim 1's novelty boundary must be redefined against it."
  ],
  "novelty_conclusion": "Claim 2 (class-level marginal/conditional KL ablation of the epistemic channel in OPSD) is novel within the searched literature but incremental: it carries DKD over to a token class and moves 2603.24472's GRPO sufficiency test into OPSD. Claim 1 partially overlaps 2609.39118. Only the answer-free, length-matched, own-prefix vs. other-prefix, multi-seed refinement in the confirmed-degradation 1.7B configuration remains new. Feasibility and baselines are verified.",
  "closest_neighbors": [
    "Diagnosing On-Policy Self-Distillation for Reasoning Language Models (arXiv 2609.39118)",
    "What Does Privileged Information Add to On-Policy Self-Distillation? (arXiv 2609.20612)",
    "Rethinking On-Policy Self-Distillation for Thinking Models (arXiv 2607.05184)",
    "Diagnosing and Mitigating Thinking Collapse in On-Policy Self-Distillation (arXiv 2607.10805)",
    "Privileged Solutions or Context-Induced Teacher Behavior? Dissecting On-Policy Self-Distillation (arXiv 2608.09228)"
  ]
}
```
