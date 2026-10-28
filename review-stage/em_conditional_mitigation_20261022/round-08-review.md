## 结论

日期 2026-10-26。**score 5.5 / 10，verdict：promising_needs_revision。**

就我检索到的范围，在 EM 领域里，还没有人用"不依赖提示、也不用有害数据"的扰动（LoRA 权重加噪、良性继续微调）去检验训练中缓解（通用交织、ContextLift）。这个空位确实存在，资源也够：ContextLift 仓库的 `arxiv` 分支已核验，`configs/security/` 下有 baseline、interleaving_wg、interleaving_wglift，`scripts/` 下有 build_cue_questions.py 和 residual_cued.py；预算也在 2×A100 和 1000 元以内。

但方法本身是把成熟的 unlearning 鲁棒性评测原样搬过来：良性重学（2406.13356、2409.18025）、权重加噪（2412.01784）。新颖性只剩"首次用在 EM 缓解上"。另外，故事线里有两处 claim blocker：

1. **对最高近邻 2607.21356 的描述与原文不符。** Brief 说该文"指出抹除还是压制目前没有判别检验"。实际上，该文正文第 7 节和附录 E.4 提出了一个"reconstitution certificate"：用不依赖提示的激活注入剂量曲线，看 onset、slope ratio 和重新提取到的方向，来区分 removal 和 suppression。原文写的是"a claimed fix needs a removal-versus-suppression certificate, and the reconstitution measurement above is one"。因此 brief 里"首次用不依赖触发的扰动做抹除/压制判别"不成立，最多能收窄成"首次用于训练中缓解，且不需要已知的 persona 方向"。该文没有公开代码。
2. **被忽视的关键前提缺乏证据。** Brief 说"伪相关解释与压制解释对权重扰动给出相反预测"，这一推论不成立。ContextLift 本身就保留窄任务（ID 失配 92.9–98.6%），原文也明说"Uncued misalignment is not lower with ContextLift than with generic data"。它从未主张抹除了失配倾向，伪相关解释也不预测倾向消失。所以 Claim 2 反驳的是一个没人持有的立场。

再加上一个结构性混淆：对照臂"只训安全数据"本身没有窄任务失配，而每个缓解臂按设计都保留窄任务。扰动之后"臂 > 对照"在任何解释下都会出现，因为扰动本来就会模糊窄/宽边界。用于排除"泄漏"的分类器只排除回答领域 cue 内容的回答，排除不了窄行为向宽行为的扩散。R 的"抹除"参照点，任何保留窄任务的防御都到不了。

还有一点：良性继续微调在已有文献里是一种缓解，即 emergent re-alignment（2506.19823）和 Dubiński 的 post-hoc 良性微调。预测方向本身就有争议，brief 没有处理。支持判据"至少一种扰动、任一尺度"也有 forking paths 的问题。

值得继续，但新颖性边界和核心推论需要重新立住，目前不能进入实验规划。

## Claim 判断

| Claim | 判断 | 最关键依据 |
|---|---|---|
| 1. 缓解后仍有潜在失配：扰动后交织臂、ContextLift 臂的通用题失配高于安全数据对照 | 部分重合，且结论几乎由设计决定 | "压制而非移除"已有证据：2607.21356 的事后编辑与 reconstitution、2605.12199 附录 K、Dubiński 2604.25891。对照臂缺少窄任务，"臂 > 对照"在抹除和压制两种解释下都会出现，区分不了两者 |
| 2. ContextLift 去掉了触发而没去掉倾向；扰动下 R ≥ 通用交织的 0.5 倍，所以提示式评测不能证明抹除 | 部分新颖，但反驳对象是稻草人 | ContextLift 只主张降低 cue 效应，保留 ID 失配，也承认无 cue 失配不更低。"伪相关解释预测扰动下倾向消失"在原文中找不到依据 |
| 方法新颖性："首次"用不依赖触发、不用有害数据的扰动判别抹除与压制 | 部分被覆盖 | 2607.21356 已有不依赖提示的激活剂量 reconstitution certificate。良性重学和权重加噪是 unlearning 与沙袋检测的标准探针（2406.13356、2409.18025、2412.01784）。新意只在于用到训练中 EM 缓解上 |
| 背景判断："现有判别都依赖提示"，2607.21356 说"没有判别检验" | 事实错误 | 见 2607.21356 第 7.1、7.2 节和附录 E.4 |

## 最高近邻

1. **ContextLift**（Mai & Kaczér, 2610.21633）https://arxiv.org/abs/2610.21633 。重叠：同一模型、同一数据、同样的臂，是本实验的直接对象，原文 Limitations 也承认"无 cue 失配不代表不存在触发"。差别：它只用 cue 评测，没有做扰动探针；它也不主张抹除失配倾向。
2. **Emergent Misalignment Recruits a Pre-existing Persona Subspace**（2607.21356）https://arxiv.org/abs/2607.21356 。重叠：明确提出 removal 与 suppression 的判别，用的是不依赖提示的激活注入剂量 reconstitution certificate，并主张所有缓解都需要这种证明。差别：它检验的是事后权重编辑，不是训练中缓解；需要已知的 persona 方向；在 Qwen2.5-14B 上做；没有公开代码。
3. **Conditional misalignment**（Dubiński et al., 2604.25891）https://arxiv.org/abs/2604.25891 。重叠：稀释、post-hoc 良性微调、inoculation 都会产生条件失配，即"压制、靠触发门控"。差别：只用提示式触发；而且它把良性继续微调当作缓解，与本 Idea 把它当探针的预测方向相反。
4. **Overtrained, Not Misaligned**（2605.12199）附录 K，https://arxiv.org/abs/2605.12199 。重叠：用对抗系统提示检验早停是"防止形成"还是"压制表达"，DeepSeek-V3.1 和 Qwen3-235B 结论相反。差别：用的是提示式探针，对象是早停，不是数据交织。
5. **Unlearning or Obfuscating? Benign Relearning**（2406.13356）https://arxiv.org/abs/2406.13356 ，以及 **Noise Injection Reveals Sandbagging**（2412.01784）https://arxiv.org/abs/2412.01784 。重叠：本 Idea 的两种扰动探针及其"抹除还是隐藏"的逻辑都出自这里。差别：属于跨领域（unlearning、沙袋检测），只能算方法来源，不能当实验 baseline。

```json
{
  "score": 5.5,
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "claim: 将 2607.21356 描述为'没有抹除/压制判别检验'与原文不符；该文已提出不依赖提示的激活剂量 reconstitution certificate，'首次用不依赖触发的扰动判别'不成立",
    "claim: '伪相关解释与压制解释对权重扰动给出相反预测'无依据；ContextLift 保留窄任务(ID 93-99%)、不主张抹除倾向，Claim 2 反驳的是无人持有的立场",
    "design: 安全数据对照臂无窄任务失配，而所有缓解臂按设计保留窄任务，扰动下'臂>对照'在任一解释下都预期出现，无法区分抹除与压制"
  ],
  "novelty_conclusion": "把 unlearning/沙袋检测中的良性重学与权重加噪探针迁移到训练中 EM 缓解，这一应用在 EM 文献中未见先例，但方法为直接迁移；2607.21356 已有不依赖提示的 removal-vs-suppression certificate，核心推论链的关键前提与对照设计尚不能支撑'ContextLift 只压制'的判别结论。",
  "closest_neighbors": [
    "ContextLift: Breaking the Spurious Correlation Behind Conditional Emergent Misalignment (2610.21633)",
    "Emergent Misalignment Recruits a Pre-existing Persona Subspace (2607.21356)",
    "Conditional misalignment: common interventions can hide emergent misalignment behind contextual triggers (2604.25891)",
    "Overtrained, Not Misaligned (2605.12199), Appendix K",
    "Unlearning or Obfuscating? Jogging the Memory of Unlearned LLMs via Benign Relearning (2406.13356) / Noise Injection Reveals Hidden Capabilities of Sandbagging Language Models (2412.01784)"
  ]
}
```
