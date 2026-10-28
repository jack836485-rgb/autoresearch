## 背景

**定位关键词：** function calling；pagination；API tools

**一句话定位：** 分页API的function-calling agent如何根据存在、否定存在或计数要求决定何时有足够证据完成。

## 核心 Claim

查询语义决定分页充分证据：存在的正结论可由一个见证支持；否定存在及精确计数需要相同查询范围的完整枚举。待验证AppWorld中这一区分是否减少过早完成，同时比统一全枚举省下存在查询调用。范围限静态只读分页，不主张解决所有agent停止或状态变化。

已有分页遗漏经验事实但AppWorld分组效果未验证；原选用的代码块入口看不到每个返回，现已改为官方FC逐调用入口；被忽视关键仍是不同量词有不同所需证据；以CPU量词条件控制完成；只有相反调用收益交互与独立正确性标注才支持。

## 方法设计的核心思想

使用已公开逐调用结果的SimplifiedFunctionCallingAgent，不使用只有整段stdout的ReAct观察口。具体插入点：在second_onwards_execution_inputs_usage_and_status收到last_execution_outputs后，以metadata.id/function_name匹配前一轮self.messages中的tool_calls.arguments，解析每条content公开结果更新页/游标/见证；在生成新execution_inputs后，读取同轮type化查询与完整tool_calls，若拟调用supervisor.complete_task且证据条件不满足，移除该未执行完成调用，并给相同tool_call_id追加一个本地tool message说明尚缺范围，然后让原actor下一轮决定查询。控制器不能自动执行任何业务API。相同预算下所有实验臂将max_api_calls_per_interaction设为1，避免同轮其他操作与完成混合；同一helper对照共享该接口。语义类型和predicate由原actor在正常输出中给出，未知不声称否定或精确值。

## 最小实验

先在AppWorld train/dev固定公开任务语义分组及静态分页API子集，不从测试失败反选；由独立人工判存在/否定/计数及每轮可见覆盖。FC原agent、强分页语义提示、固定再读一页、统一枚举覆盖门、本方法相同actor/候选API发现/解码/任务/总token与工具硬预算。对自然任务分别报告TGC/SGC和错误完成；额外同场景存在/计数成对诊断单独报告。支持条件是计数/否定少过早完成且存在组相对全枚举少调用，超过强提示；失败条件是类型错、无分页错误、同预算提示等效或必须访问隐藏数据。首次可行性验收只需记录标准call_id/result并确认虚拟阻止完成时消息协议合法，不运行性能实验。

固定共同actor/模型快照、原FC api_predictor模型与预算、工具列表、任务ID和公开分组、seed/temperature、最大总输入输出token/LLM调用/API调用。所有臂同一max_api_calls_per_interaction=1、同样文本解析和数据可见范围。控制器统计不调用额外LLM，类型声明在原actor输出内计费；被阻止的调用也计其生成token及后续处理，不伪装免费反思。参数为方案规格，用户实验预算未定，本轮不启动运行。

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 开源代码与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| AppWorld官方FC | 同一function calling/API分页任务 | https://arxiv.org/abs/2407.18901 | https://github.com/StonyBrookNLP/appworld；已读function_calling_agent.py，其last_execution_outputs含tool_call_id与content；已确认每个ExecutionIO输入为单个print(API(...)) | appworld run auto --agent-name simplified_function_calling_agent --model-name {共同模型} --dataset-name dev；配置统一max_api_calls_per_interaction=1，test冻结后用官方split | 是；源码核验，未实跑 |
| 强分页语义提示 | 同一actor同语义规则，排除提示贡献 | 本项目完整标准规范 | 同一FC提示直接说明存在见证可停、否定/计数须查全；没有CPU账本或完成门 | 同入口、同提示/输出预算，上下文多出的语义文本计费 | 是 |
| 固定再读一页 | 排除多一次返回收益 | 公开分页参数规范 | 同一FC提示让actor在首列表返回后调用文档支持下一页一次；不得硬编码业务API | 相同工具/LLM/token上限，由actor生成下一页请求 | 是 |
| 统一全枚举门 | 排除只有CPU覆盖而无量词的解释 | 标准可直接本地实现 | 共享同一个逐call_id/参数/返回状态表和完成拦截，全部查询都等到公开分页终止信号才允许该查询完成；不能把单个空中间页自动当全集完成 | 与主方法同数据和插入点；仅停条件统一不区分量词；未完成返回未知并计失败 | 是 |
