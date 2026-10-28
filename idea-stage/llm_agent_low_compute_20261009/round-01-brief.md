## 背景

**定位关键词：** tool failures；dynamic replanning；multi-step tool use

**一句话定位：** 多步工具 agent 如何在发现上游输出错误后撤销由旧输出得出的后续判断。

## 核心 Claim

ToolMaze 展示 agent 会把语义错误值传到下游；重取到正确值不等于已基于旧值做出的判断自动失效。主张恢复应按观察依赖撤销旧结论，而不是只重试失败工具或重写整个历史。其超过普通重试的收益只应出现在已发生下游消费的轨迹。

ToolMaze 的隐式故障例子给出错误传播，但未直接证明重取后的陈旧依赖；遗漏的可能关键是恢复同时改变证据有效性；本方法按消费关系撤销局部结论；只有传播组改善且无传播组不获益，才支持该机制。

## 方法设计的核心思想

输入 agent 可见工具调用、参数、返回及公开工具 schema；在生成同一轮行动时让模型同时标出它使用的先前结果 ID，仅建立实际消费的边。若上游返回被替换，CPU 沿边标记派生结果过期，下一轮只给受影响子图及未受影响结果，要求重验受影响调用。没有 gold DAG，也不撤销环境写效果；先限只读/计算型链。

## 最小实验

在 ToolMaze c3/c4 的 P3/P4 先量化错误值下游消费与重取后仍引用旧值，加入固定相同的一步延迟暴露条件作为机制诊断而不混入原始官方分数。对照官方 FC、failure-aware prompt、相同图展示但不失效的消融；分层比较下游未消费/已消费，指标 TSR、恢复率、旧值复用和总调用。

同一模型快照、相同数据和顺序、相同推理模式/温度/seed/最大步数、相同总输入输出 token、LLM 调用与工具调用上限；机制、反思和检查均计入总预算。参数为实验前待确定项，本轮不运行。只读取 agent 可见输入，不读评价答案/隐藏状态。

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 开源代码与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| ToolMaze native function calling | tool failures、dynamic replanning、相同 C/P 任务 | https://arxiv.org/abs/2606.05806 | https://github.com/Zhudongsheng75/ToolMaze；已读取 evaluation/scripts/run_eval.py 的 create_agent/evaluate_single_task/main 和 README | python evaluation/scripts/run_eval.py --task-category c3 --modes P0 P1 P2 P3 P4 --agent-type openai --model {同一模型} --limit {预先固定任务数} | 是 |
| 同预算 failure-aware prompting | 相同工具失败设置，只提醒可能存在显式/隐式及暂时/永久失败 | https://arxiv.org/html/2606.05806v1#S4 | 同上 runner；标准提示对照，可直接在相同 agent system prompt 写入完整提醒，不读取 perturbation 标签 | 复制同一配置，唯一变化为提示是否包含上述四类失败提醒；同模型、相同总调用/token/tool预算 | 是 |
