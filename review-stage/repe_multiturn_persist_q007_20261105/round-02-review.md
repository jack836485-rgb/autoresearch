## 结论

2026-11-05，总体 score 5.0，verdict：needs_rethink。主贡献是对 GCAD 所提"KV 污染"解释做一次重算历史 cache 的因果检验，再加上随之而来的"干净历史 steering"。论文正文确实没有报告这项检验，它也便宜、有信息量。但作为主会主贡献分量不够，原因有三。第一，这个修法已被最高近邻预先覆盖：GCAD 公开代码里实现了 clean-KV steering 工具；persona_vectors 的 `response` 模式配合每回合重新 prefill 的流程，实质上就是 S2。第二，"双通路分离"中的 (b)"控制走转录"在当前设计下无法判别，因为 S2 每回合仍在当前生成位置持续 steer。第三，剩下的 (a) 只是排除一个解释的单项消融，而且 S1 本身混入了"用户回合和系统提示也被 steer"的因素。

## Claim 判断

| 维度 | 分数 | 依据 |
|---|---|---|
| 重要性 | 6 | 多轮 steering 的连贯性崩坏是真实瓶颈：GCAD 在 Qwen2.5-7B 上测得 15 个特质平均漂移 −18.6，evil 特质的连贯性从 T1 的 37.5 掉到 T10 的 7.1。弄清损伤是否经由历史 KV 传递，对使用者有直接价值。但成功时新增的主要是"不要缓存被 steer 的历史"这一条工程规则，加上对一篇论文假设的证实或否证。影响范围有限。 |
| 新颖度 | 5 | GCAD 正文的 5.3 节和附录 I 都没有 cache 重算或清理的消融，这一点属实。但 GCAD 仓库 `core/activation_steer.py` 里有 `truncate_kv_cache_inplace`，注释写明它服务于"clean-KV steering strategy"：steer 的前向结束后截断脏条目，再用干净前向写回。这比 S2 更细，是逐 token 的干净 KV。另外，persona_vectors 的 `positions="response"` 只 steer 最后一个位置，配合 GCAD 式的逐回合重新分词和 prefill，历史本来就是干净的。所以"干净历史 steering"作为方法只是换名或复现。剩下有新意的部分只是"把它当作因果检验来报告"。 |
| 有效性 | 5 | **(a) 有部分依据。** GCAD 的 no-steering 基线 5 回合漂移只有 −5.4，提示控制定性上稳定；SKOP 说明 steer 会改变 q–k 匹配。这些使"被 steer 的上下文 KV 放大损伤"成为合理预期，S2 大概率会降低漂移。但要注意，GCAD 公开的多轮流程（`eval_multiturn_pipeline.py`）每回合把全部历史重新分词再 `generate`，`positions="all"` 会把 steer 加到历史上**所有**位置，包括系统提示和历次用户回合。因此 S1 相对 S2 多出的不只是"被 steer 的响应 KV"，还有"随回合线性增长的、被 steer 的用户和系统位置"。即便漂移减半，也不能归因到 GCAD 所说的"生成 token 写回 cache"这条通路。**(b) 缺少判别力。** S2 每回合对当前生成仍逐 token steer，即使转录完全不携带控制，特质也会由当前 steer 重新注入。S1≈S2 的等价结果因此推不出"控制走转录"。要检验它，必须有在第 k 回合撤掉 steer、只保留转录或只保留 KV 的条件。**(c)** 没有说明前缀是每回合施加还是只在首回合施加，判别力取决于这一点。其余依据中，2605.26772 的 48% 指的是被 steer 的 CoT，迁移到多轮 persona 需要额外条件。2604.08169 的摘要里查不到"重复放大与选择性成反比"，需要核实。2610.04967 只说两条通路都可能存在，没有明确写出"行为实验分不清"。80% 功效基于一个尚未运行的预实验方差。 |

**与起点的关系：** 研究对象仍是原问题，但只推进了"持续干预为何累积损伤"这一半中的一个候选通路。"何时前缀足够"这一半，在 (b)/(c) 的设计下实际上还没有被回答。

**实验能否判别主张：** (a) 的整条轨迹对比能检验"被 steer 的历史 KV 整体是否贡献损伤"，但混入了被 steer 的用户和系统位置。另外，S1 与 S2 从第 2 回合起文本就分叉，无法分开"KV 直接作用"和"KV 让文本先坏再间接作用"。区分这两者需要固定同一份转录、只交换 KV 的分叉设计。(b) 在当前设计下不可判别，是 Claim 阻断。

**可行性：pass。** 约 2100 万生成 token 外加 prefill，用 8B 模型的 HF hook 批量生成，在 2×A100 上 2–3 天可以完成。本地判官加上 API 生成脚本，远低于 1000 元预算。GCAD 代码可以 clone（已检查），多轮流程、hook 和 clean-KV 工具都在。需要注意几点。公开向量只覆盖 Qwen2.5-7B，Llama-3.1-8B 和 Qwen3-8B 要用 persona_vectors 流程重新抽取，抽取时需要 GPT-4.1-mini 过滤，费用不大。GCAD 用的是温度 1.0 加 GPT-4.1-mini 判官，本方案改为贪心解码加开源判官，S1 能否复现 −18.6 量级的漂移并不确定，而贪心解码在 steer 下更容易陷入重复退化。这些属于可控的实现风险，不是资源缺口。

## 最高近邻

1. **GCAD / Prompt-Activation Duality**（https://arxiv.org/abs/2605.10664 ；代码 https://github.com/NihiI-obstat/Gated-Cropped-Attention-Delta ）。重叠点：同一个 10 回合 persona 协议、同样的模型和特质，KV 污染假设由它提出；仓库里已有 clean-KV steering 工具。差别：正文没有报告 cache 重算的因果检验，也没有区分控制和损伤两条通路。
2. **persona_vectors**（https://github.com/safety-research/persona_vectors ）。重叠点：`positions` 有 all、prompt、response 三种设置，`response` 只 steer 末位，配合重新 prefill 时与 S2 等价，是 S1 和 S2 的现成实现。差别：没有多轮分析。
3. **Prefix Steering**（https://arxiv.org/abs/2610.04967 ）。重叠点：短暂 steer 加上依靠生成上下文延续控制，承认"被改的表示"和"生成的上下文"两条通路都可能起作用。差别：只有单阶段评测，没有转录移植或 KV 对照。
4. **Model vs. User: Whose Values Prevail?**（https://arxiv.org/abs/2610.19817 ）。重叠点：多轮价值 steering 的衰减和反转，冲突与一致两种方向。差别：用探针测量，不区分通路。
5. **Memory Inception**（https://arxiv.org/abs/2605.06225 ）。重叠点：把 KV 当作 steering 的载体，不改可见转录就能在对话中途转向。差别：研究的是控制载体，不是损伤来源。

```json
{
  "score": 5.0,
  "contribution_scores": {"importance": 6.0, "novelty": 5.0, "effectiveness": 5.0},
  "contribution_assessment": "主贡献是对 GCAD 的 KV 污染假设做重算历史 cache 的因果检验，外加干净历史 steering。重要性 6：多轮连贯性崩坏是真实问题（GCAD 测得 −18.6），但成功后的产出主要是一条工程规则和对单一解释的证实或否证。新颖度 5：GCAD 正文没有这项消融，但其公开仓库已有 clean-KV steering 工具，persona_vectors 的 response 模式配合重新 prefill 即等价于 S2，修法作为方法属于换名。有效性 5：(a) 有 no-steering 和提示控制稳定、SKOP 的 q–k 改道等邻近依据，S2 降低漂移的预期合理；但 GCAD 流程用 positions=all，把 steer 加到所有历史位置（含用户和系统），S1 对 S2 的差异不能归因到生成 token 写回 cache。(b) 中 S2 仍持续 steer 当前回合，特质等价推不出控制走转录。还缺固定转录、交换 KV 的分叉设计来区分直接效应与经由文本的间接效应。",
  "feasibility": "pass",
  "feasibility_reason": "GCAD 代码可 clone，多轮流程、hook 和 clean-KV 工具都在；约 2100 万生成 token 加 prefill，用 8B 模型在 2×A100 上 2–3 天可完成，API 费用远低于 1000 元。Llama 和 Qwen3 需要用 persona_vectors 流程重新抽取向量；贪心解码加开源判官与 GCAD 的温度 1.0 加 GPT-4.1-mini 不同，S1 复现存在风险，但都可控。",
  "verdict": "needs_rethink",
  "fatal_blockers": [
    "新颖度阻断：干净历史 steering 已被最高近邻覆盖（GCAD 仓库的 clean-KV steering 工具；persona_vectors response 模式配合重新 prefill 等价于 S2），作为方法贡献只是换名。",
    "Claim 阻断 (b)：S2 每回合仍逐 token steer，特质等价无法区分'控制由转录携带'与'控制由当前回合 steer 重新注入'，缺少撤除 steer、只保留转录或只保留 KV 的条件。",
    "Claim 混淆 (a)：GCAD 设定（positions=all，每回合重新 prefill）同时 steer 了历史中的用户和系统位置，S1 对 S2 不能单独检验'生成 token 写回 cache'的污染通路；也没有固定转录、交换 KV 的分叉设计来区分 KV 直接效应与文本先坏的间接效应。",
    "贡献分量不足：去掉阻断部分后只剩对单一已有假设的一项消融，三项分数离两项 ≥8 差距明显。"
  ],
  "novelty_conclusion": "因果检验本身在已发表文献中没有出现，但修法已在 GCAD 公开代码和 persona_vectors 的 positions=response 设置中出现，双通路分离的另一半在当前设计下无法检验；新意只是增量级。",
  "closest_neighbors": [
    "Prompt-Activation Duality: Improving Activation Steering via Attention-Level Interventions (GCAD, 2605.10664) + public repo clean-KV utility",
    "safety-research/persona_vectors (positions=all/prompt/response steering)",
    "One Token Can Be Enough: Bridging Prompting and Activation Steering with Prefix Steering (2610.04967)",
    "Model vs. User: Whose Values Prevail? Inference-Time Value Alignment in Multi-Turn Conversations (2610.19817)",
    "Memory Inception: Latent-Space KV Cache Manipulation for Steering LLMs (2605.06225)"
  ]
}
```
