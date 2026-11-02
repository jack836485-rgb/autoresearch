# Idea 候选池（A-Q002）

- 输入模式：`problem_card`
- 输入论文：不适用
- 输入问题卡：`path-stage/LLM热门方向_算力适配_20261028` 的 `A-Q002`

## 当前选择

- Reviewer 调用：`0 / 17`
- 当前选中 Idea：`IDEA-002`
- 当前自评分：`7.6/10`
- 选择理由：IDEA-002 在卡片切口（补等量对照）之上，指出 2609.02417 的 V_d 理论只覆盖"验证器暴露"这一定位信息来源，而 ALFWorld / WebShop 上主流方法（GiGPO 类）的定位信息来自 rollout 间的状态复现；并用"只改信用分组、不改模型输入"的方式因果操纵这一来源。IDEA-001 只是审计。
- 状态：`等待第 1 次 reviewer 调用`

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
- 状态：`selected`
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
