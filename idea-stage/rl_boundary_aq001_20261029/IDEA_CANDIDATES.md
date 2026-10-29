# Idea 候选池

> 本文件由 idea improver 持续维护。保留所有进入过比较的实质性候选及其演化关系；不要把完整 proposal 写进这里。

- 输入模式：`problem_card`
- 输入论文：不适用
- 输入问题卡：`path-stage/LLM热门方向_算力适配_20261028/` 中的 `A-Q001`

## 当前选择

- Reviewer 调用：`6 / 8`
- 当前选中 Idea：无（等待用户决定）
- 当前自评分：IDEA-008 `7.5/10`（Call 6 得 7.8）
- 选择理由：剩余阻碍是“修法新颖性取决于实验结果”，纸面修订无法消除；剂量混杂与 2609.02417 定位可修。
- 状态：`暂停：等待用户决定`

## 候选列表

### IDEA-001：同一 SFT 起点只隔离 RL，按初始成功率分层测 pass@(k,T) 与 Reach/Solve

- 来源：`问题卡切口`
- 父 Idea：`无`
- 状态：`available`
- 定位关键词：agentic RL；pass@k；pass@(k,T)；checkpoint handoff；GRPO
- 一句话背景：多轮工具 agent 的 RL 何时扩大可解集合、何时只锐化。
- 自评分：`5.0/10`
- 一段话概括：从同一 SFT 检查点只做 GRPO，按初始采样成功率（0 / 低 / 高）分层，测 pass@(k,T) 与 Reach/Solve，控制 harness、环境、数据与预算。
- 打分理由：纯诊断，[2604.14877] 已在匹配数据下分离 SFT 与 RL 并按任务类型给出结论，增量主要是分层与组合测量，缺少方法贡献。
- Idea 生成依据：来自问题卡 A-Q001 的“可检验切口”。
- 自评分轻量新意依据：[2604.14877]、[2609.19636]、[2610.01509] 摘要。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：分层与 Reach/Solve 组合测量。
- Baseline 可复现性：未填。
- Reviewer 记录：`尚未送审`

### IDEA-002：锐化税付在路上，不在终点——多轮 agent 覆盖损失的轨迹内定位与按轮修法

- 来源：`领域共性不足`（结合 `最高近邻不足`：Sharpening Tax 只到任务级）
- 父 Idea：`无`
- 状态：`needs_revision`（子 Idea：IDEA-005）
- 定位关键词：sharpening tax；pass@k；agentic RL；checkpoint handoff；reach and solve；exploration；WebShop；BFCL
- 一句话背景：多轮工具 agent 的后训练在一些基准上缩小大 k 覆盖（锐化税），在另一些基准上扩大覆盖，原因未分离。
- 自评分：`7.3/10`
- 一段话概括：Claim：多轮 agent 的覆盖变化应拆成“能否到达可解状态（Reach）”与“到达后能否完成（Solve）”两段。后训练普遍提高 Solve，却让早期几轮的分支选择塌缩、降低 Reach 的多样性；当任务成败主要卡在早期探索（如 WebShop 的搜索与翻页）时表现为锐化税，主要卡在执行（如 BFCL 的 API 调用序列）时表现为扩展。方法：（1）测试时按轮交接解码——前 m 轮用基座、之后用后训练模型；（2）训练时只在早期 m 轮对起始策略做锚定（KL 或提高采样温度），m 由定位实验给出。最小实验：用 Sharpening Tax 已发布的 ≤9B 基座 / 后训练对，在 WebShop 与 BFCL v4 multi-turn 上做四种交接组合的大 k 曲线；再在 verl-agent 上从同一起点训练 GRPO / GRPO+PTGS / 早期轮锚定，比较 pass@1 与 pass@128。
- Story line：Sharpening Tax [2610.01509] 在 14 对发布检查点、3 个 agentic 基准上发现后训练把任务推向“总能解 / 从不解”两端，并报告全局调温度不能解决准确率与覆盖的矛盾；Pass@(k,T) [2604.14877] 却在受控工具 RL 上看到大 k 扩展，只出现在需要组合式信息收集的任务上。用 Sharpening Tax 公开的逐任务结果计算可见，同一对检查点在不同基准上方向相反：Qwen2.5-7B 在 BFCL v4 multi-turn 上 pass@128 比基座高 38.0 个百分点，在 WebShop 上低 14.4；Ministral-3-8B 分别为高 10.5 与低 24.2。所以差别不只来自配方。被忽视的是多轮结构：早期决策决定后面能到达哪些状态。Reach or Solve [2609.19636] 已用检查点交接在 pass@1 上分离到达与完成，但没有在大 k 覆盖上做。本 Idea 用按轮交接把覆盖损失定位到轨迹的某一段，并只在那一段保留多样性。可推翻的预期：在 WebShop 上，“基座前 m 轮 + 后训练其余轮”的 pass@128 不低于基座、pass@1 接近后训练模型，而反向交接恢复不了覆盖；在 BFCL 上覆盖增益来自 Solve 段；训练时早期轮锚定在相同 pass@1 下比 PTGS 和全局温度付更少的税。若反向交接同样能恢复覆盖，或覆盖损失均匀分布在各轮，则 Claim 被推翻。
- 打分理由：问题分量大、能直接解释卡上的跨论文矛盾，诊断只需推理即可快速给出 go/no-go，修法简单；按轮调温度与 EAD（token 级退火）[2510.05251]、PTGS（按题调温）相邻，主要新意在轨迹内定位，需要 reviewer 检索确认。
- Idea 生成依据：问题卡 A-Q001 证据 [2610.01509]、[2604.14877]、[2609.19636]；主执行器用 Sharpening Tax 仓库 `data/outcomes_42cells.csv.gz`（14 对 × 3 基准、每任务 128 次 rollout）按 pass@k 无偏估计自行计算的逐基准覆盖差；EAD [2510.05251]。
- 自评分轻量新意依据：检索“multi-turn agent RL early turn entropy collapse coverage”“hybrid decoding base prefix RL continuation pass@k”“turn-level temperature KL anchoring early turns”“RL agent coverage loss localized early decisions handoff”。命中 RAGEN-2 [2604.06268]（模板坍缩）、EAD、TurnOPD [2607.05804]、ExpDis [2610.10536]、CANOPY [2609.01245]、What Outcome RL Buys [2610.34894]（单轮数学的题目级 Reach，非多轮状态）；未检出在多轮 agent 上按轮定位锐化税的工作。需要 reviewer 检索。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：把多轮 agent 的锐化税定位到轨迹中的到达段，并据此给出只作用于早期轮的测试时与训练时修法。
- Baseline 可复现性：

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 开源代码与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| Sharpening Tax harness / 指标 / 按任务路由 | 同基准、同检查点的锐化税测量 | https://arxiv.org/abs/2610.01509 | https://github.com/changdaeoh/sharpening-tax 已浅克隆核验（2026-10-02，含 `sharpening_tax/benchmarks/{webshop,bfcl,acebench}.py`、`metrics.py`、逐任务结果 CSV；README 说明不含 RL 训练基础设施） | 用其 harness 采样与评分；按任务路由按附录 D.4 本地实现 | 是 |
| PTGS | 同基准上降低锐化税的 RL 采样方法 | 同上 | 同仓库 `ptgs/integration.py` 的 `PTGSHooks`（组温度分配与结果回填钩子） | 接入 verl-agent 的 GRPO 组采样 | 是 |
| GRPO（WebShop） | 多轮 agent RL 标准做法 | https://arxiv.org/abs/2505.10978 | https://github.com/langfengQ/verl-agent 已核验（2026-06-09，`examples/grpo_trainer/run_webshop.sh`） | 直接运行，改起点模型与种子 | 是 |
| 检查点交接 | 拆分到达与完成的协议 | https://arxiv.org/abs/2609.19636 | 未见代码；协议简单，可在 WebShop / BFCL 上按动作回放本地实现 | 回放前 m 轮动作后交给另一策略 | 是 |
| BFCL v4 multi-turn | 评测环境 | https://github.com/ShishirPatil/gorilla | 已核验 HEAD 6ea5797（2026-03-23）含 `BFCL_v4_multi_turn_base.json`，与 Sharpening Tax 固定的提交一致 | 设置 `BFCL_ROOT` | 是 |

- Reviewer 记录：`Call 1（常规，Opus 默认 effort）：5.5/10，promising_needs_revision，最高近邻 Sharpening Tax（2610.01509）、Reach or Solve（2609.19636）、Pass@k Inversion / PBA（2607.20543）、BACo（2511.05650）、EAD（2510.05251）/ REFT（2605.28295）`。阻碍：(1) 阶段 A 选的 Qwen3.5-4B/9B 在 WebShop 上 pass@128 只降 1.0/1.8，“方向相反”不成立，应选 Qwen2.5-7B、Ministral-3-8B；(2) 阶段 B 缺“GRPO 在 WebShop 上确实产生税”的前提，且训练与评测 harness 格式不一致；(3) 缺“后训练模型只在前 m 轮提温 / 首动作多样化”对照，且 B→R ≥ B→B 可单由 R 更强的完成能力解释。主执行器已用公开数据复核 (1)：Qwen2.5-7B WebShop 丢 107 个基座可解任务，Ministral-3-8B 丢 144 个。
- 现象核验：用 Sharpening Tax 公开逐任务结果自行计算（pass@k 无偏估计，k=128），≤9B 七对检查点在 BFCL 上全部持平或扩展，在 WebShop / ACEBench 上部分付税（如 Qwen2.5-7B：BFCL −38.0、WebShop +14.4、ACEBench +14.2，正值表示基座覆盖更高）。直接运行该仓库代码被安全策略拦下，只读取了数据文件。

### IDEA-003：锐化税来自小组采样下的信号饥饿

- 来源：`领域共性不足`
- 父 Idea：`无`
- 状态：`covered`
- 定位关键词：GRPO；zero-variance prompts；pass@k；signal starvation
- 一句话背景：RL 训练时成功率低于 1/G（G 为组大小）的任务拿不到梯度，可能被其他任务的更新挤压到零。
- 自评分：`4.0/10`
- 一段话概括：检验锐化税是否集中在训练时 p<1/G 的任务上，扩大组大小能否消除。
- 打分理由：CANOPY [2609.01245] 的“信号饥饿”、RAGEN-2 [2604.06268] 的 SNR 机制、PTGS 的按题调温已经覆盖。
- Idea 生成依据：[2609.01245]、[2604.06268]、[2610.01509]。
- 自评分轻量新意依据：同上三篇摘要。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：无，已被覆盖。
- Baseline 可复现性：未填。
- Reviewer 记录：`尚未送审`

### IDEA-004：从基座到达过的稀有状态重启 RL（Go-Explore 式）

- 来源：`相似领域成熟方法迁移`（Go-Explore 的“回到稀有状态再探索”）
- 父 Idea：`无`
- 状态：`available`
- 定位关键词：agentic RL；exploration；state reset；curriculum
- 一句话背景：多轮 agent RL 中，稀有但可解的状态很少被采样到。
- 自评分：`4.5/10`
- 一段话概括：用基座大 k 采样收集成功轨迹经过的中间状态，RL 训练时以一定比例从这些状态重启环境。
- 打分理由：SCoRe [2509.14257] 已从验证前缀开始做短视野 RL，反向课程类方法也已存在；新意低。
- Idea 生成依据：Go-Explore 思路；[2509.14257]。
- 自评分轻量新意依据：[2509.14257] 摘要。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：与已有前缀 RL 重合度高。
- Baseline 可复现性：未填。
- Reviewer 记录：`尚未送审`

### IDEA-005：RL 丢掉的是基座早期轮的分支分布，不只是多样性——按轮交接定位与基座锚定修法

- 来源：`领域共性不足`（结合 `最高近邻不足`）
- 父 Idea：`IDEA-002`
- 状态：`needs_revision`（子 Idea：IDEA-006）
- 定位关键词：sharpening tax；pass@k；agentic RL；checkpoint handoff；reach and solve；base model anchoring；WebShop；BFCL
- 一句话背景：多轮工具 agent 的后训练在一些基准上缩小大 k 覆盖、在另一些基准上扩大覆盖，原因未分离。
- 自评分：`7.0/10`
- 一段话概括：相对 IDEA-002 的实质修改：(1) Claim 收紧为“锐化税付在早期轮，且丢的是基座在早期轮的分支分布而不是多样性本身”，用“后训练模型前 m 轮提温 / 首动作多样化”对照把两者分开；(2) 诊断只用真正有方向反转的 Qwen2.5-7B 与 Ministral-3-8B，判别性比较改为固定完成者比较到达者（B→R vs R→R）、固定到达者比较完成者（R→B vs B→B）；(3) 训练修法改为只在早期 m 轮对冻结基座加 KL 锚定，从 Qwen2.5-7B 基座在 Sharpening Tax 的同一 harness 下训练与评测，并先做“GRPO 是否在 WebShop 上产生税”的前置检查，不成立则训练部分不作结论。
- Story line：同一对检查点在不同基准上覆盖方向相反（Qwen2.5-7B：WebShop 丢 107 个基座可解任务、BFCL 新解出 82 个；Ministral-3-8B：WebShop 丢 144 个、BFCL 新解出 46 个），说明差别不只来自配方。Sharpening Tax 指出全局调温不能化解矛盾，PBA [2607.20543] 在单轮数学上把税归因于基座中稀有正确轨迹在有限组采样里消失，并用按题锚定修复；但多轮 agent 中稀有正确轨迹往往由早期几轮的选择决定。若税付在早期轮且丢的是分布，那么固定完成者时换上基座做到达者应恢复覆盖，而让后训练模型在早期轮提温不能达到同等效果；据此，只在早期轮锚定基座的训练应比全局锚定、PTGS 与早期提温付更少的税。若早期提温与基座交接效果相同，则丢的只是多样性，修法退化为 EAD/REFT 的轮级版本，本 Claim 被推翻。
- 打分理由：修复了 Call 1 的三条阻碍，Claim 更尖锐且有明确推翻条件；新意边界仍依赖“分布 vs 多样性”的结果，修法与 PBA、EAD 相邻。
- Idea 生成依据：Call 1 review；[2607.20543]、[2511.05650]、[2605.28295] 摘要（主执行器已读）；Sharpening Tax 公开数据复核。
- 自评分轻量新意依据：检索见 IDEA-002；新增近邻 PBA、BACo、REFT 均为单轮或开放生成，未涉及多轮按轮定位；需要 reviewer 检索。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：在多轮 agent 上区分“丢失早期分支分布”与“丢失多样性”，并据此给出只锚定早期轮的训练修法。
- Baseline 可复现性：同 IDEA-002，另加 REFT（首动作多样化，按论文描述在早期轮本地实现）与全局 KL 锚定（verl-agent 自带 KL 损失项）。
- Reviewer 记录：`Call 2（常规，Opus 默认 effort）：6.8/10，promising_needs_revision，无 fatal blocker；最高近邻 Sharpening Tax、Reach or Solve（代码 github.com/Xuanxuana1/AgenticRL_Handoff，主执行器已核验）、PBA（2607.20543）、Sparse but Critical（2603.22446）、DPH-RL（2509.07430，代码 github.com/seamoke/DPH-RL，已核验）`。问题：(1) verl 的 KL 在策略样本上估计，惩罚不到丢掉的基座稀有分支，修法与机制不对齐，DPH-RL 已指出需前向 KL / JS；(2) 诊断用发布的 Instruct 对（混合 SFT/偏好/RL），修法作用于纯 GRPO，因果链跨了两种检查点；(3) Claim 1 只是再统计，且基座与后训练走不同 harness，任务结构与格式适配未分开；(4) 2 个种子分辨力不足。

### IDEA-006：纯 RL 的锐化税付在早期轮的基座分支上——按轮交接诊断与早期轮前向 KL

- 来源：`领域共性不足`（结合 `最高近邻不足`）
- 父 Idea：`IDEA-005`
- 状态：`needs_revision`（子 Idea：IDEA-007）
- 定位关键词：sharpening tax；pass@k；agentic RL；checkpoint handoff；reach and solve；forward KL；base model anchoring；WebShop
- 一句话背景：多轮工具 agent 的 RL 为什么在大 k 采样下缩小可解覆盖，丢失发生在轨迹哪里，能否只修那一段。
- 自评分：`7.4/10`
- 一段话概括：相对 IDEA-005 的实质修改：(1) 核心诊断改在“基座 B vs 从 B 出发只做 GRPO 得到的 G”上做，两者同一 harness，直接隔离 RL 并去掉格式混淆；发布的 Instruct 对只作外部印证，原 Claim 1 降为动机；(2) 修法改为只在前 m 轮使用质量覆盖型散度：在离线采样的基座早期轮片段上计算前向 KL（等价于对这些片段的似然项），后续轮不加，与“丢失基座稀有分支”的机制对齐；(3) 增加全局前向 KL（DPH-RL）与早期轮反向 KL 两个对照，分别检验“位置选择”与“散度方向”；(4) 训练种子增至 3。
- Story line：Sharpening Tax 与 PBA 指出后训练 / RLVR 会丢掉基座中稀有的正确轨迹，DPH-RL 指出反向 KL 保不住覆盖而前向 KL / JS 可以，但这三者都在任务级或单轮上操作；多轮 agent 中，稀有的正确轨迹往往由早期几轮的选择决定，而后续轮正是 RL 提高完成能力的地方。若锐化税付在早期轮的基座分支上，那么全局前向 KL 会把后续轮的完成能力也拉回基座、牺牲 pass@1，只在早期轮施加前向 KL 才能同时保住覆盖与 pass@1。诊断先在纯 RL 检查点上验证定位，再据此设定 m。推翻条件：G 上的覆盖损失不集中在早期轮；或等熵提温 / 首动作多样化恢复同样多的覆盖；或早期轮前向 KL 在相同 pass@1 下不优于全局前向 KL。
- 打分理由：修复了 Call 2 的四点意见，诊断与修法在同一检查点上闭环，散度方向与机制一致；修法仍可被看作 DPH-RL 的按轮选择版，新意主要落在多轮按轮定位与“分布 vs 多样性”区分上。
- Idea 生成依据：Call 2 review；DPH-RL、Sparse but Critical 摘要与 DPH-RL README（主执行器已读）；Handoff 仓库 README。
- 自评分轻量新意依据：同 IDEA-002 / 005 的检索；新增近邻 Sparse but Critical（单轮数学 token 级交叉采样）、DPH-RL（单轮、按题），均不涉及多轮按轮定位；需要 reviewer 检索。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：在纯 RL 的多轮 agent 上把锐化税定位到早期轮并区分分布与多样性，据此提出只在早期轮施加前向 KL 的训练修法。
- Baseline 可复现性：Sharpening Tax harness / PTGS（已核验）；verl-agent GRPO（已核验）；DPH-RL 前向 KL（github.com/seamoke/DPH-RL，2026-02-10，基于 verl，README 给出离线采样初始策略与 `forward` / `js` 散度配置）；Handoff（github.com/Xuanxuana1/AgenticRL_Handoff，2026-09-26，ALFWorld / TravelPlanner 的 writer / reader 交接，扩展到 WebShop / BFCL）。
- Reviewer 记录：`Call 3（常规，Opus 默认 effort）：8.2/10，experiment_ready，无 fatal blocker；最高近邻 Reach or Solve（2609.19636）、What RL Brings to Reasoning（2610.24663）、Sharpening Tax（2610.01509）、DPH-RL（2509.07430）、PASS@(k,T)（2604.14877）`。非阻断缺口：两种前向 KL 只按散度总量对齐单一系数，“相同 pass@1”未严格控制；交接组 64 次 rollout 只支持 k≤64；verl-agent WebShop 默认全量商品与 15 步上限，需与 harness 的 1000 商品、30 步对齐；需正面定位 2610.24663“后段选择贡献更大”的单轮结论。Call 4（复核，请求 xhigh，实际为 Opus 默认 effort 加深度思考提示）：6.5/10，promising_needs_revision，fatal blocker：未引用、未对照 Locked at the Entrance（arXiv 2608.29188，代码 github.com/ershiyidian/early-branch-locking，主执行器已核验，含 `countdown/layer_interpolation.py`）。该文在单轮 Countdown 与数学上已证明覆盖收缩集中在入口、替代分支仍可执行、提温与提示无效、晚层参数插值可在不损 pass@1 下提升覆盖 37%。另建议补“早期轮熵奖励”训练组以闭合 Claim 2→3。

### IDEA-007：多轮 agent 的覆盖只在入口被锁，还是在每次观察后被重新锁定——逐轮锁定剖面与决策轮前向 KL

- 来源：`领域共性不足`（结合 `最高近邻不足`：Locked at the Entrance 只在单轮）
- 父 Idea：`IDEA-006`
- 状态：`needs_revision`（子 Idea：IDEA-008）
- 定位关键词：sharpening tax；pass@k；agentic RL；checkpoint handoff；entrance locking；forward KL；WebShop；agentic search
- 一句话背景：单轮 RLVR 的覆盖收缩已被定位在入口；多轮 agent 每次收到环境观察后都会出现新的决策点，覆盖损失是否仍只在入口未知。
- 自评分：`7.2/10`
- 一段话概括：相对 IDEA-006 的实质修改：(1) Claim 1 改为两个竞争假设的区分——“入口锁定”（单轮 RLVR [2608.29188]；agent 搜索中第一轮查询冗余 [2606.17209]）vs “观察后重新锁定”（每次搜索结果返回后的检索 / 选择决策轮都被锁）；(2) 诊断从前缀交接改为逐轮替换（只把第 t 轮换成基座生成，其余轮由 G 生成并在真实环境中继续），并设同模型分叉对照测噪声底 [2608.08239]，得到逐轮锁定剖面；(3) 加入入口类对照：第一轮基座替换、DivInit、[2608.29188] 的晚层参数插值；(4) 修法改为在“决策轮”（发出搜索或在搜索结果页上做选择的轮）施加前向 KL，与“只在入口”和“全局”前向 KL、决策轮熵奖励、PTGS 对照，前向 KL 各组扫 3 个系数画 pass@1–pass@64 前沿；(5) 全部比较统一在 pass@64。
- Story line：[2608.29188] 在单轮任务上发现 RLVR 的覆盖丢在入口、替代分支仍可执行，入口修法有效；[2606.17209] 在 agent 搜索上把并行采样的瓶颈追到第一轮查询冗余。但多轮 agent 的每一轮都以新的环境观察为条件，搜索结果返回后的重新检索与选择同样是分支点。若 RL 在这些观察后的决策轮也锁定分支，那么只修入口（第一轮多样化、晚层插值）就不够，而全局锚定又会把后续轮中 RL 提高的完成能力拉回基座。逐轮替换剖面能直接区分两种假设：若可找回的覆盖集中在第一轮，单轮结论迁移到 agent，入口修法足够；若在后续决策轮也有相当部分，入口修法不足，修法必须覆盖所有决策轮。训练比较检验“决策轮前向 KL”是否在相同 pass@1 下优于入口前向 KL、全局前向 KL、晚层插值、决策轮熵奖励与 PTGS。
- 打分理由：Claim 1 变成多轮特有且两种结果都有信息量的区分问题，补齐了 Call 4 的最高近邻与对照；风险在于若剖面集中在第一轮，主结论会退化为单轮结论的迁移；实验总量增至约 11–12 天。
- Idea 生成依据：Call 4 review；[2608.29188] 摘要、局限性与仓库；[2606.17209]、[2608.08239]、[2610.25957]、[2609.20715] 摘要（主执行器已读）。
- 自评分轻量新意依据：检索“RL narrows solution space multi-turn agent each turn observation locking”“search agent RL query diversity collapse”“per-turn substitution base action RL agent attribution”，未检出在多轮 agent 上做逐轮锁定剖面或观察后重新锁定的工作；需要 reviewer 检索。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：在多轮 agent 的纯 RL 检查点上，用真实环境中的逐轮替换区分入口锁定与观察后重新锁定，并给出作用于决策轮的前向 KL 修法。
- Baseline 可复现性：IDEA-006 所列，加 Locked at the Entrance 晚层插值（github.com/ershiyidian/early-branch-locking，2026-09-01，`src/early_branch_locking/countdown/layer_interpolation.py`，与任务无关的权重插值，可直接作用于 G 与其早期检查点）与 DivInit（arXiv 2606.17209，摘要称代码已公开，送审前需核验）。
- Reviewer 记录：`Call 5（常规，Opus 默认 effort）：7.5/10，promising_needs_revision，无 fatal blocker；最高近邻 Locked at the Entrance（2608.29188）、Reach or Solve（2609.19636）、Sharpening Tax（2610.01509）、DPH-RL（2509.07430）、DDO（2609.10052）`。判断：Claim 1（逐轮替换区分入口锁定与观察后重新锁定）新颖且可证伪；Claim 2 部分是单轮“提温无效”的迁移，增量在观察后各轮与等熵对照；Claim 3 是 DPH-RL 前向 KL 加按轮掩码，方法新意薄且依赖 Claim 1。未收紧处：未与 DDO（WebShop 中段决策状态分支、成功策略覆盖）划界；“sharpening tax / checkpoint handoff / entrance locking”均为 2026 年单篇术语，应配 pass@k coverage、diversity collapse 等通用词；逐轮替换须固定 `WEBSHOP_ENV_SEED`；外部印证中基座与 Instruct 走不同格式，跨模型替换需按各自格式重新渲染历史。

### IDEA-008：多轮 agent 的纯 RL 是只在入口锁定还是在观察后重新锁定——逐轮锁定剖面与按剖面开处方的前向 KL

- 来源：`领域共性不足`（结合 `最高近邻不足`）
- 父 Idea：`IDEA-007`
- 状态：`needs_revision`
- 定位关键词：multi-turn agent RL；pass@k coverage；diversity collapse；entrance locking；checkpoint handoff；forward KL；WebShop
- 一句话背景：单轮 RLVR 的覆盖收缩已被定位在入口；多轮 agent 每次收到环境观察都会出现新的决策点，RL 造成的覆盖损失是否只在入口未知。
- 自评分：`7.5/10`
- 一段话概括：相对 IDEA-007 的实质修改：(1) Claim 3 改为“诊断开处方”的可证伪主张——锚定施加在哪些轮由阶段 A 的锁定剖面决定，并与“相同锚定 token 占比的随机选轮”对照，检验起作用的是锚定哪些轮而不是锚定多少；(2) Claim 2 收窄为增量部分：在观察之后的决策轮上，用等熵对照区分分布与多样性（单轮“提温无效”归属 [2608.29188]）；(3) 与 DDO [2609.10052] 划界：DDO 用 122B 专家在共享决策状态收集分支做离线偏好训练，不诊断 RL 在哪里锁定、也不在 RL 内修，不同预算，不作同预算对照；(4) 定位关键词换成通用词；(5) 固定 `WEBSHOP_ENV_SEED`；外部印证中按各模型自身格式重新渲染同一段历史。
- Story line：同 IDEA-007，修法部分改为：若剖面显示锁定集中在某些轮型（入口或观察后决策轮），则按剖面选定的轮施加前向 KL，应在相同 pass@1 下优于入口、全局与随机选轮（同 token 占比）的前向 KL；若随机选轮与按剖面选轮相当，说明起作用的只是锚定量，Claim 3 被推翻。
- 打分理由：保留 Call 5 认可的新颖诊断，把修法改成能被随机掩码对照推翻的“诊断—处方”主张，并补齐 Call 5 的划界与落地细节；方法本身仍简单，价值依赖诊断结果。
- Idea 生成依据：Call 5 review；DDO 摘要与目录（主执行器已读）。
- 自评分轻量新意依据：同 IDEA-007；DDO 为离线偏好训练、专家分支、无 RL 前后定位。需要 reviewer 检索。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：在多轮 agent 的纯 RL 检查点上区分入口锁定与观察后重新锁定，并验证“按锁定剖面选轮施加前向 KL”优于同量随机选轮。
- Baseline 可复现性：同 IDEA-007；DDO 代码 github.com/koguma00/direct_diverse_optimization（摘要页链接，未核验，因不作同预算对照）。
- Reviewer 记录：`Call 6（常规，Opus 默认 effort）：7.8/10，promising_needs_revision，无 fatal blocker；最高近邻 Locked at the Entrance（2608.29188）、Reach or Solve（2609.19636）、Sharpening Tax（2610.01509）、Coverage, Not Targeting（2609.02417）、PBA（2607.20543）`。判断：诊断（逐轮替换剖面区分入口锁定与重新锁定）新颖；修法新颖性取决于结果——若 L(t) 集中在第 1 轮，按剖面前向 KL 退化为入口前向 KL；匹配集中度的随机轮对照已见于 2609.02417，且其结果为“定向不优于随机”，削弱 Claim 3 先验；Claim 1 的“只换第一轮 vs 换全部决策轮”有替换轮数的剂量混杂；另提到 Critical-State RL（2609.24985）。
