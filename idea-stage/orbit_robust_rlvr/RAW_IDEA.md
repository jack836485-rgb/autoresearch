# 原始想法：区分 RLVR 的能力放大与能力获得

## 用户原始判断

当前真正的问题已不再是“RL 能不能让模型做数学”，而是 RLVR 的提升究竟来自把 base model 已有但低概率的正确轨迹移到高概率区，还是来自模型获得了 base model 原先无法稳定执行的新推理能力。大样本 `pass@k`、CoT 正确性、representation-based exploration、curriculum RL、teacher-guided exploration 等工作给出了互相补充但仍不统一的答案。目标是提出一种可证伪的区分方法，并设计更可能促成后一种变化的 RL。

## 冻结的 Problem Anchor

- **底线问题：** 在有程序化 verifier 的数学与符号推理中，给出一个有限预算、统计上保守的操作性判据，区分“提高已有成功模式的采样概率”和“获得可跨问题变体复用的新能力”，并让训练目标直接优化后一种现象。
- **目标领域与设置：** 开源 7B 级语言模型的 RLVR；主验证使用可程序生成、可精确变换和验证的数学/逻辑任务，标准竞赛数学只作为后续外部迁移验证。
- **必须解决的瓶颈：** `pass@k` 会被幸运命中和采样策略影响；文本、hidden state、gradient 或 perplexity 的“新颖”并不保证出现了可复用的解题能力；有限采样也不能证明某轨迹在 base policy 的理论 support 之外。
- **计算与数据假设：** 最小验证固定 `Qwen2.5-Math-7B`、一个 8×80GB GPU 节点量级、3 个训练 seed；所有方法使用同一训练 prompt 数、总 rollout token、更新步数、最大响应长度和评测 token 预算。数据优先使用 Reasoning Gym 的程序化 generator/verifier，并用 OMEGA 的 OOD generalization split 做补充。这里不启动训练；实际资源若不足，实验规划阶段再在保持控制变量的前提下统一缩放模型和预算。
- **时间与投稿假设：** 目标是一篇以测量协议加最小训练机制为主的 ML/NLP 论文；首轮只验证一个模型规模、3--4 个可精确同构变换的任务族，不做大规模模型 scaling。
- **非目标：** 不声称有限实验能证明概率为零；不把自然语言 CoT 的表面差异等同于新策略；不依赖闭源 teacher、人工过程标注或新的预训练知识；不把结论外推到开放域推理。
- **进入实验规划的成功条件：** 一个无 fatal blocker、reviewer 分数严格高于 7.5 的候选，且其最小实验能在相同训练预算下同时比较 base、vanilla GRPO 和至少一个已核验 exploration baseline，并给出明确的支持与推翻结果。

## 已核验的争论起点

1. Yue et al., *Does Reinforcement Learning Really Incentivize Reasoning Capacity in LLMs Beyond the Base Model?*：https://arxiv.org/abs/2504.13837
2. Wen et al., *Reinforcement Learning with Verifiable Rewards Implicitly Incentivizes Correct Reasoning in Base LLMs*：https://arxiv.org/abs/2506.14245
3. Dragoi et al., *Beyond Pass@k: Breadth-Depth Metrics for Reasoning Boundaries*：https://arxiv.org/abs/2510.08325
4. Tuyls et al., *Representation-Based Exploration for Language Models*：https://arxiv.org/abs/2510.11686
5. Sun et al., *From Base Rollouts to RL Reasoning: A Budgeted Search Perspective*：https://arxiv.org/abs/2609.01274
6. Sun et al., *OMEGA: Can LLMs Reason Outside the Box in Math?*：https://arxiv.org/abs/2506.18880
