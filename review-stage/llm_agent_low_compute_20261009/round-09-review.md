## 结论

**日期：** 2026-10-09  
**Score：** 7.4/10  
**Verdict：** `promising_needs_revision`  
**新意判断：** 部分重合但保有明确窄新意。现有工作已经覆盖“按请求所需证据决定继续调用或停止”的大框架；当前方案较清楚的增量是把分页查询的存在、否定存在、全称与精确计数映射为不对称的完成证据，并用同预算下相反的调用收益交互验证机制。  
**是否值得继续：** 值得，但当前尚未达到 `experiment_ready`。唯一 fatal blocker 是核心 CPU 门在官方 AppWorld ReAct 执行路径中的观测与拦截入口尚未被公开实现或具体复现路线证实：官方 runner 将一个完整 Python 代码块交给 `world.batch_execute`，外围只收到整块输出；公开 `RequestTracker` 记录方法、URL 和参数，不记录每次 API 返回。因而方案所需的逐页返回、见证和结束信号目前不能由已核验入口取得。

## Claim 判断

| Claim | 判断 | 关键依据 |
|---|---|---|
| Agent 很少请求第二个分页 chunk | 部分重合 | *Agents Don’t Paginate* 在公开 MCP 中间件日志上报告第二 chunk 请求率为零，但它不研究 AppWorld；方案已正确把 AppWorld 中的具体因果失败表述为待诊断，而非既成事实。 |
| 存在见证可提前停止，否定存在、全称正结论和精确计数要求枚举完备 | 新颖（窄域） | 逻辑原则本身是数据库查询常识；未检索到把该量词不对称具体落到 AppWorld 分页 API、同一 actor 和同预算停止门的既有方法。 |
| 显式运行时状态依据证据充分性控制继续、综合或停止 | 部分重合 | *AgentLoop* 已提出请求槽、工具证据、缺口归因和运行时停止控制；*Don’t Stop Early* 也使用证据充分性终止。差别是本方案以分页覆盖及量词语义给出确定性完成条件，而不是通用槽闭合或模型辅助充分性判断。 |
| 计数/否定减少过早停止，存在查询相对全枚举减少调用，且两者形成反向交互 | 新颖 | 这是可证伪的机制性实验主张；现有近邻分别研究分页遗漏或通用过搜/证据终止，未报告 AppWorld 上这一量词分组交互。 |
| AppWorld 上的最小实验可按所述 runner 直接复现 | 未成立 | 官方 ReAct、数据集入口和运行命令均公开；但当前公开代码证据只证明整段代码执行与请求参数日志，未证明 CPU 门能够观察每次分页返回并在 actor 完成前施加所述语义门。 |

## 最高近邻

1. [AgentLoop: Runtime Control of Slot-closed Execution Loops for Tool-augmented LLM Agents](https://arxiv.org/abs/2609.33315)（2026）。重叠最大：显式运行时状态、证据验证、缺口归因及继续/综合/停止控制；差别是其槽闭合由辅助模型验证，未涉及分页、存在/否定/计数量词或 AppWorld。
2. [Don’t Stop Early: Scalable Enterprise Deep Research with Controlled Information Flow and Evidence-Aware Termination](https://aclanthology.org/2026.acl-industry.116/)（ACL 2026）。重叠在用证据充分性标准抑制过早停止；差别是深度研究覆盖目标，不是 API 分页的确定性枚举证据，也没有量词相反收益检验。
3. [Agents Don’t Paginate: First-Chunk Selection for LLM Tool Responses](https://arxiv.org/abs/2608.26130)（2026）。直接支持“agent 不翻第二 chunk”的外部经验事实；差别是方法优化首 chunk 选择，并明确不是端到端 agent 完成率实验，不研究查询语义停止或 AppWorld。
4. [PECAN: LLM-Guided Dynamic Progress Control with Attention-Guided Hierarchical Weighted Graph for Long-Document QA](https://aclanthology.org/2025.findings-acl.689/)（ACL Findings 2025）。重叠在按查询动态判断当前证据是否足够并停止检索；差别是长文档图检索和 LLM 充分性判断，不追踪分页 API 的枚举完备性。
5. [AppWorld: A Controllable World of Apps and People for Benchmarking Interactive Coding Agents](https://arxiv.org/abs/2407.18901)（ACL 2024）。同一 benchmark 与公开 ReAct 基线，论文和提示示例明确包含 `page_index`/`page_limit` 及遍历全部页面；它没有提出量词感知停止门，也未给出该失败的分组因果诊断。

```json
{"score":7.4,"verdict":"promising_needs_revision","fatal_blockers":["核心 CPU 门在官方 AppWorld ReAct 路径中观察逐页 API 返回、见证与公开结束信号的插入点和复现路线尚未由公开实现证实；现有 runner 外围只得到整段代码输出，公开 RequestTracker 只记录请求参数而不记录响应。"],"novelty_conclusion":"通用的证据感知运行时停止已被 AgentLoop 和 evidence-aware termination 工作部分覆盖，但将存在、否定存在、全称和精确计数的证明义务用于 AppWorld 分页停止，并以同预算反向收益交互验证机制，仍具有明确的窄域新意。","closest_neighbors":["AgentLoop: Runtime Control of Slot-closed Execution Loops for Tool-augmented LLM Agents","Don’t Stop Early: Scalable Enterprise Deep Research with Controlled Information Flow and Evidence-Aware Termination","Agents Don’t Paginate: First-Chunk Selection for LLM Tool Responses","PECAN: LLM-Guided Dynamic Progress Control with Attention-Guided Hierarchical Weighted Graph for Long-Document QA","AppWorld: A Controllable World of Apps and People for Benchmarking Interactive Coding Agents"]}
```
