## 结论

- 日期：2026-10-09
- Score：4.2/10
- Verdict：`needs_rethink`
- 新意判断：核心问题真实，但当前核心机制没有形成可辨认的新颖边界。IDSS 已在同任务的 τ-bench Retail/Airline 上维护意图、变量、约束、执行状态和任务依赖，并通过约束传播更新动作可执行性；其案例还明确展示了在重规划时保留未受影响的原要求。当前方案的“局部约束编辑—传播至相依决定—保留无关要求”与之高度重合。Drift-Bench++ 又已在 τ² Retail/Airline 上把用户意图表示成 frame+conditions，以结构化 edit 和可执行 intent graph 实现需求替换、删除及后续 intent shift，进一步压缩了实验构造的新意空间。
- 是否值得继续：不值得以当前 Claim 进入实验规划。当前存在核心机制已覆盖、失败证据归因不成立、同任务关键近邻缺失及实验域不一致四项阻断。

## Claim 判断

| Claim | 判断 | 关键依据 |
|---|---|---|
| “AppWorld-UL 报告用户回复后遗忘旧要求” | 已被当前引文否定 | [AppWorld-UL](https://arxiv.org/html/2607.20536)证明交互任务困难，并讨论用户回复可改变任务，但其交互分析测量是否提出必要问题，未报告“新回复覆盖旧要求”这一错误；该具体失败归因没有论文证据。 |
| 最新用户回复造成目标变化，模型会丢失仍有效的旧约束 | 部分重合 | [LLMs Get Lost in Evolving User Intent](https://arxiv.org/html/2607.20734)直接构造 argument reveal/revision/function switch 并观察显著退化；[Intent-Eval](https://arxiv.org/html/2610.06496)进一步发现模型会把已拒绝或已被替代的内容当作仍生效要求。现象成立，但不是 AppWorld-UL 的已报告结论。 |
| 普通目标摘要容易把最新要求当作完整替换 | 部分重合且因果未证 | [U-Fold](https://arxiv.org/html/2601.18285)已报告静态摘要会丢失细粒度约束并滞后于演化意图；但“完整替换”仍只是本方案诊断假设，尚无当前 brief 所述任务上的观察证据。 |
| 将用户变化表示为增加/撤回/更改的局部约束编辑 | 高度重合 | [Drift-Bench++](https://arxiv.org/html/2609.38604)在 τ² Retail/Airline 中已将意图分解为 frame+condition set，并恢复、应用 removing/replacing 等结构化 edit，且用原生 oracle 验证变化效果。 |
| 只重查引用被改约束的决定，同时保留无关要求 | 核心已被覆盖，差异未建立 | [IDSS](https://arxiv.org/html/2608.15755)已显式跟踪 intents、variables、constraints、execution status 和 dependencies，并用 constraint propagation 更新动作可执行性；同一 τ-bench 上的案例还在阻断旧路径时保留原 baggage requirement。当前 brief 没有证明“用户编辑触发的反向依赖重开”相对 IDSS 是不同 Claim。 |
| 最小实验能在同预算下证伪依赖传播收益 | 设计方向可证伪，但当前不可进入规划 | “逐项保留无依赖”与“局部重开”可隔离传播收益；但 brief 开头指定 retail 扩展，官方 LLMAgent 复现行却指定 telecom，且没有纳入同任务、同机制的 IDSS/U-Fold。任务域和关键 baseline 均未闭合，属于 fatal feasibility blocker。 |

## 最高近邻

1. [Intent-Driven Situation Tracking for User-Centric Multi-Turn Agents (IDSS)](https://arxiv.org/html/2608.15755)：同为无训练、显式状态、意图/约束/依赖跟踪和约束传播，并已在 τ-bench Retail/Airline 验证；差别仅是候选强调用户编辑触发的决定重查，而 IDSS 更广泛地连接工具事实与任务约束，此差别尚不足以形成独立 Claim。
2. [Beyond Oracle Communication: Drift-Bench++](https://arxiv.org/html/2609.38604)：同在 τ² Retail/Airline 上构造可执行的 evolving-intent 任务，以 condition set、结构化 edit 和 intent graph 表示局部需求变化；差别是其贡献主要是 benchmark/protocol，而不是候选所述的局部重规划 agent。
3. [U-Fold: Dynamic Intent-Aware Context Folding for User-Centric Agents](https://arxiv.org/html/2601.18285)：同在 τ-bench/τ²-bench 处理演化意图与旧约束遗漏，并以动态摘要和相关工具日志保留信息；差别是它每轮重建工作上下文，没有显式的约束到计划决定依赖图。
4. [LLMs Get Lost in Evolving User Intent](https://arxiv.org/html/2607.20734)：直接验证需求 reveal/revision/switch 导致模型退化，且公开了构造与评测代码；差别是其 GSM8K、BIRD-SQL、BrowseComp+、SWE-bench 不是当前客服工具任务，只能支撑现象而不能充当同任务 baseline。
5. [AppWorld-UL](https://arxiv.org/html/2607.20536)：支持用户回复可补充或改变长程工具任务以及交互带来明显困难；差别是它关注 clarification、infeasibility、approval，未建立“新回复导致旧要求遗忘”或局部依赖传播机制。

```json
{"score":4.2,"verdict":"needs_rethink","fatal_blockers":["核心机制与IDSS在同任务上的显式意图/约束/依赖跟踪及约束传播高度重合，当前brief未建立独立Claim边界","AppWorld-UL未报告所声称的‘用户回复后遗忘旧要求’，因果故事的关键证据归因不成立","最小实验在retail扩展与telecom复现命令之间不一致，且未纳入IDSS/U-Fold等最接近同任务方法，baseline证据不闭合"],"novelty_conclusion":"演化意图与旧约束遗忘是成立的问题，但局部约束编辑、依赖传播和保留无关要求的核心已被同任务近邻实质覆盖；当前方案不具备进入实验规划所需的新颖边界。","closest_neighbors":["Intent-Driven Situation Tracking for User-Centric Multi-Turn Agents (IDSS)","Beyond Oracle Communication: Drift-Bench++","U-Fold: Dynamic Intent-Aware Context Folding for User-Centric Agents","LLMs Get Lost in Evolving User Intent","AppWorld-UL"]}
```
