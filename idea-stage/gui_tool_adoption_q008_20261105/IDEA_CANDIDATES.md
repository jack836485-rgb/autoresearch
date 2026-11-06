# Idea 候选池

- 输入模式：`problem_card`
- 输入论文：不适用
- 输入问题卡：`path-stage/GUI_Agent研究地图_20261104/` 的 `Q008`

## 当前选择

- Reviewer 调用：`0 / 30`
- 当前选中 Idea：无
- 状态：`停止（未送审）：送审前查新发现 ToolCUA 已用按任务的工具有益标签做奖励，见 PIVOT_OR_STOP.md`

## 候选列表

### IDEA-001：问题卡切口——分解采用率上升后的失败

- 来源：`问题卡切口`
- 父 Idea：`无`
- 状态：`needs_revision`
- 定位关键词：OSWorld-MCP；tool invocation；computer-use agent
- 一句话背景：混合 GUI–工具 agent 采用率被奖励拉高后准确率不变。
- 与起点问题的关系：原问题；诊断。
- 主贡献：按调用时机、参数化、调用后上下文分解失败。
- 贡献自评：重要性 6.0 / 新颖度 5.0 / 有效性 5.5。
- 自评分：`5.3/10`
- 打分理由：诊断种子；Hybrid Computer Use（Microsoft Research，2026-10）已报告畸形参数调用 17.4%→1.4%（技能 + 动作守卫）。
- Reviewer 记录：`尚未送审`

### IDEA-002：按策略实测的任务级工具优势预测采用型 RL 的收益，并据此门控采用奖励

- 来源：`最高近邻不足`
- 父 Idea：`IDEA-001`
- 状态：`covered`
- 定位关键词：OSWorld-MCP；tool invocation；reinforcement learning；reward shaping
- 一句话背景：稠密采用奖励提高采用不提高准确率（2608.03327），工具调用任务成功率更低（writer 42% 对 82%）。
- 与起点问题的关系：原问题。
- 主贡献：测试时实测 Δ_T = acc(强制工具) − acc(纯 GUI)，预测采用型 RL 在各任务上的准确率变化，并只在 Δ_T>0 的任务上给采用奖励。
- 贡献自评：重要性 6.5 / 新颖度 5.0 / 有效性 6.0。
- 自评分：`5.8/10`
- 打分理由：ToolCUA（arXiv:2605.12481，§2.4）的 R_tool = I_succ·I[(t_b>0∧c>0)∨(t_b<0∧c=0)] 已按任务的工具有益标签 t_b（来自 OSWorld-MCP 任务标注、人工核验）奖励"该用时用、不该用时不用"；ToolCUA 附录 C.1 也已报告加工具后多个模型掉点（EvoCUA-32B 52.6%→40.5%、Claude-4.5-Sonnet 61.9%→48.4%），归因为过度切换。剩余增量只是"按策略实测的优势代替静态标注"。另 ToolCUA 训练用 8×8 卡训练 + 4×8 卡推理 + 约 250 个 Docker 实例，超出用户算力。
- 自评分轻量新意依据：WebFetch 读取 ToolCUA §2.4 与附录 C.1。
- Reviewer 记录：`未送审`
