## 背景

**定位关键词：** multi-turn agent RL；pass@k coverage；diversity collapse；checkpoint handoff；forward KL；replay；WebShop；ALFWorld

**一句话定位：** RL 会让多轮工具 agent 在大 k 采样下丢失可解任务覆盖。现有保覆盖方法有的在单轮上提出（DPH-RL、TAR、入口修复），有的在多轮上提出但只在任务级或第一轮上操作（PTGS、DivInit）；它们在多轮轨迹中实际作用于哪里、因此能找回多少覆盖，尚无检验。

## 核心 Claim

**已知与归属**：
- **单轮上提出的方法**：
  - Locked at the Entrance（arXiv 2608.29188）在单轮 Countdown / 数学上把 RLVR 的覆盖收缩定位到入口，晚层插值有效；
  - DPH-RL（arXiv 2509.07430）用离线基座样本上的前向 KL 保 pass@k；
  - TAR（arXiv 2610.24236）回放被抑制的基座多样成功解。
- **多轮上提出、但只在任务级或第一轮操作的方法**：
  - Sharpening Tax（arXiv 2610.01509）在 WebShop、BFCL、ACEBench 上做任务级的锐化税测量；它提出的 PTGS 按题调采样温度，在多轮 Sokoban / FrozenLake 上验证；
  - DivInit（arXiv 2606.17209）在多轮搜索 agent 中只修第一轮查询。
- **协议与理论来源**：
  - 检查点交接来自 Reach or Solve（arXiv 2609.19636）；
  - 真实环境分叉与同模型噪声底来自 The Replay Gap（arXiv 2608.08239）；
  - 学生偏离基座状态属于 DAgger 式协变量偏移，多轮蒸馏中的讨论见 ReOPD（arXiv 2607.04763）。

1. **按轮定位：区分入口锁定与观察后重新锁定。**
   - 设 B 为起点策略，G 为从 B 出发、同一设置下只做 GRPO 的检查点。
   - 在真实环境中逐轮替换：只把第 t 轮换成 B 生成，其余由 G 生成并继续，减去同模型分叉的噪声底，得到可找回覆盖剖面 L(t)。
   - 比较只在替换轮数相同的组之间进行。
   - 在 WebShop 与 ALFWorld 上分别报告。剖面落在哪里都报告，不作为成败条件。
2. **测试时对应物预测训练方法的覆盖增益（主贡献）。** 每族方法有一个可在推理期直接测量的对应物，它描述“基座在该方法够得着的位置上接管”能找回多少覆盖：

   | 方法族 | 代表方法 | 测试时对应物 |
   |---|---|---|
   | 入口 | 入口前向 KL | B 只接管第 1 轮 |
   | 离线回放（无门控） | DPH-RL | 每一轮若 G 当前环境状态与该任务某条基座成功轨迹的状态相同，则由 B 接管 |
   | 离线回放（抑制门控） | TAR | 同上的共享状态中，只在“G 对该基座成功动作的对数似然低于 B 自身的对数似然”（即该动作被抑制，与 TAR 的激活条件相同）时由 B 接管 |
   | 采样侧 | PTGS | 推理期 PTGS：按 PTGS 的难度后验为每个任务设定采样温度后由 G 采样（Sharpening Tax 附录 E.4 给出的推理期变体） |
   | 剖面处方 | 按剖面选轮的前向 KL | B 接管剖面选出的轮集合 S |
   | 随机选轮 | 同 token 占比随机选轮的前向 KL | B 接管同数量的随机轮 |

   - 六个对应物两两不同，每个训练方法都有唯一的对应物。
   - 对应物增益 P_m(i) 定义为对应物的 pass@16 减去 G 的 pass@16，按任务 i 直接测量，不做跨轮相加。pass@16 用每任务 32 次 rollout 的无偏估计计算，得到连续值而非 0/1。
   - 预测：任务 i 上，训练方法 m 相对 GRPO 的 pass@16 增益 Δ_m(i)（3 个训练种子的均值）由**该方法自己的**对应物增益 P_m(i) 预测，而不只是由任务共有的提升空间预测。“基座能解、G 全失败”的任务对所有方法都有空间，因此检验只用同一任务内、不同方法之间的差异：
     - **任务内回归**：Δ_m(i) = α_i + γ_m + b·P_m(i) + ε。任务固定效应 α_i 吸收共享提升空间，方法固定效应 γ_m 吸收方法整体强弱；预测 b > 0。
     - **任务内置换检验**：在每个任务内随机打乱“方法—对应物”配对 1000 次，真实 b 须高于置换分布的 95% 分位。
     - **自身对应物优于他人对应物**：对每个方法 m，在任务内用 P_m 解释 Δ_m 的偏 R²，须高于用其他任一方法的对应物 P_m' 的偏 R²。
     - 方法平均增益与平均对应物增益的排序一致性只作补充报告。
   - 训练方法会改变整条策略，不只作用于对应物所示位置；本 Claim 正是检验这一近似在多大程度上成立。
3. **处方**：由 Claim 2，剖面选轮前向 KL 应找回最多覆盖，并优于同 token 占比的随机选轮。Coverage, Not Targeting（arXiv 2609.02417）发现信用分配的定向与随机同样有害；我们假设锚定与之不同，因为它作用于分布而非奖励。这个假设由随机选轮对照直接检验。

**推翻条件**：
- Claim 2：在阶段 A 后预注册的最小可检出效应之下，任务内回归的 b 的 95% 置信区间包含 0；或真实 b 不高于任务内置换分布的 95% 分位；或多数方法的自身对应物不优于他人对应物。
- Claim 3：剖面选轮前向 KL 不优于随机选轮。

## 方法设计的核心思想

**测量（只用推理）**：
- 在 (B, G) 上做逐轮替换、同模型分叉和六个对应物；WebShop 固定 `WEBSHOP_ENV_SEED`，ALFWorld 固定游戏文件与种子。
- 离线回放对应物所用的基座成功轨迹库，与训练离线回放方法所用的是同一批离线样本。状态等价按环境状态程序判定：WebShop 比较页面类型与当前检索结果 / 商品；ALFWorld 比较位置、物品与容器状态。

**处方方法**：在 S 中各轮的离线基座成功片段上，对当前策略加负对数似然（前向 KL(π_B‖π)，估计方式同 DPH-RL），其余轮不加。

**与最高近邻的关键差别**：
- 现有方法各自提出了一种保覆盖的手段，但没有给出在多轮轨迹中该方法作用于哪里、能找回多少的可测预测；
- Sharpening Tax 的按任务路由在基座与后训练模型之间整条轨迹切换，不做按轮接管，也不预测训练方法的效果；
- Reach or Solve 只比较 SFT↔RL 的到达与完成成功率。

## 最小实验

**阶段 0：前置检查（约 1 天）。**
- WebShop：
  - B = Qwen2.5-7B 基座。Sharpening Tax 的 WebShop 文本 harness 移植进 verl-agent，商品子集、步数上限与 `WEBSHOP_ENV_SEED` 一致，训练与评测同一设置。
  - 训练用 WebShop train 划分。留出评测取 800 个不在训练中的目标；若该商品子集下不足 800 个，改用全量商品索引，并同步修改 harness。
- ALFWorld：
  - B = Qwen2.5-7B 基座；若其 pass@32 低于 30%，改用 Qwen2.5-7B-Instruct 作起点。
  - 留出评测取 unseen 134 个 + seen 140 个任务。
- 各跑 1 个种子的 GRPO 得到 G。进入后续的门槛：G 的 pass@32 比 B 低至少 5 个百分点，且至少有 60 个任务“B 有成功、G 32 次全失败”。都不满足则报告“纯 RL 不产生锐化税”并停止。

**阶段 A：测量（约 2.5 天）。**
- WebShop 800 个任务（t = 1…6）、ALFWorld 274 个任务（t ∈ {1, 2, 4, 8, 12, 16}）。
- 每格做逐轮替换与同模型分叉，32 次 rollout，含剂量匹配组；六个对应物各 32 次。
- 剖面集合 S 只在另取的 200 个开发任务（WebShop；ALFWorld 从训练划分中留出 60 个不参与训练的任务）上的剖面选出，评测任务不参与选择。
- 功效分析：用阶段 0 的 G 与额外 2 个 GRPO 种子（在阶段 B 中复用）估计任务级增益的种子方差，模拟任务内回归，预注册 b 的最小可检出效应；若不足以检出 b = 0.3，则把 WebShop 评测任务增至 1500。

**阶段 B：训练（约 12 天训练 + 3 天评测）。**
- WebShop 七组：GRPO、入口前向 KL、DPH-RL（全局前向 KL）、TAR、PTGS、剖面选轮前向 KL、随机选轮前向 KL。
- ALFWorld 四组：GRPO、入口前向 KL、TAR、剖面选轮前向 KL。
- 超参：每个方法在 200 个开发任务上用 1 个种子比较 2 个超参（散度系数或 PTGS 温度跨度），选 pass@1 与 GRPO 最接近者；该运行计为该组第 1 个种子。
- 所有组 3 个种子；同一环境内组大小、步数、学习率、rollout 预算相同；回放与前向 KL 组用同一批离线基座成功样本。
- 评测：留出任务每任务 32 次 rollout，报告 pass@1、pass@16（无偏估计，主分析）与 pass@32，另报告 pass@64 的子集结果。Sharpening Tax 报告少量 rollout 的税估计可预测大预算的税，因此主分析用连续的 pass@16 估计。

**移植路线**（均为 verl 结构）：
- TAR：把其仓库 `verl/trainer/ppo/core_algos.py` 的 `compute_tar_weights`、`compute_tar_loss` 与 `verl/workers/actor/dp_actor.py` 的 `_backward_tar_loss` 复制到 verl-agent 的同名文件。记忆库条目改为多轮基座成功轨迹，response_mask 只覆盖动作 token。
- DPH-RL：参照其 `scripts/llama/forward_kl.sh` 与离线 `data.sft_files` 机制，在 verl-agent 的 actor 更新中加入同样按动作 token 掩码的离线 NLL 项。剖面选轮、入口、随机选轮只在此基础上改轮掩码。

**Baseline 来源与复现入口**：

| Baseline / 组件 | 与本任务的关系 | 论文 | 代码与复现入口 |
|---|---|---|---|
| TAR | 离线回放族代表 | https://arxiv.org/abs/2610.24236 | https://github.com/wenzhilics/tar（2026-10-16；`recipe/tar/build_memory_bank.py`、`recipe/tar/run_qwen2_5_0.5b_tar.sh`、`verl/trainer/ppo/core_algos.py` 的 `compute_tar_weights` / `compute_tar_loss`、`verl/workers/actor/dp_actor.py` 的 `_backward_tar_loss`） |
| DPH-RL | 离线回放族代表（全局前向 KL） | https://arxiv.org/abs/2509.07430 | https://github.com/seamoke/DPH-RL（2026-02-10；`scripts/llama/forward_kl.sh`，README 的离线采样与 `forward` 配置） |
| PTGS | 采样侧代表（多轮 Sokoban / FrozenLake 上提出） | https://arxiv.org/abs/2610.01509 | https://github.com/changdaeoh/sharpening-tax（`ptgs/integration.py` 的 `PTGSHooks`；`sharpening_tax/benchmarks/webshop.py` 支持 `WEBSHOP_ENV_SEED`） |
| GRPO | 多轮 agent RL 标准做法 | https://arxiv.org/abs/2505.10978 | https://github.com/langfengQ/verl-agent（2026-06-09；`examples/grpo_trainer/run_webshop.sh`、`run_alfworld.sh`；`verl/workers/actor/dp_actor.py`、`verl/trainer/ppo/core_algos.py`） |
| 逐轮替换与分叉 | 真实环境中的检查点交接 | https://arxiv.org/abs/2609.19636 、https://arxiv.org/abs/2608.08239 | https://github.com/Xuanxuana1/AgenticRL_Handoff（2026-09-26；`src/handoff/alfworld/{environment,rollout}.py`；为 WebShop 增加固定种子的真实环境回放） |

**算力与 API 预算**（8×A100 80G，无付费 API）：
- 阶段 0：2 个环境各 1 次 GRPO（各约 8 卡 × 8–12 小时）加评测，约 1 天。
- 阶段 A：
  - WebShop 800 × 19 种条件 × 32 ≈ 49 万条；ALFWorld 274 × 16 × 32 ≈ 14 万条；
  - 按约 23 万条 / 天，约 2.6 天。
- 阶段 B：
  - WebShop 7 组 × 3 种子 + 6 次超参比较中的第二个设置 = 27 次；ALFWorld 4 × 3 + 3 = 15 次；
  - 共 42 次，每次约 8 卡 × 7 小时，约 12 天；
  - 评测：(21 × 800 + 12 × 274) × 32 ≈ 64 万条，约 3 天。
- 合计约 19 天；API 费用为 0。阶段 0 与阶段 A 共约 3.6 天，即可得到剖面、全部对应物增益与功效分析。
