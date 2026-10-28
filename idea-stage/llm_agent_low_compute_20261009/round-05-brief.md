## 背景

**定位关键词：** tool failures；implicit failures；perturbation recovery

**一句话定位：** 工具 agent 如何区分结构合法的坏返回与真实但罕见的环境数据。

## 核心 Claim

ToolMaze 中隐式失败难于显式失败；仅用常识范围检查会误伤真实异常。主张对允许等价改写的工具，选择一个公开语义保证不改变答案的输入变换，检查返回的相应关系，改善检测而不过度重试。

现有失败分析证明语义错误会被接受；常识合法不等于功能正确；把成熟软件测试的等价关系迁到工具返回；如果探测只能识别人为显眼错误或比固定重试无收益，则该 Claim 不成立。

## 方法设计的核心思想

先抽象为同一查询的两种表达必须满足已知关系；迁移 metamorphic testing。只在公开 schema/文档支持的单位变换、往返转换或顺序不变查询上，由同一模型提议变换与关系；CPU 比较两个公开返回。不假定任意工具都有变换，未知关系则不探测。

## 最小实验

ToolMaze 可满足关系的预先筛选工具子集；诊断隐式故障和干净极端值的混淆，再比较 FC、failure-aware、固定重试、范围检查、关系探测；相同额外一次工具调用与总 token，指标检测召回/误报、TSR、恢复调用。若真实文档支持的工具过少，放弃。

同一模型快照、相同数据和顺序、相同推理模式/温度/seed/最大步数、相同总输入输出 token、LLM 调用与工具调用上限；机制、反思和检查均计入总预算。参数为实验前待确定项，本轮不运行。只读取 agent 可见输入，不读评价答案/隐藏状态。

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 开源代码与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| ToolMaze native function calling | tool failures、dynamic replanning、相同 C/P 任务 | https://arxiv.org/abs/2606.05806 | https://github.com/Zhudongsheng75/ToolMaze；已读取 evaluation/scripts/run_eval.py 的 create_agent/evaluate_single_task/main 和 README | python evaluation/scripts/run_eval.py --task-category c3 --modes P0 P1 P2 P3 P4 --agent-type openai --model {同一模型} --limit {预先固定任务数} | 是 |
| 同预算 failure-aware prompting | 相同工具失败设置，只提醒可能存在显式/隐式及暂时/永久失败 | https://arxiv.org/html/2606.05806v1#S4 | 同上 runner；标准提示对照，可直接在相同 agent system prompt 写入完整提醒，不读取 perturbation 标签 | 复制同一配置，唯一变化为提示是否包含上述四类失败提醒；同模型、相同总调用/token/tool预算 | 是 |
