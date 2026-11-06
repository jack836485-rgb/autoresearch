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
Today's date: 2026-11-05. Known tool workarounds: arXiv 摘要与 HTML 正文可用 WebFetch 或 WebSearch 获取；arxiv.org 偶有限流，可稍后重试；Hugging Face 模型卡可用 curl https://huggingface.co/<repo>/raw/main/README.md 读取；GitHub API 经代理可能返回 403，可用 git ls-remote
Finish all searches before answering and leave no background tasks running. Do not read other
files in this workspace and do not write files, except your raw review to /home/claude/autoresearch/review-stage/reason_action_gap_gui_q002_20261105/round-03-review.md (UTF-8).
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

**定位关键词：** computer-use agent；inertia（screen–action recurrence）；reinforcement learning；Echo Trap；knowing-doing gap

**一句话定位：** 截图驱动的开源 computer-use 智能体在动作没有改变屏幕后，常重复同一动作，且推理里常"承认"失败；这种惯性从哪一个训练阶段来，目前没有受控证据。

**与起点问题的关系：** 原问题的训练侧部分。保留对象（开源截图 CUA）、失败状态（截图核验的屏幕未变后重复）和三种候选解释，直接回答"训练侧来源是什么"。不提出修法；指令冲突下的终止不在范围内。

## 核心 Claim

成功后新增的认识：对 GUI agent 的"知而不改"，RL 微调到底是加重还是缓解，以及作用在哪一环。候选的三环是：
- 失败记录被当作可复制的示范；
- 推理自我复读；
- 新鲜的失败承认没有转成不同的动作。

这决定 GUI agent 的 RL 配方是否需要针对"无效步"的专门处理。目前文本 agent 上有两个方向相反的结论：
- Google DeepMind（arXiv:2504.16078）在 bandit 与井字棋上发现，RL 微调能部分缩小 knowing-doing gap；
- RAGEN（arXiv:2504.20073）在多轮 RL 中观察到 Echo Trap，即推理模式坍缩并重复。

GUI 上还没有人用同底座的 RL 前后检查点检验过这个问题。

可推翻的判断：用同底座、只差一步桌面环境 RL 的公开检查点对，在完全相同的、已记录的卡住状态上离线比较以下三项：
1. 纠错增益：上下文含失败步与不含失败步时，重发失败动作的对数概率之差；
2. 自我复读率：在卡住状态重新采样推理时，与前几步推理几乎逐字相同的比例；
3. 承认–动作耦合：重新采样得到的推理新鲜地承认失败时，动作与失败动作不同的条件概率。

RL 检查点在其中至少一项上与 RL 前检查点有显著差异，且方向在两个检查点对上一致。三项都无差异，则"训练侧来源在 RL"被推翻，惯性应归于底座或 SFT 阶段。

当前依据：
- **跨家族的预检结果（相关，有混杂）**：在公开 OSWorld-Verified 轨迹中抽取截图未变的重复步（像素比较判定屏幕未变），推理与前 6 步某次推理相似度大于 0.9 的比例如下：
  - 以 RL 训练著称的 EvoCUA-8B：44%（非重复步基线 10.1%）；
  - UI-TARS：24%（基线 4.7%）；
  - 以 AgentNet SFT 为主的 OpenCUA-7B：13%（基线 0.3%）。
  这一结果与"RL 加重复读"相容，但模型家族、数据和规模都不同，不能归因。
- **"只用成功轨迹 SFT 造成惯性"站不住**：OpenCUA 的训练数据 AgentNet（Ubuntu 公开部分）共 82,448 步，其中 3,832 步紧跟在被标为上一步错误的步之后，只有 15 步（0.4%）重复了错误动作；而 OpenCUA-7B 仍会在新鲜承认失败后重复。
- **两条文本侧机制都有现成依据**：
  - Feedback That Backfires（arXiv:2608.23651）在 ≤1.7B 指令模型上发现，失败记录的纠错增益为负，83% 来自失败调用的表面形式；
  - Mitigating Conversational Inertia（arXiv:2602.03664）发现 agent 把自己先前的响应当 few-shot 来模仿；
  - Absorbed in Inertia（arXiv:2609.37176）在四个开源 CUA 上发现 55–89% 的重复伴随失败承认，并且清空历史后重复至多 4%，说明惯性主要经由上下文起作用。
- **检查点对可得**：`mPLUG/GUI-Owl-7B` 与 `mPLUG/GUI-Owl-7B-Desktop-RL` 都以 Qwen2.5-VL-7B-Instruct 为底座。后者的模型卡写明是"专门为桌面环境做 RL 调优的 GUI-Owl 变体，用于验证环境 RL 的改进"。

仍未知：
- Desktop-RL 的初始化是否正是公开的 GUI-Owl-7B 权重（模型卡未明说），以及它的 RL 奖励与步数；
- 离线三项是否预测在线惯性率；
- 第二个检查点对的选择（见最小实验）。

## 方法设计的核心思想

**输入**：从 OSWorld-Verified 公开轨迹中，按"动作执行后截图未变、下一步对同一屏幕重复同一动作"机械检出的卡住状态。主体用 GUI-Owl-7B 自己的轨迹（`mobile-agent-v3-gui-owl-7b.zip`，已核验存在于该数据集），即对 RL 前模型是在策略状态。

**动作**：
1. **重建上下文**：按 Mobile-Agent-v3 公开 cookbook 的提示格式，重建每个卡住状态当时的输入（任务、历史动作与推理、最近截图）。用"重建上下文下原动作的贪心复现率"检验重建是否正确，复现率不足 80% 的状态剔除。
2. **对两个检查点做同样的三项测量**：
   - 纠错增益：比较含失败步的上下文 H_fail 与删去失败步的 H_pre 下，失败动作 token 的对数概率差；
   - 复读率：在 H_fail 下各采样 16 次推理，计算其与前 6 步推理的最大字符相似度，超过 0.9 计为复读；
   - 耦合：在采样中，挑出经 judge 判为"新鲜承认失败"且非复读的推理，计算随后动作不同于失败动作的比例。
3. **分层**：按动作类型（点击、热键、输入）与任务域分层报告，并做任务级 bootstrap。

**输出**：每个检查点对在三项上的差值及置信区间，以及"RL 作用在哪一环"的判断。

**与最高近邻的关键差别**：
- Absorbed in Inertia 比较的是四个不同家族的模型，并测激活与修法，没有同底座的训练阶段对照；
- Feedback That Backfires 只测小型文本模型，不涉及 RL 前后；
- DeepMind 与 RAGEN 是文本小环境。

本研究在 GUI 截图–动作循环的真实卡住状态上，用同底座检查点对隔离 RL 这一步的效应。

## 最小实验

**检查点对**：
- 主对：GUI-Owl-7B 与 GUI-Owl-7B-Desktop-RL（两者权重公开，已在 HF 列表中核验存在）。
- 第二对：用同一 RL 前检查点 GUI-Owl-7B，在 OSWorld 训练任务上自行做一小段 GRPO 桌面 RL，得到"同初始化、已知配方"的 RL 检查点。这样既能确认主对的结论不来自初始化差异，又能剂量化（取 RL 0/50/100/200 步的检查点，看三项是否随步数单调变化）。需要 OSWorld Docker VM，服务器是否支持 KVM 尚未确认；不支持时第二对改用 AndroidWorld 之外的可用网页环境，或只报告主对并标明为单对证据。
- 对照：底座 Qwen2.5-VL-7B-Instruct（同格式提示）作为"未经 GUI 训练"参照；OpenCUA-7B（以 AgentNet SFT 为主，同底座家族）作为"SFT 路线"参照，用以把 SFT 与 RL 的效应分开。

**数据**：GUI-Owl-7B 的 OSWorld-Verified 轨迹约 361 条。按 EvoCUA-8B 与 OpenCUA-7B 的预检比例估计，截图未变的重复状态有数百个；不足时，从同数据集中 OpenCUA-7B 三次运行的状态补充，作为离策略状态单独报告。judge 用 GPT 类模型，按 Inertia 公开的承认判定提示，人工复核 150 个。

**支持 / 推翻的结果**：
- 支持：主对在至少一项上的差值置信区间不含零；第二对方向一致，且随 RL 步数单调变化；SFT 参照（OpenCUA-7B 相对底座）的变化方向与 RL 不同或不显著。
- 推翻：主对与第二对在三项上都无显著差异，或方向相反。

**成本**：
- 主对与参照都是离线前向与采样：4 个 7B 模型 × 约 500 个状态 × 17 次前向，单张 A100 约 1–2 天；
- 第二对的 GRPO 小段训练：8×A100 约 2–3 天，需 OSWorld VM；
- judge 约 1 万次调用，费用数百元。

Frozen Problem Anchor and user constraints:

- **起点问题**：开源截图驱动 GUI/computer-use 智能体（UI-TARS、GUI-Owl、OpenCUA、EvoCUA 一类）在推理文本中已承认前一动作失败或指令存在冲突后，下一动作仍重复或照常执行；需要定位推理与动作的耦合在哪里断开、断开的训练侧来源是什么，以及能否据此改善恢复、终止与循环失败。
- **初始任务与评测**：屏幕–动作重复（惯性）检测、ConflictGUI 冲突指令终止、CUA-Recovery / AndroidFlux 类错误恢复成功率；在线桌面/移动环境（OSWorld、AndroidWorld 类）或离线轨迹。
- **瓶颈与证据边界**：现象与激活关联已测，成因未定；激活 steering 不稳定；恢复数据训练有效但不解释“知而不改”；通用 knowing-doing gap 已有非 GUI 研究；承认判定依赖 LLM judge。
- **用户资源约束**：正式实验 8×A100 80GB，单次最好不超过 5 天；预研 2×A100 80GB / 4×L40 48GB / 8×4090 24GB；付费 API（如 GPT judge）1000 元以内可自主决定；token 资源稀缺。在线 Android 模拟器或桌面虚拟机能否在服务器上运行尚待确认，离线轨迹诊断不受此限。
- **时间与目标**：自 2026-10 起半年内投出一篇主会论文。
- **非目标**：不做世界模型、视频生成、机器人方向。
- **进入实验规划的成功条件**：独立 Reviewer 两次（常规 high + 复核 xhigh）判定三项贡献分都 ≥6 且至少两项 ≥8、可行性 pass、`experiment_ready`、无致命阻断；最小实验能在上述算力内完成，强基线有可信复现路线。
