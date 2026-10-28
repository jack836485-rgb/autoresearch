## 结论

**日期：** 2026-10-09  
**Score：** 7.4/10  
**Verdict：** `promising_needs_revision`

该想法仍有狭窄而可检验的新意：现有近邻分别覆盖了运行时局部状态调试、结构化失败反馈、AppWorld 上的诊断式恢复和执行反馈驱动的上下文更新，但本次检索未发现工作把 actor 自己的 JSON 访问表达式确定性地还原为“首个 container/key/length/value-type 矛盾”，并明确限制 empty/None 的证据外推、保留其他已成功访问路径。与此同时，上位因果故事已经拥挤：VeriHarness 已直接研究“失败位置 + 观察值 + 可行动信息”，且其消融显示仅有位置和观察值时接近原始诊断；LDB 也已证明局部运行时状态可用于定位和修复。因此当前贡献更像 AppWorld 上精确限定的反馈接口，而不是新的执行反馈范式。

值得继续，但只值得按 brief 中已冻结的诊断闸门继续；目前尚不能进入 `experiment_ready`。AppWorld 原文支持输出字段臆造、错误 API 使用及根据错误消息调整行为困难，却不支持 empty/None 被全局误泛化或成功路径在恢复中被破坏是已观察到的常见失败。官方 AppWorld ReAct/FullCode 与 ACE no-GT 的公开实现和运行入口均可核验，未发现致命可行性阻塞；未解决的是新意边界与目标自然失败的实际样本量，而非代码入口。

## Claim 判断

| Claim | 判断 | 关键依据 |
|---|---|---|
| AppWorld schema 可靠，agent 会臆造输入/输出字段、误用 API，并难以依据错误消息调整 | **部分重合；证据基本成立** | [AppWorld](https://arxiv.org/html/2407.18901) 说明响应 schema 由 API 代码自动生成，并在人工错误分析中明确记录 output-schema 字段臆造、错误 API；论文也把基于 errors/messages 调整行为列为主要困难。它没有把“错误后整体重猜 schema”单独测量出来。 |
| empty/None 会被误解释为全局 schema 变化，恢复会破坏已成功路径 | **新颖假设；尚未证实** | AppWorld、ACE、DARC 均未给出该具体自然失败的发生率或轨迹证据。brief 明确把它写成待诊断假设而非既成事实，因此当前不是虚假 Claim，但也尚不能支撑效果 Claim。 |
| CPU 从实际返回与访问表达式生成首个局部结构矛盾 | **部分重合** | [VeriHarness](https://arxiv.org/abs/2607.14167) 已把失败位置、观察值和可接受替代项结构化返回；[LDB](https://arxiv.org/abs/2402.16906) 已按基本块采集运行时变量并局部定位错误。差别在于本方法用访问表达式和当前 JSON 做确定性 container/key/length/type 校验，不调用 LLM 判定块语义，也不直接给业务答案。 |
| 局部修复保留已成功路径，不因单次 empty/None 改写全局结构认识 | **部分重合** | LDB 的选择性块级调试和 ACE 的增量更新都主张避免整体重写；但前者面向完整程序语义，后者面向跨任务 playbook。本方法的路径级非外推约束仍是更窄差别，尚无 AppWorld 结果证明它带来收益。 |
| 同预算实验能区分局部矛盾、普通错误提醒、全量 shape 与长期执行反馈 | **可证伪且基本可复现；不是新意本身** | [AppWorld 官方仓库](https://github.com/StonyBrookNLP/appworld) 公开 `simplified_react_code_agent`、`simplified_full_code_agent`、`appworld run auto` 和 `show_api_response_schemas`；[ACE AppWorld 仓库](https://github.com/ace-agent/ace-appworld) 公开 `ACE_offline_no_GT_adaptation`、`ACE_offline_no_GT_evaluation`、`ACE_online_no_GT`。相同 actor、token、调用与步骤上限使主比较可反驳。 |

## 最高近邻

- [Structured Feedback Improves Repair in an LLM Agent Loop / VeriHarness (2026)](https://arxiv.org/abs/2607.14167)：最接近反馈接口 Claim，已比较原始诊断与“位置、观察值、可接受替代项”；差别是 TextWorld 动作验证而非 AppWorld JSON 访问表达式，且其结果对“只给位置与观察值”构成直接负面先验。
- [Debug like a Human: A Large Language Model Debugger via Verifying Runtime Execution Step-by-step / LDB (2024)](https://arxiv.org/abs/2402.16906)：最接近局部运行时证据机制，按基本块追踪中间变量并定位错误；差别是依赖可见测试与 LLM 语义判定，未处理 API 返回路径、empty/None 证据边界或 AppWorld。
- [Diagnosis Before Recovery: Turning Agent Failures into Selective Self-Correction / DARC (2026)](https://arxiv.org/abs/2608.11772)：最接近同任务定位，已在 AppWorld 上用诊断限制恢复干预并组合 Auto-Knowledge、local induction 与 retrieval fallback；差别是任务家族级“程序知识宽度”诊断，而非单次访问表达式的局部结构矛盾，且截至当前检索未见公开代码链接。
- [Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models / ACE (2025/2026)](https://arxiv.org/abs/2510.04618) 与[公开 AppWorld 实现](https://github.com/ace-agent/ace-appworld)：同 AppWorld、同自然执行反馈、无权重更新，并用增量 playbook 避免上下文整体重写；差别是学习可复用程序知识，成本和作用范围远大于一次失败路径的确定性校验。
- [AppWorld: A Controllable World of Apps and People for Benchmarking Interactive Coding Agents (2024)](https://arxiv.org/html/2407.18901) 与[官方仓库](https://github.com/StonyBrookNLP/appworld)：直接支持字段臆造、API 误用、错误栈与可靠 response schema，也把去除 response schema 留作未来方向；差别是它没有提出或实测当前局部矛盾恢复协议。

```json
{"score":7.4,"verdict":"promising_needs_revision","fatal_blockers":[],"novelty_conclusion":"精确到 AppWorld JSON 访问表达式的首个局部结构矛盾仍有狭窄新意，但其上位思想已被 LDB、VeriHarness、DARC 和 ACE 部分覆盖；当前证据尚不能证明目标自然失败具有足够频率，或仅靠局部位置与观察结构能优于等预算错误反馈。","closest_neighbors":["Structured Feedback Improves Repair in an LLM Agent Loop (2026)","Debug like a Human: A Large Language Model Debugger via Verifying Runtime Execution Step-by-step (2024)","Diagnosis Before Recovery: Turning Agent Failures into Selective Self-Correction (2026)","Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models (2025/2026)","AppWorld: A Controllable World of Apps and People for Benchmarking Interactive Coding Agents (2024)"]}
```
