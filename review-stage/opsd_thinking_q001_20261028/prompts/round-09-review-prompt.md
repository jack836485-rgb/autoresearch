You are an independent senior reviewer checking whether a research idea is novel enough
for experiment planning. You are not a co-author and must not redesign the idea.

You are intentionally zero-context. Judge only the current four-part brief, the frozen
Problem Anchor, and the user's constraints. Search the closest prior work yourself; the
author's own literature notes are deliberately withheld. Do not invent papers, links, or results.
Today's date: 2026-10-28. Known tool workarounds: Shell 访问 arxiv.org 与 api.github.com 会被代理拒绝（403）；请用你的 WebSearch/WebFetch 工具读论文（先搜索以获得可抓取的 URL；同一站点连续抓取过快会被限流，请逐页抓取；arxiv 的 PDF 链接（如 arxiv.org/pdf/<id>v1）或 huggingface.co/papers/<id>.md 通常比 HTML 更完整；部分论文有多个版本，请核对最新版本），用 git clone --depth 1 --filter=blob:none --no-checkout 加 git ls-tree / git show 查看仓库文件
Finish all searches before answering and leave no background tasks running. Do not read other
files in this workspace and do not write files, except your raw review to /home/claude/autoresearch/review-stage/opsd_thinking_q001_20261028/round-09-review.md (UTF-8).
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

**一句话定位：** 在策略自蒸馏（OPSD）中，同一模型看到参考解答后充当教师，在学生自己的 rollout 上按逐 token 前向 KL 拟合。学生 rollout 开着思考时，OPSD 会让思考模型退化。本 Idea 在确认会退化的设置下检验两件事。第一，领域里普遍采用的"认知 token 被压低导致退化"这一解释，在 OPSD 中是否成立。第二，退化是否只需"上下文前缀偏移"、不需要本题信息。

## 核心 Claim

**现有方法在什么条件下失败。**
- 2609.20612 在 Qwen3-1.7B 上用同一参考视图与配置对比。评测都开思考，基座为 80.21。
  - 直接回答式 rollout（DR）训练到第 100 步：82.62（Full Trace）。
  - 开思考 rollout（TH，损失只覆盖前 1,024 token）：72.79。
- 2607.05184 也发现只有训练时开思考才有害：Qwen3-4B 训练开思考 0.532，关思考 0.590，基座 0.591。
- 2608.04794 在 think 模式下训练 Qwen3-8B 做多轮工具调用（BFCL），平均也下降 3.51。
- 退化并不总会出现。2609.39118（表 4）在学生与教师都开思考、rollout 上限 1,024、学习率 1e-6 的条件下，Qwen3-1.7B 各种教师上下文都没有退化，OLMo-3-7B-Think 则全部退化。

**领域里的主流解释：认知抑制。在 OPSD 中它从未被因果检验。**
- 知道答案的教师给 wait、hmm、maybe 等认知 token 更低的概率，学生因此少犹豫、少核对。多篇工作以此为前提：
  - 2607.05184 称之为 fork 抑制，作者自认"未被隔离或证明为因果"；
  - 2607.10805（AD-OPSD）在 Qwen3-1.7B T/T 下观察到认知密度从 10.3 降到 7.9，并按熵在高熵位置把更新锚定到基座；
  - Purified OPSD（2607.02234）以"保留认知行为"作为目标。
- 已有的因果证据都不在 OPSD 中：
  - 2603.24472（v4，GRPO 中的因果干预一节）在 GRPO 中惩罚认知 token，复现了下降与推理变短；
  - 2607.05184 附录 E 在不带特权信息的 OPD 中比较"只在 marker 位置计损失"与"随机位置计损失"，两者无法区分。
- 反证：2609.20612 指出 marker 抑制在 DR（增益）与 TH（损失）中同号，所以区分不了结局；它的 marker 损失排除只在 DR 下做过。
- 至今没有人在退化的 TH-OPSD 中，只去掉或只保留"认知类总量"这一部分信号来检验它。

**语义还是偏移：TH 下只有单种子、带混淆的初步证据。**
- 2609.39118 表 4 在 TH 下做了"无关解答"教师上下文对照：在另一个题库的题与解前置于本题之前。
  - OLMo-3-7B-Think 上，无关解答降 6.0，完整解答降 4.7，只给答案降 7.4。作者据此认为作用来自前缀分布，而不是语义。
  - 这组对照只有单种子；无关解答带着那道题自己的答案，长度也没有匹配；Qwen3-1.7B 在该设置下没有退化。
- 其余的他题对照都在学生不开思考时进行：2609.20612、OP²SD（2608.09228，结论是 "remains competitive"）、2608.18271。

**被忽视的关键：用前向 KL 的类分组恒等式隔离认知通道。** 这一分解来自 Decoupled KD（2203.08679）的目标类/非目标类分解，此处推广到认知 token 类 $E$：

$$\mathrm{KL}(\pi_T\|\pi_S)=\underbrace{\mathrm{KL}(\mathrm{Bern}(m_T)\|\mathrm{Bern}(m_S))}_{L_{\text{marg}}}+\underbrace{m_T\,\mathrm{KL}(\pi_T^{E}\|\pi_S^{E})+(1-m_T)\,\mathrm{KL}(\pi_T^{\neg E}\|\pi_S^{\neg E})}_{L_{\text{cond}}}$$

- $m_T$、$m_S$ 是教师、学生在 $E$ 上的总概率；$\pi^{E}$、$\pi^{\neg E}$ 是 $E$ 内与 $E$ 外重新归一的条件分布。
- $L_{\text{marg}}$ 只管"多犹豫还是少犹豫"，$L_{\text{cond}}$ 是其余全部信号。
- 只用一项训练，就能分别检验认知通道的必要性与充分性。

**本 Idea 主张：**

1. **（主）认知通道既不必要也不充分。**
   - 不必要：只用 $L_{\text{cond}}$ 训练仍复现大部分下降。
   - 不充分：只用剂量匹配的 $L_{\text{marg}}$ 训练时，$E$ 密度降幅与完整 KL 相当，但准确率不显著下降。
   - 这一主张若成立，会动摇以认知抑制为前提的修法方向。
2. **（次）偏移即足够。** 在确认退化的 Qwen3-1.7B 配置下，两种教师上下文造成相当的退化：
   - I-own：本题解答轨迹的开头，不含答案；
   - I-other：等长的他题轨迹开头，同样不含答案。
   - 这是对 2609.39118 单种子观察的干净检验：两边等长、都不含任何答案、多种子。"他题答案误导"这一混淆也因此被排除。

**结果如何判定（事先固定，穷尽）**

记号与统计：
- Δ 为相对基座 B 的变化；差值用按题目配对、跨该臂全部种子重采样的 bootstrap，取 95% CI。
- 所有判定只在事先检查通过后进行。事先检查要求：T0（官方截断目标、完整 Full Trace）与 T0u（未截断）相对 B 显著下降，且降幅不小于原文 −7.4 的一半。否则后续判定作废，如实报告。
- 等价界 δ 取 T0u 降幅点估计的 25%，且不小于 1 分，在 T0u 全部种子跑完后、其他臂评测前算定。

**主张一（认知通道）**

各臂：
- T1：只用 $L_{\text{cond}}$。
- T2：只用 $wL_{\text{marg}}$，$w$ 为剂量匹配权重。
- T3：同 T1，但 $E$ 换成频率匹配的随机类。

判定量与检查：
- 挽回比例 $r=(T1-T0u)/(B-T0u)$。
- M1：评测 rollout 上，T1 的短语级广义认知密度与 B 相差不超过 ±10%。
- M2：评测 rollout 上，T2 的 $E$ 密度降幅不小于 T0u 的一半。

| 结果 | 判定 |
|---|---|
| $r$ 的 CI 上界 < 0.25 且 M1 通过；M2 通过且 T2 − B 的 CI 下界 > −δ | 支持主张一 |
| $r$ 的 CI 上界 < 0.25 但 M1 未通过 | 不可识别：认知抑制泄漏到 $E$ 之外 |
| M2 通过且 T2 − B 的 CI 上界 < 0 | 推翻"不充分"：与 T0u 同等幅度的认知抑制本身就足以造成退化 |
| $r$ 的 CI 下界 ≥ 0.5 且 T1 − T3 的 CI 下界 > 0 | 推翻"不必要"：认知通道是必要的 |
| $r$ 的 CI 下界 ≥ 0.5 但 T1 − T3 的 CI 含 0 | 非特异 |
| M2 未通过 | T2 信号太弱，充分性不可检验 |
| 其余 | 两项都有贡献，报告 $r$ 与 T2 − B |

另外报告 T1 − T4，不进判定。T4 是 TH 下的 marker 位置损失排除，用来对照"按类保留总量"和"按位置排除损失"两种做法。

**主张二（偏移即足够）**

| 结果 | 判定 |
|---|---|
| ΔI-own 与 ΔI-other 的 CI 上界都 < 0，且 I-other − I-own 的 CI 落在 ±δ 内 | 支持主张二 |
| ΔI-own 的 CI 上界 < 0，ΔI-other 的 CI 下界 > −δ，且 I-other − I-own 的 CI 下界 > 0 | 推翻主张二：退化需要本题信息 |
| ΔI-own 与 ΔI-other 都不显著为负 | 不含答案的开头不足以造成退化：退化需要轨迹后段或答案本身，报告 T0u − I-own |
| 其余 | 部分：报告偏移份额 s = ΔI-other / ΔI-own 及其 CI |

## 方法设计的核心思想

**输入：**
- Qwen3-1.7B；2609.20612 的 AMPLE-Math 冻结切分；开思考的冻结教师。
- 选用该文的配置，是因为在这套配置下 Qwen3-1.7B 的 TH 退化已有报告；在 2609.39118 的配置下这个模型不退化。
- 认知类 $E$：
  - 2609.20612 的 11 个 marker、2603.24472 的 10 个认知词，以及 hmm、alternatively、recall，取并集；
  - 取它们的各大小写与带空格的整词单 token；
  - 多 token 词只取首子词，且要求该首子词在初始学生 rollout 中超过一半的出现属于这些词；
  - 规则与最终列表在训练前固定。
- 随机类：总概率与 $E$ 相差 20% 以内的整词单 token 普通词，排除认知词、数字与数学符号，用固定种子抽取。

**实际动作：**
1. **低成本复现 TH。** 仓库 `train_opsd.py` 中的 `apply_loss_horizon` 只截取前 1,024 个补全 token。所以生成上限设为 1,024 时，损失与原文 20,764 上限的 TH 训练相同。
2. **按项构造损失。** 每个位置由教师与学生的 logits 直接算出 $L_{\text{marg}}$ 与 $L_{\text{cond}}$，$m_T$ 当作常数。T0u、T1、T2、T3 都不做逐项截断，所以 T0u 精确等于两项之和。官方截断目标 T0 只作复现锚点。
3. **T2 的剂量匹配。** 事先检查中，从 $w\in\{1,10,100\}$ 里选最小的一个，使 T2 在第 100 步训练 rollout 上的 $E$ 密度降幅不小于 T0u。选择只看训练 rollout 的 marker 统计，不看任何准确率，选定后固定。
4. **两种不含答案的开头上下文（主张二）。**
   - I-own：本题 Full Trace 的前 L token，L 为该题轨迹长度的 40%。
   - I-other：按 `length_matched_other_problem.py` 的配对规则选另一题，取它 Full Trace 的前 L token。
   - 用仓库的数学判分器归一化标准答案。若 I-own 中出现本题答案，或 I-other 中出现配对题答案（包括 `\boxed`），就剔除该题；各臂用同一训练子集。
   - 保留率低于 60% 时，把 40% 降到 30%。
   - Full Trace 正文本身会推出答案，所以只去掉仓库拼接的 `\boxed` 后缀是不够的。
5. **描述量（不进判定）。**
   - 训练前 $L_{\text{marg}}$ 占总 KL 的比例。
   - 参考路径拉力：学生给参考解答文本的平均对数概率减去基座的对应值，与 DR 锚点并列报告。

**输出：** 各臂在开思考评测下相对基座的变化、两张判定表的结论、$r$、s、M1/M2、marker 密度、平均长度、撞上限比例。

**与最高近邻的关键差别：**
- **2609.39118**：TH 下有无关解答对照，但单种子；无关解答带着自己的答案、不等长；Qwen3-1.7B 在其设置下不退化；没有任何按认知类的损失干预。本 Idea 在确认退化的配置下，用多种子、等长、双方都不含答案的开头重新检验，并主要贡献认知通道的因果检验。
- **2609.20612**：同代码同设置，但所有内容对照与 marker 排除都只在 DR 下做。
- **2607.05184**：marker 掩码在不带特权信息的 OPD 中进行，按位置。
- **AD-OPSD**：按熵门控，不按认知类。
- **2603.24472**：因果检验在 GRPO 中。
- **Purified OPSD、2608.04794**：分解只作诊断。

## 最小实验

**模型与设置：**
- Qwen3-1.7B，Full Trace 视图。
- 全部沿用 2609.20612 仓库的默认配置：100 步，有效 batch 32，恒定学习率，损失温度 1.1，rollout 温度 1.1，LoRA 秩 64、α 128，覆盖 7 个投影模块，教师冻结并开思考。
- TH 臂统一使用 `ROLLOUTS=thinking TRAIN_MAX_NEW_TOKENS=1024 LOSS_HORIZON=1024`，只改损失项或教师上下文。

**各臂：**
- T0（复现锚点），3 个种子。
- T0u，5 个种子；它同时是两个主张的参照。
- 主张一：T1、T2、T3、T4，各 3 个种子。
- 主张二：I-own、I-other，各 5 个种子。
- DR 锚点，3 个种子；基座直接评测。

共 9 个训练配置，3 × 5 + 6 × 3 = 33 次训练。

**事先检查：**
- 统计答案过滤的保留率。
- 跑 T0、T0u 的种子 0，降幅不足原文一半时停止并报告。
- 用最多 3 次短训练选定 $w$。

**评测：**
- 主指标沿用 2609.20612 的协议：384 题冻结测试切分，开思考，Avg@4，并给出 4k/8k/16k 前缀判分。
- 外部基准 AIME24、AIME25、HMMT25：只评 B、T0u、T1、T2 的种子 0，每题 4 条，上限 38,912。只作描述，不进判定。

**Baseline 与复现入口：**

| 名称 | 与本任务的关系 | 论文 | 代码与复现入口 |
|---|---|---|---|
| TH 训练的 OPSD（T0） | 同任务、同模型、同评测的退化设置，最高近邻 | https://arxiv.org/abs/2609.20612 | https://github.com/xiuyuz/opsd-reference-study （2026-10-28 核验：`training/launch_run.sh`、`training/train_opsd.py`（`apply_loss_horizon`、`--pi-override-file`、`--fork-mask-mode`）、`opsd/opsd_loss.py`（官方 OPSD 前向 KL 与逐元素截断的移植）、`opsd/constants.py`（`CORRECTION_MARKERS`）、`data/controls/truncated_full_trace.py`、`data/controls/length_matched_other_problem.py`、`evaluation/build_eval_queue.py`）；`CONDITION=full_trace ROLLOUTS=thinking TRAIN_MAX_NEW_TOKENS=1024 LOSS_HORIZON=1024 bash training/launch_run.sh` |
| marker 位置损失排除（T4） | 同任务已有的 marker 干预，在 TH 下运行 | 同上 | 同上，加 `EXTRA_ARGS="--fork-mask-mode exclude"` |
| 不含答案的开头上下文（I-own、I-other） | 同上设置，只换教师上下文 | 同上 | 按两个控制脚本的截断与配对规则生成，再做答案过滤，经 `--pi-override-file` 传入 |
| DR 训练的 OPSD | 增益锚点 | 同上 | `CONDITION=full_trace ROLLOUTS=direct bash training/launch_run.sh` |
| 基座 | 参照 | — | `evaluation/build_eval_queue.py --mode thinking` 评测原模型 |

T0u、T1、T2、T3 的损失在 `opsd/opsd_loss.py` 旁新增一个函数实现。

**为什么不用无特权教师作对照：** 在 TH 下，不带参考的教师与学生是同一模型、同一模式、同一上下文，KL 恒为 0。仓库的 `--unprivileged-teacher` 只在 DR 下有意义。

**预算：**
- 该仓库报告每次运行在单张 80GB GPU 上完成，DR 的 100 步约半小时（H100）。我们的 TH 臂生成上限同为 1,024，按 A100 每次约 1.5 小时计，33 次约 50 A100 小时。
- 测试切分评测：每个检查点约 6 A100 小时，约 198 A100 小时。
- 外部基准：4 个检查点 × 3 个任务，每题 4 条，约 96 A100 小时。
- 参考路径拉力、$w$ 选择，约 10 A100 小时。
- 合计约 355 A100 小时，2 张 A100 约 7.5 天。数学题规则判分，不需要付费 API。

**支持结果：** 主张一判为"支持"；主张二判为"支持"。两者都只依据测试切分上的判定表。

**推翻结果：** 两张判定表中的推翻格；"不可识别""非特异""信号太弱""部分""开头不足以造成退化"等各格都作为结论如实报告。

Frozen Problem Anchor and user constraints:

- 根本问题：特权上下文自蒸馏（OPSD）为何让训练时开思考的推理模型在长评测预算下退化？退化来自特权信息语义还是教师上下文分布偏移？失效时长度变短还是变长由什么决定？
- 领域与设置：数学推理；思考模型（Qwen3 系列等）在训练时开思考做 OPSD；OpenThoughts 类数学数据；在 AIME24/25、HMMT25 上评测 avg@k，评测生成预算 4k–38k。
- 必须解决的瓶颈：失效时长度方向冲突未对齐；1-shot OPD 一致有效只在自 RL 教师下测；外推到非数学与异族教师无证据。
- 约束：2×A100 80G；开源模型、LoRA 可接受；付费 API 1000 元以内；半年内投主会。
- 进入实验规划的成功条件：有一个可证伪的 Claim，最小实验能在上述资源内区分本 Idea 与最高近邻。
