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
Today's date: 2026-11-05. Known tool workarounds: arXiv 摘要与 HTML 正文可用 WebFetch 或 WebSearch 获取；CAVEAT 代码可 git clone https://github.com/microsoft/CAVEAT；Hugging Face 模型卡可用 curl https://huggingface.co/<repo>/raw/main/README.md；GitHub API 经代理可能 403
Finish all searches before answering and leave no background tasks running. Do not read other
files in this workspace and do not write files, except your raw review to /home/claude/autoresearch/review-stage/incentive_search_q007_20261105/round-04-review.md (UTF-8).
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

**定位关键词：** computer-use agent；web shopping agent；dark patterns；on-policy distillation；privileged information

**一句话定位：** 代用户购物的网页智能体在市场有激励时（赞助位、偏好排序、滴漏定价、预勾选附加项等界面引导）放弃用户最优商品。推理强度和 harness 能缓解前沿模型，但要多花约 2.6 倍运行时间。小模型即使配 harness 也几乎无效。

**与起点问题的关系：** 原问题；保留对象（购物 agent）、官方 CAVEAT 环境与匹配对照评测（clean 条件与引导条件）、全部 8 类机制及 combined 条件，回答"能否不靠更多推理时调用修复"，主要针对开源中小模型；不回答"哪种机制主导失败"的诊断问题。

## 核心 Claim

成功后新增一种训练方法：用同一个模型看到的"去引导页面"当教师，做在线自蒸馏，让中小模型在测试时不加任何额外调用，就能在引导条件下保持接近自己在 clean 条件下的选择质量。

这利用了 CAVEAT 特有的匹配对照结构：clean 与引导条件的用户请求、商品集和最优解完全相同，只改界面呈现。因此训练时，任一状态都能拿到同一状态的"无引导渲染"。这是一种只在训练时可得、测试时不可得的特权信息。

可推翻的判断：同一个 7–8B 起点模型在官方 CAVEAT 上比较：
1. 经过干净视角自蒸馏后，在留出环境的引导条件下，最优购买率显著高于起点模型配 BrowserUse，也高于起点模型配官方 CAVEAT-Harness，而平均步数与调用数不超过 BrowserUse 的 1.2 倍；
2. 它在引导条件下的最优购买率，与起点模型自己在 clean 条件下的差距缩小一半以上；
3. 用相同数据做离线行为克隆，即在 clean 条件下的成功轨迹上做 SFT，再在引导页面上执行，提升明显更小。这说明收益来自在线、按状态对齐的教师信号，而不是多看了好轨迹。

若起点模型在 clean 条件下本身就很差，教师信号太弱，方法不适用于该模型，结论需限定到 clean 条件下表现够好的模型。

当前依据：
- **CAVEAT 的条件对比**（arXiv:2609.27273，CMU、Microsoft Research；代码与 9 个环境已开源于 github.com/microsoft/CAVEAT，含 clean、8 类机制与 combined 条件、BrowserUse 基线与 CAVEAT-Harness）：
  - 匹配对照 78.6%，开启引导后 17.3%；
  - 单机制隔离下，GPT-5.6-Sol-low 全关时 100%，只开赞助位 63.3%、只开偏好排序 75%、只开滴漏定价 83.3%；
  - 同一模型在 clean 与引导条件下的巨大差距说明，失败主要来自呈现方式，而不是能力不足。看 clean 页面的同一模型，正是一个"知道该怎么选"的教师。
- **CAVEAT 的小模型路线依赖外部教师**：Qwen3.5-27B 配 harness 在迁移评测上只有 4.2%。CAVEAT-27B 用 GPT-5.6-Sol-low 加 harness 作外部教师，经 SFT 与 DAgger 式在线纠正后到 22.9%；仓库 README 写其后训练为"通用 SFT、迭代 SFT 与 on-policy 蒸馏"，权重尚未发布。它依赖更强的外部教师和 harness，不使用匹配对照。
- **GUI 上的特权信息自蒸馏已证明有效**：
  - Gated Hindsight Distillation（arXiv:2608.06065）在移动 GUI 上，以下一张截图作为特权信息，让同参数教师给学生的在策略回答重新打分，只在学生失败而教师能恢复示范动作时蒸馏，在 AndroidWorld 与 AndroidLab 上优于 GRPO；
  - 同类的在策略自蒸馏（以特权上下文为教师的同一模型）在推理任务上已有大量工作。

仍未知：
- 7–8B 模型在 CAVEAT clean 条件下的最优购买率（决定教师强度）；
- 状态对齐：引导改变了列表顺序，按 URL 与商品 ID 对齐是否足以让教师在"同一状态"上给出有意义的动作分布；
- 蒸馏后能否泛化到训练中没见过的环境和机制组合。

## 方法设计的核心思想

**输入**：官方 CAVEAT 环境的两个并行实例，用同一商品集和任务，一个开引导条件，一个开 clean 条件。

**动作**：
1. **学生在线采样**：学生 π_θ 在引导实例中按 BrowserUse 方式采样轨迹。
2. **教师对齐评分**：对学生每一步，把当前页面的 URL（搜索查询、商品页、购物车或结账页）在 clean 实例中打开，得到同一状态的无引导渲染。教师是同一组参数 π_θ（训练前冻结一份），输入相同的历史与任务、但换成 clean 渲染，对学生已采样的动作给出对数概率。
   - 涉及位置的动作（点击第 k 个结果）按商品 ID 映射到 clean 页面上的对应元素；
   - 滴漏定价下，clean 页面直接显示含费总价。
3. **门控蒸馏**：只在教师与学生的动作分布差异大的步骤上，以教师分布为目标最小化反向 KL。差异用两者在该步对学生动作的对数概率差来度量。其余步骤只加小权重的 KL 正则。
4. **推理**：测试时只运行学生，看引导页面，没有 clean 实例，也没有额外调用。

**输出**：一个在引导页面上行为接近"自己看到 clean 页面时"的策略。

**与最高近邻的关键差别**：
- CAVEAT-27B：教师是更强的外部模型加 harness，学生学的是 harness 的决策流程，测试时仍依赖 harness；
- 本方法：教师是同一模型看 clean 页面，学的是"忽略呈现引导"，测试时不需要 harness。
- GHD：特权信息是下一张截图，用于解决证据不可见。本方法的特权信息是同一状态的反事实无引导渲染，用于解决呈现被操纵。

## 最小实验

**起点模型**：Qwen3-VL-8B-Instruct，主模型；另选一个 7–8B 开源 GUI 模型（如 UI-TARS-1.5-7B），作为第二个起点。CAVEAT 接受任意 OpenAI 兼容接口，本地 vLLM 部署即可。

**预检（no-go 检查）**：先只评测起点模型在 clean 与 combined 条件下的最优购买率，每任务 3 次。
- 若 clean 下低于 30%，或 clean 与 combined 的差距小于 15 个百分点，则教师信号不足或问题不存在，停止训练部分。

**划分**：按环境划分，如在 caveat_shop 以外的 8 个 storefront 环境上训练，在 caveat_shop（Standard 与 Hard）上测试；再做一次反向划分。

**对照（同起点、同训练环境与任务、同测试设置）**：
- 起点模型配 BrowserUse；
- 起点模型配官方 CAVEAT-Harness；
- 离线行为克隆：用起点模型自己在 clean 条件下的成功轨迹，按 URL 映射到引导页面后做 SFT；
- 去掉门控的全步蒸馏；
- 外部教师 DAgger：用更大的开源模型（如 Qwen3.5-27B 或 32B 级）看引导页面配 harness 作教师，复现 CAVEAT-27B 的第二阶段思路。原配方的提示与步数未公开，标明为独立复现。

**指标**：
- 留出环境中 clean、8 类单机制、combined 条件下的最优购买率（Wilson 区间）；
- 平均步数、调用数与 token 数；
- clean 条件下的最优购买率不下降（检查是否损伤正常能力）。

**支持 / 推翻的结果**：
- 支持：
  - 留出 combined 条件下，本方法比 BrowserUse 与 CAVEAT-Harness 都高，且差值置信区间不含零；
  - 与自身 clean 差距缩小一半以上，调用数 ≤1.2 倍 BrowserUse；
  - 离线行为克隆明显更弱。
- 推翻：
  - 本方法不优于离线行为克隆或 CAVEAT-Harness；
  - 或在留出环境上无提升（只在训练环境上过拟合）。

**成本**：
- 预检：2 个模型 × 约 20 个任务 × 2 个条件 × 3 次，单张 A100 约半天；
- 训练：8B 模型在策略蒸馏，每轮采样数百条轨迹，加教师评分（clean 实例并行），8×A100 约 2–3 天；
- 评测：每个模型约 1 天；
- 不需要 KVM 或付费 API。外部教师 DAgger 用本地开源大模型。

Frozen Problem Anchor and user constraints:

- **起点问题**：代用户购物/预订的计算机使用智能体，在环境自身有激励（赞助位、偏好排序、滴漏定价等）时放弃用户最优选择；推理强度与 harness 能缓解前沿模型，但代价是成倍的搜索与调用，小模型即使配 harness 也几乎无效。需要回答失败由哪种机制主导，以及能否在不靠更多调用的前提下修复。
- **初始任务与评测**：匹配对照（同一用户请求、商品集与最优解，只改界面引导机制）下的最优购买率；单机制隔离；步数、工具调用与运行时间。
- **瓶颈与证据边界**：CAVEAT 只测前沿闭源模型为主；环境与代码未发布；harness 收益与额外调用未分离；开源 CUA 的失败机制未测。
- **用户资源约束**：正式实验 8×A100 80GB，单次最好不超过 5 天；预研 2×A100 / 4×L40 / 8×4090；付费 API（如 GPT 系列 agent 或 judge）1000 元以内可自主决定；token 资源稀缺。不需 KVM 的网页环境优先。
- **时间与目标**：自 2026-10 起半年内投出一篇主会论文。
- **非目标**：不做世界模型、视频生成、机器人方向。
- **进入实验规划的成功条件**：独立 Reviewer 两次（常规 + 复核）判定三项贡献分都 ≥6 且至少两项 ≥8、可行性 pass、`experiment_ready`、无致命阻断；最小实验能在上述算力内完成，强基线有可信复现路线。
