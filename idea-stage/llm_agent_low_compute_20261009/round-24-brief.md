## 背景

**定位关键词：** API tools；pagination；stateful execution

**一句话定位：** 交互式代码agent如何在分页读取同时删除或修改结果对象时完成全部目标对象。

## 核心 Claim

分页通常基于稳定集合，但AppWorld允许同一agent在扫描时修改状态。待验证：删除一页对象后继续增加offset，会跳过前移对象，即使每次调用成功。主张将agent自身写操作造成的集合变化纳入分页计划，避免把静态覆盖当成动态完成。

状态执行和offset分页都是真实支持结构，二者组合可达；遗漏可能来自agent自己的写动作而非罕见并发；分页范围随写操作重开；若没有自致跳过对象，放弃。

## 方法设计的核心思想

原actor从文档与自身生成代码标出读取集合和写目标；CPU指出同集合修改可能使此前页号覆盖失效，给原actor剩余范围及合法策略选择：先收集ID再执行、文档支持时用稳定cursor、或重新查当前前缀。控制器不替actor硬编码业务API。

## 最小实验

AppWorld bulk-action train/dev任务先诊断扫描-修改顺序与遗漏。ReAct、通用分页提醒、先收集后执行的标准策略、写后覆盖重开；所有组同工具/token预算。若简单先收集ID就完全解决，停止复杂机制。

同一模型快照、相同数据和顺序、相同推理模式/温度/seed/最大步数、相同总输入输出 token、LLM 调用与工具调用上限；机制、反思和检查均计入总预算。参数为实验前待确定项，本轮不运行。只读取 agent 可见输入，不读评价答案/隐藏状态。

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 开源代码与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| AppWorld ReAct code agent | interactive coding agents、API tools、同一 AppWorld 任务 | https://arxiv.org/abs/2407.18901 | https://github.com/StonyBrookNLP/appworld；已读取 experiments/code/simplified/react_code_agent.py，对应 SimplifiedReActCodeAgent | appworld run auto --agent-name simplified_react_code_agent --model-name {同一模型} --dataset-name dev；正式测试冻结后切 test_normal/test_challenge | 是 |
| AppWorld full-code repair | 同一环境中的整段代码生成与错误反馈修复 | https://arxiv.org/abs/2407.18901 | https://github.com/StonyBrookNLP/appworld；已读取 experiments/code/simplified/full_code_agent.py，对应 SimplifiedFullCodeAgent | appworld run auto --agent-name simplified_full_code_agent --model-name {同一模型} --dataset-name dev；必须统一 API 发现与交互上限 | 是 |
