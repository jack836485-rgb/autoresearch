## 结论

截至 2026-11-01，**score 5.5 / 10，verdict：promising_needs_revision**。

新颖性判断：把安全语境下的工具调用失败归因为"拒绝投影 vs 与判断无关的调用偏置"的竞争，并用只用良性数据校准的偏置抵消去检验，这个组合在检索范围内还没有论文直接做过，**部分新颖**。但新颖性的边界还没有划清，原因有四点：

1. **漏引了两篇最近的同题工作**。
   - 2609.35117 在 AgentHarm 上、在几乎同一组模型（Qwen3-32B、Llama-3.1-8B、Ministral-3-8B）上已经给出"伤害信息仍在，工具语境下有效拒绝阈值更高"的解释。这与本 Idea 的"偏置抵消拒绝"在机制叙事上高度重合。
   - 2610.23071 已经估计出一个"调用准入"方向，并指出它不针对具体操作。

   因此背景中"现有工作只归因于拒绝信号下降或判断-行动耦合弱"的说法不成立，故事链里"被忽视的关键"已有一半被别人说出。
2. **"偏置抵消"本身是已有干预的一档强度**。沿调用 / 不调用方向做常数平移，就是 2608.25198 调用方向转向扫描中的一个点；IBH 只给出了取哪一档的规则。对照里缺少"同方向、多档强度的纯调用转向"，C2 的"选择性"就无法和"单纯压低调用"区分开。2610.28982 已经指出，拒绝修补主要靠压低工具使用起作用，所以这条对照是必需的。
3. **C1 的可证伪性弱**。
   - 偏置定义为拒绝投影解释不了的截距，"控制拒绝投影后偏置仍预测不安全调用率"接近同义反复。
   - 每个模型只有 6 个上下文点，做偏相关检验的统计功效极低。
   - 偏置在 When2Call 上校准，不安全调用率在 AgentHarm 上测量，两边的上下文操纵如何对齐也没有写明。
4. **C2 的超可加交互很可能由阈值的非线性自动产生**。在 sigmoid 型决策下，两个平移在比率尺度上本来就会超可加。不在 logit 尺度上检验，这个交互不能证明机制。

此外，C3 与 SafeKeep 的 schema direction 重叠。SafeKeep 的 schema direction 由 schema 与 prose 两种说明格式的激活差得到，与请求本身无关，论文已证明它与拒绝方向相反，且减去它能减少有害执行。C3 必须说明"调用偏置"与这个 schema direction 不是同一个量。

Baseline 可行性：AgentHarm（inspect_evals）、refusal_direction、agent-sae（含 Qwen3.5-9B、Ministral-3-8B 的 SAE）、activation-steering、SafeKeep 均已浅克隆核验，代码都存在。剩余问题如下：
- SafeKeep 的 demo 一次只处理单条输入，原文只用过 Llama-3.1-8B 和 Qwen2.5-7B，需要自己封装进 AgentHarm，并逐模型适配聊天模板。
- AgentHarm 原评分器是 gpt-4o，不是 gpt-4o-mini，所以"原评分器"的说法与预算不一致。
- 这些都不是致命问题。

是否值得继续：值得，问题本身有分量，算力也在约束内。但当前版本的核心 Claim 与近邻的边界还没站住，不能进入实验。

## Claim 判断

| Claim | 判断 | 最关键依据 |
|---|---|---|
| 背景：三条解释"从未放在一起检验" | 部分重合 | 2609.35117 已在 AgentHarm、同组模型上提出"阈值上移而非伤害感知下降"；2610.23071 已同时操纵拒绝方向与调用准入方向。两篇均未引用。 |
| C1：调用边际 = 拒绝投影 + 与判断无关的调用偏置，偏置随工具数量和格式变化，并独立预测不安全调用 | 部分重合 | "与判断无关的偏置"在安全语境下的定义是新的。但 2609.35117 的阈值上移、2610.23071 的准入方向（不针对具体操作）、SafeKeep 的 schema direction 已覆盖"语境带来的与判断无关的平移"。按残差定义的偏置也接近同义反复，且每模型只有 n=6。 |
| C2：只用良性数据抵消偏置，与拒绝修补超可加；同等不安全调用降幅下，良性损失低于拒绝转向和 CAST | 部分新颖，未可检验 | 偏置抵消等于 2608.25198 调用方向转向的一档强度，缺这条同方向扫描对照。超可加未指定 logit 尺度，可能只是非线性的产物。 |
| C3：扁平格式的安全收益主要经由降低调用偏置 | 部分重合 | SafeKeep 已给出"schema direction 与拒绝方向相反、减去它能减少有害执行"的机制。C3 只有证明调用偏置与 schema direction 可分离，才是新的判断。 |

## 最高近邻

1. **Tool Mediation Alters Refusal Mechanisms in Large Language Models**（arXiv 2609.35117，https://arxiv.org/abs/2609.35117）
   - 重叠：AgentHarm，8 个开源模型（含 Qwen3-32B、Llama-3.1-8B、Ministral-3-8B）；结论是伤害信息仍可解码，但工具语境下的有效拒绝阈值显著更高。
   - 差别：没有分离调用偏置，没有做恢复性干预，没有操纵工具数量和格式。
2. **Behavior Beyond Text: Evaluating Refusal Transfer Failure in LLM Agents**（arXiv 2610.28982，https://arxiv.org/abs/2610.28982）
   - 重叠：拒绝方向的激活下降，修补只部分有效且主要靠压低调用，转向强时伤害良性调用。
   - 差别：只操纵拒绝方向，没有建模调用偏置。
3. **Before Retrieval Begins: Safety and Tool-Use Decisions in LLM Agents**（arXiv 2610.23071，https://arxiv.org/abs/2610.23071）
   - 重叠：在决策 token 上估计调用准入方向（不针对具体操作），并对照转向拒绝方向，结论是两者只部分耦合。
   - 差别：单一检索工具；没有利用良性数据校准偏置，也没有检验交互。
4. **Tool Specifications Matter / SafeKeep**（arXiv 2607.29254，https://arxiv.org/abs/2607.29254；代码 https://github.com/snowcatsmoking/SafeKeep）
   - 重叠：schema direction 是与请求无关的格式平移，与拒绝方向相反，减去它能降低有害执行。
   - 差别：把这个平移归为削弱拒绝，没有与调用决策方向对照。
5. **Tunable Tool-Call Rates in LLM Agents via Representation Steering**（arXiv 2608.25198，https://arxiv.org/abs/2608.25198；代码 https://github.com/YuqiChen4188/Steering-Tool-Use-Propensity）
   - 重叠：单一线性调用方向，扫描强度可连续调节调用率；本 Idea 的偏置抵消是其中一档。
   - 差别：不涉及安全或有害请求。

（IBH 2605.18882 是本 Idea 的方法来源，只研究良性的过度调用，不涉及安全，不列入上面的最高近邻。）

```json
{
  "score": 5.5,
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "Novelty/claim: the background claim that the existing work gives only two explanations is false. 2609.35117 (AgentHarm, overlapping models) already gives the 'higher effective refusal threshold' account and 2610.23071 already estimates a call-admission direction that is not operation-specific; neither is cited.",
    "Claim/experiment: bias cancellation is a constant shift along the call direction, i.e. one strength of the call-direction steering in 2608.25198. Without a same-direction strength-sweep baseline, C2's selectivity cannot be told apart from plain call suppression.",
    "Claim: C2's superadditive interaction is not specified on the logit scale, so it may only reflect the nonlinearity of a sigmoid threshold. C1 defines the bias as the residual after the refusal projection, which is near-tautological, and n=6 contexts per model is underpowered."
  ],
  "novelty_conclusion": "Partially novel. The safety-context decomposition into refusal projection versus a judgment-independent call bias, with a bias calibrated on benign data only, has not been done directly. But the threshold-shift account (2609.35117), the call-admission direction (2610.23071), the schema direction (SafeKeep) and call-direction steering (2608.25198) together cover most of the mechanism story and the intervention form. The novelty boundary is unresolved.",
  "closest_neighbors": [
    "Tool Mediation Alters Refusal Mechanisms in Large Language Models (arXiv 2609.35117)",
    "Behavior Beyond Text: Evaluating Refusal Transfer Failure in LLM Agents (arXiv 2610.28982)",
    "Before Retrieval Begins: Safety and Tool-Use Decisions in LLM Agents (arXiv 2610.23071)",
    "Tool Specifications Matter: Uncovering and Mitigating Safety Risks in AI Agents / SafeKeep (arXiv 2607.29254)",
    "Tunable Tool-Call Rates in LLM Agents via Representation Steering (arXiv 2608.25198)"
  ]
}
```
