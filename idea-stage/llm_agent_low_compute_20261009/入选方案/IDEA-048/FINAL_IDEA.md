## 术语与缩写表

| 术语 | 中文/全称 | 在本方案中 |
|---|---|---|
| Boolean Series / mask | 布尔筛选序列 | 每个bool原本由某个数据行的条件得到。 |
| label alignment | 标签对齐 | pandas按index标签决定bool应用到哪行，标签可能被重新使用。 |
| row identity | 行来源身份 | 从公开输入分配的顺序行ID，随纯行变换传播；普通元数据，不是hash/指纹。 |
| DA-Code / DS-STAR | 数据分析基准／强验证agent | CPU数据分析和API模型，首版只取CSV分析子任务。 |
| RADAR | 数据分析运行时检查 | 已有schema/字段/显式join/提交检查，完整公开实现未核验。 |

## Title

# 标签相同但数据行已变：布尔筛选在数据分析agent中的行绑定诊断

**候选ID：** IDEA-048。**独立审查：** Call33，8.0/10，experiment_ready，无致命阻塞。未运行模型实验。

**定位关键词：** data wrangling；execution feedback；data provenance。

**一句话背景：** 数据分析agent排序或重设索引后复用旧布尔mask时，怎样发现合法标签对齐实际筛选了另一批数据行。

**独立创新点：** 以公开行变换的对应关系验证Boolean Series复用，而非用schema/长度/标签相同充当语义行绑定。

## 1. 引言式概述

### 1.1 任务锚点与最小范围

研究一个Python action内部的CSV数据清理/分析，不做ML训练。首版限定sort_values、过滤、reset_index和列比较形成的Boolean Series，再用[]/.loc选择。join、groupby、改列值或跨action的任意依赖不在首版。

### 1.2 现有方法怎样处理

[pandas](https://pandas.pydata.org/docs/user_guide/indexing.html)按标签对齐布尔Series；RADAR已在DA-Code上用类型化操作与可见检查减少静默错误；已有细粒度dataframe provenance与NBSafety检测陈旧状态。本案不发明对齐/血缘，差别只在mask原行与当前目标行逐位关系。

### 1.3 具体瓶颈与证据边界

可能的自然错误：在原df算mask，排序并reset_index后旧整数标签被重新使用，再套旧mask。代码可跑、dtype/长度相同，却筛另一批行。这个pandas语义后果可推导；是否在DA-Code自然agent轨迹频繁出现仍需盲标，不能由RADAR总体静默错误率替代。

### 1.4 我们实际做什么

我们保留每个bool对应的来源行，跟随纯行变换维护对应关系。应用mask时比较该bool原来源和实际目标，给首个可见错配。默认原actor修代码；纯行重排时按ID重附可作单独消融，未知出处或值已改变不自动修。

### 1.5 最小实验概览

同DA-Code task/data/API模型与完整预算，比DA-Agent、DS-STAR原生、schema/index检查、总是重算mask和行来源诊断。总是重算的便宜控制已经等效时停止。只对少数支持操作有效不能宣称通用数据分析正确性。

### 1.6 拟验证贡献

1. 对标签合法但行身份错配的mask复用做独立诊断。
2. 支持范围内bool来源—目标身份比较及可见反例。
3. 与强原生验证和便宜重算的同预算比较。

## 2. 详细方法计划

### 2.1 方法直觉

一条bool应该继续跟着产生它的那一行，而不是跟着后来重用的整数标签。

1. 为read_csv得到的行分配顺序ID，侧表维护，不改变用户数据。
2. sort/filter/reset_index传播行对应；bool比较保留来源对应。
3. mask实际用于当前df时逐位比较。
4. 返回第一个具体错配和两行可见证据。
5. 原actor重算/调整代码，未知结构保持unknown。

### 2.2 输入、输出与成立条件

输入是公开数据和实际支持操作、bool与df的对应表。输出是身份一致、具体不一致或不支持。只处理按行语义形成的Boolean Series，显式位置数组不纳入；业务上有意的跨表键对齐也不能按“不来自同一物理df”就认定错误。

### 2.3 算法与数据流

侧表用顺序ID而非内容哈希，记录每次纯行变换的旧位置到新位置关系。标签重排本身正常；只有实际应用的bool来源行与当前被选行分离才提供诊断。新列值已改变时旧predicate也可能陈旧，但这是另一问题，不在当前自动重附保证。

pandas正常运行不意味着符合任务；同时，controller发现来源不同也不是业务错误真值。独立标注检查实际意图及合法复用，避免把正常alignment当错误。

### 2.4 最小实现与算力

已读DA-Agent、PythonController、DS-STAR run/coder/debug/verify/router与LLM helper。新增仅支持操作的CPU追踪和反馈；API actor无需GPU。DS-STAR实际debug_round有正确拼写，guidelines.txt源码会无条件读取，需准备同格式说明；LLM helper未统一总token和采样，实验需调用边界统一计账与参数，不能原样声称公平。

## 3. 最小验证实验

### 3.1 目的

先发现自然错误且能与合法alignment区别，再验证行来源证据能否比shape/index或简单重算更好。

### 3.2 数据与切分

冻结DA-Code公开CSV DW/DM/EDA子集，排除ML/重视觉任务。筛选依公开任务与框架支持，不按主方法结果挑任务。dev冻结支持操作，held-out盲标自然mask复用及误筛；所有不支持任务仍在整体成功分母。原始任务评分与配对错误前缀诊断分开。

### 3.3 Baselines（唯一实验baseline定义）

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 开源代码与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| DA-Agent on DA-Code | 同CSV数据分析与表输出 | https://arxiv.org/abs/2410.07331 | https://github.com/yiyihum/da-code；run.py、PromptAgent、PythonController已读 | python run.py --model {共同actor} --task_config da_code/configs/task/dm.jsonl --source_dir da_code/source --max_steps {共同} --max_memory_length {共同} --max_tokens {共同} --example_index {固定} --output_dir {slot}；CPU Docker | 是；未实跑 |
| DS-STAR原生 | 同DA-Code已发表强验证基线 | https://arxiv.org/abs/2509.21825 | https://github.com/google-research/ds-star；run_ds_star.py真实parser、agents/ds_star.py coder/debug/verify/router、tools/llm.py已直接读 | 每公开任务复制instruction到tasks/{id}/question.txt，guidelines.txt提供同格式说明（实际无论是否optional均会读取），source文件到data；python run_ds_star.py --task {id} --llm {共同支持gpt/Gemini快照} --debug_round {cap} --max_round {cap} --max_workers 1；原LLM helper未强制total token，统一补调用边界预算与输出上限/共同采样配置；所有file分析/verify/router计费，不改算法 | 是；源码核验未实跑 |
| 通用mask重算 | 强便宜对照 | 本地标准规范 | 每次sort/filter/reset_index后，用实际支持且保存的原列比较表达式在当前df重算mask；不支持则unknown，不能自动猜predicate | 同采集/表达式与actor，CPU耗时完整记账 | 是 |
| schema/index与runtime checks | 一般可见检查，隔离row identity增量 | pandas规范＋RADAR公开规则，不称复现RADAR | 记录dtype/shape/len、index唯一性，执行SQL时按已见schema验列、要求多行隐式join有显式键；所有规则CPU可直接实现，Python不追加行身份追踪 | 同可见数据、反馈额度与执行预算；RADAR全文无可核验官方代码，不列其原作者算法基线 | 是；标准本地控制 |


同actor/辅助模型、原始文件、task/seed、历史窗口、上下文/输出/步骤与总API/token预算。DS-STAR保留原生计划/分析/verify，全部成本计入。RADAR无已核验完整代码，仅将公开、可完全指定的小规则作为本地控制，不标其原作者分数。

### 3.4 指标

主指标官方table match与task成功，次指标实际误筛行、身份诊断precision/recall、误报、支持覆盖、CPU时间/内存以及全部模型/执行成本。代码不异常不是主终点。

### 3.5 支持和失败条件

自然错配存在，身份检测准确且比廉价控制/DS-STAR改善同预算任务才继续。总是重算已等效、错误罕见、主要操作不支持、误报合法alignment或追踪比重算更贵则停止。

## 4. 后续实验计划

1. 消融来源身份，仅使用label/shape。
2. 分sort、filter、reset_index及组合，检查真正触发条件。
3. 纯行重附与actor提示两臂分开，避免混淆确定性修复和额外推理。
4. 不同actor/数据量下记录CPU/RAM及模型成本。
5. 展示真实错配、合法对齐和unknown三类案例。

## 5. 风险与开放问题

初版行变换覆盖很窄，自然频率可能低。追踪ID不能替代语义意图；位置选择/合法键对齐必须排除。改列值后旧谓词是否有效不在当前保证。简单重算可能始终更便宜，必须以它为硬停止对照。

## References Used

1. [DA-Code](https://arxiv.org/abs/2410.07331)，[代码](https://github.com/yiyihum/da-code)，同任务。
2. [DS-STAR](https://arxiv.org/abs/2509.21825)，[代码](https://github.com/google-research/ds-star)，强同任务API基线。
3. [RADAR](https://arxiv.org/abs/2609.32528)，已读规则，完整代码未核验。
4. [pandas indexing](https://pandas.pydata.org/docs/user_guide/indexing.html)，标签/布尔语义。
5. [Fine-grained Provenance](https://arxiv.org/abs/2310.18079)，2024，成熟行级血缘近邻。
6. [NBSafety](https://arxiv.org/abs/2012.06981)，2021，陈旧notebook状态近邻。

没有新的性能、费用或显存结果。
