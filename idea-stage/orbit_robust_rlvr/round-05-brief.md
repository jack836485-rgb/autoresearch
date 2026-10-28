## 背景

**定位关键词：** reinforcement learning with verifiable rewards；bidirectional proposal；off-policy policy gradient；sparse-reward planning

**一句话定位：** 这是在可逆、程序可验证的长程规划中，当完整成功轨迹罕见但正反局部动作串可采时，如何用双向组合提高成功样本效率、同时仍然无偏优化原始正向策略的问题。

## 核心 Claim

1. 本文不声称有限词表 LLM 会获得 base 理论 support 之外的轨迹，只定义预注册预算下的**经验性组合能力获得**。每个任务族 500 个独立 held-out 实例各生成一个结构保持变体；训练后每个 seed 在关闭 proposal、bridge、verifier search 与投票后，对原题和变体各独立采一次，二者都成功才记 pair-success。每个 seed 的单侧 95% Clopper--Pearson 下界须高于 `0.20`；冻结 base 对每个成员固定采 8 次，温度分配为 `0.6/0.8/1.0 -> 3/3/2`，每次同一 token cap，best-of-8 pair-success 的单侧上界须低于 `0.05`。这是条件于 checkpoint、decoder、预算和测试分布的行为证书，不是零概率证明。
2. 在固定 `L` 步 canonical 动作空间中，令 `p_old(y|x)` 为旧策略从原始起点到目标的完整串分布；固定 `h=floor(L/2)`，令 `q_old(y|x)` 为同一旧策略在“起点走 h 步”prompt 下生成 `y_1:h` 的概率，乘以在“目标反向走 L-h 步”prompt 下生成 `reverse(inverse(y_h+1:L))` 的概率。行为分布为 `m_old=(p_old+q_old)/2`。不按 endpoint、合法性或 reward 拒绝任何 `q` 样本，则对 `y~m_old` 使用 stop-gradient `w(y)=p_old(y)/m_old(y)` 和动作无关的上一批 difficulty baseline `b_d`，在旧参数处有 `E_m[w(R-b_d) grad log p_old]=grad E_p[R]`，且 `0<=w<=2`。因此它不是把拼接轨迹冒充 on-policy 数据，而是一个有界 importance-sampled policy-gradient estimator。
3. 方法是否真正改善 exploration 由两个可否证量决定：在训练前冻结的 10k probe 实例上，`q` 的 verifier success 必须高于 `p`，且主 estimator 的每个有效成功梯度方差必须低于 full-forward estimator；训练后主方法须在至少两个任务族上对 full-forward policy gradient、GRPO、DIVER 与 BES 的 pair-success 取得预注册显著优势，第三族满足 `-0.02` 非劣界。否则结论是“双向 proposal 没有发现更有用的完整轨迹”或“proposal 有搜索收益但不能转成独立策略能力”，而不是新能力。

## 方法设计的核心思想

所有模型都在同一个 grammar-constrained canonical action decoder 上工作，并被要求恰好输出环境给出的最短动作数 `L`；`L` 对全部方法和 base 可见。响应 token cap `T` 只负责容纳该任务族最长 canonical 序列，与 `L` 分开记录。每个训练实例分层产生 8 个完整候选：4 个直接采自 `p_old`；另 4 个各自独立采一个长度 `h` 的正向半串和一个长度 `L-h` 的反向半串，再将后者逆序取逆后组成长度 `L` 的 `y`。不做 rejection sampling、不枚举笛卡尔积；endpoint 不相遇、含非法状态转移或未到目标的组合仍保留并令 `R=0`。`R=1` 的唯一定义是：同一 deterministic transition wrapper 从原始起点执行恰好 `L` 个动作时每步合法且终态等于目标；三个任务和所有 baseline 共用这一事件，不使用 Reasoning Gym 原有 shaped score。

对每个候选都以 teacher forcing 计算 `p_old(y|x)`；再把 `y` 在固定切点唯一拆开，以两个半程 prompt 计算 `q_old(y|x)`，所以 `m_old` 对来自任一分量的样本都可求值。loss 为 `-w(R-b_d) sum_t log p_theta(y_t|x,y_<t)`，`w` 和 `b_d` stop-gradient；每个 fresh batch 只更新一次后重新采样，避免把旧 importance ratio 跨多个 epoch 复用。`b_d` 是前一批同任务、同长度桶的加权成功率，不依赖当前动作；第一批取 0。完整 `y`、包括后半串和固定终止位置，都在原始 prompt 条件下接受直接梯度。主超参只固定 mixture 系数 `1/2`，没有 exploration bonus 系数；同时报告 `q/p` success ratio、importance-weight 分布、ESS、成功样本梯度方差和 proposal-only 在线成功率。若 `q` 不增 success 或 ESS/方差诊断恶化，停止训练并报告机制前提不成立。

## 最小实验

固定 `Qwen2.5-Math-7B`、3 个训练 seed、每题 8 个行为样本、单 batch 单更新和相同 optimizer；使用 Reasoning Gym commit `49b07130b3fcd12f2d064bba7c43869543a0e7e7` 的 Tower of Hanoi、Shortest Path、Word Ladder。三个环境的转移与逆动作已在上一轮逐文件核验：Hanoi 为合法顶盘移动及其反向，Shortest Path 为无向网格中的上下/左右逆动作，Word Ladder 为单字母替换的对称邻接。每题用公开 generator/BFS metadata 计算最短动作数 `L`，只把 `L` 而非 oracle path 给模型；训练长度分别为 Hanoi 3--4 disks、网格最短路 4--8、词梯 3--5，测试为 5--6、9--14、6--8。变体分别是 peg 标签置换、网格旋转/反射并重映射方向、交换词梯起终点。train/dev/test generator seeds 完全隔离。

比较 full-forward policy gradient、vanilla GRPO、DIVER、unweighted bridge replay、BES 与本方法。full-forward 对照共享本方法 loss/baseline/单次更新但用 8 个 `p` 样本和 `w=1`；unweighted replay共享 `4p+4q` 全部样本但令 `w=1`。DIVER 固定 https://github.com/NJU-RL/DIVER/tree/5870b47c695abdfc3a29b7a50c4b329ba7e4be06 的 `scripts/train/train_diver.sh`、`div_coeff=0.1` 和 `RewardManager`。BES 固定 https://github.com/Embodied-Minds-Lab/BES/tree/7c2696f3b5c340dfe34062df93af009cee9152bc，使用已公开的 `logical/verl/scripts/run_bes_local.sh --algo bes` 与 `bes_agent_loop.py`，把其 K&K scorer 换成同一 action wrapper，并令主/反向模型都是同一 base；所有 forward、backward、reflection/search 生成 token 都计入共同预算，若官方接口不能完成该最小适配则记为不可复现而不自写替代。每种方法同时匹配累计生成响应 token 和参与反向传播的响应 token，另报告不同 prompt prefill FLOPs；到达任一预算先停止并丢弃跨界 batch。主指标及区间按核心 Claim 逐 seed 计算；方法差用 500 个底层实例为 cluster 的配对 bootstrap，至少两族单侧 95% CI 全高于 0，第三族 CI 下界高于 `-0.02`。任何 baseline 的核心模型、decoder、`L/T`、二元 verifier、训练实例与 token 预算都不得改变。
