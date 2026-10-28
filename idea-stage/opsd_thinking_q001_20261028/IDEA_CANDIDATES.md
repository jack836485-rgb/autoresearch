# Idea 候选池

> 本文件由 idea improver 持续维护。保留所有进入过比较的实质性候选及其演化关系；不要把完整 proposal 写进这里。

- 输入模式：`problem_card`
- 输入论文：不适用
- 输入问题卡：`path-stage/LLM新兴领域研究地图_20261021`，Q001

## 当前选择

- Reviewer 调用：`1 / 20`
- 当前选中 Idea：`IDEA-006`
- 当前自评分：`7.7/10`
- 选择理由：IDEA-005 首审 5.5（方向律接近同义反复；2609.20612 已有训练前 correction pressure，且 marker 抑制不区分 DR/TH 两种结局）。IDEA-006 改为在真正退化的 TH 设置中拆开 2609.20612 自述未分开的混杂（模式/监督段/教师信息），是池中自评最高的 available 候选。
- 状态：`等待第 2 次 reviewer 调用`

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
- 状态：`selected`
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

- Reviewer 记录：`尚未送审`
