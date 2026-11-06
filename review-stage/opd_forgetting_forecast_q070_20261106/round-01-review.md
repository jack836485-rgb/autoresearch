## 结论

2026-11-06 评审：总体 score 5.0，verdict = promising_needs_revision。主贡献是“OPD 训练前跨教师来源预测 OOD 遗忘”，并用分层对手区分静态距离、教师能力和初始方向干扰三种解释。这个任务表述有价值，在 OPD 里也确实没人做过。但核心预测量（校准到固定域内 JS 后的单批方向干扰）本质上衡量的是选择性 ρ，不是遗忘量。OPDArena 已有数据显示，跨类别比较时 ρ 的排序和遗忘排序可以相反。而且三维都没有到 8 分的项，所以现在还不够进入实验规划。

## Claim 判断

| 维度 | 分数 | 依据 |
|---|---|---|
| 重要性 | 6.5 | 按“保留”筛 OPD 教师，与 ESC 那类按“收益”筛教师是互补的，有实际用处。但这个设置里遗忘幅度不大：OPDArena Table 1 中 OPD 各教师的 OOD 变化在 −4.14～+1.39 pp，外部教师之间只差 1–2 pp，影响面有限。只在数学单一训练域、Qwen 两个家族上做，外推范围也窄。 |
| 新颖度 | 6.5 | 我检索到的工作里，没有在 OPD 中把“训练前预测遗忘量、跨教师类别同线”当作任务来做的。ESC（2610.39020）预测的是收益；OPDArena 只算了局部 ρ；Razor 和 OPDArena 的 OOD JS 都是训练后才测。不过探针本身就是 OPDArena §G.2 / Eq. 22–24 的“校准域内 JS 后测 OOD”，只是把规模扩大、把评价改成遗忘；分层对手比较是常规的预测器竞赛；风格/内容分解直接用的是 2611.07722 的类别规则。新意主要来自任务定义和评测，机制本身没有实质新东西，所以算可辨认的增量，不到 8。 |
| 有效性（先验合理性） | 5.0 | 支持的证据：Eq. 23–24 在小步、固定方向下成立；2606.18024 在 NTK 或线性化的 PEFT 下可以在训练前精确预测遗忘；Table 18 与 Table 14 中 ρ 的排序一致。**直接反证**：探针把方向校准到同一个域内 JS，消掉了“训练会在域内走多远”这一项，可遗忘量大约是 ρ × D_in(t)。OPDArena Table 3（第 120 步）里，Qwen2.5-1.5B 学生的 A 大基座教师 ρ=0.311、OOD −0.39，B 大 SFT 教师 ρ=0.217、OOD −0.69；Qwen3-4B 学生的 A ρ=0.643 却 OOD +0.31，B ρ=0.218、OOD −1.92。也就是说，跨类别时 ρ 和遗忘方向相反，能单调对上遗忘的是绝对 D_OOD。到第 780 步，排序又随学生翻转：Table 1 中 Qwen2.5-1.5B 下 OPD(Q3-8B) −1.83 对 Self-OPD(SFT) −0.21，Qwen3-4B 下是 −0.38 对 −2.15。这说明决定排序的是 D_in 随步数增长的速度，单步方向量没有覆盖这个因素。另外两处：(a) 探针用的是原始梯度 g，而实际配方是 Adam 加常数 lr，第一步更新约等于逐坐标的符号方向，Fisher 能量比会随之改变，所以“初始更新方向”的定义需要说明；(b) H3 的先验偏弱：Table 12 中首位置置零后 OOD 差 ≤0.53 pp；2611.07722 中风格 token 约 0.6M、数学 token 约 4.7M，按总量算风格位置的振幅（约 0.74M）低于数学位置（约 1.63M），所以“风格分量占干扰大头”缺少依据。 |
| 待预研 | 不计分 | 各预测量在 11 个和 8 个教师上能达到多高的秩相关；300 步时遗忘跨度能否超过种子噪声的 3 倍；探针方向能多大程度代表 300 步的路径；外部指令/推理教师在 Raw 格式 rollout 上的反馈表现如何。 |

**与起点的关系**：这是起点问题的直接扩展，对象、条件和“同一曲线”目标都没变。起点的静态 OOD KL 设想被放进 Tier 0 作为对手，可以直接回答。起点里没回答、这里也没回答的是：遗忘“量”随训练步数的增长由什么决定。

**实验能否判别主张**：部分能判别。H1 和 H3 的设计可以分清各自的竞争解释，H3 用等反馈总量的内容位置掩码做对照，这一点做得对。H2 的判据要求“两个学生上都高于每一个 Tier 0 量，且 CI 与最好的 Tier 0 量不重叠”。每个学生只有 11 和 8 个教师，Tier 0 约有 12 个竞争量，教师层面的 bootstrap CI 必然很宽，ESC 原文在 5 个教师时自己也承认 CI 包含 0。所以这个判据大概率得不出结论，而计划里的兜底（“按胜出的量改写结论”）在 n 这么小时也很难成立。留一类外推时，用来拟合的只有 4 个点（2 个自训加 2 个构造），平均绝对误差的意义也有限。主指标“金标对数似然”在 IFEval 上没有定义，因为 IFEval 没有金标答案。

**可行性：pass**。OPDArena 代码可公开访问（git ls-remote 已确认），配方在 Table 7 有完整说明；opd-esc 仓库可访问；hkust-nlp/Qwen-2.5-1.5B-SimpleRL-Zoo 在 HF 上公开。Qwen2.5 学生配 Qwen3 教师在 OPDArena Table 1 里已经跑过。1.5B 学生、7–14B 教师，在 2×A100 上每步 1.5–2 分钟、300 步 8–10 h 的估计合理；总计约 26 次运行、500 GPU·h 左右加上评测，能放进 960 GPU·h。探针没有现成代码，但 §G.2 的公式和校准流程写得足够清楚，可以独立实现。风格/内容规则按 2611.07722 附录独立实现，并先做复现检查，路线可信。需要事先写清的一点：指令/推理类外部教师在 Raw 格式前缀上打分时，存在模板错配（OPDArena Table 10/15 显示输入格式会显著改变教师的开头和 EOS 概率）。这会把“外部后训练类”的表现和格式效应混在一起，但不妨碍实验能做出来。

## 最高近邻

1. OPDArena（https://arxiv.org/abs/2610.25651）：同一基座、只换教师，测遗忘；§G.2 / Table 18 在训练前算校准后的局部 ρ，§G.3 定义了 ρ_T。重叠度最高。差别：它只有 2 学生 × 3 构造教师，没有预测遗忘量，没有外部后训练教师，也没有和静态量比较。
2. Distilling the Shape of Uncertainty / ESC（https://arxiv.org/abs/2610.39020）：在 OPD 训练前做教师选择，有 Spearman、regret 和 bootstrap CI 的评测协议。差别：它预测域内收益，不管遗忘。
3. Every Coin Has Two Sides（https://arxiv.org/abs/2608.16647）：同源与跨源教师在 OPD 中跨域迁移的差别，以及 Top-16 overlap 的初始差异。这和 H1 的“类别内可排、跨类别不同线”直接相关，但它没有训练前预测遗忘。
4. Catastrophic Forgetting is Low-Rank（https://arxiv.org/abs/2606.18024）：在训练前用跨任务 NTK 核预测遗忘向量。它是机制来源，在 NTK 或线性 PEFT 下精确，但不是 OPD，也不涉及教师比较。
5. RL's Razor（https://arxiv.org/abs/2509.04259）及 Reinforcing What the Student Has Learned / SD-OPD（https://arxiv.org/abs/2611.07722）：前者给出训练后 KL 与遗忘的关联；后者给出风格位置与数学位置的振幅差，但没测遗忘。分别对应事后上界参照和 H3 的观察来源。

```json
{
  "score": 5.0,
  "contribution_scores": {"importance": 6.5, "novelty": 6.5, "effectiveness": 5.0},
  "contribution_assessment": "主贡献是把 OPD 训练前跨教师来源预测 OOD 遗忘定义为任务，并用分层对手区分静态距离、教师能力和初始方向干扰；任务定义和评测是新的，但探针沿用 OPDArena §G.2，风格/内容分解沿用 2611.07722，新意属于增量。有效性方面：Eq.23–24 只支持校准后的 ρ（选择性），而遗忘量大约是 ρ×D_in(t)；OPDArena Table 3 中 A 与 B 教师（两个学生上都如此）跨类别时 ρ 排序与遗忘排序相反，Table 1 中第 780 步的排序还随学生翻转，构成直接反证。探针没有说明 Adam 预条件下的方向；H3 有 Table 12 的部分反证，按总量算风格振幅也不占优。三维都没有 ≥8 的项。",
  "feasibility": "pass",
  "feasibility_reason": "OPDArena 与 opd-esc 代码可访问，Table 7 配方完整，SimpleRL-Zoo 教师公开，Qwen2.5 与 Qwen3 混配已有先例；探针可按 §G.2 独立实现；约 26 次 300 步运行加评测约 500 GPU·h，在 960 GPU·h 内。需要说明后训练外部教师在 Raw 格式上的模板错配。",
  "verdict": "promising_needs_revision",
  "fatal_blockers": [
    "贡献门槛未达到：重要性 6.5、新颖度 6.5、有效性 5.0，没有 ≥8 的维度。",
    "核心预测量与已有数据冲突：探针校准到固定域内 JS，只衡量选择性 ρ，消掉了域内移动幅度；OPDArena Table 3 中 A 与 B 教师在 Qwen2.5-1.5B 和 Qwen3-4B 两个学生上，跨类别时 ρ 排序与遗忘排序都相反，Table 1 中第 780 步的排序也随学生翻转。Claim 缺少能预测遗忘“量”或 D_in 增长速度的机制。",
    "H2 判据难以判别：每个学生只有 11 和 8 个教师，却要对约 12 个 Tier 0 量要求 CI 不重叠，大概率得不出结论；留一类外推只用 4 个点拟合；IFEval 上的金标似然主指标没有定义。"
  ],
  "novelty_conclusion": "在 OPD 中把训练前遗忘预测当作跨教师类别的任务来做，检索里没有发现直接先例。但探针就是 OPDArena §G.2 的局部 ρ 方法扩大规模，分解规则来自 2611.07722，评测协议仿照 ESC，所以是有内容的增量，不是独立的新机制。“第一个训练前遗忘预测量”的说法需要收紧，因为 OPDArena 已经在训练前算过局部 ρ。",
  "closest_neighbors": [
    "OPDArena: Understanding Learning and Forgetting in On-Policy Distillation (arXiv 2610.25651)",
    "Distilling the Shape of Uncertainty: What On-Policy Distillation Learns and How to Predict It (arXiv 2610.39020)",
    "Every Coin Has Two Sides: On the Dual Nature of Generalization in On-Policy Distillation of Large Language Models (arXiv 2608.16647)",
    "Catastrophic Forgetting is Low-Rank: A Function-Space Theory for Continual Adaptation (arXiv 2606.18024)",
    "RL's Razor: Why Online Reinforcement Learning Forgets Less (arXiv 2509.04259); Reinforcing What the Student Has Learned: Teacher-Guided On-Policy Distillation (arXiv 2611.07722)"
  ]
}
```
