# 输入问题卡

## 来源

- 地图：`path-stage/LLM热门方向_算力适配_20261028/`（`研究问题.json` 中 `A-Q001`）；卡片继承自 `path-stage/AgenticRL研究地图_20261021/` 的 Q001，正文展开见该图 §3 Q001
- 问题 ID：A-Q001
- 地图检索日期：2026-10-29；近期窗口：2026-04-28 至 2026-10-28（arXiv v1 日期）
- 机构口径：ai-frontier-search 白名单加 QS 2027 前 50；2604.14877 为窗口外背景

## 具体问题

在多轮工具使用 agent 上，RL 什么时候扩大可解任务集合、什么时候只是锐化已有行为？发布模型观察到的大 k 覆盖损失，与受控工具 RL 观察到的能力扩展，差别来自哪些条件？

## 关键证据

| 作品 | 原文链接 | 具体观察 | 证据边界 |
|---|---|---|---|
| A Learning-Rate-Gated Failure of GRPO in a Small Language and Vision-Language Model Web Agent（Monash） | https://arxiv.org/abs/2607.12640 | 已掌握任务上没有配置可信地超过 SFT，中高学习率在文本轨道上更差；采样可达任务上同一配方成功率提升最多 22 个百分点 | 单一基准、小模型；Set-of-Marks 轨道上的伤害只是名义上的 |
| Sharpening Tax in Post-Training（Meta Superintelligence Labs、Stanford） | https://arxiv.org/abs/2610.01509 | k=128 时 36/42 组的锐化税 >0；后训练把任务推向总是解出或从不解出两端 | 作者说明后训练配方未公开，'RL 后训练'是宽泛用法，SFT／DPO 也会锐化；不能单独归因于 RL |
| Does RL Expand the Capability Boundary of LLM Agents? A Pass@(k,T) Analysis（CUHK、Fudan） | https://arxiv.org/abs/2604.14877 | 工具使用 RL 的 pass 曲线在大 k 时高于基座且差距扩大；扩展只在需要组合策略的任务上出现 | 窗口外背景（2026-04-16）；只读了摘要 |
| Reach or Solve? Attributing Agentic RL Gains with Checkpoint Handoffs（SJTU） | https://arxiv.org/abs/2609.19636 | 5 个条件中到达×完成交互均为正；预测交互 20.7 个百分点，观测 24.2；只在共同到达状态上比较会使效应翻号（摘要） | 第二个基准的名称未在所取片段中确认 |
| A Pinch of SFT, A Dash of RL（Amazon Advertising） | https://arxiv.org/abs/2609.22194 | 教师最弱的技能（59.19，其次最低 84.53）经 RL 退化 2.05 分；前瞻诊断预测对 15/18（83.3%） | 前瞻部分控制较弱，作者称其支持操作有用性而非普遍规律 |
| Learning Generalizable Behaviors for Terminal Agents（Salesforce） | https://arxiv.org/abs/2608.22631 | 行为特征预测任务成功 AUC 0.74；单项技能是否出现约 0.55 | 相关性，作者称其与假设'一致' |

## 已有解决方法与剩余边界

- 已有解决方法：
  - 按初始采样可达性筛选 RL 任务 [2607.12640]
  - 按教师支持度与奖励可观察余量，把技能分派到只 SFT、SFT→RL 或补环境 [2609.22194]
  - 用 Reach/Solve 检查点交接做归因 [2609.19636]
  - 用 Sharpening Tax 作诊断指标 [2610.01509]
- 已支持的解释：存在采样可达余量时 GRPO 才有增益（含阳性对照）[2607.12640]
- 尚未解决：本轮范围内未检出在同一 SFT 起点上只隔离 RL 阶段、并按初始采样成功率分层测 pass@(k,T) 的研究；也没有把覆盖变化拆成 Reach 与 Solve 的工作。锐化税论文中未检出对 Pass@(k,T) 工作的讨论（关键词级）。

## 待验证解释与分歧

- 待验证解释：
  - RL 主要塑造组合与调度已有技能的行为（作者假设，相关性证据）[2608.22631]
  - 覆盖损失来自 RL 本身（未分离，作者未主张）[2610.01509]
- 地图正文中的分歧：Sharpening Tax 用发布的“基座 vs 后训练”检查点观察到大 k 覆盖损失；Pass@(k,T) 分析在受控工具 RL 上观察到大 k 扩展。两者差在三处：完整的未公开后训练 vs 只有 RL 阶段；通用 agentic 基准 vs 组合式工具任务；轻量 harness 的基座 vs 原生 agent 格式。现有证据无法判断覆盖损失来自 SFT、偏好优化还是 RL。
- 相关卡：A-Q002（终端状态验证器的多轮 agent RL 中，轮次级信用方法的增益来自定位关键轮次还是信号覆盖面变大）

## 可检验切口与查新状态

- 可检验切口：同一 SFT 检查点只做 RL；按初始采样成功率分层（0、低、高）；观察 pass@(k,T) 与 Reach/Solve；控制 harness、环境、SFT 数据和训练预算
- 查新状态：针对 Pass@(k,T) 做了一次反证核对；未做窗口外全面查新；2026-10-29 补充：在 81 个主题、8534 篇候选内做了标题与摘要层检索，未做针对性查新

## Problem Anchor（冻结）

- **根本问题**：多轮工具使用 agent 的 RL 什么时候扩大可解任务集合、什么时候只锐化已有行为；发布模型的大 k 覆盖损失与受控工具 RL 的能力扩展为何相反。
- **目标领域与设置**：LLM agent 的 agentic RL（GRPO 类，可验证奖励）；多轮工具使用或 web / 终端类可程序评分基准；pass@k 与 pass@(k,T) 覆盖评测；开源 ≤9B 模型为主。
- **必须解决的瓶颈**：覆盖损失与扩展的来源未分离（SFT、偏好优化还是 RL；任务结构；harness 格式），没有在同一起点上只隔离 RL 阶段、按初始可达性分层的证据，也没有能利用这一判断的方法。
- **约束**：
  - 算力：预研 2×A100 80G / 4×L40 48G / 8×4090 24G；正式实验 8×A100 80G。
  - API：1000 元以内可自主决定；token 资源稀缺。
  - 时间与目标：半年内（自 2026-10 起）投一篇主会。
  - 实验代码与数据集在服务器上通过 ssh 开发，不存本地。
  - 非目标：从头预训练；依赖大规模异步 RL 基础设施的方案。
- **成功条件**：得到一个在 ≤9B、8×A100 上可完成最小实验、baseline 可复现、Claim 可被实验推翻且通过两轮独立 reviewer 门槛的 idea。
