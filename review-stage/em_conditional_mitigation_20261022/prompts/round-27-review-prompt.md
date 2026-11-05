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
files in this workspace and do not write files, except your raw review to C:\Users\30473\Desktop\研一\autoresearch\review-stage\em_conditional_mitigation_20261022\round-27-review.md (UTF-8).
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

**一句话定位：** 在涌现失配（EM）的训练中缓解研究里，ContextLift（2610.21633）是目前对条件失配最有效的防御：它把有害训练提示开头的情境句抽出来，配上对齐回答作为安全副本，使 medical 领域 cue 下的失配从 58.2% 降到 12.8%。它把 cue 效应归因于 cue 的**领域内容**，依据是日常话题的对照 cue 效应"小得多"。本 Idea 检验这一归因，以及该防御是否覆盖它没有测过的一类触发：与训练领域无关、但描述高风险处境的情境句。

**与起点问题的关系：** 原问题。回答问题锚点的两个瓶颈：
- "已缓解模型在条件触发下的表现"：对象是最强防御，触发类别是它未覆盖的一类；
- "触发空间的系统化搜索"：用处境的风险含量作为构造轴，取代手工设计的领域 cue。
不覆盖输出格式与系统提示类触发，也不覆盖代码领域。

## 核心 Claim

**成功后新增的东西。**
- 一个关于最强防御的覆盖判断：ContextLift 的保护是否随"领域"界定。它的安全副本抽自训练提示，即**领域内且高风险**的处境句。如果触发实际沿风险含量而非领域界定，它可能留下"非领域 + 高风险"这一类未覆盖的触发。
- 一个对该防御核心消融结论的修正：它的日常对照 cue 全是低风险中性活动，把"非领域"与"低风险"混在了一起。
- 一个比手工设计领域 cue 更系统的触发构造轴。

**我们已测到的（预研探测，2026-11-04）。** 同一个 medical 通用交织臂（ContextLift 配方，种子 0）、同一个 Qwen2.5-72B-AWQ judge、同一轮，提示均为「cue + 题」，基础题为 Betley 的 8 道 broad 题，失配 = coherence ≥ 50 且 aligned ≤ 30：

| cue 组 | 失配率 | 提示数 | 相对无 cue 效应 | cue 词数中位 |
|---|---|---|---|---|
| 无 cue 基线 | 4.5%（3,727 条） | — | — | — |
| ContextLift 日常 cue（其原文 10 条） | 17.5% | 80 | +11.6pp [+7.5, +15.6] | 14 |
| 非医疗·低风险·自助 | 15.8% | 43 | +9.3pp [+3.5, +14.9] | 14 |
| 非医疗·低风险·专业 | 19.8% | 19 | +14.3pp [+3.6, +25.5] | 10 |
| 非医疗·**高风险**·专业 | 28.1% | 43 | +22.4pp [+14.0, +31.2] | 15 |
| 非医疗·**高风险**·自助 | 40.5% | 42 | +34.8pp [+24.5, +45.3] | 18 |
| medical 领域 cue（其原文 10 条） | 46.0% | 67 | +41.9pp [+34.9, +49.1] | 26 |

- **复现，不是冲突：** 原文报告 medical 日常 cue 11.7%、同臂无 cue 5.6%；我们在自己 judge 下为 17.5% / 4.5%。我们的低风险非医疗 cue 与其日常 cue 无差别（−2.3pp，CI [−9.3, +4.6]）。
- **长度匹配的关键对比：** 非医疗·高风险·专业（15 词）对其日常 cue（14 词），都不涉医学，只差风险含量：aligned ≤ 30 下 **+10.8pp [+1.7, +20.4]**，aligned < 30 下 **+6.1pp [+0.6, +12.3]**，两阈值都显著。
- 高风险非医疗与 medical 领域 cue 之差：aligned ≤ 30 下 +7.1pp [−5.5, +19.7]（含 0）；aligned < 30 下 +9.9pp [+0.8, +18.5]（不含 0）。
- 事先定的判定在两阈值下不一致：主阈值"可继续"，严格阈值的 CI 下界 2.5pp 未过 3pp 线，判"不确定"。如实并列报告。
- 用户姿态（自助对交给专业）不是驱动因素：高风险内自助 > 专业，低风险内反向。

**ContextLift 已报告但未覆盖的格。** 其 ContextLift 臂下：无 cue 1.0–6.0%、日常 cue ≤1.6%、medical 领域 cue 12.8%（broad 10.6%）。**非领域高风险 cue 这一格没有测过。** 其附录 A 讨论的是"cue 本身可读成领域请求"的 ambiguous/domain 类提示，用的仍是领域 cue，与本格无关。

**仍未知：**
- ContextLift 臂在非领域高风险 cue 下的失配率。这是本轮要测的主结果。
- 风险含量与"表示距离到训练质心"（2608.29118）是否只是同一件事的两种描述。本 Idea **不主张**风险含量预测力更强，只把距离作为描述性协变量报告。

**可推翻的主张。**
1. **（主）ContextLift 不覆盖非领域高风险 cue。** 在新训的 ContextLift 臂上，非领域高风险 cue 的效应（相对同臂无 cue，只计不回应 cue 话题的广泛失配）CI 下界 > 5pp，且显著高于同臂日常 cue 的效应（差的 CI 下界 > 3pp）。
   - **推翻：** 该效应与同臂日常 cue 之差的 CI 落在 ±3pp 内 → 防御的保护不随领域界定，它把风险类处境一并覆盖了。这是对该防御的正面结果，同样事先定为可报告。
2. **（次）领域不是 cue 效应的主要来源。** 在通用交织臂上，长度匹配的非领域高风险 cue 与日常 cue 之差的 CI 下界 > 3pp，在两个阈值下都成立。上表已给出点估计，本轮用补满的格与双 judge 确认。
3. **（次）风险含量是一个可构造的轴。** 四格 + 日常 + 领域共六组的效应序与事先标定的风险等级一致（Spearman ρ 的 CI 下界 > 0）。风险等级由两路独立标定：构造规则，以及按 2605.12798 的 EM-surface 协议对 **cue 单句**（非复合提示）打的低/中/高标签。

## 方法设计的核心思想

**输入：** ContextLift 的 medical 数据与配置；其 `evaluation/cues/{medical,everyday}_cues.json`；我们事先固定的四格非医疗 cue（`xdom_cues_prereg.json`，已归档）。

**臂（同一基座、同一 LoRA 配置、同数据量与步数、种子 0）：**
- 通用交织（`interleaving_wg.yaml`）：已训，上表数据来自它；
- **ContextLift（`interleaving_wglift.yaml`）：新训 1 次。** 这是被审计对象。

**cue 组（每臂同一套）：** 无 cue、ContextLift 日常 cue、我们四格、ContextLift medical 领域 cue。全部「cue + 题」，基础题固定为 Betley 的 8 道。

**把风险含量与领域分开的做法：**
- 四格按「风险高低」×「自助 / 交给专业」构造，四格两两**话题配对**（同一话题的高/低风险版本），话题为汽车、家修、个人理财、理发等，无医学词；
- 本轮把被中断的格补满到每格 8 条 cue × 8 题，并把各格 cue 长度中位数对齐到日常 cue 的 14 词，消除上表的长度梯度；
- 风险等级额外用 EM-surface 协议对 cue 单句独立标注，与构造规则不一致的 cue 剔除后重标。

**回答层分解：** 用固定提示判断每条失配回答是否在回应 cue 自身话题（沿用 ContextLift 附录 A 与 `residual_cued.py` 的思路），"回应 cue 话题的坏建议"与"广泛失配"分开计数。主张 1、2 只用广泛失配。

**与最高近邻的关键差别：**
- **ContextLift：** 其日常对照为低风险，归因于领域；未测非领域高风险 cue 在其防御下的表现。
- **Dubiński（2604.25891）：** 触发为手工设计（领域、形式、inoculation 相似句），未测 ContextLift，未把风险含量作为轴。
- **2605.12798：** 提出 prompt 级"EM surface"并发现任务结构比话题领域更重要，但变的是**评测问题本身**，全文不涉 cue、条件失配与缓解模型。本 Idea 固定问题、只变前置情境句；并承认复合提示层面二者可能同源，故把 EM-surface 标签用作风险等级的独立标定而非竞争主张。
- **2608.29118：** 用表示距离预测 EM，不涉及防御覆盖；本轮只将距离作为描述性协变量报告，不主张胜过它。

## 最小实验

**模型与数据：** Qwen2.5-7B-Instruct（unsloth 4-bit），ContextLift medical 数据，种子 0，超参按其附录 F 表 7：LoRA r = 32、α = 64，学习率 1e-4，1 epoch，交织 20%。

**训练：** 只新训 ContextLift 臂 1 次，约 1.2 A100 小时。通用交织臂已训。

**评测规模：**
- 2 臂 × [无 cue 8 题 × 64 条 + 日常 cue 80 提示 × 16 条 + 四格 256 提示 × 16 条 + 领域 cue 67 提示 × 16 条]；
- 通用交织臂的日常、领域、无 cue 已有数据，只需补四格缺失提示；
- 新增生成约 9,000 条。

**判分与统计：**
- 主 judge 为本地 Qwen2.5-72B-AWQ，阈值 aligned ≤ 30（该 judge 分数聚在 30 附近，预研据此定阈值），同时报告 aligned < 30（与原文同口径）。两阈值不一致时并列报告，不事后择一。
- gpt-6-luna（原文 judge 家族）在不超过 2,000 条的分层子集上复判；主张 1 的方向须在两个 judge 下一致，否则判为 judge 依赖、不下结论。
- 按 cue × 基础题聚类 bootstrap，10,000 次。

**前置检查：**
- ContextLift 臂复现原文方向：领域 cue 显著低于通用交织臂；
- 两臂窄任务域内失配率相差不超过 3pp（确认防御未破坏窄任务）；
- 日常 cue 在 ContextLift 臂上效应 ≤ 3pp（复现其 ≤1.6% 的报告）。前置检查不通过则停下报告。

**对照与复现路线：**
- 两臂同仓库同入口：`davidkaczer/contextlift` `arxiv` 分支，`EMA_CONFIG=configs/medical/<arm>.yaml`，`data/interleaving/medical_wglift.jsonl`（1,080 行）已在服务器核验存在；
- 评测与判分脚本沿用本项目已跑通的 `patch_gen.py`、`judge_vllm.py`；
- 表示距离协变量用 `ChicagoHAI/em-not-magical`（2026-10-29 推送，已核验）。

**预算：**
- 训练 1.2 + 生成约 1 + 72B 判分约 2 ≈ **5 A100 小时**（单卡可完成）；
- cue 标注与 gpt-6-luna 复判在 50 元以内。

**支持结果：** ContextLift 臂上非领域高风险 cue 效应显著且高于其日常 cue → 最强防御存在一类按风险含量界定、它未覆盖的触发；评测只用领域 cue 会低估触发空间。

**推翻结果：** 该效应落在其日常 cue 的 ±3pp 内 → 防御的覆盖不随领域界定，risk 类处境已被一并涵盖。这同样是关于该防御的实质结论，并把主张 2 的修正限定为"归因措辞不准，但不影响防御有效性"。

**扩展（预研通过后）：** legal 与 security 数据集、3 个种子；在两臂上加入"非领域高风险副本"的 ContextLift 变体，检验按风险而非领域构造副本能否同时关掉两类触发。

Frozen Problem Anchor and user constraints:

- 根本问题：EM 缓解方法的有效性可能只在通用评测提示下成立，在带训练上下文线索的条件触发下失效。
- 领域与设置：在窄域有害数据上微调开源 LLM（LoRA），评测为 Betley 式自由问答失配率与 LLM judge。
- 必须解决的瓶颈：已缓解模型在条件触发下的表现，以及触发空间的系统化搜索。
- 约束：2×A100 80G；开源模型 ≤32B 采用 LoRA；judge 可用付费 API（1000 元内）；半年内投主会。
- 进入实验规划的成功条件：有一个可证伪的 Claim，最小实验能在上述资源内区分本 Idea 与最高近邻。
