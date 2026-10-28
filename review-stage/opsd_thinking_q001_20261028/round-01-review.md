## 结论

2026-10-28 评审：**score 5.5 / 10，verdict = promising_needs_revision。**

- **问题本身成立。** 方向冲突有据可查：
  - Purified OPSD（2607.02234）在同一套设置下（JSD、上限 1,024）报告 R1-Distill-7B 的 "Wait" 从 34K 升到 83K，而 Qwen3-8B 从 27K 降到 10K。
  - 2603.24472 在 R1-Distill-7B 上报告压低。
  - 2609.39118 报告评测长度增长。
  - 2607.05184 报告长度压缩到约 0.8×。
- **"被忽视的关键"不成立。** 训练前用教师与学生的对数概率差来刻画修正类 token 的做法已经有人做过。
  - 2609.20612 在冻结基座的 rollout 上计算 correction pressure F_v。它取的是采样到的 wait/but/maybe/actually/check 等 token 上的 log p^T − log p^S。
  - 该文在 Qwen 的所有参考视图上都得到 F_v < 0，但符号不能区分迁移结果相反的配置。它的模板替换结果落在含 0 的区间内。在 marker 位置排除或降权损失，marker 使用的变化不到约 1.1%。
  - 2609.39118 报告初始 forward KL 不能预测效应方向。
  - brief 没有引用这两篇，也没有与它们划界。
- **仍然新颖的部分：**
  - 把 ρ 定义为认知集合上的全分布边际质量，而不是只看采样到的 token；
  - "已验证" 与 "可能有错" 两种呈现框架的因果翻转设计；
  - EMP 这种边际重缩放，并配随机类对照。
- **主张一有同义反复的风险。** 学生向教师的认知边际移动，几乎就是蒸馏的定义。只有当这一点在长预算评测里仍然成立，并且能解释准确率退化时，主张一才有信息量。
- **主张二与已有负结果相冲。** 2609.20612 的 marker 层面干预几乎无效，brief 却没有把这种最直接、实现很简单的竞争干预放进 baseline。
- **算力估计偏乐观。**
  - 官方 README 写明每次全参训练约需 5–12 小时 8×H100，教师提示最长 25k。
  - brief 估算 2×A100 上 LoRA 每步 40 秒，很可能低估 2–4 倍。
  - 官方 `train.py` 没有接入 LoRA 参数，需要自行接入。
  - 这些不构成致命问题，但 160 A100 小时的总预算不可信。
- **判断：值得继续，** 前提是把新颖性边界改写为相对 2609.20612 与 2609.39118 的增量。

## Claim 判断

| Claim | 判断 | 关键依据 |
|---|---|---|
| 方向在不同论文乃至同一模型上冲突 | 新颖（作为问题陈述有据） | 2607.02234 在同一设置下 R1-Distill 升、Qwen3-8B 降；2603.24472 在 R1-Distill 上压低；2609.39118 长度增长 6.0%–25.3%（Table 3）。2607.05184 中 wait 从 3.85 降到 2.54 的归属（OPSD 学生还是 gold-demo OPD）需要再核对。 |
| 现有解释只能预测压低 | 部分重合 | 2609.39118 已指出教师信号取决于"整个教师前缀与推理模式对齐"，不只是特权语义，并观察到长度增长与崩溃两类结局。说"无人解释双向"偏强。 |
| ρ 是被忽视的、训练前可测的方向决定量 | 部分重合 | 2609.20612 的 F_v 是同类训练前量（采样 token 版本），其符号不区分结局；2609.39118 的初始 KL 不能预测方向。ρ 的差别在于全分布边际，并且只预测认知词的方向，而不是准确率。 |
| 方向律：改呈现模板翻转 ρ，认知词与长度随之翻转；上限与损失只改幅度 | 部分新颖 | 没有找到"已验证"对"可能有错"的框架翻转实验。2608.09228 改的是内容（错误解答），不是框架；2609.20612 的模板替换没有显著效果。风险有两点：一是在 Qwen 上 F_v 普遍为负，模板 B 可能翻不出符号；二是认知词随教师移动接近同义反复。 |
| EMP 是必要的修法，随机类对照无效 | 部分新颖 | 只缩放认知边际、保留集合内形状，这种操作没有找到先例。但 2609.20612 的 marker 损失降权几乎不改变行为；2607.10805（AD-OPSD）在高熵位置锚定基座；2607.02234 用 PMI 去掉参考分量。最直接的竞争者（marker 位置降权或排除）不在 baseline 中。 |

## 最高近邻

1. **What Does Privileged Information Add to On-Policy Self-Distillation?**（https://arxiv.org/abs/2609.20612）
   - 重叠：Qwen3-1.7B 加 LoRA，训练前在冻结基座上算修正类 marker 的教师减学生对数概率差，做模板替换与 marker 损失降权，开思考训练会退化。
   - 差别：用采样 token 而非边际质量；没有检验符号与训练后 marker 变化的关系；没有框架翻转；没有边际重缩放。
2. **Diagnosing On-Policy Self-Distillation for Reasoning Language Models**（https://arxiv.org/abs/2609.39118）
   - 重叠：教师前缀与推理模式决定信号；有长度增长与退化；初始 KL 不能预测方向；扫过 rollout 上限和 β（forward KL、JSD、reverse KL）。
   - 差别：没有测认知 token，没有方向律，没有修法。
3. **Rethinking On-Policy Self-Distillation for Thinking Models**（https://arxiv.org/abs/2607.05184）
   - 重叠：同任务、同数据、同评测；有长预算退化、长度压缩、fork 抑制、wait 下降。
   - 差别：只看压低方向，没有因果检验，没有修法。
4. **Purified OPSD: On-Policy Self-Distillation Without Losing How to Think**（https://arxiv.org/abs/2607.02234）
   - 重叠：同任务修法，用 PMI 去掉参考诱导分量；在同一设置下 R1-Distill 的 Wait 上升、Qwen3-8B 下降。
   - 差别：作用于整个分布，没有方向预测量；没有找到公开代码。
5. **Diagnosing and Mitigating Thinking Collapse in OPSD (AD-OPSD)**（https://arxiv.org/abs/2607.10805）
   - 重叠：Qwen3-1.7B 加 LoRA，认知 token 密度从 10.3 降到 7.9，在高熵位置把目标锚定到基座。
   - 差别：门控按熵选位置，不针对认知类边际，只处理压低方向；没有找到代码。

```json
{
  "score": 5.5,
  "verdict": "promising_needs_revision",
  "fatal_blockers": [],
  "novelty_conclusion": "问题陈述（方向冲突）有据可查，但'训练前可测的教师减学生认知 token 偏差'已被 2609.20612 的 correction pressure F_v 覆盖。F_v 在 Qwen 上普遍为负且不区分结局；2609.39118 也显示初始 KL 不能预测方向。brief 两篇都未引用。剩余新颖点是：边际质量版的 ρ、'已验证'对'可能有错'的框架翻转因果设计、只缩放认知边际并配随机类对照的 EMP。方向律有接近同义反复的风险；EMP 的最直接竞争者（marker 位置损失降权或排除，2609.20612 报告几乎无效）不在 baseline 中。算力估计（160 A100 小时）明显偏低，官方 README 写的是每次 5–12 小时 8×H100，且官方 train.py 未接入 LoRA。",
  "closest_neighbors": [
    "What Does Privileged Information Add to On-Policy Self-Distillation? (2609.20612)",
    "Diagnosing On-Policy Self-Distillation for Reasoning Language Models (2609.39118)",
    "Rethinking On-Policy Self-Distillation for Thinking Models (2607.05184)",
    "Purified OPSD: On-Policy Self-Distillation Without Losing How to Think (2607.02234)",
    "Diagnosing and Mitigating Thinking Collapse in On-Policy Self-Distillation (2607.10805)"
  ]
}
```
