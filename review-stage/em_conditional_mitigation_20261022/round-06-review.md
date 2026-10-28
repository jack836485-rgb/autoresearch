## 结论

评审日期 2026-10-26。**score 6.0 / 10，verdict: promising_needs_revision。**

"按通用失配选出的早停检查点在训练上下文 cue 下是否仍有条件失配"这个实证问题，目前确实没人测过：2604.25891 测了稀释、事后 HHH 微调和 inoculation，没有早停；ContextLift 明确写着"Checkpoint last; no early stopping"；2605.12199 的早停只在自己的 240 题补全基准和 TruthfulQA 上评测，没有 cue 提示。baseline 都在同一领域、同一任务，复现路线都核验过（contextlift 仓库有 `configs/{security,legal,medical}/baseline.yaml`，`save_steps` 可配，共 675 步；em-not-magical 仓库有 sec3–sec5），预算也够。

但新颖性边界还没守住，有两处 claim blocker：

1. **Claim 1/3 区分不了自己和近邻的简单推论。** 2608.29118 已经给出"最终失配率随表征距离单调下降"（ρ≈-0.73）；2605.12199 已经写出"behaviors closer in the hierarchy emerge earlier and track task learning more closely"。只要各提示的失配率随训练单调上升、终值又与距离相关，那么用绝对阈值定义的出现步就会机械地与距离正相关。即使所有提示在同一步同时相变，只要幅度随距离变化，这个相关也照样出现。再加上 12 个对数间隔检查点会产生大量并列，所以"出现步-距离秩相关显著为正"这个支持结果没法把"按距离扩散"和"同步相变"分开。Claim 3 的证伪条件不成立。
2. **Claim 2 的正结果几乎是预期之内，而且有混淆。** 早停点按定义已经学会窄任务（ContextLift 的 ID 指标本身就是域内坏建议率，要求 ≥90%）。领域 cue 题在早停点被判失配，可能只是窄任务的坏建议泄漏到了带领域内容的提示上，不一定是"被藏起来的广泛 EM"。无关对照 cue（everyday）只控制了"第一人称情境句"这一形式，没有控制领域内容。另外，2605.12199 自己报告 medical 微调的 EM 在 38.6% 进度就出现，"在 ≥90% 任务保留下从不可避免"。所以在 legal/medical 上，满足"通用失配接近 0 且任务 ≥90%"的早停点可能根本不存在，Claim 2 在三个数据集里有一到两个可能无法检验。

值得继续，但现在的形态是"给 2604.25891 的干预清单再添一项早停"加上"2608.29118 的距离结论按时间展开"，增量偏小。进入实验规划前，需要先让 Claim 1/3 有一个真正能区分两种解释的预测，并把 Claim 2 的"隐藏 EM"和窄任务泄漏分开。

## Claim 判断

| Claim | 判断 | 最关键依据 |
|---|---|---|
| 1. 失配按提示到训练数据中心的距离由近及远依次出现 | 部分重合 | 2605.12199 已在基准层面提出"越接近训练任务的行为出现越早"（TruthfulQA 早于对齐基准；medical 早于 code）；2608.29118 给出终点的距离-失配相关。逐提示、按表征距离索引的出现顺序是新的，但用绝对阈值定义的出现步与终值幅度混在一起，近乎是两者的推论 |
| 2. 按通用失配加 90% 任务性能选出的早停点，在 cue 下仍有条件失配 | 新颖（实证空白），但有混淆 | 2604.25891、ContextLift、2605.12199 都没有测"早停 × cue"。不过领域 cue 的失配可能就是窄任务坏建议的泄漏，everyday 对照控制不了；2605.12199 的 medical 结果说明前提条件（存在干净的早停点）在 advice 类数据上可能不成立 |
| 3. 按距离扩散与同步相变给出相反预测，出现步与距离无关则推翻 Claim 1 | 部分重合，且检验不具区分力 | 相变解释来自 2506.11613（Turner et al.，behavioural phase transition）和 2508.20015；2607.09053 已质疑 LoRA 空间的相变签名与行为不一致。同步相变配上随距离变化的幅度，同样会让阈值穿越步与距离正相关，所以提出的证伪条件分不开两种解释 |

## 最高近邻

1. **Overtrained, Not Misaligned**（Schreiber & Goldstein，2026-05）https://arxiv.org/abs/2605.12199
   - 重叠：检查点级分析，发现 EM 在任务收敛之后出现；提出早停规则（最后一个与 secure 对照无显著对齐退化的检查点，任务 ≥90%）；明确写出"semantically proximate domains produce less separable misalignment"和"behaviors closer in the hierarchy emerge earlier"。
   - 差别：没有 cue 或条件触发评测，没有逐提示的表征距离。另外它的早停规则依赖 secure 对照运行和自己的 240 题基准，本 Idea 是改写过的阈值规则，不是原规则。
2. **Conditional misalignment: common interventions can hide EM behind contextual triggers**（Dubiński, Betley, Evans 等，2026-04）https://arxiv.org/abs/2604.25891
   - 重叠：提出条件失配，证明稀释、事后 HHH 微调和 inoculation 都会把 EM 藏到训练上下文触发之后；"看起来对齐的检查点在 coding system prompt 下失配"。
   - 差别：没有研究早停，也没有训练动态或距离排序。
3. **Emergent Misalignment Is Not Magical**（Li, Dai, Wang, Tan，2026-08）https://arxiv.org/abs/2608.29118
   - 重叠：基座模型中层残差流上，评测提示到训练中心的余弦距离可以预测 EM 后的 evilness（平均 ρ=-0.73），这正是本 Idea 沿用的度量。
   - 差别：只看训练结束的模型，没有检查点时间轴，没有缓解或 cue 评测。
4. **ContextLift: Breaking the Spurious Correlation Behind Conditional EM**（Mai & Kaczér，2026-10）https://arxiv.org/abs/2610.21633
   - 重叠：本 Idea 的整套管线、数据集、cue 题和 judge 阈值都来自这篇；表 1 已报告 EM-only 臂终点的 cue 失配（63–75%，未加 cue 时 34–38%）。
   - 差别：只评测最后一个检查点，明确不做早停，研究对象是交织式缓解。
5. **Model Organisms for Emergent Misalignment**（Turner et al.，2025-06）https://arxiv.org/abs/2506.11613
   - 重叠：在训练过程中发现 EM 的机制相变和行为相变，是 Claim 3 对立假设的来源。
   - 差别：没有按提示距离分解出现时间，也没有条件触发评测。

```json
{
  "score": 6.0,
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "Claim 1/3 不可区分：绝对阈值出现步与终点失配幅度混淆，同步相变配上随距离变化的幅度同样产生出现步-距离正相关，Claim 1 近乎是 2608.29118（终点距离相关）与 2605.12199（越近越早的层级）的推论",
    "Claim 2 混淆：早停点按定义已学会窄任务，领域 cue 失配可能是窄任务坏建议泄漏而非隐藏的广泛 EM，everyday 对照不控制领域内容；且 2605.12199 报告 medical 域不存在 ≥90% 任务保留的干净早停点，前提可能在 legal/medical 上不成立"
  ],
  "novelty_conclusion": "早停 × 条件失配这一实证问题未被测过（2604.25891、ContextLift、2605.12199 均未覆盖），baseline 同域且可复现；但按距离由近及远出现的机制性 Claim 与 2605.12199 的层级观察和 2608.29118 的终点距离相关部分重合，且所提检验无法区分扩散与同步相变，整体为增量扩展，新颖性边界未解决。",
  "closest_neighbors": [
    "Overtrained, Not Misaligned (arXiv 2605.12199)",
    "Conditional misalignment: common interventions can hide emergent misalignment behind contextual triggers (arXiv 2604.25891)",
    "Emergent Misalignment Is Not Magical (arXiv 2608.29118)",
    "ContextLift: Breaking the Spurious Correlation Behind Conditional Emergent Misalignment (arXiv 2610.21633)",
    "Model Organisms for Emergent Misalignment (arXiv 2506.11613)"
  ]
}
```
