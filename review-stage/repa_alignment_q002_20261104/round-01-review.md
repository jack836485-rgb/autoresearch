## 结论
2026-11-04，总体 score 5.3，verdict：promising_needs_revision。如果关键结果成立，主贡献是第一次直接测量表征对齐（REPA）在数据受限训练下怎样改变 τ_gen、τ_mem 和泛化窗口，并把作用归因到"实例可识别性"而非"语义"。检索没有找到 REPA 与记忆化的直接测量，所以空位是真的。但现在分量不够：效应方向只是一个合理的经验问题，"加速拟合的因素也加速记忆化"本身就是现有时间尺度框架的自然推论；用来做因果归因的 (b)(c) 两臂又各自混入了别的变量。三项都没到 8 分，过不了门槛。

## Claim 判断

| 维度 | 分数 | 依据 |
|---|---|---|
| 重要性 | 6.0 | REPA 已是 DiT 训练的默认组件。"加速是否也加速复制"对从头训练的小数据、领域数据用户有实际意义，两个方向的结果都值得知道。但影响范围有限：REPA 的主战场是全量 ImageNet，那里不在记忆化区间；数据受限的从业者多数微调预训练模型，不从头加 REPA 训练。不管结果朝哪个方向，都不会明显改变领域里的重要判断。 |
| 新颖度 | 6.5 | 没有检索到 REPA 或 HASTE 与记忆化、τ_mem 的直接测量，2×2 拆分目标的思路也可辨认。但核心预测与已有认识高度相邻：Marion & Wu 发现增大模型同时提前拟合与记忆化；Gu 等（2310.02664）发现给每张训练图一个唯一的随机标签就能大幅触发记忆化。(b) 臂其实是"从噪声输入回归每张图唯一编码"的辅助实例识别损失，它提前 τ_mem 基本可以由 Gu 等的结果预测。新意主要落在"第一次对 REPA 做这项测量"，机制层面的新理解有限。 |
| 有效性 | 5.0 | **现有依据**：时间尺度框架（Bonnaire 等、Favero 等）可以迁移到 SiT 潜空间，只是 τ_mem ∝ n 在 DiT 潜空间的类条件设置下还没核验；SSL 特征对单个实例可分（SSCD、DINO 被用来做复制检测）；HASTE 和 PixelREPA 支持相反方向。两个方向的直接证据都没有，作者自己也承认这一点。**归因链缺口**：① 去噪目标本身就是训练图，实例身份已经由主损失完整提供。"对齐目标携带可识别性"必须说明 DINOv2 额外提供了什么，比如在不同噪声级下从 x_t 检索实例的难易，而 brief 没有给出这一机制量。② (b) 的随机编码没有空间平滑性，也和图像内容无关，与 (a) 同时差在可学性、和 x_t 的可预测关系、可识别程度三处。(b) 提前 τ_mem 并不能说明 (a) 的提前来自可识别性。③ (c) 同时去掉了实例信息、空间结构和类内方差，作者也承认这是混淆。所以即使观察到"(a)(b) 提前、(c) 不提前"，"是可识别性而非语义"这个因果结论也仍然识别不出来。 |

**与起点问题的关系**：这是邻近新问题。它保留了"对齐向学生提供了什么"这一对象，转向不构成否决。原问题里全量数据下的加速机制和种子噪声问题，本题都不回答。

**实验能否判别主张**："(a) 相对 (d) 提前还是推迟 τ_mem"这一层可以判别；"可识别性还是语义"这一层不能判别，原因见上面的 ②③。还有一个测量问题：τ_gen 用"对相应子集"的 FID 定义。如果参考集是训练子集，复制样本反而会压低 FID，生成和复制就被混在一起，应改用同类 held-out 图。另外 n 只有 1k 时 FID 的参考统计不稳定，"首次进入平台"的判据也需要事先固定。

**可行性：pass**。REPA 和 HASTE 都有官方代码，不对齐基线就在同一仓库里；Bonnaire 等的 f_mem 代码公开；ImageNet、SD-VAE、DINOv2 都可得；(b)(c) 只需离线预计算目标张量后替换。SiT-B/2 的每次运行大约在 10–20 GPU 小时这一量级，预研在 2×A100 上 1–2 天内可以完成。风险：τ_mem ∝ n，n=16k 很可能在 20 万步内不出现记忆化，结果会被截断；n=4k 若需要更长训练，正式预算要按实际 τ_mem 重估。不过这不影响最小实验能否做出来。

## 最高近邻
1. Bonnaire 等，Why Diffusion Models Don't Memorize（NeurIPS 2025），https://arxiv.org/abs/2505.17638 。重叠：τ_gen/τ_mem 框架、f_mem 协议。差别：只改 n 和模型规模，没有外部表征监督。
2. Marion & Wu，Understanding diffusion models requires rethinking (again) generalization，https://arxiv.org/abs/2605.06077 。重叠：增大模型同时提前拟合与记忆化，这是"加速因素也加速记忆化"的直接先例。差别：没有涉及表征对齐。
3. Gu 等，On Memorization in Diffusion Models（TMLR 2025），https://arxiv.org/abs/2310.02664 。重叠：每图唯一的随机标签会显著触发记忆化，与 (b) 臂的机制高度重合。差别：标签作为输入条件，不是中间层对齐目标；没有涉及 REPA。
4. HASTE，REPA Works Until It Doesn't（2505.16792），https://arxiv.org/abs/2505.16792 。重叠：对齐后期有害、早停。差别：只在全量 ImageNet 上测 FID 和收敛，没有测记忆化。
5. Generalization of Diffusion Models Arises with a Balanced Representation Space（ICLR 2026），https://arxiv.org/abs/2512.20963 。重叠：把记忆化和泛化与内部表征结构联系起来，并提到 REPA。差别：没有把对齐目标作为干预，也没有测时间尺度。

```json
{
  "score": 5.3,
  "contribution_scores": {"importance": 6.0, "novelty": 6.5, "effectiveness": 5.0},
  "contribution_assessment": "主贡献是第一次测量 REPA 在数据受限下对 τ_gen/τ_mem/泛化窗口的作用，并把作用归因到'实例可识别性 vs 语义'。测量空位真实存在，但影响面有限（从头加 REPA 训练小数据的场景不多），核心预测与 Marion & Wu（模型规模同时提前拟合与记忆化）、Gu 等（唯一随机标签触发记忆化）相邻。效应方向两边都有依据，没有直接证据。归因设计不可识别：去噪目标本身已携带实例身份，DINOv2 额外提供什么没有给出机制量；随机编码臂同时改变了可学性、与 x_t 的关系和可识别程度；类内平均臂同时去掉了实例、空间结构和类内方差。",
  "feasibility": "pass",
  "feasibility_reason": "REPA、HASTE、f_mem 都有公开代码，数据与编码器公开，(b)(c) 只需离线替换目标张量；SiT-B/2 单次运行约 10–20 GPU 小时，预研 2×A100 1–2 天可完成。n=16k 的 τ_mem 可能被截断，正式预算需按实测 τ_mem 重估。",
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "贡献门槛不满足：三项中没有一项 ≥8；只测出 REPA 提前或推迟 τ_mem，分量有限，且'加速因素也加速记忆化'接近现有时间尺度框架的推论",
    "'是可识别性而非语义'的因果 Claim 不可识别：(b) 随机编码与 (a) 同时差在可学性、与 x_t 的可预测关系和可识别程度，其提前 τ_mem 可由 Gu 等的唯一标签结果预测；(c) 同时去掉实例、空间结构和类内方差；去噪目标本身已携带实例身份，DINOv2 目标额外提供了什么没有给出机制量",
    "τ_gen 用'对相应子集'的 FID 定义，若参考集是训练子集，复制会压低 FID，生成和复制被混在一起，需改用 held-out 参考集"
  ],
  "novelty_conclusion": "没有检索到 REPA/对齐目标与记忆化时间尺度的直接测量，测量层面有新意；机制预测与 Marion & Wu、Gu 等高度相邻，(b) 臂近似把 Gu 等的唯一标签实验换成对齐目标，机制新意有限。",
  "closest_neighbors": [
    "Why Diffusion Models Don't Memorize: The Role of Implicit Dynamical Regularization in Training (2505.17638)",
    "Understanding diffusion models requires rethinking (again) generalization (2605.06077)",
    "On Memorization in Diffusion Models (2310.02664)",
    "REPA Works Until It Doesn't: Early-Stopped, Holistic Alignment Supercharges Diffusion Training (2505.16792)",
    "Generalization of Diffusion Models Arises with a Balanced Representation Space (2512.20963)"
  ]
}
```
