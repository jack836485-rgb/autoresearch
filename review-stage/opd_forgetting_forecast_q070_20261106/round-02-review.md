## 结论
2026-11-06：总体 score 6.3，verdict = promising_needs_revision。如果结果成立，主贡献是一条训练前就能用的、有符号、按任务给出的 OPD 域外变化规律：同源教师的逐任务能力差会被继承，跨源教师的能力差被同源度门控、基本传不过来。它还提供一个用于"保留"的教师筛选规则，并用同规模跨源教师把来源和规模拆开。问题和实验都成形了，但贡献的分量还不够。"同源会把学生往教师水平拉、能升也能降；跨源主要拟合训练分布"这件事，2608.16647 已经定性报告过（§4.1、§5）；"跨源强教师的 OOD 优势传不过来"，OPDArena 的 Table 1/3 也已经有数。本工作实际新增的是定量化、训练前预测和来源/规模的拆分。三项里没有一项能有依据地给到 8 分，因此不过门槛。

## Claim 判断
| 维度 | 分数 | 依据 |
|---|---|---|
| 重要性 | 6.5 | OPD 的教师选择和保留是真实问题。能逐任务、带符号地在训练前预测（比如提前知道 IFEval 或知识类任务会降），比只给 macro 遗忘更有用。但同一套配方下外部教师造成的 macro 遗忘只有 0.4–1.8 pp（OPDArena Table 1，Qwen2.5-1.5B），较大的是 Self-OPD(SFT) 在 8B 上的 −4.14。结果也只覆盖数学训练域和 Qwen 系，影响范围有限。另外，"Razor 式距离在 OPD 中不成立"需要收窄：OPDArena Fig. 2 显示训练后 OOD JS 和遗忘正相关，被否定的只能是"训练前静态师生距离当主效应"这一种说法。 |
| 新颖度 | 6.0 | 定性规律已经发表：2608.16647 中同源教师只用数学提示就把学生的代码和科学能力拉向教师水平，弱于学生时会拉到初始以下（§4.1、Fig. 4a）；跨源教师主要拟合训练分布，初始 Top-16 重叠低且训练中不升（§5 Fig. 6）。OPDArena 报告了同源继承（Table 9、Fig. 12）和跨源大教师致遗忘（Table 2/3）。ESC（2610.39020）已经把训练前预测写成教师选择任务，只是只预测域内收益。可辨认的增量是三点：把规律写成"κ(o_t)·G(t,k) + a_t"这种有符号、逐任务、可嵌套比较的形式；目标对象换成通用能力遗忘；用 Qwen3-1.7B(-Base) 这类同规模跨源教师拆开来源和规模（2608.16647 的跨源教师都更大）。三点都属于整合和定量化，没有新机制。 |
| 有效性（先验合理性） | 6.5 | H1 有两篇独立的直接证据：OPDArena D.3 中 Self-OPD(SFT) 继承了教师的 OOD 下降（Qwen3-8B：−2.83 → −4.14），2608.16647 中同源弱教师把 GPQA 拉到初始以下。H2 在同一配方下有直接数据：Qwen2.5-7B Base 教师 OOD 比学生高约 14.6 pp，学生却是 −0.39（Table 3 step 120）/ −0.66（Table 1）；Qwen3-8B Base 教师高约 16 pp，学生 −1.83。有部分相左的证据：2604.13016 §3.3 发现同家族 1.5B/7B 教师从学生视角"分布上不可区分"。那是域内、R1-Distill 系的结果，但它让人怀疑 Qwen2.5 的 1.5B/7B 配对到底算不算"跨源"，所以用连续的 o_t 而不是二分标签是必要的。没处理好的竞争解释是任务层面的易感性：数学 OPD 可能普遍压低某些任务，比如知识类的 TriviaQA/NQ。Qwen2.5-Math 系同源教师恰好在这些任务上弱，于是"符号跟随 G"也可能由任务效应单独产生。当前模型 ΔOOD ≈ a_t + κG 里没有任务固定效应，H1 也就不能和这个解释区分开。另外，Self-OPD(SFT) 的遗忘超过教师本身，这意味着 κ>1 或者 a_t 为负，单靠"继承"解释不了。 |
| 待预研 | — | 各教师 κ 的绝对大小、同源组与跨源组斜率差能否超过种子噪声、a_t 由什么决定、o_t 和 κ 的单调关系是否成立、M5 在留一教师预测上比 M1–M4 好多少。这些都不计入分数。 |

**与起点的关系：** 研究的仍是原问题，只是把预测形式从"静态 KL 主效应"改成了"同源度门控的有符号继承"。原问题里还没回答的部分是遗忘的时间进程和数学以外的训练域，brief 已经如实写出。

**实验能否判别主张：** 大体能。10 个教师、70 个格子；同规模跨源教师的 G 有正有负，可以识别跨源斜率；6 个金标任务改用金标对数似然，降低了遗忘测量的噪声，是对的。不足有三点。(1) 混合效应模型必须明确加入任务固定效应，或者对每个任务按教师做中心化，否则 H1 和"任务易感性 × Math 教师在知识类任务上弱"分不开。(2) 7B 跨源教师在 7 个任务上的 G 几乎都是正的，跨源斜率主要靠 Qwen3-1.7B 那一对来识别，H2 的交互检验实际上只靠 2 个教师支撑，功效很低。(3) 指令和数学指令教师在 Raw 前缀上的 G 带有模板偏差，"配对内抵消"只对组间差成立，对组内斜率不成立。

**可行性：pass。** OPDArena 代码和 SimpleRL-Zoo 仓库都能访问。HF 元数据确认 Qwen2.5-Math-1.5B 的 base_model 是 Qwen2.5-1.5B，Qwen2.5-Math-1.5B-Instruct 的 base_model 是 Qwen2.5-Math-1.5B，所以同源归类成立。算力上，2×A100 每次运行 300 步约 9 h，20 次共约 400 GPU·h，8 卡并行约 2–3 天，在约束内；不需要人工标注，也不需要付费 API。有一个必须先修的实现问题：Qwen2.5-Math-1.5B/7B（含 Instruct）的 config 是 max_position_embeddings=4096、rope_theta=10000，而 brief 设的是"提示 ≤1024 + 响应 4096"，教师会在超过 4K 的位置上给出失真的反馈。这 4 个教师，包括预研用的两个，必须统一把总长度限制在 4096 以内，否则会被误读为教师效应。

## 最高近邻
1. Every Coin Has Two Sides（https://arxiv.org/abs/2608.16647）：同源 OPD 跨域把学生拉向教师水平，能升也能降；跨源主要拟合训练分布；初始 Top-16 重叠可以区分来源。本工作和它的差别：它没有测通用能力遗忘，没有训练前定量预测，跨源教师都更大，来源和规模混在一起。
2. OPDArena（https://arxiv.org/abs/2610.25651）：同一配方、同一 OOD 套件下报告了 Self-OPD 继承教师遗忘（Table 9、Fig. 12）、跨源大基座教师致遗忘和 ρ（Table 2/3），以及训练后 OOD JS 与遗忘相关（Fig. 2）。本工作和它的差别：它没有统一成有符号规律，也没有在训练前预测。
3. Distilling the Shape of Uncertainty / ESC（https://arxiv.org/abs/2610.39020）：已经把训练前教师选择写成预测任务，并和重叠类预测量比较。本工作和它的差别：ESC 只预测域内收益，不涉及 OOD 遗忘和来源门控。
4. Rethinking OPD: Phenomenology, Mechanism, and Recipe（https://arxiv.org/abs/2604.13016）：思维模式兼容性和初始重叠决定 OPD 成败；同家族 1.5B/7B 教师从学生视角不可区分。这一点和本工作把同家族 7B 归为跨源部分相左，而且只覆盖域内。
5. RL's Razor（https://arxiv.org/abs/2509.04259）：遗忘和训练后在训练任务上的 KL 相关。本工作和它的差别：它的 KL 在训练后测、不带符号，也没涉及教师来源。

```json
{
  "score": 6.3,
  "contribution_scores": {"importance": 6.5, "novelty": 6.0, "effectiveness": 6.5},
  "contribution_assessment": "主贡献：OPD 域外变化 ≈ a_t + κ(同源度)·有符号逐任务能力差，可在训练前预测，并用同规模跨源教师拆开来源与规模。重要性 6.5：教师保留筛选有用，但外部教师 macro 遗忘仅 0.4–1.8 pp，只有数学域、Qwen 系。新颖度 6.0：同源双向继承、跨源只拟合已有 2608.16647 定性结论，跨源强教师致遗忘已有 OPDArena Table 1/2/3，ESC 已把训练前教师选择写成预测任务；新增的是定量化、有符号逐任务形式、来源/规模拆分。有效性 6.5：H1 有两篇直接证据，H2 有 OPDArena 同配方数值；2604.13016 同家族 1.5B/7B 不可区分构成部分反证；任务易感性竞争解释未处理（模型无任务固定效应）；Self-OPD(SFT) 超过教师的遗忘需要 κ>1 或负 a_t。待预研：κ 大小、组间斜率差是否超过种子噪声、a_t 的来源、M5 相对 M1–M4 的预测增益。",
  "feasibility": "pass",
  "feasibility_reason": "OPDArena 代码和 SimpleRL-Zoo 可获得，HF 元数据确认 Qwen2.5-Math-1.5B(-Instruct) 与学生同源；2×A100 每次约 9 h，20 次约 400 GPU·h，8 卡约 2–3 天，无人工标注和付费 API。需先修：Qwen2.5-Math 系教师 max_position_embeddings=4096、rope_theta=1e4，提示+响应须统一限制在 4096 内。",
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "贡献不足：三项均 <8（6.5/6.0/6.5），核心定性规律（同源双向继承、跨源只拟合、跨源强教师致遗忘）已由 2608.16647 和 OPDArena 报告，本工作的增量主要是定量化与来源/规模拆分，分量不足以过门槛",
    "Claim 判别：门控继承模型缺少任务固定效应，H1 的'符号跟随 G'无法和'数学 OPD 的任务易感性 × Qwen2.5-Math 教师在知识类任务上弱'分开；跨源斜率主要靠 Qwen3-1.7B 一对识别，H2 功效很低"
  ],
  "novelty_conclusion": "目标领域没有发现同时做到有符号、逐任务、训练前预测 OPD 通用能力遗忘并拆开来源与规模的工作，但定性现象已被 2608.16647 和 OPDArena 覆盖，ESC 已把训练前教师选择写成预测任务；属于可辨认的整合与定量化增量（约 6 分），不是新机制。",
  "closest_neighbors": [
    "Every Coin Has Two Sides: On the Dual Nature of Generalization in On-Policy Distillation (arXiv 2608.16647)",
    "OPDArena: Understanding Learning and Forgetting in On-Policy Distillation (arXiv 2610.25651)",
    "Distilling the Shape of Uncertainty: What On-Policy Distillation Learns and How to Predict It (arXiv 2610.39020)",
    "Rethinking On-Policy Distillation of Large Language Models: Phenomenology, Mechanism, and Recipe (arXiv 2604.13016)",
    "RL's Razor: Why Online Reinforcement Learning Forgets Less (arXiv 2509.04259)"
  ]
}
```
