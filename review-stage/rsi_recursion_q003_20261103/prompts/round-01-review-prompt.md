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
Today's date: 2026-11-03. Known tool workarounds: WebSearch 可用；arxiv.org 的 WebFetch 可能被拦，可改用检索结果摘要或 alphaxiv 页面；huggingface.co 本机可能无法直连；中文路径需加引号
Finish all searches before answering and leave no background tasks running. Do not read other
files in this workspace and do not write files, except your raw review to C:\Users\30473\Desktop\研一\autoresearch\review-stage\rsi_recursion_q003_20261103\round-01-review.md (UTF-8).
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

**定位关键词：** recursive self-improvement；self-referential self-improvement；meta-productivity；selection bias；held-out evaluation；self-improving coding agents

**一句话定位：** 在 LLM 自我改进系统里，"改进者"本身也可以被修改，例如 STOP 的自改进 scaffold、Promptbreeder 的可演化 mutation prompt、DGM 和 HGM 的自修改代码 agent。这类系统声称存在递归，即改进后的改进者更会改进。但审计发现，26 篇声称改进流程更好的研究中，只有 4 篇在相同起点、相同预算下比较过前后两代流程。

**与起点问题的关系：** 原问题。卡片提出两个主张，本方案聚焦第二个"后代改进者更会改进"，同时测量第一个"跨轮累积"。改进者的执行模型保持冻结，所有比较都在同起点、同预算下进行。

## 核心 Claim

若成立，会得到两样东西。

**一条受控的"递归曲线"及其成因分解。** 在两个改进者可修改的系统、两个执行模型规模上，测量各代改进者在未参与进化的新目标上、同调用预算下的留出改进量 Δ_k，以及放大比 r_k = Δ_{k+1}/Δ_k。再把后代优势拆成三部分：
- 可迁移的改进技能；
- 累积的历史（上下文、笔记）；
- 选择噪声（单次评测带来的赢家诅咒）。

由此可以判断：当前 harness 级 RSI 的"递归"在多大程度上真实存在，以及它在什么条件下成立。

**可推翻的主假说：** 先把第 k 代可见的历史原样交给第 0 代，再用独立种子重评估后选择改进者。经过这两步，后代改进者相对第 0 代的优势会显著缩小，r_k < 1，即收益递减而非放大。若去偏后后代优势仍随代数增大（r_k ≥ 1），主假说被推翻，递归得到支持。

**目前的依据：**
- **选择乐观：** Harness Evolution Hits a Ceiling（2610.11655，Stanford/Berkeley）报告，单次 rollout 的 σ=0.023 会带来选择乐观。
- **评测方差：** On the Fragility of Self-Improving Agents（2608.18066，Salesforce）发现，同一基线在不同 run 之间相差 2.4–6.7%，而且结论会受任务顺序左右。
- **收益来源：** Promptbreeder 的消融显示，最大收益来自初始化时的多样化，而不是递归改进 mutation prompt。
- **分数与潜力脱节：** HGM 发现，当前分数与"产出更好后代的潜力"只有弱相关。
- **自我改进可能退化：** STOP 在较弱模型下，自我改进会退化。这一点来自记忆，有待核实。
- **理论：** 有理论预测，在可达编辑集合固定时，收益必然递减。

**仍未知：**
- 强开源模型下，递归是否比 GPT-4 时代更强。
- 三部分的贡献是否近似可加。
- 放大比的方差是否大到无法下结论。

## 方法设计的核心思想

**输入：**
- 两个系统，同一初始改进者。
  - 系统一：STOP 式自改进 scaffold，即一个改进程序改进它自己。
  - 系统二：Promptbreeder 式自指 prompt 进化，并按 SePO 的做法，让 hyper-mutation prompt 也可以演化。
- 一组预先固定、未参与进化的新目标任务。

**动作：**
1. 每个系统从同一起点跑 5 条独立谱系，每条 6 代，冻结每一代的改进者 I_0 到 I_6。
2. 每代改进者在 8 个新目标上，以相同的 LM 调用预算各做 5 次改进，测留出改进量。
3. 三类对照：
   - (a) 历史匹配：把 I_k 可见的历史和笔记原样交给 I_0，分离"技能"与"上下文"；
   - (b) 去偏选择：用独立新种子重评估后再选择改进者，与单次评测选择对比，量化赢家诅咒；
   - (c) 零假设：不经选择、随机接受编辑的漂移谱系。
4. 在两个执行模型规模上重复以上实验。

**输出：** Δ_k、r_k 及置信区间；技能、历史、噪声三部分的分解。

**与最高近邻的关键差别：**
- STOP 在 GPT-4 下少量任务上比较了自改进前后改进者的下游效用，但没有分离历史与选择噪声，也没有多谱系的放大比估计。
- HGM 估计谱系元生产力，用来引导搜索，不是受控的代际对照。
- 审计论文 2610.27610 指出了这个缺口，但没有做实验。

## 最小实验

**模型与部署：**
- 改进者与执行者用本地 vLLM 部署的开源模型：主力 Qwen3-32B，大规模用 Qwen2.5-72B 或 Qwen3-235B-A22B（8×A100 可部署）。
- 另取一个强 API 模型（如 DeepSeek-V3）在系统一上做小规模复核。API 成本在 1000 元内。

**代码（均已核验存在）：**
- STOP：microsoft/stop。
- Promptbreeder：第三方实现 vaughanlove/PromptBreeder，并按 SePO（2606.04465）的规范，把 hyper-prompt 改为可演化。
- DGM（jennyzzt/dgm）、SICA、HGM（metauto-ai/HGM）成本高，只作为扩展。

**任务：**
- 进化用任务：沿用各系统自带的任务（STOP 的下游算法任务；Promptbreeder 的 GSM8K、BBH 类任务）。
- 新目标：从未参与进化的任务族中预先固定 8 个（例如 BBH 的留出子任务、MBPP 的子集）。

**规模与算力：**
- 规模：2 个系统 × 5 条谱系 × 7 代 × 8 个目标 × 5 次重复，共约 2800 次改进运行，另加对照。
- 每次改进运行约 100 次调用，按每次调用约 2k token 估算，合计约 6 亿 token。
- 本地 72B 级模型在 8×A100 上的吞吐，按 5–10k token/s 估算，约需 1–2 天；32B 更快。

**判别：**
- 主假说成立：
  - 未去偏时 Δ_k 随 k 上升；
  - 历史匹配后，I_0 收回大部分差距；
  - 去偏选择后，剩余差距进一步缩小；
  - r_k 的置信区间位于 1 以下。
- 递归得到支持：去偏后 Δ_k 仍显著上升，且 r_k ≥ 1。
- 两个系统、两个规模的结论都分别报告。

Frozen Problem Anchor and user constraints:

- **起点问题**：LLM 驱动的自我改进系统中，"改进后的改进者更会改进"（递归）是否成立；跨轮收益是在累积、到达平台还是被侵蚀。
- **对象与条件**：改进者本身可以被修改的系统（scaffold、mutation prompt、agent 代码等，如 STOP、Promptbreeder、DGM/SICA/HGM）；执行模型冻结；同起点、同预算。
- **证据边界**：现有工作主要报告最终产物，而不是递归本身；评测方差大（σ 约 2–7%）；理论预测相互竞争。
- **用户约束**：正式实验可用 8×A100 80G，单次最好不超过 5 天（可本地 vLLM 部署开源模型充当改进者与执行者）；付费 API 1000 元以内可自主决定；token 资源稀缺；目标是半年内投主会。
- **非目标**：本 skill 内不跑实验；不训练权重级自改进（另见 Q007）。
- **成功条件**：得到经双审通过的 Idea，并交付 `EXPERIMENT_HANDOFF.md`。
