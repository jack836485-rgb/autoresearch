## 结论

日期：2026-10-09。**Score：7.1/10；Verdict：`promising_needs_revision`。** 新意主要成立在组合与评测层面：把持续、参数响应型 silent fault、BFCL 多轮执行、有限调用预算和 false-confidence 语义放进同一在线诊断实验，目前未发现直接同构工作。但核心算法 Claim 不独立：MR×fault 可辨别矩阵、按剩余故障覆盖贪心选择关系，以及依据测试结果保留未排除候选，分别被 fault-based MR prioritization 和经典顺序故障诊断覆盖。问题锚点有论文证据，因果假设可证伪，同任务公开代码和运行入口也可核验；当前版本有条件值得继续，但未达到 `experiment_ready` 门槛。

致命阻塞有两项：一是“按故障与关系可辨别性选择少数探针”的核心机制与既有 fault-based MR prioritization 近乎同构；二是“探针通过只删除可排除解释、其余保持 unknown”属于经典候选集消元语义，不能作为新的诊断原则。它们阻塞当前方法新颖性主张，不阻塞该组合能否实现和做实验。

## Claim 判断

| Claim | 判断 | 关键依据 |
|---|---|---|
| 持续隐式工具故障及正常格式错误会被 agent 过度信任 | 部分重合 | [Tools Fail](https://aclanthology.org/2024.emnlp-main.790/)、[ToolMaze](https://arxiv.org/abs/2606.05806) 与 [Loud Failures, Quiet Failures](https://arxiv.org/abs/2610.10062) 已分别覆盖 silent error、implicit permanent fault 和 BFCL quiet failure；“重复一致会制造假证据”仍是待验证假设，不是已有观察。 |
| 在 BFCL 中构造参数响应型、持续而非单次的 silent fault 诊断 | 新颖 | Loud/Quiet 的 quiet corruption 仅触发一次且后续调用恢复正常；ToolMaze 有永久隐式故障，但没有 BFCL 上的关系探针诊断与保守置信语义。 |
| 从公开文档冻结只读工具的 MR 库并执行 seed/follow-up 检查 | 部分重合 | [ARMeta](https://arxiv.org/abs/2605.28321) 已从 API 规范构造并执行 equality、inclusion、exclusion、difference 等关系；差别是本候选把关系用于运行中的 tool agent，而非离线 API 测试。 |
| 建立 MR×fault 可辨别矩阵，并在预算内贪心选择能排除最多剩余故障的 MR | 已被覆盖 | [Metamorphic Relation Prioritization](https://arxiv.org/abs/2109.09798) 已用 mutant-kill matrix，逐步选择覆盖最多剩余 mutant 的 MR，并以 random MR 为基线；fault 与 mutant 的表述变化不构成新的选择机制。 |
| MR pass 只排除该关系能排除的故障，其余保持 unknown | 已被覆盖 | 顺序故障诊断长期使用 test×fault 矩阵和候选解释更新；pass/fail 只消去与观察不相容的候选。该语义在 agent 场景很重要，但不是独立新原理。 |
| any-pass-trust 会在关系保持型坏输出上造成 false confidence | 新颖的实验问题 | 最高近邻未在 BFCL 多轮 agent 中直接比较“保守候选消元”和“一次 MR 通过即整体信任”；目前没有结果，故只能表述为可证伪假设。 |
| 同预算最小实验具备可执行 baseline | 已支持 | `brittle-agents` 公开了 BFCL frozen suite、`run_agents.py`、fault layer、`--model`、`--task-limit`、`--spend-cap` 和 check-results prompt arm；持续 fault 与 MR controller 需新实现，但不构成 baseline 证据缺失。 |

## 最高近邻

1. [Metamorphic Relation Prioritization for Effective Regression Testing](https://arxiv.org/abs/2109.09798)（[代码](https://github.com/UNF-STLab/MRPrioritization)）：与 MR×fault/mutant 矩阵、随机关系基线、预算受限的剩余故障覆盖贪心选择直接重叠；差别是它做离线回归测试，不维护 tool-agent 运行时的 unknown 状态。
2. [Optimal Sequential Diagnostic Strategy Generation Considering Test Placement Cost for Multimode Systems](https://pmc.ncbi.nlm.nih.gov/articles/PMC4634445/)：已用 test×fault D-matrix、候选故障和测试成本生成顺序诊断策略；差别是对象为工程系统，不使用 API metamorphic relation 或 LLM agent。
3. [Multi-Agent LLM-based Metamorphic Testing for REST APIs](https://arxiv.org/abs/2605.28321)：已从 OpenAPI 文档生成并执行 seed/follow-up MR，包括集合包含和差异关系；差别是离线 API 测试、多 agent 生成流程，不做运行时故障解释消元。
4. [Loud Failures, Quiet Failures](https://arxiv.org/abs/2610.10062)（[代码](https://github.com/obadaKraishan/brittle-agents)）：与 BFCL executable multi-turn、quiet corruption、check-results prompt 和公开复现入口完全同任务；差别是故障只触发一次，没有持续参数响应 fault 或 MR controller。
5. [Tools Fail: Detecting Silent Errors in Faulty Tools](https://aclanthology.org/2024.emnlp-main.790/)（[代码](https://github.com/jiminsun/tools-fail)）：已提出 silent-tool-error 的检测、归因、恢复框架并测试 disclaimer/confidence/checklist；差别是没有基于故障可辨别性的在线 MR 选择，也不研究 probe-pass false confidence。

```json
{"score":7.1,"verdict":"promising_needs_revision","fatal_blockers":["核心算法新颖性：MR×fault可辨别矩阵及按剩余故障覆盖贪心选MR已被fault-based MR prioritization直接覆盖","Claim新颖性：probe pass仅消去不相容解释并保留unknown属于经典顺序故障诊断的候选集更新语义"],"novelty_conclusion":"持续参数响应型silent fault下的BFCL在线保守诊断与false-confidence评测具有组合新意，但当前核心选择算法和pass语义均已有直接方法学先例，尚不足以experiment_ready。","closest_neighbors":["Metamorphic Relation Prioritization for Effective Regression Testing","Optimal Sequential Diagnostic Strategy Generation Considering Test Placement Cost for Multimode Systems","Multi-Agent LLM-based Metamorphic Testing for REST APIs","Loud Failures, Quiet Failures","Tools Fail: Detecting Silent Errors in Faulty Tools"]}
```
