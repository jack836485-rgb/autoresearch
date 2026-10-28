## 术语与缩写表

| 术语 | 全称或中文 | 本方案中的含义 |
|---|---|---|
| ALFWorld / TextWorld | 文字家务任务环境 | actor通过文字动作和环境反馈完成找物、清洗、加热和放置等任务，首版不用视觉模拟器。 |
| MemRL | Memory Reinforcement Learning | 固定LLM，用执行成败更新外部经验效用，再结合语义检索选经验。 |
| memory-Q | 经验数值效用 | 一条经验在后续检索时使用的奖励估计；不是经验文本，也不是LLM权重。 |
| eligibility | 更新资格 | 本次失败是否有最低执行证据，允许对某条经验写入负奖励；不是因果责任判决。 |
| binding | 动作绑定 | 将一条经验中的参数化动作与这次实际动作的变量对应起来。 |
| execution lapse | 执行偏离 | 指导可能有效，但actor没有照着落实；这是EmbodiSkill已有的区分。 |
| TIDE | Trajectory-Informed Directed Memory Evolution | 推荐反馈驱动的经验演化工作，已有“只检索不负责的经验不应获得credit”的概念。 |

## Title

# 程序经验的负反馈需要执行支持：用动作绑定约束逐条memory-Q更新

**候选 ID：** IDEA-039。**独立审阅：** Call 22，8.1/10，`experiment_ready`，fatal blockers为空。尚无模型实验结果。

**定位关键词：** episodic memory；credit assignment；ALFWorld。

**一句话背景：** 多条经验共同进入agent上下文后，任务失败不应自动证明每条经验都应该降分。

**独立创新点：** 将同轮memory/template声明、实际`env.step`动作和环境回执组合成无需训练、无需反事实rollout的负向效用更新资格门，只声称最低执行支持。

## 1. 引言式概述

### 1.1 任务锚点与最小范围

先限定ALFWorld的文字环境、一个冻结actor和多条注入经验。研究对象是失败结束时哪些ID收到负效用更新，初版不改成功奖励、不重新设计记忆内容，也不训练curator。

关键问题不是“怎样准确判断每条经验的因果收益”。更小而可做的问题是：当某条经验只进入上下文、没有落实到动作时，是否应仅凭终局失败给它负奖励？

该资格门在CPU上解析声明、实例化动作并对照回执。LLM与embedding可使用同一API；本地不需要GPU训练。构建、反思、检索和actor调用仍有费用，必须完整计入预算。

### 1.2 现有方法怎样处理

[MemRL](https://arxiv.org/abs/2601.03192)通过标量Q更新外部经验的效用。其ALFWorld runner汇总最终注入条目的ID，`MemoryService.update_values`将同一终局奖励给每个ID。论文G.2已经承认多记忆引用的信用归因歧义，因此“存在归因问题”不是新贡献。

[EmbodiSkill](https://arxiv.org/abs/2605.10332)以LLM反思区分技能缺陷和执行偏离，并在后者保留技能正文。[MemP](https://arxiv.org/abs/2508.06433)在失败后修订检索到的程序记忆。[EASE](https://arxiv.org/abs/2609.36746)借skill-free参考轨迹和行为差异为训练中的curation动作筛选credit。

最高概念近邻[TIDE](https://arxiv.org/abs/2609.37544)已经提出未影响决策的检索记忆不应credit，还结合语义与移除反事实。不能把“没用就不罚”宣称成首创。本方案较窄的差别是，在ALFWorld里将执行绑定用于负Q更新资格，既不做额外反事实任务，也不让反思模型判定完整因果责任。

### 1.3 具体失败与证据边界

**已核验：** 源码存在“最终注入ID统一负更新”的通道。

**尚需诊断：** 未采用条目是否因此被反复降分，后续是否错失有效经验，并最终影响成功率。一般性多记忆归因困难不能替代这一具体效应的实证。

例如同时注入“先清洗后放置”“加热使用微波炉”和“找物先检查容器”。actor可能从未执行加热，任务却因为导航或步数耗尽失败；统一负更新会连加热经验一起降分。这只是说明可能性，没有实际轨迹或效应量。

### 1.4 我们实际做什么

我们为能从公开训练轨迹连回参数化动作的经验附一个动作模板侧表，原经验文本和原检索保持不变。actor正常行动时同时声明采用哪个memory/template及变量绑定。CPU检查对应模板能否实例化为实际合法动作，以及该动作是否真的送入环境并取得相应回执。

任务最终失败时，仅有执行支持的ID成为负Q更新候选。没有落实、只声明没执行、或没有可绑定支持的条目不能因这次失败自动获得该负资格。不能把“候选资格”进一步说成该经验导致了失败。

### 1.5 最小实验概览

先固定同一多记忆库、actor、任务流、检索候选和预算，比较全部负更新、自报负更新、等次数随机负更新与执行绑定资格。学习后冻结，衡量成功率及经验误弃。另以同预算原生MemP和EmbodiSkill作强方法比较，保留它们的反思编辑能力。若简单减少更新数量已等效，就否定执行证据的额外必要性。

### 1.6 拟验证贡献

1. 一个以可观察实际动作为支持的负向memory-Q资格门，新增部分不调用critic。
2. 对“检索出现—实际落实—终局反馈”三个环节的独立诊断，避免把出现和采用混为一谈。
3. 与自报、等更新数量随机控制及同任务反思方法的完整预算比较，检验是否值得使用。

当前未取得任务性能提升，也未证明误罚普遍发生。

## 2. 详细方法计划

### 2.1 方法直觉

先确认这次确实照着某条指导做了，再允许这次失败改变它的数值评分。

1. 对共同训练池中的经验，建立能够回溯到源动作的模板ID；不可回溯的部分保留原文，并另报覆盖范围。
2. 多记忆检索仍用原方法，actor接收原内容与同样的ID/模板侧表。
3. actor在正常生成行动的JSON里附上memory ID、template ID和变量绑定；这部分输出计入费用。
4. CPU实例化模板，与真实送入`env.step`的动作对齐并记录回执；声明本身不够。
5. 任务失败时过滤原Q更新的ID列表；成功时先维持原规则，保持首版scope窄。

### 2.2 输入、输出与成立条件

- 输入：原经验文本、源训练轨迹、可回溯模板、最终注入ID、actor声明、实际动作与公开环境回执、终局成败。
- 输出：本次失败允许收到负Q更新的ID子集，以及无法绑定/无执行支持的诊断记录。
- 成立条件：ALFWorld动作语法可解析；经验至少一部分能回溯到具体动作；实际环境调用与返回能按轮次关联；目标经验的使用可由动作而非纯隐式思路体现。

成功的环境回执不是必要条件，因为做过一个动作也可能没有进展。回执只用于确认动作确实进入相应执行路径及其公开结果；无效语法或未送入环境不作落实证据。环境文本“Nothing happens”不应未经分析就等同从未执行：这类边界要在dev标注中明确，无法判断时记录为不确定，不能伪造标签。

只在文本行动可绑定的子范围声称机制成立。抽象建议可能影响策略但没有对应具体动作；它们的覆盖不足是失败条件，不能被偷偷计为“没有使用”。

### 2.3 算法与更新规则

原actor声明不是评价真值，CPU也不判断“该动作是否因经验而发生”。它验证的是更窄的关系：声明实例化出的动作和真实环境动作是否相同。

令 $m$ 是经验ID，$t$ 是当前任务，$a_{t,j}$ 是第 $j$ 轮真实环境动作。$D_{t,j,m}$表示actor声明使用m，$B_{t,j,m}$表示合法模板和变量绑定实例化后与真实动作匹配，$X_{t,j}$表示该动作具有相应执行记录与回执。定义负更新资格：

$$
E_{t,m}=\mathbb{1}\left[\exists j:\ D_{t,j,m}\land B_{t,j,m}\land X_{t,j}\right].
$$

$E_{t,m}=1$仅表示存在可观察的执行支持，不表示该经验有正收益或负收益。

若该任务失败，原MemRL负奖励为 $r_t$、原学习率为 $\alpha$、更新前数值为 $Q_t(m)$，则：

$$
Q_{t+1}(m)=Q_t(m)+\alpha E_{t,m}\big[r_t-Q_t(m)\big].
$$

没有执行支持时本次负更新不发生；成功任务仍沿用原正更新。原EMA公式不新，研究增量是负资格如何从记忆声明连到环境动作。

模板先用ALFWorld已支持的动作形式，绑定只处理公开对象、容器与位置槽位；同义策略但不同动作不能靠宽松字符串相似度随意认定匹配。自然的泛化采用是否被漏记，由独立盲标检验。所有实验臂共用ID/模板格式，避免只给主方法额外可读元数据。

### 2.4 最小实现与算力

以[MemRL](https://github.com/MemTensor/MemRL)的ALFWorld runner和MemoryService为基座，增加同轮采用声明、CPU绑定检查及任务结束负ID过滤。文字环境CPU运行，actor/embedding用相同API，记录所有输入输出；无反向传播、训练checkpoint或额外反事实rollout。

[EmbodiSkill](https://github.com/air-embodied-brain/EmbodiSkill)已核验`tasks/run_epochs.py`、核心EmbodiSkill类及LLM接口；支持actor与skill模型分别指定并使用OpenAI-compatible服务。

[MemP](https://github.com/zjunlp/MemP)公开核心可读，但原运行脚本有实际复现问题：actor的`llm`默认模型是占位字符串、调用未传`args.model`，脚本覆盖凭据，例子路径拼接缺分隔。必须在本地复现副本明确修正参数传递和路径，不能声称原CLI原样可跑。核心build/retrieve/update通过真实Memory接口保留，修复不改方法。

所有这些只是源码核验，本轮没有安装或端到端运行。

## 3. 最小验证实验

### 3.1 目的

先看是否存在足够多未落实经验却收到负更新，再看绑定资格是否比更便宜的自报/随机减少更新更有效。不能仅报告更新数减少作为成功。

### 3.2 数据与切分

ALFWorld文字环境，使用train获取共同初始经验与更新任务流，dev冻结模板边界、解码和覆盖规范，held-out seen/unseen测结果。拟用k=3以出现多条经验共同注入；具体金额、模型快照、任务数量和重复种子尚待实验阶段确定。

先做固定库受控实验：经验内容/ID和候选支持固定，仅改变负更新规则。真实策略产生的动作可以不同，但task IDs、环境seed、预算与数据范围相同。独立盲标从原轨迹与建议文本判断是否落实，不能将actor自报或主方法检测结果当真值。

再做完整原生方法比较，保留强方法的文本编辑、新经验写入与反思。受控固定库结果和原生端到端结果必须分别命名，不能将受限强方法的劣势当方法优越。

### 3.3 Baselines（唯一实验baseline定义）

| Baseline | 同任务关系/来源 | 已核验实现或完整规范 | 具体复现方式 |
|---|---|---|---|
| MemRL统一负更新 | 直接同任务效用学习；[论文](https://arxiv.org/abs/2601.03192) | [官方代码](https://github.com/MemTensor/MemRL)，已读runner、MemoryService及配置 | `python run/run_alfworld.py --config configs/rl_alf_config.yaml`；固定库模式暂停新写入；原生在线模式另报 |
| 只按self-report | 排除声明格式或actor自报已足够 | 原同轮JSON声明的ID直接获得负资格，不检查真实动作/回执 | 原`update_values`前过滤ID，其他更新不变 |
| 同次数随机负更新 | 排除只减少更新数量 | 从最终注入ID均匀无放回抽取与主方法执行支持相同数量，随机seed固定 | 资格时刻和数量先冻结，再随机选ID；不追加模型调用 |
| EmbodiSkill | 同ALFWorld的skill defect/execution lapse区分；[论文](https://arxiv.org/abs/2605.10332) | [代码](https://github.com/air-embodied-brain/EmbodiSkill)，真实core/run_epochs/LLM已读 | `python tasks/run_epochs.py --task alfworld --reasoning io --skill_module embodiskill --agent_model {共同actor} --agent_api_type openai --skill_model {共同反思模型} --skill_api_type openai --num_epochs {统一} --max_trials {cap} --train_shuffle_seed 42 --output_dir {slot}`；保留原生编辑，反思修订计费 |
| MemP reflect/update | 同程序经验构建、检索及失败修订；[论文](https://arxiv.org/abs/2508.06433) | [代码](https://github.com/zjunlp/MemP)，已读Memory、memory_adjust、llm_api和online runner | 真实`Memory(policy={build:direct,retrieve:query,update:reflect},is_cold_start=True,traj_file_path={共同train池},retrieve_num=3,memory_dir={slot})`；API_KEY/API_BASE_URL/MODEL_NAME按真实接口设；修正actor模型传递及路径后由共同TextWorld runner调用build/retrieve/update，不改变算法 |
| 无记忆ReAct | 检查辅助成本是否值得；[规范](https://arxiv.org/abs/2210.03629) | MemRL `_sample_from_batch_baseline`无memory采样路径已读 | 每task只一次基础运行，同actor/few-shot；可将省下的memory预算用于执行，不用pass-k成功上界冒充pass-1 |

上述本地简单控制都可按完整规范实现。所有方法固定actor/embedding快照、few-shot、task/seed、最大上下文与输出、工具和LLM请求上限及学习task数；actor声明、模板构建、强方法反思/embedding/检索/修订均计入总预算。反思模型能力相同，不能只给强方法更强模型或更长训练流。

EASE和TIDE是已读重要近邻；EASE仓库当次访问404，不纳入已核验可运行baseline。TIDE的推荐任务不匹配ALFWorld，不能作为跨领域实验对照。

### 3.4 指标

主指标是冻结后的held-out成功率及后续检索误弃。诊断指标是未落实条目接收负更新的比例、真实采用识别精确率/召回率，以及抽象建议无法绑定的覆盖缺口。误弃必须由后续独立任务/配对执行证据定义，不能用主方法自己的效用分数当标签。

次指标包括完整LLM/embedding调用与输入输出token、动作步数、反思成本、API费用及CPU解析时间。无效声明和无法绑定任务仍在总体成功率分母，不只报告可绑定子集的漂亮结果。

### 3.5 支持和失败条件

支持需同时满足：误负更新实际存在；执行绑定比self-report和等次数随机更准确；后续同预算成功或误弃改善；没有靠强模型、未来结果或额外执行获得收益。

如果污染规模很小、模板覆盖过低、泛化采用经常被漏记、随机少更新已完全等效、或同预算EmbodiSkill明显更好，应停止该机制。即使门能更准确验证“做过”，也不必然让终局奖励成为正确因果信用；不能把这件事偷换成归因已解决。

## 4. 后续实验计划

1. 在不同k、actor和ALFWorld任务族上验证，每个设置内部参数公平。
2. 消融ID声明、模板绑定与环境回执，找出是否真的需要全部环节。
3. 恢复各组共同的新经验写入规则，检验固定库结论是否延续。
4. 对照正更新也做资格过滤的后续扩展，但它不是本轮已过门槛Claim，不能提前并入首版。
5. 展示一条未落实却被原Q降分的自然轨迹及其后续影响，并展示主方法漏掉抽象采用的失败例。

## 5. 风险与开放问题

- **同动作可能本来就会发生。** 执行绑定不排除passenger credit，不估计相对无记忆收益；本方案只是最低更新资格。
- **模板覆盖有限。** 抽象知识可能没有唯一动作证据，不能将“无法绑定”自动解释为“未采用”。先独立标注覆盖再决定是否值得继续。
- **环境返回歧义。** “Nothing happens”、无效动作和正常无进展要区分；不能只凭自然语言回执猜测执行状态。
- **误罚仍可能发生。** 一条有效经验真正执行了，任务也可能因后续独立错误失败，本门不会修好所有误归因。
- **复现实现尚未跑。** MemP需小型源码修复/adapter，EmbodiSkill需数据与依赖；若接入改变了方法必须另报告，不掩饰成官方原样复现。
- **独立审查仍是provisional。** 同家族新零上下文reviewer通过门槛，不等于性能已验证或必能投稿。

## References Used

1. **MemRL: Self-Evolving Agents via Runtime Reinforcement Learning on Episodic Memory**，2026。[论文](https://arxiv.org/abs/2601.03192)，[代码](https://github.com/MemTensor/MemRL)。角色：问题入口、同任务核心baseline；已直接核验关键源码。
2. **EmbodiSkill: Skill-Aware Reflection for Self-Evolving Embodied Agents**，2026。[论文](https://arxiv.org/abs/2605.10332)，[代码](https://github.com/air-embodied-brain/EmbodiSkill)。角色：最强同任务执行偏离近邻和baseline；已读原理与入口/core。
3. **MemP: Exploring Agent Procedural Memory**，2025/ACL 2026。[论文](https://arxiv.org/abs/2508.06433)，[代码](https://github.com/zjunlp/MemP)。角色：同任务经验更新baseline；已核验核心及具体脚本缺口，没有声称原CLI实跑。
4. **How Can Recommendation Feedback Evolve Agent Memory? (TIDE)**，2026。[论文](https://arxiv.org/abs/2609.37544)。角色：最高概念近邻，一般实际使用责任原则已有先例；已打开一级全文，不作跨任务baseline。
5. **EASE: Behavior-Adaptive Skill Curation for Self-Evolving Agents**，2026。[论文](https://arxiv.org/abs/2609.36746)。角色：检索/行为双门与训练curator近邻；代码当次404，不列可运行baseline。
6. **Learning from Environmental Feedback: Credit Assignment across Multiple Timescales for Agentic Reinforcement Learning (EFCA)**，2026。[论文](https://arxiv.org/abs/2608.08255)。角色：动作环境反馈近邻；训练参数化策略，不符合首版无训练条件。
7. **When Successful Memories Mislead Embodied Agents: Memory Adaptation for Task-Conditioned Execution (MATE)**，2026。[论文](https://arxiv.org/abs/2609.35808)。角色：确定性动作规范化/负迁移近邻；已打开一级全文。
8. **ReAct: Synergizing Reasoning and Acting in Language Models**，2022/ICLR 2023。[论文](https://arxiv.org/abs/2210.03629)。角色：标准无memory基础actor。

本文件没有生成新的性能、费用或显存结果。
