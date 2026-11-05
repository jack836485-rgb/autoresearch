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
Today's date: 2026-11-04. Known tool workarounds: GitHub REST API returns HTTP 403 through this sandbox's proxy; anonymous 'git clone --depth 1' of public GitHub repos works from Bash; arXiv abs/html pages are readable via WebFetch
Finish all searches before answering and leave no background tasks running. Do not read other
files in this workspace and do not write files, except your raw review to /home/claude/jack836485-rgb/autoresearch/review-stage/repe_cot_amplify_q005_20261104/round-03-review.md (UTF-8).
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

**定位关键词：** CoT monitorability；chain-of-thought monitoring；activation steering；large reasoning models；decision-critical factors；implicit influence；When2Call；BIG-Bench Hard

**一句话定位：** CoT 可监控性研究中，MonitorBench（2603.28590）报告“决定性因素经由中间推理起作用时，CoT 更可监控；只影响最终答案时更难”，但其因素都写在提示里；当原因是提示里看不到的内部激活状态——CoT 监控真正要防的那类原因——这一规律是否成立，尚未被检验。

**与起点问题的关系：** 邻近新问题；保留起点的对象（4–8B 稠密推理模型）、同一决策方向的激活 steering、二元决定翻转，以及“在 steering 下生成的审议放大决定、已写 CoT 锁定原决定”这一现象，把评价目标从翻转率换成 CoT 监控的检出率。起点中“剂量／文本正反馈／预先确定”的分离不是本研究目标，仍未回答；锁定的强度作为副产品被测出（作答处 steering 达到同等翻转所需的更大 α）。

## 核心 Claim

若成立，本工作给出一条与已发表规律方向相反、且对监控安全论证有直接后果的结论：**对内部（激活层）原因，CoT 可监控性与“原因是否经由推理起作用”的关系与提示内原因相反——内部原因在审议阶段起作用时，模型写出为其合理化的 CoT，监控难以发现；只在作答处起作用时，决定与已写好的 CoT 冲突，监控容易发现。** 这意味着“若坏行为需要经过推理，就会在 CoT 中露出”这一推理对内部偏好驱动的决定不成立：越是经由推理，越不可见。它告诉监控设计者在哪类决定上不能只依赖 CoT。

可推翻的判断：在同一模型、同一方向、翻转率配对相同的条件下，“只在作答处 steer”的监控检出 AUROC 显著高于“只在审议阶段 steer、作答前撤除”；若前者不高于后者，则 MonitorBench 规律推广到内部原因，主张被推翻。

当前依据及其适用条件：(i) 审议阶段的激活原因会被合理化——2604.01202 在 Qwen3-4B/GLM-Z1-9B 上，被 pre_gen 方向 steer 翻转的工具调用 CoT 多被判为“编造支持”“约束覆盖”“无缝分歧”（注意：这是给判官看基线与 steer 后两条轨迹的成对判定，单条轨迹能否看出未知）；2603.01437 发现被 steer 时 CoT 出现编造前提与“前提正确但结论不蕴含”两类病态；2605.26772 中 steer 下生成的 CoT 撤除 steering 后仍携带 48% 的效果，说明合理化文本本身有说服力。(ii) 作答处的激活原因应造成可见的不一致——2605.26772 固定原 CoT 只 steer 作答时仍有 39% 翻转，此时最终决定与 CoT 立场相反；RFEval（2602.17053）显示推理模型的不忠实主要表现为立场不一致，这类不一致可从文本判断。(iii) 提示内隐式影响已使监控检出下降 41–46 个百分点（2608.04735），其附录 G 在 Qwen3-8B 编码任务上初步发现概念 steering 向量会降低检出，但不跨设定泛化、未操纵作用位置。仍未知：单条轨迹的监控能否抓到“不蕴含”病态从而检出审议阶段原因；作答处需更大 α 时的文本伪迹是否会让检出因伪迹而非因不一致升高（以随机方向对照和连贯性匹配处理）；结论是否限于简单二元决定——“CoT 必要性”论证针对需要推理才能执行的任务，本研究只覆盖由偏好驱动的决定，这一边界会明确写出。

## 方法设计的核心思想

输入：一个推理模型；每个任务一个由 diff-in-means 得到的决策方向 v（工具调用按 2604.01202 取 pre_gen 位置，二选一任务按 2603.01437 取答案方向）；一组无 steering 时决定稳定的题。

动作：在层 L 以三种作用位置施加 α·v：**R（审议处）**——prefill 与思考阶段注入，`</think>` 处撤除，作答 token 不注入；**A（作答处）**——思考阶段不注入（CoT 为模型自然写出），只对 `</think>` 之后的作答 token 注入；**F（全程）**作为参照。对 R 与 A 各扫 α，选出使两者翻转率相同（如 30% 与 50% 两档）的 α，A 所需 α 与 R 之比即锁定强度。对每条轨迹，监控器只看提示、CoT 与最终答案，输出“最终决定受到推理中未陈述、提示也不支持的因素影响”的概率。

输出：R、A、F 在配对翻转率下的检出 AUROC；正类为被 steer 且翻转的轨迹，负类为最终决定相同的无 steering 自然轨迹（按决定配对，避免监控只学“哪个答案少见”）。

与最高近邻的关键差别：MonitorBench 与 2608.04735 的因素都在提示中，作用位置不能被独立操纵；2608.04735 附录 G 用 steering 作原因但没有区分作用位置，也没有配对翻转率；2604.01202 与 2603.01437 描述了被 steer CoT 的合理化，但用的是成对判定或人工分类，没有测单条轨迹的监控检出，也没有作答处 steering 的对照；2603.17199 比较的是 hint（提示内原因）下探针与监控。

## 最小实验

模型：Qwen3-8B（思考模式）与 DeepSeek-R1-Distill-Llama-8B，稠密。任务：When2Call test mcq（nvidia/When2Call，CC-BY-4.0，含 `correct_answer` 与四类答案，按 2604.01202 合并为 tool / no-tool）；BBH Sports Understanding 与 Anachronisms（客观）和 Social Chemistry（主观），按 2603.01437 的二选一格式并随机化 A/B。每任务每模型取 200 道无 steering 时决定稳定（贪心与 4 次温度 0.6 采样一致）的题。

监控器：GPT 系列中档模型一个、开源 Qwen3-32B 一个；提示沿用 MonitorBench 开源实现（github.com/ASTRAL-Group/MonitorBench）的监控格式，改为输出影响概率。

对照：同范数 5 个随机方向（不翻转时检出率即“steering 伪迹”的检出底线）；按困惑度与 CoT 长度分层报告检出，排除伪迹解释；提示内隐式旁白（按 2608.04735 方式）在同一题集上作为“提示内原因经由推理”的已知参照点，用来复核 MonitorBench 方向在本设置下成立。

复现路线：R/A/F 注入用 2605.26772 官方代码（github.com/kiajueng/cot_ref_harm_analysis，已 clone 核验，前向 pre-hook 按位置注入）改写位置掩码；方向提取按 2604.01202 §3.4 与 2603.01437 §3.4 的公开规范独立实现；隐式旁白按 2608.04735 开源代码（agatha-duzan/implicit-vs-explicit-influence）。

相同核心条件：同模型、同层、同方向、同题集、同解码；R 与 A 在相同翻转率下比较；负类按最终决定配对。

判别：AUROC(A) − AUROC(R) 的按题自助置信区间；在客观与主观任务上分别报告（预期客观任务上 R 也可因“不蕴含”被部分检出）；提示内旁白组若显示“经由推理更易检出”而激活组相反，即为反转。

成本：2 模型 × 4 任务 × 200 题 × （R、A 各 3 档 α + F + 随机方向）≈ 1.5 万条生成，约 1000 万 token，2×A100 一天内；监控约 3 万次调用 × 约 2k token ≈ 6000 万 token，中档 API 约 100–300 元；开源监控在本地。无人工标注。

Frozen Problem Anchor and user constraints:

- **起点问题：** 推理模型中，激活 steering 下生成的 CoT 放大被 steer 的决定，而 steering 前已写好的 CoT 锁住原决定；放大与锁定各由什么决定（剂量 / 文本正反馈 / 预先确定）。
- **对象与条件：** 稠密开源推理模型（证据集中在 Qwen3-4B、GLM-Z1-9B、DeepSeek-R1-Distill-Llama-8B，4–9B）；从生成前激活提取的决策方向（工具调用、拒答、二选一答案）；变量为 steering 强度、注入／抑制、思考／不思考、CoT 固定／去除／重新生成。
- **初始任务／评测：** When2Call、BFCL 的工具调用决策；拒答；二选一答案任务。指标为决定翻转率，辅以 CoT 长度与合理化比例。
- **瓶颈与证据边界：** 现象由两篇独立工作报告但均未分离；剂量混淆、随机方向对照与被 steer token 数未核实；推理模型“steer 不动”的反例只来自 MoE 模型；多数证据为单次运行、n=100、窗口外且非白名单，其中两篇仅读摘要。
- **用户资源约束：** 预研 2×A100 80G / 4×L40 48G / 8×4090 24G；正式实验可用 8×A100 80G、最好不超过 5 天；付费 API（如 GPT judge）1000 元内可自主决定；token 资源较稀缺。
- **时间与目标：** 自 2026-10 起半年内投出一篇主会论文。
- **非目标：** 不做世界模型、视频生成、机器人方向。
- **进入实验规划的成功条件：** 独立 reviewer 两次（high + xhigh 复核）对同一 brief 判定三项贡献都 ≥6 且至少两项 ≥8、可行性 pass、verdict 为 experiment_ready、无 fatal blocker；产出 `EXPERIMENT_HANDOFF.md`。
