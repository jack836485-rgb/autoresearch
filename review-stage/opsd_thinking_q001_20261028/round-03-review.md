## 结论

截至 2026-10-28：**score 6.0/10，verdict = promising_needs_revision**。

新颖性判断：
- 在 TH-OPSD 中按"$E$ 类边际 / 类内条件"两项做"只留一项"的因果检验，我没有检索到先例。2609.20612、2607.05184、2607.10805（AD-OPSD）、2607.02234（Purified OPSD）、2608.04794 都没有做这种分解。
- 但分解工具本身不新。按类分组的 KL 链式分解就是 Decoupled KD（TCKD/NCKD，2203.08679）的推广。"知道答案的教师给出学生模仿不来的内容引导"这一解释，也已由 Purified OPSD（reference-induced 分量）和 2608.04794（PI bias）提出。所以本 Idea 的增量是一个诊断性的因果实验，不是新机制，也不是新方法。

可行性：
- 我在仓库里核验了复现入口，属实：`apply_loss_horizon` 只截取前 N 个 token；`--fork-mask-mode exclude` 存在；`CORRECTION_MARKERS` 正是这 11 个词；`opsd_loss.py` 是带逐元素截断的前向 KL。
- 生成上限 1,024 与原文 TH 的被监督 token 等价，这个论证成立。各 baseline 同域、同任务，都有公开实现。没有可行性层面的致命问题。

但 Claim 层面有两个阻塞项，目前不能进入实验规划：
1. **H-content 无法被识别。** 条件项装下了"$E$ 总量以外的一切"，并不等于"内容引导"。$E$ 只取 11 个整词单 token，漏掉了 2607.05184 报告降幅最大的 hmm、altern、recall，也漏掉了 "Let me verify" 这类以非 $E$ token 开头的认知短语。因此结果落在"支持 H-content"一格，也可以解释为认知抑制落在了 $E$ 之外。
2. **证据链有一处错引。** 2603.24472 并没有"在 GRPO 中惩罚认知 token 并复现下降"。原文的 GRPO 反而增加了认知 token，下降来自 SDPO 与 SFT，作者也明确说没有对认知 token 做因果干预。

另有一个技术缺口：仓库实际优化的是逐元素截断（0.05）后的目标，T0 = 边际项 + 条件项只对未截断的 KL 精确成立。另外 T1 的条件项按 $m_S$ 而不是 $m_T$ 加权，"精确分解"的说法需要收窄。

是否值得继续：值得。H-marker 被推翻或被支持都有信息量，成本也在 2×A100 预算内。但必须先解决"条件项 ≠ 内容引导"的识别问题，并改正错引。

## Claim 判断

| Claim | 判断 | 关键依据 |
|---|---|---|
| TH 训练的 OPSD 让思考模型退化，DR 不会 | 已被覆盖（作为背景是正确的） | 2609.20612 表 11：80.21 → 82.62（DR）/ 72.79（TH）；2607.05184 表 3：0.591 / 0.590 / 0.532，数字核验一致 |
| 认知抑制的解释在 OPSD 中未被因果隔离 | 成立 | 2607.05184 原话："not perfectly isolated or proved to be causal"；2609.20612 的 marker 排除只在 DR 下单种子做过，抑制在 DR 与 TH 中同号 |
| 2603.24472 在 GRPO 中惩罚认知 token 复现了下降 | 错误陈述，是 Claim 阻塞项 | 原文 GRPO 增加认知 token；下降来自 SDPO 与 SFT；原文明确没有对认知 token 做因果干预 |
| 前向 KL 可精确拆成类边际项与类内条件项，作为被忽视的关键 | 部分重合 | 这是 KL 分组性质，DKD（2203.08679）已用于 KD；新意只在把它用作 TH-OPSD 的因果探针。截断目标下不精确，T1 改为按 $m_S$ 加权 |
| 只留条件项（T1）仍复现大部分下降，等于支持 H-content | 新颖，但不可识别 | $E$ 之外仍含 hmm、alternatively、recall 和多 token 认知短语的抑制；条件项是残差桶，结果不能直接归为"模仿缺口" |
| 只留边际项（T2）不会造成显著下降 | 新颖 | 未见先例；T3 随机类对照设计合理。T2 能否产生足够大的训练信号（边际 KL 量级很小）需要事先报告 |
| 低成本 TH 复现：上限 1,024 与原文损失等价 | 成立 | 仓库 `train_opsd.py` 中 `apply_loss_horizon` 只用前 N 个 token；rollout 前缀不受上限影响；另设种子 0 事先检查兜底 |

## 最高近邻

1. **What Does Privileged Information Add to On-Policy Self-Distillation?（2609.20612）** https://arxiv.org/abs/2609.20612 ，代码 https://github.com/xiuyuz/opsd-reference-study 。同模型、同代码、同 TH 退化设置，并做过 marker 损失排除与降权。差别：干预只在 DR 下单种子做；没有做 KL 的类边际/条件分解。本 Idea 中的 T4 只是给它补一个 TH 实验，新意必须由 T1、T2、T3 承担。
2. **Rethinking On-Policy Self-Distillation for Thinking Models（2607.05184）** https://arxiv.org/abs/2607.05184 。提出 fork 抑制，对比 marker 掩码与随机掩码，统计边际 marker 概率。差别：掩码对照是在无特权 OPD 下做的，机制被作者自认为非因果；没有分解目标分布。
3. **Diagnosing and Mitigating Thinking Collapse in OPSD（2607.10805，AD-OPSD）** https://arxiv.org/abs/2607.10805 。在 Qwen3-1.7B 上诊断认知 token 密度坍塌，在高熵位置混入基座先验。差别：证据是相关性的；在全词表上混合，不分离类总量与类内形状。
4. **Purified OPSD（2607.02234）** https://arxiv.org/abs/2607.02234 。把教师信号拆成 reference-induced 分量与可迁移分量（PMI），这在概念上就是 H-content。差别：按"参考诱导与否"拆分，而不是按认知类边际拆分；对 marker 的分析只是观察。
5. **Privileged, but Biased（2608.04794）** https://arxiv.org/abs/2608.04794 。PI 教师偏向上下文中的那条解答（模仿缺口），并按 token 类别归因损失，低信息与不确定性类占 55%。差别：没有在 TH-OPSD 中做"只留一项"的因果干预。

（方法层面的近邻：Decoupled Knowledge Distillation，https://arxiv.org/abs/2203.08679 ，目标类与非目标类的 KL 分解。）

```json
{
  "score": 6.0,
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "Claim identification: the conditional term is a residual bucket (everything except the mass of 11 whole-word single tokens). It excludes markers documented as most suppressed (hmm, alternatively, recall) and multi-token epistemic phrases, so a 'supports H-content' outcome does not isolate content guidance from epistemic suppression outside E.",
    "Evidence chain misattribution: 2603.24472 does not penalize epistemic tokens in GRPO or reproduce degradation; its GRPO increases epistemic tokens, and the authors state no causal intervention on epistemic tokens was done."
  ],
  "novelty_conclusion": "The causal marginal-vs-conditional ablation inside thinking-rollout OPSD appears unexplored, so the diagnostic experiment is novel. The decomposition is the standard KL grouping identity (DKD-style), and the H-content explanation overlaps Purified OPSD (reference-induced component) and PI-bias (2608.04794). Novelty is partial; it is a diagnostic contribution. T4 merely adds a TH run to 2609.20612.",
  "closest_neighbors": [
    "What Does Privileged Information Add to On-Policy Self-Distillation? (arXiv 2609.20612)",
    "Rethinking On-Policy Self-Distillation for Thinking Models (arXiv 2607.05184)",
    "Diagnosing and Mitigating Thinking Collapse in On-Policy Self-Distillation (arXiv 2607.10805)",
    "Purified OPSD: On-Policy Self-Distillation Without Losing How to Think (arXiv 2607.02234)",
    "Privileged, but Biased: How PI-Conditioned Teachers Break Self-Distillation (arXiv 2608.04794)"
  ]
}
```
