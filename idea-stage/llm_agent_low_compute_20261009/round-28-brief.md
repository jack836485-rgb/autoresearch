## 背景

**定位关键词：** API documentation；interactive coding agents；execution feedback

**一句话定位：** 代码 agent 如何在公开 API schema 缺失或过时后修正自己的接口理解。

## 核心 Claim

AppWorld 附录指出不完整/过时 response schema 是现实困难。主张 API返回可推翻某一个接口假设，但不应迫使 agent 重新读全部工具文档；维护最小 schema 修订可减少重复错误。

接口声明不完整在论文中作为 limitation；可能遗漏的是失败对局部 schema 假设提供信息；以真实返回局部修订；若不依赖错误 schema 仍提升则需重新定位。

## 方法设计的核心思想

输入文档和实际公开返回；CPU比较字段类型/层级与 agent 生成的访问表达式，原模型只更改被反例否定的字段路径，并记录例外。初期只读返回结构，不处理安全输入或恶意变化。

## 最小实验

官方 AppWorld 原任务与对 response 文档进行固定缺字段/类型声明扰动的诊断版本分开；ReAct、报错重生成、全量重读、最小 schema 修订同预算。指标重复访问错误、TGC与调用成本。

同一模型快照、相同数据和顺序、相同推理模式/温度/seed/最大步数、相同总输入输出 token、LLM 调用与工具调用上限；机制、反思和检查均计入总预算。参数为实验前待确定项，本轮不运行。只读取 agent 可见输入，不读评价答案/隐藏状态。

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 开源代码与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| AppWorld ReAct code agent | interactive coding agents、API tools、同一 AppWorld 任务 | https://arxiv.org/abs/2407.18901 | https://github.com/StonyBrookNLP/appworld；已读取 experiments/code/simplified/react_code_agent.py，对应 SimplifiedReActCodeAgent | appworld run auto --agent-name simplified_react_code_agent --model-name {同一模型} --dataset-name dev；正式测试冻结后切 test_normal/test_challenge | 是 |
| AppWorld full-code repair | 同一环境中的整段代码生成与错误反馈修复 | https://arxiv.org/abs/2407.18901 | https://github.com/StonyBrookNLP/appworld；已读取 experiments/code/simplified/full_code_agent.py，对应 SimplifiedFullCodeAgent | appworld run auto --agent-name simplified_full_code_agent --model-name {同一模型} --dataset-name dev；必须统一 API 发现与交互上限 | 是 |
