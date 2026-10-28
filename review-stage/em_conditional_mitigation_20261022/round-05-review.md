## 结论
截至 2026-10-22：**score 4.0 / 10，verdict = needs_rethink**，不值得按当前形式进入实验规划。

- 新颖性：Claim 1 部分重合。"窄任务泄漏 vs 广泛失配"这一区分已有人提出，工具也已公开：ContextLift 明确写了"bad domain advice is the narrow behavior and not broad misalignment"，按 broad 和 domain 两类给 cued prompt 分类并按臂报告；仓库中的 `scripts/residual_cued.py` 接受任意 arm 参数，能统计"含领域词汇"和"回应 cue 自身话题"的条数。Turner et al. 早就用语义 judge 检查失配回答是否只是领域泄漏。本 Idea 真正新增的只有两点：用 LLM judge 替代关键词并做人工校准，以及扩展到所有臂和更多诱导器。这是对现有分析的增量补全。
- 致命可行性问题：Claim 2 依赖"隐蔽诱导器 = Qwen3-32B 上的 insecure code"。已有文献直接报告 insecure code 在 Qwen3-32B 上不产生失配（Chua et al. 2025），开源模型只有 >200B 时才稳定出现 EM（2605.12199）；ContextLift 和 Dubiński 的代码 organism 在 Qwen2.5-7B 上也都无效。缓解后的 cued 残余很可能接近 0，分解无从谈起。
- 致命 Claim 问题：诱导器类型与基座模型（7B vs 32B）、训练配置、触发形式（只有代码臂用代码格式触发）完全混杂，而且隐蔽类只有一个实例。另外，Dubiński 的评测流程会过滤含代码的输出，"代码类以广泛分量为主"有一部分是这一过滤造成的。因此"诱导器类型决定比例"在这个设计下无法被检验。
- 最小实验没有把双轴 judge 与 ContextLift 已有的 prompt 分类和关键词残余统计做对比，所以无法说明本方法与最高近邻在同等预算下的结论有什么不同。

## Claim 判断
| Claim | 判断 | 最关键依据 |
|---|---|---|
| 1. cued 失配 = 泄漏 + 广泛，现有指标把两者合并 | 部分重合 | ContextLift 附录 A 已按 broad/domain 拆分 prompt 并逐臂报告（generic 在 broad prompt 上为 17.0/35.9/52.4%），也读过本臂残余：74/89/90% 的残余在回答 cue 句，只有 3/2/8 条不含领域词汇。`residual_cued.py` 可直接对任意臂运行。Turner et al. 2506.11613 有领域语义 judge。新增部分只有答案级 LLM 双轴判定、人工 κ 校准，以及跨臂报告。 |
| 2. 比例由诱导器类型决定（建议类以泄漏为主，代码类以广泛为主），可以解释两组观察的分歧 | 作为假设是新的，但当前实验无法检验 | (a) insecure code 在 Qwen3-32B 上是 null organism（2506.13206："shows no misalignment on Qwen3-32B"；2605.12199：稳定 EM 只出现在 >200B 模型）；(b) 诱导器与模型、配置、触发形式混杂，隐蔽类 n=1；(c) Dubiński 的"conditional behaviour is not itself narrow"同样基于建议类 organism（毒鱼食谱、bad security advice），分歧同样可以用 cue 形式（第一人称情境句 vs 格式或嵌入式触发）来解释，设计没有排除这一点。 |
| 3. 按广泛分量重排后，至少一类诱导器上的缓解排名会改变 | 部分新，但证据力弱 | 4 类诱导器中"至少一类"成立即算通过，判据过宽，也没有多重比较控制。ContextLift 在 broad prompt 子集上的排名（generic ≫ ContextLift）已经与合并排名一致，排名真正可能变化的只剩事后良性微调这一臂。 |

## 最高近邻
1. **ContextLift**（Mai & Kaczér, 2026）https://arxiv.org/abs/2610.21633 ，代码 https://github.com/davidkaczer/contextlift （`scripts/residual_cued.py`、`classify_cued_prompts.py`）。重叠：同一管线、同一组诱导器和 cue，已提出泄漏与广泛的区分并做了 prompt 级和残余级统计。差别：论文只报告了 ContextLift 一个臂的残余，用的是关键词启发式，没有人工校准，也没有事后良性微调臂和隐蔽诱导器。
2. **Conditional misalignment**（Dubiński et al., 2026）https://arxiv.org/abs/2604.25891 。重叠：定义了条件失配，覆盖稀释、事后 HHH 微调和接种提示，并明确断言触发后的行为"not itself narrow"。差别：没有在答案级别对泄漏和广泛做定量分解。
3. **Model Organisms for Emergent Misalignment**（Turner et al., 2025）https://arxiv.org/abs/2506.11613 。重叠：用医疗、金融、运动、代码四个语义 judge 检验失配回答是否只是训练领域的泄漏（例如运动臂中 90% 的失配回答与运动无关）。差别：针对的是未缓解、无 cue 的模型。
4. **Emergent Misalignment is Easy, Narrow Misalignment is Hard**（Soligo et al., 2026）https://arxiv.org/abs/2602.07852 。重叠：区分窄解与广解，并给出两者的表征。差别：研究的是未缓解模型的训练归纳偏置，不涉及 cue 或缓解后的残余。
5. **Thought Crime**（Chua et al., 2025）https://arxiv.org/abs/2506.13206 ，以及 **Overtrained, Not Misaligned** https://arxiv.org/abs/2605.12199 。这两篇与本 Idea 的新颖性不重叠，列出是作为可行性反证：insecure code 在 Qwen3-32B 和 Qwen3-30B 上没有产生 EM，直接影响隐蔽诱导器臂能否成立。

```json
{
  "score": 4.0,
  "verdict": "needs_rethink",
  "fatal_blockers": [
    "feasibility: covert inducer (insecure code on Qwen3-32B) has published null-EM evidence (2506.13206; 2605.12199), and the code organism is also null on Qwen2.5-7B (ContextLift, Dubinski); post-mitigation cued residual likely ~0, so Claim 2 cannot be tested",
    "claim: inducer type is confounded with base model (7B vs 32B), training config, and trigger type (code-format triggers only on code arm), with only one covert inducer; Dubinski-style is-code filtering removes code leakage, so 'code -> broad' is partly built in by construction",
    "novelty: Claim 1's leakage-vs-broad distinction and a per-arm tool (ContextLift Appendix A, scripts/residual_cued.py, prompt-class split) already exist, plus Turner et al. semantic-topic judges; the minimal experiment does not compare the two-axis judge against these existing decompositions, so it cannot distinguish itself from the closest work"
  ],
  "novelty_conclusion": "Claim 1 partially covered by ContextLift (concept, prompt-class split, residual keyword tool usable on any arm) and Turner et al. semantic judges; the new part is a calibrated cross-arm, cross-inducer extension. Claim 2 is a new hypothesis, but the planned experiment cannot test it because of a null covert organism and confounds. Claim 3 is weak. Overall an incremental extension of ContextLift's residual analysis.",
  "closest_neighbors": [
    "ContextLift: Breaking the Spurious Correlation Behind Conditional Emergent Misalignment (arXiv 2610.21633)",
    "Conditional misalignment: common interventions can hide emergent misalignment behind contextual triggers (arXiv 2604.25891)",
    "Model Organisms for Emergent Misalignment (arXiv 2506.11613)",
    "Emergent Misalignment is Easy, Narrow Misalignment is Hard (arXiv 2602.07852)",
    "Thought Crime: Backdoors and Emergent Misalignment in Reasoning Models (arXiv 2506.13206)"
  ]
}
```
