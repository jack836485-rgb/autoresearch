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
Today's date: 2026-11-03. Known tool workarounds: huggingface.co 本地直连超时，可用 hf-mirror.com；raw.githubusercontent.com 可能超时
Finish all searches before answering and leave no background tasks running. Do not read other
files in this workspace and do not write files, except your raw review to C:\Users\30473\Desktop\研一\autoresearch\review-stage\ai4ai_strategy_lockin_rq004_20261103\round-03-review.md (UTF-8).
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

**定位关键词：** PostTrainBench；strategy-level capability（策略层面能力）；plan continuation bias（计划延续偏差）；premature commitment（过早承诺）；inertia bias；stopping rule／futility boundary（停止准则／无效性边界）

**一句话定位：** 在 LLM agent 自动后训练（PostTrainBench：给定基座模型、目标基准与限时单卡预算，自主完成数据、训练与评测）中，agent 跑完第一轮训练后几乎从不更换训练策略。人类在中途指名一个替代策略可以显著提分，泛泛地提示“重新考虑”则无效。

**与起点问题的关系：** 原问题。保留对象、任务与预算形式，研究没有人类时如何回收人类中途指令的收益，以及其中哪个成分起作用。起点问题中“锚定、信号不足、模型偏好”三者的完整分离只通过消融部分回答。

## 核心 Claim

**主贡献（若成立）：** 一种不需要人类、不需要训练的研究策略修订机制，并用消融把“人类中途指令为什么有效”拆成可复用的成分。

机制是“事前策略合约”：在开训之前，agent 尚未投入、不受事后惯性影响，此时由它写下：
- 所选策略在每个评测检查点的预期分数区间；
- 一个可机械判定的切换触发条件；
- 一个指名的备选策略及其启动方式。

运行中由外部监控器机械检查触发条件。触发时把指名备选作为指令交给 agent，形式与人类中途指令相同。

**可推翻的判断：** 在相同预算下：
1. 完整合约的最终测试分显著高于原 agent，也高于“检查点泛化重新考虑”；
2. “只给触发、不给备选”时收益基本消失；
3. “只给备选、由 agent 自行决定是否采用”时收益明显小于完整合约。

若 1 不成立，或者 2 中只给触发与完整合约等效，主张即被推翻。

**目前支持预期的依据（均非本方案的结果）：**
- **指名的替代方案是有效成分。** 在同一 checkpoint、同一剩余预算下，人类指名切换（GSM8K：SFT→GRPO；HumanEval：SFT→执行反馈训练；AIME：SFT→GRPO+可验证奖励）在三个基准上都胜过 agent 自己续写，最多 +17.44 分。不指名替代、只要求重新考虑的分叉，全部重申原策略（arXiv:2608.19072 §4.3、附录 D.2、D.2.3；样本为少量分叉）。
- **事后判断受惯性影响，事前制定可以避开。** 在观测受控时，agent 评估“自己先前动作”的结果明显差于评估他人动作（IBIS，arXiv:2608.23045）。
- **投入之前 agent 对策略建议是开放的。** 训练前的人类审阅能改变 agent 锁定在哪个策略上（2608.19072 §4.3.1）。
- **跨领域成熟做法。** 航空用事前设定的复飞准则对抗计划延续偏差；临床试验用预注册的无效性边界决定中止。

**未知：**
- agent 自己事前指名的备选，质量能否接近人类指名；
- 事前预期区间是否校准。LLM 会系统性低估实验结果的变化幅度（arXiv:2610.22599），触发可能误报或漏报；
- 所用 agent 模型是否复现锁定。

## 方法设计的核心思想

**输入：** 官方任务描述与预算。

**动作：**
1. **开训前的合约步骤。** agent 用固定模板写出主策略、各检查点的预期分数区间、切换触发（例如“第 k 次评测的分数低于预期下限”或“连续两次评测提升小于 δ”）、指名的备选策略与启动步骤。合约写入只读文件。
2. **运行中由 harness 外部的监控器执行。** 每次官方评测完成后，用规则比对合约；触发时向 agent 注入固定格式的指令：“按合约切换到 <备选>，剩余预算 T”。监控器不调用 LLM。
3. **每次运行至多触发一次。** 切换之后不再干预。

**输出：** 最终提交的 checkpoint 与官方测试分；记录合约、触发时刻与切换前后的分数。

**与最高近邻的关键差别：**
- 2608.19072 证明人类指名有效、不指名无效，但没有给出无人类的机制，也没有拆分“指名”与“触发”。
- IBIS 与 HMA 用上下文隔离改善判断，但切换决定仍由 agent 当场做出。
- 通用 agent 中的证据门控（ECLoop，2607.28815）、声明计划加排序备选（2609.38108）、阶段停止准则（Sakana，2606.15497）都不在研究策略层面，也不是事前预期与触发相结合。

## 最小实验

**任务：**
- PostTrainBench 官方 harness（github.com/aisa-group/PostTrainBench，已核验，含 opencode、glm5、kimi_claude、qwen3max 等 agent 入口）。
- 基准 GSM8K、HumanEval，基座 Qwen3-1.7B-Base，即 2608.19072 中人类指名切换有收益的设定。
- 预算：每次运行 10 小时、单张 A100。官方为单张 H100 10 小时，A100 约慢一倍；所有臂相同，原文数值只作参照。

**agent 模型：**
- 一个低价 API 模型，候选 GLM-5、Kimi K2.6、Qwen3-Max，都有官方入口和公开轨迹（hf-mirror 上的 aisa-group/PostTrainBench-Trajectories 已核验含 opencode_zai_glm-5、opencode_kimi-k2.6、qwen3max 目录）。
- 实验前，先按 2608.19072 附录 A 的规则（训练算法或数据来源改变）离线标注候选模型公开轨迹的相邻训练切换率，选锁定明显的模型。若都不锁定，该设定不成立，实验停止。

**臂（同一 agent 模型、同一预算）：**
1. 原 agent（官方提示）；
2. 检查点泛化重新考虑：按 2608.19072 D.2.3 规范，每次评测后注入“重新考虑当前策略、不指名替代”；
3. 检查点上下文隔离重判：IBIS／HMA 原则，每次评测后新开一个会话，读工作区与日志后判断继续还是切换；
4. 完整合约；
5. 只给备选：合约只写备选，检查点上作为选项提示，由 agent 决定；
6. 只给触发：触发时注入泛化重新考虑。

臂 1、4 各 3 个种子，其余各 2 个种子，2 个基准，共 26 次运行。

**观察量：**
- 官方测试分；
- 切换率、触发率；
- 自定备选与 2608.19072 人类指名备选是否相同；
- 预期区间的命中率（校准）；
- 污染与违规模型判定（官方 judge）。

**支持主张：** 4 显著优于 1 和 2；6 接近 1；5 介于两者之间。

**推翻主张：** 4 不优于 1；或者 6 与 4 等效。

**成本估算：**
- 26 次 × 10 小时 ≈ 260 A100 小时。8 卡并行约 1.5 天，加试跑约 2 天。
- API：低价模型每次运行估 1500 万–3000 万 token，以缓存命中为主，约 20–45 元／次，合计约 600–1200 元，可能略超 1000 元。超出时先把臂 5、6 降为各 1 个种子。
- 离线标注公开轨迹约 100 条，LLM 辅助加人工抽检，约 1 人日。

Frozen Problem Anchor and user constraints:

- **起点问题**：LLM agent 在 AI 研发任务（以自动后训练为主：给定基座模型与目标基准，自主设计数据／训练／评测并提交 checkpoint）中，执行层面能干，但策略层面（数据来源、训练范式、目标能力等高层选择）很少随实验反馈修订。
- **对象与条件**：前沿或开源 agent 作为研究者；训练对象为 1.7B–4B 小基座；单卡、限时的训练预算；评测为固定基准的 pass@1／pass@k。
- **初始任务／评测**：PostTrainBench（Rank et al., 2026；arXiv:2603.08640）；可参照 RSIBench-Data、AI4AI-Bench。
- **瓶颈**：锁定来源未分离（锚定／信号不足／模型偏好）；已有修法依赖外部人类或强制多样性。
- **证据边界**：主证据来自同一份轨迹分析（2608.19072）；其余为摘要层。
- **用户约束**：
  - 算力：可用 8×A100 80G，单个实验最好不超过 5 天；预研阶段常用 2×A100 / 4×L40 / 8×4090。
  - API：付费 API 1000 元以内可自主使用，效果很好时可追加。
  - token 稀缺；目标 2027-04 前投出主会论文（自 2026-10 起半年）。
  - 实验代码与数据放在服务器（ssh），不在本地。
  - 非目标：不回到 OPSD 方向；本 skill 不运行实验。
- **进入实验规划的成功条件**：候选通过两次独立审查（三项贡献 ≥6 且至少两项 ≥8、可行性通过），其最小实验能在上述算力与 API 预算内完成，并能区分其主张。
