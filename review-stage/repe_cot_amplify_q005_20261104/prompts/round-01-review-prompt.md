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
files in this workspace and do not write files, except your raw review to /home/claude/jack836485-rgb/autoresearch/review-stage/repe_cot_amplify_q005_20261104/round-01-review.md (UTF-8).
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

**定位关键词：** activation steering；steering vector；large reasoning models；chain-of-thought；commitment boundary；When2Call；JailbreakBench

**一句话定位：** 激活 steering 领域中，开源推理模型对同一决策方向时而更易被 steer（在 steering 下重新生成 CoT 时，2604.01202、2605.26772），时而更难（保留 steering 前已写好的 CoT 时，2605.26772），这一“放大与锁定”并存的成因尚未被分离。

**与起点问题的关系：** 原问题；保留对象（4–8B 稠密推理模型）、决定类型（工具调用、拒答）与翻转率指标，把“剂量／文本正反馈／预先确定”三种解释改写为以 CoT 承诺边界为时间参照、可逐一分离的操纵；MoE 模型是否抵抗 steering 不在本研究范围。

## 核心 Claim

若成立，本工作给出推理模型上 steering 可控性随 CoT 时间位置变化的因果地图，并用一个机制统一放大与锁定：**steering 只在 CoT 写下决定承诺之前有效；它的效果主要通过被 steer 轨迹自己写下的承诺文本被继续携带，而不是靠被 steer 的 token 数累积；一旦原 CoT 已越过承诺边界，即使允许模型在 steering 下继续审议，翻转率也显著下降。** 这能解释为什么思考模式比不思考更易被 steer、固定 CoT 为何抵抗、以及为何短窗口 steering 足够，并直接告诉使用者在推理模型上该在何时、多长地 steer。

可推翻的判断：在同一方向、同一 α、相同被 steer token 数下，steering 起点位于原 CoT 承诺边界之后时的翻转率，显著低于位于其前时；而在被 steer 轨迹写下自身承诺之后撤除 steering 并**不 steer 重算 KV**（只剩文本），翻转率接近全程 steering。

当前依据：(i) 2605.26772 在 DeepSeek-R1-Distill-Llama-8B 上于层 l 所有位置注入拒答方向（固定 CoT 时原 CoT 位置也在 prefill 中被注入），固定原 CoT 只重生成答案 39%，重生成 CoT 94%，用 steer 下生成的 CoT 但不 steer 仍有 48%——被 steer 的位置数相近而结果相差悬殊，提示文本而非剂量起主要作用，且文本能独立携带约一半效果；(ii) 2507.03167 发现蒸馏推理模型 CoT 开头一句可完全决定拒答；(iii) 2606.13603 发现 CoT 通常在单一步内跨过承诺边界、远早于 CoT 结束；(iv) 2610.04967 在非思考任务上表明极短的初始 steering 能保留大部分控制效果。

仍未知：2605.26772 的“固定 CoT”不允许模型继续审议，锁定究竟来自已写承诺还是来自不给再审议机会，未被测过；KV 通路与文本通路各占多少未分离；工具调用决定在 pre_gen 已可解码（AUROC>0.9，2604.01202）时承诺边界是否就落在开头、从而让“承诺前窗口”极短；这些机制是否跨模型、跨决定类型成立未知。

## 方法设计的核心思想

输入：一个推理模型、一个从 pre_gen（工具调用，沿用 2604.01202）或 EOI（拒答，沿用 2605.26772）激活以 diff-in-means 得到的决策方向 v、一组以无 steering 基线决定为参照的题目。

动作：(1) **承诺边界定位**：对每题的无 steering CoT 按句截断、强制结束思考并读取决定 token 的概率（沿用 2606.13603 流程，改为二分类决定），取决定概率首次稳定越过阈值的句子为 b。(2) **起点扫描**：保留原 CoT 至第 s 句（s ∈ {0, b−2, b−1, b, b+1, b+3}），从此处起在 steering 下继续生成直至作答，允许再审议；被保留前缀的位置分“prefill 时也注入”与“不注入”两种。(3) **释放扫描**：从 think_start 起只 steer 前 w 个 decode token（w ∈ {1, 16, 64, 256}，以及“被 steer 轨迹自身越过承诺边界 b′ 即停”）后撤除，分“保留被 steer 位置的 KV”与“撤除后不 steer 重算全部 KV（只剩文本）”。(4) **剂量匹配**：思考与不思考模式下限定被 steer 的 decode 位置数相同（如 prefill + 前 k 个 token）。

输出：翻转率随 (s−b)、w、通路（KV/文本）、模式的曲面；CoT 长度与承诺重新打开（强制作答曲线是否回落）作为辅助观测。

与最高近邻的关键差别：2605.26772 只在 CoT 起点施加 steering、单模型单任务，固定 CoT 时不允许续写；2604.01202 全程注入、未控制剂量、无范数匹配随机方向；2610.04967 研究短窗口但不在思考模式决定任务上、不以 CoT 承诺为参照、不分 KV 与文本；2606.13603 定位承诺边界但不涉及 steering。本工作以测得的承诺边界为自变量参照，补上“承诺之后仍可续写时 steering 能否翻转”这一未测格，并分离 KV 与文本。

## 最小实验

模型：Qwen3-4B 与 Qwen3-8B（可切换思考/不思考，与 2604.01202 衔接）、DeepSeek-R1-Distill-Llama-8B（与 2605.26772 衔接），均为稠密模型。任务：When2Call test mcq（nvidia/When2Call，CC-BY-4.0，含 `correct_answer` 与四类答案，按 2604.01202 合并为 tool / no-tool），注入与抑制各取 150 个基线决定稳定（贪心与 4 次采样一致）的题；JailbreakBench 100 条基线全拒的有害指令，拒答按 2605.26772 用 Llama-Guard 判（其附录 A 与人工标注一致率 0.86）。

强对照与复现路线：
- 全程 steering（思考/不思考）：2604.01202 §3.4 规范充分（层 20、pre_gen diff-in-means、prefill+decode 全程、α 按激活范数取 3 档），代码未公开，按规范独立实现。
- 固定/去除/重生成/交换 CoT：2605.26772 官方代码已核验（`generate_with_intervention.py`、`generate_with_new_trace.py`，前向 pre-hook 加 α·r），直接复用并扩到 Qwen3。
- Prefix Steering：2610.04967 §5 规范（从最终 prompt token 起 steer 固定 k 个 token），代码未确认，独立实现作为释放扫描“保留 KV”一支。
- 承诺边界：2606.13603 官方代码已核验（按句截断+强制作答+稳定判定），改为读取二分类决定 token 概率。
- 方向特异性：每档 α 5 个范数匹配随机方向。

相同核心条件：同模型同方向同层、同 α 网格、贪心解码、同一题集；所有条件以无 steering 的基线决定为参照计翻转。

判别结果：锁定 vs 剂量——同 α、同被 steer token 数下，s>b 与 s<b 的翻转率差（Wilson 区间与按题配对的置换检验）；文本携带 vs KV——释放后“重算 KV”与“保留 KV”与全程 steering 的差；预先确定——pre_gen 探针间隔在控制 s−b 后的逻辑回归系数；剂量——思考 vs 不思考在剂量匹配下的差是否消失。若 s>b 时翻转率不下降，或剂量匹配后思考仍显著更易被 steer 且文本通路贡献很小，则统一解释被推翻。

成本：约 3 模型 × 2 任务 × 300–400 题 × 约 20 个条件 × 2 档 α ≈ 5 万条生成，平均约 700 token；HF 前向 hook 批量生成在 8B 上单张 A100 约 1–2k token/s，8×A100 约 1 天；承诺边界每题约 20 次带缓存的前向，可忽略。拒答判分用本地 Llama-Guard，无 API 费用；不需人工标注。

Frozen Problem Anchor and user constraints:

- **起点问题：** 推理模型中，激活 steering 下生成的 CoT 放大被 steer 的决定，而 steering 前已写好的 CoT 锁住原决定；放大与锁定各由什么决定（剂量 / 文本正反馈 / 预先确定）。
- **对象与条件：** 稠密开源推理模型（证据集中在 Qwen3-4B、GLM-Z1-9B、DeepSeek-R1-Distill-Llama-8B，4–9B）；从生成前激活提取的决策方向（工具调用、拒答、二选一答案）；变量为 steering 强度、注入／抑制、思考／不思考、CoT 固定／去除／重新生成。
- **初始任务／评测：** When2Call、BFCL 的工具调用决策；拒答；二选一答案任务。指标为决定翻转率，辅以 CoT 长度与合理化比例。
- **瓶颈与证据边界：** 现象由两篇独立工作报告但均未分离；剂量混淆、随机方向对照与被 steer token 数未核实；推理模型“steer 不动”的反例只来自 MoE 模型；多数证据为单次运行、n=100、窗口外且非白名单，其中两篇仅读摘要。
- **用户资源约束：** 预研 2×A100 80G / 4×L40 48G / 8×4090 24G；正式实验可用 8×A100 80G、最好不超过 5 天；付费 API（如 GPT judge）1000 元内可自主决定；token 资源较稀缺。
- **时间与目标：** 自 2026-10 起半年内投出一篇主会论文。
- **非目标：** 不做世界模型、视频生成、机器人方向。
- **进入实验规划的成功条件：** 独立 reviewer 两次（high + xhigh 复核）对同一 brief 判定三项贡献都 ≥6 且至少两项 ≥8、可行性 pass、verdict 为 experiment_ready、无 fatal blocker；产出 `EXPERIMENT_HANDOFF.md`。
