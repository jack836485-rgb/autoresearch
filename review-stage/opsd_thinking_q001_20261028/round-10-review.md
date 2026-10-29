## 结论

2026-10-28 评审：**score 8.2，verdict = experiment_ready**。

- **新颖性：** 核心动作是在训练时开思考（TH）的 OPSD 中，按认知类把前向 KL 拆成边际项与条件项，再做"只保留一项"的训练干预，借此把长度方向与准确率退化分别归到两个通道。按我的检索，目前没有工作做过这件事。
  - 最高近邻各自只占一块：位置级 marker 排除（只在 DR 下）、熵门控掩码、只作诊断的分解、GRPO 中的认知 token 惩罚、外部教师 OPD 中的 EOS 归组。
  - 去掉任何一篇近邻的名字，剩下的贡献仍然成立。它不是在给 2609.20612 补实验：$L_{\text{marg}}$ 在每个位置都起作用，位置掩码隔离不了它。
- **可行性：** 已核验仓库 `xiuyuz/opsd-reference-study`。
  - `apply_loss_horizon`、`--fork-mask-mode`、`--pi-override-file`、`--unprivileged-teacher`、`CORRECTION_MARKERS`、两个控制脚本和两份切分文件都在。
  - 损失只截取前 1,024 个补全 token。生成上限设为 1,024 时，被蒸馏前缀的分布与原文 TH 训练相同，复现成立。
  - 官方损失按（位置, 词表）逐元素截断，阈值 0.05，因此恒等式只对未截断的 T0u 成立。方案已把 T0 只作锚点，并为 T0u 设了事先检查。
  - TH 下无特权教师的 KL 恒为 0，这一点也成立：教师与学生同权重、同 prompt，且 LoRA 初始为零。
  - 所有 baseline 同领域、同任务、同代码，复现入口具体可行，预算在 2×A100 内。
- **非致命问题：**
  - 2607.10805（AD-OPSD）在 T/T OPSD 中做过熵掩码干预：Qwen3-1.7B 掩掉 top-20% 熵 token 后，认知密度回到 9.8，准确率却降到 31.4（标准 OPSD 为 33.9）。这本身就是 OPSD 内部"密度与准确率可以分离"的干预证据。所以"已有因果证据都不在 OPSD 中"这一表述不准确，主张一的结论方向已被部分预示。
  - 2609.20511 已把外部教师 OPD 中的长度膨胀归因于停止 token 不匹配，因此"至今没有工作说明长度方向由教师信号的哪一部分决定"需要限定在 OPSD 内。
  - 主张三基本是对 2609.39118 / 2609.20612 已有上下文对照的受控补全，新颖性低，但它只是次要主张。

值得继续，可以进入实验规划。

## Claim 判断

| Claim | 判断 | 最关键依据 |
|---|---|---|
| 失败条件：TH-OPSD 退化，DR 不退化 | 已被覆盖（作为前提，正确） | 2609.20612 表 11/12、2607.05184（Qwen3-4B：开思考训练 0.532 / 关思考 0.590 / 基座 0.591）的数字核对无误 |
| 长度方向在论文之间、配置之内不一致 | 部分重合，引用正确 | 2609.39118 表 4 中 Qwen3-1.7B 长度增长；2607.05184 在长预算下变短；2609.20612 的 Full Trace 视图变短、Answer Only 视图变长，对比对象是 DR 臂而非基座，方案已用"前提"格处理。"无人解释长度来源"的说法需排除 2609.20511（OPD 中的 EOS 归组） |
| 主张一：认知边际通道对准确率既不必要也不充分 | 新颖（方法），结论方向部分重合 | 没有工作在 OPSD 中按类做"只保留一项"的干预。2607.05184 附录 E 是位置级做法，且不带特权信息；2609.20612 只在 DR 下做排除；2603.24472 §5.4 的干预在 GRPO 中，且结论相反（惩罚认知 token 会降准确率）；AD-OPSD 的熵掩码已显示密度回升而准确率未回升。M1、M2、T3 能区分"非特异"与"泄漏"两种情况 |
| 主张二：长度方向由 $L_{\text{marg}}$ 承载 | 新颖 | 已核验的近邻中，没有人在两种参考视图下用分项损失来归因长度。另一种解释是停止 token 承载长度，它落在 $L_{\text{cond}}$ 内，表中已有对应的推翻格 |
| 主张三：不含答案的轨迹开头足以造成退化 | 部分重合（增量） | 2609.39118 读作前缀分布效应，但只有单种子，无关解答带答案、长度不匹配；2609.20612 有相同的控制脚本，但只在 DR 下运行。本方案的增量是去掉答案、长度匹配并用 5 个种子 |
| 定位关键词与 baseline | 成立 | on-policy self-distillation、privileged information、epistemic tokens、forward KL 都是现有文献在用的术语；T0、T4、DR、Answer Only 视图都有同仓库的公开入口 |

## 最高近邻

1. **What Does Privileged Information Add to On-Policy Self-Distillation?**（2609.20612）https://arxiv.org/abs/2609.20612 ；代码 https://github.com/xiuyuz/opsd-reference-study
   - 重叠：同代码、同模型，TH 退化，有 marker 压力分析。
   - 差别：marker 排除只在 DR 下做，且按位置进行；没有 KL 的类分解，长度方向只作观察。
2. **Rethinking On-Policy Self-Distillation for Thinking Models**（2607.05184）https://arxiv.org/abs/2607.05184
   - 重叠：发现只有开思考训练才退化；长预算下回复变短；用 fork 抑制作解释。
   - 差别：作者自认非因果；附录 E 只做了位置级 marker 损失，而且是不带特权信息的 OPD。
3. **Diagnosing and Mitigating Thinking Collapse in On-Policy Self-Distillation**（AD-OPSD，2607.10805）https://arxiv.org/abs/2607.10805
   - 重叠：T/T 设置下认知密度从 10.3 降到 7.9；用熵掩码做干预，得出密度与准确率分离的结果。
   - 差别：按熵门控，不按认知类；不研究长度。
4. **Diagnosing On-Policy Self-Distillation for Reasoning Language Models**（2609.39118）https://arxiv.org/abs/2609.39118
   - 重叠：提出前缀分布效应，TH 下长度增长，并做了熵与 token 选择干预。
   - 差别：单种子；无关解答带答案；没有按认知类的损失干预。
5. **Why Does Self-Distillation (Sometimes) Degrade the Reasoning Capability of LLMs?**（2603.24472 v4）https://arxiv.org/abs/2603.24472
   - 重叠：提出认知抑制的解释；§5.4 惩罚认知 token，结果是回复变短、准确率下降。
   - 差别：因果干预在 GRPO 中，不在 OPSD 中；没有拆分长度与准确率。

```json
{
  "score": 8.2,
  "verdict": "experiment_ready",
  "fatal_blockers": [],
  "novelty_conclusion": "No verified prior work applies a class-grouped marginal/conditional forward-KL decomposition with leave-one-term-out training in thinking-rollout OPSD to separate length direction from accuracy degradation; the closest works cover only position-level marker masking under DR or without privileged information (2609.20612, 2607.05184), entropy masking (2607.10805), diagnostic decompositions (2607.02234, 2608.04794), GRPO epistemic-token penalties (2603.24472), and EOS grouping in OPD with an external teacher (2609.20511). Non-fatal points: AD-OPSD's entropy masking already shows density/accuracy dissociation inside OPSD, so the statement that there is no causal evidence in OPSD is inaccurate; the 'no one explains length' claim should be scoped to OPSD; Claim 3 is incremental.",
  "closest_neighbors": [
    "What Does Privileged Information Add to On-Policy Self-Distillation? (2609.20612)",
    "Rethinking On-Policy Self-Distillation for Thinking Models (2607.05184)",
    "Diagnosing and Mitigating Thinking Collapse in On-Policy Self-Distillation (2607.10805)",
    "Diagnosing On-Policy Self-Distillation for Reasoning Language Models (2609.39118)",
    "Why Does Self-Distillation (Sometimes) Degrade the Reasoning Capability of LLMs? (2603.24472)"
  ]
}
```
