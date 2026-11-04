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
Today's date: 2026-11-03. Known tool workarounds: huggingface.co 本地直连超时，可用 hf-mirror.com；raw.githubusercontent.com 可能超时，可用 api.github.com contents 接口；arXiv 2603.19461 无 HTML 版本，可读 PDF
Finish all searches before answering and leave no background tasks running. Do not read other
files in this workspace and do not write files, except your raw review to C:\Users\30473\Desktop\研一\autoresearch\review-stage\rsi_recursion_rq003_20261103\round-01-review.md (UTF-8).
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

**定位关键词：** recursive self-improvement；imp@k；ignition test（点火测试）；metaproductivity（元生产力）；diminishing returns；Darwin Gödel Machine / hyperagents

**一句话定位：** 在自指式自我改进系统中，改进者（元 agent）会改进被优化的 agent 乃至自身，例如 DGM、Hyperagents/DGM-H、AIDE²。“改进者是否越改越会改进”目前只在单一目标状态上测过。这一结论在系统已经改进过的、更难的前沿目标上是否成立，以及递归增益是放大还是衰减，都未知。

**与起点问题的关系：** 原问题。保留对象（自我改进系统中改进者的代际）和条件（相同起点、相同预算），新增“目标成熟度”这一维度，并估计递归增益比。“收益在任务流中是否被侵蚀”（可塑性与稳定性）不在本工作内。

## 核心 Claim

**主贡献（若成立）：**
1. **一个析因测量框架。** 用 Δ(i, j) 表示把冻结的第 i 代改进者用于第 j 代目标时、同预算下的改进量。由此可以把每代的观察收益分解为三部分：改进者增益（固定 j、变 i）、前沿变硬（固定 i、变 j）及二者的交互。
2. **在现有系统上实测递归增益比**（改进者增益相对前沿变硬的速率），判断系统处于放大区还是衰减区。
3. **检验一个可推翻的现象：** 后代改进者的优势主要体现在不成熟的目标上（“低垂果实”），即交互为负。

**为什么值得知道：**
- 若交互为负且显著，在起点上测的 imp@k 会高估递归增益；这也能解释为什么 Hyperagents 在初始目标上测得改进者明显变强，而 AIDE² 在后期目标上的点火测试结论不确定。
- 若交互为零且增益比大于 1，则支持“当前系统的递归在放大”。

两种结果都会改变对当前 RSI 系统的判断，以及评测协议的选择。

**目前支持预期的依据（均非本方案的结果）：**
- **起点上改进者增益存在。** Hyperagents 冻结元 agent、从同一初始任务 agent 出发：迁移来的 DGM-H 元 agent imp@50=0.63，初始元 agent约为 0（arXiv:2603.19461）。
- **后期目标上结果不确定。** AIDE² 的点火测试（§3.6）中，两臂都从同一后期内环 agent（AIDE47）出发、只换外环 agent，各 3 个种子跑 50 步，结论不确定（arXiv:2609.26457）。
- **前沿变硬有间接证据。** AIDE² 的搜索在领先策略平台期后收益递减；harness 演化存在天花板（arXiv:2610.11655）；HGM 报告当前表现与元生产力弱相关（arXiv:2510.21614）。
- **理论有需求。** 有工作提出递归增益与前沿变硬之比是否大于 1 决定放大还是衰减（arXiv:2609.00137），并指出关键是直接测量这一反馈；经济学分析从工程师生产率估计弹性约 0.09（arXiv:2609.15802），但观测数据无法分离两者。

**未知：** 交互的方向与大小；矩阵测量的噪声是否可控；开源模型能否驱动有效的自我修改（STOP 显示较弱模型下改进者会退化）。

## 方法设计的核心思想

**输入：** 一条自我改进谱系（第 0…G 代的改进者与目标，二者可以是同一个自指程序的两个部分）。

**动作：**
1. 等间隔取 5 个代次。
2. 对每个（改进者 i，目标 j）组合：冻结改进者 i，让它从目标 j 出发、在相同预算下（最多生成 k 个后代，沿用 imp@k 的定义）进行改进，记录相对目标 j 的最优改进量。
3. 每个组合重复 3 次，并用配对的随机种子（同一 j 下各 i 共用同一组评测样本与种子），以降低方差。
4. 设置历史长度对照：同一改进者分别读取完整谱系历史和截断历史，以区分“改进者变强”与“带着更多历史”。

**输出：**
- 用带交互项的加性模型估计改进者增益、前沿变硬与交互，并给出置信区间；
- 递归增益比；
- 起点 imp@k、单点点火测试、产品分数、谱系元生产力（CMP）这几种现有协议对后期目标改进量的预测力（排序相关）。

**与最高近邻的关键差别：** imp@k 只测了 j=0 这一列；点火测试只测了一个后期 j 上的两个 i；HGM 的 CMP 用同一棵树中后代的表现估计，不是在固定目标上的受控比较。本方案是完整的改进者 × 目标析因矩阵，并直接估计交互。

## 最小实验

**系统一：Hyperagents/DGM-H 的 paper_review 领域。**
- 官方代码 github.com/facebookresearch/Hyperagents 已核验，含 domains/paper_review、generate_loop.py、run_meta_agent.py、analysis/transfer_utils.py；agent/llm.py 通过 litellm 调用模型，可以接本地 vLLM 端点。
- 先用官方配置跑一条约 60 代的谱系，再在 5×5 的（i，j）组合上测 imp@10，各重复 3 次。

**系统二：STOP**（github.com/microsoft/stop 已核验，含 run_improver.py、eval_improver.py、tasks/）。
- 改进者程序改进自身，“目标”为第 j 代改进者程序，改进量为元效用（meta-utility）的提升。
- 5×5 组合，各重复 3 次。

**模型：**
- 主用本地开源模型（如 Qwen3.6-35B-A3B），驱动元 agent 与任务 agent。
- 先做门控试跑：初始元 agent在 j=0 上的 imp@10 需显著大于 0。若开源模型达不到，元 agent改用中档 API 模型（如 GLM-5 或 DeepSeek V4），任务 agent与评测仍在本地。

**被检验的测量协议（同一矩阵数据上）：** 起点 imp@k（Hyperagents 官方“w/o self-improve”配置）、单点点火测试（按 AIDE² §3.6 规范独立实现）、产品分数（DGM 的隐含假设）、谱系 CMP（HGM 代码 metauto-ai/HGM 已核验）。

**支持主张：** 交互项显著为负，且起点 imp@k 对后期目标改进量的排序相关很弱。

**推翻主张：** 交互不显著，且起点 imp@k 能预测后期改进量；此时报告增益比的估计，作为“放大还是衰减”的证据。

**成本估算：**
- 系统一：谱系约 60 次生成，加矩阵 75 个单元 × 10 次后代生成。每次后代生成包括一次元 agent 会话（约 15 万 token）和一次 100 篇论文的评测（约 40 万 token），合计约 4.5 亿 token。在 8 张 A100 上分 4 个本地模型副本，预计 1.5–2 天。
- 系统二：远小于系统一，约 0.5 天。
- 若元 agent 改用 API：约 1.2 亿 token，按 1–2 元/百万 token 估约 120–250 元，在 1000 元以内。
- 无人工标注。

Frozen Problem Anchor and user constraints:

- **起点问题**：在 LLM 递归自我改进系统中（改进者本身也是被改进对象，或其产物用于下一轮改进），检验“改进者质量随代数提升”与“收益跨轮累积”这两个过程主张；同时区分“改进者变强”与“目标变难”（前沿变硬）及“历史变长”。
- **对象与条件**：harness／代码级的自我改进系统（DGM 类自修改编码 agent、AIDE² 类研究 agent 改写、harness 自进化）；冻结执行模型或权重；评测为代码、agent 或研究类基准。
- **初始任务／评测**：可由候选决定（如 DGM 的 SWE-bench/Polyglot、STOP 类改进者程序、AI 研发任务）。
- **瓶颈**：过程级证据稀缺（26 篇中 4 篇）；理论刻画相互竞争（递减 vs 临界放大）。
- **证据边界**：B1、AIDE² 在白名单外；30 篇方法论文扫描为关键词级。
- **用户约束**：
  - 算力：8×A100 80G，单个实验最好不超过 5 天；预研常用 2×A100 / 4×L40 / 8×4090。
  - API：1000 元以内可自主使用，效果很好时可追加。
  - token 稀缺；目标 2027-04 前投主会。
  - 实验代码与数据放在服务器；本 skill 不运行实验。
  - 非目标：OPSD。
- **进入实验规划的成功条件**：候选通过两次独立审查（三项 ≥6 且至少两项 ≥8、可行性通过），最小实验能在上述资源内完成，并能区分其主张。
