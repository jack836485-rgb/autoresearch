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
files in this workspace and do not write files, except your raw review to /home/claude/autoresearch/review-stage/repe_cot_amplify_q005_20261104/round-05-review.md (UTF-8).
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

**定位关键词：** interleaved thinking；preserved thinking；LLM agents；tool use；indirect prompt injection；AgentDojo；reasoning models；chain-of-thought

**一句话定位：** 在多步工具调用的推理模型智能体中，跨步保留并回传先前的推理是被推荐的做法——Z.AI 文档称 Preserved Thinking 可提升表现与缓存命中、主要推荐用于编码/智能体场景；Kimi K2 Thinking 要求在工具调用循环内回传全部 reasoning_content 以保持多步计划连续；Qwen3 的模板默认在当前轮工具循环内保留推理；AutoForge（2512.22857）报告保留推理对多轮智能体有益。但保留的推理是否同时把早先的错误承诺或被注入的目标锁进后续行动，未被测量。

**与起点问题的关系：** 邻近新问题；保留起点的核心现象——“steering 之前已写好的 CoT 锁住原决定”——把对象从单轮激活 steering 换成多步智能体中跨步保留的推理，把干预换成自然出现的错误信息与间接提示注入。起点问题中“放大”一侧以及剂量／文本正反馈／预先确定的分离不在本研究回答范围内。

## 核心 Claim

若成立，本工作表明**跨步保留推理是一项带有可纠正性与安全代价的设计**，并指出它与一类注入防御的直接冲突：(1) 智能体在先前推理中写下的结论，在后续工具返回更正证据时更难被修正；(2) 一旦被注入的目标被写进保留的推理，即使之后把工具输出中的注入文本净化掉，攻击仍会持续——以净化工具输出为手段的防御（如 AgentSentry 的上下文净化、CachePrune 的 KV 剪枝）在保留推理的智能体上会系统性失效，必须同时处理推理历史。由此给智能体设计者一个可操作的结论：保留推理换来的效用，需要用推理历史的净化或剥离策略来配套。

可推翻的判断：在同一模型、同一任务上，(a) 第 t 步工具给出错误信息、第 t+1 步给出更正时，保留推理条件下最终行动采用更正的比例显著低于剥离推理条件；(b) 第 t 步注入、第 t+1 步起对工具输出做神谕净化（按 AgentDojo 已知的注入位置删去注入文本）后，保留推理条件下的攻击成功率显著高于剥离推理条件，而剥离推理时神谕净化使攻击成功率接近无注入水平。若 (a)(b) 两项在保留与剥离之间都无显著差别，主张被推翻。

当前依据及适用条件：(i) 同模型上的直接证据——2610.25760 在 Qwen3-8B 与 Qwen3.5-9B 的文件系统智能体任务中把“行动时生成推理”和“保留早先推理”分开，发现给智能体一段为另一段历史写的推理时，它会照该推理行事、甚至违背自己的历史；这是在单一玩具任务和固定历史上测得的，没有涉及纠正证据或注入。(ii) 单轮上已写推理锁定决定——2605.26772 在 DeepSeek-R1-Distill-Llama-8B 上，固定已写 CoT 时同一 steering 只翻转 39%，去掉 CoT 后 70%；2506.10979 发现注入的思路常被模型沿着续写。(iii) 注入会跨步持续——AgentSentry（2602.22724）指出多轮注入内容可在中间步骤持续、稍后才触发未授权动作，但其净化只作用于工具返回内容。仍未知：真实基准中模型在推理里复述注入目标的频率（决定 (b) 的覆盖面，将单独报告）；纠正证据下锁定的幅度；对默认保留推理的模型做剥离是否本身造成分布外退化——为此把良性任务效用作为并列结局，若剥离显著损害效用，结论改写为“效用—可纠正性权衡”而非“剥离更好”。

## 方法设计的核心思想

输入：一个推理模型智能体（ReAct 式工具循环，每步先思考再调用工具），一个任务环境及其判定函数。

动作：在每一步构造上下文时施加一个开关——**保留**：把此前各步的思考按模型原生格式回传（Qwen3 模板与 gpt-oss harmony 在工具循环内的默认）；**剥离**：只回传此前各步的工具调用与工具返回，删去思考。其余一切相同。交叉两类受控事件：**纠正证据**——第 t 步某个工具返回被程序化改为错误值，第 t+1 步另一工具返回给出更正（环境状态以更正值为准）；**注入 + 净化**——第 t 步工具输出含注入；从第 t+1 步起，(i) 不净化，(ii) 神谕净化（删去该注入文本），(iii) 一个已发表的净化防御。另记录模型在思考中复述注入目标或错误值的比例，作为中介量。

输出：良性效用、更正采用率、各净化条件下的攻击成功率，按保留/剥离对比；按“思考中是否复述了注入目标/错误值”分层。

与最高近邻的关键差别：2610.25760 只在一个玩具任务的固定历史上替换推理，没有纠正证据、注入或防御；AutoForge 只报告保留推理的效用收益；AgentSentry、CachePrune、ICON 的净化与纠正只作用于工具输出或其 KV，都没有把保留推理当作注入的第二个载体；2605.26772 是单轮、激活 steering。本工作在真实智能体基准上把保留开关与纠正证据、注入净化交叉。

## 最小实验

模型：Qwen3-8B（思考模式，模板在当前轮工具循环内默认保留推理）与 gpt-oss-20b（harmony 格式在工具循环内保留推理，训练时即如此）；本地 vLLM 部署，AgentDojo 自带 `LocalLLM` 管线（已 clone 核验 `agent_pipeline/llms/local_llm.py`）。

环境与数据：AgentDojo（公开，含 workspace/slack/travel/banking 四套环境、用户任务与注入任务、注入位置占位与 utility/security 判定函数）。良性效用用全部用户任务；注入用其标准攻击（如 important_instructions）；纠正证据套件从这些环境的工具返回程序化构造约 200 个情形，判定按环境状态机械给出。

对照：保留 vs 剥离（主开关）；神谕净化（理想上界）；一个已发表净化防御（AgentSentry 2602.22724 的上下文净化，或 CachePrune 2504.21228；先核验代码，不可用则按论文规范实现其净化步骤，并注明为独立实现）；无注入基线。

相同核心条件：同模型、同解码（温度与采样数固定，每情形 3 次采样）、同工具与同环境种子；唯一差别是历史中是否含先前思考。

判别：更正采用率与攻击成功率的保留−剥离差，按情形配对的自助置信区间；按“思考中是否复述注入目标/错误值”分层，检验差别是否由复述中介；良性效用的保留−剥离差，判断剥离是否分布外退化。

成本：AgentDojo 约 100 个用户任务 × 主要注入组合，加纠正套件 200 情形；2 模型 × 2 开关 × 3 净化条件 × 3 采样，约 1–2 万条轨迹、每条约 5–15 步；8B 与 20B 在 2×A100 上用 vLLM 约 2–3 天。判定为规则函数，无 API 费用、无人工标注。

Frozen Problem Anchor and user constraints:

- **起点问题：** 推理模型中，激活 steering 下生成的 CoT 放大被 steer 的决定，而 steering 前已写好的 CoT 锁住原决定；放大与锁定各由什么决定（剂量 / 文本正反馈 / 预先确定）。
- **对象与条件：** 稠密开源推理模型（证据集中在 Qwen3-4B、GLM-Z1-9B、DeepSeek-R1-Distill-Llama-8B，4–9B）；从生成前激活提取的决策方向（工具调用、拒答、二选一答案）；变量为 steering 强度、注入／抑制、思考／不思考、CoT 固定／去除／重新生成。
- **初始任务／评测：** When2Call、BFCL 的工具调用决策；拒答；二选一答案任务。指标为决定翻转率，辅以 CoT 长度与合理化比例。
- **瓶颈与证据边界：** 现象由两篇独立工作报告但均未分离；剂量混淆、随机方向对照与被 steer token 数未核实；推理模型“steer 不动”的反例只来自 MoE 模型；多数证据为单次运行、n=100、窗口外且非白名单，其中两篇仅读摘要。
- **用户资源约束：** 预研 2×A100 80G / 4×L40 48G / 8×4090 24G；正式实验可用 8×A100 80G、最好不超过 5 天；付费 API（如 GPT judge）1000 元内可自主决定；token 资源较稀缺。
- **时间与目标：** 自 2026-10 起半年内投出一篇主会论文。
- **非目标：** 不做世界模型、视频生成、机器人方向。
- **进入实验规划的成功条件：** 独立 reviewer 两次（high + xhigh 复核）对同一 brief 判定三项贡献都 ≥6 且至少两项 ≥8、可行性 pass、verdict 为 experiment_ready、无 fatal blocker；产出 `EXPERIMENT_HANDOFF.md`。
