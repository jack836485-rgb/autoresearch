## 结论

实际检索日期：**2026-10-10**。**score：7.3；verdict：promising_needs_revision**。未发现足以直接否定整个方向的 fatal blocker，但尚未达到 experiment_ready。

研究价值成立：完整集合任务能够揭示“返回内容正确”与“取得全部目标”之间的恢复差距。不过，静默遗漏、局部正确却错误宣称完整，以及完整性与答案质量分开评测，均已有原作覆盖。可能独立的部分是**语义收缩与返回 cap 的交互，以及同公共历史下的预算内恢复证据协议**；目前尚不能确认它超出了已有问题的重新组合。

当前目标演化成立。它仍属于 Q001 的静默异常与 Q005 的可执行恢复边界；REST API 缺漏实证、GetNext 和 SilentProbe 均提供聚焦依据。first-touch 问题未覆盖可以接受。冻结模型、CPU 环境、隐藏真值仅供离线评估、完整成本和参数待确认等安排符合硬约束。

## Claim 判断

| 当前 Claim | 判断 | 关键依据及可验证性 |
|---|---|---|
| 见证全部通过、返回行均正确，完整任务仍失败 | **部分重合** | GetNext 已说明 top-k 返回不足以覆盖目标；ToolUniverse 审计明确讨论截断结果被当作完整证据。当前弱见证反例可构造，但存在性本身不足以建立独立任务贡献。[GetNext §I–III](https://arxiv.org/html/1208.3876v1)、[ToolUniverse §1、§4–5](https://arxiv.org/html/2609.26836v1) |
| 区分缺少区分记录、记录不可取得、取得后未修复 | **部分重合，有协议增量空间** | GetNext 已研究受限接口下的可识别性；Outcome Monitors 已分离检测与恢复。未找到完全相同的公共历史策略树协议，但“存在同一公共策略”还取决于明确的候选世界与动作集合。[GetNext §II、VI](https://arxiv.org/html/1208.3876v1)、[Outcome Monitors §3](https://arxiv.org/html/2608.19303v1) |
| 分开统计返回 soundness、集合 recall 和错误完整性声明 | **已覆盖基本原则** | 局部答案正确性与完整性意识分离，已是 Partial Evidence Bench 的核心评测设计；ToolUniverse 也单列完整性维度。精确 id 集合提供更清晰的计分方式，但这些指标本身不是新机制。[Partial Evidence Bench §3、§5](https://arxiv.org/html/2605.05379v1) |
| 语义收缩与覆盖限制形成独立恢复问题 | **新颖候选，尚未证实** | REST 变形测试已经发现过滤导致缺漏；SilentProbe 已报告差分探测看不见的语义降级。当前交互 Claim 可证伪，但给出的 40/10/25 例子尚未充分区分语义效应与普通 top-k 遗漏。[REST 原作 §5](https://javiertroyauma.github.io/publications/TSE2017_REST_prePrint.pdf)、[SilentProbe §4.5](https://arxiv.org/html/2609.00035v1) |
| 三种 get 条件形成不同可恢复性 | **部分重合，当前设定存在退化** | 按 Brief 的准确 id/数值行、静态表和仅过滤偏移设定，已见 id 的 get 只重复已有记录，不能揭示未返回 id。因此“无补读”与“已见 id 补读”对遗漏恢复的信息能力相同。这是从当前接口定义得到的判断。 |
| 最小实验可以实现并对齐核心预算 | **基本成立，关键区分仍不足** | 已在线读取 ToolMaze 的 Function Calling 循环及普通/failure-aware 提示，提供可复现入口。Outcome Monitors §3 的检测、建库和 receipt 机制可作为移植依据；作者 artifact 本轮未核实。完整成本安排合理，但公开编码穷举不能代替已经定义覆盖条件的 GetNext 或完整分区关系。[ToolMaze 源码](https://raw.githubusercontent.com/Zhudongsheng75/ToolMaze/main/evaluation/agents/openai_agent.py) |

当前不足主要影响**任务独立性和实验解释力**，尚不是不可修复的方向性否定。也没有依据声称已经解决静默遗漏或取得恢复增益。

## 最高近邻

1. **Digging Deeper into Deep Web Databases by Breaking Through the Top-k Barrier（2012）**
   [原文](https://arxiv.org/html/1208.3876v1)。已核验 §I–III、VI 及算法伪代码。重合在受限接口、查询重写、覆盖候选和查询成本；当前差别是工具语义可能收缩，以及冻结 agent 的恢复与完整性声明。原作假设查询语义正确，并有 overflow 标志，不能直接把其保证搬到当前故障条件。

2. **Metamorphic Testing of RESTful Web APIs（2018；2017 在线发表）**
   [作者预印本](https://javiertroyauma.github.io/publications/TSE2017_REST_prePrint.pdf)。已核验 Complete 分区关系及 §5 的 AND/NOT 缺漏实例。重合在通过多次公开查询发现遗漏；当前差别是 cap、隐藏语义偏移和预算内 agent 恢复。原作还主动限制结果规模以减轻近似检索干扰，说明 cap 交互确有研究边界。

3. **SilentProbe: Measuring Silent Failure in Production APIs Used as Agent Tools（2026）**
   [原文](https://arxiv.org/html/2609.00035v1)。已核验 §3–4.5。重合在语义参数错误、机械 probe 的盲区和失败恢复；当前差别是只遗漏目标记录而保持返回 soundness 的完整集合协议。其语义降级实例主要涉及用户请求被弱化，不能作为阈值向内 coercion 的直接实证。

4. **Silent Failures in Agent–Tool Interaction: An Audit of ToolUniverse（2026）**
   [原文](https://arxiv.org/html/2609.26836v1)。已核验方法、完整性维度及截断与过滤案例。重合在工具成功但记录不全、遗漏传播及错误完整性声明；当前差别是确定性的恢复干预、同公共前缀和预算可达性。该审计不要求 agent 主动诊断目标失败，也未给出当前协议。

5. **Partial Evidence Bench: Benchmarking Authorization-Limited Evidence in Agentic Systems（2026）**
   [原文](https://arxiv.org/html/2605.05379v1)。已核验 §3–6。重合在局部正确、完整性意识、缺口报告和 false-complete 计分。差别是其缺口来自授权边界，并提供可见边界信号；当前研究来自工具语义与 cap。它是概念和指标近邻，不能直接充当当前恢复任务的同任务 baseline；其代码仓库本轮未核实。

```json
{
  "score": 7.3,
  "verdict": "promising_needs_revision",
  "fatal_blockers": [],
  "novelty_conclusion": "静默遗漏、局部正确与错误完整性声明、完整性和答案质量分离均已有覆盖。可能独立的贡献是语义收缩与返回cap的交互及同公共历史下预算内恢复证据协议，但当前最小实验尚不足以确认独立任务边界；已见id补读在现有准确行和静态表设定下不增加遗漏恢复信息。",
  "search_performed": true,
  "closest_neighbors": [
    {
      "title": "Digging Deeper into Deep Web Databases by Breaking Through the Top-k Barrier",
      "url": "https://arxiv.org/html/1208.3876v1",
      "overlap": "受限top-k接口、查询重写、候选覆盖、可识别性及查询成本",
      "difference": "原作假设查询语义正确并提供overflow标志；当前关注隐藏语义收缩与冻结agent的恢复及完整性声明",
      "verified": true
    },
    {
      "title": "Metamorphic Testing of RESTful Web APIs",
      "url": "https://javiertroyauma.github.io/publications/TSE2017_REST_prePrint.pdf",
      "overlap": "使用公开查询之间的完整分区关系发现过滤导致的遗漏",
      "difference": "当前加入返回cap、隐藏语义偏移与预算内agent恢复；原作限制结果规模以减轻近似检索干扰",
      "verified": true
    },
    {
      "title": "SilentProbe: Measuring Silent Failure in Production APIs Used as Agent Tools",
      "url": "https://arxiv.org/html/2609.00035v1",
      "overlap": "语义参数错误、差分probe盲区、静默失败检测与恢复",
      "difference": "当前目标是返回soundness保持正确而完整集合缺漏；原作语义降级不直接实证阈值向内coercion",
      "verified": true
    },
    {
      "title": "Silent Failures in Agent–Tool Interaction: An Audit of ToolUniverse",
      "url": "https://arxiv.org/html/2609.26836v1",
      "overlap": "工具成功但记录不全、cap与过滤缺漏、部分结果被当作完整证据",
      "difference": "当前提出确定性恢复干预、同公共前缀及预算可达性；原作是文档驱动审计而非当前恢复协议",
      "verified": true
    },
    {
      "title": "Partial Evidence Bench: Benchmarking Authorization-Limited Evidence in Agentic Systems",
      "url": "https://arxiv.org/html/2605.05379v1",
      "overlap": "局部答案正确性与完整性意识分离、缺口报告及错误完整性声明计分",
      "difference": "原作缺口来自授权边界且具有可见边界信号；当前缺口来自工具语义与cap，不能直接使用其方法作为同任务恢复baseline",
      "verified": true
    }
  ],
  "goal_assessment": {
    "within_initial_scope": true,
    "hard_constraints_satisfied": true,
    "evolution_supported": true,
    "reason": "完整查询恢复仍关联Q001的静默语义异常和Q005的可执行恢复边界；REST缺漏实证、GetNext和SilentProbe支持聚焦。first-touch不足未覆盖已明确说明，不构成偏题。当前仅进行文献与方案审查，冻结模型、CPU环境、隐藏真值仅离线评估、完整成本及核心参数待确认符合约束；没有实测解决声明。"
  }
}
```