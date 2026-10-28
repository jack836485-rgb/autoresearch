## 结论

实际检索日期：**2026-10-10**。**score：7.4；verdict：promising_needs_revision；无 fatal blocker，未达到通过阈值。**

当前目标演化成立，仍关联 Q001 的语义误读与 Q005 的无必要／无效修复。Elastic 的真实协议以及 ToolUniverse 对限定信息丢失、结论放大和用途适配的观察，支持这一聚焦；无需处理全部初始 drawbacks。冻结模型、CPU 模拟、公开信息限制、完整计费与本阶段不执行实验等硬约束均满足。

研究价值在于：通过相同工具观测下的成对用户需求，区分证据解释错误、恢复选择错误和恢复能力不足。**独立新意目前仅可能来自这套受控评测；区间判断、需求条件性停止以及证据充分性判断均已有原作覆盖。** 当前最小实验能识别具体 agent 错误，但“提供新的可区分失败结构”尚缺明确判据：已有近邻已经区分解释、用途适配、继续检索和证据支持。仅出现阈值任务与精确任务成功率不同，或 backend 恢复率与任务恢复率不同，不足以支持该贡献。

## Claim 判断

| Claim | 判断 | 最关键原文依据与可验证性 |
|---|---|---|
| 同一不完整计数可以支持阈值决定，却不能支持精确总数 | **已覆盖** | Elastic 的 Track total hits 明确说明下界适用于不需要阈值之后准确数量的需求；Quickly check for matching docs 直接提供存在性任务的提前终止入口。该性质成立，但属于已有协议语义。[官方原文](https://www.elastic.co/docs/solutions/search/the-search-api) |
| `eq` 不足以证明完整，单独升级 `track_total_hits` 可能仍无效 | **已覆盖** | Search timeout 原文给出 `timed_out=true`、`relation=eq` 的部分结果。可以在模拟任务中验证 agent 是否正确组合限定信息；该规则本身没有新颖性。[官方原文](https://www.elastic.co/docs/solutions/search/the-search-api) |
| 恢复应按当前结论所需证据定义，而非只看后台完整恢复 | **部分重合** | ToolUniverse 的核心问题已经按“支持预期结论所需的意义”定义可靠性，Appendix A 同时包含用途适配、限定保留和恢复。当前差别是成对需求、预算与能力控制。[原文 §1、§5、Appendix A](https://arxiv.org/html/2609.26836v1) |
| 成对任务可以揭示既有完整性任务之外的新失败结构 | **潜在新颖，尚未建立** | SearchDecision-Bench 已测证据充分性、下一动作与 Claim 支持，SearchJev 会据充分性强制回答或继续搜索。当前计数限定交互更可控，但现有 Brief 尚不能判定何种观察超出了已有失败类别。可证伪性弱于其余 Claim。[原文 §2、Appendix D](https://arxiv.org/html/2610.05107v1) |
| 区间标准策略与公开精化动作构成可复现能力参照 | **已覆盖机制，可实现** | ThalamusDB 已返回确定性聚合上下界并支持有预算的渐进处理。当前标准策略足够简单，可作为新任务上的参照。Demanded Abstract Interpretation 则主要处理增量、按需静态分析，并非计数恢复或阈值精化的同任务基线。[ThalamusDB §4.3](https://saehanjo.github.io/assets/files/thalamusdb.pdf)、[DAI §5–7](https://arxiv.org/html/2104.01270v1) |
| 同冻结 actor 的普通／failure-aware 等对照及核心预算可以对齐 | **可复现，无关键阻断** | 已读取 ToolMaze 的 `OpenAIAgent`：公开模型、temperature、max_tokens、Function Calling 循环及两种提示入口。迁移到新任务可行；这支持普通 actor 实现，并不等于复现整套近邻系统。完整成本与待确认参数已有边界，尚无实测收益。[源码](https://raw.githubusercontent.com/Zhudongsheng75/ToolMaze/main/evaluation/agents/openai_agent.py) |

## 最高近邻

1. **Elasticsearch Search API** — [官方原文](https://www.elastic.co/docs/solutions/search/the-search-api)。已核验 Track total hits、Search timeout、Quickly check for matching docs。覆盖下界／精确值、部分结果仍为 `eq`、需求决定是否需要完整计数。当前差别是对冻结 agent 的恢复行为进行成对评测。

2. **Silent Failures in Agent–Tool Interaction: An Audit of ToolUniverse** — [原文](https://arxiv.org/html/2609.26836v1)。已核验正文及评测 rubric。覆盖限定丢失、部分结果被加强为结论、预期用途与证据适配。当前差别是可穷举的计数环境和受控恢复动作；原作尚未给出这里的阈值／精确需求配对。

3. **SearchJev: A Fast and Calibrated System-1 Model for Search Agents** — [原文](https://arxiv.org/html/2610.05107v1)、[作者代码](https://github.com/EvoScientist/SearchJev)。已核验 SearchDecision-Bench 与充分性控制流程。覆盖“证据是否足够回答”和“继续搜索还是终止”。当前差别是公开计数限定与恢复权限；其训练后的搜索判断器不能直接当作本任务的同冻结模型 baseline。

4. **When Tools Fail: Benchmarking Dynamic Replanning and Anomaly Recovery in LLM Agents** — [原文](https://arxiv.org/html/2606.05806v1)、[actor 源码](https://raw.githubusercontent.com/Zhudongsheng75/ToolMaze/main/evaluation/agents/openai_agent.py)。已核验恢复定义和实现入口。覆盖隐式故障、有效恢复集合、重试／换路／正确终止及恢复成本。当前差别是合法的部分证据可能已经完成用户任务，而非必须消除工具扰动。

5. **ThalamusDB: Approximate Query Processing on Multi-Modal Data** — [原文](https://saehanjo.github.io/assets/files/thalamusdb.pdf)、[作者系统](https://github.com/itrummer/thalamusdb)。已核验聚合上下界、渐进处理及预算停止入口。覆盖主要区间机制；当前差别是 agent 对限定信息与用户需求的解释及修复选择。跨域系统提供机制参照，不是直接同任务对照。

```json
{
  "score": 7.4,
  "verdict": "promising_needs_revision",
  "fatal_blockers": [],
  "novelty_conclusion": "独立机制创新未成立且当前方案对此保持诚实；潜在贡献是计数限定语义与成对用户结论需求交叉的受控恢复评测。已有工作覆盖需求条件性停止、证据充分性和用途适配，当前新增失败结构的判据不足以排除仅替换答案类型或增加协议测试的解释，因此未达到通过阈值。",
  "search_performed": true,
  "closest_neighbors": [
    {
      "title": "Elasticsearch Search API",
      "url": "https://www.elastic.co/docs/solutions/search/the-search-api",
      "overlap": "下界与精确计数语义、超时仍返回eq的部分结果、存在性需求下提前终止",
      "difference": "当前提出冻结agent在成对用户需求下的恢复行为评测",
      "verified": true
    },
    {
      "title": "Silent Failures in Agent–Tool Interaction: An Audit of ToolUniverse",
      "url": "https://arxiv.org/html/2609.26836v1",
      "overlap": "限定信息丢失、部分结果结论放大、预期用途与证据适配、恢复及解释失败",
      "difference": "当前提供可穷举计数环境以及阈值与精确需求配对，原作未展示该具体受控交互",
      "verified": true
    },
    {
      "title": "SearchJev: A Fast and Calibrated System-1 Model for Search Agents",
      "url": "https://arxiv.org/html/2610.05107v1",
      "overlap": "用户问题条件下的证据充分性、下一动作选择、Claim支持及继续搜索或终止",
      "difference": "当前针对公开计数限定和恢复权限，避免训练模型；其搜索判断器不是直接同任务baseline",
      "verified": true
    },
    {
      "title": "When Tools Fail: Benchmarking Dynamic Replanning and Anomaly Recovery in LLM Agents",
      "url": "https://arxiv.org/html/2606.05806v1",
      "overlap": "隐式故障、有效恢复集合、重试换路与正确终止、恢复成本和公开Function Calling actor",
      "difference": "当前研究合法部分证据已经支持用户任务的情况，并配对结论需求",
      "verified": true
    },
    {
      "title": "ThalamusDB: Approximate Query Processing on Multi-Modal Data",
      "url": "https://saehanjo.github.io/assets/files/thalamusdb.pdf",
      "overlap": "确定性聚合上下界、渐进精化和预算停止",
      "difference": "当前研究agent对结果限定和结论需求的解释与恢复选择，未提出新区间算法",
      "verified": true
    }
  ],
  "goal_assessment": {
    "within_initial_scope": true,
    "hard_constraints_satisfied": true,
    "evolution_supported": true,
    "reason": "从一般隐式语义错误与诊断恢复聚焦到计数结果限定及用户结论需求，仍关联Q001的结论放大和Q005的无必要或无效修复。Elastic真实协议与ToolUniverse原文提供演化依据。未覆盖任意数字污染、first-touch和一般工作流回滚不构成偏题。运行时仅用公开信息，真值仅离线评估；模型冻结、CPU模拟、完整计费及本阶段不执行实验等约束得到遵守。当前仅提出待检验任务贡献，没有宣称实测解决。"
  }
}
```