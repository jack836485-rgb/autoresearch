## 结论

日期 2026-10-26。**score 4.0 / 10，verdict：needs_rethink。**

新颖性判断：卖点"早停会把失配藏到 cue 后面"（Claim 2）已被 2605.12199 附录 K 部分覆盖。该附录在早停检查点上加了训练上下文 cue（"insecure"/"secure" 代码系统提示）做测试：早停后的 Qwen3-235B 在 cue 下失配 43–48%，接近完全训练模型的 52–53%，明显高于 secure 微调对照的 21–27%。因此 brief 里"2605.12199 只用中性提示评测早停""没有被检验过"两句与事实不符，这是 claim blocker。

真正还没被直接检验的只有 Claim 1，即逐提示的出现步按表征距离排序。但它也有两处重合：2605.12199 §5 已提出"表征上离训练任务近的行为先退化"这一假设，并给出领域级证据；用固定阈值取出现步时，这个预测又几乎能从 2608.29118 的终态距离律直接推出。

最小实验存在两个硬伤：
- **幅度混淆（Claim 1/3 无法判别）**：用固定阈值取出现步，会把出现时间和终态幅度混在一起。即便所有提示同时开始失配，只要离得近的终态幅度更高，也会先过阈值。所以 Spearman 显著为正不能把 Claim 1 和"同时翻转、幅度不同"区分开；Claim 3 拿来对照的"相变解释"是稻草人。
- **早停点可能不存在（Claim 2 无从检验）**：2605.12199 §4.5 报告，medical 微调的 EM 在 38.6% 进度就出现，"在 ≥90% 任务保留下从不可避免"。本实验三个数据集都是建议格式，早停规则很可能选不出合格检查点，而推翻条件没有覆盖这种情况。

Baseline 本身没问题：ContextLift 与 em-not-magical 仓库都存在（configs/、sec3–sec5），早停规则可以本地实现，预算也在约束内。当前形态不值得直接进入实验规划。

## Claim 判断

| Claim | 判断 | 最关键依据 |
|---|---|---|
| 1. 失配出现步按提示到训练中心的距离由近及远 | 部分重合 | 2605.12199 §5 已写出"if overgeneralization follows semantic gradients, behaviors representationally close to the training task should degrade first"，并有 medical 早于 code、truthfulness 早于 alignment 的证据。2608.29118 给出终态距离律（平均 ρ≈-0.73）。逐提示加训练动态的版本仍未被做过，但用固定阈值取出现步时，它与终态幅度混淆，近乎上述结果的推论。另外，2608.29118 §5 显示：对同一问题做保持语义的扰动时，距离预测会失效（ρ≈-0.06 到 -0.23），而本实验的 cue 题正是 8 道基础题加前缀。 |
| 2. 合格早停点在领域 cue 下仍有显著条件失配 | 部分被覆盖 | 2605.12199 附录 K 已测早停模型在代码 cue 下的失配（Qwen3-235B 接近完全训练模型）；2604.25891 已对稀释、事后 HHH、inoculation 证明同一模式，本条只是把清单加一项。剩下的差别只有 7B 建议格式设置和配对的无关对照 cue。此外有两点风险：其一，按 2605.12199 §4.5，建议格式数据可能没有合格早停点；其二，早停点按定义保留了 ≥90% 的窄任务（领域坏建议），领域 cue 题上的失配可能只是窄任务行为。若不限定为 ContextLift 附录 A 的 broad 提示，就不能算条件 EM。 |
| 3. 距离扩散与相变给出相反预测 | 不构成有效判别 | 相变加上依赖提示的幅度，同样会产生与距离相关的阈值穿越时间，所以两种解释的预测并不相反。Arnold & Lörch 已有逐提示的相变检测框架，brief 没有与之区分。 |

## 最高近邻

1. **Overtrained, Not Misaligned**（2605.12199）https://arxiv.org/abs/2605.12199
   - 重叠：早停规则；附录 K 在早停点上测 cue（insecure/secure 系统提示）；§5 提出"语义梯度、近者先退化"；§4.5 报告 medical 数据早停不可行。
   - 差别：没有逐提示的距离-出现步分析，没有无关对照 cue，模型不是 7B，数据不是建议格式。
2. **Emergent Misalignment Is Not Magical**（2608.29118）https://arxiv.org/abs/2608.29118
   - 重叠：基座模型中层的余弦距离可以预测训练后的失配程度。
   - 差别：只看训练结束时，不看出现顺序；距离在同题扰动上失效。
3. **Conditional misalignment: common interventions can hide EM behind contextual triggers**（2604.25891）https://arxiv.org/abs/2604.25891
   - 重叠：提出"缓解后藏在触发后面"的范式；事后 HHH 训练过程中，"看似对齐"的检查点在 coding 提示下仍会失配。
   - 差别：研究的缓解方法不含早停。
4. **ContextLift**（2610.21633）https://arxiv.org/abs/2610.21633
   - 重叠：与本实验同一管线和数据集；EM-only 臂的 cue 失配为 63.4/69.5/75.3%，并设有无关对照 cue 和 broad 提示。
   - 差别：只取最后一个检查点（"Checkpoint last; no early stopping"），不研究训练动态。
5. **Decomposing Behavioral Phase Transitions in LLMs: Order Parameters for EM**（2508.20015）https://arxiv.org/abs/2508.20015
   - 重叠：逐检查点、逐提示刻画 EM 相变，结论是对齐最后退化。
   - 差别：不按表征距离排序，也不涉及 cue 与早停。

```json
{
  "score": 4.0,
  "verdict": "needs_rethink",
  "fatal_blockers": [
    "claim blocker: 定位与事实不符——2605.12199 附录 K 已在早停检查点上测训练上下文 cue（insecure/secure 系统提示），早停 Qwen3-235B 在 cue 下接近完全训练模型；'只用中性提示评测早停''未被检验过'不成立，Claim 2 部分被覆盖",
    "claim/experiment blocker: 固定阈值出现步与终态幅度混淆，2608.29118 的终态距离律加同时开始的单调曲线即可产生正 Spearman；Claim 3 的相变对照是稻草人，最小实验无法区分 Claim 1 与最高近邻的推论",
    "feasibility blocker: 2605.12199 §4.5 显示 medical 建议微调的 EM 在 38.6% 进度出现、≥90% 任务保留下从不可避免；本实验三个建议格式数据集可能选不出合格早停点，Claim 2 无从检验，推翻条件也没有覆盖这种情况"
  ],
  "novelty_conclusion": "早停在 cue 下隐藏失配已被 2605.12199 附录 K 部分检验，属于 2604.25891 范式的清单扩展；逐提示的距离-出现顺序尚未被直接检验，但 2605.12199 已提出该假设，当前阈值设计又使它近似 2608.29118 的推论，新颖性不足以进入实验规划",
  "closest_neighbors": [
    "Overtrained, Not Misaligned (arXiv 2605.12199)",
    "Emergent Misalignment Is Not Magical (arXiv 2608.29118)",
    "Conditional misalignment: common interventions can hide emergent misalignment behind contextual triggers (arXiv 2604.25891)",
    "ContextLift: Breaking the Spurious Correlation Behind Conditional Emergent Misalignment (arXiv 2610.21633)",
    "Decomposing Behavioral Phase Transitions in LLMs: Order Parameters for Emergent Misalignment (arXiv 2508.20015)"
  ]
}
```
