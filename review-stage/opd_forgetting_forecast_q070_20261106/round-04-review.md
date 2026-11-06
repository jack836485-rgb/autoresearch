## 结论
2026-11-06，总体 score 6.2，verdict：promising_needs_revision。主贡献是把同源教师有符号继承、来源门控和 MOPD 跷跷板这三个已知的定性现象，写成一条训练前可算、逐题可检验的线性规律 Δℓ_i ≈ a_t + α_task + κ(o_t)·G_{t,i}。按现有设计，这个贡献还不够通过门槛，原因有三。第一，H1 在很大程度上由已知事实推出：同源 OPD 会关闭 OOD 预测差距，因此逐题对数优势向教师移动。第二，门控和叠加只是把已有的定性结论定量化，三项都达不到 8 分。第三，H3 的判别设计无法区分核心对手：留出教师内的 Spearman 对 κ(o_t)·G 与对称 G 给出相同秩次。起点问题的主体（跨教师的遗忘差异）则被放进了未解释的 a_t。

## Claim 判断
| 维度 | 分数 | 依据 |
|---|---|---|
| 重要性 | 6.5 | 若成立，可以在训练前逐题判断某教师会让学生丢哪些 OOD 能力，并免去 MOPD 混合比例的网格试跑，有实用价值。但起点问题关心的是跨教师来源的遗忘差异，而 brief 自己把跨源遗忘归为“与能力无关的扰动 a_t”。a_t 只靠 10 个教师上的教师级对照①去解释（跨源约 4–6 个），实际上是一个残差桶。规律主要解释的是同源教师下各题之间的重新分配，不是总遗忘量的教师间差异。 |
| 新颖度 | 6.5 | 经检索，没有发现“逐题、有符号、来源门控”的 OPD 遗忘预测，也没有 MOPD 混合比例的定量叠加预测，可辨认的增量是存在的。但近邻很近：2608.16647 已给出同源向教师水平靠拢、跨源只拟合训练分布、份额单调跷跷板，以及 Fig. 8 中来源拉力可以反转份额效应（这与 Σw_jκ_jG_j 的预测一致，说明线性叠加的定性形状已被报告过）；OPDArena Table 9 显示同源学生关闭了 64–90% 的 OOD 预测差距，按题对数优势向教师插值几乎是它的直接推论；2605.30070 已对 OPSD 提出“初始师生差 → 最终提升”的线性预测律，形式上与 κ·G 相同（只是在域内、聚合层面）。因此 H1 新意有限，新意主要在 H2 的连续门控和 H4 的定量叠加，属于把定性结论定量化，达不到 8。 |
| 有效性（先验合理性） | 7.0 | H1：两篇独立论文给出直接支持（2608.16647 中 JustRL 把 GPQA 拉到初始以下、Nemotron 把 GPQA 拉高；OPDArena Table 1/9），反向 KL 下的策略对齐也提供了机制。H2：2608.16647 的初始 Top-16 重叠差异（Fig. 6）和 OPDArena Table 2/3 中更大 Base 教师 G 大但 OOD 不升，都与跨源 κ≈0 一致。H4：在共享状态上，加权反向 KL 的不动点 p∝Πq_j^{w_j} 在对数空间按份额线性，这是一个理论依据。没有发现直接反证，但有两处已知风险：2608.16647 Fig. 5 的拉锯说明固定步数下并不处于稳态；κ 因学生而异，Qwen3-8B 上 >1。还有一个隐患：OPDArena Table 3 中各教师的 OOD JS 在第 120 步相差近一个数量级（0.12 vs 0.69–0.99 ×10⁻²），Base 型教师（Qwen2.5-Math-7B、Qwen3-1.7B-Base）与指令/RL 型教师的位移区间可能不重叠，50 步一个检查点时，H2 的“相同位移”比较可能只能放在位移很小、噪声主导的区间。 |
| 待预研 | — | κ 的实际大小与跨教师的分离度；匹配位移区间是否存在；κ(o_t)·G 相对逐题 KL 和风格 KL 的 Spearman 优势有多大；MOPD 叠加误差相对种子噪声的大小；a_t 能否被对照①预测。以上不计入分数。 |

与起点的关系：回答的是起点问题的细化版（逐题、同一学生和配方、只换教师），外加 MOPD 推论。原问题中“哪个训练前量预测跨教师的总遗忘量”这一部分，被 a_t 吸收后基本没有回答。另外，“训练前可用”需要先训练其余教师来拟合 o_t→κ，实际是“标定后训练前可用”，应明说。

实验能否判别主张：部分不能。
1. **H3 的核心对比失效。** 在每个被留出的教师内算逐题 Spearman 时，κ(o_t) 对该教师是一个正常数，κ(o_t)·G 与“不分来源的对称 G（教师 OOD 损失）”秩次完全相同，两者的差只来自 α_task 的混入。来源门控与教师 OOD 损失之争（起点要求区分的两个对手）只能在跨教师的合并层面检验，例如教师×题合并后的 R² 或 Spearman，或教师级聚合变化的排序。现在的配对置换检验只覆盖题级对手（逐题前缀 KL、对照②），无法检验教师级对手（认知标记率、对照①）。
2. **回归均值只做 5 层分箱是粗粒度控制。** G = T − S 与 S 负相关，任何扰动都会使极端的 S 回归。层内 S 仍连续变化，应把 S 作为连续协变量（例如样条）。跨源教师 κ≈0 的预测正好能当作内置阴性对照，这一点是好的。
3. **H4 的阈值“≤2 倍种子噪声”可能过宽。** 种子噪声只来自 2 个单教师 × 2 种子，不来自 MOPD。H4 缺少能被拒绝的竞争模型，比如“只按路由领域生效”或“饱和/非线性份额响应”。3 个份额加两端点可以检验曲率，应把它作为判别依据。

可行性：pass。OPDArena 代码已核验，`train.py` 中有 `top_k_strategy=only_stu`、`save_freq` 和 `--teacher`，有 `analysis/prefixes.py` 与 `distributions.py`。各教师在 HF 上可获得（SimpleRL-Zoo 1.5B/7B 均公开；Qwen2.5-Math-1.5B 的 base_model 为 Qwen2.5-1.5B，Math-1.5B-Instruct 的为 Math-1.5B；Qwen2.5-Math-7B 的 max_position_embeddings 为 4096），词表与 OPDArena 已用的跨族配对一致。22–24 次运行约 440–480 GPU·h，加评测约 50 GPU·h，在 8×A100×5 天（960 GPU·h）以内。预研第 1 步只做前向计算，能廉价地给出 no-go。逐题标签是对数似然差，可以复现构造，不需要人工标注。需要说明两点：总长 ≤4096、300 步与 OPDArena 的 1024+7168、780 步不同，聚合数字不能直接对照；MOPD 需要改双教师打分，属小改。

## 最高近邻
1. **Every Coin Has Two Sides（arXiv 2608.16647）** https://arxiv.org/abs/2608.16647 ：同源/跨源 OPD 的跨域迁移、Top-16 重叠、MOPD 份额跷跷板、拉锯，以及来源拉力反转份额效应（Fig. 4–8）。重叠：全部三类现象。差别：只做定性和聚合比较，无逐题、无训练前定量预测。
2. **OPDArena（arXiv 2610.25651）** https://arxiv.org/abs/2610.25651 ：同一配方与 OOD 套件；Self-OPD 继承、更大 Base 教师致遗忘（Table 1–3），OOD JS 与遗忘在训练后相关，同源学生 OOD 预测差距关闭 64–90%（Table 9）。差别：没有训练前、逐题的规律。
3. **A Predictive Law for On-Policy Self-Distillation From World Feedback（arXiv 2605.30070）** https://arxiv.org/abs/2605.30070 ：训练前初始师生差与最终提升呈线性关系，形式与 κ·G 同构。差别：OPSD 自教师、域内收益、聚合层面，不涉及来源门控和遗忘。
4. **ESC: Distilling the Shape of Uncertainty（arXiv 2610.39020）** https://arxiv.org/abs/2610.39020 ：训练前预测 OPD 结果，作为教师选择任务。差别：只预测域内收益，教师级，不涉及 OOD 遗忘。
5. **What Will My Model Forget?（arXiv 2402.01865）及 Low-rank Example Associations（arXiv 2406.14026）** https://arxiv.org/abs/2402.01865 、https://arxiv.org/abs/2406.14026 ：逐例预测微调遗忘。差别：依据是样本关联或矩阵补全，不是教师能力差，也不涉及 OPD。

```json
{
  "score": 6.2,
  "contribution_scores": {"importance": 6.5, "novelty": 6.5, "effectiveness": 7.0},
  "contribution_assessment": "主贡献是把同源有符号继承、来源门控、MOPD跷跷板定量化为训练前逐题线性规律。H1几乎由OPDArena Table 9的OOD预测差距关闭推出，新意集中在连续κ(o_t)门控与份额线性叠加；2605.30070已有OPSD初始差→收益的线性律，2608.16647 Fig.4-8已定性给出叠加形状。跨源遗忘被归入未解释的a_t，起点问题的跨教师总遗忘差异基本未答。先验合理性有两篇直接证据和加权反向KL不动点论证，无直接反证；风险在于Fig.5的非稳态，以及各教师OOD位移区间可能不重叠，导致匹配位移难以实现。三项都未达8，不满足门槛。",
  "feasibility": "pass",
  "feasibility_reason": "OPDArena代码已核验，含only_stu、save_freq、--teacher与prefix/distribution分析；教师均在HF公开，Qwen2.5-Math-7B为4096上下文；22-24次运行约480 GPU·h加评测，在8×A100×5天内；预研第1步只需前向计算即可给出no-go；逐题标签为可复现的对数似然差。",
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "贡献门槛未达：重要性6.5/新颖度6.5/有效性7.0，没有一项≥8；H1近似由已知的OOD预测差距关闭推出，H2/H4是对2608.16647定性结论的定量化，跨源遗忘留在残差a_t中",
    "H3判别失效：留出教师内的逐题Spearman对κ(o_t)·G与对称G（教师OOD损失）秩次相同，无法检验来源门控与教师OOD损失之争；教师级对手（认知标记率、对照①）也无法在题内检验，需要跨教师合并层面的评估",
    "H2匹配位移可能不可行：Base型与指令/RL型教师的OOD JS相差近一个数量级，50步检查点下共同位移区间可能只剩噪声主导的小位移段"
  ],
  "novelty_conclusion": "未检索到逐题、有符号、来源门控的OPD遗忘训练前预测，也未检索到MOPD份额的定量叠加预测，属可辨认增量；但2608.16647（定性三现象）、OPDArena Table 9（预测差距关闭）与2605.30070（OPSD线性差距律）使H1与规律形式的新意有限，整体约6.5。",
  "closest_neighbors": [
    "Every Coin Has Two Sides: On the Dual Nature of Generalization in On-Policy Distillation of Large Language Models (arXiv 2608.16647)",
    "OPDArena: Understanding Learning and Forgetting in On-Policy Distillation (arXiv 2610.25651)",
    "A Predictive Law for On-Policy Self-Distillation From World Feedback (arXiv 2605.30070)",
    "Distilling the Shape of Uncertainty: What On-Policy Distillation Learns and How to Predict It (arXiv 2610.39020)",
    "What Will My Model Forget? Forecasting Forgotten Examples in Language Model Refinement (arXiv 2402.01865)"
  ]
}
```
