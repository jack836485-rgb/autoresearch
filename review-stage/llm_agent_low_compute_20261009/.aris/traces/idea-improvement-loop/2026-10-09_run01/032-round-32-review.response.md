## 结论

**日期：** 2026-10-09  
**Score：** 7.4/10  
**Verdict：** `promising_needs_revision`

新意判断：**窄机制具有独立性，但当前 Claim 还不能进入实验规划。** 检索到的工作已经分别覆盖了 AppWorld 中的输出 schema 误解、基于执行反馈积累 API schema 经验、轨迹级根因定位，以及“失败位置 + 观察值 + 期望值”的结构化修复反馈；但没有一项把 actor 实际执行的 JSON 访问表达式转成局部 container/key/length/value-type 需求，再只对同次公开返回给出首个矛盾并保留其他成功路径。因此，“访问需求驱动的局部结构契约”比一般 schema 摘要、轨迹反思或全局 schema 推断更窄，也有可检验的新意。

值得继续查证，但有两个 fatal claim blockers。第一，[AppWorld Appendix A](https://arxiv.org/html/2407.18901v1#A1)只说明代理在并非完美了解 API 时会通过增量探索和试错交互，没有提出“删除 response schema”的正式困难设置；官方代码确实支持 `show_api_response_schemas=False`，所以实验可运行，但不能把该协议归因给原论文。第二，AppWorld 的人工错误分析只确认代理会臆造输出字段、误用 API，并未证明在 schema-blind 条件下，单次 `KeyError`/`TypeError` 或 empty/`None` 经常诱发全局 schema 误泛化。后者目前只能是待诊断假设，不能写成已建立的失败事实。公开实现路线本身可行：AppWorld 测试覆盖静态与动态文档同时隐藏 schema，官方 ReAct/FullCode CLI 存在；ACE 仓库也公开了 no-GT 的 offline/online 命令。阻碍来自 Claim 证据，而非工程可运行性。

## Claim 判断

| Claim | 判断 | 关键依据 |
|---|---|---|
| AppWorld 的 response schema 由 FastAPI/代码自动生成且被作者视为可靠 | 已被覆盖，事实成立 | [AppWorld](https://arxiv.org/abs/2407.18901)明确写明 response schema、参数约束、URL 和 HTTP method 由 FastAPI 从代码生成，并以 1,780 个单元测试和 98% 覆盖率支撑环境可靠性。 |
| Appendix A 明确提出删除 response schema 后让代理交互理解返回 | 不成立 | [Appendix A](https://arxiv.org/html/2407.18901v1#A1)只对比“完美知道输入/输出 schema”与现实中的增量探索；没有定义删 schema 的 benchmark 协议。仓库的隐藏开关只能证明该消融可构造，不能反向证明论文提出过它。 |
| schema-blind AppWorld 中，单个 KeyError/TypeError 或 empty/None 常导致整体接口重猜和全局类型误泛化 | 未被证实，Claim blocker | 原论文只报告输出字段臆造、API 理解/使用错误与错误后适应困难；未报告此特定因果链或发生率。brief 的先诊断、失败即停止使它可证伪，但“常被”仍把假设写成了事实。 |
| 从实际访问表达式生成局部结构需求，在当前返回上定位首个矛盾并保留成功路径 | 新颖（窄范围） | AgentDebug 定位轨迹级最早根因，VeriHarness 返回失败位置/观察/期望，ACE 从执行反馈整理 schema 经验；检索未见它们对 actor 的 dict/list/转换表达式做确定性、需求驱动的局部 JSON 契约检查。 |
| empty list 只否定当前索引可达、None 只否定无 guard 转换，不据此推断全局 schema | 新颖的证据边界，机制上成立 | 这是对单次观测可支持结论范围的明确限制，区别于从样本归纳完整 schema；但其对任务成功和反例误泛化的实际收益尚无结果。 |
| 同信息和总预算下，以 ReAct/FullCode、局部 error、全量 shape、ACE no-GT 对照可检验机制 | 基本成立 | [AppWorld 官方仓库](https://github.com/StonyBrookNLP/appworld)公开 `simplified_react_code_agent`、`simplified_full_code_agent` 与 schema 隐藏测试；[ACE AppWorld 仓库](https://github.com/ace-agent/ace-appworld)公开 `ACE_offline_no_GT_adaptation`、`ACE_offline_no_GT_evaluation`、`ACE_online_no_GT`。这些是同任务可运行路线，且预算规则把 reflector/检查成本计入。 |

## 最高近邻

1. [Structured Feedback Improves Repair in an LLM Agent Loop / VeriHarness](https://arxiv.org/abs/2607.14167)。同样在固定调用预算下由代码控制 validator，返回失败位置、观察值和期望信息；差别是其 TextWorld validator 枚举可接受动作，未从 coding agent 的 JSON 访问表达式生成局部结构需求，也未处理证据保留。

2. [Where LLM Agents Fail and How They Can Learn From Failures / AgentDebug](https://arxiv.org/abs/2509.25370)；[公开实现](https://github.com/ulab-uiuc/AgentDebug)。同样隔离最早/关键根因并把定向反馈送回 agent；差别是它用 LLM 分析完整轨迹并依赖任务 Eval/重 rollout，候选只检查当前公开返回上的确定性结构矛盾。

3. [Agentic Context Engineering (ACE)](https://arxiv.org/abs/2510.04618)；[AppWorld 实现](https://github.com/ace-agent/ace-appworld)。这是同 AppWorld、no-GT、自然执行反馈的强近邻，其 reflector 还明确整理输出格式/schema 误解；差别是 ACE 生成并积累自然语言 playbook，候选不跨任务归纳完整 schema，只报告当前访问需求的局部矛盾。

4. [ACON: Optimizing Context Compression for Long-horizon LLM Agents](https://arxiv.org/abs/2510.00615)；[公开实现](https://github.com/microsoft/acon)。同在 AppWorld 中保留后续会引用的 response-schema 字段、原始数据和关键变量，以免压缩丢失结构信息；差别是 ACON 优化 observation/history 压缩，未定位访问表达式与当前返回之间的最小矛盾。

5. [AppWorld](https://arxiv.org/abs/2407.18901)；[公开实现](https://github.com/StonyBrookNLP/appworld)。它已报告输出 schema 字段臆造和基于错误消息适应的困难，并提供 `show_api_response_schemas=False` 的可运行代码路径；差别是论文没有提出局部契约检查，也没有把删 schema 定义为其正式评测设置。

```json
{"score":7.4,"verdict":"promising_needs_revision","fatal_blockers":["AppWorld Appendix A 未提出删除 response schema 的正式困难设置；该协议虽可由官方代码构造，但当前归因不成立","没有一级证据证明 schema-blind AppWorld 中单次 KeyError/TypeError 或 empty/None 经常导致整体接口重猜或全局 schema 误泛化；该失败只能作为待诊断假设"],"novelty_conclusion":"访问需求驱动的局部 JSON 结构契约、首个矛盾定位与成功路径证据保留这一完整机制未被检索到的单篇工作覆盖；但结构化修复反馈、轨迹根因定位、AppWorld schema 经验积累和结构信息保留已有强近邻，且当前对 benchmark 设置与失败发生率的两项事实性 Claim 不成立或未证实。","closest_neighbors":["Structured Feedback Improves Repair in an LLM Agent Loop / VeriHarness (arXiv:2607.14167)","Where LLM Agents Fail and How They Can Learn From Failures / AgentDebug (arXiv:2509.25370)","Agentic Context Engineering (arXiv:2510.04618)","ACON: Optimizing Context Compression for Long-horizon LLM Agents (arXiv:2510.00615)","AppWorld (arXiv:2407.18901)"]}
```
