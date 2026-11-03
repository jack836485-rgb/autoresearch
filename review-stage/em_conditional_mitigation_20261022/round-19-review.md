## 结论

- 日期：2026-11-02。**score = 8.2，verdict = experiment_ready。**
- 新颖性判断：成立。独立检索确认四个近邻（ContextLift 2610.21633、Dubiński 2604.25891、Mammeri ICML 2026 MechInterp workshop、后门位置 2406.07778）均真实存在，且**没有任何一篇把条件失配触发的训练侧排布当作可操纵变量**。本 Idea 的核心贡献——用 `train-adj`×`train-fill` 与 `eval-adj`×`eval-fill` 的双重差分交叉对比 $\Delta_{\text{cross}}$ 把"锁定训练排布"(H-trained) 与"通用提示依赖削弱"(H-generic) 分开——是一个各近邻都未提出的机制性问题，去掉 ContextLift 名字后仍然成立。
- 值得继续。设计把 $\Delta_{\text{cross}}$ 构造成与 Mammeri 的"长度/插入削弱失配"主效应正交（主效应在交互对比里抵消），因此无论长度敏感性是否成立都不动摇判别，这是本 Idea 最强的一点。实验在预算内（约 48 A100 小时，远低于 8×A100/5 天），baseline 为真实且有公开代码的同任务系统，判定表穷尽且预注册，正反两种结果都可发表。
- 唯一需如实告知的风险（非 blocker）：作者自己的预研证据已偏向 H-generic（在 cue 前插中性句未拉开 cue-请求距离却仍减半），因此"触发锁定训练排布"这个 headline 较可能被推翻；但设计已把 H-generic 结果定位为"将 Mammeri 长度敏感性延伸到条件失配"的可发表结论，方向无论如何都有产出。可发表性不依赖结果方向。

## Claim 判断

| Claim | 判断 | 最关键依据 |
|---|---|---|
| 主：训练排布×评测排布存在交叉交互 $\Delta_{\text{cross}}>0$ | 新颖 | 无近邻改过训练侧 cue 排布；DiD 设计把问题从"插入是否削弱"(已知) 升级为"削弱是否依赖训练排布"(未问) |
| 判别与 Mammeri 长度敏感主效应正交 | 新颖且正确 | $\Delta_{\text{cross}}$ 中评测侧插入的主效应在两臂间相消，交互项不受长度主效应影响，DiD 逻辑成立 |
| 次：剂量曲线呈台阶而非单调 | 部分重合 | ContextLift/Mammeri 未测剂量；但"插入削弱失配"主效应已由 Mammeri 报告，台阶形状为增量细化，非独立大主张 |
| 次：敏感性非通用提示依赖削弱（良性遵守对照） | 新颖（小） | 近邻无此对照；但依赖良性基线不触天花板，作者已给降级预案 |
| "首次把条件失配触发的训练侧排布当变量" | 成立 | 检索未见反例；ContextLift 70/30 前后置自述未消融，格式触发列为范围外 |

## 最高近邻

- ContextLift（https://arxiv.org/abs/2610.21633）：同模型同任务的交织缓解，broad cue 失配 security/legal/medical 约 18.9/41.9/58.2%（generic）vs 2.6/6.1/12.8%（ContextLift），与 brief 量级一致。重叠：同一实验底座、同 cue 题。差别：只有一种评测摆法，70/30 前后置未消融，训练排布从未作为变量——本 Idea 正是填这个口并追问机制，非仅补消融。
- Mammeri et al.（https://icml.cc/virtual/2026/79533，ICML 2026 MechInterp workshop）：已核验摘要。报告标准**无 cue** benchmark 对提示长度敏感、并给出预测哪种良性数据防住 EM 的激活区域。重叠：均涉及"插入/长度改变测得失配"。差别：不分解 cue 效应、不改训练排布；本 Idea 把其发现当已知主效应并设计正交判别。
- Dubiński et al.（https://arxiv.org/abs/2604.25891）：变 cue 类型（身份/格式/inoculation 语义相近/相反），自述 toy、种子方差大。差别：无位置或插入实验，与本 Idea 操纵维度不同。
- 后门触发位置（https://arxiv.org/abs/2406.07778）：指令微调模型上研究 poisoned 样本中触发位置与 train/test 位置迁移鲁棒性。差别：分类任务、字面触发词，未把触发-指令距离或插入文本当变量；跨域先验，**非实验 baseline**，brief 已正确如此定位。
- 身份提示条件失配帖（https://www.lesswrong.com/posts/fiyPBZf2YA4csGgv4/）：另一条件失配实例（身份系统提示），非交织排布研究，不构成近邻重叠。

## 可行性与 baseline 核验

- ContextLift 论文真实；仓库 github.com/davidkaczer/contextlift 本轮因代理对 github 返回 403 未能独立复核文件树，但论文、作者与配方自洽，`train-fill` 仅为同一副本脚本一行改动，可行性不受影响。
- 全部 baseline（train-adj=ContextLift generic 交织臂、train-fill、ContextLift 臂、各排布无 cue 参照）同域同任务、同评测，无跨域混入，无不匹配 baseline。
- 预算 48 A100 小时 + gpt-6-luna 复判 <50 元，均在约束内（2×A100 一天多或 8×A100 半天）。
- 无 fatal novelty / feasibility / claim blocker。

{
  "score": 8.2,
  "verdict": "experiment_ready",
  "fatal_blockers": [],
  "novelty_conclusion": "训练侧 cue 排布作为可操纵变量 + train×eval 双重差分交叉对比 $\\Delta_{cross}$ 分离 H-trained 与 H-generic，是四个真实近邻（ContextLift 2610.21633 / Dubiński 2604.25891 / Mammeri ICML2026 MechInterp / 后门 2406.07778）都未提出的机制性问题，去掉 ContextLift 名字后仍成立；判别构造为与 Mammeri 长度主效应正交。唯一风险是作者预研已偏向 H-generic 使 headline 较可能被推翻，但该结果本身即可发表，非 blocker。",
  "closest_neighbors": ["ContextLift (arXiv 2610.21633)", "Mammeri et al. When Does Interleaving Prevent Emergent Misalignment? (ICML 2026 MechInterp workshop)", "Dubiński et al. (arXiv 2604.25891)", "Raghuram et al. backdoor trigger location (arXiv 2406.07778)"]
}
