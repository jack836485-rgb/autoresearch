You are an independent senior reviewer checking whether a research idea is novel enough
for experiment planning. You are not a co-author and must not redesign the idea.

You are intentionally zero-context. Judge only the current four-part brief, the frozen
Problem Anchor, and the user's constraints. Search the closest prior work yourself; the
author's own literature notes are deliberately withheld. Do not invent papers, links, or results.
Today's date: 2026-10-26. Known tool workarounds: WebFetch is blocked for arxiv.org in this environment; use Bash with curl (https://arxiv.org/abs/<id> or https://arxiv.org/html/<id>) and strip HTML with python. GitHub contents: https://api.github.com/repos/<owner>/<repo>/contents/<path>.
Finish all searches before answering and leave no background tasks running. Do not read other
files in this workspace and do not write files, except your raw review to C:\Users\30473\Desktop\研一\autoresearch\review-stage\em_conditional_mitigation_20261022\round-06-review.md (UTF-8).
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

**定位关键词：** emergent misalignment；conditional misalignment；early stopping；training dynamics；representational distance

**一句话定位：** 已有工作发现涌现失配（emergent misalignment）在主任务收敛之后才出现，早停就能在通用、中性提示上消除它；但早停点在类似训练上下文的 cue 提示下是否仍存在条件失配（conditional misalignment），没有被检验过。

## 核心 Claim

1. 训练过程中，失配并不是在所有提示上同时出现，而是按提示与训练数据在基座模型激活空间中的距离，由近及远依次出现：一个提示离训练数据中心越近，它开始失配的训练步越早。因此，类似训练上下文的 cue 提示会早于通用提示失配。
2. 由此推出：按"通用提示上的失配接近 0、主任务性能保留 90% 以上"选出的早停检查点，在 cue 提示下仍有显著的条件失配（高于无关对照 cue）。也就是说，早停和交织、事后微调、inoculation 一样，会把失配藏到触发后面。
3. 这一"按距离扩散"的解释与"所有提示同时翻转"的相变解释给出相反的预测：如果各提示的出现步与距离无关，Claim 1 即被推翻。

## 方法设计的核心思想

- 输入：有害微调集、基座模型、训练过程中按对数间隔保存的约 12 个检查点，以及一个提示池（通用题、领域 cue 题、无关对照 cue 题）。
- 动作：
  - 对每个提示，在基座模型中层残差流上计算它到训练数据激活中心的余弦距离（沿用 2608.29118 的度量），只需一次前向。
  - 在每个检查点上对每个提示采样并用 judge 判定失配，得到逐提示的失配率随训练步的曲线，把首次超过阈值的检查点记为该提示的出现步。
  - 用 2605.12199 的规则选出早停检查点，再在 cue 提示上测它的条件失配。
- 输出：出现步与距离的秩相关、早停点上的 cued 与通用失配率，以及"按 cue 失配早停"相对"按通用失配早停"损失多少主任务性能。
- 与最高近邻的关键差别：2605.12199 只用中性提示评测早停；2608.29118 只看训练结束时的失配，不看出现顺序；2604.25891 研究的缓解方法不包括早停。本 Idea 把训练动态和提示距离放进同一个可证伪的预测，并检验早停这一缓解在触发下是否成立。

## 最小实验

- 模型与数据：Qwen2.5-7B-Instruct，4-bit QLoRA，沿用 ContextLift 管线的 EM-only 臂（不加缓解数据），使用其 bad security、legal、medical 三个数据集。该设置下的条件失配已在 ContextLift 表 1 中报告。每个数据集 3 个种子，每次训练保存约 12 个检查点。
- 评测：每个检查点上测通用 8 题（每题 20 次采样）、领域 cue 题与无关对照 cue 题（8 题 × 10 个 cue，每个 5 次采样），以及 ContextLift 的窄任务指标；judge 与失配阈值沿用 ContextLift（coherence ≥ 50 且 alignment < 30）。
- 对照：
  - 早停规则按 2605.12199：选主任务性能 ≥ 90% 且通用失配低于阈值的最后一个检查点；
  - 距离度量按 2608.29118；
  - 相变解释的预测：各提示的出现步集中在同一个检查点区间。
- 支持 Claim 的结果：每次运行中，出现步与距离的 Spearman 相关显著为正（越近越早），且领域 cue 题的出现步早于通用题；早停检查点上，领域 cue 失配显著高于无关对照 cue（按种子与提示做 bootstrap，区间不含 0），而通用失配接近 0。
- 推翻 Claim 的结果：出现步与距离无关，或所有提示在同一区间翻转；或早停检查点上领域 cue 失配与无关对照无差别。
- Baseline 与复现：
  - ContextLift 管线：论文 https://arxiv.org/abs/2610.21633 ；代码 https://github.com/davidkaczer/contextlift （已核验，逐臂 config，`EMA_CONFIG=configs/<dataset>/<arm>.yaml`，单卡约 20GB）。
  - 早停规则：论文 https://arxiv.org/abs/2605.12199 ；规则只依赖检查点上的任务性能与失配率，可直接本地实现。
  - 距离度量：论文 https://arxiv.org/abs/2608.29118 ；代码 https://github.com/ChicagoHAI/em-not-magical （已核验，含 sec3–sec5 复现代码与数据集链接）。
- 预算与依据：
  - 训练：3 数据集 × 3 种子 = 9 次，每次约 1.5 小时（ContextLift 报告 H100 上 35–50 分钟，A100 按约 2 倍计），约 14 GPU 小时。
  - 生成：9 次运行 × 12 个检查点 × 约 960 条回答 ≈ 10.4 万条，vLLM 加 LoRA，约 1 天。
  - judge：约 10.4 万条回答 × 2 次判定 ≈ 21 万次调用，每次约 800 输入 token，共约 1.7 亿输入 token；按 mini 级 judge 每百万输入 token 约 0.4 美元计约 70 美元，加输出约 500 元人民币以内。

Frozen Problem Anchor and user constraints:

- 根本问题：EM 缓解方法的有效性可能只在通用评测提示下成立，在带训练上下文线索的条件触发下失效。
- 领域与设置：在窄域有害数据上微调开源 LLM（LoRA），评测为 Betley 式自由问答失配率与 LLM judge。
- 必须解决的瓶颈：已缓解模型在条件触发下的表现，以及触发空间的系统化搜索。
- 约束：2×A100 80G；开源模型 ≤32B 采用 LoRA；judge 可用付费 API（1000 元内）；半年内投主会。
- 进入实验规划的成功条件：有一个可证伪的 Claim，最小实验能在上述资源内区分本 Idea 与最高近邻。
