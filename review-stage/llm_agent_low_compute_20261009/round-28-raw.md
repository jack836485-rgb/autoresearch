## 结论

日期：2026-10-09。**Score：6.9/10**；**Verdict：`promising_needs_revision`**。新意结论是**部分重合，仍有较窄的机制差异**：DRAFT 和 DocsChisel 已覆盖“从工具交互/失败轨迹中学习并修改工具文档”，ACE 又在 AppWorld 上覆盖了“根据执行反馈做局部增量上下文更新”。本候选仍未被明确覆盖的部分，是把实际返回结构与 agent 生成的访问表达式做 CPU 级结构对照，且只修改被反例否定的字段路径并保留例外。

该方向**值得继续，但当前不足以进入实验规划**。AppWorld 原文确实将缺失、不完整或过时 response schema 列为值得研究的更难设置，但它同时说明当前 AppWorld 文档由 FastAPI 自动生成、返回会遵循公开 schema；因此 brief 中的错误是待注入的诊断条件，不是原论文已观测的 agent 失败。官方 ReAct/full-code 代码和 CLI 路线可核验，但当前对照集遗漏了同一 AppWorld 任务、公开实现、同样利用执行反馈更新上下文的 ACE；而且“固定缺字段/类型扰动”还没有冻结到可核验的 endpoint、字段集、扰动映射和运行入口。按本 rubric，这两点构成当前 fatal feasibility blockers。

## Claim 判断

| Claim | 判断 | 关键依据 |
|---|---|---|
| 缺失/过时 response schema 是 AppWorld 支持的研究问题 | 已被覆盖（问题定义） | [AppWorld 论文](https://aclanthology.org/2024.acl-long.850.pdf) Appendix A 明确建议消融 response schema，让 agent 通过交互识别返回结构；这是 future setting，不是原 benchmark 中已报告的失败来源。 |
| 用交互反馈/失败轨迹修正工具文档或接口理解 | 已被覆盖 | [DRAFT](https://arxiv.org/abs/2410.08197) 从交互结果迭代改写文档；[DocsChisel](https://arxiv.org/abs/2608.10037) 从失败轨迹识别文档问题并在 information-field 级增删修改；[ACE](https://arxiv.org/abs/2510.04618) 从自然执行反馈生成局部 delta context。 |
| 实际返回 × agent 访问表达式的 CPU 结构对照，仅修改被反例否定的字段路径并记录例外 | 新颖/部分重合 | 未在上述一级近邻中找到该精确组合。但其上位范式“反馈驱动的局部文档/上下文修订”已由 DocsChisel 和 ACE 占据，因而新意只能落在确定性结构检查与最小修订边界上。 |
| 最小 schema 修订在同预算下比报错重生成或全量重读更少重复访问错误，且提升 TGC/成本 | 新颖但未证实 | 这是清晰可证伪的实验性 Claim，尚无结果。当前 brief 没有冻结扰动实例与修改后的可运行入口，且没有纳入同任务的公开 ACE 对照，故尚不满足 experiment-ready 标准。 |

## 最高近邻

1. [DocsChisel: Adaptive Tool Documentation Optimization Framework for LLM Agents](https://arxiv.org/abs/2608.10037) — 从目标 agent 的失败执行轨迹识别 documentation-related issues，并在工具的 information-field 级增、删、修。差别是它用 LLM 和多轮重执行优化整体文档，在 WorkBench/API-Bank 评估；未见 AppWorld 上由真实返回驱动的确定性字段路径修订。
2. [From Exploration to Mastery (DRAFT)](https://arxiv.org/abs/2410.08197) （[公开代码](https://github.com/quchangle1/DRAFT)）— 已直接覆盖“文档不完整/不准确/过时 + 工具交互反馈 + 动态文档修订”。差别是 DRAFT 用自生成探索实例及 LLM Analyzer/Rewriter 做全文档迭代，而本候选限定为当前任务观测到的 schema 反例和单路径修订。
3. [Agentic Context Engineering (ACE)](https://arxiv.org/abs/2510.04618) （[AppWorld 公开实现与复现命令](https://github.com/ace-agent/ace-appworld)）— 同样从执行成败中提取经验，以局部 delta 更新可持续复用的上下文，且直接在 AppWorld 上评估。差别是 ACE 修订通用自然语言 playbook，未把返回结构矛盾形式化为字段路径级 schema patch；它是当前 brief 遗漏的关键同任务基线。
4. [Agent Memory Distillation](https://arxiv.org/abs/2608.07169) （[公开代码](https://github.com/taeilkim2465/agentic_memory_distillation)）— 在 AppWorld 等 benchmark 上构建 per-function 调用约定与常见陷阱的 Function Memory，并在 tool-calling error 后反应式检索。差别是它从大教师的成功轨迹离线蒸馏给小学生，而非从当前 agent 的实际返回自我修正 schema。
5. [AppWorld](https://aclanthology.org/2024.acl-long.850.pdf) （[官方仓库](https://github.com/StonyBrookNLP/appworld)）— 直接提出去掉 response schema 后让 agent 通过环境返回识别结构的未来设置，并提供 `simplified_react_code_agent`/`simplified_full_code_agent` 及 `appworld run auto` 入口。差别是其当前文档可靠且返回遵循 schema，论文没有提供从反例维护最小 schema 修订的机制。

```json
{"score":6.9,"verdict":"promising_needs_revision","fatal_blockers":["同一 AppWorld 任务上已有公开实现和明确复现路线的 ACE，其同样利用执行反馈做局部增量上下文更新，但当前最小实验未将其纳入或证明预算不可比。","诊断版的缺字段/类型扰动尚未冻结到具体 endpoint、字段、扰动映射和可运行入口，因而当前无法核验重复访问错误与 TGC 的同预算因果比较。"],"novelty_conclusion":"反馈驱动的工具文档/上下文修订已被 DRAFT、DocsChisel 和 ACE 覆盖；真实返回与访问表达式的 CPU 结构对照、反例限定的单字段路径修订及例外记录尚有较窄新意，值得继续但未达 experiment-ready。","closest_neighbors":["DocsChisel (arXiv:2608.10037)","DRAFT (arXiv:2410.08197)","Agentic Context Engineering (arXiv:2510.04618)","Agent Memory Distillation (arXiv:2608.07169)","AppWorld (ACL 2024)"]}
```
