# Idea 候选池

> 本文件由 idea improver 持续维护。保留所有进入过比较的实质性候选及其演化关系；不要把完整 proposal 写进这里。

- 输入模式：`problem_card`
- 输入论文：不适用
- 输入问题卡：`path-stage/LLM新兴领域研究地图_20261021`，Q001

## 当前选择

- Reviewer 调用：`8 / 20`
- 当前选中 Idea：`IDEA-012`
- 当前自评分：`7.9/10`
- 选择理由：IDEA-011 首审 8.2、复核 6.0。复核指出问题卡论文 2609.39118 表 4 已在 TH 下做过无关解答对照，主张一的"从未检验"不成立。IDEA-012 按此重新定位：把认知通道的因果检验升为主张一；主张二改为在确认退化的配置下，对 2609.39118 单种子的"偏移即足够"做干净检验，方向与现有证据一致。它是池中自评最高的 available 候选。
- 状态：`等待第 9 次 reviewer 调用`

> 2026-10-28 改进者检索要点（只记来源，不送审）：
> - 卡片之外，近期窗口内还有大量 OPSD 机制与修法工作（HJSang/awesome-OPSD 收录 60 篇）：
>   - Purified OPSD 2607.02234：参考解答诱导的更新分量，用 PMI 目标去掉；R1-Distill-Qwen-7B 上 "Wait" 从 34K 升到 83K，Qwen3-8B 上认知词崩塌。
>   - 2603.24472：SDPO 下 R1-Distill-Qwen-7B 认知词减少、AIME24 降约 40%；在 GRPO 中惩罚认知 token 会复现下降。
>   - AR-OPD 2606.10385：部分特权锚点加残差。
>   - 2609.25623：特权上下文抽象层级。
>   - OP²SD 2608.09228：换成另一题的示例。
>   - 2609.20612：无参考对照。
>   - RLCSD 2606.11709：正确提示与错误提示的对比。
>   - DASD 2605.22263：按熵路由吸引或排斥。
>   - 2605.13255：教师熵置信门。
>   - OPSD 官方仓库的逐 token 散度截断（README：风格 token 的 KL 是数学 token 的 6–15 倍）。
> - 2607.05184 本身已用词汇代理测到"特权教师给 wait/but 更低概率"，但自认非因果、未给修法。
> - 方向冲突（同为 R1-Distill-Qwen-7B，2603.24472 认知词降、Purified 认知词升；2607.05184 变短、2609.39118 变长）在上述列表中没有系统研究，需要 reviewer 检索。

## 候选列表

### IDEA-001：交叉教师上下文 × 高熵梯度 × 损失的诊断矩阵

- 来源：`问题卡切口`
- 父 Idea：`无`
- 状态：`available`
- 定位关键词：on-policy self-distillation；privileged information；thinking models；reverse KL；JSD
- 一句话背景：OPSD 让训练时开思考的推理模型在长评测预算下退化，但上下文语义、熵位置梯度和损失形式哪一个起作用尚不清楚。
- 自评分：`5.0/10`
- 一段话概括：照问题卡切口，在固定模型与数据上交叉教师上下文{无/完整/无关/只给答案} × 高熵梯度{遮/不遮} × 损失{JSD/前向 KL}，看认知词密度、长度、pass@1/pass@k 随评测预算的曲线。
- 打分理由：这是纯诊断矩阵。其中"上下文语义 vs 偏移"已被 OP²SD、2609.20612、Purified OPSD 覆盖，"高熵遮罩"已被 AD-OPSD 覆盖；组合本身缺少待判别的主张。
- Idea 生成依据：来自问题卡 Q001。
- 自评分轻量新意依据：见上方检索要点。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：弱，主要是组合。
- Baseline 可复现性：未展开（未送审）。
- Reviewer 记录：`尚未送审`

### IDEA-002：把教师信号分解为"特权语义"与"上下文偏移"两个分量

- 来源：`领域共性不足`
- 父 Idea：`无`
- 状态：`covered`
- 定位关键词：on-policy self-distillation；privileged information；pointwise mutual information
- 一句话背景：2607.05184 与 2609.39118 对退化来源（语义泄露 vs 上下文偏移）给出相反的解读。
- 自评分：`4.0/10`
- 一段话概括：用"同长度无关解答"教师把对数比拆成 Δ_sem 与 Δ_shift，分别只用一个分量做蒸馏，看哪个分量带来缩短与长预算退化。
- 打分理由：已被覆盖。Purified OPSD 用"只看参考解答的教师"把更新拆成参考诱导分量与可迁移分量，并给出 PMI 修法；OP²SD 与 2609.20612 已做替换解答与无参考对照。
- Idea 生成依据：来自问题卡 Q001（2607.05184、2609.39118）。
- 自评分轻量新意依据：Purified OPSD 2607.02234（§3 分解）；OP²SD 2608.09228；2609.20612。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：无（已覆盖）。
- Baseline 可复现性：未展开。
- Reviewer 记录：`尚未送审（改进者核对后判为已覆盖）`

### IDEA-003：把特权信息只用于价值估计（非对称 actor-critic），不作模仿目标

- 来源：`相似领域成熟方法迁移`（POMDP 中的非对称 actor-critic 与模仿缺口）
- 父 Idea：`无`
- 状态：`available`
- 定位关键词：privileged information；asymmetric actor-critic；on-policy distillation；value function
- 一句话背景：模仿看得到全状态的专家会丢掉信息收集类动作（模仿缺口）；机器人领域的标准做法是只让 critic 使用特权信息。
- 自评分：`4.5/10`
- 一段话概括：不把参考解答作为逐 token 模仿目标，而是用它估计前缀价值（例如由特权模型给出到达参考答案的概率），再做优势加权更新。
- 打分理由：迁移结构成立，但 Le Critique 2608.16739（特权价值函数用于 LLM RL）与 SIPO、RLCSD 等"RL + 特权信号"工作已接近；它也不回答问题卡的方向冲突。未细读 Le Critique，需要 reviewer 检索。
- Idea 生成依据：Warrington et al. 2021（非对称模仿学习中的模仿缺口）；Le Critique 2608.16739（标题与检索摘要）。
- 自评分轻量新意依据：需要 reviewer 检索。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：弱。
- Baseline 可复现性：未展开。
- Reviewer 记录：`尚未送审`

### IDEA-004：训练上限造成的截断比例决定失效时长度变长还是变短

- 来源：`领域共性不足`
- 父 Idea：`无`
- 状态：`available`
- 定位关键词：on-policy distillation；truncation；response length；thinking models
- 一句话背景：2610.03185 显示截断回复进入损失会导致长度爆炸；2609.39118（上限 1,024）变长，2607.05184（上限 4,096）变短。
- 自评分：`5.5/10`
- 一段话概括：主张长度方向由训练 rollout 的截断比例决定。改变训练上限并遮掉截断回复，检验长度方向是否随之翻转。
- 打分理由：可以解释两篇之间的长度冲突，但解释不了同为 R1-Distill-Qwen-7B 时认知词方向相反（2603.24472 vs Purified）；而且思考模型在 1,024 上限下几乎全部被截断，遮掉截断回复会去掉大部分数据。作为竞争解释并入 IDEA-005 更合适。
- Idea 生成依据：2610.03185 §5.2；问题卡分歧。
- 自评分轻量新意依据：未见针对这一冲突的工作，需要 reviewer 检索。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：一个可检验的方向解释。
- Baseline 可复现性：未展开。
- Reviewer 记录：`尚未送审`

### IDEA-005：OPSD 失效的方向由教师对特权上下文的初始认知反应决定——用呈现模板翻转方向的因果检验，以及保持认知类质量的修法

- 来源：`领域共性不足`（结合 `最高近邻不足`：2607.05184 的 fork 抑制机制未做因果检验）
- 父 Idea：`无`
- 状态：`needs_revision`
- 定位关键词：on-policy self-distillation；privileged information；thinking models；epistemic tokens；response length
- 一句话背景：OPSD 会改变思考模型的认知类 token（wait、hmm 等）与回复长度，但改变方向在不同论文、同一模型之间相互矛盾，现有"特权教师更自信更简洁"的解释只能说明其中一个方向。
- 自评分：`7.6/10`
- 一段话概括：
  - **主张一（方向律）：** 用初始化时的一个静态量 ρ 预测 OPSD 后认知词密度与长度变化的方向。ρ 是在固定的学生 rollout 上，教师与学生在认知词集合上的总概率之比的对数均值。用同一份参考解答、不同呈现模板（"已验证正确的参考解答"与"一份待检查、可能有错的解答"）翻转 ρ 的符号，检验在模型、数据、训练上限与损失都固定时，方向是否随之翻转。训练上限（对应截断解释）与损失（JSD/前向 KL）作为竞争解释一并交叉。
  - **主张二（必要性，兼作修法）：** 在每个位置把教师分布在认知词集合上的总质量重新归一到学生的总质量（EMP），其余位置照常蒸馏。预期它在两个方向上都消除长预算退化；把同样的操作施加到频率匹配的随机 token 类上则无效。
  - **最小实验：** Qwen3-1.7B 开思考，OpenThoughts 15k，模板 × 上限 × 种子，加损失检验、EMP、随机类对照与逐 token 截断 baseline；R1-Distill-Qwen-7B 两个模板做外部检验。
- Story line：
  - 明确失败：同为 Qwen3，OPSD 压低认知词、长预算下回复变短（2607.05184、2603.24472、2607.10805）；同为 R1-Distill-Qwen-7B，SDPO 压低认知词（2603.24472），OPSD 却让 "Wait" 从 34K 升到 83K（Purified OPSD）；2609.39118 中退化伴随评测长度增长。
  - 现有解释"特权教师更自信、更简洁"只预测压低这一个方向；截断与损失解释各自只覆盖部分冲突。
  - 被忽视的关键：方向取决于该模型在看到特权上下文时，认知类质量相对学生是升还是降。这是一个可在训练前测得、又可以用呈现模板直接操纵的量。
  - 本 Idea 的动作：先测 ρ，再用模板翻转 ρ，在交叉上限与损失的设计中检验方向是否跟随 ρ；然后用 EMP 只抹掉认知类边际的差异，检验长预算退化是否因此消失。
  - 预期：方向跟随 ρ、不跟随上限或损失，则支持方向律；方向跟随上限，则支持截断解释。EMP 消除退化而随机类对照不能，就为"认知行为改变是因、不是伴随"提供必要性证据。
- 打分理由：
  - 直接回应问题卡"尚未解决"中的方向冲突，并把 IDEA-004 作为竞争解释纳入判别设计。
  - 2603.24472 已在 GRPO 中给出"压低认知 token 会伤害"的充分性证据；本 Idea 补上 OPSD 中的必要性，并解释方向本身。
  - 风险：修法层与 Purified OPSD、AD-OPSD、DASD、逐 token 截断同属"保护认知行为"的大类；模板 B 可能翻不出正的 ρ；7B 外部检验成本较高。
- Idea 生成依据：
  - 2607.05184（fork 抑制、词汇代理、表 5 的 wait/hmm 密度、长预算变短）；
  - 2603.24472（10 个认知词、GRPO 惩罚干预、R1-Distill 下降）；
  - Purified OPSD 2607.02234（R1-Distill "Wait" 上升、Qwen3-8B 崩塌）；
  - 2609.39118（变长）；2610.03185（截断）；
  - OPSD 官方仓库 README（风格 token 的 KL 偏高）。
  - 其中 2607.05184、2609.39118、2610.03185 来自问题卡 Q001。
- 自评分轻量新意依据：
  - 检索"self-distillation wait tokens increase/decrease direction model"，以及 awesome-OPSD 60 篇摘要中的 length/epistemic/direction/truncation，只命中机制描述和单向的修法，未见对方向冲突的系统判别，也未见用呈现模板操纵认知反应。
  - EMP 这一修法形式未见；但"保护认知行为"的目标已有多篇，需要 reviewer 检索。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：用一个训练前可测、可操纵的量（教师对特权上下文的认知反应）统一解释 OPSD 失效方向的跨论文冲突，并用类特异的边际保持干预给出必要性检验。
- Baseline 可复现性：

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 开源代码与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| vanilla OPSD（思考模型设置） | 同任务同评测：思考模型 OPSD 的长预算退化，最高近邻 | https://arxiv.org/abs/2607.05184 | https://github.com/princeton-pli/rethinking-opsd-for-thinking-models （2026-10-28 git ls-tree 核验：`train.py`、`opsd/trainer.py`、`run_budget_sweep.py`、`run_eval.py`、`data_tools/build_openthoughts_30k.py`、`make_openthoughts_15k_subset.py`、`submit_experiment.sh`；README 列出 25 个实验名） | `data_tools/` 构建 OpenThoughts 15k → `train.py`（JSD，上限 4,096）→ `run_budget_sweep.py` | 是 |
| OPSD + 逐 token 散度截断 | 同任务的"压低风格 token 信号"修法 | https://arxiv.org/abs/2601.18734 | https://github.com/siyan-zhao/OPSD （核验：`opsd_trainer.py` 中 `generalized_jsd_loss(..., token_clip)`，`scripts/run_opsd_1b.sh` 用 Qwen3-1.7B、`--jsd_token_clip 0.05`） | 把 token_clip 逻辑移植进同一套训练代码 | 是 |
| 基座模型 | 参照 | — | 无需仓库 | 直接评测 | 是 |
| AD-OPSD、Purified OPSD | 同任务修法 | 2607.10805、2607.02234 | 未找到公开代码（awesome-OPSD 中 code_url 为空） | 无法核验 | 否（作相关工作） |

- Reviewer 记录：`Call 1（常规，effort high）：5.5/10，promising_needs_revision，无 fatal，最高近邻 2609.20612、2609.39118、2607.05184、Purified OPSD 2607.02234、AD-OPSD 2607.10805`。要点：方向冲突作为问题有据；但训练前的教师−学生 marker 偏差已有 2609.20612 的 correction pressure（采样 token 版，Qwen 上普遍为负、不区分结局），2609.39118 的初始 KL 也不能预测方向；方向律接近同义反复（学生向教师边际移动即蒸馏定义）；最直接的竞争干预（marker 位置损失排除/降权，2609.20612 报告几乎无效）未进 baseline；算力严重低估（官方 README：每次 5–12 h × 8×H100，评测每任务 8 分片 × 约 4 h）。改进者核对 2609.20612 原文与仓库：marker 干预与换参考只在 DR 下做；TH 下 Full Trace 第 100 步 72.79 vs 基座 80.21、DR 82.62；作者自述模式/时间跨度/监督比例未分开；marker 抑制不区分结局。子候选：IDEA-006（不继承本候选的方向律）。

### IDEA-006：特权监督伤害的是思考段而不是答案段——用预算强制的完整思考 rollout 和分段掩码拆开 TH 训练的混杂，检验模仿缺口

- 来源：`领域共性不足`（2609.20612 自述未分开的混杂；2607.05184 训练开思考才有害）+ `相似领域成熟方法迁移`（非对称模仿学习中的模仿缺口）
- 父 Idea：`无`（由 IDEA-005 的 Call 1 审查与 2609.20612 原文触发，Claim 与机制都不同）
- 状态：`needs_revision`
- 定位关键词：on-policy self-distillation；privileged information；thinking models；budget forcing；imitation gap
- 一句话背景：同一套 OPSD 在直接回答 rollout 上有增益、在开思考 rollout 上变成损失（2609.20612），而模式、监督段与教师信息这几个因素至今没有分开。
- 自评分：`7.7/10`
- 一段话概括：
  - 主张一：用预算强制把开思考 rollout 截成完整的"短思考 + 答案"，在同一批 rollout 上只改损失掩码。只监督思考段会复现 TH 的下降，只监督答案段得到 DR 级的增益。
  - 主张二：思考段的伤害需要本题的特权信息。换成长度匹配的另一题参考后，下降显著减小。
  - 实验：在 2609.20612 的代码与配置上，用 Qwen3-1.7B、Full Trace 视图，7 个臂 × 3 个种子，rollout 都不超过约 1,050 token。利用"损失只覆盖前 1,024 token"这一点，低成本复现 TH 的下降。
- Story line：
  - 明确失败：2609.20612 中 TH 训练下降到 72.79（基座 80.21，DR 82.62），作者自述模式、跨度、监督比例未分开，并指出 marker 抑制不区分两种结局；2607.05184 也发现训练开思考才有害。
  - 对照证据：TOPD（2605.31490）用不带特权信息的外部教师只监督前段，反而有增益，说明"监督开头段"本身不有害。
  - 被忽视的关键：特权监督的可模仿性取决于段，这是模仿缺口在推理上的对应。思考段的探索行为在已知答案的教师下学不来；事后写出解答的段可以模仿。
  - 本 Idea 的动作：预算强制完整 rollout，加思考段/答案段掩码，加另一题参考的 2×2。
  - 预期：思考段掩码下降、答案段掩码上升，则支持；答案段也下降，则推翻（任何 TH 监督都有害）；另一题参考同样伤害思考段，则推翻主张二（上下文偏移即足够）。
- 打分理由：
  - 直接拆开最高近邻明确留下的混杂。用的是已核验的单 GPU 代码，成本低，可证伪，结果不论落在哪一格都有信息量。
  - 风险：预算强制截短思考本身可能改变结论，所以判定表设了这一格；评测成本主要在测试切分；"模仿缺口"的机制解释只是被判别设计间接检验。
- Idea 生成依据：
  - 2609.20612（表 11、表 2、讨论节；仓库 configs/experiments.md 与 controls）；
  - 2607.05184（表 3，来自问题卡 Q001）；
  - TOPD 2605.31490（截断 OPD 的分段分析）；
  - Weihs et al. 2021《Bridging the Imitation Gap by Adaptive Insubordination》与 Warrington et al. 2021《Robust Asymmetric Learning in POMDPs》（模仿缺口）。
- 自评分轻量新意依据：检索"self-distillation thinking segment vs answer segment loss mask""on-policy distillation budget forcing thinking rollouts"，只命中 2607.05184、Purified、Bridged、TOPD（无特权、按位置分 10% 段）；2609.20612 的 TH 变体只有思考段内的窗口位置，未见分段掩码或强制完整 TH。需要 reviewer 检索。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：第一次在开思考的 OPSD 中把"推理模式、监督的段、教师掌握的信息"拆开做因果检验，把 TH 损失定位到"带本题特权信息的思考段监督"。
- Baseline 可复现性：

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 开源代码与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| DR 训练的 OPSD | 同任务、同模型、同评测的增益锚点 | https://arxiv.org/abs/2609.20612 | https://github.com/xiuyuz/opsd-reference-study （2026-10-28 git ls-tree 核验：`training/launch_run.sh`、`training/train_opsd.py`、`training/rollout_worker.py`、`opsd/opsd_loss.py`、`configs/experiments.md`、`data/controls/length_matched_other_problem.py`、`evaluation/build_eval_queue.py`；README 称每次运行在单张 80GB GPU 上完成） | `CONDITION=full_trace ROLLOUTS=direct bash training/launch_run.sh` | 是 |
| TH 训练的 OPSD | 同任务的退化设置 | 同上 | 同上 | `ROLLOUTS=thinking TRAIN_MAX_NEW_TOKENS=1024 LOSS_HORIZON=1024`（原文 20764） | 是 |
| 基座 | 参照 | — | — | `evaluation/build_eval_queue.py --mode thinking` | 是 |
| TOPD | 不带特权信息的截断 OPD，方法启发 | https://arxiv.org/abs/2605.31490 | 未核验 | — | 否（跨设置启发） |

- Reviewer 记录：`Call 2（常规，effort high）：6.0/10，promising_needs_revision，最高近邻 2609.20612、2607.05184、OP²SD 2608.09228、2603.24472、2608.25936`。fatal：R4−R3>0 同样被 fork/epistemic 抑制预测，只定位不判机制；512 预算强制截断多数思考，答案段不是事后书写，且 R3/R4 被监督 token 数未匹配；另一题参考混淆“无本题信息”与“错误答案”，OP²SD/2608.18271 已报告非思考设置下的效果；判定表未覆盖 ΔR3<0 且 ΔR4 不显著。改进者核对 2607.05184 附录 E：非特权 OPD 中只在 marker 位置与随机位置计损失无法区分；marker 边际 0.00928→0.00853（加参考）。子候选：IDEA-007。

### IDEA-007：TH 训练下 OPSD 的退化由"内容引导"而非"认知类总量"承载——前向 KL 的边际/条件精确分解与只留一项的因果检验

- 来源：`领域共性不足`（多篇工作都把退化归因于认知抑制，但 2609.20612 指出它区分不了结局）+ `相似领域成熟方法迁移`（非对称模仿学习中的模仿缺口）
- 父 Idea：`IDEA-006`
- 状态：`needs_revision`
- 定位关键词：on-policy self-distillation；privileged information；thinking models；epistemic tokens；forward KL
- 一句话背景：TH 训练让 OPSD 的增益变成损失。主流解释是认知类 token 被压低，但它没有在特权、开思考的 OPSD 中被隔离检验，且有反证。
- 自评分：`7.8/10`
- 一段话概括：
  - 每个位置的前向 KL 可精确拆成两项：一是认知 marker 类总量的伯努利 KL（边际项），二是类内条件分布的 KL（条件项）。
  - 在自然 TH rollout（上限 1,024，与原文损失等价）上，用同样的 token、同样的 rollout，只改目标：T1 只留条件项，T2 只留边际项，T3 是换成频率匹配随机类的 T1，T4 是现有的 marker 位置排除。
  - 主张 H-content：T1 复现大部分下降，T2 不造成显著下降。判定表事先固定且穷尽，挽回比例 r 是核心量。
- Story line：
  - 明确失败：2609.20612 中 TH 训练让 OPSD 从 82.62（DR）降到 72.79（基座 80.21）；2607.05184 也发现训练开思考才有害。
  - 现有解释：主流把它归因于认知抑制（2607.05184、2603.24472、2607.10805），但 OPSD 中未被隔离；2609.20612 指出 marker 抑制在 DR 与 TH 中都存在，而且 DR 下的 marker 排除几乎不改变行为；加参考后 marker 类边际只从 0.00928 降到 0.00853（2607.05184 附录 E）。
  - 被忽视的关键：前向 KL 可以把"多犹豫还是少犹豫"与"往哪走"精确分开。
  - 本 Idea 的动作：只留其中一项分别训练，配随机类对照。
  - 预期：T1 仍退化、T2 不退化，则支持事后引导（模仿缺口）；反之支持认知抑制。两种结果都改变该领域对修法方向的判断。
- 打分理由：
  - 判别直接针对 Call 2 指出的"只定位不判机制"；所有 TH 臂被监督的 token 完全相同，去掉了预算强制与另一题参考的混淆；判定表穷尽。
  - 用的是已核验的单 GPU 代码，生成成本约为原文的 1/20。
  - 风险：边际项本身占 KL 比例很小，T2 可能因为信号太弱而"无害"，被看成平凡结果，所以判定表要求 T1 同时复现下降；T1 的条件项权重用的是 m_S 而不是 m_T，只是近似。
- Idea 生成依据：
  - 2609.20612（表 11、表 2、讨论节；仓库 `train_opsd.py` 的 `apply_loss_horizon` 与 `--fork-mask-mode`，`opsd_loss.py` 的前向 KL）；
  - 2607.05184（附录 E 的掩码与边际统计、附录 A）；
  - 2603.24472（GRPO 认知惩罚）；2607.10805；
  - Weihs et al. 2021、Warrington et al. 2021（模仿缺口）；2608.25936（综述的模仿缺口框架）。
- 自评分轻量新意依据：2607.05184 只在非特权 OPD 中比较 marker 位置与随机位置的损失；2609.20612 的 marker 干预只在 DR 下做；未见按边际/条件分解目标的 OPSD 工作。需要 reviewer 检索。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：在真正退化的 TH 设置中，用前向 KL 的精确分解，把"认知类总量"与"内容引导"分开做因果检验，判别 OPSD 退化的承载机制。
- Baseline 可复现性：

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 开源代码与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| TH 训练的 OPSD（T0） | 同任务同模型同评测的退化设置 | https://arxiv.org/abs/2609.20612 | https://github.com/xiuyuz/opsd-reference-study （2026-10-28 git show 核验 `train_opsd.py` 的 `apply_loss_horizon`、`--fork-mask-mode`，`opsd_loss.py`，`constants.CORRECTION_MARKERS`） | `CONDITION=full_trace ROLLOUTS=thinking TRAIN_MAX_NEW_TOKENS=1024 LOSS_HORIZON=1024 bash training/launch_run.sh` | 是 |
| marker 位置损失排除（T4） | 同任务已有干预 | 同上 | 同上 | 加 `--fork-mask-mode exclude` | 是 |
| DR 训练的 OPSD | 增益锚点 | 同上 | 同上 | `ROLLOUTS=direct` | 是 |
| 基座 | 参照 | — | — | `evaluation/build_eval_queue.py --mode thinking` | 是 |

- Reviewer 记录：`Call 3（常规，effort high）：6.0/10，promising_needs_revision，最高近邻 2609.20612、2607.05184、AD-OPSD 2607.10805、Purified OPSD 2607.02234、2608.04794（PI bias）；方法近邻 DKD 2203.08679`。fatal：条件项是残差桶，E 只含 11 个整词单 token，漏 hmm、alternatively、recall 与多 token 认知短语，H-content 不可识别；称 2603.24472 无 GRPO 认知惩罚（改进者核对 v4 “A Causal Intervention” 一节：确有，κ=0.5，复现下降与变短；reviewer 疑读旧版）。另：截断目标下分解不精确；T1 按 m_S 加权。子候选：IDEA-008。

### IDEA-008：IDEA-007 的可识别版——扩大认知类、精确未截断分解、两项操纵检查与参考路径拉力

- 来源：`领域共性不足` + `相似领域成熟方法迁移`（模仿缺口；分解形式来自 DKD 2203.08679）
- 父 Idea：`IDEA-007`
- 状态：`needs_revision`
- 定位关键词：on-policy self-distillation；privileged information；thinking models；epistemic tokens；forward KL
- 一句话背景：同 IDEA-007。
- 自评分：`7.9/10`
- 一段话概括：
  - Claim 不变，H-content 只在操纵检查通过后才成立。
  - $E$ 改为三份已发表词表的并集，并加入多 token 认知词中专属的首子词。
  - 损失直接按 $L_{\text{marg}}$、$L_{\text{cond}}$（以 $m_T$ 加权、不截断）构造，使 T0u 精确等于两项之和；官方截断目标只作复现锚点。
  - M1：T1 的短语级广义认知密度与基座相差不超过 ±10%。M2：T2 确实移动了 $E$ 密度。
  - 用学生对参考解答的对数概率提升（对应 2608.04794 的 PI 偏差）作为 H-content 的正向证据。
  - 判定表新增"不可识别""T2 太弱"两格。
  - 引用 2603.24472 时注明 v4 版本与章节；把 DKD 列为分解形式的出处。
- 打分理由：修掉 Call 3 的两条 fatal（其中错引一条经核对属旧版误读，改为写明版本）。新意仍是诊断性因果实验，上限受限。
- Idea 生成依据：同 IDEA-007；2608.04794（PI 偏差分数）；DKD 2203.08679；2603.24472 v4。
- 自评分轻量新意依据：同 IDEA-007；Call 3 reviewer 独立检索也未见 TH-OPSD 中的边际/条件因果消融。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：同 IDEA-007，加上可识别性设计。
- Baseline 可复现性：同 IDEA-007 表；另加 T0u（未截断完整 KL）作分解参照。
- Reviewer 记录：`Call 4（常规，effort high）：6.5/10，promising_needs_revision，最高近邻 2609.20612、2607.05184、Purified OPSD、AD-OPSD、2608.04794`。fatal：参考路径拉力是相关指标，未与 DR 锚点对照，也没有 TH 下他题/错误参考来区分参考语义与上下文偏移；L_marg 占比小，“r 上界<0.25”近乎由构造保证。另：2603.24472 的因果研究应按 GRPO 节引用；2607.10805 的 10.3→7.9 有表内不一致。改进者核对 OP²SD（2608.09228）：主设置为非思考学生，附录 H 两边开思考只跑本题参考 OPSD（49.24 vs 基座 49.86，单种子），他题参考在开思考下未测；他题参考含他题答案。子候选：IDEA-009。

### IDEA-009：TH 下 OPSD 的退化需要"本题信息"而非"同形上下文"——去答案等长的两种教师上下文，加认知通道的必要性与充分性检验

- 来源：`领域共性不足`（问题卡锚点"语义还是偏移"在真正退化的 TH 设置下未检验）+ `最高近邻不足`（2609.20612、OP²SD 的他题对照只在 DR 下做，且带他题答案）
- 父 Idea：`IDEA-008`
- 状态：`needs_revision`
- 定位关键词：on-policy self-distillation；privileged information；thinking models；epistemic tokens；forward KL
- 一句话背景：TH 训练让 OPSD 退化，但"本题信息 vs 上下文偏移"只在不退化的直接回答设置下回答过。
- 自评分：`8.0/10`
- 一段话概括：
  - 主张一（主）：I-own（本题 Full Trace 去答案截长）造成退化，I-other（他题 Full Trace 去答案、同长）不造成退化。两者格式、长度、是否含答案都相同，只差内容是否属于本题。
  - 主张二（次）：认知总量通道既不必要（T1 只用条件项仍退化）也不充分（T2 只用边际项、E 密度确实下降，但不退化）。设 M1、M2 两项操纵检查。
  - 判定表穷尽，含"去答案后退化消失 → 需要答案本身"一格。
  - 参考路径拉力降为描述量，与 DR 并列。
  - 实验为 8 个配置 × 3 个种子，约 280 A100 小时。
- Story line：
  - 明确失败：2609.20612 中 TH 训练的 OPSD 从 DR 的 82.62 降到 72.79（基座 80.21）；2607.05184 也发现训练开思考才有害。
  - 现状：语义 vs 偏移的对照（OP²SD、2609.20612）只在不退化的直接回答设置下做过，且他题参考带着他题答案；OP²SD 附录 H 开思考只有本题参考、单种子；认知抑制在 OPSD 中无因果检验。
  - 被忽视的关键：在真正退化的设置里，用去答案等长的两种上下文分开"本题信息"与"同形上下文"；用 DKD 式分解检验认知通道，重点放在不由构造决定的充分性一侧。
  - 预期：I-own 退化而 I-other 不退化，则支持"需要本题信息"；I-other 同样退化，则说明偏移即足够；去答案后退化消失，则说明答案本身是关键。
- 打分理由：
  - 直接回答问题卡锚点，并修掉 Call 2（他题答案混淆）与 Call 4（参考路径不可识别、由构造决定）的问题。
  - 每个结局都改变"该给 TH 学生的教师看什么"这一实践判断。
  - 风险：I-own 去掉答案段后可能不再退化；评测成本在测试切分上；分析型贡献。
- Idea 生成依据：2609.20612（表 11、讨论节、仓库控制脚本）；OP²SD 2608.09228（主结果与附录 H）；2607.05184（表 3、附录 E）；2603.24472 v4；DKD 2203.08679；2608.04794。
- 自评分轻量新意依据：OP²SD 自述他题参考在开思考下未测；2609.20612 的控制都在 DR 下；Call 1–4 四位 reviewer 均未报告 TH 下的语义 vs 偏移对照。需要 reviewer 检索。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：在真正发生退化的 TH-OPSD 中，用去答案等长的同形上下文干净地分离"本题信息"与"上下文偏移"，并对认知通道做因果的必要性与充分性检验。
- Baseline 可复现性：同 IDEA-007 表；去答案上下文用仓库 `data/controls/truncated_full_trace.py` 与 `length_matched_other_problem.py` 的规则生成，经 `--pi-override-file` 传入（2026-10-28 git show 核验）。
- Reviewer 记录：`Call 5（常规，effort high）：6.5/10，promising_needs_revision，最高近邻 2609.20612、OP²SD 2608.09228、2607.05184、AD-OPSD 2607.10805、Purified OPSD`。fatal："去答案"未实现——`truncated_full_trace.py` 只去掉拼接的 \boxed 后缀，Full Trace 正文本身推出答案，I-own 保留本题答案、I-other 带他题答案；另有措辞：2609.20612 未明说"机制未建立"，OP²SD 原话为 remains competitive。非阻断：T2 可能检验力不足；贡献偏增量（仓库控制从 DR 挪到 TH，加 DKD 迁移）。子候选：IDEA-010。

### IDEA-010：IDEA-009 的修正版——答案过滤的等长轨迹开头作上下文，T2 剂量匹配

- 来源：`领域共性不足` + `最高近邻不足`
- 父 Idea：`IDEA-009`
- 状态：`needs_revision`
- 定位关键词：同 IDEA-009
- 一句话背景：同 IDEA-009。
- 自评分：`8.0/10`
- 一段话概括：
  - Claim 不变。
  - I-own 与 I-other 改为取 Full Trace 的前 40% token（等长），并用仓库判分器过滤掉含本题或配对题答案的样本；保留率低于 60% 时降到 30%；各臂使用同一训练子集。完整含答案的轨迹作为第三个参照。
  - T2 用权重 w∈{1,10,100} 做剂量匹配：只按训练 rollout 上 E 密度的降幅不小于 T0u 来选 w。这样检验的是"同等幅度的认知抑制是否足以造成退化"。
  - 订正两处措辞：2609.20612 的原话；OP²SD 的 remains competitive。
- 打分理由：修掉 Call 5 唯一的 fatal，并回应充分性检验力的问题；增量性质不变。
- Idea 生成依据：同 IDEA-009；Call 5 审查。
- 自评分轻量新意依据：同 IDEA-009；Call 5 reviewer 独立检索确认 TH 下的语义 vs 偏移对照与类分解消融均未见先例。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：同 IDEA-009。
- Baseline 可复现性：同 IDEA-009。
- Reviewer 记录：`Call 6（常规，effort high）：7.5/10，promising_needs_revision，无 fatal，最高近邻 2609.20612、AD-OPSD 2607.10805、OP²SD 2608.09228、2607.05184、2608.18271`。意见：漏引同设置近邻 AD-OPSD 与 2608.18271；主张二缺 TH 下 fork_mask_mode 排除对照；主张一的 −1 分等价界在 3 个种子下功效不足；外部基准只用种子 0 却写进支持条件。新意判断：两项检验都无先例，主张一偏补 2609.20612 在 TH 下缺的格。子候选：IDEA-011。

### IDEA-011：IDEA-010 的边界收紧版

- 来源：`领域共性不足` + `最高近邻不足`
- 父 Idea：`IDEA-010`
- 状态：`needs_revision`
- 定位关键词：同 IDEA-009
- 一句话背景：同 IDEA-009。
- 自评分：`8.1/10`
- 一段话概括：Claim 与核心设计不变，改动如下：
  - 引入 AD-OPSD（同设置下按熵掩码）与 2608.18271，重新划定"认知通道没有按类的因果检验"这一边界。
  - 新增 T4，即 TH 下的 marker 位置排除，报告 T1 − T4，但不进判定。
  - 主张一的三臂各用 5 个种子；等价界 δ 取 T0u 降幅点估计的 25%，且不小于 1 分，在 I-other 评测前算定。
  - 外部基准只作描述，不进判定。
  - 规模为 33 次训练，约 355 A100 小时。
- 打分理由：Call 6 无 fatal，本版逐条回应全部非阻断意见；增量性质不变。
- Idea 生成依据：同 IDEA-009；2608.18271（摘要）；Call 6 审查。
- 自评分轻量新意依据：同 IDEA-010。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：同 IDEA-009。
- Baseline 可复现性：同 IDEA-009，另加 T4（`--fork-mask-mode exclude`，2026-10-28 核验存在于 `train_opsd.py`）。
- Reviewer 记录：`Call 7（常规，effort high）：8.2/10，experiment_ready，无 fatal，最高近邻 2609.20612、OP²SD 2608.09228、2608.04794、2607.05184、AD-OPSD 2607.10805`。首轮通过，待复核。非阻断：应纳入 2608.04794 在 think 模式下的结果（不含答案的 hint/skill 形式 PI 降 −5.13/−3.46，整段解答 −0.28），与 ΔI-own 预期相关；主张二"不充分"的等价判定在 3 个种子、1 分界下功效偏弱；统计口径"跨 3 个种子"与主张一的 5 个种子不一致；未能核验 2607.05184 附录 E 的 0.00928→0.00853。；`Call 8（复核，xhigh 角色；harness 无法设置推理强度，按默认运行）：6.0/10，promising_needs_revision，最高近邻 2609.39118、2609.20612、2607.05184、AD-OPSD、OP²SD`。fatal：前提"TH 下语义 vs 偏移从未检验"不成立，2609.39118 表 4 在 Th/Th、上限 1,024 下有 Unrelated solution 对照。改进者核对原文：OLMo-3-7B-Think 无关 −6.0、完整 −4.7、答案 −7.4，三者相当，作者读作前缀分布效应；Qwen3-1.7B 在其设置下（lr 1e-6）各臂均不退化；单种子，无关解答带自己的答案、未匹配长度。复核未通过。子候选：IDEA-012。

### IDEA-012：OPSD 的 TH 退化不经由认知通道（主），且偏移即足够（次）——按 2609.39118 重新定位

- 来源：`领域共性不足` + `最高近邻不足`
- 父 Idea：`IDEA-011`
- 状态：`selected`
- 定位关键词：同 IDEA-009
- 一句话背景：TH 训练让 OPSD 退化。领域主流用认知抑制来解释，但它在 OPSD 中从未经过因果检验；语义 vs 偏移在 TH 下只有单种子、带混淆的初步证据（2609.39118）。
- 自评分：`7.9/10`
- 一段话概括：
  - 主张一（主）：认知通道既不必要（T1 仍退化）也不充分（剂量匹配的 T2 不退化）。设 M1、M2 检查、随机类对照，另报告 T1 − T4。
  - 主张二（次）：在确认退化的 Qwen3-1.7B 配置下，本题开头与他题开头（等长、双方都不含答案）造成相当的退化，CI 落在 ±δ 内。这一方向与 2609.39118 的 OLMo 结果一致；本 Idea 补上多种子、等长、无答案三点，从而排除"他题答案误导"这一混淆。
  - 背景中补入 2609.39118 表 4 的数字、Qwen3-1.7B 在其配置下不退化的事实，以及 2608.04794 的 think 模式结果。
- 打分理由：首审 8.2 的设计基本保留，修掉复核唯一的 fatal（漏掉 TH 下已有的无关解答对照）。主张一的新意由多位 reviewer 确认；主张二降为干净复核，增量有限。
- Idea 生成依据：同 IDEA-011；2609.39118 表 4、表 9（来自问题卡 Q001，本次读全文核对）；2608.04794（think 模式结果）。
- 自评分轻量新意依据：Call 3–8 的 reviewer 都未检索到 OPSD 中按认知类的单项消融；2609.39118 的对照单种子且带混淆。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：首次在退化的 TH-OPSD 中对认知抑制假说做按类的必要性与充分性因果检验，并在确认退化的配置下干净复核"偏移即足够"。
- Baseline 可复现性：同 IDEA-011。
- Reviewer 记录：`尚未送审`
