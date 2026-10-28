## 结论

日期：2026-10-09。**score：6.7/10；verdict：`promising_needs_revision`。** 当前方案可检验、预算控制较完整，AppWorld 官方 FC 入口和同任务对照也有公开复现路径；但新意边界尚未成立。量词条件本身是基本查询语义，AppWorld 官方材料已经把分页访问区分为 `find_one_from_pages` 与 `find_all_from_pages`，并明确要求分页 API 遍历全部结果；更关键的是，ECT 已公开“类型化任务要求—工具证据账本—完成门—拒绝完成后继续”的近同构机制，Goal-Autopilot 也已把可执行条件门作为终止授权核心。因此当前可辨认的独立部分主要是“在 AppWorld 上比较存在、否定存在和精确计数的调用/错误完成交互”，属于尚未验证的窄实证 Claim，而不是已与最近工作分离的方法 Claim。值得继续核验这个实证问题，但当前形态不足以直接进入以独立方法新意为前提的实验规划。

## Claim 判断

| Claim | 判断 | 关键依据 |
|---|---|---|
| 存在正结论只需见证，否定存在与精确计数需同范围完整枚举 | 部分重合 | 这是标准量词/查询充分性事实；AppWorld 官方任务生成指南已公开 `find_one_from_pages` 与 `find_all_from_pages` 的对应分页语义，官方 FC prompt 也要求处理全部分页结果。 |
| 用逐调用证据账本，在 `complete_task` 边界按范围、覆盖与基数阻止无证据完成 | 已被核心覆盖 | [ECT](https://arxiv.org/abs/2608.23623) 已把 trusted requirements、receipt ledger、scope/cardinality 检查、deterministic verifier 和 `complete/continue` 门作为中心机制，并公开源代码与闭环结果；本方案是其 AppWorld 分页特化且更弱的证据模型。 |
| 阻止完成后以同一 tool-call id 返回局部反馈，让原 actor 继续查询 | 部分重合 | ECT 已验证拒绝完成后的闭环恢复；[Goal-Autopilot](https://arxiv.org/abs/2606.11688) 也以硬完成门和失败后继续/停滞为核心。这里的 FC 消息协议插入点具体，但不是独立机制层新意。 |
| 量词条件门可同时减少否定/计数的过早完成，并比统一全枚举节省存在查询调用 | 新颖但未证实 | 未发现直接在 AppWorld 同任务、同预算下报告这一双向交互的工作；brief 明确承认尚无 AppWorld 分组结果。该项是当前最清楚的独立、可证伪 Claim。 |
| AppWorld 最小实验及对照足以验证因果链 | 部分成立 | 官方 FC 代码确实逐条暴露 `tool_call_id`、函数名与结果，CLI、数据 split 和评测均公开；强语义提示、固定多一页、统一全枚举门是同 actor 同任务控制。但尚无公开任务清单/组规模证明存在、否定和计数三组均有足够样本，且 actor 输出中的语义类型与 predicate 尚未证明能被稳定、无额外信息地解析。 |

## 最高近邻

1. [When May an Agent Stop? Evidence-Carrying Termination for Tool-Using LLMs](https://arxiv.org/abs/2608.23623)（2026）：重叠在证据账本、范围/基数义务、确定性完成门、拒绝后继续与错误完成指标；差别是其任务为六类合成工具任务并要求证书/回放，本方案只做 AppWorld 静态分页并以量词选择较轻的覆盖条件。
2. [Goal-Autopilot: A Verifiable Anti-Fabrication Firewall for Unattended Long-Horizon Agents](https://arxiv.org/abs/2606.11688)（2026）：重叠在“模型提出完成、CPU 可执行 gate 决定能否 DONE”及错误完成/保守继续；差别是其使用目标编译后的 FSM 与每状态 gate，未研究分页量词或存在查询相对全枚举的调用收益。
3. [AppWorld: A Controllable World of Apps and People for Benchmarking Interactive Coding Agents](https://arxiv.org/abs/2407.18901)（2024）及[官方仓库](https://github.com/StonyBrookNLP/appworld)：与目标 benchmark、API/function calling、分页任务、TGC/SGC 和复现入口完全相同；官方指南已提供 `find_one_from_pages`/`find_all_from_pages`，官方 FC prompt 已要求遍历所有分页，差别是没有量词条件化完成门及对应分组实验。
4. [Agents Don't Paginate: First-Chunk Selection for LLM Tool Responses](https://arxiv.org/abs/2608.26130)（2026）：直接报告公开 MCP 日志中 agent 不请求第二块的分页失败现象；差别是研究工具响应截断后的首块选择与 SWE-bench 文件定位，不研究 API 查询量词、完整枚举证明或完成调用拦截。
5. [AgentSpec: Customizable Runtime Enforcement for Safe and Reliable LLM Agents](https://arxiv.org/abs/2503.18666)（2025）：重叠在轻量规则、trigger/predicate 和运行时阻止 agent 动作；差别是目标为跨域安全/合规约束，不处理分页证据充分性、查询量词或 AppWorld 完成正确性。

```json
{"score":6.7,"verdict":"promising_needs_revision","fatal_blockers":["新意边界未成立：ECT 已覆盖证据账本、范围/基数校验、确定性完成门和拒绝后的闭环恢复，AppWorld 官方工具又已覆盖 find-one 与 find-all 的分页语义；当前 brief 尚未证明量词条件化 AppWorld 实证足以构成独立方法 Claim。"],"novelty_conclusion":"可辨认的新意仅是同一 AppWorld 场景下，存在、否定存在与精确计数之间的错误完成—API 调用交互；完成门及分页一/全语义的机制主干已有直接近邻覆盖，因此当前不具备 experiment_ready 所需的独立新意边界。","closest_neighbors":["When May an Agent Stop? Evidence-Carrying Termination for Tool-Using LLMs","Goal-Autopilot: A Verifiable Anti-Fabrication Firewall for Unattended Long-Horizon Agents","AppWorld: A Controllable World of Apps and People for Benchmarking Interactive Coding Agents","Agents Don't Paginate: First-Chunk Selection for LLM Tool Responses","AgentSpec: Customizable Runtime Enforcement for Safe and Reliable LLM Agents"]}
```
