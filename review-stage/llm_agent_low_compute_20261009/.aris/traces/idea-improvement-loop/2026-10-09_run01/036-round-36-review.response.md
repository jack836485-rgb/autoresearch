## 结论

截至 2026-10-09，**score：7.1/10；verdict：`promising_needs_revision`**。新意属于“任务特定的新组合”，而不是新的约束搜索原理：我没有找到把 TravelPlanner 中“被候选编辑删除的最后一个显式支持”直接用作至多 3-slot 联合修补种子的既有工作；但按约束依赖/解释选择变量、冻结其余变量、允许联合移动内部暂时不可行并只提交最终可行解，已经分别被 explanation-based LNS、dependency-curated LNS、dynamic-CSP minimal-change repair 和标准 LNS 覆盖。值得继续查证，但当前不值得进入实验规划：一是同任务、公开实现的 SCOPE 与 SMT/全池求解路线没有进入最小实验，尽管 brief 把“全池标准 CSP 更便宜”列为停止条件；二是主方法和三个局部基线所共享的“原 actor”没有可执行入口，官方 ReAct/Reflexion 是整份计划生成器而不是 slot-repair actor；三是 CORAL 的公平信息边界仍未闭合，其默认确实不读 oracle fields，但实际 solver 按 reference 中的城市访问完整 benchmark 城市数据库，并不从序列化的 `reference_information` 限定候选。以上是当前的致命可行性/Claim 阻断。

## Claim 判断

| Claim | 判断 | 关键依据 |
|---|---|---|
| TravelPlanner 中逐次处理约束会破坏先前已满足约束 | 已被覆盖（诊断） | [TravelPlanner](https://arxiv.org/abs/2402.01622) 已报告多约束整体跟踪困难；[Flex-TravelPlanner](https://arxiv.org/abs/2506.04649) 更直接观测到加入局部约束后预算由通过转为失败。它们支持现象，不支持本方法。 |
| CORAL 降预算会删除既有支持 | 部分有据、部分无据 | [CORAL repair 源码](https://github.com/ChouYuanjue/coral-travel-planner/blob/main/src/coral/planning/travelplanner_solver.py#L278-L323) 先补 cuisine、再删除 travel-day meals，因此删除唯一 cuisine 见证在代码上可达；但酒店替换取自 `valid_hotels`，而该集合已过滤 room type、house rule、minimum nights（[源码](https://github.com/ChouYuanjue/coral-travel-planner/blob/main/src/coral/benchmarks/travelplanner.py#L379-L402)），故“改变最低住宿要求导致既有住宿条件失效”没有现有证据。brief 正确地没有声称发生率。 |
| 用被删最后见证引出相关 slot，再做有界联合修补 | 部分重合 | “支持见证”是 TravelPlanner 特定实例化；但 [Dependency-Curated LNS](https://doi.org/10.4230/LIPIcs.CP.2025.20) 已用约束依赖得到低基数变量集合，[Explanation-Based LNS](https://doi.org/10.1007/s10601-014-9166-6) 已用冲突解释选择需放松的决策。方法级增量窄于当前表述。 |
| 允许联合候选中间暂时违约，只验最终 whole-plan | 已被覆盖 | 这是 LNS/CP 的标准 destroy-and-repair 语义，也是 minimal-change dynamic CSP repair 的既有设定；不能单独承担新意。 |
| 同预算下，见证定向邻域比随机同大小邻域更少摆动且最终成功更高 | 新颖但未证实 | 这是清楚、可证伪的 TravelPlanner 特定经验 Claim；尚无实验，因此只能称假设。当前缺少同信息边界的 SCOPE/全池程序化求解基线，且 slot-repair actor 无可复现入口，尚不能公平归因给“见证定向”。 |

## 最高近邻

1. [CORAL Travel Planning](https://github.com/ChouYuanjue/coral-travel-planner)：同一 TravelPlanner、公开代码、raw-query grounding 与局部 cuisine/hotel/budget repair，任务重叠最高；差别是 CORAL 顺序执行手写修补，没有最后见证依赖和有界联合邻域。其默认非 oracle，但候选实际来自完整城市数据库，和 sole-planning 序列化候选的等价性尚未被代码路径证明。
2. [Dependency-Curated Large Neighbourhood Search](https://doi.org/10.4230/LIPIcs.CP.2025.20)：用约束中的变量依赖压缩 LNS 的可放松变量集合，与“围绕被破坏支持找相关 slots”高度同构；差别是通用 COP/LNS、从可行 incumbent 优化，不处理 LLM 提议、TravelPlanner repair regression 或同 token 预算。
3. [Explanation-Based Large Neighborhood Search](https://doi.org/10.1007/s10601-014-9166-6)：用冲突/目标域解释定位应放松的决策，再由 CP 修复，其因果邻域选择先于本方案；差别是本方案只维护公开规则的轻量支持见证，并以候选编辑将删除的最后见证触发联合提交。
4. [Programming over Thinking: Efficient and Robust Multi-Constraint Planning](https://aclanthology.org/2026.acl-long.2028/)（[代码](https://github.com/DerrickGXD/SCOPE)）：同一 TravelPlanner、同样重构 `reference_information`、公开运行入口，报告 93.1% success，并用可复用程序枚举/过滤候选；差别是从头程序化求解而非修复已有计划。它是当前最明显但缺失的同任务强基线，也直接对应 brief 的“全池重建是否更便宜”停止条件。
5. [Large Language Models Can Solve Real-World Planning Rigorously with Formal Verification Tools](https://aclanthology.org/2025.naacl-long.176/)（[代码](https://github.com/yih301/LLM_Formal_Travel_Planner)）：同一 TravelPlanner 上把多约束规划编码为 SMT，并用 unsat 原因驱动交互修复；差别是依赖人工示例与完整形式求解，不是对 actor 单编辑的最小局部修补，信息与一次性建模成本需单列才可公平比较。

```json
{"score":7.1,"verdict":"promising_needs_revision","fatal_blockers":["缺少同任务、公开实现且直接对应停止条件的 SCOPE/SMT 或同规则全池程序化求解基线，现有实验不能判断局部见证邻域是否优于完整重建","主方法及单编辑、严格保持、随机联合邻域共同依赖的 slot-repair actor 没有可执行实现或具体复现入口；官方 ReAct/Reflexion 不是该 actor","CORAL 候选范围与官方 sole-planning reference_information 的等价性尚未核验，且酒店替换会破坏最低住宿要求这一既有失败陈述不受所引源码支持"],"novelty_conclusion":"TravelPlanner 特定的最后见证触发式三槽联合修补未发现直接先例，但核心搜索机制已被解释/依赖引导 LNS 与 minimal-change CSP repair 大幅覆盖；剩余新意主要是同预算下的任务特定诊断与经验效果。","closest_neighbors":["CORAL Travel Planning","Dependency-Curated Large Neighbourhood Search","Explanation-Based Large Neighborhood Search","Programming over Thinking (SCOPE)","Large Language Models Can Solve Real-World Planning Rigorously with Formal Verification Tools"]}
```
