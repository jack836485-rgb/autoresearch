# 输入问题卡

## 来源

- 地图：`path-stage/LLM热门方向_刷新_20261101/研究问题.json` 与 `研究地图.md`，问题 ID **A-Q006**（继承自 `AgenticRL研究地图_20261021` 的 Q006，经 `LLM热门方向_算力适配_20261028`）。
- 刷新图检索日 2026-11-01；继承卡片的近期窗口为 2026-04-28 至 2026-10-28，刷新窗口延至 2026-11-01；机构口径为 ai-frontier-search 白名单加 QS 前 50。
- 本轮读取：A-Q006 卡全部字段；刷新图 `### A-Q006` 段落与推荐顺序第 3 条。卡片 `与其他问题的关系` 为空；地图目录无 `文献笔记/反证检索.txt`。
- 用户约束：本卡审查预算 **15** 次（覆盖 skill 默认的 6 次）。

## 具体问题

异步 agentic RL 流水线缺失 old logits 时，偏差修复与陈旧度校正纠缠，阈值耦合如何导致后期崩溃？声称"无损"的加速系统是否保留了 old logits？

## 关键证据

| 作品 | 原文链接 | 具体观察 | 证据边界 |
|---|---|---|---|
| Missing Old Logits in Asynchronous Agentic RL（2605.12070，北大/清华） | https://arxiv.org/abs/2605.12070 | §4.1、§6.4：异步 RL（延迟更新与部分 rollout），在精确 old logits 条件下改变陈旧度阈值与偏差掩码阈值；宽松阈值前期快，但后期更易崩溃；掩码与 PPO 裁剪通过最终活跃 token 集合耦合 | 具体数值未取（卡片记录） |

## 已有解决方法与剩余边界

- 已有解决方法：快照版本追踪、专用 old-logit 模型、中断部分 rollout 同步等精确获取方式，以及近似校正路线 [2605.12070]。
- 已支持的解释：缺失 old logits 使两类校正语义纠缠 [2605.12070]。
- 尚未解决：本轮未核对其他异步／加速系统论文是否保留 old logits。
- 解决状态：部分解决。

## 待验证解释与分歧

- 卡片 `待验证解释` 为空。
- 刷新图：除本卡证据外未检出直接新作；拥挤度"低"；需要异步 RL 基础设施，算力适配低–中。

## 可检验切口与查新状态

- 可检验切口：对声称无损的异步系统，比较精确 old logits 与近似替代下的后期稳定性，控制陈旧度分布。
- 查新状态：未进行针对性查新；2026-10-29 补充：在 81 个主题、8534 篇候选内做了标题与摘要层检索，未做针对性查新。
- 拥挤度检查（2026-11-01）：低；依据为除 2605.12070 外未检出直接新作。

## 本轮补充核验（主执行器，2026-11-05）

以下由主执行器直接读原文或代码核验，用于生成候选；不传给 reviewer。

1. **2605.12070 v3（2026-09-29）**：分解 $\pi_\theta/\mu_{old}=(\pi_\theta/\pi_{old})(\pi_{old}/\mu_{old})$，其中 $\pi_{old}$ 是训练端在 rollout 版本上的概率（old logits）。异步 + 部分 rollout 时 $\pi_{old}$ 丢失，常用代理（当前训练端、线性/对数线性插值）只是改写单一总比率的有效边界（Proposition 1）。实验：ROLL 框架，Qwen3-4B 与 Qwen3-30B-A3B，τ²-Bench 与 VitaBench，最大版本差 3。Table 2（avg）：4B VitaBench in-store Decoupled PPO 19.83 / Linear_prox 22.37 / PPO-EWMA 25 / Snapshot 28.89；30B-A3B in-store 18.28 / 31.47 / 33.41 / 34.62，delivery 25.88 / 20.74 / 28.49 / 30.74。Table 6：Snapshot 每步额外 95.2 s（4B）/ 178.2 s（30B-A3B），最多驻留 5 个快照共 76.4 GB，两次测量运行均因 Ray actor 不可用终止。结论自述 PPO-EWMA 在高度非平稳陈旧度或极端版本差下可能不可靠。文中给的代码仓库 `millioniron/ROLL` 匿名不可读。
2. **2610.40945（2026-10-29）**：用训练端在采样端权重上的一次前向，把采样 token 误差精确拆成数值偏差 $e_t$ 与策略滞后 $\ell_t$；Qwen3-0.6B/1.7B、Countdown 上，数值偏差在训练中近似常数（FP8 采样约 0.02 nats/token，BF16 低于 $10^{-3}$），且与累计更新 $\Delta$ 无关；滞后一阶为 $\Delta^\top s_t$。DLC 需要训练端在采样端权重上的前向（即 old logits），在其设置中采样端固定于 $\theta_0$ 所以可得；未处理 old logits 缺失。
3. **其他近邻**：A-3PO（2512.06547，对数线性近端策略）；ENTR（2607.22186，用 rollout logprobs 作锚点、按熵归一化信任域，陈旧度到 30 版本，无公开代码）；RDC（2610.21682，MoE 路由漂移过滤）；VCPO（2602.17616）；COPC（2610.09597，优势陈旧）；Predictive Divergence Masks（2607.10848）。均未用"采样端在当前权重上重打分"来恢复 old logits。
4. **框架核验（AReaL，2026-11-05 主分支 `inclusionAI/AReaL`）**：逐 token `versions` 已记录；`use_decoupled_loss` + `prox_logp_method ∈ {recompute, loglinear, metrics}`（recompute 即 Decoupled PPO，loglinear 即 A-3PO）；M2PO 掩码；远程 SGLang/vLLM 引擎已有 `compute_logp` 打分路径（SGLang `return_logprob` + `logprob_start_len` 取 `input_token_logprobs`）；有 score centering（采样端 top-k head）实现；有 `examples/tau2`、`examples/search_agent`、`examples/r3`（Moonlight MoE 路由回放）。verl fully-async 默认用 rollout logprobs 作 old_log_prob，关掉 bypass 后近似 AReaL Decoupled PPO；文档未提供采样端用新权重重打分。

## 问题锚点（Problem Anchor）

- **起点问题**：异步（含延迟更新与部分 rollout）agentic RL 中，训练端在 rollout 版本上的 old logits 缺失，使训练–推理偏差修复与策略陈旧度校正无法按语义分开；阈值耦合导致后期崩溃；"无损"加速系统是否保留 old logits 未核对。
- **对象与条件**：PPO/GRPO 类 token 级离策略校正；推理端（vLLM/SGLang）与训练端（FSDP/Megatron）数值不同；rollout 与训练异步，单条轨迹可跨多个参数版本。
- **初始任务/评测**：agentic 多轮工具任务（2605.12070 用 τ²-Bench、VitaBench）；Qwen3-4B 稠密与 Qwen3-30B-A3B MoE；最大版本差 3。
- **瓶颈与证据边界**：精确获取 old logits 的现有方法（快照、专用模型、中断同步）系统代价高；近似参考（插值、EWMA）不恢复语义。原证据只到版本差 3、两种骨干、单框架；后期崩溃机理只有阈值扫描证据。
- **用户约束**：预研 2×A100 80G / 4×L40 48G / 8×4090 24G；正式实验 8×A100 80G，单次最好不超过 5 天；付费 API 1000 元内可自主；token 资源稀缺；目标自 2026-10 起半年内投一篇主会；不做世界模型、视频生成、机器人。预研只回答 go/no-go，先做最便宜的否证检查。
- **进入实验规划的成功条件**：一个候选通过两次独立审查（三项贡献分都 ≥6 且至少两项 ≥8，可行性 pass，verdict 为 experiment_ready，无致命阻断），并给出可在上述算力内完成、能区分主张的最小实验与可复现强基线。
