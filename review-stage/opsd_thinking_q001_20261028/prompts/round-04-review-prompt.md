You are an independent senior reviewer checking whether a research idea is novel enough
for experiment planning. You are not a co-author and must not redesign the idea.

You are intentionally zero-context. Judge only the current four-part brief, the frozen
Problem Anchor, and the user's constraints. Search the closest prior work yourself; the
author's own literature notes are deliberately withheld. Do not invent papers, links, or results.
Today's date: 2026-10-28. Known tool workarounds: Shell 访问 arxiv.org 与 api.github.com 会被代理拒绝（403）；请用你的 WebSearch/WebFetch 工具读论文（先搜索以获得可抓取的 URL；同一站点连续抓取过快会被限流，请逐页抓取；arxiv 的 PDF 链接通常比 HTML 更完整；部分论文有多个版本，引用时请核对最新版本，例如 alphaxiv 页面会显示版本号），用 git clone --depth 1 --filter=blob:none --no-checkout 加 git ls-tree / git show 查看仓库文件
Finish all searches before answering and leave no background tasks running. Do not read other
files in this workspace and do not write files, except your raw review to /home/claude/autoresearch/review-stage/opsd_thinking_q001_20261028/round-04-review.md (UTF-8).
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

**一句话定位：** 在策略自蒸馏（OPSD）中，同一模型看到参考解答后充当教师，在学生自己的 rollout 上按逐 token 前向 KL 拟合。学生 rollout 开着思考时，OPSD 会让思考模型退化。本 Idea 检验这一退化由教师信号的哪一部分承载：是"认知类 token 总量被压低"，还是"认知总量之外、朝参考解答路径的引导"。

## 核心 Claim

**现有方法在什么条件下失败。**
- 2609.20612 在 Qwen3-1.7B 上用同一参考视图和同一配置做了对比（评测都开思考，基座 80.21）：
  - 直接回答式 rollout（DR）训练到第 100 步得 82.62（Full Trace）；
  - 开思考 rollout（TH，损失只覆盖前 1,024 token）只得 72.79。
- 2607.05184 也发现只有训练时开思考才有害：Qwen3-4B 训练开思考 0.532、关思考 0.590，基座 0.591。

**两种竞争解释，以及在 OPSD 中缺失的因果检验。**
- **认知抑制。** 知道答案的教师给 wait、hmm、maybe 等更低的概率，学生因此少犹豫、少核对。
  - 证据：2607.05184 称之为 fork 抑制，作者自认"未被隔离或证明为因果"；2607.10805 报告认知 token 密度从 10.3 降到 7.9。
  - 2603.24472（v4，"A Causal Intervention" 一节）在 GRPO 中把认知 token 位置的优势截到 −κ（κ=0.5），复现了下降与推理变短。但那是 RL 中的充分性检验，不是 OPSD。
  - 反证：2609.20612 发现 marker 抑制在 DR（增益）与 TH（损失）中同号，所以它区分不了两种结局；该文在 DR 下排除 marker 位置的损失，marker 使用的变化不超过 1.1%。另外，加入参考解答后，marker 类的边际概率只从 0.00928 降到 0.00853（2607.05184 附录 E）。
- **参考路径引导。**
  - Purified OPSD（2607.02234）把教师更新拆成参考诱导分量与可迁移分量，认为前者是"死记参考的推理路径"。
  - 2608.04794 定义了 PI 偏差分数，即教师相对学生对上下文中那条解答的对数概率差：对上下文中的解答为 0.52，对另一条正确解答至多 0.02。
  - 这两篇都是观察性的，没有在 TH-OPSD 中做"只保留某一部分信号"的因果干预。

**被忽视的关键：用前向 KL 的类分组恒等式把两种解释分开。** 这一分解形式来自 Decoupled KD（2203.08679）的目标类/非目标类分解。记 $E$ 为认知 token 类，$m_T$、$m_S$ 为教师、学生在 $E$ 上的总概率，每个位置有

$$\mathrm{KL}(\pi_T\|\pi_S)=\underbrace{\mathrm{KL}(\mathrm{Bern}(m_T)\|\mathrm{Bern}(m_S))}_{L_{\text{marg}}}+\underbrace{m_T\,\mathrm{KL}(\pi_T^{E}\|\pi_S^{E})+(1-m_T)\,\mathrm{KL}(\pi_T^{\neg E}\|\pi_S^{\neg E})}_{L_{\text{cond}}}$$

- $\pi^{E}$ 与 $\pi^{\neg E}$ 分别是在 $E$ 内、$E$ 外重新归一的条件分布。
- $L_{\text{marg}}$ 只管"多犹豫还是少犹豫"；$L_{\text{cond}}$ 管"在同样多的犹豫下往哪里走"，其中包含朝参考路径的引导。
- 只用其中一项训练，就能分别检验两种解释的必要性与充分性。

**本 Idea 主张：** 在 TH 训练的 OPSD 中，退化主要由 $L_{\text{cond}}$ 承载，并伴随学生向参考解答路径靠拢；$L_{\text{marg}}$ 单独训练时不造成显著下降。这一主张只有在下面的操纵检查通过后才成立。

**结果如何判定（事先固定，穷尽）**

记号：
- T0u：未截断的完整前向 KL，等于 $L_{\text{marg}}+L_{\text{cond}}$。
- T1：只用 $L_{\text{cond}}$。
- T2：只用 $L_{\text{marg}}$。
- T3：同 T1，但把 $E$ 换成频率匹配的随机类。
- B：基座。
- 挽回比例 $r=(T1-T0u)/(B-T0u)$。
- 差值都用按题目配对、跨 3 个种子重采样的 bootstrap 求 95% CI。

两项操纵检查，都在评测 rollout 上测：
- **(M1)** T1 的广义认知密度与 B 相差不超过 ±10%。广义认知密度用一个比 $E$ 更宽的短语级正则统计，包括 "let me (check|verify|double-check|recheck|reconsider)"、"hold on"、"on second thought" 等多词短语。
- **(M2)** T2 的 $E$ 密度变化不小于 T0u 的一半，用来确认 T2 确实携带了边际信号。

| 结果 | 判定 |
|---|---|
| 事先检查中 T0（官方截断目标）相对 B 的下降不足原文 −7.4 的一半，或 T0u 的下降不显著 | 未复现，后续判定作废 |
| $r$ 的 CI 上界 < 0.25；T2 − B 的 CI 下界 > −1 分；M1、M2 都通过；T1 的参考路径拉力显著 > 0，T2 的不显著 | 支持 H-content |
| $r$ 的 CI 上界 < 0.25，但 M1 未通过 | 不可识别：认知抑制泄漏到 $E$ 之外，不支持任一机制 |
| $r$ 的 CI 上界 < 0.25，T2 − B 的 CI 下界 > −1，但 M2 未通过 | T2 的边际信号太弱，充分性不可检验，只报告必要性结果 |
| $r$ 的 CI 下界 ≥ 0.5，T1 − T3 的 CI 下界 > 0，T2 − B 的 CI 上界 < 0 | 支持 H-marker，主张被推翻 |
| $r$ 的 CI 下界 ≥ 0.5，但 T1 − T3 的 CI 含 0 | 非特异：改动任何小类边际都会改变训练，两种机制都不支持 |
| 其余 | 两项都有贡献：报告 $r$、T2 − B 与参考路径拉力 |

参考路径拉力：在留出的开发切分题上，学生在不看参考时给参考解答文本的平均每 token 对数概率，减去基座的对应值。它对应 2608.04794 的 PI 偏差，只是测在训练后的学生上。

## 方法设计的核心思想

**输入：**
- Qwen3-1.7B；2609.20612 的 AMPLE-Math 冻结切分；Full Trace 参考视图；开思考的冻结教师。
- $E$ 的构成：
  - 三份已发表词表的并集：2609.20612 的 11 个 marker、2603.24472 的 10 个认知词、2607.05184 表 5 统计的 hmm，另加 alternatively、recall；
  - 取各大小写与带空格的整词单 token 变体；
  - 对多 token 词，取首个子词，但只在该子词在初始学生 rollout 中超过一半的出现都属于这些认知词时才纳入（例如 "altern"）。
  - 构建规则与最终列表在训练前固定。
- 随机类 $R$：整词单 token 普通词，平均总概率与 $E$ 相差 20% 以内，排除认知词、数字和数学符号，用固定种子抽取。

**实际动作：**
1. **低成本复现 TH。** 仓库 `train_opsd.py` 中的 `apply_loss_horizon` 只截取前 1,024 个补全 token，不使用之后的内容。所以生成上限设为 1,024 时，损失与原文 20,764 上限的 TH 训练相同。
2. **按项构造损失。** 每个位置由教师和学生的 logits 直接算出 $L_{\text{marg}}$ 与 $L_{\text{cond}}$。$m_T$ 为常数，学生侧保留梯度。T0u、T1、T2、T3 分别优化"两项之和""只有条件项""只有边际项""随机类上的条件项"。这些都不加逐项截断，所以 T0u 精确等于两项之和。官方的截断目标 T0 只作为复现锚点。
3. **现有干预作次要对照（T4）。** 在 TH 下使用 2609.20612 的 `--fork-mask-mode exclude`。
4. **训练前描述量。** 在初始 TH rollout 上统计 $L_{\text{marg}}$ 占总 KL 的比例。

**输出：** 各臂在开思考评测下相对基座的变化、$r$、M1/M2 两项检查、参考路径拉力、marker 密度、平均长度、撞上限的比例。

**与最高近邻的关键差别：**
- 2609.20612：marker 干预只在 DR 下做，TH 只改参考视图与损失窗口。
- 2607.05184：只在不带特权信息的 OPD 中比较 marker 位置与随机位置的损失。
- Purified OPSD、2608.04794：按"是否参考诱导"做观察或修正，不分离认知总量，也没有只保留一项的因果检验。
- 2603.24472：干预在 GRPO 中，不是 OPSD。
- 本 Idea 在真正退化的 TH 设置中，用 DKD 式的精确分解，对两种机制分别做"只保留一项"的干预，配随机类对照、操纵检查和参考路径拉力这一正向指标。

## 最小实验

**模型与设置：** Qwen3-1.7B，Full Trace 视图。在这个模型、这套代码与配置下，TH 下降已有报告（2609.20612 表 11）。训练全部沿用该仓库默认配置：100 步，有效 batch 32，恒定学习率，损失温度 1.1，rollout 温度 1.1，LoRA 秩 64、α 128 覆盖 7 个投影模块，教师冻结并开思考。

TH 臂统一使用 `ROLLOUTS=thinking TRAIN_MAX_NEW_TOKENS=1024 LOSS_HORIZON=1024`，被监督的 token 完全相同，只改损失项。

**各臂（每臂 3 个种子）：**
- T0（官方截断目标，复现锚点）、T0u、T1、T2、T3、T4；
- DR 锚点（原文配方）；
- 基座直接评测。

共 7 个训练配置 × 3 = 21 次。

**事先检查：** 先跑 T0 与 T0u 的种子 0。任一臂的下降不足原文一半就停下来报告。

**评测：**
- 主指标：沿用 2609.20612 的协议，在 384 题冻结测试切分上做开思考评测，Avg@4，并给出 4k/8k/16k 前缀判分。
- 参考路径拉力在开发切分上测。
- 外部基准：AIME24、AIME25、HMMT25，只评 B、T0u、T1、T2 的种子 0，每题 4 条，上限 38,912。

**Baseline 与复现入口：**

| 名称 | 与本任务的关系 | 论文 | 代码与复现入口 |
|---|---|---|---|
| TH 训练的 OPSD（T0） | 同任务、同模型、同评测的退化设置，最高近邻 | https://arxiv.org/abs/2609.20612 | https://github.com/xiuyuz/opsd-reference-study （2026-10-28 核验：`training/launch_run.sh`、`training/train_opsd.py`（`apply_loss_horizon`、`--fork-mask-mode`）、`opsd/opsd_loss.py`（官方 OPSD 前向 KL 与逐元素截断的移植）、`opsd/constants.py`（`CORRECTION_MARKERS`）、`configs/experiments.md`、`evaluation/build_eval_queue.py`）；`CONDITION=full_trace ROLLOUTS=thinking TRAIN_MAX_NEW_TOKENS=1024 LOSS_HORIZON=1024 bash training/launch_run.sh` |
| marker 位置损失排除（T4） | 同任务已有的 marker 干预 | 同上 | 同上，加 `EXTRA_ARGS="--fork-mask-mode exclude"` |
| DR 训练的 OPSD | 增益锚点 | 同上 | `CONDITION=full_trace ROLLOUTS=direct bash training/launch_run.sh` |
| 基座 | 参照 | — | `evaluation/build_eval_queue.py --mode thinking` 评测原模型 |

T0u、T1、T2、T3 的损失在 `opsd/opsd_loss.py` 旁边新增一个函数实现，约几十行。

**为什么不用无特权教师作对照：** 在 TH 下，不带参考的教师与学生是同一模型、同一模式、同一上下文，KL 恒为 0。仓库的 `--unprivileged-teacher` 只在 DR 下有意义。

**预算：**
- 该仓库报告每次运行在单张 80GB GPU 上完成，DR 的 100 步约半小时（H100）。我们的 TH 臂生成上限同为 1,024，按 A100 每次约 1.5 小时计，21 次约 32 A100 小时。
- 测试切分评测：每个检查点 2–4 H100 GPU 小时，按 A100 约 6 小时计，约 126 A100 小时。
- 外部基准：4 个检查点 × 3 个任务，每题 4 条，约 96 A100 小时。
- 参考路径拉力只需前向，约 5 A100 小时。
- 合计约 260 A100 小时，2 张 A100 约 5.5 天。数学题规则判分，不需要付费 API。

**支持结果：** 判定为"支持 H-content"，且外部基准上 T1 与 T0u 同样低于基座，T2 不低于基座。

**推翻结果：** 判定为"支持 H-marker"。"不可识别""非特异""T2 太弱""两项都有贡献"各格都作为结论如实报告。

Frozen Problem Anchor and user constraints:

- 根本问题：特权上下文自蒸馏（OPSD）为何让训练时开思考的推理模型在长评测预算下退化？退化来自特权信息语义还是教师上下文分布偏移？失效时长度变短还是变长由什么决定？
- 领域与设置：数学推理；思考模型（Qwen3 系列等）在训练时开思考做 OPSD；OpenThoughts 类数学数据；在 AIME24/25、HMMT25 上评测 avg@k，评测生成预算 4k–38k。
- 必须解决的瓶颈：失效时长度方向冲突未对齐；1-shot OPD 一致有效只在自 RL 教师下测；外推到非数学与异族教师无证据。
- 约束：2×A100 80G；开源模型、LoRA 可接受；付费 API 1000 元以内；半年内投主会。
- 进入实验规划的成功条件：有一个可证伪的 Claim，最小实验能在上述资源内区分本 Idea 与最高近邻。
