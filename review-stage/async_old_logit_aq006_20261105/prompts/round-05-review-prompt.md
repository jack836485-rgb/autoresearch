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
Today's date: 2026-11-05. Known tool workarounds: arXiv abs/html/pdf pages are reachable via curl in Bash (pdftotext available); GitHub REST API returns 403 but 'git clone --depth 1' works for public repos; WebSearch and WebFetch are available
Finish all searches before answering and leave no background tasks running. Do not read other
files in this workspace and do not write files, except your raw review to /home/claude/autoresearch/review-stage/async_old_logit_aq006_20261105/round-05-review.md (UTF-8).
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

**定位关键词：** training-inference mismatch；score centering；policy staleness；importance sampling；training collapse

**一句话定位：** 在 LLM 强化学习中，训练–推理偏差（推理引擎数值差或异步陈旧权重）导致的训练崩溃，近期被解释为"漂移项沿反馈环逐步累积"，但这一机理只在人为放大的偏差和几十到几百步的短训练上验证过，温和偏差下长程训练是否崩溃、何时崩溃，目前无法事先判断。

**与起点问题的关系：** 子问题。保留起点问题中的评价目标（异步/离策略校正下的后期崩溃）和偏差来源（数值偏差与陈旧度），把对象从"缺失的 old logits"换成"漂移累积速度与崩溃时间"。起点问题中 old logits 如何获取、哪些系统保留 old logits，本 Idea 不回答。

## 核心 Claim

**主贡献（规律 + 判断工具）：** 若成立，新增一个可标定、可外推的崩溃时间规律：在给定校正方法下，训练在**累积漂移**达到一个近似不随偏差来源与偏差幅度变化的阈值（"漂移预算"）时崩溃；偏差幅度、学习率与陈旧度只改变到达阈值所需的步数。由此，用训练前若干步可测的漂移量及其增长率，就能预测崩溃步数。这给出两件此前没有的东西：
1. 把"放大偏差是温和长程偏差的代理"从一个假设变成可检验的时间换算；
2. 在不跑长程训练的情况下，事先判断某个配置（BF16 非逐比特一致推理、FP8 rollout、陈旧度 $k$、学习率）在给定步数预算内是否会崩，从而决定是否值得付出修复代价（逐比特一致推理约 9–12% 吞吐、score centering、精确 old logits）。

**被测量的量：** 第 $k$ 步的漂移量 $d_k=\big\|\sum_t \bar A_t\,\hat{\bar s}_t\big\|$（按批次 token 数归一），其中 $\hat{\bar s}_t$ 是 score centering（2609.20807）用采样端 top-$k$ 概率估计的"采样器下得分均值"，$\bar A_t$ 为该前缀的优势；它就是策略梯度中被 score centering 抵消的那一项。累积漂移 $D_K=\sum_{k\le K}\eta\, d_k$（$\eta$ 为学习率）。

**可推翻的判断：**
1. 在放大偏差扫描中（三类来源 × 三档幅度 × 两个学习率），同一校正方法的崩溃步 $T_c$ 处的累积漂移 $D_{T_c}$ 的变异系数明显小于 $T_c$ 本身的变异系数（即预算近似不变）；
2. 用前 50 步估计的初始漂移与增长率，按标定后的预算外推自然偏差配置的 $T_c$，在长程运行中与实测 $T_c$ 的误差在 ±30% 以内；预测"不会在预算步数内崩溃"的配置确实不崩；
3. 该预测的提前量与误报率优于三种现有在线信号：滞后比率 ESS 降到 1/2（2610.40945）、响应长度骤增（2602.01826）、训练–推理 KL 阈值。
若 (1) 不成立（预算随来源或幅度系统变化），说明放大偏差不能按时间换算代理温和偏差，这本身就推翻了两篇机理工作共用的代理假设。

**当前依据与适用条件：**
- 2609.20807（Score Centering）在 §5.1 明说找不到能在几个 GPU 小时内拉开方法差距的自然设置，因而刻意放大偏差，并把结果作为"温和偏差下长程训练"的代理；同节记录了文献分歧：FP8-RL（2601.18150）只用 token 级 IS 即稳定训练 FP8 rollout，而 MAI-Thinking-1 技术报告在 BF16 采样下仍出现发散，作者认为二者都与"漂移随训练累积"一致，但未检验。其图 3 显示同一方法的崩溃步随噪声增大单调提前（如 DPPO 约在 160/80/20 步崩溃，TIS 在三档噪声下分别为稳定/约 180/约 40 步）。
- 2610.40945 给出滞后反馈环的显式形式（累积更新 $\Delta_{k+1}\approx(I-\eta M)\Delta_k+\eta g_k$），并在 Qwen3-1.7B 上观察到 IS 恰在滞后比率 ESS 降到 1/2 的那一步失效；其实验同样是 40 步短训练。
- 2602.01826 发现偏差与梯度噪声随训练同步升高，缩小更新步长能压住偏差增长，与"漂移按 $\eta d$ 累积"一致。
- 2605.14220（VeXact）在零偏差参考下显示，自然的小数值偏差本身就能导致 Qwen3-1.7B 与 Qwen3-30B-A3B 训练崩溃，说明自然偏差下的崩溃是真实现象。
- 仍未知：预算是否跨来源近似不变（数值偏差的漂移近似恒定，陈旧度的漂移随更新增长，二者的阈值可能不同）；自然偏差下崩溃是否落在可负担的步数内；漂移量的 top-$k$ 估计在温和偏差下的信噪比。现有证据只说明"更大偏差更早崩溃"，没有说明存在不变的阈值。

## 方法设计的核心思想

- **输入**：一次 RL 训练的前若干步（采样端 top-128 概率、优势、学习率）。
- **动作**：每步计算 $d_k$（与 score centering 的修正项同一计算，开销为一次已有的 head 收集），累积 $D_K$；在放大偏差扫描中标定各校正方法的预算 $D^*$；对新配置，用前 50 步拟合 $d_k$ 的增长（常数或指数，按反馈环形式选择），解出 $D_{T}=D^*$ 的 $T$ 作为崩溃步预测。崩溃按统一规则判定：干净评测准确率从峰值下降超过一半且不恢复。
- **输出**：预测的崩溃步与置信区间；"在给定步数预算内是否安全"的判断。
- **与最高近邻的关键差别**：2609.20807 与 2610.40945 解释为什么会崩，并给出修正方法，但不预测何时崩；2610.40945 的 ESS 规则与 2602.01826 的响应长度是在崩溃临近时触发的在线信号；本 Idea 给出跨幅度的时间换算与提前预测，并检验两篇机理工作共用的代理假设。

## 最小实验

- **模型与任务**：Qwen3-0.6B（主）与 Qwen3-1.7B（检验），Countdown（2609.20807 与 2610.40945 共用的设置：64 题 × 8 采样、512 token、±1 奖励减组均值）。
- **实现**：放大偏差扫描用 Score Centering 作者的参考实现（`github.com/martin-marek/score-centering` 的 `train_rl.py`，已有 `staleness`、`weight_noise_scale`、int8/fp8 采样器、`kv_quant_bits` 开关）；自然偏差用 AReaL 已移植的 Countdown 实验（`examples/math/score_centering_countdown.md`，Qwen3-0.6B，SGLang BF16 推理 + FSDP 训练，含采样端 top-128 收集），零偏差参考用批不变推理或 VeXact 方式。
- **阶段 0（便宜，可直接 no-go）**：权重噪声 3 档 × PG × 2 种子，共 6 次 300 步运行。若 $D_{T_c}$ 的变异系数不小于 $T_c$ 的变异系数，判 no-go。
- **阶段 1（标定）**：三类来源（权重噪声 3 档；采样器 int8、fp8 与 KV fp4；陈旧度每 8/16/32 步同步）× 两种校正（PG、TIS）× 两个学习率（SGD $10^{-2}$ 与 $5\times10^{-3}$）× 2 种子，0.6B 共 72 次，每次最多 400 步；1.7B 取权重噪声与陈旧度各 2 档 × PG × 1 种子共 4 次。另加 AdamW（$10^{-6}$）的 2 次运行，检验预算对优化器的依赖。
- **阶段 2（外推检验）**：自然偏差 4 个配置——BF16 引擎差 × {PG, TIS}、FP8 W8A8 rollout × PG、零偏差参考 × PG，各 3000 步、1 种子，用前 50 步预测、全程检验。
- **对照预警**：滞后比率 ESS<1/2、响应长度骤增（按 2602.01826 的触发规则）、训练–推理 KL 阈值；比较提前量（预测步与实测崩溃步之差）、误报（预测崩溃但未崩）与漏报。
- **支持主张的结果**：阶段 1 中各方法的 $D_{T_c}$ 变异系数显著小于 $T_c$；阶段 2 中崩溃配置的预测误差在 ±30% 内，未崩配置被正确判为安全，且提前量大于三种现有信号。**推翻**：预算随来源系统偏移（例如陈旧度来源的预算比数值来源高一倍以上），或自然配置的预测误差超过 ±30%。
- **算力**：2609.20807 报告其权重噪声扫描 108 次 0.6B 运行约 280 H100 小时（每次约 2.6 H100 小时）。按 A100 约慢一倍估计，阶段 0–1 约 80 次 × 约 5 A100 小时 ≈ 400 A100 小时；阶段 2 约 4 × 50 A100 小时 ≈ 200 A100 小时；合计约 600 A100 小时，8 张 A100 约 3.2 天，在 5 天约束内；阶段 0 可在预研的 2 张 A100 上约 15 小时完成。不需要付费 API。

Frozen Problem Anchor and user constraints:

- **起点问题**：异步（含延迟更新与部分 rollout）agentic RL 中，训练端在 rollout 版本上的 old logits 缺失，使训练–推理偏差修复与策略陈旧度校正无法按语义分开；阈值耦合导致后期崩溃；"无损"加速系统是否保留 old logits 未核对。
- **对象与条件**：PPO/GRPO 类 token 级离策略校正；推理端（vLLM/SGLang）与训练端（FSDP/Megatron）数值不同；rollout 与训练异步，单条轨迹可跨多个参数版本。
- **初始任务/评测**：agentic 多轮工具任务（2605.12070 用 τ²-Bench、VitaBench）；Qwen3-4B 稠密与 Qwen3-30B-A3B MoE；最大版本差 3。
- **瓶颈与证据边界**：精确获取 old logits 的现有方法（快照、专用模型、中断同步）系统代价高；近似参考（插值、EWMA）不恢复语义。原证据只到版本差 3、两种骨干、单框架；后期崩溃机理只有阈值扫描证据。
- **用户约束**：预研 2×A100 80G / 4×L40 48G / 8×4090 24G；正式实验 8×A100 80G，单次最好不超过 5 天；付费 API 1000 元内可自主；token 资源稀缺；目标自 2026-10 起半年内投一篇主会；不做世界模型、视频生成、机器人。预研只回答 go/no-go，先做最便宜的否证检查。
- **进入实验规划的成功条件**：一个候选通过两次独立审查（三项贡献分都 ≥6 且至少两项 ≥8，可行性 pass，verdict 为 experiment_ready，无致命阻断），并给出可在上述算力内完成、能区分主张的最小实验与可复现强基线。
