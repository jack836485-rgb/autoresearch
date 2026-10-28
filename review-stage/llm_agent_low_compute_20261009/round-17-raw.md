## 结论

当前日期：2026-10-09。**score: 5.2/10；verdict: `needs_rethink`**。问题有真实一级证据，固定 `k` 的诊断与对照也可证伪；但“硬时间过滤会不可恢复地损害召回，因而应保留原始语义候选”的核心 Claim 已被 SATF 在同一 LongMemEval 任务上直接提出并实验化，Cognis 也已采用保留语义分数的时间加成。精确的 BM25 固定槽位分配是实现差异，不足以支撑当前独立新意。而且最小实验未纳入 SATF 及 LongMemEval 官方 time-aware query expansion 的已打开代码与具体复现路线，构成 fatal baseline blocker。**不值得以当前独立 Claim 继续进入实验规划。**

## Claim 判断

| Claim | 判断 | 关键依据 |
|---|---|---|
| 小模型会对无明确时间范围的问题误生成范围，使 gold evidence 移出 reader 的 top-`k` | 已被覆盖 | LongMemEval E.4 明确给出 Llama-3.1-8B 假阳性范围及低 recall 结论；官方代码将范围外候选后移，在有限 top-`k` 下即产生该失败。 |
| “错误时间筛选的不可恢复性”是被忽视的关键瓶颈 | 已被覆盖 | SATF 直接将 hard filtering 降召回作为动机，并报告 GPT-4o time-range filter 将 R@10 从 0.795 降至 0.701。 |
| 保留原始语义候选可在不扩大 reader 上下文时恢复误筛 | 部分重合，核心已覆盖 | SATF 对原候选集软重排、不删除范围外项，仍输出固定 top-`k`；Cognis 亦以时间分数加成而非硬删除。当前方案的槽位配额只是较窄的机制变体。 |
| 文本可确定日期时规则筛选，不可锚定时保留全局候选 | 部分重合 | Cognis 先做时间意图/触发词检测再加成；Chronos 同时保留原始 turn calendar 与时间 event calendar，证据不足时可扩大搜索。差别是它们不使用本 brief 的 BM25 固定槽位规则。 |
| 当前最小实验能建立独立研究贡献 | 已被阻断 | 对照可测，但缺少最高近邻 SATF 与官方 time-aware 实现；Chain-of-Note 是 reader 基线，不能替代同任务时间检索基线。 |

## 最高近邻

1. [Self-Anchored Temporal Filtering for LLM-Free Temporal-Aware Memory Retrieval](https://lemma-public-asset.analemma.ai/online/fars/live/live_live_20260213/idea_2323913d-28fd-4658-a687-f3e80c5d90e3/main.pdf) ([code](https://gitlab.com/fars-a/self-anchored-temporal-filtering))：同一 LongMemEval，直接论证硬时间过滤会伤害召回，并保留原候选做软时间重排；差别为 Stella 密集检索+高斯时间亲和度，而非 BM25+固定槽位。
2. [LongMemEval](https://arxiv.org/abs/2410.10813) ([code](https://github.com/xiaowu0162/LongMemEval))：E.4 已观察小模型在无时间引用时误生范围并降低 recall；当前 idea 的失败故事来自此已知结果，新增的只是保底配额。
3. [Cognis: Context-Aware Memory for Conversational AI Agents](https://arxiv.org/abs/2604.19771)：在 LongMemEval 上将 BM25/向量融合分数与 temporal score 加权，时间分数有非零下限，因而不做硬删除；差别是系统更重且无固定 BM25 配额消融。
4. [Chronos: Temporal-Aware Conversational Agents with Structured Event Retrieval for Long-Term Memory](https://arxiv.org/abs/2603.16862)：并行维护时间 event calendar 与原始 turn calendar，支持按时间收紧和证据不足时扩大搜索；差别是 agentic 多步检索、变动成本与密集/API 组件。
5. [Did You Check the Right Pocket? Cost-Sensitive Store Routing for Memory-Augmented Agents](https://arxiv.org/abs/2603.15658) ([code](https://github.com/krimler/memroute))：已将“语义信号清晰时窄路由、模糊时用保守 fallback 保 coverage”形式化，并使用 LongMemEval 类型；但它是 store routing 与合成标签，不是时间候选排名。

```json
{"score":5.2,"verdict":"needs_rethink","fatal_blockers":["SATF 已在同一 LongMemEval 上覆盖‘避免硬时间过滤、保留原始候选’的核心 Claim 与机制目标","当前最小实验缺失 SATF 及 LongMemEval 官方 time-aware query expansion 这两个同任务、公开代码、可复现的关键基线"],"novelty_conclusion":"硬时间筛选的召回损失及通过保留全局语义候选来恢复的核心已被覆盖；BM25 固定 k 槽位分配仅是增量实现差异。","closest_neighbors":["Self-Anchored Temporal Filtering (SATF)","LongMemEval","Cognis","Chronos","Did You Check the Right Pocket?"]}
```
