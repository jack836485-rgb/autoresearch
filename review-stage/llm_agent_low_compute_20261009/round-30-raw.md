## 结论

**日期：** 2026-10-09  
**Score：** 6.8/10  
**Verdict：** `promising_needs_revision`

新意判断：**部分新颖，但尚不足以进入实验规划。** 在同一 SWE-bench 修复轨迹内，只对共同已执行的 pytest nodeid 做跨轮 P→F/F→P 状态差分，并在固定反馈 token 预算中优先展示本轮新增回归，这个完整操作没有被下列单篇近邻直接覆盖；MiniSWE 的公开配置也确实在输出超过 10,000 字符时只保留头尾各 5,000 字符。不过，P→F/F→P 差分本身、面向编码 agent 的回归抑制、相关回归测试筛选以及 pytest/tool-output 压缩都已有直接先例，因此贡献更接近一个特定于轨迹内反馈分配的组合机制，而不是新的测试或回归诊断范式。

值得继续，但当前存在 fatal baseline blocker：最小实验只有 native/pytest 参数/单次结构化/失败聚类等内部控制，没有纳入已公开、同为 SWE-bench 编码 agent 且直接处理回归暴露或工具输出压缩的 TDAD、TestLoc/TestPrune、Squeez。按给定 rubric，这使实验无法区分收益究竟来自“跨轮状态差分”，还是来自已有的测试定位、回归约束或相关输出剪枝。另一个非致命但决定性的不确定性是，候选已正确把“中段遮蔽新增回归并诱发后续误修”写成待诊断假设；现有公开配置只能证明裁剪会发生，不能证明该因果链在自然 SWE-bench 轨迹中有足够发生率。

## Claim 判断

| Claim | 判断 | 关键依据 |
|---|---|---|
| MiniSWE 对超过 10,000 字符的 observation 保留头尾各 5,000 字符，且只提供整次命令 return code | 已被公开实现覆盖（事实成立） | 官方 `swebench.yaml` 的 `observation_template` 明确执行该 head-tail 裁剪并单列 `<returncode>`：[实现](https://github.com/SWE-agent/mini-swe-agent/blob/main/src/minisweagent/config/benchmarks/swebench.yaml)。 |
| 自然修复轨迹中，旧失败/重复日志会把本轮新增回归挤到中段，导致 agent 继续追旧错误并累积破坏 | 尚未成立的诊断假设 | 裁剪实现支持“可能被隐藏”，但当前没有轨迹发生率、被遮蔽 nodeid 或后续决策转移证据；brief 将其列为先诊断再决定是否继续，因而没有冒充已观察结论。 |
| 对共同已执行测试做跨轮 P→F/F→P 差分，并优先把 P→F 及代表反例分配给有限反馈预算 | 部分重合、边界上有新意 | AgentDevel 已将 P→F/F→P 作为一等证据，TDAD 已在 SWE-bench 中显式降低 pass-to-pass regressions；但它们没有直接给出“同一修复轨迹、共同 pytest nodeid、固定 observation budget 下的新回归优先序列化”。 |
| 该机制不是一般日志去噪或失败聚类，而是跨轮状态变化带来的额外信号 | 新颖性可检验，但尚未与最高近邻隔离 | 单次结构化与失败聚类控制能排除一部分替代解释；Squeez 已直接针对 pytest 等 tool output 做任务条件剪枝，TestLoc 已筛选并在修改前后运行相关回归测试，二者未进入实验表。 |
| 在相同模型、token、调用与工具预算下，可用 resolved、后续回归和新回归可见率证伪机制 | 基本成立 | 设计给出相同模型快照、顺序、seed/温度、最大步数及总 token/调用上限，并设置“短输出已够、无真实遮蔽、单次结构化同效或公开测试覆盖不足即停止”；但缺失公开近邻 baseline 使比较集目前不完备。 |

## 最高近邻

1. [TDAD: Test-Driven Agentic Development](https://arxiv.org/abs/2603.17973)；[公开实现](https://github.com/pepealonso95/TDAD)。同为 SWE-bench 编码 agent，显式追踪 pass-to-pass regressions，并用代码—测试影响图把受改动影响的测试呈现给 agent；差别是它在执行前选择/运行高风险测试，而候选在 agent 已运行的共同测试上做跨轮结果差分和反馈预算重排。

2. [Can Old Tests Do New Tricks for Resolving SWE Issues? / TestLoc-TestPrune](https://arxiv.org/abs/2510.18270)；[公开实现](https://github.com/IBM/Issue-Test-Localizer)。同样针对 SWE-bench 中大型回归测试集的上下文噪声与成本，公开工具支持在修改前后运行最小相关回归集；差别是它改变/缩小执行测试集合，候选不增加或选择测试，只重排相同已执行测试的可见反馈。

3. [Squeez: Task-Conditioned Tool-Output Pruning for Coding Agents](https://arxiv.org/abs/2604.04979)；[公开实现](https://github.com/KRLabsOrg/squeez)。直接压缩 SWE-bench 工作流中的 pytest、stack trace 等 tool output，并提供 `pytest ... | squeez` 的可运行入口；差别是它用训练模型按查询抽取单次相关片段，候选用 CPU 确定性跨轮状态差分识别新增回归。

4. [AgentDevel: Reframing Self-Evolving LLM Agents as Release Engineering](https://arxiv.org/abs/2601.04620)。最直接覆盖 P→F/F→P “flip-centered” 原语，并优先把回归作为一等证据；差别是比较 agent 发布版本在 benchmark 样例上的翻转并据此门控发布，不处理单条代码修复轨迹中的 pytest observation。

5. [ExecCritic: Learn to Test, Test to Improve for Coding Agents](https://arxiv.org/abs/2609.09133)；[公开实现](https://github.com/MSR-Orchard/execcritic)。在 SWE-bench Verified 上用冻结测试和有界执行反馈驱动多轮修复，直接证明执行反馈质量会改变 resolved；差别是其主要贡献是独立生成/验证测试与训练 repair policy，候选只利用现有公开 pytest 的跨轮状态变化且不训练。

```json
{"score":6.8,"verdict":"promising_needs_revision","fatal_blockers":["缺少同任务且有公开实现的最高近邻实验基线：TDAD、TestLoc/TestPrune 与 Squeez；当前内部控制不足以把跨轮状态差分的贡献与已有回归测试定位、回归约束或工具输出剪枝区分开"],"novelty_conclusion":"完整机制在‘同一 SWE-bench 修复轨迹中，对共同已执行 pytest nodeid 做跨轮 P→F/F→P 差分，并在固定反馈预算中优先呈现新增回归’这一窄边界上未见单篇工作直接覆盖；但核心原语和相邻功能分别已被 AgentDevel、TDAD、TestLoc/TestPrune 与 Squeez 覆盖，因此属于部分新颖的组合机制，当前不满足 experiment_ready。","closest_neighbors":["TDAD: Test-Driven Agentic Development (arXiv:2603.17973)","Can Old Tests Do New Tricks for Resolving SWE Issues? / TestLoc-TestPrune (arXiv:2510.18270)","Squeez: Task-Conditioned Tool-Output Pruning for Coding Agents (arXiv:2604.04979)","AgentDevel: Reframing Self-Evolving LLM Agents as Release Engineering (arXiv:2601.04620)","ExecCritic: Learn to Test, Test to Improve for Coding Agents (arXiv:2609.09133)"]}
```
