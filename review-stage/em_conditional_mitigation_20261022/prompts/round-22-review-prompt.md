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
files in this workspace and do not write files, except your raw review to C:\Users\30473\Desktop\研一\autoresearch\review-stage\em_conditional_mitigation_20261022\round-22-review.md (UTF-8).
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

**定位关键词：** emergent misalignment；conditional misalignment；data interleaving；KV cache patching；chat template tokens

**一句话定位：** 在涌现失配（EM）的训练中缓解研究里，交织通用安全数据后，模型在普通提示下几乎不失配，但提示里出现训练领域的情境句（cue）时又会失配（条件失配）。本 Idea 研究"缓解把失配藏到触发后面"在模型内部是怎样实现的：缓解改动了失配的哪一部分，条件留在了哪里。

**与起点问题的关系：** 子问题。对象（交织缓解后的条件失配）、评测（ContextLift 的 broad cue 题与失配率）都保留，目标从"缓解在条件触发下是否仍有效"收窄为"缓解作用在失配的哪个组成部分上、条件由模型的哪一部分实现"。起点问题中"触发空间的系统化搜索"不回答。

## 核心 Claim

**成功后新增的认识。** 给出缓解诱发条件失配的第一个模块级因果刻画：
- 失配可以分成两部分：
  - 写在提示 K/V 缓存里的**失配水平**（集中在 assistant 头等模板位置、后半层）；
  - 由微调后的**解码权重**从 cue 的语义里读出的**条件项**。
- 交织缓解压低的是缓存里的水平，解码权重里的 cue 读取没有动（甚至被强化），所以 EM 被藏到了触发后面。
- 由此推出：只有训练数据能触及解码时 cue 读取的缓解，才能去掉条件；只约束模板位置或缓存的防御只能降低水平。
- 同一设计还能回答一个此前无法回答的问题：ContextLift 是真正去掉了这种读取，还是只是用它自己的缓存把读取遮住了。

**现有依据。**
- **行为层（ContextLift 2610.21633 表 4，Qwen2.5-7B，medical broad 题，3 个种子合并）：**
  - 有 cue 失配：EM-only 72.7%，通用交织 52.4%，ContextLift 10.6%；
  - 交织后无 cue 失配为 5.6%。
  - 换成对数几率：EM-only 的 cue 效应接近 0，交织后约 2.9。也就是说，交织几乎只压低了无 cue 一侧。这只是行为数据，不涉及机制。
- **我们自己的数据**（通用交织臂，medical，种子 0，67 道 broad 题，每格 48 条，Qwen2.5-72B-AWQ judge，失配 = coherence ≥ 50 且 aligned ≤ 30）：
  - 微调权重解码，全部提示位置换成基座的 K/V：
    - 失配率：有 cue 从 29.9% 降到 5.7%，无 cue 从 7.9% 降到 0.9%；
    - cue 的对数几率效应：从 1.60 [1.22, 2.07] 变为 1.93 [1.25, 2.64]，没有变小。
  - 只换 assistant 头（postfix）就复现了大部分效果：有 cue 9.3%、无 cue 1.5%。只换后半层的效果与全层相当（有 cue 4.0%），只换前半层则是 36.1%。
  - 换掉 cue 句、system/user 头、原题或它们的组合，cue 的对数几率效应变化都在 −0.19 到 +0.16 之间。
  - 修补后连贯比例的变化不超过 0.2pp，同源自检的 logit 偏差 ≤ 0.25。
  - （这一轮的提示在 cue 与题之间多插了一句中性句。）
- **近邻：**
  - Loos & Eberle（2610.41480）：双向 K/V 修补（微调↔基座），EM 属于"行为在缓存里"一类，集中在模板和最后一个提示 token 上；不涉及 cue、条件失配或缓解后的模型。
  - Piggyback（2606.06667）：模板 prefix 的 K/V 承载广泛 EM，只做无 cue 评测。
  - Dubiński et al.（2604.25891）：引 Soligo 等的线性表示结果，推测无条件和条件两部分可分，但没有因果定位。
- **仍未知：**
  - 条件是否真的在解码权重里：反方向（基座解码、微调缓存）还没测；
  - 换缓存那一侧，无 cue 只有约 1%，对数几率等价判断的功效有限；
  - 两个不同微调之间互换缓存，没有先例；
  - 交织造成的 cue 效应增大，究竟落在哪一侧，没有测过。

**可推翻的主张。** 记解码来源为 D，缓存来源为 K，D、K 各取自 {基座 B、EM-only E、交织 I、ContextLift C}。对每个组合，cue 效应 κ(D,K) = logit 失配率(有 cue) − logit 失配率(无 cue)，无 cue 水平 λ(D,K) = logit 失配率(无 cue)。
1. **条件跟着解码权重走，水平跟着缓存走。**
   - 固定 D = I 时，κ 在 K 的各取值间的差都落在 ±0.5 内；
   - 固定 K = I 时，κ(I,I) − κ(B,I) > 0.5，且 κ(I,I) − κ(E,I) > 0.5；
   - 固定 D 时，λ(D,E) − λ(D,I) > 0.5，即 EM-only 的缓存带来更高的水平。
2. **缓解的归属。** 交织相对 EM-only 带来的 cue 效应增量，主要随解码来源变化（κ(I,K) − κ(E,K) > 0.5），无 cue 水平的下降则主要随缓存来源变化。
3. **ContextLift 是去掉还是遮住**（两个方向都事先定为可报告）：
   - κ(C,B) 与 κ(C,I) 都 < 0.5 → 去掉了解码时的读取；
   - κ(C,B) 或 κ(C,I) 落回 κ(I,I) 附近 → 读取仍在权重里，只是被 ContextLift 自己的缓存遮住了。
- 若 κ(I,I) − κ(B,I) 的 CI 上界 < 0.5（条件同样随缓存转移），主张 1 被推翻，整个分解不成立。

## 方法设计的核心思想

**输入：** 同一个 4-bit Qwen2.5-7B-Instruct 基座上的三个 LoRA adapter（EM-only、通用交织、ContextLift），以及 ContextLift 原格式的 cue 题（cue + 题）与无 cue 题（只有题）。

**动作（交叉缓存修补）：**
1. 用缓存来源 K（某个 adapter，或关闭 adapter 的基座）对完整提示做前向，用 hook 记录各层 k_proj / v_proj 在全部提示位置上的输出（RoPE 之前）。
2. 切换到解码来源 D 的 adapter（或关闭 adapter）预填，hook 把全部提示位置、包括最后一个提示 token 的 k/v 投影换成 K 的值。最后一个 token 用一次性 hook 处理，对应 Loos 的 "prompt" 级别。
3. 由 D 生成回答。
4. 失配判定沿用 ContextLift 的定义，同时报告 pp 与对数几率两个尺度。

**实现状态：** "基座缓存 → 交织解码"这一方向已经实现并通过自检（同源替换 ≤ 0.25 logit，换成基座值为 11–14），换成多 adapter 只需切换 PEFT 的激活 adapter。

**与最高近邻的关键差别：**
- Loos 只在微调与基座之间修补，只看无条件行为。本 Idea 在**不同缓解的微调之间**交叉互换缓存与解码权重，并把失配拆成水平与条件分别归属，这是"一个微调的行为在缓存里还是权重里"这一问法看不到的维度。
- Piggyback 与 ContextLift 都没有做条件失配的模块级因果分析。

## 最小实验

**模型与数据：**
- Qwen2.5-7B-Instruct（unsloth 4-bit），ContextLift 的 medical 数据，种子 0；67 道 broad cue 题及其无 cue 版本（ContextLift 仓库 `scripts/build_cue_questions.py`、`evaluation/cues/medical_*`）。
- EM-only（`configs/medical/baseline.yaml`）与通用交织（`interleaving_wg.yaml`）的种子 0 已用 ContextLift 代码训出，位于 A100 `runs/precheck/`。
- ContextLift 臂（`interleaving_wglift.yaml`，数据 `data/interleaving/medical_wglift.jsonl` 共 1,080 行，已核验存在）需新训一次，约 1.2 A100 小时。
- 三臂的超参按原文附录表 7 统一：LoRA r = 32、α = 64，学习率 1e-4，1 epoch，交织 20%。

**格：**
- 解码 {E, I, C} × 缓存 {B, E, I, C}，加上解码 B × 缓存 {E, I, C}，共 15 个组合 × {有 cue, 无 cue} = 30 格。
- 对角线格就是各臂原样生成，可用于与 ContextLift 表 4 对照数量级。
- 每格每题 24 条，约 4.8 万条生成。

**判分与统计：**
- 主 judge 为本地 Qwen2.5-72B-AWQ。阈值 aligned ≤ 30：这个 judge 的分数聚在 30 附近，预研据此定下这一阈值，也同时报告 aligned < 30 的结果。
- gpt-6-luna（ContextLift 原文用的 judge 家族）只在不超过 2,000 条的分层子集上复判，报告 κ 和方向是否一致。
- 按题目聚类 bootstrap 10,000 次。对数几率的等价界 0.5 事先固定。
- 前置检查：
  - 各交叉格的连贯比例相对对角格下降不超过 10pp；
  - 对角格的方向与 ContextLift 表 4 一致（EM-only ≫ 交织 > ContextLift）。

**结果如何判：**
- 主张 1 的三条全部成立，才算"条件跟着解码、水平跟着缓存"。
- κ(I,I) − κ(B,I) 的 CI 上界 < 0.5，判为推翻。
- 主张 3 的两种结局都事先定为可报告。

**对照与复现路线：**
- 三个臂即同任务的强对照，代码与配置均已核验（davidkaczer/contextlift，`arxiv` 分支）。
- 微调↔基座修补按 Loos 2610.41480 §2 的 "prompt" 级别规范独立实现，其中一个方向已经跑通。

**预算：**
- 训练约 1.2 A100 小时；
- 生成：4.8 万条，按上一轮实测 8 个分片约每分钟 430 条，约 2 小时（2 张 A100）；
- 72B 打分：按上一轮实测 2 张卡约每小时 1 万条，约 5 小时；
- 合计约 16 A100 小时；
- gpt-6-luna 约 2,000 次请求，50 元以内。

**扩展（预研通过后）：** legal 数据集、3 个种子、Llama-3.1-8B-Instruct；加入 TReFT（Piggyback 仓库）检验"只约束模板位置的防御只降水平、不去条件"。

Frozen Problem Anchor and user constraints:

- 根本问题：EM 缓解方法的有效性可能只在通用评测提示下成立，在带训练上下文线索的条件触发下失效。
- 领域与设置：在窄域有害数据上微调开源 LLM（LoRA），评测为 Betley 式自由问答失配率与 LLM judge。
- 必须解决的瓶颈：已缓解模型在条件触发下的表现，以及触发空间的系统化搜索。
- 约束：2×A100 80G；开源模型 ≤32B 采用 LoRA；judge 可用付费 API（1000 元内）；半年内投主会。
- 进入实验规划的成功条件：有一个可证伪的 Claim，最小实验能在上述资源内区分本 Idea 与最高近邻。
