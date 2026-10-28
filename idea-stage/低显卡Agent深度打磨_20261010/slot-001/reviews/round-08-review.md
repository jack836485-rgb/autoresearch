## 结论

实际检索日期：**2026-10-10**。**score：7.7；verdict：experiment_ready；无 fatal blocker。**

可支持的独立贡献是一个受控任务：固定正确的不足诊断、用户目标与当前证据，检验 agent 是否仍混淆工具作用、预算阻断和能力阻断。诊断到恢复的总体差距、公开恢复提示、工具语义建模和成本规划均已有覆盖；当前方案没有将这些重新申报为方法创新。能力配组、公开历史上的可达性标签及明确失败判据，使剩余任务贡献具备可证伪性，也不只是修补单篇论文。

目标演化成立：精确计数仍对应 Q001 的工具语义误读，正确诊断后的可执行性对应 Q005；Elastic 的计数与部分结果语义提供真实接口依据。未处理 first-touch 不构成偏题。注意，按最小实验的实际设计，**eq“无需修复”是干净对照；固定 gte／不足诊断的配组只包含后三类状态**，四类不能全部称为诊断等价。

已核验 [ToolMaze FunctionCalling actor 的实现](https://raw.githubusercontent.com/Zhudongsheng75/ToolMaze/main/evaluation/agents/openai_agent.py)，存在公开工具初始化、逐步调用及 token 记录入口。[SearchJev 的 `decide` 实现](https://raw.githubusercontent.com/EvoScientist/SearchJev/main/training/inference.py)接受任意 state、question 和选项；同 actor 的菜单对照可以验证接口因素，但不能作为训练版 SearchJev 的复现。当前阶段的预算对齐原则可成立，具体参数留待用户确认符合约束；尚无实测证据证明失败结构存在。

## Claim 判断

| Claim | 判断 | 最关键原文依据与可验证边界 |
|---|---|---|
| 下界不能加强为精确计数，精度与覆盖须分别判断 | 已覆盖 | [Elastic 官方文档](https://www.elastic.co/docs/solutions/search/the-search-api)明确解释 gte，并展示 timed_out=true、relation=eq 的可能不完整计数；[ToolUniverse 审计 §1、§5](https://arxiv.org/html/2609.26836v1)讨论限定、范围与用途条件性可靠性。可作任务依据，不能算创新。 |
| 正确诊断不保证可执行恢复 | 已覆盖 | [PROBE §4.3](https://arxiv.org/html/2605.08717v2)明确把恢复差距关联到执行路径与环境约束；[DARC §6.2](https://arxiv.org/html/2608.11772v1)已有相同公开信息下的 diagnosis-only 与 ranked recovery 对照。总体命题已成立，当前不能再次作为发现。 |
| 固定正确诊断与公共证据，改变公开能力及预算，识别有效首动作与两类阻断 | 部分重合，有剩余任务新意 | [ToolMaze §3.2–3.3](https://arxiv.org/html/2606.05806v1)已有替代路径、不可恢复终止和穷举参照；[CostBench §3、附录 B.2/B.5](https://arxiv.org/html/2511.02734v1)已有工具成本、禁用与最优路径。已读原作没有覆盖当前这种固定语义诊断的计数配组。可由配组错误及正确阻断判断检验。 |
| 诊断正确后，语义规划能消除提醒或文档重排不能消除的动作错误 | 部分重合，仍待检验 | [Outcome Monitors §5](https://arxiv.org/html/2608.19303v1)已经分离诊断细节和公开恢复工具列表；当前差别在完整作用语义、动作闭包与预算可达性。若提醒已足够，或差别仅来自成本不齐，此 Claim 按现有判据失败。 |
| 公共历史一致世界上的 AND/OR 支持性规划、typed decision 接口 | 已覆盖的标准机制 | [Bertoli 等，IJCAI 2001](https://www.ijcai.org/Proceedings/01/IJCAI-2001-e.pdf)已有部分可观测条件规划；[SearchJev Table 1、附录 D.3](https://arxiv.org/html/2610.05107v1)已有充分性、下一动作、支持性判断及 forced continue。作为参照合理，不构成算法创新。 |

## 最高近邻

1. **[Outcome Monitors: Recovery Affordances for Silent Tool Failures](https://arxiv.org/html/2608.19303v1)**  
   已核验 §3、§5。公开 invariant 诊断、冻结 actor、非强制提示及公开恢复工具列表高度重合，且已有拆除／恢复工具列表的控制实验。当前差别是固定正确诊断后研究能力闭包、预算可达性与支持性首动作，不是提示增加恢复工具。

2. **[Diagnosis Before Recovery: Turning Agent Failures into Selective Self-Correction](https://arxiv.org/html/2608.11772v1)**  
   已核验 §3–4、§6.2。已有诊断限定干预集合、成本感知恢复策略，以及信息和预算匹配的 diagnosis-only 对照。当前是 episode 级的计数语义配组；DARC 是任务族诊断与冻结恢复 harness。不能把其跨域排名器直接称为计数任务 baseline。

3. **[When Tools Fail: Benchmarking Dynamic Replanning and Anomaly Recovery in LLM Agents](https://arxiv.org/html/2606.05806v1)**  
   已核验 §3.2–3.5 及 actor 源码。已有正常格式的语义错误、重试／换路／终止、完整路径枚举和恢复成本。当前差别是合法限定输出、正确诊断固定，以及按公共证据是否支持精确结论来评分。

4. **[Debugging the Debuggers: Failure-Anchored Structured Recovery for Software Engineering Agents](https://arxiv.org/html/2605.08717v2)**  
   已核验 §4.3、Table 3。已有从诊断到有界可执行指导的差距，并明确环境可能不支持直接修复。当前通过能力／预算配组隔离原因；PROBE 的分类汇总没有完成这种配组，也不能直接推出正确诊断条件下的恢复率。

5. **[CostBench: Evaluating Multi-Turn Cost-Optimal Planning and Adaptation in Dynamic Environments for LLM Tool-Use Agents](https://arxiv.org/html/2511.02734v1)**  
   已核验正文及附录 B.2、B.5。已有不同工具作用、成本、禁用事件及最优规划参照。其目标是取得目标 datatype，且保留可解路径；当前目标是获得支持精确计数的证据，并区分暂时预算不足与公开动作闭包不可修复。

```json
{
  "score": 7.7,
  "verdict": "experiment_ready",
  "fatal_blockers": [],
  "novelty_conclusion": "诊断到恢复的总体差距、公开恢复提示、工具语义与成本规划已有覆盖。剩余独立贡献是固定正确诊断、目标及公共证据后，按公开能力和预算构建恢复不等价配组，并检验语义上有效的首动作及能力/预算阻断。该任务贡献可证伪，尚未实测成立；不支持算法创新或普遍恢复能力提升的主张。",
  "search_performed": true,
  "closest_neighbors": [
    {
      "title": "Outcome Monitors: Recovery Affordances for Silent Tool Failures",
      "url": "https://arxiv.org/html/2608.19303v1",
      "overlap": "公开 invariant 诊断、冻结 actor、非强制反馈、公开恢复工具列表，以及诊断细节和恢复列表的分解控制。",
      "difference": "当前研究固定正确诊断后，检验完整工具作用、能力闭包和预算可达性；不把公开恢复提示本身申报为创新。",
      "verified": true
    },
    {
      "title": "Diagnosis Before Recovery: Turning Agent Failures into Selective Self-Correction",
      "url": "https://arxiv.org/html/2608.11772v1",
      "overlap": "诊断限定恢复干预、成本感知策略，以及信息和预算匹配的 diagnosis-only 与 ranked recovery 比较。",
      "difference": "DARC 构建任务族恢复 harness；当前构建 episode 级的计数语义诊断等价配组和阻断标签。",
      "verified": true
    },
    {
      "title": "When Tools Fail: Benchmarking Dynamic Replanning and Anomaly Recovery in LLM Agents",
      "url": "https://arxiv.org/html/2606.05806v1",
      "overlap": "语义工具错误、重试/换路/终止、替代路径、穷举恢复参照和恢复成本。",
      "difference": "当前固定合法限定输出及正确诊断，以公共历史是否支持精确计数作为终点，不按金标准 DAG 路径定义正确性。",
      "verified": true
    },
    {
      "title": "Debugging the Debuggers: Failure-Anchored Structured Recovery for Software Engineering Agents",
      "url": "https://arxiv.org/html/2605.08717v2",
      "overlap": "正确诊断与可执行恢复之间的差距，以及环境或 agent 行为范围可能不支持直接修复。",
      "difference": "当前通过公开能力和预算配组隔离恢复阻断；PROBE 的分类汇总没有实现这种条件配组。",
      "verified": true
    },
    {
      "title": "CostBench: Evaluating Multi-Turn Cost-Optimal Planning and Adaptation in Dynamic Environments for LLM Tool-Use Agents",
      "url": "https://arxiv.org/html/2511.02734v1",
      "overlap": "工具作用和成本建模、工具禁用、动态可行路径与最优规划参照。",
      "difference": "CostBench 以取得目标 datatype 为终点并保留可解路径；当前要求证据支持精确计数，包含预算阻断和动作闭包不可修复。",
      "verified": true
    }
  ],
  "goal_assessment": {
    "within_initial_scope": true,
    "hard_constraints_satisfied": true,
    "evolution_supported": true,
    "reason": "精确计数限定误读仍对应 Q001，正确诊断后的可执行性和能力/预算阻断对应 Q005；Elastic 官方接口语义及 PROBE、ToolUniverse 原作支持该聚焦。当前不覆盖 first-touch 合理。在线诊断和行动依据公开信息，隐藏世界及可达性标签仅离线使用；冻结 API actor 和 CPU 有限环境符合资源偏好；没有执行实验、调用付费推理 API 或生成实验代码。eq 无需修复应按已写明的最小实验理解为独立干净对照，固定 gte 诊断配组实际比较后三类状态。具体模型及核心预算参数留待用户确认符合本阶段约束。"
  }
}
```