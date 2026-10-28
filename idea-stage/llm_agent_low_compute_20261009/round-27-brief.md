## 背景

**定位关键词：** tool-schema dependencies；state-conditioned planning；AppWorld

**一句话定位：** 工具agent在同时拿到多对象的同类型参数后，怎样避免把来自不同对象的字段拼成一次调用。

## 核心 Claim

HyperAgent以schema可用性和port依赖做状态条件工具规划，原文不足讨论同名参数的多个producer及联合可用；更窄的待诊断失败是每个参数都有来源、整体schema也合法，却把不同返回行或不同父调用的对象ID/属性错配。主张可执行性还需公开返回行/父参数能见证一组关联输入的联合绑定；CPU保留关系元组并做带已知实体关联约束的join，而不把可用参数降为独立集合。并非发明数据库join，也不泛称解决实体消歧。

多个producer和schema可用性是已报告规划问题；独立字段来源无法证明一起属于同一目标；把返回行及父调用变成联合见证，再检查关联参数join；若比逐字段provenance更少错配并提升相同预算成功率，才支持。

## 方法设计的核心思想

在同AppWorld FC runner记录每次公开工具调用参数及逐调用返回。每个返回对象或列表行保留本轮调用和行号，相关父参数（如order_id）附在该行。关联约束只能来自用户请求、公开文档的输入输出描述和实际返回中的实体关联键；原actor初次解释工具时输出关联组与port对应，同一次调用计费。CPU为下一动作建立候选关系元组，以明确owner/id连接键自然join相关字段，常量/独立的新值不被强制与对象同源。参数分别找到但没有联合见证则让原actor选补充查询或改绑定；不凭类型相同/字符串相似认定实体相等。不要求所有参数同一物理row，不将同一user下的所有order当成同一order。不读环境数据库或评测器字段；未知关联保持未验证，不伪造关系。

## 最小实验

AppWorld多对象读写任务先独立检查每参数有观测来源而组合跨行/跨父调用的错误是否出现。共用FC动作接口、同actor/schema上下文和观察预算；比较native FC、相同结构化参数来源表、每字段provenance检查、schema-set可用性控制、联合元组绑定。完全相同的关联说明给简单控制，唯一区别是保留独立集合还是关联元组。主指标同预算task success、关联输入错配与不必要补查；盲标将真的错配与合法跨对象组合分开；不靠减少执行次数的拒绝策略冒充成功。未出现错误、未知关联覆盖过低、只靠强提示已解决、或严格join阻断合法调用时停止。

同一模型快照、相同数据和顺序、相同推理模式/温度/seed/最大步数、相同总输入输出 token、LLM 调用与工具调用上限；机制、反思和检查均计入总预算。参数为实验前待确定项，本轮不运行。只读取 agent 可见输入，不读评价答案/隐藏状态。

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 开源代码与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| 官方AppWorld FC | 同AppWorld多对象API任务 | https://arxiv.org/abs/2407.18901 | https://github.com/StonyBrookNLP/appworld；SimplifiedFunctionCallingAgent已读，ExecutionIO逐调用参数/返回可见 | appworld run auto --agent-name simplified_function_calling_agent --model-name {共同actor} --dataset-name dev；固定同API/token/model/task cap | 是；未实跑 |
| 结构化独立来源表 | 排除只是ID/来源结构更清晰 | 本地标准对照 | 每field列可见value、call与row，交同actor；不做联合求解，仍接同关联说明 | 同公开返回、同actor和输入输出预算 | 是 |
| 每字段provenance检查 | 排除只验证值不是幻觉 | 本地标准对照 | 验证每个参数value曾在匹配port的实际返回/用户输入出现，但不要求关联输入可join | 同来源表，不读私有状态 | 是 |
| schema-set控制 | 定位丢失联合性机制 | 完整本地标准控制；不是无公开代码的HyperAgent复现 | 保留每schema字段可用value集合，所有必需字段非空即可交actor填参；相关说明/文档同主方法 | 同FC runner，CPU策略直接实现，不能标原作者HyperAgent分数 | 是 |
