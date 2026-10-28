# 审查记录

- Call 1（常规，effort high）：IDEA-005，5.5/10，promising_needs_revision，Gate 结果 failed。问题陈述（方向冲突）有据可查，但'训练前可测的教师减学生认知 token 偏差'已被 2609.20612 的 correction pressure F_v 覆盖。F_v 在 Qwen 上普遍为负且不区分结局；2609.39118 也显示初始 KL 不能预测方向。brief 两篇都未引用。剩余新颖点是：边际质量版的 ρ、'已验证'对'可能有错'的框架翻转因果设计、只缩放认知边际并配随机类对照的 
- Call 2（常规，effort high）：IDEA-006，6.0/10，promising_needs_revision，Gate 结果 failed。As of 2026-10-28, segment-wise (thinking vs answer) loss masking and an other-problem reference control under thinking-enabled OPSD rollouts have no direct prior work, but the result only localizes ha
- Call 3（常规，effort high）：IDEA-007，6.0/10，promising_needs_revision，Gate 结果 failed。The causal marginal-vs-conditional ablation inside thinking-rollout OPSD appears unexplored, so the diagnostic experiment is novel. The decomposition is the standard KL grouping identity (DKD-style), 
