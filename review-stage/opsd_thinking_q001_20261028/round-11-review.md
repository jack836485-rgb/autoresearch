## 结论

2026-10-28 评审：score 8.2，verdict experiment_ready。检索范围内，没有工作在开思考训练的 OPSD（TH-OPSD）中用按认知类分组的前向 KL 做"只保留一项"的训练干预，从而把长度方向和准确率退化分别归到不同通道。核心 Claim（主张一、二）新颖，主张三是次要且增量的 TH 版复现。值得进入实验规划。

已核验的事实：
- 仓库 xiuyuz/opsd-reference-study 中，brief 列出的文件与参数都存在：`apply_loss_horizon`、`--pi-override-file`、`--fork-mask-mode`、`CORRECTION_MARKERS`（11 个）、两个控制脚本、`--mode thinking`。
- `chunked_kl_backward` 只对截断后的前 1,024 个 token 计算并按 token 数归一。因此"生成上限 1,024 等价于原 TH 训练损失"这一捷径成立。
- 2609.20612、2609.39118、2607.05184、2607.10805 中被引用的数字均与原文一致。

不构成 fatal、但需要在规划中写清的问题：
1. **遗漏相邻反证。** 2603.24472 附录 H 在 SDPO 中用鼓励不确定性的教师提示，把认知词计数从 8.8 提到 31.4，退化仍然存在。这已部分预示主张一的"不必要"一半（设置不同：SDPO、提示层而非损失通道）。brief 写"已有因果证据都不在 OPSD 中"本身成立，但应把这条列为相邻证据并划清边界。
2. **长度方向相反的前提尚未确立。** 2609.20612 中 Answer Only 变长是相对 DR 臂而言；2609.39118 上限 1,024 的表 4 中，多数上下文相对基座都变长。因此两种视图相对 B 方向相反未必出现。brief 已设前提格处理，但主张二很可能退化为单方向归因。
3. **T0u 不是官方目标。** 官方损失对每个（token, vocab）元素截断到 0.05，T0u 去掉了截断，退化可能改变。事先检查已覆盖这一点。
4. **等价判定的功效。** 当 δ 约为 1.85 分、每臂 5 个种子时，"T2−B 的 CI 下界 > −δ"可能因 CI 过宽而落入"其余"格。建议用 T0 和 T0u 种子 0 的方差先估功效。
5. **$L_{\text{marg}}$ 不纯。** 调整 $m_S$ 会同比例改变 ¬E 中停止 token 的质量，所以 T2 的长度效应里混有停止 token 通道。brief 已把停止 token 变化列为描述量，解释时应作为限定条件写明。

## Claim 判断

| Claim | 判断 | 最关键依据 |
|---|---|---|
| 主张一：认知边际通道对 TH-OPSD 准确率退化既不必要也不充分（T1/T2/T3 判定） | 新颖（"不必要"一半与 2603.24472 附录 H 部分重合） | 2607.05184 附录 E 是无特权 OPD 中的位置掩码；2609.20612 的 marker 排除只在 DR 下做；AD-OPSD 用熵门控；Purified OPSD 做 PMI 分解；2608.04794 只做诊断。均没有 TH-OPSD 中的类分组单项训练。2603.24472 附录 H 在 SDPO 中提升认知词计数仍不止退化，属相邻证据 |
| 主张二：长度方向由认知边际通道承载 | 新颖 | 检索未见任何工作把 OPSD 长度方向归因到教师信号的某一部分。2609.39118 只报长度增长，2607.05184 只报变短。前提"两视图方向相反"未被现有证据确立 |
| 主张三：不含答案的轨迹形式前缀足以造成退化 | 部分重合 | 2609.39118 表 4（单种子）已读作前缀分布效应；2608.18271 显示错配参考常不差于正确参考；2609.20612 在 DR 下做过截断与他题对照。本 Idea 的增量是 TH 下、答案过滤、长度匹配、5 种子的等价检验 |
| 方法：前向 KL 的类分组恒等式（DKD 推广）+ 单项训练 + 剂量匹配 + 频率匹配随机类 | 新颖组合，非简单重标 | 恒等式本身来自 DKD（2203.08679），这里是作为因果干预工具使用，并配有 M1/M2 操纵检查和随机类对照，能直接区分最高近邻的位置掩码方案 |
| Baseline 与可行性 | 通过 | 所有 baseline 同领域、同任务、同代码，复现入口已核验；约 520 A100 小时，在 2×A100 预算内 |

## 最高近邻

1. **What Does Privileged Information Add to On-Policy Self-Distillation?（2609.20612）** https://arxiv.org/abs/2609.20612 ，代码 https://github.com/xiuyuz/opsd-reference-study
   - 重叠：同代码、同模型，TH 退化、视图与长度观察、marker 抑制同号。
   - 差别：内容对照与 marker 排除只在 DR 下做；没有按类的 KL 分解，长度方向只作观察。其未来工作列出"检验被抑制的重新考虑"，本 Idea 是独立的机制检验，不是对该文的补实验。
2. **Diagnosing On-Policy Self-Distillation for Reasoning Language Models（2609.39118）** https://arxiv.org/abs/2609.39118
   - 重叠：TH/TH 设置、上下文对照、前缀分布解释、长度增长。
   - 差别：单种子；无关解答带答案且长度不匹配；只有熵/优势选 token，没有按认知类的损失干预。
3. **Rethinking On-Policy Self-Distillation for Thinking Models（2607.05184）** https://arxiv.org/abs/2607.05184
   - 重叠：只在开思考训练时有害、fork 抑制假说、认知 marker 位置掩码。
   - 差别：作者自认机制非因果；附录 E 是无特权 OPD 中的位置掩码，不是分布层面的类边际分解；用 JSD。
4. **Why Does Self-Distillation (Sometimes) Degrade the Reasoning Capability of LLMs?（2603.24472）** https://arxiv.org/abs/2603.24472
   - 重叠：认知抑制解释；GRPO 中惩罚认知 token 导致变短并掉点；附录 H 在 SDPO 中提升认知词不止退化。
   - 差别：干预在 GRPO 和教师提示层，不在 TH-OPSD 的损失通道，也不分离长度与准确率。
5. **Diagnosing and Mitigating Thinking Collapse in OPSD（AD-OPSD，2607.10805）** https://arxiv.org/abs/2607.10805
   - 重叠：Qwen3-1.7B T/T 设置下认知密度下降，以及缓解方法。
   - 差别：按熵沙箱门控混入基座目标；没有类分组 KL，也没有单项因果检验。

```json
{
  "score": 8.2,
  "verdict": "experiment_ready",
  "fatal_blockers": [],
  "novelty_conclusion": "检索范围内无工作在 TH-OPSD 中用认知类分组前向 KL 的单项训练干预分离长度方向与准确率退化；主张一、二新颖（主张一的'不必要'一半与 2603.24472 附录 H 的 SDPO 提示层证据部分重合，需补充边界），主张三为对 2609.39118/2608.18271 前缀分布结论的增量 TH 检验。基线与复现入口已核验，预算可行；非 fatal 风险为两视图相对基座长度方向相反未确立、未截断 T0u 的退化需事先检查、5 种子等价检验功效、L_marg 混入停止 token 质量。",
  "closest_neighbors": [
    "What Does Privileged Information Add to On-Policy Self-Distillation? (2609.20612)",
    "Diagnosing On-Policy Self-Distillation for Reasoning Language Models (2609.39118)",
    "Rethinking On-Policy Self-Distillation for Thinking Models (2607.05184)",
    "Why Does Self-Distillation (Sometimes) Degrade the Reasoning Capability of LLMs? (2603.24472)",
    "Diagnosing and Mitigating Thinking Collapse in On-Policy Self-Distillation (2607.10805)"
  ]
}
```
