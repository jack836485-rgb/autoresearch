## 背景

**定位关键词：** asynchronous reinforcement learning；training-inference mismatch；policy staleness；decoupled PPO；importance sampling；partial rollout

**一句话定位：** 在异步 LLM agentic RL 的离策略校正中，训练端在 rollout 生成版本上的 token 概率（old logits）经常缺失，导致"训练–推理数值偏差修复"与"策略陈旧度校正"无法按语义分开。

**与起点问题的关系：** 原问题。保留对象（缺失 old logits 时的解耦离策略校正）、条件（异步、延迟更新、部分 rollout 使一条轨迹跨多个参数版本）和评价目标（后期稳定性与任务成功率），提出一种不需要历史权重的 old logits 恢复方法；起点问题中"哪些声称无损的系统没有保留 old logits"的系统审计不在本 Idea 内，阈值耦合导致后期崩溃的机理只通过恢复精确语义间接检验。

## 核心 Claim

**主贡献：** 一个逐 token 的 old-logit 估计，使任何陈旧度、任何跨版本的部分 rollout 都能以一次推理端 prefill 的代价获得接近精确的"偏差 × 陈旧度"分解，而不保存或重载历史权重。

记 token $y_t$ 在版本 $v_t$ 由推理端采样，其推理端概率 $q_{v_t}(y_t)$ 已在采样时记录；训练端当前权重为 $\theta$。缺失的量是训练端在 $v_t$ 上的概率 $p_{v_t}(y_t)$。本方法在推理端载入 $\theta$（异步系统每次更新后本来就要同步）后，对待训练轨迹做一次 prefill 打分得到 $q_\theta(y_t)$，并用训练端解耦损失本来就要算的 $p_\theta(y_t)$，估计
$$\log\hat p_{v_t}=\log q_{v_t}+\big(\log p_\theta-\log q_\theta\big).$$
于是陈旧度比率 $p_\theta/\hat p_{v_t}=q_\theta/q_{v_t}$ 在同一推理端数值下测量，偏差比率 $\hat p_{v_t}/q_{v_t}=p_\theta/q_\theta$ 在同一权重下测量，两者语义都干净。估计误差恰为数值偏差 $e_x=\log p_x-\log q_x$ 随版本的变化 $e_\theta-e_{v_t}$；一阶近似为（两种数值实现下的得分之差）与权重更新量的内积，是"偏差 × 滞后"的二阶小量。现有代理的误差则是一阶的：用当前训练端作参考（Decoupled PPO）误差为全部滞后，直接用 rollout 概率作参考误差为全部偏差，插值/EWMA 代理只改变有效裁剪边界或参考位置。

**可推翻的判断：** 在数值偏差不可忽略的设置（MoE 不做路由回放）中，(1) 本估计的逐 token 误差、以及由其决定的解耦掩码/PPO 裁剪 token 集合与精确 old logits 的不一致率，在版本差 1–16 内都明显低于所有零历史权重代理；(2) 用它替代精确 old logits 训练，任务成功率与后期稳定性与精确快照处于同一噪声带，并优于最强的非精确代理，额外代价远低于快照。

**当前依据与适用条件：**
- 精确 old logits 有实质价值：2605.12070（异步 agentic RL，ROLL，最大版本差 3）在同一解耦目标下，Snapshot 精确 old logits 相对当前训练端代理在 VitaBench in-store 上 4B 从 19.83 到 28.89、30B-A3B 从 18.28 到 34.62（avg@2），但每步额外 95–178 s、最多驻留 76 GB 快照，作者实验只到版本差 3，并说明其低成本近似 PPO-EWMA 在极端版本差下可能不可靠。
- 估计误差小的依据：2610.40945 用训练端在采样权重上的前向精确拆分误差，在 Qwen3-0.6B/1.7B 上观察到数值偏差在训练中近似常数（FP8 采样约 0.02 nats/token，BF16 低于 $10^{-3}$）且不随累计更新变化，滞后一阶为累计更新在得分上的投影。这支持"偏差可在当前版本测量后搬回旧版本"。
- 仍未知：该常数性是逐 token 成立还是只在平均意义上成立；MoE 中路由在两个版本间翻转的 token 可能破坏一阶论证；推理端 prefill 打分与生成时 decode 的数值差会进入估计；上述 2610.40945 证据只在小稠密模型、单轮 Countdown 上。本 Idea 的效果依据是"恢复精确语义"加上"精确语义已被证明有用"，而非已测得的本方法收益。

## 方法设计的核心思想

- **输入**：异步缓冲区中的轨迹，含逐 token 生成版本 $v_t$ 与推理端 logprob $\log q_{v_t}$（AReaL 已记录 `versions` 与 `logprobs`）；当前训练端权重 $\theta$。
- **动作**：每次权重同步后，推理端在 $\theta$ 上对即将训练的批次做一次 prefill 打分（只取 logprob，不生成），得到 $\log q_\theta$；训练端照常前向得到 $\log p_\theta$；按上式构造 $\log\hat p_{v_t}$，原样代入 2605.12070 的解耦目标（偏差比率做对称掩码，陈旧度比率做 PPO 裁剪）。MoE 时同时记录推理端在 $v_t$ 与 $\theta$ 上的路由，路由不一致的 token 单独统计（必要时掩码）。$\log\hat p$ 在一次更新的所有 minibatch 内固定。
- **输出**：替代缺失 old logits 的逐 token 估计，以及两个语义分离的比率。
- **与最高近邻的关键差别**：Snapshot/专用 old-logit 模型在训练端重放历史权重，成本随版本数与跨版本轨迹增长；PPO-EWMA 与 A-3PO 构造近似参考策略，不恢复真实 old logits；DLC（2610.40945）的分解需要训练端在采样权重上前向，即假设 old logits 可得。本方法改为"偏差在当前版本测、滞后在推理端测"，只需推理端已持有的当前权重。

## 最小实验

**阶段 A：离线保真度（先做，可直接给出 no-go）。**
- 设置：AReaL 异步训练 Search-R1（公开 NQ+HotpotQA 训练集与 e5 检索器）。稠密 Qwen3-4B（BF16 推理）与 MoE Moonlight-16B-A3B（BF16 推理、不做路由回放）各跑约 20 步并保存每步权重（Moonlight 约 32 GB/版本，存数据分区）。
- 对 512 条在版本 $v$ 生成的轨迹，真值为训练端在 $v$ 上前向的 $\log p_v$；在 $\theta=v+g$，$g\in\{1,2,4,8,16\}$ 上比较五种 old-logit 来源：rollout 概率（Bypass）、当前训练端（Decoupled PPO）、A-3PO 对数线性插值、修订版 PPO-EWMA、本估计。指标：逐 token $|\log\hat p-\log p_v|$ 分布；在固定阈值下偏差掩码与 PPO 裁剪 token 集合与真值的不一致率；推理端 prefill 与生成时 decode 在同一版本上的 logprob 差；MoE 路由翻转 token 的占比与其误差。
- 停止条件：若 MoE 设置下 $g\le4$ 时本估计的决策不一致率不低于最佳代理的一半，则判 no-go，不进入阶段 B。

**阶段 B：异步训练对比（8×A100，4 卡推理 + 4 卡训练，沿用 AReaL `examples/r3` 的 Moonlight 单机配置）。**
- 相同核心条件：同一 Search-R1 数据、组大小、学习率、最大版本差 4、部分 rollout 开启；统一使用 2605.12070 的解耦目标与同一组偏差/陈旧度阈值，各臂只改变 old logits 来源；250 步。
- 对照与复现路线：
  - Bypass（rollout 概率作 old）：标准设置，偏差比率恒为 1。
  - Bypass + R3：AReaL 已核验示例（`return_routed_experts` 与 `enable_router_replay`），代表 MoE 偏差的工程修复。
  - Decoupled PPO：AReaL 已核验实现（`use_decoupled_loss`，`prox_logp_method=recompute`）。
  - 修订版 PPO-EWMA：原作者仓库不可读，按 2605.12070 §5.2 与附录 B 独立复现（β 按期望陈旧度窗口取中心，Train-Infer Mask 低于 0.2 时重置）。
  - Snapshot 精确 old logits（上界）：按 2605.12070 §5.1 独立实现，CPU 保留最近 4 个版本权重，按逐 token 版本分组做训练端前向。
  - 本方法：在 AReaL 远程 SGLang 引擎已有的 `compute_logp` 打分路径（`return_logprob` + `logprob_start_len`）上加一个"权重同步后对待训练批次打分"的钩子。
- 种子：6 臂各 1 种子；Snapshot、本方法与阶段 A 中最好的零历史权重代理各补 1 个种子。
- 评测：7 个 QA 测试集 EM；后期崩溃（成功率从峰值下降超过预设幅度）；活跃 token 比例；每步额外耗时、推理端 GPU 时间占用与内存。
- 支持主张的结果：本方法与 Snapshot 的 EM 与稳定性在两种子噪声带内，优于最强非精确代理，且额外耗时显著低于 Snapshot。推翻主张的结果：本方法退化到 Bypass 或 Decoupled PPO 的水平，或阶段 A 的保真度优势不转化为训练差异。
- 扩展（预算允许）：最大版本差 8，比较本方法、修订版 PPO-EWMA、Bypass+R3 与按 2607.22186 方法节独立复现的 ENTR（无公开代码）；Snapshot 在此处内存成本过高，只在阶段 A 离线评估。

**成本估计：** 阶段 A 约 1 天（4 张 A100，多为前向，约 700 GB 磁盘存权重）；阶段 B 约 9 次运行 × 约 12 小时 ≈ 4.5 天（8 张 A100），步时按单机 Moonlight 异步多轮任务约 3 分钟估计，待阶段 A 实测修正；不需要付费 API。本方法新增代价为每步一次推理端 prefill，规模为批次 token 数，预计远小于 Snapshot 的训练端历史前向，以实测为准。
