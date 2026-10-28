## 背景

**定位关键词：** reinforcement learning with verifiable rewards；exact behavior density；bidirectional proposal；multiple importance sampling；capability acquisition

**一句话定位：** 这是在可逆、程序可验证但成功轨迹稀疏的规划任务中，用同一旧策略的两个短方向条件分布构造完整候选，并在不改变原始正向 RLVR 目标的条件下提高发现成功轨迹概率的问题。

有限 `pass@k` 不能证明 base model 对某种推理的理论概率为零，因此本文不声称证明 support 扩张。本文要验证一个更严格且可操作的命题：RL 后的单次正向策略，能否在冻结的组合泛化测试上超过同一 base model 的 best-of-8 有限预算包络。方法的新意也限定为一个窄组合：RL-PLUS 已经把外部轨迹、MIS 和 capability boundary 放在一起，TACSTaR 已在 typed workflow 中使用目标条件 proposal 与 balance heuristic，BES 已做双向轨迹重组；尚未发现已有工作在离散可逆 RLVR 中同时给出“同一模型自生成、精确可求值的双向 `q`，无拒绝固定长度采样，轨迹级 `p/m<=2`，以及对原始正向目标的无偏更新”。

## 核心 Claim

1. 令 `p_old(y|x)` 为更新前旧策略从原始起点产生长度 `L` 动作串的概率，`q_old(y|x)` 为旧策略独立产生正向前半和反向后半后经固定逆映射组成同一长度串的概率。用 `4p+4q` 分层采样、`m_old=(p_old+q_old)/2` 和 `w=p_old/m_old` 时，`w<=2`；若所有旧密度与权重停止梯度，则八项算术平均在 `theta=theta_old` 处无偏估计原始目标 `grad E_{y~p_theta}[R(y)]`，不是把 proposal 的搜索目标偷换成训练目标。
2. 方法贡献是否成立由两个互相独立的结果约束。优化层面，本方法必须在每个训练 seed 上同时优于 full-forward trajectory PG、vanilla GRPO、RL-PLUS 和 unweighted bidirectional replay；能力层面，关闭双向 proposal、oracle、verifier search 和投票后，最终策略的一次原题采样与一次结构变体采样必须联合成功，且其单侧下界超过冻结 base 在原题和变体上各 best-of-8 的单侧上界。
3. “获得新能力”只解释为上述预注册预算下、对未见更长实例与结构变体的可复用组合能力，不外推为理论 support 扩张。若只提高在线 proposal 成功率而最终独立正向策略不提高，若 unweighted replay 完全解释提升，或任一确认性比较不过线，论文必须分别报告为“搜索收益未蒸馏”“数据暴露效应”或负结果。

## 方法设计的核心思想

固定模型为 `Qwen/Qwen2.5-Math-7B-Instruct` revision `ef9926d75ab1d54532f6a30dd5e760355eb9aa4d`。动作字符序列固定为 `C=(A,...,Z,a,...,z,0,1,2,3)`，其 Qwen tokenizer ID 固定为 `(32,...,57,64,...,89,15,16,17,18)`；已直接核验该 revision，生成器只采样 token ID，不把连续字符重新送入 BPE。Hanoi 使用 `A:P1->P2, B:P2->P1, C:P1->P3, D:P3->P1, E:P2->P3, F:P3->P2`，逆置换为 `A<->B,C<->D,E<->F`。Shortest Path 使用 `A:up,B:down,C:left,D:right`，逆置换为 `A<->B,C<->D`。

Knight Swap 的 4x3 顶点为 `A1,A2,A3,B1,B2,B3,C1,C2,C3,D1,D2,D3`；14 条无向边按以下顺序冻结：`(A1,B3),(A1,C2),(A2,C1),(A2,C3),(A3,B1),(A3,C2),(B1,C3),(B1,D2),(B2,D1),(B2,D3),(B3,C1),(B3,D2),(C1,D3),(C3,D1)`。对第 `j` 条边 `(u,v)`，白方 `u->v,v->u` 分别映射 `C[2j],C[2j+1]`，黑方分别映射 `C[28+2j],C[29+2j]`，`j=0,...,13`；逆置换就是每一对相邻字符互换。由此 56 个动作与全部 inverse 唯一确定。

结构变体也在训练前固定。Hanoi 按 test index 模 5 循环 peg 置换 `(1,3,2),(2,1,3),(2,3,1),(3,1,2),(3,2,1)`，tuple 定义为 `(pi(1),pi(2),pi(3))`，token `(i->j)` 同步改为 `(pi(i)->pi(j))`。Shortest Path 按 index 模 7 循环 `rot90,rot180,rot270,mirror-LR,mirror-UD,transpose-main,transpose-anti`，其 `(A,B,C,D)` 方向-token 像依次固定为 `(D,C,A,B),(B,A,D,C),(C,D,B,A),(A,B,D,C),(B,A,C,D),(C,D,A,B),(D,C,B,A)`。Knight Swap 按 index 模 3 循环 `sigma_H(c,r)=(5-c,r)`、`sigma_V(c,r)=(c,4-r)`、`sigma_180=sigma_H o sigma_V`；动作 `(color,u,v)` 映射成 `(color,sigma(u),sigma(v))`，三者均为上述固定 knight graph 的自同构。变体 prompt 同步变换状态、目标、图和动作 legend，不改变最短长度。

每个样本只允许任务固定动作集，当前状态不改变 mask；非法动作或错误行棋方立即进入吸收失败态，但仍消费到第 `L` 个动作。每步分布是旧模型 logits 在固定动作 token 上、temperature `1.0` 的 masked softmax；`top_p=1,top_k=-1`，EOS/pad 不在动作集，外部恰在 `L` 步停止。采样、旧密度计算和训练 log-prob 共用同一个 `masked_log_softmax`。Knight 的反向 prompt 从交换完成的终态出发，以“终态 next turn 的对手”，即最后一个正向 mover，作为第一行动方。

对每题令 `h=floor(L/2)`。四条样本直接从原 prompt 按 `p_old` 采 `L` 步；另四条各自从原始起点采 `h` 步，从目标状态的反向 prompt 采 `L-h` 步，然后将反向串逆序并逐 token 取 inverse，拼成原方向候选。没有相遇、合法性、reward 或 top-k 拒绝。对任意候选 `y`，

`log p_old(y)=sum_{t=1}^L log pi_old(y_t|x,y_<t)`，

`log q_old(y)=sum_{t=1}^h log pi_old(y_t|x,y_<t)+sum_{s=1}^{L-h} log pi_old(inv(y_{L+1-s})|x_rev,inv(y_L),...,inv(y_{L+2-s}))`。

生成 batch 时把 update 前的当前参数逻辑记作 `theta_old`，在 optimizer step 前完成 generation 并缓存所需旧 log-prob；无需保留第二份物理模型。`p_old,q_old,m_old,w` 全用这些缓存、float64 log-sum-exp 计算并 detach。二元 verifier 只在恰好 `L` 步合法到目标时给 `R=1`。上一批同 `(task,L)` 桶的 64x8 reward 均值为 `b_old`，初始化为 0，并在当前 optimizer step 完成后才更新。对单个 prompt 的 loss 为

`Jhat_x(theta)=-(1/8) sum_{i=1}^8 stopgrad[w_i(R_i-b_old)] sum_{t=1}^L log pi_theta(y_it|x,y_i,<t)`，

其中四个 `y_i~p_old`、四个 `y_i~q_old`；最终 loss 是 64 个 `Jhat_x` 的算术平均。每个 fresh batch 只做一次 backward、一次 optimizer step，不重放。Unweighted ablation 的唯一差异是令八个 `w_i=1`。

## 最小实验

实现基于 Reasoning Gym commit `49b07130b3fcd12f2d064bba7c43869543a0e7e7` 的状态转移/BFS，但使用一个公共 fixed-action adapter：(A) Arbitrary-state Hanoi 在 3 pegs 上把每个 disk 的 peg assignment 作为合法状态，随机独立生成 start/goal，BFS 给最短 `L`；train/probe/dev 为 5 disks、`L=6,...,10`，test 为 6 disks、`L=11,...,16`。(B) Shortest Path 固定 train/probe/dev 为 12x12、test 为 16x16、`p_blocked=0.20`，过滤不可达项；训练长度 `6,...,10`，测试长度 `11,...,14`。(C) Knight Swap 固定完整 4x3 graph、每色 2 子，只保留可解项；train/probe/dev 长度为 `6,8,10`，test 为 `12,14,16`。对 Knight 全状态的独立枚举已得到长度桶计数 `6:72,8:284,10:696,12:1784,14:1736,16:888`，足以容纳下述互异 split。

所有 split 由候选 index `i in [0,999999]` 递增扫描，每个候选的随机源严格为 `Random(namespace_seed+i)`，namespace seed 分别为 train `0`、probe `100000`、dev `200000`、test `300000`；接受满足冻结长度桶的前若干项，并对 canonical `(task,start,goal,turn,graph)` 做集合去重，后生成 split 还排除所有早先 split。若扫描上限内 quota 不足，实验直接记为该任务不可行，不扩区间、不改难度。每桶 quota 固定如下：Hanoi train/probe/dev 各为 `128/32/32`，test 每个 `L=11,...,16` 为 160；Shortest Path train/probe/dev 各为 `128/32/32`，test 每个 `L=11,...,14` 为 240；Knight 的 train 为 `48/128/256`、probe 为 `12/32/64`、dev 为 `12/32/64`（顺序均为 `L=6,8,10`），test 每个 `L=12,14,16` 为 320。test 因而每任务恰为 960 个底层实例。probe 只报告机制量，dev 只做崩溃/格式诊断，二者都不选择任务、超参、checkpoint、decoder 或阈值。

固定训练 seeds 为 `{11,22,33}`。13 个 `(task,L)` 桶按 `H6,H7,H8,H9,H10,S6,S7,S8,S9,S10,K6,K8,K10` 循环 20 次，共 260 optimizer steps；每步从当前桶按训练 seed 洗牌后循环取 64 prompts，每题 8 条轨迹。全参数 FSDP bf16，AdamW `lr=1e-6,betas=(0.9,0.95),eps=1e-8,weight_decay=0.1`，constant LR，无 warmup，global grad clip `1.0`，每步一次更新。所有方法固定相同模型 revision、prompt、桶顺序、64 prompts、8 路动作、每路长度 `L`、`8L` 个 actor action positions、260 steps 和 final-step checkpoint；另报告实际 prompt-prefill FLOPs、墙钟与峰值显存，不声称 prefill compute 相同。

四个确认性 baseline 为：(1) full-forward trajectory PG：八条均采自 `p_old`，其余 loss/baseline 完全相同；(2) vanilla GRPO：八条正向轨迹，`use_std=false`；(3) RL-PLUS：固定官方 commit `eb4aa4d4e2d7ce206056f9d7740138bfc94fad8f`，保留 `main_rlplus_ppo`、`n=8,n_prefix=1,min_prefix_ratio=max_prefix_ratio=1,prefix_share_across_samples=false` 与 `compute_token_on_off_policy_loss` 的 token-level MIS/EBAF。唯一 baseline-specific adapter 在 `RLHFDatasetWithTarget.__getitem__` 之后直接写入 BFS oracle 的 `tgt_input_ids`，绕过 `_process_target` 的文本 BPE；公共 actor adapter 对 logits 加同一固定动作 mask。每个同 L batch 的 response length 就是 L，官方 rollout 追加的 oracle EOS 在拼回 response 时被 L 截断；官方路径仍对八路各调用 L token generation，其中一条生成结果被完整 oracle prefix 覆盖，最终八条各 L 个 action positions 进入 actor forward/backward。(4) unweighted bidirectional replay：与本方法同一 `4p+4q`，只令 `w=1`。DIVER commit `5870b47` 的固定脚本会对连续单字符输出 `.split()` 后算 BLEU-5，且 `train_diver.sh` 同时设 `rs_type=belu,neg_rs_scale=0`；因此在不改核心算法时退化，不列入确认性 baseline，只在 related work 披露。

在冻结 probe 上，初始化和 final checkpoint 各从 `p` 与 `q` 每实例各采 32 条。除成功率外，按 `(task,L)` 报告 action-logit score SNR：对样本定义 `z(y)=concat_t(e_{y_t}-pi_old(.|history_t))`，`G_p=Rz`，mixture 样本定义 `G_m=wRz`；对同样本数 N，`SNR=N||mean_i G_i||_2^2 / [(1/(N-1))sum_i||G_i-mean G||_2^2]`。这是对固定动作 logits 的无偏 reward-gradient 诊断，不冒充全参数梯度，也不参与模型或阈值选择。

最终评测只用 temperature 1、固定动作 mask 的一次采样。每个 test 底层实例分别评原题和按上述循环表指定的一个非恒等变体，pair-success 是两次采样都被 verifier 判 1。对 base，原题和变体各独立采 8 条，base pair-success 定义为“原题八条中至少一条成功且变体八条中至少一条成功”。能力证书 family 固定为 3 training seeds x 3 tasks x 2 endpoints 共 18 个单侧 Clopper--Pearson 端点，总 `alpha=0.05`，每个端点用 `alpha*=0.05/18`；九个 seed-task 比较都必须满足 RL pass@1 pair-success LCB 严格高于 base best-of-8 pair-success UCB。

确认性优越性 family 固定为 3 seeds x 4 baselines=12。每个比较在三任务共 2880 个同底层实例上，以 pair-success 的 discordant counts `b=#(main=1,base=0), c=#(main=0,base=1)` 做 one-sided exact McNemar：`p=P[Binomial(b+c,0.5)>=b]`；对 12 个 p 值做 Holm step-down、family-wise `alpha=0.05`，且每个原始效果 `(b-c)/2880` 必须为正、12 项全部拒绝。没有 bootstrap、任务挑选或 seed 平均替代。任一能力证书或确认性比较失败，就不接受主 Claim。
