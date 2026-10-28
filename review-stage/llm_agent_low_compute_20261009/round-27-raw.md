## 结论

**日期：2026-10-09；score：7.3/10；verdict：`promising_needs_revision`。** 新意判断为**部分新颖、边界未闭合**：把公开返回的列表行、调用实例及父调用参数保留成关系元组，并只允许有联合见证的关联参数组合，确实比逐字段 provenance 更窄、更具体；但 [HyperAgent](https://arxiv.org/abs/2608.02650) 已明确要求必需输入联合可用、输出由同一次调用联合产出，并声称有确定性 runtime binding validation，因此不能把“联合性”或“同次调用绑定”本身作为新贡献。目前公开证据只支持候选可能在**具体值的行级/父调用级关系 join**上有增量，尚不能确认 HyperAgent 的实现没有覆盖该粒度。

值得继续保留为前置诊断候选，但**尚不值得直接进入正式实验计划**：AppWorld 上这种跨行/跨父调用错配仍是待检验假设，而非已观察到的 benchmark 失败；候选已把“未出现错误即停止”写成证伪条件，因而不是 claim blocker。可行性方面没有致命阻塞：官方 [AppWorld 仓库](https://github.com/StonyBrookNLP/appworld) 确认 `appworld run auto --agent-name simplified_function_calling_agent --model-name {model} --dataset-name dev` 是真实入口；[FunctionCallingAgent](https://github.com/StonyBrookNLP/appworld/blob/main/experiments/code/simplified/function_calling_agent.py) 将调用参数写入执行输入，[Agent runner](https://github.com/StonyBrookNLP/appworld/blob/main/experiments/code/simplified/agent.py) 在 `batch_execute` 后逐项配对输入与返回。官方 `ExecutionIO` 最终返回对象本身没有同时保留原参数，但公开配对点足以记录二者；native FC 加三个同任务、同预算机制控制构成可执行对照。

## Claim 判断

| Claim | 判断 | 关键依据 |
|---|---|---|
| “每个参数均有来源且 schema 合法，仍可能因跨返回行/父调用组合而错配”是独立失败类型 | 部分重合 | [Entity Binding Failures](https://arxiv.org/abs/2606.30531) 已覆盖“正确工具、错误实体”、多实体绑定和 provenance；候选更窄地指向已有具体值之间的关系不一致，但 AppWorld 中该失败的发生率尚未观察。 |
| 逐字段 provenance 或 schema-set availability 不能证明参数共同属于同一目标 | 部分重合 | HyperAgent 已区分逐端口依赖与工具 hyperedge 的联合约束，并让一个 producer 联合支持多个输入；[PACT](https://arxiv.org/abs/2605.11039) 也已证明逐参数来源跟踪有用。二者都未在公开文字中明确给出跨列表行/父调用的业务关系 join。 |
| 以调用实例、返回行、父参数组成关系元组，并按公开实体键 join 后再执行 | 新颖但未闭合 | 未检索到最高近邻明确采用这一运行时实例级元组；但 HyperAgent 已声明“同次调用联合产出”及 runtime binding validation，缺少公开实现使二者机制边界无法最终核验。 |
| 同预算比较 native FC、独立来源表、逐字段 provenance、schema-set 与联合元组，可归因于联合绑定 | 新颖且可检验 | 控制仅改变独立值集合与关系元组；模型、任务、调用和 token 上限固定，另报错配、补查与合法跨对象调用，可区分收益与拒绝导致的表面成功。官方 FC 入口和输入/输出配对源码已核验。 |

## 最高近邻

1. [HyperAgent: Planning and Acting over Tool-Schema Hypergraphs for Tool-Use LLM Agents](https://arxiv.org/abs/2608.02650)（2026）。重叠最大：AppWorld、port/schema 依赖、多个 producer、联合输入可用、同调用联合输出、运行时绑定校验；差别只剩公开文字未定义列表行/父调用实例的关系元组 join，因此当前新意边界未闭合。

2. [Entity Binding Failures in Tool-Augmented Agents](https://arxiv.org/abs/2606.30531)（2026）。已定义正确工具但错误实体、多实体绑定、entity provenance 与执行前 gate；其算法逐 mention 检索和判定，未描述由真实返回行及父调用共同见证的跨参数关系 join，且实验不是 AppWorld。

3. [In-N-Out: A Parameter-Level API Graph Dataset for Tool Agents](https://arxiv.org/abs/2509.01560)（2025）。已在参数级标注 API 输入输出依赖，是 HyperAgent 的直接图数据基础；主要处理静态 schema/port 关系与工具组合，不处理一次运行中多个具体返回对象之间的行级绑定。

4. [The Granularity Mismatch in Agent Security: Argument-Level Provenance Solves Enforcement and Isolates the LLM Reasoning Bottleneck](https://arxiv.org/abs/2605.11039)（2026）。PACT 跨步骤跟踪每个参数的来源并按参数角色检查；重叠在细粒度 provenance，差别是其目标为安全信任约束，未做业务实体关系元组 join，也不是同任务实验 baseline。

5. [AppWorld: A Controllable World of Apps and People for Benchmarking Interactive Coding Agents](https://arxiv.org/abs/2407.18901)（2024）。提供同任务公开环境、状态式评测和多对象 API 工作流；它支持候选的实验入口与 collateral-damage 检查，但论文没有报告候选所称跨行/跨父调用错配，故只能支撑可测性，不能支撑失败已存在。

```json
{"score":7.3,"verdict":"promising_needs_revision","fatal_blockers":[],"novelty_conclusion":"实例级返回行/父调用关系元组及联合见证可能构成窄增量，但HyperAgent已覆盖联合可用、同调用联合产出和运行时绑定校验，公开证据尚不能闭合二者边界；AppWorld官方FC入口与同预算控制可执行。","closest_neighbors":["HyperAgent: Planning and Acting over Tool-Schema Hypergraphs for Tool-Use LLM Agents (2026)","Entity Binding Failures in Tool-Augmented Agents (2026)","In-N-Out: A Parameter-Level API Graph Dataset for Tool Agents (2025)","The Granularity Mismatch in Agent Security: Argument-Level Provenance Solves Enforcement and Isolates the LLM Reasoning Bottleneck (2026)","AppWorld: A Controllable World of Apps and People for Benchmarking Interactive Coding Agents (2024)"]}
```
