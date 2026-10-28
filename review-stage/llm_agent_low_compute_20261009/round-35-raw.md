## 结论

**日期：** 2026-10-09  
**Score：** 8.0/10  
**Verdict：** `experiment_ready`

新意成立在一个窄而独立、可证伪的机制组合上：在 AppWorld 交互式代码 agent 的单次 JSON 提取失败中，不增加 API 调用或外部 rollout，用当前失败样本检查可执行性，并用同一提取器此前真实成功执行的适用 JSON 约束候选保持原观测输出，再由原 actor 作最终语义选择。程序修复已有“修复失败测试且不破坏旧通过测试”的骨架，agent 工具生成也已有执行 trace、schema/value 与候选验证；但本轮检索未发现工作同时覆盖历史 agent 可见 JSON、纯提取器搜索空间、no-GT 有限观测保持和同预算 AppWorld 恢复。

值得继续。AppWorld 原文直接支持输入/输出字段臆造与 API 误用；“修当前 empty/None/嵌套结构会破坏旧提取行为”仍被诚实标为待诊断假设。有限行为保持只保证指定旧输入上的观测一致，不声称旧输出是语义真值，且实验单报非真值保持、vacuous 修补与真实任务后果，因此没有 Claim blocker。官方 ReAct/FullCode 的 `appworld run auto` 入口和 ACE no-GT 的公开配置、运行命令均已核验；全部构建、反思与查询计入统一预算后，没有 fatal feasibility blocker。

## Claim 判断

| Claim | 判断 | 关键依据 |
|---|---|---|
| AppWorld 中存在字段臆造、返回 schema 误用和错误 API | **已被覆盖（问题依据成立）** | [AppWorld](https://arxiv.org/abs/2407.18901) 的人工错误分析明确记录 input/output schema 字段臆造（如访问不存在的 `song_id`）及错误 API；它没有研究本方案的行为保持修补。 |
| 针对当前 empty/None/嵌套结构的修补会改变同一提取器的既有输出 | **新颖的待诊断假设** | 已检索工作没有给出这一 AppWorld 自然失败的发生率或因果结果；brief 未把它写成既成事实，并以旧输出变化、任务后果和停止条件先行证伪。 |
| 对候选同时检查当前失败结构与适用旧样本的原观测输出，再把通过/反例交回 actor | **部分重合** | [SWE-RL / Agentless Mini](https://arxiv.org/abs/2502.18449) 已用 reproduction tests 与事前筛选的旧 passing tests 执行、重排候选 patch；[Tool-Making](https://arxiv.org/abs/2607.08010) 已从执行 trace、schema/value 生成并测试修复候选工具。差别在于本方案面向在线 tool-agent 的历史 JSON 提取器，以无 gold 的有限观测保持约束局部修补。 |
| 旧观测值保持能证明有限行为不回归，但不能证明语义正确 | **新颖边界，论断成立** | 保留集限定为同一提取器的适用旧样本，需事前声明本来应改变的行为；旧输出不作任务真值，跨接口样本不混入，因而 Claim 没有把有限回放夸大为语义保证。 |
| 同预算 AppWorld 实验与强同任务 baseline 可复现 | **部分重合；可行** | [AppWorld 官方仓库](https://github.com/StonyBrookNLP/appworld) 公开 simplified ReAct/FullCode、配置、日志与 `appworld run auto`；[ACE AppWorld 仓库](https://github.com/ace-agent/ace-appworld) 公开 `ACE_offline_no_GT_adaptation`、`ACE_offline_no_GT_evaluation`、`ACE_online_no_GT`，对应配置设 `use_gt_code: false`。本地强提示、当前样本、多样本结构及观测保持组共享候选数和总预算，可隔离机制。 |

## 最高近邻

1. [SWE-RL: Advancing LLM Reasoning via Reinforcement Learning on Open Software Evolution / Agentless Mini (NeurIPS 2025)](https://arxiv.org/abs/2502.18449)：重叠是候选 patch 同时接受失败复现与经筛选的旧 passing tests，并据执行结果重排；差别是仓库级程序修复与测试套件，不是交互式 tool-agent 的历史 JSON、no-GT 提取器修补。
2. [Tool-Making and Self-Evolving LLM Agents in Low-Latency Systems (2026)](https://arxiv.org/abs/2607.08010)：重叠是采集真实执行 trace、schema/value，生成候选工具并经 test-repair 后部署；差别是离线稳定 SOP 工具并依赖标注 verdict，本方案处理单次失败、无标注有限观测保持且无新环境 rollout。
3. [Structured Feedback Improves Repair in an LLM Agent Loop / VeriHarness (2026)](https://arxiv.org/abs/2607.14167)：重叠是代码控制的 validator 执行、拒绝候选并向同一修复回路返回结构化反例；差别是 TextWorld 中的位置、观察值与可接受替代反馈，没有把历史成功行为保持作为独立变量。

```json
{"score":8.0,"verdict":"experiment_ready","fatal_blockers":[],"novelty_conclusion":"程序修复和工具生成分别覆盖旧通过测试保持、执行 trace 驱动候选验证，但未直接覆盖 AppWorld 单次失败中基于 agent 历史原始 JSON 的纯提取器 no-GT 有限观测保持、无额外 rollout 验证及同一 actor 语义选择这一完整组合；目标回归现象仍是明确可先行证伪的诊断假设。","closest_neighbors":["SWE-RL / Agentless Mini (NeurIPS 2025)","Tool-Making and Self-Evolving LLM Agents in Low-Latency Systems (2026)","Structured Feedback Improves Repair in an LLM Agent Loop / VeriHarness (2026)"]}
```
