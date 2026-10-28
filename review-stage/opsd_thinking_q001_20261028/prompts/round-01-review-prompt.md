You are an independent senior reviewer checking whether a research idea is novel enough
for experiment planning. You are not a co-author and must not redesign the idea.

You are intentionally zero-context. Judge only the current four-part brief, the frozen
Problem Anchor, and the user's constraints. Search the closest prior work yourself; the
author's own literature notes are deliberately withheld. Do not invent papers, links, or results.
Today's date: 2026-10-28. Known tool workarounds: Shell 访问 arxiv.org 与 api.github.com 会被代理拒绝（403）；请用你的 WebSearch/WebFetch 工具读论文（先搜索以获得可抓取的 URL；同一站点连续抓取过快会被限流，请逐页抓取），用 git clone --depth 1 --filter=blob:none --no-checkout 加 git ls-tree / git show 查看仓库文件
Finish all searches before answering and leave no background tasks running. Do not read other
files in this workspace and do not write files, except your raw review to /home/claude/autoresearch/review-stage/opsd_thinking_q001_20261028/round-01-review.md (UTF-8).
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

**定位关键词：** on-policy self-distillation；privileged information；thinking models；epistemic tokens；response length

**一句话定位：** 在策略自蒸馏（OPSD）让同一模型在看到参考解答等特权上下文时充当教师，并在学生自己的 rollout 上逐 token 拟合教师。它会改变思考模型的认知类 token（wait、hmm、maybe 等）和回复长度，但改变的方向在不同论文之间、甚至同一模型上相互矛盾。

## 核心 Claim

**现有方法在什么条件下失败。**
- **Qwen3 上是压低方向。** 训练时开思考的 Qwen3 经 OPSD 后，在 AIME24/25、HMMT25 上的长预算（32k–38k）结果下降，例如 Qwen3-1.7B avg@16 从 0.372 降到 0.308；回复明显更短（2607.05184）。同一篇中，给外部教师加参考解答的 OPD 也让 wait 的密度从每千 token 3.85 降到 2.54，不加参考解答的 OPD 则基本不变。2607.10805 在 Qwen3-1.7B 加 LoRA 上复现了这一点，认知词密度从 10.3 降到 7.9。2603.24472 在 Qwen3-8B 上也观察到压低。
- **其他设置上方向相反或冲突。**
  - 同为 DeepSeek-R1-Distill-Qwen-7B，2603.24472 报告自蒸馏（SDPO，教师看完整解答）压低认知词，AIME24 下降约 40%；Purified OPSD（2607.02234）报告 OPSD 让 "Wait" 的总数从 34K 升到 83K。
  - 2609.39118 在 Qwen3/OLMo-3 上（前向 KL，训练上限 1,024）发现退化伴随评测长度增长 6%–25%。

**现有解释只覆盖一个方向。**
- 主流解释是：特权教师因为知道答案而更自信、更简洁，学生学到后不再表达不确定性（2603.24472；2607.05184 称为 fork 抑制，作者自认未证明因果）。这只能预测压低。
- 各篇设置也不同：
  - 损失：JSD、前向 KL 或 SDPO 的目标；
  - 训练上限：1,024 对 4,096。2610.03185 发现截断回复进入损失会让长度膨胀；
  - 参考解答在教师提示中的呈现方式。
- 没有工作把这些因素放进同一个设计里判别。

**被忽视的关键：方向取决于教师对特权上下文的"初始认知反应"。**
- 定义 ρ：在训练前固定的学生 rollout 上，先在每个位置算出教师分布在认知 token 集合上的总概率 m_T，以及学生的对应量 m_S，再对所有位置取 log(m_T/m_S) 的均值。
- ρ < 0：教师看到参考解答后比学生更少表达不确定。ρ > 0：教师反而更多地"停下来核对"。
- ρ 取决于模型如何对待提示里的参考解答。它在训练前就能测出来，也可以在不改变参考内容的前提下，只改呈现模板来操纵。

**本 Idea 主张：**

1. **方向律。** OPSD 训练后，长预算评测中认知词密度变化的符号与 ρ 相同。在同一模型、同一数据、同一训练上限和损失下，把呈现模板从"已验证正确的参考解答"换成"一份待检查、可能有错的解答"，若能翻转 ρ 的符号，认知词的变化方向也随之翻转。长度变化同向。训练上限与损失只改变幅度，不改变符号。
2. **必要性。** EMP（epistemic-mass-preserving）在每个位置把教师在认知 token 集合上的总质量重新缩放成学生的总质量，集合内各 token 的相对比例和集合外的分布都保留教师的形状，其余照常蒸馏。主张它在 ρ < 0 与 ρ > 0 两种设置下都能消除长预算退化，同时保留短预算下的收益。对一个频率匹配的随机 token 类做同样的操作则做不到。

**结果如何判定（事先固定）**

主设计是 Qwen3-1.7B 上的 模板 {A, B} × 训练上限 {1,024, 4,096}，损失 JSD，每格 2 个种子。三种竞争解释的预测如下：

| 结果 | 判定 |
|---|---|
| 认知词变化的符号在至少 7/8 次运行中与 ρ 相同；模板翻转在两个上限下都翻转符号；上限改变在两个模板下都不翻转符号 | 支持方向律 |
| 符号跟随上限，不跟随模板 | 支持截断解释，方向律被推翻 |
| 前向 KL 对照中，符号在同模板、同上限下随损失翻转 | 支持损失解释，方向律被推翻 |
| 模板 B 在事先检查中翻不出 ρ > 0 | 主张一改为分级检验：认知词变化幅度与 ρ 的秩相关；如实报告"未能翻转" |
| 其余 | 不确定，报告效应量 |

- 长度：判定规则与认知词相同。若长度跟随上限、认知词跟随 ρ，就报告"两类方向由不同因素决定"。这本身就能解释 2607.05184 与 2609.39118 的长度冲突。
- 主张二：
  - **支持：** 在 vanilla OPSD 有长预算退化的格子里，EMP 在 38k 预算下的 avg@16 不低于基座（配对 bootstrap 95% CI），并显著高于 vanilla OPSD 和随机类对照；在 4k–8k 预算下不低于 vanilla OPSD。
  - **推翻：** EMP 与随机类对照没有差别，或 EMP 仍显著低于基座。
- 显著性：认知词变化用按题目重采样的 bootstrap，95% CI 不含 0 才计符号。

## 方法设计的核心思想

**输入：**
- 思考模型的初始权重；带参考解答的数学题（OpenThoughts）；两种呈现模板，内容相同、只改框架用语；一个事先固定的认知 token 集合。
- 认知 token 集合沿用 2603.24472 的 10 个认知词（wait、hmm、perhaps、maybe、actually、alternatively、seems、might、likely、check），取它们在分词器中为单 token 的大小写与带空格变体。

**实际动作：**
1. **测 ρ（训练前，只需前向）。** 用初始模型在 200 道训练题上各采样 1 条学生 rollout，在每个位置算教师与学生在认知集合上的总概率，得到每种（模型，模板）的 ρ。模板 B 事先准备 3 种措辞，只按 ρ 选定一种，不看任何训练结果。
2. **OPSD 训练。** 与 2607.05184 的设置相同：JSD、1 epoch、OpenThoughts 15k、训练时开思考。区别只在模板与上限。为了适配 2×A100 使用 LoRA；2607.10805 已在 Qwen3-1.7B 加 LoRA 上复现了退化。
3. **EMP。** 对每个位置的教师分布 $\pi_T$ 做重新缩放：认知集合 $E$ 内的 token 乘以 $m_S/m_T$，集合外的 token 乘以 $(1-m_S)/(1-m_T)$，其中 $m_S$ 是学生（梯度截断）在 $E$ 上的总概率。缩放后再计算 JSD。这一步不需要额外的前向。随机类对照把 $E$ 换成一组单 token 普通词：它们在学生 rollout 上的平均总概率与 $E$ 相差不超过 20%，排除认知词、数字和数学符号，用固定种子抽取。
4. **评测。** 在 4k、8k、16k、32k、38k 五个生成预算下测 avg@16、每千 token 的认知词密度和平均长度。

**输出：** 每个格子的 ρ、认知词与长度变化（带 CI）、各预算下的 avg@16 曲线，以及判定表的结论。

**与最高近邻的关键差别：**
- 2607.05184 只观察到压低方向，并把它归因于 fork 抑制，没有做因果检验，也没有给出修法。
- 2603.24472 在 GRPO 中惩罚认知 token，给出的是"压低会伤害"的充分性证据，没有解释方向为何会反过来。
- Purified OPSD 用 PMI 目标去掉参考诱导的分量；AD-OPSD 在高熵分叉处把更新锚定到基座；DASD 按熵切换吸引与排斥；OPSD 官方仓库截断逐 token 散度。它们都只针对压低方向，或作用于整个分布、整类高熵位置。
- 本 Idea 用一个训练前可测、可操纵的量解释方向本身，并用只作用于认知类边际、带随机类对照的干预检验必要性。

## 最小实验

**模型与数据：**
- 主模型：Qwen3-1.7B，训练与评测都开思考。在这个模型上，退化与认知词压低都已有报告：2607.05184 全参训练，2607.10805 用 LoRA。
- 外部检验模型：DeepSeek-R1-Distill-Qwen-7B，两篇论文在它上面报告了相反的方向。
- 训练数据：2607.05184 仓库构建的 OpenThoughts 数学 15k 子集，教师特权上下文为 `solution` 列。
- 评测：AIME24、AIME25、HMMT25，avg@16，温度与 top-p 沿用该仓库。

**训练运行（同一套代码；各臂只在列出的因素上不同，学习率、步数、batch、LoRA 秩都相同）：**
- 主设计：Qwen3-1.7B，模板 {A, B} × 上限 {1,024, 4,096} × JSD × 2 个种子，共 8 次。
- 损失检验：模板 {A, B} × 上限 4,096 × 前向 KL × 1 个种子，共 2 次。
- EMP：模板 {A, B} × 4,096 × JSD × 2 个种子，共 4 次。随机类对照：模板 A × 2 个种子，共 2 次。逐 token 截断 baseline（token_clip=0.05）：模板 A × 2 个种子，共 2 次。
- 外部检验：R1-Distill-Qwen-7B，模板 {A, B} × 4,096 × JSD × 1 个种子，共 2 次。
- 基座模型直接评测。

**Baseline 与复现入口：**

| 名称 | 与本任务的关系 | 论文 | 代码与复现入口 |
|---|---|---|---|
| vanilla OPSD（思考模型、长预算） | 同任务、同评测，最高近邻，退化现象的来源 | https://arxiv.org/abs/2607.05184 | https://github.com/princeton-pli/rethinking-opsd-for-thinking-models （2026-10-28 核验：`train.py`、`opsd/trainer.py`、`run_budget_sweep.py`、`run_eval.py`、`data_tools/build_openthoughts_30k.py`、`make_openthoughts_15k_subset.py`、`submit_experiment.sh`）；按 README 先构建数据，再 `train.py`，再 `run_budget_sweep.py` |
| OPSD + 逐 token 散度截断 | 同任务中压低风格 token 信号的已有做法 | https://arxiv.org/abs/2601.18734 | https://github.com/siyan-zhao/OPSD （核验：`opsd_trainer.py` 的 `generalized_jsd_loss(..., token_clip)`；`scripts/run_opsd_1b.sh` 用 Qwen3-1.7B、`--jsd_token_clip 0.05`）；截断逻辑移植进同一套训练代码 |
| 基座模型 | 参照 | — | 直接评测 |

AD-OPSD（2607.10805）与 Purified OPSD（2607.02234）是同任务的修法，但未找到公开代码，所以只作相关工作讨论，不进最小实验。

**预算：**
- 2607.05184 的主训练是 15k 题、1 epoch、有效 batch 64，约 234 步。
- 2×A100 上 Qwen3-1.7B 加 LoRA：上限 4,096 时，每步生成约 64 × 3.5k token，加上教师与学生的前向和反向，估计约 40 秒，一次训练约 2.6 小时（5.2 A100 小时）。上限 1,024 约减半。
- 五个预算的评测：约 90 题 × 16 条，长度最多 38k，按 vLLM 估约 2 A100 小时。
- Qwen3-1.7B 共 18 次运行，约 115 A100 小时；R1-Distill-Qwen-7B 两次运行，每次约 20 A100 小时；ρ 测量约 2 A100 小时。
- 合计约 160 A100 小时，2 张 A100 约 3.5 天。数学题用规则判分，不需要付费 API。

**支持结果：** 判定为"支持方向律"；主张二成立；R1-Distill-Qwen-7B 上两个模板的方向与其 ρ 的符号一致。

**推翻结果：** 判定表中的"支持截断解释"或"支持损失解释"；EMP 与随机类对照没有差别。

Frozen Problem Anchor and user constraints:

- 根本问题：特权上下文自蒸馏（OPSD）为何让训练时开思考的推理模型在长评测预算下退化？退化来自特权信息语义还是教师上下文分布偏移？失效时长度变短还是变长由什么决定？
- 领域与设置：数学推理；思考模型（Qwen3 系列等）在训练时开思考做 OPSD；OpenThoughts 类数学数据；在 AIME24/25、HMMT25 上评测 avg@k，评测生成预算 4k–38k。
- 必须解决的瓶颈：失效时长度方向冲突未对齐；1-shot OPD 一致有效只在自 RL 教师下测；外推到非数学与异族教师无证据。
- 约束：2×A100 80G；开源模型、LoRA 可接受；付费 API 1000 元以内；半年内投主会。
- 进入实验规划的成功条件：有一个可证伪的 Claim，最小实验能在上述资源内区分本 Idea 与最高近邻。
