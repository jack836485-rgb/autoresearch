## 结论

2026-10-28 评审：**score 8.2，verdict = experiment_ready**。

- **新颖性：** 成立，但属于增量型机制分析。我检索到的条件失配工作（ContextLift 2610.21633、Dubiński et al. 2604.25891、BCT 封堵 inoculation 的 2606.05817、Su et al. 2601.23081）都只有行为或表示层证据，没有对情境句位置做因果修补。Piggyback 2606.06667 有位置级 KV 修补，但只评测无 cue 题，并把"用户 query 特征也可能是载体"明确列为未来工作。所以本 Idea 是把一个已有方法推进到一个未被检验的设置，不是重新发明。真正新的内容有两点：
  - 用同提示前置中性句做对照、H-pos 与 H-read 都有正面判据的门控判别。
  - "TReFT 是否把广泛 EM 转成条件 EM"的检验，并且在回答层把泄漏与广泛分开。
- **证据链：** 我核对了关键数字，都与原文一致。
  - ContextLift 表 4：B 类 17.0/35.9/52.4%。
  - 残余回答的人工阅读只针对 ContextLift 臂，74/89/90% 是在回答情境句。
  - Piggyback 中 Qwen-2.5-7B 的 General 分从 39.7 升到 86.5；修补 query 的增益更小，也不稳定；query 特征列为未来工作。
  - Dubiński 没有做机制分析，并认为 cue 下的失配是广泛的。
- **Baseline：** 两个仓库在 2026-10-28 都能访问，所列文件都存在（`configs/*/{baseline,interleaving_wg,interleaving_wglift}.yaml`、`scripts/{classify_cued_prompts,residual_cued}.py`、`release/src/{sft,intervention}.py` 等）。`residual_cued.py` 对每个 cue 有一条话题关键词规则，可以用于任意臂。所有 baseline 都是同领域、同任务，复现路径具体。
- **非致命问题（不阻断）：**
  - 冻结 Anchor 中"触发空间的系统化搜索"这一瓶颈没有覆盖。本 Idea 只覆盖"已缓解模型在条件触发下的表现"。
  - 前置中性句因为因果掩码，本来就不可能携带 cue 信息。所以它只能排除"修补任何用户段都会扰动"这类解释，不能作为位置特异性的强对照。
  - security 的 cue 效应约 15pp，样本量下 r_cue 的 CI 可能过宽；H-read 的 20% 等价界也可能很难达到。不过"3 个数据集中至少 2 个"的规则和"不确定"格可以兜住这些情况。
  - 反向证据的引用不全。2503.04429 我没能核实（抓取被拒）；而 Lasnier et al.（2602.10382）和 Kulumba et al.（2605.18646）在 token 级后门上发现触发信息汇聚在触发位置的末 token。这为 H-pos 提供了先验，会削弱"事先无法确定"这一说法，但不推翻语义情境触发仍未被检验这一点。
  - 2608.29118 抓取被拒，没能核实。
- **是否值得继续：** 值得，进入实验规划。

## Claim 判断

| Claim | 判断 | 最关键依据 |
|---|---|---|
| 现有失败：通用交织后 broad cue 题仍有 17.0/35.9/52.4% 的失配 | 有据（已核实） | ContextLift 附录 A 表 4 |
| 空白：条件失配没有位置级因果证据，通用交织臂也没有泄漏/广泛分解 | 新颖（已核实） | ContextLift、Dubiński、BCT 帖都是纯行为证据；ContextLift 的残余阅读只针对 ContextLift 臂 |
| Claim 1：只把 cue 句 K/V 换成基座值就能削减 ≥50% 的 cue 效应（H-pos），并与 H-read 做正面判别 | 新颖；方法与 Piggyback 部分重合 | Piggyback 只修补模板与 query，只评测无 cue 题；后门修补工作用的是良性 token 触发，不涉及 EM 和语义情境 |
| Claim 1 的回答层分解（泄漏与广泛） | 新颖 | 已有工作没有按 B 类、对通用交织臂做这一分解 |
| Claim 2：TReFT 把广泛 EM 转成条件 EM，且剩余广泛 cue 效应由 cue 句承载 | 新颖；现象层与 Dubiński 部分重合 | Dubiński 只说明数据类缓解会把 EM 藏到触发之后，没有测 TReFT 这类位置约束防御；Piggyback 没有测触发 |
| 最小实验能与近邻区分（同代码、同数据、同步数，判定事先固定） | 成立 | 4 臂共用 ContextLift 训练代码，约 86 A100 小时；判定表有正面推翻条件 |

## 最高近邻

1. **The Piggyback Hypothesis of Generalization（TReFT）**：https://arxiv.org/abs/2606.06667 ，仓库 https://github.com/CHATS-lab/Token-Regularized-Fine-Tuning 。重叠：位置级 KV 修补，把广泛 EM 定位到模板 prefix，并提出 TReFT。差别：只评测无 cue 题；query 修补只作对照，"query 特征是否也是载体"留作未来工作；没有检验 TReFT 是否留下条件失配。
2. **ContextLift（When Does Interleaving Prevent EM / 2610.21633）**：https://arxiv.org/abs/2610.21633 ，仓库 https://github.com/davidkaczer/contextlift 。重叠：相同的模型、数据集、cue 题和 B 类划分，把条件失配解释为伪相关。差别：没有机制实验；泄漏阅读只做了 ContextLift 臂，没有按 B 类分开。
3. **Conditional misalignment: common interventions can hide EM behind contextual triggers（Dubiński et al.）**：https://arxiv.org/abs/2604.25891 。重叠：最早报告条件失配现象，并认为触发后的失配是广泛的。差别：纯行为证据；没有 TReFT 这类位置约束防御；没有正式的窄域与广泛分解。
4. **Language Triggers Hijack Language Circuits（Lasnier et al.）**：https://arxiv.org/abs/2602.10382 ，以及同组的 https://arxiv.org/abs/2605.18646 。重叠：在触发 token 的位置和层上做激活修补，发现触发信息汇聚在触发末 token。差别：触发是预训练注入的良性语言切换 token 序列，不涉及语义情境和 EM。
5. **BLOCK-EM: Preventing EM by Blocking Causal Features**：https://arxiv.org/abs/2602.00767 。重叠：在 EM 上区分 prompt 位置和 decode 位置做修补。差别：不研究条件或触发失配，也不修补情境句位置。

```json
{
  "score": 8.2,
  "verdict": "experiment_ready",
  "fatal_blockers": [],
  "novelty_conclusion": "No published work does position-level causal patching of cue-sentence K/V for conditional emergent misalignment, splits generic-interleaving residuals into narrow leakage vs broad, or tests whether TReFT converts broad EM into conditional EM. The novelty is incremental: it extends Piggyback's KV patching to a setting Piggyback listed as future work. The causal chain and baselines check out (both repositories verified 2026-10-28). Non-blocking issues: the Anchor's trigger-space search is not covered; the pre-cue neutral control cannot carry cue information by construction; security may be underpowered; the token-trigger patching literature that sets the H-pos prior is not cited.",
  "closest_neighbors": [
    "The Piggyback Hypothesis of Generalization: Explaining and Mitigating Emergent Misalignment (arXiv 2606.06667)",
    "ContextLift / When Does Interleaving Prevent Emergent Misalignment? (arXiv 2610.21633)",
    "Conditional misalignment: common interventions can hide emergent misalignment behind contextual triggers (arXiv 2604.25891)",
    "Language Triggers Hijack Language Circuits: A Mechanistic Analysis of Backdoor Behaviors in LLMs (arXiv 2602.10382)",
    "BLOCK-EM: Preventing Emergent Misalignment by Blocking Causal Features (arXiv 2602.00767)"
  ]
}
```
