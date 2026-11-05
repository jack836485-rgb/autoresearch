## 结论
2026-11-05：总体 score 5.5，verdict **promising_needs_revision**。主贡献是测量多轮前缀 steering 的跨轮持续由什么承载：保留下来的转录，还是被 steer 位置的 KV。附带一个“表达强度 × 冲突”的判据，以及推理模板剥离思考带来的交叉预测。这个问题真实存在，原作者也明确留了口。但按当前设计，主结论大概率与已有证据（转录回放、自身回答污染、steer 下生成的 CoT 能单独携带效果）给出的方向一致。KV 通路最可能占有份额的情形是全程注入，这正是 GCAD 的 KV 污染假说，而主实验没有对它做隔离。所以贡献分量和新意都达不到两项 ≥8 的门槛。

## Claim 判断
| 维度 | 分数 | 依据 |
|---|---|---|
| 重要性 | 6.0 | 回答了 2610.04967 结论中明说的未决问题（原文：“our behavioral experiments do not distinguish between these mechanisms”，并提出“when a brief prefix suffices”），对使用前缀 steering 的人有实用判据。影响有限，原因有三。第一，对象只限前缀 steering 这一个 2026-10 的新方法。第二，“转录承载”与 2601.20834、2602.24287、2605.26772 的方向一致，成立后改变的领域判断不大。第三，判据中“冲突使效果衰减”已由 2610.19817 报告（用户与助手方向相反时，早期效果会衰减或反转），“上一轮表达强度能预测下一轮”接近自相关，本身就是转录假说的推论。 |
| 新颖度 | 6.5 | 保留 KV 与重算 KV 的转录移植是标准因果拆分手段，在 steering 多轮持续这个对象上我没有检索到已有工作。GCAD 只给出间接论据，即提示控制和无 steering 基线不衰减，并没有重算 cache。推理模板剥离先前思考、由此导致跨轮衰减这一交叉，是有内容的新切口。判据部分新意较弱。 |
| 有效性 | 6.0 | 现有依据：2601.20834 显示回放他人写的脚本就能复现表示变化；2602.24287 显示自身回答会跨轮污染；2605.26772 撤除 steering 后，steer 下生成的 CoT 仍保留 48% 的效果（单轮，R1-Distill-Llama-8B）；2604.01202 表 1 中 Qwen3-4B 在 α=12 时思考模式翻转率 62%，非思考 29%（When2Call 单轮工具调用）。这些依据支持预测 (1) 的方向。迁移上的缺口有三。(a) 2605.26772 的主结论是 CoT 强化了拒答、抵消了 steering，可见 CoT 是放大还是对冲 steering 取决于特质，所以 (3) 中“第 1 轮效果更强”对价值或 persona 特质没有直接依据，交叉的符号和幅度都未知。(b) “保留先前思考”的模板对 Qwen3 和 R1-Distill 都偏离训练分布，即使出现“恢复”也可能来自分布外效应，而不是 CoT 份额。(c) 2601.20834 发现线性表示会随对话剧烈漂移，所以沿 v 的固定探针投影作为跨轮度量本身不稳定，判官评分只能部分弥补。 |

**与原问题的关系**：回答的是原问题中的“何时前缀足够”。“持续干预为何累积损伤或反转”仍未回答，只作为对照测量（D 臂），没有对 D 做 KV 与转录的隔离。

**实验能否判别主张**：对 (1)，A−B 的按脚本配对置换检验在“不显著”时并不能支持“几乎完全由转录承载”。这是一个等价主张，需要预先设定等价界和功效，否则零结果和功效不足无法区分。这是 Claim 阻断，但可以修复。此外，前缀 steering 被 steer 的只有 k=1–5 个位置，A−B 只能检验这一种 KV 扰动。把结论推广为“多轮中 steering 的跨轮持续”，本实验并不能判别。(2) 中冲突档是预先固定的脚本变量，这一点可以判别。(3) 的 2×2 交互可以测，但如上所述，存在模板分布外的竞争解释，而且第 1 轮效果强度在两种模式间没有对齐（同 α 下效果不同），衰减快慢需要按第 1 轮效果归一化后才可比。

**可行性：pass。** 前缀 steering 公开代码 github.com/xzAscC/Prefix 和 Assistant Axis 代码 github.com/safety-research/assistant-axis 都已核实存在（git ls-remote）。GCAD 代码已公开（github.com/NihiI-obstat/Gated-Cropped-Attention-Delta），用作参照不必只引数值。StTP 需按论文规范独立实现。转录移植只需要用无 hook 的新 prefill 重算，实现简单。Qwen3 与 R1-Distill 的默认模板确实会剥离历史思考，改成保留只需改模板。约 4.3 万轮、2–3 千万 token 的贪心生成，加本地判官，在 2×A100 上一至两天可以完成。但思考/非思考 × 剥离/保留会额外增加臂数，“约 6 个条件”可能低估，好在仍在预算内。脚本用 API 生成约 50 元，数据可以自行构造，没有外部数据缺口。

## 最高近邻
1. **One Token Can Be Enough: Prefix Steering**（https://arxiv.org/abs/2610.04967）：单轮或单阶段的前缀 steering，结论中明确留下“潜在状态还是生成 token 承载”与“何时前缀足够”这两个问题。差别：本工作把这两个问题放到多轮里，用 KV 重算做因果拆分。
2. **Prompt-Activation Duality / GCAD**（https://arxiv.org/abs/2605.10664）：多轮 10 回合、保留 KV、逐 token 注入，把退化归因于 KV-cache 污染。论据是间接的，没有重算 cache。差别：本工作做了隔离，但隔离的是前缀 steering，不是 GCAD 所说的持续注入。
3. **Model vs. User: Whose Values Prevail?**（https://arxiv.org/abs/2610.19817）：Qwen3-14B 和 Llama-3.1-8B/70B，模拟用户，CAA 与提示类方法，报告冲突下的衰减与反转。不区分 KV 与转录，不涉及思考模板。
4. **Linear representations … change dramatically over a conversation**（https://arxiv.org/abs/2601.20834）：回放他人脚本即可复现表示变化，steering 效果随对话位置而变。这直接支持“转录承载”，同时削弱固定探针度量的可靠性。
5. **Chain-of-Thought Disrupts Simple Steering of Refusal**（https://arxiv.org/abs/2605.26772）：steer 下重生成的 CoT 在撤除 steering 后保留 48% 的效果，但 CoT 总体上对冲拒答 steering。这是单轮的“文本承载”证据，同时提示交叉方向未必成立。

```json
{
  "score": 5.5,
  "contribution_scores": {"importance": 6.0, "novelty": 6.5, "effectiveness": 6.0},
  "contribution_assessment": "主贡献：用转录移植（重算KV）拆分多轮前缀steering跨轮持续的承载通路，并给出表达强度×冲突的判据与推理模板剥离思考的交叉预测。重要性6：回答2610.04967明确留下的机制问题，但对象限于前缀steering，结论方向与2601.20834/2602.24287/2605.26772一致，判据中冲突致衰减已由2610.19817报告。新颖度6.5：KV重算拆分在该对象上未见先例，思考模板交叉是新切口，但手段标准、判据新意弱。有效性6：(1)方向有邻近证据；(3)依赖CoT放大steering，而2605.26772显示CoT可对冲steering，2604.01202仅单任务，保留思考模板分布外；固定探针跨轮漂移。未达两项≥8。",
  "feasibility": "pass",
  "feasibility_reason": "Prefix、Assistant Axis、GCAD代码均公开可得，KV重算只需无hook重新prefill，Qwen3/R1模板剥离与保留可控；约4.3万轮贪心生成与本地判官在2×A100一至两天内可完成，脚本API成本约50元。",
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "贡献门槛未达：importance 6 / novelty 6.5 / effectiveness 6，无两项≥8；主结论(转录承载)与已有证据方向一致，成立后对领域判断改变有限",
    "Claim(1)是等价主张，仅用A−B置换检验不显著无法支持“几乎完全由转录承载”，缺等价界与功效设定",
    "主实验只隔离前缀steering(k=1–5个被steer位置)的KV份额，未隔离KV通路最可能起作用的全程注入(GCAD的KV污染假说)，无法支持推广到多轮steering一般的“跨轮持续由转录承载”"
  ],
  "novelty_conclusion": "未检索到对多轮steering做KV重算/转录移植拆分的已有工作，推理模板剥离思考导致跨轮衰减的交叉亦属新切口；但拆分手段标准，转录承载方向已被2601.20834、2602.24287、2605.26772间接支持，判据部分与2610.19817重叠，新意为可辨认的中等增量。",
  "closest_neighbors": [
    "One Token Can Be Enough: Bridging Prompting and Activation Steering with Prefix Steering (arXiv 2610.04967)",
    "Prompt-Activation Duality: Improving Activation Steering via Attention-Level Interventions (arXiv 2605.10664)",
    "Model vs. User: Whose Values Prevail? Inference-Time Value Alignment in Multi-Turn Conversations (arXiv 2610.19817)",
    "Linear representations in language models can change dramatically over a conversation (arXiv 2601.20834)",
    "Beyond a Single Direction: Chain-of-Thought Disrupts Simple Steering of Refusal (arXiv 2605.26772)"
  ]
}
```
