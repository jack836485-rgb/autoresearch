## 术语与缩写表

| 术语 | 中文/全称 | 在本方案中 |
|---|---|---|
| JSON提取器 | 无I/O表达式/短函数 | 从一个公开工具返回提取后续使用值，不能再次调用API。 |
| finite observational preservation | 有限观测保持 | 修补在指定旧JSON上返回原观测值；不意味着这些值语义正确。 |
| candidate repair | 候选修补 | 同一次actor修复轮生成最多3个提取器，CPU验证。 |
| CEGIS | Counterexample-Guided Inductive Synthesis | 用反例排除候选的成熟思路；本案不发明它。 |
| AppWorld / ACE | 应用环境／增量context agent | 同任务复现入口与强执行反馈对照。 |

## Title

# 修复工具返回提取器时，用已有公开样本排除破坏旧访问的候选

**候选ID：** IDEA-050。**独立审查：** Call35，8.0/10，experiment_ready，无致命阻塞。未运行模型实验。

**定位关键词：** API documentation；interactive coding agents；execution feedback。

**一句话背景：** 交互式代码agent即使有正确工具文档，仍可能访问不存在字段或误用当前返回；怎样以局部执行证据修复。

**独立创新点：** 不重跑工具或调用critic，用已观察过的真实JSON与原提取输出验证修补候选的有限行为保持。

## 1. 引言式概述

### 1.1 任务锚点与最小范围

限定原始AppWorld完整API文档下的纯JSON提取器修复。没有后台API重放、额外任务rollout、critic或模型训练。一个actor修复轮最多3个候选；所有候选生成、历史序列化和CPU测试都计入预算。

### 1.2 现有方法怎样处理

AppWorld报告字段臆造和接口误用。LDB与VeriHarness已有局部运行时/结构化反馈，ACE已有执行经验；程序修复也早已同时修失败测试并保持旧通过测试，Agentless Mini和Tool-Making是重要先例。当前新意只限tool agent自己已经观察过的JSON与输出、无gold的纯提取器修补验证。

### 1.3 具体瓶颈与证据边界

更窄待诊断假设：为当前empty/None或嵌套结构修补提取器，可能改变它对其它已有适用返回的行为。一次错误定位只告诉哪里坏，不保证该修补保留其它观测。发生率和任务效应均未知；此前成功访问也可能给过语义错误值。

### 1.4 我们实际做什么

我们让同一修复轮提出少量纯候选，在当前失败结构和已有适用样本上CPU重放；除检查异常/类型外，还检查需保留的原观测值。失败候选收到具体反例，剩余候选由原actor判断语义。无需新增API调用，也不把旧输出变成正确答案。

### 1.5 最小实验概览

同样最多3个候选、样本/原值/上下文和预算，对比只测当前失败、多样本结构测试及观测值保持；加官方FullCode、强局部提示和ACE原生。只有观测保持的独立增量改善真实TGC/成本，才说明这层验证值得做。

### 1.6 拟验证贡献

1. agent已可见历史输入输出的有限保持约束。
2. 无环境重跑的纯候选CPU验证与反例。
3. 候选数量/信息/预算严格相同的机制消融，以及非真值保持风险诊断。

## 2. 详细方法计划

### 2.1 方法直觉

修这一次错误前，先在自己已经见过的输入上检查有没有又改坏其它行为。

1. 保存当前提取器适用旧JSON与真实观测输出。
2. 修复轮生成最多3个纯候选。
3. 当前样本只验证可执行，不提供gold值。
4. 旧样本验证有限输出保持，给冲突反例。
5. 原actor选语义上合理候选，并继续原任务。

### 2.2 输入、输出与成立条件

输入是当前失败返回、同一提取器旧适用样本/输出、事前声明的保留范围及候选函数。输出为通过候选或明确反例。只支持无I/O有限表达式、dict/list访问、guard、基础转换与简单组合；跨接口/版本不能随便混样本。

### 2.3 算法与数据流

对每个旧适用输入执行候选，比较原观测输出的实际值和类型，不用哈希。原actor若认为某些旧行为本来就应改变，必须在生成候选前说明并从保留范围移出；不得事后删反例让候选通过。

无条件None/空值可能结构无异常，但不能据此完成任务或删掉必需后续动作。当前样本可执行、旧值保持都只是必要的有限检查，不证明选了正确业务字段，也不保证未来输入。旧行为原来有错时保留可能有害，必须独立报告。

### 2.4 最小实现与算力

基于已核验AppWorld FullCode/持久Python调用记录及ACE no-GT。新增提取器样本集与纯函数CPU测试；不执行未确认I/O候选，不重做工具效果。CPU可能在JSON很大时花费明显内存/时间，需要测量；样本保留与模型输入都计费，不能以不训练为理由忽略成本。

## 3. 最小验证实验

### 3.1 目的

先确认当前修补导致旧观测变化且影响任务的自然病例，再验证值保持是否超越只测当前或多样本类型。

### 3.2 数据与切分

原始AppWorld train/dev自然字段/访问错误，完整schema不变。开发冻结支持提取器与样本适用规则；同错误前缀配对恢复与自然held-out端到端分开。所有组看到同原始样本/原值和访问错误，不能给主方法额外真实返回或人工正确保留集。

### 3.3 Baselines（唯一实验baseline定义）

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 开源代码与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| 官方ReAct/FullCode | 同AppWorld schema-blind任务 | https://arxiv.org/abs/2407.18901 | https://github.com/StonyBrookNLP/appworld；真实agent、ApiDocCollection.load/remove_fields及environment已读 | appworld run auto --agent-name simplified_full_code_agent（或simplified_react_code_agent） --model-name {共同actor} --dataset-name dev；主实验原始完整文档/真实环境，blind消融另报 | 是；未实跑 |
| 强局部修复提示 | 排除告知成功行为保留即可解决 | 本地完整标准控制 | 同原始样本/旧输出、失败访问和明确保留要求，原actor提一次修补；不做CPU候选重放 | 同actor/总token/API cap，辅助样本序列化计费 | 是 |
| 候选当前测试/多样本结构测试 | 隔离候选数与旧观测值约束 | 本地完整标准控制 | 所有候选组同最多3个候选；一组只检当前样本可执行，另一组检所有适用样本无异常及类型；主方法另要求保留既有观测值 | 限定纯表达式，实测CPU；不生成新任务/不使用gold | 是 |
| ACE no-GT on AppWorld | 同任务执行反馈增量context强近邻 | https://arxiv.org/abs/2510.04618 | https://github.com/ace-agent/ace-appworld；adaptation_react.py、adaptation_agent、generator/reflector no-GT提示和config真实内容已读 | 从已核验ACE AppWorld fork源码安装；appworld run ACE_offline_no_GT_adaptation再ACE_offline_no_GT_evaluation，或ACE_online_no_GT；主比较均保留完整API文档，统一actor/reflector/train流/全部构建与query预算，不给GT或免费playbook | 是；未实跑 |


候选组最多3个、同生成token cap与修复机会；FullCode/ACE原生结果另报，保持其算法和完整构建/反思预算。actor/reflector使用同能力快照，task、seed、few-shot、步骤、工具/LLM与总token固定。

### 3.4 指标

主指标TGC和真实恢复轮数；机制指标当前错误解决却旧观测回归、值保持相对结构测试的效果、vacuous候选、错误旧值被保留的比例。次报完整调用/token/费用、CPU时间/RAM和样本覆盖。不以CPU测试通过率代替成功。

### 3.5 支持和失败条件

自然旧行为回归存在，同候选数/信息/预算下观测保持比结构测试有益，且没有靠保留错误旧值或跳过任务得到假好结果才继续。结构测试已够、样本少/不适用、主要旧值错、或更少异常但TGC下降时停止。

## 4. 后续实验计划

1. 消融旧观测值，只保留多样本结构测试。
2. 同预算改变候选数与样本覆盖，每组内部参数公平。
3. 分empty/null/嵌套结构与本来需改旧行为的错误。
4. 衡量JSON规模、CPU/RAM和样本序列化成本。
5. 展示一条避免旧行为回归和一条错误旧值被保留的真实轨迹。

## 5. 风险与开放问题

有限保持不是语义正确。旧输出可能错，未来返回可能不同，适用样本也可能混错。纯提取器边界窄；将整个有副作用代码放进重放会改变问题，因此首版严格保持无I/O范围。简单结构测试可能已经足够。

## References Used

1. [AppWorld](https://arxiv.org/abs/2407.18901)，同任务公开实现。
2. [ACE](https://arxiv.org/abs/2510.04618)，[AppWorld fork](https://github.com/ace-agent/ace-appworld)，强baseline。
3. [SWE-RL / Agentless Mini](https://arxiv.org/abs/2502.18449)，候选修复与旧通过测试近邻，非同任务baseline。
4. [Tool-Making](https://arxiv.org/abs/2607.08010)，执行trace/schema/value与候选工具验证近邻。
5. [VeriHarness](https://arxiv.org/abs/2607.14167)，结构化反例近邻。
6. [LDB](https://arxiv.org/abs/2402.16906)，已读局部运行时调试。

没有新的性能、费用或显存结果。
