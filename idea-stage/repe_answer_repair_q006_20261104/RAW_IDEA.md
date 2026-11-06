# 输入问题卡

## 来源

- 地图：`path-stage/表示工程研究地图_20261104/`（`研究问题.json` Q006 全部字段与 `研究地图.md` 的 `### Q006` 节）
- 问题 ID：Q006（细化自 Q001）
- 地图检索日期：2026-11-04；近期窗口：2026-05-04 至 2026-11-04
- 机构口径：ai-frontier-search 白名单 + QS 前 50；白名单外与窗口外证据在证据角色中单独标注
- 本轮读取：Q006 全部字段、地图 Q006 正文、Q001 与 Q005 的具体问题行；证据论文全文已在 `资料/细化正文/`。该目录无 `文献笔记/反证检索.txt`。
- 用户约束：Q006 审查预算沿用 Q005 剩余的 13 次（用户可改）。

## 具体问题

答案级 steering 在“信息来源选择”类失败（受线索诱导的偏差、上下文与参数知识冲突）上能恢复正确答案，但在“推理过程”类失败（矛盾盲视、过度思考、工具调用决策）上只注入全局标签偏置，纠正错误的同时破坏原本正确的决定；这条分界由什么决定？

## 关键证据

| 作品 | 原文链接 | 具体观察 | 证据边界 |
|---|---|---|---|
| How Does Alignment Tuning Shape Representations of Sycophancy and Related Cue-Induced Biases in LLMs?（2607.18114，Toronto） | https://arxiv.org/abs/2607.18114 | 每种偏差都有可解码、可 steer 的线性方向，steering 在所有家族上恢复无偏答案，并保留大多数原本正确的答案 | 仅摘要 |
| Which Knowledge Should LLMs Trust? Uncovering a Generalizable Steering Direction Across Knowledge Conflicts（2610.20067，PKU） | https://arxiv.org/abs/2610.20067 | 单一方向可在上下文与参数答案之间切换，并迁移到 RAG、记忆与规则遵循 | 仅摘要 |
| Evaluating the Semantic Specificity of Representation Steering in Language Models（2608.29431，Cambridge，§5.1–5.3） | https://arxiv.org/abs/2608.29431 | oracle 门控下 100% 恢复；无门控时原本答对的规则准确率随 α 单调下降，错误集中在目标标签 | 具体数值未取到 |
| Decodable but Not Corrected by Fixed Residual-Stream Linear Steering（2605.05715，Amazon，贡献节、§4.1） | https://arxiv.org/abs/2605.05715 | 可解码 71.6%，steering Δ≈0 | 失败模式标签由判分器标注 |
| When Does Correction Become Repair? Mechanistic Auditing of Internal Interventions in Tool-Using LLMs（2609.36138，白名单外，仅摘要） | https://arxiv.org/abs/2609.36138 | 5 个模型有方向特异的净增益；但净增益 +55 的干预破坏了它触及的基线正确决策中的一半以上 | 仅摘要；代码已公开 |

## 已有解决方法与剩余边界

- 已有解决方法：oracle／条件门控（2608.29431 的 oracle 门控；CAST 类条件 steering）只在已知目标子集时有效。
- 已支持的解释：推理类失败上的 steering 表现为全局标签偏置（2608.29431）；行为移动不等于修复（2609.36138）。
- 尚未解决：成功与失败案例来自不同任务、模型和指标，没有在同一模型上同时测纠正率与破坏率；“正确行为是否实例一致”能否预测修复比例未检验。

## 待验证解释与分歧

- steering 只提供全局先验偏移：正确行为在实例间一致时（总是忽略线索、总是信上下文）它就是修复；正确行为依实例而定时，它只能在纠错与破坏之间交换（本地图推测）。
- 地图正文分歧：信息来源选择类（2607.18114、2610.20067）能修好 vs 推理过程类（2608.29431、2605.05715、2609.36138）修不好。

## 可检验切口与查新状态

- 可检验切口：在同一模型上构造成对任务：同一能力的“实例一致”版本（如总是该忽略的线索）与“实例相关”版本（如部分样本该信线索），分别测纠正率与对原本正确样本的破坏率；对照全局 steering、条件门控、逐样本检索目标（2611.04757）。
- 查新状态：做了定向网页检索（steering 只做全局偏移、不能修复推理错误），未检出直接研究；2611.04757（逐样本 steering 何时需要）与之相邻。
- 已知边界：成功证据多为摘要级；推理类失败的数值部分未取到。

## 问题锚点（Problem Anchor）

- **起点问题：** 同一类“答案级 steering”为何在信息来源选择类失败上是修复（纠正错误且保留正确），在推理过程类失败上只是全局标签偏移（纠正与破坏交换）；决定这条分界的变量是什么。
- **对象与条件：** 4–9B 开源指令/推理模型（证据中 Llama-3.1-8B、Qwen2.5-7B、Gemma、OLMo、Qwen3 等）；残差流线性 steering（diff-in-means、探针方向、门控变体）；信息来源类任务（BCT 线索偏差、知识冲突）与推理过程类任务（矛盾盲视、MedQA 过度思考、When2Call/MetaTool 工具决策）。
- **初始任务/评测：** 纠正率（基线错→steer 后对）与破坏率（基线对→steer 后错），以及在模型本就胜任的规则上的跨规则迁移（2608.29431 的 CRT）。
- **瓶颈与证据边界：** 成功与失败证据来自不同模型、任务与指标；两篇成功证据只读到摘要级；未在同一模型上同时测纠正与破坏。
- **用户资源约束：** 预研 2×A100 80G / 4×L40 48G / 8×4090 24G；正式实验可用 8×A100 80G、最好不超过 5 天；付费 API 1000 元内可自主决定；token 资源较稀缺。
- **时间与目标：** 自 2026-10 起半年内投出一篇主会论文。
- **非目标：** 不做世界模型、视频生成、机器人方向。
- **进入实验规划的成功条件：** 独立 reviewer 两次（常规 + 复核）对同一 brief 判定三项贡献都 ≥6 且至少两项 ≥8、可行性 pass、experiment_ready、无 fatal blocker；产出 `EXPERIMENT_HANDOFF.md`。
