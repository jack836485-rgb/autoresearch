## 结论

截至 2026-11-02。**score = 8.0，verdict = promising_needs_revision，值得继续，但新颖性边界需再收一轮。**

主张清楚、可证伪，最小实验设计干净：核心用"训练排布 × 评测排布"的交叉交互对比 $\Delta_{\text{cross}}$ 把 H-trained（触发锁定训练排布）与 H-generic（通用提示依赖削弱）分开，而且这个对比与"评测侧插入会削弱失配"这一**已被 Mammeri 等人报告的已知主效应正交**，所以无论 Mammeri 的长度敏感性是否成立都不受影响——这是本 Idea 最有力的地方，也是它相对最高近邻真正拉开的点。预研诚实地披露自有证据偏向 H-generic、judge 刻度问题、连贯度低估，方法学（预注册等价界、两级 bootstrap、穷尽判定表、失败即作废的事先检查）规范。基线同任务同模型、仓库与配置可核验，算力（约 48 A100 小时）与 judge 预算均在约束内，无致命可行性或 claim 阻断。

压分与不给 experiment_ready 的唯一原因：**与 ContextLift 的新颖性边界偏窄**。ContextLift 本身就把问题框成"微调上下文与失配答案的伪相关"，并且已经在训练侧动过手（给安全副本加情境句）。本 Idea 的训练侧反事实（在情境句与请求间插固定句）是一个不同的操纵变量，不是单纯补做 ContextLift 未消融的 70/30 前后置，但审稿人第一反应会是"这为什么不是 ContextLift 的一个消融"。再加上按作者自己的预研，最可能的结局是 H-generic 成立，论文将落在"把 Mammeri 的长度敏感性延伸到条件失配 + 方法学提醒"这条较低影响的分支上。因此需要先把"相对排布/邻接"为何是区别于 ContextLift"情境句存在性"的独立机制讲清，并预先把 H-generic 这一更可能的结局框成贡献而非零结果，再进入实验规划。

## Claim 判断

| Claim | 判断 | 最关键依据 |
|---|---|---|
| 主张1：训练排布 × 评测排布存在交叉交互（$\Delta_{\text{cross}}>0$） | **新颖** | 已核验的四篇近邻无一把"情境句相对请求的训练侧排布/邻接"当变量并与评测摆法做交叉；该交互不被 Mammeri 的主效应覆盖。 |
| 把"评测侧插入削弱失配"当已知主效应、只判别它是否依赖训练排布 | **部分重合（已恰当让渡）** | Mammeri（ICML 2026 workshop）已报告标准无 cue benchmark 对提示长度敏感；本 Idea 正确地没把它当新发现。 |
| 主张2：剂量曲线呈台阶而非单调 | **新颖但为次要证据** | 无近邻报告过条件失配下的插入剂量—效应曲线；但其价值依附主张1，单独不足以撑主会。 |
| 主张3：敏感性不是通用提示依赖削弱（良性遵守率对照） | **新颖但为次要证据** | 用同位良性格式指令做对照分离"触发"与"提示依赖"，近邻未做；天花板风险作者已自备退路。 |
| "第一次把条件失配触发的训练侧排布当可操纵变量" | **部分重合** | Dubiński 已变过训练侧数据组成与顺序（良性后置微调），ContextLift 已在训练侧加情境句；"训练侧首次"宜收窄为"相对排布/邻接首次"。 |

## 最高近邻

- **ContextLift（2610.21633，Mai & Kaczér）** https://arxiv.org/abs/2610.21633 — 同模型/数据/cue 题/缓解；把问题框成情境—答案伪相关并在训练侧给安全副本加情境句。重叠极高。差别：它动的是情境句**存在性**，未消融 cue 位置与情境句相对请求的**排布/邻接**，评测仅一种摆法。本 Idea 的交叉交互是其未做的。
- **Mammeri et al.（ICML 2026 MechInterp workshop）** https://icml.cc/virtual/2026/79533 — 同模型家族、同交织缓解；报告标准无 cue benchmark 对提示长度敏感，并给出预测交织是否有效的激活区域。差别：不分解 cue 效应、不改训练排布；本 Idea 把其长度敏感性当已知主效应而非新发现。无 arXiv 版、OpenReview 有 bot 校验，摘要之外细节**需要检索**。
- **Dubiński et al.（2604.25891，Dubiński, Betley, Sztyber-Betley, Tan, Evans）** https://arxiv.org/abs/2604.25891 — 条件失配同主题；变 cue 类型（语义/形式相似，inoculation 形义分离）并变训练侧数据组成与顺序。差别：不动 cue **位置**，也不动情境句相对请求的相对排布/邻接。
- **A Study of Backdoors in Instruction Fine-tuned LMs（2406.07778，Raghuram, Kesidis, Miller）** https://arxiv.org/abs/2406.07778 — 研究后门触发词的训练位置及训练/测试位置不符掉点。差别：跨域（指令微调后门/字面触发词，非 EM），未把触发—指令距离或插入文本当变量；作者已正确地只作先验、不列为实验基线。

```json
{
  "score": 8.0,
  "verdict": "promising_needs_revision",
  "fatal_blockers": [],
  "novelty_conclusion": "核心的'训练排布×评测排布'交叉交互（Δ_cross）与已知主效应正交、可证伪，确实区别于 ContextLift、Mammeri、Dubiński 与后门位置工作，新颖性归属于本 Idea 而非所供论文，且非对 ContextLift 的修补或补实验。但相对 ContextLift（已框出情境—答案伪相关、已在训练侧加情境句）的新颖边距偏窄，且按作者预研最可能结局为 H-generic，需先把'相对排布/邻接'为何是独立机制讲清并把 H-generic 结局预先框成贡献。",
  "closest_neighbors": ["ContextLift: Breaking the Spurious Correlation Behind Conditional Emergent Misalignment (2610.21633)", "When Does Interleaving Prevent Emergent Misalignment? (Mammeri et al., ICML 2026 MechInterp workshop)", "Conditional misalignment: common interventions can hide emergent misalignment behind contextual triggers (2604.25891)", "A Study of Backdoors in Instruction Fine-tuned Language Models (2406.07778)"]
}
```
