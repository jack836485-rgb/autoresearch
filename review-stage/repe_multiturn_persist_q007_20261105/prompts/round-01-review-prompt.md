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
Today's date: 2026-11-05. Known tool workarounds: GitHub REST API returns HTTP 403 through this sandbox's proxy; anonymous 'git clone --depth 1' of public GitHub repos works from Bash; arXiv abs/html pages are readable via WebFetch
Finish all searches before answering and leave no background tasks running. Do not read other
files in this workspace and do not write files, except your raw review to /home/claude/autoresearch/review-stage/repe_multiturn_persist_q007_20261105/round-01-review.md (UTF-8).
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

**定位关键词：** prefix steering；activation steering；multi-turn conversations；persona drift；reasoning models；chat template；KV cache

**一句话定位：** 前缀 steering（2610.04967）在单轮中只需短暂注入就能持续影响后续生成，但作者明确写道，行为实验分不清机制是“被改的表示”还是“生成的上下文”，也不知道在多阶段任务中何时前缀足够；在多轮对话中，早期成功的 steering 几轮后会衰减或反转（2610.19817），而输入驱动的 persona 漂移却会随对话累积（Assistant Axis，2601.10387）——跨轮持续性由什么承载、何时前缀够用，尚无同一设置下的测量。

**与起点问题的关系：** 原问题；保留起点的多轮协议、特质保持与连贯性随回合的曲线、以及“新回合内容与目标特质的冲突程度”这一变量，把“何时前缀足够”具体化为“被 steer 的状态写进了哪一段会被保留的文本、后续回合是否与之冲突”。持续干预为何累积损伤只作为对照测量，不是主目标。

## 核心 Claim

若成立，本工作回答前缀 steering 作者留下的机制问题，并给出何时前缀足够的判据：**多轮中 steering 的跨轮持续几乎完全由保留下来的转录承载，而不是由被改的表示（被 steer 位置的 KV）承载。** 由此推出三个可推翻的预测：

(1) **转录移植等效。** 把第 1 轮在前缀 steering 下生成的对话转录，交给一个全新的、从未被 steer 的同一模型（重新计算全部 KV）继续，后续回合的特质保持曲线与保留原 KV 继续的曲线无显著差别。

(2) **判据。** 撤除 steering 后，下一轮的特质保持可以由两个量预测：上一轮被保留的可见文本中特质的表达强度，以及新用户回合与目标特质的冲突程度。冲突低时一次前缀即可，冲突高时必须每回合在回合起点重新注入。

(3) **推理模型的交叉。** 推理模型的聊天模板会在后续回合剥离先前的思考，只保留可见回答（例如 Qwen3 模板），所以 steering 在当轮经由 CoT 被放大的那部分不会跨轮保留。预测：同一模型思考模式与非思考模式相比，第 1 轮效果更强，但跨轮衰减更快；改为保留先前思考的模板后，跨轮持续恢复。

若 (1) 中保留 KV 显著优于移植，或 (3) 的交叉不存在，主张即被推翻。

当前依据及适用条件：(i) 多轮表示变化主要由转录驱动——2601.20834 发现回放一段由另一个模型写的对话脚本，也能复现线性表示的剧烈变化；(ii) 模型自己过去的回答会跨轮传播状态——2602.24287 发现以自身回答为条件会造成上下文污染，错误与风格跨轮传播；(iii) 单轮中被 steer 生成的文本能独立携带效果——2605.26772 撤除 steering 后，steer 下生成的 CoT 仍保留 48% 的效果；推理模型在 steering 下思考时被放大——2604.01202 在 Qwen3-4B 上思考模式翻转 62% 对不思考 29%；(iv) 多轮中会衰减——2610.19817（摘要级）。仍未知：跨轮时 KV 通路是否还有独立份额（2605.10664 推测多轮退化来自 KV 污染，但未隔离）；交叉的幅度是否足以测出；判据中“表达强度”的测量（探针投影或判官评分）是否稳定。

## 方法设计的核心思想

输入：一个模型、一个特质方向 v（diff-in-means，按 2610.04967 或 persona vector 协议提取）、一套多轮对话脚本（用户回合预先固定并回放，按冲突程度分为支持、中性、反对三档）。

动作（同一 α 与同一被 steer 的 token 数）：
- A：前缀 steering 只在第 1 轮回答的前 k 个 token 施加；
- B：同 A，但第 2 轮起把第 1 轮的转录交给新实例继续，重算 KV（转录移植）；
- C：每回合起点重新施加前缀；
- D：全程注入；
- E：选择性注入（2604.08169 的 StTP 或 Assistant Axis 式封顶）。

对推理模型另设两种模板：剥离先前思考（默认）与保留先前思考。

测量：每回合特质表达（沿 v 的探针投影，加上判官评分）与连贯性（困惑度加判官评分）；上一轮可见文本中的特质表达强度作为预测变量。

输出：各条件的特质保持与连贯性曲线；A−B 差（KV 份额）；以“上一轮表达强度 × 冲突档”对下一轮保持的回归；思考 vs 非思考、剥离 vs 保留模板的交叉。

与最高近邻的关键差别：2610.04967 只做单轮或单阶段，作者把机制区分留作未来工作；2610.19817 在多轮中测衰减，但不区分 KV 与转录、不涉及推理模型；2605.10664 的 GCAD 在注意力层干预以减少多轮损伤，没有隔离通路；Assistant Axis 测输入驱动漂移并用封顶稳定，不测前缀的跨轮持续；2601.20834 测自然对话中的表示变化，不涉及 steering。

## 最小实验

模型：Qwen3-8B（可切换思考/非思考，模板默认剥离先前思考）、Llama-3.1-8B-Instruct（非推理对照）、DeepSeek-R1-Distill-Llama-8B（只有思考模式，与 2605.26772 衔接）。

特质与脚本：两类特质。一类是 2610.19817 式的价值权衡；另一类是 persona 特质，如乐观/谨慎，方向按 Assistant Axis 公开代码（github.com/safety-research/assistant-axis）的流程提取。用户回合由固定脚本回放：每特质 50 段 8 轮脚本 × 三档冲突，用一个强模型一次性写好并人工抽检 30 段。回放已有依据：2601.20834 证明回放脚本有效。

对照与复现：前缀 steering 按 2610.04967 §5 的规范独立实现；StTP 按 2604.08169 的规范独立实现；Assistant Axis 封顶用其公开代码；GCAD 若代码不可得，只引用其报告数值，不作为必需对照。

相同核心条件：同模型、同层、同 α、同被 steer token 数、同脚本、贪心解码；转录移植与保留 KV 两臂只在是否重算 KV 上不同。

判别：A−B 曲线差的按脚本配对置换检验；回归中交互项（表达强度 × 冲突）；思考/非思考 × 剥离/保留的 2×2 交互。

成本：3 模型 × 2 特质 × 150 段 × 8 轮 × 约 6 个条件 ≈ 4.3 万轮生成，每轮约 300 token（推理模型约 1k）；约 2–3 千万 token，2×A100 一至两天。判官评分用本地开源模型，脚本生成用 API 约 50 元。

Frozen Problem Anchor and user constraints:

- **起点问题：** 多阶段控制任务中前缀 steering 何时足够、何时必须持续；持续干预为何累积损伤或衰减、反转。
- **对象与条件：** 开源指令/推理模型（证据中 Llama、Qwen 系列，7B–70B）；persona、价值、对齐特质的激活 steering；多轮对话与智能体循环。
- **初始任务/评测：** 特质表达与连贯性随回合数的曲线。
- **瓶颈与证据边界：** 各方法各自一种设定；多轮衰减证据仅摘要；KV 污染未隔离。
- **用户资源约束：** 预研 2×A100 80G / 4×L40 48G / 8×4090 24G；正式 8×A100 最好 ≤5 天；API 1000 元内自主；token 稀缺。
- **时间与目标：** 自 2026-10 起半年内投主会。**非目标：** 世界模型、视频生成、机器人。
- **进入实验规划的成功条件：** 两次独立审查（常规+复核）均三项 ≥6、至少两项 ≥8、可行性 pass、experiment_ready、无 fatal blocker；产出 EXPERIMENT_HANDOFF.md。
