## 结论

截至 2026-10-28：**score 6.5，verdict = promising_needs_revision**。

两个问题此前确实没人检验过：
- 在开思考 rollout（TH）、即确实发生退化的 OPSD 设置下，退化来自本题信息还是同形上下文偏移；
- 认知 token 总量通道是否必要、是否充分。

我核查了以下论文，均未覆盖这两点：2609.20612、2607.05184、2608.09228、2607.10805、2609.25623、2608.04794、Purified OPSD。基线仓库和复现入口真实存在，预算也可行。

新颖性偏增量：
- 主张一本质上是把 2609.20612 仓库里已有的两个控制脚本，从直接回答 rollout（DR）挪到 TH 下运行；
- 主张二是把 DKD 分解套到认知类 token 上，做"只保留一项"的消融。

有一个需要修订的阻断项：**I-own / I-other 的"去答案"并不成立。** 理由：
- `truncated_full_trace.py` 只去掉仓库额外拼接的 `The final answer is \boxed{...}` 后缀；
- `full_trace` 是来源数据集的原文推理轨迹，均值 4,720 token，正文自身会推出最终答案；
- L 取两条轨迹去后缀长度的较小值，而两条轨迹本来按长度配对，所以 I-own 基本保留了完整轨迹，也就保留了本题答案；I-other 则带着另一题的答案。

这样一来，brief 声称的"格式、长度、是否含答案都相同"不成立。"无本题信息"与"被错误答案误导"仍然混在一起，判定表第四格"退化需要答案本身"也无法解读。

另有两处措辞问题：
- brief 说 2609.20612 作者"明确说 TH 退化机制没有建立"，原文没有这句话，只说 marker 抑制在两种模式下同号、区分不了相反的结局；
- OP²SD 摘要的说法是"remains competitive"，不是"相当甚至更好"。

修订后值得继续。目前不应进入实验规划。

## Claim 判断

| Claim | 判断 | 最关键依据 |
|---|---|---|
| 失败条件：TH 下 OPSD 退化，DR 下获益 | 已被覆盖（作为前提成立） | 2609.20612 表 11：80.21 → 82.62（DR）/ 72.79（TH）；2607.05184 表 3：训练开思考 0.532，关思考 0.590，基座 0.591 |
| 主张一：TH 下退化需要本题信息，同形他题上下文不会造成退化 | 部分重合，需修订 | 他题参考对照只在 DR / 非思考下做过：2609.20612 表 2、OP²SD 正文；OP²SD 附录 H 在两边都开思考时只跑了本题参考。TH 下未检验，这点属实。但"去答案"没有实现，与"错误答案误导"的混淆仍在。2609.21619（Cal-OPD）和 Purified OPSD 在概念上已区分"上下文诱导的教师偏移"与"可迁移信号"，但两者都没有在 TH 下做训练对照 |
| 主张二（不必要）：只用 $L_{\text{cond}}$ 仍复现大部分下降 | 新颖（检验形式） | 2607.05184 附录 E 的 marker 掩码在无特权的 OPD 中，按位置掩码；2609.20612 的 marker 排除只在 DR 下做过；2607.10805 在思考学生、思考教师设置下按熵掩码，不按认知类。都没有在 TH 下做按类的边际/条件分解 |
| 主张二（不充分）：只用 $L_{\text{marg}}$ 时，$E$ 密度下降但准确率不降 | 新颖但检验力存疑 | 2603.24472 v4 §5.4 在 GRPO 中惩罚认知 token 可复现退化，但那是 RL 中的检验。$L_{\text{marg}}$ 在 KL 中占比极小，恒定学习率、100 步下，T2 很可能落入"M2 未通过、不可检验"一格 |
| 方法新颖性（DKD 式分解用于认知类） | 部分重合 | DKD（2203.08679）的目标类/非目标类分解在数学上同构，属于直接迁移；Purified OPSD、2608.04794 的分解只作诊断。在这个任务上首次用于必要性/充分性训练消融 |
| 基线与可复现性 | 成立 | 2026-10-28 核验 https://github.com/xiuyuz/opsd-reference-study：`launch_run.sh` 的 `ROLLOUTS=thinking`、`LOSS_HORIZON`，`train_opsd.py` 的 `apply_loss_horizon`、`--pi-override-file`，`opsd_loss.py`，两个控制脚本，`build_eval_queue.py --mode thinking` 均存在。损失截断在教师打分之前执行，所以生成上限设为 1,024 与原文 TH 损失分布等价，这个论证成立 |

## 最高近邻

1. **What Does Privileged Information Add to On-Policy Self-Distillation?**（2609.20612）https://arxiv.org/abs/2609.20612
   - 重叠：同模型、同数据、同代码、同 TH 退化设置；他题参考与截断对照都已实现，但只在 DR 下运行；marker 排除也只在 DR 下做过。
   - 差别：TH 下没有跑任何内容对照；没有按类分解 KL。
2. **Privileged Solutions or Context-Induced Teacher Behavior? Dissecting On-Policy Self-Distillation**（OP²SD，2608.09228）https://huggingface.co/papers/2608.09228
   - 重叠：直接提出"特权解答 vs 上下文诱导"这一问题，并用他题解答作教师上下文。
   - 差别：学生不开思考；附录 H 在两边都开思考时只跑了本题参考，且是单种子。
3. **Rethinking On-Policy Self-Distillation for Thinking Models**（2607.05184）https://arxiv.org/abs/2607.05184
   - 重叠：开思考训练才有害；提出 fork / 认知 token 抑制解释；附录 E 有 marker 掩码与随机子集对照。
   - 差别：掩码对照在无特权的 OPD 中；所有特权上下文内容都正确，没有错配或去答案的对照；作者自认未证明因果。
4. **Diagnosing and Mitigating Thinking Collapse in On-Policy Self-Distillation**（2607.10805）https://arxiv.org/pdf/2607.10805
   - 重叠：Qwen3-1.7B 在思考学生、思考教师设置下的 OPSD 退化，认知 token 密度，生成上限 1,024，按熵掩码梯度。
   - 差别：没有内容/偏移对照；掩码按熵而不是按认知类；没有边际/条件分解。
5. **Purified OPSD: On-Policy Self-Distillation Without Losing How to Think**（2607.02234）https://arxiv.org/pdf/2607.02234
   - 重叠：把教师信号分解为"参考诱导"与"可迁移"两部分，与主张一的问题同构。
   - 差别：分解作用于全词表，不按 token 类；没有他题或去答案对照；是否开思考 rollout 未说明。

```json
{
  "score": 6.5,
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "Claim-1 blocker: I-own/I-other '去答案' is not achieved — truncated_full_trace.py only strips the appended canonical '\\boxed' suffix, while the verbatim full_trace body (mean ~4.7k tokens) derives the answer itself; with L=min of length-paired traces, I-own keeps its own answer and I-other carries another problem's answer, so the claimed 'same format/length/answer presence' separation and the 4th decision row are not identifiable as designed",
    "Minor claim inaccuracy: 2609.20612 does not explicitly state the TH mechanism is unestablished; OP²SD abstract says 'remains competitive', not equal-or-better"
  ],
  "novelty_conclusion": "TH-setting info-vs-shift control and token-class (DKD-style) marginal/conditional necessity-sufficiency test are not covered by any found work, but the contribution is incremental (existing repo controls moved from DR to TH, plus DKD transfer); Claim-1 cleanliness currently fails due to answer content inside full_trace bodies; T2 sufficiency test risks being underpowered.",
  "closest_neighbors": [
    "What Does Privileged Information Add to On-Policy Self-Distillation? (2609.20612)",
    "Privileged Solutions or Context-Induced Teacher Behavior? Dissecting On-Policy Self-Distillation (2608.09228)",
    "Rethinking On-Policy Self-Distillation for Thinking Models (2607.05184)",
    "Diagnosing and Mitigating Thinking Collapse in On-Policy Self-Distillation (2607.10805)",
    "Purified OPSD: On-Policy Self-Distillation Without Losing How to Think (2607.02234)"
  ]
}
```
