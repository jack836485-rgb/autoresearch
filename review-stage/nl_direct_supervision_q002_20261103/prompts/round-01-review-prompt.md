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
Today's date: 2026-11-03. Known tool workarounds: WebSearch 可用；arxiv.org 的 WebFetch 可能被拦，可改用检索结果摘要或 alphaxiv/HF papers 页面；中文路径需加引号
Finish all searches before answering and leave no background tasks running. Do not read other
files in this workspace and do not write files, except your raw review to C:\Users\30473\Desktop\研一\autoresearch\review-stage\nl_direct_supervision_q002_20261103\round-01-review.md (UTF-8).
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

**定位关键词：** continuous chain-of-thought；direct supervision；multi-token prediction；GSM8k-Aug-NL；sequence-level knowledge distillation；non-autoregressive translation

**一句话定位：** 连续 latent CoT 里有一类直接监督方法（CoLaR、C-MTP），每个 latent 对齐 s 个 token 的压缩表示，可以并行训练。这类方法在冗长的 NL 推理轨迹上相对显式 CoT 微调的保留率，明显低于在结构化算式轨迹上的保留率；间接监督（CODI）则没有这种退化。

**与起点问题的关系：** 原问题。底座（Llama-3.2-1B-Instruct）、数据（GSM8k-Aug 与 GSM8k-Aug-NL，两者来自同一批 GPT-4 轨迹，EQ 版只保留算式）、评测和方法族都不变。C-MTP 作者给出两个未经检验的解释（缺少压缩压力、teacher forcing 误差累积），本方案在此之外提出第三种解释，做判别，并给出修法。

## 核心 Claim

若成立，会得到三样东西：
- 一个机制结论：直接监督在 NL 上退化，主要是因为"块内多个 token 并行预测"遇上了"NL 措辞的多模态"。这是非自回归机器翻译里的老问题，不是链变长带来的误差累积。
- 一个修法：沿用非自回归翻译的标准做法，用 CoT 教师贪心重生成训练轨迹（序列级蒸馏）。它在保持 NL 冗长度的同时降低目标熵，让直接监督在 NL 上回到接近 EQ 的保留率，而且仍可并行训练。
- 一个判据：决定直接监督能否用于某种轨迹的，是目标条件熵，而不是轨迹长度。

可推翻的判断：在长度与熵的 2×2 语料上，长而低熵的轨迹（模板化 NL、教师重生成 NL）让 C-MTP 和 CoLaR 的保留率接近 EQ，且这一收益随块长 s 增大而增大；CODI 基本不变。若模板化 NL 与原 NL 一样差，或者重生成无效，Claim 被推翻。

现有依据：
- C-MTP 公开的表 2 与表 4（Llama-3.2-1B，5 次运行平均）中，GSM8k-Test 上相对同数据 CoT-SFT 的保留率如下：
  - C-MTP 在块长 s=2、3、4 时，EQ 为 86.1%、75.1%、65.7%，NL 为 81.0%、63.4%、47.7%。NL 造成的损失从 5.1 增大到 18.0 个百分点。
  - 同时，NL 上的平均链长从 34 步降到 17 步。链长误差累积的解释预测"链越短损失越小"，观察到的却是反方向。
  - CODI 的保留率 EQ 85.6%、NL 89.1%，不退化。
- C-MTP 附录 A：它的 MTP 头用一个小 MLP，把同一个隐状态投影成 s 个 token 的分布，各 token 条件独立。
- 非自回归翻译中，序列级蒸馏对并行解码器至关重要；Zhou et al.（ICLR 2020）表明它降低了语料的条件熵，提升幅度与模型容量相关。
- PIPO（2605.27255）指出 CoLaR 的单峰高斯不适合多模态的多 token 续写。

未知：
- CoLaR 的 NL 损失不随 s 单调增大（22.9、15.7、14.2 个百分点），可能有地板效应，也可能另有机制。
- 1B 教师重生成的轨迹在训练题上的正确率与覆盖率。
- 把多模态压低后，OOD 泛化（GSM-Hard、SVAMP）是否受损。

## 方法设计的核心思想

**输入：** 训练题与 GPT-4 原 NL 轨迹。

**动作：**
1. 用 NL 数据上训练好的 CoT-SFT 教师，在训练题上贪心解码重生成轨迹，只保留答案正确的，得到"重生成 NL"。
2. 另构造"模板化 NL"：把 EQ 算式套进固定句式，并补到与原 NL 等长，作为"长但低熵"的对照，用来把长度与熵分开。
3. 用一个固定的参考模型测量各语料的逐 token 条件熵；同时测 MTP 头相对自回归教师在同一块上的 NLL 差（块内独立性差距），作为多模态的直接度量。
4. 直接监督方法不改动，只换训练语料。

**输出：** 各方法在 4 种语料上的保留率，以及熵、独立性差距与保留率之间的关系。

**与最高近邻的区别：**
- C-MTP 把 NL 退化归因于压缩压力与误差累积，没有做检验，也没有修法。
- KaVa 改用压缩 KV 蒸馏这条间接监督路线来绕开问题，放弃了直接监督的并行训练。
- 本方案在不改模型的前提下，从数据侧降低目标多模态，并用对照判别原因。

## 最小实验

**底座与配置：** Llama-3.2-1B-Instruct，LoRA，沿用 C-MTP 的设置（github Varun221/cmtp_research，已核验含 `cmtp/scripts/train_cot.sh`、`train_mtp.sh`、`test_mtp.sh` 和 `codi/`）。训练步数、latent 预算与评测都与 C-MTP 一致。

**语料（共 4 种，同一批训练题）：**
- EQ（GSM8k-Aug）
- 原 NL（GSM8k-Aug-NL）
- 模板化 NL（由 EQ 确定性生成）
- 重生成 NL（教师贪心解码，只保留答对的；保留率与覆盖率都会报告）

**方法：** CoT-SFT（分母）、C-MTP-2、C-MTP-4、CoLaR-2（用户服务器上已有 CoLaR 代码，按 C-MTP 设置）、CODI（对照）。每种组合 2 个种子。

**评测：** GSM8k-Test 为主，外推到 GSM-Hard、SVAMP、MultiArith。

**判别：**
- **多模态假说：** 模板化 NL 和重生成 NL 上，直接监督的保留率比原 NL 显著恢复，并且 s=4 的恢复大于 s=2；保留率与块内独立性差距负相关；CODI 变化不超过种子波动。
- **链长或误差累积假说：** 模板化 NL 与原 NL 一样差。另外比较 teacher-forced 与自由展开的差距，看它能否解释损失。
- **压缩压力假说：** 模板化 NL 也会伤害直接监督。

**KaVa：** 只看到其摘要页链接的 R-KV 仓库，没有核实到 KaVa 官方实现。因此只引用它在同一数据上的报告数作为参照，不主张优于 KaVa；本方案的主张限定为"让直接监督在 NL 上恢复"。

**成本：**
- 重生成约 38 万条、每条约 70 token：用 vLLM 跑 1B 模型，单卡数小时。
- 训练约 4 种语料 × 5 种方法 × 2 个种子，但 CODI 只跑原 NL 和重生成 NL 两种语料，合计约 32 个 LoRA run。
- C-MTP 报告其实验在单张 H200 上完成；按每个 run 在 A100 上约半天到一天估算，8 张 A100 上约 3–4 天。
- 不需要 API 和人工标注。

Frozen Problem Anchor and user constraints:

- **起点问题**：直接监督的连续 latent CoT（逐块对齐文本压缩表示，可以并行训练，例如 CoLaR、C-MTP）在冗长 NL 推理轨迹上，相对显式 CoT 的保留率明显低于结构化算式轨迹；同一条件下，间接监督（CODI）不退化。要找出原因，并在保留直接监督并行训练优势的前提下修复它。
- **对象与条件**：Llama-3.2-1B-Instruct 等 1–1.5B 底座；GSM8k-Aug 与 GSM8k-Aug-NL（同源 GPT-4 轨迹，EQ 版只保留算式）；评测 GSM8k-Test，外推到 GSM-Hard、SVAMP、MultiArith。
- **证据边界**：主证据是 C-MTP 的公开表格和用户本地 CoLaR 单 checkpoint；两个作者解释未检验；KaVa 是已有修法，但没有解释成因。
- **用户约束**：正式实验可用 8×A100 80G，单次最好不超过 5 天；token 资源稀缺；付费 API 1000 元以内可自主决定；目标是 2026-10 起半年内投主会。实验代码与数据放在服务器，结果可以回传本地。用户认为"只改进 CoLaR 不足以撑起一篇论文"，希望往 NL 域靠、跨方法验证。
- **非目标**：本 skill 内不启动训练；不把注意力占比当因果证据。
- **成功条件**：得到经双审通过的 Idea，交付 `EXPERIMENT_HANDOFF.md`。
