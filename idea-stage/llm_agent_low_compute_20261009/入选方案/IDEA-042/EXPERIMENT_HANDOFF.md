# 实验交接：IDEA-042

独立7.9/10，无fatal；全文见[FINAL_IDEA.md](FINAL_IDEA.md)。

## 定位与主Claim

iterative specification refinement；structural erosion；coding agents。

待验证的窄假设：近似clone的共同外形不代表它们沿同一需求维度变化；合并不同变化轴后，下一次扩展可能又把函数切开。必须在自然轨迹检查这一链条；不能把增加需求的复杂性本身当成迭代引起退化。

我们用已发生的spec与代码diff解释anti-unification孔。只有已有至少两个实例、并有仅一个维度不同的分离证据时，才建议对该维度提炼共享骨架；联合变化或缺少证据时不提前独立抽象。这约束重构动作，不添加尚未发生的feature flag、迁移层或未来接口。

## 最小实现

已读公开MiniSWE wrapper、真实DefaultAgent/API接口、local/Docker环境、配置和run指南。入口slop-code run可运行；CPU新增AST对齐与证据表。重要修正：公开AgentCostLimits只有step/cost/net-cost，没有总token硬上限，实验需在模型调用处统一新增记账与中止；不能伪称cost_limits已提供token cap。prompt名是anti_slop/plan_first，非连字符。

## 实验与同预算baseline

判断当前更谨慎的抽象是否在未知下一轮需求中减少重新切开/重复复制，并提高同预算完成。单纯降低被自己优化的CC没有价值证据。

使用冻结的当前公开问题列表，不混用原论文20问题/93checkpoint与后续公开扩展语料的分数。当前每轮只能见当前spec，hidden tests只用于离线评测且结果不返回agent。各组同初始空工作区、任务順序、自己代码继承规则、模型/推理/seed与完整预算。另用同一累计spec的继续编辑和from-scratch诊断区分需求扩大与路径依赖，不免费给未来累计spec。

唯一baseline规范见全文§3.3。

## 止损及待定参数

自然错误合并变化轴存在，证据约束比clone-only/固定重构改善后续正确率或成本，当前正确性不明显损失才支持。没有后续收益、轴解释低可靠性、分析token抵消节省、或只有自优化指标变好则停止。

需求维度解释仍依赖actor，少量实例不证明未来独立性。当前clone指标降低可能只是优化指标，没有维护收益。AST对齐和重构开销可能更贵；不能用隐藏下一轮规格、完美人工轴标签或额外重构预算制造优势。

actor快照、正式金额、task数、seed和cap在实验前确定。本轮没有跑模型实验。
