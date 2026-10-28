## 背景

关键词：teaching set、version space、tool argument uncertainty。Q002正确问答可丢失跨问题绑定，Q003压缩后可合法地选错对象；依据[AppWorld-UL §6.7](https://arxiv.org/html/2607.20536v1)与[TRACE §7](https://arxiv.org/html/2608.06503v1)。当前聚焦可见来源的联合候选区分，不声称覆盖未知未来和所有更新使用失效。

## 核心 Claim

假设保留可见来源在当前工具候选集合上诱导的区分关系，比保留最高可能动作或独立参数边际更能减少正确多问答回答后的错绑及压缩后合法错对象动作；不要求原文actor动作正确，也不把任何候选当金标准。

## 方法设计的核心思想

在压缩边界由冻结actor一次生成有限schema-valid候选工具调用。对原始指令、问题-回复完整对和已见观察，抽取每条来源约束对候选的支持/排除/未知签名及原文位置。每条来源区分其签名不同的候选对。CPU贪心按新分开的候选对数/原文token选来源，使压缩上下文尽可能保留完整可见来源诱导的候选等价分区；无法分开的对连同未知状态明确提供actor，不伪装单值绑定。actor仅以所选逐字原文及固定任务指令决策。新实际观察到来后重生成候选和签名，不预知未来；原始观察可归档但任何回取计预算。没有正确候选或所有签名同错都不保证恢复。

[Teaching dimension](https://www.sciencedirect.com/science/article/pii/S0022000085710033)启发最小见证，已知正确概念教师不可迁移，故此处保存所有来源签名诱导的分区。[SAGE §3.2–3.3](https://arxiv.org/html/2511.08798v1)已有独立参数域belief维护，[FOCUS](https://arxiv.org/html/2609.37590v1)按未来引用效用选择，[KBRA §8.2](https://arxiv.org/html/2606.21732v1)按single-segment joint binding作成员支持检查；此处选择目的是有限候选的来源区分关系，问答完整对为一个来源单元，不做安全拒绝。[DPC](https://aclanthology.org/2026.acl-long.313.pdf)已用minimal distinguishing database选择SQL；本方法不生成环境，也不执行候选，只压缩实际到达证据，不以对照程序定真值。

## 最小实验

同AppWorld公开API交互压缩任务，构造各单参数域一致但可行joint tuple不同的澄清条件，及无相关性的对照。固定正确实际回答并自然压缩，所有任务统计原文候选覆盖率、源签名错误、压缩后的候选pair混淆率、绑定/旧约束正确率、合法错实体和TGC。对照完整当前关系表摘要、原文最近问答保留、同调用数同token随机见证、相同来源抽取但保留最大单参数域收缩来源；source-support partition与最终正确分开。若优势只在oracle签名条件或候选含gold筛选子集，或同完整预算不及直接原文保留，推翻部署Claim。模型/预算/候选数/关联arity/样本数待确认。

[AppWorld作者实现](https://github.com/stonybrooknlp/appworld)的AppWorld、world.execute、load_task_ids和world.evaluate已核实。任务在公开API上实现，用户按固定原目标回答，不改原终态测试。简单基线完整定义：当前关系表保存对象/约束/待办；最近问答按时间逐字保留；随机见证从同来源中同token抽取；单参数域对照按每来源排除单参数值数量选择而忽略joint tuple。核心模型、解码、token及完整总调用预算相同，候选生成/签名/压缩/回取/用户模拟/续跑皆计费。本轮没有运行实验。
