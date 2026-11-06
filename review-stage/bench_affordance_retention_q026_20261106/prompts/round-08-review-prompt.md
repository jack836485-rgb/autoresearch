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
Today's date: 2026-11-06. Known tool workarounds: Shell can reach arxiv.org (abs and html pages) and can git clone public GitHub repos; WebFetch to huggingface.co may require user approval; the GitHub API (gh api, api.github.com) is not available in this session
Finish all searches before answering and leave no background tasks running. Do not read other
files in this workspace and do not write files, except your raw review to /home/claude/autoresearch/review-stage/bench_affordance_retention_q026_20261106/round-08-review.md (UTF-8).
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

**定位关键词：** transportability；conditional average treatment effect；effect modification；MTAC-IFBench；SWE-Together；context compaction

**一句话定位：** 编码 agent 的上下文管理方法（压缩、截断、约束单独保存）在静态基准上看起来没有差别，却部署给给约束方式各不相同、且大多只以日志可见的用户人群；本 Idea 研究能否用一份源端测量和目标人群的约束元数据，预测这些方法在该人群上的逐条约束增益与方法排序。

**与起点问题的关系：** 原问题（收窄）。保留"按基准结构性质预测方法增益在交互口径下的保留"这一目标，把静态基准的结构性质（约束只在首轮、无中途用户回合）表述为效应修饰变量上缺少部署取值的样本。只覆盖编码 agent 的上下文管理方法；跨方法族、留出任务族与非编码领域未回答。

## 核心 Claim

成功后新增的东西：一个面向"只见日志的人群"的方法选择依据。SWE-Together 从 11,260 个真实会话只转换出 109 道可运行题，多数人群无法建可运行评测；若本方法成立，方法采用者对自己日志做一次约束标注，就能预测哪种上下文方法在该人群上最好、好多少。

为什么值得预测：在静态基准上，2610.31778 Fig. 3 中没有一种压缩策略在置信区间外优于默认自摘要；但约束一旦出现在会话中途，方法差距是数量级的——CONPACT（2608.11242）§5.1 中只保留最近 5 轮和 LLMLingua-2 的约束保留率为 0%，各 LLM 压缩器从个位数到 98% 不等，SC 提取器超过 90%。因此方法排序取决于人群中约束的构成，静态排序不能代替。

做法：(1) 在源上对约束放置做内容保持的干预（同一约束放在首轮、仓库策略文件或第 t 轮用户消息，源任务拆成多轮以造出"之后还剩 m 轮"），补出静态基准原本没有的层；(2) 以逐条约束是否被满足为单位；(3) 在源上用带交互项的条件效应模型估计方法相对对照的增益随修饰变量的变化，修饰变量为：约束类别、通道、之后剩余轮数、新增或替换、同时生效的约束数、会话长度（取对照臂轨迹的 token 数，对被比较的方法而言是处理前变量）；(4) 按目标约束的修饰变量取值预测并汇总。

可推翻的判断：在 MTAC-IFBench 与 SWE-Together 两个构成迥异的目标上，本方法预测逐条增益的误差低于四个有判别力的对照——只按轮次位置分层、只按约束类别分层、统一折扣、以及目标端少量直接试跑（10 个实例）；并且能预测出两个目标上方法排序的差异。若不优于"只按轮次分层"或"只按类别分层"，说明多变量的迁移没有必要；若不优于目标端少量试跑，说明在可运行目标上没有用处、只剩"只见日志"的情形；若不优于统一折扣，主张被推翻。

目前的依据：Z 中各变量修饰效应都有直接证据——2610.31778 App. 6.11 中功能需求丢 6.2%、过程指令 35.9%、范围排除 36.8%，Table 3 与 Fig. 4a 中丢失随压缩次数单调上升；MTAC-IFBench（2609.14992）§4.4 中策略文件约束衰减慢于用户指令，替换已有约束难于新增；Harness-IF（2608.11727）中反默认的规则低 3.6–7.4 点；CONPACT §5.3 注入位置影响保留；HDA 基线 harness 超过 40 条消息后只保留前 2 条与最后 36 条。未知与假设："条件于这些变量的增益可交换"仍是关键假设；源（英文 Python 修 bug）与 MTAC（中文绿地项目、每轮约 13 条约束）差异大，未测修饰仍可能存在——用留一层检验与目标端少量试跑直接衡量；预测误差大小待预研。

## 方法设计的核心思想

方法–对照对：OpenCode（aisa-group/compaction 分支）中自摘要压缩、小模型摘要、旧工具输出裁剪、SC 提取器，以及 HDA ReAct harness 中截断窗口（36 vs 不截断），均相对"不压缩/不截断"；执行模型 Qwen3.6-27B。压缩阈值设为 32K token，以保证源端拆成多轮后的会话会触发压缩（预研先测触发率）。

源端：SWE-bench Verified 80 题拆成 4 轮，每题注入 3 条带确定性检查器的约束（从 MTAC 可脚本判定的 Content/Quantity/Style/Language 四类和 SWE 类的过程/范围约束中按类别抽取，同时控制约束是否与基线 agent 的默认行为相反），按修饰变量的设计矩阵放置。

目标端：MTAC-IFBench 只用带 validation_code 的约束（去重 920 条：策略文件 314、首轮 97、中途按之后剩余轮数 0/1/2/3/≥4 为 89/76/83/81/180）；Workflow 与 Environment 类无脚本可判定，只在 150 条抽样上用其判官 agent 做次要分析。SWE-Together 不用反应式模拟器，而是把 oracle_intents 按原会话轮次脚本化回放，使通道与剩余轮数取自原始会话、不受方法影响；只用可确定性检查的意图（用 reference_patch 验证检查器）。

输出：逐条与"方法 × 目标"的预测与观测增益；五种预测量的误差及差的置信区间；两个目标上方法排序的预测与观测 Kendall τ；留一层可交换性检验结果。

与最高近邻的差别：BIS（2508.01203）只重加权源样本、预测模型水平；CJE（2512.11150）在目标端用 oracle 标签做校准，本方案把它对应的"目标端少量试跑"作为对照；2610.31778、CONPACT、MTAC-IFBench、Harness-IF 报告分层差异，不做跨人群的方法增益预测。

## 最小实验

规模：源端 5 对 × 80 题 × 设计矩阵 6 格 × 开/关 × 2 次，共享"关"格后约 3,000 次运行；目标端（验证）MTAC 100 实例 × 5 对 × 开/关 × 1 次约 600 个多轮会话，SWE-Together 脚本化回放 109 题 × 5 对 × 开/关 × 1 次约 650 次；共约 4,250 次。

主检验：逐条约束层面五种预测量的对数损失与平方误差，按约束、实例、方法三重自助法给 95% 区间；目标端少量试跑对照取 10 个实例并重复抽样 50 次。

可交换性：源端留一层（如留出"剩余 ≥4 轮"），用其余层的模型预测它；目标端 10 个试跑实例同时用作检验。

复现路线：aisa-group/compaction（compaction.* 配置键）、ZhiqiEliWang/compaction-integrity；HDA react_baseline.py（多轮只需把下一轮用户消息追加到 messages）；MTAC-IFBench 数据（HF thu-coai/MTAC-IFBench）与 AgentProbe 评测代码，论文报告了 OpenCode 结果；SWE-Together 任务与 tests 在其仓库，脚本化回放只需按轮次发出意图文本，不需要模拟器。

成本：约 4,250 次运行，30 路并发在 8×A100 上约 3 天；MTAC 判官次要分析与少量校准约 300 元。预研 no-go 检查：32K 阈值下源端会话的压缩触发率（若 < 50% 调低阈值）；源端 2 对、3 层、40 题上层间增益是否不同（若相同则停止），约 1 天、2×A100。

Frozen Problem Anchor and user constraints:

- **起点问题：** 方法（上下文压缩、技能、harness 演化等 agent 侧方法，而非基座模型本身）在静态 agent 基准上报告的增益，换到交互式（运行中有用户输入、信息只在对话里）、留出、过程约束口径后还剩多少；基准的结构性质能否事先预测这个保留率。
- **对象：** 方法相对其对照的增益（同一基座模型下的差值），不是模型分数或模型排名。
- **初始条件与评测：** 卡片证据来自 PaperBench / ProgramBench / PostTrainBench（压缩）、ALFWorld / LiveMath / SWE-bench Verified / CREATE（harness 演化）、技能留出迁移与安全义务基准；初始口径为终态通过率。
- **瓶颈：** 现有工作只在单一方法族内测增益是否保留（HDA、CHASE 针对 harness 演化；2610.31778、2608.11242 针对压缩），或只审计基准整体效度；跨方法族的预测关系没有检验。构造"去性质"变体可能同时改变任务难度。
- **证据边界：** 卡内多条证据只到摘要层；本轮已读 2610.31778、2610.22466、2605.10448、2607.02577、2609.18366 全文的方法与主实验，2608.11242、2606.29957 读了与本卡相关的方法与结果段落。
- **用户约束：** 预研 2×A100 80G / 4×L40 48G / 8×4090 24G；正式实验可用 8×A100 80G，最好不超过 5 天；付费 API 1000 元以内可自主决定；token 资源稀缺；目标半年内（自 2026-10 起）投主会；不做世界模型、视频生成、机器人方向。
- **进入实验规划的成功条件：** 候选通过两次独立评审门槛（三项 ≥6、其中一项 ≥7、一项 ≥8，可行性 pass，`experiment_ready`），并能在上述资源内给出判别主张的最小实验。
