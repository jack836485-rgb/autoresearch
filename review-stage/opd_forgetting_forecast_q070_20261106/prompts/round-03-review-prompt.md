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
Today's date: 2026-11-06. Known tool workarounds: arXiv 摘要与 HTML 全文可在 shell 里直接抓取（https://arxiv.org/abs/<id>、https://arxiv.org/html/<id>），也可用 WebFetch；GitHub API（gh / api.github.com）在本会话返回 403，读代码仓库请用 git clone --depth 1 <url> 到临时目录；Agent 工具无法单独设置 reasoning effort，使用默认
Finish all searches before answering and leave no background tasks running. Do not read other
files in this workspace and do not write files, except your raw review to /home/claude/jack836485-rgb/autoresearch/review-stage/opd_forgetting_forecast_q070_20261106/round-03-review.md (UTF-8).
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
| 有效性 / `effectiveness` | Idea 阶段只评**先验合理性**：方法为什么有望改善目标问题（或现象／视角为什么可靠、有解释力），以及已有证据是否与关键假设相矛盾。**实际效果大小不在此评分**，见下文“待预研”。 | 6：关键假设有具体且适用的机制、理论或邻近证据支持，且未发现与之矛盾的已有证据。8：从动作到预期改善的因果链完整，每个关键假设都有适用依据，主要竞争解释或已知反例已被现有证据排除或明确处理，没有尚未解释的大跳跃。两档都不要求已知收益幅度。 |

**跨领域迁移的新颖度。** 新颖度相对的是目标领域。别的领域已有的方法说明机制来源，不等于目标领域已经有这项工作：
- 经检索确认目标领域还没有这一做法时，迁移本身就是对目标领域的实质新意，新颖度一般不低于 7；
- 能说明朴素迁移在目标领域会遇到什么问题、并给出相应的结构性适配时，可以给到 8 或更高；
- 只有目标领域已有直接近邻时，才按普通增量评判；
- 跨领域来源可以在讨论"机制本身是否原创"时引用，但不能仅因为别的领域有类似思想就压低对目标领域的新颖度。

这是实验前的 Idea 审查，有效性在这里拆成三件事，分开处理：

1. **先验合理性**（计分）：现在有什么依据支持"这个动作有望起作用"，依据适用于哪些条件，迁移成立需要什么关键条件。
2. **已有直接反证**（计分，严重时作为阻断）：近邻的原始数据、受控实验或理论结果与关键假设直接矛盾时，必须指出并扣分；不能因为"还没做预研"而放过。
3. **实际效果大小**（不计分，标注“待预研”）：收益有多大、能否超过强基线多少、覆盖与外推范围，是预研要回答的问题。Reviewer 在审查中把这类未知列为“待预研”，不能因其未知而压低有效性分数，也不能用"效果可能很大"抬高分数。

成功阈值（如“提升10个百分点”）、公平对照、更多种子和完整消融只说明怎样验证，不是方法会有效的依据；修正这些设计不能自动升高有效性分数。其他场景的成功需要说明使其迁移成立的关键条件，不能直接当成当前设置的效果。

诊断或自适应分配方案还需说明：信号为何与所选干预的相对收益有关。能预测错误、难度或漏检，不等于能判断哪一种修法更有效；简单测试上的能力也不自动迁移到依赖结构不同的真实任务。可以保留这类候选送审，但要把缺少依据的迁移环节写成未知，不能仅靠更换监督目标或补上消融就视作效果已获支持。

不要求在本 skill 中运行 pilot，也不能因为尚未正式实验就机械地把有效性封顶为6分；效果大小统一标注为“待预研”，交给后续预研回答。方法可由适用理论、紧邻实验和真实案例支持预期；现象／视角可由已核验的原始观察、竞争解释预测或反例结构支持。新颖且重要、有效性有6分依据的方案仍可按8/7/6这类组合通过。明确区分已有证据、待验证假设和未来成功条件，不冒充已经获得的实验结果。最小实验是否能辨别主张仍须单独判断，设计无法判别时是 Claim 阻断，不能用有效性高分掩盖。

贡献通过条件为：**三项都 ≥6，且按分数排序后，次高一项 ≥7、最高一项 ≥8**（即一项 ≥6、一项 ≥7、一项 ≥8）。例如 8/7/6、6/8/7、9/7/6 可以通过；8/6/6、7/7/7、9/9/5 不通过。不取平均数，也不要求三项都 ≥8。总体 `score` 只记录综合判断与支持候选排序，不另设总体分数门槛，不得覆盖三项判断。

## 可行性独立判断

给出 `feasibility: pass | fail` 和一句具体理由。关键操作须有可信的实现路径，所需数据、模型、工具和预算可获得，最小关键实验能在用户约束下完成。依赖没有依据的新能力、无法得到的资源，或关键步骤明显大概率无法实施的候选，不因新颖或重要而放行。应降低实现难度或重新选择候选，不能为追求高新颖度堆出不可信方案。

效果未知是正常研究风险，不等于实现不可行。Reviewer 应分别判断“这个实验能否做出来”和“它能否有说服力地支持主张”。

## 如何使用这些标准

Improver 先用一句话写清“这项工作成功后，新增了什么值得知道或值得使用的东西”，再据此提出机制、Claim 和最小实验。主 Claim 应表达独立研究贡献，诊断性断言可以支撑它，但可证伪性本身不代表贡献充分。自评记录三项暂定分数、依据和未知部分，用于候选排序；**不要求先自评达到放行门槛才准送审**，不得为了送审抬高分数。主贡献具体、存在可信实现路线且关键实验能判别的候选，即使贡献潜力尚不确定，也可接受独立反馈。只剩诊断种子、明显无独立贡献或无可信实现路径时，先实质改进或停止，不为用满预算反复送审。最终三维硬门槛仅由独立 Reviewer 和正式放行应用。

Reviewer 必须回答：**关键结果若成立，主贡献是什么；现在有哪些依据支持其重要性、新意和效果；实现路径与验证是否可信？** 查新不能代替重要性和有效性判断，理想结果的价值也不能替代效果的当前依据。贡献不足或可行性不通过应写入 `fatal_blockers`，不可给出 `experiment_ready`。

修订可以缩小范围、降低成本或收紧措辞，但每次都须重新判断主贡献。若缩小后只剩一个分量不足的断言，不能凭“更容易验证”通过；补充种子、统计检验或控制变量也不能自动提升主贡献的分量。没有合格候选时继续实质改进或停止，不强行产出 Final Idea。

Independently assess the same main contribution on importance, novelty, and effectiveness,
with evidence-based reasons for each score. Judge feasibility separately. Give one overall
score from 1 to 10 for reference; it cannot override the three-dimensional gate. Explicitly
answer what would become worth knowing or using if the key planned results held. A falsifiable
assertion is not automatically a sufficient contribution. Do not invent positive results.
For effectiveness, score only prior plausibility: the evidence available now, why it applies
to this setting, and whether existing evidence directly contradicts a key assumption (direct
counter-evidence must lower the score and may be a fatal blocker). Do not score the size of
the expected gain: list it under 待预研 (pending pre-study) and neither lower nor raise the
score because it is unknown. A success threshold and a well-controlled future experiment do
not establish plausibility. Do not require a pilot or cap effectiveness mechanically merely
because this is a pre-experiment idea.
For novelty, judge against the target field. A method borrowed from another field counts as
novel for the target field when your own search finds no such work there (normally at least
7); do not lower it merely because a similar idea exists elsewhere.
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
- experiment_ready: all three contribution scores >= 6, and after sorting the middle one >= 7 and the highest >= 8, feasibility pass,
  and no fatal contribution, novelty, feasibility, or claim blocker
- promising_needs_revision: potentially salvageable, but contribution, evidence, novelty, or feasibility needs revision
- needs_rethink: the main contribution is too weak, covered, unsupported, or cannot be tested by the experiment
- reject: not worth further work under the stated constraints

对外只输出下面三个 Markdown 部分，不要给重构方向、修改清单、实验 checklist 或长综述：
## 结论
<用当前日期给出总体 score、verdict；用一句话判断主贡献是什么、是否足够，以及为什么。总体分数不作为额外门槛。>

## Claim 判断
<先用三行短表给出重要性、新颖度、有效性的分数与依据；有效性只评先验合理性：先说明当前依据、迁移条件，以及是否存在与关键假设直接矛盾的已有证据，不能只说“若提高X则8分”；收益大小等效果层面的未知另列一行“待预研”，不计入分数。用一句话说明回答原问题、子问题或邻近新问题及原问题未答部分，不因转向自动否决。另说实验能否判别主张。再给可行性pass/fail、具体实现与预算依据，区分无代码和规范/资源确实不足，核实关键数据可得路线与标签含义。不强制现象类贡献附加修法。>

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

**定位关键词：** on-policy distillation；reverse KL；forward KL；catastrophic forgetting；same-origin teacher；teacher selection

**一句话定位：** 在策略蒸馏（OPD）后训练中，学生在训练域（数学）之外的通用能力会随教师改变，本工作研究这种改变在单道 OOD 题上如何从教师传到学生——是否对称、是否受师生来源门控、是否取决于 KL 方向——以及能否据此在训练前预测学生会丢哪些题。

**与起点问题的关系：** 原问题，细化到逐题。保留对象（OPD 学生相对基座的 OOD 能力变化）、条件（同一学生基座与配方、只换教师）和“外部大教师与由学生基座派生的教师用同一模型解释”的目标。起点的两个候选预测量都保留并成为对手：“冻结教师在 OOD 前缀上相对学生基座的 KL”在每道题的前缀上计算；“教师 OOD 损失”变成每道题教师相对学生的有符号能力差。仍未回答：遗忘的时间进程（只在固定步数比较），以及数学以外的训练域。

前提证据。(1) 同源继承：OPDArena（arXiv 2610.25651）中由学生基座训出的 SFT/RLVR 教师，其学生在 OOD 前缀上关闭了到教师 64–90% 的预测差距（Table 9），OOD 变化接近或超过教师（Qwen3-8B：教师 SFT −2.83 → 学生 −4.14，§D.3）；arXiv 2608.16647 中同源教师只用数学提示就把学生的代码/科学能力拉向教师水平，弱于学生时拉到初始以下（§4.1），跨源教师主要拟合训练分布、初始 Top-16 重叠更低（§5）。(2) 反向 KL 传不了学生不产生的内容：arXiv 2610.09639 中由学生继续训练得到的教师掌握的新事实，经反向 KL OPD 后学生单步召回仅 13.12%，改前向 KL 升到 54.10%（Qwen3-4B）/94.10%（Gemma-2-2B）（§4.1–4.2，归因于反向 KL 只惩罚学生已有显著概率的 token）；ErrOPD（arXiv 2605.08737）中学生几乎不犯的教师错误，前向 KL 传递 +13–23 分，反向 KL <0.05 分。这两组证据分别只讨论平均水平上的继承，或域内注入的新内容；尚无工作在域外通用能力上看继承的两侧，即教师更弱的题与教师更强的题是否同样被继承。

## 核心 Claim

若主结果成立，本工作给出一个机制性新现象及其训练前用法：**反向 KL 的 OPD 对同源教师的域外能力差是单向继承的**。学生原本答对、教师答错的题会被继承成遗忘；教师答对、学生原本答错的题基本传不过来；跨源教师两侧都不传；把目标换成前向 KL，收益侧的继承会恢复。由此，OPD 的通用能力遗忘可以在训练前**逐题**预测，判据是同源教师上“学生对、教师错”的那些题，并且能解释两个反常：平均更强的同源教师仍可能让学生遗忘；Self-OPD(SFT) 的遗忘超过 SFT 教师自身（收益侧被阻断，缺陷侧全额继承）。

可推翻的判断（对每道 OOD 题 i，G_i 为训练前测得的教师相对学生基座的金标对数优势差，Δℓ_i 为学生训练后对数优势变化；回归含任务固定效应与学生初始对数优势协变量，分两侧估计斜率 κ−（G_i<0）与 κ+（G_i>0））：
- （H1 同源继承）同源教师 κ− > 0。
- （H2 不对称）同源教师 κ− 显著大于 κ+，知识类任务（TriviaQA、NQ-Open、MMLU）上差距最大。
- （H3 KL 方向因果）同一同源教师改用前向 KL 后 κ+ 显著上升。
- （H4 来源门控）跨源教师在控制协变量后 κ− 与 κ+ 都接近 0，并显著小于同源教师。
- （H5 训练前可用）用“G_i<0 且教师同源”预测题从对变错的 AUROC，高于起点的逐题前缀 KL、教师级 OOD 损失与下文两个对照。

若 H2 不成立（两侧对称），结论改写为“对称的整体对齐”（即 2608.16647 的图景），逐题预测仍然成立；若 H4 不成立，则继承与来源无关；若逐题前缀 KL 胜出，起点假设成立。

当前依据与适用条件：H1、H4 有上述两篇独立的同源/跨源证据；H2、H3 的机制依据是反向 KL 的平均梯度按学生自身概率加权（OPDArena Eq. 11），以及 2610.09639 与 ErrOPD 在域内的 KL 方向对照。教师压低学生已有的高概率答案，落在学生会产生的 token 上，因而受惩罚并传递；提升学生不产生的答案则几乎不受惩罚。有两处未经检验的跳跃，这也是本工作要检验的。第一，域外题不在训练提示中，继承靠共享参数传播，域内“按学生概率缩放”的机制能否延伸到域外，尚无直接证据。第二，缺陷侧继承目前只有聚合层证据（Self-OPD(SFT)），没有逐题证据。已核对的反面观察：OPDArena Table 3 的跨类别 ρ 与遗忘排序翻转（1.5B：A 0.311/−0.39，B 0.217/−0.69）不构成反证，B 为跨源 7B SFT 教师，H4 预测其 OOD 优势不被继承。效果大小待预研。

## 方法设计的核心思想

输入：学生基座 p0、冻结教师 q、OOD 题库。训练前只做前向：
- **逐题有符号能力差 G_i**：HellaSwag/ARC-C/MMLU 用金标选项与最强干扰项的对数似然差（候选似然）；TriviaQA/NQ-Open 用金标答案的长度归一对数似然（5-shot）；BBH 用直接作答提示下的金标答案对数似然。G_i = 教师值 − p0 值。IFEval 无金标，只进准确率。
- **同源度 o_t**：OOD 前缀上 p0 与 q 的初始 Top-16 重叠与 JS，连续量。同家族不同规模是否算跨源由 o_t 决定，不预设二分（回应 2604.13016“同家族 1.5B/7B 从学生视角不可区分”）。参数距离只用来核验来源。
- **对手预测量**：起点的逐题前缀 KL(q‖p0)；教师级 OOD 损失；教师认知标记率（arXiv 2603.24472）。**对照①**：教师在训练题上输出的 p0 困惑度、教师自评校正打分差（OPDArena Eq. 16）、PPL≥2.5 的 token 比例（arXiv 2501.14315）。**对照②**：每题前缀上的 KL 按风格位置与内容位置拆分（arXiv 2611.07722 的类别规则；在 OOD 题上，答案候选 token 属内容），并同时报逐 token 均值与总量。

训练后：按题计算 Δℓ_i，分两侧回归得 κ−、κ+；同源与跨源的差、反向与前向 KL 的差都在教师 × 题的层面上检验。

与最高近邻的差别：2608.16647 与 OPDArena 是平均水平上的、对称的继承图景，未区分两侧，也未逐题；2610.09639 与 ErrOPD 的 KL 方向效应都在域内、针对注入的新内容，未涉及域外通用能力、教师来源和“压低学生已有输出”这一侧；ESC（arXiv 2610.39020）只预测域内收益。2601.15394 在蒸馏前逐样本预测训练数据记忆，对象不同。

## 最小实验

**教师（学生 S1 = Qwen2.5-1.5B-Base）。** 四对“同类后训练、不同来源”的公开教师：零 RL——hkust-nlp/Qwen-2.5-1.5B-SimpleRL-Zoo 与 Qwen-2.5-7B-SimpleRL-Zoo（github.com/hkust-nlp/simpleRL-reason 已核验，各由对应 Qwen2.5 基座训出）；通用指令——Qwen2.5-1.5B-Instruct 与 Qwen2.5-7B-Instruct；数学继续预训练——Qwen2.5-Math-1.5B 与 Qwen2.5-Math-7B（由 Qwen2.5 基座初始化，arXiv 2409.12122；HF 元数据 base_model 为 Qwen2.5-1.5B）；数学指令——Qwen2.5-Math-1.5B-Instruct（base_model 为 Qwen2.5-Math-1.5B）与 Qwen2.5-Math-7B-Instruct。另加两个**同规模跨源**教师 Qwen3-1.7B-Base 与 Qwen3-1.7B，共 10 个。每个教师在约 3 万道题上，G_i 都有正有负（7B 教师平均更强，但题级仍有大量“学生对、教师错”的题），所以跨源两侧斜率由每个教师自身识别，不依赖少数教师。指令类教师在 Raw 前缀上的模板偏差两个来源都有，且两侧斜率都在同一教师内部比较。
**复现学生 S2 = Qwen3-1.7B-Base**：同源 Qwen3-1.7B，跨源 Qwen2.5-1.5B-Instruct、Qwen3-4B、Qwen2.5-Math-1.5B。
**KL 方向对照（H3）**：对同源的 Qwen2.5-Math-1.5B 与 Qwen2.5-1.5B-Instruct 各加一次前向 KL 的 OPD，在教师 Top-16 支持上计算前向 KL；其余设置不变。实现方式是在 OPDArena 的 verl 损失处改一处，另行实现。

**训练与测量。** 使用 OPDArena 公开代码（github.com/StellarCurtain/OPDArena，`opdarena.train --method opd`；SFT/RLVR 检查点未发布，本设计不需要），按其 Table 7 设置：OpenR1-50K，官方下载器复现数据顺序；lr 1e-6；每步 64 题 × 4 回答；学生 Top-16 支持与学生概率加权；KL 系数 0。**提示与响应总长统一 ≤4096**（Qwen2.5-Math 系 max_position_embeddings=4096），共 300 步，所有运行共用同一数据顺序。S1 上对 2 个教师各加 2 个种子，用于估计逐题的训练噪声与回归均值伪迹。第 150 与 300 步测量：HellaSwag/ARC-C/MMLU 全量（10,042/1,172/14,042 题），TriviaQA/NQ-Open 各 2,000 题，BBH 27 任务各 50 题，逐题记录金标对数优势；另报 7 任务准确率宏平均（含 IFEval 全 541 题），与 OPDArena 可比。合计 10 + 4 + 2 + 4 = 20 次运行。

**判别与伪迹控制。** 回归均值是主要伪迹：G_i 与学生初始对数优势相关，任何扰动都会让高置信题下降、低置信题上升。处理方式有三：(a) 以学生初始对数优势为协变量；(b) 用跨源教师与种子间差异估计“无继承”的基线斜率，同源效应按相对该基线的差检验；(c) 用前向/反向 KL 的组内差，伪迹在两者中相同。统计采用按题与按教师的双重聚类 bootstrap。H5 的评价方式为：每个教师内部，预测“题从对变错”的 AUROC 与 precision@k，在 10 个教师上做配对置换检验。

**对照①②的位置。** 对照①是教师级量，用来预测每个教师的截距，即与能力差无关的整体扰动；对照②是题级量，与 G_i 并列进入 H5 的比较，检验遗忘的题是否主要由风格位置的偏移预测。风格/内容分类按 2611.07722 附录 C.2 的规则另行实现（其代码 aim-uofa/sd-opd 只含训练代码，未发布词表，已核验），先在 S1 与一个指令教师上复现“风格/数学逐 token 均值比约 3–5 倍”。已知部分反证：OPDArena Table 12 显示首位置置零后 OOD 差 ≤0.53 pp。

**基线与复现路线。** 固定前缀 KL/JS 与 Top-16 重叠：OPDArena `analysis.prefixes`/`analysis.distributions --teacher`（已核验）。ESC/Overlap@16：github.com/maybenotime/opd-esc（`verl_opd/plugins/k1_probe/k1_probe.py`，已核验）。困惑度、打分差与认知标记率按原文公式实现。早期检查点外推（第 20 步的逐题变化）作强参照。

**算力与预研。** 逐题能力差只需前向，约 12 个模型 × 3 万题，约 5 GPU·h。每次 OPD 在 2×A100 上约 1.5–2 分钟/步，300 步约 8–10 h；20 次约 400 GPU·h，加评测约 40 GPU·h，可在 8×A100 × 5 天内完成。预研（2×A100）分三步：
1. 不训练，算 S1 的 10 个教师的 G_i 与 o_t。若同源与跨源的 o_t 不分离，或同源教师“学生对、教师错”的题少于 5%，即停。
2. 只训 Qwen2.5-Math-1.5B，反向与前向 KL 各 150 步，另加 1 个反向 KL 的重复种子（约 18 h）。预期反向 KL 下 κ− 明显大于 κ+，前向 KL 下 κ+ 上升；若 κ−、κ+ 都不超过种子间基线，即停。
3. 通过后再训 1 个跨源教师，看 H4。
无付费 API，无人工标注。

Frozen Problem Anchor and user constraints:

- **起点问题**：OPD 中，学生在训练域（数学）之外的能力遗忘随教师来源变化很大；能否只用训练开始前可测的量（冻结教师、学生基座、少量前缀/rollout）预测这个遗忘，并让外部大教师与 Self-OPD（SFT/RLVR）教师落在同一条预测曲线上。
- **对象**：OPD 学生（Qwen 系基座模型）与冻结教师；遗忘 = 学生 OOD 通用能力相对基座的变化。
- **条件**：同一学生基座、同一训练数据与 OPD 配方（在策略采样 + 逐 token 反向 KL / 学生 Top-k 支持），只换教师。
- **初始任务/评测**：OPDArena 设置——OpenR1 数学训练；域内 AMC23/AIME24/AIME25/HMMT25/Math500；OOD HellaSwag/ARC-C/MMLU/IFEval/TriviaQA/BBH/NQ-Open。
- **瓶颈**：已有关联（Razor 的 KL、OPDArena 的 OOD JS）都在训练后测；训练前的教师侧量（ρ_T、域内打分差、初始方向局部 ρ）只有定义或零星数值，没有跨教师来源的定量检验。
- **证据边界**：只有数学训练域；Qwen 两个家族；OPDArena 外部教师组内遗忘差 1–2 pp、两种子平均、无 CI。
- **用户约束**：不做世界模型/视频/机器人；正式实验 8×A100 80G，最好 ≤5 天；预研 2×A100；付费 API ≤1000 元可自主；token 资源稀缺；目标半年内投主会。必须保留两个对照：① 域内基线预测量（教师在域内提示上的输出在学生基座下的困惑度，参照 2501.14315）；② 逐 token KL 按风格位置与内容位置拆分（参照 2611.07722）。
- **进入实验规划的成功条件**：给出一个可在上述算力内完成、能区分“静态分布距离 / 教师 OOD 损失 / 不确定性表达率 / 域内困惑度 / 其他训练前量”谁预测 OPD 遗忘的最小实验，且遗忘测量的分辨力足以区分结论。
