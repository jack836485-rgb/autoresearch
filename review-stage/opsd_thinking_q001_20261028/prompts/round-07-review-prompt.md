You are an independent senior reviewer checking whether a research idea is novel enough
for experiment planning. You are not a co-author and must not redesign the idea.

You are intentionally zero-context. Judge only the current four-part brief, the frozen
Problem Anchor, and the user's constraints. Search the closest prior work yourself; the
author's own literature notes are deliberately withheld. Do not invent papers, links, or results.
Today's date: 2026-10-28. Known tool workarounds: Shell 访问 arxiv.org 与 api.github.com 会被代理拒绝（403）；请用你的 WebSearch/WebFetch 工具读论文（先搜索以获得可抓取的 URL；同一站点连续抓取过快会被限流，请逐页抓取；arxiv 的 PDF 链接或 huggingface.co/papers/<id>.md 通常比 HTML 更完整；部分论文有多个版本，请核对最新版本），用 git clone --depth 1 --filter=blob:none --no-checkout 加 git ls-tree / git show 查看仓库文件
Finish all searches before answering and leave no background tasks running. Do not read other
files in this workspace and do not write files, except your raw review to /home/claude/autoresearch/review-stage/opsd_thinking_q001_20261028/round-07-review.md (UTF-8).
Your final message must contain only the review below.

Score the idea from 1 to 10. Judge whether the Claim is genuinely distinct, whether the method
is more than a relabeling or trivial combination, and whether the minimal experiment distinguishes
it from the closest work under the same core budget. Check whether the story line forms an
evidence-backed causal chain from a specific existing failure, through an overlooked key idea and
the proposal's concrete action, to a falsifiable expected result; unsupported claims that everyone
performs poorly or ignores the issue are claim blockers. Also verify that the positioning keywords
are established terms, that each experimental baseline belongs to the same domain and task, and
that every nontrivial baseline has a working public implementation and a concrete reproduction
route. Cross-domain inspiration is not an experimental baseline. Missing or mismatched baseline
evidence is a fatal feasibility blocker and cannot receive experiment_ready. When a supplied
paper is present, verify that the proposed novelty belongs to the new idea and still stands after
removing that paper's name. Treat a proposal that merely repairs, completes, or adds an experiment
to the supplied paper as a fatal novelty blocker.

Verdict meanings:
- experiment_ready: score > 8 and no fatal novelty, feasibility, or claim blocker
- promising_needs_revision: potentially salvageable, but the novelty boundary remains unresolved
- needs_rethink: the core claim is covered or the experiment cannot test it
- reject: not worth further work under the stated constraints

对外只输出下面三个 Markdown 部分，不要给重构方向、修改清单、实验 checklist 或长综述：
## 结论
<用当前日期给出 score、verdict、新颖性判断，以及是否值得继续。>

## Claim 判断
<用短表格逐条判断 Claim：新颖、部分重合或已被覆盖；每条只给最关键依据。>

## 最高近邻
<最多列 5 篇重叠最高的论文或系统；给出可核验链接、重叠点和仍有的差别。每篇 1-2 行；无法核验就写"需要检索"。>

末尾附上仅供主执行器解析的 JSON，不要增加其他章节：
   {
     "score": 0.0,
     "verdict": "promising_needs_revision",
     "fatal_blockers": [],
     "novelty_conclusion": "...",
     "closest_neighbors": ["paper title or needs_search"]
   }

Current four-part brief:

## 背景

**定位关键词：** on-policy self-distillation；privileged information；thinking models；epistemic tokens；forward KL

**一句话定位：** 在策略自蒸馏（OPSD）中，同一模型看到参考解答后充当教师，在学生自己的 rollout 上按逐 token 前向 KL 拟合。学生 rollout 开着思考时，OPSD 会让思考模型退化。本 Idea 在真正发生退化的开思考设置下，回答两个问题：
- 退化需要的是"本题的特权信息"，还是"上下文里多了一段同形解答"带来的分布偏移？
- 认知类 token 总量这一通道，对退化是否必要、是否充分？

## 核心 Claim

**现有方法在什么条件下失败。**
- 2609.20612 在 Qwen3-1.7B 上用同一参考视图和配置做了对比。评测都开思考，基座得 80.21：
  - 直接回答式 rollout（DR）训练到第 100 步得 82.62（Full Trace）；
  - 开思考 rollout（TH，损失只覆盖前 1,024 token）只得 72.79。
- 2607.05184 也发现只有训练时开思考才有害：Qwen3-4B 训练开思考 0.532，关思考 0.590，基座 0.591。

**"语义还是偏移"在 TH 下从未检验过。**
- 在不开思考的设置下，这个问题已有答案：
  - 换成另一道题的解答作教师上下文，效果仍具竞争力（OP²SD 2608.09228 摘要原话为 "remains competitive"）；
  - 不带参考的教师就能解释 Qwen3-1.7B 的大部分增益（2609.20612）。
- 但这两项对照都只在直接回答式 rollout 上做过，而那里根本没有退化。2609.20612 指出，TH 同时改变了推理模式、监督跨度与被监督比例；marker 抑制在两种模式下同号，所以区分不了相反的结局。它没有在 TH 下做任何内容对照。OP²SD 附录 H 在两边都开思考时只跑了本题参考的 OPSD：AIME24 49.24，比基座 49.86 低 0.62，单种子，作者自认无法归因；另一题参考在开思考下没有测。2608.18271 也报告他题参考能复现正确参考的大部分效果，有时更好，但没有报告退化。
- 另外，"另一题参考"自带另一题的答案，会把"没有本题信息"与"被错误答案误导"混在一起。

**认知通道在 OPSD 中没有按类的因果检验。**
- 主流解释是知道答案的教师压低 wait、hmm、maybe 等认知 token（2607.05184 称为 fork 抑制，作者自认未证明因果）。
- 2603.24472（v4，GRPO 中的因果干预一节，DeepSeek-R1-Distill-Qwen-7B）惩罚认知 token，复现了下降与推理变短。但那是 RL 中的充分性检验。
- 2609.20612 发现 marker 抑制在 DR 与 TH 中同号，区分不了两种结局；它的 marker 损失排除只在 DR 下做过。
- 同一设置下最接近的干预是 AD-OPSD（2607.10805）：Qwen3-1.7B，学生与教师都开思考，上限 1,024。它按熵选位置，在高熵位置把更新锚定到基座，认知词密度在 T/T 下从 10.3 降到 7.9。它是按熵掩码，不是按认知类掩码，也没有内容对照。

**被忽视的关键：两个可以干净分开的对照。**
- **本题信息 vs 同形上下文。** 两种教师上下文都取解答轨迹的开头一段，截到同一 token 长度，并经过过滤，确保都不含答案：
  - 一个取本题自己的轨迹开头，给出本题的部分推理，但不含本题答案；
  - 一个取长度匹配的另一题轨迹开头，不含那道题的答案。
  - 两者格式、长度相同，都不含任何最终答案，唯一的差别是内容是否属于本题。
  - 完整的本题轨迹（含答案）作为第三个参照。
- **认知总量 vs 其余信号。** 前向 KL 按类分组可以精确分解。这是 Decoupled KD（2203.08679）的目标类/非目标类分解在认知 token 类 $E$ 上的推广：
  $$\mathrm{KL}(\pi_T\|\pi_S)=\underbrace{\mathrm{KL}(\mathrm{Bern}(m_T)\|\mathrm{Bern}(m_S))}_{L_{\text{marg}}}+\underbrace{m_T\,\mathrm{KL}(\pi_T^{E}\|\pi_S^{E})+(1-m_T)\,\mathrm{KL}(\pi_T^{\neg E}\|\pi_S^{\neg E})}_{L_{\text{cond}}}$$
  - $m_T$、$m_S$ 是教师与学生在 $E$ 上的总概率；$\pi^{E}$、$\pi^{\neg E}$ 是在 $E$ 内、$E$ 外重新归一的条件分布。
  - $L_{\text{marg}}$ 只管"多犹豫还是少犹豫"，$L_{\text{cond}}$ 是其余全部信号。
  - 2607.05184 附录 E 显示，加参考后 marker 边际只从 0.00928 降到 0.00853，所以 $L_{\text{marg}}$ 在 KL 中占比很小。2603.24472 的 GRPO 结果又说明，这一小通道在行为上可能很强。因此"只用 $L_{\text{marg}}$ 训练是否就足以造成退化"事先无法确定。这是该通道上信息量最大的检验。

**本 Idea 主张：**
1. **（主）退化需要本题信息。** 在 TH 下，教师看到"本题解答轨迹的开头（不含答案）"会造成显著下降；看到"另一题轨迹的同长开头（不含答案）"不会。
2. **（次）认知总量通道既不必要也不充分。**
   - 不必要：只用 $L_{\text{cond}}$ 训练仍会复现大部分下降。
   - 不充分：只用 $L_{\text{marg}}$ 训练时，$E$ 密度确实下降，但准确率不显著下降。

**结果如何判定（事先固定，穷尽）**

记号：
- Δ 为相对基座 B 的变化。
- 差值用按题目配对、跨 3 个种子重采样的 bootstrap，取 95% CI。
- 所有判定只在事先检查通过后进行。事先检查要求：T0（官方截断目标、完整参考）与 T0u（未截断）都相对 B 显著下降，且下降不小于原文 −7.4 的一半。否则后续判定作废，如实报告。

**主张一（本题信息）**，I-own 与 I-other 为上述两种不含答案的开头上下文。等价界 δ 取 T0u 降幅点估计的 25%，在 T0u 全部种子跑完、I-other 评测之前算定，并且不小于 1 分。主张一的三臂各用 5 个种子。

| 结果 | 判定 |
|---|---|
| ΔI-own 的 CI 上界 < 0，ΔI-other 的 CI 下界 > −δ，且 I-other − I-own 的 CI 下界 > 0 | 支持"需要本题信息" |
| ΔI-other 的 CI 上界 < 0，且 I-other − I-own 的 CI 含 0 | 推翻主张一：同形上下文即足以造成退化 |
| ΔI-own 与 ΔI-other 都显著为负，且 I-other − I-own 的 CI 下界 > 0 | 部分：报告偏移份额 s = ΔI-other / ΔI-own |
| ΔI-own 不显著为负（只给不含答案的本题开头时退化消失） | 推翻主张一的前提：退化需要轨迹后段或答案本身，报告 T0u − I-own |
| 其余 | 不确定，报告效应量 |

**主张二（认知通道）**：
- T1 只用 $L_{\text{cond}}$；T2 只用 $L_{\text{marg}}$；T3 同 T1 但 $E$ 换成频率匹配的随机类。
- 挽回比例 $r=(T1-T0u)/(B-T0u)$。
- 两项操纵检查：
  - M1：评测 rollout 上，T1 的短语级广义认知密度与 B 相差不超过 ±10%。
  - M2：T2 的 $E$ 密度降幅不小于 T0u 的一半。

| 结果 | 判定 |
|---|---|
| $r$ 的 CI 上界 < 0.25 且 M1 通过；M2 通过且 T2 − B 的 CI 下界 > −1 分 | 支持主张二（既不必要也不充分） |
| $r$ 的 CI 上界 < 0.25 但 M1 未通过 | 不可识别：认知抑制泄漏到 $E$ 之外 |
| M2 通过且 T2 − B 的 CI 上界 < 0 | 推翻"不充分"：仅认知总量就足以造成退化 |
| $r$ 的 CI 下界 ≥ 0.5 且 T1 − T3 的 CI 下界 > 0 | 推翻"不必要"：认知总量通道是必要的 |
| $r$ 的 CI 下界 ≥ 0.5 但 T1 − T3 的 CI 含 0 | 非特异 |
| M2 未通过 | T2 信号太弱，充分性不可检验 |
| 其余 | 两项都有贡献，报告 $r$ 与 T2 − B |

另外报告 T1 − T4，不进判定。T4 为 TH 下仓库现成的 marker 位置损失排除，用来说明按类保留总量与按位置排除损失的差别。

## 方法设计的核心思想

**输入：**
- Qwen3-1.7B；2609.20612 的 AMPLE-Math 冻结切分；开思考的冻结教师。
- 认知类 $E$：
  - 取 2609.20612 的 11 个 marker、2603.24472 的 10 个认知词、hmm、alternatively、recall 的并集；
  - 包括各大小写与带空格的整词单 token；
  - 多 token 词只取首子词，且要求该首子词在初始学生 rollout 中超过一半的出现都属于这些词；
  - 构建规则与最终列表在训练前固定。
- 随机类：总概率与 $E$ 相差 20% 以内的整词单 token 普通词，排除认知词、数字与数学符号，用固定种子抽取。

**实际动作：**
1. **低成本复现 TH。** 仓库 `train_opsd.py` 的 `apply_loss_horizon` 只截取前 1,024 个补全 token。所以生成上限设为 1,024，损失就与原文 20,764 上限的 TH 训练相同。
2. **两种不含答案的开头上下文。**
   - Full Trace 是来源数据集的原文推理轨迹，正文本身会推出答案。所以只去掉仓库拼接的 `\boxed` 后缀并不能去掉答案。
   - 改为取开头：
     - I-own：本题 Full Trace 的前 L token，L 为该题轨迹长度的 40%，在 token 边界截断。
     - I-other：按 `length_matched_other_problem.py` 的配对规则取另一题，截取它 Full Trace 的前 L token（与 I-own 同长）。
   - 答案过滤：用仓库的数学判分器把各题标准答案归一化。若 I-own 的文本中出现本题答案，或 I-other 的文本中出现配对题的答案（包括 `\boxed`），就从训练集剔除该题。剔除规则在训练前固定。
   - 事先统计保留率：若低于 60%，把 40% 降到 30% 再统计一次；仍不足就如实报告，并用保留下来的子集。
   - 被剔除的题在所有臂上都剔除，以保证各臂训练集相同。
3. **T2 的剂量匹配。** $L_{\text{marg}}$ 在 KL 中占比很小，按原权重训练 100 步可能移动不了认知密度。所以在事先检查中，从 $w\in\{1,10,100\}$ 里选出最小的权重，使 T2 在第 100 步训练 rollout 上的 $E$ 密度降幅不小于 T0u。这一选择只看训练 rollout 的 marker 统计，不看任何准确率，选定后固定为 T2 的损失 $w\,L_{\text{marg}}$。这样检验的是：与 T0u 同等幅度的认知抑制本身，是否足以造成退化。
4. **按项构造损失。** T0u、T1、T2、T3 由每个位置的教师和学生 logits 直接算 $L_{\text{marg}}$ 与 $L_{\text{cond}}$。$m_T$ 视为常数。这些都不做逐项截断，所以 T0u 精确等于两项之和。I-own、I-other 也用未截断的完整 KL，以便和 T0u 比较。官方截断目标 T0 只作复现锚点。
5. **描述量（不进判定）。**
   - 训练前，$L_{\text{marg}}$ 占总 KL 的比例。
   - 参考路径拉力：在开发切分上，学生不看参考时给参考解答文本的平均每 token 对数概率，减去基座的对应值。对应 2608.04794 的 PI 偏差。与 DR 锚点并列报告。

**输出：** 各臂在开思考评测下相对基座的变化、两张判定表的结论、$r$、s、M1/M2、marker 密度、平均长度、撞上限的比例，以及参考路径拉力。

**与最高近邻的关键差别：**
- 2609.20612 与 OP²SD：本题参考 vs 他题参考的对照只在直接回答设置下做过，而且他题参考带着错误答案。本 Idea 在真正退化的 TH 下，用经过答案过滤、等长的两种轨迹开头，把"本题信息"与"同形上下文"分开，并用完整轨迹作参照。
- 2607.05184：掩码对照在不带特权信息的 OPD 中进行，按位置掩码。
- AD-OPSD（2607.10805）：同设置，但按熵选位置、锚定到基座，不按认知类，也没有内容对照。
- 2608.18271：他题参考对照，未报告退化设置。
- 2603.24472：因果研究在 GRPO 中。
- Purified OPSD、2608.04794：分解与 PI 偏差只作诊断。
- 本 Idea 用 DKD 式分解对认知通道做"只保留一项"的必要性与充分性检验。

## 最小实验

**模型与设置：**
- Qwen3-1.7B。在这个模型、这套代码和配置下，TH 下降已有报告（2609.20612 表 11）。
- 全部沿用该仓库默认配置：100 步；有效 batch 32；恒定学习率；损失温度 1.1；rollout 温度 1.1；LoRA 秩 64、α 128，覆盖 7 个投影模块；教师冻结并开思考。
- TH 臂统一使用 `ROLLOUTS=thinking TRAIN_MAX_NEW_TOKENS=1024 LOSS_HORIZON=1024`，被监督的 token 规则相同，只改教师上下文或损失项。

**各臂：**
- 复现锚点：T0（官方截断、完整 Full Trace），3 个种子。
- 主张一：T0u（未截断、完整 Full Trace）、I-own、I-other，各 5 个种子。
- 主张二：T1、T2、T3，以及 T4（TH 下 `--fork-mask-mode exclude`），各 3 个种子。
- DR 锚点：原文配方。
- 基座直接评测。

- DR 锚点 3 个种子。

共 9 个训练配置，3 × 5 + 6 × 3 = 33 次训练。

**事先检查：**
- 先统计答案过滤的保留率（见方法第 2 步）。
- 跑 T0、T0u、I-own 的种子 0：T0 或 T0u 的下降不足原文一半时停止并报告；I-own 不显著下降时，按主张一判定表的第四格处理。
- 用最多 3 次短训练选定 T2 的权重 $w$（只看训练 rollout 的 marker 统计）。

**评测：**
- 主指标沿用 2609.20612 的协议：384 题冻结测试切分，开思考，Avg@4，并给出 4k/8k/16k 前缀判分。
- 外部基准 AIME24、AIME25、HMMT25：只评 B、T0u、I-own、I-other 的种子 0，每题 4 条，上限 38,912。只作描述，不进任何判定。

**Baseline 与复现入口：**

| 名称 | 与本任务的关系 | 论文 | 代码与复现入口 |
|---|---|---|---|
| TH 训练的 OPSD（T0） | 同任务、同模型、同评测的退化设置，最高近邻 | https://arxiv.org/abs/2609.20612 | https://github.com/xiuyuz/opsd-reference-study （2026-10-28 核验：`training/launch_run.sh`、`training/train_opsd.py`（`apply_loss_horizon`、`--pi-override-file`）、`opsd/opsd_loss.py`（官方 OPSD 前向 KL 与逐元素截断的移植）、`opsd/constants.py`（`CORRECTION_MARKERS`）、`data/controls/truncated_full_trace.py`、`data/controls/length_matched_other_problem.py`、`evaluation/build_eval_queue.py`）；`CONDITION=full_trace ROLLOUTS=thinking TRAIN_MAX_NEW_TOKENS=1024 LOSS_HORIZON=1024 bash training/launch_run.sh` |
| 不含答案的开头上下文（I-own / I-other） | 同上设置，只换教师上下文 | 同上 | 按 `truncated_full_trace.py` 的截断方式和 `length_matched_other_problem.py` 的配对规则生成，再用仓库判分器做答案过滤，经 `--pi-override-file` 传入 |
| marker 位置损失排除（T4） | 同任务已有的 marker 干预，在 TH 下运行 | 同上 | 同上，加 `EXTRA_ARGS="--fork-mask-mode exclude"` |
| DR 训练的 OPSD | 增益锚点 | 同上 | `CONDITION=full_trace ROLLOUTS=direct bash training/launch_run.sh` |
| 基座 | 参照 | — | `evaluation/build_eval_queue.py --mode thinking` 评测原模型 |

T0u、T1、T2、T3 的损失在 `opsd/opsd_loss.py` 旁新增一个函数实现。

**为什么不用无特权教师作对照：** 在 TH 下，不带参考的教师与学生是同一模型、同一模式、同一上下文，KL 恒为 0。仓库的 `--unprivileged-teacher` 只在 DR 下有意义。

**预算：**
- 该仓库报告：每次运行在单张 80GB GPU 上完成，DR 的 100 步约半小时（H100）。我们的 TH 臂生成上限同为 1,024，按 A100 每次约 1.5 小时计，33 次约 50 A100 小时。
- 测试切分评测：每个检查点约 6 A100 小时，共约 198 A100 小时。
- 外部基准：4 个检查点 × 3 个任务，每题 4 条，约 96 A100 小时。
- 参考路径拉力只需前向，约 5 A100 小时；T2 权重选择最多 3 次短训练，约 5 A100 小时。
- 合计约 355 A100 小时，2 张 A100 约 7.5 天。数学题用规则判分，不需要付费 API。

**支持结果：** 主张一判为"需要本题信息"；主张二判为"既不必要也不充分"。两者都只依据测试切分的判定表。

**推翻结果：** 两张判定表中的各推翻格；"部分""不可识别""非特异""信号太弱"各格都作为结论如实报告。

Frozen Problem Anchor and user constraints:

- 根本问题：特权上下文自蒸馏（OPSD）为何让训练时开思考的推理模型在长评测预算下退化？退化来自特权信息语义还是教师上下文分布偏移？失效时长度变短还是变长由什么决定？
- 领域与设置：数学推理；思考模型（Qwen3 系列等）在训练时开思考做 OPSD；OpenThoughts 类数学数据；在 AIME24/25、HMMT25 上评测 avg@k，评测生成预算 4k–38k。
- 必须解决的瓶颈：失效时长度方向冲突未对齐；1-shot OPD 一致有效只在自 RL 教师下测；外推到非数学与异族教师无证据。
- 约束：2×A100 80G；开源模型、LoRA 可接受；付费 API 1000 元以内；半年内投主会。
- 进入实验规划的成功条件：有一个可证伪的 Claim，最小实验能在上述资源内区分本 Idea 与最高近邻。
