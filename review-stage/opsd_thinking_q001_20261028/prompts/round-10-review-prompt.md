You are an independent senior reviewer checking whether a research idea is novel enough
for experiment planning. You are not a co-author and must not redesign the idea.

You are intentionally zero-context. Judge only the current four-part brief, the frozen
Problem Anchor, and the user's constraints. Search the closest prior work yourself; the
author's own literature notes are deliberately withheld. Do not invent papers, links, or results.
Today's date: 2026-10-28. Known tool workarounds: Shell 访问 arxiv.org 与 api.github.com 会被代理拒绝（403）；请用你的 WebSearch/WebFetch 工具读论文（先搜索以获得可抓取的 URL；同一站点连续抓取过快会被限流，请逐页抓取；arxiv 的 PDF 链接（如 arxiv.org/pdf/<id>v1）或 huggingface.co/papers/<id>.md 通常比 HTML 更完整；部分论文有多个版本，请核对最新版本），用 git clone --depth 1 --filter=blob:none --no-checkout 加 git ls-tree / git show 查看仓库文件
Finish all searches before answering and leave no background tasks running. Do not read other
files in this workspace and do not write files, except your raw review to /home/claude/autoresearch/review-stage/opsd_thinking_q001_20261028/round-10-review.md (UTF-8).
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

**一句话定位：** 在策略自蒸馏（OPSD）中，同一模型看到参考解答后充当教师，在学生自己的 rollout 上逐 token 拟合前向 KL。学生 rollout 开着思考（TH）时，OPSD 会让思考模型准确率下降；回复长度有时变短、有时变长。本 Idea 在确认会退化的设置下检验一条分离假说：认知类 token（wait、hmm、maybe 等）的总量这一通道，决定长度朝哪个方向变，但不承载准确率退化。

## 核心 Claim

**现有方法在什么条件下失败。**
- 2609.20612 在同一代码与配置下比较了两种 rollout，评测都开思考。
  - Qwen3-1.7B（基座 80.21）：直接回答式 rollout（DR）训练到第 100 步得 82.62（Full Trace）；TH 训练（损失只覆盖前 1,024 token）只得 72.79。
  - SmolLM3-3B（基座 82.16）：TH 训练在第 50 步的两个种子均值为 77.99。
- 2607.05184 也发现只有训练时开思考才有害：Qwen3-4B 训练开思考得 0.532，关思考 0.590，基座 0.591。

**长度方向在论文之间、甚至同一配置之内都不一致。**
- 2607.05184：OPSD 在长预算下回复变短。
- 2609.39118：TH 下多数教师上下文让评测长度增长。
- 2609.20612 的同一个 TH 配置内也不一致：Full Trace 与 Clean Solution 视图的学生回复变短，Answer Only 视图的学生输出更长、撞上限更多（文中对比对象是 DR 训练臂）。
- 至今没有工作说明长度方向由教师信号的哪一部分决定。

**主流解释把两件事绑在一起，而且在 OPSD 中没有因果证据。**
- 主流解释是认知抑制：知道答案的教师给认知 token 更低的概率，学生于是少犹豫、少核对，回复变短，准确率也下降。这一解释同时预测长度与准确率。
  - 2607.05184 称之为 fork 抑制，作者自认"未被隔离或证明为因果"。
  - 2607.10805（AD-OPSD）报告 Qwen3-1.7B 在学生与教师都开思考时，认知密度从 10.3 降到 7.9。
- 已有的因果证据都不在 OPSD 中：
  - 2603.24472（v4，GRPO 中的因果干预一节）在 GRPO 中惩罚认知 token，结果是推理变短、准确率下降。
  - 2607.05184 附录 E 在不带特权信息的 OPD 中比较"只在 marker 位置计损失"和"在随机位置计损失"，两者无法区分。
- 2609.20612 指出，marker 抑制在 DR（增益）与 TH（损失）下同号，区分不了两种结局；它的 marker 损失排除只在 DR 下做过。

**被忽视的关键：用前向 KL 的类分组恒等式隔离认知通道。** 这一分解形式来自 Decoupled KD（2203.08679），这里推广到认知 token 类 $E$：

$$\mathrm{KL}(\pi_T\|\pi_S)=\underbrace{\mathrm{KL}(\mathrm{Bern}(m_T)\|\mathrm{Bern}(m_S))}_{L_{\text{marg}}}+\underbrace{m_T\,\mathrm{KL}(\pi_T^{E}\|\pi_S^{E})+(1-m_T)\,\mathrm{KL}(\pi_T^{\neg E}\|\pi_S^{\neg E})}_{L_{\text{cond}}}$$

- $m_T$、$m_S$ 是教师、学生在 $E$ 上的总概率；$\pi^{E}$、$\pi^{\neg E}$ 是在 $E$ 内、$E$ 外重新归一的条件分布。
- $L_{\text{marg}}$ 只管"多犹豫还是少犹豫"；$L_{\text{cond}}$ 是其余全部信号，包括停止 token 和内容引导。
- 只用其中一项训练，就能把长度与准确率分别归到两个通道上。

**本 Idea 主张（分离假说）：认知边际通道承载长度方向，不承载准确率退化。**
1. **准确率：认知通道既不必要也不充分。**
   - 只用 $L_{\text{cond}}$ 训练，仍复现大部分准确率下降。
   - 只用剂量匹配的 $L_{\text{marg}}$ 训练，$E$ 密度的变化与完整 KL 相当，但准确率不显著下降。
   - 主结果在 Qwen3-1.7B 上判定，并在 SmolLM3-3B 上复现。
2. **长度：方向由认知边际通道承载。** 在长度方向相反的两种参考视图（Full Trace、Answer Only）下，只用 $L_{\text{marg}}$ 都能复现完整 KL 的长度变化方向和至少一半的幅度；只用 $L_{\text{cond}}$ 都不能。
3. **（次）轨迹形式的前缀偏移即足以造成退化。**
   - 2609.39118 表 4（学生与教师都开思考，上限 1,024，单种子）中：
     - Qwen3-1.7B 只在轨迹形式的上下文（OpenThoughts CoT 加标准解答）下退化，34.0 → 30.8；完整解答 +1.3，无关解答 +3.1。
     - OLMo-3-7B-Think 下，无关解答 −6.0 与完整解答 −4.7 相当。作者据此读作前缀分布效应。
   - 本 Idea 在确认退化的 Qwen3-1.7B 配置下检验：两种轨迹形式的开头造成相当的退化，CI 落在 ±δ 内。一种是本题轨迹开头（I-own），另一种是等长的他题轨迹开头（I-other），两者都不含任何答案。

**统计与判定（事先固定，穷尽）**

- **统计方法：** 采用两级 bootstrap。外层在每个臂内对种子有放回重采样，内层在选中的种子内按题目重采样；跨臂比较时按题目配对。基座 B 没有训练，只做题目重采样。这样种子间的训练方差会进入 CI。凡涉及等价判定的臂，都用 5 个种子。
- **等价界 δ：** 取 T0u 准确率降幅点估计的 25%，且不小于 1 分；在 T0u 全部种子跑完、其他臂评测之前算定。
- **事先检查：** T0（官方截断目标）与 T0u（未截断）都相对 B 显著下降，且降幅不小于原文的一半（Qwen3-1.7B 为 −7.4 的一半，SmolLM3-3B 为 −4.2 的一半）。不满足的模型，其后续判定作废并如实报告。

**主张一（准确率）**

记号：
- T1 只用 $L_{\text{cond}}$。
- T2 只用 $wL_{\text{marg}}$。
- T3 与 T1 相同，但 $E$ 换成频率匹配的随机类。
- 挽回比例 $r=(T1-T0u)/(B-T0u)$。

两项操纵检查：
- M1：T1 的短语级广义认知密度与 B 相差不超过 ±10%。
- M2：T2 的 $E$ 密度变化与 T0u 同向，幅度不小于 T0u 的一半。

| 结果 | 判定 |
|---|---|
| $r$ 的 CI 上界 < 0.25 且 M1 通过；M2 通过且 T2 − B 的 CI 下界 > −δ | 支持主张一 |
| $r$ 的 CI 上界 < 0.25 但 M1 未通过 | 不可识别：认知抑制泄漏到 $E$ 之外 |
| M2 通过且 T2 − B 的 CI 上界 < 0 | 推翻"不充分" |
| $r$ 的 CI 下界 ≥ 0.5 且 T1 − T3 的 CI 下界 > 0 | 推翻"不必要" |
| $r$ 的 CI 下界 ≥ 0.5 但 T1 − T3 的 CI 含 0 | 非特异 |
| M2 未通过 | T2 信号太弱，充分性不可检验 |
| 其余 | 两项都有贡献，报告 $r$ 与 T2 − B |

主判定用 Qwen3-1.7B；SmolLM3-3B 上做同一判定，作为复现报告。另报告 T1 − T4，不进判定，其中 T4 是 TH 下的 marker 位置损失排除。

**主张二（长度）**

- 记 $\ell(X)$ 为臂 X 在开思考评测下平均回复长度相对 B 的变化。
- 前提：在 Full Trace 与 Answer Only 两种视图下，T0u 的长度变化都显著（CI 不含 0）。只在满足前提的视图上判定；若两种视图都满足且方向相同，照常判定并如实报告"未出现方向翻转"。

| 结果（在所有满足前提的视图上都成立） | 判定 |
|---|---|
| $\ell(T2)/\ell(T0u)$ 的 CI 下界 ≥ 0.5，且 $\ell(T1)/\ell(T0u)$ 的 CI 上界 < 0.5 | 支持主张二：长度由认知边际通道承载 |
| $\ell(T1)/\ell(T0u)$ 的 CI 下界 ≥ 0.5，且 $\ell(T2)/\ell(T0u)$ 的 CI 上界 < 0.5 | 推翻：长度由条件项承载（报告停止 token 质量变化作描述） |
| 其余 | 两通道都参与，报告比值与 CI |

**主张三（前缀偏移）**

| 结果 | 判定 |
|---|---|
| ΔI-own 与 ΔI-other 的 CI 上界都 < 0，且 I-other − I-own 的 CI 落在 ±δ 内 | 支持主张三 |
| ΔI-own 的 CI 上界 < 0，ΔI-other 的 CI 下界 > −δ，且 I-other − I-own 的 CI 下界 > 0 | 推翻：退化需要本题信息 |
| ΔI-own 与 ΔI-other 都不显著为负 | 不含答案的开头不足以造成退化，报告 T0u − I-own |
| 其余 | 部分：报告 s = ΔI-other / ΔI-own 及其 CI |

## 方法设计的核心思想

**输入：**
- **模型：** Qwen3-1.7B 与 SmolLM3-3B。这两个骨干在 2609.20612 的同一份代码中都报告过 TH 退化，冻结切分已随仓库提供。Qwen3-1.7B 采用该文的配置，因为在 2609.39118 的配置（学习率 1e-6）下，它只在轨迹形式的上下文中退化。
- **参考视图：** 2609.20612 的 AMPLE-Math 中的 Full Trace 与 Answer Only；教师冻结，开思考。
- **认知类 $E$：** 以下来源的并集——2609.20612 的 11 个 marker、2603.24472 的 10 个认知词，以及 hmm、alternatively、recall。
  - 取大小写与带空格的整词单 token。
  - 多 token 词只取首子词，且要求该子词在初始学生 rollout 中超过一半的出现属于这些词。
  - 每个模型的分词器各自按同一规则构建，规则与列表在训练前固定。
- **随机类：** 总概率与 $E$ 相差 20% 以内的整词单 token 普通词，排除认知词、数字与数学符号，用固定种子抽取。

**实际动作：**
1. **低成本复现 TH。** 仓库 `train_opsd.py` 中的 `apply_loss_horizon` 只截取前 1,024 个补全 token。所以把生成上限设为 1,024 时，损失的分布与原文 TH 训练相同。
2. **按项构造损失。** 每个位置由教师与学生的 logits 直接算出 $L_{\text{marg}}$ 与 $L_{\text{cond}}$，$m_T$ 当作常数。T0u、T1、T2、T3 都不做逐项截断，因此 T0u 精确等于两项之和。官方截断目标 T0 只作复现锚点。
3. **T2 的剂量匹配（每个模型 × 视图各选一次）。**
   - 从 $w\in\{1,10,100\}$ 中选最小的一个，使 T2 在训练 rollout 末段的 $E$ 密度变化与 T0u 同向，且幅度不小于 T0u。
   - 选择只看训练 rollout 的 marker 统计，不看准确率或评测长度；选定后固定。
4. **两种不含答案的轨迹开头（主张三，只用 Qwen3-1.7B、Full Trace）。**
   - I-own：本题 Full Trace 的前 40% token。
   - I-other：按 `length_matched_other_problem.py` 的配对规则选另一题，取它 Full Trace 的同长开头。
   - 用仓库的数学判分器归一化标准答案，剔除文本中出现本题答案或配对题答案的题目；各臂使用同一训练子集。保留率低于 60% 时，把 40% 降到 30%。
5. **描述量（不进判定）：**
   - 训练前 $L_{\text{marg}}$ 占总 KL 的比例。
   - 各臂停止 token（`</think>`、EOS）的平均概率变化。
   - 参考路径拉力，与 DR 锚点并列。

**输出：** 三张判定表的结论；$r$、s、长度比值、M1/M2；各臂的 marker 密度、平均长度、撞上限比例。

**与最高近邻的关键差别：**
- **2609.20612：** 同代码同设置，但所有内容对照与 marker 排除都只在 DR 下做，长度方向只作观察。
- **2609.39118：** TH 下的上下文对照只有单种子，无关解答带答案、长度不匹配，也没有任何按类的损失干预。
- **2607.05184：** marker 掩码在不带特权信息的 OPD 中按位置进行。
- **AD-OPSD：** 按熵门控，不按认知类。
- **2603.24472：** 因果检验在 GRPO 中。
- **Purified OPSD、2608.04794：** 分解只作诊断。
- **本 Idea：** 在退化的 TH-OPSD 中，用按类的"只保留一项"干预，把长度方向与准确率退化分别归到不同通道。

## 最小实验

**训练配置：** 全部沿用 2609.20612 仓库默认值：
- 有效 batch 32，恒定学习率，损失温度 1.1，rollout 温度 1.1；
- LoRA 秩 64、α 128，作用于 7 个投影模块；教师冻结且开思考。
- 步数：Qwen3-1.7B 训练 100 步，SmolLM3-3B 训练 50 步，即原文报告各自 TH 退化的检查点。
- TH 臂统一用 `ROLLOUTS=thinking TRAIN_MAX_NEW_TOKENS=1024 LOSS_HORIZON=1024`，臂间只改损失项或教师上下文。

**各臂：**
- **Qwen3-1.7B、Full Trace：**
  - T0：3 个种子。
  - T0u、T1、T2：各 5 个种子。
  - T3、T4：各 3 个种子。
  - I-own、I-other：各 5 个种子。
  - DR 锚点：3 个种子。
  - 合计 37 次。
- **Qwen3-1.7B、Answer Only（主张二）：** T0u、T1、T2 各 3 个种子，共 9 次。
- **SmolLM3-3B、Full Trace（主张一复现）：** T0u、T1、T2 各 3 个种子，共 9 次。
- 基座直接评测。
- 总计 55 次训练。

**事先检查：**
- 统计答案过滤后的保留率。
- 各模型先跑 T0 与 T0u 的种子 0；降幅不足原文一半的模型停止，并如实报告。
- 每个"模型 × 视图"用最多 3 次短训练选定 $w$。

**评测：**
- 主指标沿用 2609.20612 的协议：冻结测试切分，开思考，Avg@4，并给出 4k/8k/16k 前缀判分与平均长度。
- 外部基准 AIME24、AIME25、HMMT25：只评 Qwen3-1.7B 的 B、T0u、T1、T2 的种子 0，每题 4 条，上限 38,912。只作描述，不进判定。

**Baseline 与复现入口：**

| 名称 | 与本任务的关系 | 论文 | 代码与复现入口 |
|---|---|---|---|
| TH 训练的 OPSD（T0） | 同任务、同模型、同评测的退化设置，最高近邻 | https://arxiv.org/abs/2609.20612 | https://github.com/xiuyuz/opsd-reference-study （2026-10-28 核验：`training/launch_run.sh`、`training/train_opsd.py`（`apply_loss_horizon`、`--pi-override-file`、`--fork-mask-mode`）、`opsd/opsd_loss.py`（官方 OPSD 前向 KL 与逐元素截断的移植）、`opsd/constants.py`（`CORRECTION_MARKERS`）、`data/controls/truncated_full_trace.py`、`data/controls/length_matched_other_problem.py`、`data/splits/{qwen3_1p7b,smollm3_3b}_splits.json`、`configs/experiments.md`、`evaluation/build_eval_queue.py`）；`CONDITION=full_trace ROLLOUTS=thinking TRAIN_MAX_NEW_TOKENS=1024 LOSS_HORIZON=1024 bash training/launch_run.sh`；SmolLM3 用 `MODEL=HuggingFaceTB/SmolLM3-3B` 及其切分文件 |
| Answer Only 视图的 TH 训练 | 同设置下长度方向相反的视图 | 同上 | `CONDITION=answer_only`，其余同上 |
| marker 位置损失排除（T4） | 同任务已有的 marker 干预，在 TH 下运行 | 同上 | 加 `EXTRA_ARGS="--fork-mask-mode exclude"` |
| 不含答案的开头上下文 | 只换教师上下文 | 同上 | 按两个控制脚本的截断与配对规则生成，再做答案过滤，经 `--pi-override-file` 传入 |
| DR 训练的 OPSD | 增益锚点 | 同上 | `ROLLOUTS=direct` |
| 基座 | 参照 | — | `evaluation/build_eval_queue.py --mode thinking` 评测原模型 |

T0u、T1、T2、T3 的损失在 `opsd/opsd_loss.py` 旁新增一个函数实现。

**为什么不用无特权教师作对照：** 在 TH 下，不带参考的教师与学生是同一模型、同一模式、同一上下文，KL 恒为 0。仓库的 `--unprivileged-teacher` 只在 DR 下有意义。

**预算：**
- **训练：** 仓库报告每次运行都能在单张 80GB GPU 上完成，DR 的 100 步约半小时（H100）。我们的 TH 臂生成上限同为 1,024，按 A100 每次约 1.5 小时计（SmolLM3 步数减半、模型约大一倍，按同样时长计），55 次约 83 A100 小时。$w$ 选择约 12 次短训练，约 10 A100 小时。
- **测试切分评测：** 每个检查点约 6 A100 小时，约 330 A100 小时。
- **外部基准：** 4 个检查点 × 3 个任务，每题 4 条，约 96 A100 小时。
- **合计：** 约 520 A100 小时，2 张 A100 约 11 天。数学题规则判分，不需要付费 API。

**支持结果：** 主张一在 Qwen3-1.7B 上判为"支持"，并在 SmolLM3-3B 上同向；主张二判为"支持"。两者合起来就是分离假说成立：认知边际通道决定长度方向，但不承载准确率退化。主张三单独报告。所有判定都只依据测试切分上的判定表。

**推翻结果：** 各判定表的推翻格。"不可识别""非特异""信号太弱""两通道都参与""部分"等格也都作为结论如实报告。

Frozen Problem Anchor and user constraints:

- 根本问题：特权上下文自蒸馏（OPSD）为何让训练时开思考的推理模型在长评测预算下退化？退化来自特权信息语义还是教师上下文分布偏移？失效时长度变短还是变长由什么决定？
- 领域与设置：数学推理；思考模型（Qwen3 系列等）在训练时开思考做 OPSD；OpenThoughts 类数学数据；在 AIME24/25、HMMT25 上评测 avg@k，评测生成预算 4k–38k。
- 必须解决的瓶颈：失效时长度方向冲突未对齐；1-shot OPD 一致有效只在自 RL 教师下测；外推到非数学与异族教师无证据。
- 约束：2×A100 80G；开源模型、LoRA 可接受；付费 API 1000 元以内；半年内投主会。
- 进入实验规划的成功条件：有一个可证伪的 Claim，最小实验能在上述资源内区分本 Idea 与最高近邻。
