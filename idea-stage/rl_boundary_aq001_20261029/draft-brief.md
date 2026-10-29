## 背景

**定位关键词：** multi-turn agent RL；pass@k coverage；diversity collapse；forward KL；checkpoint handoff；WebShop；ALFWorld

**一句话定位：** 多轮工具 agent 的 RL 在大 k 采样下丢失可解任务覆盖时，丢失发生在轨迹的哪些轮因环境而异；保覆盖的修法应当在训练中自己找到这些轮，而不是写死位置。

## 核心 Claim

**已知**：
- **丢失的是什么**：Sharpening Tax（arXiv 2610.01509）与 PBA（arXiv 2607.20543）说明 RL 会丢掉基座中稀有的成功轨迹，PBA 按题向基座锚定。
- **丢在哪里（单轮）**：Locked at the Entrance（arXiv 2608.29188）在单轮任务上把丢失定位到入口；DivInit（arXiv 2606.17209）在 agent 搜索上只修第一轮。
- **怎么保**：DPH-RL（arXiv 2509.07430）用前向 KL 保覆盖，但施加在整条序列上。
- **相邻的定向工作**：Archer（arXiv 2507.15778）在单轮里按熵对不同 token 施加不同 KL；Critical-State RL（arXiv 2609.24985）诊断出值得训练的状态后只训练那里。
- **反面证据**：Coverage, Not Targeting（arXiv 2609.02417）发现多轮 agent 的信用分配在低验证信息密度下，“集中到选定轮”与“集中到随机轮”同样有害，定向是二阶的。

1. **锁定位置因环境而异。** 设 B 为起点策略，G 为从 B 出发、同一设置下只做 GRPO 的检查点。在真实环境中逐轮替换（只把第 t 轮换成 B 生成，其余轮由 G 生成并继续），减去同模型分叉的噪声底，得到可找回覆盖的剖面 L(t)。我们预期 WebShop 与 ALFWorld 的 L(t) 形状不同：WebShop 集中在入口与搜索后的选择轮，ALFWorld 分布在中段的探索轮。为避免剂量混杂，“入口 vs 后续轮”的比较只在替换轮数相同的组之间进行。
2. **锚定的定向是一阶的，与信用分配不同。** 与 2609.02417 的结论相对，前向 KL 锚定施加在哪些轮，比施加多少更重要：在锚定 token 占比相同的条件下，按 L(t) 选轮明显优于随机选轮。理由是锚定作用于分布（保住被抛弃的分支），而信用分配作用于奖励信号。
3. **按轮自适应的风险任务前向 KL，在两个环境上都追平各自剖面最优的固定掩码，而任何单一固定掩码都做不到。**
   - **风险任务**：起点策略离线样本中有成功、但当前策略这一组 rollout 全部失败的任务。
   - **做法**：只在风险任务上，按轮估计当前策略对基座成功动作的偏离，按偏离分配前向 KL 权重，不需要先跑诊断。
   - **预期一**：自适应权重与 L(t) 正相关；
   - **预期二**：在 pass@1–pass@64 前沿上，它在两个环境上都不劣于该环境的剖面最优掩码；而入口、全局、PBA 式按任务门控（全轮）、以及“在 WebShop 上诊断得到的掩码迁移到 ALFWorld”，至少在一个环境上落后。

**推翻条件**：
- 两环境 L(t) 剖面无显著差别，且某个固定掩码在两处都最好（Claim 1、3 减弱为“无需诊断即可追平最优掩码”）；
- 按剖面选轮与同 token 占比随机选轮相当（Claim 2 不成立）；
- 自适应权重与 L(t) 不相关，或自适应方法在任一环境上明显落后于剖面最优掩码（Claim 3 不成立）。

## 方法设计的核心思想

**诊断（用于验证，不是方法的输入）**：在真实环境中做逐轮替换与同模型分叉（Replay Gap，arXiv 2608.08239，指出必须在真实环境中重建状态）。WebShop 固定 `WEBSHOP_ENV_SEED`，ALFWorld 固定游戏文件与种子。得到 L(t) 与“剖面最优掩码”S*，即显著高于噪声底的轮。

**修法（按轮自适应的风险任务前向 KL GRPO）**：
1. 训练前对每个训练任务离线采样起点策略的轨迹，保留成功轨迹的“观察历史—动作”片段，按轮位置分组。
2. 每 N 步更新一次风险任务集合 R：起点策略有成功样本、当前策略本组 rollout 全部失败的任务。
3. 对 R 中任务，按轮 t 估计偏离 d_t = 平均[log π_B(a | h) − log π_θ(a | h)]，取起点策略成功片段中第 t 轮的动作。权重 w_t = max(d_t, 0) / mean(max(d, 0))，使总锚定量与全局前向 KL 相同。
4. 损失：GRPO 损失 + β · Σ_t w_t ·（R 中任务第 t 轮起点成功动作的负对数似然），即加权的逐轮前向 KL(π_B‖π)，估计方式同 DPH-RL。
5. 非风险任务与 w_t = 0 的轮不加散度。

**与最高近邻的关键差别**：
- DPH-RL：整条序列、单轮；
- PBA：按题门控、单轮、在策略样本上估计；
- Archer：按熵、单轮、减弱推理 token 的约束；
- Locked at the Entrance / DivInit：只修入口；
- Critical-State RL：选择可训练状态做 contextual-bandit 训练，不是保覆盖；
- Reach or Solve（arXiv 2609.19636）：SFT↔RL 交接、pass@1、无修法。

本方法在多轮 agent RL 中按轮、按风险任务自适应地决定前向 KL 施加在哪里，并用真实环境逐轮替换剖面验证它找到的位置。

## 最小实验

**阶段 0：前置检查（约 1 天）。**
- WebShop：B = Qwen2.5-7B 基座。把 Sharpening Tax 的 WebShop 文本 harness 移植进 verl-agent，商品子集、步数上限与 `WEBSHOP_ENV_SEED` 与之一致，训练与评测同一设置。
- ALFWorld：B = Qwen2.5-7B 基座；若其在 unseen 134 个任务上 pass@64 低于 30%，改用 Qwen2.5-7B-Instruct 作起点。纯 RL 的隔离相对起点成立。
- 各跑 1 个种子的 GRPO 得到 G。只有 G 的 pass@64 比 B 低至少 5 个百分点的环境才进入后续；两个环境都不满足则报告“纯 RL 不产生锐化税”并停止。PASS@(k,T)（arXiv 2604.14877）报告工具 RL 可扩大边界，这一结果是可能的。

**阶段 A：诊断（约 2.5 天）。**
- WebShop 300 个留出任务，t = 1…6；ALFWorld unseen 134 个任务，t ∈ {1, 2, 4, 8, 12, 16}。
- 每格做逐轮替换与同模型分叉，64 次 rollout。
- 剂量匹配：入口单轮替换 vs 后续单轮替换；以及 2 轮集合之间的比较。
- 多样性对照：同样轮上的等熵提温、REFT 式（arXiv 2605.28295）首动作多样化。
- 入口类测试时对照：DivInit、对 G 做晚层插值。

**阶段 B：训练比较（约 12 天训练 + 2.5 天评测）。**
- 两个环境各六个锚定组：全局前向 KL、PBA 式按任务门控前向 KL（全轮）、入口前向 KL、随机选轮前向 KL（锚定 token 占比与自适应方法相同）、剖面最优掩码前向 KL（S* 来自阶段 A）、自适应（本方法）。
- ALFWorld 再加“WebShop 的 S* 迁移”组。
- WebShop 另加 PTGS（同基准上降低锐化税的方法）与熵奖励。
- 系数与种子：每个锚定组扫 2 个系数（1 个种子）画 pass@1–pass@64 前沿；再对本方法与前沿上最强的另一组，在 pass@1 与 GRPO 最接近的系数上补到 3 个种子。GRPO 各环境 3 个种子（阶段 0 的计为第 1 个）。
- 控制：同一环境内所有组组大小、步数、学习率、rollout 预算相同，前向 KL 组用同一批离线起点样本。
- 评测：WebShop 300 个留出任务、ALFWorld unseen 134 个任务的 pass@1 与 pass@64，按任务配对 bootstrap 报告置信区间；另报告训练中 w_t 与 L(t) 的 Spearman 相关。

**支持 / 推翻 Claim 的结果**：见核心 Claim 的预期与推翻条件。

**Baseline 来源与复现入口**：

| Baseline / 组件 | 与本任务的关系 | 论文 | 代码与复现入口 |
|---|---|---|---|
| Sharpening Tax harness、指标 | 同基准的锐化税测量 | https://arxiv.org/abs/2610.01509 | https://github.com/changdaeoh/sharpening-tax（2026-10-02；`sharpening_tax/benchmarks/webshop.py`、`metrics.py`） |
| PTGS | 同基准上降低锐化税的 RL 采样方法 | 同上 | 同仓库 `ptgs/integration.py` 的 `PTGSHooks`，接入 verl-agent 的 GRPO 组采样（原作只在 Sokoban / FrozenLake 验证） |
| GRPO、熵奖励 | 多轮 agent RL 标准做法 | https://arxiv.org/abs/2505.10978 | https://github.com/langfengQ/verl-agent（2026-06-09；`examples/grpo_trainer/run_webshop.sh`、`run_alfworld.sh`；熵项为框架选项） |
| 全局 / 入口 / 随机 / 剖面掩码 / 自适应前向 KL | 保 pass@k 的质量覆盖型散度 | https://arxiv.org/abs/2509.07430 | https://github.com/seamoke/DPH-RL（2026-02-10；README 的离线采样与 `forward` 散度配置；损失项移植到 verl-agent 并按轮加权） |
| PBA 式按任务门控 | 按题锚定基座保覆盖 | https://arxiv.org/abs/2607.20543 | 未见代码；按论文描述本地实现（按任务是否有足够起点成功证据门控，对风险任务施加向冻结起点的散度），此处统一用前向 KL 以与其余组可比 |
| 晚层参数插值 | 单轮入口锁定的修法 | https://arxiv.org/abs/2608.29188 | https://github.com/ershiyidian/early-branch-locking（2026-09-01；`src/early_branch_locking/countdown/layer_interpolation.py`） |
| DivInit | agent 搜索的第一轮多样化 | https://arxiv.org/abs/2606.17209 | https://github.com/cxcscmu/diverse-query-initialization（main 可访问） |
| REFT / 等熵提温 | 只增加多样性的对照 | https://arxiv.org/abs/2605.28295 | 在选定轮的首动作上做 top-N 均匀采样 / 温度调整 |
| 逐轮替换与分叉 | 真实环境中的检查点交接 | https://arxiv.org/abs/2609.19636 、https://arxiv.org/abs/2608.08239 | https://github.com/Xuanxuana1/AgenticRL_Handoff（2026-09-26；`src/handoff/alfworld/{environment,rollout}.py` 可直接用于 ALFWorld；为 WebShop 增加固定 `WEBSHOP_ENV_SEED` 的真实环境回放） |

**算力与 API 预算**（8×A100 80G，无付费 API）：
- 阶段 0：2 个环境各 1 次 GRPO（各约 8 卡 × 8–12 小时）加评测，约 1 天。
- 阶段 A：WebShop 约 35 万条、ALFWorld 约 20 万条轨迹（ALFWorld 轨迹更长），vLLM 约 2.5 天。
- 阶段 B：
  - WebShop：12 次扫描 + 4 次补种子 + 2 次 GRPO + PTGS 2 次 + 熵奖励 2 次 = 22 次；
  - ALFWorld：14 次扫描 + 4 次补种子 + 2 次 GRPO = 20 次；
  - 每次约 8 卡 × 6–8 小时，约 12 天；评测约 2.5 天。
- 合计约 18 天；API 费用为 0。
- 阶段 0 与阶段 A 共约 3.5 天，即可判断 Claim 1 并得到 S*。若两环境剖面相同，阶段 B 可缩减为单环境验证“自适应追平最优掩码”。
