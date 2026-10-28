## 背景

**定位关键词：** agent memory；failure trajectories；execution feedback

**一句话定位：** 经验 agent 如何避免把预算耗尽或前置失败误记成某条有效策略不可用。

## 核心 Claim

ACE 与 ReasoningBank 提炼失败经验；待诊断一种错误：轨迹失败但建议动作从未到达，反思却写“不要用该方法”。主张负经验必须附已尝试证据和失败作用域，未尝试步骤不得被负更新。

baseline依赖反思准确性且可能有害；局部失败是否被提升为整体禁用待验证；用尝试回执限制负规则；若未尝试误禁不出现或仅额外提醒等效则否定。

## 方法设计的核心思想

从合法可见调用轨迹辨认建议步骤是否被真正调用以及失败发生的前置位置；经验提炼时只允许对实际尝试的动作产生否定规则，未到达写作未知。不归因所有因果，不要求反事实rollout。

## 最小实验

AppWorld同一固定训练轨迹与记忆token；诊断负经验是否把未执行步骤否定。对照 ReAct、ACE no-GT、提示“勿过度归因”、尝试证据约束。dev独立人工标注否定作用域，冻结后评估TGC与有效策略误禁率。

同一模型快照、相同数据和顺序、相同推理模式/温度/seed/最大步数、相同总输入输出 token、LLM 调用与工具调用上限；机制、反思和检查均计入总预算。参数为实验前待确定项，本轮不运行。只读取 agent 可见输入，不读评价答案/隐藏状态。

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 开源代码与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| AppWorld ReAct code agent | interactive coding agents、API tools、同一 AppWorld 任务 | https://arxiv.org/abs/2407.18901 | https://github.com/StonyBrookNLP/appworld；已读取 experiments/code/simplified/react_code_agent.py，对应 SimplifiedReActCodeAgent | appworld run auto --agent-name simplified_react_code_agent --model-name {同一模型} --dataset-name dev；正式测试冻结后切 test_normal/test_challenge | 是 |
| AppWorld full-code repair | 同一环境中的整段代码生成与错误反馈修复 | https://arxiv.org/abs/2407.18901 | https://github.com/StonyBrookNLP/appworld；已读取 experiments/code/simplified/full_code_agent.py，对应 SimplifiedFullCodeAgent | appworld run auto --agent-name simplified_full_code_agent --model-name {同一模型} --dataset-name dev；必须统一 API 发现与交互上限 | 是 |
| ACE offline no-GT | 同一 AppWorld 经验提炼与复用任务；全部对照统一在 ace-appworld fork | https://arxiv.org/abs/2510.04618 | https://github.com/ace-agent/ace-appworld；已读 adaptation_react.py/evaluation_react.py 和 ACE_offline_no_GT_adaptation.jsonnet | 从源码安装；appworld run ACE_offline_no_GT_adaptation，随后 ACE_offline_no_GT_evaluation；锁定 generator/reflector/curator 为相同模型，预算统一，冻结训练轨迹；no-GT提示与可见字段待源代码审阅后确认不泄露测试答案 | 是；不声称运行验证过 |
| 同预算反归因提醒 | 同一AppWorld经验提炼，排除额外prompt收益 | 标准本地实验规范 | 相同ACE反思提示加入“失败只否定已执行且有失败证据的动作，未执行动作仍未知”，不接入本方法的CPU尝试证据约束 | 同一fork、actor/reflector/curator与输入轨迹，总token相同；仅规则提醒 | 是 |
