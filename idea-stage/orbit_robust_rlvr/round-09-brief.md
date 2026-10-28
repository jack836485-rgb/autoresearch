## 背景

**定位关键词：** reinforcement learning with verifiable rewards；exact behavior density；bidirectional proposal；multiple importance sampling；distribution-free capability certificate

**一句话定位：** 这是在可逆、程序可验证但成功轨迹稀疏的规划任务中，用同一旧策略的两个短方向条件分布构造完整候选，在不改变原始正向 RLVR 目标的条件下改善探索，并严格检验该收益能否内化为脱离搜索的独立能力。

有限 `pass@k` 不能证明 base model 对某种推理的理论概率为零，本文因此不声称证明 support 扩张，而检验一个预算相对且可证伪的命题：RL 后的单次正向策略，能否在未见更长实例及其结构变体上超过同一 base model 的 best-of-8 包络。新意限定为窄组合：RL-PLUS 已把外部轨迹、MIS 和 capability boundary 放在一起，TACSTaR 已在 typed workflow 中使用目标条件 proposal 与 balance heuristic，Forward-Backward RL 与 BES 已使用反向目标端轨迹；尚未发现已有工作在离散可逆 RLVR 中同时给出“同一模型自生成、精确可求值的双向 `q`，无拒绝固定长度采样，轨迹级 `p/m<=2`，以及对原始正向目标的无偏更新”。

## 核心 Claim

1. 令 `p_old(y|x)` 为更新前旧策略从原始起点产生长度 `L` 动作串的概率，`q_old(y|x)` 为旧策略独立产生正向前半和反向后半后经固定逆映射组成同一长度串的概率。用 `4p+4q` 分层采样、`m_old=(p_old+q_old)/2` 和 `w=p_old/m_old` 时，`w<=2`；若所有旧密度与权重停止梯度，则 batch 算术平均在 `theta=theta_old` 处无偏估计原始目标 `grad E_{y~p_theta}[R(y)]`，没有把 proposal 的搜索目标偷换成训练目标。
2. 优化层面的 Claim 要求本方法在每个训练 seed 上同时优于 full-forward trajectory PG、vanilla GRPO、RL-PLUS 和 unweighted bidirectional replay。能力层面的 Claim 要求关闭双向 proposal、oracle、verifier search 和投票后，最终策略的一次原题采样与一次结构变体采样联合成功，并以对独立非同分布 Bernoulli 指标有效的 Hoeffding 下界超过 base 原题/变体各 best-of-8 的 Hoeffding 上界。
3. “获得新能力”只解释为上述预注册预算下、对未见更长实例与结构变体的可复用组合能力，不外推为理论 support 扩张。若只提高在线 proposal 成功率而最终独立正向策略不提高，若 unweighted replay 完全解释提升，或任一确认性比较不过线，分别报告为“搜索收益未蒸馏”“数据暴露效应”或负结果。

## 方法设计的核心思想

固定 `Qwen/Qwen2.5-Math-7B-Instruct` revision `ef9926d75ab1d54532f6a30dd5e760355eb9aa4d`。动作字符序列固定为 `C=(A,...,Z,a,...,z,0,1,2,3)`，token IDs 为 `(32,...,57,64,...,89,15,16,17,18)`；生成器直接采 token ID，不把连续字符重新 BPE。Hanoi 使用 `A:P1->P2,B:P2->P1,C:P1->P3,D:P3->P1,E:P2->P3,F:P3->P2`，inverse 为 `A<->B,C<->D,E<->F`。Shortest Path 使用 `A:up,B:down,C:left,D:right`，inverse 为 `A<->B,C<->D`。

Knight Swap 的顶点顺序为 `A1,A2,A3,B1,B2,B3,C1,C2,C3,D1,D2,D3`，边序固定为 `(A1,B3),(A1,C2),(A2,C1),(A2,C3),(A3,B1),(A3,C2),(B1,C3),(B1,D2),(B2,D1),(B2,D3),(B3,C1),(B3,D2),(C1,D3),(C3,D1)`。第 `j` 条边 `(u,v)` 的白方 `u->v,v->u` 映射 `C[2j],C[2j+1]`，黑方映射 `C[28+2j],C[29+2j]`，`j=0,...,13`；inverse 是每对相邻字符互换。Hanoi 的五个非恒等变体 `(pi(1),pi(2),pi(3))` 固定为 `(1,3,2),(2,1,3),(2,3,1),(3,1,2),(3,2,1)`。Shortest Path 的七个变体按 `rot90,rot180,rot270,mirror-LR,mirror-UD,transpose-main,transpose-anti` 排列，`(A,B,C,D)` 的像依次为 `(D,C,A,B),(B,A,D,C),(C,D,B,A),(A,B,D,C),(B,A,C,D),(C,D,A,B),(D,C,B,A)`。Knight 的三个变体为 `sigma_H(c,r)=(5-c,r)`、`sigma_V(c,r)=(c,4-r)`、`sigma_180=sigma_H o sigma_V`；动作端点同步映射。test index 分别模 5、7、3 循环，prompt 的状态、目标、图和 legend 一并变换。

Prompt 只有一个固定序列化入口。system 字符串精确为 `You are a deterministic planner. Follow the action-code interface.`；user 字符串依次为七行 `TASK={HANOI|GRID|KNIGHT}`、`STATE={json}`、`GOAL={json}`、`TURN={NONE|w|B}`、`GRAPH={json|null}`、`ACTION_CODES={json}`、`HORIZON={L}`，再接第八行 `Return exactly HORIZON action-code tokens and no other token.`。所有 JSON 使用 Python `json.dumps(obj,sort_keys=True,separators=(",",":"),ensure_ascii=True)`；messages 经上述固定 revision 的 `apply_chat_template(tokenize=True,add_generation_prompt=True)` 一次编码。Hanoi state/goal 是按 disk 从小到大排列的 peg 整数数组；GRID state/goal 是坐标数组，graph 是行优先的 `O/X` 字符串数组；Knight state/goal 是键为 `B,w`、值为排序顶点数组的对象，graph 是键和邻居都字典序排序的 adjacency object。反向 prompt 使用同一 serializer，只交换 state/goal；Knight 的 TURN 设为 forward terminal next-turn 的对手，即最后一个正向 mover。

每题的 mask 在整个长度内固定，非法动作或错误行棋方进入吸收失败态但仍消费到第 `L` 个动作。每步分布是动作 token 上 temperature `1.0` 的 masked softmax，`top_p=1,top_k=-1`，EOS/pad 不在动作集，外部恰在 `L` 步停止；sampling、旧密度和训练 log-prob 共用同一 `masked_log_softmax`。

令 `h=floor(L/2)`。每题四条样本从原 prompt 按 `p_old` 采 `L` 步；另四条各自从起点采 `h` 步、从目标反向 prompt 采 `L-h` 步，将反向串逆序并逐 token 取 inverse 后拼接。所有串保留，不按相遇、合法性或 reward 筛选。对任意 `y`，

`log p_old(y)=sum_{t=1}^L log pi_old(y_t|x,y_<t)`，

`log q_old(y)=sum_{t=1}^h log pi_old(y_t|x,y_<t)+sum_{s=1}^{L-h} log pi_old(inv(y_{L+1-s})|x_rev,inv(y_L),...,inv(y_{L+2-s}))`。

update 前完成 generation 以及计算交叉密度所需的额外 teacher-forced pass，并缓存旧 log-prob；`p_old,q_old,m_old,w` 全用 float64 log-sum-exp 计算并 detach。恰好 `L` 步合法到目标时 `R=1`。`b_old` 是上一次访问同 `(task,L)` 桶时的 `64x8` reward 均值，初始 0，当前 step 完成后才更新。单题 loss 为 `Jhat_x=-(1/8)sum_i stopgrad[w_i(R_i-b_old)]sum_t log pi_theta(y_it|x,y_i,<t)`，batch loss 是 64 个 `Jhat_x` 的平均；每个 fresh batch 仅一次 backward 和 optimizer step。Unweighted ablation 唯一差异是 `w=1`。

## 最小实验

环境使用 Python `3.11.9` 的 `random.Random(int)` 与 Reasoning Gym commit `49b07130b3fcd12f2d064bba7c43869543a0e7e7` 的转移/BFS。每个 split 对 `i=0,...,999999` 只扫描一遍，RNG seed 固定为 `namespace_offset+i`，offset 为 train `0`、probe `10000000`、dev `20000000`、test `30000000`。候选生成后计算 BFS 最短长度并路由到对应未满 quota；不符合桶、桶已满或 canonical key 已出现在本 split/更早 split 就跳过，所有桶满时停止。canonical key 是 canonical JSON 的 `(task,state,goal,turn,graph)`，直接字符串集合比较，不使用近似去重。扫描耗尽仍未满则任务记为不可行，不改规则。

Hanoi 候选固定 `n=5`（train/probe/dev）或 `n=6`（test）：按 disk 从小到大连续调用 `rng.randrange(3)+1` 共 `n` 次得到 state，再调用 `n` 次得到 goal；二者相等则拒绝。每 peg 内 disk 顺序由大小唯一确定。GRID 候选固定 12x12 或 16x16、`p_blocked=0.20`：按行优先连续调用 `rng.random()<0.20` 生成每格，随后依次调用 `randint` 生成 start row/col 并覆写为 open，再循环调用 end row/col 直到不同并覆写为 open；其顺序与固定 Reasoning Gym `_get_grid` 一致。Knight 候选使用固定 12 顶点：`white=sorted(rng.sample(V,2))`，`remaining=[v for v in V if v not in white]`，`black=sorted(rng.sample(remaining,2))`，`turn=("w","B")[rng.randrange(2)]`，goal 固定交换白黑位置。

桶与 quota 不变：Hanoi train/probe/dev 在 `L=6,...,10` 每桶 `128/32/32`，test 在 `L=11,...,16` 每桶 160；GRID train/probe/dev 在 `L=6,...,10` 每桶 `128/32/32`，test 在 `L=11,...,14` 每桶 240；Knight train 在 `L=6,8,10` 为 `48/128/256`，probe/dev 各为 `12/32/64`，test 在 `L=12,14,16` 每桶 320。每任务 test 均为 960。Knight 全状态计数已独立枚举为 `6:72,8:284,10:696,12:1784,14:1736,16:888`。probe 只报告机制，dev 只查崩溃/格式，不选择任何实验项。

固定训练 seeds `{11,22,33}`。13 个桶按 `H6,H7,H8,H9,H10,S6,S7,S8,S9,S10,K6,K8,K10` 循环 20 次，共 260 steps。第 `v` 次访问 bucket `b` 时，用 `Random(training_seed*1000000+b*10000+v)` 打乱该桶 canonical-key 排序后的 index；不足 64 的桶反复拼接同一 permutation，取前 64。每题 8 条轨迹。自定义 action sampler 的每个随机流 seed 为 `1000000000000+s_idx*1000000000+step*1000000+prompt_slot*1000+sample_slot*10+branch`，其中 `s_idx in {0,1,2}`，`sample_slot=0,...,7`，完整/正向半串 `branch=0`，反向半串 `branch=1`；所有方法共享这一公式与 PyTorch `2.5.1` CUDA generator。全参数 FSDP bf16，AdamW `lr=1e-6,betas=(0.9,0.95),eps=1e-8,weight_decay=0.1`，constant LR、无 warmup、global grad clip `1.0`。每步 64 prompts、8 路长度 `L` 动作、`8L` actor positions、一次更新，固定 final-step checkpoint；另报 prefill FLOPs、墙钟和显存，不声称 prefill 相等。除下面明确列出的 advantage 与 proposal/weight 外，main、full-PG、GRPO 和 unweighted 四条公共入口都设 `entropy_coeff=0,KL_coeff=0,ppo_epochs=1`、不做 clip、不取 token mean，先对每条响应的 `L` 个 log-prob 求和，再对 `64x8` 条响应取算术平均；由显存引起的 microbatch 切分只累积同一个全局平均梯度。

确认性 baseline 的实际目标逐一冻结。(1) Full-forward trajectory PG 每题采八条 `p_old`，复用 main 的滞后一访问 `b_old`、完整轨迹求和与 `1/(64x8)` reduction，令 `w=1`；当前 step 后更新同一个桶级 baseline。(2) GRPO 每题采八条 `p_old`，令 `A_xi=R_xi-(1/8)sum_j R_xj`，`use_std=false`；loss 精确为 `-(1/(64x8))sum_xi A_xi sum_t log pi_theta(y_xit|x,y_xi,<t)`。因为 fresh batch 只在 `theta_old` 做一次 actor pass 和一步更新，所以 PPO ratio 初值为 1；实现直接关闭 clip，避免引入无效配置自由度。(3) Unweighted replay 与 main 共用 `4p+4q`、`b_old` 和相同 reduction，唯一差异是 `w=1`。

(4) 确认性近邻记为 `RL-PLUS-core-matched`，固定官方 commit `eb4aa4d4e2d7ce206056f9d7740138bfc94fad8f` 的 `compute_grpo_outcome_advantage_split` 与 `compute_token_on_off_policy_loss`：`n=8,n_prefix=1,min_prefix_ratio=max_prefix_ratio=1,prefix_share_across_samples=false,prefix_reward_weight_alpha=1,use_off_policy_loss=true,off_policy_normalize=false,off_policy_strategy=RL-PLUS,off_policy_loss_impl=token,grpo_use_std=false,target_probs=null,off_min_clip=off_max_clip=all_max_clip=null`。为匹配公共梯度尺度，明确覆盖官方 shell 的三项训练外壳：设 `entropy_coeff=0,loss_remove_clip=true,loss_remove_token_mean=false`，再把返回的 masked token mean 乘当前固定 `L`，得到每响应 token-sum 后对 `64x8` 响应取平均；KL 仍为 0。这只保留 RL-PLUS 的 token ratio、on/off prefix mask 与 EBAF，排除 entropy 和 reduction 尺度作为混杂。官方原始 `entropy_coeff=0.001,loss_remove_token_mean=true,loss_remove_clip=true` 配置另作非确认性敏感度运行，不进入 12 项 gate。

RL-PLUS 不再调用 vLLM。它与其余方法使用同一 masked PyTorch sampler 和上述逐轨迹 CUDA generator，先实际生成八条长度 `L` 的 `p_old`；随后在进入 `DataProto` 前，把 slot 0 响应覆盖为 BFS oracle 的 `L` 个原始 token IDs，并置 `prefix_mask[0,:]=true`、其余七槽为 false。BFS 按动作表 `C` 中的 token 索引升序扩展，取第一个最短路径；训练题最短距离就是 `L`，不附加 EOS。覆盖后的八条响应由 actor 在 update 前统一 teacher-force 得到 `old_log_prob`，再进入上述两个官方核心函数；slot 0 被丢弃的模型串仍计入 `8L` 生成动作预算，覆盖后 oracle 与七条模型串共 `8L` actor positions。该 adapter 精确替代 `rlplus_vllm_rollout.py` 的采样层，不修改 advantage、token MIS/EBAF 或 actor update。DIVER commit `5870b47` 只证明其公开固定命令在本单字符接口上退化，因此不作为确认性实现；不据此声称 DIVER 方法思想不适用。

Probe 在初始化和 final checkpoint 对每实例各采 32 条 `p` 与 32 条 `q`；报告两者成功率。对含 `n_b` 个 probe 实例的桶 `b`，pure 集合 `P_b` 含每实例全部 32 条 `p`，mixture 集合 `M_b` 含同一实例前 16 条 `p` 加前 16 条 `q`，故两边唯一的样本数都是桶级 `N_b=32n_b`。定义 `z(y)=concat_t(e_{y_t}-pi_old(.|history_t))`、`G_p=Rz`、`G_m=wRz`，分别在 `P_b/M_b` 上以 float64 计算 `SNR=N_b||mean G||_2^2/[(1/(N_b-1))sum_i||G_i-mean G||_2^2]`。若迹方差分母为 0 且均值范数也为 0，SNR 定义为 0；若分母为 0 但均值范数大于 0，定义为 `+inf`。该量只作 action-logit 诊断，不参与选择。

评测使用固定动作 mask、temperature 1。方法编号固定为 main 0、full-PG 1、GRPO 2、RL-PLUS 3、unweighted 4、base 5；seed index 为 0/1/2，base 固定为 0。将三任务 test 依 H/G/K 与桶内 canonical key 顺序编号 `j=0,...,2879`。每条 response 使用独立 CUDA generator seed `9000000000+method_id*1000000000+seed_index*100000000+j*1000+variant*100+rollout`，其中 `variant=0/1`，main/baselines 的 rollout=0，base 的 rollout=0,...,7；这些区间不重叠。每个底层实例的 pair-success `X_i` 是原题与其循环变体都成功；base 的 `X_i` 是原题八条至少一条成功且变体八条至少一条成功。

能力推断条件于固定 checkpoint 和固定 960 题，仅把独立 decode 视为随机；题间成功率允许任意异质。对任一 task/seed，`X_i in [0,1]` 独立，令 `eps=sqrt(log(18/0.05)/(2*960))`，RL 下界 `L=max(0,mean(X_RL)-eps)`，base 上界 `U=min(1,mean(X_base)+eps)`。18 个预指定单侧 Hoeffding 端点经 union bound 具有至少 0.95 联合覆盖；九个 task/seed 都须 `L>U`。

确认性比较 family 为 3 seeds x 4 baselines=12。每项在 2880 个固定实例上令 `D_i=X_i^main-X_i^baseline in [-1,1]`；不同 i 的评测流独立但分布可不同。检验 `H0:(1/2880)sum_i E[D_i]<=0`，若 `dbar<=0` 则 `p_H=1`，否则用 Hoeffding-valid `p_H=exp(-2880*dbar^2/2)`；对 12 个 `p_H` 做 Holm step-down、family-wise alpha 0.05，并要求 12 项原始 `dbar>0` 且全部拒绝。该推断不使用 binomial 同质性、Poisson-binomial 近似或匹配对交换性。任一证书或比较失败即不接受主 Claim。
