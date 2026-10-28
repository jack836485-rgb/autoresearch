## 结论

日期：2026-10-09。**Score：4.6/10；Verdict：`needs_rethink`。** 失败问题本身成立，但当前新意不足以进入实验规划。到 2026 年，已有工作分别覆盖了“证据/检索充分性与答案自信分离”“用结构覆盖信号触发定向补检索”，并且同一 LongMemEval 任务上已有公开实现使用实体、时间、来源覆盖和多轮定向检索。当前候选剩余差别主要是把这些机制压缩成 CPU 规则、限制为一次改写并放进两调用预算；在尚无结果时，这属于任务适配和工程简化，不能支撑独立方法 Claim。**当前不值得按此 Claim 继续进入实验规划。**

Fatal blockers：

- **核心新意已被覆盖。** [RCL](https://arxiv.org/abs/2609.11023) 明确以模型内部答案自信之外的结构覆盖分数检测检索不足，并触发定向追加检索；[S2G-RAG](https://aclanthology.org/2026.acl-long.1185/) 依据问题与当前证据判断充分性、输出缺口并形成下一次查询；[ActiveGraph LongMemEval 公开实现/报告](https://github.com/yoheinakajima/activegraph-longmemeval/blob/main/ACTIVEGRAPH_MEMORY_V2_REPORT.md) 已在同任务中使用实体/事件/时间、来源覆盖、定向查询变体和多轮检索，并明确提出以低实体匹配、缺失操作数或不完整来源覆盖触发新检索轮。
- **必要对照与预算协议未形成可复现实验。** 表中只有官方 BM25 direct 与同检索 CoN 的命令；“始终二查”和“自置信再检索”没有固定改写提示、置信定义、阈值或运行入口。官方 `con` 映射为 `--cot true --con false`，只有一次最终生成调用，而候选包含一次 LLM 改写和一次 reader 调用；“两次调用上限”与“相同总 LLM 调用、相同总输入输出 token”如何对齐尚未定义，因而关键比较目前不是同预算可复现比较。
- **既有失败表述过强。** “reader 无法知道漏检”没有被 LongMemEval 的检索/阅读分解所证明；[Sufficient Context](https://arxiv.org/abs/2411.06037) 和 S2G-RAG 都表明只看问题与现有证据可以判别一部分上下文不足。可以成立的是 reader 无法观察未返回的历史内容，而不是 reader 原理上无法诊断证据不足；当前因果叙述把两者混为一谈。

## Claim 判断

| Claim | 判断 | 关键依据 |
|---|---|---|
| 无相关 context 不等于历史没有答案；应区分 retrieval 与 reading 错误 | 已被覆盖 | [LongMemEval](https://arxiv.org/abs/2410.10813) 已按 indexing/retrieval/reading 分解系统并用 oracle retrieval 暴露 reading 差距；[EvalMem](https://arxiv.org/abs/2609.22231) 又在 LongMemEval-S 上显式归因 encoding、retrieval、generation 缺陷。 |
| 用独立检索覆盖/充分性信号而非 reader 答案自信决定是否追加检索 | 已被覆盖 | RCL 的结构覆盖分数直接触发 targeted follow-up retrieval；S2G-RAG 的独立 S2G-Judge 以证据充分性和缺口生成下一查询；ActiveGraph 在 LongMemEval 上已有 retrieval sufficiency、source-coverage checks 和 targeted query variants。 |
| CPU 跟踪实体命中、属性与会话时间覆盖，在两调用预算内只改写一次 | 部分重合 | 具体的轻量规则和“一次改写”限制可能是实现差别；但 ActiveGraph 已在同任务公开实体、事件、时间窗、来源覆盖和多轮定向检索，RCL 也已建立“结构覆盖而非答案自信”的机制，未见足以构成方法新意的剩余技术原理。 |
| 用固定 k、相同预算，对照一次 CoN、始终二查、自置信触发和覆盖触发来验证独立收益 | 部分新颖但不可执行 | 这是合理的因果实验框架，但关键动态对照尚无具体入口，且一调用官方 CoN 与两调用改写方案的调用/token 对齐未闭合；按 rubric 构成可行性 blocker。 |
| 若覆盖信号不能区分漏检与有信息样本、或误弃增加则停止 | 已被覆盖/非独立 Claim | 这是标准的拒答风险-覆盖与触发器有效性否证条件；Sufficient Context 等工作已采用选择性生成和 coverage trade-off。 |

## 最高近邻

1. [ActiveGraph Memory v2 LongMemEval Report / public repository](https://github.com/yoheinakajima/activegraph-longmemeval/blob/main/ACTIVEGRAPH_MEMORY_V2_REPORT.md)（2026）。重叠：同一 LongMemEval-S，公开代码包含 source-coverage checks、实体/事件/时间结构、targeted query variants、multiple retrieval rounds，并明确写出低实体匹配、缺失操作数或覆盖不完整应触发定向查询。差别：它是更大的图/类型化检索系统，live sufficiency 路径尚未完整 benchmark，也没有候选的固定一次改写和 BM25 两调用最小化约束。

2. [RCL: A Retrieval-Confidence Layer for Detecting Insufficient Context](https://arxiv.org/abs/2609.11023)（2026）。重叠：使用模型内部答案自信之外的结构覆盖信号，在生成前判断检索不足，并触发 targeted follow-up retrieval；这几乎覆盖候选的抽象机制 Claim。差别：面向企业代码生成，以调用图覆盖与新颖度为特征，不是长期对话记忆或 LongMemEval。

3. [S2G-RAG: Structured Sufficiency and Gap Judging for Iterative Retrieval-Augmented QA](https://aclanthology.org/2026.acl-long.1185/)（ACL 2026；[官方代码](https://github.com/nianaaa/S2G-RAG)）。重叠：控制器只读取问题和累计证据，判断是否足够；不足时输出结构化缺口并生成下一检索查询。差别：面向多跳开放域 QA，S2G-Judge 需要训练/LoRA，计算条件和任务均不同于候选的 CPU 规则。

4. [Sufficient Context: A New Lens on Retrieval Augmented Generation Systems](https://arxiv.org/abs/2411.06037)（2024）。重叠：将上下文是否足以回答作为独立于最终答案正确性/自信的信号，并用于选择性回答和弃答，直接削弱“reader 无法诊断不足”的强表述。差别：重点是静态 RAG 的充分性分类和 abstention，没有把缺口转成二次检索。

5. [LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory](https://arxiv.org/abs/2410.10813)（ICLR 2025；[官方代码](https://github.com/xiaowu0162/LongMemEval)）。重叠：同一任务、检索/阅读错误分解、abstention、时间感知 query expansion，以及可运行的 BM25/direct/CoN 路径。差别：其 query expansion 是预设检索设计，不是依据首轮覆盖动态触发一次补检索。

```json
{"score":4.6,"verdict":"needs_rethink","fatal_blockers":["核心机制已被同任务公开实现和近期论文覆盖：独立结构/覆盖信号触发定向二次检索不是新的主张","必要动态对照缺少可复现定义，且官方一次 CoN 与改写加 reader 的两调用方案之间的调用和 token 预算协议未闭合","reader 无法知道漏检的既有失败表述缺少支持，并被上下文充分性判别工作部分反证"],"novelty_conclusion":"问题重要，但当前贡献主要是把已知的检索充分性/结构覆盖触发机制适配为 LongMemEval 上的轻量两调用规则；在没有新发现或实质不同机制前，不足以形成独立方法 Claim。","closest_neighbors":["ActiveGraph Memory v2 LongMemEval Report","RCL: A Retrieval-Confidence Layer for Detecting Insufficient Context","S2G-RAG: Structured Sufficiency and Gap Judging for Iterative Retrieval-Augmented QA","Sufficient Context: A New Lens on Retrieval Augmented Generation Systems","LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory"]}
```
