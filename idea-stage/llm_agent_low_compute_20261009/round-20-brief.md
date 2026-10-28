## 背景

**定位关键词：** temporal execution windows；tool discovery；behavioral reasoning

**一句话定位：** 工具agent如何在触发短时状态后，把探索调用与必须重新取得的瞬态值分开安排。

## 核心 Claim

ScrambleToolBench原文报告window过期导致session值失效，成功agent停止探索而快速执行，但部分失败agent混淆reset。待诊断：任务recipe正确仍会在窗口内探索稳定schema或重用过期值，消耗不可恢复机会。主张预算门槛前先完成可跨reset复用的能力验证，触发后只获取本次状态的必要值；仅将“少探索”作为统一提示无法表达该区别。

窗口造成值重置是原作者已经展示的真实失败；可能关键是稳定工具知识和瞬態执行值在时序上要求相反；把稳定探索移到窗口前并让易失值每次新取；窗口内少调用却总体更多或无成功收益不支持。

## 方法设计的核心思想

从已有可见轨迹和任务recipe给依赖项标记：接口/参数结构可复用，任务当次输出暂存。迁移带setup成本与易失中间结果的调度：原actor在正常一轮提出触发动作以及之后必要调用的依赖计划，CPU检查已知schema/合法arg是否有支持；未知接口先在触发前探测，依赖触发后才产生的值不可提前探测。window/reset标志出现后新建易失值作用域，但保留接口知识，原actor只收到本次可用参数。不是回滚副作用/通用done gate，不预测隐藏counter，不知道任务正确solution。

## 最小实验

同一ScrambleToolBench +Window，先人工/日志诊断“已知recipe但窗口内重复稳定探测”和“reset旧值复用”。官方default、完全规范的本地结构化知识表、强提示先计划再trigger、所有值清空、两阶段稳定/瞬态调度；同模型、窗口大小、seed、task/总action/token。先固定无drift/no failure再组合，记录触发前准备成本及失败窗口也入总预算，防止把探索藏在前段。支持是减少窗口内无效探测/旧值复用并提高完成，且总调用不增加；若普通提示已足够或必须oracle知道trigger/依赖，则否定。

同一模型快照、相同数据和顺序、相同推理模式/温度/seed/最大步数、相同总输入输出 token、LLM 调用与工具调用上限；机制、反思和检查均计入总预算。参数为实验前待确定项，本轮不运行。只读取 agent 可见输入，不读评价答案/隐藏状态。

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 开源代码与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| 官方default | 相同tool discovery/短时window任务 | https://arxiv.org/abs/2608.02358 | https://github.com/declare-lab/ScrambleToolBench；已读agent/env/tasks/runner；get_agent_class仅接受default，未公开memory实现 | python scripts/run_benchmark.py --backend openrouter --model {共同actor} --agent_type default --tasks 5 --episodes {N} --seed 42 --steps_per_task {cap} --window_size 10；CPU | 是 |
| 强提示Plan-before-trigger | 同任务的简单两阶段规划 | 完整本地标准规范 | 同actor提示先确认稳定接口和参数再trigger，reset后不要复用瞬態值；没有CPU标签与可用性维护 | 同runner与总token/action cap，前后探索都计费 | 是 |
| reset全部清空 | 排除只是重新取值 | 完整本地标准规范 | 相同memory格式，公开reset时清空全部工具表与任务值，不读隐藏状态；原actor重新发现 | 同window/cap/模型/task；计入重发现开销 | 是 |
| 结构化知识表 | 同tool discovery/window任务，隔离只显式保存知识的收益 | 论文§3.1+本地完整简单控制规范 | 不冒充未公开的官方memory：本地标准表存actor在原轮次声明的已发现alias/参数与流程步骤，serialize到下一轮；只按actor更新，不按稳定/瞬态调度 | 同default get_action输出增加memory_update；CPU合并JSON；所有建表输出和序列化输入token计费，不添加后台调用 | 是；本地标准控制，非原作者复现 |
