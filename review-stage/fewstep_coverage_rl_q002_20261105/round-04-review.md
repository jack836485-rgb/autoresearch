## 结论
2026-11-05，总体 score 6.0，verdict：promising_needs_revision。主贡献是在扩散领域做一项受控研究：少步学生里与 RL 相关的覆盖收缩落在布局上，CLIP/DINO 这类多样性指标测不到它，组归一化 RL 在布局子任务上的收益由"中间成功率提示占比"决定。若结果成立，它有可辨认的价值，但还不够。核心机制（混合成败提示带来组内学习信号）在 LLM（2609.33780）和 T2I GRPO（CGPO 的奖励方差课程）中都已确立，真正新增的只有"布局/外观分解"加上 P 反例。三项分数都没到 8，过不了门槛。

## Claim 判断
| 维度 | 分数 | 依据 |
|---|---|---|
| 重要性 | 6.5 | 少步学生接 RL 是活跃方向（TDM-R1、RTDMD、DMDR）。"多样性修法提高了 CLIP/DINO，不等于对 RL 有用"，对 ReSeed、DP-DMD 这类工作有实际的判断价值。但有三点限制影响范围。第一，GenEval 上 RL 本身已能从很低的起点打到 0.92–0.98：DiffusionNFT 从 CFG-free SD3.5-M 的 0.24 到 0.98，TDM-R1 从 0.61 到 0.92。所以起点覆盖的作用很可能只体现在等预算截断下的效率，不体现在可达上限。第二，作为"工具"的中间成功率占比，基本就是 CGPO/DAPO 在训练中已直接使用的组内奖励方差/混合成败信号。第三，结论只适用于可验证的二值组合奖励，偏好类奖励的机制不同。 |
| 新颖度 | 7.0 | 在扩散领域，我没有检索到研究"少步学生起点覆盖如何影响后续组归一化 RL"的直接近邻。DMDR 只指出蒸馏学生作为锚点贫乏、会导致 RL 塌缩，并改为联合训练；它没有分解覆盖，也没有研究起点。按跨领域迁移规则，这类迁移本身不低于 7。"第一步承诺布局"是针对扩散的结构性适配，P 反例在文本侧没有对应物，这是有内容的新意。没给到 8 的原因：组内退化信号这一机制在 T2I RL 里已由 CGPO（CVPR 2026）用作采样准则，在 LLM 里 2609.33780 已给出几乎同构的"起点多样性→更多混合成败提示→RL 收益"诊断。新增部分集中在分解和反例上。 |
| 有效性（先验合理性） | 6.0 | 支持的依据：多样性损失集中在第一步，有 Gandikota&Bau 2503.10637、ReSeed、DP-DMD 三方支持，布局由这一步决定是合理推论。组归一化下全同二值奖励的组没有方向，是机制事实。平均 p 相同时两极化分布带来更多退化组，是算术推论。这条主链成立。需要扣分的三处：(1) 关键反例 P 的可构造性与已有证据相冲突。Gandikota&Bau 和 ReSeed 都显示，替换后续步骤几乎恢复不了多样性，而 DINO 多样性本身强烈反映结构。4 步学生只在最后一步加偏置，要让 CLIP/DINO 升幅不低于 L（ReSeed 的 DINO 升幅约 48%），先验上不大可能。P 不成立，"外观多样性升高却无益"这一核心判别就测不了。brief 把它列为第 0 关停止条件，处理是诚实的，但这是一个已有证据不利的关键环节。(2) 奖励定义与机制不一致。官方 Flow-GRPO/DiffusionNFT 的 GenEval 奖励是部分得分（计数 r=1−\|N_gen−N_ref\|/N_ref，位置/颜色在计数正确时先给部分分），退化组远少于二值情形；brief 写的是"二值奖励"，等于偏离了官方配方，而这一点没有说明。DiffusionNFT 从 0.24 起点仍能快速学习，正说明在部分得分奖励下"成功率两极化"并非瓶颈。(3) 在 LLM 侧，2609.28145 报告过：pre-RL pass@64 相同的起点，RL 后仍相差 1.85 点。这说明单一的起点覆盖量不足以完全预测收益，"同一条曲线"这一预测有风险。 |
| 待预研 | — | 不计分：各学生布局缺口的大小；P 能否在布局方差不变时把 CLIP/DINO 提到 L 的水平；DiffusionNFT 下 4 步质量能否保持；在 RL 0.9+ 的饱和区，等预算截断下的收益差相对种子方差有多大；G=48 是否落在同一条曲线上。 |

与起点问题的关系：这是一个子问题。它回答了"现有多样性修法是否只在多样性指标上有效"，并给出了覆盖收缩的一种下游后果（RL 收益）。原问题中单样本增益与覆盖损失是否同源、部署时 best-of-k 的后果，都仍未回答。

实验能否判别主张：A/L/P 三起点加上协变量匹配，设计上能区分"布局覆盖"和"外观多样性"两种解释。G=48 控制也能检验机制是否在于组内信号。但有两个缺口：
- P 的可构造性是整套判别的前提，见上。
- "L 的实用价值"以及"RL 前诊断工具"两个子主张，缺少同任务强基线：A 起点加上按奖励方差/混合成败的提示筛选或课程（CGPO；DAPO 式动态采样；Pro-GRPO 的扩组再剪枝）。这类方法直接拉高有效提示占比，成本可能低于 L。不和它们比，就无法说明 L 或这个诊断工具值得用。这个缺口同时也是一个现成的机制检验（筛选后的 A 是否落在同一条曲线上），目前设计里没有。

可行性：pass。三个官方仓库都在：DiffusionNFT 有 sd3_geneval 配置；TDM-R1 有 4 步 GenEval G24 脚本和 TDM_sd3-5_lora；ReSeed 已发布代码和 SD3 适配器。SD3.5-L-Turbo 公开可得。教师采样 553×32 张约数十 A100 小时，合理。DiffusionNFT 报告约 150 GPU 小时就能到 0.98，4 步学生采样更便宜，所以 9 条 RL 在 8×A100 上 5 天内是可信的（单条耗时未实测）。缺的只是一些具体选择：二值奖励的实现、P 适配器的训练目标、蒸馏进 LoRA 的步数。这些是规范上的空白，不是资源不足。

## 最高近邻
1. Selecting Diverse SFT Traces Improves Post-RL Generalization（https://arxiv.org/abs/2609.33780）：LLM 侧，起点多样性带来更多混合成败提示，从而带来组相对 RL 收益，机制几乎同构；差别在于没有布局承诺结构，也没有"多样性升高却无益"的反例。
2. Curriculum Group Policy Optimization（CGPO, CVPR 2026, https://arxiv.org/abs/2605.17807）：在 T2I GRPO 中，按组内奖励方差提高混合成败提示的采样率，用的是同一信号；差别在于它在训练中做筛选，不研究起点覆盖，也不分解布局/外观。它是"实用价值"子主张必须对照的基线。
3. A First-Step Bias Restores Lost Diversity in Diffusion Model Distillation（ReSeed, https://arxiv.org/abs/2610.37110）：就是这里的 L 干预；只用 DINO/CLIP 多样性验证，不涉及 RL。
4. Visualizing Distribution Coverage in Generative Diffusion Models（https://arxiv.org/abs/2609.38853；作者机构未核实）：用 pass@k 测少步学生的覆盖收缩，发现分布匹配类比轨迹类收缩更多；不分解布局/外观，不研究后续 RL。
5. Distribution Matching Distillation Meets Reinforcement Learning（DMDR, https://arxiv.org/abs/2511.13649）：指出在蒸馏学生上直接做 RL 时，锚点贫乏会导致塌缩，并改为 DMD+RL 联合训练；没有对起点覆盖做受控分解。

```json
{
  "score": 6.0,
  "contribution_scores": {"importance": 6.5, "novelty": 7.0, "effectiveness": 6.0},
  "contribution_assessment": "主贡献：在扩散领域受控证明少步学生中与 RL 相关的覆盖收缩是布局性的，CLIP/DINO 多样性测不到它，组归一化 RL 在布局子任务上的收益由中间成功率提示占比决定。重要性 6.5：对多样性修法有判断价值，但 GenEval 上 RL 已能从极低起点饱和到 0.92-0.98，效应可能只体现在截断效率；诊断工具与 CGPO/DAPO 的组内方差信号基本重合。新颖度 7：扩散领域未检索到研究起点覆盖与后续 RL 关系的直接近邻，布局/外观分解和 P 反例是结构性适配；但混合成败提示机制已见于 2609.33780（LLM）和 CGPO（T2I）。有效性 6：第一步决定布局、退化组无信号这条链有依据；但最后一步偏置让 CLIP/DINO 升幅达到 L 的水平，与'后续步骤几乎不贡献多样性'的已有证据冲突；官方 GenEval 奖励为部分得分而非二值，退化组机制因此弱化；LLM 侧有 pre-RL pass@k 相同但 RL 结果不同的报告。效应大小待预研。",
  "feasibility": "pass",
  "feasibility_reason": "DiffusionNFT、TDM-R1、ReSeed 官方代码与 TDM/SD3.5-L-Turbo 权重都可得；第 0、1 关在 2×A100 上 3-4 天可完成；DiffusionNFT 报告约 150 GPU 小时达到 0.98，9 条 4 步 RL 在 8×A100 上 5 天内可信。未定的二值奖励实现、P 适配器训练目标、LoRA 蒸馏步数属于规范空白，不是资源不足。",
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "贡献门槛未达：重要性 6.5 / 新颖度 7.0 / 有效性 6.0，没有一项 ≥8",
    "Claim：核心反例 P（只在最后一步加偏置，CLIP/DINO 升幅不低于 L）与'多样性集中在第一步、后续步骤几乎不恢复多样性'的已有证据冲突；P 不可构造时，'外观多样性升高却无益'无法检验",
    "Claim：L 的实用价值与 RL 前诊断工具两个子主张缺少同任务强基线（A + CGPO/DAPO 式按奖励方差的提示筛选或课程、Pro-GRPO 扩组再剪枝），它们直接作用于同一个中间成功率占比",
    "Claim：机制按二值奖励推导，官方 GenEval RL 奖励是部分得分；brief 改用二值奖励偏离了官方配方，却未说明，DiffusionNFT 从 0.24 起点快速学习也削弱了'两极化是瓶颈'的前提"
  ],
  "novelty_conclusion": "在扩散领域，研究少步学生起点覆盖（按布局/外观分解）对后续组归一化 RL 影响的工作，检索中没有直接近邻，迁移加结构性适配可计 7；但组内混合成败信号这一机制已由 2609.33780（LLM）和 CGPO（T2I GRPO）确立，新意集中在分解和 P 反例上，达不到 8。",
  "closest_neighbors": [
    "Selecting Diverse SFT Traces Improves Post-RL Generalization (arXiv 2609.33780)",
    "Curriculum Group Policy Optimization: Adaptive Sampling for Unleashing the Potential of Text-to-Image Generation (arXiv 2605.17807, CVPR 2026)",
    "A First-Step Bias Restores Lost Diversity in Diffusion Model Distillation (arXiv 2610.37110)",
    "Visualizing Distribution Coverage in Generative Diffusion Models (arXiv 2609.38853)",
    "Distribution Matching Distillation Meets Reinforcement Learning (arXiv 2511.13649)"
  ]
}
```
