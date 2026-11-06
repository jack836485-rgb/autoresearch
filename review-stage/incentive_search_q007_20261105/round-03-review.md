## 结论
2026-11-05：总体 score 5.5，verdict = `promising_needs_revision`。主贡献是在一个自建的"硬约束 + 总价最低"购物环境里，用 LLM 抽取属性，再由 Weitzman/部分开箱的指数规则决定查看顺序、停止和结账前揭示，另配一套顺序/停止/揭示前提交的损失分解。按当前设计，这个贡献不够。原因有三。第一，环境与机制都是自建的，而规则本身不看页面位置、只买已揭示完整成本的候选，所以"抗赞助位、偏好排序、滴漏定价"在很大程度上由构造保证，难以说明它解决了 CAVEAT 揭示的那类问题。第二，"把 LLM 抽取与确定性决策分开"并以 Pandora/VOI 控制搜索，近邻已有相当覆盖。第三，brief 称 CAVEAT 未公开代码，但 github.com/microsoft/CAVEAT 已公开 9 个环境和 caveat-harness，同任务强基线与环境的定位因此有误。

## Claim 判断
| 维度 | 分数 | 依据 |
|---|---|---|
| 重要性 | 6.0 | 问题本身重要：CAVEAT 显示引导开启后最优购买率从 78.6% 降到 17.3%，harness 带来 2.6× 运行时间、2.3× 步数，Qwen3.5-27B 配 harness 只有 4.2%，用接近基线的调用数修复确有价值。但方案把目标限定为"约束下总价最低"这种单一标量，CAVEAT 中的多属性偏好、目标漂移、强加未声明优先级都在主张外。三类机制在自建环境中又是按规则能免疫的方式实现的，成功后能说明的多半是"标量目标、独立价值时，规则决策不受位置影响"。这个结论有用，但影响范围有限。 |
| 新颖度 | 5.5 | 已有工作覆盖了几个关键部分：CTA 已把 Pandora's Box 作为 LLM agent 任务并给出 oracle 规则；2605.05701 已有基于 VOI 的搜索动作/停止控制器；2606.07392 已把 Weitzman 指数用于 LLM 调用级联；CAM-DF 已做代价感知停止。"LLM 抽取、规则决策"是常见的神经符号分工。可辨认的增量在于：把部分开箱对应到滴漏定价，以及把这套框架用于界面引导鲁棒性。损失分解本质上是常规的"与参照策略对比"诊断，且"滴漏定价对应揭示前提交损失"在定义上近乎同义反复。 |
| 有效性 | 6.0 | 现有依据：Weitzman 规则在独立价值、已知分布下最优，且与呈现顺序无关；CAVEAT 的单机制隔离说明前三类机制确实作用于"先看谁、何时见成本"。这些依据只适用于自建环境，因为那里的机制按规则可免疫的方式实现，所以在真实属性下恢复匹配对照几乎是必然的。未知部分才是关键：7–8B 模型的属性抽取与约束判断准确率；任务内少样本下在线估计隐藏费用分布是否可靠；价值相关时损失多大；CAVEAT 中更复杂的引导（如赞助位叠加搜索过滤、多属性偏好）下规则能否保持。CTA 的反向证据也要考虑：Qwen3-8B 拿到先验并思考后，在 Pandora 任务上达到 94% 的 oracle 匹配率，Claim 3（同调用数下胜过 CTA 式）未必成立。 |

- **与起点问题的关系**：本方案回答的是原问题，只取三类机制，并把目标改成标量总价。原问题里"目标漂移、未声明优先级"导致的失败，以及另外五类机制，仍未回答。转向本身不构成阻断。
- **实验能否判别主张**：部分能。Claim 2 的"真实属性 vs 模型抽取属性"对照可以区分"读页面"和"搜索决策"这两个瓶颈，设计合理。有三处问题：
  - 机制与规则都由作者实现，"恢复到接近匹配对照"没有判别力，"接近"也未量化。
  - 1.3× 只统计工具调用，没有计入每个候选的 LLM 抽取与信念调用及其 token；token 稀缺正是本主张的成本口径。
  - 官方 CAVEAT 环境与 caveat-harness 代码已公开，却改用 WebShop 自建环境和独立复现的 harness，最强同任务对照因此不可信。CAVEAT-27B 后训练这条开源模型路线也没有作为对照。
- **可行性：pass**。WebShop 与 CAVEAT 都可本地运行且无需 KVM。8B 模型约 10 万 episode、每个约 30 步，用 vLLM 在 8×A100 上数天内可完成。实际条件数是 10 种方法 × 约 5 种引导配置，brief 写的"约 8 个条件"低估了，但仍在 5 天内。API 侧只测 4 个条件、每任务 1 次，在 1000 元内勉强可行，但这样做不出 Wilson 区间所需的 3 次重复。WebShop 原生属性有噪声，又没有结账费用页，需要人工校核约束标签并改造结账流程，约 1 周人力是合理的。

## 最高近邻
1. CAVEAT（https://arxiv.org/abs/2609.27273；代码 https://github.com/microsoft/CAVEAT，MIT，含 9 个环境与 caveat-harness）：同任务、同机制，含 harness 与 CAVEAT-27B 后训练。差别在于本方案用规则决策来降低调用。brief 中的"2.3× 工具调用"在论文中无对应数据（论文只报 2.6× 运行时间、2.3× 步数），"无代码"也与事实不符。
2. Calibrate-Then-Act（https://arxiv.org/abs/2602.16699）：已有 Pandora's Box 任务与 oracle 策略；8B 模型拿到先验后接近 oracle。差别在于它由 LLM 决策，而且不是网页购物。
3. Inference-Time Budget Control for LLM Search Agents（https://arxiv.org/abs/2605.05701）：用 VOI 控制器决定检索与停止。差别在于它做的是多跳问答，不涉及隐藏成本或界面引导。
4. Online Pandora's Box for Contextual LLM Cascading（https://arxiv.org/abs/2606.07392）：用 Weitzman 指数决定 LLM 调用顺序与停止。差别在于对象是模型级联，而非 agent 的网页搜索。
5. Scores Are Not Decisions / CAM-DF（https://arxiv.org/abs/2607.27083）：在排好序的前缀上做代价感知停止。差别在于本方案的顺序由指数决定，并有两级检查。

```json
{
  "score": 5.5,
  "contribution_scores": {"importance": 6.0, "novelty": 5.5, "effectiveness": 6.0},
  "contribution_assessment": "主贡献是自建'硬约束+总价最低'购物环境中的 LLM 抽取 + Weitzman/部分开箱指数决策控制器，并配顺序/停止/揭示前提交的损失分解。重要性有限：标量目标排除了 CAVEAT 的多属性偏好与目标漂移，机制又由作者按规则可免疫的方式实现。新颖度为增量：CTA 已有 Pandora 任务与 oracle，VOI 搜索控制器、Pandora 级联、CAM-DF 覆盖了规则式代价感知搜索。有效性依据只在构造环境内较强；关键未知是 7–8B 模型的属性抽取准确率、少样本费用估计、价值相关性，以及在官方 CAVEAT 环境中能否保持。CTA 中 8B 模型拿到先验即接近 oracle，可能推翻 Claim 3。",
  "feasibility": "pass",
  "feasibility_reason": "WebShop 与公开的 CAVEAT 环境都可本地运行、无需 KVM；8B 模型约 10 万 episode 可在 8×A100 上 5 天内完成；API 部分在 1000 元内勉强可行，但只能做单次重复；结账费用页与约束标签需约 1 周人工改造。",
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "贡献门槛未达：三项分数 6.0/5.5/6.0，没有任何一项 ≥8",
    "定位与强基线错误：CAVEAT 代码与环境已在 github.com/microsoft/CAVEAT 公开（含 caveat-harness），brief 却称无代码、改用自建环境并独立复现 harness；也未把 CAVEAT-27B 后训练路线作为开源模型对照",
    "Claim 判别力不足：三类机制与规则都由作者实现，规则不看位置、只买已揭示成本候选，'恢复到接近匹配对照'由构造保证，且'接近'未量化",
    "成本口径不完整：1.3× 只计工具调用，未计每候选的 LLM 抽取/信念调用与 token，而 token 稀缺正是主张的成本口径",
    "引用不准确：CAVEAT 未报告 2.3× 工具调用倍数，也未明确提出需要'更高效的停止与验证策略'（原文只提降低 interaction cost）"
  ],
  "novelty_conclusion": "增量新意：把 Weitzman/部分开箱规则用作购物 agent 的决策层以抵抗界面引导。CTA（Pandora 任务 + oracle）、VOI 搜索控制器、Pandora LLM 级联与 CAM-DF 已覆盖规则式代价感知搜索的核心思想；损失分解是常规的参照策略对比诊断。",
  "closest_neighbors": [
    "CAVEAT: Towards Robust Computer-Use Agents in Incentive-Misaligned Environments (arXiv:2609.27273)",
    "Calibrate-Then-Act: Cost-Aware Exploration in LLM Agents (arXiv:2602.16699)",
    "Inference-Time Budget Control for LLM Search Agents (arXiv:2605.05701)",
    "Online Pandora's Box for Contextual LLM Cascading (arXiv:2606.07392)",
    "Scores Are Not Decisions: Cost-Aware Stopping for Tool Acquisition in LLM Agents (arXiv:2607.27083)"
  ]
}
```
