# 最终审查汇总（Q001，未通过，用户决定换方向）

- 日期：2026-11-03；Reviewer 调用 1 / 19（常规，Opus 5.5 high）；终态 `rejected_no_viable_candidate`

| Call | 候选 | 总分 | 重要性 / 新颖度 / 有效性 | 可行性 | Verdict |
|---|---|---|---|---|---|
| 1 | IDEA-002 latent 内容效应随显式 CoT 收益增大 | 4.5 | 6 / 5 / 6.5 | pass | needs_rethink |

**未通过原因：**
- 2610.21182 已用任务性质调和了"占位符"与"依赖内容"两类报告的分歧。
- "CoT 收益"这个预测变量与"是否数学/符号任务"共线（Sprague 等），没有给出两者预测不同的情形。
- 在低 CoT 收益一端，"没有内容可压缩"这个平凡零假设给出相同的预测。
- 漏掉了 2602.08783（ICML 2026）：它已在 CommonsenseQA、StrategyQA 上对 Coconut、CODI 做逐步干预。

**可复用事实：**
- HF 上有 thomas-ferraz 发布的 Llama-3.2-1B Pause 与 Coconut 权重（审阅者检索确认）。
- CODI 发布了 CommonsenseQA 与 StrategyQA 的 CoT 增广数据。
- 2604.04902 发现：在 Llama-1B 上，用均值 latent 替换只伤 GSM8k（−5.8），不伤 ProntoQA 和 ProsQA。
