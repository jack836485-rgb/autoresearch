## Terminology and Acronym Glossary

| Term / acronym | Full name or translation | Plain-language meaning and role in this idea |
|---|---|---|
| RLVR | Reinforcement Learning with Verifiable Rewards，可验证奖励强化学习 | 用程序化 verifier 给生成轨迹二元奖励，再直接更新语言模型策略。 |
| GRPO | Group Relative Policy Optimization，组相对策略优化 | 本研究采用的标准 RLVR 对照；它在同一 prompt 的八条响应内标准化奖励。 |
| MIS | Multiple Importance Sampling，多重重要性采样 | 将正向分布和双向 proposal 的样本放在一起，并用可计算的密度比纠正分布差异。 |
| Pair-MIS-RLVR | 本 proposal 定义：paired-success MIS-RLVR | 本方法；直接优化原题与固定结构变体两次独立执行都成功的概率。 |
| $p_\theta$ | forward policy，正向策略分布 | 模型从题目初始状态出发生成恰好 $L$ 个动作的概率分布，也是部署时唯一使用的策略。 |
| $q_\theta$ | exact bidirectional proposal，精确双向提案分布 | 同一模型分别从起点和目标端生成两个固定长度半串，再经逆动作变换拼成完整候选。 |
| $m_\theta$ | deterministic-mixture distribution，确定混合分布 | $m=(p+q)/2$；它使 importance weight $p/m$ 严格不超过 2。 |
| pair success | 本 proposal 定义：跨变体联合成功 | 原题的一次独立正向执行和其结构变体的一次独立正向执行同时通过 verifier。 |
| capability certificate | 本 proposal 定义：有限预算能力证书 | 在冻结题集和采样预算下，trained policy 的单次 pair success 下界超过 base model 的 best-of-8 上界。 |
| RL-PLUS-core-matched | 本 proposal 定义：RL-PLUS 核心匹配对照 | 复用固定官方 commit 的 advantage 与 token on/off-policy 核心，同时匹配本实验的动作、数据和更新预算；不冒充官方完整 recipe。 |
| OMEGA | Out-of-distribution benchmark for mathematical reasoning | 用三个冻结子集检查动作规划域内的提升是否迁移到自然语言网格推理；只作描述性外部验证。 |

## Title

可逆规划中跨结构变体联合成功的精确双向 MIS-RLVR

**定位关键词：** reinforcement learning with verifiable rewards；multiple importance sampling；bidirectional search；compositional generalization；capability boundary

**一句话背景：** 本研究考察可验证规划中的 RLVR 能否把有限预算下的新搜索轨迹真正蒸馏进单次正向策略，并使这种提升同时迁移到同一问题的结构变体。

## 1. Introduction-Style Summary

### 1.1 Task Anchor and Minimal Scope

论文只锚定三个离散、可逆、可精确验证的规划任务：Tower of Hanoi、带障碍网格最短路和 $4\times3$ Knight Swap。模型输出固定词表上的恰好 $L$ 个动作；非法动作进入吸收失败态，只有第 $L$ 步后状态精确等于目标才奖励 1。训练只使用较短实例，确认性测试只使用未见的更长实例，并对每个实例同时评估原题和一个预先固定的非恒等结构变体。

这个范围刻意不覆盖开放式自然语言数学证明，也不声称用有限采样证明 base model 的理论 support 为零。本文的“获得能力”是一个预算相对、可证伪的操作性结论：关闭双向 proposal、oracle、投票和 verifier search 后，训练所得正向策略的一次原题采样与一次变体采样能否同时成功，并超过同一 base model 在两侧各八次采样形成的包络。

### 1.2 How Existing Methods Handle This Task

标准 GRPO 从当前策略为每个 prompt 生成一组轨迹，用组内相对奖励形成 advantage，再提高成功轨迹的概率。它擅长把已经偶尔出现的正确轨迹推向高概率区，但在二元稀疏奖励下，整组失败时没有正向学习信号。RL-PLUS 进一步把外部轨迹和 on-policy 轨迹混合，并以 token-level on/off-policy 校正扩展可训练轨迹来源。Forward-Backward RL、BES 和 TACSTaR 则分别展示了从目标端采样或使用目标条件 proposal 的价值。OT-GRPO 与 Share-GRPO 说明跨结构变体配对或共享轨迹可以改变训练信号。

这些工作分别覆盖了混合策略、反向采样、结构变体或配对，但它们没有直接解决本文的完整问题：用同一个旧语言模型构造可精确求值、无拒绝的双向完整轨迹 proposal，并对“原题和变体都正确”这一乘积目标给出有界且在旧参数处无偏的 trajectory-level MIS 梯度。

### 1.3 Bottleneck in Existing Methods

真正的瓶颈有两层。第一层是探索：当正向成功轨迹极稀疏时，普通 RLVR 很难在固定 rollout 预算内得到可用奖励；从目标端反向生成可以显著提高候选覆盖，但直接把这些轨迹当 on-policy 数据会产生偏差。第二层是目标：即使 proposal 提高了单题 reward 的采样效率，训练也可能只强化某一道题上的偶然轨迹，并没有直接要求能力跨结构变体复用。

只比较 `pass@1` 或 `pass@k` 无法拆开这两层。高 `pass@1` 可能只是概率锐化，大 `k` 下的 base model 又可能找回相同路径；反过来，直接要求理论 support 扩张又无法由有限采样证实。因此需要同时改变训练目标、保持 off-policy 校正可审计，并使用一个明确占优于 base 搜索包络的有限预算证书。

### 1.4 Our Improvement

我们训练一个只在训练期使用双向 proposal、部署时仍是普通正向语言模型的策略。每个训练 family 包含原题 $x$ 与固定结构变体 $T(x)$；训练目标不是两个单题 reward 的平均，而是两侧独立成功概率的乘积。每侧恰好采四条正向轨迹和四条双向轨迹，计算同一旧模型下的精确 $p$、$q$ 与 mixture density，再对两侧八条样本做 $8\times8$ 笛卡尔配对。

这个设计同时修复两类问题。双向 proposal 把目标端信息引入探索；MIS 权重保证这些轨迹仍在优化正向策略的目标；乘积目标只有在原题和变体两侧都提高时才增大，从训练目标层面要求可复用性。设计保持固定长度、无拒绝采样和有限动作空间，使 proposal 概率可精确求值，单侧权重不超过 2、联合权重不超过 4。

### 1.5 Experiment Setup at a Glance

最小实验固定 Qwen2.5-Math-7B-Instruct 的指定 revision，在 Reasoning Gym 固定 commit 的 Hanoi、GRID 和 Knight 环境上训练 260 步、3 个 seeds。五种方法看到同样的 64 个 actor prompts，每 prompt 生成八条长度 $L$ 的轨迹，均为每步 `512L` 生成动作、`512L` actor positions 和一次更新。确认性对照是 full-forward paired trajectory PG、vanilla GRPO、RL-PLUS-core-matched 和 unweighted paired replay。主成功条件同时要求：九个 task/seed 能力证书全部超过 base best-of-8 包络；相对四个 baseline 的 12 个 seed-level 差异均为正且通过 Holm 校正。OMEGA 的三个冻结子集只检查外部迁移，不用于选择 checkpoint 或超参数。

### 1.6 Contributions / Novelty

1. 提出一个直接优化跨结构变体联合成功概率的 RLVR 目标，而不是用文本多样性、hidden-state 距离或单题成功率作为“新能力”的代理。
2. 给出同一旧语言模型诱导的固定长度双向 proposal，以及单侧权重不超过 2、联合权重不超过 4、在旧参数处无偏的乘积目标 trajectory-MIS 更新。
3. 给出一个预算透明的能力证书和完整的控制变量协议，明确区分“proposal 找到成功轨迹”“成功轨迹被蒸馏进正向策略”和“超过 base model 有限搜索包络”三件事。

新颖性仅主张上述三者的完整组合。反向采样、balance-heuristic MIS、结构变体和 $K\times K$ 配对各自都不是本文首创。

## 2. Detailed Method Plan

### 2.1 Method Intuition

核心做法是：从起点和目标端共同寻找候选，但只奖励最终能让普通正向策略在原题与变体上同时成功的更新。

1. 从训练桶取 32 个底层实例，为每个实例生成原题和一个按 canonical rank 固定的结构变体，得到 64 个 prompts。固定映射避免在训练结果出来后挑“容易”的变体。
2. 对每个 prompt，从旧正向策略采四条完整轨迹；另采四条由正向前半串和目标端反向后半串拼成的轨迹。拼接不要求两半相遇，也不按合法性或 reward 筛选，因此 proposal 没有未知的接受率归一化常数。
3. 对所有八条轨迹同时计算旧策略下的 $p(y)$ 和 $q(y)$，用 $w(y)=p(y)/[(p(y)+q(y))/2]$ 校正双向数据。这样双向轨迹可以提供探索收益，却不会把训练目标换成 $q$ 的成功率。
4. 对原题和变体两侧的八条样本做完整 $8\times8$ 配对，只有一对轨迹都成功时 pair reward 才为 1。loss 同时包含两侧的完整正向 log-prob，因此梯度直接提高联合成功概率。
5. 每个 fresh batch 只做一次 optimizer update。推理和最终评测完全关闭 $q$，只从正向策略 $p_\theta$ 采样；这一步检验探索结果是否真正进入了部署策略。

### 2.2 Inputs, Outputs, and Assumptions

- Inputs: 固定 Qwen checkpoint；带精确状态转移、目标状态和二元 verifier 的可逆任务；每题最短路径长度 $L$；动作 token 及其 inverse permutation；结构保持变换 $T$；旧策略快照 $\theta_{\rm old}$。
- Outputs: 一个部署时只需正向 prompt 的策略 $p_\theta$；每步可审计的 $p/q/m$ log-density、importance weight、pair reward 与成本统计；冻结 test 上的能力证书和 baseline 比较。
- Assumptions: 任务动作空间有限且 inverse 已知；正向和反向 prompt 共用同一模型与固定动作 mask；所有轨迹长度固定为 $L$；$p$ 与 $q$ 在同一有限轨迹空间上可精确求值；原题和变体两侧使用独立随机流。

### 2.3 Algorithm / System Design

**任务接口与正向策略。** 模型固定为 `Qwen/Qwen2.5-Math-7B-Instruct@ef9926d75ab1d54532f6a30dd5e760355eb9aa4d`。动作字符按 `A-Z,a-z,0-3` 排列，对应 token IDs `32-57,64-89,15-18`；生成器直接采 token ID，不重新 BPE。每题使用固定任务级动作 mask、temperature 1、`top_p=1`、`top_k=-1`，EOS/pad 不在动作集，外部恰好执行 $L$ 步。非法动作进入吸收失败态但继续消费动作；采样、旧密度与训练 log-prob 共用同一个 `masked_log_softmax`。

Hanoi 的六个有向动作是 `A:P1->P2, B:P2->P1, C:P1->P3, D:P3->P1, E:P2->P3, F:P3->P2`，inverse 为 `A<->B,C<->D,E<->F`。GRID 使用 `A:up,B:down,C:left,D:right`，inverse 为 `A<->B,C<->D`。Knight 的 12 个顶点按 `A1,A2,A3,B1,...,D3` 排列，14 条无向边按固定字典序表编号；每条边为白方和黑方各分配两个方向 token，inverse 只交换相邻方向 token。完整边表和 token 构造写入实验交接文件，不能在实现时重新排序。

Prompt 只有一个 serializer。system 严格为 `You are a deterministic planner. Follow the action-code interface.`；user 依次包含 `TASK, STATE, GOAL, TURN, GRAPH, ACTION_CODES, HORIZON` 七行和 `Return exactly HORIZON action-code tokens and no other token.`。JSON 使用 `sort_keys=True,separators=(",",":"),ensure_ascii=True`，再由固定 tokenizer revision 的 chat template 编码。反向 prompt 只交换 state/goal；Knight 的回合取正向终态下一行动方的对手。

**直接能力目标。** 对原题或变体 $z$，定义

$$
\mu_\theta(z)=\mathbb E_{y\sim p_\theta(\cdot\mid z)}[R_z(y)],
\qquad
J_{\rm cap}(\theta)=\mathbb E_x[\mu_\theta(x)\mu_\theta(T(x))].
$$

其中 $R_z(y)\in\{0,1\}$ 表示轨迹是否恰在 $L$ 步合法到达目标。因为两次执行独立，乘积就是原题与变体同时成功的概率；它不是轨迹相似度或表示代理。

**精确双向 proposal。** 令 $h=\lfloor L/2\rfloor$。双向样本先从原 prompt 采前 $h$ 步，再从交换起终点的反向 prompt 采 $L-h$ 步；将反向串逆序、逐 token 取 inverse 后拼到前半串。所有样本保留。任意完整动作串 $y=(y_1,\ldots,y_L)$ 的密度为

$$
\log p_{\rm old}(y)=\sum_{t=1}^{L}\log\pi_{\rm old}(y_t\mid x,y_{<t}),
$$

$$
\log q_{\rm old}(y)=\sum_{t=1}^{h}\log\pi_{\rm old}(y_t\mid x,y_{<t})+
\sum_{s=1}^{L-h}\log\pi_{\rm old}(\operatorname{inv}(y_{L+1-s})\mid x_{\rm rev},\operatorname{inv}(y_L),\ldots,\operatorname{inv}(y_{L+2-s})).
$$

每侧固定采 `4p+4q`，等价于确定混合 $m_{\rm old}=(p_{\rm old}+q_{\rm old})/2$。以 float64 log-sum-exp 计算

$$
w(y)=\frac{p_{\rm old}(y)}{m_{\rm old}(y)}\le 2.
$$

generation 和全部交叉密度 teacher forcing 必须在 update 前完成；$p_{\rm old},q_{\rm old},m_{\rm old},w$ 全部停止梯度。

**乘积 MIS loss。** family $f$ 的两侧记为 $x_f^0=x_f$ 和 $x_f^1=T(x_f)$；每侧八条样本为 $y_{fi}^a$，其中 $a\in\{0,1\}$、$i\in\{1,\ldots,8\}$。当前策略对完整轨迹的 score sum 是

$$
S_{fi}^a=\sum_{t=1}^{L}\log\pi_\theta(y_{fi,t}^a\mid x_f^a,y_{fi,<t}^a).
$$

令 $c_{\rm old}$ 为同一 `(task,L)` 桶上次访问时 32 个 family、每个 family 全部 $8\times8$ 未加权 pair reward 的均值，初始为 0，当前 step 完成后才更新。family loss 是

$$
\mathcal L_f=-\frac1{64}\sum_{i=1}^{8}\sum_{j=1}^{8}
\operatorname{stopgrad}\!\left[w_{fi}^0w_{fj}^1(R_{fi}^0R_{fj}^1-c_{\rm old})\right]
(S_{fi}^0+S_{fj}^1).
$$

batch loss 是 32 个 $\mathcal L_f$ 的平均。笛卡尔积只复用现有 score，不增加生成。因为两侧采样独立，单侧 MIS 分别无偏估计成功率及其梯度，而 baseline 对 score 的期望为零，所以该 loss 在 $\theta=\theta_{\rm old}$ 处无偏估计 $-\nabla J_{\rm cap}$。单侧权重不超过 2，因此 joint weight 不超过 4。

**训练与推理路径。** 每个 fresh batch 完成一次 backward 和一次 AdamW step，不做同批多 epoch 更新。训练期保存 proposal 成功率、importance-weight 分布、effective sample size 和 action-logit SNR。最终 checkpoint 的推理只运行正向 prompt 和 $p_\theta$，不使用反向 prompt、BFS oracle、verifier search 或候选重排。

### 2.4 Implementation Notes

最小实现以 Python 3.11.9、PyTorch 2.5.1、Transformers、固定 Qwen revision 和 Reasoning Gym commit `49b07130b3fcd12f2d064bba7c43869543a0e7e7` 为基础。训练使用 bf16 全参数 FSDP；AdamW 参数固定为 `lr=1e-6, betas=(0.9,0.95), eps=1e-8, weight_decay=0.1`，constant LR、无 warmup、global grad clip 1.0。三种 seeds 为 `{11,22,33}`，13 个训练桶循环 20 次，共 260 steps。

每步有 32 个 family、64 个 actor prompts、每 prompt 八条长度 $L$ 的轨迹，故五种方法都使用 `512L` 生成动作、`512L` 带梯度 actor positions 和一次更新。main 额外需要 reverse-prompt prefill 与交叉密度 teacher forcing；因此必须分别报告生成动作、actor positions、额外 prefill FLOPs、峰值显存和墙钟，不能声称总 FLOPs 相等。一个完整训练 seed 约生成 133,120 条定长轨迹；主要算力成本来自 15 个训练 run（三 seeds 乘五种方法）和评测，而不是环境生成。

工程上先实现三类小测试：枚举小状态图验证 $p$ 与 $q$ 各自归一；用有限差分或枚举期望验证单侧及乘积 MIS 梯度；重放固定 generator 和 seed，验证 split quota、动作 inverse 和结构变换。它们若失败，分别意味着无偏性、数据合同或任务可逆性 Claim 不能进入大模型训练。

## 3. Minimal Validation Experiment

### 3.1 Purpose

最小实验只回答一个问题：在相同正向生成和 actor-update 预算下，精确双向 MIS 是否比纯正向探索或未经校正的双向 replay 更能提高未见长实例上的跨变体联合成功，并把收益蒸馏进不依赖 proposal 的正向策略。任何一个确认性 gate 失败，都不能接受主 Claim。

### 3.2 Dataset / Benchmark

训练、probe、dev 和 test 都由固定 Reasoning Gym 转移与 BFS 生成。Hanoi 使用 5 disks 训练、6 disks 测试；GRID 使用 $12\times12$ 训练、$16\times16$ 测试且 `p_blocked=0.20`；Knight 使用固定 12 顶点图。候选按 namespace offset 加索引构造独立 RNG，按 BFS 最短长度路由到尚未填满的桶；canonical key 在本 split 和更早 split 中精确去重。若扫描一百万个候选仍不能填满 quota，则直接判任务协议不可行，不修改规则。

| Task | train quota | probe/dev quota | confirmatory test quota |
|---|---:|---:|---:|
| Hanoi | $L=6\ldots10$，每桶 128 | 每桶 32 / 32 | $L=11\ldots16$，每桶 160，共 960 |
| GRID | $L=6\ldots10$，每桶 128 | 每桶 32 / 32 | $L=11\ldots14$，每桶 240，共 960 |
| Knight | $L=6,8,10$ 分别 48/128/256 | 分别 12/32/64 | $L=12,14,16$，每桶 320，共 960 |

Hanoi 的五个 peg 非恒等置换、GRID 的七个正方形旋转/镜像、Knight 的水平/垂直/180 度三个图自同构均预先固定。每个训练和测试实例按 canonical rank 模变换数选一个变体；状态、目标、图和 action legend 同步变换。probe 只做机制诊断、dev 只查崩溃与格式，二者不得选模型、超参或 checkpoint。已知 probe 的 base-key 去重不对变换轨道闭包：Hanoi 有 `13/160`、Knight 有 `35/108` 个 base prompt 等于某个训练变体，因此 probe 不能称为 transform-disjoint；确认性 test 使用互斥的更长 $L$，不受这一重合影响。

### 3.3 Baselines

| Baseline | relevance to keywords/task | paper | verified code | reproduction route | controlled core parameters |
|---|---|---|---|---|---|
| Full-forward paired trajectory PG | 直接隔离双向 proposal 对同一 pair-success 目标的作用 | 本研究的必要机制对照 | 由 main 本地实现切换 proposal，无外部 artifact | 同一 32 family；两侧各八条 $p_{\rm old}$；复用相同 $8\times8$ pair loss 和 $c_{\rm old}$；令 $w=1$ | 同模型、数据、64 prompts、`512L` 生成、`512L` actor positions、optimizer 和一次更新 |
| Vanilla GRPO | 标准 RLVR 对照 | [DeepSeekMath / GRPO](https://arxiv.org/abs/2402.03300) | [Reasoning Gym](https://github.com/open-thought/reasoning-gym/tree/49b07130b3fcd12f2d064bba7c43869543a0e7e7/training) 的 `train_grpo.py` 与 reward 入口已核验 | 相同 64 prompts 各自成组；8 个二元 reward 用样本标准差（分母 $N-1$）标准化，`eps=1e-6`；token PPO clip `[0.8,1.2]`；`ppo_epochs=1` | 相同 actor prompts、rollout 数、动作长度、模型、optimizer 和一次更新 |
| RL-PLUS-core-matched | 最接近“混合轨迹 + MIS”的 RLVR 实现 | [RL-PLUS](https://arxiv.org/abs/2508.00222) | [官方 commit](https://github.com/YihongDong/RL-PLUS/commit/eb4aa4d4e2d7ce206056f9d7740138bfc94fad8f)；`verl/trainer/ppo/core_algos.py::compute_grpo_outcome_advantage` 与 `verl/recipe/rlplus_core_alg.py::compute_token_on_off_policy_loss` 已核验 | 公共 PyTorch sampler 先生成八路，再以 BFS 最短路径 raw token IDs 覆盖 slot 0，重算 old log-prob；使用全八路 GRPO advantage、token MIS/EBAF、`alpha=beta=1`；详细开关见交接文件 | 相同 64 prompts、八路 rollout、被丢弃生成也计预算、`8L` actor positions；关闭 entropy/KL；只称 core-matched，不称官方完整 recipe |
| Unweighted paired replay | 判断提升是否只是双向数据暴露而非正确的密度校正 | 本研究的必要消融 | 由 main 本地实现切换权重，无外部 artifact | 与 main 完全相同的 `4p+4q`、$8\times8$ pair loss 和 $c_{\rm old}$，唯一差异是两侧 $w=1$ | 除 importance correction 外全部相同 |

DIVER 不进入最小确认性 baseline：固定 commit `5870b47` 的公开 diversity metric 对响应先做 whitespace split，再计算最高五阶、无平滑 BLEU；本实验的无空格单字符动作串会使其相似度退化为零。它只能作为相关工作，不能据此声称 DIVER 方法思想一般无效。

### 3.4 Metrics

**Primary metric: pair success。** 每个 checkpoint 对 test 原题和固定变体各实际生成八条响应，共 `16L` 评测动作。trained policy 的预注册主指标只读 rollout 0：两侧都成功记 $X_i=1$；base model 则在两侧分别读取 best-of-8，两侧都至少一次成功才记 1。额外七路 trained 响应只用于 secondary pass@8，不能替换主指标。

**Capability certificate。** 每 task、每 training seed 有 960 个独立 decode 指标，允许题间成功率不同。令

$$
\epsilon=\sqrt{\frac{\log(18/0.05)}{2\times960}},\quad
L_{\rm RL}=\max(0,\bar X_{\rm RL}-\epsilon),\quad
U_{\rm base}=\min(1,\bar X_{\rm base}+\epsilon).
$$

18 个预指定单侧 Hoeffding 端点经 union bound 至少有 0.95 联合覆盖；三个任务乘三个 seeds 的九项都必须满足 $L_{\rm RL}>U_{\rm base}$。

**Baseline superiority。** 对 3 seeds 乘 4 baselines 的 12 项比较，在 2880 个固定 test 实例上定义 $D_i=X_i^{\rm main}-X_i^{\rm baseline}\in[-1,1]$。若 $\bar D\le0$，取 $p_H=1$；否则取 Hoeffding-valid $p_H=\exp(-2880\bar D^2/2)$。对 12 个 p-values 作 Holm step-down，family-wise $\alpha=0.05$；要求全部原始 $\bar D>0$ 且全部拒绝。

**Secondary diagnostics。** 报告逐任务 rollout-0 success、trained pass@8、proposal $p/q$ 成功率、importance weight/ESS、action-logit SNR、峰值显存、墙钟和额外 prefill FLOPs。能力证书与 baseline superiority 是两个分别控制在 0.05 的确认性 family，不能合称二者联合后的全局 95% simultaneous guarantee。

### 3.5 Expected Result and Failure Condition

只有九个 capability comparisons 和 12 个 Holm comparisons 全部通过，才认为最小实验支持主 idea。理想机制证据是：$q$ 在稀疏桶上比 $p$ 更常发现成功候选，main 最终正向 pair success 又高于 full-forward paired PG 和 RL-PLUS-core-matched，同时显著高于 unweighted replay。

以下结果均构成明确失败解释。若 $q$ 成功率提高但最终正向策略不提高，结论是“搜索收益未蒸馏”；若 main 与 unweighted replay 无差异，说明结果主要是数据暴露而非 MIS 校正；若只提高原题而变体不提高，乘积目标没有形成预期的跨变体能力；若超过普通 baseline 但不能超过 base best-of-8 包络，只能声称概率锐化，不能声称在预注册预算下获得新能力；任一确认性 gate 失败，都将主 Claim 记为不成立，而不是事后删除任务或 seed。

## 4. Follow-Up Experiment Plan

1. Main benchmark comparison: 保持冻结主实验不变，增加 OMEGA explorative `logic_gridworld_blocked/test_out` 100 题、compositional `comp_grid_chips/test` 50 题和 transformative `trans_gridworld/test` 16 题。每个 checkpoint 每题生成八条全词表响应、最多 1024 新 token，以最后一个平衡 `\boxed{}` 中的十进制整数计 exact match；只作描述性迁移。
2. Ablation study: 分别去掉乘积目标、去掉双向 proposal、去掉 importance correction；再比较 `2p+6q`、`4p+4q`、`6p+2q`，检查探索与方差的变化。比例消融在主 gate 完成后进行，不能反向选择主设置。
3. Robustness/generalization: 在主协议通过后扩展到另一模型规模、不同长度外推和新的可逆状态图；保持动作接口与评测预算预注册。若 OMEGA 不超过 vanilla GRPO 与 full-forward PG，论文结论明确限于动作规划域。
4. Efficiency/cost analysis: 分解 generation、actor forward/backward、reverse prefill、cross-density teacher forcing 和 verifier 成本；报告单位成功 pair、单位能力增益的 GPU-hours，并比较权重 ESS 与墙钟开销。
5. Qualitative/error analysis: 将失败分为两半不相遇、拼接后非法、原题单侧失败、变体单侧失败和正确轨迹未被正向策略吸收；按任务与长度展示典型状态轨迹，而不是用自由文本相似度替代执行分析。

## 5. Risks and Open Questions

1. **新颖性是组合式而非组件式。** RL-PLUS、TACSTaR、Forward-Backward RL、OT-GRPO 和 Share-GRPO 分别覆盖 MIS、反向 proposal 或变体配对。开始大规模训练前继续检查是否出现同时覆盖三件套的新工作；论文措辞始终限定为完整估计量组合。
2. **pair reward 更稀疏。** 两侧 reward 相乘可能在最难桶上长期全零。先用冻结 probe 比较 $p$ 与 $q$ 的成功率、ESS 和零 reward batch 比例；若双向 proposal 仍无法提供 pair signal，idea 在当前模型规模上不可行。
3. **无偏性只在旧参数单步处成立。** 若实现复用同批数据做多 epoch 更新、让 density 或 weight 回传梯度，理论结论失效。实现中强制一次 update，并以小状态空间枚举梯度测试作为训练前 gate。
4. **总计算量并不完全相等。** main 的 reverse prefill 和交叉密度 teacher forcing 使 FLOPs/墙钟高于只做正向采样的方法。主比较只声称生成动作和 actor positions 相同；另以成本曲线判断提升是否值得额外算力。
5. **probe 不是 transform-disjoint。** 现有 base-key split 在 Hanoi 和 Knight 上存在训练变体重合。probe 仅作描述性诊断且不选择设置；如果后续想把 probe 变成推断数据，必须重新生成按变换轨道闭包的 split，不能沿用当前数字。
6. **两个统计 family 不能合并解释。** 能力证书和 baseline superiority 各自控制 $\alpha=0.05$，但二者联合并非全局 0.05。最终表述分别报告两组结果；若需要一个单一全局保证，必须预先重新分配 alpha，而不能事后宣称。
7. **RL-PLUS 对照是 core-matched。** 公共 sampler、动作 mask和 loss reduction 修改了官方训练外壳。它能回答固定核心机制的比较，但不能承载“优于官方完整 RL-PLUS recipe”的 Claim；官方 shell 参数只能作额外敏感度。
8. **外部迁移可能失败。** 三个主任务都是短动作规划，OMEGA 又只有 166 题。外部失败时应把贡献限定为可逆规划中的探索与蒸馏，不外推到一般数学推理。
9. **有限预算能力不等于 support 扩张。** 即使 trained rollout-0 下界超过 base best-of-8 上界，也只证明预注册题集与预算下的 operational gain。理论 support 是否改变仍是开放问题。

## References Used

1. *DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models*, 2024. https://arxiv.org/abs/2402.03300
   - Role in this proposal: GRPO 的原始方法来源和标准 RLVR baseline。
   - Confidence: verified
2. *Does Reinforcement Learning Really Incentivize Reasoning Capacity in LLMs Beyond the Base Model?*, 2025. https://arxiv.org/abs/2504.13837
   - Role in this proposal: base-versus-RL capability boundary 与大采样预算问题的背景。
   - Confidence: user-provided / verified
3. *Reasoning as Budgeted Search: Rethinking Evaluation and Scaling in LLM Post-Training*, 2026. https://arxiv.org/abs/2609.01274
   - Role in this proposal: 有限采样预算下比较能力包络的直接动机。
   - Confidence: verified
4. *RL-PLUS: Countering Capability Boundary Collapse of LLMs in Reinforcement Learning with Hybrid-policy Optimization*, 2025. https://arxiv.org/abs/2508.00222 ; https://github.com/YihongDong/RL-PLUS/commit/eb4aa4d4e2d7ce206056f9d7740138bfc94fad8f
   - Role in this proposal: 混合策略、MIS 与 capability boundary 的最高近邻及确认性 baseline。
   - Confidence: verified
5. *TACSTaR: Teaching LLMs to Automate Computational Workflows by MC-EM*, 2025. https://arxiv.org/abs/2508.18244
   - Role in this proposal: 目标条件 proposal 和 balance-heuristic importance sampling 的近邻。
   - Confidence: reviewer-invoked / verified
6. *Forward-Backward Reinforcement Learning*, 2018. https://arxiv.org/abs/1803.10227
   - Role in this proposal: 从目标状态反向采样及 Hanoi/Gridworld 场景的经典近邻。
   - Confidence: verified
7. *The Art of Interrogation: An Approach to Lightweight and Transferable Reasoning*, 2026. https://arxiv.org/abs/2606.11918
   - Role in this proposal: 结构变体两侧采样和 $K\times K$ 配对的最高近邻。
   - Confidence: reviewer-invoked
8. *R1-ShareVL: Incentivizing Reasoning Capability of Multimodal Large Language Models via Share-GRPO*, 2025. https://arxiv.org/abs/2505.16673
   - Role in this proposal: 跨 prompt 共享轨迹与 advantage 的近邻。
   - Confidence: reviewer-invoked
9. *Reasoning Gym: Reasoning Environments for Reinforcement Learning with Verifiable Rewards*, codebase. https://github.com/open-thought/reasoning-gym/commit/49b07130b3fcd12f2d064bba7c43869543a0e7e7
   - Role in this proposal: 三类任务的状态转移、BFS、generator 和 verifier 基础。
   - Confidence: verified
10. *OMEGA: Can LLMs Reason Outside the Box in Math?*, 2025. https://arxiv.org/abs/2506.18880 ; https://github.com/sunblaze-ucb/math_ood/commit/589954335e9ca8555636770fa2c55eba6efcb4f9
   - Role in this proposal: explorative、compositional 和 transformative 外部迁移评测。
   - Confidence: verified
11. *DIVER: Diverse Trajectory Exploration for LLM Reinforcement Learning*, 2025. https://arxiv.org/abs/2509.26209 ; https://github.com/NJU-RL/DIVER/tree/5870b47
   - Role in this proposal: sequence-level diversity 近邻，以及固定单字符接口下不纳入确认性 baseline 的实现依据。
   - Confidence: verified
12. *Representation-Based Exploration for Language Models*, 2025. https://arxiv.org/abs/2510.11686
   - Role in this proposal: hidden-state exploration 的相关方向，用于界定本方法直接能力目标与表示奖励的差异。
   - Confidence: user-provided / verified
