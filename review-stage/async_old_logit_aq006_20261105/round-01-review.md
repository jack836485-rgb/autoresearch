## 结论
日期 2026-11-05。总体 score 6.0，verdict 为 promising_needs_revision。主贡献是换锚点的 old-logit 估计 $\log\hat p_{v}=\log q_{v}+(\log p_\theta-\log q_\theta)$：偏差在当前权重上测，陈旧度只在推理端测，所以不需要历史权重，也天然支持跨版本的部分 rollout。我在检索范围内没有找到同样的做法，这个想法干净、便宜、可证伪。但目前贡献还不够过门槛，原因有两个。第一，估计"接近精确"依赖一个关键假设：逐 token 的数值偏差 $e$ 是权重的平滑函数，在版本之间高度相关。在作者瞄准的设置里（BF16 舍入误差、MoE 不做路由回放、路由离散翻转），这个假设恰好最没有依据。第二，已有证据显示精确 old logits 相对最强近似（修订版 PPO-EWMA）的余量很小，所以重要性有限。

## Claim 判断
| 维度 | 分数 | 依据 |
|---|---|---|
| 重要性 | 6.0 | 问题本身成立。2605.12070 显示精确 old logits 有价值，而快照每步多 95–178 s、最多驻留 76 GB。但在同一张表里，PPO-EWMA 和 Snapshot 很接近：30B-A3B 的 VitaBench in-store 是 33.41 对 34.62；4B 的 τ²-Retail pass@4 上 PPO-EWMA 还更高（90.35 对 89.47）。所以"零历史权重、近似精确"的增量价值主要在大版本差和跨版本部分 rollout 下，而这一点目前只有 2605.12070 作者的一句定性担忧（"PPO-EWMA 在极端版本差下可能不可靠"），没有量化证据。影响面是有用的系统/算法技巧，不是重要瓶颈的实质改变。 |
| 新颖度 | 7.0 | 2610.40945（DLC）的分解需要训练端在采样权重上做前向，等于假设旧权重可得。2605.12070 的三种精确方法都要保留旧权重，或靠中断时仍驻留的旧版本。A-3PO 和 PPO-EWMA 只构造近似参考。我没有检索到"把数值偏差在当前版本测出、平移回旧版本，陈旧度交给推理端自比"的估计。新意清楚，但机制很简单，本质是一个偏移量控制变量，可能被看作 DLC 分解的换锚点变体。新意的分量取决于能否证明这个平移在逐 token 上成立。 |
| 有效性 | 5.0 | **现有依据**：2610.40945 只观察到数值偏差的**平均量级**在训练中近似常数（FP8 约 0.02 nats/token，BF16 小于 $10^{-3}$），而且只在 Qwen3-0.6B/1.7B 稠密模型、单轮 Countdown、SGD 上。它没有测同一 token 的 $e_\theta$ 和 $e_{v}$ 是否相关。**迁移条件**：估计误差是 $e_\theta-e_v$，只有当 $e$ 随权重平滑变化时，它才是"偏差×滞后"的二阶小量。BF16 舍入误差和 kernel 累加顺序带来的误差，对权重的微小变化更接近伪随机；MoE 近平局的路由翻转是不连续的。如果 $e_\theta$ 和 $e_v$ 近似独立，误差方差约为 $2\mathrm{Var}(e)$，逐 token 反而比 Bypass（误差只有 $e_v$）差，优势只剩在相对 Decoupled PPO 的大 $g$ 区间。系统性的那部分偏差（量化、FP32 head 缺失等）能平移，随机的那部分不能。偏差里两者各占多少，目前未知。prefill 和 decode 的数值差也会直接进入误差。**仍未知**：逐 token 相关性、路由翻转 token 的占比和误差，以及保真度优势能否转化为训练差异。精确语义被证明有用，不等于本估计能拿到这份收益。 |

与原问题的关系：本 Idea 直接回答原问题中"缺失 old logits 时的解耦校正"部分。"哪些系统未保留 old logits"的审计，以及阈值耦合导致后期崩溃的机理，仍未回答；方案也只打算间接检验后者。范围收缩本身不构成阻断。

实验能否判别主张：阶段 A 的判别力好，能直接否证。它用真值 $\log p_v$ 逐 token 比较五种来源，看掩码和裁剪集合的不一致率，并有 MoE $g\le4$ 的 no-go 条件，正好检验上面最大的未知。我建议在已存的 $e_v,e_\theta$ 上直接报告两者的逐 token 相关系数，这是这个主张成立与否的核心量。阶段 B 判别力不足。2605.12070 中 Snapshot 和 PPO-EWMA 的差距只有 1–4 个点，而本方案每臂只有 1–2 个种子。在 Search-R1 EM 上，"优于最强非精确代理"和"与 Snapshot 同噪声带"很可能都落在噪声里，难以区分本方法、PPO-EWMA 和 Bypass+R3。此外，成本主张应该同时对比 2605.12070 的"部分 rollout 中断同步"精确路线。它同样不存旧权重，是不保存权重的精确方案中最便宜的竞争者，目前不在对照里。

可行性：pass。AReaL 中已核实以下几点：
- `examples/r3` 有 Moonlight-16B-A3B 单机 8 卡配置，SGLang 用 t4、Megatron 用 attn t4/ffn e4，并带 `return_routed_experts`。
- `prox_logp_method` 支持 recompute、loglinear 和 reuse_train_logp。
- 远程 SGLang 引擎有 `compute_logp`，打分路径用 `return_logprob` 和 `logprob_start_len`。
- 有 search_agent 示例。

本方法只需要在权重同步之后、训练之前加一次批次 prefill 打分，实现路线可信。有一点需要说明：这次打分处在训练关键路径上，会占用推理端的生成时间。阶段 A 存 20 版 Moonlight 约 640 GB 加前向，可以做。Snapshot 臂需要约 128 GB 主机内存，要按共享机器的内存余量规则确认。阶段 B 按 9×12 h ≈ 4.5 天估，贴近 5 天上限；3 分钟/步只是估计，存在超预算风险。PPO-EWMA 和 Snapshot 按 2605.12070 的 §5.2、附录 B 和 §5.1 独立复现，规范足够。

## 最高近邻
1. Missing Old Logits in Asynchronous Agentic RL（2605.12070，https://arxiv.org/abs/2605.12070）：重叠在问题定义、解耦目标、Snapshot、专用模型和中断同步三种精确方法，以及修订版 PPO-EWMA。差别：它们都需要旧权重或中断；本方法零历史权重，并支持任意跨版本 token。
2. On the Origin and Evolution of Training-Inference Mismatch（DLC，2610.40945，https://arxiv.org/abs/2610.40945）：重叠在偏差与滞后的精确拆分，以及偏差近似常数的观察。差别：DLC 用训练端在采样权重上的前向，即假设 old logits 可得；本方法把锚点换到当前权重，但需要 DLC 未验证的逐 token 可平移性。
3. A-3PO（2512.06547，https://arxiv.org/abs/2512.06547）：重叠在免额外前向的近似 proximal（对数线性插值），已进 AReaL。差别：只重参数化裁剪边界，不恢复 old logits 语义。
4. ENTR（2607.22186，https://arxiv.org/abs/2607.22186）：重叠在异步 agentic RL 的大陈旧度稳定性（最多 30 个版本），按熵归一化信赖域，把低熵区的训练–推理偏差放大视为噪声。差别：它改的是门控准则，不估计 old logits；在版本差 8 的扩展中，它是强竞争者。
5. Bitwise-consistent rollout（vLLM 博客，https://vllm.ai/blog/2026-10-14-train-inference-consistency）及 R3（2510.11370）：工程上消除或降低同一权重下的数值偏差。一旦逐比特一致，Bypass 就等于精确 old logits，问题本身消失。差别：目前只有少数模型和框架可用，AReaL/SGLang 上的 Moonlight 没有这一路径；它界定了本方法真正有用的范围。

```json
{
  "score": 6.0,
  "contribution_scores": {"importance": 6.0, "novelty": 7.0, "effectiveness": 5.0},
  "contribution_assessment": "主贡献是零历史权重的换锚点 old-logit 估计：偏差在当前权重上测，陈旧度只在推理端测。新意清楚，未检索到相同做法。重要性受限：2605.12070 中 PPO-EWMA 与 Snapshot 只差 1-4 点，增量价值主要在大版本差和跨版本部分 rollout，目前缺量化证据。有效性的关键假设（逐 token 数值偏差随权重平滑、版本间高度相关）没有直接证据：2610.40945 只显示平均量级在小稠密模型上近似常数。目标设置是 BF16 舍入加 MoE 路由离散翻转，偏差可能在版本间去相关，此时估计误差方差约为 2Var(e)，比 Bypass 更差。待验证：e_theta 与 e_v 的逐 token 相关性、路由翻转 token 的误差、prefill/decode 数值差，以及保真度优势能否转化为训练收益。",
  "feasibility": "pass",
  "feasibility_reason": "AReaL 已有 Moonlight r3 单机配置、prox_logp_method 多选项、SGLang compute_logp 打分路径和 search_agent 示例；本方法只需在同步后加一次批次 prefill 打分。阶段 A 存权重约 640 GB 加前向可行。阶段 B 约 4.5 天，贴近 5 天上限，步时尚待实测；Snapshot 臂需约 128 GB 主机内存。",
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "有效性不足：'估计误差是二阶小量'依赖数值偏差逐 token 随权重平滑且版本间相关，在 BF16 舍入与 MoE 路由翻转的目标设置下无依据；若去相关，逐 token 误差会比 Bypass 大。",
    "贡献分量未达门槛（6/7/5）：已有证据显示精确 old logits 相对 PPO-EWMA 的余量很小，大版本差下的增量价值缺少量化依据。",
    "Claim 判别不足：阶段 B 每臂 1-2 个种子，难以在 Search-R1 EM 上区分本方法、PPO-EWMA、Bypass+R3 与 Snapshot；成本主张也缺少对'部分 rollout 中断同步'这一不存权重的精确方案的对比。"
  ],
  "novelty_conclusion": "未检索到'在当前权重测偏差、平移回旧版本、陈旧度由推理端自比'的 old-logit 估计；与 DLC（需旧权重前向）、2605.12070 的精确与 EWMA 路线、A-3PO 插值都有实质差别。机制简单，新意的分量取决于能否证明逐 token 可平移。",
  "closest_neighbors": [
    "Missing Old Logits in Asynchronous Agentic RL: Semantic Mismatch and Repair Methods for Off-Policy Correction (2605.12070)",
    "On the Origin and Evolution of Training-Inference Mismatch in LLM Reinforcement Learning (2610.40945)",
    "A-3PO: Accelerating Asynchronous LLM Training with Staleness-aware Proximal Policy Approximation (2512.06547)",
    "Deconstructing Off-Policy Ratios: Entropy-Normalized Trust Regions for Asynchronous Reinforcement Learning (2607.22186)",
    "vLLM blog: Bitwise-Consistent Train-Inference RL (2026-10-14) / Stabilizing MoE RL by aligning training and inference routers (2510.11370)"
  ]
}
```
