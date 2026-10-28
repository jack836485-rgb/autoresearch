## 术语与缩写表

| 术语 | 中文/全称 | 本方案含义 |
|---|---|---|
| SlopCodeBench | 迭代规格编码基准 | 同一agent不断扩展自己的代码，测试隐藏。 |
| structural erosion | 结构侵蚀 | 复杂性集中到少量复杂函数的指标；不是可维护性的完整真值。 |
| clone | 近似代码复制 | 多个区域共享结构但部分名字/常量不同。 |
| anti-unification | 反统一 | 提取多个AST共同骨架，把不同处留成变化孔；成熟方法。 |
| 变化轴 | 本方案中的定义 | 当前spec已有且在历史实例中能够独立变化的维度，如语言或匹配种类。 |
| checkpoint | 需求轮次 | 一轮新的公开规格和自己此前工作区；未来规格不可见。 |

## Title

# 从已发生的变更提取独立变化轴，控制迭代代码的分支交叉增长

**候选ID：** IDEA-042。**独立审查：** Call26，7.9/10，experiment_ready，无致命阻塞。未运行模型实验。

**定位关键词：** iterative specification refinement；structural erosion；coding agents。

**一句话背景：** 迭代编码agent在增加新需求时，如何避免把不同变化维度不断塞进同一段分支。

**独立创新点：** 只用已发生spec/代码变化的单维实例，约束agent何时提炼共享骨架，并用后续可修改性检验。

## 1. 引言式概述

### 1.1 任务锚点与最小范围

限定SlopCodeBench公开Python任务序列，以同MiniSWE actor不断编辑自己的代码。没有模型训练；AST处理与已有代码对齐CPU执行，重构分析和生成仍使用同API预算。不能利用下一checkpoint的需求设计当前接口。

### 1.2 现有方法怎样处理

[SlopCodeBench](https://arxiv.org/abs/2603.24755)报告复制和分支集中逐轮增长，通用anti_slop/plan_first不能阻止退化。自动clone抽取/anti-unification、CREC历史co-change和REFINE基于smell重构已有直接先例。本研究不把抽函数或变化点分析当成新算法。

### 1.3 具体瓶颈与证据边界

待验证的窄假设：近似clone的共同外形不代表它们沿同一需求维度变化；合并不同变化轴后，下一次扩展可能又把函数切开。必须在自然轨迹检查这一链条；不能把增加需求的复杂性本身当成迭代引起退化。

### 1.4 我们实际做什么

我们用已发生的spec与代码diff解释anti-unification孔。只有已有至少两个实例、并有仅一个维度不同的分离证据时，才建议对该维度提炼共享骨架；联合变化或缺少证据时不提前独立抽象。这约束重构动作，不添加尚未发生的feature flag、迁移层或未来接口。

### 1.5 最小实验概览

同actor/spec/工作区与总预算比较原agent、anti_slop、plan_first、clone-only、固定每轮重构和变化证据约束。主要观察下一checkpoint严格正确率与完成成本；当前CC和重复下降只作辅助，不能作为成功标准。

### 1.6 拟验证贡献

1. 公开需求变化与AST孔的实例关联。
2. 用单轴分离证据限制在线重构，避免未观察到的抽象假设。
3. 后续真实扩展成本/正确率验证，控制累计需求复杂性。

## 2. 详细方法计划

### 2.1 方法直觉

先看不同部分是否曾在真实需求中独立变化，再决定抽象。

1. 工作区保留上一轮spec、自己的代码及diff。
2. CPU对齐变更附近近似clone，得到公共骨架和孔。
3. 原actor在正常分析里解释孔对应的当前需求维度与联合变化。
4. CPU核对历史实例是否有单轴差异；无证据不宣布独立。
5. 原actor做一次局部重构或直接扩展，并在共同预算内自测。

### 2.2 输入、输出与成立条件

输入是当前及过去可见spec、自己代码/diff和公开例子。输出是允许提炼的骨架/孔及其有限证据。依赖条件是AST区域可对齐，需求维度解释够可靠，已有例子并非偶然的相关变化。没有两个实例不代表将来不能抽象，只是当前机制不作证据不足的建议。

### 2.3 算法与数据流

AST相同节点保留，差异常量/标识符置为孔；位置属性不参与结构判断。每个候选记录实际来源区域和轮次，不生成哈希。原actor解释维度，CPU只对明确实例检查哪个孔/维度发生变化，不能通过一个自然语言标签证明完整语义独立。

重构行为以已观察变化为依据，不能根据隐藏future tests挑骨架。公开例子和自己测试只检测当前行为，不保证未知全部行为；重构导致当前错误也照实进入成功率。

### 2.4 最小实现与算力

已读公开MiniSWE wrapper、真实DefaultAgent/API接口、local/Docker环境、配置和run指南。入口slop-code run可运行；CPU新增AST对齐与证据表。重要修正：公开AgentCostLimits只有step/cost/net-cost，没有总token硬上限，实验需在模型调用处统一新增记账与中止；不能伪称cost_limits已提供token cap。prompt名是anti_slop/plan_first，非连字符。

## 3. 最小验证实验

### 3.1 目的

判断当前更谨慎的抽象是否在未知下一轮需求中减少重新切开/重复复制，并提高同预算完成。单纯降低被自己优化的CC没有价值证据。

### 3.2 数据与切分

使用冻结的当前公开问题列表，不混用原论文20问题/93checkpoint与后续公开扩展语料的分数。当前每轮只能见当前spec，hidden tests只用于离线评测且结果不返回agent。各组同初始空工作区、任务順序、自己代码继承规则、模型/推理/seed与完整预算。另用同一累计spec的继续编辑和from-scratch诊断区分需求扩大与路径依赖，不免费给未来累计spec。

### 3.3 Baselines（唯一实验baseline定义）

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 开源代码与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| SlopCodeBench MiniSWE | 同一迭代spec+自己代码工作区 | https://arxiv.org/abs/2603.24755 | https://github.com/SprocketLab/slop-code-bench；src/slop_code/agent_runner/agents/miniswe/agent.py与configs/agents/miniswe.yaml已读，实际DefaultAgent/API model/local或Docker环境 | uv sync；slop-code run --agent configs/agents/miniswe.yaml --model {共同API模型} --problem {冻结问题}；原生cost_limits仅step/cost/net-cost，统一总token硬上限需在模型调用边界新增；与原论文无cost上限的分数分开 | 是；未实跑 |
| anti_slop / plan_first | 原论文同任务提示干预 | https://arxiv.org/html/2603.24755v1#S4.SS3 | 公开prompt模板与文档；需用同MiniSWE而非换native模型 | 同run入口 --prompt anti_slop / plan_first，对应当前anti_slop.jinja / plan_first.jinja；完整提示可移植到同MiniSWE，全部token计费 | 是；提示内容可直接本地实现 |
| 仅clone/anti-unification | 排除一般重复检测与抽函数收益 | 本地标准算法规范 | Python AST去位置后做结构对齐；相同节点保留、不同常量/标识符置孔，发现至少2个区域后交同actor抽一个函数；不附spec变化轴 | 同候选数量、同重构调用和测试预算，不引入外部checkpoint | 是 |
| 固定每轮重构 | 排除多做一轮整理本身 | 本地标准对照 | 每checkpoint实现后同actor追加一次局部重构机会，没有变化轴约束 | 重构包含在共同总预算，不免费增加一轮 | 是 |


各组都可见同历史diff和spec摘要。重构/自测/历史序列化耗费同总token及步骤额度，不免费给主方法多一轮。MaintainCoder/CREC/REFINE任务或训练方式不同，只列近邻。

### 3.4 指标

主指标下一轮严格正确率和完成费用；次指标重新拆开共享区域、重复增长、当前重构引入错误、CPU对齐时间、token和步骤。侵蚀/verbosity仅辅助。未产出代码和超预算轮次按失败报告，不能从分母删去。

### 3.5 支持和失败条件

自然错误合并变化轴存在，证据约束比clone-only/固定重构改善后续正确率或成本，当前正确性不明显损失才支持。没有后续收益、轴解释低可靠性、分析token抵消节省、或只有自优化指标变好则停止。

## 4. 后续实验计划

1. 消融spec维度解释、单轴分离证据和历史diff。
2. 同条件下不同actor及预算重复。
3. 按真实需要联合变化和独立变化分组，检查错误抽象。
4. 比较继续编辑与同累计规格重写的配对结果。
5. 展示下一轮重新拆开及成功保留骨架的自然案例。

## 5. 风险与开放问题

需求维度解释仍依赖actor，少量实例不证明未来独立性。当前clone指标降低可能只是优化指标，没有维护收益。AST对齐和重构开销可能更贵；不能用隐藏下一轮规格、完美人工轴标签或额外重构预算制造优势。

## References Used

1. [SlopCodeBench](https://arxiv.org/abs/2603.24755)，任务和提示实验；[公开代码](https://github.com/SprocketLab/slop-code-bench)已读。
2. [MaintainCoder](https://arxiv.org/abs/2503.24260)，动态需求可维护生成近邻。
3. [Incremental Code Clone Detection and Elimination](https://www.cs.kent.ac.uk/pubs/2011/3087/)，anti-unification成熟原理。
4. [CREC](https://arxiv.org/abs/1807.11184)，历史演化/co-change重构近邻。
5. [REFINE](https://arxiv.org/abs/2608.23611)，evidence-guided重构近邻。

没有新的性能、费用或显存结果。
