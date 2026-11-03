## 结论
2026-11-03，总体 score 5.0，verdict：needs_rethink。主贡献是一次方法学审计：给开思考 OPSD 画出准确率–漂移前沿，用它判断已发表的 token 级修法是在改方向，还是只是走得少。在一个修法扎堆的子领域里，这个审计有用。但它不够分量，原因有三：
- "按 √KL 坐标、在匹配 KL 下比较方法"是成熟的评测视角（奖励–KL 前沿、OPD 缩放、OPSD 漂移），新意只到增量水平；
- 核心预测与 AD-OPSD 自己报告的"超过基座"结果正面冲突；
- 事先固定的判别规则会把统计功效不足误读成"在前沿上"。

## Claim 判断
| 维度 | 分数 | 依据 |
|---|---|---|
| 重要性 | 6 | 若成立，"匹配漂移的 vanilla OPSD"会成为这个方向的必要对照，可以纠正一批修法论文的归因。但结论只覆盖 Qwen3-1.7B、训练上限 1,024、100 步、五个修法；在 OPSD 本身就退化的设置里，结论最多是"这些修法只是少伤害"。2609.20612 已表明换成直答 rollout 就能把损失变为增益，2610.18613 也已经质疑 OPSD 增益的来源，所以这一判断对领域的增量影响有限。 |
| 新颖度 | 6 | 以 √KL 为坐标比较方法的先例不少：奖励–KL 前沿（Gao et al. 2210.10760；DPO 2305.18290 的 frontier 图），KL 决定遗忘（RL's Razor 2509.04259），OPD 中准确率对 √KL 近似线性（2609.32722），OPSD 中把特权上下文当作漂移来研究（2610.07842）。同比例随机遮罩对照来自 2607.05184。把这些用到"裁决 OPSD token 级修法的收益来源"上，是可辨认的组合增量，但还谈不上独立的新机制或新现象。 |
| 有效性 | 5 | **现有支持：** 本项目单种子预研（分解后任一项都能复现 80%–90% 的退化；裁剪 0.1 加 AdamW 使损失缩放失效），2607.05184 附录 E（非特权 OPD，未逐条核验），AD-OPSD 优势随上下文收窄（512→2048 上 +7.5→+1.3，已核验）。这些只间接相容于"剂量"解释，收窄也可以由很多别的原因造成。**反证：** AD-OPSD 表 2 在 Qwen3-1.7B 上高于基座（AIME24 50.6 对 48.6，AIME25 40.6 对 38.1），在 1,024 上仍有 +5.3/+6.7。如果开思考 vanilla 前沿从基座单调下降，那么任何高于基座的点都不可能落在前沿上，brief 没有处理这一矛盾。**未知：** 前沿形状；修法的增益能否在本设置下复现；度量是否公平。 |

**判别规则的问题。**
- **"CI 含 0 即判为在前沿上"不是等价检验。** 384 题、Avg@4、3 种子时，单检查点标准误约 1–1.5 个百分点，前沿拟合本身还有误差，而 PW-OPSD 报告的增益只有 +1。功效不足会被直接计为支持主假设。必须事先给出等价界和功效估计，否则主 Claim 无法被判别。
- **对 AD-OPSD 而言，"由漂移减少解释"近乎同义反复。** 它的机制本来就是把门控 token 的目标插值到冻结基座，而漂移又在基座 rollout 上测量，所以它的低漂移是机制本身造成的，"机制解释不是收益来源"这一推论不成立。
- **"剂量"与"方向"缺少可操作的定义。** 在 AdamW 加裁剪 0.1 下，每步参数位移近似固定，作为稳健性检查的参数位移基本没有区分力。修法在同步数下 KL 更低，本身就是方向性质。可检验的命题只能是"准确率是 KL 的单变量函数，不论漂移由学习率还是目标函数产生"，brief 应据此重述。
- **直答前沿的"反转"缺少增量。** 2609.20612 已在同一检查点给出直答与开思考的符号反转，前沿形状只增加很少信息。
- **覆盖不足。** 同问题的强修法 Purified OPSD（2607.02234）和 ST-OPSD（2610.34005）没有纳入。限定为"token 级加权/遮罩修法"可以接受，但重要性会随之收窄。

**与原问题的关系：** 这是原问题的一个子问题，评价目标从"退化为何发生"收窄为"已有修法的收益来源"，转向本身不构成问题。原问题中"有害方向是什么""长度方向在论文间为何冲突"仍未回答。

**可行性：pass。**
- 代码路线：opsd-reference-study、PW-OPSD、E2-OPSD 三个仓库均可访问（HTTP 200）。AD-OPSD 没有代码，但规范与表 5/6 超参公开，可以独立复现，主要风险是复现保真度。
- 预算：27 次训练加 90 个检查点评测，约 330 A100 小时，在 8×A100、5 天之内。开发切分上的二选一和 E²-OPSD exemplar 参照臂没有计入成本，但量很小。
- 数据与标签：数据与按规则判分可得，不需要付费 API。漂移只需在固定基座 rollout 上做前向即可构造。

## 最高近邻
1. Scaling Properties of Same-Family On-Policy Distillation, https://arxiv.org/abs/2609.32722 。重叠：OPD 中准确率对 √KL 近似线性，坐标完全相同。差别：外部/同族教师，不比较修法，不涉及特权导致的退化。
2. Privileged Context as Drift in On-Policy Self-Distillation, https://arxiv.org/abs/2610.07842 。重叠：在 OPSD 中以相对基座的反向 KL 和参数更新几何作为分析轴。差别：比较的是特权上下文设计（Qwen2.5-7B、持续学习），不是 token 级修法，也不涉及开思考退化。
3. Rethinking On-Policy Self-Distillation for Thinking Models, https://arxiv.org/abs/2607.05184 。重叠：开思考特权 OPSD 的退化与分叉位置诊断，同比例随机遮罩对照。差别：没有在匹配漂移下裁决已发表修法。
4. What Does Privileged Information Add to On-Policy Self-Distillation?, https://arxiv.org/abs/2609.20612 。重叠：同一代码与数据；匹配的损失干预基本不改变学生行为；直答与开思考在同一检查点符号反转。差别：没有构建漂移前沿，也没有逐个检验修法。
5. Diagnosing and Mitigating Thinking Collapse in OPSD (AD-OPSD), https://arxiv.org/abs/2607.10805 （同类审计视角另见 Does self-distillation improve reasoning?, https://arxiv.org/abs/2610.18613 ）。重叠：被审计的主要对象，同模型同任务。差别：它在固定步数下与 vanilla 比较并报告高于基座；本方案的前沿假设必须解释这一点。

```json
{
  "score": 5.0,
  "contribution_scores": {"importance": 6.0, "novelty": 6.0, "effectiveness": 5.0},
  "contribution_assessment": "主贡献是用准确率–√KL 前沿审计开思考 OPSD 的 token 级修法，判断收益来自方向还是剂量。重要性 6：若成立，能确立匹配漂移的 vanilla 对照；但设置窄（1.7B、1,024、五个修法），2609.20612 和 2610.18613 已部分质疑 OPSD 增益来源。新颖度 6：KL 前沿是成熟评测视角（2210.10760、DPO、RL's Razor），且已用于 OPD（2609.32722）和 OPSD 漂移（2610.07842），本方案是迁移组合。有效性 5：支持证据只有单种子预研、非特权 OPD 的随机遮罩结果、AD-OPSD 优势收窄这类间接线索；AD-OPSD 在 Qwen3-1.7B 上高于基座（50.6 对 48.6、40.6 对 38.1），与单调下降前沿上的'在前沿上'直接矛盾。判别规则以 CI 含 0 判'在前沿上'，缺等价界和功效分析；AD-OPSD 的锚定基座机制使漂移解释近乎同义反复。",
  "feasibility": "pass",
  "feasibility_reason": "三个仓库可访问，AD-OPSD 可按公开规范与表 5/6 独立复现；27 次训练加 90 个检查点评测约 330 A100 小时，在 8×A100、5 天内；按规则判分，无 API 成本；漂移只需在固定基座 rollout 上做前向。",
  "verdict": "needs_rethink",
  "fatal_blockers": [
    "贡献门槛不满足：重要性 6、新颖度 6、有效性 5，没有两项达到 8；KL 匹配前沿是成熟的评测视角，迁移到 OPSD 修法审计只是增量。",
    "Claim 阻断：'CI 含 0 即在前沿上'不是等价检验；在 384 题、Avg@4、3 种子的功效下，+1 到 +2 个百分点的方向效应会被误判为'可由漂移完全解释'。",
    "Claim 阻断：AD-OPSD 自报在 Qwen3-1.7B 上高于基座，与单调下降前沿上的'在前沿上'预测矛盾，brief 未处理；且 AD-OPSD 以锚定基座为机制，用基座 rollout 上的 KL 衡量剂量，无法区分'漂移减少'与'其机制'。",
    "Claim 阻断：在 AdamW 加裁剪下，同步数的 KL 差异本身由方向产生，'剂量与方向'缺少可操作的定义；参数位移的稳健性检查基本没有区分力。"
  ],
  "novelty_conclusion": "在匹配 KL 下比较方法、以 √KL 作坐标，已在 RLHF（2210.10760、DPO）、遗忘（2509.04259）、OPD（2609.32722）和 OPSD 漂移（2610.07842）中使用；把它用于裁决 OPSD token 级修法尚未见到，但属于可辨认的组合增量，不是独立的新机制或新现象。",
  "closest_neighbors": [
    "Scaling Properties of Same-Family On-Policy Distillation (2609.32722)",
    "Privileged Context as Drift in On-Policy Self-Distillation (2610.07842)",
    "Rethinking On-Policy Self-Distillation for Thinking Models (2607.05184)",
    "What Does Privileged Information Add to On-Policy Self-Distillation? (2609.20612)",
    "Diagnosing and Mitigating Thinking Collapse in On-Policy Self-Distillation (2607.10805)"
  ]
}
```
