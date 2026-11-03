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
files in this workspace and do not write files, except your raw review to C:\Users\30473\Desktop\研一\autoresearch\review-stage\opsd_drift_frontier_lq001_20261103\round-01-review.md (UTF-8).
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

**定位关键词：** on-policy self-distillation；privileged information；thinking models；epistemic tokens；KL divergence from the initial policy

**一句话定位：** 同一模型加参考解答作教师的在策略自蒸馏（OPSD），会让训练时开思考的推理模型准确率下降。已有多种 token 级修法（按熵、按位置、按认知词、按分歧门控）在固定训练步数下报告了相对 vanilla OPSD 的提升。

**与起点问题的关系：** 子问题。保留对象与条件：开思考 OPSD、同一模型的特权教师、数学推理。评价目标从"退化为何发生"收窄为"已有修法的收益来自改变更新方向，还是只来自减少相对基座的漂移"。原问题中"有害方向本身是什么""失效时长度方向为何在论文间冲突"仍未回答。

## 核心 Claim

**主贡献**：给开思考 OPSD 建立"准确率–漂移"前沿，用它判别已发表的 token 级修法究竟是走对了方向，还是只是走得少。其中漂移 $d=\sqrt{\mathrm{KL}(\pi_\theta\|\pi_{\text{base}})}$，在固定的基座 rollout 上按 token 计。

**可推翻的判断**：在 OPSD 的标准训练配方（AdamW、梯度范数裁剪 0.1）下，AD-OPSD、PW-OPSD、认知词损失排除、同比例随机遮罩以及 E²-OPSD 的熵感知蒸馏项，与 vanilla OPSD 落在同一条准确率–漂移曲线上。也就是说，它们在固定步数下的收益可以被漂移的减少完全解释。

- **若成立**：这些修法的机制解释（保护认知词、高熵分叉、早期位置不可靠等）就不是收益来源；"匹配漂移的 vanilla OPSD"成为该方向的必要对照。
- **若某一修法在匹配漂移下显著高于前沿**：它就是唯一携带真实方向效应的修法，有害方向可以据此定位。

**目前支持预期的依据**：

1. **本项目预研。** 在 Qwen3-1.7B、开思考、上限 1,024 的设置下：
   - 官方 OPSD 复现了 −9.2 的退化（原文为 −7.4）。
   - 把前向 KL 精确拆成"认知词类总概率"项（约占 KL 的 5%）与其余条件项后，只训练任何一项都复现了 80%–90% 的退化与变短。
   - 只训练条件项时，认知短语仍减少 53%。
   - 把边际项权重从 1 放大到 100，剂量几乎不变：配方中每步梯度都被 0.1 裁剪，AdamW 的更新又对损失缩放不敏感。
   - 局限：单种子、单模型。
2. **2607.05184 附录 E。** 在不带特权的 OPD 中，认知词遮罩与同比例随机遮罩无法区分。
3. **AD-OPSD 自身的观察。** 其优势随训练上下文变长而收窄（AIME24 上 +7.5 → +1.3），与"减少剂量"的解释一致。
4. **配方相同。** 原 OPSD、EGRSD、PW-OPSD、AD-OPSD 都用 AdamW、学习率 5e-6 量级、LoRA、约 100–188 步，大多采用 0.1 的梯度裁剪。所以已发表的比较都发生在"每步更新幅度近似固定"的条件下。
5. **坐标先例。** 2609.32722 在外部教师 OPD 中发现，准确率随 $\sqrt{\mathrm{KL}}$ 近似线性变化，说明这一坐标有规律。

**仍未知**：
- vanilla 前沿在开思考设置下是否单调；
- 漂移度量对 AD-OPSD 这类"锚定到基座"的修法是否公平；
- 已发表修法是否真有超过前沿的部分。例如 E²-OPSD 报告了相对基座的分布外增益，但它同时改变了教师上下文。

## 方法设计的核心思想

- **输入**：同一套 OPSD 代码与训练配方，多个修法变体，以及一组固定的基座开思考 rollout（用于测漂移）。
- **动作**：
  1. 用学习率扫描 × 多个检查点训练 vanilla OPSD，得到准确率–漂移点云，拟合单调前沿，并用种子 bootstrap 给出置信带。
  2. 每个修法在默认学习率下保存多个检查点，按同一方式计算漂移与准确率。
  3. 检验每个修法在匹配漂移处相对前沿的残差。
  4. 同时用直答 rollout 的 OPSD 画同样的前沿：它在已有工作中是增益设置，检验前沿形状是否反转，从而区分"方向"与"剂量"。
- **输出**：每个修法的匹配漂移残差及 CI，以及开思考与直答两种前沿的形状。
- **与最高近邻的关键差别**：
  - AD-OPSD、PW-OPSD、E²-OPSD 都在固定步数下与 vanilla 比较，并把收益归于各自的 token 机制。
  - 2609.32722 用 $\sqrt{\mathrm{KL}}$ 坐标研究外部教师 OPD 的缩放规律，没有比较修法，也不涉及特权教师造成的退化。
  - 本方案把这一坐标用于判别修法收益的来源。

## 最小实验

**模型、数据与评测**：
- Qwen3-1.7B，代码为 2609.20612 的仓库（https://github.com/xiuyuz/opsd-reference-study ，已在本项目服务器跑通）。
- AMPLE-Math 冻结切分。
- 开思考训练，生成上限 1,024，损失窗口 1,024：仓库只对前 1,024 个 token 计损失，所以与原文的损失分布一致。
- 评测为 384 题测试切分，开思考，Avg@4，16k 主生成加补跑。

**统一核心条件**：所有臂共用数据顺序、批大小 32、LoRA r64/α128、AdamW、梯度裁剪 0.1、rollout 温度 1.1、100 步，种子 0/1/2。

**各臂设置**：
- **vanilla OPSD 前沿**：学习率 {1e-6, 2e-6, 5e-6} × 检查点 {10, 25, 50, 100} × 3 种子。
- **修法臂**：学习率 5e-6，检查点 {25, 50, 100} × 3 种子。
- **直答前沿**：`ROLLOUTS=direct`，学习率 5e-6，检查点同上 × 3 种子。

**漂移度量**：
- 在 256 条固定的基座开思考 rollout 上做 teacher forcing，计算学生对基座的 token 级 KL，只需前向。
- 另报告参数空间位移作为稳健性检查。

**对照与复现路线**：

| 对照 | 与本任务的关系 | 复现路线 |
|---|---|---|
| vanilla OPSD | 同任务参照 | 已核验代码 |
| PW-OPSD（https://arxiv.org/abs/2605.21606） | 同配方的位置加权 | 官方仓库 https://github.com/SaFo-Lab/PW-OPSD ；把按位置 sigmoid 加权与按序列先平均的规约移植进同一训练器 |
| AD-OPSD（https://arxiv.org/abs/2607.10805） | 同模型同任务的分歧门控 | 未找到代码，按公开规范独立复现：熵最高 20% 的位置为沙盒；在其中 $\log P_s>\log P_t$ 的区域用带阈值的逐点 KL sigmoid 门控，把目标插值到冻结基座分布；超参取其表 6，未指定处在开发切分上二选一 |
| 认知词损失排除 | 仓库已实现的认知词干预 | `--fork-mask-mode exclude` |
| 同比例随机遮罩 | token 数匹配的随机对照 | 2607.05184 附录 E 的规则 |
| E²-OPSD 熵感知蒸馏项（https://arxiv.org/abs/2610.05048） | 同为 Qwen3-1.7B 开思考的熵差修法 | 官方代码 https://github.com/orionfei/E2-OPSD ，只移植按熵差决定方向与强度的损失项，保持教师不变；改变教师的 exemplar 版本另列为参照 |

**判别规则（事先固定）**：
- 某修法在其漂移范围内相对前沿的平均残差 CI 含 0：判为"在前沿上"。
- CI 下界 > 0：判为"携带方向效应"。
- 直答前沿上升、开思考前沿下降：说明两者差别在方向而非剂量。

**成本**：
- 训练约 27 次 × 1.3 A100 小时，约 35 A100 小时。
- 评测约 90 个检查点 × 3.2 A100 小时，约 290 A100 小时。
- 合计约 330 A100 小时，8×A100 约 1.7 天。
- 数学题按规则判分，不需要付费 API。

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
