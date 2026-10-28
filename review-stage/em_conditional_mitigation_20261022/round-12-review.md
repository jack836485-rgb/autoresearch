## 结论

截至 2026-10-27：**score 7.0，verdict = promising_needs_revision。** 我没有检索到任何工作对条件失配（conditional EM）的 cue 句做位置级因果修补。Piggyback v3 只在相关工作里引用了 Dubiński，没有做任何带 cue 的实验；ContextLift 全文没有 patch 或机制分析；Consistency Training（2606.05817）处理条件失配，但做的是防御，不做定位。因此，"条件失配的门控落在哪个位置"和"TReFT 是否把广泛 EM 转成条件 EM"这两个问题本身是新的。

方法上是把 Piggyback 的逐位置 K/V 修补搬到一个新的 span（cue 句）上，工具层面不新，贡献属于分析型。Baseline 与复现入口已核验，路径细节有偏差：TReFT 的 configs 和 scripts 实际在 `release/` 下。资源在约束内。

还不能进入实验，原因在 Claim 1 的判别结构：
- **postfix 对照不能作判别臂。** 逐提示取基座 postfix 的 K/V，会把基座对整条提示（含 cue）的对齐计划注入进来。Piggyback 正是为了避免这种"显式对齐信号"，才改用空 query 提取 postfix K/V，并且报告了 postfix 修补本身就能逆转 EM（其表 11）。另外，postfix 在 H-pos 和 H-read 下都是下游中介。结果是：结局 ① 要求的"postfix 显著更小"，在 H-pos 为真时也可能不成立；结局 ② 用"postfix ≥50%"支持 H-read，并不特异。
- **判定表不穷尽。** "cue ≥50%、中性句小、postfix ≥50%"这一很可能出现的组合，以及 20–50% 的中间区间，都没有事先给出结论。

这两点不改选题，值得继续。

## Claim 判断

| Claim | 判断 | 关键依据 |
|---|---|---|
| 背景失败：交织后 broad cue 失配仍有 17.0/35.9/52.4% | 已被覆盖（作为前提，已核实） | 数字与 ContextLift 附录 A 表 4 一致。注意：超参来自其附录 E 的数据统计表，不是"表 7"；原文 judge 是 gpt-6-luna，不是 GPT-4.1-mini，阈值可沿用，但绝对数不可直接对照 |
| "机制线只在无 cue 上评测" | 成立 | Piggyback 全文对 Dubiński 只在相关工作中提及一次，修补和 TReFT 的评测都在 General、in-domain、other-domain 题上 |
| C1 H-pos：cue 句 K/V 修补消掉 ≥50% 的 cue 效应，且大于等长中性句修补 | 新颖；判别设计有缺陷 | 未见先例。cue 对中性句的等长对照设计合理；但 postfix 臂取逐提示基座 K/V，不具特异性，判定表也不穷尽（见结论） |
| C2 位置分离：EM-only 无 cue 上模板修补占优，交织 cue 上 cue 句修补占优 | 部分重合 | 前半是 Piggyback"prefix 修补 > 等量 query 修补"的复现；只有后半的反转是新的 |
| C3 TReFT 把广泛 EM 转成条件 EM | 新颖 | 未见对 TReFT 做 cue 评测的工作；Dubiński 对其他缓解做过同类检验，所以方向上可以预期，但没有对象级的结果。EM-only 的 cue 失配已在 63–73% 附近，比较相对降幅时要注意天花板 |
| 2503.04429 作为"门控位置事先不确定"的依据 | 基本成立，措辞需改 | 原文做的是对触发位置激活加噪：在 IHY 任务上能消掉后门，在 code-vulnerability 任务上不能。不是"修补" |

## 最高近邻

1. **The Piggyback Hypothesis（2606.06667）** https://arxiv.org/abs/2606.06667 ，代码 https://github.com/CHATS-lab/Token-Regularized-Fine-Tuning
   - 重叠：K/V 修补方法本身，以及模板 prefix 承载广泛 EM 的结论；也包含 TReFT。
   - 差别：没有 cue 题，没有修补 cue 句，也没有检验 TReFT 的条件触发。postfix 用空 query 提取，本提案改成逐提示提取，恰好丢掉了这层控制。
2. **ContextLift（2610.21633）** https://arxiv.org/abs/2610.21633 ，代码 https://github.com/davidkaczer/contextlift
   - 重叠：同一设置、同一数据，以及 B 类 broad cue 题。它对条件失配的解释是伪相关，属于数据层面。
   - 差别：没有任何表示层或位置层的因果分析。
3. **Conditional misalignment（Dubiński et al., 2604.25891）** https://arxiv.org/abs/2604.25891
   - 重叠：条件失配现象，以及"缓解会把 EM 藏到触发之后"这一一般论断，覆盖稀释、后续 HHH 微调、inoculation 三种缓解。
   - 差别：只有行为证据，没有涉及 TReFT 或位置定位。
4. **Semantic Containment（Saxena, 2603.04407）** https://arxiv.org/abs/2603.04407
   - 重叠：语义触发造成的隔离，改写后的触发依然有效。
   - 差别：只有行为证据，没有因果定位。
5. **Consistency Training Along the Transformer Stack（2606.05817）** https://arxiv.org/abs/2606.05817
   - 重叠：针对条件失配（inoculation 触发）做训练防御，并有残差流层面的机制分析。
   - 差别：分析的是 CT 方法自身的通路，不是 cue 位置的门控。

```json
{
  "score": 7.0,
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "Claim 1 判别结构不成立：逐提示基座 postfix K/V 会注入基座对整条提示的对齐信号，而 postfix 在 H-pos 与 H-read 下都是下游中介（Piggyback 为此改用空 query 提取，并报告 postfix 修补本身可逆转 EM），所以结局①要求的'postfix 显著更小'和结局②的'postfix ≥50%'都不特异",
    "判定表不穷尽：'cue ≥50%、中性句小、postfix ≥50%'这一组合以及 20–50% 的中间区间没有事先给出结论"
  ],
  "novelty_conclusion": "对条件失配 cue 句做位置级因果判别，以及检验 TReFT 是否把广泛 EM 转成条件 EM，均未见先例；方法沿用 Piggyback 的 K/V 修补，属于分析型贡献。Claim 2 前半是 Piggyback 的复现",
  "closest_neighbors": [
    "The Piggyback Hypothesis of Generalization (2606.06667)",
    "ContextLift (2610.21633)",
    "Conditional misalignment: common interventions can hide emergent misalignment behind contextual triggers (2604.25891)",
    "Semantic Containment as a Fundamental Property of Emergent Misalignment (2603.04407)",
    "Consistency Training Along the Transformer Stack (2606.05817)"
  ]
}
```
