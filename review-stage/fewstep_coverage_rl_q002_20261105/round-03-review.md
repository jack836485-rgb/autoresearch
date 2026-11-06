## 结论
2026-11-05：总体 score 6.3，verdict = promising_needs_revision。主贡献是一个扩散领域的受控发现：少步学生的覆盖收缩集中在第一步决定的布局维度，并通过退化组按子任务限制后续 RL；附带一个工具，用 RL 前的非退化组比例预测各子任务的 RL 收益。扩散领域确实没有这样的受控研究，但这条主线的骨架（起点覆盖或多样性决定 RL 能学到什么、零方差组没有梯度）在 LLM 里已经确立。真正新的部分是"布局对外观"的分解加上用第一步适配器构造受控起点，分量还够不到 8。先验链条里最关键的一环也偏弱：TDM-R1 的生成器梯度来自跨提示学习的可微替代奖励，不来自组内优势；而且 TDM 属于 Apple 发现覆盖保持较好的轨迹类目标。三项分数达不到 8/7/6 门槛。

## Claim 判断
| 维度 | 分数 | 依据 |
|---|---|---|
| 重要性 | 6.5 | 少步学生正被直接当作在线 RL 起点（TDM-R1、Flash-DMD、DMDR）。如果"布局覆盖缺口按子任务限制 RL"成立，会改变 RL 前要不要先恢复多样性的判断，这有明确价值。但 GenEval 上的 RL 普遍能做到 0.92–0.98（TDM-R1 从 61% 到 92%；DiffusionNFT 在无 CFG 下从 0.24 到 0.98），说明起点覆盖对终点的限制可能是软的，影响多半体现在训练速度和少数子任务上，范围有限。结果只在 GenEval 型二值验证器和一个学生上，外推面窄。 |
| 新颖度 | 7.5 | 我检索到的扩散工作要么只测覆盖不研究后训练（Apple 2609.38853），要么只修多样性、只用多样性指标验证（ReSeed、DP-DMD、Distilling Diversity），要么只改 RL 配方（TDM-R1、DiverseGRPO、AdaGRPO）。SiD few-step 只有断言。按跨领域规则，这项迁移在目标领域成立，新颖度不低于 7。布局/外观分解、"第一步承诺"给出的按子任务预测，以及在 k=1 相近的条件下用第一步偏置构造起点，都算有内容的结构性适配。但"起点覆盖或 pass@k 预测 RL 效率、零方差组无信号"在 LLM 中已有直接表述（2609.33780；Towards A Better Initial Policy Model；Limit of RLVR；2606.18487 的零优势组分析）。工具部分基本就是这一结论换到图像上，所以不到 8。 |
| 有效性（先验合理性） | 6.0 | 支持的依据有：第一步决定结构、多样性损失集中在高噪声第一步，这一点有 2503.10637、ReSeed、DP-DMD 三方独立证据，适用于 SD3/SD3.5 系 DMD 类学生；GenEval 的计数和位置子任务基座分最低、可提升空间最大，这一点成立。迁移条件有两条，都偏弱。(a) 机制要求退化组真正卡住学习。可是 TDM-R1 的生成器优化的是可微替代奖励，组内对比只用来给替代奖励构造偏好对，替代奖励可以跨提示泛化，所以"退化组让对应子任务学不到"到这里需要额外的跳跃。brief 把它列为反向因素，但没有给出这一环成立的依据。(b) Apple 原文指出轨迹类和一致性类目标在大 k 下更能保住教师覆盖，而 TDM 正是轨迹分布匹配，所选学生可能恰好是布局缺口最小的那个。这条邻近证据和"该学生有可操作的布局缺口"这一前提方向相反，但还不是直接反证（第 0 关会测）。没有发现直接推翻关键假设的受控结果。 |
| 待预研 | — | TDM-SD3.5-M 学生在布局子任务上的覆盖缺口到底多大；适配器蒸馏进 LoRA 后，在 k=1 总分相差不超过 1 个百分点时，布局覆盖还剩多少差距；α=1.5 能否保住质量；终点收益和中途收益的差异幅度；RL 种子方差相对起点间差异有多大。 |

- **与起点问题的关系：** 这是子问题。它回答了"覆盖收缩的下游后果"中的 RL 一支，以及收缩发生在哪个结构维度。起点问题中，修法在多样性指标以外是否有效，只在布局维度部分回答；部署场景下 CFG 的作用、best-of-k 的实际收益等其他后果仍未回答。转向本身不是阻断。
- **实验能否判别主张：** 目前只能部分判别。(1) 起点只有 4 个，每个子任务内跨起点的秩相关样本量 n=4，谈不上显著；24 个点不独立，而且其中 4 个起点只有单种子，GenEval 分项在截断 RL 下的种子方差可能盖过起点间差异。(2) "布局与外观子任务依赖不同"与净空（headroom）混杂：布局子任务的 k=1 更低、可提升空间更大，非退化组比例又和每个提示的成功率 p 机械相关。只约束总分 k=1 相差不超过 1 个百分点，不足以排除"收益只是由各子任务 k=1 或 p 决定"这一竞争解释，需要按子任务控制 k=1 或把它作为协变量。(3) 把"G=48 得到同等收益"当作推翻条件，逻辑上有歧义：G=48 本身也会提高非退化组比例。G=48 若与 α 起点落在同一条曲线上，其实是支持"非退化组"机制、否定"起点覆盖不可替代"，brief 要把这两个子主张分开写。(4) 留出的组合基准（GenEval2/T2I-CompBench）能减轻饱和，这是对的。
- **可行性：pass。** TDM-R1 有官方代码和起点 LoRA（ICML 2026，含 GenEval 的 SD3.5-M 配置），GenEval 奖励链路有公开实现。ReSeed 其实有官方仓库（github.com/TWWinde/ReSeed，HF 上的 Wenwu2000/ReSeed），brief 写"没有官方代码"是错的，这一点只会让实现更容易，不过要从 SD3-M DMD 和 FLUX 学生移植到 TDM-SD3.5-M LoRA 上。第 0 关的算力可能被低估：SD3.5-L 教师 28 步加 CFG，553×64 张，单这一项就可能上百 A100 小时，三对模型加起来在 2×A100 上大约要数天。Z-Image-Turbo 对应的多步教师权重是否公开需要核实；缩小 N 或减少模型对就能落在预研约束内。正式实验 7 条 RL，按每条半天估计，但单条耗时没有实测，处在 8×A100、不超过 5 天的边缘。
- **阻断：** 贡献门槛未通过（最高分 7.5，不到 8），这是阻断项，不能放行。

## 最高近邻
1. **Visualizing Distribution Coverage in Generative Diffusion Models**（Apple，2609.38853）https://arxiv.org/abs/2609.38853 。重叠点：少步学生的 pass@k 被教师反超，覆盖收缩与蒸馏目标有关（轨迹类目标保持得更好）。差别：不研究后续 RL，不做布局/外观分解。
2. **A First-Step Bias Restores Lost Diversity in Diffusion Model Distillation**（ReSeed，2610.37110）https://arxiv.org/abs/2610.37110 。重叠点：第一步是多样性瓶颈，第一步偏置适配器能恢复多样性。差别：只用 DINO 多样性验证，不涉及覆盖对 RL 的后果。
3. **TDM-R1: Reinforcing Few-Step Diffusion Models with Non-Differentiable Reward**（2603.07700）https://arxiv.org/abs/2603.07700 。重叠点：同一学生、同一 RL 配方，用组内偏好对训练替代奖励。差别：改进的是配方，没有分析起点覆盖。
4. **Selecting Diverse SFT Traces Improves Post-RL Generalization**（2609.33780）https://arxiv.org/abs/2609.33780 ，以及 **Towards A Better Initial Policy Model for Scalable Long-CoT RL**（ACL Findings 2025）https://aclanthology.org/2025.findings-acl.397.pdf 。重叠点：起点多样性和 pass@k 预测 RL 收益，结论同构。差别：研究文本推理，没有图像的第一步布局承诺，也没有按子任务的预测。
5. **Diversity-Preserved Distribution Matching Distillation**（DP-DMD，2602.03139）https://arxiv.org/abs/2602.03139 ；**Few-Step Diffusion via Score identity Distillation**（2505.12674）https://arxiv.org/abs/2505.12674 。重叠点：第一步负责全局结构和多样性；SiD 断言多样性对后续 RL 重要。差别：都没有受控的"覆盖到 RL 收益"实验。

```json
{
  "score": 6.3,
  "contribution_scores": {"importance": 6.5, "novelty": 7.5, "effectiveness": 6.0},
  "contribution_assessment": "主贡献：在扩散领域受控地证明少步学生的覆盖收缩集中在第一步决定的布局维度，并通过退化组按子任务限制后续 RL；附带用 RL 前非退化组比例预测子任务收益的工具。重要性 6.5：少步 RL 起点是现实问题，但 GenEval 上 RL 普遍能做到 0.92–0.98，起点对终点的限制可能是软的，范围限于二值验证器和单一学生。新颖度 7.5：扩散领域没有这样的受控研究，按跨领域规则不低于 7；布局/外观分解和第一步受控起点是结构性适配，但核心论断与 LLM 中的起点覆盖和零优势组结论同构，工具部分基本是直接迁移，所以不到 8。有效性 6.0：第一步决定结构有三方证据；但 TDM-R1 的生成器梯度来自跨提示泛化的替代奖励，'退化组卡住学习'缺少依据；Apple 发现轨迹类目标保持覆盖较好，而所选 TDM 学生正是轨迹类，可能缺口最小。待验证：布局缺口大小、蒸馏后在 k=1 相近时的覆盖差、种子方差。另有 Claim 问题：每个子任务只有 4 个起点、布局与外观的差异与净空混杂、G=48 推翻条件含义有歧义。",
  "feasibility": "pass",
  "feasibility_reason": "TDM-R1 官方代码、起点 LoRA 与 GenEval 奖励链路都已公开，ReSeed 也有官方仓库（brief 写的'无官方代码'有误），移植到 TDM-SD3.5-M LoRA 属于常规工作；第 0 关的教师采样算力可能被低估到数倍，但缩小 N 或减少模型对后可以落在 2×A100 预研内；正式 7 条 RL 的单条耗时没有实测，处在 8×A100、不超过 5 天的边缘。",
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "贡献门槛未过：重要性 6.5、新颖度 7.5、有效性 6.0，最高一项不到 8。核心'起点覆盖限制 RL'在 LLM 中已确立，扩散侧的新增主要是布局/外观分解，分量不足",
    "Claim 判别力不足：每个子任务只有 4 个起点，秩相关无法显著；布局与外观的差异与子任务净空、各子任务 k=1 混杂，只匹配总分 k=1 排除不了'收益由各子任务 p 决定'的竞争解释"
  ],
  "novelty_conclusion": "扩散或少步文生图领域没有检索到'起点覆盖到 RL 收益'的受控研究，迁移在目标领域成立，布局/外观分解是结构性适配；但核心论断与 LLM 起点多样性文献（2609.33780、Towards A Better Initial Policy Model、Limit of RLVR）同构，非退化组比例这一工具没有超出直接迁移，新颖度 7.5。",
  "closest_neighbors": [
    "Visualizing Distribution Coverage in Generative Diffusion Models (2609.38853)",
    "A First-Step Bias Restores Lost Diversity in Diffusion Model Distillation (2610.37110)",
    "TDM-R1: Reinforcing Few-Step Diffusion Models with Non-Differentiable Reward (2603.07700)",
    "Selecting Diverse SFT Traces Improves Post-RL Generalization (2609.33780)",
    "Diversity-Preserved Distribution Matching Distillation for Fast Visual Synthesis (2602.03139)"
  ]
}
```
