## 背景

**定位关键词：** episodic memory；value-aware retrieval；ALFWorld

**一句话定位：** 记忆agent如何在可比较的共同任务支持中排除检索暴露构成造成的经验排名差异。

## 核心 Claim

MemRL已明示全局值随检索诱导分布加权，RoMeRL已分析观察性return；新假设仅是同一固定memory候选支持下，两个不同暴露策略会让标量Q排名反转，而固定参考任务族标准化能保持可比排名。只对共同支持的经验比较，不对零支持项外推，也不声称因果贡献。

原始review指出零支持外推与冻结后改mix不能改变排名；本候选把比较收在共同支持并实际改变学习期暴露账本；遗漏关键是相同参考人群而非更多探索；只有同表暴露干预造成标量排名变化而标准化降低损害才支持。

## 方法设计的核心思想

在train/dev固定一个候选池与其公开语义支持矩阵，只保留各比较memory都合法进入候选的共同任务族；不足两个族则不声称混合校正收益。在共同支持内按预先已知随机分配取得各memory×族观察，保持两种暴露权重不同但均非零；CPU给两种账本标准化到同一固定族权重。部署候选也限同一支持集，未覆盖候选不与标准化分数混排，沿用整个基准策略作为独立outside-support情况。

## 最小实验

固定actor、memory内容、k=1、共同任务ID与种子，先收集一份有限交叉支持轨迹表，所有学习法使用同表及同总费用；用两份预先不同的暴露子样本构造标量Q/分族Q/标准化Q，检查是否仅观察权重改变就产生排名反转。冻结后在共同支持held-out任务比较成功率、排名一致性；outside-support另报。强对照为同族Q与标准化，不以语义fallback混淆estimand。若没有非空共同支持、子样本偏差未影响success、或同族Q等效则否定。

同一模型快照、相同数据和顺序、相同推理模式/温度/seed/最大步数、相同总输入输出 token、LLM 调用与工具调用上限；机制、反思和检查均计入总预算。参数为实验前待确定项，本轮不运行。只读取 agent 可见输入，不读评价答案/隐藏状态。

| Baseline | 与定位关键词及目标任务的关系 | 论文或规范 | 开源代码与核验结果 | 具体复现方式 | 是否纳入最小实验 |
|---|---|---|---|---|---|
| 固定库MemRL标量Q | 同一ALFWorld支持表和效用学习 | https://arxiv.org/abs/2601.03192 | https://github.com/MemTensor/MemRL；已读ALFWorld runner/update_values/retriever | python run/run_alfworld.py --config configs/rl_alf_config.yaml；共同轨迹表冻结memory内容，CPU回放原EMA奖励更新；正式actor执行仍同入口 | 是 |
| 同任务族条件Q | 排除仅加任务条件的收益 | 标准可直接本地实现 | 每个memory×公开族一个相同EMA成功均值；只对共同支持项比较 | 使用同表、同学习率、相同已观察reward、同k=1；当前族选值，不加参考混合 | 是 |
| 固定参考标准化Q | 候选机制 | 成熟直接标准化是方法启发，不充当跨领域baseline | 同一memory×族均值表按dev预先固定族权重加权，无零支持项或混合fallback | 与条件Q相同数据和更新；唯一区别是各memory比较时合成到共同参考权重 | 主方法 |
| 无记忆ReAct | 同ALFWorldactor | https://arxiv.org/abs/2210.03629 | 同runner不注入memory；完整标准方法 | 同actor与工具预算，可将省下memory开销用于执行；总预算不增加 | 是 |
