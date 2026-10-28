# Idea 候选池

> 本文件由 idea improver 持续维护。保留所有进入过比较的实质性候选及其演化关系；不在这里展开完整 proposal。

## 当前选择

- Reviewer 调用：`11 / unlimited（用户于 2026-09-08 明确取消预算上限）`
- 当前选中 Idea：`IDEA-016`
- 当前自评分：`9.6/10`
- 选择理由：第 11 轮确认 \(J_{\rm cap}\) 直接等于原题/固定变体的联合成功概率，双侧 4p+4q 与完整 8x8 loss 在旧参数处无偏，joint weight 不超过 4；baseline、预算、任务、统计和 OMEGA 协议均达到实验规划门槛。
- 状态：`final；gate passed（7.9/10，experiment_ready，fatal blockers 为空）`

## 候选列表

### IDEA-001：宽泛的新能力测量与 exploration RL

- 来源：`原始想法`
- 父 Idea：`无`
- 状态：`needs_revision`
- 定位关键词：reinforcement learning with verifiable rewards；reasoning capability boundary；pass@k；exploration
- 一句话背景：这是 RLVR 数学推理中判断训练究竟改变成功轨迹概率还是扩展可解问题范围的问题。
- 自评分：`5.4/10`
- 一段话概括：比较 base 与 RL 模型的大样本 `pass@k` 和轨迹多样性，并给 RL 增加 exploration 信号，希望同时提高小 `k` 效率和大 `k` 覆盖；最小实验是在 Qwen2.5-Math-7B 上比较 base、GRPO 与 exploration GRPO。
- 打分理由：问题重要且忠实于用户方向，但 Claim、能力定义和 exploration 信号都未落到一个可排除现有工作的具体机制，当前版本无法被单个最小实验充分证伪。
- Improver 搜索依据：https://arxiv.org/abs/2504.13837；https://arxiv.org/abs/2506.14245；https://arxiv.org/abs/2510.11686；https://arxiv.org/abs/2609.01274
- Baseline 可复现性：

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 开源代码与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| Vanilla GRPO | 同属数学 RLVR 与 `pass@k` 评测 | https://arxiv.org/abs/2402.03300 | https://github.com/verl-project/verl；已核验 `examples/grpo_trainer/run_qwen3_8b_fsdp.sh` 和 GRPO 配置文档 | 固定 Qwen、训练数据、rollout token 与更新步数后运行 GRPO | 是 |
| RepExp | 同属数学 RLVR 的 representation-based exploration | https://arxiv.org/abs/2510.11686 | https://github.com/verl-project/verl-recipe/tree/main/rep_exp；已核验 `rep_exp/train_elliptical.sh`、`main_rep_exp.py` 与 elliptical reward manager | 按 recipe 替换为同一模型和数据，保持总 rollout token | 是 |
| DIVER | 同属数学 RLVR 的 sequence-level diversity exploration | https://arxiv.org/abs/2509.26209 | https://github.com/NJU-RL/DIVER；已核验 `scripts/train/baseline.sh`、`verl/div_src/reward_fn.py` | 使用仓库训练脚本并统一模型、数据与预算 | 是 |

- Reviewer 记录：`尚未送审`

### IDEA-002：按 base 低似然奖励正确轨迹

- 来源：`最高近邻不足`
- 父 Idea：`IDEA-001`
- 状态：`covered`
- 定位关键词：RLVR；reference policy；trajectory likelihood；distribution sharpening
- 一句话背景：这是数学 RLVR 中缓解 GRPO 偏向强化高概率正确轨迹、忽略低概率正确轨迹的问题。
- 自评分：`4.3/10`
- 一段话概括：冻结 base model，对每条 verifier 判定正确的 rollout 按其在 base 下的负对数似然加权，使稀有正确轨迹获得更大 advantage；最小实验比较 vanilla GRPO、低似然加权 GRPO 与 base 的 `pass@k`。
- 打分理由：机制可行但已经被正式定理证明中的 unlikeliness reward、跨域 puzzle-to-math 的 base-perplexity novelty，以及多种 diversity reward 高度覆盖。
- Improver 搜索依据：https://aclanthology.org/2025.emnlp-main.1298/；https://arxiv.org/abs/2605.29190；https://arxiv.org/abs/2509.26209
- Baseline 可复现性：

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 开源代码与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| GRPO-Unlikeliness | 直接实现按低概率正确证明加权 | https://aclanthology.org/2025.emnlp-main.1298/ | https://github.com/AndreHe02/rewarding-unlikely-release；已核验为 veRL + Lean 在线 verifier 的官方训练实现 | 使用仓库 README 的 GRPO 训练入口；自然语言数学迁移不作为直接 baseline | 否，任务域不匹配 |
| Vanilla GRPO | 同属数学 RLVR | https://arxiv.org/abs/2402.03300 | https://github.com/verl-project/verl；已核验 GRPO 示例 | 与候选 reward 开关共享训练脚本 | 是 |

- Reviewer 记录：`未送审；搜索后判定核心机制已覆盖`

### IDEA-003：用 unseen-species 估计推理策略缺失质量

- 来源：`相似领域成熟方法迁移`
- 父 Idea：`IDEA-001`
- 状态：`available`
- 定位关键词：sample coverage；missing mass；reasoning diversity；capability boundary
- 一句话背景：这是在有限采样下估计语言模型尚未观察到的正确推理策略质量、避免把任意 `k` 当成能力边界的问题。
- 自评分：`7.6/10`
- 一段话概括：先把正确 CoT 聚成策略等价类，再用 Good--Turing/coverage estimation 从 singleton 与重复类估计未见策略质量，以 base 与 RL 的估计差异替代单一大 `k`；最小实验对固定 rollout 逐步截断，检验估计量能否预测后续样本中新出现的策略类，并比较 GRPO、RepExp 与 DIVER。
- 打分理由：统计迁移本身较新且实验便宜，但策略聚类误差可能主导结果，而且它只测量未见质量，尚未直接给出促成可复用新能力的训练机制。
- Improver 搜索依据：https://www.jstor.org/stable/2333344；https://proceedings.neurips.cc/paper/2013/hash/53c04118df112c13a8c34b38343b9c10-Abstract.html；https://arxiv.org/abs/2510.08325
- Baseline 可复现性：

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 开源代码与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| Empirical observed strategy count | 同一正确轨迹策略覆盖任务的直接插件估计 | 完整定义为去重后的已观测策略数 | 无仓库但可由聚类标签计数直接本地实现 | 对每个采样截断点直接计数 | 是 |
| Chao/Good--Turing missing mass | 同一 unseen-strategy estimation 任务的成熟统计基线 | https://www.jstor.org/stable/2333344 | 无专用仓库但公式由 singleton 频数直接实现，不依赖隐藏数据 | 在冻结策略标签上计算 missing mass 与 bootstrap 区间 | 是 |
| Vanilla GRPO / RepExp / DIVER | 提供不同推理分布以测试估计量 | 对应论文见 IDEA-001 | 三个公开实现均已核验，入口见 IDEA-001 | 读取公开 checkpoint 或按同预算生成 rollout | 是 |

- Reviewer 记录：`尚未送审`

### IDEA-004：同构问题族上的能力证书与稳健 RLVR

- 来源：`最高近邻不足`
- 父 Idea：`IDEA-001`
- 状态：`needs_rethink`
- 定位关键词：reinforcement learning with verifiable rewards；compositional generalization；counterfactual evaluation；distributionally robust optimization
- 一句话背景：这是在程序可验证的数学与符号推理中，用结构保持的问题变换判断 RLVR 是否获得可复用能力的问题。
- 自评分：`8.5/10`
- 一段话概括：把同一底层问题经实体重命名、输入置换和结构保持改写得到的实例组成一个变换族；只有 RL 模型在未见底层实例的多种变体上可靠成功、并超过给 base 更大采样预算得到的 decoding envelope，才记为经验性的能力获得。训练时在固定总 rollout token 下把一个 minibatch 分配给同族多个变体，并用变体成功率的 lower-tail/CVaR 形成 family reward，迫使策略提高跨变体最差表现，而不是奖励文本或 hidden-state 距离。最小实验在 Reasoning Gym 的 Countdown、graph、logic 等有精确变换和 verifier 的任务上比较 base、vanilla GRPO、RepExp、DIVER 和本方法。
- 打分理由：它直接修补 `pass@k`、Cover@τ 和多样性 bonus 都没有要求“新行为可跨等价变体复用”的缺口，训练信号不依赖 teacher，且可在公开程序化环境中以同预算、三 seed 证伪。
- Improver 搜索依据：https://arxiv.org/abs/2504.13837；https://arxiv.org/abs/2510.08325；https://arxiv.org/abs/2609.01274；https://arxiv.org/abs/2506.18880；https://arxiv.org/abs/2604.22074；https://github.com/open-thought/reasoning-gym；https://arxiv.org/abs/2508.14029
- Baseline 可复现性：

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 开源代码与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| Base decoding envelope | 直接检验同一 model 在预算化搜索下的可达成功 | https://arxiv.org/abs/2609.01274 | 以冻结 checkpoint 和明确温度/采样网格直接实现；不依赖额外权重 | 每个 held-out family 给 base 8 倍于 RL 单点评测的总 token，并报告最优非 oracle decoder | 是 |
| Vanilla GRPO | 同一模型、同一程序化任务、同一 verifier 的标准 RLVR | https://arxiv.org/abs/2402.03300 | https://github.com/open-thought/reasoning-gym；已核验 `training/train_grpo.py`、`training/rewards/reward.py` 与训练配置 | 使用 Reasoning Gym 原生动态数据和 verifier，关闭 family reward | 是 |
| RepExp | 同一 RLVR exploration 问题的 hidden-state exploration 最高近邻 | https://arxiv.org/abs/2510.11686 | https://github.com/verl-project/verl-recipe/tree/main/rep_exp；已核验 `train_elliptical.sh`、`main_rep_exp.py`、`elliptical_reward_manager.py` | 将相同 Reasoning Gym prompts 接入 recipe，保持模型、rollout token 和步数一致 | 是 |
| DIVER | 同一 RLVR exploration 问题的 sequence-level diversity 近邻 | https://arxiv.org/abs/2509.26209 | https://github.com/NJU-RL/DIVER；已核验 `scripts/train/baseline.sh` 与 `verl/div_src/reward_fn.py` | 将相同 prompts/verifier 接入官方 reward 实现并统一预算 | 是 |
| OMEGA GRPO | 同一数学 OOD/compositional generalization 设置的外部验证 | https://arxiv.org/abs/2506.18880 | https://github.com/sunblaze-ucb/omega；已核验公开 generators、train/ID/OOD splits | 仅在最小实验通过后使用其现成 split 做外部迁移，不混入主训练 | 否，属于后续实验 |

- Reviewer 记录：`第 1 次独立审阅 2.8/10，needs_rethink。公共 family-CVaR 信号被 GRPO 组内中心化消除；与 PIRL/group-DRO 高度重叠；DIVER 入口错误且 RepExp 未给出同任务适配路线。`

### IDEA-005：verifier-grounded Quality-Diversity 轨迹档案

- 来源：`相似领域成熟方法迁移`
- 父 Idea：`IDEA-001`
- 状态：`available`
- 定位关键词：quality-diversity；MAP-Elites；verifiable rewards；reasoning diversity
- 一句话背景：这是在数学 RLVR 中同时保留多个可验证解题行为、避免单一高回报模式占据策略分布的问题。
- 自评分：`7.8/10`
- 一段话概括：用 verifier 可读的任务元数据和可执行解答结构定义 behavior descriptor，将正确 rollout 放入 MAP-Elites 风格档案，并优先训练仍为空或低质量的行为格；最小实验比较档案覆盖、`pass@k` 与 held-out 任务成功率是否优于 GRPO、RepExp 和 DIVER。
- 打分理由：Quality-Diversity 是成熟且契合的迁移路线，但自然语言数学中 behavior descriptor 难以稳定获得，而且容易被评价为 DIVER/count-based exploration 的结构化版本。
- Improver 搜索依据：https://arxiv.org/abs/1504.04909；https://arxiv.org/abs/1708.09251；https://arxiv.org/abs/2509.26209；https://arxiv.org/abs/2510.16614
- Baseline 可复现性：

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 开源代码与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| Vanilla GRPO | 同一 RLVR 任务的标准优化 | https://arxiv.org/abs/2402.03300 | https://github.com/open-thought/reasoning-gym；已核验 `training/train_grpo.py` | 关闭 archive sampling/reward | 是 |
| RepExp | 同一任务上的 representation diversity exploration | https://arxiv.org/abs/2510.11686 | https://github.com/verl-project/verl-recipe/tree/main/rep_exp；入口已核验 | 统一数据和 rollout 预算 | 是 |
| DIVER | 同一任务上的 global sequence diversity | https://arxiv.org/abs/2509.26209 | https://github.com/NJU-RL/DIVER；入口已核验 | 统一数据和 rollout 预算 | 是 |
| MAP-Elites | 方法灵感来自跨域 Quality-Diversity，不作为 LLM 实验 baseline | https://arxiv.org/abs/1504.04909 | 成熟算法可直接实现，但不属于同一语言模型任务 | 仅用于 archive 机制设计 | 否，跨域 inspiration |

- Reviewer 记录：`尚未送审`

### IDEA-006：反事实轨迹似然比驱动的规则条件化 RLVR

- 来源：`第 1 次 reviewer 致命阻塞后的方向重构`
- 父 Idea：`IDEA-004`
- 状态：`needs_revision`
- 定位关键词：reinforcement learning with verifiable rewards；counterfactual generalization；rule following；algorithmic generalization
- 一句话背景：这是在程序化符号推理中，区分模型只是提高固定任务解法概率，还是学会按题面给出的新规则改变推理轨迹的问题。
- 自评分：`8.6/10`
- 一段话概括：用 Algebrarium 的随机 Latin square/有限代数生成一对共享表达式树、但运算规则不同且答案必然不同的任务；对真实规则下 verifier-valid 的轨迹，提高其在真实 prompt 下的似然，同时降低同一轨迹在反事实规则 prompt 下的似然，再与普通 outcome GRPO 联合。能力获得只作有限预算经验判定：在未见规则表和更深组合上，RL 模型的联合规则响应率置信下界超过阈值，而 base 在预注册的 8 倍采样预算下置信上界低于阈值。最小实验用相同成对 prompts 的 outcome-only GRPO 分离“数据暴露”与似然比目标，并加入同数据、同优化 token 的生成器轨迹 SFT。
- 打分理由：与 PIRL/同构扰动要求不变输出相反，本候选改变任务语义并要求输出随规则变化；与 ACRE 的答案选项重排一致性相比，它使用 verifier-valid 完整轨迹作为跨规则硬负例，且有直接的 exposure-only ablation。公开生成器、verifier 与 GRPO 入口均可核验，有限采样结论也明确写成置信区间而非理论 support。
- Improver 搜索依据：https://arxiv.org/abs/2307.02477；https://arxiv.org/abs/2502.11525；https://arxiv.org/abs/2510.10104；https://arxiv.org/abs/2602.08281；https://arxiv.org/abs/2608.08802；https://github.com/Linzwcs/Algebrarium；https://github.com/open-thought/reasoning-gym
- Baseline 可复现性：

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 开源代码与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| Base model 预注册采样包络 | 同一模型、同一未见代数规则任务上的有限预算能力上界 | https://arxiv.org/abs/2609.01274 | 无需外部权重；使用冻结 checkpoint 与固定采样网格直接实现 | 预先固定温度 `{0.6,0.8,1.0}`、每题总响应 token 为 RL pass@1 评测的 8 倍，不按 test 结果挑 decoder；用单侧 Clopper--Pearson 上界 | 是 |
| Singleton GRPO | 同一模型、同一规则任务的标准 RLVR | https://arxiv.org/abs/2402.03300 | https://github.com/open-thought/reasoning-gym；已核验 `training/train_grpo.py`、`training/rewards/reward.py` | 将 Algebrarium JSONL 适配为 Reasoning Gym dataset，普通单 prompt outcome reward | 是 |
| Paired-exposure GRPO | 与本方法看到完全相同的规则对，隔离数据暴露效应 | 本研究的必要机制消融，不冒充外部方法 | 复用同一个 `training/train_grpo.py`，仅让两个 prompt 各自按 outcome reward 独立分组 | 固定相同 prompt、rollout、响应 token、更新步数和 optimizer；关闭跨 prompt 似然比 | 是 |
| DIVER | 同一 7B RLVR 设置下的 sequence-level exploration baseline | https://arxiv.org/abs/2509.26209 | https://github.com/NJU-RL/DIVER；已核验真正入口 `scripts/train/train_diver.sh` 使用 `actor_rollout_ref.actor.div_coeff=0.1`，并核验 `verl/div_src/reward_fn.py::RewardManager` | 将同一 Algebrarium parquet 与 scorer 接到 `RewardManager`，保持 `main_rl`、8 rollouts、模型和核心预算一致；不再使用 `baseline.sh` | 是 |
| Generator-trace SFT | 检验显式可执行轨迹监督是否比 RL 更容易引入规则条件化模式 | https://github.com/Linzwcs/Algebrarium | 已核验 `python -m algebrarium.cli`、`src/algebrarium/generators.py` 与 CoT/确定答案输出；训练使用公开 Transformers/TRL SFT 入口 | 使用同一 generator prompts 和其确定性轨迹，匹配优化 token 数，不使用外部 teacher | 是 |
| Counterfactual evaluation / Meta-RFFT / ACRE / PIRL | 分别覆盖反事实规则评测、规则 SFT、选项置换一致性 RL、同义 prompt 不变性 | 对应链接见搜索依据 | 前两者有数据或生成代码；ACRE/PIRL 任务域和目标不同，且不是同一符号任务可直接运行 baseline | 作为最高近邻和边界说明，不纳入最小同域实验 | 否 |

- Reviewer 记录：`第 2 次独立审阅 7.2/10，promising_needs_revision。似然比梯度成立、DIVER 入口有效，但正向自模仿与反事实抑制混淆；逐步模型轨迹 verifier 未在公开 Algebrarium 中实现；仅一个非独立规则族。`

### IDEA-007：按下游组合敏感度分配原子技能 RL 预算

- 来源：`相似领域成熟方法迁移`
- 父 Idea：`IDEA-001`
- 状态：`available`
- 定位关键词：atomic skills；compositional generalization；curriculum reinforcement learning；multi-task optimization
- 一句话背景：这是在组合推理成功率由多个原子技能概率共同决定时，避免全局 outcome RL 牺牲瓶颈技能的问题。
- 自评分：`6.7/10`
- 一段话概括：在 Algebrarium 中分别估计每个原子操作的成功率及其在 held-out 组合图中的出现次数，优先把 rollout 预算分配给对组合任务对数成功率边际贡献最大的瓶颈操作，并约束其他操作不退化；训练只看单步操作，测试未见多步组合。
- 打分理由：机制可直接检验且不会受公共 reward 中心化影响，但“New Skills or Sharper Primitives?” 已建立原子概率到组合性能的框架，SCRL 与多任务/课程数据分配也覆盖大部分方法骨架，剩余的新意偏窄。
- Improver 搜索依据：https://arxiv.org/abs/2602.08281；https://arxiv.org/abs/2605.22074；https://arxiv.org/abs/2605.26934；https://arxiv.org/abs/2403.09479
- Baseline 可复现性：

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 开源代码与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| Uniform atomic GRPO | 与候选相同原子技能和组合测试的直接基线 | https://arxiv.org/abs/2602.08281 | https://github.com/Linzwcs/Algebrarium；公开 generator，但论文训练配置需进一步核验 | 固定每种原子操作 prompt 数，使用同一 GRPO 实现 | 是 |
| Difficulty curriculum | 同一程序化任务的数据分配基线 | https://github.com/open-thought/reasoning-gym | 已核验 `coaching/curriculum_config.py` 与 `training/train_grpo.py` 的 curriculum route | 只按题目深度升序调整采样，匹配总预算 | 是 |

- Reviewer 记录：`未送审；主执行器因与原子技能及 curriculum 近邻重叠较高而未选中`

### IDEA-008：首分歧状态排斥的反事实规则 RLVR

- 来源：`第 2 次 reviewer 的三个 fatal blocker 定向修订`
- 父 Idea：`IDEA-006`
- 状态：`needs_rethink`
- 定位关键词：reinforcement learning with verifiable rewards；counterfactual generalization；rule-conditioned reasoning；unlikelihood training
- 一句话背景：这是在可执行规则世界中，让 RLVR 不只奖励答对，还在规则被干预时准确撤销已经失效的第一步状态转移的问题。
- 自评分：`8.8/10`
- 一段话概括：模型输出固定格式的执行状态序列；确定性 interpreter 重放正确 rollout，并在反事实规则下找出第一个不再成立的状态转移，只对该错误 next-state token span 加 unlikelihood，普通 outcome GRPO 仍负责正向学习。规则条件化获得证书要求 RL 在三类独立规则族的 held-out rules/depth 上同时显著超过 base 的预注册采样包络。最小实验用 outcome-only、在线正向自模仿、结构化部分奖励和首分歧排斥的等数据等前向对照，区分负向反事实信号、额外监督梯度与状态级 reward shaping。
- 打分理由：该方法不再依赖不存在的 Algebrarium 模型轨迹 scorer，而给出由 canonical state 和 interpreter 组成的可执行 verifier；它只新增负向首分歧目标，直接解决上一轮因正向 MLE 混入而不可归因的问题；Latin/quasigroup、反事实进位制、PLSemanticsBench 非标准程序语义是三类不同规则族。与 NormWorlds-CF 的 change-field reward 和 ACRE 的一致性 reward 相比，新增量是用 counterfactual replay 自动定位“何处必须分叉”并作 token-level exclusion。
- Improver 搜索依据：https://arxiv.org/abs/2602.08281；https://arxiv.org/abs/2607.03957；https://arxiv.org/abs/2510.03415；https://arxiv.org/abs/2510.10104；https://arxiv.org/abs/1908.04319；https://github.com/Linzwcs/Algebrarium；https://github.com/ZhaofengWu/counterfactual-evaluation；https://github.com/EngineeringSoftware/PLSemanticsBench；https://github.com/NJU-RL/DIVER
- Baseline 可复现性：

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 开源代码与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| Base 预注册采样包络 | 同一 7B checkpoint 在同一规则对上的有限预算可达性 | https://arxiv.org/abs/2609.01274 | 冻结 checkpoint 即可直接实现，不需要新权重 | 温度 `{0.6,0.8,1.0}`、固定 8 倍响应 token；每个规则族分别报告单侧置信上界，不作理论 support 声明 | 是 |
| Paired outcome-only GRPO | 完全相同规则对数据上的标准 RLVR 与数据暴露控制 | https://arxiv.org/abs/2402.03300 | https://github.com/open-thought/reasoning-gym；已核验 `training/train_grpo.py` 和 reward route | 两世界各自 group-normalize outcome reward；执行和本方法相同的 counterfactual replay/teacher-forced pass 但 stop-gradient | 是 |
| Online positive self-imitation | 排除任何额外 token-level 监督都能解释增益 | 本研究机制消融 | 复用 paired GRPO；只对 on-policy verifier-correct 状态 span 加正向 NLL | 与本方法共享正确 rollouts、token mask、额外 forward 和系数绝对值 | 是 |
| State-reward GRPO | 覆盖 NormWorlds-CF 类结构化 reward shaping 的同域替代对照 | https://arxiv.org/abs/2607.03957 | 三套 interpreter 都输出 canonical states；不依赖原论文未公开训练代码 | 奖励为正确状态转移比例，仍在 prompt 内做 GRPO；同一 scorer 同一预算 | 是 |
| DIVER | sequence-level exploration baseline | https://arxiv.org/abs/2509.26209 | https://github.com/NJU-RL/DIVER；已核验 `scripts/train/train_diver.sh`、`div_coeff=0.1`、`RewardManager` | 展平相同规则对 parquet，接三套 interpreter scorer，保持 8 rollouts 和核心预算 | 是 |
| Generator-trace SFT | 用户关注的 distillation/显式轨迹监督对照 | Algebrarium 与 PLSemanticsBench 论文 | 三套公开数据均有 deterministic trace；使用公开 TRL SFT | 匹配训练 prompt 和优化 token，不使用 LLM teacher | 是 |

- Reviewer 记录：`第 3 次独立审阅 5.2/10，needs_rethink。首分歧整段 token mask 会惩罚共享 token 且后续 token 条件于错误前缀，不能实现声称的状态干预；三个公开任务入口及规模与 brief 不符；DIVER 同域入口和 loss 系数也未冻结。`

### IDEA-009：可验证双向桥接 RL

- 来源：`第 3 次 reviewer 否决后的机制换代`
- 父 Idea：`IDEA-001`
- 状态：`needs_rethink`
- 定位关键词：reinforcement learning with verifiable rewards；bidirectional search；trajectory composition；sparse-reward exploration
- 一句话背景：这是在可逆、程序可验证的长程推理任务中，当 base 和普通 RLVR 都只能产生合法局部路径而不能采到完整成功轨迹时，如何把这些局部能力组合成可复用完整能力的问题。
- 自评分：`8.9/10`
- 一段话概括：对同一任务从起点到终点、从终点到起点各采样 8 条有共同长度上限的 on-policy 轨迹；若一条正向轨迹和一条反向轨迹都全程合法、endpoint 完全相同，且正向动作接反向动作的逆序逆操作后总长度不超过共同上限，则 deterministic verifier 得到一条此前未被端到端采样的完整解，并把这两个实际采样的 rollout 记为正例。训练用普通 GRPO 更新这两个 rollout，不对拼接轨迹做 SFT；评测时关闭桥接搜索，只让单个策略从原始起点独立完成 held-out 任务。最小实验在 Reasoning Gym 的 Tower of Hanoi、Shortest Path 和 Word Ladder 上比较 base 8 倍采样包络、相同正反 prompt 的 outcome-only GRPO、DIVER、R3L 和本方法。
- 打分理由：它直接利用 verifier 的状态转移结构突破 all-zero outcome group，而不是把文本/hidden state/gradient 距离当能力；与 SCRL 的参考链子问题、R3L 的语言反思重试、DIVER 的单向序列多样性均有明确机制差异。三个公共任务的起点、终点、动作逆映射和逐步 verifier 已逐文件核验，关键对照看到完全相同的正反 prompts 且无需连续超参。
- Improver 搜索依据：https://arxiv.org/abs/2504.13837；https://arxiv.org/abs/2601.03715；https://arxiv.org/abs/2605.22074；https://arxiv.org/abs/2509.26209；https://arxiv.org/abs/2510.11686；https://arxiv.org/abs/2208.02434；https://arxiv.org/abs/2602.22871；https://github.com/open-thought/reasoning-gym/tree/49b07130b3fcd12f2d064bba7c43869543a0e7e7；https://github.com/NJU-RL/DIVER/tree/5870b47c695abdfc3a29b7a50c4b329ba7e4be06；https://github.com/shiweijiezero/R3L
- Baseline 可复现性：

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 开源代码与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| Base 预注册采样包络 | 区分单纯增加采样预算与训练后单次求解能力 | https://arxiv.org/abs/2609.01274 | 冻结同一个 Qwen2.5-Math-7B checkpoint 即可；不需要外部权重 | 温度 `{0.6,0.8,1.0}`，每题累计响应 token 为 RL pass@1 的 8 倍；评测禁用桥接和 verifier 搜索 | 是 |
| 双向 exposure-only GRPO | 与本方法输入、方向、rollout 数和 token 完全相同的 vanilla RLVR 控制 | https://arxiv.org/abs/2402.03300 | Reasoning Gym commit `49b0713` 的三个任务 scorer 已核验；训练复用其 `training/train_grpo.py` | 每个底层题生成正向和反向 prompt，各 8 rollouts；只在单条 rollout 独立到达其目标时给 1，否则 0 | 是 |
| DIVER | 同一 sparse-reward exploration 问题的 sequence-level diversity baseline | https://arxiv.org/abs/2509.26209 | 仓库默认分支是 `diver`；固定 commit `5870b47`，已核验 `scripts/train/train_diver.sh` 的 `div_coeff=0.1` 与 `verl/div_src/reward_fn.py::RewardManager` | 保持官方 diversity loss；在 `_select_rm_score_fn` 只增加三个共享 deterministic scorer 分派，正反 prompts 与总 token 同本方法 | 是 |
| R3L | 最接近的失败轨迹反思、重试与 pivotal credit baseline | https://arxiv.org/abs/2601.03715 | https://github.com/shiweijiezero/R3L；已核验 7B 配置、`examples/R3L/dapo/` 入口与四类环境 workflow | 在其公开 workflow 接口加入同一三个环境；语言反馈只报告首个非法动作或“合法但未到目标”，并匹配生成 token 总量 | 是 |
| Oracle-trace SFT | 检验显式完整路径监督是否仍比 RL 更容易引入组合模式 | Reasoning Gym 三个 generator 的公开 `answer`/`solution` 字段 | commit `49b0713` 的 generator 均给确定解或 BFS 解；不调用外部 teacher | 只用训练 split 的公开解，匹配优化 token；作为监督上界，不与 RL 机制混称 | 是 |
- Reviewer 记录：`第 4 次独立审阅 5.9/10；原始 verdict 使用了词表外的 not_experiment_ready，按 gate 记为 needs_rethink。三个任务可逆性通过，DIVER 固定入口通过；fatal blockers 是双向分别归一化时的方差条件写错、半轨迹奖励强化提前 EOS 却不训练正向完整后缀、R3L 预算/任务入口不可复现，以及动作 horizon/token/scorer 事件未统一。最高近邻是 BES、SCRL、R3L、RevThink。`

### IDEA-010：有界重要性加权的双向轨迹提案 RL

- 来源：`第 4 次 reviewer 的信用路径否决 + BES/EM Policy Gradient 最近邻缺口`
- 父 Idea：`IDEA-009`
- 状态：`promising_needs_revision`
- 定位关键词：reinforcement learning with verifiable rewards；bidirectional proposal；off-policy policy gradient；sparse-reward planning
- 一句话背景：这是在可逆、程序可验证的长程规划中，用正反两个容易采到的局部动作串提出完整候选，同时仍然无偏优化原始正向策略的问题。
- 自评分：`8.7/10`
- 一段话概括：对每个已知最短动作数 `L` 的任务，固定切点 `h=floor(L/2)`；旧策略一半直接从原始 prompt 采完整动作串，另一半分别从起点采 `h` 步、从终点采 `L-h` 步，再把后者逆序取逆后与前者组成完整串。所有组合无论是否相遇都保留并由同一个二元 verifier 打分，因此双向 proposal `q_old(y)` 是两个半串概率的可计算乘积。行为分布固定为 `m_old=(p_old+q_old)/2`，用 stop-gradient 权重 `w=p_old/m_old<=2` 对完整串在原始 prompt 下作单步 policy-gradient 更新；这条梯度在旧参数处无偏指向原始正向期望 reward，并直接覆盖完整后缀与终止位置。最小实验以同预算 full-forward policy gradient、GRPO、DIVER、未校正 bridge replay 和 BES 为对照，检验 proposal 是否把 verifier success 的梯度方差降到普通采样可学习的范围，并在关闭 proposal 后得到 held-out 独立求解能力。
- 打分理由：相对 IDEA-009，这是目标函数和采样分布的实质换代，而非措辞修补；半轨迹不再是训练单位，且 mixture importance ratio 给出严格上界。相对 BES，窄新增量是对可逆轨迹 proposal 给出精确密度、拒绝筛选为零、对原始策略作有界校正，而不是 MaxRL/搜索轨迹直接回放；相对通用 off-policy reasoning RL，新增量是 verifier 状态图诱导的双向 proposal 及其同域方差检验。风险在于 proposal 可能并不比正向策略更接近成功条件，或即使成功更多也因小权重不能降低方差；这两点都由预注册诊断直接否证。
- Improver 搜索依据：https://arxiv.org/abs/2504.13837；https://arxiv.org/abs/2510.08325；https://arxiv.org/abs/2510.11686；https://arxiv.org/abs/2504.18587；https://arxiv.org/abs/2605.28814；https://arxiv.org/abs/2601.03715；https://github.com/open-thought/reasoning-gym/tree/49b07130b3fcd12f2d064bba7c43869543a0e7e7；https://github.com/NJU-RL/DIVER/tree/5870b47c695abdfc3a29b7a50c4b329ba7e4be06；https://github.com/Embodied-Minds-Lab/BES/tree/7c2696f3b5c340dfe34062df93af009cee9152bc
- Baseline 可复现性：

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 开源代码与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| Full-forward policy gradient | 与本方法同一完整轨迹 loss，唯一差异是 `m=p`、`w=1` | REINFORCE 的标准序列级 score-function estimator | 复用本研究同一训练入口和 verifier，不依赖外部实现 | 每题 8 条正向完整样本；同一 prior-batch difficulty baseline、单次更新、响应 token 与 optimizer token 预算 | 是，首要机制对照 |
| Vanilla GRPO | 用户问题中的标准 outcome RLVR | https://arxiv.org/abs/2402.03300 | Reasoning Gym commit `49b0713` 已核验 `training/train_grpo.py` 与 reward route | 同一 checkpoint、训练实例、8 rollouts、canonical decoder、二元 verifier 与总 token | 是 |
| DIVER | sequence-level exploration 的直接近邻 | https://arxiv.org/abs/2509.26209 | 固定默认 `diver` 分支 commit `5870b47`，已核验 `scripts/train/train_diver.sh`、`div_coeff=0.1` 与 `verl/div_src/reward_fn.py` | 只增加三个共享二元 verifier 分派；其余使用官方 diversity loss，匹配总生成/优化 token | 是 |
| Unweighted bridge replay | 隔离 proposal 本身与 importance correction，亦近似 BES/MaxRL 式成功候选直接回放 | 本研究必要消融 | 与主方法共用完整代码路径，仅固定 `w=1` | `4p+4q`、同一成功样本、loss 与预算；只关闭密度校正 | 是 |
| BES | 双向搜索、轨迹重组与 post-training 的最高近邻 | https://arxiv.org/abs/2605.28814 | 官方 commit `7c2696f` 已核验 `logical/verl/scripts/run_bes_local.sh --algo bes`、`bes_agent_loop.py`、K&K 数据及 SFT/BES checkpoints；现成任务不是本研究状态图 | 在其公开 agent-loop 接口接入相同 canonical action/verifier；主模型与 backward model 都固定为同一 base，搜索所有 LLM 输出计入相同生成 token 预算。适配失败则只报告不可复现，不以自写近似替代 | 是，最近机制基线 |
| EM Policy Gradient | 最近的 LLM off-policy reasoning RL，但不使用可逆 proposal 或可计算 mixture ratio | https://arxiv.org/abs/2504.18587 | 只核验论文，未找到作者公开的唯一训练仓库 | 用于界定近邻；不在最小实验中自写复现 | 否 |
- Reviewer 记录：`第 5 次独立审阅 7.2/10，promising_needs_revision，3 个 fatal blockers。抽象的 p/q/m 恒等式、w<=2、prior-batch action-independent baseline 与 4p+4q 分层采样通过；未通过项是 grammar mask/温度/top-p/exact-L 条件归一化没有形成唯一实际 PMF，BES agent loop 不能只换 scorer 迁移到目标任务，以及任取两族显著与未冻结 checkpoint/decoder/probe split 产生选择泄漏。技术最高近邻更新为 RL-PLUS。`

### IDEA-011：精确动作分布上的双向 MIS 策略梯度

- 来源：`最高近邻不足`
- 父 Idea：`IDEA-010`
- 状态：`promising_needs_revision`
- 定位关键词：reinforcement learning with verifiable rewards；multiple importance sampling；bidirectional search；capability boundary
- 一句话背景：这是在程序可验证的可逆规划任务中，当单向 RLVR 很少采到完整成功轨迹时，如何用概率已知的双向采样提高训练信号而不改变原始正向策略目标的问题。
- 自评分：`9.0/10`
- 一段话概括：把 Qwen2.5-Math-7B 直接变成固定动作码策略：Hanoi 使用 6 个有向 peg move，Shortest Path 使用 4 个方向，Knight Swap 使用完整 4x3 棋盘上的 56 个“颜色、起点、终点”有向动作；实际 tokenizer 已核验 94 个可打印 ASCII 字符均为单 token，所以无需新增 embedding。每一步只在该任务固定动作码集合上以 temperature 1 的 masked softmax 采样，非法动作进入吸收失败态，外部恰在公开 BFS 最短动作数 `L` 后停止；采样和 teacher forcing 共用同一 logits/mask，无 EOS、top-p 或长度条件。4 条完整正向轨迹与 4 条“正向 h 步 + 反向 L-h 步后逆序取逆”的完整 proposal 构成等权混合，所有 proposal 都保留；用精确行为概率的 balance weight 更新原始正向完整轨迹。三个预指定任务都作为共同主要任务，final-step checkpoint 和固定 decoder 下，方法必须在每个 seed 的等权三任务平均 pair-success 上同时超过四个确认性 baseline，12 个比较统一 Holm 校正；不再允许任取两族、挑 checkpoint 或 probe/test 重用。
- 打分理由：上一轮 reviewer 已确认理想化 MIS 恒等式与完整轨迹信用路径；本版用真实 tokenizer 与固定 action PMF 消除唯一数学落地漏洞，用官方 RL-PLUS commit 的真实入口替换 BES 伪适配，并冻结全部选择。相对 RL-PLUS 的增量不是 MIS 本身，而是由同一模型的可逆半轨迹形成已知 `q`、轨迹级无偏 balance weight 和不依赖外部 demonstrations 的能力获得检验；相对 bidirectional path tracing，这是向自回归 LLM policy gradient 的可检验迁移。主要研究风险是严格 importance weight 可能把 `q` 找到但在 `p` 下极低概率的成功轨迹权重压得太小；这正由 unweighted replay 消融和预注册梯度信噪比直接检验。
- Improver 搜索依据：https://arxiv.org/abs/2508.00222；https://github.com/YihongDong/RL-PLUS/tree/eb4aa4d4e2d7ce206056f9d7740138bfc94fad8f；https://arxiv.org/abs/2605.28814；https://arxiv.org/abs/2504.18587；https://arxiv.org/abs/2509.26209；https://arxiv.org/abs/1903.11908；https://github.com/open-thought/reasoning-gym/tree/49b07130b3fcd12f2d064bba7c43869543a0e7e7；`reference-code/orbit_robust_rlvr/qwen_tokenizer/tokenizer.json` 的结构化词表核验。
- Baseline 可复现性：

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 开源代码与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| Full-forward trajectory PG | 同一正向策略目标与完整轨迹 score-function estimator，隔离 proposal 的方差收益 | 标准 REINFORCE；loss 在本候选中完全定义 | 共享本研究训练代码；不需要隐藏数据或外部权重 | 每题采 8 条正向轨迹，复用同一上一批长度桶 baseline、单 batch 单更新、AdamW 和 final-step checkpoint | 是 |
| Vanilla GRPO | 同一 RLVR 稀疏二元 outcome 设置 | https://arxiv.org/abs/2402.03300 | Reasoning Gym commit `49b0713` 已核验 `training/train_grpo.py`；动作 wrapper 使用同一公共 sampler | 每题 8 条正向动作轨迹，组内 outcome normalization；模型、prompt、动作 mask、实例和预算相同 | 是 |
| DIVER | 同一 RLVR exploration 问题的 sequence-level diversity baseline | https://arxiv.org/abs/2509.26209 | https://github.com/NJU-RL/DIVER/tree/5870b47c695abdfc3a29b7a50c4b329ba7e4be06；已核验 `scripts/train/train_diver.sh`、`div_coeff=0.1`、`verl/div_src/reward_fn.py` | 保持官方 diversity loss 与 `div_coeff`，只让 rollout/scorer 读取共享动作码 batch；匹配 8 条轨迹和 token/step 预算 | 是 |
| RL-PLUS | 已直接研究 capability boundary collapse、hybrid-policy optimization 与 MIS 的技术最高近邻 | https://arxiv.org/abs/2508.00222 | https://github.com/YihongDong/RL-PLUS/tree/eb4aa4d4e2d7ce206056f9d7740138bfc94fad8f；已核验 `exp_scripts/train_RL-PLUS.sh -> verl.recipe.main_rlplus_ppo`、`rlplus_core_alg.py::compute_token_on_off_policy_loss` 与 parquet `target` schema | 每个训练实例的 `target` 使用公开 BFS oracle path 的同一动作码；共享 sampler 后保留官方 `n=8,n_prefix=1,prefix_ratio=1`、token-level MIS/EBAF 核心函数和方法系数；共同模型/optimizer/step/token 预算 | 是 |
| Unweighted bidirectional replay | 隔离双向 proposal 的数据效应与精确 importance correction | 本研究必要机制消融 | 与主方法同一代码路径，只把轨迹权重固定为 1 | 同一 `4p+4q` 样本、二元 verifier、baseline 与预算 | 是，消融 |
| BES | 双向搜索与轨迹重组的机制近邻，但官方实现不可直接迁移到本任务 | https://arxiv.org/abs/2605.28814 | commit `7c2696f` 的 `bes_agent_loop.py` 深度依赖 K&K `names`、oracle solution、goal tree 和文本编辑；scorer-only 适配不可行 | 只作 related work，不自写近似 baseline | 否 |
- Reviewer 记录：`第 6 次独立审阅 7.1/10，promising_needs_revision，6 个 fatal blockers。未发现机制级直接复现，tokenizer PMF、p/q/m 恒等式、w<=2、完整轨迹 credit 和三个任务的可逆性条件成立；未通过项是实际 token/逆变换表、detached loss、RL-PLUS/DIVER 的真实接入、统计 family/SNR 以及 split/超参仍未完全冻结。`

### IDEA-012：冻结动作码的双向 MIS-RLVR

- 来源：`第 6 次 reviewer 对执行与预注册自由度的定向修订`
- 父 Idea：`IDEA-011`
- 状态：`promising_needs_revision`
- 定位关键词：reinforcement learning with verifiable rewards；exact behavior density；bidirectional proposal；multiple importance sampling；capability acquisition
- 一句话背景：这是在可逆、程序可验证但成功轨迹稀疏的规划任务中，用同一旧策略的两个短方向条件分布构造完整候选，并在不改变原始正向 RLVR 目标的条件下提高发现成功轨迹概率的问题。
- 自评分：`9.1/10`
- 一段话概括：直接以 token ID 运行 Qwen2.5-Math-7B-Instruct 的固定动作策略，字符表固定为 `A-Z,a-z,0-3`；Hanoi、Shortest Path 和 4x3 Knight Swap 的动作、逆置换及结构变体都由送审前的显式表或唯一公式确定。每批每题 `4p+4q`，其中 `q` 为起点前半与目标反向后半的乘积，不拒绝任何串；`p_old/q_old/m_old` 全部由 update 前参数计算并 detach，最终 loss 对 batch 内 `64x8` 条完整正向 score-function 项取算术平均，因此 `p_old/m_old<=2` 且在旧参数处无偏。数据 quota、候选索引区间、13 个 `(task,L)` 桶循环 20 次和共 260 步全部冻结，所有方法每步 64 prompts、每题 8 条长度 L 动作串。确认性比较只保留可执行的 full-forward PG、GRPO、token-ID 适配后的 RL-PLUS 和 unweighted replay；用 12 个 one-sided exact McNemar 检验做 Holm 0.05 校正。能力证书在 960 个底层 test 实例上用 18 个 Bonferroni-Clopper--Pearson 端点要求单采样 RL 下界超过 base best-of-8 上界。
- 打分理由：新意仍是窄而真实的组合，不声称发明双向搜索或 MIS；相对 RL-PLUS，关键差异是无外部轨迹、可计算的轨迹级 `q`、有界 balance weight 和原始正向目标无偏性。第 6 轮的数学部分已经通过，本版主要把可实现性从“原则上”推进为唯一规范。真实风险不是定义缺口，而是 `q` 的成功增益可能抵不过 importance down-weight；这可由冻结 probe、unweighted 消融和最终独立正向评测直接否证。
- Improver 搜索及代码核验依据：https://arxiv.org/abs/2508.00222；https://github.com/YihongDong/RL-PLUS/tree/eb4aa4d4e2d7ce206056f9d7740138bfc94fad8f；https://arxiv.org/abs/2605.28814；https://arxiv.org/abs/2508.18244；https://arxiv.org/abs/2504.18587；https://arxiv.org/abs/2509.26209；https://github.com/NJU-RL/DIVER/tree/5870b47c695abdfc3a29b7a50c4b329ba7e4be06；https://github.com/open-thought/reasoning-gym/tree/49b07130b3fcd12f2d064bba7c43869543a0e7e7；本地 tokenizer 与 Knight 状态图枚举核验。
- Baseline 可复现性：

| Baseline | 与定位关键词及目标任务的关系 | 固定实现 | 唯一适配与预算 | 是否纳入最小实验 |
|---|---|---|---|---|
| Full-forward trajectory PG | 同一正向目标、loss、baseline 与优化器，隔离 proposal | 本研究公共训练入口 | 每题 8 条 `p_old` 完整串；每步 64 prompts、`8L` 采样动作和 `8L` 反传动作 | 是，首要机制对照 |
| Vanilla GRPO | 标准 outcome RLVR | 同一公共入口的 group-normalized 分支 | 每题 8 条正向串；`use_std=false`，其余模型、batch、步数和动作预算相同 | 是 |
| RL-PLUS | MIS/off-policy capability-boundary 最高技术近邻 | 官方 commit `eb4aa4d` 的 `main_rlplus_ppo`、`rlplus_vllm_rollout.py` 和 `compute_token_on_off_policy_loss` | 唯一差异是 dataset 后直接注入 `tgt_input_ids`，绕开文本 BPE；共享 masked logits。保留 `n=8,n_prefix=1,ratio=1`、token MIS/EBAF；固定 L 截断使 oracle EOS 不进入动作位，8 路都实际调用 L 步生成且 8L 动作参与 actor forward/backward | 是 |
| Unweighted bidirectional replay | 区分 proposal 暴露与精确校正 | 与主方法同一代码路径 | 同一 `4p+4q`、reward、baseline 和 loss，只令 `w=1` | 是，确认性机制对照 |
| DIVER | sequence-level exploration 近邻 | 官方 commit `5870b47` 已核验 | 该 commit 先把连续单字符 decode 后 `.split()` 做 BLEU-5，且公开 `train_diver.sh` 的 `rs_type=belu,neg_rs_scale=0` 使该动作接口下奖励退化；不修改算法后不能形成有效同域 baseline | 否，只作 related work |
| BES / TACSTaR | 双向搜索/目标条件 proposal 近邻 | 固定论文与公开实现 | 目标、筛选和训练范式不同，不以本地近似冒充复现 | 否 |
- Reviewer 记录：`第 7 次独立审阅 7.4/10，promising_needs_revision，2 个 fatal blockers。精确 MIS、动作逆映射、Knight 桶容量与 RL-PLUS token-ID 路由均通过；剩余问题是 RNG 到实例/评测流没有唯一规定，以及异质固定题集不满足 Clopper--Pearson 和 pooled exact McNemar 的底层假设。`

### IDEA-013：确定性协议下的双向 MIS-RLVR

- 来源：`第 7 次 reviewer 的两个局部 fatal blocker 定向修订`
- 父 Idea：`IDEA-012`
- 状态：`promising_needs_revision`
- 定位关键词：reinforcement learning with verifiable rewards；exact behavior density；bidirectional proposal；distribution-free capability certificate
- 一句话背景：这是在可逆稀疏奖励规划中，用精确双向 proposal 改善 RLVR 探索，并以对题目异质性稳健的预注册证书判断其是否形成可脱离搜索独立执行的能力。
- 自评分：`9.3/10`
- 一段话概括：方法仍是 reviewer 已确认的 `4p+4q` 轨迹级 balance MIS；新增的是不可变实验协议。Python 3.11 的三个 generator 按逐次 RNG 调用定义，split 在百万 index 内单遍路由到固定 quota；prompt 用 canonical JSON 和固定 chat template 序列化；训练每条 rollout 与评测每条 response 都有无碰撞整数 seed 公式。统计上，能力证书对每个固定 task/seed 的 960 个独立但可异质 pair-success 指标使用 one-sided Hoeffding LCB/UCB，确认性比较对 2880 个 `D_i in [-1,1]` 使用 Hoeffding-valid p-value，再做 Bonferroni/Holm。因而不再借用 binomial 同质性或 McNemar 交换性。
- 打分理由：这是 IDEA-012 的执行闭合，不是为追分改变 Claim。新颖性结论已有独立审阅支持：没有核验到同时包含精确自生成目标条件反向 `q`、轨迹级 balance MIS 和原正向 RLVR 无偏梯度的先例。现在的主要不确定性只剩实验是否产生正结果，而不是能否构造数据、计算 loss 或有效检验。
- Improver 搜索及核验依据：继承 IDEA-012 的全部固定论文/commit；第 7 轮新增核验 https://arxiv.org/abs/1803.10227、https://projecteuclid.org/journals/statistical-science/volume-16/issue-2/Interval-Estimation-for-a-Binomial-Proportion/10.1214/ss/1009213286.pdf、https://academic.oup.com/biometrics/article/62/3/921/7321763；分布无关替代使用 Hoeffding 对独立有界非同分布变量的标准上界。
- Baseline 可复现性：`Full-forward PG / GRPO / RL-PLUS / unweighted replay` 与 IDEA-012 完全相同；唯一新增是所有方法共享确定性 prompt、split、训练/eval RNG 协议。DIVER 只排除固定公开命令作为有效同域实现，不声称 DIVER 思路本身不适用。
- Reviewer 记录：`第 8 次独立审阅 7.3/10，promising_needs_revision，3 个 fatal blockers。MIS、动作/变体、固定长度反向拼接、token IDs、确定性 split/RNG、所有 quota 与 Hoeffding/Holm 推断均通过；剩余问题是各 baseline 的真实目标未完全冻结、RL-PLUS vLLM 与 CUDA Generator 合同冲突，以及 SNR 的 N/零方差语义不唯一。`

### IDEA-014：统一优化合同的双向 MIS-RLVR

- 来源：`第 8 次 reviewer 的三个局部执行 blocker 定向修订`
- 父 Idea：`IDEA-013`
- 状态：`promising_needs_revision`
- 定位关键词：reinforcement learning with verifiable rewards；exact behavior density；bidirectional proposal；controlled baseline objective；distribution-free capability certificate
- 一句话背景：这是在可逆稀疏奖励规划中，用精确双向 proposal 改善 RLVR 探索，同时用无采样器冲突、无损失尺度混杂的对照和分布无关证书判断收益是否内化为独立能力。
- 自评分：`9.4/10`
- 一段话概括：核心仍是已通过数学审计的 `4p+4q` 轨迹级 balance MIS。新增公共优化合同：main、full-PG、GRPO 和 unweighted 都关闭 entropy/KL/clip，按完整轨迹 token-sum 后对 `64x8` 平均；full-PG 明确复用滞后桶 baseline，GRPO 明确用不除标准差的组均值 advantage。RL-PLUS 确认性实现保留官方 token ratio、prefix mask 和 EBAF，但统一 reduction/entropy，并以公共 PyTorch sampler 先生成八路、再用确定性 BFS oracle 覆盖 slot 0 后进入官方核心 loss，彻底移除 vLLM RNG 冲突。Probe 的 `N_b=32n_b` 和零方差 SNR 也唯一规定。
- 打分理由：第 8 轮已独立复现全部数据 quota 并通过 MIS 和统计推导，本轮只消除会影响公平性与复现性的配置自由度。RL-PLUS 的论文机制和公共算力预算同时保留；其官方 shell 的原始 entropy/reduction 另作非确认性敏感度，不再污染主比较。若下一轮仍否决，应只能指向某个明确的官方核心语义或尚未发现的直接近邻，而不再是协议缺口。
- Improver 搜索及代码核验依据：继承 IDEA-013 全部来源；新增逐行核验 RL-PLUS commit `eb4aa4d` 的 `exp_scripts/train_RL-PLUS.sh`、`rlplus_core_alg.py::compute_token_on_off_policy_loss`、`compute_grpo_outcome_advantage_split` 与 actor microbatch reduction。确认官方 shell 使用 `entropy_coeff=0.001,loss_remove_token_mean=true,loss_remove_clip=true`，确认核心函数允许在公共 sampler 产出的 `DataProto`、raw response IDs 和 prefix mask 上独立调用。
- Baseline 可复现性：full-PG 使用 main 的 `b_old`、完整轨迹和同 reduction；GRPO 的 `A=R-group_mean(R)` 与完整公式已冻结；unweighted 只令 `w=1`；`RL-PLUS-core-matched` 的所有保留/覆盖配置、BFS tie-break、slot-0 覆盖、old-log-prob 重算和预算记账均在 round-09 brief 中逐项固定。DIVER 仍只作相关工作。
- Reviewer 记录：`第 9 次独立审阅 7.2/10，promising_needs_revision，4 个 fatal blockers。核心 p/q/m、4+4 loss、w<=2、动作、容量、Hoeffding/Holm、桶级 SNR、公共 sampler 和 RL-PLUS slot 覆盖路径均成立；剩余问题是 use_std=false 不能称 vanilla GRPO、RL-PLUS 应使用全八路 advantage 并冻结 beta、评测实际 token 预算不等，以及 GRID 尺寸未分配到 split。`

### IDEA-015：等预算能力证书下的精确双向 MIS-RLVR

- 来源：`第 9 次 reviewer 的四个标签与冻结 blocker 定向修订`
- 父 Idea：`IDEA-014`
- 状态：`needs_rethink`
- 定位关键词：reinforcement learning with verifiable rewards；exact bidirectional density；trajectory MIS；equal-budget capability certificate；controlled baselines
- 一句话背景：这是在可逆稀疏奖励规划中，用精确双向 proposal 提高成功轨迹发现率，同时以等生成预算、结构外推和原始正向独立解码判断探索收益是否真正进入模型策略。
- 自评分：`9.5/10`
- 一段话概括：不改 `4p+4q` 方法。Vanilla GRPO 恢复 `A=(R-mean)/(sample_std+1e-6)` 和 `cliprange=0.2`；RL-PLUS-core-matched 改用官方 launcher 真正调用的全八路 `compute_grpo_outcome_advantage`，明确 `alpha=beta=1` 及所有影响梯度的开关。GRID 唯一规定 train/probe/dev 为 12x12、test 为 16x16。评测时每个 checkpoint 对原题/变体都生成八路，所以总预算同为 `16L`；trained 方法主证书预注册只读 rollout 0，base envelope 读八路 best-of-8，额外七路不参与 trained 主 Claim。
- 打分理由：这四处均是可直接验证的有限修订。第 9 轮已经明确判定共同 PyTorch sampler、oracle 覆盖、old-log-prob 重算及 `8L` 训练预算在工程上可行；本版只让 baseline 名称与实际目标一致，并满足冻结 Anchor 的等评测预算。窄创新边界维持不变：不是新 MIS 理论，而是精确自生成双向密度、原 forward RLVR 无偏更新和能力内化证书的组合。
- Improver 搜索及代码核验依据：继承 IDEA-014；新增核验 RL-PLUS commit `eb4aa4d` 的 `rlplus_trainer.py::compute_advantage`，确认 launcher 的 `algorithm.adv_estimator=grpo` 进入 `core_algos.compute_grpo_outcome_advantage` 并覆盖全部八路；确认 YAML 的 `prefix_reward_weight_beta=1.0`。Vanilla GRPO 依 DeepSeekMath 定义恢复组内标准差。
- Baseline 可复现性：主 brief 已给出 vanilla GRPO 的 sample-std、epsilon、ratio、clip 和 reduction；RL-PLUS-core-matched 明确不是官方 recipe，固定其全八路 advantage、alpha/beta、ratio/EBAF 与所有 loss 开关；full-PG/unweighted 保持上一轮已通过的公共合同。官方 RL-PLUS recipe 仅作非确认性敏感度。
- Reviewer 记录：`第 10 次独立审阅 7.4/10，needs_rethink，2 个 fatal blockers。第 9 轮四项故障全部关闭；p/q/m、sampler/action/split、baseline、公平预算与统计均成立。剩余冲突是主 loss 仍估计单题正向回报、没有直接优化跨变体联合成功，以及缺少 Anchor 指定的 OMEGA 外部补充。`

### IDEA-016：双侧乘积目标的精确双向 MIS-RLVR

- 来源：`第 10 次 reviewer 对冻结 Problem Anchor 的机制级修订`
- 父 Idea：`IDEA-015`
- 状态：`final`
- 定位关键词：reinforcement learning with verifiable rewards；paired capability objective；exact bidirectional density；trajectory MIS；capability acquisition
- 一句话背景：这是在可逆稀疏奖励规划中，直接最大化同一底层问题及其结构变体被两次独立正向执行同时解决的概率，并用双向 proposal 的精确密度缓解乘积奖励更稀疏的问题。
- 自评分：`9.6/10`
- 一段话概括：每批由 32 个底层实例及其预注册非恒等变体组成 64 prompts，每侧各采 `4p+4q`。目标改为 `J_cap=E_x[mu(x)mu(Tx)]`；两侧八样本做 `8x8` 笛卡尔积，联合 weight 为 `w_i^0w_j^1<=4`，pair loss 同时包含两侧完整 forward score，因此在旧参数处无偏估计结构联合成功目标的梯度。Full-forward paired PG 用同一目标隔离 proposal，unweighted paired replay 隔离校正，vanilla GRPO 和 RL-PLUS-core-matched 看到逐字相同 64 prompts 与预算。外部补充冻结 OMEGA explorative/compositional/transformative 的 grid-related 全量子集、revision、生成与 integer scorer。
- 打分理由：该修改正面满足“训练目标直接优化后一种现象”，不再把能力复用只留给评测。稀疏度增加是可证伪的实际风险，也正是精确双向 proposal 应被检验的场景；product-MIS 的无偏性来自两个独立 deterministic-mixture 估计器的乘积，不需要新的 rejection、teacher 或连续超参。第 10 轮已通过的 tokenizer、环境、sampler、baseline 与统计合同全部继承。
- Improver 搜索及代码核验依据：继承 IDEA-015；OMEGA 官方代码固定到 commit `589954335e9ca8555636770fa2c55eba6efcb4f9`，官方 Hugging Face revisions 固定为 explorative `b04ae8d`、compositional `fabf91c0`、transformative `f188d999`；数据服务核验三个选定 split 分别恰有 `100/50/16` 题且 ground truth 为整数计数。
- Baseline 可复现性：full-forward paired PG 复用同一 product objective；vanilla GRPO 与 RL-PLUS-core-matched 以相同 paired prompt exposure 运行各自冻结目标；unweighted paired replay 只去掉两侧 importance weight。训练仍为每步 64 prompts、每 prompt 8 条、260 步、3 seeds。
- Reviewer 记录：`第 11 次独立审阅 7.9/10，experiment_ready，fatal blockers 为空，gate 通过。Reviewer 确认乘积目标直接优化跨变体联合成功，完整 8x8 MIS loss 在旧参数处无偏、joint weight<=4，五方法预算与 OMEGA 协议闭合。非致命边界：probe 未按变换轨道完全隔离；能力证书和 baseline 比较是两个独立 alpha=0.05 family；新颖性只限完整组合。`
