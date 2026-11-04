# 最终审查汇总（RSI Q003，未通过；剩余预算未用）

- 日期：2026-11-03。Reviewer 调用 3 / 18，都是常规调用（Opus 5.5，effort high）。终态 `rejected_no_viable_candidate`。

| Call | 候选 | 总分 | 重要性 / 新颖度 / 有效性 | 可行性 | Verdict |
|---|---|---|---|---|---|
| 1 | IDEA-002 递归增益三分解（STOP、Promptbreeder） | 5.5 | 6.5 / 5.5 / 5.5 | pass | promising_needs_revision |
| 2 | IDEA-004 统计纪律类编辑移植（DGM-H） | 4.0 | 6 / 5 / 4 | fail | needs_rethink |
| 3 | IDEA-005 坏起点修复混杂 | 4.8 | 5.5 / 5 / 6 | pass | needs_rethink |

## 为什么没有通过
- 关于 harness 级 RSI 评测的审计，2026 年 7–10 月已经很密：审计论文 2610.27610（提出交换测试，讨论状态依赖与天花板收缩）、HDA 2610.22466、2607.12227、Winner's Curse 2610.09239。三个候选最后都落成"给某篇论文补一个对照"。
- 已有正面递归证据的系统（Hyperagents/DGM-H、MetaRSI）只能用强 API 模型驱动。2609.17817 报告，gpt-oss-120b、Qwen3.5-397B、DeepSeek V4 Pro 都驱动不了 Hyperagents，用户的 8×A100 在这里发挥不了作用；1000 元 API 只够 1–2 次完整运行。

## 可复用事实（均已核验）
- Hyperagents 的三个源域，初始 agent 都在约 0 分，原因包括接口或格式失败（p.7、p.9）；作者自承"早期改进有一部分是在学习任务接口"。
- IMO 批改上，单次调用的静态 ProofAutoGrader 得 0.670，迁移 meta agent 得 0.630。
- Winner's Curse：所测接受规则在整次运行上都没有胜过贪心；用 16 个选择样本时，选择集分数比留出准确率高出 13–20 点。
- 一次 Hyperagents 运行（100 次迭代）约需 8360 万 token（附录 D.2）。
