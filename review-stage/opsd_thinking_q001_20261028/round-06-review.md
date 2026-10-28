## 结论

2026-10-28 评审：**score 7.5 / 10，verdict = promising_needs_revision**，值得继续，但目前不满足 experiment_ready（要求 > 8）。

- **新颖性：** 主张一（TH 下"本题信息 vs 同形上下文"的训练对照）经检索确认无人做过。2609.20612 的 other-problem 与 truncated-trace 对照、2608.18271 的 off-problem 对照、OP²SD 的他题参考都只在学生不开思考时做过。2607.10805 在 T/T 下做诊断，但没有任何内容对照。主张二（按认知类做 DKD 式分解，用"只保留一项"检验必要性与充分性）也未见先例。
- **增量性：** 主张一本质上补的是 2609.20612 表中缺的 TH 那一格，用的是同一仓库、同一切分、同一模型。真正独立于该论文的贡献，主要落在主张二的分解检验和答案过滤后的"开头"设计上。
- **事实核验：** 故事链中引用的数字与原文一致：80.21 / 82.62 / 72.79；0.532 / 0.590 / 0.591；0.00928 → 0.00853；OP²SD 摘要的 "remains competitive"；附录 H 的 49.24 vs 49.86、单种子；2603.24472 v4 §5.4 的 GRPO 优势惩罚；2609.20612 原文承认推理模式、horizon、监督比例同时变化。
- **复现可行性：** 仓库可复现。`apply_loss_horizon` 只做前缀切片，所以生成上限设为 1,024 等价于原 TH 的损失。`--pi-override-file`、两个 control 脚本、`CORRECTION_MARKERS` 均已核实存在。
- **未解决的新颖性边界：**
  - 漏掉了同设置下的最高近邻 2607.10805（Qwen3-1.7B、T/T、上限 1024、在 OPSD 中按熵做梯度掩码干预）。"认知通道在 OPSD 中没有因果检验"需要相对它重新限定。
  - 主张二没有把仓库现成的 marker 损失排除（`fork_mask_mode`）放到 TH 下作为同任务 baseline，因此 T1 与"TH 下 marker 排除"的区别没有在实验中体现。
  - 主张一的"支持"格要求 ΔI-other 的 CI 下界 > −1 分，实质是等价性检验。只有 3 个种子，很可能落入"不确定"。外部基准只用种子 0、每题 4 条，却被写进"支持结果"的条件。

## Claim 判断

| Claim | 判断 | 最关键依据 |
|---|---|---|
| 现有失败：OPSD 在 TH 下退化，在 DR 下获益 | 已被覆盖（作为前提，引用正确） | 2609.20612 表 11；2607.05184 表 3；2607.10805 的 T/T：AIME25 38.1→33.9 |
| "语义 vs 偏移"在 TH 下从未检验 | 成立 | 2609.20612 的内容对照全在 DR；OP²SD、2608.18271、DualOPSD 的学生都不开思考；2607.10805 只用完整参考一种上下文；2608.04794 的无关题解只用于 PI Bias Score 诊断，没有用于训练 |
| 主张一：退化需要本题信息（等长、去答案的 I-own vs I-other） | 新颖，但偏增量 | 相当于把 2609.20612 的 truncated / other-problem 对照移到 TH，并加答案过滤。设计干净，但等价界在 3 个种子下统计功效存疑 |
| 认知通道在 OPSD 中没有因果检验 | 部分重合 | 2607.10805 在 OPSD T/T 中做了熵掩码干预，但不是按类干预；2609.20612 的 marker 排除只在 DR 下做（已核实）；2607.05184 的 epistemic-only 损失只在无特权 OPD 中做 |
| 主张二：$L_{\text{marg}}$/$L_{\text{cond}}$ 分解下，认知总量既不必要也不充分 | 新颖（方法上是 DKD 的直接推广） | 未见按认知类做"只保留一项"的检验。分解按划分的 KL 链式法则精确成立。M1/M2 与剂量匹配合理。缺少与 TH 下 `fork_mask_mode` 排除的对照 |

## 最高近邻

1. **What Does Privileged Information Add to On-Policy Self-Distillation?**（2609.20612，https://arxiv.org/abs/2609.20612，代码 https://github.com/xiuyuz/opsd-reference-study）
   - 重叠：同模型、同数据、同代码，报告了 TH 退化，在 DR 下做了 other-problem、truncated、reference-free、marker 排除。
   - 差别：TH 下没有任何内容对照，也没有按类的分解检验。
2. **Diagnosing and Mitigating Thinking Collapse in On-Policy Self-Distillation**（2607.10805，https://arxiv.org/pdf/2607.10805）
   - 重叠：Qwen3-1.7B，T/T，上限 1024，用认知词密度刻画坍缩，在 OPSD 中做熵梯度掩码干预，提出 AD-OPSD。
   - 差别：没有内容对照，也没有按认知类做掩码或分解。brief 未引用这篇。
3. **Privileged Solutions or Context-Induced Teacher Behavior?（OP²SD）**（2608.09228，https://arxiv.org/abs/2608.09228）
   - 重叠：他题参考仍具竞争力，附录 H 有两边都开思考的 OPSD。
   - 差别：他题参考没有在学生开思考时测，附录 H 是单种子，没有去答案或等长开头。
4. **Rethinking On-Policy Self-Distillation for Thinking Models**（2607.05184，https://arxiv.org/abs/2607.05184）
   - 重叠：确立了"训练开思考才有害"，提出 fork 抑制，给出 marker 边际，做了 epistemic-only OPD 掩码。
   - 差别：掩码只在无特权 OPD 中做，作者自认没有因果证据，也没有内容对照。
5. **Rethinking Privileged Information in On-Policy Self-Distillation**（2608.18271，https://arxiv.org/pdf/2608.18271）
   - 重叠：off-problem 他题参考对照，结论是语义贡献有限。
   - 差别：学生始终不开思考，也没有报告退化。brief 未引用这篇。

```json
{
  "score": 7.5,
  "verdict": "promising_needs_revision",
  "fatal_blockers": [],
  "novelty_conclusion": "TH 下的答案过滤、等长开头内容对照，以及认知类 DKD 式'只保留一项'的必要性/充分性检验，经检索均无先例，但主张一偏向补齐 2609.20612 在 TH 下缺失的对照。未引用同设置近邻 2607.10805（T/T、1.7B、上限 1024、OPSD 内熵掩码干预）与 2608.18271；主张二缺少 TH 下现成 fork_mask_mode 排除的对照；主张一的 -1 分等价界在 3 个种子下统计功效不足，新颖性边界与可判定性尚未收紧。",
  "closest_neighbors": [
    "What Does Privileged Information Add to On-Policy Self-Distillation? (2609.20612)",
    "Diagnosing and Mitigating Thinking Collapse in On-Policy Self-Distillation (2607.10805)",
    "Privileged Solutions or Context-Induced Teacher Behavior? Dissecting On-Policy Self-Distillation (2608.09228)",
    "Rethinking On-Policy Self-Distillation for Thinking Models (2607.05184)",
    "Rethinking Privileged Information in On-Policy Self-Distillation (2608.18271)"
  ]
}
```
