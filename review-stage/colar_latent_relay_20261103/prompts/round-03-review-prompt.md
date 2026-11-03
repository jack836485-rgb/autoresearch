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
files in this workspace and do not write files, except your raw review to C:\Users\30473\Desktop\研一\autoresearch\review-stage\colar_latent_relay_20261103\round-03-review.md (UTF-8).
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

**定位关键词：** continuous chain-of-thought；latent reasoning；GSM8k-Aug-NL；MATH；CODI；SIM-CoT

**一句话定位：** 连续 latent CoT 研究中，C-MTP（arXiv 2607.16972，ICML 2026）报告了一个现象：直接监督和间接监督方法在结构化或半自然的推理轨迹上（GSM8K，约 25–62 token）接近显式 CoT 微调，但在真实轨迹上（MATH，由被训练的模型自己生成，约 350 token）只剩 CoT-SFT 的约 30–35%。这个崩塌的原因目前没有被解释。

**与起点问题的关系：** 邻近新问题。起点是在 CoLaR 上观察到的现象：算式版和自然语言版的 GSM8K-Aug 上，latent 生成都只看最近 2–3 个 latent，答案也读链尾。这里把该近窗现象作为四个竞争解释之一来检验，研究目标改为"解释 latent CoT 为何离不开结构化轨迹"。起点中"链尾集中来自版式还是来自机制"这一问题，这里不直接回答。

## 核心 Claim

若成立，这项工作的贡献是一个经过控制的因素分解：在同一批题上，把 latent CoT 相对 CoT-SFT 的崩塌分到四个因素：
- 轨迹冗长度（内容不变）
- 题目难度
- 自回归 latent 展开的误差累积
- 较早的中间信息因近窗而丢失

分解按方法家族（直接监督 / 间接监督 / 逐步重建）分别给出主导因素，并用主导因素推出的最便宜修法做一次干预检验。它要回答的是一个已被报告、却被混杂的判断，即"结构化 benchmark 高估了 latent CoT"：失败究竟出在 latent 方法处理不了自然语言轨迹，还是出在题目更难。答案决定领域下一步该做的是轨迹凝练、展开训练，还是状态监督。

**可推翻的主假说：** 在内容等价的条件下，冗长度是主导因素。在同一批 MATH 题上，把真实轨迹凝练为紧凑步骤后，latent 方法相对 CoT-SFT 的保留率应大幅回升；把 GSM8K 轨迹扩写成真实风格后，保留率应明显下降。若保留率主要随题目来源变化，而不随冗长度变化，主假说被推翻，"难度主导"成立。

**目前的依据：**
- C-MTP 的对比同时改变了轨迹形式和题目来源（GSM8K 对 MATH），所以 65% 的崩塌既可能来自冗长，也可能来自难度。这一点读原文设置即可确认。
- 在用户训练的 CoLaR（Llama-3.2-1B，压缩因子 5）上，同一批 500 道 GSM8K 测试题、同一架构，用自然语言版轨迹（平均约 55 token）训练的正确率为 18.4%，用算式版训练的为 28.6%，说明内容相同时冗长度本身有害。这只是单 checkpoint、单方法的结果，也可能有训练充分度的差异。
- C-MTP 自己观察到，间接监督因为不必表示每个 token，更适合冗长轨迹。
- 在显式 CoT 中，删除约 80% 的低熵步骤不掉点（arXiv 2508.03346），说明真实轨迹的信息冗余很大。
- 近窗与误差累积两项目前只有间接依据：CoLaR 上近窗注意力占比 72–80%，链尾联合置零就崩；C-MTP 附录中有误差累积的个例。

**未知：** LLM 重写能否严格保住内容；各因素之间是否有交互；1B 级模型在 MATH 上的地板效应。

## 方法设计的核心思想

**输入：** 同一批训练题和源轨迹。
- MATH：沿用 C-MTP 的真实轨迹，由被训练的底座模型自己生成。
- GSM8K：使用 GSM8K-Aug 与 GSM8k-Aug-NL。

**动作：**

1. **构造内容等价的冗长度阶梯。** 用 LLM 把每条源轨迹重写成三档：
   - 紧凑算式步（类似 GSM8K-Aug）
   - 每步一句（类似 GSM8k-Aug-NL）
   - 真实风格（MATH 用原轨迹，GSM8K 扩写）

   自动校验每档都保留源轨迹的全部中间数值和最终答案，不合格就丢弃。各档上 CoT-SFT 的准确率作为内容保真对照：CoT-SFT 在三档上应基本持平。

2. **2（题目来源）× 3（冗长度）网格。** 在每个格子上训练 CoT-SFT、C-MTP、CODI、SIM-CoT，主指标是"相对同格 CoT-SFT 的保留率"。

3. **另外两个因素的测量。**
   - 误差累积：比较 teacher-forced 与自由展开的差距。对直接监督方法，把 gold 压缩目标喂作历史 latent。
   - 近窗丢失：推理时把注意力限制在"题目 + 最近 W 个 latent"，看保留曲线；再用线性探针测较早中间量能否从近窗读出。两者只作辅助证据。

4. **修法干预检验。** 按分解得到的主导因素做一次最便宜的修法。例如冗长度主导时，"先凝练、再 latent 化"：在凝练轨迹上训练 latent，在 MATH 测试集上与直接用真实轨迹训练的结果比较。

**输出：** 各方法家族的因素分解表，以及一次修法验证。

**与最高近邻 C-MTP 的差别：** C-MTP 报告了崩塌，但其对比混入了题目来源，也没有区分原因。本方案在同题上用内容等价的阶梯，把冗长度和难度拆开，并把误差累积与近窗丢失作为竞争解释一并测量。

## 最小实验

**底座：** Qwen2.5-1.5B-Instruct 为主（MATH 上 CoT-SFT 水平较高，可减轻地板效应），Llama-3.2-1B-Instruct 作复核。两者都是 C-MTP 使用的底座，LoRA 设置也沿用 C-MTP。

**代码：**
- C-MTP 仓库（github Varun221/cmtp_research，已核验含 `cmtp/train.py`、`cmtp/test_cot.py`、`codi/`、`data_math/` 的轨迹生成与评分脚本）提供 CoT-SFT、C-MTP、CODI 的实现和 MATH 管线。
- SIM-CoT 用官方实现（github InternLM/SIM-CoT，ICLR 2026）。

**数据与重写：**
- MATH：7.5k 训练题，测试用 MATH-500。
- GSM8K：取 7.5k 道训练题的子集，测试用全部 1319 题。
- 两边训练题数相同，避免数据量差异。
- 重写用 API，约 1.5 万条 × 3 档，预计少于 300 元。重写丢弃率与抽检 200 条的人工核对结果一并报告。

**规模：** 6 个格子 × 4 种方法 × 2 个种子，约 48 个 LoRA run。每个 run 的训练集只有 7.5k 题，在单卡 A100 上数小时，在 8 张 A100 上约 2–3 天。另加修法干预检验 2–4 个 run。

**判别：**
- 若冗长度主导：同一题源下，保留率随冗长度单调下降，并且降幅大于同一冗长度下 GSM8K 与 MATH 之间的差；"先凝练、再 latent 化"在 MATH 测试集上的保留率显著高于用真实轨迹训练。
- 若难度主导：保留率随题源变化，而在冗长度上基本持平。
- 若误差累积主导：teacher-forced 与自由展开的差距随冗长度增大，并能解释大部分保留率损失。
- 结果按方法家族分别报告。不论哪种结果，都会推翻至少一种当前的领域解释。

Frozen Problem Anchor and user constraints:

- **起点问题**：连续 latent CoT（以 CoLaR 为主）在 GSM8K 类数学应用题上，信息为何集中在链尾、生成为何近似只看最近 2–3 个 latent；这是 latent 推理特有的"接力式循环状态"机制，还是对监督 CoT 文本版式与局部依赖的继承？它对 latent CoT 的失败、方法设计或解释研究意味着什么？
- **对象与条件**：CoLaR（Llama-3.2-1B-Instruct，CF5，GSM8K-Aug 算式版与 NL 版）；可对照的 Coconut、CODI 等 latent CoT 家族；同底座显式 CoT。初始评测为 GSM8K 测试集（含 GSM-Hard、SVAMP、MultiArith 作外推）。
- **瓶颈与证据边界**：现有证据为单 checkpoint、单随机链、注意力描述加置零干预；EQ 与 NL 共享架构与数据来源，不能当成两个独立方法家族；置零是离流形干预；EQ checkpoint 是用户改进版而非官方权重。
- **用户约束**：预研可用 2×A100 80G / 4×L40 48G / 8×4090 24G；正式实验可用 8×A100 80G，单次最好不超过 5 天；token 资源稀缺；付费 API 1000 元以内可自主决定；目标是 2026-10 起半年内投主会。实验代码与数据放服务器，结果可回传本地。
- **非目标**：本 skill 内不启动训练或新的 GPU 干预；不把注意力占比直接当因果贡献；不把 NL/EQ 差异直接当数据形式的因果效应。
- **实验规划的成功条件**：得到一个经双审通过、主贡献明确、最小实验能判别 Claim 的 Idea，并交付 `EXPERIMENT_HANDOFF.md`。
