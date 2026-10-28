## 背景

**定位关键词：** episodic memory；value-aware retrieval；runtime learning

**一句话定位：** 经验检索 agent 如何避免记忆评分只反映它恰好在哪些容易任务中被调用。

## 核心 Claim

MemRL 理论的全局 Q(m) 对检索诱导的任务分布求平均；同一经验被用于容易任务时会高分，换到困难任务时可能误排。待诊断：固定真实任务混合不变，检索策略变化仍引发经验排名反转。主张用固定任务族参考分布标准化效用，减少检索选择偏差；不声称得到经验的因果贡献。

原论文承认检索分布参与全局效用，仍未知这种选择影响是否实害；遗漏可能是记忆价值与被使用任务难度混合；标准化到同一参考人群；若控制任务族后偏差不影响任务成功，停止。

## 方法设计的核心思想

每条记忆记录公开任务族中的成功/使用数，初始少量槽位随机探索保证支持；CPU用预先固定的任务族权重合成标准化效用，低覆盖项沿用语义排序；模型与记忆内容不变。没有额外rollout，不从测试结果反推权重。

## 最小实验

ALFWorld六类任务，固定总任务流与初始记忆；k=1，比较标量Q、按当前族Q、纯语义、固定参考混合Q。构建预算相同，独立冻结评分后在自然task mix与重排task mix评估；诊断同记忆相同族收益不变但总排名变动。若按当前族Q等效或无排名反转，则新意不足。

同一模型快照、相同数据和顺序、相同推理模式/温度/seed/最大步数、相同总输入输出 token、LLM 调用与工具调用上限；机制、反思和检查均计入总预算。参数为实验前待确定项，本轮不运行。只读取 agent 可见输入，不读评价答案/隐藏状态。

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 开源代码与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| MemRL on ALFWorld | episodic memory、utility、runtime learning；同一文字交互 ALFWorld 任务 | https://arxiv.org/abs/2601.03192 | https://github.com/MemTensor/MemRL；已读取 run/run_alfworld.py、alfworld_rl_runner.py、memory_service.update_values、retrievers.py 与 rl_alf_config.yaml；API LLM/embedding，无模型训练 | python run/run_alfworld.py --config configs/rl_alf_config.yaml；统一 text-only AlfredTWEnv、LLM/embedding、候选集合、k、max_steps和总调用；Linux/WSL2安装 ALFWorld/数据，CPU环境 | 是；源码核验，未运行 |
| 相同 agent + semantic-only retrieval | 同一记忆库与ALFWorld交互，排除模型或不同数据效果 | https://arxiv.org/abs/2601.03192 | 同一官方 runner；已读 enable_value_driven 分支和 query retriever | 相同 YAML 设 experiment.enable_value_driven=false；保留同一检索候选/k/token/轨迹获取预算 | 是 |
| 相同 agent + 无记忆 | ALFWorld任务的基础 ReAct；评估记忆开销是否值得 | https://arxiv.org/abs/2210.03629 | 标准可直接本地实现：同 runner 生成调用不注入 retrieved memories；同原始few-shot、模型和工具 | 保留同actor输入/输出上限和工具上限；可用未花记忆构建token继续执行，但不能超过统一硬上限；无需隐藏数据/checkpoint | 是 |
