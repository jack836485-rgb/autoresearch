## 结论
2026-11-05，总体 score 5.5，verdict：promising_needs_revision。主贡献是一个工程上干净的方法：在异步 MoE RL 中，每步同步后用推理端在当前权重上做一次 prefill，得到 $q_\theta$ 与 $R^{inf}_\theta$，训练端回放这份当前路由，并把总比率按恒等式改写为"当前版本的数值偏差 × 推理端两版本采样器之比"。贡献可辨认且可实现，但还不够：一是相对 PR²/RDC/2512.01374，新意只是用"精确重打分"替代"预测路由"或"过滤"，以及调换分解顺序；二是有效性依据正反都有，2512.01374 中与本方法主张直接相反的证据没有被处理。三项中没有一项达到 8，过不了门槛。

## Claim 判断
| 维度 | 分数 | 依据 |
|---|---|---|
| 重要性 | 6.5 | MoE 异步 RL 的稳定性是真实瓶颈，R3 在异步下的冻结代价已有 RDC 的 +4.5 和 PR² 的增益作旁证。但若成立，新增的只是 R3 的一个替代回放来源和一种比率写法，影响限于"每批一次更新"的异步 MoE 设置。若关键结果成立，值得知道的是：每步同步时，一次推理端重打分就能同时拿到路由一致性和当前专家梯度，不需要预测器，也不需要整条丢弃响应。 |
| 新颖度 | 6.0 | "R3 回放的路由会陈旧，应改用更新后的路由"已由 PR² 提出（它预测路由）。"R3 丢失当前训练路由专家的梯度"已由 RDC 论证。2512.01374 已把 R2/R3 写成"偏差项 × 陈旧项"的分解。本方法的增量有两点：在"每批一次更新"这一条件下，可以用推理端 prefill 精确得到当前路由与 $q_\theta$；以及把分解改写为 $p_\theta/q_\theta \cdot q_\theta/q_v$，绕开 old logits。我在 2605.12070 全文中没找到这种调换顺序的分解，它也确实不需要快照。但在结构上，它就是把 AReaL 的 decoupled PPO 里的近端策略换成"推理端当前权重"。另外，按每批一次更新的写法，陈旧因子与梯度脱钩，所谓"PPO 裁剪"实际上只是截断 IS 权重，并不是信任域。 |
| 有效性 | 5.5 | **现有支持**：R3 证明数值路由翻转需要消除；RDC 显示异步下保留原生路由优于 R3；vLLM 2026-10-14 博客显示，在数值逐比特一致、每步 1 次更新时，不回放路由也能训练，且 4 次更新时约 7% 的 token 换了专家组合。本方法正是在近似模拟"数值一致 + 当前路由"。**反向证据（brief 未处理）**：2512.01374 在 30B MoE 上发现，离策略程度大（gbs=4×/8× mbs）时 R3 优于 R2，R2 后期崩溃，结论是"离策略越大，越需要冻结路由"。本方法让陈旧的路由变化进入比率，恰好走向这条证据的反面。**迁移条件**：RDC 用 Qwen3-30B-A3B、FP8 vLLM、每 4 次本地更新同步一次；PR² 是同步多次更新。两者都不是"每步同步、版本差 ≤4"的 Moonlight 设置。**未知**：陈旧翻转率的实际量级，比率尾部是否会抵消收益。阶段 0 能回答前者，但不能回答后者。 |

与起点的关系：属于邻近新问题，把 old-logit 缺失时的语义分解迁移到 MoE 路由层。分解对稠密模型给出了一条无需 old logits 的精确路线，这推进了起点问题。但对"无损系统是否保留 old logits"的审计，以及 agentic 多轮任务的效果，仍未回答。转向本身不构成阻断。

实验能否判别主张：部分能。(a) 阶段 0 的 no-go 检查设计合理。(b) 主比较"优于 R3+TIS 与 RDC+TIS"用 Moonlight-16B-A3B 跑 150 步，并以 AIME24/25 avg@16 作为主判据。该模型在 AIME 上很可能接近地板，三种子差距很难超过种子间标准差，判别力存疑。(c) "收益来自路由来源还是比率形式"是最关键的竞争解释，但消融与 TIS 只跑 1 个种子，不足以归因。(d) prefill 位于"同步→重打分→训练"的关键路径上，会占用推理端生成算力，但对照只按等步数比较，没有给出等墙钟或吞吐的核算。(e) brief 没有处理 2512.01374 的 R2/R3 证据；按其结论，R2 类对照（训练端原生路由回放）是同任务下的应有对照。目前 TIS 臂（原生路由）只有 1 个种子。

可行性：pass。已核实 AReaL 主仓库有 `examples/r3`（Moonlight-16B-A3B，SGLang d1p1t4 + Megatron 4 卡，`return_routed_experts` 与 `enable_router_replay`）。`areal/engine/r3/preprocess.py` 按 prompt+completion−1 行解码路由。`remote_inf_engine.py` 在中断续写时保留已接收的路由行，只拼接新增后缀，因此 R3 基线确实回放的是生成时路由。prefill 请求（max_new_tokens=1，返回输入 logprob 与路由）可以复用现有通道。RDC 没有代码，但 Eq.2–6 足以独立实现。按每步约 1M token 估算，11 次运行约 3.5 天，在 8×A100、5 天的约束内，不需要付费 API。主要风险在评测判别力和步时实测，不在实现。

## 最高近邻
1. Router Drift Control (RDC), 2610.21682 — https://arxiv.org/abs/2610.21682 ：认定 R3 在异步下丢失当前专家梯度，保留原生路由并过滤高漂移响应，在异步下比 R3 高 4.5。差别：RDC 不回放路由、整条过滤；它的异步设置是每 4 次更新同步一次。
2. PR²: Predictive Routing Replay, 2606.00395 — https://arxiv.org/abs/2606.00395 ：提出 router staleness，主张用更新后的路由替代冻结路由。差别：PR² 用预测器预测路由，用于同步多次更新；本方法在每批一次更新时用 prefill 得到精确路由。
3. Stabilizing RL with LLMs: Formulation and Practices, 2512.01374 — https://arxiv.org/abs/2512.01374 ：把 R2/R3 写成偏差项与陈旧项的分解，并实测离策略程度大时 R3 优于 R2、R2 会崩溃。这是对本方法有效性最直接的反向证据，brief 未引用。
4. Stabilizing MoE RL by Aligning Training and Inference Routers (R3), 2510.11370 — https://arxiv.org/abs/2510.11370 ：本方法要替换的基线。差别仅在回放哪个版本的推理端路由。
5. Missing Old Logits in Asynchronous Agentic RL, 2605.12070 — https://arxiv.org/abs/2605.12070 ：给出 $p_\theta/p_v \cdot p_v/q_v$ 的语义分解，以及快照、专用模型、中断同步三种精确路线。差别：没有考虑在推理端当前权重上重打分、调换顺序的分解。参考 vLLM 博客 https://vllm.ai/blog/2026-10-14-train-inference-consistency ：数值逐比特一致且每步 1 次更新时不需要 R3。

```json
{
  "score": 5.5,
  "contribution_scores": {"importance": 6.5, "novelty": 6.0, "effectiveness": 5.5},
  "contribution_assessment": "主贡献：异步MoE RL每步同步后用推理端当前权重prefill得到q_θ与R^inf_θ，训练端回放当前路由，并按 p_θ/q_θ·q_θ/q_v 恒等分解做偏差掩码与陈旧度截断。重要性6.5：MoE异步稳定性是真实瓶颈，但贡献是R3的替代回放来源与比率写法，范围限于每批一次更新的设置。新颖度6.0：PR²已提出用更新后路由替代冻结路由，RDC已论证R3丢失当前专家梯度，2512.01374已给出R2/R3的偏差×陈旧分解；增量是在每批一次更新下用prefill精确获得当前路由，以及不需要old logits的调换顺序分解（结构上等同于把decoupled PPO的近端策略取为推理端当前权重）；陈旧因子与梯度脱钩，'PPO裁剪'实为IS截断。有效性5.5：RDC、PR²与vLLM逐比特一致博客支持使用当前路由；但2512.01374显示离策略程度大时R3优于R2、R2会崩溃，与本方法让陈旧路由变化进入比率的做法相反，brief未处理；各证据的模型、同步方式与目标设置不同，比率尾部效应未知。",
  "feasibility": "pass",
  "feasibility_reason": "已核实AReaL examples/r3（Moonlight-16B-A3B，SGLang 4卡+Megatron 4卡，return_routed_experts/enable_router_replay）及preprocess按prompt+completion−1行解码前缀路由；中断续写时保留生成时路由行；prefill打分可复用现有通道；RDC的Eq.2–6足以独立实现；11次运行约3.5天，在8×A100、5天约束内。",
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "贡献门槛未达：三项均低于8（6.5/6.0/5.5），新意相对PR²（更新后路由）、RDC（R3梯度丢失）与2512.01374（R2/R3分解）只是精确重打分与调换分解顺序。",
    "有效性定位缺口：未处理2512.01374中'离策略程度大时冻结路由（R3）优于R2、R2会崩溃'的反向证据；本方法让陈旧路由变化进入比率，恰在这条证据的反方向。",
    "判别力不足：Moonlight-16B-A3B在AIME上可能接近地板，以AIME avg@16的3种子均值作主判据难以判别；区分'路由来源 vs 比率形式'的消融和原生路由TIS臂只有1个种子，无法归因。",
    "预算核算缺失：prefill位于同步→训练的关键路径上并占用推理端算力，对照只按等步数比较，没有等墙钟或吞吐核算。"
  ],
  "novelty_conclusion": "未找到完全相同的方法（推理端当前权重prefill重打分 + 回放当前推理端路由 + p_θ/q_θ·q_θ/q_v 分解）；但核心思想分别被PR²（用更新后路由替代冻结路由）、RDC（R3丢失当前专家梯度、保留原生路由）和2512.01374（R2/R3的偏差×陈旧分解）覆盖，增量为条件化的精确实现与分解顺序调换，属可辨认的增量而非实质独立新机制。",
  "closest_neighbors": [
    "Router Drift Control: Mitigating Off-Policy Degradation in Mixture-of-Experts Reinforcement Learning (arXiv 2610.21682)",
    "PR2: Predictive Routing Replay for MoE-Based LLM Reinforcement Learning (arXiv 2606.00395)",
    "Stabilizing Reinforcement Learning with LLMs: Formulation and Practices (arXiv 2512.01374)",
    "Stabilizing MoE Reinforcement Learning by Aligning Training and Inference Routers (arXiv 2510.11370)",
    "Missing Old Logits in Asynchronous Agentic RL: Semantic Mismatch and Repair Methods for Off-Policy Correction (arXiv 2605.12070)"
  ]
}
```
