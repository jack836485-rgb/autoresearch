## 术语与缩写表

| 术语 / 缩写 | 全称或译名 | 含义与在本 Idea 中的作用 |
|---|---|---|
| pass@k | 采样 k 次至少成功一次的概率 | 衡量覆盖：多次采样能解出多少任务。本文用每任务 32 次 rollout 的无偏估计计算 pass@16 作主指标 |
| 覆盖 / 锐化税 | coverage / sharpening tax | 后训练提高单次成功率（pass@1）、却让大 k 下能解的任务变少，少掉的那部分称锐化税（Sharpening Tax，arXiv 2610.01509 提出的诊断量） |
| GRPO | Group Relative Policy Optimization | 一组 rollout 内按相对奖励计算优势的 RL 算法，多轮 agent RL 的标准做法；本文的 G 由它训练 |
| B / G | 起点策略 / 纯 RL 检查点（本文定义） | B 是 RL 前的起点模型；G 是从 B 出发、在同一设置下只做 GRPO 得到的模型。比较二者即隔离了 RL 本身的作用 |
| 保覆盖方法 | coverage-preserving methods | 为防止 RL 丢覆盖而设计的训练方法，如 DPH-RL、TAR、PTGS 与入口修复 |
| 前向 KL | forward KL，KL(π_B‖π) | 在基座样本上最大化当前策略似然的散度项，惩罚“基座会做、当前策略不做”的动作，适合保住稀有分支；与在自身样本上估计的反向 KL 相对 |
| DPH-RL | Diversity-Preserving Hybrid RL | 用离线基座样本上的前向 KL 等质量覆盖型散度保 pass@k 的方法（arXiv 2509.07430），原在单轮数学 / SQL 上验证 |
| TAR | Targeted Adaptive Replay | 建基座多样成功解库，只在这些解被当前策略抑制时加权回放的方法（arXiv 2610.24236），原在单轮数学上验证 |
| PTGS | Posterior-Tempered Group Sampling | 按每题难度的贝叶斯后验设定 RL 采样温度的方法（arXiv 2610.01509），在多轮 Sokoban / FrozenLake 上验证，并有推理期变体（其附录 E.4） |
| 入口锁定 | entrance locking | RL 的覆盖损失集中在轨迹第一步的现象，由 Locked at the Entrance（arXiv 2608.29188）在单轮任务上发现 |
| 观察后重新锁定 | re-locking after observation（本文定义） | 多轮 agent 中，收到环境观察之后的决策轮也被 RL 锁定分支的假设 |
| 逐轮替换 | per-turn substitution（本文定义） | 在真实环境中只把第 t 轮动作换成 B 生成、其余由 G 生成并继续，测这一轮能找回多少覆盖 |
| 同模型分叉 | same-model fork | 第 t 轮由 G 自己重新采样的对照，用来估计重放与采样噪声底（方法来自 The Replay Gap，arXiv 2608.08239） |
| L(t) | 可找回覆盖剖面（本文定义） | 第 t 轮逐轮替换的 pass@16 减去同模型分叉的 pass@16，描述覆盖损失落在哪些轮 |
| 测试时对应物 | test-time counterpart（本文定义） | 为每个训练方法定义的推理期操作，描述“基座在该方法够得着的位置上接管”，无需训练即可测量 |
| P_m(i) / Δ_m(i) | 对应物增益 / 训练增益（本文定义） | 任务 i 上，方法 m 的对应物相对 G 的 pass@16 增益，以及方法 m 训练后相对 GRPO 的 pass@16 增益（3 个种子均值） |
| 规律面板 | law panel（本文定义） | 从 RL 训练划分中抽取、用于主检验的任务集合；离线回放方法的库正是在这些任务上采样的 |
| 剖面选轮前向 KL | profile-selected forward KL（本文定义） | 只在剖面选出的轮上施加前向 KL 的训练方法，是本文规律给出的处方 |
| WebShop / ALFWorld | 网购 agent 基准 / 文本家务 agent 基准 | 两个可程序评分、可确定回放的多轮 agent 环境 |

# 多轮 agent 中保覆盖方法作用于哪里：用测试时对应物预测训练方法的覆盖增益

**定位关键词：** multi-turn agent RL；pass@k coverage；diversity collapse；checkpoint handoff；forward KL；replay；WebShop；ALFWorld

**一句话背景：** 多轮工具 agent 的强化学习常常提高单次成功率、却在大 k 采样下丢失可解任务覆盖，现有保覆盖方法在多轮轨迹中实际作用于哪里、能找回多少覆盖，尚未被检验。

**输入论文及其角色（如适用）：** 不适用（输入为问题卡 A-Q001，见 `path-stage/LLM热门方向_算力适配_20261028/`）。

**本 Idea 的独立创新点：** 为每类保覆盖训练方法定义一个推理期可测的“基座接管”对应物，并在任务内、跨方法检验它能否在训练前按任务预测该方法相对 GRPO 的覆盖增益。

## 1. 引言式概述

### 1.1 任务锚点与最小范围

- **任务**：多轮工具 agent 的结果奖励 RL（GRPO 类），在可确定回放的环境 WebShop 与 ALFWorld 上，研究 RL 对 pass@k 覆盖的影响，以及保覆盖方法的效果。
- **模型**：Qwen2.5-7B 规模的开源起点模型。
- **不在范围内**：
  - 单轮推理任务；
  - 发布检查点（混合了 SFT、偏好优化与 RL）的归因；
  - 新的 RL 算法设计；
  - 闭源模型。

### 1.2 现有方法如何处理这个问题

- **单轮上提出的方法**：
  - Locked at the Entrance（arXiv 2608.29188）在单轮 Countdown 与数学上发现，RLVR 的覆盖收缩集中在入口，替代分支补上入口前缀后仍可执行；用晚层参数插值修复。
  - DPH-RL（arXiv 2509.07430）在离线基座样本上施加前向 KL 以保 pass@k。
  - TAR（arXiv 2610.24236）建基座成功解库，在它们被抑制时加权回放。
  - PBA（arXiv 2607.20543）按题判断风险，再向冻结基座锚定。
- **多轮上提出、但只在任务级或第一轮上操作的方法**：
  - Sharpening Tax（arXiv 2610.01509）在 WebShop、BFCL、ACEBench 上做任务级锐化税测量；它提出的 PTGS 按题调采样温度，在多轮 Sokoban / FrozenLake 上验证。
  - DivInit（arXiv 2606.17209）只修多轮搜索 agent 第一轮的查询冗余。
- **相关的诊断协议**：
  - Reach or Solve（arXiv 2609.19636）在 ALFWorld 上用一次检查点交接，把 SFT↔RL 的成功率拆成“到达”与“完成”；
  - The Replay Gap（arXiv 2608.08239）在真实环境中分叉换模型，并用同模型分叉估计噪声底。

### 1.3 现有方法的瓶颈

每个保覆盖方法都隐含一个“覆盖丢在哪里、我能作用到哪里”的假设：

| 方法类型 | 隐含假设 |
|---|---|
| 入口修复 | 覆盖丢在第一步 |
| 离线回放（DPH-RL、TAR） | 回放的基座状态会被当前策略再次访问 |
| PTGS | 只需按题调整采样温度 |

单轮任务里所有状态都由同一个提示决定，这些假设大多自然成立。多轮 agent 中，每次环境观察都会带来新的决策点，策略一旦换了分支，后续状态就与基座不同（DAgger 式协变量偏移；多轮蒸馏中的讨论见 ReOPD，arXiv 2607.04763）。目前没有工作测量多轮 agent 中 RL 丢失的覆盖落在哪些轮，也没有工作检验各方法的“可作用位置”能否解释它们的实际效果。结果是：选方法只能逐个训练、试错，没有训练前的依据。

### 1.4 本文的改进

我们实际做的事情是：先只用推理，为每个保覆盖方法测出“如果基座在该方法够得着的位置上接管，能找回多少覆盖”（测试时对应物增益）；再训练这些方法，检验这个推理期测量能否在同一任务上、跨方法预测各方法的真实训练增益。与现有工作相比，改变的是评价与选择方法的方式：从“训练后比较平均分”变成“训练前按任务预测、训练后在任务内检验”。我们刻意保持各方法本身不变（原样移植），只在最后用规律给出一个简单处方：只在剖面选出的轮上施加前向 KL，并用同 token 占比的随机选轮对照检验它。

### 1.5 实验设置一览

在 WebShop 与 ALFWorld 上，从 Qwen2.5-7B 起点 B 训练纯 GRPO 检查点 G。前置检查确认 G 在训练分布上确实付了锐化税：pass@32 至少低 5 个百分点，且至少 60 个“B 能解、G 全失败”的任务。随后：

1. 在规律面板（训练划分中的任务）上测逐轮剖面 L(t) 与六个测试时对应物；
2. 训练入口前向 KL、DPH-RL、TAR、PTGS、剖面选轮前向 KL、随机选轮前向 KL，以及 GRPO，各 3 个种子；
3. 用任务固定效应回归、任务内置换检验、自身对应物优于他人对应物与成对差分检验判断规律是否成立；
4. 留出任务作泛化次检验。

主指标为 pass@16，用每任务 32 次 rollout 的无偏估计计算。

### 1.6 贡献

1. **测量**：在多轮 agent 的纯 RL 检查点上，用真实环境逐轮替换并扣除同模型噪声底，按轮定位 RL 丢失的覆盖，区分入口锁定与观察后重新锁定。
2. **主贡献（可推翻的预测规律）**：为每个保覆盖训练方法定义唯一的推理期对应物，并证明（或推翻）对应物增益能在任务内、跨方法预测训练增益。规律成立时，选方法不再依赖逐个训练试错。
3. **处方**：由规律推出的剖面选轮前向 KL，并用同 token 占比随机选轮检验“锚定的定向是否重要”。这与 Coverage, Not Targeting（arXiv 2609.02417）中“信用分配的定向与随机同样有害”的结论形成可检验的对照。

## 2. 方法细节

### 2.1 方法直觉

核心思想：一个训练方法能找回多少覆盖，应当约等于“基座在这个方法能作用到的位置上接管”时能找回多少。后者只需推理就能测。

1. **训练 G**：从 B 出发只做 GRPO 得到 G，确认它丢了覆盖。这样隔离了 RL 本身的作用。
2. **逐轮替换**：在真实环境中，只把第 t 轮换成 B 来生成，其余仍由 G 生成，看能找回多少覆盖，并减去 G 自己重新采样的噪声底，得到 L(t)。这告诉我们覆盖丢在哪些轮。
3. **为每个方法定义对应物**：按方法的作用位置决定基座在哪里接管，测出对应物增益 P_m(i)。这一步把“方法够得着哪里”变成一个数。
4. **训练各方法**：在同一设置下训练所有方法，得到训练增益 Δ_m(i)。
5. **检验规律**：在同一任务上比较不同方法，看对应物增益更大的方法，训练增益是否也更大。这一步区分了“方法特异的预测力”与“任务共有的提升空间”。
6. **处方**：只在剖面选出的轮上施加前向 KL，并与随机选轮比较。

### 2.2 输入、输出与假设

- **输入**：起点策略 B；在同一设置下训练的 G；可确定回放的环境（WebShop 固定 `WEBSHOP_ENV_SEED`，ALFWorld 固定游戏文件与种子）；训练划分上的离线基座成功轨迹库。
- **输出**：逐轮剖面 L(t)；六个对应物增益 P_m(i)；各方法训练增益 Δ_m(i)；规律检验结果；处方方法的效果。
- **假设**：
  - 纯 GRPO 在所选设置下确实产生锐化税（由阶段 0 门槛检验）；
  - 环境可在给定动作序列下确定地重建状态；
  - 状态等价可由环境状态程序判定。

### 2.3 算法与系统设计

**(a) 逐轮替换与剖面。** 对规律面板中的任务 i、轮次 t：

- 替换条件：在真实环境中由 G 运行到第 t−1 轮，第 t 轮由 B 生成，之后回到 G；
- 对照条件：第 t 轮由 G 重新采样。

各 32 次 rollout，计算

$$L_i(t) = \widehat{\text{pass@16}}_{\text{替换}}(i,t) - \widehat{\text{pass@16}}_{\text{分叉}}(i,t)$$

其中 $\widehat{\text{pass@16}}$ 是由 32 次 rollout 中成功次数 c 给出的无偏估计 $1-\binom{32-c}{16}/\binom{32}{16}$。这个量表示“只让基座接管第 t 轮”比“G 自己在第 t 轮重新采样”多找回的覆盖。比较只在替换轮数相同的组之间进行，以排除剂量混杂。

**(b) 六个测试时对应物。**

| 方法族 | 训练方法 | 测试时对应物 |
|---|---|---|
| 入口 | 入口前向 KL | B 只接管第 1 轮 |
| 离线回放（无门控） | DPH-RL | 每一轮若 G 当前环境状态与该任务某条基座成功轨迹的状态相同，则由 B 接管 |
| 离线回放（抑制门控） | TAR | 同上的共享状态中，只在该基座成功动作被 G 抑制时由 B 接管 |
| 采样侧 | PTGS | 推理期 PTGS：按 PTGS 的难度后验为每个任务设定温度后由 G 采样 |
| 剖面处方 | 剖面选轮前向 KL | B 接管剖面选出的轮集合 S |
| 随机选轮 | 随机选轮前向 KL | B 接管同数量的随机轮 |

对应物增益为

$$P_m(i) = \widehat{\text{pass@16}}_{\text{对应物 } m}(i) - \widehat{\text{pass@16}}_{G}(i)$$

它直接测量，不做跨轮相加。

各对应物使用的数据：

- **规律面板**：离线回放对应物所用的基座成功轨迹，就是训练 DPH-RL / TAR 的库中该任务的那几条。
- **留出任务**：基座成功轨迹另行采样，不进入任何训练库。
- **S 的选取**：S 在独立的开发任务上按剖面选出，评测任务不参与选择。

**(c) 规律检验。** 设 $\Delta_m(i)$ 为方法 m 在任务 i 上相对 GRPO 的 pass@16 增益（3 个种子均值）。主回归为

$$\Delta_m(i) = \alpha_i + \gamma_m + b\,P_m(i) + \varepsilon_{m,i}$$

- **α_i（任务固定效应）**：吸收任务共有的提升空间。“B 能解、G 全失败”的任务对所有方法都有空间，这部分不应被算作预测力。
- **γ_m（方法固定效应）**：吸收方法整体强弱。
- **b**：只由同一任务内、不同方法之间的差异识别。规律预测 b > 0。

辅助检验：

- **任务内置换**：每个任务内打乱“方法—对应物”配对 1000 次，真实 b 须高于置换分布的 95% 分位。
- **自身优于他人**：每个方法的自身对应物，在任务内对其训练增益的偏 R²，须高于其他方法的对应物。
- **成对差分**：对每对方法用 $[P_m(i)-P_{m'}(i)]$ 回归 $[\Delta_m(i)-\Delta_{m'}(i)]$，斜率为正；相关高于 0.9 的对应物对只用此检验判定。
- 方法均值排序一致性只作补充。

**(d) 预注册的退化情形。** 若第 1 轮之后的状态匹配率低于 10%，离线回放对应物在数值上接近入口对应物。此时预测：DPH-RL / TAR 的训练增益与入口前向 KL 无显著差别。

**(e) 处方方法。** 在 S 中各轮的离线基座成功片段上，对当前策略加负对数似然，即 S 上状态的前向 KL(π_B‖π)，估计方式同 DPH-RL；其余轮不加散度。

### 2.4 实现说明

- **训练框架**：verl-agent（`examples/grpo_trainer/run_webshop.sh`、`run_alfworld.sh`）。WebShop 环境换成 Sharpening Tax 的文本 harness（`sharpening_tax/benchmarks/webshop.py`），商品子集、步数上限与 `WEBSHOP_ENV_SEED` 保持一致；按 verl-agent 多环境 worker 的方式起多个 WebShop 服务并行。
- **TAR 移植**：复制其 `verl/trainer/ppo/core_algos.py` 中的 `compute_tar_weights`、`compute_tar_loss`，以及 `verl/workers/actor/dp_actor.py` 中的 `_backward_tar_loss`。记忆库条目改为多轮基座成功轨迹，response_mask 只覆盖动作 token。TAR 的门控在源码中是轨迹平均的 b(τ)=mean(log π_ref − log π_old)>0，再乘逐 token 软权重；多轮移植后对应物的门控须按同一粒度计算（见第 5 节风险 2）。
- **DPH-RL 移植**：参照其 `scripts/llama/forward_kl.sh` 与离线 `data.sft_files` 机制，在 verl-agent actor 更新中加入按动作 token 掩码的离线 NLL 项。入口、剖面、随机选轮三种方法只改轮掩码。
- **PTGS**：用 `ptgs/integration.py` 的 `PTGSHooks` 接入 GRPO 组采样。
- **逐轮替换**：参照 AgenticRL_Handoff 的 `src/handoff/alfworld/{environment,rollout}.py`（基于 SkillRL 的 ALFWorld），在 verl-agent 的两个环境中实现。
- **算力**：8×A100 80G。阶段 0 约 1 天；阶段 A 约 3.9 天；阶段 B 训练 42 次约 12 天，评测约 5.5 天。合计约 22 天，慢 30% 时约 28 天；无 API 费用。

## 3. 最小验证实验

### 3.1 目的

检验主贡献：推理期对应物增益能否在任务内、跨方法预测保覆盖训练方法相对 GRPO 的覆盖增益。

### 3.2 数据集与基准

- **WebShop**：
  - 规律面板：从训练划分随机抽 800 个任务；
  - 留出任务：800 个不在训练中的目标；若商品子集下不足 800 个，改用全量商品索引；
  - 开发任务：另取 200 个，用于选 S 和超参。
- **ALFWorld**：
  - 规律面板：从训练划分抽 274 个；
  - 留出任务：unseen 134 个 + seen 140 个；
  - 开发任务：从训练划分留出 60 个不参与训练的任务。
- **起点**：Qwen2.5-7B 基座；ALFWorld 上若其 pass@32 低于 30%，改用 Qwen2.5-7B-Instruct。

### 3.3 Baselines

核验方式：2026-10-29 以完整 `git clone --depth 1` 核验。

| Baseline | 与关键词 / 任务的关系 | 论文 | 已核验代码（HEAD / 文件数） | 复现路线 | 控制的核心参数 |
|---|---|---|---|---|---|
| GRPO | 多轮 agent RL 标准做法；所有增益的参照 | https://arxiv.org/abs/2505.10978 | https://github.com/langfengQ/verl-agent （20bd331 / 1334） | `examples/grpo_trainer/run_webshop.sh`、`run_alfworld.sh` | 同一环境内组大小、步数、学习率、rollout 预算一致 |
| 入口前向 KL | 入口类保覆盖的训练版 | https://arxiv.org/abs/2608.29188 （入口定位）、https://arxiv.org/abs/2509.07430 （前向 KL） | 同 DPH-RL | DPH-RL 前向 KL 只掩码第 1 轮 | 同上；与其他前向 KL 组共用离线样本 |
| DPH-RL | 离线前向 KL 保 pass@k | https://arxiv.org/abs/2509.07430 | https://github.com/seamoke/DPH-RL （fea6990 / 675） | `scripts/llama/{offline_sampling,forward_kl}.sh`，移植到 verl-agent | 同上 |
| TAR | 抑制门控回放保多样性 | https://arxiv.org/abs/2610.24236 | https://github.com/wenzhilics/tar （0b7d515 / 718） | `recipe/tar/build_memory_bank.py`、`compute_tar_weights` / `compute_tar_loss` / `_backward_tar_loss` 移植 | 同上 |
| PTGS | 多轮 agent RL 中按题调温保覆盖 | https://arxiv.org/abs/2610.01509 | https://github.com/changdaeoh/sharpening-tax （789ae06 / 54） | `ptgs/integration.py` 的 `PTGSHooks` 接入 GRPO（仅 WebShop） | 同上 |
| 随机选轮前向 KL | 处方的同量对照 | https://arxiv.org/abs/2609.02417 （随机对照范式） | 同 DPH-RL | 与 S 相同 token 占比、每 batch 随机抽轮 | 同上（仅 WebShop） |

**超参选择**：每个方法在开发任务上用 1 个种子比较 2 个超参，选 pass@1 与 GRPO 最接近者，该运行计为第 1 个种子；之后补到 3 个种子。

### 3.4 指标

- **主指标**：规律面板上任务内回归的 b（含 95% 置信区间）、置换检验分位、自身优于他人与成对差分的结果。
- **次要指标**：
  - 留出任务上的同样检验；
  - 各方法的 pass@1、pass@16、pass@32 与 pass@64 子集；
  - 六个对应物的相关矩阵；
  - 逐轮剖面 L(t) 与状态匹配率。
- **有意义的结果**：b 显著为正，且超过阶段 A 预注册的最小可检出效应；置换检验通过；多数方法的自身对应物优于他人。

### 3.5 预期结果与失败条件

- **前置门槛**：规律面板上 G 的 pass@32 比 B 低至少 5 个百分点，且至少 60 个任务“B 有成功、G 全失败”。都不满足则报告“该设置下纯 RL 不产生锐化税”并停止。
- **支持（值得继续）**：
  - b > 0 且置信区间不含 0；
  - 真实 b 高于置换分布 95% 分位；
  - 多数方法的自身对应物优于他人；
  - 剖面选轮前向 KL 优于随机选轮。
- **推翻**：
  - 在预注册最小可检出效应之下，b 的置信区间包含 0；
  - 或真实 b 不高于置换分布 95% 分位；
  - 或多数方法的自身对应物不优于他人；
  - 处方部分：剖面选轮不优于随机选轮。
- 剖面 L(t) 落在哪里都报告，不作为成败条件。

## 4. 后续实验计划

1. **主结果**：规律面板与留出任务上的完整规律检验、各方法前沿（pass@1–pass@k），两个环境。
2. **消融**：
   - 对应物定义的敏感性：状态等价的判定粒度、TAR 门控粒度；
   - S 的阈值；
   - 主指标的 k 取值（8 / 16 / 32）。
3. **稳健性与泛化**：
   - 第三个起点模型族（如 Qwen3 或 Llama 系列）；
   - 更大评测集（WebShop 1500 题）；
   - 不同 GRPO 训练步数下 G 的剖面变化。
4. **成本**：对应物测量的推理成本，与逐个训练所有方法的成本对比；说明规律在选方法上节省的算力。
5. **定性分析**：被重新锁定的决策轮案例（如 WebShop 搜索结果页上的选择）、离线回放失效的状态失配案例。

## 5. 风险与开放问题

1. **纯 RL 不产生锐化税**：PASS@(k,T)（arXiv 2604.14877）报告受控工具 RL 在组合任务上扩大边界。阶段 0 门槛把这一前提变成可推翻条件；不成立时报告为负结果并停止。所有结论都限定在“RL 确实丢覆盖”的设置下。
2. **TAR 对应物粒度**：TAR 源码门控是轨迹平均 b(τ) 再乘逐 token 软权重，而对应物按动作比较似然。须在实现中让对应物的门控与多轮移植后的 TAR 门控采用同一粒度（按基座成功轨迹片段计算 b(τ)），并报告两种粒度下的敏感性。
3. **退化推论是零差异预测**：若触发退化情形，“DPH-RL / TAR 与入口前向 KL 无显著差别”不能靠不显著来支持。须在阶段 A 后预注册等价界（如 ±2 个百分点的 pass@16），用 TOST 等价检验判定。
4. **识别变异偏薄**：
   - ALFWorld 只有 3 个非 GRPO 方法、没有随机选轮；
   - WebShop 上离线回放对应物可能退化。

   主检验与处方检验以 WebShop 为主，ALFWorld 作补充。阶段 A 的功效分析不足时，把 WebShop 评测增至 1500 题。
5. **任务级种子噪声**：3 个种子均值的 Δ_m(i) 仍可能噪声大。阶段 A 用 GRPO 的 3 个种子估计方差并模拟回归，预注册最小可检出效应。
6. **处方的新意薄**：剖面选轮前向 KL 本身是 DPH-RL 加轮掩码，价值依赖主规律成立；论文叙事以规律为主，处方为推论。
7. **吞吐与时长**：7B 多轮 GRPO 每次约 7 小时、每天约 23 万条 rollout 的估计可能偏乐观。阶段 0 与阶段 A（约 5 天）先行，结果可行再投入阶段 B。

## References Used

1. Sharpening Tax in Post-Training — Changdae Oh 等，2026. https://arxiv.org/abs/2610.01509
   - 作用：最近邻；锐化税定义、WebShop harness、PTGS 与推理期 PTGS；baseline
   - 置信度：verified
2. Locked at the Entrance, Open Inside: Where RLVR Narrows the Solution Space — Qiancheng Zhou, Ruizhe Li，2026. https://arxiv.org/abs/2608.29188
   - 作用：单轮入口锁定；入口前向 KL 的依据
   - 置信度：verified
3. The Choice of Divergence（DPH-RL）— Long Li 等，2025/2026. https://arxiv.org/abs/2509.07430
   - 作用：离线前向 KL；baseline 与处方的损失形式
   - 置信度：verified
4. Preserving Reasoning Diversity in RLVR via Adaptive Replay（TAR）— Wen-Zhi Li, Sainyam Galhotra, Claire Cardie，2026. https://arxiv.org/abs/2610.24236
   - 作用：抑制门控回放；baseline
   - 置信度：verified
5. Reach or Solve? Deep Diving into Agentic RL Gains with Checkpoint Handoffs — Xuan Liu, Jingbin Qian，2026. https://arxiv.org/abs/2609.19636
   - 作用：检查点交接协议来源
   - 置信度：verified
6. The Replay Gap: Static Evaluation of Model Switching in LLM Agents Scores the Wrong World — Ashritha Gonuguntla，2026. https://arxiv.org/abs/2608.08239
   - 作用：真实环境分叉与同模型噪声底
   - 置信度：verified
7. Beyond Parallel Sampling: Diverse Query Initialization for Agentic Search（DivInit）— Sidhaarth Murali 等，2026. https://arxiv.org/abs/2606.17209
   - 作用：多轮第一轮修复的相关工作
   - 置信度：verified
8. When RLVR Shrinks the Reasoning Boundary: Diagnosing Pass@k Inversion（PBA）— Todd Zhou，2026. https://arxiv.org/abs/2607.20543
   - 作用：单轮按题基座锚定的相关工作
   - 置信度：verified
9. Coverage, Not Targeting: A Structural Regime in Multi-Turn Agent Credit Assignment — Chenyu Zhou 等，2026. https://arxiv.org/abs/2609.02417
   - 作用：随机定向对照范式与相对结论
   - 置信度：verified
10. Multi-Turn On-Policy Distillation with Prefix Replay（ReOPD）— Baohao Liao 等，2026. https://arxiv.org/abs/2607.04763
    - 作用：多轮前缀 / 状态失配的相关讨论
    - 置信度：verified
11. Does RL Expand the Capability Boundary of LLM Agents? A Pass@(k,T) Analysis — Zhiyuan Zhai 等，2026. https://arxiv.org/abs/2604.14877
    - 作用：相反方向的证据；阶段 0 门槛的依据
    - 置信度：verified
12. Group-in-Group Policy Optimization for LLM Agent Training（verl-agent）— Lang Feng 等，2025. https://arxiv.org/abs/2505.10978
    - 作用：训练框架与 GRPO baseline
    - 置信度：verified
13. What RL Brings to Reasoning: A Few Decisions the Base Model Would Not Make — Siyu Zhang 等，2026. https://arxiv.org/abs/2610.24663
    - 作用：单轮 token 级稀疏替换的相关工作
    - 置信度：verified
