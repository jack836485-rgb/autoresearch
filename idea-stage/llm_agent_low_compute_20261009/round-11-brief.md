## 背景

**定位关键词：** conversational agents；multi-turn interaction；policy compliance

**一句话定位：** 工具客服 agent 如何在用户修改一项需求后保留其他仍有效的任务约束。

## 核心 Claim

AppWorld-UL 报告用户回复后遗忘旧要求。假设普通目标摘要容易把最新要求当完整替换。主张把用户变化当局部约束编辑，仅重查与编辑相依的决定，保留不相关要求。

最新用户回复会带来目标变化且旧要求遗忘已有证据；关键可能是修改的作用域；对变化传播到相依决定但不覆盖整目标；如果只要列要求就等效，否定依赖传播创新。

## 方法设计的核心思想

初始目标拆成可追溯要求；用户回复由同一模型输出增加/撤回/更改哪项要求；CPU 标记引用改变项的计划决定需要重新评估，其余要求继续保留。不自动撤销已执行操作，必要时向用户解释可行性。

## 最小实验

修正后的 retail 文本任务，预定义用户改变颜色/数量/退款方式且保留其他约束的交互诊断扩展；官方原分数与扩展分别报告。LLMAgent、每轮全量重新摘要、逐项保留无依赖、局部重开对照。相同 turns/tokens，指标旧要求违反、过期决定沿用、成功。

同一模型快照、相同数据和顺序、相同推理模式/温度/seed/最大步数、相同总输入输出 token、LLM 调用与工具调用上限；机制、反思和检查均计入总预算。参数为实验前待确定项，本轮不运行。只读取 agent 可见输入，不读评价答案/隐藏状态。

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 开源代码与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| 官方 LLMAgent | conversational agents、dual-control、telecom | https://arxiv.org/abs/2506.07982 | https://github.com/sierra-research/tau2-bench；已读取 src/tau2/agent/llm_agent.py 和 agent/README.md；当前仓库为 τ³，使用其修正后的文本 telecom，不混称原论文分数 | uv sync；tau2 run --domain telecom --agent-llm {同一模型} --user-llm {固定模拟器} --num-trials {固定次数} --num-tasks {固定任务数}；自定义 agent 通过 HalfDuplexAgent.generate_next_message 注册 | 是 |
| 结构化状态提示 | 相同对话和工具场景，排除仅增加提示格式的收益 | https://github.com/sierra-research/tau2-bench/blob/main/src/tau2/agent/README.md | 标准本地对照：每轮用同一个 LLM 输出固定 JSON 的目标/已知事实/待办并作为下轮输入；不接入隐藏用户工具日志或评价 | 同一 LLMAgent 派生；同预算加入一份状态表，但没有本候选特有的更新机制 | 是 |
| AgentSWE Plan-Reason-Verify-Act | 同一tau2 telecom/retail对话任务，结构化state/plan/verify近邻 | https://rdi.berkeley.edu/agentx-agentbeats.html | https://github.com/soumya-batra/tau2-agentbeats；已读取README、src/agent.py评测adapter与agent-template/src/agent.py真实actor；其self._plan持久化plan/state并生成Plan-Reason-Verify-Act JSON | agent-template目录uv sync；AGENT_LLM环境变量设为共同actor；uv run src/server.py启动purple server；root目录uv run src/server.py启动tau2 green evaluator；相同task IDs/seed/模型/工具与整体token预算，不沿用README大模型分数 | 是；源码验证，集成未实跑 |
