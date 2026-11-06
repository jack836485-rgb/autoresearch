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
Today's date: 2026-11-06. Known tool workarounds: Shell can reach arxiv.org (abs and html pages), huggingface.co model cards via WebFetch, and can git clone public GitHub repos; the GitHub API (gh api, api.github.com) is not available in this session
Finish all searches before answering and leave no background tasks running. Do not read other
files in this workspace and do not write files, except your raw review to /home/claude/autoresearch/review-stage/bench_affordance_retention_q026_20261106/round-03-review.md (UTF-8).
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

**定位关键词：** agentic reinforcement learning；SWE-bench Verified；R2E-Gym；instruction following；multi-turn interaction；interruption

**一句话定位：** 开源编码 agent 的 agentic RL（如 DeepSWE、SkyRL 的 SA-SWE）在 R2E-Gym 这类"目标只在首条消息、运行中没有真人输入"的环境里训练，奖励只看首轮目标是否完成；本 Idea 研究这样训练出的策略在部署中是否专门学会不响应轨迹中途到来的用户指令。

**与起点问题的关系：** 邻近新问题。保留起点中的结构性质"目标固定、运行中没有用户输入"及其后果"静态分数掩盖交互使用中的失效"，但对象从"方法在静态基准上的评测增益"换成"在同结构的训练环境中 RL 得到的模型行为"。起点中的跨方法族增益保留率预测、只判终态、搜索集可穷举均未回答。

## 核心 Claim

成功后新增的东西：一个后训练层面的现象，以及它对 agentic RL 环境设计的直接含义。在固定目标、无中途用户输入的环境里做 agentic RL，会在提升 SWE 分数的同时，专门拉大"晚到差距"——同一条指令放在首轮时会遵守，在轨迹中途以用户消息给出时不遵守——而首轮遵守率和一般多轮对话中的指令遵循基本不变。这与已知的"推理 RL 损害指令遵循"（MathIF）是不同的失效：后者是整体下降，这里是按指令到达时间的选择性折扣。若成立，开源 agentic RL 的环境设计需要在训练中加入中途用户回合；把开源 SWE-RL 模型用作交互式助手时，其静态分数会高估交互可用性。

可推翻的判断：在上下文完整（不截断、不压缩）的同一 harness 中，DeepSWE-Preview 的晚到差距显著大于其基座 Qwen3-32B；训练中注入过中途提示的 SA-SWE-32B 晚到差距介于二者之间或接近基座；且 DeepSWE 的首轮遵守率与一般多轮指令遵循没有同等幅度的下降。若三者晚到差距相同，或 DeepSWE 的差异完全由首轮遵守与一般遵循的下降解释，主张不成立。

目前的依据：(1) 训练环境的结构：DeepSWE 模型卡说明它由 Qwen3-32B 纯 RL 得到，使用 R2E-Gym 约 4.5K 题，SWE-bench Verified 在 200 步 RL 中从约 23% 升到 42.2%；R2E-Gym 代码（src/r2egym/agenthub/agent/agent.py 第 491、497 行）把每步工具观察以 user 角色追加，因此训练中首轮之后的 user 消息全部是环境输出，奖励只取决于首轮目标。(2) agentic RL 侵蚀指令遵循的已知迹象：Laguna 技术报告（2605.27605）§4.3.2 指出，没有显式指令遵循监督时，agentic RL 会灾难性遗忘系统提示中的行为约束，超过一半的 agentic 任务因此零奖励；MathIF（2505.14810）发现推理 RL 与长思维链蒸馏损害指令遵循，生成越长越明显。(3) 角色标签不足以区分来源：2603.12277 显示模型按文本"听起来像谁"判断来源而非依角色标签，所以从"user 角色里出现的都是环境输出"中学到的折扣有可能落到真人消息上。(4) 天然对照：SA-SWE-32B（SkyRL-Agent 2511.16108）同样由 Qwen3-32B 在 R2E-Gym 4.5K 题上纯 RL 得到（125 步，ReAct 下 24.4%→39.4%），但训练中注入了中途提示（步数/上下文预算警告、无效工具调用纠正、重查失败编辑）。适用条件与未知：以上是相关证据，没有任何工作直接测过 RL 前后对中途用户指令的响应；DeepSWE 与 SA-SWE 在算法、步数、thinking 设置上也不同，自然实验只能给相关证据；晚到差距的大小待预研。

## 方法设计的核心思想

输入：Qwen3-32B、DeepSWE-Preview、SA-SWE-32B 三个公开权重；R2E-Gym harness；SWE-bench Verified 100 题。

动作：每题配一条与模型默认行为冲突的过程/范围指令（如"不要修改 X 文件""先写复现脚本再改源码""不要用 sed 原地编辑""只改一个文件"），用命令日志与最终 diff 确定性判定是否遵守。四种条件：无指令（得到各模型的默认行为）；指令放首轮；指令在第 k=8 步以独立的 user 消息给出；同一指令附在第 k 步的工具观察里。上下文 64K、不截断、不压缩，三模型同解码设置。只在"无指令时会违反"的题上计遵守率（反默认子集，避免把巧合当遵守），只统计第 k 步时尚未提交的轨迹。

输出：每个模型的首轮遵守率、中途遵守率、晚到差距（二者之差）及按通道（独立 user 消息 vs 附在观察里）的拆分；resolved 率单列；一般多轮对话指令遵循作为特异性对照。

与最高近邻的关键差别：MathIF 测单轮推理任务中的整体指令遵循，不区分指令到达时间；Laguna 报告的是系统提示约束的遗忘；InterruptBench、SWE-Interact、SWE-Together 比较的是不同模型在交互中的表现，没有对同一基座做 RL 前后比较，也不区分晚到折扣与整体遵循下降；Agent-RLVR、SkyRL 在训练中注入引导或提示是为了提高任务成功率，没有测它对响应用户指令的影响。

## 最小实验

主实验（只需推理）：3 个模型 × 4 种条件 × 100 题 × 2 次重复 = 2,400 次运行。主检验：DeepSWE 与基座的晚到差距之差（按题配对、题级自助法 95% 区间），以及 SA-SWE 相对二者的位置；辅助检验：首轮遵守率之差与一般多轮指令遵循之差，用来排除"整体遵循下降"这一竞争解释；thinking 生成长度作为协变量，排除 MathIF 所说的"生成越长越不遵守"；第 k 步的上下文长度分布三模型分别报告，排除位置与长度混淆。

外部复测：SWE-Together 中约 40 道带可确定性检查的中途 workflow/范围意图的题（已核验 109 题均含 tests/ 门控与 oracle_intents.json，92 题有会话中途的非提问意图），3 模型 × 2 次，约 240 次运行；结局为 tests 门控与按意图写的确定性检查；模拟器自托管（需放开 SWE-Together 代码中 vLLM 只用于 agent 席位的限制）。

因果补充（视主实验结果决定是否做）：在 Qwen3-4B 上用 rllm/SkyRL 在 R2E-Gym 子集上做两组小规模 RL，唯一差别是是否以一定概率在轨迹中途注入"用户约束"并把遵守计入奖励；比较两组的晚到差距与 SWE-bench 增益。

强对照与相同核心条件：每个 RL 检查点都与同一基座在同一 harness、同上下文上限、同步数上限、同温度下比较；SA-SWE 训练用的是 SkyRL 的 ReAct harness，因此对 SA-SWE 与基座再在其原生 harness 中复测一遍，避免 harness 不匹配造成的差异。

复现路线：DeepSWE 模型卡给出 R2E-Gym 评测配置（64K 上下文、100 步）；R2E-Gym 代码公开，注入指令只需在第 k 步向 history 追加一条消息或改写观察字符串；SA-SWE-32B 权重在 NovaSky-AI/SA-SWE-32B，SkyRL 代码公开；SWE-Together 数据与 harness 公开。

关键数据：指令与检查器需新建，约 1–2 人日；默认行为由"无指令"运行确定，若某条指令对三模型的反默认子集都太小（< 30 题），换指令。SWE-Together 意图检查器约 2 人日，用 reference_patch 验证。

成本：32B 推理 TP=2，8×A100 上 4 个副本并行，按每次约 30 分钟、每副本 4 路并发估计主实验约 2.5–3 天；外部复测约半天；模拟器自托管，API 只用于少量 rubric 一致性校准（约 100–200 元）。预研先做最便宜的 no-go 检查：DeepSWE 与基座在 50 题 × 首轮/中途两条件 × 1 次上的晚到差距（2×A100 约 1 天）；若差距为 0，停止。因果补充的 4B RL 估计 8×A100 约 3 天，只在主实验支持时做。

Frozen Problem Anchor and user constraints:

- **起点问题：** 方法（上下文压缩、技能、harness 演化等 agent 侧方法，而非基座模型本身）在静态 agent 基准上报告的增益，换到交互式（运行中有用户输入、信息只在对话里）、留出、过程约束口径后还剩多少；基准的结构性质能否事先预测这个保留率。
- **对象：** 方法相对其对照的增益（同一基座模型下的差值），不是模型分数或模型排名。
- **初始条件与评测：** 卡片证据来自 PaperBench / ProgramBench / PostTrainBench（压缩）、ALFWorld / LiveMath / SWE-bench Verified / CREATE（harness 演化）、技能留出迁移与安全义务基准；初始口径为终态通过率。
- **瓶颈：** 现有工作只在单一方法族内测增益是否保留（HDA、CHASE 针对 harness 演化；2610.31778、2608.11242 针对压缩），或只审计基准整体效度；跨方法族的预测关系没有检验。构造"去性质"变体可能同时改变任务难度。
- **证据边界：** 卡内多条证据只到摘要层；本轮已读 2610.31778、2610.22466、2605.10448、2607.02577、2609.18366 全文的方法与主实验，2608.11242、2606.29957 读了与本卡相关的方法与结果段落。
- **用户约束：** 预研 2×A100 80G / 4×L40 48G / 8×4090 24G；正式实验可用 8×A100 80G，最好不超过 5 天；付费 API 1000 元以内可自主决定；token 资源稀缺；目标半年内（自 2026-10 起）投主会；不做世界模型、视频生成、机器人方向。
- **进入实验规划的成功条件：** 候选通过两次独立评审门槛（三项 ≥6、其中一项 ≥7、一项 ≥8，可行性 pass，`experiment_ready`），并能在上述资源内给出判别主张的最小实验。
