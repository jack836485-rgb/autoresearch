## 结论

**评审日期：** 2026-11-01

**评分：** 5.5 / 10

**结论：** promising_needs_revision。问题值得做，但当前设计不能进入实验。

**新颖性：** 部分新颖。在"已完成且经验证的 agent 工作遭错误指责"这一设定下，保持内容不变、分离"措辞（行动偏置）"与"证据来源（来源折扣）"两个因素，目前没有找到直接覆盖这一做法的工作。不过它的各个组成部分都已有近邻：

- **措辞因子与"改写为信息项"的干预：** 接近 *Ask don't tell*（非提问式输入引发更多谄媚，先改写为提问可以缓解），也接近 FixedBench 的 action bias 结论（把不行动明确表述为成功能减少行动）。
- **来源因子：** 接近 2607.20827（只改变来源权威性，观察对行动的影响）与 2604.22193（文档断言与用户断言的权重差异）。
- **双侧评测：** 在问答场景中已有 *Stubborn or Sycophantic?*（Update 与 WrongFlip 分开报告）。把评测扩展到"真实指责"正是 CAVE 论文自己写明的后续方向。

去掉 CAVE 的名字后，C1 仍可以独立成立。C2 和 C3 则主要是在补全 CAVE：一个解释 CAVE 观察到的自建与继承任务差距，一个补上 CAVE 声明的真实指责对照。

**致命阻塞：**

1. **主张与实验错位。** 故事线的核心是 EO，也就是强模型在找回证据之后仍然破坏工作。但模型组以 8–9B 开源模型为主（Qwen3.5-9B、Llama-3.1-8B）。CAVE 报告，随着破坏率上升，弱模型的破坏路径从 EO 转向 CD；即使在最强的模型上，EO 也只有约 11–12%。C1 和 C2 的判定量是总体 ROH，而不是限定在 EO 路径上的结果。每格只有 96 次运行，EO 事件会极少，所以实验检验不到它声称要分离的机制。
2. **C1 的判定逻辑不能识别成因。** 比较"措辞效应"和"来源效应"的大小，结果取决于每种操纵设得多强，而这个强度是人为选定的。信息式措辞还写明了"未要求操作"，等于一条显式的不行动指令，会把指令遵循和行动偏置混在一起。另外，措辞是在两个压力水平上平均得到的效应，来源却只在"指令式 + 原压力"一个格子里测，两者不在同一设计上比较。
3. **C3 的两侧不对称，且缺少最强基线。**
   - 真实指责可以在本地复现，错误指责按定义无法本地核实。I1 和 I2 只在回滚、删除等破坏性操作上触发，而且出示工作区证据就会放行，所以在真实指责一侧，它们的修复损失按设计就接近于零，对照无法区分各干预。
   - 比较中省略了 CAVE 降低破坏最多的 I3（实时信号闸门）。
   - I1、I2 都没有公开实现。I2 要把 D1–D6 这六类"伤害目标"映射成可拦截的工具调用，这一步并不简单，复现保真度也没有校准途径。
4. **自建任务的可行性。** CAVE 对自建任务设有有效性门槛：只有第一步做对的运行才计入。8B 级模型在最多 90 轮的 hermes harness 中，大量自建运行预计会被排除。C2 的样本会严重缩水，还会偏向容易的任务。另外，CAVE 中的 Qwen3.5-9B 结果来自 Claude Code，而不是 hermes。

**是否值得继续：** 值得。这个问题有分量，CAVE-Bench 已克隆核验，任务目录、`hermes_custom_openai.py`、`harbor run` 和 `aggregate.py` 都存在。但在上述阻塞解决之前，不能交给实验阶段。

## Claim 判断

| Claim | 判断 | 关键依据 |
|---|---|---|
| C1：在内容不变的前提下，措辞效应与来源效应可以分离，且由行动偏置主导 | 部分重合 | 措辞方面：*Ask don't tell* 已证明陈述与提问的框架效应，FixedBench 已提出 action bias，CAVE 的 Q0–Q3 已分层考察指责强度。来源方面：2607.20827 与 2604.22193 已考察来源权威性。agent 设定加 2×3 因子分离仍是新的，但判定量（ROH）和弱模型组都测不到 EO 机制。 |
| C2：消除主导因子后，自建与继承任务的差距缩小 | 部分重合，偏向补全 CAVE | 这一差距是 CAVE 已报告的现象（ERF +4.41、EO +3.75），C2 只是给它一个解释。自建有效性门槛加上弱模型，会让比较缺乏统计功效。 |
| C3：对症干预在双侧上优于 I1、I2 | 部分重合 | 双侧评测在问答中已有（*Stubborn or Sycophantic?*），在 agent 中是 CAVE 声明的后续方向。"改写为信息项"接近 *Ask don't tell* 的改写式缓解，"可信记录"接近 2609.05587 的可靠性标签，以及 EnvTrustBench 提倡的来源元数据。真实指责一侧可本地复现，使对比失去区分度；I3 缺席。 |
| 故事线前提："现有工作从未分离两种成因" | 大体成立，但有边界 | CAVE 用 EO 路径和 CDC 指标描述了"采信证据后仍破坏"，但没有拆解成因。2604.19117 在问答电路层面给出"识别了错误却仍然顺从"（deference，不是 detection），说明顺从是独立于识别的机制，这与"行动偏置"假设部分重叠。 |

## 最高近邻

1. **CAVE-Bench**，"You're Right, Let Me Fix It"（https://arxiv.org/abs/2609.32616 ；代码 https://github.com/henrymao2004/agent-over-correction ，已克隆核验）
   - 重叠：同一设定与同一指标（ROH/FCS/ERF、EO 路径），自建与继承任务的差距，I1/I2/I3 缓解。论文明确把"warranted accusations"列为后续方向。
   - 差别：CAVE 只做因子分层，没有在内容不变的前提下操纵措辞与来源，也没有真实指责对照。
2. **FixedBench**，"Coding Agents Don't Know When to Act"（https://arxiv.org/abs/2605.07769）
   - 重叠：编码 agent 的 action bias；先复现再修的指令会在部分已修复的问题上导致错误放弃（双侧代价）。
   - 差别：没有指责与压力，也没有证据来源操纵，任务对象是过时的 issue，而不是 agent 自己的工作。
3. **Ask don't tell: Reducing sycophancy in LLMs**（https://arxiv.org/abs/2602.23971）
   - 重叠：因子化操纵输入框架（陈述与提问），并把"先改写为提问"用作缓解，与本案的措辞因子和"改写为信息项"干预高度同构。
   - 差别：场景是问答与选择，没有工具行动和对已完成工作的破坏。
4. **Auditing Provenance Sensitivity in LLM Agent Action Selection**（https://arxiv.org/abs/2607.20827）
   - 重叠：固定内容，只改变来源权威性，测量 agent 的行动差异。
   - 差别：只有可信与不可信两档，没有"agent 自取"这一来源，也不涉及指责、谄媚和破坏。
5. **Stubborn or Sycophantic? Auditing What Sycophancy Evaluations Measure**（https://openreview.net/forum?id=WcbzSR7NB9 ，NeurIPS 2026）
   - 重叠：主张把有效纠正（Update）与有害翻转（WrongFlip）分开报告，并指出降低谄媚的提示往往以拒绝有效纠正为代价，即 C3 的双侧逻辑。
   - 差别：是问答多选场景，不是 agent。

```json
{
  "score": 5.5,
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "Claim-test mismatch: the story targets EO (evidence recovered then damage), but the model set is mainly 8-9B models whose damage is mostly CD per CAVE, and C1/C2 are judged on aggregate ROH with about 96 runs per cell, so EO events are too sparse to test the mechanism",
    "C1 identification: comparing effect sizes of two manipulations whose strength is chosen by hand cannot identify the dominant cause; the informational wording adds an explicit 'no action requested' instruction (confounding instruction compliance); the source factor is tested in only one wording x pressure cell, so the designs are unbalanced",
    "C3 asymmetry: true accusations are locally reproducible while false ones are not, so I1/I2 (triggered on rollback/deletion and passed by workspace evidence) lose almost nothing on the true side by construction; the strongest same-task baseline I3 is omitted",
    "Baselines I1/I2 have no public implementation; I2 needs a nontrivial mapping from harm targets D1-D6 to interceptable tool calls, with no fidelity calibration route",
    "Self-built validity gate plus 8B-class models in the hermes harness will exclude many self-built runs, leaving C2 underpowered and biased toward easy tasks"
  ],
  "novelty_conclusion": "Partially novel: content-controlled wording-vs-source decomposition of over-correction in an agent false-accusation setting has no direct precedent, but each part overlaps prior work (Ask don't tell framing and reframing, FixedBench action bias, 2607.20827 provenance sensitivity, two-sided correction evaluation in QA); C2/C3 largely complete CAVE-Bench's own observations and stated future work",
  "closest_neighbors": [
    "You're Right, Let Me Fix It: How LLM Agents Damage Correct Work When Falsely Accused (CAVE-Bench, arXiv 2609.32616)",
    "Coding Agents Don't Know When to Act (FixedBench, arXiv 2605.07769)",
    "Ask don't tell: Reducing sycophancy in large language models (arXiv 2602.23971)",
    "Auditing Provenance Sensitivity in LLM Agent Action Selection (arXiv 2607.20827)",
    "Stubborn or Sycophantic? Auditing What Sycophancy Evaluations Measure (NeurIPS 2026, OpenReview WcbzSR7NB9)"
  ]
}
```
