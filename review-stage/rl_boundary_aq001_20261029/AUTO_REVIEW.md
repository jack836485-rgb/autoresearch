# 审查记录

- Call 1（常规，effort high）：IDEA-002，5.5/10，promising_needs_revision，Gate 结果 failed。轮级 pass@k 交接诊断（锐化税付在到达段）是可证伪的新问题；Claim 1 是 Sharpening Tax 公开数据的再分析；两个修法分别是 BACo/EAD/REFT 与 PBA 的轮级组合，新意取决于能否胜过 R 早期轮提温的对照
- Call 2（常规，effort high）：IDEA-005，6.8/10，promising_needs_revision，Gate 结果 failed。多轮agent中基于pass@k的按轮基座/后训练交接诊断及分布-vs-多样性检验未见先例，具备新意；Claim 1为已发表数据再分析且受harness差异混淆；Claim 3相当于PBA/DPH-RL式基座锚定按轮位置选择，且所用策略样本KL(π‖π_B)与'丢失基座稀有分支'机制不对齐、诊断未在纯RL检查点上复现，新意边界未定。
- Call 3（常规，effort high）：IDEA-006，8.2/10，experiment_ready，Gate 结果 first_pass。No existing work localizes the large-k coverage loss of pure RL vs base to early turns of multi-turn tool agents via turn handoff, nor separates branch distribution from diversity with entropy-matched
