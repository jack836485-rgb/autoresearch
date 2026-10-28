## 结论

截至 2026-10-09，**score：5.2/10；verdict：needs_rethink**。当前 Claim 的核心新意不足以进入实验规划：`Memory Is a Derivation` 已明确报告压缩会把 plan 变成 accomplished fact；MemIR 已把来源、证据角色和 truth-bearing claim 分型并限制事实授权；MemTxn 已给出 answer-model 外、无需 verifier call 的确定性来源支持准入门。AppWorld 内、同预算地测量“错误升格率→TGC”的任务化验证尚未见直接覆盖，但这更像已知机制在新 benchmark 上的诊断，而不是独立方法 Claim。**当前形态不值得继续进入实验规划。** Fatal blockers 为：核心失效与机制已被近邻覆盖；列出的公开 baseline 仅证明 AppWorld agent 可运行，未提供普通摘要/同长结构摘要的已打开同任务实现与具体复现路线，且 full-code repair 不是该压缩失败的匹配 baseline。

## Claim 判断

| Claim | 判断 | 关键依据 |
|---|---|---|
| 压缩会把“计划/尝试/推测”升格成“已成功/已知” | 已被覆盖 | [`Memory Is a Derivation`](https://arxiv.org/abs/2609.36130) 在方法部分直接以 “turning a plan into an accomplished fact” 作为压缩写入不受历史支持的例子，并评估 provenance、compositional validity 与 admission。候选正确将 AppWorld 中是否发生该失效标为待诊断假设，而非已报告事实。 |
| 断言应携带来源与证据角色，只有受支持断言可作为事实 | 已被覆盖 | [MemIR](https://arxiv.org/abs/2605.25869) 将 raw evidence、retrieval cues、truth-bearing claims 分成 typed atoms，要求显式来源，并把 factual authorization 限于 supported claim atoms；与“三状态+来源”的核心机制实质重合。 |
| 用 CPU/确定性规则阻止不受支持的状态升级，不增加 LLM judge | 部分重合，接近覆盖 | [MemTxn](https://arxiv.org/abs/2607.27834) 已在 answer model 外用无 verifier call 的 Ordered PatchTest 做来源支持准入，并显式维护 Proposed/Rejected/Active 等状态。候选的三类执行状态更窄，但不足以形成新的机制主张。 |
| 在 AppWorld 压缩点进行同预算因果验证，以错误升格率和 TGC 衡量 | 部分新颖，但实验基线 fatal | [AppWorld ReAct 公开实现](https://github.com/StonyBrookNLP/appworld/blob/main/experiments/code/simplified/react_code_agent.py) 的确会先遮蔽旧 observation，再移除完整历史块；官方仓库也给出 dev/test 运行入口。但当前 baseline 表只有 ReAct 与 full-code 两种 agent harness，未给普通摘要、同长结构摘要的公开实现和可复现入口；full-code repair 也不隔离压缩机制。 |
| “ACE 全量重写丢知识、AppWorld 截断历史”作为问题依据 | 事实有依据，不构成新颖 Claim | [ACE](https://arxiv.org/abs/2510.04618) 报告 brevity bias/context collapse；AppWorld 代码可核验裁剪逻辑。二者只支持问题存在，不能支持 AppWorld 中证据状态升格已经发生。 |

## 最高近邻

1. [`Memory Is a Derivation: The Distributed-Evidence Paradox in Long-Term Agents`](https://arxiv.org/abs/2609.36130)：重叠最直接，明确覆盖“计划被写成已完成”、来源不足、组合语义失真与写入准入；差别是其对象为跨会话持久记忆并使用模型验证器，而非 AppWorld 单次长程代码轨迹中的确定性状态门。
2. [`Mitigating Provenance-Role Collapse in Long-Term Agents via Typed Memory Representation`](https://arxiv.org/abs/2605.25869)：重叠在 typed provenance、证据/推断角色分离以及只有受支持 claim 才有事实权限；差别是其完整方法包含长期记忆检索与 claim-centered bundles，并在 LoCoMo/BEAM-100K 上验证，不是 AppWorld 压缩点实验。
3. [`MemTxn: A Transaction Boundary for Source-Supported Updates and Complete-State Recovery in Agent Memory`](https://arxiv.org/abs/2607.27834)：重叠在模型外、确定性、来源约束的状态准入且不调用 LLM judge；差别是其合同针对持久更新、冲突版本与恢复，不专门建模计划/尝试/工具回执三类执行状态。

```json
{"score":5.2,"verdict":"needs_rethink","fatal_blockers":["novelty: 压缩把计划升格为已完成这一核心失效已被 Memory Is a Derivation 明确报告，来源/证据角色分型与事实授权机制又被 MemIR 覆盖，确定性来源准入被 MemTxn 覆盖","feasibility: 当前 baseline 表未提供普通摘要与同长结构摘要的已打开同任务实现及具体复现路线；full-code repair 不是隔离历史压缩失败的匹配 baseline"],"novelty_conclusion":"AppWorld 内同预算测量错误升格率与 TGC 的任务化实验尚有局部新意，但核心诊断和机制均已有直接先例，现状不能作为独立新方法进入实验规划。","closest_neighbors":["Memory Is a Derivation: The Distributed-Evidence Paradox in Long-Term Agents (arXiv:2609.36130)","Mitigating Provenance-Role Collapse in Long-Term Agents via Typed Memory Representation (arXiv:2605.25869)","MemTxn: A Transaction Boundary for Source-Supported Updates and Complete-State Recovery in Agent Memory (arXiv:2607.27834)"]}
```
