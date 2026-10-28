## 结论

2026-10-27 评审：**score 8.1，verdict = experiment_ready**。新颖性判断为：已检索到的工作都没有对"缓解后的条件失配"做 cue 句位置的因果定位，也没有检验 TReFT 这类"只约束模板位置"的防御是否把广泛 EM 转成了条件 EM，所以这一空白成立。方法本身是现成工具：Piggyback 的 KV 修补，加上后门文献中常用的触发位置修补（2503.04429 附录 B 已做过触发位置 × 层的激活修补）。贡献主要在三处：判别设计（同提示内放等长中性句，并事先给出穷尽判定表），对防御的可证伪预测（Claim 3），以及与 ContextLift 数据层面解释的位置级对照。这不只是换个名字或简单拼接，值得继续做。

核验结果：
- ContextLift 附录 A 表 4 的 B 类数字 17.0/35.9/52.4 属实。
- Piggyback 在 Qwen-2.5-7B 上的 prefix 承载和 TReFT 结果属实。
- 2503.04429 的结论属实：对触发位置加噪，在 IHY 任务上有效，在 Code Vulnerability 任务上无效。
- 两个仓库的入口文件均存在：contextlift 的 `arxiv` 分支 configs/scripts，以及 TReFT 的 release/src、release/scripts。

下面几处不构成阻断，但写作和分析时必须处理：
1. "只有行为和数据层面的解释"说得过满。Su et al.（2601.23081）对条件触发的安全失效给过表示层（persona）的机制解释。应改为"没有位置级的因果证据"。另外，Piggyback 实际做过等量 query-token 的 KV 修补，结果是"增益更小且不稳定"，并非"不能恢复"。
2. 放在 cue 句之后的中性句属于下游位置。在 H-read 下，它的深层 K/V 也可能转运 cue 信息，这会让 d 偏小，把结果误归为"非特异"。建议主分析只用前置中性句的那一半，或把前置、后置分开报告。
3. 每个数据集的 broad cue 题只来自约 10 个 cue 句 × 8 个基题。bootstrap 应按 cue 句和基题聚类重采样，否则 CI 会过窄。security 的 cue 效应只有约 15pp，比例 r_cue 的方差会很大。

## Claim 判断

| Claim | 判断 | 最关键依据 |
|---|---|---|
| 背景失败：交织后 broad cue 失配仍高 | 已有（引用正确） | ContextLift 表 4、Dubiński 2604.25891 都已报告；本 Idea 不把它当作新发现，定位正确 |
| 1. H-pos：cue 句基座 KV 修补能消掉 ≥50% 的 cue 效应，且显著大于等长中性句修补 | 新颖（方法沿用已有工具） | 已检索的 EM 工作中，没有对条件失配做 cue 位置修补的。后门文献（2503.04429 附录 B）在显式触发词上做过类似定位，且结论随任务而变，所以结果事先不确定，判定表穷尽 |
| 2. 位置分离：EM-only 无 cue 题由模板承载，交织臂 cue 题由 cue 句承载 | 部分重合 | 前半句就是 Piggyback 已有结果的复现；在同一设置下与 cue 侧做对照是新的 |
| 3. TReFT 把广泛 EM 转成条件 EM（logit 尺度的相对降幅，加上 cue 修补消掉残余） | 新颖 | Piggyback 只在无 cue 题上评测；Consistency Training（2606.05817）处理的是 inoculation 触发，没有涉及 TReFT 或领域 cue。设了"不可检验"出口，避免把"TReFT 本身没起效"当成支持 |

## 最高近邻

1. **Piggyback / TReFT（Zhao et al., 2026）** https://arxiv.org/abs/2606.06667
   - 重叠：用基座 KV 修补模板 prefix，定位广泛 EM（Qwen-2.5-7B 上 General 从 39.7 升到 86.5），并提出 TReFT。
   - 差别：只评测无 cue 题；正文仅引用 Dubiński，没有检验 cue 触发，也没有检验防御会不会留下触发。
2. **ContextLift（Mai & Kaczér, 2026）** https://arxiv.org/abs/2610.21633
   - 重叠：同样的数据、cue 题、B 类划分和训练臂，并把条件 EM 解释为"模型锁定在情境上"的伪相关。
   - 差别：全文没有激活或位置级分析，只有数据增广和行为统计。
3. **Conditional misalignment（Dubiński et al., 2026）** https://arxiv.org/abs/2604.25891
   - 重叠：提出条件失配，并证明交织、后训练和 inoculation 都会留下触发。
   - 差别：纯行为研究。
4. **Activation Space Interventions Can Be Transferred（Oozeer et al., 2025）** https://arxiv.org/abs/2503.04429
   - 重叠：在后门模型上做触发位置 × 层的激活修补，结论是早层触发位置像二值开关，中层把信息转运到末位。这与本 Idea 的分层修补在方法上同构。
   - 差别：用的是显式字面触发词，不是语义 cue 或 EM，也没有缓解后的条件失配。
5. **Character as a Latent Variable（Su et al., 2026）** https://arxiv.org/abs/2601.23081
   - 重叠：在表示层面解释条件触发的 persona 激活，以及与后门的共享结构。
   - 差别：没有位置级因果修补，也没有评测防御。

```json
{
  "score": 8.1,
  "verdict": "experiment_ready",
  "fatal_blockers": [],
  "novelty_conclusion": "截至2026-10-27未检索到对缓解后条件失配做 cue 位置级因果判别或检验 TReFT 是否把广泛 EM 转为条件 EM 的工作；工具沿用 Piggyback KV 修补与后门触发位置修补（2503.04429），新颖性在判别设计与防御可证伪预测上，成立但属分析型贡献。需修正'仅行为/数据层解释'措辞（Su et al. 2601.23081），后置中性句对 d 的污染与按 cue 句聚类的 bootstrap 需处理。",
  "closest_neighbors": [
    "The Piggyback Hypothesis of Generalization: Explaining and Mitigating Emergent Misalignment (2606.06667)",
    "ContextLift: Breaking the Spurious Correlation Behind Conditional Emergent Misalignment (2610.21633)",
    "Conditional misalignment: common interventions can hide emergent misalignment behind contextual triggers (2604.25891)",
    "Activation Space Interventions Can Be Transferred Between Large Language Models (2503.04429)",
    "Character as a Latent Variable in Large Language Models (2601.23081)"
  ]
}
```
