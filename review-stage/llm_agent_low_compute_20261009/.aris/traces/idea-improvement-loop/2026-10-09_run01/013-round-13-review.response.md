## 结论

日期：2026-10-09。**Score：7.2/10；Verdict：`promising_needs_revision`。** 精确地把 `call_id/name/args/result` 绑定到负经验，并用“未执行只能未知、真实报错只能限定到观察条件、调用成功但任务失败不能推出该动作有害”的确定性规则限制结论强度，仍未被下列近邻完整覆盖；它比一般的轨迹反思或根因归因更窄，也更可检验。

但新颖性边界已被 BASM 显著压缩：BASM 同样在 AppWorld 上使用失败上下文生成 risk cues、avoidance rules 和 recovery notes，以确定性验证器筛除不合规技能，并在执行时检查是否应抑制工具调用。当前最小实验没有 BASM 或其等价、可核验复现的同预算对照；截至本日，BASM 论文也未给出可核验的公开代码入口。因而实验尚不能排除收益只是既有“失败边界 + avoidance rule”机制的一个更硬模板化实现。这是当前的 fatal feasibility/novelty-boundary blocker。Idea 值得继续做诊断性验证，但尚未达到 experiment-ready。

## Claim 判断

| Claim | 判断 | 关键依据 |
|---|---|---|
| 失败轨迹会把“未执行、局部工具报错、后续任务失败”升级成过强禁用建议 | 部分重合、具体细分尚未覆盖 | Memory-Collapse 已展示失败尝试可产生 phantom strategies，BASM 已展示不带有效边界的记忆会提高错误工具偏好；但未找到一级工作逐项量化这三种 AppWorld 执行证据的“证据越级率”。brief 将其写成待诊断假设，表述合格。 |
| 依据真实调用结果，在写入前确定性限制负结论的类型与作用域 | 部分重合但仍有独立点 | BASM 已从失败上下文构造风险、禁用和恢复边界，并进行确定性 schema/tool 校验；Trace2Skill 会丢弃无法得到因果解释的失败补丁。两者都未把每条负结论绑定到具体 `call_id/result`，也未给出该三态结论强度格。 |
| 不做反事实 rollout 或昂贵根因归因，也能减少无根据禁用且保留有效抽象 | 新颖、未验证 | ALTK 用 LLM 回溯 immediate/proximate/root cause；DeFA 用依赖图和多次 LLM 调用定位决定性错误。这里明确不声称根因，只限制可写出的结论，机制不同；但是否能同时改善 TGC/SGC 与规则保留率仍完全取决于待跑实验。 |
| 在统一 actor、检索和 token/API 预算下优于 raw trajectory 与自然语言提醒 | 可证伪，但当前不能充分区分最高近邻 | raw、提醒、ACE、ALTK 与确定性门的对照能区分“保留证据”“提示三态”和“执行约束”；然而同任务、同目标的 BASM 未进入最小实验，故正结果仍不能确立相对最高近邻的独立贡献。 |

## 最高近邻

1. [When Not to Imitate: Boundary-Aware Skill Memory for Reliable Tool-Use LLM Agents](https://arxiv.org/abs/2608.22339)（Lin et al., 2026）：同在 AppWorld，从成功/失败上下文提取 applicability、risk、avoidance、recovery 字段，并用 checker 抑制错误调用；差别是它不按具体调用结果限制负结论的证据强度。论文未给出可核验公开代码。
2. [Trace2Skill: Distill Trajectory-Local Lessons into Transferable Agent Skills](https://arxiv.org/abs/2603.25158)（Ni et al., 2026）：失败分析会检查轨迹、产物与 ground truth，无法因果解释的失败不进入技能补丁；差别是其验证依赖 agentic analyst，不是 AppWorld 调用结果上的廉价确定性门。
3. [Trajectory-Informed Memory Generation for Self-Improving Agent Systems](https://arxiv.org/abs/2603.10600)（Fang et al., 2026）：在 AppWorld 上做 step-level 决策归因并生成带 provenance 的 recovery/negative guidance；差别是归因由 LLM 回溯推断，未限制“成功调用但全局失败”可导出的负结论。
4. [Useful Memories Become Faulty When Continuously Updated by LLMs](https://arxiv.org/abs/2605.12978)（Zhang et al., 2026）：证明抽象会引入 phantom strategies，主张保留原始 episode 并显式 gate consolidation；差别是其 gate 为一般性结论，未给出调用级证据格或负条目作用域约束。
5. [DeFA: Dependency-Guided Failure Attribution for LLM Agents](https://arxiv.org/abs/2610.01256)（Deng et al., 2026）：把 protocol/tool-result 关系与语义依赖组成 failure-propagation evidence，并证明诊断可改善 Trace2Skill；差别是目标是决定性错误定位，成本与本方法“只约束可下结论范围”的目标不同。

```json
{
  "score": 7.2,
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "最小实验未纳入或提供可复现的最高同任务近邻 BASM 对照；BASM 已在 AppWorld 上从失败上下文生成 risk/avoidance/recovery 边界并执行工具调用检查，而截至 2026-10-09 未核验到其公开代码，因此当前无法在同预算下区分本方法与该既有机制。"
  ],
  "novelty_conclusion": "调用结果绑定的三态负结论强度约束仍有独立新意，但 BASM 已覆盖失败边界、avoidance rule 和调用抑制的主要外层机制；缺少对该最高近邻的可复现实验区分，当前不能判定 experiment-ready。",
  "closest_neighbors": [
    "When Not to Imitate: Boundary-Aware Skill Memory for Reliable Tool-Use LLM Agents",
    "Trace2Skill: Distill Trajectory-Local Lessons into Transferable Agent Skills",
    "Trajectory-Informed Memory Generation for Self-Improving Agent Systems",
    "Useful Memories Become Faulty When Continuously Updated by LLMs",
    "DeFA: Dependency-Guided Failure Attribution for LLM Agents"
  ]
}
```
