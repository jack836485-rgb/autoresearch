## 背景

**定位关键词：** dual-control；conversational agents；communication and coordination

**一句话定位：** 客服 agent 如何在用户也改变环境时更新先前已知的设备状态。

## 核心 Claim

τ²-bench 报告 dual-control 比 no-user 更难，但未证明主要是陈旧状态。待诊断假设：用户执行动作可能使先前状态事实失效，模型继续沿旧事实排查。主张只撤销被用户动作影响的已知事实，避免全部重问和错误沿用。

真实任务存在用户共享控制及重新查状态要求；被忽视的可能变量是状态来源与动作影响；候选让动作触发局部未知；若没有陈旧事实失败或全部重问等效，则否定机制。

## 方法设计的核心思想

维护事实=值+可见来源+相关公开动作类型；用户说已执行动作后，先标记相关事实未知，必要时向用户询问新的可观察状态。不访问 user tool 隐藏日志，不把“我做了”当环境成功。映射由模型从公开 policy/schema 在任务前生成，CPU 更新。

## 最小实验

固定修正后 telecom 文本任务与模拟器；先在可见对话中人工标注动作之后仍用旧状态的案例，以最终环境状态只作离线分析；对照 LLMAgent、结构化状态提示、全部失效、选择性失效，统一 user turns/工具/LLM token预算。指标 pass^1、陈旧状态使用、重复提问。

同一模型快照、相同数据和顺序、相同推理模式/温度/seed/最大步数、相同总输入输出 token、LLM 调用与工具调用上限；机制、反思和检查均计入总预算。参数为实验前待确定项，本轮不运行。只读取 agent 可见输入，不读评价答案/隐藏状态。

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 开源代码与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| 官方 LLMAgent | conversational agents、dual-control、telecom | https://arxiv.org/abs/2506.07982 | https://github.com/sierra-research/tau2-bench；已读取 src/tau2/agent/llm_agent.py 和 agent/README.md；当前仓库为 τ³，使用其修正后的文本 telecom，不混称原论文分数 | uv sync；tau2 run --domain telecom --agent-llm {同一模型} --user-llm {固定模拟器} --num-trials {固定次数} --num-tasks {固定任务数}；自定义 agent 通过 HalfDuplexAgent.generate_next_message 注册 | 是 |
| 结构化状态提示 | 相同对话和工具场景，排除仅增加提示格式的收益 | https://github.com/sierra-research/tau2-bench/blob/main/src/tau2/agent/README.md | 标准本地对照：每轮用同一个 LLM 输出固定 JSON 的目标/已知事实/待办并作为下轮输入；不接入隐藏用户工具日志或评价 | 同一 LLMAgent 派生；同预算加入一份状态表，但没有本候选特有的更新机制 | 是 |
