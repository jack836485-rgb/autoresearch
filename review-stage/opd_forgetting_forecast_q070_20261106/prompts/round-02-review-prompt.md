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
files in this workspace and do not write files, except your raw review to /home/claude/jack836485-rgb/autoresearch/review-stage/opd_forgetting_forecast_q070_20261106/round-02-review.md (UTF-8).
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

**定位关键词：** on-policy distillation；catastrophic forgetting；teacher selection；same-origin teacher；KL divergence；top-k overlap

**一句话定位：** 在策略蒸馏（OPD）后训练中，学生在训练域（数学）之外的通用能力变化随教师来源而变、可正可负，本工作研究能否在训练前用教师相对学生的逐任务能力差与师生同源程度解释并预测这一变化。

**与起点问题的关系：** 原问题。保留对象（OPD 学生相对基座的 OOD 能力变化）、条件（同一学生基座与配方、只换教师）和“外部大教师与由学生基座训出的教师落在同一条曲线上”的目标。改变的是预测形式：起点把“冻结教师在 OOD 前缀上相对学生基座的 KL”当作遗忘的主效应，并拿“教师 OOD 损失”作对手；本工作把前者当作继承强度的调节量、后者当作被继承的有符号量，两个主效应模型都是本模型的嵌套特例，可直接比较。仍未回答：遗忘随训练步数的时间进程（只预测固定步数下的相对大小）；也只覆盖数学训练域。

前提证据：三处独立观察指向同一规律。(1) 同源继承：OPDArena（arXiv 2610.25651）中由学生基座训出的 SFT/RLVR 教师，其学生在 OOD 固定前缀上关闭了到教师 64–90% 的预测差距（Table 9：d_out,OOD 0.10–0.36），OOD 变化接近或超过教师（Qwen3-8B：教师 SFT −2.83 → 学生 −4.14；RLVR +0.75 → +0.75；§D.3）。(2) 同源可升可降、跨源不传：arXiv 2608.16647 中同源教师只用数学提示就把学生的代码/科学能力拉向教师水平，科学能力弱于学生的数学教师使学生 GPQA 降到初始以下（§4.1、Fig. 4a）；跨源教师主要提升训练分布，初始 Top-16 重叠更低且训练中不升（§5 Fig. 6）。(3) 跨源强教师致遗忘：OPDArena 中 OOD 能力强于学生的大基座教师让学生 OOD 下降（Table 2：Qwen3-8B Base 教师 OOD 51.37，学生 35.20 → 33.37）。这三处分别被解释为“继承”“同源泛化”“遗忘”，尚无工作把它们写成同一条可在训练前预测的规律，也没有把 OPD 的 OOD 变化当作逐任务、有符号的量去预测。

## 核心 Claim

若主结果成立，本工作给出 OPD 域外变化的一条**门控继承规律**及其训练前预测：对学生 s、教师 t、OOD 任务 k，

ΔOOD(t,k) ≈ a_t + κ(o_t) · G(t,k)

其中 G(t,k) 是训练前测得的教师相对学生基座在任务 k 上的有符号能力差，o_t 是训练前测得的师生同源度（OOD 前缀上的初始 Top-16 重叠或 JS），κ 随同源度单调上升，a_t 是与教师能力无关的扰动项。可推翻的判断：（H1 继承）同源教师的 κ 显著大于 0，学生逐任务变化的符号跟随 G 的符号——教师在某任务上更弱，学生在该任务上就降；（H2 门控）跨源教师的 κ 显著小于同源教师且接近 0，即其 OOD 优势不能转成学生收益，并有负截距；（H3 训练前可测）κ 对教师的排序可由训练前同源度给出，且 H1–H2 的模型在留一教师预测上优于起点的静态 KL 主效应模型、教师 OOD 损失主效应模型、认知标记率模型与域内困惑度模型。

它改变的判断：Razor 式“离基座越远遗忘越多”在 OPD 中不成立——师生距离调节的是继承而不是直接造成遗忘；OPD 的“遗忘”大部分是对同源教师能力缺陷的继承（Self-OPD(SFT) 遗忘超过 SFT 本身即此），跨源强教师的 OOD 优势无法转移只留下扰动。可用之物：训练前的教师筛选规则——按“保留”看同源度与逐任务差距，不看教师自身 OOD 能力或距离大小。若 H2 不成立（跨源也继承），结论改写为“继承与来源无关”；若静态 KL 主效应胜出，起点假设成立。

当前依据与适用条件：H1 有上述两篇独立直接证据（同源、同训练域）；H2 有 2608.16647 的定性证据与 OPDArena Table 2 的两个点，均未在同规模、同后训练类型下控制来源。本工作对 OPDArena Table 3 的 A/B 翻转（1.5B：A ρ 0.311/OOD −0.39，B 0.217/−0.69；4B：A 0.643/+0.31，B 0.218/−1.92）的解释是：B 是跨源的 7B/8B SFT 教师，其更强的 OOD 不被继承，只剩扰动，因此 ρ 与遗忘排序可以相反；该解释待本实验检验。未知：κ 的绝对大小与学生吸收程度有关（Qwen2.5-1.5B 上 SFT 教师 −0.95 → 学生 −0.21，κ 偏小）；扰动项 a_t 由什么决定没有直接证据。效果大小待预研。

## 方法设计的核心思想

输入：学生基座 p0、冻结教师 q、OOD 评测集与固定前缀。训练前计算：
- **G(t,k)**：教师与 p0 在同一 OOD 任务上的有符号能力差——6 个有金标任务用金标答案对数似然差，IFEval 用准确率差。即起点问题中的“教师 OOD 损失”，按任务保留符号。
- **o_t 同源度**：OOD 固定前缀上 p0 与 q 的初始 Top-16 重叠（2608.16647 §5 的度量）与 JS/KL（OPDArena Eq. 5）；参数距离只用于核验同源，不作预测量。
- **扰动项候选**（用于预测 a_t，起点要求的两个对照在此）：对照①域内基线预测量——教师在训练题上的输出在 p0 下的困惑度、教师自评校正后的打分差（OPDArena Eq. 16）与 p0 下 PPL≥2.5 的 token 比例（arXiv 2501.14315）；对照②在 p0 的域内 rollout 与 OOD 前缀上按风格/内容位置分别计算逐 token |log q − log p0| 与 KL（arXiv 2611.07722 的类别规则），同时报逐 token 均值与按 token 数的总量。

训练后在（教师×任务）格子上拟合混合效应回归，比较嵌套模型：M0 只有截距；M1 起点的静态 KL 主效应；M2 教师 OOD 损失主效应（κ 对所有教师相同）；M3 认知标记率主效应；M4 域内困惑度主效应；M5 本模型（κ 由同源度调节 + 截距）；M5+ 再用对照①②预测截距。

与最高近邻的差别：2608.16647 定性报告同源泛化、跨源拟合，未测通用能力遗忘、未做训练前定量预测，同源与跨源在其设计中与规模、后训练类型混在一起；OPDArena 报告同源继承与跨源强教师致遗忘，但未统一、未预测；ESC（arXiv 2610.39020）只预测域内收益；RL's Razor 的 KL 在训练后测且无符号。本工作把三处现象写成一条有符号、逐任务、训练前可测的规律，并用匹配配对把“来源”从规模与后训练类型中拆出。

## 最小实验

**配对教师（学生 S1 = Qwen2.5-1.5B-Base）。** 四对“同类后训练、不同来源”的公开教师：零 RL——hkust-nlp/Qwen-2.5-1.5B-SimpleRL-Zoo（同源）vs Qwen-2.5-7B-SimpleRL-Zoo（跨源），两者各由对应 Qwen2.5 基座零 RL 训出（github.com/hkust-nlp/simpleRL-reason 已核验）；通用指令——Qwen2.5-1.5B-Instruct vs Qwen2.5-7B-Instruct；数学继续预训练——Qwen2.5-Math-1.5B vs Qwen2.5-Math-7B（均由 Qwen2.5 基座初始化，Qwen2.5-Math 技术报告 arXiv 2409.12122）；数学指令——Qwen2.5-Math-1.5B-Instruct vs Qwen2.5-Math-7B-Instruct。另加两个**同规模跨源**教师 Qwen3-1.7B-Base 与 Qwen3-1.7B，把“来源”与“规模”拆开（Qwen3-1.7B-Base 的 OOD 宏平均 36.09 与 S1 的 35.20 接近，逐任务差有正有负，OPDArena Table 6），共 10 个教师。同源性在预研中用与 S1 的参数距离复核（同源应远小于跨源；Qwen2.5-Math-1.5B-Instruct 的起点报告未明说，若不同源则改归类）。指令/数学指令教师在 Raw 前缀上打分存在模板错配，但同源与跨源两侧都含同类教师，错配在配对内抵消。
**复现学生 S2 = Qwen3-1.7B-Base**：同源 Qwen3-1.7B（后训练版）、跨源 Qwen2.5-1.5B-Instruct（同规模）、Qwen3-4B（同家族不同预训练运行）、Qwen2.5-Math-1.5B，共 4 个。

**训练与标签。** OPDArena 公开代码（github.com/StellarCurtain/OPDArena，`opdarena.train --method opd`）按其 Table 7：OpenR1-50K（官方下载器复现顺序）、lr 1e-6、每步 64 题 × 4 回答、学生 Top-16 与学生概率加权、KL 0；响应上限 4096、300 步；所有教师同一数据顺序。S1 另对 2 个教师各加 2 个种子估计训练噪声。第 150 与 300 步评测 OOD：HellaSwag/ARC-C/MMLU 全量候选似然（10,042/1,172/14,042 题），TriviaQA/NQ-Open 各 2,000 题，BBH 27 任务各 50 题，IFEval 全 541 题；6 个金标任务的主指标是金标答案对数似然变化，IFEval 用准确率；另报 7 任务准确率宏平均与 OPDArena 可比。共 14 个教师运行 + 4 个种子 = 18 次。

**判别。** S1 有 10 教师 × 7 任务 = 70 个格子，S2 有 28 个。H1：同源教师组内 ΔOOD 对 G 的斜率 > 0，且逐任务符号一致率显著高于 50%；H2：跨源组斜率显著小于同源组（交互项检验，教师层面聚类 bootstrap）；H3：留一教师交叉验证中 M5 的预测误差低于 M1–M4（配对比较每个被留出教师的误差，10 个教师上做符号检验/置换检验），并检查同源度 o_t 的连续值能否解释 κ（同源/跨源二分之外，Qwen3-1.7B 系与 Qwen2.5-Math 系提供中间值）。不再要求十几个对手两两 CI 不重叠。

**扰动项诊断（对照①②）。** 在 M5 基础上，检验截距 a_t 能否由域内困惑度/打分差、风格位置与内容位置的 KL 分量预测；若风格分量预测截距而内容分量不预测，对一个跨源教师追加一次“风格位置反馈置零”与一次“等反馈总量的随机内容位置置零”的 300 步运行（2 次）。风格/内容按 2611.07722 附录 C.2 规则独立实现（其代码 aim-uofa/sd-opd 只含训练代码、未发布词表，已核验），先在 S1 与一个指令教师上重现“风格/数学逐 token 均值比约 3–5 倍”。已知部分反证：OPDArena Table 12 首位置置零 OOD 差 ≤0.53 pp；按 token 总量风格幅度低于数学（2611.07722：约 0.74M vs 1.63M），因此这是次要假设。

**基线与复现路线。** 静态距离与 Top-16 重叠：OPDArena `analysis.prefixes`/`analysis.distributions --teacher`（已核验）加 Top-16 集合交集计算；ESC 代码 github.com/maybenotime/opd-esc（`verl_opd/plugins/k1_probe/k1_probe.py`，已核验）可用于重叠与熵形状。困惑度、打分差、认知标记率（arXiv 2603.24472 的 10 个标记）按原文公式实现。早期检查点外推（第 20 步逐任务变化）作强参照。训练后 OOD JS 作事后上界参照。

**算力与预研。** 训练前量约 4 GPU·h。OPD 按 2×A100 约 1.5–2 分钟/步，300 步约 8–10 h；18 次 + 2 次掩码约 20 次，约 380–420 GPU·h，加评测约 40 GPU·h，在 8×A100 × 5 天内。预研（2×A100）：先不训练，算 S1 的 10 个教师的 G 与 o_t——若同源教师的逐任务 G 几乎全同号（无法检验符号跟随）或同源/跨源的 o_t 不分离，则停；否则只训 Qwen2.5-Math-1.5B（同源、通用能力预计弱于学生）与 Qwen2.5-Math-7B（跨源）各 150 步并加 1 个重复种子（约 18 h）：前者逐任务变化应与其 G 同号且跨任务相关，后者应不随 G 变化；两者差异不超过种子噪声即停。无付费 API、无人工标注。

Frozen Problem Anchor and user constraints:

- **起点问题**：OPD 中，学生在训练域（数学）之外的能力遗忘随教师来源变化很大；能否只用训练开始前可测的量（冻结教师、学生基座、少量前缀/rollout）预测这个遗忘，并让外部大教师与 Self-OPD（SFT/RLVR）教师落在同一条预测曲线上。
- **对象**：OPD 学生（Qwen 系基座模型）与冻结教师；遗忘 = 学生 OOD 通用能力相对基座的变化。
- **条件**：同一学生基座、同一训练数据与 OPD 配方（在策略采样 + 逐 token 反向 KL / 学生 Top-k 支持），只换教师。
- **初始任务/评测**：OPDArena 设置——OpenR1 数学训练；域内 AMC23/AIME24/AIME25/HMMT25/Math500；OOD HellaSwag/ARC-C/MMLU/IFEval/TriviaQA/BBH/NQ-Open。
- **瓶颈**：已有关联（Razor 的 KL、OPDArena 的 OOD JS）都在训练后测；训练前的教师侧量（ρ_T、域内打分差、初始方向局部 ρ）只有定义或零星数值，没有跨教师来源的定量检验。
- **证据边界**：只有数学训练域；Qwen 两个家族；OPDArena 外部教师组内遗忘差 1–2 pp、两种子平均、无 CI。
- **用户约束**：不做世界模型/视频/机器人；正式实验 8×A100 80G，最好 ≤5 天；预研 2×A100；付费 API ≤1000 元可自主；token 资源稀缺；目标半年内投主会。必须保留两个对照：① 域内基线预测量（教师在域内提示上的输出在学生基座下的困惑度，参照 2501.14315）；② 逐 token KL 按风格位置与内容位置拆分（参照 2611.07722）。
- **进入实验规划的成功条件**：给出一个可在上述算力内完成、能区分“静态分布距离 / 教师 OOD 损失 / 不确定性表达率 / 域内困惑度 / 其他训练前量”谁预测 OPD 遗忘的最小实验，且遗忘测量的分辨力足以区分结论。
