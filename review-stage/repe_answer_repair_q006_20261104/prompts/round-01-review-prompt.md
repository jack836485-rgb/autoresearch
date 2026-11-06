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
files in this workspace and do not write files, except your raw review to /home/claude/autoresearch/review-stage/repe_answer_repair_q006_20261104/round-01-review.md (UTF-8).
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

**定位关键词：** activation steering；contrastive activation addition；representation repair；collateral damage；cue-induced bias；knowledge conflict；contradiction blindness；When2Call

**一句话定位：** 答案级激活 steering 在线索诱导偏差（2607.18114）与上下文/参数知识冲突（2610.20067）上被报告为修复——纠正错误并保留多数正确答案；在矛盾盲视（2608.29431）、医学问答过度思考（2605.05715）与工具调用决策（2609.36138）上却被报告为只移动标签或纠正与破坏相抵。两类证据来自不同模型、任务与指标，没有人在同一模型、同一“纠正率/破坏率”指标下比较，也没有能在干预前判断某种失败“修得好修不好”的依据。

**与起点问题的关系：** 原问题；保留起点的对象（7–8B 开源模型上的残差流线性 steering）、两类任务与“纠正 vs 破坏”评价，把“分界由什么决定”具体化为三个在干预前可计算的量，并要求它们前瞻性地预测留出失败类型上的修复结果。

## 核心 Claim

若成立，本工作给出一张同模型同指标的“修复地图”，以及一条干预前可算、可前瞻验证的判别规则，回答何时 steering 是修复、何时只是先验偏移。三种候选解释各有一篇直接证据，但从未在同一设置下分离：
- **在场性**（2609.11216 在绑定任务上的发现）：正确答案在失败样本的干预位置上是否可被线性读出。读不出时，任何加性修法的修复上限都低；
- **类内离散度**（2611.04757）：所需位移在所请求类内的离散程度，用该文的 R、D 量衡量。离散度高时固定方向失败，逐样本检索目标（RGS）胜出；
- **标签混淆度**（2608.29431）：构造对比集时“成功”与“输出某标签”的相关程度。混淆度高时，固定 CAA 学到的是标签偏好，破坏率高。

可推翻的判断：先在 4 种失败类型上用三量拟合一条预测规则并冻结；在 2 种留出类型上，规则事先预测的“最佳修法”及其纠正率、破坏率的排序与实测一致。在实例层面，在场性（探针对正确答案的置信度）预测逐样本纠正概率的 AUROC 显著高于“失败可解码性”（2605.05715 所测的那一类信号）。若三量既不能前瞻预测留出类型，也不能在实例层面区分可修与不可修，主张即被推翻。

成功后新增的东西：使用者在动手前就能判断一种失败该不该用 steering、该用哪一种（固定、类条件、逐样本检索、探针解码目标）、大致能修多少、会破坏多少。同时把“信息来源类能修、推理过程类修不好”从任务类别的经验观察，改写为由可测量决定的结论。

当前依据及适用条件：
- 在场性：2609.11216 在 16 个模型的绑定任务上，答错样本中探针仍能恢复正确绑定，高于基线 0.196；沿探针解码目标 steer 后，8 个模型平均准确率提升 0.168。Orgad 等（2410.02707）报告模型可能编码正确答案却持续生成错误答案。
- 类内离散度：2611.04757 在替换语料上证明，类内目标变化时检索胜过固定方向，而且四个只用状态计算的量能事先排序规则表现，但它没有测推理失败上的纠正与破坏。
- 标签混淆：2608.29431 指出矛盾题上成功与输出“contradiction”几乎完全混淆；无门控时，在本就胜任的规则上准确率从 99.6% 降到 40.4%。
- 加性修法在推理失败上的上限：2605.05715 中，即使 oracle 质心位移，也只有 58% 的过度思考轨迹靠近正确类，非线性学习干预仅 +2.8pp；它还报告失败信号可解码（71.6%），但逐样本探针与 steering 效果的相关 r≈0，这正对应“会失败可解码 ≠ 正确答案在场”。

仍未知：三量是否彼此可分，例如矛盾盲视可能同时混淆度高、在场性低，届时只能报告联合效应；6 种类型给出的类型级规则统计力有限，因此以实例层面的预测为主要检验；推理模型与指令模型是否一致。

## 方法设计的核心思想

输入：一个模型；一种失败类型的数据（输入、金标准答案、模型基线输出）；干预层与位置（各类型沿用原论文设置）。

动作：(1) 计算三量。在场性——在基线答错的样本上，用在正确样本上训练的线性探针读出金标准答案的准确率及逐样本置信度；类内离散度——按 2611.04757 计算 R 与 D；标签混淆度——对比集中“成功”与输出标签的相关系数。(2) 跑四种修法：固定 CAA；类条件 CAA；RGS（k 近邻成功状态均值作为逐样本目标）；探针解码目标 steering（沿探针读出的答案方向，2609.11216 方式）。另设 oracle 逐样本目标作上限。α 在开发集上按净增益选定，之后冻结。(3) 同一指标评测：纠正率（基线错→对）、破坏率（基线对→错），以及 CRT 式的胜任子集破坏（2608.29431）。

输出：每种类型、每种修法的纠正率与破坏率；三量对它们的预测，包括类型层面的留出检验与实例层面的 AUROC。

与最高近邻的关键差别：2611.04757 只在替换和行为 A/B 语料上比较规则，不测推理失败的纠正与破坏；2609.11216 只做绑定一种任务；2608.29431 只审计矛盾盲视一种失败；2605.05715 只测过度思考且只用固定方向族。本工作把三者的解释放到同一模型、同一指标下，并做前瞻预测。

## 最小实验

模型：Llama-3.1-8B-Instruct（2605.05715 主模型）与 Qwen2.5-7B-Instruct（2605.05715 跨架构模型，也在 2607.18114/2610.20067 的家族范围内）；Qwen3-8B 非思考模式作第三个模型。

失败类型与数据（各类型取 ≥300 个失败样本与等量正确样本）：
- 信息来源类：BCT 建议答案偏差（2607.18114 代码与数据，github.com/prakharg55/bias-direction-EMNLP）；上下文/参数知识冲突（2610.20067 代码与数据，github.com/AheadOFpotato/knowledge_selection_steering）。
- 推理过程类：矛盾盲视（Asymmetricity-2.0，HF MoyYuan/Asymmetricity-2.0，2608.29431 公开数据）；When2Call 工具决策（nvidia/When2Call，CC-BY-4.0；落点审计按 2609.36138 公开代码 github.com/ruizheliUOA/mechanistic-tool-use-llm）。
- 中间类：实体绑定（2609.11216，代码未公开，按其任务规范构造）；MedQA 过度思考（2605.05715 未发布标签，按其定义重建：重采样能答对、扩展 CoT 中答错，判分器标注并抽检 100 条）。

前瞻设计：先在 BCT、知识冲突、矛盾盲视、When2Call 上拟合三量到最佳修法与纠正/破坏率的规则并冻结；再在绑定与过度思考上事先写下预测，之后才运行修法。

对照与复现：固定 CAA 为标准算法；RGS 与类条件 CAA 按 2611.04757 §3 的规范独立实现（代码未见公开）；探针解码目标按 2609.11216 规范独立实现；CRT 审计复用 2608.29431 数据；5 个范数匹配随机方向作方向特异性对照。

相同核心条件：同模型、同层、同位置、同 α 选择协议、同开发/测试划分；所有修法都以无干预基线为参照计纠正与破坏。

成本：每模型每类型约 600 样本 × 5 种修法（含 oracle）× 2 档 α，加探针训练与 RGS 的状态库，单 token 或短答任务为主，过度思考需 CoT 生成（约 1.3k 样本 × 若干条件 × 约 1k token）；3 模型合计约 1–2 天 2×A100。过度思考重建的判分用本地开源判官或 API，约 100–200 元。

Frozen Problem Anchor and user constraints:

- **起点问题：** 同一类“答案级 steering”为何在信息来源选择类失败上是修复（纠正错误且保留正确），在推理过程类失败上只是全局标签偏移（纠正与破坏交换）；决定这条分界的变量是什么。
- **对象与条件：** 4–9B 开源指令/推理模型（证据中 Llama-3.1-8B、Qwen2.5-7B、Gemma、OLMo、Qwen3 等）；残差流线性 steering（diff-in-means、探针方向、门控变体）；信息来源类任务（BCT 线索偏差、知识冲突）与推理过程类任务（矛盾盲视、MedQA 过度思考、When2Call/MetaTool 工具决策）。
- **初始任务/评测：** 纠正率（基线错→steer 后对）与破坏率（基线对→steer 后错），以及在模型本就胜任的规则上的跨规则迁移（2608.29431 的 CRT）。
- **瓶颈与证据边界：** 成功与失败证据来自不同模型、任务与指标；两篇成功证据只读到摘要级；未在同一模型上同时测纠正与破坏。
- **用户资源约束：** 预研 2×A100 80G / 4×L40 48G / 8×4090 24G；正式实验可用 8×A100 80G、最好不超过 5 天；付费 API 1000 元内可自主决定；token 资源较稀缺。
- **时间与目标：** 自 2026-10 起半年内投出一篇主会论文。
- **非目标：** 不做世界模型、视频生成、机器人方向。
- **进入实验规划的成功条件：** 独立 reviewer 两次（常规 + 复核）对同一 brief 判定三项贡献都 ≥6 且至少两项 ≥8、可行性 pass、experiment_ready、无 fatal blocker；产出 `EXPERIMENT_HANDOFF.md`。
