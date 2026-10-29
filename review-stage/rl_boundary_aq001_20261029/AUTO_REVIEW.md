# 审查记录

- Call 1（常规，effort high）：IDEA-002，5.5/10，promising_needs_revision，Gate 结果 failed。轮级 pass@k 交接诊断（锐化税付在到达段）是可证伪的新问题；Claim 1 是 Sharpening Tax 公开数据的再分析；两个修法分别是 BACo/EAD/REFT 与 PBA 的轮级组合，新意取决于能否胜过 R 早期轮提温的对照
- Call 2（常规，effort high）：IDEA-005，6.8/10，promising_needs_revision，Gate 结果 failed。多轮agent中基于pass@k的按轮基座/后训练交接诊断及分布-vs-多样性检验未见先例，具备新意；Claim 1为已发表数据再分析且受harness差异混淆；Claim 3相当于PBA/DPH-RL式基座锚定按轮位置选择，且所用策略样本KL(π‖π_B)与'丢失基座稀有分支'机制不对齐、诊断未在纯RL检查点上复现，新意边界未定。
- Call 3（常规，effort high）：IDEA-006，8.2/10，experiment_ready，Gate 结果 first_pass。No existing work localizes the large-k coverage loss of pure RL vs base to early turns of multi-turn tool agents via turn handoff, nor separates branch distribution from diversity with entropy-matched
- Call 4（复核，effort xhigh）：IDEA-006，6.5/10，promising_needs_revision，Gate 结果 confirmation_failed。Partially novel. Turn-level, environment-replayed localization of pass@k coverage loss on a pure-GRPO multi-turn agent checkpoint, together with the entropy-matched distribution-vs-diversity control, 
- Call 5（常规，effort high）：IDEA-007，7.5/10，promising_needs_revision，Gate 结果 failed。Claim 1（在多轮 agent 纯 RL 检查点上，用真实环境逐轮基座替换区分入口锁定与观察后重新锁定）在检索范围内新颖且可证伪。Claim 2 部分是 Locked at the Entrance 单轮提温无效结论的迁移。Claim 3 是 DPH-RL 前向 KL 加按轮掩码，方法新意薄且依赖 Claim 1。简报未与 DDO（2609.10052，WebShop 中段决策状态分支与覆盖）
- Call 6（常规，effort high）：IDEA-008，7.8/10，promising_needs_revision，Gate 结果 failed。The per-turn base-substitution profile that separates entrance locking from post-observation re-locking in multi-turn agent RL appears novel; no covering work found. The fix's novelty is conditional: 
