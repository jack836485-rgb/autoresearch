## 结论
日期 2026-10-22。score 5.0/10，verdict：promising_needs_revision。可以继续，但新颖性边界没有解决，还不能进入实验规划。

- **核心动作已有先例。** "按训练域泄漏和广泛失配拆开计数"在近邻里已经有做法：Turner 等用 semantic judge 衡量回答里的训练域内容；Dubiński 等用 Is-code、Is-recipe judge 先剔除窄任务回答，再计失配；ContextLift 附录 A 的 Table 4 按 broad 与 ambiguous/domain 拆开三个臂的 cued 失配，还逐条读了 ContextLift 臂的残余回答：74–90% 在回应 cue 句子，除 3、2、8 条外都含领域词汇。因此 brief 的起点"现有指标把两者合并计数"说过头了，是一个 claim blocker。
- **真正空白的部分。** 在回答层面，对通用交织臂和事后良性微调臂做定量分解；检验分解后各缓解方法的排名是否改变。这是一个有用但增量的评测分析，更像 ContextLift 附录 A 的系统化延伸。
- **Claim 2 的检验设计有混杂，而且可能做不成。**
  - 唯一的隐蔽诱导器同时换了模型（7B 换成 Qwen3-32B）和触发方式（cue 句子换成代码格式）。"诱导器类型决定比例"和模型、触发方式无法分开。
  - insecure code 的窄行为在自由问答里本来就几乎无法表达。代码臂"以广泛分量为主"接近定义性结论，而且 Dubiński 已经做了剔除代码回答之后再计失配。
  - 这个 organism 在 Qwen2.5-7B 上无效（ContextLift 附录 B）。Dubiński 的混合数据结果是在 GPT-4o 上得到的。2605.12199 报告 EM 在开源模型上远非普遍。目前没有证据表明稀释后的 insecure code 在 Qwen3-32B 4-bit LoRA 上会产生条件失配。如果是零结果，Claim 2 就无法检验。

## Claim 判断
| Claim | 判断 | 关键依据 |
|---|---|---|
| 1. 缓解后的 cued 失配 = 窄任务泄漏 + 广泛条件失配，现有指标把两者合并 | 大部分已被覆盖 | Turner 等的 semantic judge 测量训练域泄漏；Dubiński 用 Is-code/Is-recipe judge 剔除窄任务回答；ContextLift 的 Table 4 做了按 prompt 的 broad/domain 拆分，并对残余回答做了定量阅读。仍然空白的只有：在回答层面、对通用交织臂和事后微调臂做分解 |
| 2. 分解比例由诱导器类型决定（建议类以泄漏为主，代码类以广泛为主），可以解释两组观察的分歧 | 部分重合，检验有混杂 | 代码这一半是 Dubiński 在剔除代码回答后已经给出的结论。所谓"分歧"也可以用缓解臂不同来解释：ContextLift 只读了自己那一臂；在通用交织臂上，broad prompt 的失配仍有 17/36/52%。诱导器类型与模型、触发方式完全混杂，隐蔽诱导器只有一种，而且可能是零结果 |
| 3. 条件失配率不能跨诱导器比较；按广泛分量排序会改变缓解方法排名 | 较新，但增量 | 没找到有人做过跨缓解方法的分解后排名。不过 ContextLift 在 broad 子集上对通用交织的优势已经很大，所以排名翻转主要只能指望事后良性微调臂 |

## 最高近邻
1. ContextLift（2610.21633）https://arxiv.org/abs/2610.21633 。重叠：同一管线、同样三个建议类数据集；附录 A 的 Table 4 按 prompt 类拆分 cued 失配，并对残余回答做了定量阅读；仓库里有 `classify_cued_prompts.py`。差别：没有做回答层面的双轴判定，没有分析事后微调臂，也没有跨诱导器比较。
2. Conditional misalignment（2604.25891）https://arxiv.org/abs/2604.25891 。重叠：提出条件失配，明确说触发后是"广泛而非窄域"的失配，并用 Is-code/Is-recipe judge 剔除窄任务回答。差别：只剔除不分解，也没有跨缓解方法量化泄漏比例。
3. Model Organisms for Emergent Misalignment（2506.11613）https://arxiv.org/abs/2506.11613 。重叠：用 medical/finance/sport/code semantic judge 衡量回答里的训练域内容，用来区分窄域与"emergent"。差别：只针对未缓解、无 cue 的模型。
4. Emergent Misalignment is Easy, Narrow Misalignment is Hard（2602.07852）https://arxiv.org/abs/2602.07852 。重叠：区分窄解与广解。差别：在表示层面、针对未缓解模型，不涉及 cued 评测。
5. Overtrained, Not Misaligned（2605.12199）https://arxiv.org/abs/2605.12199 。重叠：说明 EM 在开源模型上远非普遍，与规模相关。差别：不是方法近邻，但直接关系到 Qwen3-32B insecure code 臂能不能做成。

```json
{
  "score": 5.0,
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "claim: the premise that existing conditional-misalignment metrics merge narrow leakage and broad misalignment is overstated - Dubinski et al. already exclude on-task code/recipe answers, ContextLift Table 4 already splits cued misalignment by broad vs domain prompts across arms and quantifies residual cue-answering, Turner et al. already use semantic domain judges",
    "feasibility/claim: Claim 2 rests on a single covert inducer that is confounded with model size (7B vs Qwen3-32B) and trigger type (cue sentence vs code format), whose narrow behavior is near-definitionally inexpressible in free-form QA, and for which there is no evidence that diluted insecure code yields conditional misalignment on Qwen3-32B 4-bit LoRA (null on Qwen2.5-7B per ContextLift; original result on GPT-4o)"
  ],
  "novelty_conclusion": "Decomposing cued misalignment into narrow-task leakage vs broad misalignment is largely anticipated by ContextLift Appendix A, Dubinski et al. task-exclusion judges, and Turner et al. semantic judges; the remaining novelty is a response-level cross-mitigation (generic interleaving, post-hoc benign FT) decomposition and ranking-change test, which is incremental, while the inducer-type claim is confounded and its covert arm may be null.",
  "closest_neighbors": [
    "ContextLift: Breaking the Spurious Correlation Behind Conditional Emergent Misalignment (2610.21633)",
    "Conditional misalignment: common interventions can hide emergent misalignment behind contextual triggers (2604.25891)",
    "Model Organisms for Emergent Misalignment (2506.11613)",
    "Emergent Misalignment is Easy, Narrow Misalignment is Hard (2602.07852)",
    "Overtrained, Not Misaligned (2605.12199)"
  ]
}
```
