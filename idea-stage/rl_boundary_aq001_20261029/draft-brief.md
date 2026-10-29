## 背景

**定位关键词：** agentic RL；sharpening tax；pass@k；checkpoint handoff；reach and solve；forward KL；base model anchoring；WebShop

**一句话定位：** 多轮工具使用 agent 的 RL 为什么在大 k 采样下缩小可解任务覆盖（锐化税），这部分覆盖在轨迹的哪一段丢失，能否只修那一段而保住 RL 的单次准确率增益。

## 核心 Claim

**动机（不作为贡献）**：Sharpening Tax（arXiv 2610.01509）公开的逐任务结果显示，同一对发布检查点在不同基准上覆盖方向相反。例如 Qwen2.5-7B 的后训练版在 WebShop 上让 107 个基座可解任务变成 0 次成功，在 BFCL v4 multi-turn 上新解出 82 个。但发布检查点混合了 SFT、偏好优化与 RL，基座与后训练版的提示路径也不同，所以下面的主结论只在“基座 vs 纯 RL”上建立。

1. **纯 RL 的锐化税付在早期轮。** 设 B 为基座，G 为从 B 出发、在同一文本 harness 下只做 GRPO 得到的检查点。按轮交接时，固定完成者为 G，把到达者从 G 换成 B（B→G vs G→G），大 k 覆盖的损失大部分被找回；固定到达者为 B，把完成者从 B 换成 G（B→G vs B→B），覆盖不降反升。即 RL 在后续轮提高了完成能力，覆盖损失来自早期几轮的选择。
2. **丢的是基座早期轮的分支分布，不只是多样性。** 让 G 只在前 m 轮把温度调到首轮动作熵与 B 相同（G_hot→G），或在前 m 轮做首动作 top-N 均匀采样（REFT 式，arXiv 2605.28295），找回的覆盖明显少于 B→G。也就是说，RL 改变的是早期轮把概率放在哪些分支上；单纯增加开头多样性（EAD，arXiv 2510.05251；REFT）不足以补救。
3. **只在前 m 轮施加质量覆盖型散度，能同时保住覆盖与 pass@1。** DPH-RL（arXiv 2509.07430）在单轮任务上表明，反向 KL 保不住覆盖，前向 KL / JS 可以。若 Claim 1、2 成立：
   - 在整条轨迹上加前向 KL，会把后续轮的完成能力也拉回基座、损失 pass@1；
   - 只在早期轮加反向 KL，惩罚不到丢失的稀有分支；
   - 只在前 m 轮对基座加前向 KL，应在相同 pass@1 下比这两者以及 PTGS 保住更多覆盖。

**推翻条件**：G 的覆盖损失不集中在早期轮（B→G 找回的不多于 G→B）；或 G_hot→G、G_REFT→G 与 B→G 找回同样多；或早期轮前向 KL 在相同 pass@1 下不优于全局前向 KL。

## 方法设计的核心思想

**诊断（按轮交接）**：前 m 轮由一个策略生成，把这段历史在环境中原样回放，再交给另一个策略继续。比较 B→B、G→G、B→G、G→B、G_hot→G、G_REFT→G 在 pass@k（k 至 128）上的曲线，交接点 m ∈ {1, 3}，并按任务统计覆盖损失发生在哪一侧。

**修法（早期轮前向 KL GRPO）**：
1. 训练前，对每个训练任务离线采样若干条基座轨迹，只保留前 m 轮（动作与回放得到的观察）。
2. 训练时，在 GRPO 损失之外，加“当前策略对这些基座早期轮动作的负对数似然”。它等价于只在前 m 轮的状态分布上的前向 KL(π_B‖π)，与 DPH-RL 用初始策略离线样本估计前向 KL 的做法相同。
3. 后续轮不加任何散度项；m 取诊断给出的值。

**与最高近邻的关键差别**：
- Sharpening Tax：任务级诊断与 PTGS；
- Reach or Solve（arXiv 2609.19636）：pass@1 上的 SFT↔RL 交接，交接点接近终点，不提修法；
- PBA（arXiv 2607.20543）：单轮数学、按题锚定基座；
- Sparse but Critical（arXiv 2603.22446）：单轮数学、token 级交叉采样，不看 pass@k；
- DPH-RL：单轮、在整条序列或按题施加前向 KL。

本方法在多轮 agent 的纯 RL 检查点上按轮定位锐化税，区分“丢分布”与“丢多样性”，并只在被定位的早期轮施加质量覆盖型散度。

## 最小实验

**阶段 0：前置检查（约 0.5 天）。**
- 设置：Qwen2.5-7B 基座 B。把 Sharpening Tax 的 WebShop 文本 harness 移植进 verl-agent 的 WebShop 环境，训练与评测用同一提示格式。
- 做法：跑 1 个种子的 GRPO 得到 G，在 300 个留出任务上比较 G 与 B 的 pass@64。
- 判定：只有 G 的 pass@64 比 B 低至少 5 个百分点，才继续阶段 A、B 的主结论；否则报告“该设置下 RL 不产生锐化税”。
- 依据：Sharpening Tax 公开数据中，该基座在此 harness 下 WebShop 的 pass@128 为 71.2%、pass@1 为 15.5%，有足够的初始成功率供 GRPO 学习。

**阶段 A：诊断，在 (B, G) 上做（约 1 天）。**
- 范围：WebShop 300 个留出任务；六种组合 × m ∈ {1, 3} × 64 次 rollout，G→G 与 B→B 各 128 次。
- 外部印证：在发布的 Qwen2.5-7B、Ministral-3-8B 对上，WebShop 与 BFCL v4 multi-turn base 各 200 个任务，只做 m=1 的 B→R 与 R_hot→R。

**阶段 B：训练修法比较。**
- 起点：B；同一 harness。
- 五组：GRPO、GRPO+PTGS、GRPO+全局前向 KL（DPH-RL）、GRPO+早期轮反向 KL、GRPO+早期轮前向 KL（本方法）。
- 控制：组大小、步数、学习率、rollout 预算相同；两种前向 KL 用同一批离线基座样本，系数按“训练中散度项总量相近”对齐；m 取阶段 A 的结果。
- 种子：3 个训练种子，阶段 0 的 GRPO 计为 GRPO 组的第 1 个。
- 评测：300 个留出任务上的 pass@1 与 pass@64，按任务配对 bootstrap 报告置信区间，并画 pass@1–pass@64 前沿。

**支持 / 推翻 Claim 的结果**：
- 支持：(B→G − G→G) 显著为正，且大于 (G_hot→G − G→G) 与 (G_REFT→G − G→G)；(B→G − B→B) ≥ 0；早期轮前向 KL 的 pass@1 不低于 GRPO，pass@64 高于全局前向 KL、早期轮反向 KL 与 PTGS（或在相同 pass@64 下 pass@1 更高）。
- 推翻：见核心 Claim 中的推翻条件。

**Baseline 来源与复现入口**：

| Baseline / 组件 | 与本任务的关系 | 论文 | 代码与复现入口 |
|---|---|---|---|
| Sharpening Tax harness、指标、逐任务结果 | 同基准的锐化税测量 | https://arxiv.org/abs/2610.01509 | https://github.com/changdaeoh/sharpening-tax（2026-10-02；`sharpening_tax/benchmarks/{webshop,bfcl}.py`、`metrics.py`、`data/outcomes_42cells.csv.gz`；BFCL 依赖 gorilla@6ea5797） |
| PTGS | 同基准上降低锐化税的 RL 采样方法 | 同上 | 同仓库 `ptgs/integration.py` 的 `PTGSHooks`，接入 verl-agent 的 GRPO 组采样 |
| GRPO、早期轮反向 KL | 多轮 agent RL 标准做法 | https://arxiv.org/abs/2505.10978 | https://github.com/langfengQ/verl-agent（2026-06-09；`examples/grpo_trainer/run_webshop.sh`，`use_kl_loss` 为框架选项，按轮位置加掩码） |
| 全局前向 KL（DPH-RL） | 为保 pass@k 设计的质量覆盖型散度 | https://arxiv.org/abs/2509.07430 | https://github.com/seamoke/DPH-RL（2026-02-10；基于 verl，README 给出离线采样初始策略与 `forward` / `js` 散度配置；将其损失项移植到 verl-agent） |
| 按轮交接 | 拆分到达与完成的评测协议 | https://arxiv.org/abs/2609.19636 | https://github.com/Xuanxuana1/AgenticRL_Handoff（2026-09-26；`src/handoff/`，ALFWorld / TravelPlanner 的 writer / reader 交接；为 WebShop 增加 `env.reset(session=goal_idx)` 后按序回放、为 BFCL 增加有状态 API 重放） |
| REFT / 等熵提温 | 只增加开头多样性的对照 | https://arxiv.org/abs/2605.28295 、https://arxiv.org/abs/2510.05251 | 在前 m 轮首动作上做 top-N 均匀采样 / 温度调整，采样层小改动 |
| 环境 | — | WebShop、BFCL v4 | WebShop 随 verl-agent 与 Sharpening Tax harness 提供；https://github.com/ShishirPatil/gorilla（`bfcl_eval/data/BFCL_v4_multi_turn_base.json`） |

**算力与 API 预算**（8×A100 80G，无付费 API）：
- 阶段 0：1 次 GRPO 约 8 卡 × 8–10 小时，加 300 × 64 次评测，约 0.5 天。
- 阶段 A：(B, G) 上 300 个任务 × (6 组合 × 2 交接点 × 64 + 2 × 128) ≈ 31 万条，外部印证约 10 万条；每条约 8 轮、生成约 1.6k token，vLLM 约 1.5 天。
- 阶段 B：离线基座早期轮采样不到 0.2 天；训练 5 组 × 3 种子 − 1 = 14 次，每次约 8 卡 × 8 小时，约 4.7 天；评测 15 个模型 × 300 个任务 × 64 次，约 1 天。
- 合计约 8–9 天；API 费用为 0。阶段 0 与阶段 A 共约 2 天，即可判断主 Claim 是否成立。
