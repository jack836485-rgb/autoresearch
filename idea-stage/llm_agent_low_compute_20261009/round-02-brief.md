## 背景

**定位关键词：** agent memory；execution feedback；context adaptation

**一句话定位：** 经验复用 agent 如何避免把一次成功的操作规则推广到不成立的任务状态。

## 核心 Claim

ACE 附录明确承认反思器可能生成有害经验，ExpeL 消融也显示加入反思可能变差。假设有害经验中一类错误是过宽适用条件，helpful/harmful 总计数混合了不同状态。主张使用最小反例收紧经验条件，而非全局删除经验。

反思经验可能有害是 baseline 作者明示 limitation；潜在关键是错误出在适用范围而非规则整体；本方法把失败视为范围反例；若有害经验并非范围问题或状态条件对照等效，则否定。

## 方法设计的核心思想

每条经验保留来源轨迹及其触发事实；训练或 dev 轨迹中出现与经验冲突的执行反馈时，只查找使结果不同的可见前提，形成一个保留原规则的排除条件；推理时同一模型判断条件并给出来源，CPU 维护规则。不做额外大规模反事实 rollout，不把 gold test反馈写入记忆。

## 最小实验

AppWorld train固定轨迹生成经验、dev诊断过宽条件，测试前冻结；比较 ReAct、同一批轨迹提炼的简单经验表、状态条件经验、反例收紧经验。同模型和轨迹、相同记忆 token与构建预算，分析错误适用率、保留有用经验比例、TGC。ACE 作为最高近邻，官方 adapter未读完前暂不纳入最小实验。

同一模型快照、相同数据和顺序、相同推理模式/温度/seed/最大步数、相同总输入输出 token、LLM 调用与工具调用上限；机制、反思和检查均计入总预算。参数为实验前待确定项，本轮不运行。只读取 agent 可见输入，不读评价答案/隐藏状态。

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 开源代码与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| AppWorld ReAct code agent | interactive coding agents、API tools、同一 AppWorld 任务 | https://arxiv.org/abs/2407.18901 | https://github.com/StonyBrookNLP/appworld；已读取 experiments/code/simplified/react_code_agent.py，对应 SimplifiedReActCodeAgent | appworld run auto --agent-name simplified_react_code_agent --model-name {同一模型} --dataset-name dev；正式测试冻结后切 test_normal/test_challenge | 是 |
| AppWorld full-code repair | 同一环境中的整段代码生成与错误反馈修复 | https://arxiv.org/abs/2407.18901 | https://github.com/StonyBrookNLP/appworld；已读取 experiments/code/simplified/full_code_agent.py，对应 SimplifiedFullCodeAgent | appworld run auto --agent-name simplified_full_code_agent --model-name {同一模型} --dataset-name dev；必须统一 API 发现与交互上限 | 是 |
| ACE offline no-GT | 同一 AppWorld 经验提炼与复用任务；全部对照统一在 ace-appworld fork | https://arxiv.org/abs/2510.04618 | https://github.com/ace-agent/ace-appworld；已读 adaptation_react.py/evaluation_react.py 和 ACE_offline_no_GT_adaptation.jsonnet | 从源码安装；appworld run ACE_offline_no_GT_adaptation，随后 ACE_offline_no_GT_evaluation；锁定 generator/reflector/curator 为相同模型，预算统一，冻结训练轨迹；no-GT提示与可见字段待源代码审阅后确认不泄露测试答案 | 是；不声称运行验证过 |
