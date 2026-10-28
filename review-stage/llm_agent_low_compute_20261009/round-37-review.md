## 结论

截至 2026-10-09，**score：8.2/10；verdict：`experiment_ready`**。新意成立在窄而清楚的边界上：不是 relational join、provenance、entity binding 或 tool-schema graph 本身，而是在 AppWorld 多对象调用中，把“每个字段都有真实来源”提升为“这一组字段有返回行/父调用关系支持”，并把联合值见证以 `known supported / known contradicted / unknown` 反馈给原 actor；再用同 actor、同 raw history 和同 token/调用预算的机制对照检验其自然发生率与任务影响。

最强近邻 HyperAgent 已经覆盖 schema-value bindings、同一次调用联合产出、state-conditioned support graph 和 deterministic runtime binding validation，因此调用级联合检查不能作为新意；Entity Binding Failures、PACT 和 Binding Drift 也使逐参数 provenance、实体 gate 与跨步绑定保持不再新颖。但已核验的一手材料没有给出按列表行及父调用键重建业务关系 tuple、允许有据跨行 join、并把缺少联合见证与真正冲突区分开的 AppWorld 运行时机制。R1/R2 只是证明 marginal-only 信息不足的教材级诊断，不被包装成新定理；AppWorld 自然错配频率则被明确保留为待检验假设。

值得继续，且无 fatal blocker。官方 [AppWorld](https://arxiv.org/abs/2407.18901) 与[公开仓库](https://github.com/StonyBrookNLP/appworld)提供匹配任务、SimplifiedFunctionCallingAgent、`appworld run auto` 入口、环境 I/O 与 API 调用日志；所列逐字段、same-invocation、same-row 和显式键 join 控制在同一 runner 上可实现。HyperAgent 当前作者页只给论文链接、未给公开代码，因此将其作为强近邻而非不可复现 baseline 是诚实边界。显式关系覆盖低、same-row 已等效、自然错配无实际影响或 native 同预算已正确组合均已写成停止条件，属于可证伪风险，不是 Claim 或可行性阻断。

## Claim 判断

| Claim | 判断 | 关键依据 |
|---|---|---|
| 逐字段 grounding 不等于关联参数的联合 grounding | **部分重合** | [HyperAgent](https://arxiv.org/abs/2608.02650) 明确要求输入联合可用、输出由同一次调用联合产生，并维护 runtime schema-value bindings；[Entity Binding Failures](https://arxiv.org/abs/2606.30531) 要求多实体绑定均正确。两者支持问题边界，但前者主要是 schema/调用级联合，后者主要是逐实体解析，均未展示行级关系 tuple。 |
| 保留返回行、调用 ID 与父参数，按公开实体键自然 join 后对候选参数组给三值判定 | **新颖，带明确近邻** | HyperAgent 的 deterministic binding validation 与同调用 hyperedge 是最接近机制；[PACT](https://arxiv.org/abs/2605.11039) 已做跨步骤参数 provenance 和逐 argument contract。现有一手描述没有覆盖非恶意、多对象参数之间的业务关系 join、合法跨行支持与 `unknown` 非拒绝语义。 |
| R1/R2 同 marginal、不同关系可诊断 marginal-only 控制丢失联合信息 | **已被覆盖（原理），本实验用途成立** | 这是关系模型的基本事实，不构成理论新意；它能隔离表示和控制能力，但不能证明 AppWorld 或 HyperAgent 自然存在该缺陷，brief 已明确限制其结论。 |
| AppWorld 自然轨迹存在跨对象无支持组合，关系见证可在同预算下改善可靠性 | **新颖但未证实的经验 Claim** | AppWorld 提供多应用、长程 API 任务与可审计执行日志，但检索到的论文没有报告该错误的自然频率。独立标注错配、额外补查、合法跨行组合及任务结果，并允许零效应结论，使该 Claim 可直接证伪。 |
| 最小实验有匹配任务、公开实现与具体复现入口 | **可行，部分重合** | 官方仓库公开 `simplified_function_calling_agent`，支持 `appworld run auto --agent-name simplified_function_calling_agent --model-name {共同actor} --dataset-name dev`；测试与实现暴露逐交互输出和 API 调用记录。HyperAgent 未发现作者公开实现，不能作为可执行 baseline，但 native FC 加三个完整机制控制足以检验所声明增量。 |

## 最高近邻

1. [HyperAgent: Planning and Acting over Tool-Schema Hypergraphs for Tool-Use LLM Agents](https://arxiv.org/abs/2608.02650)：同在 AppWorld，已有 schema-value state、同调用联合产出、state-conditioned support graph 与 deterministic runtime binding validation；差别是公开方法没有说明按返回行/父调用键验证具体值 tuple，也没有三值关系反馈。
2. [Entity Binding Failures in Tool-Augmented Agents](https://arxiv.org/abs/2606.30531)：已有多实体 binding、entity-resolution preconditions、逐实体 provenance、澄清与执行 gate；差别是受控企业任务按各实体是否解析判定，不验证多个真实参数值之间的业务关系，也不是 AppWorld 同预算实验。
3. [The Granularity Mismatch in Agent Security: Argument-Level Provenance Solves Enforcement](https://arxiv.org/abs/2605.11039)：PACT 已追踪跨步骤参数来源并在调用前逐 argument 检查；差别是目标为不可信来源与权限角色约束，未检查可信值之间的 owner/id 关系 tuple，且 AgentDojo 不是同任务 baseline。
4. [Binding Drift in Multi-Step Tool-Augmented Agents](https://arxiv.org/abs/2607.18316)：已有 entity lock、provenance checkpoint 与 drift-aware gate，直接覆盖“跨步保持对象绑定”的一般思路；差别是固定 referent 的跨步漂移，不处理一次调用中多个对象字段的无支持拼接或显式键 join。
5. [In-N-Out: A Parameter-Level API Graph Dataset for Tool Agents](https://arxiv.org/abs/2509.01560)：已有文档级 output-to-input 参数依赖图，也是 HyperAgent 的图数据基础；差别是 schema 依赖与工具组合数据集，不是对实际返回行、父调用和值关系的运行时见证。

```json
{"score":8.2,"verdict":"experiment_ready","fatal_blockers":[],"novelty_conclusion":"调用级联合、schema-value binding、逐实体 provenance 与参数来源检查均已有强近邻；但 AppWorld 中按返回行和父调用显式键构造关系 tuple、区分 supported/contradicted/unknown 并在同预算下检验自然跨对象错配，未被已核验工作完整覆盖，构成窄而独立且可证伪的经验机制 Claim。","closest_neighbors":["HyperAgent","Entity Binding Failures in Tool-Augmented Agents","PACT","Binding Drift in Multi-Step Tool-Augmented Agents","In-N-Out"]}
```
