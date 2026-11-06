## 结论
2026-11-05，总体 score 4.5，verdict：needs_rethink。

主贡献分两部分。一是认识：跨尺度扩散 OPD 的伪影有一个必要成因来自"教师在学生状态上不可靠"。二是工具：自适应重加噪，用来保留双分支 CFG。两部分目前都不够：
- 认识部分：GFD 自己的固定状态 KL 表里已有不利证据。
- 工具部分：机制上被 DMD/VSD 式重加噪和时间步自适应覆盖；它要解决的"失去可调引导"有已知的廉价替代，即 w 条件化的引导蒸馏，而 brief 夸大了 GFD 在这方面的代价。

## Claim 判断
| 维度 | 分数 | 依据 |
|---|---|---|
| 重要性 | 6.0 | 如果成立，会修正 GFD 的归因：GFD 只怪容量加 CFG 放大，没有分离状态可靠性，而它在 2.2 节自己引用了 Xin et al. 来说明学生状态上教师不可靠。这有真实价值，但影响有限，原因有三。① GFD 学生并没有完全失去引导：部署时 w=2，图 6 做了 w 扫描，只是增量语义变小。② 想要可调引导，可以直接用 w 条件化的折叠蒸馏（Meng et al. 2023），未必需要回到双分支。③ 负提示的价值，在 GFD 的评测里没有被证明是瓶颈。 |
| 新颖度 | 5.5 | 用"状态 × 目标"的 2×2 去分离状态成因，在跨尺度扩散 OPD 里是可辨认的新问题。但机制本身新意有限：<br>- "把学生样本加噪到扩散后的边缘分布，让教师的分数可靠"是 VSD/DMD/Diff-Instruct 的核心论证；<br>- 按状态自适应选噪声级，有 Time-Shift Sampler 的先例；<br>- 噪声-去噪投影已在 Any-OPD/Poly-OPD 中出现；<br>- 用教师在相邻噪声级上的预测自洽性当可靠性信号，属于常规启发式；<br>- 教师轨迹状态这一臂就是标准离策略 KD。 |
| 有效性 | 4.5 | **现有支持依据：** LLM OPD 中教师在学生前缀上不可靠的证据（SKD、AC-OPD 等），但模态不同；扩散教师在中高噪声下本来就覆盖了整个高斯平滑空间，迁移条件没有论证。有一条对本题有利的混杂：PDM M→M 不出伪影，而其中教师与学生同基座、状态天然兼容。<br>**直接反证：** GFD 表 1 的 KL 正是在教师轨迹这类可靠状态上测的。PDM/split-KL L→M 在这些状态上的分支 KL 是 0.023/0.022 和 0.021/0.020，与 M→M 的 0.017/0.023 同量级，组合 KL 却是 0.063/0.074，而 M→M 为 0.041。也就是说，在可靠状态上，双分支目标照样因为失去误差抵消而放大误差。本题要预测"换状态后双分支接近 GFD"，就需要换状态能把残差 d 压低一个量级，目前没有任何依据。<br>**自适应重加噪的两个问题：** ① 信号能预测教师不可靠，不等于能预测重加噪的收益（诊断与修法之间的缺口）。② 离流形状态被推到更高噪声后，恰恰是产生纹理伪影的低噪声段失去监督，可能直接抵消收益。 |

**与原问题的关系：** 本题回答原问题中"状态偏离"这一条因果分支。容量与 CFG 放大各占多少，仍只是部分回答，这一点本身不构成阻断。

**实验能否判别主张：** 判别力不足，有四处问题。
1. 教师轨迹状态这一臂把"监督可靠"和"暴露偏差"（训练在教师状态、部署在学生状态）混在一起。伪影不变时，不能推出"纯容量解释"。重加噪臂同样会把"低噪声监督缺失"和"状态不可靠"混在一起。
2. 预研用 SD3.5-L 基座做纯压缩，与 GFD 出现伪影的设置（Flow-GRPO 分任务大教师）不同，第一关很可能复现不出伪影，从而回答不了问题。
3. "保留可调引导"的主张缺两组强对照：w 条件化的 GFD（Meng 式），以及 GFD 自身的 w 扫描。负提示测试没有定义指标。
4. 与 GFD 对比时应拆开外推目标（λ=1.25）：它与状态选择正交，也可以加到双分支上，否则"接近 GFD"不可比。

另外有一处小事实错误：DiffusionOPD 其实有官方代码（ali-vilab/DiffusionOPD），brief 写成没有。

**可行性：** pass，但有条件。
- 实现路线可信：GFD 官方 VeOmni 代码已公开训练代码，切换损失和监督状态只需改数据流；8B 教师推理加 2.5B 全参训练，在 80G 卡上配合分片是现实的。
- 关键资源缺口：README 写明蒸馏 checkpoint 尚未发布，配置需要"SD3.5 Large experts"，分任务 RL 大教师没有公开。自训教师时，GFD 报告 M 规模上直接 Flow-GRPO 约 160 H100 小时，L 规模更高，超出预研 2×A100 约 80 小时的预算，只能放进正式预算。
- 预研第一关存在不复现的风险。

## 最高近邻
1. GFD-OPD（https://arxiv.org/abs/2609.39692）：同任务、同模型对、同指标，固定状态 KL 已在教师轨迹和真实加噪状态上测过，并引用了教师在学生状态上不可靠的论点。差别是它没有把监督状态当作干预变量；学生部署时仍带 w=2 的 CFG，负提示未测。
2. PDM / Rethinking CFG in On-Policy Diffusion Distillation（https://arxiv.org/abs/2607.24731）：分支感知的 OPD 目标，主打跨引导尺度稳健，是"保留双分支"的现有方法。差别是它不处理跨尺度，也不处理状态可靠性。
3. Any-OPD（https://arxiv.org/abs/2608.03316）：用教师的噪声-去噪投影，把学生样本拉到教师流形，并按噪声级匹配。差别是强度固定、作用在最终样本上，面向异构模型，不涉及 CFG 分支。
4. DMD / DMD2（https://arxiv.org/abs/2311.18828）、VSD 类分数蒸馏：把学生样本重加噪后用教师分数监督，这正是"重加噪让教师可靠"的原型；DMD2 同样把 CFG 折进学生。差别是它们是单步生成器蒸馏，不是按状态自适应的 OPD。
5. On Distillation of Guided Diffusion Models（Meng et al., https://arxiv.org/abs/2210.03142）：用 w 条件化的学生吸收引导，同时保留可调引导尺度，可直接作为"保留可控性"主张的替代方案与对照。

（另有 Time-Shift Sampler，https://arxiv.org/abs/2305.15583：按状态的实际方差自适应地选择时间步，是"按状态选噪声级"的机制先例。）

```json
{
  "score": 4.5,
  "contribution_scores": {"importance": 6.0, "novelty": 5.5, "effectiveness": 4.5},
  "contribution_assessment": "主贡献是'跨尺度扩散OPD伪影部分来自教师在学生状态上不可靠'的认识，加上用自适应重加噪保留双分支CFG的工具。重要性有限：GFD学生部署时仍带w=2的CFG并做了w扫描，w条件化折叠蒸馏可廉价保留可调引导，负提示价值未证。新颖度有限：重加噪到扩散边缘分布是DMD/VSD的核心思想，按状态选噪声级有Time-Shift Sampler先例，Any-OPD已有噪声-去噪投影，教师状态臂即离策略KD。有效性缺依据：GFD表1在教师轨迹这类可靠状态上，双分支L→M的分支KL与M→M同量级（约0.02），组合KL仍为0.063/0.074（M→M为0.041），说明失去抵消后的放大在可靠状态上依然存在，换状态能否把残差d压到接近GFD没有依据；LLM侧证据迁移到扩散的条件未论证；重加噪会去掉产生纹理伪影的低噪声段监督；可靠性信号只预测教师不可靠，不预测修法收益。",
  "feasibility": "pass",
  "feasibility_reason": "GFD官方VeOmni训练代码已公开，切换损失与监督状态只需改数据流，2.5B全参训练加8B教师推理在80G卡上配合分片可行。但GFD所用的Flow-GRPO分任务SD3.5-L教师未公开（README仅发布训练代码），自训教师成本超过L规模下160 H100小时量级，超出预研预算，只能纳入正式预算；预研改用基座L做纯压缩可能复现不出伪影。",
  "verdict": "needs_rethink",
  "fatal_blockers": [
    "有效性：GFD表1显示，在教师轨迹这类可靠状态上，双分支目标的组合误差放大依然存在（分支KL约0.02，组合KL 0.063/0.074，M→M为0.041），'换成可靠状态后双分支接近GFD'这一核心预测缺少依据，且有直接反证",
    "Claim判别：教师轨迹状态臂混入了暴露偏差，重加噪臂混入了低噪声段监督缺失，'伪影不变则为纯容量解释'的推翻逻辑不成立",
    "Claim/基线：'保留可调引导'缺少w条件化折叠蒸馏（Meng et al. 2023）和GFD自身w扫描这两组强对照，brief夸大了GFD失去CFG的程度",
    "新颖度：重加噪让教师可靠属于DMD/VSD/Any-OPD已有机制，自适应选噪声级有Time-Shift Sampler先例，剩余新意主要是一个启发式阈值",
    "预研设置：GFD的RL大教师未公开，基座L到M的纯压缩可能复现不出伪影，go/no-go第一关有失效风险"
  ],
  "novelty_conclusion": "把监督状态当作跨尺度扩散OPD失败成因的因果检验是可辨认的增量问题；作为方法，重加噪与按状态自适应选时间步均有直接先例（DMD/VSD、Any-OPD、Time-Shift Sampler），保留可控性也有w条件化蒸馏这一已知替代，新意不足以支撑主会贡献。",
  "closest_neighbors": [
    "GFD-OPD: Guidance-Folded On-Policy Distillation of Diffusion Models Across Scales (arXiv 2609.39692)",
    "Rethinking Classifier-Free Guidance in On-Policy Diffusion Distillation / PDM (arXiv 2607.24731)",
    "Any-OPD: Heterogeneous On-Policy Distillation for Flow-Matching Models via Representation-Space Bridging (arXiv 2608.03316)",
    "One-step Diffusion with Distribution Matching Distillation (DMD, arXiv 2311.18828)",
    "On Distillation of Guided Diffusion Models (arXiv 2210.03142)"
  ]
}
```
