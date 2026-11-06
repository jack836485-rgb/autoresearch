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
Today's date: 2026-11-05. Known tool workarounds: arXiv 摘要与 HTML 正文可用 WebFetch 或 WebSearch 获取；Hugging Face 模型卡可用 curl https://huggingface.co/<repo>/raw/main/README.md；HF 模型搜索用 https://huggingface.co/api/models?search=<词>；GitHub API 经代理可能 403，可用 git ls-remote
Finish all searches before answering and leave no background tasks running. Do not read other
files in this workspace and do not write files, except your raw review to /home/claude/autoresearch/review-stage/reason_action_gap_gui_q002_20261105/round-04-review.md (UTF-8).
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

**定位关键词：** computer-use agent；inertia（screen–action recurrence）；reinforcement learning；OSWorld；knowing-doing gap

**一句话定位：** 截图驱动的开源 computer-use 智能体在动作没有改变屏幕后常重复同一动作，且推理常"承认"失败；近一年出现了多种在 OSWorld 上做在线 RL 的配方，它们提高了任务成功率，但没有人测过它们让这种惯性变好还是变坏。

**与起点问题的关系：** 原问题的训练侧部分。保留对象（开源截图 CUA）、失败定义（截图核验的屏幕未变后重复、推理承认失败）和评测协议（Absorbed in Inertia 公开的检测与判定流程），直接回答"训练侧来源"中关于 RL 的一支。不提出修法；指令冲突下的终止不在范围内；SFT 阶段的作用只作对照，不作主张。

## 核心 Claim

成功后新增的认识：当前主流的 GUI 在线 RL 配方提升成功率的同时，是在减轻还是加重"知而不改"式惯性，以及这种变化是否跨配方一致。

这个问题在文本 agent 上有两个方向相反的结论：
- Google DeepMind（arXiv:2504.16078）在 bandit 与井字棋上发现，RL 微调能部分缩小 knowing-doing gap；
- RAGEN（arXiv:2504.20073）在多轮 RL 中观察到 Echo Trap，即推理模式坍缩、重复。

GUI 上的答案会直接影响 RL 配方是否需要专门处理"无效步"：如果 RL 普遍加重惯性，那么在成功率之外，还需要一项会被 RL 推高的独立失败指标；如果普遍减轻，惯性就主要是起点模型的问题。

可推翻的判断（送审前固定主指标、方向检验方式与通过标准）：
- **主指标 1（在线）**：每执行动作的惯性率，即截图核验的屏幕–动作重复且推理被判为承认失败，严格沿用 Absorbed in Inertia 的公开检测器与 judge 提示。
- **主指标 2（离线）**：在同一组卡住状态上，失败记录的纠错增益，即上下文含失败步与不含失败步时，重发失败动作的对数概率之差。
- **比较对象**：同一公开初始化与其 RL 后代，共四对：
  - UI-TARS-1.5-7B → ARPO_UITARS1.5_7B；
  - UI-TARS-1.5-7B → DART-GUI-7B（初始化待核实，若不是 UI-TARS-1.5-7B 则剔除）；
  - UI-TARS-7B-DPO → SEAgent-1.0-7B；
  - UI-TARS-7B-DPO → ZeroGUI-OSWorld-7B。
- **判定标准**：只有至少 3 对的 RL 后代在主指标 1 上与初始化同号显著不同（Holm 校正，任务级配对 bootstrap），才下"RL 系统性地加重（或减轻）惯性"的结论；同号对少于 3 对，结论为"效应依配方而异"，并报告哪类配方元素与方向相关。
- **推翻条件**：四对在主指标 1 上都无显著差异，则"当前 GUI RL 改变惯性"被推翻，惯性应归于起点模型。

当前依据：
- **跨家族预检（有混杂，只作动机）**：在公开 OSWorld-Verified 轨迹中，截图核验的屏幕未变重复步里，推理与前 6 步某次推理相似度大于 0.9 的比例为：
  - EvoCUA-8B 44%（非重复步基线 10.1%）；
  - 出自 GUI-Owl 7B 一次 TRPO 桌面 RL 运行的轨迹 55%，且新鲜承认失败只有约 1%；
  - 以 AgentNet SFT 为主的 OpenCUA-7B 13%（基线 0.3%）。
  方向与"RL 加重复读"相容，但家族、数据与规模都不同。
- **"只用成功轨迹 SFT 造成惯性"站不住**：AgentNet 公开 Ubuntu 部分 82,448 步中，3,832 步紧随被标为上一步错误的步，只有 15 步（0.4%）重复了错误动作。
- **测量协议可复用**：Absorbed in Inertia（arXiv:2609.37176）在 UI-TARS-1.5-7B 等四个开源 CUA 上测得 55–89% 的重复伴随失败承认。其代码与派生数据公开，包括检测器、judge、补丁过的 OSWorld 与 OpenComputer。UI-TARS-1.5-7B 正是本研究两个初始化之一，可作为复现锚点。
- **检查点与配方公开**：
  - ARPO 模型卡写明从 UI-TARS-1.5-7B 在 OSWorld 上训练，OSWorld 总体 23.5% → 29.9%，并给出同初始化 GRPO 的 26.0%；
  - SEAgent 与 ZeroGUI-OSWorld 的模型卡 `base_model` 均为 UI-TARS-7B-DPO，论文分别为 arXiv:2508.04700 与 arXiv:2505.23762。

仍未知：
- 四种配方的效应方向；
- 离线纠错增益与在线惯性率是否一致；
- DART-GUI 的初始化。

## 方法设计的核心思想

**输入**：两个公开初始化及其 RL 后代，同一 OSWorld 任务集，同一 UI-TARS 系提示与动作空间（四个后代都沿用 UI-TARS 的格式）。

**动作**：
1. **在线测量**：每个检查点在 OSWorld 上以相同步数上限、温度和截图历史长度运行，用 Inertia 公开的检测器标出屏幕–动作重复，用其 judge 提示判定推理是否承认失败，计算每执行动作的惯性率与任务成功率。UI-TARS-1.5-7B 的惯性率先与 Inertia 已报告值对照，确认协议复现。
2. **离线测量**：取所有检查点在线运行中检出的卡住状态的并集，形成共享状态集。在每个检查点上对每个状态做 teacher forcing，计算纠错增益与重新采样推理的复读率。共享状态集让每个模型都在相同状态上被测，避免"按某个模型自己卡住的地方选状态"带来的同向选择偏差。另外单独报告各模型在自身状态上的结果。
3. **成功率与惯性的联合报告**：判断 RL 带来的成功率提升是否伴随惯性变化。

**输出**：四对的效应量与置信区间，以及结论"系统性加重 / 系统性减轻 / 依配方而异"。

**与最高近邻的关键差别**：
- Absorbed in Inertia 比较四个不同家族的模型，并测激活与修法，没有同初始化的训练阶段对照；
- ARPO、SEAgent、ZeroGUI 只报告成功率；
- DeepMind 与 RAGEN 是文本小环境。

本研究在 GUI 截图–动作循环中，用同初始化的多个独立 RL 配方隔离 RL 这一步对惯性的效应。

## 最小实验

**模型**：UI-TARS-1.5-7B、ARPO_UITARS1.5_7B、DART-GUI-7B（待核实）、UI-TARS-7B-DPO、SEAgent-1.0-7B、ZeroGUI-OSWorld-7B，共 6 个 7B 检查点，权重均已在 Hugging Face 列表中核验存在。

**环境**：OSWorld 全部 369 个任务，每检查点 2 次运行，步数上限 50。
- ARPO 与 ZeroGUI 在 OSWorld 任务上训练过（ZeroGUI 含测试时适应），它们的成功率提升是在训练任务上测的。惯性率比较不依赖这些任务是否被见过，但仍按"ARPO 训练的 128 个任务 / 其余任务"分层报告。
- 虚拟机：优先用服务器上的 OSWorld Docker（需 KVM，开跑前先检查 `/dev/kvm`）。没有 KVM 时，用 OSWorld 官方支持的 AWS provider：6 × 369 × 2 ≈ 4,400 次任务运行，每次约 15 分钟。按小型实例估计约 1,100 实例小时，费用约 300–500 元，在 1000 元内。

**离线部分**：共享状态集预计约 1,000–2,000 个（按已有轨迹中截图未变重复的比例估算），6 个检查点 × 17 次前向，单张 A100 约 2 天。

**判定（送审前固定）**：主指标 1 与主指标 2 各报四对效应量；结论按"核心 Claim"中的 ≥3 对同号显著规则给出；不按动作类型或任务域做显著性检验，只作描述。

**成本**：
- 在线推理：6 个 7B 模型，vLLM，8×A100 约 2–3 天；
- 虚拟机：KVM 或 AWS 约 300–500 元；
- judge 约 2 万次调用，约数百元。
- 总 API 与云费用控制在 1000 元内；若超出，先砍到每检查点 1 次运行。

Frozen Problem Anchor and user constraints:

- **起点问题**：开源截图驱动 GUI/computer-use 智能体（UI-TARS、GUI-Owl、OpenCUA、EvoCUA 一类）在推理文本中已承认前一动作失败或指令存在冲突后，下一动作仍重复或照常执行；需要定位推理与动作的耦合在哪里断开、断开的训练侧来源是什么，以及能否据此改善恢复、终止与循环失败。
- **初始任务与评测**：屏幕–动作重复（惯性）检测、ConflictGUI 冲突指令终止、CUA-Recovery / AndroidFlux 类错误恢复成功率；在线桌面/移动环境（OSWorld、AndroidWorld 类）或离线轨迹。
- **瓶颈与证据边界**：现象与激活关联已测，成因未定；激活 steering 不稳定；恢复数据训练有效但不解释“知而不改”；通用 knowing-doing gap 已有非 GUI 研究；承认判定依赖 LLM judge。
- **用户资源约束**：正式实验 8×A100 80GB，单次最好不超过 5 天；预研 2×A100 80GB / 4×L40 48GB / 8×4090 24GB；付费 API（如 GPT judge）1000 元以内可自主决定；token 资源稀缺。在线 Android 模拟器或桌面虚拟机能否在服务器上运行尚待确认，离线轨迹诊断不受此限。
- **时间与目标**：自 2026-10 起半年内投出一篇主会论文。
- **非目标**：不做世界模型、视频生成、机器人方向。
- **进入实验规划的成功条件**：独立 Reviewer 两次（常规 high + 复核 xhigh）判定三项贡献分都 ≥6 且至少两项 ≥8、可行性 pass、`experiment_ready`、无致命阻断；最小实验能在上述算力内完成，强基线有可信复现路线。
