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
Today's date: 2026-11-05. Known tool workarounds: arXiv API 和 Semantic Scholar 偶尔返回 429，可用 WebSearch 或直接打开 arxiv.org/abs 页面
Finish all searches before answering and leave no background tasks running. Do not read other
files in this workspace and do not write files, except your raw review to C:\Users\30473\Desktop\研一\autoresearch\review-stage\fewstep_coverage_rl_q002_20261105\round-04-review.md (UTF-8).
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

**定位关键词：** few-step diffusion、diffusion distillation、GenEval、pass@k、reinforcement learning

**一句话定位：** 这是少步文生图模型后训练里的具体问题。蒸馏得到的少步学生按 pass@k 看覆盖收缩，已有修法（第一步偏置、早期步用基座等）都用 CLIP/DINO/LPIPS 这类样本间多样性指标来验证；这些学生正被当作组归一化在线 RL 的起点。哪一种覆盖与后续 RL 有关、常规多样性指标能否测到它，扩散领域没有受控研究。

**与起点问题的关系：** 子问题。保留对象（少步学生的覆盖收缩）和 pass@k 评价，直接回答起点问题中"现有多样性修法是否只在多样性指标上有效"；把覆盖收缩分解为布局与外观，并检验它对后续 RL 的按子任务后果。"单样本增益与覆盖损失是否同源"只在布局维度部分回答。

## 核心 Claim

**成功后新增的认识与工具：**
- 认识一：少步学生与 RL 相关的覆盖收缩主要在布局上（第一步承诺的结构），而 CLIP/DINO 等常规多样性指标主要反映外观，所以"多样性提高"不等于"与 RL 相关的覆盖恢复"。
- 认识二：在平均成功率相同的起点之间，组归一化 RL 在依赖布局的可验证子任务（GenEval 的计数、位置、双物体）上的收益，取决于各提示成功率分布的两极化程度，即成功率处于 0 和 1 之间的提示占比；外观子任务基本不受此限制。
- 工具：RL 前按子任务统计的"中间成功率提示占比"，以及"外观多样性提高、布局不变"这一反例对照，用来判断一个多样性修法是否值得在 RL 前使用。

**可推翻的判断：**
- 设计：在同一学生上构造三个起点，平均 k=1 相差不超过 1 个百分点，并且在每个子任务上，k=1 都按协变量记录和匹配；
  - (A) 原学生；
  - (L) 第一步偏置，主要提高布局多样性；
  - (P) 最后一步偏置，主要提高外观多样性，CLIP/DINO 多样性升幅不低于 L。
- 预测：用相同的组归一化 RL 训练后，L 在布局子任务上的收益高于 A 和 P；P 在布局子任务上与 A 无差别，尽管 P 的 CLIP/DINO 多样性更高。
- 推翻：P 和 L 收益相同；或 L 不优于 A；或布局与外观子任务没有差别。
- 补充对照：A 起点把组大小加倍（G=48）。它预期也会提高"中间成功率占比"，并落在同一条"占比对收益"的曲线上，这支持机制；L 用一半的采样成本达到同等收益，这是 L 的实用价值。两个子主张分开判断。

**目前支持预期的依据（先验合理性）：**
1. 蒸馏学生在第一步确定结构、多样性损失集中在第一个高噪声步，有三方独立证据：2503.10637、ReSeed 2610.37110、DP-DMD 2602.03139。布局正是这一步决定的。
2. 组归一化 RL 在退化组上没有方向信号。DiffusionNFT（2509.16117，算法 1）把组内奖励减去组均值，再映射成最优概率 r=0.5+0.5·clip(r_norm/Z)；组内二值奖励全同时，所有样本的 r=0.5，正负两支损失对称，没有改进方向。这是该配方中的机制性事实。
3. 在平均成功率相同时，各提示成功率越两极化（p 接近 0 或 1），退化组越多，这是 1−p^G−(1−p)^G 对每个提示的直接推论。所以预测量看的是"成功率分布形状"，不是平均 p。
4. 布局子任务是基座最弱的部分：SD3.5-M 在 GenEval 上计数 0.50、位置 0.24（rCM 2510.08431 的分项）。
5. Apple（2609.38853）：少步学生在 k=1 领先、N=256 内多数被教师反超，且轨迹类目标（MeanFlow、LCM）比分布匹配类（DMD2）更能保住覆盖。所以第 0 关在 TDM（轨迹类）与 SD3.5-L-Turbo（对抗蒸馏）之间按布局缺口选学生。
6. 扩散领域内，SiD few-step（2505.12674）只断言多样性对蒸馏后 RL 重要；LLM 中起点多样性预测 RL 收益已有同构结论（2609.33780 等），但文本没有布局承诺结构，也没有"外观多样性提高却无益"这样的反例结构。

**已知反向因素：** DiffusionNFT 在前向过程上训练，用于少步学生可能损害少步能力（D-OPSD 2605.05204 报告过类似的训练与推理状态不匹配），设为关卡。在第二配方 TDM-R1 中，替代奖励可能跨提示泛化，预测其效应更弱，作为配方依赖性的检验。

**待预研：**
- 各学生的布局覆盖缺口大小；
- P 干预能否在不改布局的情况下把外观多样性提到与 L 相当；
- DiffusionNFT 下少步质量能否保持；
- 效应幅度相对 RL 种子方差的大小。

## 方法设计的核心思想

- **输入：** 第 0 关选出的少步学生，以及两种轻量偏置适配器：第一步（L），按 ReSeed 官方实现；最后一步（P），用同一参数化，作用在最后一步。两者的效果都蒸馏进学生 LoRA 后移除适配器，所以三个起点只在初始化上不同。
- **RL 前测量：** 每个起点、每个子任务的 pass@k（N=32）、各提示成功率分布、"中间成功率提示占比"，以及布局多样性（检测框数量与位置的方差）和外观多样性（CLIP/DINO/颜色直方图）。
- **RL：** 主配方 DiffusionNFT，用 4 步学生采样；第二配方 TDM-R1。奖励为 GenEval 二值奖励，组大小 G=24，等预算。
- **输出：**
  - 多样性指标与 RL 收益的关系：外观多样性不预测收益，布局多样性预测收益；
  - 各（起点、子任务）点上"中间成功率占比对子任务收益"的关系，以每个子任务的 k=1 为协变量；
  - 两种配方之间的差异。
- **与最高近邻的差别：**
  - Apple 只测覆盖，不分解布局与外观，也不研究后续 RL；
  - ReSeed、DP-DMD 只用多样性指标验证修法；
  - TDM-R1、DiffusionNFT 改进的是配方；
  - LLM 侧研究没有"外观多样性提高却无益"的结构性反例。

## 最小实验

- **代码与资源（已核验）：**
  - DiffusionNFT 官方仓库 github.com/NVlabs/DiffusionNFT（ICLR 2026 Oral；scripts/train_nft_sd3.py，config/nft.py:sd3_geneval，8 卡、G=24、LoRA r=32；支持 GenEval、OCR、PickScore 等奖励）；
  - TDM-R1 官方仓库 github.com/Luo-Yihong/TDM-R1（geneval_sd3_8gpu_G24_24_4step，起点 Luo-Yihong/TDM_sd3-5_lora）；
  - ReSeed 官方仓库 github.com/TWWinde/ReSeed（2026-10-28 推送）。
  - P 适配器复用 ReSeed 的参数化，只改作用步；"蒸馏进 LoRA"是标准回归，未定的选择是步数。
- **第 0 关（纯推理，2×A100）：**
  - 在 TDM-SD3.5-M 与 SD3.5-L-Turbo 两个学生及教师上，按 GenEval 子任务测 pass@k（N=32）、成功率分布，以及布局方差和外观方差；
  - 选出布局缺口更大的学生，并检验 P 干预能否在布局方差不变的情况下提高外观多样性。
  - 两条都不满足则停止。
  - 教师采样成本：SD3.5-L 28 步加 CFG，553×32 张，约数十 A100 小时。
- **第 1 关（2×A100，单种子）：** 在 DiffusionNFT 下短训，检查少步质量（4 步 GenEval k=1 和 HPS 不下降超过 1 个百分点）；再比较 A 与 L 在布局子任务上的中途收益。质量不保持则换成 TDM-R1 作为主配方。
- **正式（8×A100，不超过 5 天）：**
  - DiffusionNFT 下 A、L、P 三个起点各 2 个种子，加 A 起点 G=48 一条，共 7 条；
  - TDM-R1 下 A、L 两条；
  - 全部等预算截断；
  - 评测用 GenEval 分项，以及留出的 GenEval2 或 T2I-CompBench 空间与计数子集。
- **判别结果：**
  - 支持：L 在布局子任务上的收益高于 A 和 P，差异大于种子间离散；P 尽管 CLIP/DINO 多样性更高，布局收益与 A 无差别；G=48 与 L 落在同一条"中间成功率占比对收益"曲线上；TDM-R1 下效应更弱。
  - 推翻：P 与 L 收益相同，或 L 不优于 A。
- **算力（未实测）：** 每条 RL 等预算截断，按 8×A100 约 0.4–0.5 天估计，9 条约 4–4.5 天；第 0 关和第 1 关在 2×A100 上合计约 3–4 天。单条 RL 的耗时没有实测。

Frozen Problem Anchor and user constraints:

- 起点问题：部署中的少步文生图模型（蒸馏学生加 CFG），单样本分数与多样本覆盖之间的落差，以及现有修法与下游后果。
- 初始评测：GenEval/GenEval2/DPG 等验证器上的 pass@k 与 best-of-k，以及样本间 CLIP 多样性。
- 瓶颈：修法只用多样性指标验证；覆盖收缩的后果未知。
- 用户约束：预研 2×A100 80G，单模型单种子，只回答 go/no-go；正式实验 8×A100 不超过 5 天；token 稀缺；半年内投主会；不做世界模型、视频、机器人。
- 进入实验规划的成功条件：两次通过独立审查门槛。
