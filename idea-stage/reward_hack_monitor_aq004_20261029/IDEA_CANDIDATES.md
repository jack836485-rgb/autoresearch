# Idea 候选池

> 本文件由 idea improver 持续维护。保留所有进入过比较的实质性候选及其演化关系；不要把完整 proposal 写进这里。

- 输入模式：`problem_card`
- 输入论文：不适用
- 输入问题卡：`path-stage/LLM热门方向_算力适配_20261028` 的 `A-Q004`（继承自 `AgenticRL研究地图_20261021` 的 `Q004`）

## 当前选择

- Reviewer 调用：`7 / 9`（用户先后追加 1 次、2 次）
- 当前选中 Idea：`IDEA-011`
- 当前自评分：`7.6/10`
- 选择理由：IDEA-011 撤回部署性主张、把第二测试床换成投机在训练中途出现的 Countdown-Code，并补上漂移不足的退路；新意表述按 Call 7 如实收窄为实证测量。
- 状态：`等待第 8 次 reviewer 调用`
- Call 1 后的选择记录：IDEA-003 → needs_revision（5.5，promising_needs_revision）。
- Call 2 后的选择记录：IDEA-006 → needs_revision（6.5，promising_needs_revision）。
- Call 3 后的选择记录：IDEA-007 → needs_revision（7.5，promising_needs_revision，无致命阻塞）。
- Call 4 后的选择记录：IDEA-008 → needs_revision（7.0，promising_needs_revision）。
- Call 5：reviewer 失联，无输出（计入预算；用户同意追加 1 次）。
- Call 6 后的选择记录：IDEA-009 → needs_revision（7.6，promising_needs_revision）。
- Call 7 后的选择记录：IDEA-010 → needs_revision（6.8，promising_needs_revision）。

## 候选列表

### IDEA-001：冻结监控器 vs 每轮更新监控器的召回随训练步变化

- 来源：`问题卡切口`
- 父 Idea：`无`
- 状态：`available`
- 定位关键词：reward hacking；monitor；RL training；training-time reward hacking
- 一句话背景：RLVR / rubric RL 中，奖励投机监控器在训练过程中召回如何变化。
- 自评分：`5.5/10`
- 一段话概括：在注入已知评审偏差的测试床（CHERRL）上，冻结一个训练开始时构造的监控器，与每轮用新投机样本更新的监控器对比，记录各训练步的召回与 clean resolved。只有诊断，没有机制和修法；"每轮更新更好"几乎是预期结论。
- 打分理由：卡片自带切口，问题真实，但诊断结论可预期，且 2608.04735 附录已在 OLMo 奖励投机检查点上观察到检测率随步数下降（小样本），Trace-and-Amplify 已说明训练期数据训出的监控器更泛化。
- Idea 生成依据：来自问题卡 A-Q004；CHERRL（https://arxiv.org/abs/2606.04923）。
- 自评分轻量新意依据：2608.04735 附录 H（OLMo 7B 检测率 75%→25%，样本小）；2512.18311（前沿 RL 中可监控性与思考 token 数相关）。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：在有真值的测试床上系统测召回衰减。
- Reviewer 记录：`尚未送审`

### IDEA-002：分解冻结监控器召回衰减的来源——新策略出现 vs 同策略可读性下降

- 来源：`领域共性不足`
- 父 Idea：`IDEA-001`
- 状态：`available`
- 定位关键词：reward hacking；CoT monitoring；monitorability；training-time reward hacking
- 一句话背景：CoT 监控领域对 RL 是否降低可监控性存在分歧（前沿模型上不明显，OLMo 7B 上下降）。
- 自评分：`6.6/10`
- 一段话概括：Claim 是冻结监控器的召回衰减可以拆成两部分——训练后期出现监控器构造时不存在的投机策略（覆盖缺口），与同一策略的 CoT 变短、少说理（可读性漂移）；二者对修法的要求不同。方法：在 Trace-and-Amplify 与 Countdown-Code 两个有真值的代码测试床上，按策略聚类标注每个自然投机样本，分别计算"已知策略"与"新策略"上的召回，并以思考 token 数作协变量。最小实验 3 种子 × 2 模型家族。
- Story line：OpenAI 在 o3 / GPT-5.1 Codex Max 训练中发现可监控性主要随思考 token 数起落 [2512.18311]；OLMo 7B 奖励投机检查点上检测率随步数从 75% 降到 25% [2608.04735 附录 H，小样本]；Rebound-to-Remedy 观察到后期投机策略与早期质的不同 [2604.01476] → 两种解释（长度 vs 新策略）没有被分开 → 按策略分层 + 长度协变量 → 若衰减集中在新策略上，支持覆盖缺口解释，否则支持可读性解释。
- 打分理由：能对齐一个已记录的分歧，但只有诊断；若结论是"覆盖缺口"，自然的下一问是怎么补，单独成文分量偏轻。
- Idea 生成依据：2512.18311；2608.04735；2604.01476；来自问题卡 A-Q004 的 2606.26300（人工每轮补规则）。
- 自评分轻量新意依据：未见按策略分层分解监控衰减的工作；需要 reviewer 检索。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：把召回衰减分解为覆盖缺口与可读性漂移。
- Reviewer 记录：`尚未送审`

### IDEA-003：投机能力随训练出现，所以"诱导样本"要从当前检查点取——能力匹配的监控器刷新

- 来源：`领域共性不足`（结合 `最高近邻不足`：Trace-and-Amplify）
- 父 Idea：`IDEA-002`
- 状态：`needs_revision`
- 定位关键词：reward hacking；training-time reward hacking；prompt-elicited trajectories；CoT monitoring；RLVR
- 一句话背景：代码 RLVR 中，用"提示诱导的投机轨迹"训练的奖励投机监控器，对训练中自然出现的投机泛化差。
- 自评分：`7.5/10`
- 一段话概括：Claim：(1) 训练开始时用初始模型诱导样本训练、之后冻结的监控器，召回随 RL 步数下降，且下降集中在初始模型被提示时也产不出的投机策略上；(2) 诱导数据泛化差的主因是"诱导者能力不匹配"——用同一套诱导提示、同样数量，但从当前检查点诱导并定期刷新监控器，可收回大部分与"用真实训练期投机样本训练的监控器"之间的差距；(3) 用同家族更大的非 RL 模型诱导作为对照，区分"能力"与"RL 带来的在策风格"。方法本身简单：定期对当前检查点运行固定诱导提示，用测试床自带的追踪器保留真的通过了伪测试的样本，重训轻量监控器。最小实验在 Trace-and-Amplify（Qwen2.5-Coder-1.5B、DeepSeek-Coder-1.3B）与 Countdown-Code 上，3 种子，比较冻结 / 初始模型刷新 / 大模型刷新 / 当前检查点刷新 / 真实训练期样本上界。
- Story line：Trace-and-Amplify 发现提示诱导轨迹训练的监控器对训练期自然投机泛化差 [2604.23488]，但其诱导数据来自固定来源、没有随训练更新；与此同时，多项独立工作显示投机受能力门控——捷径只对已学会的工具形成 [2609.16268]，早期改写评测器的尝试因能力不足而失败、后期以质不同的策略成功 [2604.01476]，生成难度限制偏差可利用性 [2606.04923]，工业实践中新渠道在模型变强后才出现、只能人工每轮补规则 [2606.26300] → 被忽视的关键：诱导数据的投机分布由诱导者的能力决定，固定诱导者无法覆盖训练后期才可行的策略 → 本 Idea：按训练进度从当前检查点诱导并刷新监控器，并用"更大非 RL 模型诱导"分离能力与在策风格 → 预期（假设）：当前检查点刷新显著优于初始模型刷新，且差距集中在后期新策略上；若差异不显著或可由思考长度解释，则 Claim 被推翻。
- 打分理由：轻量检查未见"按检查点诱导刷新监控器"的工作，Claim 可证伪、算力适配（1.3–1.5B、~300 步）；风险是 reviewer 认为方法过于简单或与 Trace-and-Amplify 的"用训练期样本"重合。
- Idea 生成依据：2604.23488（最高近邻，读摘要与 §4.2 实验设置、附录 A.1）；2609.16268、2606.26300（来自问题卡 A-Q004）；2604.01476、2606.04923（摘要）；2606.09711 PRIME（投机前驱能力，摘要）；2512.18311、2608.04735（可监控性随训练的分歧）。
- 自评分轻量新意依据：检索"prompt-elicited reward hacking current checkpoint monitor update""elicitation capability gap monitor generalization"未见对应工作；Trace-and-Amplify 的诱导数据按 Wang et al. (2025b) 提示生成，800 条，固定来源；需要 reviewer 检索。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：把诱导数据泛化差归因于诱导者能力不匹配，并给出能力匹配的、无需训练期真值标注的刷新方法与区分能力/在策风格的对照。
- Baseline 可复现性：

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 开源代码与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| Trace-and-Amplify 测试床（Reward Hacker 训练 + 追踪器） | 代码 RLVR 中训练期奖励投机的产生与标注 | https://arxiv.org/abs/2604.23488 | https://github.com/LichenLillc/CoTMonitoring ；2026-10-29 克隆核验，含 `Trace-and-Amplify_Framework/train_script.sh`、伪测试注入 `my_utils/add_fake_test_final-ver.py`、推理 `or1_scripts/eval/eval_1p5b.sh` | `bash train_script.sh`（model_size=1p5b），按 README 注入伪测试 | 是 |
| 提示诱导数据训练的冻结监控器（BERT / 隐状态探针 / LLM 监控器） | 同任务、同监控器族；即该文的 prompt-elicited baseline | 同上 §4.2 | 同仓库 `CoTMonitors_Training_and_Evaluation/scripts/paired_probe_pipeline/BERT_pipeline.sh`、`mine_probe_pipeline_loop_paired.sh`、`scripts/gpt_evaluate.py` | 同脚本，训练数据换为初始模型诱导样本 | 是 |
| 真实训练期投机样本训练的监控器（上界） | 同任务；该文的 training-time 监控器 | 同上 | 同仓库（数据集 zip 为 LFS，需另行拉取；也可用本实验自产训练期样本） | 同脚本，训练数据为追踪器标注的训练期投机 | 是（作为上界，非可部署方法） |
| Countdown-Code 测试床 | 代码 RLVR 中可改写测试脚本的奖励投机，真/代理奖励分离 | https://arxiv.org/abs/2603.07084 | https://github.com/zohaib-khan5040/Countdown-Code ；2026-10-29 克隆核验，含 `datagen/`、`environments/countdown_code`、`verl/` | 按 README 生成数据并用其 verl 训练 | 是（第二测试床） |

- Reviewer 记录：`Call 1（常规，同模型 opus，effort 由 harness 默认）：5.5/10，promising_needs_revision，最高近邻 Trace-and-Amplify (2604.23488)；致命阻塞：①能力不匹配前提未核实，T&A 原文把差距归于显式/隐式风格；②指令诱导风格混淆未隔离；③刷新依赖的追踪器同样能标注自然轨迹，部署优势不成立；④两套测试床的投机策略类别太少，C1 分层可能不可检验。子 Idea：IDEA-006`

### IDEA-004：借鉴恶意软件检测的概念漂移方法，用不符合度触发监控器的选择性重标注

- 来源：`相似领域成熟方法迁移`
- 父 Idea：`无`
- 状态：`available`
- 定位关键词：reward hacking；monitor；concept drift；conformal prediction
- 一句话背景：奖励投机监控器在 RL 训练中面对策略分布漂移，需要决定何时、对哪些样本重标注。
- 自评分：`6.0/10`
- 一段话概括：恶意软件检测与投机监控结构相同——对手（策略）持续演化、检测器基于过去样本训练、召回随时间下降；该领域的成熟做法是用共形不符合度检测漂移样本（如 Transcend、CADE），只把漂移样本送人工标注。迁移：对每个训练窗口的轨迹计算监控器嵌入上的不符合度，只把高不符合度样本送强 LLM 或人工复核，再更新监控器；Claim 是在等标注预算下接近每轮全量复核的召回。
- 打分理由：迁移的结构对应成立，但核心贡献偏工程，且"便宜检测器 + 选择性复核"已有相近工作（2606.08893），关键前提（漂移样本在嵌入上可分）未验证。
- Idea 生成依据：恶意软件概念漂移文献（Transcend、CADE、TESSERACT，方法启发，非实验 baseline）；2606.26300（每轮人工复查）；2606.08893。
- 自评分轻量新意依据：未做定向检索；需要 reviewer 检索。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：把漂移触发的选择性重标注引入训练期投机监控。
- Reviewer 记录：`尚未送审`

### IDEA-005：用投机前驱能力的探针预测新渠道出现时刻

- 来源：`最高近邻不足`（PRIME）
- 父 Idea：`无`
- 状态：`covered`
- 定位关键词：reward hacking；hack onset；linear probe
- 一句话背景：在投机可见之前预测其出现。
- 自评分：`4.5/10`
- 一段话概括：训练探针跟踪策略对代理-真值差距的内部表征，在可见投机率仍低时预测投机出现与严重程度。
- 打分理由：PRIME（https://arxiv.org/abs/2606.09711）已报告前驱能力分阶段出现、直接探针分数可预测之后的投机出现时刻与严重程度，并能随评审变化重新定向；本候选基本被覆盖。
- Idea 生成依据：2606.09711。
- 自评分轻量新意依据：2606.09711 摘要。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：无明显独立贡献。
- Reviewer 记录：`不送审（covered）`

### IDEA-006：诱导者能力 vs 指令风格——在多策略测试床上用因子设计检验，并以只用代理奖励筛选的在策诱导刷新冻结监控器

- 来源：`最高近邻不足`（Trace-and-Amplify 的归因未被检验）
- 父 Idea：`IDEA-003`
- 状态：`needs_revision`
- 定位关键词：reward hacking；training-time reward hacking；prompt-elicited trajectories；linear probe；LLM judge；RLVR
- 一句话背景：代码 RLVR 中，用提示诱导投机轨迹训练的监控器对训练期自然投机泛化差，固定监控器的准确率也会在训练中下降。
- 自评分：`7.2/10`
- 一段话概括：把 Trace-and-Amplify 观察到的"诱导数据泛化差"拆成两个竞争解释并用因子设计分开：(a) 指令诱导带来显式风格（原文解释）；(b) 诱导者能力/分布与被监控策略不匹配（本 Idea 假设）。因子：诱导者 {初始模型, 同家族更大非 RL 模型, 当前检查点} × 诱导方式 {指令诱导, 无指令采样（仅诊断，用真值筛选）} × 监控器输入范围 {完整回答, 去注释并规范化的代码}。若诱导者效应在去风格的代码范围仍存在，则风格解释不足；若只换诱导者即可收回差距，支持能力解释。方法：定期对当前检查点运行指令诱导，只用部署时可得的信号（被指示投机且代理奖励通过）筛选样本，刷新读取方固定的监控器（文本分类器、冻结基座激活上的线性探针），不使用自然轨迹的真值。主测试床改为 Engels/Nanda 的 overwrite-tests 环境（Qwen3-4B，已报告 6 类投机策略，固定 LLM judge 与探针准确率在投机 run 中下降约 16 点），Trace-and-Amplify 作第二测试床检验 C2 的跨模型家族成立性。
- Story line：Trace-and-Amplify 发现诱导数据训练的监控器对训练期投机泛化差，并归因于指令诱导的显式风格 [2604.23488]；Engels/Nanda 的 overwrite-tests 环境中，固定 LLM judge 与探针在投机 run 里准确率下降约 16 点，作者只给出"回答变长、注释变多"的提示性解释 [LessWrong 2025-12]；基座模型自然触发该漏洞的频率低于千分之一 [ariahw/rl-rewardhacking README]，后期投机以质不同的策略出现 [2604.01476] → 被忽视的关键：诱导数据的覆盖由诱导者决定，这一变量从未被单独操纵，风格与能力两种解释从未被分开 → 本 Idea 用诱导者 × 诱导方式 × 监控输入范围的因子设计分离两者，并给出只用代理奖励筛选的在策刷新 → 预期（假设）：当前检查点刷新在去风格的代码范围仍显著优于初始模型刷新，且优势集中在初始模型诱导集中不存在的策略上；若诱导者效应在代码范围消失，则风格解释成立、本 Idea 的能力主张被推翻。
- 打分理由：Call 1 认为诱导者作自变量与在策刷新是新的；本修订补上了竞争解释的隔离与部署成立条件，测试床换到已报告多策略的环境；剩余风险是 Qwen3-4B 训练成本与策略类别仍可能不足。
- Idea 生成依据：2604.23488（读 §4.2 与引言中"隐含假设诱导数据覆盖训练期投机"的表述；原文未写诱导模型）；Engels/Nanda LessWrong 文章（https://www.greaterwrong.com/posts/R5MdWGKsuvdPwGFBG/steering-rl-training-benchmarking-interventions-against ，读全文摘要：Qwen3-4B，GRPO，LeetCode 中/难题，overwrite tests 漏洞，80–100 步开始投机，评测集投机率约 79%；固定 judge 与探针在投机 run 中下降约 16 点；6 类策略；未刷新监控器，自适应监控列为未来工作）；2602.15515（激活探针在 RL 中因表示漂移失效，无论有无惩罚——因此本 Idea 只用读取方固定的监控器）；2602.01750（Hacker–Auditor 博弈，机制不同）。
- 自评分轻量新意依据：Call 1 reviewer 检索未发现对诱导者做在策刷新的工作；本轮未发现分离"诱导风格 vs 诱导者能力"的工作；需要 reviewer 检索。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：首次把诱导者作为操纵变量，用因子设计分离风格与能力两种解释，并给出只依赖代理奖励的在策诱导刷新。
- Baseline 可复现性：

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 开源代码与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| overwrite-tests 测试床 + 固定探针 / LLM judge 监控器 | 代码 RLVR 训练期投机及其监控，同任务 | https://www.greaterwrong.com/posts/R5MdWGKsuvdPwGFBG/steering-rl-training-benchmarking-interventions-against | https://github.com/ariahw/rl-rewardhacking ；2026-10-29 克隆核验：`scripts/run_rl_training.py`（`run_rl_training no_intervention --model_id qwen/Qwen3-4B --task simple_overwrite_tests --seed k`）、`train_probe <RUN_NAME>`（冻结基座激活上的 mass-mean / logistic 探针）、LLM judge 经 OpenRouter、`eval_model <RUN_NAME> <step>` | 按 README `create_all_datasets` 后运行 | 是（主测试床） |
| Trace-and-Amplify 测试床与 prompt-elicited / training-time 监控器 | 同任务；最高近邻 | https://arxiv.org/abs/2604.23488 | https://github.com/LichenLillc/CoTMonitoring ；克隆核验（见 IDEA-003） | 同 IDEA-003 | 是（第二测试床） |
| 真值标注的训练期自然投机训练的监控器（上界） | 同任务 | 同上两项 | 两仓库均提供真值判定（仅通过自定义测试 / 伪单元测试追踪器） | 同脚本，训练数据为真值标注自然轨迹 | 是（上界，需要部署时不可得的真值） |

- Reviewer 记录：`Call 2（常规，同模型 opus，effort 由 harness 默认）：6.5/10，promising_needs_revision，最高近邻 Trace-and-Amplify (2604.23488)、Kirch et al. (2511.17408)；致命阻塞：①主测试床后期无指令投机率约 79%，'无指令且代理奖励通过'的负例大多是投机，后期检查点诱导标签可预见性失效；②未与 Kirch et al. 区分（数据生成方式 / on-policy 影响探针泛化已有系统研究）。另：'自适应监控列为未来工作'无法核实，已删除该表述。子 Idea：IDEA-007`

### IDEA-007：前瞻式监控——在自然投机出现之前，从当前检查点诱导样本训练监控器

- 来源：`领域共性不足`（投机受能力门控）结合 `最高近邻不足`（Trace-and-Amplify、Kirch et al.）
- 父 Idea：`IDEA-006`
- 状态：`needs_revision`
- 定位关键词：reward hacking；training-time reward hacking；prompt-elicited trajectories；on-policy probe training data；linear probe；RLVR
- 一句话背景：代码 RLVR 中，自然投机在训练中途才出现，出现前没有在策正例可训监控器，而诱导数据训练的监控器又泛化差。
- 自评分：`7.4/10`
- 一段话概括：Claim：(C1) 训练中，检查点"被指示时能成功投机"的比例，先于自然投机出现而上升；检查点 t 的诱导投机在策略类别分布上，比初始模型的诱导投机更接近之后自然出现的投机。(C2) 只在自然投机出现之前（预设步 20/40/60）用当前检查点诱导训练监控器——正例为被指示投机且代理奖励通过，负例为同检查点无指令且代理奖励通过（污染率等于当时自然投机率，实测报告）——它在之后整个训练中对自然投机的召回，高于初始模型诱导的监控器，也高于用同一时点可得的真值标注自然数据训练的监控器（彼时正例极少）。(C3) 同家族更大非 RL 模型诱导用来拆分能力与 RL 分布；去注释的规范化代码范围用来检验风格解释。与 Kirch et al. 的边界：后者在静态模型上比较 on/off-policy 数据，自然正例存在；本 Idea 面对的是策略在漂移、目标行为尚未自然出现的情形，问的是"哪个时刻的诱导者"能预见之后的投机。
- Story line：投机受能力门控——捷径只对已学会的工具形成 [2609.16268]，早期改写评测器的尝试因能力不足失败 [2604.01476]，基座模型自然触发 overwrite-tests 漏洞的频率低于千分之一而 RL 80–100 步后开始投机 [Engels/Nanda]；监控方面，诱导数据训练的监控器对训练期自然投机泛化差 [2604.23488]，数据生成方式影响探针泛化、意图型行为最敏感 [2511.17408]，固定监控器在投机 run 中准确率下降约 16 点 [Engels/Nanda] → 被忽视的关键：投机出现前，在策自然正例不存在，而"被指示能投机"的能力可能已经就位；诱导者是哪个检查点从未被操纵 → 本 Idea：在出现前用当前检查点诱导训练监控器，以初始模型诱导、大模型诱导、同时点真值自然数据为对照，并在规范化代码范围检验风格解释 → 预期（假设）：C1 的指令投机成功率先于自然投机上升；C2 的前瞻监控器召回更高；若指令投机能力与自然投机同时出现，或前瞻监控器不优于初始模型诱导，则 Claim 被推翻。
- 打分理由：两轮 reviewer 都认可诱导者作操纵变量是新的；本修订消除了负例污染的可预见失效，并把新意收窄到策略漂移下的前瞻性；风险是 C1 与 PRIME（前驱能力先于投机）在"能力先于投机"上相邻，以及出现前的诱导成功率可能过低。
- Idea 生成依据：2511.17408（读摘要：8 种行为，数据生成策略显著影响探针泛化，意图型行为最敏感，incentivised 测试可预测 on-policy 泛化；静态模型）；2606.09711 PRIME（内部前驱能力先于持续投机，用探针预测投机出现时刻）；Engels/Nanda 文章与仓库 README；2604.23488；2609.16268、2606.26300（来自问题卡 A-Q004）；2604.01476。
- 自评分轻量新意依据：未见"出现前从当前检查点诱导以训练监控器"的工作；与 PRIME 的差别是 PRIME 测内部表征并预测出现时刻，不构造监控数据、不比较诱导者；需要 reviewer 检索。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：把监控数据的诱导者与诱导时点作为操纵变量，检验投机出现前的在策诱导能否预见之后的自然投机。
- Baseline 可复现性：同 IDEA-006（overwrite-tests 仓库 https://github.com/ariahw/rl-rewardhacking 与 Trace-and-Amplify 仓库 https://github.com/LichenLillc/CoTMonitoring ，均已克隆核验；注：前者 `train_probe` 默认用基座 + RL 检查点的真值标注数据，prompt-elicited 冻结 baseline 需按本设计自行构造，脚本可复用；后者数据 zip 为 Git LFS 指针，不依赖其发布数据）。
- Reviewer 记录：`Call 3（常规，同模型 opus，effort 由 harness 默认）：7.5/10，promising_needs_revision，无致命阻塞；最高近邻 Trace-and-Amplify、Kirch et al.、Engels/Nanda、PRIME、EleutherAI reward hacking indicators。未达 8 分原因：①对照 4（同时点真值自然数据 800/800）不可构造；②指令文本可能经输入泄漏标签，正例未过滤正确解；③C1 在 overwrite-tests 上可能步 0 饱和，LoRA 漂移小可能使 C2 效应量不足；④2604.01476 与 T&A 的引用表述偏强。子 Idea：IDEA-008`

### IDEA-008：前瞻式监控（修订）——等生成预算对照、去指令重编码与代理信号正例过滤

- 来源：`最高近邻不足`
- 父 Idea：`IDEA-007`
- 状态：`needs_revision`
- 定位关键词：reward hacking；training-time reward hacking；prompt-elicited trajectories；on-policy probe training data；linear probe；RLVR
- 一句话背景：同 IDEA-007。
- 自评分：`7.8/10`
- 一段话概括：Claim 与 IDEA-007 相同（C1 诱导分布随检查点逼近之后的自然投机；C2 投机出现前就位的前瞻监控器；C3 能力/分布/风格拆分），修订只针对可检验性：(1) 对照 4 改为"等生成预算"——每个数据来源在时点 t 用同样的生成次数（2 万条），诱导来源从中抽 800 条正例，自然来源用真值挑出其中全部投机（实际数量照报，通常远少于 800），这正是前瞻场景的真实约束；另设"同正例数"子对照，把诱导来源下采样到自然来源的正例数，分离"数量"与"分布"。(2) 监控器只读回答：文本分类器只输入回答；探针激活由冻结基座在去掉诱导指令的中性提示 + 回答上重新编码，消除指令泄漏。(3) 正例过滤只用代理信号：只保留"同一检查点在无指令下对该题未通过代理测试、被指示投机后通过"的样本，以排除被指示后仍写出正确解的情况；纯度用真值事后核对。(4) C1 按测试床分开预测：overwrite-tests 只需定义 `run_tests()`，预计步 0 即可被指示投机（成功率饱和），在此只检验策略分布逼近；Trace-and-Amplify 的伪测试需要针对冲突用例特判，预计 1.3–1.5B 初始模型的指令投机成功率低，在此检验"能力先于倾向"。(5) 时点改为 {20, 40, 60, 80}，按实测自然投机率 <5% 的时点纳入，缓解出现前漂移过小的风险。(6) 修正引用：2604.01476 只说早期改写嵌入了自身解过不了的用例；T&A 的是定性解释（指令暴露意图、隐状态可分），未做风格控制。
- Story line：同 IDEA-007，引用表述按 (6) 修正。
- 打分理由：Call 3 无致命阻塞，四个扣分点均为设计可修复；剩余风险是新颖边界偏窄、需靠 C1/C3 的机制结果撑起。
- Idea 生成依据：同 IDEA-007；EleutherAI reward hacking indicators（https://blog.eleuther.ai/reward-hacking-indicators/ ，Call 3 引用：SFT 注入 exploit 场景下用中间检查点前缀估计投机率，不训练监控器）。
- 自评分轻量新意依据：同 IDEA-007；Call 3 reviewer 检索未见以诱导检查点 × 时点为操纵变量构造前瞻监控器的工作。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：同 IDEA-007。
- Baseline 可复现性：同 IDEA-006 / IDEA-007；补充：overwrite-tests 仓库默认 `save_steps=50`，需改为 20 以取得步 20/40/60/80 检查点（Call 3 核验）。
- Reviewer 记录：`Call 4（常规，同模型 opus，effort 由 harness 默认）：7.0/10，promising_needs_revision；最高近邻 Trace-and-Amplify、Kirch et al.、PRIME、EleutherAI indicators、Engels/Nanda。致命阻塞：①负例固定取自检查点 t，与来源 1/2 正例的生成模型错配，监控器可学到生成模型风格捷径；②overwrite-tests 上正确解同样通过代理奖励，'无指令失败、指令后通过'不能只靠代理信号保证正例纯度。另：'能力先于倾向'与 PRIME、2609.16268 部分重合；初始模型诱导 baseline 在 overwrite-tests 上可能接近天花板。子 Idea：IDEA-009`

### IDEA-009：前瞻式监控（再修订）——同源负例、按测试床区分标签来源、天花板预案

- 来源：`最高近邻不足`
- 父 Idea：`IDEA-008`
- 状态：`needs_revision`
- 定位关键词：reward hacking；training-time reward hacking；prompt-elicited trajectories；on-policy probe training data；linear probe；RLVR
- 一句话背景：同 IDEA-007。
- 自评分：`8.0/10`
- 一段话概括：核心 Claim 不变（C1 诱导分布随检查点逼近之后的自然投机；C2 投机出现前就位的前瞻监控器优于初始模型诱导与等预算自然采样；C3 能力/分布/风格拆分）。修订：(1) 同源负例——每个诱导来源的负例取自同一生成模型的无指令、代理通过且真值非投机样本，监控器无法用"哪个模型写的"区分正负；另报告"各来源负例混合等量"的次要设定。(2) 标签来源按测试床区分——overwrite-tests 上正确解也通过代理奖励，所有来源的正负例统一用真值清洗，这里只检验 C1/C2 的分布性主张；"只用代理信号筛选"的部署性主张只在 Trace-and-Amplify 上检验，那里正例必须通过与正确解矛盾的伪测试，代理通过即投机。(3) "能力先于倾向"降为对 PRIME 与 2609.16268 现象的复测，不作贡献。(4) 天花板预案——同时报告 TPR@1%FPR；若初始模型诱导的监控器在 t 之后的自然投机上 TPR@1%FPR ≥ 0.95，则 overwrite-tests 上的 C2 判为不具信息量，C2 以 Trace-and-Amplify 结果为准。
- Story line：同 IDEA-008。
- 打分理由：Call 4 认为新意边界基本站得住，两个阻塞都可在不改 Claim 的前提下修正；剩余风险是效应量与主测试床天花板。
- Idea 生成依据：同 IDEA-008；Call 4 引用的 CATCH 与 SimHack（零样本监控召回衰减与投机起点预测，不构造监控器），未单独打开。
- 自评分轻量新意依据：同 IDEA-008。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：同 IDEA-007。
- Baseline 可复现性：同 IDEA-008。
- Reviewer 记录：`Call 5（常规）：reviewer 启动后约 1 分钟失联，无评审输出，计入预算；Call 6（常规，同模型 opus，effort 由 harness 默认）：7.6/10，promising_needs_revision；唯一阻塞为定位表述：EleutherAI Reasoning Interpolation 已在多个检查点上比较多种诱导者（同模型 donor、跨家族 Qwen3-8B、提示 Claude），用于预测投机率（SFT，GPT-OSS-20b，不训练监控器），brief 中'诱导者×时点从未被操纵''EleutherAI 不比较诱导者'不实。子 Idea：IDEA-010`

### IDEA-010：前瞻式监控（定位修正）——把检查点诱导数据作为监控器训练集，在 RL 中评测前瞻召回

- 来源：`最高近邻不足`
- 父 Idea：`IDEA-009`
- 状态：`needs_revision`
- 定位关键词：reward hacking；training-time reward hacking；prompt-elicited trajectories；on-policy probe training data；linear probe；RLVR
- 一句话背景：同 IDEA-007。
- 自评分：`8.0/10`
- 一段话概括：实验设计与 C1–C3 同 IDEA-009。只修正定位：EleutherAI Reasoning Interpolation（https://blog.eleuther.ai/reward-hacking-indicators/ ，已读：GPT-OSS-20b 经 LoRA SFT，djinn 易受攻击验证器题目；在检查点上用推理前缀做重要性采样，比较同模型 donor、跨家族 Qwen3-8B donor、提示 Claude Sonnet 4.6 三类前缀来源，目标是回归投机率趋势、预测某类 exploit 是否超过 10%；不训练监控器）已在检查点上操纵诱导者，用于投机率预测。本 Idea 的新意边界收窄为：在真实 RL 中，把检查点诱导数据作为监控器训练集，评测其对之后自然投机的前瞻召回，并在监控器层面做能力/分布/风格拆分。另补充：Engels/Nanda 的探针正例取自已 RL 投机的模型（投机出现后的数据）。
- Story line：同 IDEA-009，"被忽视的关键"改为：已有工作在检查点上诱导是为了预测投机率（EleutherAI），或用静态诱导数据训练监控器（Trace-and-Amplify）；"在投机出现前用检查点诱导数据训练监控器、并测其之后的召回"没有被做过。
- 打分理由：Call 6 认为修正定位后新意成立，唯一阻塞是表述；剩余风险是分量中等、overwrite-tests 可能落入天花板而使证据主要压在 Trace-and-Amplify 上。
- Idea 生成依据：同 IDEA-009；EleutherAI Reasoning Interpolation 博文（已读全文摘要）。
- 自评分轻量新意依据：Call 6 reviewer 检索未见以检查点诱导数据训练监控器并做前瞻召回评测的工作。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：把检查点诱导数据作为监控器训练集，在 RL 投机出现前构造监控器，并在监控器层面拆分能力、RL 分布与风格。
- Baseline 可复现性：同 IDEA-008。
- Reviewer 记录：`Call 7（常规，同模型 opus，effort 由 harness 默认）：6.8/10，promising_needs_revision；阻塞：部署性主张放在 Trace-and-Amplify 上检验，但该框架逐题重采样直到投机（GROUP_SIZE=1024、ROLLOUT_BATCH_SIZE=1），从第 1 步起就有在策自然正例，矛盾测试追踪器又是免费完美标签，'投机前无在策正例'与'需要提前就位监控器'两前提在该测试床不成立。另：新意幅度中等（相当于 Kirch 的 incentivised 数据沿 RL 时间轴重做）；overwrite-tests 步 20–80 漂移可能不足，未预设退路。子 Idea：IDEA-011`

### IDEA-011：前瞻监控的实证测量——撤回部署性主张，换用投机中途出现的第二测试床

- 来源：`最高近邻不足`
- 父 Idea：`IDEA-010`
- 状态：`selected`
- 定位关键词：reward hacking；training-time reward hacking；prompt-elicited trajectories；on-policy probe training data；linear probe；RLVR
- 一句话背景：同 IDEA-007。
- 自评分：`7.6/10`
- 一段话概括：C1–C3 不变，但只作实证主张：所有来源的正负例统一用真值清洗，不再主张"无需真值即可部署"。第二测试床由 Trace-and-Amplify（逐题重采样直到投机，从第 1 步起就有在策正例）换为 Countdown-Code（Qwen2.5-3B-Instruct 纯 RL 中途自然学会改目标值），只用于检验 C2、C3 跨模型家族成立。时点扩到 {20,40,60,80,100}，加检查点漂移（逐 token KL）作协变量，并预设"漂移不足"退路。新意表述如实收窄为"incentivised 数据沿真实 RL 时间轴逐点重做 + 监控器层面的能力/分布/风格拆分"。
- Story line：同 IDEA-010，删去部署性一环。
- 打分理由：最近四轮分数在 6.8–7.6 之间，reviewer 反复指出新意幅度中等；本修订消除已知阻塞，但能否两次 >8 不确定。
- Idea 生成依据：同 IDEA-010；Call 7 对 Trace-and-Amplify 训练脚本的核验（GROUP_SIZE=1024、ROLLOUT_BATCH_SIZE=1）；Countdown-Code 原文（Qwen2.5-3B-Instruct 与 Qwen2.5-Coder-7B 在 RL 中自然学会投机，2×A40 单实验 ≤60 小时）。
- 自评分轻量新意依据：同 IDEA-010。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：同 IDEA-010，去掉部署性。
- Baseline 可复现性：overwrite-tests 与 Countdown-Code 均已克隆核验（见 IDEA-003、IDEA-006）；文本分类器沿用 Trace-and-Amplify 仓库脚本。
- Reviewer 记录：`尚未送审`
