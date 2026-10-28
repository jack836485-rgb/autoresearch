## 术语与缩写表

| 术语 | 中文/全称 | 在本方案中 |
|---|---|---|
| SWE-bench | 真实仓库issue修复基准 | agent改代码，隐藏评测仅离线用于resolved。 |
| pytest nodeid | 测试唯一名称 | 定位同一个已执行测试；源码变了则不作同一检验比较。 |
| P→F / F→P | 通过到失败／失败到通过 | 前后两轮共同测试的可观察状态变化，不等于唯一根因。 |
| head-tail | 输出头尾裁剪 | MiniSWE超过10000字符时保留各5000字符。 |
| TDAD / TestLoc | 影响分析／测试定位方法 | 改变选了哪些测试，保留其原生能力作强比较。 |
| Squeez | 工具输出剪枝 | 按当前任务压缩一次原始输出的已有方法。 |

## Title

# 固定测试策略下的跨轮回归反馈分配，直接对照测试定位与输出剪枝

**候选ID：** IDEA-046。**独立审查：** Call31，8.2/10，experiment_ready，无致命阻塞。未运行模型实验。

**定位关键词：** software engineering agents；execution feedback；SWE-bench。

**一句话背景：** 编码agent在多次修复后，怎样从有限测试输出中看到本轮新引入的回归，而不是继续追旧的报错。

**独立创新点：** 将agent上轮与本轮已执行公共测试的状态变化用于有限反馈预算，而非按输出位置裁剪或只聚合本轮失败。

## 1. 引言式概述

### 1.1 任务锚点与最小范围

在SWE-bench修复轨迹内研究实际pytest反馈，新增部分CPU做确定性状态比较，无模型训练。actor使用API；已有Squeez模型只做推理，原2B与150M版本分别报告，不混淆结果。

### 1.2 现有方法怎样处理

MiniSWE当前配置按字符头尾裁剪工具输出。TDAD和TestLoc提供高价值选测与回归控制，Squeez压缩pytest/stacktrace，AgentDevel已有P→F原语。不能把测试状态差分或输出压缩声称为首创；本案只利用同一条修复轨迹的共同测试变化来安排有限在线反馈。

### 1.3 具体瓶颈与证据边界

待诊断：旧失败和重复日志占据头尾，本轮新增回归被藏在中段，只有命令级returncode无法告知agent它又破坏了什么。公开配置证明裁剪入口，未证明自然遮蔽频率或后续误修因果链。若没有这类失败，不继续完整实验。

### 1.4 我们实际做什么

我们对两轮共同执行且测试源码未改的nodeid比较状态，先让同一反馈预算展示新增P→F及断言，再展示原有失败。没有前次可比结果时采用单次结构化反馈；skip/未跑不是通过。完整日志仍可供各组相同预算下请求。

### 1.5 最小实验概览

选测策略与反馈策略分开：保留原生、TDAD、TestLoc三类选测能力，每类内部比较头尾、结构化、聚类、Squeez和状态差分。必须在同选测支持、预算和机会下改善resolved/回归，不能把更好选测的收益当反馈机制收益。

### 1.6 拟验证贡献

1. 对真实修复轨迹的跨轮共同test状态建立低成本反馈。
2. 自然回归遮蔽及决策后果的独立诊断。
3. 原生选测×呈现的归因比较，隔离差分的增量。

## 2. 详细方法计划

### 2.1 方法直觉

告诉agent“这次新坏了什么”，再让它决定修什么。

1. 共用pytest plugin记录公开test的nodeid、执行状态及断言。
2. 比较共同已跑且源码未变的test。
3. 将P→F置于固定反馈前部，报告其数量和代表证据。
4. 剩余空间呈现原有失败，重复直接按异常/首项目帧分组。
5. 原actor继续修复；完整日志访问照常计费。

### 2.2 输入、输出与成立条件

输入是两轮实际公开测试结果、测试源码和原始日志。输出是受限token的状态变化反馈。需要可稳定定位测试，不能将未收集、skip、timeout或修改fixture后改变的test当成相同通过证据。比较仅限共同支持，不外推未跑的suite。

### 2.3 算法与数据流

前次pass、本次fail标为新回归；前次fail、本次pass标为修复。原测试源码用实际文本比较，不加hash；测试源或已知fixture被改则标不可比。反馈先给变化总数，再填test ID、首项目帧和具体断言，剩余原失败按冻结顺序。

它不判断是哪行改动造成失败，也不使用SWE-bench隐藏P2P/F2P标签。若结果不稳定，差分只能作可观察变化，需要另报flaky边界。不能只选好看的、完整两次测试的轨迹进入总resolved分母。

### 2.4 最小实现与算力

已读MiniSWE default/benchmark runner/config，TDAD CLI index/impact/run-tests，TestLoc真实4阶段pipeline，Squeez extractor的device与extract。API actor和CPU测试容器；Squeez可显式device=cpu，CPU内存和时长必须测量，源码提供路径不等于已跑通。所有额外选测、定位LLM、覆盖收集、日志采集和反馈序列化计入总预算。

## 3. 最小验证实验

### 3.1 目的

先确认自然遮蔽链，再检验状态差分是否超越现有压缩、选测与回归策略。

### 3.2 数据与切分

SWE-bench公开pytest可运行的实例，按公开框架支持筛选而非主方法结果筛选。开发冻结规则，held-out固定实例和seed；全部组同repo/issue/actor/模型推理、温度、上下文/输出、API与命令cap。原生端到端结果与共同已执行测试的机制诊断分开。

### 3.3 Baselines（唯一实验baseline定义）

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 开源代码与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| MiniSWE on SWE-bench | 同真实issue修复与repository tests | https://arxiv.org/abs/2310.06770 | https://github.com/SWE-agent/mini-swe-agent；default.py、run/benchmarks/swebench.py与swebench.yaml已读 | mini-extra swebench --model {共同API模型} --subset lite --split test --slice {固定范围} --config {各臂同cap配置} --workers 1 --output {slot}；CPU Docker/x86 Linux | 是；未实跑 |
| pytest简短反馈 | 强便宜已有测试呈现 | https://docs.pytest.org/en/stable/how-to/output.html | 本地标准命令控制：--tb=short，不改已选suite；另将--maxfail视作较少执行的独立强控制并完整记录未跑test | 同MiniSWE和反馈token cap，maxfail未跑不能算通过 | 是 |
| 单次结构化输出 | 排除只是删除噪声日志 | 本地完整标准对照 | 同plugin本轮test状态、首项目帧与断言，按nodeid排序装入同token上限，无跨轮比较 | 同已有结果、相同日志访问预算 | 是 |
| 仅失败聚类 | 排除相似失败去重 | 本地完整标准对照 | 按exception类型与首项目栈帧直接分组，逐组轮转取代表+数量，不计算pass-to-fail差分 | 同采集/执行/反馈cap，无hash或额外LLM | 是 |
| TDAD原生选测 | 同SWE-bench回归控制最高近邻 | https://arxiv.org/abs/2603.17973 | https://github.com/pepealonso95/TDAD；tdad/src/tdad/cli.py已直接读，NetworkX index与impact真实分支 | pip install -e tdad；tdad index {repo}；tdad impact {repo} --files {changed}；tdad run-tests {repo} --tests {nodeids}；其skill/map给相同MiniSWE actor，索引和测试费用全计入 | 是；未实跑 |
| TestLoc/TestPrune原生 | 同SWE-bench公开测试定位/缩减 | https://arxiv.org/abs/2510.18270 | https://github.com/IBM/Issue-Test-Localizer；run_pipeline.py真实4阶段及README的tools/regression_tests集成已核验 | python src/run_pipeline.py --instance_id {iid} --model {共同actor} --dataset princeton-nlp/SWE-bench_Verified --log_dir {slot} --max_workers 1；minimized_tests.json按官方regression_tests工具接同MiniSWE，不用免费预计算gold；定位LLM/coverage开销计费 | 是；源码核验未实跑 |
| Squeez输出剪枝 | 同pytest/stacktrace反馈压缩最高近邻 | https://arxiv.org/abs/2604.04979 | https://github.com/KRLabsOrg/squeez；真实ToolOutputExtractor.__init__、transformers/highlighter CPU分支、extract已直接读 | ToolOutputExtractor(model_path=KRLabsOrg/squeez-2b,device=cpu,max_length={公开支持限}).extract(task={同issue},tool_output={原始日志})；150M模型KRLabsOrg/verbatim-rag-modern-bert-v2另报，不混称2B结果；CPU时间/内存计入且无训练 | 是；未实跑 |


每种原生选测策略内部固定测试来源和执行预算，反馈策略不免费追加tests；另报告完整组合端到端。Squeez原2B与其150M替代不混称；无训练或本地GPU强制要求。主方法plugin信息全部对照可见，不提供免费失败前测试。

### 3.4 指标

主指标resolved及实际后续回归；诊断是新增P→F在原头尾中是否可见、agent是否响应，以及无谓修复次数。完整token、测试执行/coverage、辅助模型、CPU时间/内存和费用全部报告。不能只报输出压缩比例。

### 3.5 支持和失败条件

需要真实遮蔽，差分在固定选测策略内比Squeez/单次结构化有效，最终resolved或回归改善且成本公平。短pytest已足够、变化只来自flaky、公共支持过少或强选测已消除遮蔽则止损。

## 4. 后续实验计划

1. 去除差分，只保留同样结构化与聚类，测独立增量。
2. 比较原生/TDAD/TestLoc各自的结果，保持原方法能力。
3. 分长短输出和真实新增回归，确认触发条件。
4. 不同actor和预算，每个设置内部保持公平。
5. 展示一次遮蔽导致误修和一次差分误报的真实轨迹。

## 5. 风险与开放问题

自然遮蔽规模未验证；共同测试支持可能少，flaky也可能产生P→F。测试/fixture变化不能被忽略。辅助Squeez CPU开销与测试定位成本可能大，不能只算主actor费用。只改善可见率却不改善任务不是成功。

## References Used

1. [SWE-bench](https://arxiv.org/abs/2310.06770)，任务；[MiniSWE](https://github.com/SWE-agent/mini-swe-agent)实际runner/config已读。
2. [TDAD](https://arxiv.org/abs/2603.17973)，[实现](https://github.com/pepealonso95/TDAD)，原生选测基线。
3. [TestLoc/TestPrune](https://arxiv.org/abs/2510.18270)，[实现](https://github.com/IBM/Issue-Test-Localizer)，原生选测基线。
4. [Squeez](https://arxiv.org/abs/2604.04979)，[实现](https://github.com/KRLabsOrg/squeez)，输出剪枝基线。
5. [AgentDevel](https://arxiv.org/abs/2601.04620)，发布版本flip原语近邻。
6. [Tokenmaxxing](https://arxiv.org/abs/2607.22807)，离线测试向量近邻，reviewer检索。
7. [SWE-Pruner Pro](https://arxiv.org/abs/2607.18213)，内部表示/训练剪枝近邻，非首版无训练机制。

没有新的性能、费用或显存结果。
