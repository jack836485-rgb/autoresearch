## 结论

日期：2026-10-09。**score：6.4/10；verdict：promising_needs_revision。** 当前宽泛新意判断为“核心部分已被覆盖，窄机制仅部分新颖”，不应按现有 Claim 直接进入实验。最关键的覆盖来自 ScrambleToolBench 原文自身：其 `+ Memory` 已明确“解耦长期抽象知识与瞬态执行状态”，以 Task Recipes 和 Tool Knowledge 跨 reset 保留可复用信息，并在 `+ Window` 报告完成率增益；原文还把窗口激活后停止诊断探索、reset 后重新取得会话值总结为成功策略。当前尚可区分的部分是 CPU 依赖标注、未知 schema 的触发前探测，以及 reset 后易失值作用域的显式调度，但本轮未找到它们作为一个整体在同一 benchmark 上被实现和验证。值得继续查清这一窄边界，但当前存在核心 Claim 覆盖和最强同任务 memory 基线不可直接复现两个 fatal blockers。

## Claim 判断

| Claim | 判断 | 关键依据 |
|---|---|---|
| Window 过期会 reset 并重新生成中间值；失败 agent 会复用失效 session 值 | 已被覆盖 | ScrambleToolBench §2.4、§4.4.3 已直接定义并展示该失败；这是可靠问题锚点，不是新 Claim。 |
| 稳定工具知识/recipe 应与瞬态执行值分离 | 已被覆盖 | 原文 §3.1 的 `+ Memory` 已逐字主张 decouple long-term abstract knowledge from transient execution states，并跨 task/reset 保存 Task Recipes 与 Tool Knowledge。 |
| 在 trigger 前探测未知接口，trigger 后只重新取得必要瞬态值，并由 CPU 依赖检查与 reset 作用域执行 | 部分重合 | 原文已报告窗口内停止诊断探索、聚焦已知步骤及 reset 后重取值；但未给出依赖标签、触发前迁移和易失作用域这一确定性调度器。Recuris、Concord、TRACE 又分别覆盖状态/技能分层、失效观察抑制、有效与陈旧记忆的选择性保留。 |
| “少探索”统一提示不足，显式两阶段调度在同总预算下提高完成率且总调用不增加 | 新颖但未证实 | 这是可证伪的比较性实验 Claim，当前没有结果；原文 `+ Memory` 已在 `+ Window` 提升完成率，因此增益必须相对该同任务近邻成立，不能只超过 default 或提示。 |
| 最小实验已有任务匹配、公开实现与具体复现路线 | 部分成立/可行性阻断 | 官方仓库公开了 `default`、`--window_size`、seed、任务与 action 预算；但 `get_agent_class` 仅接受 `default`，论文 `+ Memory` 未公开实现。候选的本地结构化知识表明确不是该基线复现，现有命令也未执行所声明的总 token 上限，因此最强同任务基线和完整预算匹配尚无可直接运行路线。 |

## 最高近邻

1. [ScrambleToolBench: Agents Search Exhaustively Even When Their Own Map Points to the Next Step](https://arxiv.org/abs/2608.02358)；[官方代码](https://github.com/declare-lab/ScrambleToolBench)。直接覆盖 temporal window、reset、失效值、窗口内停止探索，以及长期 recipe/tool knowledge 与瞬态执行状态解耦；差别只剩显式依赖标签、触发前探测迁移和易失值作用域调度，且官方代码未包含论文 `+ Memory`。
2. [When Agent Context Goes Stale: Incoherence in Volatile Agent Context](https://arxiv.org/abs/2610.05281)；[代码](https://github.com/FFFFFFFANG1/Concord)。把工具观察绑定到可变源，在源变化后更新、标注或抑制陈旧上下文；不处理 ScrambleToolBench 的短 action window，也不调度 trigger 前后的探索。
3. [Recursive Experiential-Working Memory Evolution for Long-Horizon Agent Harnesses](https://arxiv.org/abs/2608.24876)；[代码](https://github.com/Gen-Verse/Recuris)。用 Working Memory 维护已验证当前状态，并据此调用可复用 Experiential Memory，覆盖“当前状态/稳定经验分层”；不针对 reset 后值失效或窗口前 schema 探测。
4. [TRACE: Governing Memory Validity in Evolving Multi-Agent Systems](https://arxiv.org/abs/2609.33517)。明确比较 Restore 与 Reset，并在 re-entry 时保留有效项、拒绝陈旧项；场景是多 agent 离开/返回后的 memory admission，不是工具发现和窗口内调用预算。
5. [When Not to Imitate: Boundary-Aware Skill Memory for Reliable Tool-Use LLM Agents](https://arxiv.org/abs/2608.22339)。以 applicability/risk/recovery 边界让工具技能按当前状态生效或被抑制，覆盖“可复用流程不能无条件执行”；未覆盖临时值生命周期和 trigger 前后调度。

```json
{"score":6.4,"verdict":"promising_needs_revision","fatal_blockers":["核心Claim中的稳定工具知识/recipe与瞬态执行状态分离，已被ScrambleToolBench原文+Memory基线明确提出并在+Window条件报告增益","同任务最接近的论文+Memory基线未在官方仓库公开；当前本地结构化知识表明确不是其复现，因而缺少可直接运行且预算匹配的最强同任务基线"],"novelty_conclusion":"宽泛核心已被原基准论文覆盖；CPU依赖标注、触发前未知schema探测与reset易失值作用域组成的窄调度机制仅属部分新颖，当前边界不足以进入实验。","closest_neighbors":["ScrambleToolBench: Agents Search Exhaustively Even When Their Own Map Points to the Next Step","When Agent Context Goes Stale: Incoherence in Volatile Agent Context","Recursive Experiential-Working Memory Evolution for Long-Horizon Agent Harnesses","TRACE: Governing Memory Validity in Evolving Multi-Agent Systems","When Not to Imitate: Boundary-Aware Skill Memory for Reliable Tool-Use LLM Agents"]}
```
