## 背景

**定位关键词：** reinforcement learning with verifiable rewards；bidirectional search；trajectory composition；sparse-reward exploration

**一句话定位：** 这是在可逆、程序可验证的长程推理任务中，当 base 只能产生合法局部路径却很少端到端成功时，用两个独立失败半轨迹的精确状态相遇为 RLVR 提供新组合信号的问题。

## 核心 Claim

1. 有限实验不能证明某条轨迹在 base policy 下的理论概率为零。本文只定义**组合能力获得证书**：在预注册的每个 held-out 任务族及其结构保持变体对上，训练后模型不使用桥接搜索、外部 verifier 搜索或多数投票，独立生成两条均成功的完整解，其 pair-success 单侧 95% 下界高于 `0.20`；冻结 base 在预注册 8 倍响应 token 包络下的对应上界低于 `0.05`。这只证明给定模型、预算和分布上的经验性获得。
2. 当一个 GRPO group 中所有单向完整轨迹 outcome 都为 0 时，vanilla RLVR 没有 outcome advantage；但只要至少一对全程合法的正反半轨迹在同一 canonical endpoint 相遇、且至少还有一条未相遇轨迹，双向桥接的二元 rollout reward 就有非零组内方差。它因此能强化两个真实采样到、可由 verifier 拼成完整解的局部路径，而不是奖励表面、hidden-state 或 gradient 新颖性。
3. 若这个“从失败中组合成功”的信号确实促成可复用能力，本方法应在至少两个任务族上同时超过相同正反 prompt 的 outcome-only GRPO、DIVER 和 R3L，并通过组合能力证书；第三个任务族不得显著退化。若优势只在训练时允许 bridge search 的指标上出现，或评测时独立完整求解不提升，则 Claim 被推翻。

## 方法设计的核心思想

每个任务表示成有限可逆状态图，公开 deterministic transition function 给出 `T(s,a)` 与逆动作 `a^-1`。对同一底层实例构造两个格式完全相同、只交换起终点的 prompt；每个方向各采样 8 条最长为 `H` 的 on-policy 动作序列，verifier 从头重放，任何非法动作都令该序列无效。对合法正向 rollout `f_i` 和合法反向 rollout `b_j`，只有在二者最终 canonical state 完全相同、且 `len(f_i)+len(b_j)<=H` 时，才接受桥接路径 `f_i + reverse(inverse(b_j))`；随后再从原始起点完整执行一次，终态正确才令 `bridge(i,j)=1`。单条 rollout 的 reward 是“自身已经到达该方向目标，或参与至少一条 verified bridge”这一二元值，不另加连续系数；正反方向分别做普通 GRPO group normalization。训练只更新实际 on-policy 采样的 `f_i`、`b_j`，不对拼接路径做 MLE/SFT，也不使用 generator 的 oracle path、参考 CoT、PRM、状态距离或跨 batch archive。关键控制让 outcome-only GRPO 和 DIVER 看见逐字相同的两向 prompts、各 8 rollouts、相同 `H` 和总 token，只关闭跨方向 endpoint matching。

## 最小实验

固定 `Qwen2.5-Math-7B`、3 seeds、一个 `8x80GB` 节点量级；所有 RL 方法使用相同底层题、正反 prompt 数、每方向 8 rollouts、训练与评测响应 token、更新步数和最大长度 `H`。数据固定到 Reasoning Gym commit `49b07130b3fcd12f2d064bba7c43869543a0e7e7` 的三个公开任务：(A) `reasoning_gym/games/tower_of_hanoi.py`，已核验 `_parse_move`、`_validate_move`、完整 `score_answer`，反向任务交换 start/target peg 并反转每个 move；训练 3--4 disks、测试 5--6 disks，变体为 peg 标签置换；(B) `reasoning_gym/graphs/shortest_path.py`，已核验 `_is_valid_path` 与方向序列 scorer，反向任务交换 `*`/`#` 并使用上下、左右逆动作；训练最短路 4--8、测试 9--14，变体为网格旋转/反射及方向重映射；(C) `reasoning_gym/algorithmic/word_ladder.py`，已核验词表、邻接规则和逐词 scorer，反向任务交换 start/end 并反转词链；训练最短链 3--5、测试 6--8，变体对即正向/反向题。训练只读取状态和 verifier；公开 BFS/Frame--Stewart 解只用于生成难度 split 和 oracle-trace SFT，不提供给任一 RL 方法。开发 seeds 只用来冻结各任务 `H` 及一个“base 单向完整成功率低于 0.10、但 16 条 base rollout 内 verified bridge 率非零”的难度带，test seeds 完全隔离。

比较 base 8 倍采样包络、双向 exposure-only GRPO、DIVER、R3L、oracle-trace SFT 与本方法。DIVER 固定其默认 `diver` 分支 commit `5870b47c695abdfc3a29b7a50c4b329ba7e4be06`，入口为 `scripts/train/train_diver.sh`，保持官方 `div_coeff=0.1`；只在 `verl/div_src/reward_fn.py::_select_rm_score_fn` 增加与其他方法共用的三个 scorer 分派。R3L 使用 https://github.com/shiweijiezero/R3L 的公开 7B 配置和 workflow 接口，匹配包括反思在内的总生成 token。每族评测至少 500 个 held-out 变体对；主指标是关闭 bridge 后的 pair success、pass@1、base 8 倍包络证书和按最短解长度分桶的成功曲线，训练诊断是“两个 outcome 均为 0 但 bridge 为 1”的更新比例。区间以底层实例为 cluster 做跨 seed hierarchical bootstrap，证书另用单侧 Clopper--Pearson 界。若本方法未在至少两个族显著优于三个 RL baseline、第三族不劣，或只有在线桥接成功而独立求解无提升，就按负结果报告；若 SFT 更强，则结论明确限定为双向 RL 仍不如显式完整路径监督。
