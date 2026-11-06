## 结论
日期 2026-11-05。总体 score 4.5，verdict：needs_rethink。主贡献是"同一校正方法下，崩溃发生在累积漂移 $D=\sum\eta d_k$ 达到一个不随偏差来源与幅度变化的预算时，因此可用前 50 步外推崩溃步"。这一贡献不够。"崩溃预算＋粗扫描标定＋按训练步数预算选配置"已由 Song et al.（2607.01083）对陈旧度来源提出，brief 没有引用；那篇的预算是累积学习率 $\sum\eta$，不是漂移加权量，而且在 AdamW 下，崩溃时间与陈旧度 S 无关。这与"偏差幅度只改变到达同一 $D^*$ 所需步数"直接冲突。此外，2602.01826 显示自然偏差下 mismatch 依赖训练状态、晚期才突增，前 50 步外推缺乏依据。最小实验也没有把 $\sum\eta$、累积 KL 这类更简单的累积量放进对照，无法证明"漂移"这个具体量有解释力。

## Claim 判断
| 维度 | 分数 | 依据 |
|---|---|---|
| 重要性 | 6.0 | 事先判断某个配置在给定步数内会不会崩，并检验"放大偏差可代理温和长程偏差"这一被广泛采用的假设，有明确价值。但实用分量有限：score centering 本身是几乎免费的加法修正（只需采样端 top-k），"是否值得付修复代价"这一决策的价值不大；陈旧度方向的标定规则 Song et al. 已给出。若 (1) 不成立，也只说明预算依赖来源，不能"推翻"两篇工作的代理假设，因为每种来源仍可各自代理，所以反向结果的分量也被高估了。 |
| 新颖度 | 5.0 | 最高近邻 Song et al. 已有：崩溃时间 $t_{obs}\eta\approx c_2$ 的"累积学习率预算"、预算在不同 S 下近似不变、预算随模型与设置变化，以及"粗扫描估计预算再按目标训练长度选 S 和 η"的标定规则。2610.40945 已证明动力学只依赖 $\eta k$（半学习率曲线完全重合）。本 Idea 的增量有三点：以 score centering 漂移项加权的累积量、跨数值/陈旧度来源统一、和在线预警比提前量。这是可辨认的增量，但不是新的规律类型。 |
| 有效性（先验合理性） | 4.5 | 支持证据：2609.20807 图 3 中，同一方法的崩溃步随噪声单调提前（DPPO 160/80/20，TIS 稳定/180/40，已核对原文）；2610.40945 证明 $\eta k$ 时间重标度。这只能说明"偏差大则崩得早"，不能说明存在不变阈值。<br>直接反证与机制断点有四条：<br>① Song et al. 在 AdamW 下，不同 S 的崩溃时钟相同，即崩溃时的 $D$ 必随 S 变化；他们还给出稳定边界（$S\eta$ 低于阈值时漂移有界、可远超时钟不崩）。这与"任何非零漂移都线性累积到 $D^*$"的模型不符。图 3 中 TIS 在最小噪声下稳定，同样更像阈值行为。<br>② 2602.01826 发现自然 BF16 mismatch 前期平坦、临近崩溃时才起势；学习率降 10 倍时崩溃并非慢 10 倍，而是约 1.5k 步突增。这是状态依赖的非齐次增长，与"前 50 步拟合常数或指数增长后外推 3000 步"直接矛盾。VeXact 也显示聚合统计量在失败初期近乎平坦。<br>③ 2610.40945 指出，数值偏差是近似常数偏置，陈旧度是含负特征值的反馈环，两者机制不同；在 TIS 下，起作用的是截断残差（ESS<1/2 之后），而不是被 score centering 抵消的漂移项 $d_k$。所测量的量与 TIS 的失效机制不对应。<br>④ 学习率维度在 SGD 下近似纯时间重标度，必然会抬高 $T_c$ 的变异系数、而不改变 $D$，判断 (1) 会被这一平凡效应"自动"满足一部分。 |
| 待预研 | — | 不计分：外推误差能否进入 ±30%；自然 BF16/FP8 配置在 3000 步内是否真会崩；top-k 漂移估计在温和偏差下的信噪比。 |

**与起点问题的关系**：这是子问题（从缺失的 old logits 转向漂移累积与崩溃时间）。原问题中 old logits 的获取、哪些系统保留 old logits、agentic 多轮任务都没有回答。转向本身不构成阻断。

**实验能否判别主张**：不能充分判别。
- 对照缺少 Song 式 $\sum\eta$ 预算、累积训练–推理 KL 或 $|\log\text{ratio}|$ 预算这些"剂量"替代量。即使 $D$ 的变异系数小于 $T_c$，也分不清是"漂移"有解释力，还是任意单调的累积偏差量都行。
- 陈旧度只设每 8/16/32 步同步（原文用 64 步才在约 1200 步内拉开差距），400 步上限下大量运行会被截尾，跨来源不变性这一核心判断可能根本测不到。
- 阶段 2 只有 3 个非零偏差配置、各 1 种子。AReaL 移植在噪声为 0 的对照中 300 步未崩，自然配置很可能在 3000 步内也不崩，于是判断 2、3 退化为"预测安全"，而"永远不崩"的平凡预测器同样能通过。
- 已知 response-length surge 约在崩溃前 100–200 步出现，作为提前量基线是合适的。

**可行性：pass（有保留）**。实现路径真实可用：score-centering 仓库的 `train_rl.py` 已有 `staleness`、`weight_noise_scale`、int8/float8 采样器和 `kv_quant_bits` 开关（已克隆核对，JAX/optax，默认 SGD）；AReaL 的 `examples/math/score_centering_countdown.md` 存在，配置为 Qwen3-0.6B、SGLang BF16、SGD 0.01、top-128 head、300 步。
- 算力被低估。原文量化/陈旧度运行平均约 15.6 H100 小时/1200 步，权重噪声约 2.6 H100 小时/300 步。按此折算，阶段 1 约 600 A100 小时，阶段 2 每次 3000 步约 80 A100 小时，合计约 1000 A100 小时，接近或超过 8×A100×5 天（约 960 A100 小时）。不过崩溃即停可以节省一部分。
- 对 PG/TIS 运行计算 $d_k$ 的参数空间范数需要额外一次反向，不只是"已有的 head 收集"。开销可接受。

## 最高近邻
1. Song et al., Scaling Laws for Collapse in Asynchronous GRPO, https://arxiv.org/abs/2607.01083 。重叠：崩溃时间约等于累积学习率预算除以 η，预算在 S 间近似不变，粗扫描标定后按训练长度选配置，并有稳定边界。差别：只覆盖陈旧度、AdamW、Llama/Qwen3-8B；预算是 $\sum\eta$ 而非漂移加权量；不做跨来源统一，也不做早期外推。
2. Marek & Ryabinin, Score Centering Stabilizes Off-policy RL, https://arxiv.org/abs/2609.20807 。重叠：漂移项定义、"漂移随训练累积、放大偏差可代理温和长程偏差"的假设，以及实验设置与代码。差别：只做解释和修正，不预测崩溃时间。
3. On the Origin and Evolution of Training-Inference Mismatch in LLM RL, https://arxiv.org/abs/2610.40945 。重叠：数值偏差与滞后的分解、反馈环 $(I-\eta M)\Delta_k$、$\eta k$ 标度、ESS<1/2 失效点。差别：只做 40 步短训练，不给崩溃时间规律。
4. Beyond Precision: TIM is an Optimization Problem…, https://arxiv.org/abs/2602.01826 。重叠：mismatch 随优化升高、response-length surge 预警、调学习率。差别：只有在线预警，不做定量外推；同时提供了反证（降学习率后崩溃并非等比延后）。
5. Diagnosing TIM via a Zero-Mismatch Reference (VeXact), https://arxiv.org/abs/2605.14220 。重叠：自然小数值偏差可独立致崩，零偏差参考。差别：设置为 8k 长序列数学任务，不预测时间；同时显示聚合 KL 在失败初期平坦。

```json
{
  "score": 4.5,
  "contribution_scores": {"importance": 6.0, "novelty": 5.0, "effectiveness": 4.5},
  "contribution_assessment": "主贡献是'按校正方法存在跨来源、跨幅度不变的累积漂移预算，可用前50步外推崩溃步'。重要性6：可事先判断配置是否会崩，并检验放大偏差代理假设，但score centering几乎免费，决策价值有限，反向结果也不足以推翻代理假设。新颖度5：Song et al. 2607.01083已提出崩溃时间的累积学习率预算、跨S不变性和粗扫描标定规则，2610.40945已给出eta*k标度；剩余增量是漂移加权、跨来源统一和早期外推。有效性4.5：只有'偏差大则崩得早'的单调证据；Song在AdamW下崩溃时钟与S无关且存在稳定边界，2602.01826显示自然mismatch状态依赖、晚期突增（降lr 10倍并非慢10倍），2610.40945显示两类来源机制不同，且TIS下的有效偏差是截断残差而非d_k，这些都与关键假设冲突。实验缺少sum(eta)、累积KL等替代剂量对照；陈旧度8/16/32在400步内易被截尾；自然配置可能不崩，使外推检验退化。效果幅度待预研。",
  "feasibility": "pass",
  "feasibility_reason": "score-centering仓库train_rl.py已有staleness/weight_noise_scale/int8/fp8/kv_quant_bits开关（已核对），AReaL的score_centering_countdown示例存在（Qwen3-0.6B、SGLang BF16、SGD、top-128）；但按原文每步成本折算，总量约1000 A100小时，接近或超过8卡5天，估计偏低，需依赖崩溃即停；PG/TIS下计算d_k需额外一次反向。",
  "verdict": "needs_rethink",
  "fatal_blockers": [
    "新颖度/定位：未引用最高近邻 Song et al. 2607.01083，该文已提出崩溃时间的累积学习率预算（跨同步间隔近似不变）和粗扫描标定规则，本Idea的'漂移预算'只是其加权与跨来源推广",
    "有效性反证：Song et al. 在AdamW下崩溃时钟与陈旧度无关且存在稳定边界，与'幅度只改变到达同一D*的步数'冲突；2602.01826显示自然mismatch状态依赖、晚期突增，与前50步外推冲突；TIS下的有效偏差是截断残差而非被测的d_k",
    "Claim判别力：缺少sum(eta)、累积KL或|log ratio|等简单累积量对照，无法证明'漂移'这一具体量的解释力；学习率维度在SGD下是平凡时间重标度；陈旧度档位在400步上限下易截尾；自然偏差配置可能3000步内不崩，判断2/3会退化为平凡的'安全'预测"
  ],
  "novelty_conclusion": "相较2607.01083（陈旧度的累积学习率崩溃预算与标定规则）和2610.40945（eta*k标度），本Idea仅在漂移加权、跨来源统一和早期外推上有增量，属于普通增量，不是新的规律类型。",
  "closest_neighbors": [
    "Scaling Laws for Collapse in Asynchronous GRPO (arXiv 2607.01083)",
    "Score Centering Stabilizes Off-policy Reinforcement Learning (arXiv 2609.20807)",
    "On the Origin and Evolution of Training-Inference Mismatch in LLM Reinforcement Learning (arXiv 2610.40945)",
    "Beyond Precision: Training-Inference Mismatch is an Optimization Problem and Simple LR Scheduling Fixes It (arXiv 2602.01826)",
    "Diagnosing Training Inference Mismatch in LLM RL via a Zero-Mismatch Reference (arXiv 2605.14220)"
  ]
}
```
