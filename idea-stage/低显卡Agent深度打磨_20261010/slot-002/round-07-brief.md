## 背景

关键词：functional compression、side information、tool-use memory。Q002正确回答后的选择绑定可丢失，Q003压缩后可合法错实体。依据[AppWorld-UL §4/§6.7](https://arxiv.org/html/2607.20536v1)的用户独占知识/错误分析与[TRACE §7](https://arxiv.org/html/2608.06503v1)。[PAIR §3.1](https://arxiv.org/html/2609.36526v1)指出AppWorld缺失环境信息可以额外交互重建，额外步骤与成功不同。当前聚焦可恢复当前事实与不可由当前工具重建的历史选择关系，不主张所有缺失状态同类。

## 核心 Claim

假设当前动作所需的历史区别应按可见工具的可恢复性分配记忆，而非统一span效用；保留不能由正常工具读取重建的问答/历史选择关系，并把可恢复环境属性移到实际只读查询，在同完整成本下减少Q002错绑和Q003静默错对象。

## 方法设计的核心思想

将可见指令/实际问答/source-supported联合调用候选变成需区分的候选对。只有公开API schema和已知正常读明确返回该字段，且该区别属于当前环境事实而非历史选择/原问题选项时，才允许用实际重读作为区分边的载体；用户意图、确认时选择对象及历史关系不由当前工具结果代替。CPU联合选择逐字历史见证或合法只读query的覆盖，目标是在共享token/工具预算内覆盖当前所需区别；查询实际执行一次后其真实结果加入actor上下文，任何预测/重读失败保留为失败。未见未来数据不参加选择，不执行备选写动作，不宣称source判断正确。数据库函数通信的已知图压缩只提供原理，没有套通用压缩定理。

[Functional Compression through Graph Coloring](https://www.mit.edu/~medard/2010papers/funccomp.pdf)的函数/side-info必须区分原理已知；固定准确分布/函数不能迁移，方法不使用未实际读取的值。[ARC](https://arxiv.org/html/2607.25066v1)已有归档回取，[FOCUS](https://arxiv.org/html/2609.37590v1)已有未来span效用，[SAGE](https://arxiv.org/html/2511.08798v1)已有cost-sensitive澄清。此处存储/实际工具读取联合选择的独立性仍需核实，不把基本覆盖优化当新数学。

## 最小实验

AppWorld公开API同边界澄清任务，配对当前动作区别由用户回复决定或可由正常只读查询重建；再加当前字段变化但历史用户选对象不变条件。对照按recency保留、按FOCUS原文span未来引用选择（完整可实现原文协议）、只存全部Q/A及全属性、同parser但允许工具读替代所有区别、只存不重读。固定actor/解码/来源集合/工具/token与总输入输出预算。全任务统计来源分类错、实际query返回是否能区分、绑定/旧约束、合法错实体、Task Success与总成本。隐藏用户知识/终态只离线，不给在线方法；每次parser、查询、压缩、source回取/续跑成本计入。若只是更多查询解释改进、错误把历史区别当当前可恢复、同总预算不及全部Q/A保留，推翻。模型/预算/候选数/query上限/样本数待确认。

[AppWorld](https://github.com/stonybrooknlp/appworld)和[新任务指南](https://raw.githubusercontent.com/StonyBrookNLP/appworld/main/guides/developing_new_task_generators.md)入口已亲读。单纯Q/A全保留基线：按同token上限逐字存全部已到达Q/A、工具属性正常摘要；只有历史源见证基线：同候选和parser选择原文，不执行额外requery；单纯全部requery基线：对声称可读字段都实际读，用户历史关系仍只从已见原文取，不偷用隐藏知识。CPU覆盖是完整可实现标准定义，每source覆盖pairs与已见schema读返回字段映射，query结果只在实际读后使用。FOCUS按原文算法/提示在同任务重实现；TRACE公共runner/模板允许新adapter新cohort，原研究harness未公开，不称完整原作复现。本轮未实验。
