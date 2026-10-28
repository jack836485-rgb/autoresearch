## 结论

**日期：** 2026-10-09  
**Score：** 6.6 / 10  
**Verdict：** `promising_needs_revision`

候选抓住了一个真实且可证伪的失败：DA-Code 的 `dm-csv-010` 明确要求“先求月总量、再对月总量取均值”，公开数据又包含 `orders` 到 `order_items` 的一对多关系；因此，“代码成功执行但统计单元被换权”不是臆造场景。DA-Code 论文也报告了任务语境误解与持续代码错误，但没有公开证明 `dm-csv-010` 的自然轨迹确实以该类权重错误为主，故这仍是合理的待诊断 Claim，而非已知事实。

新意边界未过关。RADAR 已在同一 DA-Code 上提出“类型化操作记录—运行时校验—携带支持观测的定向反馈—原 agent 修订”的完整范式，并明确针对成功执行但统计定义错误的静默失败；Simon 等已用 aggregable properties 传播规则判断 join、aggregate 等操作后 `average`/`count` 的语义正确性；Huang 等又直接用 join-key group weighting 处理 fanout 导致的重复计数。当前方案的“声明目标统计单元、追踪重复次数与归约层级、返回最小反例”是一个有用的窄化实现，但从现有文字看更像把上述聚合正确性机制接入 RADAR 式 agent 反馈，而不是已证明不可由两者直接组合得到的独立机制。

最小实验的 DA-Agent、pandas `validate+indicator` 和本地 profiling 对照均可复现；但实验没有纳入已有官方代码、且已在 DA-Code 上验证的 DS-STAR，也没有可执行地隔离候选相对 RADAR 的增量。因而即使结果优于 DA-Agent，也无法判断收益来自统计单元权重追踪，还是来自一般性的计划验证、额外反馈或运行时检查。这是当前的致命归因/可行性 blocker。该方向值得继续澄清边界，但当前不应进入实验规划或执行。

## Claim 判断

| Claim | 判断 | 最关键依据 |
|---|---|---|
| DA-Code 中存在“合法 join/groupby 但月均值被算成行均值”的自然失败入口 | 部分支持 | [`dm-csv-010`](https://github.com/yiyihum/da-code/blob/main/da_code/configs/task/dm.jsonl) 明确要求 mean of monthly totals，公开 `orders.csv`/`order_items.csv` 构成一对多；但 [DA-Code](https://arxiv.org/abs/2410.07331) 只报告一般性任务误解与持续代码错误，没有该任务的错误频率或轨迹证据。 |
| shape、dtype、是否执行成功不足以保证统计单元和聚合语义正确 | 已被覆盖 | [Simon et al.](https://arxiv.org/abs/2111.13927) 已形式化说明 common analytic operations 后的 aggregability/summarizability，并专门检测 `average`、`count` 等非分配聚合错误。 |
| 追踪单元重复次数与归约层级能识别 join fanout 和换权 | 大幅重合 | [Huang et al.](https://arxiv.org/abs/2307.00417) 已把 join-key group 而非 tuple 作为权重单位来处理 fanout 与 double counting；候选的重复次数/一单元一票与其核心语义高度一致。 |
| 把上述追踪结果作为最小可见反例反馈给原 actor 是独立机制 | 部分重合 | [RADAR](https://arxiv.org/abs/2609.32528) 已在 DA-Code 上记录类型化操作及观测，并在冲突时返回支持观测和定向诊断以驱动修订；候选更专注 pandas 聚合权重，但尚未证明这种专门化超出直接组合。 |
| 同预算下该反馈能提高自然权重错误恢复率与任务成功率 | 新颖但未被当前实验辨识 | 这是可证伪的经验 Claim；现有设计遗漏同任务、可复现的 [DS-STAR 官方代码](https://github.com/google-research/ds-star)，且未与 RADAR 式运行时验证作可归因区分。 |

## 最高近邻

1. **Fail Loudly: An Auditable Runtime for Agentic Data Analysis (RADAR, 2026)** — [论文](https://arxiv.org/abs/2609.32528)。同样针对数据分析 agent 中“成功执行但语义错误”的静默失败，在 DA-Code 上用类型化操作记录、运行时校验和定向诊断反馈促使修订；公开规则未见统计单元权重或聚合层级追踪，这是候选仍可能保留的窄差别。

2. **Controlling the Correctness of Aggregation Operations During Sessions of Interactive Analytic Queries (2021)** — [论文](https://arxiv.org/abs/2111.13927)。传播 aggregable properties，覆盖 filter、join、aggregate 等操作并判断 `average`/`count` 的语义正确性；没有 LLM actor、DA-Code 或最小反例式反馈。

3. **Aggregation Consistency Errors in Semantic Layers and How to Avoid Them (2023)** — [论文](https://arxiv.org/abs/2307.00417)。直接处理 join fanout、double counting，并让每个 join-key group 获得等权后再分配到 tuples；没有 agent 工具循环，也没有自然错误轨迹恢复实验。

4. **DS-STAR: Data Science Agent for Solving Diverse Tasks across Heterogeneous Formats and Open-Ended Queries (2026)** — [论文](https://arxiv.org/abs/2509.21825)，[官方代码](https://github.com/google-research/ds-star)。在 DA-Code 上以文件分析、逐步计划、代码执行和 sufficiency verification 迭代修订；它不显式维护统计单元权重，但构成同任务、可复现的强验证基线。

5. **DA-Code: Agent Data Science Code Generation Benchmark for Large Language Models (2024)** — [论文](https://arxiv.org/abs/2410.07331)，[代码与数据](https://github.com/yiyihum/da-code)。提供候选使用的真实任务、DA-Agent 和执行评测，并报告任务误解等一般失败；它没有语义聚合守卫，因此是任务来源和基础 baseline，而非候选机制的直接先例。

```json
{
  "score": 6.6,
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "RADAR 已在同一 DA-Code 上覆盖类型化执行记录、运行时校验和定向诊断反馈；结合既有 aggregable-properties 与 join-key weighting 工作后，当前方案尚未证明其统计单元追踪不是这些机制的直接组合或任务化实现。",
    "最小实验遗漏有官方代码且已在 DA-Code 上验证的 DS-STAR，也未可执行地隔离相对 RADAR 的增量，因此无法把收益归因于统计单元权重与聚合层级追踪。"
  ],
  "novelty_conclusion": "真实问题和窄机制有研究价值，但核心故事同时被 RADAR 的同任务运行时反馈范式与既有聚合正确性/权重传播工作夹住；当前仅能判断为可能有用的专门化，不能判断为实验就绪的独立贡献。",
  "closest_neighbors": [
    "Fail Loudly: An Auditable Runtime for Agentic Data Analysis (RADAR)",
    "Controlling the Correctness of Aggregation Operations During Sessions of Interactive Analytic Queries",
    "Aggregation Consistency Errors in Semantic Layers and How to Avoid Them",
    "DS-STAR: Data Science Agent for Solving Diverse Tasks across Heterogeneous Formats and Open-Ended Queries",
    "DA-Code: Agent Data Science Code Generation Benchmark for Large Language Models"
  ]
}
```
