## 背景

**定位关键词：** reinforcement learning with verifiable rewards；multiple importance sampling；bidirectional search；capability boundary

**一句话定位：** 这是在程序可验证的可逆规划任务中，当单向 RLVR 很少采到完整成功轨迹时，如何用概率已知的双向采样提高训练信号而不改变原始正向策略目标的问题。

## 核心 Claim

1. 有限采样不能证明 base 对某条轨迹的理论概率为零，因此本文只检验预算相对的组合能力获得：在三个预指定 held-out 任务及其结构保持变体上，训练后模型关闭双向 proposal、verifier search 和投票，以一次独立正向采样同时解出原题和变体；若每个训练 seed 在三个任务各自的 Bonferroni 校正 pair-success 下界都高于冻结 base 固定 best-of-8 的对应上界，才称为获得了 base 在该预算内未表现出的可复用组合能力。
2. 本方法的行为分布在真实 Qwen tokenizer 上完全可求值。正向策略和双向 proposal 都生成固定 `L` 个动作 token，后者不做相遇、合法性或 reward 筛选；两者等量分层采样时，使用正向概率除以二者等权混合概率的轨迹级权重，严格不超过 2，并在旧参数处无偏估计原始正向期望 reward 的策略梯度。上一批同任务同长度桶的 action-independent baseline 不改变该期望。
3. 如果双向 proposal 真能把局部能力组合成训练信号，它必须在冻结的 mechanism-probe split 上同时表现为更高的成功样本率和更高的有效成功梯度信噪比，并在确认性测试中同时超过 full-forward trajectory PG、GRPO、DIVER 与 RL-PLUS。任一前提失败、只有在线 proposal 成功而独立正向评测不提升，或 unweighted replay 完全解释结果，都推翻相应 Claim。

## 方法设计的核心思想

固定 Qwen2.5-Math-7B tokenizer；已核验其 94 个可打印 ASCII 字符全是单 token。Hanoi 的动作集固定为 6 个有向 peg move，Shortest Path 固定为 4 个方向，Knight Swap 固定为完整 4x3 棋盘上 56 个“颜色、起点、终点”有向 move；每项动作在整个任务族中映射到同一个 token，逆动作就是预先登记的 token 置换。模型每一步只在该任务的固定动作 token 集合上以 temperature 1 的 masked softmax 采样；不按当前状态屏蔽非法 move，非法 move 使 verifier 进入吸收失败态。外部在恰好 `L` 个动作后停止，EOS 不在动作空间，top-p/top-k 全关闭。训练和 teacher forcing 调用同一个 masked-log-softmax 函数，因此没有 exact-L 条件概率或隐藏重归一化。

对每题令切点为向下取整的 `L/2`。每批产生 4 条原 prompt 下的完整正向轨迹；另产生 4 对半轨迹，每对由旧模型从起点生成前半、从目标状态和正确反向 turn 生成后半，再把反向 token 串逆序并逐 token 取逆，组成原始方向的长度 `L` 候选。所有候选都保留；deterministic verifier 从原始起点执行，非法或未到目标为 0，合法到达为 1。对任意候选都能用同一 masked policy 计算正向概率；双向概率等于前半 prompt 概率与反向后半 prompt 概率之积。二者的等权 mixture 给出轨迹级 balance weight，loss 只对原始完整正向 prompt 下的 `L` 个 token 求 log-prob；每个 fresh batch 只作一次 optimizer update。相对 RL-PLUS，核心差异不是使用 MIS，而是 `q` 由同一模型的可逆半轨迹生成、行为概率已知、权重是完整轨迹级且不需要 external demonstration 或未知行为策略代理。

## 最小实验

使用 Reasoning Gym commit `49b07130b3fcd12f2d064bba7c43869543a0e7e7` 的三个共同主要任务：(A) Tower of Hanoi 固定 3 pegs，train 为 3--5 disks、test 为 6 disks，`L=2^n-1`，变体是 peg 标签置换；(B) Shortest Path 过滤 BFS 不可达实例，train 最短路 6--10、test 11--14，变体是网格旋转/反射并同步重映射方向；(C) Knight Swap 只取可解实例、每色 2 pieces，train 最短解 4--10、test 11--16，公开 BFS `num_steps` 为 `L`，反向初始 turn 固定为终态 turn 的相反方，也就是最后一个正向 mover，变体把公开 adjacency-list 的节点标签整体置换。公开 oracle path 只给 RL-PLUS baseline；其他 RL 方法只看到状态、目标、动作 legend 和 `L`。实例 namespace 固定为 train seed `0`、probe `100000`、dev `200000`、test `300000`，对应索引区间互不重叠；probe 只检验预先声明的机制前提，不选择任务、阈值、decoder 或 checkpoint。

固定 3 个训练 seeds、每题 8 条轨迹、AdamW、学习率、batch、单 batch 单更新、累计生成动作 token、参与反向传播的动作 token、训练 prompt 数和 optimizer steps。比较 full-forward trajectory PG、vanilla GRPO、DIVER、RL-PLUS、unweighted bidirectional replay 与本方法。DIVER 固定 https://github.com/NJU-RL/DIVER/tree/5870b47c695abdfc3a29b7a50c4b329ba7e4be06 的 `train_diver.sh`、`div_coeff=0.1` 和 `RewardManager`。RL-PLUS 固定 https://github.com/YihongDong/RL-PLUS/tree/eb4aa4d4e2d7ce206056f9d7740138bfc94fad8f 的 `exp_scripts/train_RL-PLUS.sh`、`main_rlplus_ppo` 与 `compute_token_on_off_policy_loss`，通过其公开 parquet `target` 字段给同一动作码 oracle path，保留官方 `n_prefix=1`、完整 prefix、MIS/EBAF 及方法系数。所有方法共享模型、动作 sampler、二元 verifier、训练实例和 final-step checkpoint；dev 不选 checkpoint，评测固定 temperature 1 的单次 masked-action sampling。每任务测试 1000 个底层实例及一个预先按索引循环指定的变体。对每个 seed，主方法与四个确认性 baseline 的三任务等权 pair-success 差做按任务分层的 paired bootstrap，12 个单侧比较统一 Holm 校正并全部要求大于 0；unweighted replay 只作机制归因。能力证书在三个任务分别使用 Bonferroni 校正的单侧区间，并要求每个 seed 的 pass@1 下界高于冻结 base best-of-8 上界。任何一项失败就按预注册负结果报告。
