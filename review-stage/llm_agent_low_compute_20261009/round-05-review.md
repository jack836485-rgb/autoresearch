## 结论

日期：2026-10-09。**score：7.2/10；verdict：`promising_needs_revision`。** 新意主要成立在组合层：把文档支持的 metamorphic relation 作为工具 agent 的在线双调用检测器，并在 ToolMaze 隐式故障下同时测召回、误报与恢复；现有近邻分别覆盖隐式故障、契约式结果校验或离线 API 蜕变测试，但未发现直接覆盖这一完整组合的工作。值得继续，但当前不能判为 `experiment_ready`。致命阻塞有三项：其一，ToolMaze 的 P2/P4 实现对后续调用直接回放同一缓存扰动输出、忽略新参数（[`sandbox.py` L513–580](https://github.com/Zhudongsheng75/ToolMaze/blob/main/evaluation/core/sandbox.py#L513-L580)），故关系探测可能只识别注入器的“固定回放”伪影，现有设计不能把收益归因于一般语义故障检测；其二，最小实验点名固定重试和范围检查，但只为 native FC 与 failure-aware prompt 给出了开放实现和复现入口，baseline 证据不完整；其三，“常识范围检查会误伤真实异常”目前是待检验假设而非已有观察，brief 未给出支持该既定表述的一级证据。

## Claim 判断

| Claim | 判断 | 关键依据 |
|---|---|---|
| ToolMaze 中隐式失败难于显式失败 | 已被覆盖 | [ToolMaze](https://arxiv.org/abs/2606.05806) 已报告隐式语义失败下恢复最差；[Loud Failures, Quiet Failures](https://arxiv.org/abs/2610.10062) 又在 BFCL 多轮任务中给出 quiet 58.8% 对 loud 91.3% 的检测差距。 |
| 常识范围检查会把真实罕见值当成故障 | 新颖（尚未支持） | 当前 brief 没有论文证据或已运行结果；“干净极端值”只是计划中的可证伪条件，不能当成已观察失败。 |
| 文档保证的等价输入变换与输出关系可在线检测坏返回，并优于同预算固定重试 | 部分重合 | [ARMeta](https://arxiv.org/abs/2605.28321) 已由 OpenAPI 生成并执行 metamorphic tests；[ToolGate](https://arxiv.org/abs/2601.04688) 已用运行时 postcondition 拒绝逻辑错误返回。在线用于单 agent 恢复及与固定重试同预算比较仍有区别，但 ToolMaze 固定回放机制使该因果比较目前不可辨识。 |
| 关系探测能减少过度重试并提高 ToolMaze TSR/恢复 | 新颖（未验证） | 指标和否证条件明确，但无实验；固定重试、范围检查没有与公开 runner 对应的实现/入口，且 P3 的第二次调用天然恢复、P4 的第二次调用固定回放，机制效应与 benchmark 实现耦合。 |

## 最高近邻

- [When Tools Fail: Benchmarking Dynamic Replanning and Anomaly Recovery in LLM Agents](https://arxiv.org/abs/2606.05806)：同一 benchmark、同一显式/隐式与暂时/永久故障轴，并已有 native 与 failure-aware prompt；差别是它评估恢复，不提出文档关系驱动的双调用检测器。
- [ToolGate: Contract-Grounded and Verified Tool Execution for LLMs](https://arxiv.org/abs/2601.04688)：同为运行时、无需改权重的工具结果验收，postcondition 已覆盖空结果和语义/状态不一致；差别是单次调用的 Hoare 契约，而非两次等价调用之间的 metamorphic relation，也非 ToolMaze 同任务实验。
- [Multi-Agent LLM-based Metamorphic Testing for REST APIs](https://arxiv.org/abs/2605.28321)：从 OpenAPI 识别 metamorphic scenarios 并生成可执行测试，和“模型从公开文档提出变换与关系”高度重合；差别是离线 API 软件测试、两套 web 应用与多 agent 工作流，不处理任务中 agent 的故障恢复。
- [Tools Fail: Detecting Silent Errors in Faulty Tools](https://aclanthology.org/2024.emnlp-main.790/)：直接研究结构正常但错误的工具输出及检测/恢复；差别是计算器与 embodied planning，并以提示/期望判断为主，没有文档保证的关系探针。
- [Loud Failures, Quiet Failures: Fault Detection and Recovery in Tool-Using Language Model Agents](https://arxiv.org/abs/2610.10062)：同样区分显式与静默错误，含无故障基线、误报语境和“要求检查结果”的 prompt 对照；差别是 BFCL 故障测量研究，没有提出确定性的关系检测机制。

```json
{"score":7.2,"verdict":"promising_needs_revision","fatal_blockers":["ToolMaze 的 P2/P4 对每次命中回放同一缓存扰动输出而不按变换后的参数重新产生故障返回，关系探测可能只识别 benchmark 注入伪影，当前实验不能支持一般语义故障检测的因果 Claim。","最小实验声明比较固定重试和范围检查，但未提供这两个同任务 baseline 的开放实现、核验结果与具体复现入口，baseline 证据不完整。","‘常识范围检查会误伤真实异常’被写成既定 Claim，但当前只有待运行的干净极端值实验，没有一级证据或观察结果支持。"],"novelty_conclusion":"文档约束的 metamorphic relation 用于 ToolMaze 在线隐式故障探测具有组合新意，但原理组件已有 ARMeta、ToolGate 与 silent-tool-failure 工作覆盖；benchmark 注入伪影、baseline 证据和未证实的范围检查失败使边界尚不能进入实验规划。","closest_neighbors":["When Tools Fail: Benchmarking Dynamic Replanning and Anomaly Recovery in LLM Agents","ToolGate: Contract-Grounded and Verified Tool Execution for LLMs","Multi-Agent LLM-based Metamorphic Testing for REST APIs","Tools Fail: Detecting Silent Errors in Faulty Tools","Loud Failures, Quiet Failures: Fault Detection and Recovery in Tool-Using Language Model Agents"]}
```
