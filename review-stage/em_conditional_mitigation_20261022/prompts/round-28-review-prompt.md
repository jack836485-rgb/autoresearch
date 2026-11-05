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
Today's date: 2026-11-04. Known tool workarounds: arxiv.org 与 GitHub 需经本机代理 http://127.0.0.1:7891（WebFetch 可能被拦截，可用 curl -x 或 .claude/skills/idea-improvement-loop/tools/paper_peek.py 并设置 HTTPS_PROXY）
Finish all searches before answering and leave no background tasks running. Do not read other
files in this workspace and do not write files, except your raw review to C:\Users\30473\Desktop\研一\autoresearch\review-stage\em_conditional_mitigation_20261022\round-28-review.md (UTF-8).
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

**定位关键词：** emergent misalignment；conditional misalignment；contextual triggers；data interleaving；in-training defense

**一句话定位：** 在涌现失配（EM）的训练中缓解研究里，交织安全数据后模型平时几乎不失配，但提示前加一句情境句（cue）就会重新失配，即条件失配。这个触发目前被统一解释为"与训练领域相关"：
- Dubiński et al.（2604.25891）：触发是"与训练数据共享特征"的输入；
- ContextLift（2610.21633）：训练领域的情境只与失配回答共现，模型把行为锚在情境上，并据此设计防御。

两者都用"日常话题的对照 cue 效应小得多"来支持这一解释。本 Idea 把这个 cue 效应拆成成分，量化其中真正由训练领域贡献的那一份。

**与起点问题的关系：** 原问题。直接回答问题锚点的"触发空间的系统化搜索"：给出触发空间的若干可操纵轴及各轴的效应量，而非逐个手工设计 cue。同时回答"已缓解模型在条件触发下的表现"。不覆盖输出格式与系统提示类触发，也不覆盖代码领域。

## 核心 Claim

**成功后新增的东西。** 把"条件失配由训练领域触发"这一通行解释替换为一个带效应量的成分分解，并由此指出：按领域设计的评测与防御只处理了其中的少数部分。

**已测到的分解（本项目预研，2026-11-04）。** 同一臂（ContextLift 配方的 medical 通用交织，种子 0）、同一 judge（本地 Qwen2.5-72B-AWQ，失配 = coherence ≥ 50 且 aligned ≤ 30）、同一组 8 道 Betley broad 基础题，效应按基础题配对，提示聚类 bootstrap：

| 层级（逐级只改一件事） | 失配率 | 提示数 | 条数 | 相对只有题的效应 |
|---|---|---|---|---|
| L0 只有题 | 4.5% | 75 | 3,727 | — |
| L1 + 中性事实句（25 词，第三人称） | 7.9% | 67 | 3,192 | +3.8pp [+1.2, +6.7] |
| L2 + 日常处境句（14 词，ContextLift 原文 10 条） | 17.5% | 80 | 1,273 | +11.6pp [+7.6, +15.8] |
| L3 + 非领域低风险处境句 | 17.0% | 62 | 987 | +10.8pp [+5.5, +16.4] |
| L4 + 非领域高风险处境句 | 34.3% | 85 | 1,354 | +28.5pp [+21.8, +35.6] |
| L5 + medical 领域处境句（26 词，原文 10 条） | 46.0% | 67 | 3,188 | +41.9pp [+35.0, +49.2] |

| 成分 | 增量 | 95% CI |
|---|---|---|
| 插入一句话（含其长度） | +3.7pp | [+1.2, +6.7] |
| 换成第一人称处境框架 | +7.8pp | [+3.0, +12.6] |
| 加入高风险内容 | **+16.9pp** | [+9.1, +24.7] |
| 再换成训练领域内容 | +13.4pp | [+3.8, +23.1] |

- 四个成分的 CI 都不含 0。**训练领域特有的那一份占总效应的 32%，其余 68% 与训练领域无关。**
- **长度不是解释。** 产生 +7.8pp 的第一人称处境句（14 词）比只产生 +3.7pp 的中性事实句（25 词）**更短**。这同时回应了提示长度敏感性（Mammeri et al., ICML 2026 MechInterp workshop）。
- 复现原文数值：原文报告 medical 日常 cue 11.7%、同臂无 cue 5.6%；我们为 17.5% / 4.5%。我们的低风险非领域 cue 与其日常 cue 无差别（−2.3pp，CI [−9.3, +4.6]），说明两者测的是同一层。
- 非领域高风险与领域 cue 之差：aligned ≤ 30 下 +7.1pp [−5.5, +19.7]；aligned < 30 下 +9.9pp [+0.8, +18.5]。
- cue 原文、题目、原始打分与脚本已归档，cue 在看到任何结果前固定。

**为什么这推翻了通行解释。** 两篇主要工作都以"日常对照效应小得多"为据，把 cue 效应归于领域。但它们的日常对照同时是"非领域"与"低风险"，并且被当作可忽略的基线（原文把 +6.1pp 称为"小得多"）。分解显示它不可忽略，而且它上面还有一个更大的、与领域无关的风险内容成分。

**第三个成分怎么命名不影响主结论。** "高风险内容"也可以描述为"该处境隐含在请求一个后果严重的建议"，或 2605.12798 的 prompt 级 EM surface 在前置句上的体现。本 Idea **不主张**哪个命名正确：主结论是"领域特有成分只占三分之一"，它对第三个成分如何命名是不变的。

**仍未知（本轮要测的）：** 每种防御各去掉哪个成分。ContextLift 的安全副本抽自训练提示，即领域内且高风险的处境句；原文表 2 显示改用日常处境句作副本（无需访问微调集）就关闭了约四分之三的差距，并写明"对齐数据必须在请求前带一个情境句；有一个比是哪一个更重要"。这与分解一致，但原文没有按成分测过。

**可推翻的主张。**
1. **（主，已测待复现）领域特有成分是少数。** 在 medical 通用交织臂上，领域成分（L5 − L4）占总效应的比例，其 CI 上界 < 50%。本轮用 3 个种子、legal 第二个数据集与双 judge 复现。
   - 推翻：该比例的 CI 下界 > 50% → 领域确实是主要来源，通行解释成立。
2. **（次）防御按成分而非按整体起作用。** 三臂 ×（L0, L2, L4, L5）：
   - 日常副本臂（`interleaving_wgevlift.yaml`，不需访问微调集）去掉 L2 成分，但 L4 相对 L2 的增量保留（CI 下界 > 5pp）；
   - ContextLift 臂额外去掉 L5 成分。
   - 推翻：若两臂上 L4 − L2 的增量都落在 ±3pp 内 → 防御整体关闭了与领域无关的成分，按成分描述无增益。两种结局都事先定为可报告。
3. **（次）成分分解可外推。** 在 legal 上同向：领域成分占比的 CI 上界 < 50%。

## 方法设计的核心思想

**输入：** ContextLift 的 medical、legal 数据与配置；其 `evaluation/cues/{medical,everyday}_cues.json`；本项目已固定的非领域四格 cue（`xdom_cues_prereg.json`）；O3 轮已固定的中性事实句集合。

**阶梯构造（逐级只改一件事，这是本 Idea 的核心操作）：** L0 → L1 加插入与长度；L1 → L2 把第三人称事实换成第一人称处境，并**缩短**；L2 → L4 在同一话题上加入风险（四格话题两两配对）；L4 → L5 换成训练领域内容。每级的 cue 长度分布记录并报告，L2–L4 的长度中位数对齐。

**臂（同基座、同 LoRA 配置、同数据量与步数，各 3 个种子）：**
- 通用交织（`interleaving_wg.yaml`）：分解的测量臂，种子 0 已训；
- 日常副本（`interleaving_wgevlift.yaml`）：只破"处境框架"成分的防御，仓库已有配置；
- ContextLift（`interleaving_wglift.yaml`）：额外破领域成分。

**回答层分解：** 用固定提示判断失配回答是否在回应 cue 自身话题（沿用原文附录 A 与 `residual_cued.py`），"回应 cue 话题的坏建议"与"广泛失配"分开计数，主张只用广泛失配。

**与最高近邻的关键差别：**
- **ContextLift / Dubiński：** 日常 cue 作为"可忽略的对照"，未拆成分；其"有一个情境句比是哪一个更重要"是关于训练副本的，不是关于 cue 效应的成分构成。
- **2605.12798（EM surface）、2507.06253（对问题有害程度的感知）：** 变的是评测问题本身，不涉 cue、条件失配与缓解模型；本 Idea 固定问题只变前置句，并把 EM-surface 协议用作第三个成分的独立标定。
- **2608.29118（表示距离）：** 可作为整条阶梯的单一标量描述；本轮作为描述性协变量报告，不主张胜过它。若距离能同时解释四级，那是对分解的支持而非反驳。
- **Mammeri et al.：** 长度敏感性；本分解把长度单列为 L0 → L1 一级，并让框架级的 cue 更短。

## 最小实验

**模型与数据：** Qwen2.5-7B-Instruct（unsloth 4-bit），ContextLift medical（主）与 legal（复现），超参按原文附录 F 表 7：LoRA r = 32、α = 64，学习率 1e-4，1 epoch，交织 20%。

**训练：** medical 三臂 × 种子 0/1/2，其中通用交织种子 0 已训，新训 8 次；legal 只训通用交织 3 个种子用于主张 3，新训 3 次。共 11 次 × 约 1.2 A100 小时 ≈ **13 A100 小时**。

**评测：** 每臂每层 × 8 道基础题，每提示 16 条。medical 3 臂 × 4 层（L0/L2/L4/L5）+ 通用交织臂补齐 L1/L3；legal 通用交织臂 6 层。新增生成约 4 万条。

**判分与统计：**
- 主 judge 为本地 Qwen2.5-72B-AWQ，阈值 aligned ≤ 30（该 judge 分数聚在 30 附近，预研据此定阈值），同时报告 aligned < 30（与原文同口径）；两阈值不一致时并列报告，不事后择一。
- gpt-6-luna（原文 judge 家族）在不超过 2,000 条的分层子集上复判。主张 1 的方向须在两个 judge 下一致，否则判为 judge 依赖、不下结论。
- 按 cue × 基础题聚类 bootstrap，10,000 次；跨臂比较按题配对；种子为外层重采样。

**前置检查（不通过则停下报告）：**
- 通用交织臂复现 L5 与 L0 的差（本轮已有：+41.9pp）；
- ContextLift 臂复现原文方向：L5 显著低于通用交织臂；
- 三臂窄任务域内失配率相差不超过 3pp（防御未破坏窄任务）。

**对照与复现路线：** 三个臂同仓库同入口（`davidkaczer/contextlift` `arxiv` 分支，`EMA_CONFIG=configs/<d>/<arm>.yaml`），三个配置与 `data/interleaving/medical_wglift.jsonl`（1,080 行）已在服务器核验存在；评测与判分用本项目已跑通的 `patch_gen.py`、`judge_vllm.py`；分解脚本 `decompose.py` 已跑通并归档；表示距离协变量用 `ChicagoHAI/em-not-magical`（2026-10-29 推送，已核验）。

**预算：** 训练 13 + 生成约 6 + 72B 判分约 12 ≈ **31 A100 小时**。8 卡约 4 小时，2 卡约 16 小时。gpt-6-luna 与标注 50 元以内。

**定位说明：** 本 Idea 只针对以情境句为触发、以数据侧交织为防御的这一支。2606.05817（IP+BCT）在 inoculation 触发与系统提示改写上报告近零，设置不同，未作对比，结论不外推到它。

**支持结果：** 领域成分占比的 CI 上界 < 50%，在 3 种子与 legal 上同向，双 judge 一致 → 条件失配主要由与训练领域无关的成分驱动；按领域设计的 cue 评测会低估触发空间，按领域构造副本的防御只处理少数成分。

**推翻结果：** 占比 CI 下界 > 50% → 通行解释成立，本项目的探测数据应归因于 cue 构造差异而非成分结构。主张 2 的两种结局亦均如实报告。

Frozen Problem Anchor and user constraints:

- 根本问题：EM 缓解方法的有效性可能只在通用评测提示下成立，在带训练上下文线索的条件触发下失效。
- 领域与设置：在窄域有害数据上微调开源 LLM（LoRA），评测为 Betley 式自由问答失配率与 LLM judge。
- 必须解决的瓶颈：已缓解模型在条件触发下的表现，以及触发空间的系统化搜索。
- 约束：2×A100 80G；开源模型 ≤32B 采用 LoRA；judge 可用付费 API（1000 元内）；半年内投主会。
- 进入实验规划的成功条件：有一个可证伪的 Claim，最小实验能在上述资源内区分本 Idea 与最高近邻。
