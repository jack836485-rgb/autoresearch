## 结论

2026-10-28 评审：**score 6.5 / 10，verdict = promising_needs_revision**。

新颖性：在 TH 训练的 OPSD 中，用前向 KL 的类分组链式分解（$L_{\text{marg}}$ / $L_{\text{cond}}$）做"只保留一项"的因果干预，我没有检索到先例。已核验的近邻都没有做这一步：
- 2607.05184 只在无特权的 OPD 里做了 epistemic-only 与随机比例掩码（附录 E 表 20）。
- 2609.20612 的 marker 干预只在 DR 下做。
- Purified OPSD 与 2608.04794 的分解只用于诊断，或只通过改 PI 形式来干预。
- 2603.24472 的因果研究在 GRPO 中（DeepSeek-R1-Distill-Qwen-7B）。
- 综述 2608.25936 明说 PMI 解释尚未被检验。

可行性良好：
- Baseline 同域、同任务、同模型，仓库可用。
- 生成上限 1,024 与 LOSS_HORIZON=1,024 在损失上分布等价，这一点代码核验成立。
- 预算在 2×A100 内。

阻碍"可进实验"的是一个 **claim blocker**：实验能检验"退化由非 $E$ 总量的部分承载"，但不能把它识别为"朝参考解答路径的引导"。
- **参考路径拉力本身区分不了结局。** 文中用"同号、区分不了"驳回 marker 假说，同样的批评也适用于参考路径拉力。DR 训练同样看参考解答并获得增益，很可能也有正的拉力，而判定表没有用 DR 锚点的拉力做对照。
- **$L_{\text{cond}}$ 里混有别的成分。** 它装着 $E$ 总量以外的全部教师信号：参考语义、教师上下文分布偏移、通用风格。设计中没有能把参考语义与"上下文偏移"分开的条件，例如 TH 下的他题或错误参考对照。Problem Anchor 明确要求回答这个问题。
- **主支持结果近乎由构造决定。** $L_{\text{marg}}$ 在总 KL 中占比可能很小，附录 E 的边际只从 0.00928 降到 0.00853。所以"$r$ 上界 < 0.25"几乎必然出现，而它真正提供的只是"$E$ 总量通道非必要"这一较窄的结论。

结论：值得继续，但需要先把"H-content = 参考路径"这条机制链在识别上闭合。

## Claim 判断

| Claim | 判断 | 关键依据 |
|---|---|---|
| TH-OPSD 让思考模型退化，DR 不会（82.62 / 72.79 / 基座 80.21；Qwen3-4B 0.532 / 0.590 / 0.591） | 已被覆盖（作为背景事实正确） | 2609.20612 表 11、2607.05184 表 3 原文数值核验一致 |
| 认知抑制是否致因，在 OPSD 中未做因果检验 | 新颖（缺口属实） | 2607.05184 自认非因果；2609.20612 的 marker 干预只在 DR 下；2603.24472 的因果研究在 GRPO（§5.4 "Causal Study…during GRPO"，不叫 "A Causal Intervention"；10.3→7.9 在 2607.10805 中有表内不一致，引用需小修） |
| 用 DKD 式类分组恒等式做"只保留一项"的干预来分离两种机制 | 部分重合 | 分解形式来自 DKD（2203.08679），属于已知技巧；在 TH-OPSD 中做因果拆分，未见先例。在 logit 层面 $L_{\text{cond}}$ 对 $E$ 整体平移不变，分离干净；参数层面的泄漏由 M1 兜底，设计合理 |
| 退化主要由 $L_{\text{cond}}$ 承载，$L_{\text{marg}}$ 单独时无害 | 新颖，但信息量偏低 | 可证伪，配有 T3 与 M2 检查；但 $L_{\text{marg}}$ 的占比很小，T1≈T0u 近乎先验成立 |
| 承载的是"朝参考解答路径的引导" | 不可识别（claim blocker） | 拉力只是相关指标，没有 DR 拉力对照，也没有 TH 下他题或错误参考的对照（仓库已有 `--pi-override-file` 与 `data/controls/`），区分不了参考语义与教师上下文偏移 |
| Baseline 与复现路径 | 成立 | 仓库 `training/train_opsd.py`（`apply_loss_horizon`、`--fork-mask-mode`）、`opsd/opsd_loss.py`（TOKEN_CLIP=0.05 逐元素截断）均已核验；README 称 DR 100 步约 0.5 H100 小时，与 1,024 上限的估算一致 |

## 最高近邻

1. **What Does Privileged Information Add to On-Policy Self-Distillation?**（2609.20612v2）https://arxiv.org/abs/2609.20612 ；代码 https://github.com/xiuyuz/opsd-reference-study
   - 重叠：同模型、同切分、同 TH/DR 退化，以及 marker 排除。
   - 差别：该文的 marker 干预只在 DR 下，作者自认"未建立 TH 退化机制"；没有 KL 分解。
2. **Rethinking On-Policy Self-Distillation for Thinking Models**（2607.05184v1）https://arxiv.org/abs/2607.05184
   - 重叠：fork 抑制假说、训练开思考有害、marker 边际概率。
   - 差别：唯一的掩码干预在无特权的 OPD 中，并且是按位置掩码，不是按类总量分解。
3. **Purified OPSD**（2607.02234v1）https://arxiv.org/abs/2607.02234
   - 重叠：把教师信号拆成参考诱导分量与可迁移分量，并追踪认知 marker。
   - 差别：分解仅作诊断（余弦与范数占比），没有只用一项的训练；也不分离认知总量。
4. **Diagnosing and Mitigating Thinking Collapse in OPSD**（2607.10805v1）https://arxiv.org/abs/2607.10805
   - 重叠：Qwen3-1.7B/4B 在 T/T 设置下的认知密度下降，训练长度 1,024。
   - 差别：用熵沙盒与非对称门控锚定到基座，没有认知总量与条件项的分解，也没有单项消融。
5. **Privileged, but Biased**（2608.04794v1）https://arxiv.org/abs/2608.04794
   - 重叠：PI 偏差分数（0.52 对 ≤0.02），把失败归因于参考路径偏置。
   - 差别：干预只改 PI 形式（解答、提示、技能），没有在 TH-OPSD 中保留或移除某一信号分量。

```json
{
  "score": 6.5,
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "claim: H-content 被解释为'朝参考解答路径的引导'，但参考路径拉力只是相关指标；判定表未用 DR 锚点拉力做对照（DR 同样看参考却获益），也没有 TH 下他题/错误参考对照来区分参考语义与教师上下文分布偏移，无法识别 L_cond 中承载退化的是参考路径",
    "claim: L_marg 在总 KL 中占比可能很小（边际 0.00928→0.00853），'r 上界<0.25'近乎由构造保证，主支持结果信息量有限"
  ],
  "novelty_conclusion": "在 TH-OPSD 中用前向 KL 类分组分解做单项因果干预，未检索到先例；分解技巧本身来自 DKD。新颖性边界中的'H-marker 必要性/充分性'部分成立，'参考路径引导'这一机制归因尚不可识别。",
  "closest_neighbors": [
    "What Does Privileged Information Add to On-Policy Self-Distillation? (arXiv 2609.20612)",
    "Rethinking On-Policy Self-Distillation for Thinking Models (arXiv 2607.05184)",
    "Purified OPSD: On-Policy Self-Distillation Without Losing How to Think (arXiv 2607.02234)",
    "Diagnosing and Mitigating Thinking Collapse in On-Policy Self-Distillation (arXiv 2607.10805)",
    "Privileged, but Biased: How PI-Conditioned Teachers Break Self-Distillation (arXiv 2608.04794)"
  ]
}
```
