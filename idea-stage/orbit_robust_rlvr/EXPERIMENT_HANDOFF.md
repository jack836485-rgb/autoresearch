# IDEA-016 实验交接

## 交接状态

- Gate：已通过；reviewer `7.9/10`，`experiment_ready`，fatal blockers `[]`。
- 正式 proposal：`FINAL_IDEA.md`；冻结审阅：`../../review-stage/orbit_robust_rlvr/FINAL_REVIEW.md`。
- 这份交接只允许实现和运行，不允许根据 probe/dev/test 结果更改核心目标、主设置、任务、seed、baseline 或统计 gate。发现合同无法实现时停止并记录，不静默替换。
- 核心 Claim：在可逆规划中，`4p+4q` 精确双向 proposal 加有界 MIS 能优化原题/固定结构变体的联合成功概率，并把探索收益蒸馏到独立正向策略。

## 1. 固定依赖

| 项目 | 固定版本/入口 |
|---|---|
| Python | `3.11.9` |
| PyTorch | `2.5.1`，CUDA generator |
| Actor | `Qwen/Qwen2.5-Math-7B-Instruct@ef9926d75ab1d54532f6a30dd5e760355eb9aa4d` |
| Environment | Reasoning Gym `49b07130b3fcd12f2d064bba7c43869543a0e7e7` |
| RL-PLUS | `eb4aa4d4e2d7ce206056f9d7740138bfc94fad8f` |
| OMEGA code | `589954335e9ca8555636770fa2c55eba6efcb4f9` |
| Main source checkouts | `reference-code/orbit_robust_rlvr/` |

实现顺序固定为：离散环境与 serializer -> 小状态空间概率/梯度测试 -> split 生成 -> 单卡一 batch smoke test -> 单 seed 短跑 -> 五方法三 seed 主实验 -> 冻结评测 -> OMEGA 描述性评测。

## 2. 动作接口

动作字符序列 `C=(A,...,Z,a,...,z,0,1,2,3)`，token IDs 为 `(32,...,57,64,...,89,15,16,17,18)`。直接采 raw token ID，不把连续字符重新 BPE。

- Hanoi：`A:P1->P2,B:P2->P1,C:P1->P3,D:P3->P1,E:P2->P3,F:P3->P2`；inverse `A<->B,C<->D,E<->F`。
- GRID：`A:up,B:down,C:left,D:right`；inverse `A<->B,C<->D`。
- Knight 顶点顺序：`A1,A2,A3,B1,B2,B3,C1,C2,C3,D1,D2,D3`。
- Knight 边顺序：`(A1,B3),(A1,C2),(A2,C1),(A2,C3),(A3,B1),(A3,C2),(B1,C3),(B1,D2),(B2,D1),(B2,D3),(B3,C1),(B3,D2),(C1,D3),(C3,D1)`。
- Knight 第 `j` 条边 `(u,v)`：白方 `u->v,v->u` 对应 `C[2j],C[2j+1]`；黑方对应 `C[28+2j],C[29+2j]`，`j=0,...,13`；inverse 交换每对相邻字符。

固定任务级 mask 在整个 $L$ 内不变。非法动作或错误行棋方进入吸收失败态但继续消费动作。每步为动作 token 上 temperature 1 的 masked softmax；`top_p=1,top_k=-1`，EOS/pad 不在动作集，外部恰在 $L$ 步停止。sampling、旧密度和训练 log-prob 必须调用同一 `masked_log_softmax`。

## 3. 结构变体与 prompt

- Hanoi 五个非恒等 peg 置换：`(1,3,2),(2,1,3),(2,3,1),(3,1,2),(3,2,1)`。
- GRID 变换顺序：`rot90,rot180,rot270,mirror-LR,mirror-UD,transpose-main,transpose-anti`；`(A,B,C,D)` 的像依次为 `(D,C,A,B),(B,A,D,C),(C,D,B,A),(A,B,D,C),(B,A,C,D),(C,D,A,B),(D,C,B,A)`。
- Knight：`sigma_H(c,r)=(5-c,r)`、`sigma_V(c,r)=(c,4-r)`、`sigma_180=sigma_H o sigma_V`；动作端点同步映射。
- 每个 split 内按 canonical key 排序得到 rank `r`，变体取 `r mod 5/7/3`；状态、目标、图和 legend 全部同步变换。

System 精确字符串：

```text
You are a deterministic planner. Follow the action-code interface.
```

User 精确八行：

```text
TASK={HANOI|GRID|KNIGHT}
STATE={json}
GOAL={json}
TURN={NONE|w|B}
GRAPH={json|null}
ACTION_CODES={json}
HORIZON={L}
Return exactly HORIZON action-code tokens and no other token.
```

JSON 使用 `json.dumps(obj,sort_keys=True,separators=(",",":"),ensure_ascii=True)`；messages 经固定 actor revision 的 `apply_chat_template(tokenize=True,add_generation_prompt=True)` 一次编码。Hanoi state/goal 按 disk 从小到大存 peg 整数数组；GRID 坐标为数组、graph 为行优先 `O/X` 字符串数组；Knight state/goal 为键 `B,w` 的排序顶点数组对象，graph 的键和邻居均字典序排序。反向 prompt 交换 state/goal；Knight TURN 设为 forward terminal next-turn 的对手。

## 4. 数据生成合同

每个 split 对 `i=0,...,999999` 单遍扫描，`rng=random.Random(namespace_offset+i)`；offset 为 train `0`、probe `10000000`、dev `20000000`、test `30000000`。候选生成后以 BFS 计算最短距离并路由到相应未满桶；不属于目标桶、桶已满、或 canonical key 已在本 split/更早 split 中出现则跳过。canonical key 是 canonical JSON 的 `(task,state,goal,turn,graph)`。任一 quota 未在扫描预算内填满则报协议不可行。

- Hanoi：train/probe/dev 固定 `n=5`，test `n=6`。按 disk 从小到大连续 `rng.randrange(3)+1` 生成 state 的 n 个 peg，再同样生成 goal；相等则拒绝。
- GRID：train/probe/dev 固定 12x12，test 固定 16x16，`p_blocked=0.20`。按行优先逐格调用 `rng.random()<0.20`，随后调用 `randint` 生成 start row/col 并覆写 open，再循环调用 end row/col 直到与 start 不同并覆写 open。
- Knight：`white=sorted(rng.sample(V,2))`；`remaining=[v for v in V if v not in white]`；`black=sorted(rng.sample(remaining,2))`；`turn=("w","B")[rng.randrange(2)]`；goal 交换白黑位置。

| Task | train | probe | dev | test |
|---|---|---|---|---|
| Hanoi | L6-10 各 128 | 各 32 | 各 32 | L11-16 各 160 |
| GRID | L6-10 各 128 | 各 32 | 各 32 | L11-14 各 240 |
| Knight | L6/8/10 为 48/128/256 | 12/32/64 | 12/32/64 | L12/14/16 各 320 |

每任务 test 均为 960。Knight 全状态计数预期：`L6:72,L8:284,L10:696,L12:1784,L14:1736,L16:888`。probe 仅诊断、dev 仅查崩溃与格式，不选择设置。已知 Hanoi probe `13/160`、Knight probe `35/108` 的 base prompt 等于某训练结构变体，故 probe 不得称 transform-disjoint；test 由更长 L 隔离。

## 5. 主方法实现

令 `h=floor(L/2)`。每侧四条样本来自完整正向 `p_old`；另四条从起点采 h 步、从交换起终点的反向 prompt 采 `L-h` 步，反向串逆序并逐 token 取 inverse 后拼接。无相遇、合法性或 reward rejection。

对每条完整 y 计算：

```text
log_p = sum_t log pi_old(y_t | x, y_<t)
log_q = sum_{t<=h} log pi_old(y_t | x, y_<t)
      + sum_{s<=L-h} log pi_old(inv(y_{L+1-s}) | x_rev,
                                inv(y_L),...,inv(y_{L+2-s}))
log_m = logaddexp(log_p, log_q) - log(2)
w = exp(log_p - log_m)
```

所有旧密度用 float64 计算。update 前完成 generation 和交叉密度 teacher forcing；`p_old,q_old,m_old,w` 全 detach。预期断言为 `0<=w<=2+tol`。

每个 family 两侧各八条独立分层样本，完整 $8\times8$ loss：

```text
pair_adv_ij = stopgrad(w0_i * w1_j * (R0_i * R1_j - c_old))
L_family = -(1/64) * sum_ij pair_adv_ij * (S0_i + S1_j)
L_batch = mean over 32 families
```

`S` 是当前 actor 对完整 y 的 token log-prob sum。`c_old` 为上次访问同 `(task,L)` 桶时，32 个 family 全部未加权 `8x8` pair reward 的算术均值；初值 0，当前 step 完成后更新。joint weight 应满足 `<=4+tol`。每个 fresh batch 只做一次 backward/step。

## 6. 训练调度与随机流

- Training seeds：`11,22,33`。
- 桶顺序：`H6,H7,H8,H9,H10,S6,S7,S8,S9,S10,K6,K8,K10`，循环 20 次，共 260 steps。
- bucket 第 v 次访问：`Random(training_seed*1000000+b*10000+v)` 打乱索引，取前 32 个底层实例；展开原题/变体并交错为 64 prompts，不重复。
- rollout seed：`1000000000000+s_idx*1000000000+step*1000000+prompt_slot*1000+sample_slot*10+branch`。`s_idx=0,1,2`，`prompt_slot=0..63`，`sample_slot=0..7`，正向完整/前半串 branch 0，反向半串 branch 1。
- 全参数 FSDP bf16；AdamW `lr=1e-6,betas=(0.9,0.95),eps=1e-8,weight_decay=0.1`；constant LR、无 warmup、global grad clip 1.0。
- 每步 64 prompts x 8 rollouts；每条恰长 L；一次更新。main/full-PG/unweighted 均按完整轨迹 token sum 后平均 family；vanilla GRPO 和 RL-PLUS 的精确 reduction 见下节。
- 公共默认：`entropy_coeff=0,KL_coeff=0,ppo_epochs=1`。microbatch 只累积同一个全局目标梯度。

## 7. 五方法冻结配置

1. `main`：第 5 节的两侧 `4p+4q`、joint MIS 和 pair product loss。
2. `full_forward_pair_pg`：同一 32 family、两侧各八条 p，复用 `8x8` pair product loss 与 `c_old`，两侧 `w=1`。
3. `vanilla_grpo`：相同 64 prompts，每 prompt 独立 8 路。`mu=mean(R)`；`s=sqrt(sum(R-mu)^2/7)`；`A=(R-mu)/(s+1e-6)`，全同奖励时 A=0。token ratio `r=exp(logpi-logp_old)`；clip `[0.8,1.2]`；loss 对 `64x8` 响应平均，每响应使用冻结的 token reduction；`ppo_epochs=1`，无同批第二次更新。
4. `rlplus_core_matched`：固定官方全八路 `core_algos.compute_grpo_outcome_advantage`，不使用 split 版本；固定 `algorithm.adv_estimator=grpo,n=8,n_prefix=1,min_prefix_ratio=max_prefix_ratio=1,prefix_share_across_samples=false,prefix_reward_weight_alpha=1,prefix_reward_weight_beta=1,use_off_policy_loss=true,off_policy_normalize=false,off_policy_strategy=RL-PLUS,off_policy_loss_impl=token,grpo_use_std=false,target_probs=null,off_min_clip=off_max_clip=all_max_clip=null,clip_ratio=0.2,clip_upper_bound=1.0,ppo_epochs=1,shuffle=false,use_sft_prefix_reward=false,use_sft_reward=false,use_sft_multitask_loss=false,use_adaptive_temperature=false,use_ppo_kl_loss=false,use_kl_loss=false,use_ref=false`。外壳设 `entropy_coeff=0,loss_remove_clip=true,loss_remove_token_mean=false`，官方 masked token mean 乘固定 L 还原每响应 token sum，再对 `64x8` 平均。公共 sampler 先生成八条 p；slot 0 覆盖为按动作 token 索引升序 BFS 的第一条最短轨迹 raw IDs，`prefix_mask[0,:]=true`、其余 false；覆盖后统一 teacher-force old log-prob。被丢弃串计生成预算，oracle 串计 actor positions。官方原始 shell 三项外壳只作非确认性敏感度。
5. `unweighted_pair_replay`：与 main 完全相同，仅令两侧 `w=1`。

每种方法每步必须记录并断言：64 actor prompts、512 条生成轨迹、`512L` 生成动作、`512L` 梯度 actor positions、一次 optimizer update。额外记录 main 的 reverse prefill 与 cross-density teacher-forcing FLOPs，不要求总 FLOPs/墙钟相等。

## 8. Probe 诊断

仅在初始化和 final checkpoint 运行。每个 probe 实例采 32 条 p 和 32 条 q。桶 b 的 pure 集合含每实例全部 32p；mixture 集合含前 16p+前16q；两边样本数均为 `N_b=32*n_b`。

定义 `z(y)=concat_t(e_{y_t}-pi_old(.|history_t))`、`G_p=Rz`、`G_m=wRz`，用 float64 计算：

```text
SNR = N_b * ||mean(G)||^2 /
      [(1/(N_b-1)) * sum_i ||G_i-mean(G)||^2]
```

分母与均值范数均 0 时 SNR=0；分母 0、均值非零时 SNR=+inf。SNR 只诊断，不参与任何选择。

## 9. 确认性评测与统计

方法 ID：main 0、full-PG 1、GRPO 2、RL-PLUS 3、unweighted 4、base 5。seed index 为 0/1/2；base 固定 0。三任务 test 依 H/G/K、桶内 canonical key 编号 `j=0..2879`。

每 checkpoint 对原题和变体各生成 rollout 0..7：

```text
seed = 9000000000
     + method_id*1000000000
     + seed_index*100000000
     + j*1000 + variant*100 + rollout
```

trained primary 只读取两侧 rollout 0 的联合成功；base 读取两侧各 best-of-8 后的联合成功。所有 checkpoint 实际消费相同 `16L` 评测动作；trained 额外七路只报 secondary pass@8。

能力 family：对每 task/seed 的 960 个指标，`eps=sqrt(log(18/0.05)/(2*960))`；`L=max(0,mean_RL-eps)`，`U=min(1,mean_base+eps)`。九项都须 `L>U`。

Baseline family：每 seed x 4 baselines，共 12 项。2880 个实例上 `D_i=X_main-X_baseline in [-1,1]`；`dbar<=0` 时 p=1，否则 `p=exp(-2880*dbar^2/2)`；12 项作 Holm step-down，FWER 0.05，且全部 `dbar>0`、全部拒绝。

两个 family 各自 alpha 0.05，不得宣称合并后仍有全局 95% simultaneous coverage。

## 10. OMEGA 描述性外部评测

数据 revisions 与切片：

- `allenai/omega-explorative@b04ae8d4757a2229e8ed65ac6a923e502d0bbb95`：`logic_gridworld_blocked/test_out` 全部 100。
- `allenai/omega-compositional@fabf91c0e85ab3ba5ec2ecfc38a2f30a6d0fadb9`：`comp_grid_chips/test` 全部 50。
- `allenai/omega-transformative@f188d999ef40f51843828d6d268c720feb3d355a`：`trans_gridworld/test` 全部 16。

保留官方 `messages`，使用固定 Qwen chat template；移除 action mask，以全词表 temperature 1、top-p 1、top-k -1、正常 EOS、最多 1024 新 token，每 checkpoint 每题八路。seed：

```text
19000000000000 + dataset_id*1000000000 + method_id*100000000
+ seed_index*10000000 + row*100 + rollout
```

scorer 取响应最后一个字面 `\boxed{...}` 的平衡花括号内容，去 ASCII 逗号和空白后必须完全匹配 `[+-]?[0-9]+`，按十进制整数和同样规范化的 `ground_truth` 比较；无完整 box 计 0。报告 rollout-0 exact accuracy 和 best-of-8。该结果不选模型、不进入主 gate；若 main 不超过 GRPO 与 full-forward PG，结论限于动作规划域。

## 11. 训练前必须通过的检查

1. Tokenizer：56 个动作字符的 raw ID 与冻结表逐一一致；decode/encode 单 token round trip 一致。失败则不能运行。
2. Environment：三个 inverse 连续执行恢复边/状态；七个 GRID 变换和三个 Knight 自同构保持邻接与 reward。失败则修任务映射。
3. PMF：在可枚举小图上分别验证 `sum_y p(y)=1`、`sum_y q(y)=1` 和 `0<=p/m<=2`。失败则无偏性 Claim 失效。
4. Gradient：小图枚举精确 `grad(mu0*mu1)`，与大量 `4p+4q` Monte Carlo loss 梯度在置信误差内一致；baseline 项均值为 0。失败则停在数学实现层。
5. Split：所有 quota、canonical 去重、最短距离和 Knight 计数复现；test L 与 train L 互斥。失败则不启动训练。
6. Budget：每方法一个 smoke step 的 prompt、trajectory、action、actor-position 和 update 计数等于冻结值。失败则比较不可归因。
7. RNG：同配置重跑完全复现；训练、主评测和 OMEGA 各 seed 域无碰撞。失败则修 seed 路由。

## 12. 结果判定

- 接受主 Claim：九项 capability certificate 与 12 项 Holm 比较全部通过。
- `q` 提升、部署 p 不提升：搜索收益未蒸馏。
- main 不优于 unweighted：数据暴露解释足够，MIS 机制未被支持。
- 只超过普通 baseline、未超过 base best-of-8：只报告概率锐化。
- 任一任务/seed/baseline gate 失败：主 Claim 不成立，不删除比较、不换 checkpoint、不调 decoder。
