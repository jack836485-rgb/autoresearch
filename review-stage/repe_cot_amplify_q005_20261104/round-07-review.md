## 结论
日期 2026-11-04，总体 score 5.0，verdict：needs_rethink。主贡献是：在推理模型里沿调用/不调用方向做短暂推动，用决定是否容易被推翻来做逐题的 no-call 检测和弃权规则。这个贡献不够。原因有三。第一，按 brief 自己的定义，两侧推动会退化为“基线决定能否被反向推翻”，也就是一种方向性的决策间隔／扰动鲁棒性读数。第二，brief 主打的场景（稳定、惯性的过度调用）恰恰是这个探针在机制上会放过的情形。第三，没有任何证据把可推动度和金标准 no-call 联系起来。

## Claim 判断
| 维度 | 分数 | 依据 |
|---|---|---|
| 重要性 | 6 | 工具过度调用是真实、可度量的瓶颈：AMCS 在 When2Call 上报告 no-call 准确率经纠偏可提升 4–17 个点。不需训练的逐题检测器有实用价值，但它只是又一个弃权置信信号，影响范围有限。 |
| 新颖度 | 5.5 | 设 p₊=1[正推后调用]、p₋=1[负推后不调用]。基线已调用的题，正推几乎必然仍调用，所以 p₊≈1、U≈p₋；基线不调用的题同理 U≈p₊。“都低”需要推向哪边就反向翻转，几乎不会出现。因此规则实际是：“基线是调用且被负推推翻 → 不调用，否则沿用基线”。这是用方向性激活扰动下的翻转度当作置信度，和随机激活噪声下的一致性（2502.03799）、提示施压下的翻转（2603.03330）同属一族。翻转与抵抗现象本身也已在 2604.01202 中、同一任务和同类模型上报告过。新意只在“方向和弃权动作对齐、只推前 k 个 token”，属于可辨认的增量。 |
| 有效性 | 4.5 | 现有依据：2604.01202 在 Qwen3-4B 和 GLM-Z1-9B 上（每方向 n=100，全 token 注入）显示翻转率 7–79%，翻转的 CoT 常被判为编造支持或越过约束。但该文没有按金标准类别、也没有按基线对错拆分翻转，只是定性地把抵抗和 probe 置信度联系起来。2603.22161 证明置信方向能因果地移动弃权，说明推得动，但不说明推得动的题更可能是 no-call。迁移上缺两环。(1) AMCS 把过度调用诊断为跨题共有的内在偏移，偏移越大的惯性调用越能抵抗负推，于是会被保留为调用，这和 brief 的核心卖点相反，除非加大 α，而那会让金标准 call 也被翻掉。(2) 翻转度很可能主要由 pre_gen 间隔决定（probe 对模型自身决定的 AUROC>0.9），“推理带来超出间隔的证据敏感性”这一关键假设目前没有直接或邻近证据。此外，只在 prefill 和前 k 个 token 推动后撤除能否仍有足够翻转率也未知，已有翻转数据都来自全程注入。 |

与起点的关系：这是一个邻近新问题，把“推理为被推动的决定找理由”反过来当作检测工具。转向本身不构成阻断。起点中剂量、文本正反馈与预先确定三者的分离仍未回答。

实验能否判别：对照设计基本覆盖了竞争解释，包括采样一致性、pre_gen 间隔、5 个范数匹配的随机方向、AMCS 和非思考模式。判断 (a) 可以被推翻。不足有三处。(1) 缺少用金标准 no-call 监督训练的线性方向／探针（如 2509.22449 的 unanswerability direction；When2Call 还提供 train_pref 数据）。这是逐题检测的强基线。现在的“pre_gen 探针间隔”如果只拟合模型自身决定，就测不出两者的差别。(2) 关键判别应在“基线已调用”的子集内，比较可推动度在控制 pre_gen 间隔后是否仍区分金标准 call 与 no-call。否则 (a) 即使成立，也可能只是间隔的昂贵复读。(3) 第三次生成里，顺着基线方向的那次推动在信息上近乎冗余，同预算公平性需要重新说明。还有一处细节：HF 数据卡显示 When2Call 的 correct_answer 只有 3 个取值，brief 列了 4 类，需核对；AMCS 用的是生成加 LLM judge 的评测，二元调用与否可以直接解析，但 AMCS 的数字不能直接搬过来比。

可行性：pass。AMCS 的官方代码与 Qwen3.5-4B/9B 的 SAE 权重已公开（github.com/SKURA502/agent-sae，含 When2Call 评测脚本）。diff-in-means 方向和 HF hook 实现简单。When2Call mcq（3,652 题）和 BFCL v3 公开可得，金标准由数据集给出。约 6 万条生成、约 1 亿 token，在 8×A100 上 5 天内宽裕。提示式不确定性分解（2606.19559）有公开代码与附录提示，但原文在 WebShop/ALFWorld 上，迁移到 When2Call 属于独立实现。

## 最高近邻
1. Therefore I am. I Think（arXiv 2604.01202, https://arxiv.org/abs/2604.01202）：同任务（When2Call/BFCL），同样用 pre_gen 决策方向做 steering，报告了翻转与抵抗、CoT 合理化和思考／非思考差异。差别：它不把翻转度当检测器，没有按金标准拆分，且是全 token 注入。
2. To Call or Not to Call: Diagnosing Intrinsic Over-Calling Bias in LLM Agents（arXiv 2605.18882, https://arxiv.org/html/2605.18882v1）：同模型 Qwen3.5-4B/9B，沿 SAE 方向做常数闭式纠偏，no-call 准确率提升 4–17 个点；不测 BFCL，未说明是否用思考模式。差别：没有逐题判断。
3. Enhancing Hallucination Detection through Noise Injection（arXiv 2502.03799, https://arxiv.org/abs/2502.03799）：扰动中间激活后看答案一致性来估计不确定性。差别：它用随机扰动，不是决策方向推动，也不针对推理模型或工具调用。
4. Detecting (Un)answerability in LLMs with Linear Directions（arXiv 2509.22449, https://arxiv.org/abs/2509.22449）：用金标准监督的 diff-in-means 方向做逐题不可回答检测，并能因果控制弃权。差别：任务是抽取式 QA，不是工具调用；它是本方案缺失的强基线类型。
5. Certainty Robustness: Evaluating LLM Stability Under Self-Challenging Prompts（arXiv 2603.03330, https://arxiv.org/abs/2603.03330）：用施压后答案是否翻转来衡量置信可靠性。差别：它在提示层面施压、用于评测而非决策，任务也不是工具调用。

```json
{
  "score": 5.0,
  "contribution_scores": {"importance": 6.0, "novelty": 5.5, "effectiveness": 4.5},
  "contribution_assessment": "主贡献是推理模型中用决策方向短暂推动后的可推翻度做逐题 no-call 检测与弃权。重要性 6：过度调用是真实瓶颈，但这只是又一个置信信号。新颖度 5.5：按定义两侧推动退化为基线决定的单侧可翻转度（顺基线方向的推动几乎必然维持原决定），属方向性扰动置信度，和激活噪声一致性、施压翻转同族，翻转与抵抗现象已见于 2604.01202。有效性 4.5：没有证据把可推动度和金标准 no-call 联系起来（2604.01202 未按金标准拆分，且是全 token 注入）；AMCS 的偏移诊断意味着惯性过度调用会抵抗负推而被保留，与核心卖点相反；可推动度大概率由 pre_gen 间隔决定；只推前 k 个 token 能否产生足够翻转未知。",
  "feasibility": "pass",
  "feasibility_reason": "AMCS 官方代码和 Qwen3.5-4B/9B 的 SAE 已公开，When2Call（3652 题）与 BFCL v3 公开且金标准现成，HF hook steering 实现简单；约 6 万条生成、约 1e8 token，在 8×A100、5 天内可完成。",
  "verdict": "needs_rethink",
  "fatal_blockers": [
    "贡献不足：三项分数 6/5.5/4.5，没有一项达到 8，未过三维门槛",
    "Claim 阻断：两侧可推动度按定义退化为基线决定的单侧可翻转度，核心是方向性的决策间隔／鲁棒性读数，和 pre_gen 间隔、激活扰动一致性难以区分",
    "Claim 阻断：主打的“稳定惯性过度调用”在机制上会抵抗负推而被保留为调用，与 AMCS 的跨题偏移诊断一致，卖点没有机制支持",
    "基线缺失：没有用金标准 no-call 监督的线性方向／探针（unanswerability direction 类），也没有在基线已调用子集内控制 pre_gen 间隔的判别分析"
  ],
  "novelty_conclusion": "没有被某一篇工作直接覆盖，但这是把方向性激活扰动下的翻转度当作弃权置信度的增量组合。翻转与抵抗现象在同任务上已有报告（2604.01202），扰动一致性做不确定性估计也已有先例（2502.03799）。两侧设计按定义退化为单侧，实质新意有限。",
  "closest_neighbors": [
    "Therefore I am. I Think (arXiv 2604.01202)",
    "To Call or Not to Call: Diagnosing Intrinsic Over-Calling Bias in LLM Agents (arXiv 2605.18882)",
    "Enhancing Hallucination Detection through Noise Injection (arXiv 2502.03799)",
    "Detecting (Un)answerability in Large Language Models with Linear Directions (arXiv 2509.22449)",
    "Certainty Robustness: Evaluating LLM Stability Under Self-Challenging Prompts (arXiv 2603.03330)"
  ]
}
```
