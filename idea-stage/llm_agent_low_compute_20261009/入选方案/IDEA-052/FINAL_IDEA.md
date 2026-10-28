## 术语与缩写表

| 术语 | 中文/全称 | 在本方案中 |
|---|---|---|
| grounding | 接地 | 某个具体参数值能在用户输入或真实公开返回中找到支持。 |
| joint witness | 联合值见证 | 不只是各值存在，还能从返回行/父调用关系支持它们一起组成一组参数。 |
| relation tuple | 关系元组 | 保留字段之间的实际关联，不能降成互不相关的值集合。 |
| natural join | 自然连接 | 用公开、明确的关联键连接有据关系；成熟数据库操作。 |
| supported / contradicted / unknown | 支持／冲突／未知 | 当前观测能支持、能反驳，或覆盖不足不能判断组合。 |
| HyperAgent / PACT | schema图规划／参数来源检查 | 已有联合调用和逐参数机制，不假设其未知实现一定遗漏本问题。 |

## Title

# 逐字段接地仍会拼错关系：以联合值见证约束工具调用

**候选ID：** IDEA-052。**独立审查：** Call37，8.2/10，experiment_ready，无致命阻塞。未运行模型实验。

**定位关键词：** tool-schema dependencies；state-conditioned planning；AppWorld。

**一句话背景：** 工具agent在同时拿到多对象的同类型参数后，怎样避免把来自不同对象的字段拼成一次调用。

**独立创新点：** 对具体参数组合保留行/父调用关系的联合见证，区分已冲突与覆盖未知，并在同调用/同row对照中检验。

## 1. 引言式概述

### 1.1 任务锚点与最小范围

限定AppWorld可信工具的多对象调用，研究业务参数关系而非安全攻防。一个冻结actor使用API，CPU记录关系并检查组合；没有模型训练或GPU推理要求。目标是完成原任务，同时减少分别有来源却组合错配的调用。

### 1.2 现有方法怎样处理

HyperAgent已维护schema-value bindings、同调用联合输出与deterministic binding validation；Entity Binding Failures已有多实体gate，PACT已有逐参数provenance，Binding Drift已有跨步对象保持。不能把这些说成不存在。当前只主张已核验描述未完整展示返回行/父调用键的业务关系join及三值反馈；HyperAgent无已核验公开完整代码，所以不对其实际runtime作负面事实结论。

### 1.3 具体瓶颈与证据边界

逐字段值存在不直接证明它们属于同一关联对象。例如两个关系R1={(x1,y1),(x2,y2)}、R2={(x1,y2),(x2,y1)}的schema和值集合相同，但(x1,y1)只有前者支持。这个例子是教材事实，只诊断marginal-only表示，不是新定理，也不能证明某个实际agent用的state只保留marginals。自然AppWorld错配频率和任务影响仍未知。

### 1.4 我们实际做什么

我们保留实际调用参数、返回对象/列表行和公开父关联键，构建关系元组。下一调用的关联参数只有在公开关系中能连接时才有联合支持；已知冲突给原actor修正，覆盖不足是unknown。允许正确跨行连接，不强制所有输入来自同一物理row，不把缺少一个当前tuple等同全局无效。

### 1.5 最小实验概览

先做同marginal、不同关系的表示诊断，再在原始AppWorld上同actor/raw history/信息与预算比较native FC、逐字段验证、same-call、same-row与关系join。主结论必须是自然任务成功/成本与错配改善，不能只说在构造反例上胜出。

### 1.6 拟验证贡献

1. 具体参数组合的行/父调用联合值见证。
2. 区分可支持、可反驳和观测覆盖未知的反馈。
3. 同call/同row对照与自然多对象任务，检验关系检查是否值得做。

## 2. 详细方法计划

### 2.1 方法直觉

先确认这组值有关系支持，再让原actor调用。

1. 同FC runner记录真实参数和逐调用返回。
2. 按返回对象/列表行保存字段，父关联参数只有公开文档/返回明确支持时附上。
3. 原actor在正常分析里声明本动作关联组和port对应，各组同享该说明并计费。
4. CPU按已知键连接，输出supported/contradicted/unknown及可见证据。
5. actor改组合、补查或继续；不能以拒绝更多动作冒充任务更成功。

### 2.2 输入、输出与成立条件

输入是公开调用/返回、关联说明、用户条件和拟调用值。输出是当前组合的三值关系反馈。需要至少一些明确关联键；不能靠字段类型相同、名字相似或同一user就认定两order相同。独立新常量不强制同源，多对象合法跨行组合必须允许。

### 2.3 算法与数据流

每个row保留调用实例和行号，真实父参数作为关系的一部分；均是普通可读元数据，无hash/指纹。按明确owner/id等键做join，得到受支持值组。known contradicted必须有实际反驳证据，完整枚举缺席只有证明覆盖完整时才能作为反证；其余保持unknown。

未知不自动升级为业务错误或强拒绝，actor仍承担语义选择。某个支持元组不证明符合用户目标，也不保证其当前仍有效。首版在关联读取至消费之间没有相关关系写入的范围验证；同agent相关写发生后，旧见证只作历史，需当前可见证据，不能继续当现时支持。这是实际状态边界，不新建通用迁移/权限框架。

### 2.4 最小实现与算力

已读官方SimplifiedFunctionCallingAgent及runner的执行输入/返回配对点，AppWorld CLI是真实入口。增加CPU关系侧表和join，记录只限agent本来能获得的调用输入与公开返回，不读DB、hidden evaluator、gold solution。所有说明、额外补查、关系序列化、失败及CPU处理成本计入，未端到端运行。

## 3. 最小验证实验

### 3.1 目的

证明控制是否保留必要关系信息，并判断自然任务中这一信息差是否真的影响调用和完成。表示例子不能替代自然诊断。

### 3.2 数据与切分

先冻结R1/R2成对表示测试，只用于关系与marginal差别，不报为AppWorld分数。再按公开多对象API结构选train/dev任务，独立标注跨关系错配、合法跨行组合及补查；dev冻结关联解释，held-out报全集成功与支持覆盖。不按主方法成功挑任务，构造例子与自然结果分开。

### 3.3 Baselines（唯一实验baseline定义）

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 开源代码与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| 官方AppWorld FC | 同AppWorld多对象API任务 | https://arxiv.org/abs/2407.18901 | https://github.com/StonyBrookNLP/appworld；SimplifiedFunctionCallingAgent已读，ExecutionIO逐调用参数/返回可见 | appworld run auto --agent-name simplified_function_calling_agent --model-name {共同actor} --dataset-name dev；固定同API/token/model/task cap | 是；未实跑 |
| 逐字段观测验证 | 排除幻觉字段和值已足够 | 本地完整标准规范 | 每个参数在对应port的用户输入/真实公开返回出现，原actor据同关联说明组合；不执行关系join | 同raw历史、actor与总预算 | 是 |
| same-invocation co-production | 强调用级联合检查 | 本地标准控制；不冒充HyperAgent | 关联参数值必须在同一实际成功工具调用的返回或其父输入出现，列表各row不进一步约束；独立新常量不强制同源 | 同row/call记录、业务说明和actor | 是 |
| same-row tuple gate | 强简单元组检查及过度限制对照 | 本地完整标准规范 | 关联参数必须有同一返回对象/列表row支持；来自不同row/call即报告缺联合支持（unknown仍不伪装业务错） | 主方法和此组得到同显式关联键，差别为物理row限制vs有据自然join | 是 |


同模型快照、task/seed、API/文档/关联说明、raw历史、上下文/输出、工具和LLM总调用/token上限。marginal-only控制只代表明确指定的消融，不代表HyperAgent。HyperAgent、Entity Binding/PACT/Binding Drift任务或公开实现条件不匹配当前实验，只列强近邻。

### 3.4 指标

主指标原task成功、实际关联组合错误与完整成本；次指标已冲突/未知区分准确度、合法跨行误报、额外补查、明确关系覆盖、CPU时间/RAM。unknown不能用错配真值标签计入“正确拦截”；少执行导致低错配而完成率更差不算收益。

### 3.5 支持和失败条件

自然错配有影响，关系join比逐字段和同call减少错误，又比同row少误报并在同预算任务更好才支持。明确关系覆盖低、same-row已等效、native已会正确结合、三值解释不可靠或全部收益来自保守不执行时停止。

## 4. 后续实验计划

1. 消融父调用键、返回row及unknown语义，保持其它信息一致。
2. 分同row、同call跨row、跨call有键连接三类，核对合法范围。
3. 同模型内改变输出长度、候选对象数和预算。
4. 相关关系写后的新观测作为后续扩展，不提前泛化首版静态关系保证。
5. 展示自然错配、合法跨行和覆盖不足的真实例子。

## 5. 风险与开放问题

关联说明仍由actor解释，可能错；明确键不总存在，历史见证也可能过期。联合支持只是业务关系必要证据，不证明用户指代或整体任务正确。教材反例和公开近邻没有相同实现不能充当已经胜过现有方法的结果。

## References Used

1. [AppWorld](https://arxiv.org/abs/2407.18901)，[官方代码](https://github.com/StonyBrookNLP/appworld)，同任务与FC入口。
2. [HyperAgent](https://arxiv.org/abs/2608.02650)，已直接读state/联合输出/runtime binding，完整代码未核验。
3. [Entity Binding Failures](https://arxiv.org/abs/2606.30531)，已直接读gate与provenance，逐实体近邻。
4. [PACT](https://arxiv.org/abs/2605.11039)，逐argument来源近邻，安全任务非本次baseline。
5. [Binding Drift](https://arxiv.org/abs/2607.18316)，跨步保持与错误传播近邻。
6. [In-N-Out](https://arxiv.org/abs/2509.01560)，静态port依赖近邻。

没有新的性能、费用或显存结果。
