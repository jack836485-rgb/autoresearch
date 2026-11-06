# 审查记录

- Call 1（常规，effort high）：IDEA-002，6.0/10，promising_needs_revision，贡献三项 {'importance': 6.0, 'novelty': 7.0, 'effectiveness': 5.0}，可行性 pass，Gate 结果 failed。主贡献是零历史权重的换锚点 old-logit 估计：偏差在当前权重上测，陈旧度只在推理端测。新意清楚，未检索到相同做法。重要性受限：2605.12070 中 PPO-EWMA 与 Snapshot 只差 1-4 点，增量价值主要在大版本差和跨版本部分 rollout，目前缺量化证据。有效性的关键假设（逐 token 数值偏差随权重平滑、版本间高度相关）没有直接证据：2610.40945 只显示平
- Call 2（常规，effort high）：IDEA-005，5.0/10，needs_rethink，贡献三项 {'importance': 6.0, 'novelty': 5.5, 'effectiveness': 6.0}，可行性 pass，Gate 结果 failed。主贡献：在异步 agentic RL 中把精确 old logits 的收益归因为'生成版本作裁剪参考'加'中心化去漂移'，两者都不需要 old logits，只有 MoE 重尾偏差时才需精确分解。重要性 6：给出实用判据，但 rollout logprob 作 anchor 已是 verl bypass、fully-async 的默认做法，R2 不做路由回放的设置偏人为。新颖度 5.5：拆分维度
