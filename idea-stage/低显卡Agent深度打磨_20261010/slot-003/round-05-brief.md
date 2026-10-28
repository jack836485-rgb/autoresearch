## 背景

**定位关键词：** LLM agents, procedural memory, stochastic dominance, budget-constrained inference

同一技能可能用更多检查换取较晚的正确完成；若只看一档预算或单个成功减成本标量，低预算下负贡献不等于所有预算下都无价值。

当前目标及演化依据：聚焦同一冻结actor与公开任务类内的经验完成成本分布，不声称对未知未来任务有最优全局淘汰；相对初始目标处理预算条件的暴露与保留混淆，D02选择混杂不作普遍解决。

https://arxiv.org/html/2609.14138：§III-B–D用初始任务特征联合选memory mode与generation tier，reward为正确性减归一化费用；联合资源选择已有覆盖。
https://arxiv.org/html/2606.25115：摘要及方法框架已有value-minus-harm per-byte、budget-triggered KEEP，不能把费用进入保留标准当贡献。
https://arxiv.org/html/2606.09421：§3/附录F已有经济utility驱动技能改写策略；成本/质量折中和条件化策略已有覆盖。
https://arxiv.org/html/2606.15017：§1及实验把辅助模块费用重分配给普通actor作为关键对照；相同actor阶段预算不等于全成本相同。
https://arxiv.org/html/2606.15390：随机技能掩码的贡献为成功差，本版不重提条件因果屏蔽。

## 核心 Claim

待验证：在actor对预算上限不作策略重规划、且只在共同公开状态类比较时，经验对正确完成成本的分布可能与无经验分布交叉。以分布支配判断经验可删、以当前预算处的完成概率差判断是否暴露，能保留高预算有益经验同时减少低预算成本负迁移；不把任意一档负分直接当永久有害。

## 方法设计的核心思想

开发集对同模型/解码/无budget提示的actor分别收集有/无经验到完成或共同最大步数的轨迹，预算作为共同外部停止条件。记录每步真实累计全部成本及离线完成结果，不在runtime展示hidden结果。用相同轨迹的可评价prefix估计F_e(b)=在成本不超过b时正确完成的概率，避免为每个预算档重做一套不同策略；这里不恢复agent/Python状态或运行反事实分支，prefix只做离线结果评价。对有支持的状态类，若F_e在全部预注册budget范围均不优于F_0且至少一处更差则标该类无保留收益；曲线交叉则保留库内，仅当前b有正差的区间暴露；证据不足不删。测试冻结曲线和state分组，只读可见任务/已发生费用查询；不推断超出开发支持范围的删除资格。

最高近邻及差别：LIMBO已联合memory/budget，Forget-to-Improve已有cost-aware KEEP，成本改写已有economic utility。当前可能的差别仅是有限预算下完成成本分布交叉及保留支配规则、同策略prefix样本复用；随机支配与anytime analysis均为成熟思想，不能把CDF表示本身叫新机制，待独立审。

## 最小实验

AppWorld train生成冻结库、dev收集共同最大horizon轨迹并用offline公开执行快照评价prefix，official test只aggregate。同actor/解码/任务/库/检索k/最大单次输出与全链路总API+工具预算，比无经验、固定检索、一档成功差屏蔽、明确可实现的LinUCB(memory on/off×预算档、reward=成功-lambda费用)、按完成成本分布偏序的保留/暴露。后两者共享同一开发rollout总费用，所有曲线估计/库构建/选择费均计；两方法各预算档固定同核心条件。dev诊断曲线是否交叉、prefix重用与逐档独立运行是否在共同budget-blind策略下相符；test报告成功/全部任务、总成本、库保留量，误删局部有益只dev独立全面干预参照。若LIMBO式成本控制或一档标量已等效、交叉不存在、prefix不能代表短预算策略或估计花费抵掉节省，则推翻。模型、任务类、最大horizon、budget单位/范围、k、lambda、样本量待确认。

基线定义/复现：[{"name": "无经验/固定top-k/独立贡献屏蔽", "paper_url": "https://arxiv.org/html/2606.15390", "code_url": null, "reproduction": "完整标准定义：无经验不注入；top-k按固定文本相似度取k条；独立屏蔽在开发任务对固定Bernoulli掩码有无经验的成功差取均值、同任务邻居加权后仅保留非负条目。是明确标准基线，不冒充ASSAY官方实现。", "controlled_parameters": "同actor/解码/任务划分/技能库/检索容量/全链路总预算", "extra_costs": "开发归因rollout、embedding、注入、任何重试全计费"}, {"name": "AppWorld ReAct基础agent", "paper_url": "https://github.com/StonyBrookNLP/appworld", "code_url": "https://raw.githubusercontent.com/StonyBrookNLP/appworld/main/experiments/code/simplified/react_code_agent.py", "reproduction": "已亲读environment.py execute与save/load_state；simplified/react_code_agent.py next_execution_inputs_usage_and_status读取工具输出、调用language_model.generate、记录usage并生成代码；simplified/agent.py为执行循环。可用公开train/dev/test任务及AppWorld CPU世界，未来需安装而本阶段未执行。", "controlled_parameters": "同任务、模型和预算", "extra_costs": "应用模拟CPU耗时与API全计"}]
