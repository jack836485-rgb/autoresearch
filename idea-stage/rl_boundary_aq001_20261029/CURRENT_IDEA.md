## 背景

**定位关键词：** multi-turn agent RL；pass@k coverage；diversity collapse；replay；forward KL；state distribution；WebShop；ALFWorld

**一句话定位：** 单轮 RLVR 中，用离线回放基座成功解来保住 pass@k 覆盖的方法已经有效；搬到多轮工具 agent 时，回放的基座动作所在的状态，当前策略可能根本到不了。本研究检验这类方法在多轮 agent 中何时失效、为什么，以及能否在训练前预测。

## 核心 Claim

**已知**：
- **离线回放保覆盖（单轮）**：DPH-RL（arXiv 2509.07430）用离线基座样本上的前向 KL；PBA（arXiv 2607.20543）对风险题向基座锚定；TAR（arXiv 2610.24236）建基座多样成功解库，只在这些解被当前策略抑制时激活回放，按单侧对数似然差加权。三者都在单轮数学 / SQL 上验证。
- **覆盖丢在哪里（单轮）**：Locked at the Entrance（arXiv 2608.29188）在单轮上把丢失定位到入口。
- **状态来源重要**：2605.16826 把蒸馏目标拆成“前缀来源 × KL 方向”；2605.22731 提出后训练的状态分布视角；两者都在单轮蒸馏或 SFT/RL 上，不涉及保覆盖。
- **多轮中的回放**：Prefix-GRPO（arXiv 2607.19395）在多轮 agent 中回放教师前缀再在线续写，目标是学习效率，不是保覆盖。

1. **多轮 agent 中，基座与纯 RL 策略的状态重叠在第一次分支偏离后迅速下降，覆盖损失有相当部分落在低重叠状态上。**
   - 设 B 为起点策略，G 为从 B 出发只做 GRPO 的检查点。
   - **可找回覆盖剖面 L(t)**：在真实环境中逐轮替换（只把第 t 轮换成 B 生成，其余由 G 生成并继续），减去同模型分叉的噪声底，并做替换轮数相同的剂量匹配。
   - **状态重叠 O(t)**：在风险任务（B 有成功、G 整组失败）上，G 第 t 轮的状态与 B 成功轨迹第 t 轮状态等价的比例。WebShop 按页面类型与商品 / 检索结果判等，ALFWorld 按位置、物品与容器状态判等，均由环境状态程序判定。
   - **预期**：O(1) ≈ 1（入口共享），之后下降；L(t) 在 O(t) 低的轮上仍有显著值。
2. **离线回放类方法只能找回落在共享状态上的那部分覆盖。** 回放的监督施加在基座访问的状态上；当前策略不再访问这些状态时，回放既改变不了它在实际所处状态上的选择，也就找不回对应的覆盖。
3. **只改状态来源的受控对照可检验这一机制，且差异可在训练前预测。**
   - 对照组：保留 TAR 的“被抑制才激活、按单侧对数似然差加权”门控与风险任务限定，只把查询基座动作的状态从“基座离线轨迹”换成“当前策略在风险任务 rollout 中实际访问的状态”（在这些状态上采样基座动作，无需额外环境交互）。
   - 预测：两者的 pass@64 差随低重叠锁定量 M_low = Σ_t L(t)·(1 − O(t)) 增大。在任务级（按 M_low 分层）与环境级都成立；在 M_low ≈ 0 的任务上两者相同，即入口锁定、状态共享时离线回放足够，这也解释了单轮方法为何有效。

**推翻条件**：
- Claim 1：O(t) 在入口之后不下降，或 L(t) 全部落在高重叠轮；
- Claim 3：状态来源对照的覆盖差与 M_low 无关（任务级 Spearman 不显著），或学生状态版本在高 M_low 任务上不优于离线版本。

## 方法设计的核心思想

**测量（训练前，用于预测）**：在 (B, G) 上计算 L(t)、O(t) 与每个任务的 M_low。G 取 1 个种子的 GRPO 检查点。

**受控对照的两个版本**（只差状态来源）：
- **离线版（TAR 移植到多轮）**：训练前对每个训练任务离线采样 B 的成功轨迹建库；训练时，对风险任务上这些轨迹中的动作计算 δ = log π_B − log π_θ，在 δ > 0 处按 δ 加权 NLL。
- **学生状态版**：训练时，在风险任务的 G 自身 rollout 中，于每个状态采样 k 个 B 的动作；对这些动作计算同样的 δ，并在 δ > 0 处按同样方式加权 NLL。这相当于 2605.16826 所称“学生前缀 + 前向 KL”的目标，加上 TAR 的门控与风险限定。

两者的系数、风险任务集合、更新频率完全相同。

**与最高近邻的关键差别**：TAR、DPH-RL、PBA 在单轮上不存在状态失配问题；2605.16826、2605.22731 讨论状态来源，但在单轮蒸馏或 SFT/RL 保留上；Prefix-GRPO 在多轮中回放教师前缀，目标是学习效率；Locked at the Entrance 只定位单轮入口。本研究提出并检验多轮 agent 中“离线回放只能锚定共享状态”的机制，以及训练前可测、按任务的预测量。

## 最小实验

**阶段 0：前置检查（约 1 天）。**
- WebShop：B = Qwen2.5-7B 基座。Sharpening Tax 的 WebShop 文本 harness 移植进 verl-agent，商品子集、步数上限与 `WEBSHOP_ENV_SEED` 一致，训练与评测同一设置。
- ALFWorld：B = Qwen2.5-7B 基座；若其在 unseen 134 个任务上 pass@64 低于 30%，改用 Qwen2.5-7B-Instruct 作起点。
- 各跑 1 个种子的 GRPO 得到 G。只有 G 的 pass@64 比 B 低至少 5 个百分点的环境进入后续；都不满足则报告“纯 RL 不产生锐化税”并停止。

**阶段 A：测量（约 2.5 天）。**
- WebShop 300 个留出任务（t = 1…6），ALFWorld unseen 134 个任务（t ∈ {1, 2, 4, 8, 12, 16}）。
- 每格做逐轮替换与同模型分叉，64 次 rollout；做剂量匹配比较。
- 用环境状态计算 O(t) 与每任务 M_low。

**阶段 B：训练比较（约 11 天训练 + 2.5 天评测）。**
- 每个环境六组：GRPO、DPH-RL（离线前向 KL，全局）、PBA（风险门控）、TAR 离线版、学生状态版、学生状态前向 KL 不加门控（2605.16826 式目标，指向基座）。WebShop 另加 PTGS。
- 系数与种子：五个锚定组各扫 2 个系数（1 个种子），画 pass@1–pass@64 前沿；在 pass@1 与 GRPO 最接近的系数上，把 TAR 离线版与学生状态版补到 3 个种子。GRPO 3 个种子（阶段 0 的计为第 1 个）。
- 控制：同一环境内组大小、步数、学习率、rollout 预算相同。学生状态版额外的基座采样只在风险任务的状态上进行，计入训练时间并单独报告。
- 评测：WebShop 300 个留出任务、ALFWorld 134 个 unseen 任务的 pass@1 与 pass@64，按任务配对 bootstrap。
- 主分析：按阶段 A 的 M_low 把任务分为三层，检验“学生状态版 − TAR 离线版”的 pass@64 差是否随 M_low 单调增大（任务级 Spearman 与分层差）。

**支持 / 推翻 Claim 的结果**：见核心 Claim 的预期与推翻条件。

**Baseline 来源与复现入口**：

| Baseline / 组件 | 与本任务的关系 | 论文 | 代码与复现入口 |
|---|---|---|---|
| TAR | 离线回放基座成功解保覆盖，门控与本研究对照共用 | https://arxiv.org/abs/2610.24236 | https://github.com/wenzhilics/tar（2026-10-16；verl `recipe/tar/`，`build_memory_bank.py` 建库；移植到 verl-agent 的多轮轨迹） |
| DPH-RL | 离线前向 KL 保 pass@k | https://arxiv.org/abs/2509.07430 | https://github.com/seamoke/DPH-RL（2026-02-10；README 的离线采样与 `forward` 散度配置） |
| PBA | 按题风险门控、向基座锚定 | https://arxiv.org/abs/2607.20543 | 未见代码；按论文描述本地实现（风险门控 + 向冻结起点的散度） |
| 学生前缀前向 KL | 状态来源 × KL 方向中的 DAgger 式目标 | https://arxiv.org/abs/2605.16826 | 在 G 的 rollout 状态上采样基座动作做 NLL，verl-agent 内本地实现 |
| PTGS | 同基准上降低锐化税的 RL 采样方法 | https://arxiv.org/abs/2610.01509 | https://github.com/changdaeoh/sharpening-tax（`ptgs/integration.py` 的 `PTGSHooks`；原作只在 Sokoban / FrozenLake 验证） |
| GRPO | 多轮 agent RL 标准做法 | https://arxiv.org/abs/2505.10978 | https://github.com/langfengQ/verl-agent（2026-06-09；`examples/grpo_trainer/run_webshop.sh`、`run_alfworld.sh`） |
| WebShop harness | 同基准锐化税测量 | https://arxiv.org/abs/2610.01509 | 同 sharpening-tax 仓库 `sharpening_tax/benchmarks/webshop.py`（支持 `WEBSHOP_ENV_SEED`） |
| 逐轮替换与分叉 | 真实环境中的检查点交接 | https://arxiv.org/abs/2609.19636 、https://arxiv.org/abs/2608.08239 | https://github.com/Xuanxuana1/AgenticRL_Handoff（2026-09-26；`src/handoff/alfworld/{environment,rollout}.py` 用于 ALFWorld；为 WebShop 增加固定种子的真实环境回放） |

**算力与 API 预算**（8×A100 80G，无付费 API）：
- 阶段 0：2 个环境各 1 次 GRPO（各约 8 卡 × 8–12 小时）加评测，约 1 天。
- 阶段 A：WebShop 约 23 万条、ALFWorld 约 10 万条轨迹，vLLM 约 2.5 天。
- 阶段 B：
  - 每环境 10 次扫描 + 4 次补种子 + 2 次 GRPO = 16 次，WebShop 另加 PTGS 2 次，共 34 次；
  - 每次约 8 卡 × 6–8 小时；学生状态版因额外基座采样约多 20%；
  - 约 11 天；评测约 2.5 天。
- 合计约 17 天；API 费用为 0。阶段 0 与阶段 A 共约 3.5 天，即可判断 Claim 1，并得到每任务 M_low。
