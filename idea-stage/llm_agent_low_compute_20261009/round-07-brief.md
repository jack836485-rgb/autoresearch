## 背景

**定位关键词：** API tools；interactive coding agents；pagination

**一句话定位：** 工具 agent 如何判断检索没有结果还是尚未查完结果。

## 核心 Claim

AppWorld 的公开提示专门提醒分页；待诊断 agent 会把某一页空结果或截断列表当全局不存在。主张将否定结论绑定到 agent 实际完成的搜索覆盖，避免过早否定或无限翻页。

分页是公开 API 的真实结构；空结果与全局不存在可能被混淆；用查询覆盖范围限定否定推断；若简单分页提示解决同预算失败则无独立贡献。

## 方法设计的核心思想

同一模型根据公开 API 文档提出查询及分页过程；CPU 跟踪可见游标/页号、已读范围、终止标志，把“未查到”保留为局部结论。允许停止只针对任务所需范围，不能硬编码特定 API。

## 最小实验

AppWorld train/dev 预先筛选需要多页检索的任务；诊断失败是否源于未覆盖。官方 ReAct/full-code、普通分页提醒、固定多翻一页、覆盖状态控制；相同 API调用和token上限，指标遗漏对象、虚假不存在、TGC。

同一模型快照、相同数据和顺序、相同推理模式/温度/seed/最大步数、相同总输入输出 token、LLM 调用与工具调用上限；机制、反思和检查均计入总预算。参数为实验前待确定项，本轮不运行。只读取 agent 可见输入，不读评价答案/隐藏状态。

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 开源代码与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| AppWorld ReAct code agent | interactive coding agents、API tools、同一 AppWorld 任务 | https://arxiv.org/abs/2407.18901 | https://github.com/StonyBrookNLP/appworld；已读取 experiments/code/simplified/react_code_agent.py，对应 SimplifiedReActCodeAgent | appworld run auto --agent-name simplified_react_code_agent --model-name {同一模型} --dataset-name dev；正式测试冻结后切 test_normal/test_challenge | 是 |
| AppWorld full-code repair | 同一环境中的整段代码生成与错误反馈修复 | https://arxiv.org/abs/2407.18901 | https://github.com/StonyBrookNLP/appworld；已读取 experiments/code/simplified/full_code_agent.py，对应 SimplifiedFullCodeAgent | appworld run auto --agent-name simplified_full_code_agent --model-name {同一模型} --dataset-name dev；必须统一 API 发现与交互上限 | 是 |
| 固定多翻一页 | 同一AppWorld分页任务，排除只增加一次访问的收益 | 公开API文档分页规范 | 标准本地对照：相同actor生成公开分页API调用；提示在首个列表结果后继续同查询下一页一次，不用hidden state | 同一ReAct提示仅固定多读下一页；额外调用纳入同一硬上限；不硬编码特定API | 是 |
| 普通分页提醒 | 同一任务，排除单纯提醒 | AppWorld公开prompt分页说明 | 标准本地对照：相同actor提示分页结果不一定完整，仍由actor选全部行动 | 同一runner与完整token/tool预算；仅提示差异 | 是 |
