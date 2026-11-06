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
files in this workspace and do not write files, except your raw review to /home/claude/jack836485-rgb/autoresearch/review-stage/repe_cot_amplify_q005_20261104/round-04-review.md (UTF-8).
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

**定位关键词：** large reasoning models；activation steering；runtime intervention；safety recovery；chain-of-thought；KV cache；JailbreakBench；XSTest；When2Call；AgentDojo

**一句话定位：** 推理模型的运行时纠正（激活 steering、注入纠正前缀如 SafeThink）只在推理早期有效，一旦 CoT 写下决定承诺，干预基本失效；唯一可靠的办法是回滚到承诺之前重写，而在智能体中这意味着丢弃已完成的推理并重做工具调用。

**与起点问题的关系：** 子问题（方法）；保留起点的对象（4–8B 稠密推理模型）、决策方向 steering 与“steering 前已写好的 CoT 锁住原决定”这一现象，把起点的“锁定由什么决定”具体化为可干预的问题——锁定是否集中在少数承诺片段被后续读取这一点上；若屏蔽这些片段即可解锁，同时构成锁定机制的因果证据。起点中“放大”一侧以及剂量／文本／预先确定的分离仍未回答。

## 核心 Claim

若成立，本工作提供一种**不回滚即可逆转已承诺决定**的运行时纠正：在触发纠正的时刻 t，用按句的接收端注意力阻断找出承载决定的少量承诺片段 S，此后生成的所有 token 在所有层都不再读取 S 的 KV，同时施加纠正（决策方向的短窗口 steering，或纠正前缀）。可推翻的判断：在同模型、同触发时刻下，“屏蔽 S + 纠正”的恢复率显著高于“只纠正”，接近“回滚到 S 之前重写 + 纠正”；屏蔽同 token 数的随机句无此效果；在智能体轨迹中，它在恢复率相近时保留已完成的工具调用与用户任务进度，从而以更低代价完成恢复。若屏蔽 S 的解锁幅度远小于去掉整段 CoT，或随机屏蔽同样有效，则“锁定集中于少数承诺片段”被推翻，方法也失去依据。

成功后新增的东西：运行时守卫（如 TRACES、PROACT-Agent 一类只负责检测漂移的工作）在检出偏离后，有一个能恢复、而不必中止或重做的处置手段；同时得到“锁定 = 少数承诺片段的可读性”这一机制结论，解释为什么 steering 与扰动在承诺之后失效。

当前依据及适用条件：(i) 同模型同任务上，移除 CoT 文本能解锁——2605.26772 在 DeepSeek-R1-Distill-Llama-8B 拒答上，固定原 CoT 只 steer 作答 39%，完全去掉 CoT 70%（同一方向、同层）；(ii) 承载决定的文本高度集中——2507.03167 发现蒸馏模型 CoT 开头一句可完全决定拒答，DRTC（2602.15332）在四个推理模型上按片段阻断信息流时影响高度集中（Gini 约 0.50–0.58）；(iii) 承诺之后的扰动难以改变答案——2606.13603 在承诺边界后扰动时答案保留 72%、边界前 27%；2602.11096 中纠正前缀主要在前 1–3 步有效；(iv) 承诺可由少量组件中介——2605.17113 少于 10% 的注意力头可跨环境因果抑制欺骗承诺。仍未知：只屏蔽少数片段能否接近去掉全部 CoT 的解锁幅度（i 中 70% 是整段去除）；屏蔽后其余推理与工具结果是否仍被正常使用、输出是否连贯；在多轮智能体轨迹中承诺是否同样集中于少数片段；接收端阻断的定位在纠正之后是否稳定。

## 方法设计的核心思想

输入：一条推理轨迹前缀（含提示、已生成 CoT，智能体中含工具调用与返回）、纠正时刻 t（由已有守卫触发；实验中以强制作答曲线显示目标决定已稳定为准）、目标方向（恢复拒答／恢复帮助／恢复用户任务）。

动作：(1) **承诺片段定位**：对 t 之前的每个句子（工具返回作为整体单元，不屏蔽），构造 4D 注意力掩码，使 t 及之后的位置在所有层不注意该句；读取强制作答的决定 logit 变化，贪心选出使决定越过中点所需的最少片段集合 S（上限为 t 前 token 数的 15%）。每句一次带缓存的前向，成本与 DRTC 的阻断相当。(2) **屏蔽 + 纠正**：保持对 S 的屏蔽继续生成，同时施加纠正：决策方向 diff-in-means 的短窗口 steering（只在 t 之后前 k 个 token），或注入纠正前缀（SafeThink 式“Wait, think safely”）。(3) 生成完成后照常执行（智能体中继续调用工具）。

输出：纠正后的决定与完整轨迹。

与最高近邻的关键差别：DRTC 用接收端阻断做归因，不用于纠正；FASB（2508.17621）与回滚类方法丢弃并重写偏离部分；SafeThink 只在早期注入前缀；2605.26772 只在“整段保留／整段去除”两极比较；运行时守卫（TRACES、PROACT-Agent）只负责检测。本方法保留轨迹、只切断少数承诺片段的可读性，再纠正。

## 最小实验

模型：DeepSeek-R1-Distill-Llama-8B（与 2605.26772 同模型）与 Qwen3-8B（思考模式），稠密，HF eager/SDPA 注意力支持自定义 4D 掩码。

设置与数据：(a) 恢复拒答——JailbreakBench 有害指令中，模型在越狱模板或以 steer 下生成的服从型 CoT 前缀（2605.26772 交换设置，撤除 steering 后仍 48% 服从）条件下已承诺服从的轨迹，拒答由 Llama-Guard 判（2605.26772 附录 A 与人工一致 0.86）；(b) 恢复帮助——XSTest 中良性但模型已承诺拒绝的轨迹；(c) 恢复工具决定——When2Call test mcq（CC-BY-4.0，含 `correct_answer`）中已承诺错误调用/不调用的轨迹；(d) 智能体——AgentDojo 中模型读到注入后已在推理中承诺执行注入任务的轨迹，用其自带的效用与安全判定函数。每设置每模型 100–200 条，t 取强制作答曲线稳定后第 1 句与第 3 句两档。

对照（同触发时刻、同纠正强度）：只 steer（2605.26772 官方代码 github.com/kiajueng/cot_ref_harm_analysis，已 clone 核验）；只注入纠正前缀（SafeThink，2602.11096 规范，独立实现）；只屏蔽 S 不纠正；屏蔽同 token 数的随机句 + 纠正；回滚到 S 最早片段之前并在纠正下重写（FASB 式回溯，2508.17621 规范，独立实现；智能体中记录需重做的工具调用数）；去掉 t 之前全部 CoT + 纠正（2605.26772 的上限参照）。

判别：恢复率的按条配对差与 Wilson 区间；屏蔽+纠正相对只纠正的提升、相对回滚的差距；随机屏蔽是否失效；连贯性（困惑度与 LLM 判官）与效用（XSTest 回答质量、AgentDojo 用户任务完成率）；代价（额外 token、重做工具调用）。

成本：定位每条约 20–60 次带缓存前向；生成约 2 模型 × 4 设置 × 150 条 × 7 条件 ≈ 8400 条，约 700 万 token，2×A100 两天内；判官用本地 Llama-Guard 与开源模型，AgentDojo 判定为规则函数；无人工标注，API 费用可忽略。

Frozen Problem Anchor and user constraints:

- **起点问题：** 推理模型中，激活 steering 下生成的 CoT 放大被 steer 的决定，而 steering 前已写好的 CoT 锁住原决定；放大与锁定各由什么决定（剂量 / 文本正反馈 / 预先确定）。
- **对象与条件：** 稠密开源推理模型（证据集中在 Qwen3-4B、GLM-Z1-9B、DeepSeek-R1-Distill-Llama-8B，4–9B）；从生成前激活提取的决策方向（工具调用、拒答、二选一答案）；变量为 steering 强度、注入／抑制、思考／不思考、CoT 固定／去除／重新生成。
- **初始任务／评测：** When2Call、BFCL 的工具调用决策；拒答；二选一答案任务。指标为决定翻转率，辅以 CoT 长度与合理化比例。
- **瓶颈与证据边界：** 现象由两篇独立工作报告但均未分离；剂量混淆、随机方向对照与被 steer token 数未核实；推理模型“steer 不动”的反例只来自 MoE 模型；多数证据为单次运行、n=100、窗口外且非白名单，其中两篇仅读摘要。
- **用户资源约束：** 预研 2×A100 80G / 4×L40 48G / 8×4090 24G；正式实验可用 8×A100 80G、最好不超过 5 天；付费 API（如 GPT judge）1000 元内可自主决定；token 资源较稀缺。
- **时间与目标：** 自 2026-10 起半年内投出一篇主会论文。
- **非目标：** 不做世界模型、视频生成、机器人方向。
- **进入实验规划的成功条件：** 独立 reviewer 两次（high + xhigh 复核）对同一 brief 判定三项贡献都 ≥6 且至少两项 ≥8、可行性 pass、verdict 为 experiment_ready、无 fatal blocker；产出 `EXPERIMENT_HANDOFF.md`。
