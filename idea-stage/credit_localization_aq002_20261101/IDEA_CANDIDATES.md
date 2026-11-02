# Idea 候选池（A-Q002）

- 输入模式：`problem_card`
- 输入论文：不适用
- 输入问题卡：`path-stage/LLM热门方向_算力适配_20261028` 的 `A-Q002`

## 当前选择

- Reviewer 调用：`3 / 17`
- 当前选中 Idea：`无（最佳已审候选为 IDEA-002 / IDEA-003，均 6.0）`
- 当前自评分：`—`
- 选择理由：IDEA-004 接受 Call 2 的判断（锚点分组即抬高 V_d），把检验改为覆盖理论的定量预测：以'落在有结果方差的锚点组中的步数比例'为锚点 V_d，检验 GiGPO 对均匀覆盖的优势是否在约 0.8 附近换号；用组大小 N 而非稀释改变 V_d，避免机械趋同。
- 状态：`暂停：用户 2026-11-01 决定先重刷研究地图，见 PIVOT_OR_STOP.md`

## 候选列表

### IDEA-001：在 ALFWorld / WebShop 上给已发表方法补等量均匀与打乱对照（卡片切口）

- 来源：`问题卡切口`
- 父 Idea：`无`
- 状态：`available`
- 定位关键词：credit assignment；GiGPO；GRPO；ALFWorld；WebShop
- 一句话背景：多数轮次信用方法论文没有等量随机 / 均匀信用对照。
- 自评分：`6.3/10`
- 一段话概括：对 GiGPO、AgentOPSD 补"总信用相同的均匀摊开"与"轨迹内打乱"对照，报告定位贡献占比。
- 打分理由：问题清楚但容易被视为审计；缺少机制与可预测性。
- Reviewer 记录：`尚未送审`

### IDEA-002：定位信息的第二个来源——rollout 间状态复现决定轮次定位何时胜过均匀覆盖

- 来源：`领域共性不足`（结合 `最高近邻不足`：2609.02417 的 V_d 只计验证器暴露）
- 父 Idea：`IDEA-001`
- 状态：`needs_revision`
- 定位关键词：credit assignment；GiGPO；anchor states；GRPO；ALFWorld；WebShop
- 一句话背景：2609.02417 用验证器信息密度 V_d 解释"覆盖胜过定位"，但 ALFWorld / WebShop 上主流的步级信用方法不靠验证器暴露中间轮次，而是靠多条 rollout 经过同一状态（锚点）来比较动作。
- 自评分：`7.6/10`
- 一段话概括：C1：在 ALFWorld / WebShop 上，GiGPO 相对 GRPO 的增益可分解为"覆盖"与"定位"两部分（等总量均匀对照、轨迹内打乱对照），两环境的定位占比不同。C2：定位占比由锚点复现率 ρ（落在大小 ≥2 的步级组中的步数比例，GiGPO 代码已记录组大小）决定，而非 V_d；因果操纵 ρ——只在信用计算时随机把比例 q 的锚点匹配拆成单例（不改变模型输入与环境），以及改变组大小 N——定位占比随 ρ 单调变化，ρ 低时均匀覆盖与 GiGPO 持平。C3：在初始策略的 rollout 上测得的 ρ 可在训练前预测"步级信用是否值得用"，并在留出环境（Sokoban）上检验。
- Story line：终端验证器只暴露极少轮次（τ²-bench k=1 占 98%），均匀覆盖胜过定位，定位与随机打乱同样有害，V_d 实测 0.15–0.4、相变点约 0.8 [2609.02417]；但 ALFWorld / WebShop 上 GiGPO 通过重复锚点构造步级优势而显著优于 GRPO [2505.10978]，ProVer 的随机片段对照只比评审选段低 1–5 点 [2609.36178]，低计数锚点会产生过大优势与振荡 [2606.05885] → 被忽视的关键：定位信息不只来自验证器，还来自 rollout 间的状态复现；V_d 理论没有这一项，两类研究因此对不齐 → 本 Idea：等量对照分解增益 + 只改信用分组的 ρ 操纵 → 可推翻：若定位占比不随 q 或 N 变化，或打乱对照在高 ρ 下与 GiGPO 持平，则"复现提供定位信息"被推翻。
- 打分理由：把卡片的诊断缺口与一个可操纵的机制连起来，操纵不改变模型输入，干净；代码现成；风险是训练轮数多、算力偏重，以及 GiGPO 原文 §5.5 已报告步级组大小随训练的动态。
- Idea 生成依据：来自问题卡 A-Q002 的 2609.02417、2609.36178、2606.05885；2505.10978 GiGPO（§5.1 设置、§5.5 步级组动态）；verl-agent 代码（`gigpo/core_gigpo.py`）；2604.11037 RTMC（跨 rollout 状态匹配构造 Q 值）；2607.21273（稠密信号经 std 归一化的崩溃，提示均匀对照需控制归一化）。
- 自评分轻量新意依据：检索"GiGPO anchor state step-level group size ablation shuffled step advantages""state revisitation across rollouts determines step-level credit quality"未见因果操纵复现率或与 V_d 统一的工作；需要 reviewer 检索。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：指出并因果检验"rollout 间状态复现"是轮次定位信息的第二来源，用它解释覆盖 / 定位两种结论在不同基准上的分歧。
- Baseline 可复现性：

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 开源代码与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| GiGPO | 同任务：ALFWorld / WebShop 步级信用 | https://arxiv.org/abs/2505.10978 | https://github.com/langfengQ/verl-agent ；2026-11-01 克隆核验：`gigpo/core_gigpo.py`（`build_step_group`、`summarize_group_size`、`step_advantage_w`、`enable_similarity`）；`examples/gigpo_trainer/run_alfworld.sh`、`run_webshop.sh` | 官方脚本：Qwen2.5-1.5B-Instruct、2 卡、150 epoch、N=8 | 是 |
| GRPO | 同任务基线 | 同仓库 | `examples/grpo_trainer/` | 官方脚本 | 是 |
| 均匀覆盖 / 轨迹内打乱对照 | 2609.02417 定义的对照 | https://arxiv.org/abs/2609.02417 | 无代码；在 `compute_gigpo_outcome_advantage` 中把步级优势替换为轨迹内均值 / 轨迹内随机置换，完全指定 | 本地修改一处函数 | 是 |
| AgentOPSD | 同任务：轮次级信用（另一类定位来源：自蒸馏） | https://arxiv.org/abs/2608.05987 | https://github.com/ZethWang/AgentOPSD ；克隆核验：README 含 ALFWorld / WebShop 安装与运行，Qwen2.5-3B/7B | 按 README | 否（算力受限，作扩展） |

- Reviewer 记录：`Call 1（常规，同模型 opus）：6.0/10，promising_needs_revision；最高近邻 2609.02417（相关工作明确引用 GiGPO 并预测其收益追踪覆盖、提出打乱对照）、GiGPO、Credit Without Ground Truth (2608.19760，ALFWorld 打乱对照、须匹配有效样本量，排除 GiGPO 类)、ECPO、Tree-GRPO (2509.21240)。阻塞：①'V_d 理论未计入复现 / 未讨论 GiGPO'不实（improver 已核对原文确认）；②C2 绝对差随 q 机械下降（mean_norm 下单例步级优势为 0），不能区分覆盖与定位，N 操纵缺 GRPO(N)；③2–3 种子对差值之比做 CI 不重叠功效不足；C3 Sokoban 官方为 VL-3B 图像模式。另：ProVer 随机对照数字应为单次运行 4.3 / 5.5 点。子 Idea：IDEA-003`

### IDEA-003：检验"覆盖而非定位"对重复状态类方法的预测——等量对照与等剂量复现操纵

- 来源：`最高近邻不足`（2609.02417 对 GiGPO 类方法给出预测但未检验）
- 父 Idea：`IDEA-002`
- 状态：`needs_revision`
- 定位关键词：credit assignment；GiGPO；anchor states；GRPO；ALFWorld；WebShop
- 一句话背景：2609.02417 预测基于重复状态的步级信用方法（GiGPO）的收益追踪其恢复的覆盖，并提出等集中度打乱对照来区分覆盖与定位；这一预测在 GiGPO 实际报告增益的 ALFWorld / WebShop 上从未被检验。
- 自评分：`7.6/10`
- 一段话概括：C1（检验预测）：在 ALFWorld（5 种子）与 WebShop（3 种子）上，GiGPO 与其轨迹内打乱对照（步级优势在轨迹内随机置换，集中度与总量不变）的配对差值；覆盖理论预测为零。C2（等剂量复现操纵）：在信用计算时以概率 q 拆散锚点，但把被拆成单例的步用"该轨迹非单例步级优势的均值"填充，使非零信用的步数与总量不随 q 变；在每个 q 下比较 GiGPO-填充与其打乱版本——若复现提供定位信息，差值随 q 下降；若只提供覆盖，差值在各 q 下都为零。C3（次要、相关性）：ALFWorld 6 类子任务的自然复现率不同，检验各子任务的定位差值与其复现率的关系。
- Story line：同 IDEA-002，动机改为："覆盖而非定位"理论在 τ²-bench / BFCL 上成立，并预测 GiGPO 类方法的收益来自覆盖 [2609.02417]；Credit Without Ground Truth 在 ALFWorld 上审计步级信用但排除了 GiGPO 类基于回报的方法，并指出比较必须匹配有效样本量 [2608.19760] → 被忽视的关键：GiGPO 在 ALFWorld / WebShop 上的增益是否真是覆盖、复现在其中提供的是覆盖还是定位，没有被等量、等剂量地检验 → 本 Idea：配对打乱对照 + 等剂量复现操纵 → 结果两向都有结论：若打乱与 GiGPO 持平，覆盖理论扩展到方法论文主基准；若显著更差且随 q 下降，则复现提供了 V_d 之外的定位信息。
- 打分理由：动机准确、两向结果都有价值、检验能区分两种解释；风险是算力偏重（约 40 次训练），以及新意被视为"执行近邻的预测"。
- Idea 生成依据：同 IDEA-002；2609.02417 相关工作段原文（improver 已核对）；2608.19760 摘要；2509.21240 Tree-GRPO 摘要；verl-agent `step_norm_reward`（单例组步级优势为 0）。
- 自评分轻量新意依据：Call 1 reviewer 未检索到在 ALFWorld / WebShop 上分解 GiGPO 增益或操纵锚点复现的工作。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：在方法论文主基准上检验覆盖理论对重复状态方法的预测，并用等剂量操纵把复现的作用分解为覆盖与定位。
- Baseline 可复现性：同 IDEA-002（verl-agent GiGPO / GRPO 已克隆核验；打乱、均匀、填充对照均为 `compute_gigpo_outcome_advantage` / `build_step_group` 中的完全指定修改）。
- Reviewer 记录：`Call 2（常规，同模型 opus）：6.0/10，promising_needs_revision；新增近邻 GACA (2609.12424，ALFWorld 1.5B 上置换 GiGPO 派生门控分数降 8.34 点)、Dark Room (2607.21273，含 GiGPO 臂的打乱 / 安慰剂对照)。阻塞：①GiGPO 步级优势是锚点处 Q(s,a)−V(s) 的蒙特卡洛估计，打乱几乎必然更差，且正差值可被'锚点抬高 V_d'吸收，不能证伪覆盖理论；缺少在 ALFWorld 上测出锚点 V_d 并推出零差值预测的环节；②C2 负斜率在 C1>0 时由填充构造保证，L2 剂量未匹配。修正：ALFWorld 官方为 mean_std_norm（已核对脚本）；'2608.19760 明确排除 GiGPO'无法核验，删去。子 Idea：IDEA-004`

### IDEA-004：锚点 V_d 与覆盖理论的相变点——在 ALFWorld / WebShop 上检验"定位何时胜过均匀覆盖"的定量预测

- 来源：`最高近邻不足`（2609.02417 的相变点 V_d*≈0.8 只在合成环境给出）
- 父 Idea：`IDEA-003`
- 状态：`rejected`
- 定位关键词：credit assignment；GiGPO；anchor states；verifier information density；ALFWorld；WebShop
- 一句话背景：覆盖理论用 V_d 预测轮次定位何时胜过均匀覆盖，合成环境中相变点约 0.8；GiGPO 的锚点分组相当于在训练时抬高可观测的步级信息，但其 V_d 从未被测，相变预测也从未在真实 agent 基准上检验。
- 自评分：`7.5/10`
- 一段话概括：定义锚点 V_d（GiGPO 中落在大小 ≥2 且组内回报方差 >0 的锚点组里的步数占轨迹长度的比例，按 2609.02417 的 k/C 口径），用组大小 N∈{4,8,16} 与环境（ALFWorld 子任务、WebShop）改变它；每个设置下比较 GiGPO 与"同一锚点、同一总量、均匀摊到全部步"的均匀对照。C1：GiGPO − 均匀的差值随锚点 V_d 单调变化，并在 V_d* 附近换号；C2：换号点落在 2609.02417 合成相变点 0.8 的置信区间内（定量检验）；C3：打乱对照作为下界，确认定位方向（差值的符号由定位而非噪声决定）。
- Story line：覆盖理论在低 V_d 的终端验证器任务上成立，并给出合成相变点约 0.8，且预测 GiGPO 类方法的收益追踪覆盖 [2609.02417]；GiGPO 的锚点分组是锚点处 Q−V 的蒙特卡洛估计，单例组 <35% [2505.10978]，GACA 在同基准上置换派生门控降 8.34 点 [2609.12424] → 被忽视的关键：锚点分组把 V_d 从终端验证器的低值抬到一个可测的水平，覆盖理论在这个区间给出了可检验的定量预测（换号点），但没人测过锚点 V_d，也没人检验相变点 → 本 Idea：测锚点 V_d、用 N 与环境改变它、比较 GiGPO 与均匀覆盖 → 可推翻：若差值不随 V_d 变化，或换号点远离 0.8，覆盖理论的定量部分被推翻；若在 0.8 附近换号，理论在真实基准上得到验证并可用于方法选择。
- 打分理由：把"结果两向都有结论"落到一个定量预测上；用 N 改变 V_d，GiGPO 与均匀臂在每个 N 下共享同一锚点与 rollout，不存在稀释造成的机械趋同；风险是锚点 V_d 与 k/C 口径的对应需要论证、N=16 算力翻倍。
- Idea 生成依据：2609.02417（摘要、表 2、§7 原句）；2505.10978（§5.1、§5.5、E.1 计算设置）；2609.12424 GACA（置换门控 −8.34）；2608.19760（剂量须匹配）；2607.21273；verl-agent 脚本（ALFWorld mean_std_norm、WebShop mean_norm）。
- 自评分轻量新意依据：Call 1、Call 2 reviewer 均未检索到测量锚点 V_d 或在真实 agent 基准上检验相变点的工作。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：定义并测量锚点 V_d，在真实 agent 基准上定量检验覆盖理论的相变预测。
- Baseline 可复现性：同 IDEA-002（verl-agent GiGPO / GRPO 已克隆核验；均匀、打乱对照为一处完全指定的修改；各环境沿用官方归一化：ALFWorld mean_std_norm、WebShop mean_norm）。
- Reviewer 记录：`Call 3（常规，同模型 opus）：4.5/10，needs_rethink。阻塞：①锚点 V_d（组大小≥2 且方差>0 的步 / 轨迹长度）与 k/C（验证器暴露对错的步 / 因果链长度）构念不对应；GiGPO 不是固定预算集中信用，均匀臂取均值抹掉步级信息，GiGPO−均匀≈有无步级信号；②'0.8 在 CI 内'判据近乎不可证伪（18/19 点为同一运行内非独立子任务点）；③C1/C3 是 2609.02417 §7 明文预测，C3 被 GACA 部分覆盖（GACA 置换的是 NLL 关键度分数，improver 原写'GiGPO 派生门控分数'不准）。`
