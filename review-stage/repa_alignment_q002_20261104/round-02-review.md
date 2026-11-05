## 结论
2026-11-04：总体 score 5.0，verdict = promising_needs_revision。如果关键结果成立，主贡献会是"潜空间的选择会改变扩散模型在训练中开始复制训练样本的时间（τ_mem）和泛化窗口，而且可以用训练前算出的 t* 预测"。我检索后没有找到直接测过 RAE 与 VAE 潜空间下 τ_mem 的工作，所以"潜空间是不是记忆化因素"这个问题本身有空位。但这份 brief 目前还不足以放行：
- **t* 与已有理论重合。** t* 本质上就是 Biroli 等提出的经验 score 坍缩时间 t_C，Achilli 等已经证明它由内在维度控制；brief 没有点出这一近邻。
- **缺少关键依据。** 从"采样过程中的坍缩时间"到"训练中的记忆化步数"，这一环没有任何依据。
- **最小实验判别力不足。** 3 个编码器排序加 1 个种子的预研，区分不开有效维度、可扩散性和解码保真度这些竞争解释。
- **结果：** 三项分数为 6 / 6 / 4.5，没有达到"至少两项 ≥8"的门槛。

## Claim 判断
| 维度 | 分数 | 依据 |
|---|---|---|
| 重要性 | 6.0 | RAE 正在被扩到文生图（Scale-RAE 2601.16208），所以"换 tokenizer 会不会改变复制风险"有实际意义。但全量数据下 τ_mem ∝ n，远超训练预算（Marion & Wu 2605.06077 正据此认为实际训练不会记忆化）。真实的复制风险主要来自重复图和小数据微调，这让结论的影响面有限。t* 若只是对 n、维度的已知依赖换个名字，也改变不了 tokenizer 选择。 |
| 新颖度 | 6.0 | 检索确认：没有工作直接测量 RAE 与 VAE 潜空间下的 τ_mem / f_mem。<br>但预测量 t* 不是新的：它等于 Biroli 等（2402.18491）经验后验凝聚得到的 collapse time t_C，Achilli 等（2502.09578）已经推出 t_C 由内在维度、而非外在维度决定。<br>Feng 等（2609.28473）已经指出重建微调会降低有效维度、改变几何，Scale-RAE 已经观察到 VAE 潜空间下过拟合更快。<br>新意因此只在"把已知的 t_C 跨 tokenizer 用作训练期 τ_mem 的预测器"，属于可辨认的增量，不足 8。 |
| 有效性 | 4.5 | **现有依据：**<br>(1) Feng 图 1：单图拟合速度随潜空间而变；<br>(2) Scale-RAE：VAE 潜空间的训练损失下降更快更深，作者解读为过拟合；<br>(3) Bonnaire 2505.17638：τ_mem ∝ n，由网络学到经验 score 的动力学决定。<br>这些依据只能支持"潜空间可能影响拟合速度"。<br>**关键跳跃：** t_C 描述的是"假设已学到经验 score 时，在哪个噪声级坍缩"，并不描述训练多少步才学到它。Bonnaire 的框架里，τ_mem 由网络容量和训练动力学决定，没有给出与 t_C 单调相关的机制。<br>**额外风险：** d = 16×16×768 ≈ 2×10⁵、n = 2k 时，按 REM 估计，所有编码器的经验后验都会在极低 SNR 下坍缩，t* 很可能贴近纯噪声端并在三种编码器间几乎饱和。t* 之间若有差异，也主要反映有效维度和样本间相关性。而有效维度同时决定 Feng 所说的可扩散性和拟合速度，所以 t* 很难与这些竞争解释分开。迁移条件与未知部分都还在。 |

**与起点问题的关系：** 这是邻近新问题。它保留了"语义表征给扩散模型带来什么"这一对象，但完全不回答原问题里 REPA 在全量 ImageNet 上的加速机制和终点质量问题。转向本身不是阻断，阻断来自上面的贡献分量不足。

**实验能否判别主张：** 目前不能充分判别。
1. **样本量太小。** 主比较只有 3 个 RAE 编码器，排序一致纯靠运气的概率是 1/6。即使排序一致，也无法把 t* 与有效维度、Feng 式单图拟合速度、解码器 rFID 区分开，因为这些量都可以零训练成本算出来，却没有作为竞争预测量预先登记。
2. **f_mem 被解码保真度混淆。** f_mem 在解码像素空间里对原始训练图算最近邻距离比，而三种编码器的重建保真度不同（MAE 与 DINOv2、SigLIP2 的 rFID 不同）。"完美复制训练潜变量"在不同臂下对应的像素距离也不同，f_mem 的阈值因此不可比，应当对解码后的训练集重建图计算，或者在潜空间内计算。
3. **τ_gen 不稳。** τ_gen 用 100 类、2k 张图的 held-out FID 平台来定义，FID 噪声很大，泛化窗口比值会不稳定。
4. **预研设计。** "挑 t* 差距最大的两个编码器"的前提是 t* 确实有差距；如果 t* 饱和，预研就失去依据。

**可行性：pass。**
- **资源：** RAE 官方仓库与 HF 上 DINOv2-B、SigLIP2-B、MAE-B 的解码器和统计量、REPA/SiT 仓库、Bonnaire 的 f_mem 代码都可获得；ImageNet 子集可以构造；t* 的 Monte Carlo 计算成本很低。
- **预算：** 2 次约 35 A100 小时的预研能在 2×A100 上完成，正式实验贴着 8×A100、5 天的上限。
- **主要实现风险：** n=2k 时，τ_mem 能否在 20 万步内出现没有依据，不过更大的模型会更快记忆化（Marion & Wu），所以属于可接受的风险。

## 最高近邻
1. **Biroli, Bonnaire, de Bortoli, Mézard, Dynamical Regimes of Diffusion Models**（[arXiv 2402.18491](https://arxiv.org/abs/2402.18491)，Nat. Commun. 2024）
   - 重叠：用训练数据算 collapse time t_C，即经验后验凝聚到单个样本的时刻，与本题的 t* 在定义上相同。
   - 差别：没有比较不同 tokenizer 潜空间，也没有把 t_C 与训练步数联系起来。
2. **Achilli et al., Memorization and Generalization in Generative Diffusion under the Manifold Hypothesis**（[arXiv 2502.09578](https://arxiv.org/abs/2502.09578)）
   - 重叠：t_c 由内在维度、而非外在维度决定，相当于已经给出"潜空间几何决定坍缩时刻"的理论版本。
   - 差别：只有理论和合成数据，不涉及真实 tokenizer，也不涉及训练期 τ_mem。
3. **Bonnaire et al., Why Diffusion Models Don't Memorize**（[arXiv 2505.17638](https://arxiv.org/abs/2505.17638)）
   - 重叠：提出 τ_gen / τ_mem 框架、τ_mem ∝ n，以及 f_mem 协议。
   - 差别：只改变 n 和模型容量，没有改变潜空间。
4. **Feng et al., On the Diffusibility of High-Dimensional Latents**（[arXiv 2609.28473](https://arxiv.org/abs/2609.28473)，ECCV 2026）
   - 重叠：潜空间几何（有效维度）改变 RAE 下的拟合与优化速度。
   - 差别：只关注可学性和生成质量，不测记忆化和泛化窗口。
5. **Scaling Text-to-Image Diffusion Transformers with Representation Autoencoders**（[arXiv 2601.16208](https://arxiv.org/abs/2601.16208)）
   - 重叠：观察到 VAE 潜空间下过拟合更快更深、RAE 潜空间更抗过拟合，并归因于高维语义潜空间。
   - 差别：只看损失曲线和生成质量，不测 τ_mem 或复制率，也没有训练前的预测量。

```json
{
  "score": 5.0,
  "contribution_scores": {"importance": 6.0, "novelty": 6.0, "effectiveness": 4.5},
  "contribution_assessment": "主贡献若成立：潜空间选择改变 τ_mem 与泛化窗口，且可由训练前的 t* 预测。'潜空间是否为记忆化因素'未见直接测量，有空位；但 t* 即 Biroli 等的 collapse time t_C，Achilli 等已证其由内在维度控制，新意只剩'跨 tokenizer 用作训练期预测器'。有效性缺少从采样期坍缩时间到训练期 τ_mem 的任何机制或证据；d≈2e5、n=2k 时 t* 很可能在各编码器间饱和，差异即使存在也与有效维度、可扩散性同源，3 个编码器的排序无法区分这些竞争解释。实际复制风险主要在重复图和小数据场景，重要性中等。",
  "feasibility": "pass",
  "feasibility_reason": "RAE 三种 B 级编码器的解码器和统计量、REPA/SiT 代码、f_mem 代码均公开，t* 计算成本很低；预研 2 次约 70 A100 小时可在 2×A100 上完成，正式实验贴着 8×A100、5 天上限；主要风险是 n=2k 时 τ_mem 能否在 20 万步内出现。",
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "贡献门槛未达：重要性 6、新颖度 6、有效性 4.5，没有任何一项达到 8",
    "预测量 t* 等同于 Biroli 等（2402.18491）的 collapse time，Achilli 等（2502.09578）已给出它由内在维度决定的理论；brief 未定位这一近邻，t* 本身不构成新意",
    "从采样坍缩时间 t* 到训练记忆化步数 τ_mem 的单调关系没有机制或证据支撑；高维 RAE 潜空间下 t* 很可能在各编码器间饱和",
    "最小实验只有 3 个编码器排序，无法把 t* 与有效维度、单图拟合速度、解码 rFID 等零成本竞争预测量区分开",
    "f_mem 在像素空间对原始训练图计算，会被不同编码器解码保真度的差异混淆，阈值跨臂不可比"
  ],
  "novelty_conclusion": "'潜空间选择影响 τ_mem 与泛化窗口'未见直接实证，问题有空位；但 t* 是已知 collapse time 的重新命名，内在维度控制坍缩已有理论，Scale-RAE 和 Feng 已观察到潜空间影响过拟合与拟合速度，新意为增量级。",
  "closest_neighbors": [
    "Dynamical Regimes of Diffusion Models (arXiv 2402.18491)",
    "Memorization and Generalization in Generative Diffusion under the Manifold Hypothesis (arXiv 2502.09578)",
    "Why Diffusion Models Don't Memorize: The Role of Implicit Dynamical Regularization in Training (arXiv 2505.17638)",
    "On the Diffusibility of High-Dimensional Latents (arXiv 2609.28473)",
    "Scaling Text-to-Image Diffusion Transformers with Representation Autoencoders (arXiv 2601.16208)"
  ]
}
```
