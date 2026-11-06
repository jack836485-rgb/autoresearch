## 结论
2026-11-05，总体 score 4.8，verdict：needs_rethink。主贡献是在少步扩散上做一个受控验证：RL 起点的覆盖会限制 RL 能达到的上限。分量不够，原因有两点。第一，LLM 上已经有理论（Coverage Principle）和受控实证（AESL、PriFT、OPD）建立了"起点覆盖或多样性决定 RL 收益"这一认识，本方案主要是把它换到图像模态，外加一个更干净的干预。第二，选定的 RL 配方 TDM-R1 不是 GRPO：它用确定性轨迹、学习式代理奖励，并带着对教师的分布匹配正则。所以主张依赖的"组内奖励方差"机制和噪声对照臂在这个配方里都无法对应，实验判别不了要证的机制。

## Claim 判断
| 维度 | 分数 | 依据 |
|---|---|---|
| 重要性 | 6 | "蒸馏学生加在线 RL"确实是在用的流水线（TDM-R1 在 Z-Image-Turbo 上做 RL，另有 RTDMD、Flash-DMD、AdvDMD）。Apple 2609.38853 已核实 DMD 类学生会损失大 k 覆盖。但结论若成立，只是给出"选起点时看 pass@k / 先恢复多样性"这样的选择建议，影响限于起点选择。它也没回答起点问题里的"同源"部分，达不到 8。 |
| 新颖度 | 5.5 | 扩散方向上，我没检索到以起点覆盖为受控变量的 RL 研究，这一点属实。但 LLM 侧几个近邻已经做过：Coverage Principle（2510.15020）把覆盖确立为后训练成功的必要条件；AESL（ICLR 2026）表明多样性峰值的 SFT 检查点 RL 后最好；PriFT（2606.09396）在相同 DAPO 设置下比较了不同起点；2608.24949 直接测了起点覆盖对 RL 的约束。SiD 原文也已明说"保持多样性对 RL 探索关键"。剩下的新意是换模态，加上"权重不变、只用 ReSeed 改第一步"这种干预形式，属于可辨认但常规的增量。 |
| 有效性 | 5 | 现有依据：学生覆盖收缩已被核实（Apple）；GRPO 需要组内方差，这是通用机理；LLM 上多样性起点有 RL 后优势，算邻近证据；ReSeed 能提高 DINO 多样性。迁移条件不成立的地方：(1) TDM-R1 用确定性 ODE 轨迹和成对组偏好来训练代理奖励，生成器目标是"代理奖励 + 对教师的反向 KL（tdm_weight=0.3）"，不是 GRPO 的组内归一化优势，"组内方差更晚塌缩"这个预测在该配方里没有直接对应量；(2) RL 中持续的教师分布匹配项本身就在塑造覆盖，可能把两个起点的差异抹平，也可能把差异放大，而这和"探索覆盖"不是同一个原因；(3) GenEval 上 TDM-R1 能把 SD3.5-M 推到 0.92，接近天花板，大 k pass@k 差异容易被压缩；(4) DINO 多样性能否转化为验证器意义上的覆盖，作者自己也标为未知。另外，SDPO 被引作"GRPO 因多样性不足而不稳定"，这是误引：它讨论的是 DDPO 类方法在少步下状态空间有限。 |

与原问题的关系：这是子问题，转向本身不扣分。原问题里"单样本增益与覆盖损失是否同源"以及"现有修法是否只治症状"都没有回答。

实验能否判别主张：现在的设计判别不了。
- 臂 (c)"提高 RL 的 SDE 噪声"在 TDM-R1 里不存在。TDM-R1 默认走确定性轨迹，随机采样只是论文中一个更差的消融变体，所以要排除的竞争解释"只是更多随机性"在主配方里没法检验。
- 机制指标（组内方差）和配方不匹配。真正的 GRPO 实现 Flow-GRPO 被放进了正式实验，预研阶段没有。
- 冻结适配器之后，RL 期间分布匹配项（fake score 跟踪学生分布）和适配器会相互作用，这是另一个解释终点差异的来源，没有对应的对照。
- 预研只跑单种子。终点上 1–3 个点的奖励或 pass@k 差异分不清是起点效应还是 RL 种子噪声，go/no-go 本身的可信度不足。
- "用途"那条主张（先恢复多样性再 RL 是一条处方），没有和 RL 内的多样性或探索方法比较，例如 DiverseGRPO、感知熵约束（2605.12112）、Pro-GRPO、ExploreNet。这条主张因此没有被检验。

可行性：pass，但前提有误需要更正。
- 我核验了公开仓库：只有 SD3.5-M 的参考训练实现（sd3_pipeline_tdmr1.py、train_tdmr1_pub.py、GenEval 的 8 卡 G=24 脚本）。Z-Image 侧只放出了基于 Z-Image-Turbo 的推理 LoRA，没有 Z-Image 训练代码。download_models.sh 下载的是 SD3.5-M 和各个奖励模型，不包含 Z-Image 学生。所以 brief 中"含 Z-Image 少步 RL 训练代码"不属实。
- 预研要么改用 SD3.5-M 路线（它的学生是 TDM 类目标，覆盖损失可能更小，操纵空间未知），要么自行把配方移植到 6B 的 Z-Image-Turbo（DMDR 学生，确有覆盖收缩）。后者要在 2×A100 上同时放生成器、fake score 和代理奖励，再从 8 卡配方缩放下来，工作量和"3–5 天"的估计都没有实测依据。
- GenEval 提示和检测器公开，ReSeed 只需要提示-噪声对和教师，独立实现是可行的。

## 最高近邻
1. Visualizing Distribution Coverage in Generative Diffusion Models（Apple，https://arxiv.org/abs/2609.38853）：用 pass@k 揭示少步学生覆盖收缩、DMD 类目标代价最大。只做测量，不研究下游 RL。
2. The Coverage Principle（https://arxiv.org/abs/2510.15020）以及 Demystifying RL Post-Training of LMs（https://arxiv.org/abs/2608.24949）：理论上和实证上都表明起点覆盖决定 RL 或 Best-of-N 能否成功。模态是 LLM，干预不是"同权重只改覆盖"。
3. Getting Your LLMs Ready for RL with Lightweight SFT（AESL，ICLR 2026，https://iclr.cc/virtual/2026/poster/10006544）和 PriFT（https://arxiv.org/abs/2606.09396）：在 LLM 上受控比较不同起点，结论是多样性或覆盖更高的起点 RL 后更好，与本 Claim 同构。
4. TDM-R1（https://arxiv.org/abs/2603.07700，代码 github.com/Luo-Yihong/TDM-R1）：少步学生 RL 的强配方，含教师分布匹配正则，用确定性轨迹。没有把起点覆盖作为变量，它本身也是混杂源。
5. ReSeed（https://arxiv.org/abs/2610.37110）及 SiD few-step（https://arxiv.org/abs/2505.12674）：前者给出第一步偏置适配器，未做 RL；后者明确断言"保持多样性对蒸馏后 RL 探索关键"，但没有对照实验。

```json
{
  "score": 4.8,
  "contribution_scores": {"importance": 6.0, "novelty": 5.5, "effectiveness": 5.0},
  "contribution_assessment": "主贡献是在少步扩散上受控检验'RL 起点覆盖限制 RL 上限'。重要性 6：流水线真实存在，但成功后只给出起点选择建议。新颖度 5.5：LLM 侧的 Coverage Principle、AESL、PriFT、2608.24949 已建立同构结论，SiD 已作同样断言，剩下的是换模态加 ReSeed 式干预。有效性 5：学生覆盖收缩和 GRPO 需要组内方差都有依据，但所选 TDM-R1 不是 GRPO（确定性轨迹、代理奖励、对教师的反向 KL 正则），机制无法对应；分布匹配正则可能抹平或混淆起点差异；GenEval 接近天花板；DINO 多样性能否转化为验证器覆盖未知。",
  "feasibility": "pass",
  "feasibility_reason": "GenEval、检测器和 ReSeed 的独立实现都可获得，SD3.5-M 版 TDM-R1 训练代码公开。但仓库没有 Z-Image 训练代码（只有基于 Z-Image-Turbo 的推理 LoRA），要么改用 SD3.5-M（TDM 学生的覆盖损失可能更小），要么自行把配方移植到 6B 模型并从 8 卡 G=24 缩到 2×A100，3–5 天的估计未经实测。",
  "verdict": "needs_rethink",
  "fatal_blockers": [
    "贡献分量不足：重要性 6、新颖度 5.5，没有两项达到 8；核心认识在 LLM 侧已有理论和受控实证（Coverage Principle、AESL、PriFT、2608.24949），SiD 已有同一断言",
    "Claim 阻断：选定的 TDM-R1 用确定性轨迹和代理奖励，并带教师分布匹配正则，不是 GRPO 组内优势；'组内方差更晚塌缩'的机制预测和 SDE 噪声对照臂 (c) 在该配方中无法实施或无对应量",
    "Claim 阻断：RL 中的教师分布匹配项与冻结适配器相互作用，是解释终点差异的竞争来源，没有对照；单种子预研分不清小幅终点差异与 RL 种子噪声",
    "事实更正：TDM-R1 公开仓库只含 SD3.5-M 训练代码，没有 Z-Image 训练代码，预研路线需要重定",
    "'处方'用途未与 RL 内多样性和探索方法（DiverseGRPO、感知熵约束、Pro-GRPO、ExploreNet）比较"
  ],
  "novelty_conclusion": "扩散方向上没有找到以起点覆盖为受控变量的 RL 研究，但 LLM 上的同构结论已经确立，SiD 也已提出同一主张；本方案的新意限于换模态加第一步适配器式干预，属于常规增量。",
  "closest_neighbors": [
    "Visualizing Distribution Coverage in Generative Diffusion Models (arXiv 2609.38853)",
    "The Coverage Principle: How Pre-Training Enables Post-Training (arXiv 2510.15020)",
    "Getting Your LLMs Ready for Reinforcement Learning with Lightweight SFT (ICLR 2026); PriFT (arXiv 2606.09396)",
    "TDM-R1: Reinforcing Few-Step Diffusion Models with Non-Differentiable Reward (arXiv 2603.07700)",
    "A First-Step Bias Restores Lost Diversity in Diffusion Model Distillation (arXiv 2610.37110); Few-Step Diffusion via Score identity Distillation (arXiv 2505.12674)"
  ]
}
```
