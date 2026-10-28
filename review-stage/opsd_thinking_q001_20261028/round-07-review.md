## 结论

截至 2026-10-28：**score 8.2，verdict 为 experiment_ready**。没有发现致命的新颖性、可行性或 Claim 阻断项，值得进入实验规划。

**新颖性：部分重合，但仍成立。**
- 在开思考 rollout（TH）下做"本题信息 vs 同形上下文"的内容对照，我检索到的近邻都没有做过：
  - 2609.20612 的 `configs/experiments.md` 显示，TH 只跑了 answer_only、clean_solution、full_trace 和损失窗口变体；
  - OP²SD、2608.18271、2609.25623 的学生都不开思考；
  - 2608.04794 在 think 模式下训练过，但无关解答只作为 PI Bias 的打分目标，从未当作教师上下文。
- 只训练 $L_{\text{marg}}$ 或只训练 $L_{\text{cond}}$，借此检验认知通道的必要性与充分性。这个杠杆在 OPSD 文献里没有出现：
  - 2607.05184 附录 E 是在无特权信息的 OPD 中做位置掩码；
  - 2603.24472 v4 §5.4 是在 GRPO 中改写认知 token 的优势；
  - AD-OPSD 按熵选位置并锚定到基座。

**主张一的增量有限。** 它本质上是把 2609.20612 只在直接回答设置下做过的内容对照搬到 TH 下，再加上答案过滤和等长开头。论文价值要靠主张二的分解检验和结果本身来撑。

**可行性已核实。** 仓库 https://github.com/xiuyuz/opsd-reference-study 存在，以下文件与参数和 brief 一致：
- `train_opsd.py` 中的 `apply_loss_horizon`、`--pi-override-file`、`--fork-mask-mode exclude`；
- `launch_run.sh` 中的 ROLLOUTS、TRAIN_MAX_NEW_TOKENS、LOSS_HORIZON；
- `opsd/opsd_loss.py` 中的逐元素截断 0.05；
- `data/controls/` 下的两个控制脚本。

因为损失只取前 1,024 个 token，且 rollout 在策略上逐 token 采样，把生成上限设为 1,024 后，损失的分布与原上限 20,764 时相同。所以这条低成本复现路线成立。

**不构成阻断、但需要注意的点：**
- brief 漏引了 2608.04794 在 think 模式下的训练结果：不含答案的 hint 与 skill 形式的 PI 分别使准确率下降 −5.13 和 −3.46，整段解答只降 −0.28。这与 ΔI-own 的预期直接相关。
- 主张二中"不充分"一项依赖 3 个种子下 ±1 分的等价判定，统计效力偏弱。
- 统计口径写的是"跨 3 个种子"，与主张一的 5 个种子不一致。
- 2607.05184 附录 E 的边际数值 0.00928 → 0.00853 我未能核验，抓取的正文没有渲染该表。
- 原文 TH 的下降只有单种子，但事先检查已经覆盖了这一风险。

## Claim 判断

| Claim | 判断 | 最关键依据 |
|---|---|---|
| 现有失败：TH 下 OPSD 退化，DR 下不退化 | 有据（非新颖点） | 2609.20612 表 11 中 Full Trace 在第 100 步 DR 82.62、TH 72.79，基座 80.21；2607.05184 中 Qwen3-4B 开思考训练 0.532、关思考 0.590、基座 0.591，均已核实 |
| "语义还是偏移"在 TH 下从未检验 | 成立 | 2609.20612 的他题参考与轨迹开头对照只在 DR 下做；OP²SD 附录 H 只在开思考下跑了本题参考（单种子，49.24 对 49.86）；2608.18271 与 2609.25623 的学生不开思考；2608.04794 未用无关解答训练 |
| 主张一：答案过滤、等长的本题开头与他题开头，区分本题信息与同形偏移 | 部分重合 | 对照思路沿用 2609.20612 与 OP²SD，但"TH 下同时去掉双方答案的等长开头对照"未见先例；2608.04794 的结果间接支持 I-own 会退化，brief 应纳入 |
| 主张二：用 DKD 式分解只训练一项，检验认知总量通道的必要性与充分性 | 新颖（分解本身已知） | 分解是 KL 链式法则与 DKD 的推广，无方法新颖性；但在 OPSD 中做"只保留一项"的因果检验，在 2607.05184（OPD 位置掩码）、2603.24472 §5.4（GRPO 优势改写，降幅更温和）、AD-OPSD（熵门控）、2608.04794（只做观测性归因）中都没有 |
| 基线与复现 | 成立 | 同任务、同模型、同仓库，入口与参数已核实；T4 与 DR 锚点均可用现成参数复现；新损失只需在 `opsd_loss.py` 旁新增一个函数 |

## 最高近邻

1. **What Does Privileged Information Add to On-Policy Self-Distillation?（2609.20612）**
   - 链接：https://arxiv.org/abs/2609.20612 ，代码 https://github.com/xiuyuz/opsd-reference-study
   - 重叠：同模型、同仓库、同 TH 退化设置，也有 marker 掩码，以及在 DR 下做的他题参考与轨迹开头对照。
   - 差别：TH 下没有任何内容对照，也没有按类分解训练。
2. **Privileged Solutions or Context-Induced Teacher Behavior?（OP²SD，2608.09228）**
   - 链接：https://arxiv.org/abs/2608.09228
   - 重叠：他题参考作教师上下文仍"remains competitive"，并把增益归因于上下文诱导。
   - 差别：学生不开思考；双方开思考时只跑了本题参考，单种子，作者自认无法归因。
3. **Privileged, but Biased: How PI-Conditioned Teachers Break Self-Distillation（2608.04794）**
   - 链接：https://www.alphaxiv.org/abs/2608.04794
   - 重叠：Qwen3-8B 在 think 模式下训练，不含答案的 hint 与 skill 也会退化；PI Bias Score 对无关解答约为 0；做了不确定性 marker 的损失归因。
   - 差别：无关解答只作打分目标，没有用作训练上下文；没有按类的干预训练。
4. **Rethinking On-Policy Self-Distillation for Thinking Models（2607.05184）**
   - 链接：https://arxiv.org/abs/2607.05184
   - 重叠：提出 fork 抑制解释，开思考与关思考对照，附录 E 有认知 token 掩码。
   - 差别：掩码在无特权信息的 OPD 中按位置进行；作者明确承认没有因果证明；没有他题对照。
5. **Diagnosing and Mitigating Thinking Collapse in OPSD（AD-OPSD，2607.10805）**
   - 链接：https://arxiv.org/abs/2607.10805
   - 重叠：Qwen3-1.7B，学生与教师都开思考，上限 1,024，认知密度从 10.3 降到 7.9。
   - 差别：按熵门控并锚定到基座，不按认知类，也没有内容对照，未给出代码。

```json
{
  "score": 8.2,
  "verdict": "experiment_ready",
  "fatal_blockers": [],
  "novelty_conclusion": "As of 2026-10-28, no work runs an own-problem vs other-problem content control under thinking-enabled rollouts (TH). 2609.20612, OP2SD, 2608.18271 and 2609.25623 run such controls only with direct-response or non-thinking rollouts; 2608.04794 trains in think mode but uses unrelated solutions only as scoring targets. No work causally tests the epistemic-class marginal channel by training on only one term of a class-level forward-KL decomposition. Claim 1 is incremental (it carries the 2609.20612 control into TH, with answer-filtered, length-matched openings); Claim 2 is the more novel lever. The brief should incorporate the 2608.04794 think-mode result (answer-free hint and skill PI degrade accuracy). Power for the Claim 2 'not sufficient' equivalence test (3 seeds, 1-point margin) is weak but not fatal.",
  "closest_neighbors": [
    "What Does Privileged Information Add to On-Policy Self-Distillation? (arXiv 2609.20612)",
    "Privileged Solutions or Context-Induced Teacher Behavior? Dissecting On-Policy Self-Distillation (arXiv 2608.09228)",
    "Privileged, but Biased: How PI-Conditioned Teachers Break Self-Distillation (arXiv 2608.04794)",
    "Rethinking On-Policy Self-Distillation for Thinking Models (arXiv 2607.05184)",
    "Diagnosing and Mitigating Thinking Collapse in On-Policy Self-Distillation (arXiv 2607.10805)"
  ]
}
```
