## 结论
2026-11-04，总体 score 5.5，verdict：promising_needs_revision。主贡献是一个现象主张：在推理模型中，剂量固定的激活种子撤除后，后续推理在欠定决定上放大它，在由证据决定、依赖 CoT 计算的题上衰减它。这个问题分得清楚，可以做，但目前不够通过。其一，预测的符号模式与已有文本注入、谄媚和 CoT 扰动研究的结论（主观任务更易被带偏，客观任务能回溯）高度一致，确认后改变的判断有限。其二，按任务划分的 D 和 B=0 处的截断读数，都能在不涉及“推理纠错”的情况下产生同样的斜率交互，现有设计还排除不了这些解释。

## Claim 判断
| 维度 | 分数 | 依据 |
|---|---|---|
| 重要性 | 6.0 | 把“思考更易被 steer”（2604.01202：When2Call 注入翻转 62% vs 29%，但 steering 也拉长了推理）拆成剂量和推理两个因素，对在推理模型上做 steering 的人有直接用处，价值明确。范围有限：(a) 安全动机中“后训练偏置被长推理放大”是持续性偏置，而本设计是撤除后的短种子，两者不对应，外推需要额外论证；(b) 若结果成立，结论是“欠定处放大、确定处纠错”，这与已有直觉和邻近结果相符，很难明显改变领域的重要判断。 |
| 新颖度 | 6.0 | 把推理长度作为自变量、用激活种子固定剂量、拆分 KV 与文本份额，这个组合目前查不到有人做过，是可辨认的增量。但各部件都已有人研究：2610.04967 已提出 Prefix Steering（k 个 token、在最终 prompt 位置起作用），并报告在 Qwen3/OLMo 3 上效果能延续到推理之后；2605.06672 发现偏置随推理长度增大；2602.07470 和 2601.23163 发现客观任务上能从 CoT 扰动中恢复；2603.16643 发现主观任务更易谄媚；2605.26772 给出了文本与激活份额的雏形（48% vs 94%）。“符号取决于证据决定性”是把这些已有结论迁移到激活种子上，机制层面没有提出新的解释。 |
| 有效性 | 5.5 | 当前依据：放大一端有自然偏置随长度增大（2605.06672，截断续写 16%→32%）和文本注入后沿错误思路续写（2506.10979、2510.06410）；纠错一端有客观任务上的回溯和恢复（2601.23163、2602.07470）；短期激活扰动能写进文本（2605.26772，48%）。这些都来自文本扰动或自然偏置，迁移到激活种子的关键条件（k≤64 的种子能否在 Qwen3-8B 思考模式下留下可测的决定偏移）没有直接证据。2603.01437 用全程 steering 在推理模型上就已经“little success”，k=4/16 的种子很可能处处 G≈0，读出来会像是在支持“剂量”或“预先确定”。判别力有三处缺口：(1) D 只在任务层级变化（逻辑推演 vs 规范判断 vs 工具调用），斜率交互与任务格式、方向质量、基线 steering 效力完全混在一起，连续的无 CoT 置信度协变量只能部分缓解，缺少同一题内对 D 的操纵；(2) B=0 的强制作答紧接被 steer 的位置，保留 KV 的支路在 B=0 处含有方向对答案 token 的直接作用。逻辑推演在早期截断时的作答接近均匀分布，后期由 CoT 计算主导，所以即便推理没有“纠正”任何东西，G 的下降也会自然出现；随机方向种子只控制了范数，没有控制方向特异的直接读出；(3) When2Call 中 request_for_info 对应缺少必填参数，证据其实决定了答案（应当追问），把它标为“欠定”与 D 的定义矛盾。 |

与起点的关系：这是原问题“放大由剂量、文本正反馈还是预先确定决定”的核心分支。原问题中“已写 CoT 的锁定”一支和 MoE 反例没有回答，这次转向本身不构成阻断。

实验能否判别主张：部分能。“斜率处处≈0”和“与 k 有关而与 B 无关”这两种情况可以识别。但“欠定处为正、确定处为负”的交互，在当前设计下还不能和“任务差异”及“短 B 处直接读出污染”区分开（见有效性 (1)(2)）；When2Call 的 D 标签含义也不成立。

可行性：pass。模型（Qwen3-8B、R1-Distill-Llama-8B）、数据（BBH、Social Chemistry 按 2603.01437 格式；nvidia/When2Call test mcq 3652 条，CC-BY-4.0，有 correct_answer 字段）、hook 实现（2605.26772 官方代码）和截断协议（2606.13603 官方代码）都能拿到；Prefix Steering 在 2610.04967 中有明确定义（t=0 为最终输入 token，前 k 个位置加系数），可以独立实现。约 2 万条续写、约 2000 万 token，在 8×A100 上 1–2 天，在用户约束之内。主要风险在效果量（种子太弱），不在实现。

## 最高近邻
- 2610.04967 One Token Can Be Enough: Prefix Steering（https://arxiv.org/abs/2610.04967）：短窗口 steering 的效果能延续到推理后的最终作答，所用模型为 Qwen3/OLMo 3。差别：没有把推理长度作为自变量，没有问推理是放大还是抵消，也没有拆分 KV 与文本。
- 2604.01202 Therefore I am. I Think（https://arxiv.org/abs/2604.01202）：思考模式比不思考更易被 steer，steering 拉长推理。差别：prefill+decode 全程 steer，剂量与长度同时变化，没有随机方向对照。
- 2605.26772 Beyond a Single Direction: CoT Disrupts Simple Steering of Refusal（https://arxiv.org/abs/2605.26772）：steer 下重新生成的 CoT 在撤除 steering 后仍保留 48% 的拒答逆转。差别：全位置 steer，只看拒答一项，不扫推理长度，也没有随机方向对照。
- 2605.06672 More Thinking, More Bias（https://arxiv.org/abs/2605.06672）：位置偏置随推理轨迹长度增大，截断续写给出因果证据。差别：研究对象是自然偏置，不是可控的激活种子。
- 2602.07470 Are Reasoning LLMs Robust to Interventions on their CoT?（https://arxiv.org/abs/2602.07470）：推理模型通常能从 CoT 扰动中恢复，早期扰动更难恢复，doubt 是恢复机制。差别：扰动在文本层，只用客观任务，没有欠定决定。

```json
{
  "score": 5.5,
  "contribution_scores": {"importance": 6.0, "novelty": 6.0, "effectiveness": 5.5},
  "contribution_assessment": "主贡献是现象主张：剂量固定的激活种子撤除后，后续推理在欠定决定上放大、在由证据决定且依赖CoT的题上衰减，并给出KV与文本份额。重要性6：能拆开‘思考更易被steer’的剂量混淆，但预测与2603.16643/2602.07470/2605.06672等已有结论一致，安全外推（持续性后训练偏置）与短种子设计不对应。新颖度6：推理长度为自变量加剂量固定激活种子的组合未见先例，但Prefix Steering（2610.04967）及其跨推理延续、偏置随长度增长、文本扰动恢复都已有人报告，符号依赖D是已有结论的迁移。有效性5.5：支撑全部来自文本注入和自然偏置，激活种子的迁移未证实；2603.01437在推理模型上全程steering已很难生效，k≤64的种子可能处处无效；D只在任务层面变化，与任务、方向质量混淆；B=0强制作答含方向对答案token的直接读出，逻辑题早期截断接近均匀分布，会在没有纠错的情况下产生负斜率；When2Call的request_for_info实为证据决定，标为欠定不成立。",
  "feasibility": "pass",
  "feasibility_reason": "模型、BBH/Social Chemistry/When2Call（CC-BY-4.0，含correct_answer）可得；hook代码（kiajueng/cot_ref_harm_analysis）与截断代码（DanielSc4/Commitment-Boundary）公开；Prefix Steering在2610.04967中定义明确；约2000万token前向，8×A100一两天可完成，在约束之内。风险在效果量，不在实现。",
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "贡献不足：重要性与新颖度都只有约6，没有一项达到8；所预测的‘欠定放大/确定纠错’与已有文本扰动、谄媚和长度偏置结论一致，确认后改变的判断有限",
    "Claim判别：D只在任务层级变化，B×D交互与任务格式、方向质量、基线steering效力混淆，缺少题内对证据决定性的操纵",
    "Claim判别：B=0截断读数紧接被steer位置，含方向对答案token的直接作用，逻辑题早期作答接近均匀分布，可在没有推理纠错时产生负斜率；随机方向种子只控制范数，控制不了这一点",
    "标签含义：When2Call的request_for_info对应缺少必填参数，证据决定了答案，标为欠定与D的定义矛盾"
  ],
  "novelty_conclusion": "以推理长度为自变量、剂量固定的激活种子加KV/文本拆分，这一组合未查到先例，属可辨认增量；但Prefix Steering及其跨推理延续（2610.04967）、偏置随推理长度增长（2605.06672）、客观任务上从CoT扰动恢复（2602.07470、2601.23163）、steer后CoT携带部分效果（2605.26772）都已有人报告，核心符号预测是已有结论向激活层的迁移，新意不足8。",
  "closest_neighbors": [
    "One Token Can Be Enough: Bridging Prompting and Activation Steering with Prefix Steering (arXiv 2610.04967)",
    "Therefore I am. I Think (arXiv 2604.01202)",
    "Beyond a Single Direction: Chain-of-Thought Disrupts Simple Steering of Refusal (arXiv 2605.26772)",
    "More Thinking, More Bias: Length-Driven Position Bias in Reasoning Models (arXiv 2605.06672)",
    "Are Reasoning LLMs Robust to Interventions on their Chain-of-Thought? (arXiv 2602.07470)"
  ]
}
```
