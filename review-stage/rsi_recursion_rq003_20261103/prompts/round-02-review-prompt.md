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
Today's date: 2026-11-03. Known tool workarounds: huggingface.co 本地直连超时，可用 hf-mirror.com；raw.githubusercontent.com 可能超时，可用 api.github.com contents 接口；arXiv 2603.19461 无 HTML 版本，可读 PDF（arxiv.org/pdf/2603.19461）
Finish all searches before answering and leave no background tasks running. Do not read other
files in this workspace and do not write files, except your raw review to C:\Users\30473\Desktop\研一\autoresearch\review-stage\rsi_recursion_rq003_20261103\round-02-review.md (UTF-8).
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

**定位关键词：** hyperagents；improvement@k（imp@k）；metacognitive self-modification；recursive self-improvement；transfer of meta-level improvements

**一句话定位：** 在自指式自我改进系统中，“系统提升了自身的改进能力”最常被引用的受控证据来自 Hyperagents/DGM-H：迁移来的元 agent 在新领域 imp@50=0.63，初始元 agent 约为 0。但这一测量的起点，是一个因缺少任务特定解析而得 0 分的任务 agent。这份优势究竟是可迁移的改进技能，还是“知道要加解析和后处理”这类通用修复，尚未被分离。

**与起点问题的关系：** 原问题。保留“同起点、同预算比较不同代改进者”的条件；把目标从单一失败起点扩展到“去掉接口失败的起点”和“已有能力的目标”，并加入记忆剥离对照。“跨轮累积”与“递归是在放大还是衰减”不在本工作内。

## 核心 Claim

**主贡献（若成立）：** 一个可推翻的发现，回答“自指改进者到底学会了什么”。

- **若成立：** 迁移元 agent 的优势在去掉接口失败后大幅缩小，在有能力的目标上消失或接近消失。这说明当前“改进能力提升”的主要实证，来自可迁移的通用接口修复知识，而非在有能力的目标上找到改进的本事；RSI 的过程主张需要在有能力的起点上重新评估。
- **若不成立：** 优势在有能力的目标上保留，且剥离持久记忆后不消失。这将是第一份不依赖接口失败的“元层面改进可迁移”证据。

两种结果都会改变对“当前系统是否提升了改进能力”的判断。

**方法副产品：**
- 在同一目标上配对比较改进者的协议。比较在同一量表、同一起点上进行，不需要跨目标比较增益幅度。
- 记忆剥离对照，用来区分谱系记忆回放与通用技能。

**目前支持预期的依据（均来自 Hyperagents 原文，arXiv:2603.19461，本轮读取 PDF 核实）：**
- 原文明确写道：IMO 评分与论文评审领域的初始 agent 得 0.0，是因为“没有任务特定的解析或后处理”，这是接口失败，不代表底座模型不会做这个任务；原文还说早期改进部分在于学会任务格式。
- 初始元 agent 在 50 轮内 imp@50≈0，即没能修好这个接口。迁移元 agent达到 0.630。
- 成分消融（Appendix D.5）显示，只迁移元 agent 就能恢复几乎全部收益（0.620 vs 0.630）。这与“元 agent 携带了修复知识”相容，但不能区分修复知识与一般改进技能。
- 另一项独立工作（arXiv:2610.27610）在理论上指出：过程主张必须用离对角的交换测试来检验，并在一组声明的起点上平均；但它没有做实验。

**未知：**
- 去掉接口失败之后，M_T 与 M0 的差距还剩多少；
- 换成较便宜的底座模型后，迁移元 agent的优势是否保持。

## 方法设计的核心思想

**输入：**
- 初始元 agent M0（官方代码）；
- 迁移元 agent M_T（官方实验日志中按原文 D.4 规则选出的迁移 hyperagent 的元 agent 部分；若日志不含，则用官方代码在 paper review 与 robotics 上重跑一次得到）；
- 三组目标任务 agent。

**动作：** 在原文的迁移领域（IMO 评分）上，用官方“DGM-H w/o self-improve”配置，让冻结的改进者在每个目标上生成至多 k 个后代，按原文 D.3 计算 imp@k。三组目标如下：

| 组 | 目标 | 作用 |
|---|---|---|
| A | 原始失败起点 | 复现原结果 |
| A' | 同一起点 + 一段与任务无关的最小解析（只把模型输出规整成要求的字段，不含评分知识） | 去掉接口失败 |
| B | 4 个有能力的目标：由 M0 在 A' 上运行得到的谱系，按测试分分层选取 | 检验“有能力的目标上是否仍有优势” |

此外，M_T 增设“剥离持久记忆文件、代码不变”的变体 M_T−mem。

**输出：** 每个目标上 imp@k(M_T) − imp@k(M0) 与 imp@k(M_T−mem) − imp@k(M0) 的配对差及置信区间，以及差值随目标组（A → A' → B）的变化。

**与最高近邻的关键差别：**
- Hyperagents 只在接口失败的起点上测；
- AIDE² 的点火测试只在一个后期目标上比较两个改进者，且结论不确定；
- 2610.27610 只给出理论框架，没有做实验；
- 本方案专门把“接口修复”“谱系记忆”与“可迁移技能”三者分开。

## 最小实验

**模型：** 元 agent 与任务 agent 用同一个中档底座模型。它通过官方 litellm 接口调用（例如一个低价 API 模型），所有改进者共用，因此差异只来自元 agent 的代码与记忆。原文用的是更强的模型，这一点作为外推边界说明。

**规模：**
- 目标：A 1 个、A' 1 个、B 4 个，共 6 个；
- 改进者：M0、M_T、M_T−mem，共 3 个；
- 每个组合重复 2 次，k=10。原文 k=50；先做 A 组复现，确认 k=10 时 M_T 与 M0 已能拉开差距。

**数据：**
- IMO-GradingBench 的训练／验证／测试划分沿用官方 domains/imo。
- 官方实验日志在 README 第 69–71 行（Google Drive），需核对其中是否包含迁移 hyperagent 的代码与记忆文件；服务器访问 Drive 可能需要代理。

**支持主张：** A 组差值大（复现原结果），A' 与 B 组差值显著缩小。

**推翻主张：** B 组差值与 A 组相当，且剥离记忆后不变。此时报告“元层面改进可迁移”的更强证据。

**成本估算：**
- 共 36 次运行 × 10 次后代生成 = 360 次元 agent 会话。按原文每次自修改约 33 万 token 计，约 1.2 亿 token；按低价 API 1–2 元/百万 token 估约 120–250 元。
- 任务 agent 评测在本地开源模型上运行，或者走同一 API。IMO 评分测试集每次评测约 0.5M token，360 次约 1.8 亿 token；走 API 则再加约 180–360 元，合计在 1000 元以内。
- 若需要重跑得到 M_T：两个领域各 100 轮，另加约 300–500 元，可能超出 1000 元。
- 本地 GPU 只用于可选的本地评测。无人工标注。

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
