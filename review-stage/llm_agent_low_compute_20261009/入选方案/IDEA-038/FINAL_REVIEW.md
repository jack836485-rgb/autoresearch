## 结论

**日期：** 2026-10-09  
**Score：** 8.4/10  
**Verdict：** `experiment_ready`  
**新意判断：** 部分方法原语已有成熟先例，但当前 Claim 在工具 agent 文献中具有清楚且未被直接覆盖的任务化新意：针对 ScrambleToolBench 的不完整旧映射，不提交到任一单一最优匹配，而保留全部最小改动解释对当前目标 alias 的支持，再用按最坏分支缩小目标候选集的 probe 消歧。其新意不在最小费用匹配或主动查询本身，而在局部 mapping drift、partial map、任务目标定位三者的组合及同任务机制验证。  
**是否值得继续：** 是。ScrambleToolBench 已实证漂移后的 belief inertia、穷举回退和高动作开销，并明确报告完整图假设在真实轨迹中通常不成立；“单一最优解释会过早确定”仍是待验证的诊断假设，brief 没有把它冒充已观察事实。实验固定同一公开 benchmark、actor、历史、step/token 预算和漂移协议，且包含 default、结构化知识表、cycle tracing、单最佳 matching、无旧先验可行集，足以区分集合保留、稀疏先验和纯外置记忆的贡献。公开仓库当前只原生提供 `default` agent，但 brief 已如实把其他方法定义为同一 runner 上的本地标准实现，并给出具体入口，因此不构成 fatal blocker。

## Claim 判断

| Claim | 判断 | 关键依据 |
|---|---|---|
| 漂移后存在 belief inertia、穷举回退与高恢复成本 | 已被覆盖 | ScrambleToolBench 直接报告这些失败；这应作为问题证据，不是本工作的新增贡献。 |
| 原 cycle tracing 在不完整旧图下缺乏保证并可能退回扫描 | 已被覆盖 | 原文的保证要求漂移前完整且当前的双向表；旧条目缺失或行为不可识别时明确回退穷举，并报告 Task 1 平均仅发现约 20.75/28 与 21.90/28 个工具。 |
| 在 partial map 下保留全部最小改动匹配对目标位置的支持，优于任取一个最优匹配 | 新颖 | 未检索到工具使用工作以该机制处理 alias permutation drift；但“全部最优/最小诊断而非单解”属于既有约束推断与诊断思想，新增性主要来自问题实例化和因果验证。 |
| 用可识别工具响应选择最小化最坏分支目标候选数的 probe | 部分重合 | 版本空间、广义二分和主动诊断早已按查询结果划分假设集；当前差别是只围绕任务所需行为的位置，在最小改动完美匹配支持集上计算，并把 probe 计入同一 API 预算。 |
| 集合保留能在同预算下减少错用/额外扫描并提高成功率 | 新颖、未验证 | 这是清楚可证伪的实验 Claim；单最佳 matching、无先验集合、cycle tracing 和完整图分层能直接检验。尚无结果，brief 对此表述克制。 |
| 最小实验可执行且 baseline 匹配 | 成立 | 官方仓库公开 runner、确定性 seed、`tasks`、`steps_per_task`、`drift_fraction` 与轨迹输出；源码证实 drift 是对所选工具 alias 的单环轮换且 `get_agent_class` 只原生支持 `default`。本地 baseline 共享观察、控制器接口和总预算，复现路径具体。 |

## 最高近邻

1. [ScrambleToolBench: Agents Search Exhaustively Even When Their Own Map Points to the Next Step](https://arxiv.org/html/2608.02358v1)（[公开代码](https://github.com/declare-lab/ScrambleToolBench)）：与 benchmark、mapping drift、行为指纹和 cycle tracing 完全同任务；差别是其确定性恢复保证依赖完整当前表，缺旧条目时回退扫描，没有最小改动解释集合或目标条件 probe。
2. [OpaqueToolsBench: Learning Nuances of Tool Behavior Through Interaction](https://arxiv.org/html/2602.15197)（[公开代码](https://github.com/shallinan1/OpaqueToolsBench)）：同样从匿名/欠描述工具的交互反馈学习行为，并在在线模式更新工具文档；它不处理跨任务 alias 置换、不维护一一映射的最小改动集合，也不做确定性的目标位置消歧。
3. [MCPEvol-Bench: Benchmarking LLM Agent Performance Across Dynamic Evolutions of MCP Servers](https://arxiv.org/abs/2607.14642)：覆盖动态工具接口演化及其性能退化；其变化是多类 MCP schema/功能 mutation，重点是 benchmark，而非在旧 partial map 下恢复匿名置换。
4. [A Model-Based Active Testing Approach to Sequential Diagnosis](https://www.jair.org/index.php/jair/article/view/10639)：维护多个诊断解释并主动选择测试以降低剩余不确定性，与“解释集合 + probe”机制高度相近；差别是对象为模型化系统故障，不是 LLM 工具 alias 漂移，也没有最小改动二分匹配与同任务 API 预算。
5. [Generalized Binary Search for Split-Neighborly Problems](https://proceedings.mlr.press/v84/mussmann18a.html)：以查询最大化划分版本空间，是最坏分支消歧的成熟算法近邻；差别是通用顺序假设识别，不包含局部漂移先验、完美匹配约束或任务目标 alias。

```json
{"score":8.4,"verdict":"experiment_ready","fatal_blockers":[],"novelty_conclusion":"通用的最小费用匹配、版本空间保留和主动查询并非新理论，但将全部最小改动映射解释用于 ScrambleToolBench 的不完整旧图恢复，并围绕当前目标位置做同预算最坏分支 probe，未被检索到的直接工具-agent近邻覆盖；Claim 边界清楚且实验可证伪。","closest_neighbors":["ScrambleToolBench: Agents Search Exhaustively Even When Their Own Map Points to the Next Step","OpaqueToolsBench: Learning Nuances of Tool Behavior Through Interaction","MCPEvol-Bench: Benchmarking LLM Agent Performance Across Dynamic Evolutions of MCP Servers","A Model-Based Active Testing Approach to Sequential Diagnosis","Generalized Binary Search for Split-Neighborly Problems"]}
```


主执行器门槛记录：选择时为available最高8.6；独立8.4>7.5且fatal为空。未运行实验。剩余风险为行为识别、稀疏先验错误、匿名角色与CPU求解成本。
