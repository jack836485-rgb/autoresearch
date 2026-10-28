## 结论

**日期：** 2026-10-09  
**Score：** 6.8/10  
**Verdict：** `promising_needs_revision`

**新意判断：** “τ²/τ³ telecom 的 dual-control 降分主要来自用户动作后继续沿用陈旧设备状态”是尚未被 τ²-bench 论文证明的任务内因果假设，具有可检验的新意；但“显式维护状态/来源/有效性，并按依赖范围局部撤销或重新验证”已与 STALE/CUPMem、MemTX、PlanFence 高度重合。剩余差别主要是把该机制收窄到客服 dual-control 中由用户可见动作触发、再向用户重查可观察状态，而不是一个新的通用状态更新原理。

**是否值得继续：** 值得继续做任务内诊断，但当前不满足 `experiment_ready`。致命可行性阻塞是 baseline 与复现证据不完整：同任务公开的 AgentSWE 已在 τ²-Bench 上实现逐轮持久化结构化 `state`/plan/verify，并给出公开代码与 telecom 结果；brief 的自定义“结构化状态提示”没有证明与该实现的关系，也没有纳入其公开复现路线。与此同时，实验入口仍指向会变化的 τ³ 主分支，模型、用户模拟器、任务集合和试验次数仍为占位符，尚不是可复现的冻结实验合同。

## Claim 判断

| Claim | 判断 | 关键依据 |
|---|---|---|
| τ²-bench 中 dual-control 比 no-user 更难 | 已被覆盖 | 原论文直接报告 Default 相比 No-User 的 pass^1 分别下降 18%（GPT-4.1）和 25%（o4-mini），并将差距概括为通信与去中心化控制负担。 |
| 主要失败机制是用户动作使旧设备事实失效，而 agent 继续沿旧事实排查 | 新颖但未验证 | τ²-bench 只给出聚合差距及 reasoning/communication 分解，没有报告陈旧状态是主要原因；brief 正确地把它写成待诊断假设，而非已观察结论。 |
| 用“值 + 可见来源 + 相关动作类型”表示事实，用户动作后仅把受影响事实标为未知 | 部分重合 | STALE/CUPMem 已研究隐式冲突、状态消解与传播感知更新；MemTX 已给记录附加 evidence/provenance/validity 并在撤销时级联修复；PlanFence 已按动作依赖范围验证局部状态。用户动作触发和不读取隐藏日志是更窄的任务实例。 |
| 选择性失效可同时少用陈旧事实、又比全部失效少重问 | 部分重合 | 这是清楚且可证伪的任务内比较，但 PlanFence 已比较 dependency-scoped 与 all-key validation 的成本边界；当前 brief 尚无证据表明在 telecom 中存在足够多可区分两者的陈旧事实案例。 |
| LLMAgent、结构化状态、全部失效、选择性失效构成同预算最小实验 | 部分成立 | 官方 LLMAgent 接口与 telecom 环境公开，四臂也能隔离局部撤销；但同任务 AgentSWE 状态追踪公开实现未纳入，且仓库 commit、模型/模拟器和任务集合未冻结，故 baseline 证据与具体复现路线未闭合。 |

## 最高近邻

1. [τ²-Bench: Evaluating Conversational Agents in a Dual-Control Environment](https://arxiv.org/abs/2506.07982)（[官方代码](https://github.com/sierra-research/tau2-bench)）：与候选使用相同 telecom dual-control、用户工具和最终状态评测；论文证明 dual-control 降分，但没有把降分归因于陈旧事实，也没有提出选择性失效机制。
2. [AgentSWE 的 τ²-Bench 比赛说明](https://rdi.berkeley.edu/agentx-agentbeats.html)（[公开实现](https://github.com/soumya-batra/tau2-agentbeats)）：同任务逐轮维护结构化 plan、事实 state、verify，并报告 telecom 101/114；它没有显式的动作影响映射或局部失效语义，但与 brief 的“结构化状态提示”是必须核验的直接 baseline 近邻。
3. [STALE: Can LLM Agents Know When Their Memories Are No Longer Valid?](https://arxiv.org/abs/2605.06527)（[CUPMem 代码](https://github.com/icedreamc/STALE)）：同样研究后续事件隐式使旧事实失效，并用结构化整合与传播感知搜索更新状态；差别是长程个性化记忆问答，而非共享环境中的工具动作与用户重查。
4. [Fresh Memory, Stale Plans: Derivation Currency for Distributed LLM-Agent Memory](https://arxiv.org/abs/2609.03340)：其 PlanFence 为计划记录精确输入来源，并在动作前只验证动作相关依赖，和“来源 + 相关动作 + 局部重验”高度重合；差别是多 agent 公共记录与权威 owner 校验，不是客服对话中的用户可见状态询问。
5. [MemTX: Transactional Belief Commit for Stateful Agent Memory](https://arxiv.org/abs/2607.23929)（[公开代码](https://github.com/lxy1134/MEMTX)）：记录 evidence、provenance、validity，撤销 belief 后做类型化级联修复；覆盖了通用的来源感知失效思想，但其事务提交、风险门控和共享持久记忆明显重于本候选的 CPU 局部状态表。

```json
{"score":6.8,"verdict":"promising_needs_revision","fatal_blockers":["同任务公开的 AgentSWE 结构化状态追踪实现未被纳入 baseline 核验，自定义结构化状态提示不足以替代已公开的同任务实现与结果","复现合同尚未冻结：τ³ 仓库 commit、agent/user 模型快照、任务集合、trial 数仍未确定，当前命令含占位符"],"novelty_conclusion":"任务内的陈旧状态因果诊断仍有新意，但选择性失效的通用机制已被 STALE/CUPMem、PlanFence 和 MemTX 显著覆盖；现阶段更像未验证的 τ²/τ³ telecom 专项实例，而非已建立边界的独立通用方法。","closest_neighbors":["τ²-Bench","AgentSWE τ²-Bench state-tracking implementation","STALE/CUPMem","Fresh Memory, Stale Plans / PlanFence","MemTX"]}
```
