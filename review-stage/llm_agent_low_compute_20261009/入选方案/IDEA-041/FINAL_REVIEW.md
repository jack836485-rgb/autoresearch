## 结论

**日期：** 2026-10-09  
**score：** 7.8/10  
**verdict：** `experiment_ready`  
**新意判断：** 核心原理不是全新：Temporal 式 durable execution 已会在 replay 时用历史结果替代已完成 Activity，Kishu 已会按变量依赖选择加载或重算，DART/AgentRewind 已处理 agent 的恢复边界与前缀保留。但未检索到同时处理 **LLM 重写的 AppWorld 单个代码块、调用实例级已提交外部效果、公开返回值恢复和纯数据依赖残余化** 的同构方法。这个 statement-level repair boundary 超过单纯重复写去重和普通程序切片，也比预先结构化的持久 workflow 更窄且更动态，构成可独立验证的新意。  
**是否值得继续：** 值得进入实验计划。AppWorld 源码与官方 FullCode 实现支持失效入口，同任务官方 baseline 有公开实现和具体命令，配对恢复与机制消融能在同总预算下否证残余求值的必要性。“丢失返回 ID/被覆盖局部值”尚未被观察，但 brief 已明确把它作为首先诊断、可能被数据否定的假设，因而不构成 claim blocker。本轮无 fatal blocker。

## Claim 判断

| Claim | 判定 | 关键依据 |
|---|---|---|
| AppWorld 中存在“代码块部分写入后报错，下一轮重生整段代码”的入口 | **已被覆盖（环境事实）** | [AppWorld](https://arxiv.org/abs/2407.18901) 明确给出 IPython stateful execution 和 stack trace；官方 [FullCode 实现](https://github.com/StonyBrookNLP/appworld/blob/main/experiments/code/simplified/full_code_agent.py) 把 stack trace 与 retrial prompt 送回模型并再生整段 code，prompt 也明示数据库写会持久。 |
| FullCode 修复避开重复写时，会因返回 ID 或循环内被覆盖局部值丢失而无法继续 | **新颖的具体失效假设，尚未证实** | 持久 `user_ns` 使普通顶层赋值未必丢失，但未完成赋值表达式和循环覆盖值仍使该路径可达。未检索到 AppWorld/FullCode 已报告该失效的比例，因此只能作待诊断假设。 |
| 用已成功调用的公开返回值替代原调用，再重算纯依赖闭包以得到可执行后缀 | **部分重合** | Temporal 已实现“已执行 Activity 从历史返回结果而不重做 I/O”；Kishu 已实现依赖感知的变量加载/单元重算。差别是本 Claim 针对模型修改后的非预编排 Python，以源码位置、循环实例和实参对齐已提交调用，而不是固定 Activity 或整个 notebook cell。 |
| 以实例级效果边界阻止静默重做，同位置不同参数仍视为新写 | **部分重合** | [DART](https://arxiv.org/abs/2605.23311) 已用依赖/效果约束判断可恢复边界；[Verified Tool Calls](https://arxiv.org/abs/2608.02645) 已处理重试前验证和去重。本方法的差别是不读隐藏状态、不依赖幂等键，并将已知成功回执及其返回值绑定到生成代码的动态执行实例。 |
| AppWorld 上的同预算配对恢复和机制消融可判断返回值/依赖恢复是否必要 | **新颖且可验证** | 官方 FullCode 是同任务、已打开实现且有 `appworld run auto` 复现路径的直接 baseline；强 prompt、回执去重和去除依赖保留均在共享观测表上比较，能分离残余求值的独立作用。[Sentry](https://arxiv.org/abs/2610.02994) 虽已在 AppWorld 评测中途失败恢复，但其当前 [GitHub](https://github.com/nuglifeleoji/Sentry) 明示完整代码尚未发布，且机制是失败检测/建议检索，不是语句级残余执行；当前不构成缺失可复现同构 baseline 的 fatal blocker。 |

## 最高近邻

- [Temporal Event History / Tasks](https://docs.temporal.io/tasks) · [开源实现](https://github.com/temporalio/temporal)：最高机制近邻；replay 从头重建状态，已完成 Activity 直接返回历史结果而不重做副作用。差别是 Activity 边界预编排且 workflow 必须确定；本案要对齐 LLM 修改后的调用实例并生成 statement-level 残余程序。
- [DART: Semantic Recoverability for Structured Tool Agents](https://arxiv.org/abs/2605.23311) · [仓库](https://github.com/KeoYang/DART)：最高 agent-recovery 近邻；根据实例、依赖和效果约束选择可接受 rollback。差别是它依赖审核过的 FSM 边界与 checkpoint，不恢复单个 Python 代码块内的返回值数据流；且公开 `runtime/recovery.py` 目前只显示通用 retry/rollback，与论文语义门控的完整复现对齐存疑。
- [AgentRewind: Recoverable Execution for Long-Horizon LLM Agents](https://arxiv.org/abs/2608.14380) · [开源 recorder](https://github.com/Futuresis/replay-agent-recorder)：保存 agent context/受控环境 checkpoint，前缀 LLM 与 tool result 由日志恢复且不重执行。差别是恢复粒度为 agent/tool 决策边界，不处理 AppWorld 单个 cell 内的 AST 数据依赖和修复后调用实例匹配。
- [Kishu: Time-Traveling for Computational Notebooks](https://arxiv.org/abs/2406.13856) · [开源实现](https://github.com/illinoisdata/kishu)：跟踪 IPython 变量及单元依赖，通过增量 checkpoint 和必要单元重算恢复 session。差别是它的目标是 notebook 时间旅行/状态恢复，不建模不可回滚的外部 API 效果，也不用已成功调用返回值编译修复后残余程序。
- [Sentry: Learning to Recover from LLM Agent Failures at Test Time](https://arxiv.org/abs/2610.02994) · [当前仓库](https://github.com/nuglifeleoji/Sentry)：是最接近的 AppWorld 同任务恢复工作，以失败检测、条件检索的恢复经验和恢复验证提高成功率。差别是它不做 effect-return residualization，且截至当前仓库明示完整代码仍待发布，尚无可直接打开的完整复现路径。

```json
{"score":7.8,"verdict":"experiment_ready","fatal_blockers":[],"novelty_conclusion":"核心原理与 durable execution、notebook 依赖恢复和 agent rollback 分别重合，但在 AppWorld 生成代码的单次失败执行内，以调用实例级公开回执保留不可回滚效果并残余化纯数据依赖，尚未发现同构公开工作；该独立新意足以进入实验计划，但实用价值依赖首先诊断出非零的真实失效频率。","closest_neighbors":["Temporal durable execution","DART: Semantic Recoverability for Structured Tool Agents","AgentRewind: Recoverable Execution for Long-Horizon LLM Agents","Kishu: Time-Traveling for Computational Notebooks","Sentry: Learning to Recover from LLM Agent Failures at Test Time"]}
```


主执行器保留的实际风险：

自然失败规模可能很小，因为IPython已有持久变量。模型修改代码后的调用对齐是主要实现风险；未确认映射不能跳过效果。成功回执不证明该写任务正确，不确定timeout也不能纳入已提交保证。最终方案不能扩大成任意Python持久工作流恢复。
