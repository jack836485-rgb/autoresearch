## 结论

截至 2026-10-28：**score 8.2，verdict = experiment_ready**。

新颖性：我做了检索。在条件失配（contextual cue 触发的 EM）上，没有找到任何位置级因果实验，也就是"只把 cue 句位置的 K/V 换回基座值"这类实验。最接近的几条工作各缺一块：
- ContextLift 与 Dubiński et al. 只有行为层结果。
- Piggyback 只修补模板与 query，且只在无 cue 题上评测。
- BLOCK-EM 只区分"prompt 段 vs 生成段"，不涉及 cue。
- 后门机制工作研究的是显式触发词，不是语义情境句，也不是 EM。

"H-pos 与 H-read 各有正面判据"和"TReFT 是否把广泛 EM 转成条件 EM"这两点，去掉近邻名字后仍然成立。它们不是在修补或补完某一篇论文。

可行性：
- 两个 baseline 仓库都能访问，所需文件都已核验存在：ContextLift `arxiv` 分支的 configs 与 scripts，TReFT `release/src/sft.py`、`intervention.py` 及 extract/patch 脚本。
- 两者都在 Qwen2.5-7B 上有报告，与本任务同域、同评测。
- 预算约 86 A100 小时加不到 400 元 judge 费用，在约束之内。

故事链有据可查：
- ContextLift 表 4 的 B 类数字（17.0/35.9/52.4%）已核实。
- 它的残余回答人工阅读只覆盖 ContextLift 臂，已核实。
- Piggyback 把 query 特征留作未来工作，没有做 cue 评测，已核实。

非致命风险：
- 分量层判定，尤其是 security 数据集和 Claim 2 用到的广泛分量，统计功效偏紧。
- Claim 2 的推翻条件是"CI 含 0"，这一条不是等价检验。
- 修补后 coherence 过滤可能人为压低失配率。
- 训练超参的出处应为 ContextLift 附录 F 表 7，brief 写成了附录 E。

值得继续，可以进入实验规划。

## Claim 判断

| Claim | 判断 | 最关键依据 |
|---|---|---|
| 背景空白：条件失配缺少位置级因果证据，通用交织臂也没有回答层的泄漏/广泛分解 | 新颖（空白属实） | ContextLift 没有任何机制或修补分析，人工阅读只覆盖 ContextLift 臂；2604.25891 可见正文只有行为分析；Su et al. 与 2608.29118 不做位置级修补 |
| Claim 1：在通用交织臂的 broad cue 题上，cue 句 K/V 换回基座值能消掉 ≥50% 的 cue 效应，且削减显著大于等长前置中性句（H-pos 与 H-read 二分） | 新颖 | Piggyback 只修补模板与等量 query token，且不含 cue 题；BLOCK-EM 只按 prompt/生成段修补；2605.18646 在显式后门上发现触发信号被搬运到末位置，所以 H-read 是现实的对立结果，结论事先不可预知。风险一：中性句与 cue 句的微调偏离幅度不同，d 与"扰动幅度"部分混淆。风险二：security 的 cue 效应约 12pp，按每题 3 条采样，r_cue 的 CI 会很宽，判定实际主要依赖 legal 与 medical |
| Claim 2：相对 EM-only，TReFT 对无 cue 广泛失配的降幅显著大于对 broad cue 广泛分量的降幅；在 TReFT 臂上，cue 句修补能消掉剩余广泛 cue 效应的至少一半 | 部分重合（测量对象新，评测思路已有先例） | Dubiński 已证明多种缓解会把 EM 藏到 cue 后面，Piggyback 引用了它但没有检验 TReFT；把它扩展到位置约束型防御，并在回答层剔除"按设计的窄域泄漏"，是新的部分。推翻条件"CI 含 0"会把功效不足与被推翻混在一起 |
| 方法：逐提示的基座 K/V 位置级修补，加泄漏/广泛判定器（κ≥0.7，否则回退到关键词规则） | 不是简单重标；工具已有，判别设计新 | 修补工具直接来自 Piggyback 的 `intervention.py`；新的部分是同提示等长中性句对照、等价界判据和对称的回答层分解 |
| 最小实验能在同一预算下区分本 Idea 与近邻 | 成立 | 4 个臂共用同一套训练代码、同样的数据与步数；ContextLift 的 B 类分类脚本与 `residual_cued.py` 都可直接用；TReFT 的惩罚项可以移植，Qwen2.5-7B 上的 λ 有表可查（10 或 30） |

## 最高近邻

1. **ContextLift**（Mai & Kaczér），https://arxiv.org/abs/2610.21633
   - 重叠：同模型、同数据；通用交织臂的 B 类 cue 失配率；残余回答多为"回答情境句"。
   - 差别：没有任何机制或修补分析；人工阅读只覆盖 ContextLift 臂。
2. **Conditional misalignment: common interventions can hide EM behind contextual triggers**（Dubiński et al.），https://arxiv.org/abs/2604.25891
   - 重叠：提出条件失配，并检验多种缓解（数据混合、HHH 后训练、inoculation 等）。
   - 差别：只做行为评测，主要在 GPT-4o/4.1 上；没有检验 TReFT，也没有位置级因果分析。
3. **The Piggyback Hypothesis / TReFT**，https://arxiv.org/abs/2606.06667
   - 重叠：用模板 KV 修补定位广泛 EM（Qwen-2.5-7B 上 39.7→86.5），并提出 TReFT。
   - 差别：只在无 cue 题上评测；query 特征留作未来工作；没有检验防御后是否残留触发。
4. **BLOCK-EM**（Ustaomeroglu & Qu），https://arxiv.org/abs/2602.00767
   - 重叠：用激活修补分析 EM 再涌现（prompt 段 vs 生成段，逐层）。
   - 差别：不研究 cue 或条件失配，也没有定位到具体情境 token。
5. **Language-Switching Triggers Take a Latent Detour Through Language Models**（Kulumba et al.），https://arxiv.org/abs/2605.18646
   - 重叠：对后门触发词做位置级修补，发现信号被搬运到末位置后读出。
   - 差别：研究的是显式拉丁语触发词和语言切换，不是语义情境 cue，不是 EM，也没有与基座 K/V 对比。

```json
{
  "score": 8.2,
  "verdict": "experiment_ready",
  "fatal_blockers": [],
  "novelty_conclusion": "No prior work does position-level causal localization of contextual-cue conditional misalignment (base-model K/V substitution at cue positions with a length-matched neutral-sentence control and an equivalence bound for H-read), and none tests whether the position-constrained defense TReFT turns broad EM into cue-conditional EM after removing designed narrow-domain leakage. ContextLift and Dubiński are behavioral only; Piggyback patches template/query on uncued prompts only. Non-fatal risks: limited power for component-level and security judgments, Claim 2's refutation is not an equivalence test, and the coherence filter under patching may bias rates.",
  "closest_neighbors": [
    "ContextLift: Breaking the Spurious Correlation Behind Conditional Emergent Misalignment (2610.21633)",
    "Conditional misalignment: common interventions can hide emergent misalignment behind contextual triggers (2604.25891)",
    "The Piggyback Hypothesis of Generalization: Explaining and Mitigating Emergent Misalignment (2606.06667)",
    "BLOCK-EM: Preventing Emergent Misalignment via Latent Blocking (2602.00767)",
    "Language-Switching Triggers Take a Latent Detour Through Language Models (2605.18646)"
  ]
}
```
