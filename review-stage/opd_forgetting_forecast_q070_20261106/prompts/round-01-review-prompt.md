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
files in this workspace and do not write files, except your raw review to /home/claude/jack836485-rgb/autoresearch/review-stage/opd_forgetting_forecast_q070_20261106/round-01-review.md (UTF-8).
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

**定位关键词：** on-policy distillation；catastrophic forgetting；teacher selection；KL divergence；Fisher information；token perplexity

**一句话定位：** 在策略蒸馏（OPD）后训练中，学生在训练域（数学）之外的通用能力遗忘随教师来源大幅变化，本工作研究能否在训练开始前跨教师来源预测这一遗忘，以及预测量揭示的遗忘来源。

**与起点问题的关系：** 原问题的扩展。保留对象（OPD 学生相对基座的 OOD 能力变化）、条件（同一学生基座与配方、只换教师）和“外部大教师与由学生基座训出的 SFT/RLVR 教师落在同一条预测曲线上”的目标；把起点设想的单一静态量（冻结教师在 OOD 前缀上相对学生基座的 KL）放进一组分层对手中比较，并加一个位置归因的干预。起点问题中“它是否强于教师 OOD 损失与教师不确定性表达率”作为其中一项对比直接回答；起点只在数学训练域上提出，本工作也只覆盖数学训练域。

前提证据：OPDArena（arXiv 2610.25651）在同一基座、同一配方下只换教师，学生 OOD 变化从 −4.14 到 +0.75 pp（Table 1，Qwen3-8B），且 OOD 能力更强的大基座教师带来更多遗忘与更高的 OOD/域内变化比 ρ（Table 2：1.998 vs 自身 RLVR 教师 0.131）；把大 SFT 教师换成只保留其后训练增量的构造教师，学生 OOD JS 由 0.99 降到 0.79、OOD 由 −0.69 变为 +0.39（Table 3）。训练前量目前只有零星证据：在基座前缀上取初始更新方向并校准域内变化后的局部 ρ，排序与训练后一致（Table 18：0.611 vs 0.074；训练后 Table 14：0.658/0.879 vs 0.088），但只覆盖 2 个学生 × 3 个构造教师、预测的是 ρ 而非遗忘量；教师侧静态比值 ρ_T 只有定义（§G.3 Eq. 30），无数值、未与遗忘相关；SFT/RLVR 教师回答在基座下的打分差能区分两类教师（Table 11：0.678 vs 0.136 nats/token），未覆盖外部教师。已知反面证据：首位置（"Okay/Alright" 开头）反馈置零只改域内、不改 OOD（Table 12，OOD 差 ≤0.53 pp）。

## 核心 Claim

若主结果成立，本工作给出 OPD 的第一个**训练前遗忘预测量**及其判别性解释：OPD 学生的 OOD 遗忘不由冻结教师与学生基座之间的静态分布距离决定（无论在 OOD 前缀还是域内输出上测），也不由教师自身的 OOD 能力或不确定性表达率决定，而由**教师反馈在学生自身 rollout 上诱导的初始更新方向对 OOD 预测的跨域干扰**决定——这一量只需一次反向传播即可在训练前测得，并能让外部大教师、外部后训练教师与由学生基座训出的 SFT/RLVR 教师落在同一条单调曲线上。进一步，把该干扰按位置类别分解，可判断它主要来自风格位置还是内容位置的反馈，并由掩码干预检验。它新增的可用之物是：跑 OPD 之前按“保留”这一轴筛教师，与按“收益”筛教师的已有方法互补。

可推翻的判断：（H1）静态距离类量（OOD 前缀 KL/JS、ρ_T、域内教师输出困惑度）在单一教师类别内可以排序，但跨类别（外部 vs 自训）不能同线；（H2）单批探针干扰量在留一类教师外推中的秩相关与误差显著优于全部静态量与教师 OOD 损失，并接近 20 步早期检查点参照；（H3）若风格位置分量占探针干扰的大部分，则只掩风格位置反馈应显著减少遗忘，而掩等量内容位置反馈不减。H1–H3 任一被推翻都直接改写结论（例如静态 OOD KL 胜出即支持起点设想，域内困惑度胜出即说明 SFT 的困惑度规律迁移到 OPD）。

当前依据与适用条件：H2 的机制依据是 JS 的局部二次展开（OPDArena Eq. 23–24：小步更新下 OOD/域内 JS 之比等于更新方向在两域预测 Fisher 下的能量比），以及持续学习中训练前由跨任务核预测遗忘的结果（arXiv 2606.18024，线性化/PEFT 下精确）；经验依据是上述 Table 18 与 Table 14 的排序一致。H1 的依据是 Table 2/3：大基座教师静态差异大、学生早期几乎不动，SFT 教师静态差异与遗忘方向却一致。未知：探针方向能否代表 300 步路径（OPDArena Fig. 5 显示 Self-OPD 学生偏离“基座–教师”参数直线）；外部指令/推理后训练教师的行为；风格归因目前只有观察证据（arXiv 2611.07722：风格位置逐 token 平均师生 log 概率差是数学位置的 3.5 倍，但未测遗忘），且 Table 12 是部分反证。效果大小（各量秩相关多高）待预研。

## 方法设计的核心思想

输入：学生基座 p0、冻结教师 q、少量训练题与 OOD 提示。三层预测量都在训练开始前（或极早期）计算：

- **Tier 0 静态量**（只需前向）：OOD 前缀上 KL(q‖p0)、KL(p0‖q)、JS 与 ρ_T；教师 OOD 损失（教师与 p0 在同一 OOD 评测上的金标对数似然差）；教师认知标记率（2603.24472 的 10 个标记）；**对照①**域内基线预测量——教师在训练题上的输出在 p0 下的困惑度、教师自评校正后的打分差、p0 下 PPL≥2.5 的 token 比例（2501.14315）；**对照②**在 p0 的域内 rollout 与 OOD 前缀上按风格/内容位置分别计算逐 token |log q − log p0| 与 KL（2611.07722 的类别规则），同时报逐 token 均值与按 token 数加权的总量；收益侧预测量 ESC 与 Overlap@16（2610.39020）；教师新增概率质量落在学生 Top-16 之外的比例（OPDArena §D.5）。
- **Tier 1 单批探针**（一次反向）：在 256 条 p0 的域内 rollout 上用 OPD 配方的教师反馈求损失梯度 g；沿 g 取步长 ε，二分使校准前缀上域内 JS 达到固定小值；在独立的 OOD 前缀上测 OOD JS 与金标对数似然变化，得到探针干扰量；再把反馈只保留风格位置或只保留内容位置分别重算，得到两个分量。
- **Tier 2 参照**：同一 OPD 运行第 20 步的 OOD JS 与金标似然变化（早期检查点外推，非训练前）。

与最高近邻的关键差别：OPDArena 只在 2 个学生 × 3 个构造教师上算局部 ρ 并与训练后 ρ 比较，没有预测遗忘量、没有外部后训练教师、没有与静态量对比；ESC 只预测域内收益；RL's Razor 的 KL 在训练后测；2501.14315 只在 SFT 上做数据侧困惑度干预。本工作把“训练前预测遗忘”定为任务，用分层对手区分三种解释，并用位置掩码给出因果检验。

## 最小实验

**学生与教师。** 学生 Qwen2.5-1.5B-Base（S1）与 Qwen3-1.7B-Base（S2）。S1 的 11 个教师：外部大基座 Qwen2.5-7B、Qwen2.5-14B、Qwen3-8B-Base；外部数学基座 Qwen2.5-Math-7B；外部后训练 Qwen2.5-7B-Instruct、Qwen2.5-Math-7B-Instruct、DeepSeek-R1-Distill-Qwen-7B（词表兼容性在预研中先核对，不兼容即删）；由学生基座训出的 RLVR 教师 hkust-nlp/Qwen-2.5-1.5B-SimpleRL-Zoo（公开，零 RL 训自 Qwen2.5-1.5B）与自训 SFT 教师（OpenR1，OPDArena 配方）；两个 logit 缩放构造教师 p0·(q/p0)^0.5（对 Qwen2.5-7B 与自训 SFT 各一）。S2 的 8 个教师：Qwen3-4B-Base、Qwen3-8B-Base、Qwen3-4B-Instruct-2507、Qwen2.5-Math-7B、自训 SFT、自训 200 步 GRPO 教师、两个缩放构造教师。OPDArena 已用 Qwen2.5 学生配 Qwen3 教师训练（Table 1），两家族常规 token 共享。

**训练与遗忘标签。** 用 OPDArena 公开代码（github.com/StellarCurtain/OPDArena，`opdarena.train --method opd/self-opd/sft/rlvr`；SFT/RLVR 教师检查点未发布，故自训）按其 Table 7 配方：OpenR1-50K（官方下载器复现其选择与顺序）、lr 1e-6、每步 64 题 × 4 回答、学生 Top-16 支持与学生概率加权、KL 0；为控制成本把响应上限从 7168 降到 4096、步数从 780 降到 300（预研按遗忘是否已可分辨再定）。所有教师共用同一配方与数据顺序，只换教师。遗忘在第 300 步测：HellaSwag/ARC-C/MMLU 全量候选似然（10,042/1,172/14,042 题），TriviaQA/NQ-Open 各 2,000 题，BBH 27 任务各 50 题，IFEval 全 541 题。**主指标**为金标答案对数似然相对基座的平均变化（连续、低方差），**次指标**为 7 任务准确率宏平均（与 OPDArena 可比）。另训 3 个重复种子估计训练噪声。OPDArena 原评测子集（HellaSwag/ARC 各 256 题）对 1–2 pp 的组内差分辨力不足，这是扩大评测与改用连续主指标的原因。

**比较与判定。** 每个学生内对教师做 Spearman/Kendall 秩相关；“同一曲线”用留一类教师外推检验：在自训 SFT/RLVR 与构造教师上拟合单调映射，预测外部教师（反向再做一次）的遗忘，报秩相关与平均绝对误差，教师层面与评测题层面双重 bootstrap 给 CI。H2 成立的判据：Tier 1 在两个学生上的留一类秩相关都高于每一个 Tier 0 量且 CI 不重叠于最好的 Tier 0 量；否则按胜出的量改写结论。

**位置归因干预（H3）。** 对 S1 上遗忘最大的外部教师与自训 SFT 教师各跑两次 300 步 OPD：一次把风格位置的反馈置零，一次把随机抽取、反馈绝对值总量相同的内容位置置零；比较 OOD 遗忘与域内收益。风格/内容按 2611.07722 附录 C.2 规则独立实现（其代码 aim-uofa/sd-opd 只含训练代码、未发布词表，已核验），先在 S1 与一个指令教师上重现“风格/数学逐 token 均值比约 3–5 倍”作检查；OOD 前缀上“内容”定义为非风格、非空白、非标记 token。

**基线与复现路线。** 静态距离：OPDArena `analysis.prefixes`/`analysis.distributions --teacher`（已核验文档与脚本）。单批探针：发布代码中无此脚本，按 OPDArena §G.2（Eq. 22–24 与“校准到相同域内 JS、在独立前缀上测”）独立实现，约百行。ESC/Overlap@16：github.com/maybenotime/opd-esc（`verl_opd/plugins/k1_probe/k1_probe.py`，已核验）。困惑度、打分差与认知标记率按原文公式与标记表实现。早期检查点外推为标准做法。训练后 OOD JS（Razor/OPDArena 的事后量）作为上界参照。

**算力。** 预测量全部计算约 6 GPU·h（每教师若干次前向 + 一次反向）。OPD：S1 每步约 256 条 × 平均约 1.5k token，估计 2×A100 上 1.5–2 分钟/步，300 步约 8–10 h；14B 教师偏上限。正式实验约 19 个教师运行 + 3 个种子重复 + 4 个掩码运行 = 26 次，约 450–520 GPU·h；SFT 教师两个约 15 GPU·h，GRPO 教师约 12 GPU·h；合计在 8×A100 × 5 天（960 GPU·h）内。预研（2×A100）先只算 S1 全部预测量（不训练），若各量对 11 个教师的排序几乎一致则实验无法判别、即停；否则在两类量分歧最大的 4 个教师上各跑 150 步并加 1 个重复种子（约 24 h），遗忘跨度不足种子标准差 3 倍即调整步数或停。无付费 API 与人工标注。

Frozen Problem Anchor and user constraints:

- **起点问题**：OPD 中，学生在训练域（数学）之外的能力遗忘随教师来源变化很大；能否只用训练开始前可测的量（冻结教师、学生基座、少量前缀/rollout）预测这个遗忘，并让外部大教师与 Self-OPD（SFT/RLVR）教师落在同一条预测曲线上。
- **对象**：OPD 学生（Qwen 系基座模型）与冻结教师；遗忘 = 学生 OOD 通用能力相对基座的变化。
- **条件**：同一学生基座、同一训练数据与 OPD 配方（在策略采样 + 逐 token 反向 KL / 学生 Top-k 支持），只换教师。
- **初始任务/评测**：OPDArena 设置——OpenR1 数学训练；域内 AMC23/AIME24/AIME25/HMMT25/Math500；OOD HellaSwag/ARC-C/MMLU/IFEval/TriviaQA/BBH/NQ-Open。
- **瓶颈**：已有关联（Razor 的 KL、OPDArena 的 OOD JS）都在训练后测；训练前的教师侧量（ρ_T、域内打分差、初始方向局部 ρ）只有定义或零星数值，没有跨教师来源的定量检验。
- **证据边界**：只有数学训练域；Qwen 两个家族；OPDArena 外部教师组内遗忘差 1–2 pp、两种子平均、无 CI。
- **用户约束**：不做世界模型/视频/机器人；正式实验 8×A100 80G，最好 ≤5 天；预研 2×A100；付费 API ≤1000 元可自主；token 资源稀缺；目标半年内投主会。必须保留两个对照：① 域内基线预测量（教师在域内提示上的输出在学生基座下的困惑度，参照 2501.14315）；② 逐 token KL 按风格位置与内容位置拆分（参照 2611.07722）。
- **进入实验规划的成功条件**：给出一个可在上述算力内完成、能区分“静态分布距离 / 教师 OOD 损失 / 不确定性表达率 / 域内困惑度 / 其他训练前量”谁预测 OPD 遗忘的最小实验，且遗忘测量的分辨力足以区分结论。
