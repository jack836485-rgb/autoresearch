## 背景

**定位关键词：** interactive coding agents；stateful execution；execution feedback

**一句话定位：** 交互式代码agent在一段程序部分写入后报错时，怎样修复后续计算而不重新执行已完成的效果。

## 核心 Claim

AppWorld明确支持持久Python变量和非回滚API写入；官方FullCode修复把stack trace发回模型重生代码。待验证一个更窄失败：修复虽避开重复写，却把该写返回的对象ID或随后被覆盖的局部值一起丢掉，导致剩余任务无法继续。贡献是以已成功效果的返回值替代原调用，并从失败点重新求值所需纯表达式，使修复保持已有外部效果和其数据依赖；不是一般幂等重试或postcondition验证。

可核验实现：src/appworld/environment.py保留self.shell.user_ns，_shell_run_cell执行IPython；普通API错误之后没有数据库自动回滚逻辑。README明确stateful变量可跨cell复用。FullCode代码_step_three将stack trace接retrial_prompt再生成整段code。只能据此主张入口存在，尚未观察到误恢复比例。instrumentation需新实现，源码核验不是实跑。

## 方法设计的核心思想

首版只支持顶层顺序赋值、表达式、固定列表for循环内直接apis调用；动态eval、嵌套异步和不确定timeout不在首版。CPU对agent自己生成的AST插入调用边界观测，记录执行实例的源码位置、循环索引、真实参数、公开返回及成功/报错；只读agent可获得的数据，不读数据库或task ground truth。错误后根据实际成功写实例划定效果边界，把它们替换为已记录返回值。修复模型只修改失败调用及未执行后缀；数据依赖闭包内的纯表达式允许重算。CPU检查修复是否重新到达已提交写实例；相同源码位置但不同参数的有意新写不能冒充已完成调用。若修复需要改动已完成效果，由原actor显式说明并执行可见补偿或换计划，不能静默跳过。只在已成功回执的范围声称可重用，不以timeout当未执行证据，不做hash/指纹。

## 最小实验

AppWorld train/dev的自然部分执行轨迹先诊断，再对同一失败前缀克隆出的世界进行配对恢复，环境克隆仅评测器使用，controller不可读其状态。对比官方FullCode、强remaining-code提示、只按成功回执跳过写、保存回执但不保留数据依赖、剩余程序求值。核心机制比较共用相同调用边界记录和上下文；另报原生端到端成本。主指标剩余任务完成率、重复写和丢失依赖引发的错误；所有初始失败、仪表记录、修复和工具调用计入总预算。若强提示或简单回执跳过等效，则否定残余求值必要性；不是在受限语法子集有效就宣称全部Python可修。

同一模型快照、相同数据和顺序、相同推理模式/温度/seed/最大步数、相同总输入输出 token、LLM 调用与工具调用上限；机制、反思和检查均计入总预算。参数为实验前待确定项，本轮不运行。只读取 agent 可见输入，不读评价答案/隐藏状态。

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 开源代码与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| 官方FullCodeRefl | 同AppWorld代码执行与错误恢复 | https://arxiv.org/abs/2407.18901 | https://github.com/StonyBrookNLP/appworld；full_code_agent.py、environment.py与README已读 | appworld run auto --agent-name simplified_full_code_agent --model-name {共同actor} --dataset-name dev；所有组同task/seed/API与token cap | 是；未实跑 |
| 强remaining-code提示 | 排除仅把部分执行事实说清楚 | 本地标准对照规范 | 同FullCode；加入成功效果、返回值、失败行并明确不得无意重跑已完成操作 | 与主方法同观测表；actor自由生成剩余code，不做CPU残余变换 | 是 |
| 成功回执去重 | 一般避免重复写的强简单策略 | 本地标准对照规范；VTC仅作原理近邻 | 按执行实例的源码位置/循环索引/已知实际参数直接比较，若已成功写则重用原返回；不求纯表达式依赖闭包 | 同仪表记录、task/actor和预算，不使用幂等键或环境私有数据库 | 是 |
| 无数据依赖的剩余后缀 | 检验返回值/局部依赖保持的独立作用 | 本地机制消融 | 在失败点继续修复，已提交写禁止重跑，但不替换已完成调用为返回表达式 | 同支持语法与执行记录；无效局部变量错误照实计入失败 | 是 |
