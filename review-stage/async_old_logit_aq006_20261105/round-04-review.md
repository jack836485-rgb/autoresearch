## 结论

2026-11-05：总体 score 4.8，verdict **needs_rethink**。如果关键结果成立，主贡献是两件事：一是一张"引擎 × 版本"的二维路由回放分类表，二是在异步 MoE RL 中借一次推理端 prefill 取得"推理端·当前"路由，并把比率按推理端拆分。贡献不够，理由有三：
- 二维拆分与比率分解在 2512.01374 中已经基本写出（R2/R3 的"训推偏差 × 陈旧度"因子分解），新增部分主要是"沿交换图的另一条边分解"这一工程替代；
- 核心的"占优"判断已有直接反证。同策略时 v=θ，"推理端·当前"就等于 R3。2512.01374 在同策略下发现 R3 无收益；RDC 在 (2048,2048) 同步单更新时 R3 低于 TIS。2512.01374 还发现低离策略下 R2 优于 R3，引擎轴的符号随陈旧度反转，与"两轴近似可加"相悖；
- brief 用来"统一解释"三项结果的框架，漏掉了这两篇论文自己给出的主要解释：回放会改变目标策略（2512.01374），或回放会造成专家梯度偏差（RDC）。

## Claim 判断

| 维度 | 分数 | 依据 |
|---|---|---|
| 重要性 | 6.0 | 异步 MoE RL 中回放哪份路由，是真实且有分歧的工程决策，把 R3、R2、RDC、PR² 的结论理顺有价值。但影响限于 MoE 异步 RL 的一个配置选择。若结果是"第四格 ≈ 原生"，可改变的判断很少。 |
| 新颖度 | 5.5 | 2512.01374 §3.2 已把 R2 写成"只降陈旧度"、R3 写成"同时降训推偏差与陈旧度"的比率因子分解，并讨论目标策略偏差。2605.12070 已提出"训推偏差项 × 陈旧度项"的语义分解。剩下的新意是：用推理端 prefill 在当前权重上取 $q_\theta$ 与 $R^{inf}_\theta$，把分解改走"训练·当前 → 推理·当前 → 推理·旧"这条边。这是可辨认、廉价、未见他人做过的替代（检索未找到异步下推理端重打分取当前路由的工作），但本质是"把同策略 R3 在异步下重新做出来"加上已有分解的换边，属常规组合级增量。 |
| 有效性 | 4.5 | 下面分四项列出当前依据与未知。 |

有效性的依据与未知：
- **版本轴（当前路由优于旧路由）有依据。** 依据有三：PR² 显示更新后路由优于冻结路由（同步多 mini-batch 设置）；RDC 在异步下的训练端·当前 + 过滤 + TIS 比 R3 高 4.5（但两轴同时变化）；vLLM 博客报告每步 4 次更新约 7% token 换专家组合。
- **引擎轴在"当前"版本上的依据是反向的。** 同策略下"推理端·当前"就是 R3。2512.01374 写明同策略 R3 "does not yield performance gains"，并归因于目标策略被改变。RDC Table 1 的 (2048,2048) 中，GRPO+R3 的 AIME24/25 为 74.9/65.4，低于 GRPO+TIS 的 80.0/71.3（有 TIS 混杂）。因此 Claim 3 中"优于原生（训练端·当前）、不劣于原生 + RDC"目前没有正向依据。较可能的结果是第四格 ≈ 原生，且低于原生 + RDC。
- **"两轴近似可加"与已有数据冲突。** 2512.01374 原文是 gbs=2×mbs 时 R2 优于 R3，4×、8×时 R3 优于 R2。brief 只引了高离策略的一半，并写成"同策略下二者等价"；实际上同策略下 R2 不适用（文中写明 inapplicable）。这属于证据引用失真。
- **"$q_\theta/q_v$ 是同一推理端上两个真实采样器之比"不准确。** $q_\theta$ 来自 prefill，而不是 decode 采样器。R3 论文指出同框架重复前向也会路由分歧，所以该因子里混有 prefill/decode 数值差，需要用版本差 0 层的翻转率作为底噪单独报告。
- **仍未知：** 为什么推理端路由在当前版本能胜过原生路由，目前没有给出机制，只剩"把数值偏差单独掩码"这一点。而这一分解不需要回放推理路由也能做（原生路由 + 推理端 prefill 的 $q_\theta$）。

**与原问题的关系**：这是邻近新问题（路由层的同类纠缠）。"推理端 prefill 取 $q_\theta$ 以绕开 old logits"对稠密模型也成立，部分推进了起点问题；起点问题中的系统审计、长视程 agentic 任务和后期崩溃机理仍未回答。转向本身不构成阻断。

**实验能否判别主张**：只能部分判别。有三个问题：
- 缺"原生路由 + 推理端分解比率"一臂，无法区分收益来自路由选择还是来自比率分解。现设计在 2×2（路由 {原生, 推理·当前} × 比率 {总比率, 分解}）中只覆盖三格，交互项不可测。
- 每臂 100 步、2 种子、MATH-500 avg@4 / AMC23 avg@16，难以分辨 1–3 点差异。RDC 中 R3 的后期退化在约 100 步之后才显现，"崩溃"类主张在 100 步内很可能观测不到。
- 未把 2512.01374 的目标策略偏差解释列为需要排除的竞争解释。

**可行性：pass。** 依据如下：
- AReaL 仓库确有 `examples/r3`（Moonlight-16B-A3B，4 卡 SGLang + 4 卡 Megatron），`areal/engine/r3/preprocess.py` 按 prompt+completion−1 行解码路由，prefill 钩子复用这一现有通道即可实现；
- R2 的 CPU 快照约 4×32 GB，可行但重；
- 15 次 × 约 5 小时在 8×A100 上 5 天内可完成，无需付费 API。

需修正两处：
- Moonlight `max_position_embeddings=8192`，"最大响应 8k"加上 prompt 会越界，示例配置的 SGLang `max_model_len` 也只有 4096；
- 仓库示例只是 3 步 GSM8K 冒烟配置，3 分钟/步的估计需阶段 0 实测。

同步后 prefill 会让训练端等待"同步 → prefill"串行完成，墙钟开销需如实计入。

## 最高近邻

1. **Stabilizing RL with LLMs: Formulation and Practices**（2512.01374）https://arxiv.org/abs/2512.01374
   - 重叠：已把 R2/R3 写成训推偏差 × 陈旧度的因子分解，并指出回放改变目标策略；同策略 R3 无收益；R2/R3 优劣随离策略程度反转。
   - 差别：无"推理端·当前"异步取法，非异步设置。
2. **Router Drift Control (RDC)**（2610.21682）https://arxiv.org/abs/2610.21682
   - 重叠：异步 Qwen3-30B-A3B 下，训练端·当前路由 + 漂移过滤 + TIS 优于 R3；给出回放的专家梯度偏差分析。
   - 差别：不回放、不做推理端重打分。
3. **PR²: Predictive Routing Replay**（2606.00395）https://arxiv.org/abs/2606.00395
   - 重叠：沿版本轴用预测的更新后路由替代冻结路由。
   - 差别：用学习的预测器、同步 mini-batch 设置，而非精确 prefill。
4. **Rollout Routing Replay (R3)**（2510.11370）https://arxiv.org/abs/2510.11370
   - 重叠：推理端路由回放，同策略下即"推理端·当前"。
   - 差别：异步下只取旧版本路由。
5. **Missing Old Logits in Asynchronous Agentic RL**（2605.12070）https://arxiv.org/abs/2605.12070
   - 重叠：提出训推偏差项与陈旧度项的语义分解，以及 old logits 获取路线。
   - 差别：沿训练端旧版本分解，未考虑推理端当前权重重打分与路由层。

```json
{
  "score": 4.8,
  "contribution_scores": {"importance": 6.0, "novelty": 5.5, "effectiveness": 4.5},
  "contribution_assessment": "主贡献为'引擎×版本'二维路由回放分类与经推理端prefill精确取得'推理端·当前'路由并按 p_θ/q_θ · q_θ/q_v 分解比率。重要性有限（MoE异步RL的配置选择）；二维因子分解与目标策略偏差讨论已见于2512.01374，语义分解已见于2605.12070，新增的是沿另一条边分解与廉价取法，属常规组合级增量；有效性方面版本轴有PR²/RDC/vLLM 7%翻转的支持，但引擎轴在当前版本上已有反证（同策略即v=θ时R3无收益或低于TIS），2512.01374显示R2/R3优劣随离策略程度反转，与'两轴可加'相悖，brief对此证据引用不完整；prefill因子并非真实decode采样器之比。",
  "feasibility": "pass",
  "feasibility_reason": "AReaL examples/r3 与 r3/preprocess.py 路由通道存在，prefill钩子可复用；R2快照约128GB主机内存可行；15次×约5h在8×A100五天内可完成；需修正Moonlight 8192上下文与8k响应冲突，并以阶段0实测步时与prefill墙钟开销。",
  "verdict": "needs_rethink",
  "fatal_blockers": [
    "贡献不足：三项均未达8，二维分解与比率因子分解已在2512.01374/2605.12070中基本给出，新增部分为常规组合级增量",
    "Claim阻断：'推理端·当前优于原生并不劣于原生+RDC'与已有同策略证据相反（2512.01374同策略R3无收益；RDC同步单更新R3低于TIS），且brief遗漏2512.01374低离策略下R2优于R3这一与'两轴可加'冲突的结果",
    "Claim阻断：框架未纳入2512.01374的目标策略偏差与RDC的专家梯度偏差这两条竞争解释，实验也缺'原生路由+推理端分解比率'一臂，无法区分收益来自路由选择还是比率分解；100步×2种子难以判别1–3点差异与后期崩溃"
  ],
  "novelty_conclusion": "未检索到在异步MoE RL中以推理端prefill于当前权重重取路由与q_θ的工作，此取法本身新；但二维轴框架与比率因子分解已被2512.01374（R2/R3因子分解与目标偏差）和2605.12070（训推×陈旧语义分解）覆盖，整体为可辨认但分量有限的增量。",
  "closest_neighbors": [
    "Stabilizing Reinforcement Learning with LLMs: Formulation and Practices (arXiv 2512.01374)",
    "Router Drift Control: Mitigating Off-Policy Degradation in Mixture-of-Experts Reinforcement Learning (arXiv 2610.21682)",
    "PR2: Predictive Routing Replay for MoE-Based LLM Reinforcement Learning (arXiv 2606.00395)",
    "Stabilizing MoE Reinforcement Learning by Aligning Training and Inference Routers (arXiv 2510.11370)",
    "Missing Old Logits in Asynchronous Agentic RL: Semantic Mismatch and Repair Methods for Off-Policy Correction (arXiv 2605.12070)"
  ]
}
```
