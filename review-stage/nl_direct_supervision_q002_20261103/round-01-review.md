## 结论
2026-11-03，总体 score 5.0，verdict：needs_rethink。

主贡献分两部分：一是机制归因，认为直接监督在 NL 上退化是"块内并行预测"遇上"NL 措辞多模态"；二是修法，用 CoT 教师的贪心重生成轨迹做序列级蒸馏。两部分都不够：
- 修法本身是 NAT 序列级蒸馏、以及 MTP 头用自生成数据训练的标准做法，搬到 latent CoT 上属于直接迁移。
- 机制归因按当前最小实验无法与竞争解释分开：模板化 NL 和重生成 NL 在降低措辞熵的同时，也降低了每个 latent 要承载的信息量，还提高了与 warm-start 教师的同分布程度。三种假说都预测这两种语料会恢复。

因此三项分数到不了"两项 ≥8"，主 Claim 也没有判别力。

## Claim 判断

| 维度 | 分数 | 依据 |
|---|---|---|
| 重要性 | 6.0 | NL 与 EQ 之间的保留率差距是真实、可复现的现象（C-MTP 表 4；KaVa 也报告了 EQ→NL 的退化），能说清"什么轨迹适合直接监督"有一定价值。但影响范围有限：(1) 只涉及 C-MTP、CoLaR 两种方法，以及 GSM8k-Aug-NL 这一个"半自然"数据集；C-MTP 作者自己指出，该数据集每句恰好对应一步算式。(2) 在真正冗长的 MATH 轨迹上，直接和间接监督都掉了约 65%，所以 GSM8k-NL 上的差距不是领域的主瓶颈。(3) 修法把 GPT-4 轨迹换成 1B 模型自己的措辞，"保留 NL"只在形式上成立。 |
| 新颖度 | 5.5 | 修法就是 Kim & Rush / Zhou et al. 2020 的序列级蒸馏；熵度量也沿用 Zhou et al.。MTP 头用自蒸馏或自生成数据训练也已是常规做法（MTP via Self-Distillation 2602.06019、FastMTP 2509.18362）。PIPO 已指出 CoLaR 的单峰假设不适合多模态的多 token 续写。新增部分只是"把这些放到 latent CoT 的 NL 退化问题上，并加一个长度×熵的对照"，属于可辨认但常规的迁移组合。 |
| 有效性 | 5.5 | **当前依据：** NAT 中序列级蒸馏降低条件熵、提升并行解码器，证据可靠；MTP 头用自生成数据会提升接受率，所以重生成数据"能提升 C-MTP 数字"有不错的迁移依据。**机制归因的依据弱：** (a) brief 用"s 增大时链长从 34 降到 17、损失反而增大"来反驳误差累积，这个推理不成立。s 增大时每个 latent 的预测难度同步上升，正确的比较是固定 s 下的 EQ 与 NL。在那个比较里，"NL 步数约为 EQ 的 2.5 倍，每步误差随 s 增大"同样预测 NL 损失随 s 扩大，所以现有表格不能区分多模态与误差累积。(b) CoLaR 的 NL 损失随 s 不增反降（22.9→15.7→14.2），直接与"收益随 s 增大"的跨方法判据相冲突，而最小实验只跑 CoLaR-2。**迁移条件：** NAT 的结论依赖"源端信息固定、只有措辞多模态"；这里模板化与重生成语料同时改变了每块的信息量、与教师的同分布程度和题目子集。**未知：** 重生成在训练题上的正确率与覆盖率；修法能否超出 word-level KD 或依赖式 MTP 头这类现成手段。 |

**与起点的关系：** 回答的是原问题（解释成因并修复），没有转向。即使修法有效，原问题中"为什么退化"这一半仍未回答，因为最小实验无法给出判别。

**实验能否判别主张：** 不能。
- **模板化 NL：** 用固定句式加填充补到等长后，每个 latent 的条件信息量接近 EQ。误差累积假说（填充步几乎无误差）和压缩压力假说（每 token 都容易表示）也都预测它会恢复。brief 把压缩压力假说写成"模板化 NL 也会伤害直接监督"，是对该假说的稻草人化。
- **重生成 NL：** 把三样东西混在一起：低熵、与 warm-start CoT 教师同分布（学生就是从该教师初始化的），以及只保留答对题目带来的题目子集偏移。计划里没有同子集的原 NL 对照，也没有"同来源但熵更高"的对照（例如同一教师按温度采样重生成），因此"恢复来自熵"无法与"恢复来自自蒸馏对齐或题目更容易"分开。
- **独立性差距与保留率的负相关：** 只有 4 种语料、2 个 s，是相关性证据。
- **竞争修法：** C-MTP 自带的 L_KD（来自 CoT 教师）与重生成的关系没有说明；块内依赖式 MTP 头（PIPO/Hydra 式条件化）是针对多模态最直接的模型侧修法，不在对照之列。

**可行性：pass。**
- 资源：C-MTP 代码公开，含 CODI；GSM8k-Aug 与 GSM8k-Aug-NL 在 HF（whynlp/gsm8k-aug、whynlp/gsm8k-aug-nl）可得；1B 模型用 vLLM 重生成约 38 万条只需数小时；模板化语料可由 EQ 确定性构造；不需要 API 或标注。
- 预算：约 32 个 LoRA run，在 8×A100 上 3–4 天，落在 5 天约束内，但余量不大。
- 种子与标签：2 个种子少于 C-MTP 的 5 次平均，s=2 上 5 个百分点量级的差异可能被种子波动淹没。标签与指标（GSM8k 准确率除以同语料 CoT-SFT）与主张一致，但分母本身随语料改变：在重生成数据上训练 CoT-SFT 等于自蒸馏，分母会变，这会影响保留率的可比性。

## 最高近邻
1. **C-MTP：Training Continuous Chain of Thought Models: A Tale of Two Regimes（2607.16972）** https://arxiv.org/abs/2607.16972
   - 重叠：同底座、同数据、同方法族，NL 退化现象本身来自这篇。
   - 差别：作者没有检验成因，也没有给修法；本方案的差别仅在归因与数据侧修法。原表数字本次未能直接打开核验。
2. **Zhou, Gu, Neubig. Understanding Knowledge Distillation in Non-autoregressive Machine Translation（ICLR 2020）** https://arxiv.org/abs/1911.02727
   - 重叠：修法（序列级蒸馏）、机制（降低条件熵以缓解并行解码多模态）和度量（条件熵、容量匹配）都来自这里。
   - 差别：只是把对象换成 latent CoT。
3. **Multi-Token Prediction via Self-Distillation（2602.06019）** https://arxiv.org/abs/2602.06019 ；**FastMTP（2509.18362）** https://arxiv.org/abs/2509.18362
   - 重叠：MTP 头用教师或自生成数据训练、对齐主模型分布，已是常规做法。
   - 差别：它们做的是推理加速，不是 latent CoT 的保留率。
4. **KaVa: Latent Reasoning via Compressed KV-Cache Distillation（2510.02312，ICLR 2026）** https://arxiv.org/abs/2510.02312
   - 重叠：同样针对 EQ→NL 的退化，同样在 Llama-3.2-1B 与 GSM8k-Aug-NL 上，并报告退化明显更小。
   - 差别：走的是间接监督，不保留并行训练；也没有解释成因。
5. **PIPO: Pair-In, Pair-Out: Latent Multi-Token Prediction（2605.27255）** https://arxiv.org/abs/2605.27255
   - 重叠：已指出 CoLaR 的单峰高斯不适合多模态的多 token 续写；它用条件化的 MTP 草稿头处理块内依赖。
   - 差别：做的是推理加速，没有研究 latent CoT 在 NL 上的退化。

```json
{
  "score": 5.0,
  "contribution_scores": {"importance": 6.0, "novelty": 5.5, "effectiveness": 5.5},
  "contribution_assessment": "主贡献 = 直接监督 latent CoT 在 NL 上退化的多模态归因 + 序列级蒸馏（教师贪心重生成）修法 + '目标条件熵而非长度'判据。重要性有限（两种方法、一个半自然数据集；MATH 上直接与间接监督同样崩溃）。新颖度低：修法与熵度量直接来自 NAT 序列级蒸馏（Zhou et al. 2020），自生成数据训练 MTP 头已常规，PIPO 已点出 CoLaR 的多模态问题。有效性：重生成数据提升 C-MTP 数字有 NAT 与 MTP 自蒸馏的迁移依据；但机制归因的现有依据推理有误（s 同时改变每步难度，链长缩短不能反驳误差累积），且 CoLaR 随 s 的非单调模式与跨方法判据冲突。待验证：重生成覆盖率、同子集与同来源高熵对照、与 word-level KD 及依赖式 MTP 头的关系。",
  "feasibility": "pass",
  "feasibility_reason": "C-MTP 公开代码（含 CODI）、HF 上的 gsm8k-aug/gsm8k-aug-nl、1B 模型 vLLM 重生成数小时、约 32 个 LoRA run 在 8×A100 上 3–4 天，均在用户约束内；风险在于 2 个种子对小差异的分辨力不足，以及重生成后 CoT-SFT 分母发生变化。",
  "verdict": "needs_rethink",
  "fatal_blockers": [
    "贡献不足：修法是 NAT 序列级蒸馏、MTP 自蒸馏数据的直接迁移，新颖度与重要性都远未达到 8，无法满足两项 ≥8 的门槛",
    "Claim 阻断：长度×熵 2×2 无法判别多模态与误差累积/压缩压力——模板化 NL（固定句式加填充）与重生成 NL 同时降低了每个 latent 的信息量，三种假说都预测恢复；brief 对压缩压力假说的预测是稻草人化",
    "Claim 阻断：重生成 NL 把低熵、与 warm-start 教师同分布、以及只保留答对题目的子集偏移混在一起，缺少同子集原 NL 对照和同来源高熵（采样重生成）对照，'恢复来自熵'不可判别",
    "现有依据推理有误：以 s 增大时链长 34→17 而损失增大来反驳误差累积不成立（s 同时提高每步难度）；CoLaR 的 NL 损失随 s 递减，与'收益随 s 增大'的跨方法判据冲突"
  ],
  "novelty_conclusion": "去掉 C-MTP 的名字后，剩下的是'把 NAT 序列级蒸馏与条件熵分析应用到 latent CoT 直接监督'，属常规迁移组合；多模态归因在 latent CoT 语境下有一定新意，但已有 PIPO 点出相近问题，且当前实验无法确立该归因。",
  "closest_neighbors": [
    "Training Continuous Chain of Thought Models: A Tale of Two Regimes (arXiv 2607.16972)",
    "Understanding Knowledge Distillation in Non-autoregressive Machine Translation (Zhou et al., ICLR 2020, arXiv 1911.02727)",
    "Multi-Token Prediction via Self-Distillation (arXiv 2602.06019) / FastMTP (arXiv 2509.18362)",
    "KaVa: Latent Reasoning via Compressed KV-Cache Distillation (arXiv 2510.02312)",
    "Pair-In, Pair-Out: Latent Multi-Token Prediction for Efficient LLMs (arXiv 2605.27255)"
  ]
}
```
