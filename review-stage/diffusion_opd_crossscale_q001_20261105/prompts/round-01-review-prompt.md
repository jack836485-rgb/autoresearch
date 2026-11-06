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
Today's date: 2026-11-05. Known tool workarounds: arXiv API 和 Semantic Scholar 前一天出现过 429，可用 WebSearch 或直接打开 arxiv.org/abs 页面
Finish all searches before answering and leave no background tasks running. Do not read other
files in this workspace and do not write files, except your raw review to C:\Users\30473\Desktop\研一\autoresearch\review-stage\diffusion_opd_crossscale_q001_20261105\round-01-review.md (UTF-8).
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

**定位关键词：** on-policy distillation、classifier-free guidance、diffusion distillation、teacher-student gap、flow matching

**一句话定位：** 这是文生图扩散/流匹配模型后训练里的具体问题：在策略蒸馏（OPD，学生在自己生成的去噪轨迹状态上接受教师预测的监督）从大教师蒸到同族小学生时（如 SD3.5-Large 到 SD3.5-Medium），标准配方产生纹理损坏、整体偏暗等伪影；现有修法把 CFG 折叠进学生的单分支，学生因此失去可调的引导尺度和负提示。

**与起点问题的关系：** 原问题。保留对象（同族大到小扩散 OPD）和评价目标，补上起点问题中"学生状态偏离教师可靠区"这一从未被检验的原因；"容量本身贡献多少"只在对照中部分回答。

## 核心 Claim

**成功后新增的认识与工具：**
- 认识：跨尺度扩散 OPD 的失败，有一个必要的组成部分来自监督状态，即教师在学生访问的状态上外推不可靠，而不只是学生容量加 CFG 组合放大。
- 工具：把学生状态按教师可靠性重新加噪到更高噪声级后再监督，可以让保留双分支 CFG 的标准 OPD 在大到小设置下不出伪影。这样不用折叠引导，学生仍能调引导尺度、用负提示。

**可推翻的判断：** 在 SD3.5-L 到 M 上，配方保持双分支 CFG 不变，只把监督状态从学生 rollout 换成教师可靠的状态，伪影指标和任务分数应接近 GFD-OPD。可靠状态有两种：教师轨迹上的状态，或经可靠性自适应重加噪的学生状态。如果换了状态后伪影依旧，就支持纯容量加放大的解释，否定本题。

**目前支持预期的依据：**
1. GFD-OPD（2609.39692）发现，在学生 rollout 上计算的 KL 与在教师轨迹和真实加噪轨迹上计算的 KL 趋势明显不同，不能反映真实差距。这说明在学生状态上，教师和学生的关系与在可靠状态上不同；但该文没有改变监督状态。
2. LLM OPD 中，多项工作证实教师在学生生成的前缀上指导不可靠：Speculative KD 2410.11325、ReOPD 2607.04763、AC-OPD 2609.22254；SPTA 2611.03133 指出教师单独表现强不代表其在学生前缀上可靠。
3. 扩散有 LLM 没有的杠杆：对两个分布同时加噪，KL 随噪声单调不增（数据处理不等式），重加噪会把学生状态推向教师训练时见过的边缘分布。Any-OPD（2608.03316）已在异构模型间用固定强度的"加噪再去噪"投影学生样本。

**反向证据与未知：**
- GFD 的分支级实验表明，分开监督两分支后各分支 KL 都下降，组合 KL 却不降；作者用 δ_g=δ_u+w·d 的抵消与放大解释这一现象，这是支持容量解释的直接证据。
- 状态可靠性在扩散中的作用目前没有直接测量。
- 重加噪会让监督目标变粗，可能牺牲细节。

## 方法设计的核心思想

- **输入：** 学生 rollout 状态 x_t，以及冻结的大教师。
- **可靠性信号：** 比较教师在 x_t 上的干净图预测，与在 x_t 小幅重加噪到 t+δ 后的干净图预测。两者差异大，说明 x_t 偏离教师可靠区；差异小，说明教师在此可靠。
- **动作：** 为每个状态选择使信号低于阈值的最低噪声级 t′，在 x_{t′} 上以双分支目标监督学生，分别匹配教师的条件与无条件预测。
- **输出：** 保留双分支 CFG 的小学生。
- **与最高近邻的差别：**
  - GFD-OPD 不改监督状态，靠折叠 CFG 消除放大，代价是失去可调引导；
  - Any-OPD 对异构模型做固定强度的投影，不按状态自适应，也不处理同族跨尺度和 CFG 分支问题；
  - LLM 侧的修法是替换 token 或微调教师，没有加噪这一手段。

## 最小实验

- **设置：** SD3.5-Large 作教师，SD3.5-Medium 作学生，沿用 GFD-OPD 的训练和评测。
  - 指标：GenEval、OCR、PickScore、HPSv3，伪影指标（潜变量频谱能量、解码图高通纹理），固定状态 KL。
  - 可控性：引导尺度扫描（w∈{1,3,5,7}），以及负提示测试。
- **2×2 判别：** 监督状态（学生 rollout / 教师轨迹状态）× 目标（组合速度匹配，即 DiffusionOPD / 双分支匹配，即 PDM 式）。再加两臂：固定强度重加噪（Any-OPD 式）和自适应重加噪（本方法）。强对照为 GFD-OPD。
- **判别结果：**
  - 支持：教师轨迹状态或自适应重加噪下，双分支配方的伪影指标接近 GFD-OPD；学生 rollout 下仍有伪影；引导尺度扫描和负提示在本方法下保留，在 GFD 下失效或退化。
  - 推翻：换状态后伪影不变。
  - 自适应优于固定强度时，说明可靠性信号有用；否则贡献只剩"重加噪"。
- **复现路线：**
  - GFD-OPD 用已核验的官方仓库 github.com/CriliasMiller/GFD-OPD（VeOmni 分支，含 SD3.5-L 到 M 的训练配置）。
  - DiffusionOPD、PDM 只改损失：GFD 文中式 (3)(4) 给出了 PDM 和双分支损失的规范；DiffusionOPD 是组合速度的 L2 匹配。在同一代码里切换。DiffusionOPD 没有官方代码。
  - 教师轨迹状态是标准离策略规则：用教师采样轨迹替换学生 rollout。
  - Any-OPD 固定投影按原文独立实现（计划；未定的选择是投影强度）。
- **关键数据与教师：**
  - SD3.5-L/M 权重公开。GFD 用的是经 RL 训练的分任务大教师，是否公开未核实。
  - 预研先用 SD3.5-L 基座当单一教师做纯压缩，第一关是复现 DiffusionOPD 的伪影；不复现时，改用 Flow-OPD 仓库（github.com/CostaliyA/Flow-OPD，已核验存在）训练一个 GenEval 专项教师，成本未核实。
- **算力：**
  - GFD 报告其方法 10 GPU 小时内超过所有基线（图 1），按每臂约 20–40 A100 小时估计。
  - 预研：学生 rollout 对教师轨迹状态，双分支目标，单种子，约 80 A100 小时，2×A100 约 1.7 天。
  - 正式：6 臂加 GFD，约 280 A100 小时，8×A100 约 1.5 天。
  - 显存：8B 教师 bf16 推理加 2.5B 学生全参训练，单张 80G 卡需要开优化器分片（未实测）。

Frozen Problem Anchor and user constraints:

- 起点问题：文生图扩散/流匹配模型的在策略蒸馏，从大教师到小学生（同族不同规模，如 SD3.5-L 到 M、FLUX.2 大到小）时的失败机制与修法。
- 初始评测：GenEval、OCR、PickScore 等任务奖励，以及图像质量指标（如 HPSv3）；伪影指标（频谱能量、高通纹理）；固定状态 KL。
- 瓶颈：三种原因没有被分离；现有修法（引导折叠）把 CFG 折进单分支。
- 用户约束：预研 2×A100 80G，单模型单种子，只回答 go/no-go；正式实验 8×A100 不超过 5 天；token 稀缺；目标是半年内投主会。不做世界模型、视频、机器人。
- 进入实验规划的成功条件：候选两次通过独立审查门槛（三项都 ≥6、至少两项 ≥8、可行性通过）。
