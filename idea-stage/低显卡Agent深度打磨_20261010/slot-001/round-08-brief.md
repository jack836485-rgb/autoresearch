## 背景
正确判断“当前证据不足”并不告诉agent哪条工具调用会补上所需语义，或在当前权限与预算内能否补上。当前研究聚焦工具计数限定被加强为精确结论（Q001）及正确诊断后无效精化/能力或预算不足（Q005），不覆盖任意数字污染或first-touch。Elastic官方Search API已规定gte下界，并给出timed_out=true仍eq的部分计数；准确性升级和覆盖恢复是不同效果（https://www.elastic.co/docs/solutions/search/the-search-api）。ToolUniverse审计已提出用途条件性可靠性，不能把保留qualifier称为新方法（https://arxiv.org/html/2609.26836v1）。SearchDecision-Bench/Table1已测sufficiency、支持性和next-action；SearchJev AppendixD.3把insufficient接到forced continue，但其typed schema可容纳任意操作选择，不声称架构不能做恢复（https://arxiv.org/html/2610.05107v1）。新增研究对象是有实际工具转移与成本的“诊断等价、恢复不等价”任务：固定结论要求及诊断正确性，只改变公开能力和预算来辨识可执行恢复；区间语义、AND/OR策略穷举与可达性均是标准基线，不申报算法创新。

## 核心 Claim
待检验：对于相同用户精确计数目标、相同当前数值/限定和相同正确诊断，公开修复能力与剩余预算可产生四种不同终态——无需修复、可执行支持性修复、只有更高预算可修复、在公开动作闭包中不可修复。建立诊断等价配组，要求agent同时输出可执行首动作及有据的停止/继续理由；测试“正确的充分性/故障类别反馈”是否仍系统性选择无效动作或把能力阻断误认为再重试即可。独立任务贡献的支持条件不是答案类型成功率不同：必须在固定正确诊断与任务目标的配组中，观察到agent修复选择错误随能力/预算变化，且完整公开语义规划基线能够恢复这些错误而相同诊断提示不能。若差别只来自额外反馈、遗漏工具说明或总预算不公平，Claim失败。

## 方法设计的核心思想
每个episode公开当前结果、用户结论要求、工具能力描述和成本；工具能力可以是精确计数仅支持指定分片、按分片读取、恢复连接后读取或只可读取已完成分片。这些是明确不同接口实例，不让工具表暗含隐藏能力。标准参照将公开结果解释成可能数值集合；依据公开工具转移和动作结果分支，在剩余预算内穷举有限AND/OR策略。终点须对该公开历史一致的所有世界支撑同一任务结论；不能以单世界真实N为oracle选动作。输出最小可行成本及有效首动作集合仅为离线标签，在线agent只能凭公开文档和实际调用推导。当前阶段不训练或运行规划器/actor。
主比较中的无诊断、只给当前正确诊断、正确诊断加原样公开能力、强公开语义规划基线，均保留相同文档和操作范围；能力信息本来全公开，第三臂只是把既有文档相关段落原样重排，不额外泄漏动作答案。正确诊断臂由在线公开限定的确定性规则生成，例如“当前计数是下界且不足以支持精确N”，不使用隐藏故障原因。把该规则的误分类与actor恢复错误分开报告。Task本身考操作作用与可达性，不称新预测模型或新恢复算法。

## 最小实验
完整CPU有限任务：两至三个静态非负分片，每片记录数取有限集合，所有成功返回均无重复/假记录；初始Search结果由公开relation和complete/missing_shards说明支持单点或下界。主要诊断等价组固定用户“报告精确N”、相同value=100/gte、完整目标范围与当前各分片已知界。四个公开能力实例分别允许（A）one-shot exact_all成本3；（B）exact_part仅覆盖指定一片成本1，必须read_other_parts累计成本4才能支撑N；（C）read_missing先restore_endpoint成本1，再exact_part成本2；（D）遗漏分片没有任何读取或恢复接口，且界不为零，因此无法支持精确N。没有one-shot隐藏旁路，能力表中公开写明适用范围；A/B/C接口作用不同，不把价格差本身当新意。完整eq干净组是无需修复对照。每个能力实例在不同总预算水平重复，含足够及不足条件；允许因实际返回把界收窄而较早完成。离线在当前公共历史一致的小世界上穷举策略，给每组预算可达性和有效首动作，不给actor这些标签。
测试冻结FunctionCalling actor（真实循环入口https://raw.githubusercontent.com/Zhudongsheng75/ToolMaze/main/evaluation/agents/openai_agent.py）、原failure-aware、上述确定性正确诊断coaching、文档相关段落重排、只升级精度/盲重复同调用/泛化forced-continue标准策略、完整公开语义AND/OR基线。SearchJev训练/inference实际入口https://raw.githubusercontent.com/EvoScientist/SearchJev/main/training/inference.py已亲读：decide接受任意state与choice菜单，但原模型本地GPU依赖及完整dual-system实现未核实，不把它强塞为同核心模型baseline；用同冻结actor、相同typed questions/legal menus的标准判别接口作对照。标准任务不冒称复现SearchDecision-Bench或ToolUniverse整套系统。
主指标按全体配组统计：支持且正确完成率、有效首动作率、正确能力/预算阻断判断、无效重试成本与干净损失；在当前确定性诊断正确子集单列这些指标，并报告该子集筛选和全部分母，不从汇总诊断率相除。预先规定贡献判据：跨公开能力等价配组的修复动作错误在budget-sufficient层存在，并被强公开语义基线消除；若只提高budget就解释全部错误、或正确诊断已足够消除，则没有新增诊断到动作的失败结构。规划、诊断、文档检索/重排、token、调用、扫描、CPU与等待都计完整总成本；纯确定性基线和同actor载体分列。模型、世界规模、预算/费用取值、样本与统计功效待确认，未运行实验或生成实验代码。
