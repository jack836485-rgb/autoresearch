You are an independent senior reviewer judging whether a research idea has a sufficient,
credible contribution to justify experiment planning for the user's target venue. You are
not a co-author and must not redesign the idea. Novelty alone is not sufficient.

You are intentionally zero-context. Judge only the current four-part brief, the frozen
Problem Anchor, and the user's constraints. Search the closest prior work yourself; the
author's own literature notes are deliberately withheld. Do not invent papers, links, or results.
The Problem Anchor records the starting problem and user constraints. A valuable subproblem
or adjacent new problem is an acceptable outcome of idea improvement. Identify its relation
to that starting point and what remains unanswered there; scope change alone is not a blocker.
Judge its actual contribution on its own evidence, rather than inheriting the starting
problem's importance or demanding that the whole starting problem be solved.
Today's date: 2026-11-03. Known tool workarounds: huggingface.co 本地直连超时，可用 hf-mirror.com；raw.githubusercontent.com 可能超时
Finish all searches before answering and leave no background tasks running. Do not read other
files in this workspace and do not write files, except your raw review to C:\Users\30473\Desktop\研一\autoresearch\review-stage\ai4ai_strategy_lockin_rq004_20261103\round-02-review.md (UTF-8).
Your final message must contain only the review below.

Use the following contribution standard, which the improver was also instructed to use:

# 贡献评判标准：Improver 与 Reviewer 共用

这是候选生成、自评、独立审查与复核共同使用的标准。Improver 在提出候选前必须理解这些评审内容，并据此设计主贡献与最小实验；Reviewer 按同一标准独立判断。分数必须有依据，不能靠扩大措辞或假设实验必然成功来达到门槛。

## 什么样的贡献可以成立

主贡献可以来自方法、发现的新现象、新视角、新任务或它们组成的一条完整研究主线。已有问题上的实质改进可以成立，不要求目标问题从未被解决；重要的新现象或新视角也可以独立成立，不强制附加一个提升任务分数的方法。

研究起点可以演化为有价值的子问题或邻近新问题，它们都可以作为最终 Idea。说明与起点的关系及原问题未答部分，按当前研究对象的独立贡献和证据判断；不因转向自动否决，也不直接沿用原问题的重要性分数。

- **方法贡献**需要落到真实任务或失败条件上，说明相较合理且足够强的 baseline 改善什么，以及为什么该机制有望带来改善。不能只展示中间统计量变化而不检验当前目标问题是否改善。
- **现象／视角贡献**需要说明新发现为何值得知道、相较已有认识新在哪里，以及它能改变什么理解、预测或研究判断。局部相关性、常规消融、仅排除一个解释，或把原因留在没有解释力的残差桶里，不能自动算作重要贡献；需要按下面三个维度判断其实际分量。它不必夸张到“颠覆领域”才能成立。
- **问题发现贡献**若主打“首次揭示领域共有且尚未解决的问题”，必须核实该问题此前的认识和已有处理情况。不要把这一要求推广为所有候选都必须研究一个从未解决的问题。

## 三个维度

对同一个主贡献分别给出 1–10 分；可用一位小数，但分数是研究判断，不是精确测量。混合贡献应有一条完整主线，不能把无关发现的重要性、另一个方法的新颖度和第三个实验的有效性拼成高分。

| 维度 / JSON 键 | 评价内容 | 6 分与 8 分的校准 |
|---|---|---|
| 贡献的重要性 / `importance` | 解决问题的分量，或现象／视角对理解与研究该领域的影响。问题可以已经有解。 | 6：有明确且值得研究的价值，但影响范围有限。8：针对重要瓶颈带来实质改变，或发现会明显改变领域内重要判断。题目宏大不等于高分。 |
| 方法／视角的新颖度 / `novelty` | 相较最高近邻，是否提出了实质不同的机制、现象或理解方式。 | 6：有可辨认的增量。8：有清楚、独立且有内容的新意，超出换名、常规组合或补做实验；不要求实现复杂。 |
| 有效性 / `effectiveness` | 当前依据在多大程度上支持方法能实质改善目标问题，或现象／视角具有可靠性与解释力。 | 6：关键假设有具体且适用的机制、理论或邻近证据支持，但收益幅度、覆盖或外推仍未知。8：已有依据较强地支持目标设置下的实质效果，关键假设与证据之间没有尚未解释的大跳跃。可以依据紧邻受控结果、适用理论或可核验原始案例，不强制先有本方案的实验结果。 |

这是实验前的 Idea 审查。有效性判断先说明**现在有什么依据支持效果、依据适用于哪些条件、仍有哪一步未知**，再说明实验如何判别。成功阈值（如“提升10个百分点”）、公平对照、更多种子和完整消融只说明怎样验证，不是方法会有效的证据；修正这些设计不能自动升高有效性分数。其他场景的成功需要说明使其迁移成立的关键条件，不能直接当成当前设置的效果。

诊断或自适应分配方案还需说明：信号为何与所选干预的相对收益有关。能预测错误、难度或漏检，不等于能判断哪一种修法更有效；简单测试上的能力也不自动迁移到依赖结构不同的真实任务。可以保留这类候选送审，但要把缺少依据的迁移环节写成未知，不能仅靠更换监督目标或补上消融就视作效果已获支持。

不要求在本 skill 中运行 pilot，也不能因为尚未正式实验就机械地把有效性封顶为6分。方法可由适用理论、紧邻实验和真实案例支持预期；现象／视角可由已核验的原始观察、竞争解释预测或反例结构支持。新颖且重要、有效性有6分依据的方案仍可按8/8/6通过。明确区分已有证据、待验证假设和未来成功条件，不冒充已经获得的实验结果。最小实验是否能辨别主张仍须单独判断，设计无法判别时是 Claim 阻断，不能用有效性高分掩盖。

贡献通过条件为：**三项都 ≥6，且至少两项 ≥8**。例如 8/8/6、8/6/8、6/8/8 可以通过；9/9/5、9/7/7 不通过。不取平均数，也不要求三项都 ≥8。总体 `score` 只记录综合判断与支持候选排序，不另设总体分数门槛，不得覆盖三项判断。

## 可行性独立判断

给出 `feasibility: pass | fail` 和一句具体理由。关键操作须有可信的实现路径，所需数据、模型、工具和预算可获得，最小关键实验能在用户约束下完成。依赖没有依据的新能力、无法得到的资源，或关键步骤明显大概率无法实施的候选，不因新颖或重要而放行。应降低实现难度或重新选择候选，不能为追求高新颖度堆出不可信方案。

效果未知是正常研究风险，不等于实现不可行。Reviewer 应分别判断“这个实验能否做出来”和“它能否有说服力地支持主张”。

## 如何使用这些标准

Improver 先用一句话写清“这项工作成功后，新增了什么值得知道或值得使用的东西”，再据此提出机制、Claim 和最小实验。主 Claim 应表达独立研究贡献，诊断性断言可以支撑它，但可证伪性本身不代表贡献充分。自评记录三项暂定分数、依据和未知部分，用于候选排序；**不要求先自评达到两个8分才准送审**，不得为了送审抬高分数。主贡献具体、存在可信实现路线且关键实验能判别的候选，即使贡献潜力尚不确定，也可接受独立反馈。只剩诊断种子、明显无独立贡献或无可信实现路径时，先实质改进或停止，不为用满预算反复送审。最终三维硬门槛仅由独立 Reviewer 和正式放行应用。

Reviewer 必须回答：**关键结果若成立，主贡献是什么；现在有哪些依据支持其重要性、新意和效果；实现路径与验证是否可信？** 查新不能代替重要性和有效性判断，理想结果的价值也不能替代效果的当前依据。贡献不足或可行性不通过应写入 `fatal_blockers`，不可给出 `experiment_ready`。

修订可以缩小范围、降低成本或收紧措辞，但每次都须重新判断主贡献。若缩小后只剩一个分量不足的断言，不能凭“更容易验证”通过；补充种子、统计检验或控制变量也不能自动提升主贡献的分量。没有合格候选时继续实质改进或停止，不强行产出 Final Idea。

Independently assess the same main contribution on importance, novelty, and effectiveness,
with evidence-based reasons for each score. Judge feasibility separately. Give one overall
score from 1 to 10 for reference; it cannot override the three-dimensional gate. Explicitly
answer what would become worth knowing or using if the key planned results held. A falsifiable
assertion is not automatically a sufficient contribution. Do not invent positive results.
For effectiveness, identify the evidence available now, why it applies to this setting, and
what remains untested. A success threshold and a well-controlled future experiment do not
establish expected gains. Do not require a pilot or cap effectiveness mechanically merely
because this is a pre-experiment idea.
For diagnostic-driven actions or adaptive routing, distinguish predicting an error from
predicting the relative benefit of a remedy. Identify the evidence and unknowns connecting
the proposed signal to that decision; do not treat a corrected learning target as evidence
that its features will work.

Search the closest prior work to verify that the contribution is distinct and more than a
relabeling or trivial combination. Check whether the minimal experiment can demonstrate its
value against strong relevant baselines or distinguish the important competing explanations
under the same core budget. Unsupported claims that everyone performs poorly or ignores the
issue are claim blockers. Verify established positioning keywords and same-task strong baselines.
A reproduction route may use inspected public code, or an independent implementation from a
sufficiently specified primary algorithm, prompt and tool protocol, with missing choices and
required artifacts stated explicitly. Public code is not mandatory and a planned reproduction
is not a completed experiment. If the necessary specification or artifacts are unavailable,
identify which Claim that prevents testing; do not demand a different-task performance baseline
or silently disregard a strong competitor. Cross-domain inspiration can constrain novelty but
is not automatically an experimental baseline. For a supplied paper, verify that the new contribution stands
after removing that paper's name; merely completing the paper is a fatal novelty blocker.
For indispensable data or states, distinguish a field/interface from information actually
released or reproducibly constructible. Check sample/release/storage evidence or the proposed
reconstruction inputs, steps, unknown coverage and labeling cost. No pilot is required, but
unavailable necessary inputs block the affected Claim. Ensure labels and metrics evaluate
that same Claim rather than mixing attempts, final success and observable violations.
If a multi-call budget is part of the Claim, check that the executable path fits it after
including prompts, inserted probes and intermediate calls, and that baselines can spend
the saved diagnostic overhead on their own computations.
Claims against the strongest fixed or mixed strategy must also account for published,
same-task improvements within the allowed capabilities, including material prompt or
aggregation changes. Comparing only the base implementation at several budgets may leave
that Claim untested; require the comparisons that could explain the proposed gain.

Verdict meanings:
- experiment_ready: all three contribution scores >= 6, at least two >= 8, feasibility pass,
  and no fatal contribution, novelty, feasibility, or claim blocker
- promising_needs_revision: potentially salvageable, but contribution, evidence, novelty, or feasibility needs revision
- needs_rethink: the main contribution is too weak, covered, unsupported, or cannot be tested by the experiment
- reject: not worth further work under the stated constraints

对外只输出下面三个 Markdown 部分，不要给重构方向、修改清单、实验 checklist 或长综述：
## 结论
<用当前日期给出总体 score、verdict；用一句话判断主贡献是什么、是否足够，以及为什么。总体分数不作为额外门槛。>

## Claim 判断
<先用三行短表给出重要性、新颖度、有效性的分数与依据；有效性先说明当前依据、迁移条件与未知部分，不能只说“若提高X则8分”。用一句话说明回答原问题、子问题或邻近新问题及原问题未答部分，不因转向自动否决。另说实验能否判别主张。再给可行性pass/fail、具体实现与预算依据，区分无代码和规范/资源确实不足，核实关键数据可得路线与标签含义。不强制现象类贡献附加修法。>

## 最高近邻
<最多列 5 篇重叠最高的论文或系统；给出可核验链接、重叠点和仍有的差别。每篇 1-2 行；无法核验就写"需要检索"。>

末尾附上仅供主执行器解析的 JSON，不要增加其他章节：
   {
     "score": 0.0,
     "contribution_scores": {"importance": 0.0, "novelty": 0.0, "effectiveness": 0.0},
     "contribution_assessment": "主贡献及其分量、三项判断的关键依据和待验证条件",
     "feasibility": "fail",
     "feasibility_reason": "关键操作、资源与最小实验能否实现的依据",
     "verdict": "promising_needs_revision",
     "fatal_blockers": [],
     "novelty_conclusion": "...",
     "closest_neighbors": ["paper title or needs_search"]
   }

Current four-part brief:

## 背景

**定位关键词：** autoresearch；keep-if-better acceptance（贪心接受）；algorithmic mode collapse（算法模式坍缩）；premature convergence（早熟收敛）；age-layered population structure（ALPS）；hyperparameter tuning budget in method comparison

**一句话定位：** 代码级自主研究循环由 LLM 提议对训练流水线的修改，执行后只保留让指标变好的修改（Karpathy autoresearch、AIDE² 等 RSI 循环都是这种做法）。这类循环中研究方向会持续收窄，新方向很难被接受。本工作研究其中由接受规则造成的那一部分。

**与起点问题的关系：** 子问题。起点问题是“AI 研发 agent 很少根据实验反馈修订研究策略，锁定来自锚定、信号不足还是模型偏好”。本工作保留“研究方向不被修订”这一对象，把条件收窄为带显式接受规则的研究循环，评价目标为循环的最终指标与盲测指标；同时提出这三种解释之外的第四种：精修程度不对等的比较。自由式后训练 agent（无显式接受规则）为什么很少主动换策略，本工作不直接回答。

## 核心 Claim

**主贡献（若成立）：**
1. **一种由协议造成的锁定机制。** 贪心接受规则把“已经沿同一方向被精修多轮的现任流水线”和“只试一次、未经针对性调整的新方向”直接比较，因此会系统性地拒绝那些在获得同等精修后本会胜出的方向。这一部分锁定由接受协议造成，与提议者是否多样无关。
2. **一个可测的判据。** 用同精修程度对照的反事实精修，测出“欠精修导致的误拒率”。
3. **一种修法。** 把进化计算中的 ALPS（按年龄分层，个体只与同年龄层竞争）迁移为按精修年龄分层的接受规则，在总执行次数不变的条件下减少误拒。

**可推翻的判断：**
- (a) 在贪心循环中被拒绝、且与现任差距不大的新方向里，有可观比例在获得与现任同等次数的精修后会超过现任，且超出幅度大于重复执行的噪声；
- (b) 在执行次数相同时，分层接受规则的最终盲测指标优于贪心接受和 DAPS，且方向收窄（语义簇数下降）更少。

若 (a) 接近零，或 (b) 在执行次数匹配时不成立，主张被推翻。

**目前支持预期的依据（均非本方案的结果）：**
- ML 方法学的受控研究表明，方法比较的结论会随调参预算翻转。例如优化器之间的排名在给足调参后改变（Choi et al., 2019, arXiv:1910.05446；Sivaprasad et al., ICML 2020）；语言模型结构的比较在等量调参后差异消失（Melis et al., ICLR 2018）。研究循环中的修改大多就是训练配方的修改，因此这一前提适用。
- ALPS 在遗传编程中，正是通过防止“精炼过的老个体压制新个体”来缓解早熟收敛（Hornby, GECCO 2006）。
- 在 LLM 研究循环中也有对应现象：
  - AIDE² 公布的被拒提议中，“停滞触发探索”（−0.040）、“重启策略”（−0.078）、“UCB-V 式探索”（−0.080）都在单次评估后就输给已调好的现任（arXiv:2609.26457 及 Weco 博客）；
  - autoresearch agent 常常跳过调参阶段（arXiv:2608.10424）；
  - AutoSOTA 日志中“有帮助的修改”比例从前两轮的 70% 降到第 6 轮以后的 43%（Rehearse，arXiv:2607.27687）；
  - 语义簇数在 500 轮内下降 50–70%（arXiv:2609.00077）。

**未知：**
- 收窄中有多大比例来自精修不对等，而不是方向本身确实更差、收益递减或评测噪声；
- 保护层的精修开销是否会抵消收益；
- 用语义聚类定义“方向”是否足够稳定。

## 方法设计的核心思想

**输入：** 一个训练流水线、一个 LLM 提议者、一个执行器（每次执行限时 5 分钟）、优化指标与盲测指标。

**动作：**
1. 每个被接受的修改记录它所属的“方向”（沿用 2609.00077 的做法：用 LLM 摘要编辑描述，再做语义聚类），以及该方向沿谱系已获得的被接受精修次数，即“精修年龄”。
2. 一个提议若属于新方向（年龄为 0），不和全局最优比，而和现任在同等精修年龄时的历史表现比（现任谱系的分数曲线可以从循环记录中读取）。
3. 通过的新方向进入受保护层，获得至多 r 次本方向内的精修，然后才与全局最优竞争。
4. 层数与 r 固定为少数几档。所有精修执行都计入总执行次数。

**输出：** 与贪心循环执行次数相同的最终流水线，以及每个方向的谱系记录。

**与最高近邻的关键差别：**
- DAPS（2609.00077）改的是提议端（按类别覆盖重新加权、抑制相似提议）加一个忠实度回退门，接受规则仍是“超过噪声阈值就保留”；
- OpenEvolve、ShinkaEvolve 的岛屿与 MAP-Elites 保持种群多样性，但岛内仍是精修程度不对等的比较；
- 赢家诅咒（2610.09239）的校准阈值处理的是随机噪声，不处理精修不对等这种系统性偏差。

## 最小实验

**任务（沿用 DAPS 仓库 github.com/BokwaiHo/arl-mode-collapse 的流水线，仓库已核验存在，入口与配置待核对）：**
- T1：Karpathy autoresearch 式 nanoGPT（约 124M）预训练。盲测为 WikiText-103 对数困惑度。
- T3：Qwen2.5-1.5B 在 GSM8K 上的推理微调。盲测为 SVAMP。
- 每次执行限时 5 分钟（单张 A100），与 DAPS 设定一致。

**提议者：** 所有方法使用同一个提议 LLM（本地开源代码模型或低价 API，固定版本与温度）。

**诊断（检验 (a)）：**
- 在贪心循环中抽取约 60 个“被拒、与现任差距在 2 个噪声标准差以内”的新方向提议。
- 从提议点分叉：新方向获得 4 次本方向内的精修，现任也继续获得 4 次精修。两边执行次数相同，各 2 个种子。
- 报告新方向超过现任的比例，以及超出幅度相对重复执行噪声的大小。
- 噪声由每个任务对固定流水线重复执行 10 次估计。

**对照（检验 (b)；每个任务每种方法 3 个种子，每个循环 120 次执行，执行次数严格相同）：**
1. 贪心 keep-if-better：DAPS 仓库中的 Vanilla AR 实现（论文 B1），即 Karpathy autoresearch 的忠实重实现。
2. DAPS 官方实现。
3. 岛屿 + MAP-Elites 种群：OpenEvolve（github.com/algorithmicsuperintelligence/openevolve，已核验含 database.py、population.py），把训练流水线作为被进化的程序，岛屿数与迁移规则取默认值。
4. 噪声校准阈值：按 2610.09239 §3.2 的贝叶斯阈值独立实现，噪声用重复执行估计。
5. 方向级逐级淘汰：每轮把多个方向各精修 k 步后淘汰一半。
6. 本方法。

**观察量：** 最终优化指标与盲测指标、语义簇数随轮次的变化、新方向的接受率。

**支持主张：** (a) 显著大于零；本方法在两个任务上盲测指标都优于 1、2、4，且收窄更少。

**推翻主张：** (a) 接近零；或者本方法只在接受率上不同，最终指标不优于 1、2。

**成本估算：**
- 循环：2 个任务 × 6 种方法 × 3 个种子 × 120 次 × 5 分钟 ≈ 360 A100 小时。
- 诊断：60 个提议 × 2 臂 × 4 次 × 2 个种子 × 5 分钟 ≈ 80 A100 小时。
- 合计约 440 A100 小时。6 张卡执行、2 张卡服务本地提议模型时约 3 天，在 8×A100、5 天的限制内。
- 若改用 API 提议者：约 4300 次提议 × 约 20k token ≈ 90M token，按国产低价 API 估约 200–400 元。
- 无人工标注。语义聚类的稳定性用 2609.00077 报告的规则分类与 LLM 标注交叉验证（κ=0.84）作参照，并自行抽检。

Frozen Problem Anchor and user constraints:

- **起点问题**：LLM agent 在 AI 研发任务（以自动后训练为主：给定基座模型与目标基准，自主设计数据／训练／评测并提交 checkpoint）中，执行层面能干，但策略层面（数据来源、训练范式、目标能力等高层选择）很少随实验反馈修订。
- **对象与条件**：前沿或开源 agent 作为研究者；训练对象为 1.7B–4B 小基座；单卡、限时的训练预算；评测为固定基准的 pass@1／pass@k。
- **初始任务／评测**：PostTrainBench（Rank et al., 2026；arXiv:2603.08640）；可参照 RSIBench-Data、AI4AI-Bench。
- **瓶颈**：锁定来源未分离（锚定／信号不足／模型偏好）；已有修法依赖外部人类或强制多样性。
- **证据边界**：主证据来自同一份轨迹分析（2608.19072）；其余为摘要层。
- **用户约束**：
  - 算力：可用 8×A100 80G，单个实验最好不超过 5 天；预研阶段常用 2×A100 / 4×L40 / 8×4090。
  - API：付费 API 1000 元以内可自主使用，效果很好时可追加。
  - token 稀缺；目标 2027-04 前投出主会论文（自 2026-10 起半年）。
  - 实验代码与数据放在服务器（ssh），不在本地。
  - 非目标：不回到 OPSD 方向；本 skill 不运行实验。
- **进入实验规划的成功条件**：候选通过两次独立审查（三项贡献 ≥6 且至少两项 ≥8、可行性通过），其最小实验能在上述算力与 API 预算内完成，并能区分其主张。
