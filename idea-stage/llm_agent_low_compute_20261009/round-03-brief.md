## 背景

**定位关键词：** episodic memory；runtime learning；ALFWorld

**一句话定位：** 记忆增强 agent 如何从被执行预算截断的任务中学习在给定步数内可用的经验。

## 核心 Claim

MemRL 的代码把最终 success=false 映射为相同负奖励，且 runner 到 max_steps 时结束；这会混合真正失败与尚未完成。待诊断：长而有效的经验在短预算任务中被负更新后，在充足预算下仍被误弃。主张学习“预算内成功的累计概率”，将非终止的预算截断作为删失记录，使同一经验可按当前预算选用，且不推测未观察的后续成功。

baseline源码明确统一负更新而执行窗口有限，预算截断误罚的实际影响尚未验证；被忽视变量可能是未完成不是终止失败；在已有不同观察窗口下估计预算内完成概率；只有控制相同预算后改善跨预算排序且超过简单跳过更新，才支持本候选。

## 方法设计的核心思想

把输入抽象为不同观察窗口下看到完成/真正终止/仍在执行，迁移生存分析的 competing risks。固定actor与记忆内容，CPU为每条经验及公开任务类记录每步在险数、成功事件、真正终止失败事件；已到预算但环境未终止的轨迹只更新已观测区间，不当作最终失败。在已观测预算范围内用累计成功概率排序，数据不足沿用同一语义排序；不用外推，不训练模型，也不追加反事实 rollout。

## 最小实验

ALFWorld TextWorld，固定同一初始memory bank，单次检索 k=1 以隔离多记忆归因。构建阶段给同一任务流随机分配预先固定的若干步数上限，cap在记忆选定后独立分配，所有组共享分配与总rollout/token预算；不能只给本方法长轨迹。先在已自然出现的较长预算记录中检查哪些短前缀未完成而后续成功（仅诊断，不伪造在线标签）。最少对照 MemRL标量Q、semantic-only、相同预算条件Q、仅跳过预算截断负更新、删失校正分布；冻结后在各已覆盖预算下测成功率/同预算token与经验误弃。若只是“不更新截断”已足够，或出现非独立cap/超预算信息，否定额外机制。

同一冻结actor模型/embedding快照、task family、初始memory bank、解码、seed与预算分配，统一k=1、候选检索集合和逐任务最大调用/token/工具数。所有方法用相同有观察支持的预算，在线更新只能见当前cap以内记录。随机cap不得依赖失败预判或被选memory；真正终止与预算截断由runner/environment事件判断，无法区分的日志不参与相应更新。显卡：API方案本地0；控制器CPU；不运行实验，实际模型/金额/样本量待用户确定。

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 开源代码与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| MemRL on ALFWorld | episodic memory、utility、runtime learning；同一文字交互 ALFWorld 任务 | https://arxiv.org/abs/2601.03192 | https://github.com/MemTensor/MemRL；已读取 run/run_alfworld.py、alfworld_rl_runner.py、memory_service.update_values、retrievers.py 与 rl_alf_config.yaml；API LLM/embedding，无模型训练 | python run/run_alfworld.py --config configs/rl_alf_config.yaml；统一 text-only AlfredTWEnv、LLM/embedding、候选集合、k、max_steps和总调用；Linux/WSL2安装 ALFWorld/数据，CPU环境 | 是；源码核验，未运行 |
| 相同 agent + semantic-only retrieval | 同一记忆库与ALFWorld交互，排除模型或不同数据效果 | https://arxiv.org/abs/2601.03192 | 同一官方 runner；已读 enable_value_driven 分支和 query retriever | 相同 YAML 设 experiment.enable_value_driven=false；保留同一检索候选/k/token/轨迹获取预算 | 是 |
| 相同 agent + 无记忆 | ALFWorld任务的基础 ReAct；评估记忆开销是否值得 | https://arxiv.org/abs/2210.03629 | 标准可直接本地实现：同 runner 生成调用不注入 retrieved memories；同原始few-shot、模型和工具 | 保留同actor输入/输出上限和工具上限；可用未花记忆构建token继续执行，但不能超过统一硬上限；无需隐藏数据/checkpoint | 是 |
