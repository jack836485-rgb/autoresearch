## 结论

实际检索日期：**2026-10-10**。**score：6.6／10；verdict：needs_rethink。**

问题具有实际价值，当前方案也能形成低成本、可证伪的工程实验。但独立机制贡献尚未成立：公开谓词检查属于已有的结果契约监控；远端不能准确执行某个条件时，在本地执行残余谓词，是成熟查询处理机制。当前新增部分是以观测到的违约触发该机制，尚未展示超出两者顺序组合的独立作用。[Outcome Monitors §3](https://arxiv.org/html/2608.19303v1#S3)、[Garlic §4.3.1](https://www.vldb.org/conf/1997/P266.PDF)

一个具体阻断是：在当前“忽略一个过滤条件”的定义下，完整返回集合已经包含正确答案。设用户条件为 \(p\land q\)，忽略 \(p\) 后返回 \(R=\{x:q(x)\}\)，直接对完整 \(R\) 本地执行 \(p\) 即得到正确集合。删除远端 \(p\) 后重新请求，再本地过滤，也得到同一集合。当前实验没有区分这两者，因此即使优于警告或重试，也不能据此支持“谓词决定实施位置”的独立贡献。这是从当前任务定义得出的机制判断，未执行实验。

目标演化成立：SilentProbe 确实记录了非空结果违反用户条件，以及语义降级不能被其移除差分检测发现的边界。聚焦有限、字段完整的只读查询仍关联 Q001／Q005；不处理写操作和 first-touch 混杂不构成偏题。当前 Brief 符合硬约束，并正确把收益写为待验证假设。[SilentProbe §1.1、§4.5](https://arxiv.org/html/2609.00035v1)

## Claim 判断

| 当前 Claim | 判断 | 原文依据与可验证性 |
|---|---|---|
| 从公开用户条件／schema 建立谓词，识别格式正常但违反条件的结果 | 部分重合 | Outcome Monitors 已按公开或学习得到的结果契约检测违约；SilentProbe 已指出结果与调用者意图比较的重要性。当前具体用户谓词可以验证，但检查机制本身不新。[Outcome Monitors §3](https://arxiv.org/html/2608.19303v1#S3)、[SilentProbe §4.5](https://arxiv.org/html/2609.00035v1#S4.SS5) |
| 删除不能正确实施的远端条件，取完整候选集后执行本地精确过滤 | 已覆盖其执行原理；触发方式部分不同 | Garlic 已处理 Web 源返回宽松匹配超集、由本地补做精确谓词；Trino 明确保留不能正确下推的约束并在本地执行。当前差别是运行时违约触发，而非事先获知能力。[Garlic §4.3.1](https://www.vldb.org/conf/1997/P266.PDF)、[Trino predicate pushdown](https://trino.io/docs/current/develop/connectors.html#predicate-pushdown) |
| 同一谓词同时作为异常见证并决定恢复算子位置，形成独立机制贡献 | 部分重合，独立性未成立 | 当前唯一新增关系是“发现违反 \(p\)，随后本地执行 \(p\)”。在规定的忽略过滤模式中，重新请求并未增加逻辑上的修复能力；现有对照不能识别该关系的额外贡献。没有检索到完整同构的 agent 论文，但这不足以将常规监控与残余过滤的组合判为独立创新。 |
| 比警告、原请求重试减少错答案与诊断后无效重试 | 尚未覆盖的具体实证假设 | 精确集合成功率、假完成和完整成本能够证伪它；当前实验可支持窄范围工程收益，不能单独支持执行位置绑定的机制 Claim。Outcome Monitors 已显示恢复工具内容可以驱动收益，需避免把确定性执行替代模型选择的效果解释为新绑定机制。[Outcome Monitors §5.3](https://arxiv.org/html/2608.19303v1) |

最小实验无需本地大模型，固定 actor、解码与总预算的安排合理。已核实 [ToolMaze Function Calling agent](https://raw.githubusercontent.com/Zhudongsheng75/ToolMaze/main/evaluation/agents/openai_agent.py) 的调用、反馈和 token 统计入口，普通／failure-aware agent 可以明确移植到拟定环境。Outcome Monitors 的公开可运行 artifact 本次未核实；警告 arm 应按机制移植理解。Garlic／Trino 是机制近邻，不能作为已经可运行的同任务 agent baseline。

## 最高近邻

1. **Don’t Scrap It, Wrap It! A Wrapper Architecture for Legacy Data Sources — Roth、Schwarz，VLDB 1997。**
   [原论文](https://www.vldb.org/conf/1997/P266.PDF)。已核验 §4.3.1：Web 源把精确字符串条件解释成宽松匹配，返回超集；优化器补加本地精确谓词。与当前恢复执行原理高度重合。差别是 Garlic 通过 wrapper 声明语义能力，当前通过结果违约发现问题。

2. **Outcome Monitors: Recovery Affordances for Silent Tool Failures — Panthi、Abdelfattah，2026。**
   [原论文](https://arxiv.org/html/2608.19303v1)。已核验契约违约检测、公开恢复工具映射，以及恢复工具内容的消融。其 monitor 不执行修复；当前直接实施特定查询恢复算子。公共可运行 artifact 未核实，不能因这一限制忽略其机制重合。

3. **SilentProbe: Measuring Silent Failure in Production APIs Used as Agent Tools — Li 等，2026。**
   [原论文](https://arxiv.org/html/2609.00035v1)、[公开 agent-loop 入口](https://raw.githubusercontent.com/Jasper0122/silentprobe/master/probe/rq6_downstream.py)。已核验忽略过滤返回超集、非法词返回空集、语义降级及差分检测边界。当前差别是有完整记录字段时进行确定性本地恢复；该入口调用真实商业 API，并非拟定 CPU 环境的现成 baseline。

4. **Trino：Predicate Pushdown／Residual Filters。**
   [官方说明](https://trino.io/docs/current/develop/connectors.html#predicate-pushdown)、[原始实现](https://raw.githubusercontent.com/trinodb/trino/master/plugin/trino-base-jdbc/src/main/java/io/trino/plugin/jdbc/PredicatePushdownController.java)。已核验 `remainingFilter`、禁用下推，以及远端宽松下推后仍保留同一原始谓词本地复核。差别是能力／语义规则驱动的查询规划，没有当前的 agent 违约触发机制。

5. **Metamorphic Testing of RESTful Web APIs — Segura 等，TSE 2018，2017 在线发表。**
   [DOI](https://doi.org/10.1109/TSE.2017.2764464)、[作者上传的原稿](https://www.researchgate.net/publication/320512973_Metamorphic_Testing_of_RESTful_Web_APIs)。已核验 §3.3 的过滤收紧／结果子集关系及查询参数测试。它负责检测 API 缺陷，不为同一 agent 任务执行本地恢复；其检测贡献不能计入当前新颖性。

```json
{
  "score": 6.6,
  "verdict": "needs_rethink",
  "fatal_blockers": [
    "当前核心机制实质为结果契约监控与成熟残余谓词执行的顺序组合，尚未成立独立机制贡献。",
    "在当前忽略一个过滤条件的定义中，完整原返回集合已可通过本地残余过滤恢复；现有最小实验未区分该等价策略，无法识别删除远端条件并重新请求的独立收益。"
  ],
  "novelty_conclusion": "未找到完整同构的agent论文，但公开谓词监控、远端弱化或禁用条件、本地执行原始残余谓词均有明确原作覆盖。运行时违约触发具有工程价值，当前证据与实验尚不足以使这一组合成为独立研究机制。",
  "search_performed": true,
  "closest_neighbors": [
    {
      "title": "Don't Scrap It, Wrap It! A Wrapper Architecture for Legacy Data Sources",
      "url": "https://www.vldb.org/conf/1997/P266.PDF",
      "overlap": "Web源无法遵循精确谓词语义时返回超集，由本地执行精确残余谓词恢复用户查询语义。",
      "difference": "原作通过wrapper能力与语义声明规划，当前通过运行时结果违约触发。",
      "verified": true
    },
    {
      "title": "Outcome Monitors: Recovery Affordances for Silent Tool Failures",
      "url": "https://arxiv.org/html/2608.19303v1",
      "overlap": "确定性结果契约检测、违约见证和公开恢复工具映射。",
      "difference": "原作发出非强制警告并由actor选择恢复；当前执行特定查询恢复算子。公共可运行artifact未核实。",
      "verified": true
    },
    {
      "title": "SilentProbe: Measuring Silent Failure in Production APIs Used as Agent Tools",
      "url": "https://arxiv.org/html/2609.00035v1",
      "overlap": "静默忽略过滤返回超集、非法词返回空集、查询条件差分和语义降级。",
      "difference": "原作主要测量故障与schema干预；当前在可完整读取且字段齐全的条件下尝试本地恢复。",
      "verified": true
    },
    {
      "title": "Trino Predicate Pushdown and Residual Filters",
      "url": "https://trino.io/docs/current/develop/connectors.html#predicate-pushdown",
      "overlap": "按远端能力或语义决定约束执行位置，保留原始残余谓词在本地执行。",
      "difference": "原系统使用connector能力规则，没有agent结果违约触发机制。",
      "verified": true
    },
    {
      "title": "Metamorphic Testing of RESTful Web APIs",
      "url": "https://doi.org/10.1109/TSE.2017.2764464",
      "overlap": "通过查询过滤条件变化及结果集合关系检测REST API语义故障。",
      "difference": "原作报告API缺陷，不执行当前agent任务的本地恢复。",
      "verified": true
    }
  ],
  "goal_assessment": {
    "within_initial_scope": true,
    "hard_constraints_satisfied": true,
    "evolution_supported": true,
    "reason": "当前聚焦有确定性公开条件、完整分页和字段可达的只读agent查询，仍关联Q001异常识别与Q005可执行恢复。SilentProbe的忽略过滤及语义降级案例支持这一聚焦；不覆盖写操作和first-touch混杂不构成偏题。Brief未使用运行时oracle，未运行实验或调用付费推理API，冻结模型及完整预算比较符合约束，未把预期收益称为实测解决。"
  }
}
```