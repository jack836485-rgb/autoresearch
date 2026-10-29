## 结论

2026-10-28 评审：**score 7.6，promising_needs_revision**。没有致命的新颖性、可行性或 Claim 阻断项。

- **主张一（认知通道既不必要也不充分）在检索范围内是新的。** 已有的因果证据有三处：2603.24472 §5.4 在 GRPO 中做；2607.05184 附录 E 在不带特权信息的 OPD 中按位置掩码；2609.20612 的 marker 排除只在 DR 下做。AD-OPSD、Purified OPSD、2608.18271、2609.39118 都没有按类分解 KL，也没有按认知类干预。用前向 KL 的链式分解，把"认知类总量"与"类内及类外条件分布"分开训练，这个探针简单但有效，不是换个名字。
- **主张二是更干净的复现，属增量。** 2609.39118 已在 TH 下得出"前缀分布而非语义"的结论。他题对照在 DR 和学生不开思考的设置下已有多篇。
- **基线与复现路线核实无误。** 仓库 `xiuyuz/opsd-reference-study` 里有 `apply_loss_horizon`、`--pi-override-file`、`--fork-mask-mode exclude`，以及两个控制脚本。TH 下教师（`disable_adapter`）与学生共享上下文，所以不带参考的教师 KL 恒为 0。KL 只看前 1,024 个补全 token，且是因果计算，所以把生成上限设为 1,024 时，损失的分布与原文 TH 相同。预算可行。
- **未到 experiment_ready 的原因有四：**
  1. "等价"判定（T2 − B 的 CI 下界 > −δ，以及主张二的 ±δ）用的是按题目配对、把各种子混在一起重采样的 bootstrap。这样忽略了种子之间的训练方差。只有 3 个种子时，CI 会偏窄，"不充分"和"相当"可能被错误地判为成立。这直接威胁主 Claim 的一半。
  2. 背景对 2609.39118 表 4 的描述有事实错误。Qwen3-1.7B 在 CoT + solution 上下文下从 34.0 降到 30.8，并非"都没有退化"。而 CoT + solution 恰恰最接近 Full Trace。
  3. 所有判定只来自单一模型、单一配置、域内 384 题。外部基准只评 4 个臂的种子 0。
  4. Problem Anchor 中的"失效时长度方向"瓶颈仍只作描述，没有对应的 Claim。

值得继续。

## Claim 判断

| Claim | 判断 | 关键依据 |
|---|---|---|
| 背景：TH-OPSD 让思考模型退化（80.21 → 72.79；Qwen3-4B 0.591 → 0.532） | 已被覆盖（作为前提，正确） | 2609.20612 表 11、2607.05184 表 3 数值核对一致 |
| 认知抑制是主流解释，且在 OPSD 中未被因果检验 | 基本成立 | 2607.05184 自认"not isolated or proved causal"。2603.24472 的因果研究在 GRPO 中。2607.05184 附录 E 在无特权信息的 OPD 中，两种掩码无法区分。2609.20612 的 marker 排除只在 DR 下 |
| 主张一·不必要：只用 L_cond 训练仍复现大部分下降 | 新颖 | 检索到的工作都没有在 OPSD 中按类分解 KL，也没有只保留类内及类外条件项来训练。M1 能检查认知抑制是否泄漏到 E 之外，设计合理 |
| 主张一·不充分：剂量匹配的 L_marg 压低 E 密度，但准确率不显著下降 | 新颖，但统计判定需加固 | 这是一个"等价"型结论。各种子混合的 bootstrap 不含种子间方差，3 个种子时可能误判通过 |
| 主张二：等长、都不含答案的 I-own 与 I-other 造成相当的退化 | 部分重合 | 2609.39118 在 TH 下已有无关解答对照，结论为前缀分布。本 Idea 增加多种子、等长、去答案。但"不含答案的开头"在 DR 下已由 2609.20612 的 trace openings 对照涉及 |
| T4：在 TH 下做 marker 位置损失排除 | 平凡，作对照即可 | 直接复用已有的 `--fork-mask-mode exclude`，不进判定，定位恰当 |
| "会动摇以认知抑制为前提的修法方向" | 略有过度外推 | AD-OPSD 按熵门控、Purified OPSD 用 PMI 目标，二者都不直接依赖按类压低认知 token 这一机制 |

## 最高近邻

1. **What Does Privileged Information Add to On-Policy Self-Distillation?（2609.20612）** https://arxiv.org/abs/2609.20612
   - 重叠：同代码、同模型、同评测；给出 TH 退化；在 DR 下做 marker 排除与他题对照；指出 marker 抑制在 DR 与 TH 中同号。
   - 差别：没有在 TH 下做任何因果干预，也没有按类分解 KL。
2. **Diagnosing On-Policy Self-Distillation for Reasoning Language Models（2609.39118）** https://arxiv.org/pdf/2609.39118
   - 重叠：在 TH 下对比无关解答、完整解答、只给答案等教师上下文，结论是前缀分布偏移。
   - 差别：单种子；无关解答带答案、不等长；没有认知类干预；Qwen3-1.7B 只在 CoT + solution 下退化（34.0 → 30.8）。
3. **Rethinking On-Policy Self-Distillation for Thinking Models（2607.05184）** https://arxiv.org/pdf/2607.05184
   - 重叠：提出 fork 抑制假说；附录 E 比较 marker 位置掩码与随机位置掩码。
   - 差别：附录 E 在不带特权信息的 OPD 中，且按位置；没有按类总量分解。
4. **Diagnosing and Mitigating Thinking Collapse in On-Policy Self-Distillation / AD-OPSD（2607.10805）** https://arxiv.org/pdf/2607.10805
   - 重叠：在 Qwen3-1.7B 上测认知密度下降，用熵门控把更新锚定到基座。
   - 差别：认知 token 只用于测量，没有按类做损失消融或分解。
5. **Why Does Self-Distillation (Sometimes) Degrade the Reasoning Capability of LLMs?（2603.24472v4）** https://arxiv.org/pdf/2603.24472v4
   - 重叠：§5.4 在 GRPO 中惩罚认知 token，复现了性能下降和回答变短。
   - 差别：因果检验不在 OPSD 中，也没有检验必要性。

```json
{
  "score": 7.6,
  "verdict": "promising_needs_revision",
  "fatal_blockers": [],
  "novelty_conclusion": "主张一（在 TH-OPSD 中用前向 KL 按类分解，分别检验认知通道的必要性与充分性）在检索范围内新颖，基线与复现路线已核实；主张二是对 2609.39118 的更干净复现，属增量。未达 experiment_ready 的原因：等价判定的 bootstrap 未计入种子间方差，3 个种子时可能误判通过；对 2609.39118 中 Qwen3-1.7B 不退化的描述有误（CoT+solution 下 34.0→30.8）；单模型、单配置；长度方向瓶颈没有对应 Claim。",
  "closest_neighbors": [
    "What Does Privileged Information Add to On-Policy Self-Distillation? (2609.20612)",
    "Diagnosing On-Policy Self-Distillation for Reasoning Language Models (2609.39118)",
    "Rethinking On-Policy Self-Distillation for Thinking Models (2607.05184)",
    "Diagnosing and Mitigating Thinking Collapse in On-Policy Self-Distillation (2607.10805)",
    "Why Does Self-Distillation (Sometimes) Degrade the Reasoning Capability of LLMs? (2603.24472v4)"
  ]
}
```
