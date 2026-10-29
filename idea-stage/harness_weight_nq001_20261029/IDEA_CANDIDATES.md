# Idea 候选池

> 本文件由 idea improver 持续维护。保留所有进入过比较的实质性候选及其演化关系；不要把完整 proposal 写进这里。

- 输入模式：`problem_card`
- 输入论文：不适用
- 输入问题卡：`path-stage/LLM热门方向_算力适配_20261028/` 中的 `N-Q001`

## 当前选择

- Reviewer 调用：`1 / 6`
- 当前选中 Idea：无（等待用户决定是否继续）
- 当前自评分：最高 available 为 IDEA-003 `5.8/10`、IDEA-006 `5.5/10`
- 选择理由：Call 1 显示 N-Q001 的“harness 内化进权重”一线已被 Harness-Zero、[2610.11655]、OPCD、Co-Harness、Evo² 等密集覆盖；剩余候选自评都不到 6，继续送审大概率不过门槛且消耗 reviewer 预算与 token，因此暂停询问用户是继续还是换卡。
- 状态：`已终止：用户决定换卡 A-Q001（见 PIVOT_OR_STOP.md）`

## 候选列表

### IDEA-001：多基准多种子的 harness × 权重 2×2 交叉

- 来源：`问题卡切口`
- 父 Idea：`无`
- 状态：`covered`
- 定位关键词：agent harness；self-evolving agents；harness evolution；LoRA fine-tuning；held-out evaluation
- 一句话背景：自进化 agent 领域中，进化 harness 与训练权重两种手段的增益能否叠加、谁能替代谁。
- 自评分：`3.5/10`
- 一段话概括：在 ≤9B 模型、两个可程序评分且有留出集的基准上做种子 / 进化 harness × 基座 / 训练权重的 2×2，多种子，记录过程失败与内容失败的构成和 token 成本。
- 打分理由：读全文摘要后发现 [2610.11655] 主结果已在 DeepPlanning 与 WebArena-Lite、8 个模型、四次 rollout 均值下完成这一交叉（卡片只记录了附录 H 的一条补充线），切口本身已被覆盖。
- Idea 生成依据：来自问题卡 N-Q001 的“可检验切口”。
- 自评分轻量新意依据：[2610.11655] 摘要：进化 harness 轨迹训练的 LoRA 在原 harness 下留出 +0.13，4B 上与 harness 叠加，9B 上 adapter 单独追平进化线；WebArena-Lite 上增益在“模型看到什么”，adapter 不增益。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：无，已被最高近邻覆盖。
- Baseline 可复现性：不送审，未填。
- Reviewer 记录：`尚未送审`

### IDEA-002：增益能否内化取决于信息可取得性——观察有据的轨迹改写

- 来源：`领域共性不足`（结合 `相似领域成熟方法迁移`：机器人特权教师蒸馏中的 imitation gap）
- 父 Idea：`无`
- 状态：`covered`（子 Idea：IDEA-006）
- 定位关键词：agent harness；context distillation；privileged information；on-policy self-distillation；imitation gap；AppWorld；ALFWorld
- 一句话背景：LLM agent 后训练中，把进化 harness 带来的增益内化进权重时，哪些增益能脱离 harness 保留下来。
- 自评分：`7.4/10`
- 一段话概括：Claim：现有内化方法（在进化 harness 轨迹上做 SFT、离线 / 在策略上下文蒸馏）的训练目标是“在额外信息存在时算出的动作”，学生在种子 harness 下看不到这份信息，于是 harness 中“改变模型看到什么”的增益训练不进去，甚至学到“没有信息也自信行动”。真正的分界不是“写 vs 看”，而是这份信息在种子 harness 下能否由 agent 自己取得：本回合早先见过的，或可用现有工具查到的。方法：观察有据的轨迹改写——用同一模型做依赖归因，找出每一步动作依赖的、只存在于进化 harness 上下文中的片段；对“早先见过”的片段，在它首次出现的那一步插入一条笔记；对“工具可查”的片段，在使用前插入对应的工具调用并在环境中真实执行；不可取得的片段所在步不进训练。改写后的轨迹在种子 harness 上下文下做 SFT。最小实验：Qwen3-4B / 8B，ALFWorld 与 AppWorld，按编辑类型（写 / 看-可取得 / 看-不可取得）分层，比较 N4 式轨迹 SFT、离线上下文蒸馏、OPCD 与本方法在种子 harness 下的留出成绩。
- Story line：[2610.11655] 在 WebArena-Lite 上发现进化 harness 的增益来自“多给一页历史”，在这些轨迹上训练的 adapter 不能把它带走，于是得出“看到的增益留在 harness”的规则；[2609.29051] 在 AppWorld 与 SWE-bench Verified 上发现，以特权信息为教师视图的在策略自蒸馏会让学生“自信地行动却没有背后的信息”，表现低于普通 RL、最差低于基座。两者的共同原因是训练目标依赖学生输入中没有的信息，即机器人特权教师蒸馏中已知的 imitation gap [2007.12173]。被忽视的是：harness 多给的信息常常在种子 harness 下也能由 agent 自己取得（翻回历史、查 API 文档），只是原轨迹里没有“去取”的动作。本 Idea 把轨迹改写成“先取信息、再用信息”的形式再训练。可推翻的预期：在“看-可取得”编辑上，改写后的 SFT 在种子 harness 下恢复明显多于离线上下文蒸馏与轨迹 SFT 的进化增益；在“写”编辑上各方法相近；在“看-不可取得”编辑上所有方法都恢复不了，且上下文蒸馏低于基座。若离线上下文蒸馏在“看-可取得”编辑上与改写持平，则 Claim 被推翻。
- 打分理由：直接与最高近邻的核心规则相冲突且可证伪，机制有成熟理论支撑、实现简单；风险在于上下文蒸馏与特权信息蒸馏方向很拥挤（OPCD、π-Distill、SKALD、Skill-SD、PSP、2610.31918），“按可取得性分层并改写成取信息动作”这一点尚需 reviewer 检索确认。
- Idea 生成依据：问题卡 N-Q001 证据 [2610.11655]；问题卡 A-Q003 的证据 [2609.29051]；imitation gap 理论 [2007.12173]、特权教师蒸馏 [1912.12294]；[2608.07169] 在 AppWorld 上用 Qwen3-4B/8B 报告注入记忆的增益（含 API 调用约定类内容）。
- 自评分轻量新意依据：检索“privileged context distillation agent harness”“imitation gap privileged information LLM agent”“rewrite trajectories insert information-gathering actions”等。最近邻：OPCD [2602.12275]（系统提示 / 经验知识的在策略上下文蒸馏）、π-Distill [2602.04942]、PSP [2609.29051]（把特权信息移到采样端）、2610.31918（层级在策略性）、SKALD [2608.09826]、Skill-SD [2604.10674]、D-OPCD [2610.07250]、Co-Harness [2607.22688]。未检出按信息可取得性区分 harness 增益并把信息改写成取信息动作的工作；需要 reviewer 检索。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：提出“信息可取得性”作为 harness 增益能否内化的判据，并给出把可取得信息改写为取信息动作的内化方法。
- Baseline 可复现性：

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 开源代码与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| 轨迹 SFT | 最高近邻的 harness 增益内化方式 | https://arxiv.org/abs/2610.11655 | 论文未开源；属于可直接实现的标准 LoRA SFT；LLaMA-Factory 已核验（main 2026-10-29，含 `examples/train_lora/qwen3_lora_sft.yaml`） | H* 输入 + H* 动作做 LoRA SFT | 是 |
| 离线上下文蒸馏 | 上下文蒸馏标准形式 | https://arxiv.org/abs/2209.15189 | 无仓库，标准方法，同上本地实现 | H0 输入 + H* 动作做 LoRA SFT | 是 |
| OPCD | 在策略上下文蒸馏，用于系统提示与文本游戏 | https://arxiv.org/abs/2602.12275 | https://github.com/microsoft/LMOps/tree/main/opcd 已核验（2026-09-15，基于 verl，含 `scripts/textgame_consolidate.sh` 与 TextGame Rollout） | 在 TextGame Rollout 接入 ALFWorld，教师为带 H* 上下文的同一模型 | 是（仅 ALFWorld） |
| A-Evolve（数据来源） | 同领域 harness 自进化实现 | https://arxiv.org/abs/2605.30621 | https://github.com/A-EVO-Lab/a-evolve/tree/release/harness-evolution 已核验（2026-08-22，`agent_evolve/benchmarks/base.py` 的 `BenchmarkAdapter`） | 为 ALFWorld / AppWorld 实现 `get_tasks` 与 `evaluate` | 作为 H* 生成工具，非对照 |
| 环境 | — | ALFWorld、AppWorld | https://github.com/alfworld/alfworld（2026-02-08）、https://github.com/StonyBrookNLP/appworld（2026-09-03）README 已核验安装与评测入口 | `alfworld-download`；`appworld install`、`appworld download data`、`appworld evaluate` | 是 |

- 现象核验：注入记忆对 Qwen3-4B/8B 在 AppWorld 上的增益见 [2608.07169]；“多显示历史”的增益见 [2610.11655] 的 WebArena-Lite（模型未逐一核对）；ALFWorld 上历史截断的增益需在 dev 先验证，brief 已写明。
- Reviewer 记录：`Call 1（常规，Opus 默认 effort）：4.0/10，needs_rethink，最高近邻 Harness-Zero（arXiv 2609.24974）`。主执行器已读原文核实：Harness-Zero 用 GPT-5.6 Sol 作 harnessing agent，在目标 harness 的动作空间里改写 Qwen3.5-9B 学生的回复（缺证据时插入取证动作），在 AppWorld 等三个领域做 LoRA SFT，宏平均从 23.3% 提到 44.3%（超过带 harness 的 41.7%），28 个 harness 独有行为平均恢复 82.3%。核心方法被覆盖；“现有方法在看的增益上失败”与其证据冲突。Reviewer 认为仍新的部分：可得性三分类与分层预测、截断历史→笔记改写、离线对数概率归因。

### IDEA-003：用“冗余度 × 可遵循度”预测每个 harness 产物的增益

- 来源：`领域共性不足`
- 父 Idea：`无`
- 状态：`available`
- 定位关键词：agent harness；harness sensitivity；skills；instruction following
- 一句话背景：自进化 agent 领域中，harness 增益为何随基座能力非单调变化，以及为何固定生产级 harness 之间差别很小。
- 自评分：`5.8/10`
- 一段话概括：假设单个 harness 产物的增益 ≈ 可遵循度 ×（1 − 冗余度）：冗余度用“有无该产物时同一状态上的动作分布差异”度量，可遵循度用产物被激活后动作是否与其规定一致度量。在多个能力档的开源模型上测这两个量，检验它们能否同时解释 [2605.30621] 的非单调与 [2610.04433] 的小差异，再用 LoRA 训练提高部分产物的冗余度，检验这些产物的增益是否按预测下降。
- 打分理由：能统一三处现象，但 [2609.40303] 已论证强模型下 harness 机制层冗余，[2605.26731] 已报告非单调与失败类型，本候选只有诊断与预测规律，缺少方法贡献。
- Idea 生成依据：来自问题卡 N-Q001；[2605.30621]、[2609.40303]、[2605.26731]。
- 自评分轻量新意依据：检索“why stronger LLMs benefit less from skills harness redundancy”，命中 [2605.26731]、[2609.40303]；未检出逐产物的定量预测。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：逐产物的冗余度与可遵循度两因素预测。
- Baseline 可复现性：未填。
- Reviewer 记录：`尚未送审`

### IDEA-004：内化之后 harness 还能否继续进化

- 来源：`最高近邻不足`
- 父 Idea：`无`
- 状态：`covered`
- 定位关键词：self-evolving agents；harness evolution；co-evolution
- 一句话背景：自进化 agent 领域中，权重内化 harness 增益后，后续 harness 进化的空间是变大还是变小。
- 自评分：`4.0/10`
- 一段话概括：比较内化前后在相同进化预算下 harness 的新增增益，检验内化是否降低模型从新产物中获益的能力。
- 打分理由：Co-Harness [2607.22688]、Evo² [2610.13025]、HASE [2607.03935] 已做权重与 harness 交替进化，D-OPCD [2610.07250] 已报告内化后 harness 可删掉饱和技能并继续进化。
- Idea 生成依据：[2610.11655] 中 9B adapter 叠加进化 harness 不再增益。
- 自评分轻量新意依据：检索“co-evolution harness and model weights LLM agent”，命中上述四篇。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：无，已被覆盖。
- Baseline 可复现性：未填。
- Reviewer 记录：`尚未送审`

### IDEA-005：首个失败信号标注会掩盖潜在内容失败

- 来源：`最高近邻不足`
- 父 Idea：`无`
- 状态：`baseline_patch`
- 定位关键词：agent failure analysis；failure taxonomy；harness evolution
- 一句话背景：[2610.11655] 按首个触发的失败信号区分过程失败与内容失败，并据此选择手段。
- 自评分：`4.0/10`
- 一段话概括：过程失败先触发时，轨迹里的内容问题不会被标出，修复过程失败后才暴露，因此按构成选手段会系统性高估 harness 的作用；用反事实续写测潜在内容失败。
- 打分理由：本质是修补单篇近邻的诊断步骤，不构成独立的领域问题。
- Idea 生成依据：[2610.11655] §3.1、§6.2（loop 停在 F4）。
- 自评分轻量新意依据：未检索。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：无独立贡献。
- Baseline 可复现性：未填。
- Reviewer 记录：`尚未送审`

### IDEA-006：harness 蒸馏的残差由不可取得的信息决定——只保留残差 harness

- 来源：`最高近邻不足`（最高近邻改为 Harness-Zero，arXiv 2609.24974）
- 父 Idea：`IDEA-002`
- 状态：`available`
- 定位关键词：agent harness；harness distillation；privileged information；context distillation；AppWorld
- 一句话背景：harness 蒸馏把进化 harness 诱导的行为训练进权重后，部署时还剩哪些增益必须由 harness 提供。
- 自评分：`5.5/10`
- 一段话概括：Claim：Harness-Zero 等蒸馏方法之后的残差（约 18% 未恢复的行为、以及分数差）集中在“原始 harness 下不可取得的任务级信息”上，而不是随机分布；因此部署时只需保留一个只提供这类信息的残差 harness，就能在远少于 H* 的上下文 token 下达到或超过 H*。最小实验：在 AppWorld 上复现 Harness-Zero 的蒸馏模型，按可得性三类给 harness 组件分层做消融，比较蒸馏模型 + 残差 harness / + 完整 H* / 不带 harness 的成绩与 token。
- 打分理由：能把 [2610.11655] 的规则、Harness-Zero 的残差和 [2610.04433] 的“harness 主要买 token”串起来，但本质是对 Harness-Zero 的残差分析加一个剪枝结论；D-OPCD [2610.07250] 已报告内化后可删掉饱和技能，新意有限；复现 Harness-Zero 需要 GPT-5.6 Sol 作 harnessing agent，API 费用可能超过 1000 元。
- Idea 生成依据：Call 1 review 及 Harness-Zero 原文（Table 4 的 28 个行为恢复率；§4.4 替代蒸馏信号比较）。
- 自评分轻量新意依据：未单独检索“residual harness after distillation”；与 D-OPCD 的“删掉饱和技能”相邻；需要 reviewer 检索。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：用信息可取得性预测 harness 蒸馏的残差，并据此给出最小残差 harness。
- Baseline 可复现性：Harness-Zero https://github.com/metaevo-ai/harness-zero（Call 1 reviewer 浅克隆核验含 `envs/appworld`、`src/harness_zero/sft.py`，主执行器未复核）。
- Reviewer 记录：`尚未送审`
