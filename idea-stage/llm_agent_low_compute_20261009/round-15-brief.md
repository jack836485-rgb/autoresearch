## 背景

**定位关键词：** episodic memory；credit assignment；runtime learning

**一句话定位：** 记忆 agent 如何避免失败任务把所有检索条目都更新成负值。

## 核心 Claim

MemRL update_values 对每个 retrieved ID 给同一个末端奖励；可能存在条目只是被检索、未进入行动却被误罚。主张仅在公开轨迹中真的落实该记忆操作时更新效用，减少未使用条目的污染；使用不等于因果贡献。

代码把检索与采用混为更新条件；未采用误罚仍待验证；用行动回执收紧更新支持；如果仅自报已足够或条目无法独立绑定，否定。

## 方法设计的核心思想

检索经验拆成可匹配的公开动作意图；原模型在行动轮声明引用的条目与建议动作，执行回执验证该动作确实发生，CPU只给通过的ID更新。没有额外judge或反事实rollout；不能只信self-report。

## 最小实验

固定MemRL多记忆k>1与同一task流，人工盲标行动和记忆联系作离线诊断；标量全更新、仅self-report更新、实际行动证据更新、随机等量更新；统一模型、k与预算，比较无关条目误更新、成功率。若行动证据匹配不可靠，终止。

同一模型快照、相同数据和顺序、相同推理模式/温度/seed/最大步数、相同总输入输出 token、LLM 调用与工具调用上限；机制、反思和检查均计入总预算。参数为实验前待确定项，本轮不运行。只读取 agent 可见输入，不读评价答案/隐藏状态。

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 开源代码与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| MemRL on ALFWorld | episodic memory、utility、runtime learning；同一文字交互 ALFWorld 任务 | https://arxiv.org/abs/2601.03192 | https://github.com/MemTensor/MemRL；已读取 run/run_alfworld.py、alfworld_rl_runner.py、memory_service.update_values、retrievers.py 与 rl_alf_config.yaml；API LLM/embedding，无模型训练 | python run/run_alfworld.py --config configs/rl_alf_config.yaml；统一 text-only AlfredTWEnv、LLM/embedding、候选集合、k、max_steps和总调用；Linux/WSL2安装 ALFWorld/数据，CPU环境 | 是；源码核验，未运行 |
| 相同 agent + semantic-only retrieval | 同一记忆库与ALFWorld交互，排除模型或不同数据效果 | https://arxiv.org/abs/2601.03192 | 同一官方 runner；已读 enable_value_driven 分支和 query retriever | 相同 YAML 设 experiment.enable_value_driven=false；保留同一检索候选/k/token/轨迹获取预算 | 是 |
| 相同 agent + 无记忆 | ALFWorld任务的基础 ReAct；评估记忆开销是否值得 | https://arxiv.org/abs/2210.03629 | 标准可直接本地实现：同 runner 生成调用不注入 retrieved memories；同原始few-shot、模型和工具 | 保留同actor输入/输出上限和工具上限；可用未花记忆构建token继续执行，但不能超过统一硬上限；无需隐藏数据/checkpoint | 是 |
