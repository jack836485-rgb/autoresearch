## 结论
2026-11-04，总体 score 4.5，verdict：needs_rethink。主贡献是对齐的累计等效算力倍数 M(N,C) 在哪个算力降到 1（即交叉点 C\*(N)），以及 C\*(N) 怎样随学生规模变化。这个贡献目前不够，原因有两个。第一，它把 HASTE 观察到的"边际收益反转"错当成"累计优势归零"：HASTE 比的是继续对齐和中途关掉的分叉，不是对齐和不对齐。已有证据显示累计优势很大：REPA SiT-XL 跑 40 万步的 FID 是 7.9，未对齐模型跑 700 万步也只有 8.3。所以在预算内大概率测不到 M=1。第二，如果真测到了 M=1，最可能的原因是小学生模型上教师前向的算力占比很高，这是计费口径造成的，不是对齐收益本身的规模律。

## Claim 判断
| 维度 | 分数 | 依据 |
|---|---|---|
| 重要性 | 5.5 | 一份按算力归一、能跨规模给出"开不开对齐、何时关"的处方有实用价值。但规模只覆盖 S/B/L（约 33M–458M 参数），只在 ImageNet-256 的 REPA 配方上，不触及"对齐补的是什么"这个机制分歧。实践里 HASTE 已经按规模给了固定关闭步数（B 是 100K，L/XL 是 250K），所以本题能带来的增量判断有限。 |
| 新颖度 | 6.0 | 检索没有找到按 FLOPs 归一、拟合等效算力倍数或交叉点的 REPA 规模研究，这一点可辨认。但框架是 Busbridge 蒸馏规模律直接搬过来，"交叉点"的经验现象来自 HASTE。HASTE 第 3.2 节和 Table 4 已经在 B、L、XL 上分别设关闭点并比较效果，所以 brief 说 HASTE "不跨规模"并不准确，新意主要剩下 FLOPs 口径和外推拟合。 |
| 有效性 | 4.0 | **现在有什么依据：** Busbridge 的结论是，有现成教师时，蒸馏只在某个随学生规模变化的算力以下优于监督训练。这个结论成立的前提是学生的上限被教师卡住，监督训练终将追上。HASTE 在 SiT-XL 上测到梯度夹角从锐角变为钝角，关掉对齐后 FID 恢复。**为什么不直接适用：** 这两条依据都只支持"继续对齐的边际收益会转负"，不支持"累计倍数 M 降到 1"。REPA 的数据反而指向 M 远大于 1：XL 跑 40 万步约等于未对齐跑 700 万步；B 在 40 万步时，未对齐 33.0、对齐 24.4，差距仍大。Busbridge 结论的前提（教师卡住学生上限）在 REPA 里没有证据，HASTE 的分叉结果说明关掉对齐就能解除限制。**仍未知：** C\*(N) 是否存在于可测的算力范围内，以及 FID 曲线外推的误差。 |

- **与原问题的关系：** 回答的是原问题"对齐是加速还是改变终点"的定量化版本，不因转向扣分。但原问题的核心，也就是终点是否被改变、机制是什么，仍然没有回答。
- **实验能否判别主张：** 不能。
  1. **M 是右删失的。** 未对齐曲线只跑到 80 万步，一旦对齐模型的 FID 低于未对齐模型在 80 万步时的最好值，M 就无法直接测，只能靠外推未对齐的 FID 曲线。这样拟合 M(N,C) 的大部分数据点本身是外推出来的。
  2. **L 留出测试几乎必然得到"40 万步内 M 不到 1"。** 按 REPA 的数据，L 在 40 万步时未对齐 18.8、对齐 9.7。这个"预测成功"没有判别力。L 只有 1 个种子，"误差落在种子散布内"这个判据在 L 上也没有估计依据。
  3. **计费口径会混入 N 依赖。** 教师计入口径下，DINOv2-B 每张图前向约 20 GFLOPs 量级，SiT-S/2 前向约 6 GFLOPs，教师成本和学生训练成本同量级甚至更高。这样 S 上出现交叉点、交叉点随 N 单调变化，都可能只是教师与学生 FLOPs 比值的直接结果。摊销口径下这个效应会消失，两种口径的结论可能相反，brief 没有说主张以哪一种为准。
  4. **与 HASTE 的对照有混杂。** HASTE 实际用的是固定步数关闭（L 是 250K），不是"梯度停止规则"，梯度夹角只用来做分析。HASTE 还同时对齐了注意力图（ATTA）。拿特征对齐的关闭时机去比它，会把两种因素混在一起。
  5. **真正有用的量没有被单独设为主张。** 能给出处方的是使终点 FID 最优的关闭时机 τ\*(N)，判据是关闭分叉与全程对齐的边际斜率比较，而不是 M=1。现在 τ\*(N) 只是 M 拟合的副产物，而且只用 S、B 两个点外推。
- **可行性：pass。**
  - 已核验的官方 REPA 和 HASTE 仓库都可用，ImageNet、SD-VAE、DINOv2-B 都公开，FLOPs 可以按结构解析算出。
  - 预研约 130 A100 小时，2×A100 约 2.7 天可行。正式实验约 830 A100 小时，8×A100 约 4.3 天，在 5 天上限内，但几乎没有余量。
  - 每 2.5 万步一次 SDE gFID-10k，对 S、B 的评测成本可控。
  - RARE 没有公开代码，平台判据需要自己定，只影响附加对照。
  - 可行性通过不抵消上面的 Claim 阻断：预研的推翻条件"S 和 B 上不出现交叉点"大概率会因为第 1、2 点而触发，或者因为第 3 点在 S 上触发且无法解释。

## 最高近邻
1. **HASTE**（REPA Works Until It Doesn't，[arXiv 2505.16792](https://arxiv.org/abs/2505.16792)，[代码](https://github.com/NUS-HPC-AI-Lab/HASTE)）
   - 重叠：对齐先助后阻、中途关掉；按规模设关闭点（B 是 100K，L/XL 是 250K），Table 4 比较了各规模的关闭效果。
   - 差别：没有 FLOPs 归一、没有拟合规律、没有跨规模外推，比较对象是边际收益而不是累计倍数。
2. **Distillation Scaling Laws**（Busbridge 等，[arXiv 2502.08606](https://arxiv.org/abs/2502.08606)）
   - 重叠：有现成教师时，蒸馏优于监督训练的区间止于一个随学生规模可预测的算力水平，本题的框架直接来自这里。
   - 差别：教师是同任务的 LM logit 蒸馏，交叉点的成因是教师卡住学生上限；在 REPA 里这个前提未得到证实。
3. **REPA**（[arXiv 2410.06940](https://arxiv.org/abs/2410.06940)）
   - 重叠：在 B/L/XL 上报告收益随规模增大，给出了 40 万步的 FID 对比和"未对齐需要 700 万步"的倍数。
   - 差别：只按固定步数比较，不按算力归一，不讨论交叉点。
4. **RARE**（What Visual Generators Need from Teachers，[arXiv 2609.34732](https://arxiv.org/abs/2609.34732)）
   - 重叠：用对齐残差进入平台作为释放信号，在训练中决定何时停止对齐。
   - 差别：依赖训练中的信号，单一配置，不做跨规模的事先预测，也没有公开代码。
5. **iREPA**（What matters for Representation Alignment，[arXiv 2512.10794](https://arxiv.org/abs/2512.10794)）
   - 重叠：讨论收益随模型规模的变化，以及教师选择的影响。
   - 差别：研究的是机制（空间结构还是全局信息），只报告固定步数的结果，与按算力定的处方无关。

```json
{
  "score": 4.5,
  "contribution_scores": {"importance": 5.5, "novelty": 6.0, "effectiveness": 4.0},
  "contribution_assessment": "主贡献是对齐累计等效算力倍数 M(N,C) 降到 1 的交叉点 C*(N) 及其随学生规模的规律。重要性有限：只覆盖 S/B/L 和单一配方，HASTE 已按规模给出固定关闭点。新意在于 FLOPs 归一和跨规模外推，没有检索到直接先例，但框架是 Busbridge 搬过来的，现象来自 HASTE。有效性依据有错配：HASTE 的反转是边际收益反转（继续对齐 vs 关闭分叉），不是累计优势归零；REPA 的数据（XL 跑 40 万步约等于未对齐跑 700 万步）指向 M 远大于 1。Busbridge 结论的前提（教师卡住学生上限）没有证据，关掉对齐就能恢复。若测到 M=1，在 SiT-S 上更可能来自教师前向 FLOPs 与学生训练同量级的计费口径。待验证：C*(N) 是否存在于可测算力内、M 的删失与外推误差、τ*(N) 能否跨规模预测。",
  "feasibility": "pass",
  "feasibility_reason": "官方 REPA/HASTE 仓库、ImageNet、SD-VAE、DINOv2-B 都可得，FLOPs 可解析计算。预研约 130 A100 小时（2×A100 约 2.7 天），正式实验约 830 A100 小时（8×A100 约 4.3 天），在 5 天内但余量很小。RARE 无代码只影响附加对照。",
  "verdict": "needs_rethink",
  "fatal_blockers": [
    "主量错配：HASTE 的证据只支持继续对齐的边际收益转负，不支持累计倍数 M 降到 1；REPA 数据显示 M 远大于 1，预算内大概率测不到 C*(N)，主张缺少依据",
    "M 右删失：未对齐曲线只到 80 万步，M 的大部分点要靠外推未对齐的 FID 曲线，拟合 M(N,C) 不可靠",
    "L 留出测试缺乏判别力：按 REPA 数据，40 万步内 M 必然远大于 1，'预测成功'几乎是必然结果；L 单种子，没有种子散布可用于判据",
    "计费口径混杂：教师计入口径下 SiT-S 的教师前向 FLOPs 与学生训练同量级，交叉点及其对 N 的单调性可能只是 FLOPs 比值的结果，两种口径的结论可能相反，主张没有指定以哪种为准",
    "与 HASTE 的对照不准确：HASTE 实际用固定步数关闭且同时对齐注意力图，不是梯度停止规则，混入了对齐形式的差异；HASTE 已按规模设关闭点，'不跨规模'的定位不成立"
  ],
  "novelty_conclusion": "没有检索到对 REPA 做 FLOPs 归一、拟合等效算力倍数或交叉点的工作，FLOPs 口径加跨规模外推是可辨认的增量。但框架直接来自 Distillation Scaling Laws，先助后阻和按规模设关闭点来自 HASTE，新意中等（约 6），不足以弥补主量错配。",
  "closest_neighbors": [
    "REPA Works Until It Doesn't: Early-Stopped, Holistic Alignment Supercharges Diffusion Training (HASTE, arXiv 2505.16792)",
    "Distillation Scaling Laws (arXiv 2502.08606)",
    "Representation Alignment for Generation: Training Diffusion Transformers Is Easier Than You Think (REPA, arXiv 2410.06940)",
    "What Visual Generators Need from Teachers: Rethinking Representation Alignment (RARE, arXiv 2609.34732)",
    "What matters for Representation Alignment: Global Information or Spatial Structure? (iREPA, arXiv 2512.10794)"
  ]
}
```
