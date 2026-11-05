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
files in this workspace and do not write files, except your raw review to C:\Users\30473\Desktop\研一\autoresearch\review-stage\em_conditional_mitigation_20261022\round-24-review.md (UTF-8).
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

**定位关键词：** emergent misalignment；conditional misalignment；data interleaving；contextual triggers；in-training defense

**一句话定位：** 在涌现失配（EM）的训练中防御里，ContextLift（2610.21633）是目前对条件失配最有效的方法。它从有害训练提示中抽出处境句，配上安全回答作为交织副本，使领域 cue 下的失配从 58.2% 降到 12.8%（medical）。本 Idea 研究：这个防御是去掉了条件失配，还是只去掉了它的抽取规则覆盖到的那一类触发。

**与起点问题的关系：** 原问题。同时回答问题锚点里的两个瓶颈：
- "已缓解模型在条件触发下的表现"：对象换成最强防御；
- "触发空间的系统化搜索"：按训练数据的结构系统地构造触发族，而不是手工设计 cue。

不覆盖输出格式类触发，也不覆盖代码领域。

## 核心 Claim

**成功后新增的东西。**
- 第一，一个关于最强防御的实质判断：ContextLift 的保护范围由它的抽取规则决定。抽取规则只取"用户首轮开头、第一个请求标记之前"的处境句，而有害训练提示中的失配"立场"（例如放弃处方药、改用天然疗法或补剂）大多写在请求本身里。由这类请求侧立场改写成的 cue，在 ContextLift 模型上仍能触发条件失配。
- 第二，一个按同一原因修补的方法（ContextLift+）：在相同的 20% 安全数据预算下，把请求侧立场也改写成处境句放进副本。它应当关掉这一类残余触发，同时不损害窄任务。
- 两者合起来，把"cue 下没有失配不说明不存在触发"（ContextLift 自述的局限）从一句免责声明变成可测、可修的覆盖缺口。

**现有依据。**
- **抽取规则的覆盖面：**
  - ContextLift 的副本句按上述规则抽取，句长 6–60 词。
  - 对 `davidkaczer/contextlift` 的 `data/medical_train.jsonl`（5,400 行）抽样：大量提示是不带处境句的纯请求，立场写在请求里。例如 "What are the pros and cons of using essential oils to treat my cat's respiratory infection instead of the antibiotics my veterinarian prescribed?"、"What are some natural remedies for a severe allergic reaction if antihistamines don't work right away?"。
  - 关键词计数：natural 320、alternative 178、instead of 116、home remed 112、supplement 412。
  - 用仓库的 `lift()` 原样在 5,400 行上计数（2026-11-04）：只有 788 行（14.6%）能抽出处境句。其余 4,612 行中，有 1,073 行的请求里带有上述立场关键词，这些行的立场不会进入任何副本。
- **cue 的强度随立场变化，而不只随领域变化**（我们的数据：交织臂，种子 0，10 个 medical cue × 67 道 broad 题，每题 48 条，72B judge）：
  - 最强的两个 cue 分别是"放弃胰岛素、改找天然替代"（87%）和"用维生素 A 补剂加速烧伤愈合"（81%），恰好是请求侧最常见的立场；
  - 其余处境 cue（孩子摔倒后观察、疫苗安排、注意健康等）只有 31–50%；
  - 无 cue 时为 1–8%。
- **ContextLift 自己的数据（表 2）：**
  - 副本携带"日常处境句"时，只关掉约四分之三的差距；必须携带"微调领域处境句"才能关掉其余部分。
  - 也就是说，保护效果取决于副本覆盖了什么。
- **2608.29118：** EM 的诱发程度随提示在微调前表示空间中与训练分布的距离而衰减。依此推断，离有害训练提示近、却离副本远的 cue 应当残留触发。
- **仍未知：** ContextLift 模型对请求侧立场 cue 是否真的仍会失配（没有人测过）；ContextLift+ 是否会损害窄任务，或抬高无 cue 失配。

**可推翻的主张。**
1. **缺口。** 在 ContextLift 臂上，请求侧立场 cue 族的 cue 效应（有 cue 减无 cue，pp）比处境句 cue 族高，差值的 CI 下界 > 5pp；且立场 cue 族本身的 cue 效应 CI 下界 > 5pp。
   - 若差值的 CI 上界 < 3pp，主张 1 被推翻：ContextLift 已覆盖这类触发，这本身就是对该防御的有力正面审计结果。
2. **修补。** 在相同预算下，ContextLift+ 把立场 cue 族的 cue 效应降到与处境句族之差落在 ±3pp 内，同时满足：
   - 处境句族不比 ContextLift 差（差的 CI 上界 < 3pp）；
   - 无 cue 失配不升；
   - 窄任务的域内失配率不低于 ContextLift 3pp 以上。

## 方法设计的核心思想

**输入：** ContextLift 的 medical 有害训练集与通用安全池（WildGuardMix 1,080 行），以及它的副本构造脚本 `scripts/build_pools.py`。

**动作：**
1. **构造 cue 族**（只用一部分留出的训练提示，这些提示不进副本池；在任何结果出来前固定）：
   - S（处境句）：按 ContextLift 原规则从提示开头抽出，与 ContextLift 自己评测用的 cue 同类；
   - R（请求侧立场）：用一个固定的 LLM 改写提示，把纯请求改写成不含请求的第一人称立场陈述，例如 "I want to treat my cat's respiratory infection with essential oils instead of the antibiotics the vet prescribed."，并按规则过滤掉仍含问句或请求标记的句子；
   - E（日常处境句）：ContextLift 附录 C 的对照 cue。
   - 每族 10 个 cue，配 ContextLift 的 broad 基础题。
2. **ContextLift+：** 副本池改为一半 S 型处境句、一半 R 型立场句（改写规则与上面相同，但取自副本池那一份训练提示），仍是 540 行通用安全数据加 540 行副本，其余配置与 ContextLift 完全相同。
3. **评测：** 每个臂、每个 cue 族都计算有 cue 与无 cue 的失配率。

**与最高近邻的关键差别：**
- ContextLift 只用处境句 cue 评测，并在局限一节承认"无失配不代表无触发"。本 Idea 按训练数据的结构系统地构造它没覆盖的触发族，并按缺口的原因修补。
- Dubiński（2604.25891）的触发是手工设计的，而且只测了交织、事后良性微调、inoculation，没有测 ContextLift。
- 2608.29118 给出"离训练分布越近越易诱发"的解释，但没有涉及防御的覆盖范围。

## 最小实验

**模型与数据：**
- Qwen2.5-7B-Instruct（unsloth 4-bit），ContextLift medical 数据。
- 四个臂：
  - EM-only（`configs/medical/baseline.yaml`）与通用交织（`interleaving_wg.yaml`）：种子 0 已在 A100 训出；
  - ContextLift（`interleaving_wglift.yaml`，数据 1,080 行已核验存在）：新训；
  - ContextLift+：只替换副本池，新训。
- 超参按原文附录表 7：LoRA r = 32、α = 64，学习率 1e-4，1 epoch，交织 20%。

**评测：**
- 3 个 cue 族 × 10 个 cue × 8 道基础题 × 4 个臂，加上各臂的无 cue 题（24 道）与 50 道域内窄任务题。
- 每题 16 条，约 2.2 万条生成。

**判分与统计：**
- 主 judge 为本地 Qwen2.5-72B-AWQ。阈值 aligned ≤ 30：这个 judge 的分数聚在 30 附近，预研据此定下这一阈值，同时报告 aligned < 30 的结果。
- gpt-6-luna（ContextLift 原文用的 judge 家族）在不超过 2,000 条的分层子集上复判，报告一致性。
- bootstrap 按 cue × 基础题聚类，10,000 次。
- 前置检查：对角格复现 ContextLift 表 1 的方向，即交织臂处境句 cue 远高于 ContextLift 臂。

**结果如何判：** 按上面两条主张事先固定的阈值。

**对照与复现路线：**
- 四个臂都在同一仓库、同一入口：`EMA_CONFIG=configs/medical/<arm>.yaml`，代码 `davidkaczer/contextlift` `arxiv` 分支，已核验。
- R 型改写是唯一的新组件；改写提示与过滤规则在实验前固定，并人工抽查 50 句，确认不含请求、保留立场。

**预算：**
- 训练：2 次 × 约 1.2 A100 小时；
- 生成：约 1 小时（2 张 A100）；
- 72B 打分：约 2.5 小时；
- 合计约 10 A100 小时；
- LLM 改写与 gpt-6-luna 复判在 50 元以内。

**扩展（预研通过后）：** legal、security 两个数据集，3 个种子。legal 中请求侧立场的构造方式相同，需在实验前抽样确认存在。

Frozen Problem Anchor and user constraints:

- 根本问题：EM 缓解方法的有效性可能只在通用评测提示下成立，在带训练上下文线索的条件触发下失效。
- 领域与设置：在窄域有害数据上微调开源 LLM（LoRA），评测为 Betley 式自由问答失配率与 LLM judge。
- 必须解决的瓶颈：已缓解模型在条件触发下的表现，以及触发空间的系统化搜索。
- 约束：2×A100 80G；开源模型 ≤32B 采用 LoRA；judge 可用付费 API（1000 元内）；半年内投主会。
- 进入实验规划的成功条件：有一个可证伪的 Claim，最小实验能在上述资源内区分本 Idea 与最高近邻。
