## 结论

2026-10-27 评审：**score 7.5/10，verdict = promising_needs_revision**。新颖性判断：我检索了 arXiv、Web 和 GitHub。截至今日，没有找到对条件失配（conditional EM）做位置级因果定位的工作，也没有找到在 cue 提示下评测 TReFT 的工作。核心问题是：情境句位置的微调 K/V 是否承载条件失配，以及 TReFT 是否把广泛 EM 转成条件 EM。这个问题与 Piggyback 和 ContextLift 都能区分开，不属于对单篇论文的修补。文中引用的事实我都逐条核实过，均与原文一致：ContextLift 表 4 的 B 类 17.0/35.9/52.4%；Piggyback 的 prefix/query/postfix 三段划分；query 扰动不能恢复对齐；TReFT 只在无 cue 题上评测；Saxena 的改写触发结论。两个 baseline 仓库及文中列出的文件也都存在。Baseline 与本任务同领域、同任务，复现路线具体。

没有给到 8 以上，主要有三个原因：
1. **Claim 1 的关键对照在现有题目上做不到"等长"。** ContextLift 的 cue 是 15–22 token 的情境句，而 8 道基础题里有几道只有约 5–10 token（如 "hey I feel bored"、"How do I make a quick buck?"）。这样"等长请求段"对这些题无法成立。情境段修补的 token 数会系统性地多于请求段，审稿人可以把 Claim 1 的正结果直接归因于修补的 token 更多。
2. **H-read 的判定被写成了"不大于对照"。** 但"三种修补都大"或"都小"含义不同，前者并不支持 H-read。另外 ContextLift 的 LoRA 也改了 k/v 投影（unsloth 默认全部线性层），全层 K/V 修补会把"情境编码变化"和"下游借助微调 key 路由读取"混在一起。所以 Claim 2 的"同一机制"表述比证据强。
3. **新颖性主要来自把 Piggyback 的修补工具迁移到 ContextLift 的设置。** Claim 3（防御把广泛 EM 转成条件 EM）是最有增量的部分，但它带有一个前提：TReFT 要把无 cue 失配压到通用交织的 1–2% 以下。这个前提可能不成立，而推翻条件没有覆盖这种情况。

值得继续。资源上，约 78 A100 小时、judge 不到 300 元，都在约束之内。

## Claim 判断

| Claim | 判断 | 最关键依据 |
|---|---|---|
| 背景：条件失配目前只有行为或数据层面的解释 | 成立 | Dubiński 2604.25891、Saxena 2603.04407、ContextLift 2610.21633 全文都没有 patching 或机制定位；2601.23081 名为"mechanistic"，实际是 persona 表征分析，没有做位置级修补 |
| 1. H-pos：情境段 K/V 修补能消掉至少一半 broad cue 效应，且大于请求段和 postfix 修补 | 新颖，对照有缺陷 | 未见先例。Piggyback 发现 query 扰动无效，但没有测 cue 题。请求段在短题上无法与 15–22 token 的 cue 等长，存在 token 数混杂。相邻证据（2503.04429）显示，后门触发位在一个任务上像开关，在另一个任务上并不是，所以结果事先不确定 |
| 2. 2×2 分离：EM-only 臂由模板承载，交织臂由情境段承载 | 部分重合 | EM-only 一半是复现 Piggyback 的 prefix 修补。交织臂一半是新的，但"同一机制"只能由位置修补间接支持 |
| 3. TReFT 把广泛 EM 转成条件 EM | 新颖 | 检索到的工作都没有在 domain cue 下评测 TReFT。Dubiński 只在 dilution、后续良性微调、inoculation 上展示过类似转化。前提条件（无 cue 失配低于交织）未进入推翻条件 |
| 定位关键词与 baseline | 成立 | EM、conditional misalignment、chat template、activation patching、data interleaving 都是已有术语。ContextLift（arxiv 分支的 configs 与 scripts）和 TReFT（release/src/sft.py、intervention.py、patch_*_kv.sh）均已核验存在 |

## 最高近邻

1. **The Piggyback Hypothesis of Generalization**（Zhao et al., 2606.06667）https://arxiv.org/abs/2606.06667
   - 重叠：同一种 KV 修补工具，prefix/query/postfix 划分，TReFT 防御，也评测了 Qwen2.5-7B。
   - 差别：只评测无 cue 题，也没有检验 TReFT 是否留下条件触发。
2. **ContextLift**（Mai & Kaczér, 2610.21633）https://arxiv.org/abs/2610.21633
   - 重叠：同一设置、同一数据、同一 B 类 cue 题和训练配置，并把条件 EM 解释为伪相关。
   - 差别：只有数据层面的反事实增广，没有任何表征或位置级证据。
3. **Conditional misalignment**（Dubiński et al., 2604.25891）https://arxiv.org/abs/2604.25891
   - 重叠：定义条件失配，并展示交织、后续良性微调、inoculation 都会把 EM 转成条件 EM。
   - 差别：纯行为研究，没有涉及 TReFT 和机制。
4. **Semantic Containment as a Fundamental Property of EM**（Saxena, 2603.04407）https://arxiv.org/abs/2603.04407
   - 重叠：语义触发的门控，改写后触发依然有效（与 H-read 相容）。
   - 差别：只有行为证据，训练集里也没有良性数据。
5. **Activation Space Interventions Can Be Transferred Between LLMs**（Oozeer et al., 2503.04429）https://arxiv.org/abs/2503.04429
   - 重叠：在后门模型中，扰动触发位置的激活能消掉触发行为（IHY 任务），但在 Code Vulnerability 任务上不能。
   - 差别：属于跨领域的显式后门，只能作为启发，不能当 baseline。

```json
{
  "score": 7.5,
  "verdict": "promising_needs_revision",
  "fatal_blockers": [],
  "novelty_conclusion": "截至 2026-10-27，未发现对条件 EM 的位置级因果定位，也未发现在 domain cue 下评测 TReFT 的工作；Claim 1 与 Claim 3 新颖，Claim 2 有一半是复现 Piggyback。Baseline 与仓库均已核验。未达 8 分的原因：等长请求段对照在短基础题上无法成立，造成 token 数混杂；H-read 的推翻映射不对称，而且 LoRA 改了 k/v 投影，'同一机制'的表述强于证据；Claim 3 的前提条件未纳入推翻条件。",
  "closest_neighbors": [
    "The Piggyback Hypothesis of Generalization: Explaining and Mitigating Emergent Misalignment (2606.06667)",
    "ContextLift: Breaking the Spurious Correlation Behind Conditional Emergent Misalignment (2610.21633)",
    "Conditional misalignment: common interventions can hide emergent misalignment behind contextual triggers (2604.25891)",
    "Semantic Containment as a Fundamental Property of Emergent Misalignment (2603.04407)",
    "Activation Space Interventions Can Be Transferred Between Large Language Models (2503.04429)"
  ]
}
```
