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
Today's date: 2026-11-06. Known tool workarounds: GitHub REST API may return 403; use 'git clone --depth 1' or 'git ls-remote'. arXiv HTML pages (https://arxiv.org/html/<id>v1) are reachable with curl for full text; HF model refs via https://huggingface.co/api/models/<repo>/refs. Python with numpy is available for checking derivations.
Finish all searches before answering and leave no background tasks running. Do not read other
files in this workspace and do not write files, except your raw review to /home/claude/jack836485-rgb/autoresearch/review-stage/random_reward_learner_q004_20261106/round-05-review.md (UTF-8).
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

**定位关键词：** spurious rewards；random rewards；RLVR；GRPO；clipping bias；policy entropy

**一句话定位：** 在随机/虚假奖励 RLVR 中，为什么同一随机奖励信号对同族不同检查点（学习者）、不同训练设定给出相反结果，且单次运行常远超起点。

**与起点问题的关系：** 原问题：保留 OLMo-2-1124-7B 预训练末（P1）与 mid-training（P2）检查点、合成 GSM 与 2610.01066 的训练协议，回答“学习者一侧由什么决定随机奖励的效果”，并解释其单次运行的高尾；裁剪生效、每批多次更新的设定只在 LoRA 内用一个真实小批量 PPO 臂检验“集中”方向；不主张解释 Qwen2.5-Math 的提分（2506.10947 Table 2 显示该设定下有约定内提升：“代码→代码”占增益 11.6%、“语言→语言”占 21.4%），也不复现全参数大批量实验。不回答 mid-training 数据的哪部分造出了检查点的输出约定。

前提证据（均已读原文）：2610.01066 Table 1 中两个学习者收到同一缓存 rollout 与同一随机奖励，P2 宽松准确率 13.5→27.2、P1 2.5→5.4；其正文说明 P2+5B 在线随机奖励均值 +26.8 来自 8 个种子中 4 个达到 59.0–77.5% 的运行（其余在起点附近或更低），P2+50B 上 32 个种子 3 个增益、15 个崩到 ≤5%（Table 17）；Table 7 中 15 个宽松 ≥50% 的随机运行严格分几乎全为 0、多数格式率为 0（例如“84 − 24 = $60”式短答，不写 `####`）；§11.7 中 P2 输出里 `####`/`\boxed` 比例从 93.5% 降到约 50%；Table 22 前缀评分下 P1 从 41.5% 降到 21–29%、P2 从 14.5% 升到约 39%。2506.10947 §4.4 与附录 B.2 报告：开裁剪时随机奖励使 Qwen2.5-Math 的代码推理比例上升并提分，关裁剪时运行“极度随机、偶有高分”；该文与 Olmo 3（2512.13961）在全参数大批量设定下随机奖励对 OLMo 基本持平。

## 核心 Claim

若成立，新增的认识是：在每批 rollout 只更新一次、裁剪基本不生效的随机奖励训练中，一次运行相当于在检查点的**输出约定**（如“`####` 行后停止”“答完续写一道新题”“自然语言作答后停止”“写到上限被截断”）之间做一次抽签并定下来；该运行的准确率约等于它所定约定在冻结检查点采样中的**条件准确率**，RL 并不在约定内部增加解题能力。抽签概率不是中性的：在 logit 参数化下随机奖励的二阶漂移压低主导约定、抬高中等质量的约定，所以“胜出”频率比初始采样质量更平。由此，学习者效应＝检查点采样分布里有没有质量不可忽略的高准确率约定（P2 有、P1 没有）；高尾＝定在这种约定上；P1 在前缀评分下变差＝从它准确的主导约定被压到别处。开裁剪且每批多次更新时，裁剪使策略向高先验集中（2512.16912 定理 4.3），预计主导约定胜出更多，方向相反。可用的东西是：从冻结检查点的采样就能在训练前读出随机奖励结果的整个分布（均值、崩溃率、高尾），以及判断一次随机奖励“增益”是否只是换了输出约定的逐运行检验。

依据：对直接 logit 参数化、组内标准化的随机优势（方差 c，组大小 G，步长 η），一阶期望更新为零，二阶期望漂移为 E[Δp_m]≈(η²c/G)·p_m·[(½+Σp²)(p_m−Σp²)−(3/2)(p_m²−Σp³)]（由 softmax 二阶导对更新协方差 η²c/G·(diag p−ppᵀ) 求迹得到，已用数值二阶导核对）；方括号是 p_m 的开口向下二次式，主导模式为负、中等质量为正、极小质量近似为零。表格模拟（3 个模式、G=4、组内标准化与否两种、各 400 次）：初始 0.6/0.3/0.1 时，策略最终集中（最大概率均值约 0.94），各模式胜出频率约 0.50/0.34/0.15（标准误约 0.025），比初始质量更平；p 空间 Wright–Fisher 近似会预测 0.6/0.3/0.1。与之相邻的理论是 2512.16912 定理 4.1：对 softmax、无裁剪随机奖励给出二阶熵漂移，偏斜策略的熵上升——与“主导模式被压低”方向一致；本 Idea 的增量在于各模式的定局概率、把模式落到输出约定，以及运行级预测。2610.01066 的双峰终点（P2+5B 八个种子 17.5/5.0/67.5/59.0/2.5/77.5/77.0/16.0）、高分运行一律换掉答案约定、P1 前缀分下降，与这一图景一致。共享参数下压平能否保持没有直接依据；本 Idea 的理由是约定在少数分叉 token 上决定（给出答案后接 `\n####`、EOS 还是 `\nQuestion:`），这些位置的选择基本与题目内容无关，等效于跨题共享的低维 softmax——这一前提在冻结采样中可直接检查（分叉 token 分布的跨题方差）。尚未知：Adam 与 LoRA 下压平的幅度；输出约定的规则划分是否稳定；约定内是否还有能力变化（由判断 1 检验）。

可推翻的判断：(1) 逐运行：随机奖励终点的贪心准确率落在“该运行所定约定”在同一题集上的两个冻结参照之间——下界为 T=1 采样中该约定的条件准确率（策略未变尖），上界为该约定内逐题多数投票的准确率（策略完全变尖），另报 T=0.3 采样的条件准确率；系统性高于上界才说明约定内能力增加（三种评分都检验）；(2) 约定胜出频率比初始采样质量更平（不是成正比，也不是更集中）；(3) 由冻结采样约定质量与约定内准确率经表格压平映射得到的终点分布，预测各检查点的均值、崩溃率与高尾，好于“中性固定＋同样的约定内准确率”，也好于起点准确率/错配模型、首段分数与格式率；(4) 真实小批量 PPO（每缓冲区 16 题×4 条、8 次 mini-batch 更新）下，开裁剪使主导约定胜出频率高于其质量，关裁剪则回到压平。

## 方法设计的核心思想

输入：检查点；训练采样器（温度 1、top-p 0.95、96 token）；200 道保留题；三种评分（宽松＝论文主评分；严格＝独立 `#### <number>` 行；首段＝截到第一个 `\nQuestion:`，即 Table 22 规则）；预先登记的约定划分规则（是否有 `####` 行、答后是否续写新题、是否以自然语言陈述答案后结束、是否在上限处截断且无答案、其他），用训练器已有的回答特征加两条规则实现，并用回答嵌入聚类作稳健性检查。

动作：(a) 冻结采样：每题 64 条（T=1）与 16 条（T=0.3），得到每个约定的质量 p_c、逐题条件准确率与约定内多数投票答案，以及答案后分叉 token 的跨题分布；(b) 预测：用表格模拟把 p_c 映射成胜出概率 q_c（同 G、同组内标准化），预测终点分布为 Σ_c q_c·δ(acc_c)；(c) 逐运行检验：对每个随机奖励运行的终点贪心输出做同样分类，取其多数约定，看运行准确率是否落在该约定在同一批题上的“采样条件准确率—多数投票准确率”区间内；(d) 胜出频率与 p_c 的关系，分压平/中性/集中三种假说比较。

与最高近邻的差别：2610.01066 把增益读作“可达性”，其 §9.4 只指出二阶项符号不定；2601.04411 用一阶均值场，把随机奖励（J=0）称为中性，并在 p 空间加 Wright–Fisher 型噪声（隐含固定概率＝初始质量）；2512.16912 定理 4.1 给出同一二阶展开对熵的作用，定理 4.3 讲裁剪降熵；2506.10947 讲裁剪偏置放大高先验行为。本 Idea 把二阶漂移落到各模式的定局概率（压平），把对象从熵或参数邻域换成“输出约定的抽签”，并给出可逐运行检验的预测。

## 最小实验

模型与数据：HF `allenai/OLMo-2-1124-7B`（965 个分支已用 HF refs API 核实；论文用的 revision 在 `mynotwo/rl-random-prob/configs/olmo2_checkpoints.json`）、OLMo-3-7B O3/O4（2610.01066 Table 4 的 revision，已在 HF refs 核实）；数据为仓库 `src/data/synthetic_gsm_rlvr_1000_seed13.jsonl`，800/200 划分（split seed 777）。

主实验：8 个检查点（P1 末、P1 3,272B、ingredient1 的 P2+5B/+13B/+42B/+50B、O3、O4）做冻结采样；同 8 点各 16 种子在线随机奖励运行，用已核验训练器 `src/trainer/rlvr_probe_v2_fixedsplit.py`（lr 3e-5、G=4、每步 1 题一次更新、参考项 0.01、LoRA r8、500 步，与论文一致；评测逐题 `outcomes` 已保存，需加一行保存全部输出文本）。预先登记：在运行前写下 ingredient2/3 的 P2+5B、+21B 共 4 个检查点由冻结采样得到的预测终点分布，再各跑 16 种子。裁剪臂：现有 `--accum_steps/--ppo_epochs` 是跨步累积，实现不了缓冲区小批量，所以另写约 80 行的缓冲区 PPO 循环（复用训练器的采样、对数概率与损失函数）：每缓冲区 16 题×4 条，计算并固定旧对数概率，打乱后分 8 个 mini-batch 各更新一次，共 125 个缓冲区（2,000 题次）；在 P1 末与 P2+5B 上开/关裁剪各 8 种子。离线臂：用共享 rollout 训练器（`src/shared_rollout/`，AdamW wd=0、无参考项、无裁剪）复现 Table 1 的 P1/P2 四格各 8 种子，检验离线时约定是否取自 rollout 来源。漂移对照：P2+5B 上零奖励（`--reward_mode zero`，只剩参考项与默认 0.01 衰减）8 种子，检验换约定是否来自正则项。

竞争预测与对照：中性固定（胜出概率＝初始质量，2601.04411 的隐含预测，配同样的约定内准确率）；集中（主导约定胜出更多，裁剪偏置/熵最小化）；起点准确率与 32 次采样正确率代入 2512.16912 式(9)；首段分数与格式率（2610.01066 Table 16/22 规则）。判别统计：(1) 用逐运行的“运行准确率−其约定冻结条件准确率”的分布与零比较（共约 200 个运行）；(2) 胜出频率对 p_c 的回归斜率与 1 比较；(3) 预测终点分布与实际的 Wasserstein 距离，按检查点 bootstrap 比较各预测。

推翻条件：运行准确率系统性高于其约定的多数投票上界（说明约定内能力在变）；分叉 token 分布跨题差异很大（共享低维 softmax 前提不成立）；胜出频率与初始质量成正比或更集中；冻结采样中 P2 不存在质量 ≥ 几个百分点的高准确率约定；裁剪臂方向不反转。

算力：在线运行约 40 分钟/80G 卡（仓库 README，H100 计），离线运行约 0.3 H200 小时（论文 §11.7）。主实验 128＋预登记 64＋零奖励 8 个运行约 145 A100 小时，裁剪臂 32 个运行（125 个缓冲区×64 条采样＋8 次更新，约为基础运行的 3–4 倍）约 100 A100 小时，离线 32 个运行约 15 A100 小时，冻结采样（12 个检查点×200 题×80 条×96 token）约 6 A100 小时；合计约 265 A100 小时，8×A100 约 1.5 天；检查点逐个下载用完即删。无付费 API、无人工标注。预研（2×A100，约 4 小时）：先只对 P1 末与 P2+5B 做冻结采样与约定分类——若 P2 采样中没有任何质量 ≥3% 且条件宽松准确率 ≥50% 的约定，就无法解释 59–77.5% 的高尾，直接 no-go；通过后再跑 P2+5B 4 个保存输出的随机奖励运行，看高分运行所定约定的冻结条件准确率是否与其分数相符。

Frozen Problem Anchor and user constraints:

- 起点问题：在随机奖励 RLVR 中，什么学习者一侧的属性决定同一随机奖励信号能否提高任务准确率；2610.01066 的 OLMo-2 P1/P2 对比显示同 rollout 同奖励下结果相差数倍。
- 对象：base 检查点（尤其 OLMo-2-1124-7B 预训练末 P1 与 mid-training P2 系列检查点），独立 Bernoulli(1/2) 随机奖励下的 GRPO 式更新。
- 条件：2610.01066 的协议（合成 GSM、96 token 上限、LoRA r8、每步 1 题×4 条、500 步、贪心评测、宽松抽取）；对照条件为 2506.10947 / Olmo 3 的大批量在线 GRPO（全参数、每批多次更新、长回答、MATH-500）。
- 初始评测：合成 GSM 200 题保留集的贪心准确率（宽松/严格/首段三种评分），可扩展到 MBPP、组合查找。
- 瓶颈：已有三类解释（rollout 质量/错配、裁剪与熵、污染与记忆）都不能解释同 rollout 同奖励下的学习者差异；2610.01066 的“可达性”只是命名；且其 Table 22 显示该差异对评分口径极敏感，2506.10947 与 Olmo 3 在大批量设定下得到相反结论。
- 证据边界：主要证据来自单一模型家族（OLMo-2）、合成算术、短回答上限；高分运行依赖宽松抽取；2610.01066 的 P1/P2 离线对比无裁剪、无参考项、无权重衰减，与其在线扫描并不完全一致。
- 用户约束：不做世界模型、视频生成、机器人；正式实验 8×A100 80G、≤5 天；预研 2×A100；token 资源紧张；付费 API 1000 元内可自主；目标半年内（自 2026-10 起）投主会。
- 进入实验规划的成功条件：候选有清楚的独立贡献；最小实验能在上述算力内区分主要竞争解释（学习者“可达性”、错配/rollout 质量、裁剪偏置、输出呈现漂移）；所需检查点、代码与数据可得并已核实。
