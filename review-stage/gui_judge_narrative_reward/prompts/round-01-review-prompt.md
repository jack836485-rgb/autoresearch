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
Today's date: 2026-11-04. Known tool workarounds: arXiv HTML/abs 可直接访问；如 WebFetch 失败可用 export.arxiv.org API
Finish all searches before answering and leave no background tasks running. Do not read other
files in this workspace and do not write files, except your raw review to C:\Users\30473\Desktop\研一\autoresearch\review-stage\gui_judge_narrative_reward\round-01-review.md (UTF-8).
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

**定位关键词：** GRPO、DAPO dynamic sampling、outcome reward model、VLM-as-a-judge、noisy rewards、computer-use agent、AndroidWorld

**一句话定位：** GUI／computer-use 智能体在线强化学习中，用不完美的 VLM 评判器给终局二值奖励时，评判器假阳性如何与 GRPO 的群组相对优势估计相互作用、以及如何在固定评判调用预算下抑制其危害。

**与起点问题的关系：** 子问题。保留起点的对象（VLM 评判器奖励 × CUA 在线 RL）与评价目标（程序化验证的真实成功率），但不再研究“策略利用智能体自述”——主流管线（如 ZeroGUI）已把智能体回复排除在评判输入之外——而研究叙述隔离之后仍然存在的假阳性在群组归一化下的放大；“策略是否会学会迎合评判器叙述”这一原问题本候选不回答。

## 核心 Claim

**成功后新增什么：** 一个关于“评判器奖励 × 群组相对 RL”的机制判断，以及一个据此设计、可直接替换现有奖励估计器的复核分配规则。

**机制判断（可推翻）：** 在评判器假阳性率 FPR 与真阳性率 TPR 固定时，一个任务组内阳性为假的后验概率是 FPR·(1−p)/(FPR·(1−p)+TPR·p)，随该任务当前真实成功率 p 下降而迅速升高；而 GRPO 的组内标准化给低成功率组中的孤立阳性最大的正优势（G 条轨迹中唯一阳性的标准化优势约为 √(G−1)），DAPO 动态采样又会丢弃全 0 组、只保留含阳性的组。因此在评判器奖励下，假阳性在“正优势质量”中的占比应显著高于它在全部阳性中的占比，且集中在难任务上。若程序化真值显示假阳性比例与组成功率无关，或其优势质量占比不高于阳性占比，则该判断被推翻。

**方法 Claim（可推翻）：** 在与 ZeroGUI 均匀投票相同的评判调用总数下，把复核预算集中到“组内阳性占比 ≤τ 的阳性”（少数阳性）上，可比均匀投票和全局噪声率校正得到更高的保留任务程序化验证成功率，增益主要出现在基座成功率低的任务上。

**当前支持预期效果的依据：**
- ZeroGUI（arXiv:2505.23762，§4.3 奖励估计消融，UI-TARS-7B-DPO 在生成任务上的人工标注轨迹）：其最佳估计器（全部截图、排除回复、Qwen2.5-VL-32B 4 次 T=1.0 全员一致投票）精度仅 61.5%、召回 51.1%，即约 38.5% 的阳性为假；加入智能体回复后精度降到 44.3%、召回升到 74.5%，下游 OSWorld 成功率反而从 27.2 降到 24.0——成功率随精度而非召回变化，作者结论是假阳性危害大于假阴性。
- OSReward（arXiv:2607.28609）：跨平台 CUA 轨迹上过度接受约占全部评判错误的 2/3；在“近似完成”占比高的困难集上，所有评判器准确率下降 20–43 个百分点。
- 上面的后验公式与 GRPO 标准化优势公式是确定的代数关系；按 ZeroGUI 级别精度，难任务上（p≈0.1）多数阳性为假是直接推论。
- 仍未知：FPR 本身是否随组成功率变化（困难任务的近似完成轨迹可能 FPR 更高，会加强效应）；复核器（更多票＋更强评判器）对少数阳性中的近似完成轨迹能否显著降低假阳性；节省的调用重新分配后，组内少数阳性的复核是否比在全部轨迹上均匀投票更能改善最终成功率——这三点只有实验能回答。

## 方法设计的核心思想

输入：每个训练步的 GRPO 组（同一任务实例 G 条轨迹，每条含逐步截图与动作，不含智能体 thought/回复）。动作：
1. 每条轨迹先做 1 次廉价评判（ZeroGUI 同款提示与输入，Qwen2.5-VL-32B），得 v_i∈{0,1}，组内阳性数 k。
2. 若 k/G ≤ τ，对这些少数阳性升级复核：额外多次投票（全员一致）并加一次更强评判器（Qwen2.5-VL-72B 或付费 API 模型）判定，只有全部通过才保留奖励 1；k/G>τ 的组直接采用 v_i。
3. 复核预算上限与 ZeroGUI 的“每条 4 次调用”对齐；未用完的预算按同规则依次扩大到次少数阳性，保证总调用数不超出均匀投票。
输出：替换后的二值奖励，送入不变的 GRPO+DAPO 更新。

与最高近邻的差别：ZeroGUI 对每条轨迹做相同次数投票；Cai et al.（arXiv:2510.00915）用全局 FP/FN 率做后向/前向校正，假设噪声率与任务和组无关。本方法不改评判器本身，而是用组内位置与基率决定“哪条轨迹值得花复核预算”，与 VeriCUA、AdaptRubric 等改进评判器的工作正交，可叠加。

## 最小实验

**环境与模型：** AndroidWorld（google-research/android_world，116 个参数化任务类，每类有程序化 `is_successful` 检查）；按任务类划分训练/保留集，并在训练类上另取未见参数实例。策略 UI-TARS-1.5-7B（或 Qwen2.5-VL-7B），GRPO＋DAPO 动态采样，G=8，相同步数、学习率、KL；训练奖励只来自评判器，程序检查只用于分析与评测。服务器需 KVM 以并行运行约 32 个模拟器（尚未核实；若不可用，改用 WebArena-Lite Docker 环境及其规则评测，设计不变）。

**第 1 步（诊断，无训练）：** 基座策略在约 120 个训练任务实例上各采样 16 条轨迹（约 1,900 条），分别得到单次评判、4 票全员一致评判与程序真值；报告按组真实成功率分箱的阳性假阳性比例，以及假阳性在 GRPO+DAPO 正优势质量中的占比，直接检验机制判断。

**第 2 步（RL 对照）：** 同一初始化、同等评判调用预算下的 4 个竞争臂＋1 个上界：
- (a) 单次评判奖励；
- (b) ZeroGUI 均匀 4 票全员一致（已核验仓库 OpenGVLab/ZeroGUI，沿用其提示与投票规则，移植到 AndroidWorld 动作空间）；
- (c) Cai et al. 后向/前向噪声校正（已核验仓库 caixq1996/noisy-RLVR；FP/FN 率用 200 条训练类规则验证轨迹估计；该类方法亦以 arXiv:2606.24515 为代表，其仓库 martasumyk/rl_with_autonomous_feedback 已核验，作为同类近邻不单独开臂）；
- (d) 本方法（τ 在诊断集上选定，训练前固定）；
- (e) 程序规则奖励上界。

**支持/推翻：** 主指标为保留任务的程序验证成功率，分基座成功率 <0.2 的难任务与其余任务报告；机制指标为训练中“携带正优势的阳性”的假阳性比例（用程序检查事后核对）。若 (d) 在难任务上不优于 (b)(c)，或其正优势阳性的假阳性比例不低于 (b)，方法 Claim 被推翻。

**成本估算：** 每臂约 120 步×64 条轨迹≈7,700 条、约 11.5 万环境步；按每步约 2.5 秒、32 个模拟器并行，环境时间约 2.5 小时；评判调用约 2.3 万次以内（32B 本地 vLLM），训练与推理合计每臂约 10 小时，5 个臂加诊断约 2–2.5 天，8×A100 内完成；若使用付费 API 作强复核器，只用于少数阳性，估计每臂数千次调用、总计 <500 元。主要不确定是模拟器并行所需的 CPU/内存与 KVM。

Frozen Problem Anchor and user constraints:

- **起点问题：** 用不完美的 VLM 评判器作为 GUI/computer-use 智能体在线 RL 的结果奖励时，评判器的系统性错误（以过度接受为主、依赖智能体自述）如何进入并扭曲策略学习。
- **对象与条件：** 多步 GUI 智能体（截图观测、点击/输入动作），基于 GRPO 类群组相对优化的在线 RL，终局二值奖励来自 VLM 评判器而非程序化验证器。
- **初始任务/评测：** OSWorld、AndroidWorld、AndroidLab、WebArena 一类带程序化成功检查的环境（程序化检查只作真值分析与评测）；评判器可靠性基准 OSReward、AgentRewardBench。
- **瓶颈与证据边界：** 评判器错误已在静态轨迹集上测量（OSReward），但没有研究评判器错误在 RL 训练中如何分布、被放大或被利用；小模型 GRPO 增益本身脆弱（2607.12640）。
- **用户约束：** 预研 2 张 A100 80G（或 4 张 L40 48G / 8 张 4090）；正式实验最多 8×A100 80G、最好 ≤5 天；token 稀缺；付费 API（如 GPT judge）1000 元内可自主决定；目标半年内（自 2026-10 起）投主会。服务器为 ssh 远程开发；当前未核实服务器是否具备 KVM/Docker（Android 模拟器或 OSWorld 虚拟机需要）。
- **非目标：** 不做纯静态评判器审计或新 benchmark；不做安全/注入攻防。
- **进入实验规划的成功条件：** 有一个在用户算力下可完成的最小实验，能在同一任务、同一策略初始化、同等评判调用预算下，区分本方案与强基线（含现有评判器去偏/投票/噪声校正方法）对程序化验证成功率的影响。
