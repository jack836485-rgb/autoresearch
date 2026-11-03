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
Today's date: 2026-11-03. Known tool workarounds: arxiv.org 需经本机代理 127.0.0.1:7891 访问（curl -x）；WebFetch 无法访问 arxiv.org
Finish all searches before answering and leave no background tasks running. Do not read other
files in this workspace and do not write files, except your raw review to C:\Users\30473\Desktop\研一\autoresearch\review-stage\opsd_drift_frontier_lq001_20261103\round-02-review.md (UTF-8).
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

**定位关键词：** on-policy self-distillation；privileged information；thinking models；budget forcing；end-of-thinking token / termination

**一句话定位：** 同一模型加参考解答作教师的在策略自蒸馏（OPSD），会让训练时开思考的推理模型在长评测预算下准确率下降、回复变短。已有修法把它归因于认知词抑制或高熵分叉，没有区分"学会了过早结束思考"与"推理能力本身下降"。

**与起点问题的关系：** 原问题。保留全部对象与条件：开思考 OPSD、同一模型的特权教师、数学推理、长评测预算。直接回答"退化来自哪里"与"失效时长度方向由什么决定"。外推到非数学任务与异族教师不在本次范围内。

## 核心 Claim

**主贡献**：把开思考 OPSD 的长预算损失分解成"终止策略被改变"与"推理质量下降"两部分。若前者为主，给出只在终止决策上把教师信号锚定回学生自身的 OPSD：它应保住 OPSD 的短预算增益，同时去掉长预算损失，在全部评测预算上不低于 vanilla OPSD 与基座。

**可推翻的判断**：
1. **推理期判别。** 推理时在 `</think>` 处强制续写，直到达到基座在同题上的长度。这一操作给 OPSD 学生带来的提升，至少消掉其长预算损失的一半，而且显著大于同一操作对基座本身的提升（差中差）。
2. **训练期判别。** 终止锚定 OPSD 的做法是：终止类 token 的总概率不向教师学，类内与类外的条件分布照常蒸馏。在 32k 预算下，它不低于基座（等价界内），同时保持 vanilla OPSD 在 4k/8k 预算下的大部分增益。
3. **长度方向。** 不同教师上下文在初始化时"教师终止概率 − 学生终止概率"的符号，预测训练后回复长度变化的方向。

反过来，如果强制续写救不回来、终止锚定也不能消除长预算损失，那就第一次干净地支持了"推理能力受损"这一解释。

**目前支持预期的依据**：

1. **本项目预研**：Qwen3-1.7B，2609.20612 的代码与数据，开思考训练上限 1,024，100 步，单种子，384 题 × 2 样本，按仓库保存的前缀截断判分。

   | 臂 | 4k | 8k | 16k | 完整预算 | 16k 内结束比例 |
   |---|---|---|---|---|---|
   | 基座 | 22.8 | 51.7 | 73.7 | 81.2 | 90% |
   | 未截断前向 KL 的 OPSD | 48.2 | 62.4 | 66.9 | 66.9 | 99.9% |

   - 两条曲线在 8k 到 16k 之间交叉，基座从 16k 到完整预算还能再涨 7.5 分。
   - 4k 内已结束的回复，两者正确率相近（83.7 对 87.9）。
   - 另外 4 个 OPSD 变体呈现同样模式，包括只训练认知词类边际项或只训练条件项的臂。这说明"按 token 类别拆信号"并不改变这一模式。

2. **2607.05184**：在 5 个思考模型上观察到 4k–8k 预算持平或更好、32k–38k 更差且更短，并指出学生学到了更短的回复，却没有学到教师的 pass@k。
3. **s1（2501.19393）**：在 `</think>` 处强制续写，能提升推理模型的长预算准确率。这说明推理期干预可以改变"何时停"而不改权重。
4. **2609.37326**：在外部教师 OPD 中，"会解题"与"知道何时停"是分开传递的两种能力，那里的学生是停不下来，方向相反。
5. **2609.20511**：在 OPD 中，长度异常可以由终止 token 的不匹配主导。

**仍未知**：
- OPSD 学生是否已经失去长程核对能力，以致续写也无用；
- 终止行为是否主要由收尾短语（多 token）而不只是 `</think>` 承载，这会决定锚定类的范围；
- 锚定后，短预算增益是否随"压缩"一起消失。

## 方法设计的核心思想

**推理期判别**：
- 对 OPSD 学生与基座分别生成。
- 学生生成 `</think>` 时，如果当前长度小于目标长度（基座在同一题、同一种子下的长度），就把 `</think>` 换成一个中性续写提示继续生成；"Wait" 提示作为另一条件。
- 计算两者在完整预算下的提升之差。

**终止锚定 OPSD**：
- 记终止类 $S$ 为 `</think>` 与 EOS。收尾短语的首 token 在初始学生 rollout 中统计 `</think>` 前的高频片段后固定，作为扩展版。
- 每个位置上，教师给 $S$ 的总概率替换为学生自身的值（当作常数）；$S$ 内与 $S$ 外的条件分布仍用教师的。
- 这等价于在前向 KL 的精确分解 $\mathrm{KL}=L_{\text{marg}}(S)+L_{\text{cond}}(S)$ 中只训练 $L_{\text{cond}}$。代码在预研中已实现，并通过了恒等式单测。

**长度方向**：在固定的基座 rollout 上，对每种教师上下文计算位置平均的终止概率差。

**与最高近邻的关键差别**：
- AD-OPSD、PW-OPSD、E²-OPSD、ST-OPSD 都修改认知词、高熵、位置或教师激活上的信号，没有单独处理终止决策，也没有在推理期分解损失来源。
- 2609.20511 处理的是外部教师 OPD 中的 EOS 不匹配，即长度膨胀。
- 2609.37326 只做诊断，而且是外部教师。

## 最小实验

**模型与数据**：
- Qwen3-1.7B，2609.20612 的代码（https://github.com/xiuyuz/opsd-reference-study ，已在本项目跑通）与 AMPLE-Math 冻结切分。
- 开思考训练，上限 1,024；仓库只对前 1,024 个 token 计损失，与原文损失分布一致。

**统一核心条件**：AdamW、学习率 5e-6、梯度裁剪 0.1、批大小 32、100 步、LoRA r64/α128、种子 0/1/2。

**评测**：
- 384 题测试切分，开思考，Avg@4，主生成 16k、补跑到 32k；报告 4k/8k/16k/32k 各预算点。
- 外部基准 AIME24/25 只作描述。

**训练臂（各 3 种子）**：
- vanilla OPSD；
- 终止锚定 OPSD（只含 `</think>`/EOS）；
- 终止锚定 OPSD（加收尾短语首 token）；
- AD-OPSD；
- PW-OPSD。

**推理期臂**：vanilla OPSD 学生与基座 × {无干预, 中性续写, "Wait" 续写}，目标长度取基座同题长度。

**长度方向**：教师上下文 {完整轨迹, 只给答案, 他题解答} 的初始终止概率差，对比 2609.20612/2609.39118 已报告的长度方向，并用 vanilla 训练做种子 0 的验证。

**对照的复现路线**：

| 对照 | 与本任务的关系 | 复现路线 |
|---|---|---|
| vanilla OPSD | 同任务参照 | 已核验代码 |
| AD-OPSD（https://arxiv.org/abs/2607.10805） | 同模型同任务、针对思考坍缩 | 无代码，按公开规范独立复现：熵最高 20% 的位置为沙盒，其中 $\log P_s>\log P_t$ 区域用带阈值的逐点 KL sigmoid 门控，把目标插值到冻结基座；超参取其表 6 |
| PW-OPSD（https://arxiv.org/abs/2605.21606） | 同配方的位置加权 | 官方仓库 https://github.com/SaFo-Lab/PW-OPSD 已核验，移植按位置 sigmoid 加权 |
| s1 budget forcing（https://arxiv.org/abs/2501.19393） | 推理期延长思考的标准做法 | 规则明确：替换 `</think>` 为续写提示，在 vLLM 生成循环中实现 |

**判别规则（事先固定，含等价界）**：
- 等价界取 2 分。按预研的单检查点方差估计功效；不足时种子加到 5 个。
- 推理期主指标：差中差的 95% CI 下界 > 0，且学生被消掉的损失比例 ≥ 0.5。
- 训练期主指标：终止锚定 OPSD 在 32k 下相对基座的差落在 ±2 分内，且 4k 增益 ≥ vanilla 的一半。

**成本**：
- 训练 15 次 × 1.3 A100 小时，约 20 A100 小时。
- 评测 16 个单元 × 3.2，约 50 A100 小时。
- 强制续写约 40 A100 小时，初始终止概率只需前向，约 5 A100 小时。
- 合计约 120 A100 小时，8×A100 不到 1 天，不需要付费 API。

Frozen Problem Anchor and user constraints:

- **起点问题**：同一模型加特权上下文的 OPSD，在训练时开思考的推理模型上，为什么让准确率下降、长度发生变化；以及现有修法是否处理了真正的原因。
- **对象与条件**：
  - 数学推理；
  - ≤8B 的思考模型（Qwen3 系为主）；
  - 学生开思考生成 rollout；
  - 教师为冻结的同一模型加参考解答；
  - 前向 KL/JSD 损失。
- **初始任务与评测**：
  - AMPLE-Math 冻结切分（2609.20612）或 OpenThoughts-Math；
  - AIME24/25、HMMT25 等。
- **瓶颈与证据边界**：
  - 现有机制解释（认知抑制、高熵分叉）都没有在 OPSD 损失通道上被因果确立；
  - 多数证据为单种子、小模型；
  - 预研显示单项损失都能复现退化，但只有单种子。
- **用户约束**：
  - 预研 2×A100 80G，只回答 go/no-go；
  - 正式实验最多 8×A100、最好不超过 5 天；
  - 付费 API 1000 元以内可自主决定；
  - token 资源稀缺；
  - 目标为自 2026-10 起半年内投主会。
- **非目标**：
  - 预训练；
  - 大于 8B 的模型；
  - 非数学任务的完整覆盖。
- **进入实验规划的成功条件**：候选在独立审查中满足贡献门槛（三项 ≥6、至少两项 ≥8）且可行性通过，最小关键实验能在上述算力内完成。
