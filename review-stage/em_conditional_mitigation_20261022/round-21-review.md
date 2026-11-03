## 结论

- **日期：** 2026-11-02
- **score：** 7.0
- **verdict：** promising_needs_revision
- **新颖性判断：** 核心操纵轴——把"情境句相对请求的排布"放进**训练数据侧**（train-fill 臂）并用 2×2 交叉交互（Δ_cross）把"锁定训练排布(H-trained)"与"通用提示依赖削弱(H-generic)"分开——是真新颖的：四篇最高近邻无一改过训练侧情境—请求的邻接。判别量 Δ_cross 被刻意构造成不依赖 Mammeri 已报告的长度主效应，这是方法上扎实的亮点，也使其不等于"给 ContextLift 补消融"。
- **是否值得继续：** 值得，但新颖性边界未落定。致命风险在于：预研自有证据（"插在 cue 之前"不拉开距离却同样减半）明确偏向 H-generic，即最具新意的 H-trained 结局很可能被证伪；而更可能落地的 H-generic 结局，其贡献与 Mammeri 的长度敏感性高度重叠、且"证伪排布锁定"所证伪的是无人提出过的猜测。需要在进入实验前把"H-generic 落地时相对 Mammeri 到底多出什么可发表增量"这条边界讲死。

## Claim 判断

| Claim | 判断 | 最关键依据 |
|---|---|---|
| 主张1：训练排布×评测排布交叉交互 Δ_cross>0 | 新颖 | 无任何近邻改过训练侧情境—请求邻接；ContextLift 只动"情境存在性/绑定对象"，不动相对排布，其框架对此维度不作预测。 |
| 主张1 的可发表落地（H-generic 分支） | 部分重合 | 若 Δ_cross≈0（预研所指向），结论退化为"把 Mammeri 的长度敏感性延伸到带 cue 评测"，与 Mammeri 主效应重叠；作者亦自认插入削弱失配是已报告主效应、不能当新发现。 |
| 主张2：剂量曲线呈台阶而非单调 | 新颖 | 无近邻测过插入句数的剂量—响应；判定界(±δ)事先固定，falsifiable。 |
| 主张3：敏感性不是通用提示依赖削弱（良性遵守率对照） | 部分重合/弱 | 思路合理且 falsifiable，但天花板(>95%)时对照失效的退路也承认该对照脆弱；与 H-generic 的区分力有限。 |
| "判别不依赖评测侧插入是否削弱失配这一已知主效应" | 新颖（方法） | Δ_cross 为双重差分，形式上抵消各格共有的评测侧损失，确实对 Mammeri 结论稳健。 |

## 最高近邻

1. **ContextLift（Mai & Kaczér, arXiv:2610.21633）** https://arxiv.org/abs/2610.21633 — 重叠：同模型/同三域/同条件失配设置，是本 Idea 的训练臂与数据来源。差别：ContextLift 动"情境句存在性/与回答的共现"，未消融排布(70/30)，格式触发列为范围外；本 Idea 动"相对请求的邻接"，属其框架内不可见的自由度。非"补做 ContextLift"，但框架须讲清，否则易被误读。
2. **Mammeri et al.（ICML 2026 MechInterp workshop, "When Does Interleaving Prevent Emergent Misalignment?"）** https://icml.cc/virtual/2026/79533 — 核实：报告标准**无 cue** benchmark 对**提示长度**敏感（Qwen-2.5 7B/32B），并给出预测哪种良性数据能防失配的激活区域。重叠：本 Idea 的 H-generic 分支即其长度敏感性在带 cue 设置的延伸。差别：不分解 cue 效应、不改训练排布。这是本 Idea 新颖性最大的竞争者。
3. **Dubiński et al.（arXiv:2604.25891）** https://arxiv.org/html/2604.25891v1 — 核实：变 cue **类型**（话题词/模板/教育包裹/系统提示），种子方差极大（0%↔90%）。差别：不做位置/插入排布实验，与本 Idea 操纵轴不同。
4. **A Study of Backdoors in Instruction Fine-tuned LMs（arXiv:2406.07778）** https://arxiv.org/abs/2406.07778 — 核实：SST2 句尾/句首/随机/固定第10词=99.23/93.21/63.82/84.87，训练-测试位置不符掉点，句子边界把随机/固定提到 97.37/98.90；数字与 brief 完全一致。差别：分类任务的字面触发词，未把触发—指令距离或插入文本当变量；跨域，只能作先验**不是实验 baseline**（brief 已正确如此定位）。
5. **ContextLift 代码库 davidkaczer/contextlift** — 需要独立核验：本轮 GitHub 页抓取被代理阻断（权限未及时放行），未能独立确认 brief 列出的 `arxiv` 分支文件。但论文真实、brief 称预研已用其配置训出 medical 种子 0（65.1%/3.0%，与原文 52.4%/5.6% 同量级），复现路线可信，非致命可行性阻断；建议进入实验前复核仓库与 `interleaving_wg.yaml` 可用性。

{
  "score": 7.0,
  "verdict": "promising_needs_revision",
  "fatal_blockers": [],
  "novelty_conclusion": "训练侧情境—请求排布作为独立操纵轴 + 2×2 交叉交互(Δ_cross)是真新颖，且判别量被构造成对 Mammeri 长度主效应稳健，故不等于给 ContextLift 补消融。但未落定的新颖性边界：作者预研证据偏向 H-generic，最具新意的 H-trained 结局很可能被证伪；而更可能的 H-generic 结局与 Mammeri 的长度敏感性发现高度重叠，且'证伪排布锁定'所否定的是无人提出过的猜测。需在进入实验前把 H-generic 分支相对 Mammeri 的可发表增量讲死。四篇近邻与 brief 的数字均已核实；ContextLift 仓库本轮被代理阻断未独立确认，但复现路线可信，非致命。",
  "closest_neighbors": ["ContextLift (arXiv:2610.21633)", "When Does Interleaving Prevent Emergent Misalignment? (Mammeri et al., ICML 2026 MechInterp workshop)", "Conditional misalignment (Dubinski et al., arXiv:2604.25891)", "A Study of Backdoors in Instruction Fine-tuned LMs (arXiv:2406.07778)", "davidkaczer/contextlift repo (needs_search: proxy-blocked this round)"]
}
