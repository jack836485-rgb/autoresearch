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
files in this workspace and do not write files, except your raw review to /home/claude/jack836485-rgb/autoresearch/review-stage/random_reward_learner_q004_20261106/round-03-review.md (UTF-8).
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

**定位关键词：** spurious rewards；random rewards；RLVR；mid-training；WiSE-FT；weight interpolation

**一句话定位：** 在随机/虚假奖励 RLVR 中，同一随机奖励信号对同族不同检查点（学习者）给出相反结果，学习者一侧由什么决定。

**与起点问题的关系：** 原问题：保留 OLMo-2-1124-7B 预训练末（P1）与 mid-training（P2）检查点、合成 GSM 与 2610.01066 的训练协议，直接回答“为什么仅 5B token 的 mid-training 就让随机奖励起作用”；用 OLMo-3-7B、SmolLM2-1.7B 的公开中间检查点做外部检验。没有中间检查点的模型（Qwen、Llama）与全参数大批量设定（2506.10947、Olmo 3 RL-Zero）不在主张范围内。

前提证据（均已读原文）：2610.01066 Table 1 中两个学习者收到同一缓存 rollout 与同一随机奖励，P2 宽松准确率 13.5→27.2、P1 2.5→5.4；Table 22 用训练前指定的前缀评分（截到第一个 `\nQuestion:`）重算同一批运行，P2 从 14.5% 升到约 39%、接近 P1 的起点 41.5%，P1 则降到 21–29%；§11.7 中 P2 输出里含 `####`/`\boxed` 的比例从 93.5% 降到约 50%，严格准确率 7.0%→约 2.7%；Table 7 里 15 个宽松 ≥50% 的随机运行严格分几乎全为 0、多数格式率为 0。OLMo 2 报告（2501.00656 §2.3）说明 mid-training 是在预训练末换成 Dolmino 数据并重新拉起学习率、再线性衰减到 0。已发表的逐种子结果中，12 个 P2 检查点的随机奖励均值增益从 −11.8 到 +26.8，与起点准确率几乎无关；OLMo-3 的 O4（mid-training +100B）随机种子终点从 4% 到 90%，高于其前后检查点的冻结分与首段分（Table 15/16）。

## 核心 Claim

若成立，新增的认识是：在这类随机奖励训练中，学习者效应主要来自**学习者最近一段训练的可逆性**——零均值的随机奖励更新优先撤销最近、尚未巩固的训练变化，把输出往上一阶段拉回；因此平均增益约等于“沿当前检查点与上一阶段检查点之间的权重插值，部分撤销最近训练所能达到的分数”减当前分数（插值余量）。2610.01066 所称 mid-training 起步时出现的“自学阶段”，在此解读下是阶段切换带来评分下降后的回升，而不是新的自我提升；P1 末在前缀评分下变差，是因为其最近的变化恰好提高了该评分。可用的东西是一个用检查点历史在训练前算出的预测量，以及判断“随机奖励增益是否只是撤销了上一阶段”的方向检验。

可推翻的判断：(1) 随机奖励训练引起的逐 token 对数概率变化，与“当前→上一阶段检查点”的变化同向，显著强于与“当前→下一检查点”的变化、以及与匹配输出 KL 的随机奖励梯度方向扰动和各向同性扰动的同向程度；(2) RL 把错题翻对的题目集中在上一阶段或插值最优点答对的题上，把对题翻错的集中在上一阶段答错的题上；(3) 插值余量预测各检查点的随机奖励均值增益，好于起点准确率/错配模型、首段分数与格式率、随机奖励梯度方向邻域，并在预先登记的 ingredient2/3 检查点上成立；(4) 在三种评分下给出与 Table 22 一致的方向（宽松下 P2 涨、前缀下 P1 降）。

当前依据：上述 Table 22、§11.7、Table 7 都表现为离开 mid-training 才装上的答案约定、向 P1 的首段水平回落；遗忘可逆性研究（2505.16831）显示最近被压下的行为可由少量无关训练恢复；推理模型上的 WiSE-FT（2504.10478）显示新旧检查点之间的权重插值常常优于两端，为“部分撤销＋混合可超过两端”提供依据；2610.01066 Thm 9.7 给出随机奖励噪声协方差∝任务提示上的 Fisher，即噪声集中在当前输出最敏感、往往也是最近被训练改动的方向（后一环节是本 Idea 的假设，未有直接证据）。不利与未知：O4 的 90% 高于前后检查点，单纯撤销不够，必须由插值超过两端解释，若插值路径达不到则本解释对 O4 失效；rank-8 LoRA 是否能沿全秩的阶段差方向移动，所以方向检验放在输出空间而非权重空间；均值增益本身噪声大（8 种子），预测强度待预研。

## 方法设计的核心思想

输入：检查点 θ_ck、其上一阶段检查点 θ_prev（预先登记两种取法：主取法为所在阶段起点，P2 各检查点取 P1 末、P1 检查点取约 400B token 之前的检查点；次取法为固定 token 间隔的前一检查点）与下一检查点 θ_next；2610.01066 的训练提示、损失、LoRA 初始化；200 题保留集；三种评分（宽松＝论文主评分；严格＝独立 `#### <number>` 行；首段＝Table 22 规则）。

动作：(a) 免训练：评测 θ(α)=θ_ck+α(θ_prev−θ_ck)，α∈{0,0.1,…,0.6}，取最大分数减当前分数为插值余量，并记录逐题对错。(b) 方向检验：在训练提示上用 θ_ck 采 256 条回答，计算每个 token 上 log π_RL−log π_ck 与 log π_prev−log π_ck、log π_next−log π_ck、以及匹配 KL 扰动的对应差，比较相关；同时比较 `####` 用法、续写新题、长度等呈现特征的回退方向。(c) 逐题富集：RL 翻对/翻错的题与插值路径上对错的列联关系。

与最高近邻的差别：2610.01066 把增益读作学习者的“可达性”，没有把检查点的训练历史作为变量；Neural Thickets（2603.12228）与 PSV（2610.40649）研究随机扰动邻域或 logit 偏置，不涉及训练历史方向；2506.10947/2512.16912 的裁剪、熵、错配解释都只用当前策略与 rollout。本 Idea 的预测与检验对象是“当前→上一阶段”这条历史方向，并用“当前→下一检查点”作反向对照。

## 最小实验

模型与检查点：HF `allenai/OLMo-2-1124-7B`（965 个分支已用 HF refs API 核实，含 `stage1-step928646-tokens3896B` 与 `stage2-ingredient{1,2,3}-step*-tokens*B`；论文用的 revision 在 `mynotwo/rl-random-prob/configs/olmo2_checkpoints.json`）；OLMo-3-7B O1–O4 与 SmolLM2-1.7B S1–S4（revision 见 2610.01066 Table 4）。数据：仓库 `src/data/synthetic_gsm_rlvr_1000_seed13.jsonl`，800/200 划分（split seed 777），96 token 上限，贪心评测。

实验 A（免训练，均值级）：12 个 ingredient1 P2 检查点、末段 12 个 P1 检查点、O1–O4、S1–S4 共 32 点算插值余量（每点 7 个 α，两份权重在 CPU 上相加后载入），与仓库 `results/checkpoint_runs.csv` 中已发表的 8 种子随机奖励宽松终点做 Spearman 相关；竞争预测量：起点准确率与 32 次采样正确率代入 2512.16912 式(9)、首段分数与格式率（2610.01066 Table 16/22 规则）、随机奖励梯度方向邻域（按训练器损失求梯度、Adam 式逐坐标归一、匹配 KL 缩放）、各向同性邻域（移植已核验的 `sunrainyg/RandOpt/randopt.py` 高斯扰动到同一 LoRA 坐标、匹配 KL）。承认 8 种子均值目标信度约 0.6，这一级只作辅助。

实验 B（新 RL 运行，逐题与方向，主检验）：用已核验训练器 `src/trainer/rlvr_probe_v2_fixedsplit.py`（lr 3e-5、G=4、参考项 0.01、LoRA r8；评测逐题 `outcomes` 已保存，需加一行保存全部输出文本，并开 `--save_adapter`），在 8 个检查点上各跑 8 种子：P1 末、P1 3,272B、ingredient1 的 +5B/+13B/+42B/+50B、O3、O4（O4 作压力测试）；另用共享 rollout 训练器（`src/shared_rollout/`，AdamW wd=0、无参考项、无裁剪）在 P1 末/P2+5B 上复现 Table 1 的 4 个格子各 8 种子，检验离线时方向是否相同。预先登记：先写下 ingredient2/3 的 +5B、+21B、+42B 共 6 个检查点的插值余量预测，再各跑 8 种子。漂移对照：P1 末与 P2+5B 上零奖励（`--reward_mode zero`，此时只剩参考项与 AdamW 默认 0.01 衰减）各 4 种子，检验回退是否来自正则项而非随机更新。

推翻条件：(1) 中 RL 变化与上一阶段方向的相关不高于与下一检查点方向或匹配扰动的相关；(2) 中富集比不显著；(3) 中插值余量在预先登记检查点上不优于首段分数或起点准确率；O4 的插值路径最高分远低于其 RL 终点分布。

算力：在线运行约 40 分钟/80G 卡（仓库 README，H100 计），离线运行约 0.3 H200 小时（论文 §11.7：64 个运行 17 H200 小时）。实验 B 在线 64＋预登记 48＋零奖励 8 个运行约 90 A100 小时，离线 32 个运行约 15 A100 小时；实验 A 约 32×7 个插值模型的 200 题评测（每个含载入约 3 分钟）约 12 A100 小时，邻域对照与方向检验的前向计算约 15 A100 小时；合计约 130 A100 小时，8×A100 一天内完成；检查点逐个下载用完即删。无付费 API、无人工标注。预研（2×A100，约 4 小时）：先只评测 P1 末↔P2+5B 的插值曲线（11 个 α、三种评分）——若路径上没有任何 α 让前缀分接近 39%、宽松分接近 27%，即不能覆盖 Table 22/Table 1 的 P2 终点均值，直接 no-go；通过后再跑 P2+5B 的 4 个保存输出的随机奖励运行做方向检验。

Frozen Problem Anchor and user constraints:

- 起点问题：在随机奖励 RLVR 中，什么学习者一侧的属性决定同一随机奖励信号能否提高任务准确率；2610.01066 的 OLMo-2 P1/P2 对比显示同 rollout 同奖励下结果相差数倍。
- 对象：base 检查点（尤其 OLMo-2-1124-7B 预训练末 P1 与 mid-training P2 系列检查点），独立 Bernoulli(1/2) 随机奖励下的 GRPO 式更新。
- 条件：2610.01066 的协议（合成 GSM、96 token 上限、LoRA r8、每步 1 题×4 条、500 步、贪心评测、宽松抽取）；对照条件为 2506.10947 / Olmo 3 的大批量在线 GRPO（全参数、每批多次更新、长回答、MATH-500）。
- 初始评测：合成 GSM 200 题保留集的贪心准确率（宽松/严格/首段三种评分），可扩展到 MBPP、组合查找。
- 瓶颈：已有三类解释（rollout 质量/错配、裁剪与熵、污染与记忆）都不能解释同 rollout 同奖励下的学习者差异；2610.01066 的“可达性”只是命名；且其 Table 22 显示该差异对评分口径极敏感，2506.10947 与 Olmo 3 在大批量设定下得到相反结论。
- 证据边界：主要证据来自单一模型家族（OLMo-2）、合成算术、短回答上限；高分运行依赖宽松抽取；2610.01066 的 P1/P2 离线对比无裁剪、无参考项、无权重衰减，与其在线扫描并不完全一致。
- 用户约束：不做世界模型、视频生成、机器人；正式实验 8×A100 80G、≤5 天；预研 2×A100；token 资源紧张；付费 API 1000 元内可自主；目标半年内（自 2026-10 起）投主会。
- 进入实验规划的成功条件：候选有清楚的独立贡献；最小实验能在上述算力内区分主要竞争解释（学习者“可达性”、错配/rollout 质量、裁剪偏置、输出呈现漂移）；所需检查点、代码与数据可得并已核实。
