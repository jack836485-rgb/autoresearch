# 实验交接：IDEA-052

独立8.2/10，无fatal；全文见[FINAL_IDEA.md](FINAL_IDEA.md)。

## 定位与主Claim

tool-schema dependencies；state-conditioned planning；AppWorld。

逐字段值存在不直接证明它们属于同一关联对象。例如两个关系R1={(x1,y1),(x2,y2)}、R2={(x1,y2),(x2,y1)}的schema和值集合相同，但(x1,y1)只有前者支持。这个例子是教材事实，只诊断marginal-only表示，不是新定理，也不能证明某个实际agent用的state只保留marginals。自然AppWorld错配频率和任务影响仍未知。

我们保留实际调用参数、返回对象/列表行和公开父关联键，构建关系元组。下一调用的关联参数只有在公开关系中能连接时才有联合支持；已知冲突给原actor修正，覆盖不足是unknown。允许正确跨行连接，不强制所有输入来自同一物理row，不把缺少一个当前tuple等同全局无效。

## 最小实现

已读官方SimplifiedFunctionCallingAgent及runner的执行输入/返回配对点，AppWorld CLI是真实入口。增加CPU关系侧表和join，记录只限agent本来能获得的调用输入与公开返回，不读DB、hidden evaluator、gold solution。所有说明、额外补查、关系序列化、失败及CPU处理成本计入，未端到端运行。

## 实验与同预算baseline

证明控制是否保留必要关系信息，并判断自然任务中这一信息差是否真的影响调用和完成。表示例子不能替代自然诊断。

先冻结R1/R2成对表示测试，只用于关系与marginal差别，不报为AppWorld分数。再按公开多对象API结构选train/dev任务，独立标注跨关系错配、合法跨行组合及补查；dev冻结关联解释，held-out报全集成功与支持覆盖。不按主方法成功挑任务，构造例子与自然结果分开。

唯一baseline规范见全文§3.3。

## 止损及待定参数

自然错配有影响，关系join比逐字段和同call减少错误，又比同row少误报并在同预算任务更好才支持。明确关系覆盖低、same-row已等效、native已会正确结合、三值解释不可靠或全部收益来自保守不执行时停止。

关联说明仍由actor解释，可能错；明确键不总存在，历史见证也可能过期。联合支持只是业务关系必要证据，不证明用户指代或整体任务正确。教材反例和公开近邻没有相同实现不能充当已经胜过现有方法的结果。

actor快照、正式金额、task数、seed和cap在实验前确定。本轮没有跑模型实验。
