## 结论

日期：2026-10-09  
**score：7.3/10**  
**verdict：promising_needs_revision**

新意判断：核心抽象“以已获得证据/覆盖状态约束 agent 的停止或完成”已被 HALT 与 Evidence-Carrying Termination 明确覆盖；本 brief 尚存的窄新意，是把它落实为 **API 分页检索中的否定语义**：某页为空或列表被截断，只能支持已查范围内的否定，不能支持全局不存在，并用游标/页号/终止标志形成可审计的覆盖状态。该窄边界未在检索到的 AppWorld 工作中被直接实现，但目前也没有实验证据表明 AppWorld 失败确由这一机制导致，因此不能视为已建立的新 failure finding。

是否值得继续：**值得继续做冻结范围内的诊断与最小实验，但当前不满足 experiment_ready。** 同任务官方 agent、普通分页提醒和固定多翻一页构成了可复现、可证伪且预算匹配的对照；若提示或固定多读一页已消除同预算差异，brief 自己承认独立贡献不成立。未发现致命可行性 blocker。

## Claim 判断

| Claim | 判断 | 关键依据 |
|---|---|---|
| AppWorld 的公开 API 存在真实分页，单页结果不等于全集 | 部分重合 | AppWorld 官方文档公开 `page_index/page_limit`、`find_one_from_pages`、`find_all_from_pages` 与 `yield_page`，且默认最多扫描 3 页；该结构事实成立，但不是新贡献。 |
| agent 会把空页或截断列表误判为全局不存在 | 新颖但未证实 | *Agents Don’t Paginate* 给出 agent 不主动请求后续 chunk 的直接经验事实，AppWorld false-success 研究也证明该 benchmark 存在大量错误完成；两者都未证明本 brief 所指的“空页/截断 → 全局不存在”因果链。当前表述只能算待检验诊断假设。 |
| 用显式覆盖状态约束否定结论和停止 | 部分重合 | HALT 已将停止定义为 evidence coverage，并在每轮检索后按覆盖决定是否停止；ECT 已要求完成声明由范围内轨迹证据和覆盖检查支撑。差别主要在分页枚举的负向存在性语义、显式游标/页范围，以及 AppWorld 同任务验证。 |
| 在同一硬预算下同时减少过早否定与无效无限翻页 | 新颖、可证伪 | 普通提醒、固定多翻一页和覆盖状态控制能区分“提示收益”“额外一次调用收益”和“状态机制收益”；当前没有结果，因而只能主张实验设计，不可主张效果。 |
| 无训练、CPU 侧、API 无关的覆盖跟踪器构成独立机制 | 部分重合 | 外置轻量停止门已见于 HALT，范围/证据账本已见于 ECT；不硬编码特定 API 与 AppWorld 分页状态是实现边界，但不足以单独支撑宽泛机制新颖性。 |

## 最高近邻

1. [HALT: Verification-Aware Stopping for Retrieval-Augmented Search Agents](https://arxiv.org/abs/2608.02009)（[官方代码](https://github.com/Noverse0/HALT)）：同样把停止改写为累计证据覆盖，并用外置轻量 verifier 控制冻结 agent。差别是其目标为多跳 QA 中“证据已足够后停止”，本 brief 针对分页 API 中“尚未覆盖时不得作全局否定”，且无需训练 verifier。

2. [When May an Agent Stop? Evidence-Carrying Termination for Tool-Using LLMs](https://arxiv.org/abs/2608.23623)：要求每个完成声明绑定有效、范围内的轨迹证据，并以 required-slot coverage 门控终止；arXiv 附件公开 verifier 与复现实物。它覆盖了“结论必须受证据范围约束”的核心原则，但未处理分页枚举完备性、负向存在性或 AppWorld。

3. [Agents Don’t Paginate: First-Chunk Selection for LLM Tool Responses](https://arxiv.org/abs/2608.26130)（[公开代码](https://github.com/meteora-pro/devboy-tools)）：直接报告 agent 在公开 MCP 中间件日志中不请求第二个 chunk，证明分页遗漏是现实行为。其任务是 SWE-bench 文件定位和首 chunk 选择，未建模“全局不存在”结论、游标覆盖状态或 AppWorld 端到端 TGC。

4. [From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents](https://arxiv.org/abs/2606.09863)：在 1,879 条 AppWorld 轨迹上研究错误完成，并发现基于 API 调用轨迹的轻量检测器有效。它支持 AppWorld 中“完成判断不可靠”的宽泛问题，但没有把失败归因于分页覆盖，也没有提出覆盖控制器。

5. [AppWorld: A Controllable World of Apps and People for Benchmarking Interactive Coding Agents](https://arxiv.org/abs/2407.18901)（[官方仓库](https://github.com/StonyBrookNLP/appworld)）：提供完全相同的 benchmark、官方 ReAct/full-code agent、CLI 入口和分页工具；官方任务生成指南已经提供跨页扫描 helper。差别是它没有将可见分页覆盖状态作为否定结论的运行时约束。

```json
{"score":7.3,"verdict":"promising_needs_revision","fatal_blockers":[],"novelty_conclusion":"证据覆盖门控停止这一宽泛机制已被 HALT 与 ECT 覆盖；分页 API 中以已查页/游标范围限定全局否定、并在 AppWorld 同预算验证，仍有窄而未证实的新意。","closest_neighbors":["HALT: Verification-Aware Stopping for Retrieval-Augmented Search Agents","When May an Agent Stop? Evidence-Carrying Termination for Tool-Using LLMs","Agents Don’t Paginate: First-Chunk Selection for LLM Tool Responses","From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents","AppWorld: A Controllable World of Apps and People for Benchmarking Interactive Coding Agents"]}
```
