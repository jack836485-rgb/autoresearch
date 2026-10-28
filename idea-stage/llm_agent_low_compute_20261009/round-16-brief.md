## 背景

**定位关键词：** interactive coding agents；context adaptation；long-horizon tasks

**一句话定位：** 长程代码 agent 如何压缩历史而不把尚未验证的猜测写成已知事实。

## 核心 Claim

ACE 记录全量重写会丢失知识，AppWorld agent 源码会截断历史；待诊断一种更窄失败：压缩把“计划尝试/推测”变成“已成功/已知”。主张压缩保留断言的证据状态，而不追求保留更多原文。

压缩的信息丢失有论文和代码依据，证据状态升格目前待验证；关键是保留真值来源而非全文；记录状态约束压缩；若状态错不是主要失败就止损。

## 方法设计的核心思想

把历史片段分成有工具回执支持、模型推测、待执行三个状态；压缩仍由原模型生成，但每个断言必须携带原片段来源与状态，CPU拒绝从待验证升为已证实；只检查来源和状态，不额外 LLM judge。

## 最小实验

AppWorld dev 在固定阈值发生压缩，先人工标注压缩前后断言状态变化；比较近期截断、普通摘要、同长结构摘要、有状态压缩。相同模型/摘要调用/token预算，衡量错误升格率、TGC。若没有升格失败或仅增加文本可解释，否定。

同一模型快照、相同数据和顺序、相同推理模式/温度/seed/最大步数、相同总输入输出 token、LLM 调用与工具调用上限；机制、反思和检查均计入总预算。参数为实验前待确定项，本轮不运行。只读取 agent 可见输入，不读评价答案/隐藏状态。

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 开源代码与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| AppWorld ReAct code agent | interactive coding agents、API tools、同一 AppWorld 任务 | https://arxiv.org/abs/2407.18901 | https://github.com/StonyBrookNLP/appworld；已读取 experiments/code/simplified/react_code_agent.py，对应 SimplifiedReActCodeAgent | appworld run auto --agent-name simplified_react_code_agent --model-name {同一模型} --dataset-name dev；正式测试冻结后切 test_normal/test_challenge | 是 |
| AppWorld full-code repair | 同一环境中的整段代码生成与错误反馈修复 | https://arxiv.org/abs/2407.18901 | https://github.com/StonyBrookNLP/appworld；已读取 experiments/code/simplified/full_code_agent.py，对应 SimplifiedFullCodeAgent | appworld run auto --agent-name simplified_full_code_agent --model-name {同一模型} --dataset-name dev；必须统一 API 发现与交互上限 | 是 |
