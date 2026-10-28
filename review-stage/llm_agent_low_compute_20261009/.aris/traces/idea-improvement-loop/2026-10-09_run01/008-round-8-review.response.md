## 结论

**日期：2026-10-09。Score：7.2/10。Verdict：`promising_needs_revision`。** 新意判断为**部分新颖**：我未检索到既有工作明确实施“只有轨迹中实际调用且带失败回执的动作才允许形成负规则；未到达动作必须保持未知”这一硬约束；但轨迹级失败归因、步骤来源追踪、证据门控以及错误经验会伤害后续执行，均已被近期工作覆盖或公开提出，因而创新边界较窄。该方向值得继续，因为机制轻量、无需训练且可在同预算下证伪；当前不满足 `experiment_ready`，致命阻塞是同任务基线证据不完整：已有公开 AppWorld 实现的 ALTK-Evolve/trajectory-informed memory，以及 Memory-Collapse-Eval 的 raw-trajectory/episodic-only control，均未进入最小实验和具体同预算复现路径。

## Claim 判断

| Claim | 判断 | 关键依据 |
|---|---|---|
| 失败轨迹会把未执行步骤错误提升为负经验 | 新颖（诊断假说，尚未被证实） | 现有工作已观察错误归因、phantom strategies 与有害记忆，但未给出 AppWorld/ACE 中“未到达动作被明确禁用”的发生率；brief 已将其写成待验证假说，而非既成事实。 |
| 用真实调用轨迹与失败回执限制负规则，未到达动作保持未知 | 部分重合 | Trajectory-Informed Memory/ALTK-Evolve 已做步骤级归因、provenance 和 outcome evidence；Consistency Gap 只从实际决策路径生成 guideline。区别在于这些方法仍依赖 LLM 归因或采样稳定性，没有发现同样的确定性 attempted-action 写入门。 |
| 该约束可减少有效策略误禁并改善同预算 TGC | 新颖但因果链未闭合 | 有害抽象和错误经验降低性能已有实证；“未执行却被否定 → 后续检索后抑制有效策略 → TGC 下降”仍是本候选自己的可证伪链条，当前没有结果支持。 |
| AppWorld 固定轨迹、固定记忆 token、同模型与调用上限的最小实验 | 部分重合且有 feasibility blocker | ACE/AppWorld 入口公开，指标与预算控制可执行；但最新公开套件已提供同一 AppWorld 上的 ACE、多种记忆方法、raw-trajectory 与 no-memory control，ALTK-Evolve 也有公开实现，当前 baseline 表遗漏了最接近的可复现对照。 |

## 最高近邻

1. [Useful Memories Become Faulty When Continuously Updated by LLMs](https://arxiv.org/abs/2605.12978)（[代码与 AppWorld 复现套件](https://github.com/DylanZSZ/Memory-Collapse-Eval)）：同样研究经验抽象的有害更新，在 AppWorld 比较 ACE 等方法与 raw-trajectory control，并展示 failed attempts 产生 phantom strategies。差别是它研究跨轨迹压缩/重写失真，没有“未调用动作不得负更新”的动作级门控。
2. [Trajectory-Informed Memory Generation for Self-Improving Agent Systems](https://arxiv.org/abs/2603.10600)（[ALTK-Evolve](https://github.com/AgentToolkit/altk-evolve)）：同为 AppWorld，从完整轨迹做步骤级决策归因，生成带来源的 failure/recovery guideline；公开实现还在加入 outcome evidence。差别是其归因由 LLM 完成，未把真实工具调用回执设为负经验写入的必要条件。
3. [Closing the Consistency Gap: Self-Evolving Agents That Learn to Stay on Course](https://arxiv.org/abs/2609.08832)：在 AppWorld/ReAct 上只对决策路径中的不稳定步骤生成记忆，并有公开代码。差别是它用每步约 30 次重采样检测变动性，目标是重复执行一致性，既不检测未到达动作，也不符合本候选的低计算约束。
4. [Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models](https://arxiv.org/abs/2510.04618)（[AppWorld 代码](https://github.com/ace-agent/ace-appworld)）：是直接基础方法，使用执行反馈生成并增量整理 playbook，也证明持续有害 reflector 更新会降低性能。差别是其公开机制没有 reached-action/failed-receipt 硬门。
5. [ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory](https://arxiv.org/abs/2509.25140)：从成功与失败轨迹抽取可复用策略并保存原轨迹，失败经验确实可能成为负信号。差别是它依赖轨迹级成功/失败 judge 与 LLM 反思，未约束负结论必须对应实际执行动作，且没有 AppWorld 同任务复现路线。

```json
{"score":7.2,"verdict":"promising_needs_revision","fatal_blockers":["同任务同预算基线证据不完整：未纳入已有公开实现和 AppWorld 路径的 ALTK-Evolve/Trajectory-Informed Memory，以及 Memory-Collapse-Eval 的 raw-trajectory/episodic-only control。"],"novelty_conclusion":"以真实调用回执约束负经验写入的窄机制尚未见被明确覆盖，但轨迹归因、来源追踪、证据门控和有害抽象均已有直接近邻，新增边界较窄。","closest_neighbors":["Useful Memories Become Faulty When Continuously Updated by LLMs","Trajectory-Informed Memory Generation for Self-Improving Agent Systems / ALTK-Evolve","Closing the Consistency Gap: Self-Evolving Agents That Learn to Stay on Course","Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models","ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory"]}
```
