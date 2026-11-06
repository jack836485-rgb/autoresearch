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
files in this workspace and do not write files, except your raw review to /home/claude/jack836485-rgb/autoresearch/review-stage/random_reward_learner_q004_20261106/round-02-review.md (UTF-8).
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

**定位关键词：** spurious rewards；random rewards；RLVR；GRPO；solution density；antithetic variates

**一句话定位：** 在随机/虚假奖励 RLVR 中，同一随机奖励信号对同族不同检查点（学习者）给出相反结果，学习者一侧由什么决定。

**与起点问题的关系：** 原问题：保留 OLMo-2-1124-7B 预训练末（P1）与 mid-training（P2）检查点、合成 GSM 与 2610.01066 的训练协议，并扩展到 SmolLM2、OLMo-3、Qwen2.5-7B、Llama-3.1-8B 与代码/查找任务。不回答“mid-training 数据的哪部分造就了该学习者状态”，也不解释全参数、大批量的 2506.10947 / Olmo 3 设定，只在 LoRA 内检验“每批更新次数×裁剪”这一边界条件。

前提证据（均已读原文）：2610.01066 Table 1 中两个学习者收到同一缓存 rollout 与同一随机奖励，P2 宽松准确率 13.5→27.2、P1 2.5→5.4，该离线训练器无参考项、无权重衰减、无裁剪（§11.7）；Table 22 用训练前指定的前缀评分（截到第一个 `\nQuestion:`）重算同一批运行，P1 41.5→21–29%（10/16、11/16 个运行降超 10 点），P2 14.5→约 39%；Table 17 中同一检查点、LoRA 终点范数相近（2.10 vs 2.30）的两种随机输入，一种 16/32 个运行变化超 10 点、另一种 0/32；其公开的逐种子结果中 12 个 P2 检查点均值增益在 −11.8 到 +26.8 间跳动，起点准确率与增益的 Spearman 相关约 −0.06。其在线扫描每步 1 题×4 条、一次更新，裁剪越界只占 0.24% 步（Table 6）；用户关注的“离线 vs 在线”差别因此主要不在采样方式本身。

## 核心 Claim

若成立，新增的认识是：随机奖励训练的**平均**效果——也就是“学习者效应”——是学习者局部分数地形在随机奖励更新方向上的二阶（偶数）部分，而不是学习者的潜在能力或“可达性”；单次运行的大幅涨跌主要是一阶（奇数）部分，即这次硬币恰好推向哪个方向。可用的东西有两个：一个把任何一次随机奖励实验拆成奇/偶两部分的配对设计；一个免训练、每个检查点几十次前向评测即可得到的偶数部分预测量，用来判断随机奖励结果作为能力探针（2610.01066）或去污染检验（Olmo 3、2507.10532）何时有信息量。

依据（不依赖实验结果）：组内标准化下把一组奖励整体翻转（r→1−r），每条回答的优势严格反号；离线缓存 rollout 时 token 与掩码不变，token 均值损失的梯度严格反号，梯度范数裁剪与 Adam 的 m/√v 都是梯度历史的奇函数，所以第一步更新严格反号，后续偏差为二阶。于是一对“同 rollout、奖励整体翻转”的运行终点约为 θ0±Δ：配对均值−当前分数＝偶数部分，配对差＝奇数部分。2610.01066 Thm 9.7 给出随机奖励梯度零均值、协方差为 c_G·Fisher，§9.4 给出期望行为变化来自协方差×曲率的二阶项；Table 1 在无参考项/无衰减/无裁剪时仍有学习者差异，说明这些漂移项不是必要条件；Table 22 的“高于中间者降、低于中间者升”与 Table 17 的同范数异效，与“偶数部分＋方向由任务输入决定”一致。尚未知：在线采样使两条运行的 rollout 在第一步后分叉，长度相关的 token 均值与参考项会引入不随翻转改变的偶数漂移，其大小需测；500 步后高阶项的大小。

可推翻的判断：(1) 在共享 rollout 协议下，P1/P2 的学习者差异主要出现在配对均值（偶数部分），而非配对差；(2) 免训练的反符号扰动在同一参数化、同一输出位移下预测的逐题偶数部分，与 RL 配对测得的逐题偶数部分一致，且明显好于各向同性扰动、无模板随机 token 方向扰动、随机 logit 偏置扰动，以及起点准确率/错配模型、正确答案对数概率间距、首段分数；(3) 同一预测量给出宽松评分下 P2>P1、前缀评分下 P1 降 P2 升；(4) 零奖励“只有漂移”的臂（参考项＋权重衰减）不复现学习者差异，去掉参考项和衰减的在线臂保留它；(5) 每批多次 mini-batch 更新且开裁剪的臂出现预测之外的偶数漂移，关裁剪后消失。

## 方法设计的核心思想

输入：检查点 θ0；2610.01066 的训练提示、LoRA 初始化（r8、同种子）与损失；200 题保留集；三种评分（宽松＝论文主评分；严格＝独立 `#### <number>` 行；首段＝Table 22 规则）。

RL 侧（测量）：每对运行共享 rollout 序列（离线协议）或共享采样随机数（在线协议），一条用奖励表 R、另一条用 1−R；逐题记录终点正确与否，得到每题的偶数部分（两条平均−起点）和奇数部分（两条之差）。

预测侧（免训练）：用 θ0 在 64 个训练提示上各采 4 条，抽随机奖励并组内标准化，按同一损失求 LoRA 梯度；重复 K 次，用这些梯度的逐坐标均方根归一（对应 Adam），得到方向 u_k；把 ±u_k 缩放到预先登记的统一输出位移 ρ*（训练提示上相对 θ0 的平均逐 token KL，由 P1 末与 P2+5B 两个检查点的 4 对校准运行在 step 500 的均值一次定下，之后对所有检查点固定，另报 0.5ρ*、2ρ* 两档），评测 θ0±δ_k，得到每题偶数部分的预测。对照扰动用同一参数化与同一 ρ*：各向同性高斯；用无模板随机 token 提示算出的梯度方向；随机 logit 偏置。

与最高近邻的差别：2610.01066 有零均值/协方差定理但把结果读作“可达性”，没有配对分解、免训练预测，也没把评分口径与位移当变量；Neural Thickets（2603.12228）测各向同性全权重邻域的密度，只在一句话里猜测与虚假奖励有关；PSV（2610.40649）说明 logit 偏移可替代权重扰动，在此作为“只是输出 token 偏好”的竞争解释直接比较。朴素迁移各向同性邻域在这里会失败（Table 17 同范数异效），所以方向取自随机奖励梯度本身、位移按输出空间匹配。

## 最小实验

模型与数据：HF `allenai/OLMo-2-1124-7B`（965 个分支已经 HF refs API 核实；论文用的 revision 在 `mynotwo/rl-random-prob/configs/olmo2_checkpoints.json`；另有 ingredient2/3 两条独立 mid-training 轨迹）；仓库自带 `data/synthetic_gsm_rlvr_1000_seed13.jsonl`，800/200 划分（split seed 777），96 token 上限，贪心评测。

主实验（逐题）：8 个检查点＝P1 末、P1 3,272B，及 ingredient1/2/3 各两个 P2 检查点（+5B 与 +42B；ingredient2/3 未被 2610.01066 跑过，预测在运行前登记）。每点 8 对离线反符号运行（`src/shared_rollout/prepare_shared_rollouts.py`、`train_shared_rollouts.py`，已核实其优化器为 AdamW、weight_decay=0、无参考项、无裁剪；加一个奖励翻转开关）与 8 对在线反符号运行（`src/trainer/rlvr_probe_v2_fixedsplit.py`；评测的逐题 `outcomes` 已保存，需加一行保存全部输出文本以做首段评分）。判别统计：每个检查点 200 题上“预测偶数部分 vs RL 偶数部分”的相关，按题与按配对做 bootstrap，比较各预测量；检验 (1) 用配对均值与配对差的方差分解。漂移臂：P1 末与 P2+5B 上零奖励（训练器 `--reward_mode zero`，已核实此时只剩参考项与 AdamW 默认 0.01 衰减）各 4 种子，去参考项去衰减（`--kl_coeff 0`，衰减置零需改一行）各 8 对；边界臂：同两点、每批 16 题×4 条、8 次 mini-batch 更新（`--accum_steps`/`--ppo_epochs`），开/关裁剪各 4 对。

次要实验（均值级，不需重跑）：仓库 `results/checkpoint_runs.csv` 的 37 个 OLMo-2 检查点×8 种子宽松结果、SmolLM2 S1–S4 与 OLMo-3 O1–O4 各 8 种子、MBPP/查找任务结果、`input_controls.csv` 的 D/E 与 Qwen2.5/Llama 结果（已本地读取，如 P2+5B 均值增益 +26.8、P2+13B −11.8）；只作“偶数部分预测量 vs 均值增益”的辅助检验，承认 8 种子目标信度约 0.6。新跑 Qwen2.5-7B、Llama-3.1-8B base 各 8 对在线反符号运行。

竞争预测量与路线：起点准确率与 32 次采样正确率代入 2512.16912 式(9)（标准公式）；教师强制正确答案行对数概率间距（标准量）；首段分数与格式率（2610.01066 Table 16/22 规则）；各向同性扰动（已核验 `sunrainyg/RandOpt/randopt.py` 的按 σ 高斯扰动，移植到同一 LoRA 坐标并按 ρ* 缩放）；随机 logit 偏置（2610.40649 §2–3 规则，独立实现：每成员一个固定高斯偏置向量加到 logits 后贪心解码，按 ρ* 缩放）。

推翻条件：配对差的方差远大于配对均值且学习者差异不在配对均值中；零奖励臂复现差异；任一对照扰动的逐题预测不比反符号梯度扰动差；ingredient2/3 预先登记预测失败。

算力：单个在线运行约 40 分钟/80G 卡（仓库 README，H100 计），离线运行约 0.3 H200 小时（论文 §11.7：64 个运行 17 H200 小时）。离线 128 运行约 65、在线 128 运行约 90、漂移臂 40 运行约 30、边界臂 16 运行（16 倍采样）约 60、Qwen/Llama 32 运行约 25 A100 小时；免训练扰动约 53 个检查点×4 类×48 对×2 方向的 200 题评测加梯度，约 45 A100 小时；合计约 315 A100 小时，8×A100 约 1.7 天；检查点逐个下载用完即删。无付费 API、无人工标注。预研（2×A100，约 10 小时）：只在 P1 末与 P2+5B 上各跑 4 对离线反符号运行和 K=32 的反符号梯度/各向同性扰动，检查学习者差异是否主要在配对均值中、预测是否给出 Table 22 的方向；否则停。

Frozen Problem Anchor and user constraints:

- 起点问题：在随机奖励 RLVR 中，什么学习者一侧的属性决定同一随机奖励信号能否提高任务准确率；2610.01066 的 OLMo-2 P1/P2 对比显示同 rollout 同奖励下结果相差数倍。
- 对象：base 检查点（尤其 OLMo-2-1124-7B 预训练末 P1 与 mid-training P2 系列检查点），独立 Bernoulli(1/2) 随机奖励下的 GRPO 式更新。
- 条件：2610.01066 的协议（合成 GSM、96 token 上限、LoRA r8、每步 1 题×4 条、500 步、贪心评测、宽松抽取）；对照条件为 2506.10947 / Olmo 3 的大批量在线 GRPO（全参数、每批多次更新、长回答、MATH-500）。
- 初始评测：合成 GSM 200 题保留集的贪心准确率（宽松/严格/首段三种评分），可扩展到 MBPP、组合查找。
- 瓶颈：已有三类解释（rollout 质量/错配、裁剪与熵、污染与记忆）都不能解释同 rollout 同奖励下的学习者差异；2610.01066 的“可达性”只是命名；且其 Table 22 显示该差异对评分口径极敏感，2506.10947 与 Olmo 3 在大批量设定下得到相反结论。
- 证据边界：主要证据来自单一模型家族（OLMo-2）、合成算术、短回答上限；高分运行依赖宽松抽取；2610.01066 的 P1/P2 离线对比无裁剪、无参考项、无权重衰减，与其在线扫描并不完全一致。
- 用户约束：不做世界模型、视频生成、机器人；正式实验 8×A100 80G、≤5 天；预研 2×A100；token 资源紧张；付费 API 1000 元内可自主；目标半年内（自 2026-10 起）投主会。
- 进入实验规划的成功条件：候选有清楚的独立贡献；最小实验能在上述算力内区分主要竞争解释（学习者“可达性”、错配/rollout 质量、裁剪偏置、输出呈现漂移）；所需检查点、代码与数据可得并已核实。
