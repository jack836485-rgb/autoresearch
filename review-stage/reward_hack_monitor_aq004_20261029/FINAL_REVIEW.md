# 最终评审：A-Q004（未通过门槛）

- 输入：`path-stage/LLM热门方向_算力适配_20261028` 的 A-Q004
- 状态：`blocked_max_reviewer_calls`（预算 9 次，已用 8 次；第 9 次未使用，原因见末尾）
- 门槛：同一 brief 两次独立评审均 > 8 且无致命阻塞。本轮没有任何 brief 首审超过 8。

## 评审轨迹

| 调用 | 候选 | 分数 | 结论 | 主要阻塞 |
|---|---|---|---|---|
| 1 | IDEA-003 | 5.5 | promising_needs_revision | 能力不匹配前提未核实；风格混淆未隔离；追踪器使"免标注"不成立；策略类别太少 |
| 2 | IDEA-006 | 6.5 | promising_needs_revision | 后期负例被投机污染；未与 Kirch et al. 区分 |
| 3 | IDEA-007 | 7.5 | promising_needs_revision | 无致命阻塞；对照不可构造、指令泄漏、步 0 饱和、引用偏强 |
| 4 | IDEA-008 | 7.0 | promising_needs_revision | 负例与正例生成模型错配；主测试床正例纯度 |
| 5 | IDEA-009 | — | — | reviewer 启动约 1 分钟后失联，无输出（计入预算） |
| 6 | IDEA-009 | 7.6 | promising_needs_revision | 定位表述：EleutherAI 已在检查点上比较诱导者 |
| 7 | IDEA-010 | 6.8 | promising_needs_revision | Trace-and-Amplify 从第 1 步起即有在策正例，部署性主张不成立 |
| 8 | IDEA-011 | 7.5 | promising_needs_revision | 无致命阻塞；新意边界薄（Kirch incentivised 数据沿 RL 时间轴重做）；漂移不足与天花板风险高 |

## 最佳结果

IDEA-011（Call 8，7.5/10，无致命阻塞）。

**Claim 判断（Call 8）**
- 问题本身新颖：未检索到"投机出现前用 RL 检查点诱导数据训练监控器，并测其对之后自然投机的前瞻召回"的工作。
- C1（诱导分布随检查点逼近）：部分重合。"能力先于投机"已有 PRIME / 2609.16268 报告；按类别距离检验是新的，但只能在 overwrite-tests 上做。
- C2（前瞻召回高于初始模型诱导与等预算自然采样）：新颖，但与 Kirch et al. 的边界薄。
- C3（大模型诱导拆分能力与 RL 分布；AST 规范化检验风格）：新颖。

**最高近邻**
1. Trace-and-Amplify：https://arxiv.org/abs/2604.23488
2. Kirch et al.：https://arxiv.org/abs/2511.17408
3. EleutherAI Reasoning Interpolation：https://blog.eleuther.ai/reward-hacking-indicators/
4. Designing Effective Monitor-Based Interventions for Mitigating Reward Hacking During RL（ICML 2026）：https://icml.cc/virtual/2026/79298
5. PRIME：https://arxiv.org/abs/2606.09711 ；SimHack：https://arxiv.org/abs/2610.28707

## 为何未达门槛

- 后四次有效评审在 6.8–7.6 之间。每轮修掉一个设计问题后，新 reviewer 会指出另一个，但"新意幅度中等"是共同结论。
- 剩余价值主要取决于实证结果，即诱导者效应是否存在、是否足够大。这在 idea 层面无法再提高。

## 剩余风险

- overwrite-tests 投机前只有约 80 步 LoRA-GRPO，检查点诱导与初始模型诱导可能几乎无差别。
- Countdown-Code 只有"改目标值"一种策略，诱导提示直接点出该做法，初始模型诱导的监控器可能已到天花板；overwrite-tests 投机有明显词面特征，也有天花板风险。
- Countdown-Code 原文未给投机出现的步数，需试跑测定。
- IDEA-010 brief 中"Trace-and-Amplify 每题 1024 个样本"取自 Call 7 对脚本参数的读取，Call 8 未能核实；原文做法是"重采样直到出现投机，带重试上限"。

## 未使用第 9 次调用的原因

规则要求首审通过后还需一次独立复核。只剩 1 次时，即使首审通过也只能以"首轮通过、未复核"收尾，不会产生 FINAL_IDEA.md；而后四轮分数没有显示出超过 8 的趋势。因此保留这次额度，建议先做下面 PIVOT_OR_STOP.md 中的试跑。
