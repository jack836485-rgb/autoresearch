## 结论

日期：2026-10-09  
**Score：4.3 / 10**  
**Verdict：needs_rethink**

当前核心新意不足以进入实验规划。BASM 已在 AppWorld 上从成功轨迹及邻近失败轨迹构造适用条件、风险线索和规避规则，并按当前状态决定应用或抑制技能；这与“利用失败反例收紧成功经验的适用范围”实质重合。当前方案仅剩“最小反例、保留原规则并添加排除条件”这一较窄差别，但 brief 未给出可区别于一般边界提取的最小性定义或机制。

实验可证伪，但基线集合缺少 BASM、QCR 和 Sentry 等同任务直接近邻；full-code repair 不是经验适用性基线。更严重的是，截至当前日期，BASM、QCR 未找到公开实现，Sentry 仓库也明确仍在准备完整代码，因而无法满足固定 rubric 对“最强同任务基线具有已打开的公开实现和具体复现路线”的要求。**不值得按当前 Claim 继续进入实验阶段。**

## Claim 判断

| Claim | 判断 | 关键依据 |
|---|---|---|
| 反思或经验可能伤害后续行为 | 已被覆盖 | ACE 仅通过主动注入有害 reflector 输出展示退化；ExpeL 在 HotpotQA 上发现把 reflection 加入 insight extraction 会降分；Sentry 进一步实证无条件暴露失败经验会降低表现。 |
| 伤害的关键来源是经验适用范围过宽 | 已被覆盖 | BASM 明确提出 Skill Imitation Trap，并把成功技能改成带 applicability、risk、avoidance、recovery 的状态条件记录；Sentry 将错误归因于 failure knowledge 的条件变量不正确；QCR 同样要求在目标状态不满足前提时拒绝复用。 |
| 用失败反例收紧条件而非全局删除经验 | 部分重合 | BASM 已将成功上下文与邻近失败上下文配对，失败仅作为边界字段的证据，并保留原有 procedure；当前方案的“最小排除条件”尚未形成足以区分二者的独立机制。 |
| 在 AppWorld 上进行同预算、状态条件化经验复用实验 | 已被覆盖 | QCR 已在 AppWorld 固定候选检索、目标状态、模型、解码和工具预算，只改变历史经验的表示与使用；BASM 也在 AppWorld 比较 Base、Proc. Skill、App. Skill 和完整边界记忆。 |
| 当前 baseline 足以验证独立贡献 | 已被覆盖/不可行 | ACE 是有效开放基线，但 ReAct 与 full-code repair 不能替代 BASM、QCR、Sentry；后三者又缺少当前可核验的完整公开复现实现，构成致命 feasibility blocker。 |

## 最高近邻

1. [When Not to Imitate: Boundary-Aware Skill Memory for Reliable Tool-Use LLM Agents](https://arxiv.org/html/2608.22339)：同样在 AppWorld 从成功轨迹和邻近失败轨迹提取适用条件、风险与规避边界，并按状态检查；差别仅在当前方案声称生成“最小排除条件”，但其最小性尚未定义。未找到公开代码。
2. [Beyond Retrieval: Query-Conditioned Reuse of Long-Horizon Agent Trajectories](https://arxiv.org/html/2608.12847)：同样在 AppWorld 用 applicability conditions 防止状态变化后的错误经验复用，并采用固定模型、状态、解码和工具预算的对照；差别是 QCR 每次针对目标查询生成支持，而非用 dev 失败永久收紧已有规则。未找到公开代码。
3. [Sentry: Learning to Recover from LLM Agent Failures at Test Time](https://arxiv.org/abs/2610.02994)：直接论证失败知识是条件知识，在 AppWorld 按当前失败状态检索带 trigger pattern 的经验；差别是它学习并调用恢复经验，而非编辑成功规则的适用域。[仓库](https://github.com/nuglifeleoji/Sentry)当前说明完整代码仍待发布。
4. [Agentic Context Engineering](https://arxiv.org/html/2510.04618)：同一 AppWorld 上维护带 helpful/harmful 计数的增量 playbook，并证明有害 reflector 输出可导致退化；差别是 ACE 依赖全局计数、合并和过滤，没有显式状态适用边界。[官方 AppWorld 实现](https://github.com/ace-agent/ace-appworld)可复现。
5. [COUNTERMEM](https://arxiv.org/abs/2609.31874)：从失败动作生成并验证局部替代方案，保存带复用条件的纠正记录，且消融显示移除 applicability condition 会增加有害复用；差别是它需要可执行反事实 rollout 和训练选择策略，未在 AppWorld 评估，也没有公开代码。

```json
{"score":4.3,"verdict":"needs_rethink","fatal_blockers":["核心 Claim 已被 BASM 在同一 AppWorld 任务上以成功轨迹加邻近失败证据、显式适用条件和状态检查实质覆盖","最小实验遗漏 BASM、QCR、Sentry 等直接同任务近邻，ReAct 与 full-code repair 不能替代经验适用性基线","截至 2026-10-09，BASM、QCR 未找到公开实现，Sentry 完整代码尚未发布，无法满足公开实现与具体复现路线要求"],"novelty_conclusion":"最小反例排除这一表述具有局部差别，但当前未形成区别于 BASM 边界提取的独立机制；总体核心已被覆盖，不应进入实验规划。","closest_neighbors":["When Not to Imitate: Boundary-Aware Skill Memory for Reliable Tool-Use LLM Agents","Beyond Retrieval: Query-Conditioned Reuse of Long-Horizon Agent Trajectories","Sentry: Learning to Recover from LLM Agent Failures at Test Time","Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models","COUNTERMEM: World-Model Verified Counter-Factual Memory for Language Agents"]}
```