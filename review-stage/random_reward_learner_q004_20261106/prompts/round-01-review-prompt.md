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
Today's date: 2026-11-06. Known tool workarounds: GitHub REST API may return 403; use 'git clone --depth 1' or 'git ls-remote'. arXiv HTML pages (https://arxiv.org/html/<id>v1) are reachable with curl for full text; HF model refs via https://huggingface.co/api/models/<repo>/refs.
Finish all searches before answering and leave no background tasks running. Do not read other
files in this workspace and do not write files, except your raw review to /home/claude/jack836485-rgb/autoresearch/review-stage/random_reward_learner_q004_20261106/round-01-review.md (UTF-8).
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

**定位关键词：** spurious rewards；random rewards；RLVR；GRPO；solution density；mid-training

**一句话定位：** 在随机/虚假奖励 RLVR 中，为什么同一随机奖励信号对不同学习者（同族不同检查点）和不同训练设定给出相反结果。

**与起点问题的关系：** 原问题：保留 OLMo-2-1124-7B 的预训练末（P1）与 mid-training（P2）检查点、合成 GSM 与 2610.01066 的训练协议，回答“学习者一侧什么决定随机奖励的效果”；同时把 2506.10947 / Olmo 3 的大批量设定纳入同一解释。原问题中“mid-training 数据的哪一部分造就了这种学习者状态”仍不回答。

前提证据（均已读原文）：2610.01066 Table 1 在同一缓存 rollout、同一随机奖励下，P2 宽松准确率 13.5→27.2、P1 2.5→5.4；但其 Table 22 用训练前预先指定的前缀评分（截到第一个 `\nQuestion:`）重算同一批运行，P1 从 41.5% 降到 21–29%（10/16、11/16 个运行降超 10 点），P2 从 14.5% 升到约 39%，方向相反并向中间收拢；Table 17 中同一检查点、LoRA 终点范数相近（2.10 vs 2.30）的两种随机输入，一种 16/32 个运行变化超 10 点、另一种 0/32；其已发表的 37 个 OLMo-2 检查点×8 种子结果中，P2 检查点均值增益在 −11.8 到 +26.8 之间跳动，与起点准确率关系很弱。2610.01066 的主扫描是在线采样（每步 1 题×4 条、一次更新，裁剪越界只占 0.24% 步，Table 6），只有 Table 1 是离线；2506.10947 与 Olmo 3 是全参数、低学习率、大批量、每批多次更新，随机奖励对 OLMo 持平，而 2506.10947 附录 B.2 报告每批只更新一次时表现稳定、去裁剪多次更新时极度随机、偶有高分。

## 核心 Claim

若成立，新增的认识是：在每批 rollout 只更新一次、裁剪基本不生效的随机奖励训练里，所谓“学习者效应”不是学习者的潜在能力或“可达性”，而是学习者在其任务提示得分子空间（随机奖励梯度的协方差方向，经 Adam 逐坐标归一）中、按实际输出位移取的**邻域分数分布**相对当前分数的位置：期望增益≈邻域均值−当前分数，高分“大奖”率≈邻域上尾。由此可用的东西是一个免训练、每个检查点几十次前向评测即可得到的预测量，以及一张“输出位移 × 每批更新次数（裁剪漂移）”的设定图，用来解释 2506.10947/Olmo 3 的持平与 2610.01066 的大奖并存，并判断随机奖励结果作为能力探针（2610.01066）或去污染检验（Olmo 3）何时有信息量。

可推翻的判断：(1) 在 37 个已发表检查点上，该邻域预测量对随机奖励均值增益与大奖率的排序预测，显著优于起点准确率/错配模型（2512.16912 式 9）、正确答案对数概率间距、首段分数/格式率，以及各向同性邻域（Neural Thickets）与随机 logit 偏置邻域（PSV）；(2) 它在同一批运行上同时预测宽松评分下 P2>P1 与前缀评分下“P1 降、P2 升”；(3) 用无模板随机 token 提示构造的同范数扰动几乎不改变准确率，与 Table 17 一致；(4) 在匹配输出位移下，一次性扰动、离线缓存游走、在线游走的终点分布一致，而每批多次更新且开裁剪的臂偏离该曲线（漂移项），关裁剪后回到曲线。

当前依据：2610.01066 Thm 9.7 证明随机奖励原始梯度零均值、协方差为 c_G·Fisher，§9.4 给出平滑行为量的期望变化来自协方差×曲率的二阶项；Table 22 的收拢形状、Table 17 的同范数异效、2506.10947 B.2 与 2512.16912（弱模型曲线“像随机游走”）都与“零均值扩散、方向由任务输入决定”一致；Neural Thickets（2603.12228）测得预训练模型邻域中任务提升扰动密度高，并仅在一句话里猜测它与虚假奖励有关。未知：Adam 动量、LoRA 的 BA 非线性与在线采样使 Fisher 沿路径变化，一次性扰动能否近似 500 步路径终点；预测强度与竞争量差距待预研。边界：只主张单次更新、裁剪不生效的区段；Qwen-Math 在裁剪生效设定下的定向收益（2506.10947）归入漂移项，不由本解释覆盖。

## 方法设计的核心思想

输入：一个检查点 θ0、2610.01066 的训练提示与 LoRA 初始化（r8、同种子）、200 题保留集、三种评分（宽松＝论文主评分；严格＝独立 `#### <number>` 行；首段＝Table 22 规则）。

动作：(a) 用 θ0 在 64 个训练提示上各采 4 条回答，抽 Bernoulli(1/2) 奖励、组内标准化，按 2610.01066 的损失求一次 LoRA 梯度；重复 K 次，用 K 个梯度估计逐坐标均方根并归一（模拟 Adam），得到 K 个扰动方向；(b) 把每个方向缩放到目标**输出位移**——训练提示上相对 θ0 的平均逐 token KL，取实际随机奖励运行在 step 500 时测得的值（用少量校准运行测）；(c) 评测 θ0+δ_k，得到邻域分数分布，输出“邻域均值−当前分数”和“分数≥50% 的比例”。对照邻域在同一参数化、同一输出位移下构造：各向同性高斯；用无模板随机 token 提示构造的得分方向；随机 logit 偏置。

与最高近邻的差别：2610.01066 把随机奖励增益解读为学习者的“可达性”，没有零均值扩散的对照，也没有把评分口径与位移尺度作为变量；Neural Thickets 测的是各向同性全权重邻域的密度，没有连到随机奖励 RL，也没有检验其猜测；PSV 说明 logit 偏移可代替权重扰动，作为本文的竞争解释之一被直接比较。本 Idea 的方向来自随机奖励梯度本身的协方差，位移按输出空间匹配，因而能跨 LoRA/全参数、在线/离线比较。

## 最小实验

模型/数据：HF `allenai/OLMo-2-1124-7B` 的 ingredient1 全部 37 个检查点（P1 25 个、P2 12 个，revision 名单在 `mynotwo/rl-random-prob/configs/olmo2_checkpoints.json`，已通过 HF refs API 核实存在，另有 ingredient2/3 两条独立 mid-training 轨迹）；任务与数据为该仓库自带的 `data/synthetic_gsm_rlvr_1000_seed13.jsonl`、800/200 划分（split seed 777）、96 token 上限、贪心评测。

预测目标（已有，不需重跑）：仓库 `results/checkpoint_runs.csv` 中 37 个检查点×8 种子的随机奖励 step-500 宽松准确率（已本地读取并复算，如 P2+5B 均值增益 +26.8、P2+13B −11.8），`shared_rollouts.csv` 的 64 个共享 rollout 终点，Table 22 前缀评分 4 个格子的均值与计数，`input_controls.csv` 的 D/E 终点。严格/首段评分与输出位移需要新运行：训练器只保存前 3 条评测输出，需加一行保存全部输出与 `--save_adapter`。

实验 A（免训练预测）：每个检查点 4 类邻域×K=48，按同一输出位移；比较预测量与已发表结果的 Spearman 相关，检查点级配对 bootstrap 比较各预测量。竞争预测量及路线：起点准确率与 32 次采样正确率代入 2512.16912 式(9)（标准公式）；教师强制正确答案行对数概率间距（标准量）；首段分数与格式率（2610.01066 Table 16/22 规则）；各向同性邻域（已核验 `sunrainyg/RandOpt/randopt.py` 的按 σ 高斯扰动，移植到同一 LoRA 坐标并按输出 KL 缩放）；随机 logit 偏置（2610.40649 §2–3 规则，独立实现：每成员固定高斯偏置向量加到 logits 后贪心解码）。

实验 B（新 RL 运行，用已核验训练器 `src/trainer/rlvr_probe_v2_fixedsplit.py`：组内 token 均值损失、参考项系数 0.01、AdamW、lr 3e-5，支持 `--accum_steps`、`--ppo_epochs`、`--disable_clipping`）：B1 校准 6 个检查点×4 种子，测输出位移并保存全部输出；B2 预先登记样本外：ingredient2/3 的 +5B/+21B/+42B 共 6 个检查点，先写下预测再各跑 8 种子；B3 设定图：P1 末与 P2+5B，臂为 lr∈{3e-6,1e-5,3e-5}（每步 1 题、一次更新）、每批 16 题×4 条一次更新、每批 16 题 8 次 mini-batch 更新开/关裁剪、2610.01066 Table 1 的离线缓存协议，各 8 种子。推翻条件：(i) 邻域预测不优于起点准确率或首段分数；(ii) 各向同性或 logit 邻域预测同样好（说明方向无关或只是 logit 层面）；(iii) 前缀评分下 P1 下降未被预测；(iv) 匹配位移下在线与离线/一次性扰动终点分布显著不同；(v) 样本外检查点预测失效。

算力：单个 RL 运行在一张 80G 卡上约 40 分钟（仓库 README，H100 计）；B1+B2 72 个运行约 50 A100 小时，B3 96 个运行（大批量臂每步采样 16 倍）约 150–200 A100 小时；实验 A 约 43 个检查点×4×48≈8,300 次 200 题×96 token 的贪心评测加梯度计算，约 30 A100 小时；合计约 250 A100 小时，8×A100 约 1.5 天。检查点逐个下载、用完即删以控制磁盘。不需要付费 API 与人工标注。预研（2×A100，约 10 小时）：只做 P1 末与 P2+5B 的 F/各向同性邻域（K=32，两档位移）与 4 个校准运行，检查能否复现 Table 1 与 Table 22 的方向，不能则停。

Frozen Problem Anchor and user constraints:

- 起点问题：在随机奖励 RLVR 中，什么学习者一侧的属性决定同一随机奖励信号能否提高任务准确率；2610.01066 的 OLMo-2 P1/P2 对比显示同 rollout 同奖励下结果相差数倍。
- 对象：base 检查点（尤其 OLMo-2-1124-7B 预训练末 P1 与 mid-training P2 系列检查点），独立 Bernoulli(1/2) 随机奖励下的 GRPO 式更新。
- 条件：2610.01066 的协议（合成 GSM、96 token 上限、LoRA r8、每步 1 题×4 条、500 步、贪心评测、宽松抽取）；对照条件为 2506.10947 / Olmo 3 的大批量在线 GRPO（全参数、每批多次更新、长回答、MATH-500）。
- 初始评测：合成 GSM 200 题保留集的贪心准确率（宽松/严格/首段三种评分），可扩展到 MBPP、组合查找。
- 瓶颈：已有三类解释（rollout 质量/错配、裁剪与熵、污染与记忆）都不能解释同 rollout 同奖励下的学习者差异；2610.01066 的“可达性”只是命名；且其 Table 22 显示该差异对评分口径极敏感，2506.10947 与 Olmo 3 在大批量设定下得到相反结论。
- 证据边界：主要证据来自单一模型家族（OLMo-2）、合成算术、短回答上限；高分运行依赖宽松抽取；2610.01066 的 P1/P2 离线对比无裁剪、无参考项、无权重衰减，与其在线扫描并不完全一致。
- 用户约束：不做世界模型、视频生成、机器人；正式实验 8×A100 80G、≤5 天；预研 2×A100；token 资源紧张；付费 API 1000 元内可自主；目标半年内（自 2026-10 起）投主会。
- 进入实验规划的成功条件：候选有清楚的独立贡献；最小实验能在上述算力内区分主要竞争解释（学习者“可达性”、错配/rollout 质量、裁剪偏置、输出呈现漂移）；所需检查点、代码与数据可得并已核实。
