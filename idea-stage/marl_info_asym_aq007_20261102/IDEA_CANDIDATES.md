# Idea 候选池

> 本文件由 idea improver 持续维护。保留所有进入过比较的实质性候选及其演化关系；不要把完整 proposal 写进这里。

- 输入模式：`problem_card`
- 输入论文：不适用
- 输入问题卡：`path-stage/LLM热门方向_算力适配_20261028/` 的 A-Q007（多智能体工作流 RL 何时优于单智能体；独立策略后期断崖）

## 当前选择

- Reviewer 调用：`1 / 6`
- 当前选中 Idea：`无`（最不受阻候选 IDEA-007，自评 4.5，未送审）
- 当前自评分：`—`
- 选择理由：Call 1 中 IDEA-005 得 5.5，被指出信息瓶颈下的正确反事实是"在同一瓶颈下训练的单智能体"（MemSearcher/MEM1 式）；修正后问题退化为同一瓶颈下的共享 vs 独立参数（IDEA-007）或"多智能体增益即上下文管理"的审计（IDEA-008），二者已有直接或半直接证据，自评均不高于 4.5，不再送审。
- 状态：`提前停止（rejected_no_viable_candidate），剩余 5 次 reviewer 额度未用`

1. 第 1 轮选择（Call 1 前）：IDEA-005，自评 6.3。作者 2026-11-01 更新版已覆盖 IDEA-002/003，IDEA-005 对准卡片唯一仍开放的工具使用条件。

## 候选列表

### IDEA-001：工具使用工作流上多种子复现角色级梯度与后期准确率

- 来源：`问题卡切口`
- 父 Idea：`无`
- 状态：`available`
- 定位关键词：multi-agent reinforcement learning；shared policy / isolated policy；GRPO；agentic search
- 一句话背景：多智能体 LLM 工作流 RL 中独立策略后期准确率下降的现象，在工具使用工作流与多种子下是否仍成立。
- 自评分：`4.0/10`
- 一段话概括：照卡片切口，在搜索类工具工作流上以 3 个种子重复共享/独立策略训练，记录逐角色梯度范数、熵与后期准确率。只有诊断没有新主张；作者更新版已给出下降机制（并行角色多走优化器步）与修法（合并步），复现即使成功也只是补种子。
- 打分理由：可行、可证伪，但贡献是给已有结论加种子与换任务，单独不足以成为主会论文。
- Idea 生成依据：来自问题卡 A-Q007；作者更新版（GitHub XHMY/marl-llm-workflows，项目页 2026-11-01）。
- 自评分轻量新意依据：未单独检索；与作者更新版的结论高度重合。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：无独立机制，仅扩展设置。
- Reviewer 记录：`尚未送审`

### IDEA-002：独立策略后期断崖源于并行角色的每步优化器步数（步数匹配对照）

- 来源：`领域共性不足`
- 父 Idea：`无`
- 状态：`covered`
- 定位关键词：isolated policy；GRPO；PPO mini-batch；gradient amplification
- 一句话背景：多智能体 GRPO 中独立策略的后期下降，究竟来自多智能体耦合，还是来自并行同角色实例让该角色每个训练步走多次（离策略）优化器步。
- 自评分：`3.0/10`
- 一段话概括：用"每角色每步一次优化器更新"与"单智能体 RL 给同样步数"的对照，区分多智能体耦合、Dr. MAS 的全局归一化失配与通用离策略漂移三种解释。注意在固定拓扑、共享结局奖励的 Voting/Orch-Workers 中，按角色归一化与全局归一化统计量相同，Dr. MAS 的修法无法解释该断崖。
- 打分理由：作者更新版已做 `t2_merged_minibatch`（每角色每步一次更新，推迟下降）与 `single_role`（无工作流的单角色也下降）两个对照，正好覆盖本候选的核心诊断。
- Idea 生成依据：2605.24202 v2 §5.1（"adds more same-role updates per iteration"）；Dr. MAS 2602.08847 §4.1；作者仓库 `docs/reproducing.md` Controls 表。
- 自评分轻量新意依据：作者仓库与项目页（2026-11-01 同步）直接覆盖。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：已被覆盖。
- Reviewer 记录：`不送审（covered）`

### IDEA-003：以"单智能体 RL 放入同一结构"为反事实分解多智能体 RL 增益，并只训练决策角色

- 来源：`最高近邻不足`
- 父 Idea：`无`
- 状态：`covered`
- 定位关键词：multi-agent reinforcement learning；single-agent RL baseline；Eval-Opt / Voting / Orch-Workers；role specialization
- 一句话背景：多智能体 RL 工作流论文常把训练后的工作流与单次回答的单智能体 RL 比较，混淆了推理结构带来的增益与联合训练带来的增益。
- 自评分：`3.5/10`
- 一段话概括：2×2 分解（推理结构：单/多 × 训练：单智能体/联合），并提出先单智能体 RL 训练求解角色、再只在工作流中训练决策角色的"角色选择性训练"。2605.24202 v2 附录 Table 3 已有单种子迹象（SA-RL 放入 Orch-Workers 58.9 > MA-RL IP 55.5）。
- 打分理由：作者更新版把"SA-RL in the same structure"作为主表列与核心结论（同结构 SA-RL 打平或胜过 Voting/Orch-Workers，只有 Eval-Opt IP 胜出且主要来自截断重试），仓库另有 `init_from_sa_adapters` 对照。
- Idea 生成依据：2605.24202 v2 附录 A.2/Table 3；作者项目页 m1/m2 结论。
- 自评分轻量新意依据：作者更新版直接覆盖。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：已被覆盖。
- Reviewer 记录：`不送审（covered）`

### IDEA-004：用集成学习的负相关学习 / 差分奖励训练 Voting 的投票者以降低错误相关

- 来源：`相似领域成熟方法迁移`
- 父 Idea：`无`
- 状态：`covered`
- 定位关键词：majority voting；self-consistency；difference rewards；ensemble diversity
- 一句话背景：Voting 工作流的联合训练在 broadcast 结局奖励下不奖励投票者之间的互补错误，因此无法超过独立训练的同结构单智能体。
- 自评分：`3.5/10`
- 一段话概括：借集成学习的负相关学习（Liu & Yao 1999）与多智能体 RL 的差分奖励，给每个投票者"有我/无我时投票结果之差"作奖励，预期投票者错误相关下降、多数投票准确率超过同结构 SA-RL。
- 打分理由：以多数投票/pass@k 为目标、用留一法优势训练单策略的工作（Optimizing LMs for Inference Time Objectives using RL，2503.19595；Inference-Aware Fine-Tuning for BoN，ICLR 2025）已覆盖核心机制，多智能体外壳不增加新意。
- Idea 生成依据：负相关学习；COMA / difference rewards；作者更新版"投票者单独计分低于 SA-RL"。
- 自评分轻量新意依据：1 次定向检索命中 2503.19595 与 BoN-aware fine-tuning。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：已被覆盖。
- Reviewer 记录：`不送审（covered）`

### IDEA-005：联合训练只在跨角色信息不对称时才超过"同结构单智能体 RL"——检索问答工具工作流中的受控检验

- 来源：`领域共性不足`
- 父 Idea：`无`
- 状态：`needs_revision`
- 定位关键词：multi-agent reinforcement learning for LLMs；agentic search / Search-R1；shared vs non-shared (isolated) policies；GRPO；information asymmetry
- 一句话背景：在多智能体 LLM 工作流的结局奖励 RL 中，联合训练相对"把单智能体 RL 模型放进同一结构"何时有正增益，这一问题在工具使用（检索问答）工作流中尚无受控答案。
- 自评分：`6.3/10`
- 一段话概括：Claim：当所有角色看到同样信息时（数学/代码，或搜索中各角色共享完整历史），一个在整任务上训练的单智能体已具备每个角色所需技能，联合训练不超过同结构 SA-RL；当下游角色只能看到上游角色选择传递的内容（上下文隔离，部署中的子 agent 常见）时，上游必须学会"传什么"，这是单智能体训练不产生的技能，联合训练才有正增益，并且增益集中在传递方。方法：在 Dr. MAS 的检索问答环境中构造同任务、同检索器的工作流族，只改变答题角色可见信息（完整历史 / 搜索者报告 ≤256 token / ≤64 token），比较联合训练（独立/共享策略）与同结构 SA-RL；交换角色（联合搜索者+SA 答题者 vs SA 搜索者+联合答题者）定位增益来源。最小实验：Qwen2.5-3B，NQ+HotpotQA 训练，7 个 QA 基准 EM，3 种子。
- Story line：作者更新版在数学/代码三种工作流上发现同结构 SA-RL 打平或胜过联合训练的 Voting/Orch-Workers，只有 Eval-Opt IP 胜出，且主要来自截断重试（单种子）；Dr. MAS 在各角色共享完整历史的搜索工作流中，多智能体 GRPO 相对单智能体 GRPO 只高约 2 点（3B）。这些工作流的共同点是信息对称——每个角色能看到的信息，单智能体在整任务训练中都已见过并学会使用。被忽视的变量是跨角色信息不对称：部署中的子 agent 常只回传摘要，下游只能依赖上游选择传递的内容。本 Idea 在同一检索环境中只调节答题者可见信息，检验联合训练增益是否随隔离强度单调出现，并用角色交换定位增益在传递方。若隔离条件下增益仍≈0，或增益落在接收方，则主张被推翻。
- 打分理由：直接对准卡片唯一仍开放的工具使用条件，主张可证伪、算力可行；风险是结论可被视为"可预期"，以及推理期信息不对称（InfoDelphi）与带私有信息的协作训练（CoSIR）构成近邻，需要 reviewer 检索确认。
- Idea 生成依据：
  - 2605.24202 v2 与作者 2026-11-01 更新版（GitHub XHMY/marl-llm-workflows 项目页 m1/m2/m4）：同信息工作流中同结构 SA-RL 打平或胜出；
  - Dr. MAS 2602.08847 v2 Table 2：搜索三角色共享完整历史，3B 单智能体 GRPO 32.5 vs 多智能体 34.8/34.5；
  - DAC 2606.10684：搜索者/生成者分角色训练，对照只有单次回答的 Search-R1（39.6 vs 42.3）；
  - InfoDelphi 2607.01661：推理期设计信息不对称，去掉不对称后多数审议增益消失（无训练）。
- 自评分轻量新意依据：3 次定向检索（信息不对称 × 多智能体 RL；搜索者/答题者多智能体 RL 对照；单智能体放入结构的反事实）未见"联合训练 vs 同结构 SA-RL × 信息隔离强度"的受控研究；最近邻 CoSIR（2610.17893，私有信息协作的自博弈训练，用信息奖励）与 InfoDelphi（推理期）。正式结论需要 reviewer 检索。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：把"联合训练何时优于同结构单智能体 RL"归因到可操控的跨角色信息不对称，并在工具工作流中用隔离强度剂量与角色交换做受控检验。
- Baseline 可复现性：

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 开源代码与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| Search-R1（单智能体 GRPO 检索问答） | 同任务（NQ+HotpotQA 训练，7 个 QA 基准）、同检索器（E5 + wiki-18）的单智能体 RL | https://arxiv.org/abs/2503.09516 | https://github.com/PeterGriffinJin/Search-R1 ；已核验含 `train_grpo.sh`、`retrieval_launch.sh` | 用 Dr. MAS 仓库同一 verl 栈复现单智能体 GRPO（`examples/grpo_trainer/run_search.sh`），与联合训练同步数、同组大小 | 是 |
| 同结构 SA-RL（SA-RL 模型放入每个角色） | 反事实对照：同结构、同推理预算，只缺联合训练 | 2605.24202 作者更新版定义（"SA-RL in the same structure"） | 无需单独仓库：载入 Search-R1 式 SA-RL 检查点作为每个角色的模型，只评测 | Dr. MAS 编排的 non-sharing 配置把三个 agent 都指向同一检查点，仅 eval | 是 |
| Dr. MAS 联合训练（共享/非共享，按角色归一化） | 同任务的多智能体 RL 方法，三角色 verifier/search/answer | https://arxiv.org/abs/2602.08847 | https://github.com/langfengQ/DrMAS ；已核验含 `agent_system/agent/orchestra/search/`、`examples/drmas_trainer/run_search.sh`（README：3×Qwen2.5-3B 非共享 4×H100 约 13h） | `run_search.sh`，`model_sharing` 取 True/False；隔离条件只修改编排中答题者的输入 | 是 |
| Vanilla 多智能体 GRPO（全局归一化） | 同任务的多智能体 RL 基础版本 | 同上（Dr. MAS 的 GRPO 对照） | 同上，`group_by_agent_id=False` | 同上 | 否（仅在完整历史条件作合理性检查） |

- Reviewer 记录：`Call 1（常规，同模型 high）：5.5/10，promising_needs_revision，最高近邻 2605.24202（项目页版）、Dr. MAS、MultiAgent-OPD 2610.23234、MemSearcher 2511.02805 / MEM1 2506.15841、s3 2505.14146`
- 致命问题（主执行器已核验）：
  1. Claim 前提"传什么只能由联合训练习得"无支撑：MemSearcher 用单智能体 multi-context GRPO 学会只保留与问题相关的记忆；隔离档里的同结构 SA-RL 从未在瓶颈下训练过，Claim 2 区分不了"多智能体联合训练"与"任何在同一瓶颈下的 RL"。
  2. Baseline 路线错误：Dr. MAS `examples/grpo_trainer/run_search.sh` 是三角色 vanilla GRPO；`verl/trainer/main_ppo.py:65` 与 `ray_trainer.py:447` 均 `assert multi_agent`，发布代码不能训练单智能体。
  3. Claim 3 方向已有证据：s3 只训练搜索方服务冻结生成器；MultiAgent-OPD 训练 Searcher 摘要。
- 主执行器补充：MultiAgent-OPD Table（Qwen3-4B，同检索器）中 MemSearcher 单智能体 36.81 与 C-MAS + RL（联合训练的级联 Searcher→摘要→Answerer）约 36.07 相当，已给出"同一瓶颈下单智能体≈联合多智能体"的跨方法迹象。

### IDEA-006：按角色设置双时间尺度学习率以抑制上下游角色的非平稳共适应

- 来源：`相似领域成熟方法迁移`
- 父 Idea：`无`
- 状态：`available`
- 定位关键词：isolated policy；two-timescale stochastic approximation；non-stationarity；multi-agent RL
- 一句话背景：独立策略下上游（求解）与下游（决策）角色同时更新，彼此输入分布都在变化，后期可能失稳。
- 自评分：`4.5/10`
- 一段话概括：借 GAN 的 TTUR 与去中心化 MARL 的多时间尺度学习（Nekoei et al. 2023），让决策角色快、求解角色慢，预期推迟后期下降且不降峰值。
- 打分理由：作者更新版已把下降定位在并行角色的优化器步数与熵上升，合并步即可推迟；按角色学习率在 Dr. MAS 框架中已是可配置项，单独贡献偏小。
- Idea 生成依据：Nekoei et al. 2023（2302.02792）；作者更新版 m4。
- 自评分轻量新意依据：1 次检索命中去中心化 MARL 多时间尺度学习，LLM 工作流中未见，但与"合并步"高度相关。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：迁移多时间尺度学习到 LLM 工作流角色。
- Reviewer 记录：`尚未送审`

### IDEA-007：同一信息瓶颈下，分角色联合训练相对"瓶颈内单智能体 RL"何时有增益

- 来源：`最高近邻不足`
- 父 Idea：`IDEA-005`
- 状态：`available`（未送审，提前停止）
- 定位关键词：agentic search；multi-context GRPO（MemSearcher）；shared vs. isolated policies；information bottleneck
- 一句话背景：检索问答中，若上游只能把有限长度的报告交给下游，联合训练两个角色是否优于让一个单智能体在同一瓶颈下自写记忆再作答的 RL。
- 自评分：`4.5/10`
- 一段话概括：按 Call 1 修正反事实：单智能体在相同报告上限下用 multi-context GRPO 训练（自写报告、清空上下文后作答），与联合训练的独立/共享策略比较，3 种子，报告上限作剂量。共享策略版本与瓶颈内单智能体几乎是同一优化问题，因此差别只剩"是否分参数"，即 2605.24202 已研究的 IP vs SP，换到工具任务并加种子。
- 打分理由：反事实正确后，主张退化为已有轴（IP vs SP）在新任务上的复现；MultiAgent-OPD 的表已显示 MemSearcher≈C-MAS + RL，预期结果偏零，新意低。
- Idea 生成依据：Call 1 审查引用的 MemSearcher、MEM1、MultiAgent-OPD（主执行器已读摘要与 MultiAgent-OPD 结果表）。
- 自评分轻量新意依据：MultiAgent-OPD 2610.23234 结果表（同底座、同检索器）已给出单智能体记忆方法与联合级联系统的对比。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：瓶颈剂量 × 参数共享的受控对照；单独不足以成文。
- Reviewer 记录：`未送审`

### IDEA-008：多智能体搜索 RL 相对 Search-R1 的增益是否只是上下文管理

- 来源：`领域共性不足`
- 父 Idea：`IDEA-005`
- 状态：`available`（未送审，提前停止）
- 定位关键词：agentic search；context management；multi-agent RL；Search-R1；MemSearcher
- 一句话背景：多智能体搜索 RL（Dr. MAS、DAC、MATPO、MultiAgent-OPD）都与完整历史的单智能体 Search-R1 比较，没有与学会管理上下文的单智能体在同训练预算下比较。
- 自评分：`4.5/10`
- 一段话概括：在同底座、同检索器、同步数下比较完整历史单智能体、记忆单智能体（MemSearcher）、联合 IP / SP 多智能体，检验"多智能体增益 = 上下文长度/噪声管理"。若记忆单智能体与多智能体打平，则多智能体搜索 RL 的增益主要来自上下文隔离。
- 打分理由：审计型结论，MultiAgent-OPD 表与 MATPO 摘要（"to manage context"）已半直接给出；问题真实但偏 benchmark 审计，主会新意不足。
- Idea 生成依据：MATPO 2510.04678 摘要；MultiAgent-OPD 2610.23234 表；MemSearcher 2511.02805。
- 自评分轻量新意依据：MultiAgent-OPD 同表已含 Search-R1、MemSearcher、Dr. MAS 与 C-MAS + RL。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：同预算受控审计。
- Reviewer 记录：`未送审`
