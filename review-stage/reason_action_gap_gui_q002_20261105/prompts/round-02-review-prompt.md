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
Today's date: 2026-11-05. Known tool workarounds: arXiv 摘要与 HTML 正文可用 WebFetch 或 WebSearch 获取；arxiv.org 偶有限流，可稍后重试或用 arxiv.org/html/<id>；GitHub API 经代理可能返回 403，可用 WebSearch 或 WebFetch 仓库页面
Finish all searches before answering and leave no background tasks running. Do not read other
files in this workspace and do not write files, except your raw review to /home/claude/autoresearch/review-stage/reason_action_gap_gui_q002_20261105/round-02-review.md (UTF-8).
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

**定位关键词：** computer-use agent；inertia（screen–action recurrence）；conversational inertia；reasoning-execution gap；OSWorld

**一句话定位：** 截图驱动的开源 computer-use 智能体在动作未改变屏幕后重复同一动作，且推理常"承认失败"；现有工作把这些步视为同一种"知而不改"并用统一修法处理，修法降低了重复却没有提升任务成功。

**与起点问题的关系：** 原问题；保留对象（开源截图 CUA 在失败后重复或照做）与评测（屏幕–动作重复、失败承认、任务成功），回答"推理与动作在何处断开"时把一个现象拆成可区分的三类并检验它们对修法的不同响应；对训练侧来源只给出一条反证，不做受控训练；指令冲突下的终止不在本研究范围。

## 核心 Claim

成功后新增的认识：GUI 智能体的"知而不改"不是一种失败，而是至少三种机制不同的失败，它们需要不同的修法；这能解释为什么统一修法（激活 steering、R³ 重置搜索、解码屏蔽失败动作）效果小且不一致，并给出"哪类状态该用哪种修法"的可检验依据。三类定义（都以截图核验的"动作后屏幕未变、随后重复同一动作"为前提）：
- **R 复读**：当前推理与近几步内某次推理几乎逐字相同，"承认"也是复读出来的，不是新的判断；
- **F 知而不改**：推理是新生成的，承认失败并指出一个与原动作不同的具体目标，但输出动作仍是原动作；
- **E 假换法**：推理是新生成的，声称"换一种方法"，但所述方法就是原动作（或只是重试）。

可推翻的判断：在至少三个开源 CUA 上，(1) 三类都占截图未变重复步的可观比例，且比例随模型/历史格式明显变化；(2) 存在"修法×类型"交互：对 F 类，只用当前截图与新鲜推理重新解码动作（不带历史中的失败动作串与重复截图）会把动作改成推理所指的目标；对 R 类，这一修法基本无效（推理本身是旧的），而把失败步改写为运行时描述后重新生成推理有效；对 E 类，两种耦合修法都只能换出无关动作，说明问题在推理而非耦合；(3) 统一修法的平均效应可以由类型比例和各类效应加权重现。若三类的修法响应没有差异，本分解没有解释力；若 F 类按推理落地后屏幕变化率与恢复率不高于解码屏蔽，说明新鲜推理所指目标本身并不比模型的次优动作好。

当前依据：
- Absorbed in Inertia（arXiv:2609.37176）在四个开源 CUA 上报告 55–89% 的屏幕–动作重复伴随失败承认（LLM judge），steering 使惯性变化 −33.8% 到 +44.0%，R³ 降惯性 17–55% 但任务分变化不显著；其公开派生数据中 UI-TARS 在 Audacity 任务里推理逐字循环、动作在三个点击之间循环，推理写着要点"Cancel"，执行的却是另一处点击。
- 本轮离线预检（公开 OSWorld-Verified 轨迹，HF `xlangai/ubuntu_osworld_verified_trajs`）：在"动作串与前 3 步内某步相同"的步中对 EvoCUA-8B / UI-TARS / OpenCUA-7B 分别随机抽 400/300/300 步，下载两次出现时的决策截图比较，截图未变的有 155/161/172 步（89%/95%/90% 出现在失败轨迹中）。其中推理与前 6 步内某次推理相似度 >0.9 的复读占 44%/24%/13%，而非重复步上仅 10.1%/4.7%/0.3%；用中英文关键词粗标的新鲜承认占 19%/31%/20%；EvoCUA 的 30 个新鲜承认中 21 个含"different approach/instead"类措辞而动作与原动作相同。标注是正则与字符串相似度，比例需要用 judge 与人工复核。
- Mitigating Conversational Inertia（arXiv:2602.03664）在文本 agent 上发现模型把自己先前的响应当作 few-shot 示范来模仿，支持 R 类机制的存在；Feedback That Backfires（arXiv:2608.23651）在小型文本模型上发现失败调用的表面形式驱动重发、解码屏蔽降重复但不提成功，支持"耦合修法的收益取决于替代动作来源"。
- Say One Thing, Do Another?（arXiv:2510.02204）在移动端单步任务上发现推理指向正确动作而执行出错（execution gap）比反过来更常见，支持 F 类中"推理所指目标往往更好"的预期，但那是单步、非失败后场景。
- 训练侧反证：OpenCUA 训练数据 AgentNet 的公开 Ubuntu 部分 82,448 步中，有 3,832 步紧随被标为上一步错误（`last_step_correct=false`）的步，其中只有 15 步（0.4%）重复了错误动作，45% 的轨迹含错误步；OpenCUA-7B 仍有新鲜承认后重复，所以"只用成功轨迹训练导致动作先验压过推理"不足以解释该模型的这一现象。

仍未知：三类比例在 judge 标注下是否稳定；F 类按推理落地的动作在真实环境中能否改变屏幕、能否推进任务；E 类是否需要推理层面的修法（例如显式记录已尝试动作）才能改善。

## 方法设计的核心思想

输入：公开轨迹中截图核验的"屏幕未变后重复"状态，以及各 agent 的原始提示构造代码（用于从截图与历史响应重建当时的上下文）。

动作：
1. 分类：用 LLM judge（只看当前推理、近 6 步推理与动作串、任务）判定 R/F/E，并抽 150 步人工复核；字符串相似度作为 R 类的机械辅证。
2. 三种修法在同一记录状态上离线施加（teacher-forcing / 重新解码，不需要环境）：
   - A 解码屏蔽：屏蔽与失败动作同类型、坐标在容差内的动作（2608.23651 的规则）；
   - B 推理落地：保留原始带历史生成的新鲜推理，再以"任务 + 当前截图 + 该推理"、不含历史动作串与历史截图的上下文重新解码动作；
   - C 失败步改写：把历史中失败步的原样动作串替换为运行时描述（"点击 (x,y) 后屏幕未变化"）并删去重复截图，重新生成推理与动作。
3. 离线指标：动作是否改变；新动作是否与推理所指目标一致（judge 读推理与动作坐标对应的界面元素）；C 下推理是否从复读变为新内容。
4. 在线指标：把 agent 重放到记录状态（OSWorld 同任务、按记录动作重放），执行各修法后的动作，记录屏幕是否改变，并让 agent 继续运行到结束，记录任务成功。

输出：每个模型的三类比例、"修法×类型"效应表，以及用类型比例加权重现统一修法平均效应的检验。

与最高近邻的关键差别：Absorbed in Inertia 把重复统一定义为"惯性"并测统一修法；CPL 在文本 agent 上处理"模仿自身先前响应"并用训练修复，不区分新鲜推理与复读；Feedback That Backfires 只处理失败调用表面形式；Say One Thing 是单步、无失败历史的推理–执行一致性。本研究在 GUI 失败后的状态上用截图核验区分三类，并检验它们对修法的不同响应。

## 最小实验

**模型与数据：** EvoCUA-8B、UI-TARS（OSWorld-Verified 的 `UI-TARS-0717-100step` 运行）、OpenCUA-7B（`action_history-3image` 50 步运行），均为公开权重与公开轨迹；已核验 traj.jsonl 每步含动作、完整推理与截图文件名，抽查通过区间读取下载截图可行。上下文未落盘，按 OSWorld `mm_agents` 中对应 agent 的代码重建，并用"重建上下文下原动作的贪心复现率"检查重建是否正确（复现率低的模型不进入离线修法实验）。规模：每模型取全部截图未变的重复步（按抽样比例估计 EvoCUA 约 1,500、其余数百到一千余），三类各至少 100 步才做该类的交互检验。

**对照与相同条件：** 三种修法与原策略在同一记录状态、同一模型、同一解码设置下比较；统一修法的已报告效应（R³、steering、Failure notice）来自 Inertia 公开派生数据，用于检验"类型加权能否重现平均效应"；其 policy 阶段代码已核验存在，可在同一 agent 上复跑 R³ 作为在线对照。

**支持/推翻的结果：** 支持：修法×类型交互显著（例如 B 在 F 类上把动作改为推理所指目标的比例显著高于 A，而在 R 类上不高于原策略；C 在 R 类上显著提高新鲜推理比例），在线重放中 F 类经 B 后屏幕改变率与继续运行成功率高于 A。推翻：三类对三种修法响应无差异，或在线 F 类经 B 后的屏幕改变率与成功率不高于 A。

**成本：** 离线分类与修法：GPT 类 judge 约 1 万次调用，费用估计数百元；离线重新解码约 3 模型 × 3,000 状态 × 3 修法，单张 A100 一至两天。在线重放：只对抽出的约 3 模型 × 3 类 × 3 修法 × 50 个状态做重放，每个状态平均重放 20 步、继续运行至多 30 步，按 vLLM + OSWorld Docker VM 并行估计 1–2 天；需要服务器支持 KVM，尚未确认；若不支持，在线部分只能改为在不需要 KVM 的浏览器环境中用同一 agent 自行采集重复状态，覆盖范围缩小到网页任务。

Frozen Problem Anchor and user constraints:

- **起点问题**：开源截图驱动 GUI/computer-use 智能体（UI-TARS、GUI-Owl、OpenCUA、EvoCUA 一类）在推理文本中已承认前一动作失败或指令存在冲突后，下一动作仍重复或照常执行；需要定位推理与动作的耦合在哪里断开、断开的训练侧来源是什么，以及能否据此改善恢复、终止与循环失败。
- **初始任务与评测**：屏幕–动作重复（惯性）检测、ConflictGUI 冲突指令终止、CUA-Recovery / AndroidFlux 类错误恢复成功率；在线桌面/移动环境（OSWorld、AndroidWorld 类）或离线轨迹。
- **瓶颈与证据边界**：现象与激活关联已测，成因未定；激活 steering 不稳定；恢复数据训练有效但不解释“知而不改”；通用 knowing-doing gap 已有非 GUI 研究；承认判定依赖 LLM judge。
- **用户资源约束**：正式实验 8×A100 80GB，单次最好不超过 5 天；预研 2×A100 80GB / 4×L40 48GB / 8×4090 24GB；付费 API（如 GPT judge）1000 元以内可自主决定；token 资源稀缺。在线 Android 模拟器或桌面虚拟机能否在服务器上运行尚待确认，离线轨迹诊断不受此限。
- **时间与目标**：自 2026-10 起半年内投出一篇主会论文。
- **非目标**：不做世界模型、视频生成、机器人方向。
- **进入实验规划的成功条件**：独立 Reviewer 两次（常规 high + 复核 xhigh）判定三项贡献分都 ≥6 且至少两项 ≥8、可行性 pass、`experiment_ready`、无致命阻断；最小实验能在上述算力内完成，强基线有可信复现路线。
