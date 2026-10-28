## 结论

实际检索日期：**2026-10-10**。**score：6.2／10；verdict：needs_rethink**。存在独立新颖性阻断，未达到实验就绪标准。

**单故障纠错公式是对的。** 在整数精确运算、数据同批不变、全部 \(n+2\) 个观测至多一个错误的条件下，两残差能够唯一定位并纠正错误，包括聚合返回自身的错误。但“加权校验、线性 syndrome、校验位纳入解码”的机制已有明确原作依据；把坐标对应到业务分组和工具返回，当前仍属于经典编码机制的直接迁移。声明“不申报新编码理论”是准确的，却没有替代性地定义出独立的 agent 机制贡献。[加权校验原文 §2](https://maths-people.anu.edu.au/~brent/pd/rpb114i.pdf)

研究价值在于有条件地降低数值报告的复核成本，而非证明模型获得一般异常恢复能力。最小实验可以验证端到端报告表现、成本与误纠正边界；然而直接 ABFT 解码器已经执行相同纠错动作，战胜警告或随机重试不能区分新增机制贡献。

目标演化成立：从 Q001 的合法数值异常和 Q005 的可执行恢复，收窄到静态只读报告，仍有关联且有原文依据。它不回答工作流状态不可恢复或 first-touch 混杂，但这不是拒绝理由。当前阶段、非 oracle 运行时及待确认核心参数的安排符合硬约束。

## Claim 判断

| 当前 Claim | 判断 | 关键依据与可验证性 |
|---|---|---|
| 两个残差定位并纠正单项错误 | **已覆盖** | 既有加权校验的 \(H\) 矩阵和 syndrome 模型覆盖该结构；取两校验关系、任意两列不共线，可推得唯一单坐标解。数学成立，可验证实现，但不能作为独立创新。[原文 §2.2](https://maths-people.anu.edu.au/~brent/pd/rpb114i.pdf) |
| 聚合返回自身出错也能定位 | **已覆盖** | 既有 \(H\) 已包含对应校验坐标的单位矩阵；当前对 S、W 的分支是其二维特例，不是额外 agent 机制。[式 2.2.1](https://maths-people.anu.edu.au/~brent/pd/rpb114i.pdf) |
| 从非绑定警告推进到明确纠错动作 | **部分重合** | Outcome Monitors 保留原输出、提供违规关系及恢复工具、不执行修复；当前确实改变恢复接口，但修复内容来自既有解码器。报告任务上的行为差别可测，不能据此推断独立纠错机制新意。[§3](https://arxiv.org/html/2608.19303v1) |
| 合法错误数值通过额外聚合参照被发现 | **部分重合** | Real-Time Detection 明确指出 plausible-value corruption 需要外部参照；当前提供了一种代数参照，但没有改变其可检测性前提。[§9–11](https://arxiv.org/html/2608.02464v1) |
| 全成本计入后比逐项复核更便宜 | **未被证明的条件性迁移** | 无索引逐组调用模型中的 \(nN\) 对最多 \(3N\) 比较成立；但 Deephaven 同时支持批量按组 `sumBy`，文档不能支持“生产复核必须扫描 n 次”。`snapshot` 的静态副本入口也已核实，完整费用仍未知。可测特定接口成本，不能外推普遍优势。[sumBy](https://deephaven.io/core/groovy/41.10/docs/reference/table-operations/group-and-aggregate/sumBy/)、[snapshot](https://deephaven.io/core/groovy/41.10/docs/reference/table-operations/snapshot/snapshot/) |

实现入口基本可信：[AggWSum](https://deephaven.io/core/groovy/41.10/docs/reference/table-operations/group-and-aggregate/AggWSum/) 提供原生加权汇总；[ToolMaze actor 源码](https://raw.githubusercontent.com/Zhudongsheng75/ToolMaze/main/evaluation/agents/openai_agent.py) 提供工具调用、结果回送与 token 计数循环。自定义 ReAct、警告和重试对照有足够标准定义可实现，但它们是新任务上的移植对照。无 LLM 的 ABFT arm 可判断纠错机制是否必要，不能承担“核心 actor 一致”的模型效果比较。

## 最高近邻

1. **Brent、Luk、Anfinson：Choosing Small Weights for Multiple Error Detection（1989）**
   [作者原文](https://maths-people.anu.edu.au/~brent/pd/rpb114i.pdf)、[作者书目](https://maths-people.anu.edu.au/~brent/pub/pub114.html)。已核验原文可检索的 §2：权重向量、含校验坐标的 \(H\)、syndrome 及列独立条件，直接重合当前二维建模。差别是业务 API 调用和报告流程，未见新的解码机制。

2. **Anfinson、Brent、Luk：A Theoretical Foundation for the Weighted Checksum Scheme**
   [作者页及原文入口](https://maths-people.anu.edu.au/brent/pub/pub109.html)。**作者摘要已核验，PDF 正文未完成读取**；作者书目列为 1989，部分引用列为 1988。摘要明确给出距离 \(d+1\) 下至多 \(d/2\) 错误的计数与纠正程序。当前单错误、两校验属于该能力范围；此项不用于逐式覆盖判定。

3. **Huang、Abraham：Algorithm-Based Fault Tolerance for Matrix Operations（1984）**
   [已成功读取的原作 PDF](https://people.bordeaux.inria.fr/gaupy/ressources/teachings/2021/algo_hpc/articles-2021/abft.pdf)。以数值冗余关系检测、定位、纠正错误，并讨论永久和暂时故障。当前差别是工具返回层的静态向量报告；原作并未研究 LLM，但“永久错误不能靠原样重试恢复”不构成新的纠错原理。

4. **Outcome Monitors: Recovery Affordances for Silent Tool Failures（2026）**
   [原文](https://arxiv.org/html/2608.19303v1)。已核验契约、conservation 关系、非 oracle 边界和非绑定恢复工具列表。当前区别是增加冗余观测并给出数值纠正动作；新任务警告 arm 可复现该接口思想，不能冒称复现原任务结论。

5. **Real-Time Detection and Repair of LLM Agent Failures（2026）**
   [原文](https://arxiv.org/html/2608.02464v1)、[公开仓库入口](https://github.com/sunnydubey1111/agent-trajectory-sentinel)。已核验 total-consistency、numeric-grounding、定位反馈和重试对照；原文承认合法错误数值需要外部参照。当前额外处理“收到的数值本身错误”，区别明确，但实现它的核心仍是经典加权校验。

```json
{
  "score": 6.2,
  "verdict": "needs_rethink",
  "fatal_blockers": [
    "当前独立机制与经典加权校验的线性syndrome及单坐标纠错同构；业务分组和工具接口迁移尚未形成额外机制贡献。直接ABFT对照执行相同纠错动作，战胜警告或随机重试不足以建立独立方法新意。"
  ],
  "novelty_conclusion": "单故障、整数精确运算、同批不漂移条件下公式成立，包含聚合观测出错的处理也属于既有加权校验模型。潜在价值是特定报告接口的成本与端到端应用研究，但当前只定义了成熟编码机制的直接迁移，真实接口成本优势未证实。",
  "search_performed": true,
  "closest_neighbors": [
    {
      "title": "Choosing Small Weights for Multiple Error Detection",
      "url": "https://maths-people.anu.edu.au/~brent/pd/rpb114i.pdf",
      "overlap": "权重向量、包含校验坐标的H矩阵、syndrome及列独立条件直接覆盖当前二维建模。",
      "difference": "当前把数据坐标映射为业务分组和工具返回，并计入报告流程成本；未见新的解码机制。",
      "verified": true
    },
    {
      "title": "A Theoretical Foundation for the Weighted Checksum Scheme",
      "url": "https://maths-people.anu.edu.au/brent/pub/pub109.html",
      "overlap": "作者摘要明确覆盖距离d+1下至多d/2错误的计数与纠正。",
      "difference": "作者摘要和书目已核验，PDF正文未完成读取，不用于逐式判定；当前为单错误工具报告应用。",
      "verified": false
    },
    {
      "title": "Algorithm-Based Fault Tolerance for Matrix Operations",
      "url": "https://people.bordeaux.inria.fr/gaupy/ressources/teachings/2021/algo_hpc/articles-2021/abft.pdf",
      "overlap": "利用数值冗余关系检测、定位、纠正错误，处理永久与暂时故障。",
      "difference": "原作研究矩阵计算及处理器故障，当前研究静态数值工具观测和报告任务。",
      "verified": true
    },
    {
      "title": "Outcome Monitors: Recovery Affordances for Silent Tool Failures",
      "url": "https://arxiv.org/html/2608.19303v1",
      "overlap": "公开契约、conservation关系、非oracle检测和恢复工具提示。",
      "difference": "原作发非绑定提示并保留输出，当前取得额外聚合观测并提供经典解码纠正动作。",
      "verified": true
    },
    {
      "title": "Real-Time Detection and Repair of LLM Agent Failures",
      "url": "https://arxiv.org/html/2608.02464v1",
      "overlap": "确定性数值一致性、定位反馈、重试对照及合法错误数值需要外部参照的边界。",
      "difference": "当前通过原生聚合建立工具数值之间的外部代数参照，而非只检查报告是否忠实于收到的值。",
      "verified": true
    }
  ],
  "goal_assessment": {
    "within_initial_scope": true,
    "hard_constraints_satisfied": true,
    "evolution_supported": true,
    "reason": "当前仍处理Q001的合法数值异常与Q005的可执行恢复，收窄到同批静态只读报告有工具监测原文依据。未处理状态恢复、query遗漏及first-touch混杂，不因这些未覆盖内容拒绝。运行时无需隐藏标签或oracle，本轮仅检索审查；预算参数留待确认，校验仅在完整成本严格小于替代复核时启用，符合项目条件性例外。"
  }
}
```