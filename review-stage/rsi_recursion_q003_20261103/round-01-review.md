## 结论

审查日期 2026-11-03。总体 score 5.5，verdict 为 promising_needs_revision。

主贡献是一项受控测量研究：在 harness 级 RSI 中做"新一代改进者对旧一代改进者"的同起点、同预算交换测试，估计递归曲线 Δ_k 与放大比 r_k，再把后代优势拆成技能、历史、选择噪声三部分。问题本身值得做，但目前分量不够。原因有三。

- 交换测试并不新。审计论文 2610.27610 已经把它规定为 C4 主张的必要检验；Hyperagents 的 imp@k 迁移实验、MetaRSI 的 meta-updated 对原始改进者实验都已做过。
- 选择噪声这一块，Winner's Curse（2610.09239）已在自改写 instruction 的设置下系统量化过。
- 真正新的部分是"历史匹配"分解，但在所选的两个系统（STOP 和 Promptbreeder）里几乎没有可交接的历史。而已报告改进者增益为正的系统（DGM-H、MetaRSI）被放在了扩展里，所以负面结论无法回应真正的正面主张。

## Claim 判断

| 维度 | 分数 | 依据 |
|---|---|---|
| 重要性 | 6.5 | RSI 的过程主张证据薄弱。审计论文的统计已核实：26 篇声称改进者变强的研究里，只有 4 篇做了同起点、同预算的前后代比较。一条去偏的递归曲线能改变研究判断，这一点有价值。但结论只覆盖 STOP 和 Promptbreeder 这类较早、较弱的系统，弱开源模型下还可能直接退化。所以即使得到 r_k<1，也很难外推到 DGM-H 或 MetaRSI。那两者在交换测试下已报告正增益（imp@50 0.63 对 0；+7.2 对 +4.9）。影响范围有限。 |
| 新颖度 | 5.5 | 下面几项都已被近邻覆盖：同起点前后代交换测试（审计论文给出规范，MetaRSI 已执行）；固定 meta agent 后在未见域上比较迁移能力（Hyperagents 的 imp@k）；单次评测选择导致的赢家诅咒与 held-out 去偏（Winner's Curse、Harness Ceiling 的 Proposition 1）。剩下的增量是两点：一是历史匹配对照，把 I_k 的历史交给 I_0；二是多谱系、多代的放大比估计，外加三部分分解。这是可辨认的增量，主要是把已知检验组合起来再加一个对照，没有新的机制或理解方式。 |
| 有效性 | 5.5 | 已核实的依据有四条。(1) 选择乐观：Harness Ceiling 报告单次 rollout σ=0.023，单次 0.535 的读数复测只有 0.44–0.46。(2) 评测方差和任务顺序效应：2608.18066。(3) Promptbreeder 消融：最大收益来自初始化重述，但测的是训练 fitness 而非留出效果，而且去掉 hyper-mutation 同样有害。(4) STOP 在 GPT-3.5/Mixtral 下自我改进会退化，这一点确有报告。这些依据支持"未去偏的后代优势被高估"，迁移条件是评测集小、单次读数。但它们不支持"历史"是独立成分。STOP 的改进者是一段自包含程序，Promptbreeder 的 mutation prompt 也不携带笔记，所以历史匹配在这两个系统里大概率是空操作，三部分分解会退化成两部分。另外，主假说把"放大"（r_k≥1）和"递归存在"（去偏后 Δ_k>Δ_0）混为一谈：r_k<1 而 Δ_k>Δ_0 时，改进者仍然更会改进。r_k 是两个小而嘈杂差值的比，Δ_k 接近 0 时没有定义；5 条谱系下，它的置信区间大概率给不出结论。 |

- **与起点问题的关系**：回答的是原问题的第二个主张（后代改进者更会改进），并顺带测第一个主张（跨轮累积）。范围没有问题。原问题仍未回答的部分有两块：带持久记忆和代码自修改的强系统里递归是否成立，以及收益来源。
- **实验能否判别主张**：只能部分判别。去偏选择对照能检验"增益来自赢家诅咒"。但它比较的是两种进化流程，产生的是不同的谱系，并不是对同一谱系做分解。历史匹配在所选系统里没有可操作的对象。用 r_k 的置信区间是否低于 1 作为判据，会把"收益递减但递归为正"判成"假说成立"。STOP 在 Qwen3-32B 上如果直接退化，也会让主假说在平凡意义上成立，无法区分"递归是假象"和"模型太弱"。
- **可行性**：pass。microsoft/stop、Promptbreeder 第三方实现、SePO 代码都已公开，接入 vLLM 的 OpenAI 兼容端点是常规操作。Qwen3-32B 和 BF16 下的 235B-A22B 都能放进 8×A100。约 6 亿 token 的核算算术正确，但没有计入三类对照（会让规模成倍增加）、进化阶段本身的 meta-utility 评估，以及第二个模型规模。用 72B 级模型时总量可能达到 20–30 亿 token，接近 5 天上限。用 32B 做主力仍然可以完成。这里不缺数据和代码，缺的是历史对照在所选系统中的可构造对象。

## 最高近邻

1. Auditing the Product, Not the Recursion（https://arxiv.org/abs/2610.27610）：定义了 C4 改进者增益主张及其交换测试，并统计出 4/26 的比例。本方案的核心实验设计基本由它规定。差别在于它没有做实验，也没有做分解。
2. Hyperagents / DGM-H（https://arxiv.org/abs/2603.19461）：固定 meta agent 后，用 imp@k 比较迁移后的 meta agent 与初始 meta agent，未见域上 0.63 对 0，p<0.05。它的收益来自持久记忆和性能追踪，正是历史这一混淆。差别在于它没有做历史匹配和选择去偏，也没有做多代曲线。
3. MetaRSI / RSI2（https://arxiv.org/abs/2609.06396）：同一系统、同一预算下比较 meta-updated 改进者与原始改进者，+7.2 对 +4.9，五个 term 的差距逐期扩大。这是正面递归证据。差别在于它没有做去噪，也没有做历史分离。
4. The Winner's Curse in LLM Self-Improvement Loops（https://arxiv.org/abs/2610.09239）：在 Qwen 自改写 instruction 的循环里，用 600 条留出数据量化赢家诅咒和锁定效应，并检验接受规则。它覆盖了本方案的"选择噪声"成分。差别在于它不涉及改进者自身的演化。
5. STOP（https://arxiv.org/abs/2310.02304）：在 GPT-4 下比较自改进前后改进者的下游效用（含迁移任务），并报告弱模型下的退化。差别在于它没有多谱系，也没有去偏或分解。

```json
{
  "score": 5.5,
  "contribution_scores": {"importance": 6.5, "novelty": 5.5, "effectiveness": 5.5},
  "contribution_assessment": "主贡献是受控交换测试下的递归曲线 Δ_k、放大比 r_k，以及技能/历史/选择噪声的三部分分解。重要性有限：结论只覆盖 STOP 和 Promptbreeder 这类较弱的系统，无法回应 DGM-H 和 MetaRSI 已报告的正面改进者增益。新颖度有限：交换测试已由审计论文规定，并由 MetaRSI 和 Hyperagents 执行；选择噪声已由 Winner's Curse 量化；剩下的增量是历史匹配对照和多代放大比。有效性方面，选择乐观和评测方差的依据已核实，但历史成分在所选系统中缺少可交接对象；r_k 比值在 Δ_k 接近 0 时不稳定；主假说把'不放大'当成'无递归'。待验证的是：去偏后 Δ_k 是否仍高于 Δ_0，以及历史成分在带记忆的系统中的贡献。",
  "feasibility": "pass",
  "feasibility_reason": "STOP、Promptbreeder 实现和 SePO 代码均公开，接入 vLLM 是常规操作。Qwen3-32B 主力实验在 8×A100 上 5 天内可完成。原核算漏计了三类对照、进化阶段的评估和第二个模型规模，72B 级模型会接近上限，但 32B 方案可行。",
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "新颖度不足：同起点交换测试已由 2610.27610 规定，并由 MetaRSI 和 Hyperagents 的 imp@k 执行；选择噪声成分已被 Winner's Curse（2610.09239）覆盖。剩余增量依赖历史分解。",
    "Claim 阻断：历史匹配对照在 STOP（自包含改进程序）和 Promptbreeder（mutation prompt 不携带笔记）中缺少可交接的历史，三部分分解在所选系统中无法实施。",
    "Claim 阻断：主假说用 r_k<1 判定递归不成立，把'收益递减'和'无递归'混为一谈；r_k 是两个小噪声差值之比，5 条谱系下无法给出判别性置信区间。",
    "重要性与外推阻断：已报告正面改进者增益的系统（DGM-H、MetaRSI）只列为扩展，弱模型下 STOP 的退化会让主假说平凡成立，无法区分'递归是假象'与'模型太弱'。"
  ],
  "novelty_conclusion": "相对审计论文、Hyperagents imp@k、MetaRSI 和 Winner's Curse，是把已知检验组合起来再加一个历史对照的增量，其中历史对照在所选系统里难以实施。去掉近邻后，剩下的独立新意不足 8 分。",
  "closest_neighbors": [
    "Auditing the Product, Not the Recursion (arXiv 2610.27610)",
    "Hyperagents (arXiv 2603.19461)",
    "MetaRSI / RSI2 (arXiv 2609.06396)",
    "The Winner's Curse in LLM Self-Improvement Loops (arXiv 2610.09239)",
    "Self-Taught Optimizer STOP (arXiv 2310.02304)"
  ]
}
```
