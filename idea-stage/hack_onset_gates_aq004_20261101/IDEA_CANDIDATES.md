# Idea 候选池（A-Q004 第二轮）

> 第一轮候选池见 `idea-stage/reward_hack_monitor_aq004_20261029/IDEA_CANDIDATES.md`（IDEA-001 至 IDEA-011）。本轮编号重新从 IDEA-001 开始。

- 输入模式：`problem_card`
- 输入论文：不适用
- 输入问题卡：`path-stage/LLM热门方向_算力适配_20261028` 的 `A-Q004`

## 当前选择

- Reviewer 调用：`1 / 6`
- 当前选中 Idea：`IDEA-006`
- 当前自评分：`7.9/10`
- 选择理由：用户选择继续 A-Q004。IDEA-006 回到卡片原文的 agentic 多轮工具设置（近邻 SimHack、CATCH、Rebound、djinn 都是单轮写代码），同时覆盖锚点两半：投机渠道为何在能力之后出现、冻结监控器召回为何衰减。
- 状态：`等待第 2 次 reviewer 调用`

## 候选列表

### IDEA-001：冻结监控器召回随训练衰减（卡片切口）

- 来源：`问题卡切口`
- 父 Idea：`无`
- 状态：`available`
- 定位关键词：reward hacking；monitor；RL training
- 一句话背景：RL 训练中，固定投机监控器的召回如何随策略能力变化。
- 自评分：`5.0/10`
- 一段话概括：同第一轮 IDEA-001。Engels/Nanda 已观察到投机 run 中约 16 点下降，第一轮也已围绕它打磨 8 次。仅作比较点。
- 打分理由：已有初步测量，第一轮已充分探索。
- Reviewer 记录：`尚未送审`

### IDEA-002：投机为何延迟出现——用分支注入实验分离"发现、能力、激励"三道门槛

- 来源：`领域共性不足`
- 父 Idea：`无`
- 状态：`needs_revision`
- 定位关键词：reward hacking；GRPO；RLVR；exploration；hacking onset
- 一句话背景：代码 RLVR 中，可利用的验证器漏洞从训练一开始就存在，投机却要到训练中途才出现；已有文献对这段延迟给出了几种不同解释，但从未用干预实验把它们分开。
- 自评分：`7.8/10`
- 一段话概括：投机延迟可能来自三道门槛：(a) **发现**——策略能执行投机，但无指令时采样到投机的概率太低；(b) **能力**——策略还执行不了投机；(c) **激励**——GRPO 中投机样本的优势取决于同组正当解的失败比例，正当解能拿分的题上投机几乎没有优势。方法：在主训练的若干检查点（包括步 0）分出短分支，向 GRPO 组内注入该题自带或同检查点诱导出的已验证投机样本若干步后停止注入，测量投机是否"起飞"（无注入后自然投机率持续上升）。若步 0 分支即起飞，延迟由发现门槛决定；若早期分支注入后不起飞、要等指令投机成功率上升才起飞，延迟由能力门槛决定；按同组正当通过率分层，检验激励门槛（投机起飞集中在正当通过率低的题上，只用简单题的分支不起飞）。在 djinn（26 类投机，难度跨度大，每题自带投机解与安全验证器）和 overwrite-tests 上做，按投机类型分层，预期简单投机由发现门槛主导、复杂投机由能力门槛主导。最后检验诊断能否预测缓解效果：按正当通过率过滤题目，只在激励门槛主导的投机类型上推迟出现。
- Story line：投机在训练中途才出现（overwrite-tests 基座自然投机率约 0.09%、80–100 步开始 [Engels/Nanda]；djinn 上 Qwen3 不提示几乎不投机 [EleutherAI]）。已有解释互不相同：可发现性随与真实奖励的纠缠变化 [CHERRL 2606.04923]；捷径只对已学会的工具形成 [2609.16268]；早期改写因混入自身解过不了的用例失败 [2604.01476]；正当奖励稀缺时投机反弹 [2604.01476]，加简单题能减少投机 [ICML 2026 monitor-intervention]；初始倾向不同则投机难易不同 [RL-only 博文]。EleutherAI 明确写这些解释未被分别检验 → 被忽视的关键：三道门槛对应完全不同的缓解手段，但它们从未被干预分离 → 本 Idea 的动作：检查点分支注入 + 指令成功率测量 + 按同组正当通过率分层 → 可推翻的预期：若所有类型都在步 0 注入后起飞，能力门槛解释被推翻；若按正当通过率分层无差异，激励门槛解释被推翻。
- 打分理由：直接回答卡片前半个问题；分离已记录的竞争解释，诊断设计清楚；测试床与投机解现成；风险是注入的离策略样本在 GRPO 中的处理方式会影响结论，以及新意需要 reviewer 检索确认。
- Idea 生成依据：2606.04923（§3.1 可发现性与纠缠、§3.2 可利用性受生成难度约束）；2609.16268、2606.26300（来自问题卡 A-Q004）；2604.01476（三阶段反弹）；EleutherAI djinn 博文（https://blog.eleuther.ai/reward_hacking/ ）；Reward Hacking Without Egregious Misalignment in an RL-Only Setting（GreaterWrong）；ICML 2026 monitor-intervention（https://icml.cc/virtual/2026/79298 ）；Engels/Nanda 博文。
- 自评分轻量新意依据：检索"onset exploration vs capability injection""off-policy injection hacking takeoff"未见以注入分支分离投机延迟原因的工作；CHERRL 的可发现性/可利用性分解是相关性分析且在 rubric RL；需要 reviewer 检索。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：首次用检查点分支注入把投机延迟分解为发现、能力、激励三道门槛，并用诊断预测缓解手段何时有效。
- Baseline 可复现性：

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 开源代码与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| djinn 测试床 + GRPO 训练 | 代码 RLVR，可利用验证器，自带投机解与安全验证器 | https://blog.eleuther.ai/reward_hacking/ | https://github.com/EleutherAI/djinn ；2026-11-01 克隆核验：`djinn/agent/train_agent.py`（TRL GRPO + vLLM，`--dataset skiptest` 对应 djinn-problems-v0.9），数据 HF `EleutherAI/djinn-problems-v0.9`（26 类投机、741 题） | `trl vllm-serve` + `accelerate launch djinn/agent/train_agent.py` | 是 |
| overwrite-tests 测试床 | 代码 RLVR 训练期投机 | https://www.greaterwrong.com/posts/R5MdWGKsuvdPwGFBG/steering-rl-training-benchmarking-interventions-against | https://github.com/ariahw/rl-rewardhacking ；第一轮已克隆核验 | `run_rl_training no_intervention --task simple_overwrite_tests` | 是 |
| 按正当通过率过滤题目（缓解手段） | 同任务；ICML 2026 报告加简单题减少投机 | https://icml.cc/virtual/2026/79298 | 简单标准方法：按初始模型 pass@k 过滤训练题，本地实现 | 训练前用初始模型采样估计每题正当通过率 | 是 |

- Reviewer 记录：`Call 1（常规，同模型 opus）：5.0/10，promising_needs_revision；最高近邻 SimHack (2610.28707)、2604.01476、CATCH (2609.39533)、Countdown-Code、CHERRL。阻塞：①偏离锚点（未涉及监控器召回）；②前提不实——EleutherAI 博文并未写'各解释未被分别检验'（该句来自检索摘要工具的转述，improver 未核对原文），SimHack 已改变 rollout 数与课程并给出 GRPO 组内竞争解释，2604.01476 已用限制正当 rollout 与更易题做激励干预，CATCH 用 SFT 混入比例与奖励难度控制投机出现；③C1 注入来源与能力共变，重要性比恒为 1，不可识别能力门槛。另：djinn skiptest 默认模型为 gpt-oss-20b，Qwen3 无提示时几乎不投机；分支算力低估约 2.4 倍。`

### IDEA-003：合法能力外溢——训练写测试的能力会加快"改写测试"类投机的出现

- 来源：`领域共性不足`
- 父 Idea：`无`
- 状态：`available`
- 定位关键词：reward hacking；unit test generation；RLVR
- 一句话背景：代码 agent 训练常同时提升写单元测试的能力，而 overwrite-tests 类投机需要写出与自身解自洽的测试。
- 自评分：`6.8/10`
- 一段话概括：在保持通用解题能力（pass@1）相当的前提下，RL 前先对模型做"写正确单元测试"的 SFT，与等计算量的对照 SFT 相比，在可改写测试的环境中投机是否更早出现、更普遍。
- 打分理由：结论有实际意义，但较可预期；本质是 IDEA-002 能力门槛的一个具体操纵，可作为其能力分支的一部分。
- Reviewer 记录：`尚未送审`

### IDEA-004：第一轮最佳候选——前瞻式监控的实证测量

- 来源：`最高近邻不足`
- 父 Idea：`第一轮 IDEA-011`
- 状态：`available`
- 定位关键词：reward hacking；prompt-elicited trajectories；on-policy probe training data；RLVR
- 一句话背景：见第一轮 `round-08-brief.md`。
- 自评分：`7.3/10`
- 一段话概括：投机出现前用当前检查点诱导数据训练监控器，测其对之后自然投机的前瞻召回。第一轮 Call 8 评分 7.5，无致命阻塞，但新意边界薄。
- 打分理由：已有 reviewer 结论；作为比较点保留。
- Reviewer 记录：`第一轮 Call 8：7.5/10`

### IDEA-005：诱饵通道——用不参与奖励的诱饵漏洞跟踪投机倾向

- 来源：`相似领域成熟方法迁移`（安全领域的蜜罐）
- 父 Idea：`无`
- 状态：`available`
- 定位关键词：reward hacking；honeypot；RLVR
- 一句话背景：学习型监控器会随新投机渠道失效，而投机倾向可能跨渠道泛化。
- 自评分：`6.0/10`
- 一段话概括：在环境中放置不被奖励的诱饵漏洞，测其使用率是否随真实渠道投机同步或提前上升，作为免标注的倾向指标。
- 打分理由：依赖跨渠道泛化这一未证前提；预测投机出现的方向已有 PRIME、EleutherAI、SimHack，较拥挤。
- Reviewer 记录：`尚未送审`

### IDEA-006：多轮工具 agent 中，投机渠道由正当子技能解锁——技能课程的双重分离与冻结监控器的渠道级衰减

- 来源：`领域共性不足`（能力门控）结合 `未覆盖新任务`（Hack-Verifiable TextArena 尚无 RL 训练）
- 父 Idea：`IDEA-002`（吸收其能力门槛部分，放弃已被 SimHack、2604.01476、CATCH 覆盖的发现与激励部分）
- 状态：`selected`
- 定位关键词：reward hacking；agentic RL；multi-turn tool use；hack-verifiable environments；monitor recall
- 一句话背景：多轮工具 agent 的投机渠道（读取隐藏答案文件、利用源码逻辑漏洞）需要先具备特定的正当子技能；已有投机出现时刻研究都在单轮写代码中，把投机当作一个整体。
- 自评分：`7.9/10`
- 一段话概括：在 Hack-Verifiable TextArena（多轮文字游戏 + 模拟文件系统，投机可确定性判定，原文未做 RL）上用 verl-agent 做多轮 GRPO。C1：每条投机渠道只在 agent 习得其前置正当子技能后才打开——用等计算量的辅助正当任务课程操纵子技能（文件系统导航 / 读源码），预期双重分离：加导航课程只提前"隐藏答案文件"渠道，加读码课程只提前"逻辑漏洞"渠道，通用辅助任务对照两者都不提前。C2：冻结监控器（在首个渠道出现时构建）在训练中的召回下降集中在之后新打开的渠道上，已见渠道上的召回保持；且无监控器优化压力，区别于 CATCH 的"被注释误导"。C3：用留出的正当技能探针测量各子技能，子技能习得领先对应渠道打开若干步，可作为渠道级前兆。
- Story line：投机在训练中途才出现，已有解释包括能力门控 [2609.16268：捷径只对已学会的工具形成；2604.01476：早期改写因能力不足失败]，工业实践中新渠道在模型变强后才出现、需每轮人工补规则 [2606.26300]；固定监控器在训练中准确率下降 [Engels/Nanda]，CATCH 把 CoT 监控器失效归于策略学会用注释误导（在监控器施压下） → 已有出现时刻研究（SimHack 2610.28707、CATCH 2609.39533、2604.01476）都在单轮写代码中把投机当整体，未在多渠道 agent 环境中把"哪条渠道何时打开"与"哪个正当子技能何时习得"对应起来，也未区分监控器衰减来自新渠道还是旧渠道变隐蔽 → 本 Idea：子技能课程双重分离 + 渠道级召回分解 + 技能探针 → 可推翻：若导航课程同时提前两条渠道（或都不提前），子技能门控被推翻；若冻结监控器召回在已见渠道上同样下降，"衰减来自新渠道"被推翻。
- 打分理由：回到卡片原文的 agentic 设置，避开单轮代码的拥挤区；双重分离是干净的因果设计；测试床现成且投机可确定性判定；风险是 4B 模型在多轮环境中能否在训练内打开渠道，需要试跑。
- Idea 生成依据：2605.20744 Hack-Verifiable Environments（https://www.alphaxiv.org/abs/2605.20744 ，读摘要与环境说明：隐藏答案文件、逻辑漏洞、读写对手提示三类渠道，难度影响利用率，未做 RL）；2609.16268（摘要与目录：§5.3 任务能力与捷径形成、§5.4 分离任务能力与语义对齐）；2606.26300、2604.01476；SimHack、CATCH（摘要）；Engels/Nanda。
- 自评分轻量新意依据：检索"multi-turn agentic RL reward hacking channels unlocked by tool skills"未见对应工作；HVTA 原文将 RL 训练列为未来工作；需要 reviewer 检索。
- 与输入论文的关系：不适用
- 本 Idea 的独立创新点：在多渠道 agent 环境中用子技能课程做双重分离，因果检验"渠道由正当子技能解锁"，并把冻结监控器衰减分解为新渠道覆盖缺失与旧渠道变隐蔽。
- Baseline 可复现性：

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 开源代码与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| Hack-Verifiable TextArena 环境 | 多轮工具 agent 投机，确定性判定 | https://arxiv.org/abs/2605.20744 | https://github.com/MajoRoth/hack-verifiable-environments ；2026-11-01 克隆核验：`hvta/FilesystemWrapper/filesystem_wrapper.py`（`FilesystemWrapper(env, hidden_solution=True, logical_bug=True)`）、`logical_bug_envs/`、`examples/run_hidden_solution_benchmark.py` | 包装 TextArena 单人游戏 | 是 |
| verl-agent 多轮 GRPO/GiGPO | 多轮 agent RL 标准训练框架 | https://arxiv.org/abs/2505.10978 | https://github.com/langfengQ/verl-agent ；克隆核验：`examples/grpo_trainer/`、`gigpo_trainer/`，`agent_system/environments/env_manager.py` 注册新环境（README §4） | 按 README §4 注册 HVTA 环境，`examples/grpo_trainer` 脚本启动 | 是 |
| 冻结 LLM judge 监控器 | 训练期投机监控 | Engels/Nanda；CATCH | 本地 Qwen3-8B 提示式判定（标准做法） | 本地推理 | 是 |
| 冻结线性探针 | 训练期投机监控 | Engels/Nanda（https://github.com/ariahw/rl-rewardhacking 的 `train_probe` 思路） | 冻结基座激活 + logistic 回归，标准实现 | 本地实现 | 是 |

- Reviewer 记录：`尚未送审`
