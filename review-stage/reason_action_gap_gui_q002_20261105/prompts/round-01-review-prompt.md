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
Today's date: 2026-11-05. Known tool workarounds: arXiv 摘要与 HTML 正文可用 WebFetch 或 WebSearch 获取；GitHub API 经代理可能返回 403，可改用 WebSearch 或 WebFetch 仓库页面
Finish all searches before answering and leave no background tasks running. Do not read other
files in this workspace and do not write files, except your raw review to /home/claude/autoresearch/review-stage/reason_action_gap_gui_q002_20261105/round-01-review.md (UTF-8).
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

**定位关键词：** computer-use agent；inertia（screen–action recurrence）；error recovery；unlikelihood training；OSWorld

**一句话定位：** 截图驱动的开源 computer-use 智能体在动作未改变屏幕、且推理已承认失败后仍重复该动作（惯性），这是错误恢复失败的一个常见环节。

**与起点问题的关系：** 原问题；保留对象（开源截图 CUA 的"知道失败却照做"）与评测（惯性、恢复成功率、任务成功率），回答"推理与动作在何处断开"并给出针对断点的训练修法；不做多种训练来源的受控对比，"训练侧来源"仍只部分回答，指令冲突下的照做（awareness-action mismatch）不在本研究范围。

## 核心 Claim

成功后新增两件东西：一是一个可直接测量的量——"失败记录的纠错增益"，即上下文中加入失败步（未改变屏幕的失败动作及其后的截图与推理）后，策略重发该失败动作的对数概率变化——在 7–8B 开源 CUA 的真实失败状态上是否为负；二是一种只用策略自身失败轨迹、不需要正确恢复动作标签、不需要教师或环境验证器的训练修法，把这一项在权重中压下去，并检验它能否比推理时的上下文修法和恢复数据训练更好地转化为恢复与任务成功。

可推翻的判断：(1) 在 OpenCUA-7B 与 EvoCUA-8B 的真实惯性状态上，纠错增益为负，且主要由失败动作的原样动作串与重复截图贡献，推理中的失败承认贡献小；(2) 失败条件化去似然训练使留出任务上的纠错增益转正、惯性率下降，同时普通步骤行为基本不变；(3) 在相同起点模型上，它在 OSWorld 留出任务成功率和 CUA-Recovery 恢复 Pass@3 上不低于 R³ 与恢复数据 SFT。若 (1) 不成立（增益不为负），本修法的前提被推翻；若 (2) 成立而 (3) 不成立，说明"压掉重复"不足以改善成功，这本身限定了惯性在恢复失败中的分量。

当前支持预期效果的依据：Absorbed in Inertia（arXiv:2609.37176）在四个开源 CUA 上发现 55–89% 的屏幕–动作重复伴随推理中的失败承认；在刚发生重复的记录状态上，激活 steering 后仍重复的比例为 69–86%，而清空交互历史后至多 4%，说明重复主要由上下文而非推理时的激活方向决定；但其 R³（重置—搜索—恢复）惯性降 17–55% 而任务分变化不显著。Feedback That Backfires（arXiv:2608.23651）在 135M–1.7B 文本工具调用模型上发现失败记录使重发失败调用的概率上升（候选集上 0.06→0.54），83% 的损害来自失败调用的表面形式，而"标记为失败"的语义贡献小；把原样调用换成运行时描述可去掉 76%，"不要重复"的指令无效。Unlikelihood training（Welleck et al., 2019, arXiv:1908.04319）在文本生成中直接压低重复 token 的概率并降低重复。CUA-Recovery（arXiv:2610.27645）显示在策略自身失败状态上提供监督能转化为恢复与任务成功（MyPCBench 9.2%→24.5%）。

仍未知：上述文本侧结论能否迁移到 7–8B、重度 agent 训练的视觉语言 CUA；GUI 中重复截图是否构成独立的复制通道；去似然后释放的概率质量是否落在有用的替代动作上（R³ 任务分不显著提升是反面信号）；合法重复（等待加载、连续滚动）是否会被误伤。

## 方法设计的核心思想

输入：策略自身在 OSWorld 上的轨迹（截图、推理、动作）。

动作：
1. 用 Inertia 的机械协议检出"动作执行后屏幕不变、下一步对同一屏幕重复同一动作"的状态，并用其公开 judge 提示标注推理是否承认失败；排除 wait、连续滚动等定义上可重复的动作类型。
2. 对每个检出状态构造两份上下文：含失败记录的原始上下文 H_fail，与删去失败步、回到失败前的上下文 H_pre（按各 agent 原始提示构造代码重建）。
3. 训练目标：在 H_fail 上对失败动作的动作 token 施加 unlikelihood 损失 −log(1−p_θ(a_fail|H_fail))；同时在同批次的普通步骤上对冻结的原策略施加 KL，保持正常行为；不提供正确替代动作的标签，推理 token 不参与损失。
4. 推理时不加任何触发器、搜索或额外调用，模型照常运行。

输出：一个权重修改后的策略，以及每个模型在留出状态上的纠错增益 log p(a_fail|H_fail) − log p(a_fail|H_pre)。

与最高近邻的关键差别：R³ 在推理时检测重复、清空历史搜索能改变屏幕的动作，再恢复历史，需要触发条件和额外环境交互，且搜索在无进度上下文下进行；本方法在权重中直接改变"带失败记录时重发失败动作"这一项，保留完整进度上下文，推理零额外开销。恢复数据训练（CUA-Recovery-Train、VeriGUI）需要验证器确认的恢复轨迹或合成失败的正确后续标签；本方法只需要"这个动作失败了"这一可机械判定的负信号。Feedback That Backfires 的改写与解码屏蔽是推理时 harness 修法，且只在小型文本模型上测过。

## 最小实验

**模型与数据：** OpenCUA-7B（Qwen2.5-VL-7B 基座，公开权重）与 EvoCUA-8B（公开权重）。失败状态来自 HF 数据集 `xlangai/ubuntu_osworld_verified_trajs`：已核验含 `evocua_8b_20260105.zip` 以及 OpenCUA-7B 的 15/50/100 步三次运行（文件名标明 `action_history-3image`）；抽查 evocua_8b 一个任务的 `traj.jsonl`，每步含 pyautogui 动作、完整 response（推理 + 动作描述 + tool_call）、截图文件名与 `result.txt`。各步实际输入上下文未落盘，按 OSWorld `mm_agents` 中对应 agent 的提示构造代码从截图与历史 response 重建，重建正确性用"重建上下文下原动作的贪心复现率"检查。数量未知：按 Inertia 报告的重复率估计每模型每次运行数百个检出状态，三次运行合计约一千至两千；不足时用原策略在训练任务上追加采样。按 OSWorld 任务 ID 把任务一分为二，训练状态只取前一半任务，所有评测在后一半任务上进行。

**诊断（先做，最便宜的 no-go 检查）：** 在留出任务的检出状态上，离线 teacher-forcing 计算纠错增益，并做通道替换：(a) 失败步动作串换为运行时描述（如"上一步点击 (x,y) 后屏幕未变化"）；(b) 删除失败后的重复截图；(c) 删去推理中的失败承认句；(d) 组合。若原始纠错增益不为负，停止方法部分。

**对照（相同起点模型、相同 OSWorld 留出任务、相同步数上限 50、相同解码设置）：**
- 原策略；
- R³ 与 Permanent reset、Failure notice：用 Inertia 公开仓库（anonymous.4open.science/r/vlm-agent-defense-D076）的 policy 阶段在相同 agent 上运行；已核验 README 列出 collection、detection、judging、steering、policy 阶段及 patched OSWorld/OpenComputer，原始 episode 未发布；
- 失败描述改写 + 解码屏蔽：按 arXiv:2608.23651 的规则在 GUI 上独立实现（把失败步原样动作串替换为运行时描述、解码时屏蔽与失败动作同类型且坐标在容差内的动作），标明为独立复现；
- 恢复数据 SFT：CUA-Recovery 代码仓库（github.com/xu-hu-2002/CUA-Recovery）在论文中给出，训练集 8.6K 条是否随仓库发布未核实；若可得，按与本方法相同的训练 token 数做 SFT；若不可得，此对照缺失，对应 Claim (3) 的这一半只能限定为"优于推理时修法"；
- 消融：只做 KL 不做 unlikelihood（排除"在失败状态上额外训练"本身的作用）；把 unlikelihood 换成在 H_fail 上对随机非失败动作的同等损失。

**指标：** 留出状态的纠错增益；在线惯性率（每执行动作的承认失败重复率）与屏幕–动作重复率；OSWorld 留出任务成功率（每条件 2 次运行，报任务级配对差与置信区间）；CUA-Recovery 恢复 Pass@3（若其环境能在本地起）；合法重复动作（滚动、等待）的保留率。

**支持/推翻主贡献的结果：** 纠错增益为负 → 训练后转正，惯性率配对下降且置信区间不含零，普通步骤动作一致率 ≥ 原策略的 95%，成功率不低于 R³ → 支持；纠错增益不为负，或训练后惯性下降但成功率与恢复率均不变 → 推翻"压掉失败记录的复制即可改善恢复"。

**成本：** 诊断为离线前向，单张 A100 约一天以内；训练为 LoRA 或全参微调几千个状态，8×A100 数小时。在线评测：2 模型 × 约 6 个条件 × 2 次运行 × 约 185 个留出任务，按 vLLM 推理 + OSWorld Docker 虚拟机并行估计约 3–5 天；需要服务器支持 KVM 以运行 OSWorld 的 Docker provider，这一点尚未确认，若不支持，只能完成离线诊断与离线纠错增益部分。失败承认判定用 GPT 类 judge，按 Inertia 的提示，约几千次调用，API 费用在数百元以内。

Frozen Problem Anchor and user constraints:

- **起点问题**：开源截图驱动 GUI/computer-use 智能体（UI-TARS、GUI-Owl、OpenCUA、EvoCUA 一类）在推理文本中已承认前一动作失败或指令存在冲突后，下一动作仍重复或照常执行；需要定位推理与动作的耦合在哪里断开、断开的训练侧来源是什么，以及能否据此改善恢复、终止与循环失败。
- **初始任务与评测**：屏幕–动作重复（惯性）检测、ConflictGUI 冲突指令终止、CUA-Recovery / AndroidFlux 类错误恢复成功率；在线桌面/移动环境（OSWorld、AndroidWorld 类）或离线轨迹。
- **瓶颈与证据边界**：现象与激活关联已测，成因未定；激活 steering 不稳定；恢复数据训练有效但不解释“知而不改”；通用 knowing-doing gap 已有非 GUI 研究；承认判定依赖 LLM judge。
- **用户资源约束**：正式实验 8×A100 80GB，单次最好不超过 5 天；预研 2×A100 80GB / 4×L40 48GB / 8×4090 24GB；付费 API（如 GPT judge）1000 元以内可自主决定；token 资源稀缺。在线 Android 模拟器或桌面虚拟机能否在服务器上运行尚待确认，离线轨迹诊断不受此限。
- **时间与目标**：自 2026-10 起半年内投出一篇主会论文。
- **非目标**：不做世界模型、视频生成、机器人方向。
- **进入实验规划的成功条件**：独立 Reviewer 两次（常规 high + 复核 xhigh）判定三项贡献分都 ≥6 且至少两项 ≥8、可行性 pass、`experiment_ready`、无致命阻断；最小实验能在上述算力内完成，强基线有可信复现路线。
