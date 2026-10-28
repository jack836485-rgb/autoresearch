## 背景

**定位关键词：** LLM agents, procedural memory, sequential randomization, causal excursion effect

软件/知识工作agent在任务中反复看到同一经验时，当前执行状态已被先前暴露所改变；任务级价值与现在再次呈现的边际价值不是同一个量。

当前目标及演化依据：从计划编辑转向任务内再暴露的历史依赖，预计处理局部暴露的成本负迁移；不声称根据task内部效应决定永久淘汰。

https://arxiv.org/html/2608.24876：§2.2.2以草拟call/turn boundary事件触发技能；当前工作状态为以前技能/动作所影响的变量，不能把状态分层后的效应当起始总体效应。
https://arxiv.org/html/2610.02070：§2-3随机检索暴露识别query-conditioned effect；本版不重提positivity或把query效应聚合当保留价值。
https://arxiv.org/html/2502.13500：Distal causal excursion effect在动态治疗状态/过去干预会影响后续变量时，以明确参考干预制度比较当次干预的终末效应。
https://arxiv.org/html/2606.15017：辅助经验调用/提示占用执行机会，需与同总费用普通actor比较。
https://arxiv.org/html/2403.08978：Algorithm2在每步状态选择建议并生成动作；再次提醒的时序和效果历史不能仅用current-context matching当识别结果。

## 核心 Claim

待验证：对曾经有益经验，任务中再次呈现可能增加重复验证而不提高终态成功；只有估计在真实历史分布下‘现在再暴露vs不再暴露’的终末边际效应，才能判断是否续发，不能用无经验总体对照或当前状态相关性代替。

## 方法设计的核心思想

开发阶段在预先公开定义的执行事件随机决定是否再次在最新上下文呈现同一经验（已存在的历史不删除），记录已知概率、过去暴露次数、公开工具receipt和本次费用。每个比较以同一既有历史制度为参照，并将后续再暴露按共同参考制度随机化，用居中/倾向加权回归估计续发对终态成功及成本的效应。测试冻结续发规则：同样检索但只在该公开状态/过去暴露次数的终末净效应有开发支持时再次发送；技能库保留不改，不声称‘不续发’消除了旧经验的作用。 可观察状态按工具receipt/任务明确约束与既有暴露记录构成，不用金标准子目标状态。与mHealth MRT不同，LLM的经验正文可能一直留在历史，因此处理定义为‘追加当次经验块’，反事实为‘不追加’，并不假设洗脱或遗忘；既有历史分布与后续随机制度必须相同。

最高近邻及差别：Recuris已有事件时技能检索，CMP有随机检索，动态治疗文献已有MRT/DCEE。本版候选只在区分‘重复提醒的边际效应’与‘经验总体价值’上可能成立；不把换到时序回归当充分新意。 AutoGuide已每步生成指南，本方案不宣称再暴露这一动作新；待区分的是无洗脱的增量处理能否产生近端/终末效应冲突，并指导较节省的提醒制度。AEWM已保留正常草拟动作，本方案不再使用该关系作新意。

## 最小实验

AppWorld train库/dev随机事件/test冻结；同actor/解码/任务/技能内容/可用动作/全链路总费用，比首次只发一次、每个匹配事件都再发、Recuris式事件检索、仅按当前state分层的续发、历史制度明确的终末效应续发。train/dev做逐任务机制分析；official test只报告aggregate成功/全部任务、续发次数和总费用。分首次/重复呈现的效应仅开发数据估计。近端‘验证成功’不能替代任务终态；旧提示及后续调用费用均计。若一般不重复注入已等效、无历史相关效应、或同费用控制器等效，则推翻。事件集合、随机概率、样本量、lambda/模型/费用上限待用户确认。

基线定义/复现：[{"name": "无经验/固定top-k/独立贡献屏蔽", "paper_url": "https://arxiv.org/html/2606.15390", "code_url": null, "reproduction": "完整标准定义：无经验不注入；top-k按固定文本相似度取k条；独立屏蔽在开发任务对固定Bernoulli掩码有无经验的成功差取均值、同任务邻居加权后仅保留非负条目。是明确标准基线，不冒充ASSAY官方实现。", "controlled_parameters": "同actor/解码/任务划分/技能库/检索容量/全链路总预算", "extra_costs": "开发归因rollout、embedding、注入、任何重试全计费"}, {"name": "AppWorld ReAct基础agent", "paper_url": "https://github.com/StonyBrookNLP/appworld", "code_url": "https://raw.githubusercontent.com/StonyBrookNLP/appworld/main/experiments/code/simplified/react_code_agent.py", "reproduction": "已亲读environment.py execute与save/load_state；simplified/react_code_agent.py next_execution_inputs_usage_and_status读取工具输出、调用language_model.generate、记录usage并生成代码；simplified/agent.py为执行循环。可用公开train/dev/test任务及AppWorld CPU世界，未来需安装而本阶段未执行。", "controlled_parameters": "同任务、模型和预算", "extra_costs": "应用模拟CPU耗时与API全计"}]
