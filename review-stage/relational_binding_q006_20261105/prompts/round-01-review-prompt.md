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
Today's date: 2026-11-05. Known tool workarounds: arXiv 摘要与 HTML 正文可用 WebFetch 或 WebSearch 获取；Hugging Face 数据集文件可用 https://huggingface.co/api/datasets/<repo>/tree/main；GitHub API 经代理可能 403，可用 git ls-remote 或 git clone --depth 1
Finish all searches before answering and leave no background tasks running. Do not read other
files in this workspace and do not write files, except your raw review to /home/claude/autoresearch/review-stage/relational_binding_q006_20261105/round-01-review.md (UTF-8).
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
| 有效性 / `effectiveness` | Idea 阶段只评**先验合理性**：方法为什么有望改善目标问题（或现象／视角为什么可靠、有解释力），以及已有证据是否与关键假设相矛盾。**实际效果大小不在此评分**，见下文“待预研”。 | 6：关键假设有具体且适用的机制、理论或邻近证据支持，且未发现与之矛盾的已有证据。8：从动作到预期改善的因果链完整，每个关键假设都有适用依据，主要竞争解释或已知反例已被现有证据排除或明确处理，没有尚未解释的大跳跃。两档都不要求已知收益幅度。 |

**跨领域迁移的新颖度。** 新颖度相对的是目标领域。别的领域已有的方法说明机制来源，不等于目标领域已经有这项工作：
- 经检索确认目标领域还没有这一做法时，迁移本身就是对目标领域的实质新意，新颖度一般不低于 7；
- 能说明朴素迁移在目标领域会遇到什么问题、并给出相应的结构性适配时，可以给到 8 或更高；
- 只有目标领域已有直接近邻时，才按普通增量评判；
- 跨领域来源可以在讨论"机制本身是否原创"时引用，但不能仅因为别的领域有类似思想就压低对目标领域的新颖度。

这是实验前的 Idea 审查，有效性在这里拆成三件事，分开处理：

1. **先验合理性**（计分）：现在有什么依据支持"这个动作有望起作用"，依据适用于哪些条件，迁移成立需要什么关键条件。
2. **已有直接反证**（计分，严重时作为阻断）：近邻的原始数据、受控实验或理论结果与关键假设直接矛盾时，必须指出并扣分；不能因为"还没做预研"而放过。
3. **实际效果大小**（不计分，标注“待预研”）：收益有多大、能否超过强基线多少、覆盖与外推范围，是预研要回答的问题。Reviewer 在审查中把这类未知列为“待预研”，不能因其未知而压低有效性分数，也不能用"效果可能很大"抬高分数。

成功阈值（如“提升10个百分点”）、公平对照、更多种子和完整消融只说明怎样验证，不是方法会有效的依据；修正这些设计不能自动升高有效性分数。其他场景的成功需要说明使其迁移成立的关键条件，不能直接当成当前设置的效果。

诊断或自适应分配方案还需说明：信号为何与所选干预的相对收益有关。能预测错误、难度或漏检，不等于能判断哪一种修法更有效；简单测试上的能力也不自动迁移到依赖结构不同的真实任务。可以保留这类候选送审，但要把缺少依据的迁移环节写成未知，不能仅靠更换监督目标或补上消融就视作效果已获支持。

不要求在本 skill 中运行 pilot，也不能因为尚未正式实验就机械地把有效性封顶为6分；效果大小统一标注为“待预研”，交给后续预研回答。方法可由适用理论、紧邻实验和真实案例支持预期；现象／视角可由已核验的原始观察、竞争解释预测或反例结构支持。新颖且重要、有效性有6分依据的方案仍可按8/7/6这类组合通过。明确区分已有证据、待验证假设和未来成功条件，不冒充已经获得的实验结果。最小实验是否能辨别主张仍须单独判断，设计无法判别时是 Claim 阻断，不能用有效性高分掩盖。

贡献通过条件为：**三项都 ≥6，且按分数排序后，次高一项 ≥7、最高一项 ≥8**（即一项 ≥6、一项 ≥7、一项 ≥8）。例如 8/7/6、6/8/7、9/7/6 可以通过；8/6/6、7/7/7、9/9/5 不通过。不取平均数，也不要求三项都 ≥8。总体 `score` 只记录综合判断与支持候选排序，不另设总体分数门槛，不得覆盖三项判断。

## 可行性独立判断

给出 `feasibility: pass | fail` 和一句具体理由。关键操作须有可信的实现路径，所需数据、模型、工具和预算可获得，最小关键实验能在用户约束下完成。依赖没有依据的新能力、无法得到的资源，或关键步骤明显大概率无法实施的候选，不因新颖或重要而放行。应降低实现难度或重新选择候选，不能为追求高新颖度堆出不可信方案。

效果未知是正常研究风险，不等于实现不可行。Reviewer 应分别判断“这个实验能否做出来”和“它能否有说服力地支持主张”。

## 如何使用这些标准

Improver 先用一句话写清“这项工作成功后，新增了什么值得知道或值得使用的东西”，再据此提出机制、Claim 和最小实验。主 Claim 应表达独立研究贡献，诊断性断言可以支撑它，但可证伪性本身不代表贡献充分。自评记录三项暂定分数、依据和未知部分，用于候选排序；**不要求先自评达到放行门槛才准送审**，不得为了送审抬高分数。主贡献具体、存在可信实现路线且关键实验能判别的候选，即使贡献潜力尚不确定，也可接受独立反馈。只剩诊断种子、明显无独立贡献或无可信实现路径时，先实质改进或停止，不为用满预算反复送审。最终三维硬门槛仅由独立 Reviewer 和正式放行应用。

Reviewer 必须回答：**关键结果若成立，主贡献是什么；现在有哪些依据支持其重要性、新意和效果；实现路径与验证是否可信？** 查新不能代替重要性和有效性判断，理想结果的价值也不能替代效果的当前依据。贡献不足或可行性不通过应写入 `fatal_blockers`，不可给出 `experiment_ready`。

修订可以缩小范围、降低成本或收紧措辞，但每次都须重新判断主贡献。若缩小后只剩一个分量不足的断言，不能凭“更容易验证”通过；补充种子、统计检验或控制变量也不能自动提升主贡献的分量。没有合格候选时继续实质改进或停止，不强行产出 Final Idea。

Independently assess the same main contribution on importance, novelty, and effectiveness,
with evidence-based reasons for each score. Judge feasibility separately. Give one overall
score from 1 to 10 for reference; it cannot override the three-dimensional gate. Explicitly
answer what would become worth knowing or using if the key planned results held. A falsifiable
assertion is not automatically a sufficient contribution. Do not invent positive results.
For effectiveness, score only prior plausibility: the evidence available now, why it applies
to this setting, and whether existing evidence directly contradicts a key assumption (direct
counter-evidence must lower the score and may be a fatal blocker). Do not score the size of
the expected gain: list it under 待预研 (pending pre-study) and neither lower nor raise the
score because it is unknown. A success threshold and a well-controlled future experiment do
not establish plausibility. Do not require a pilot or cap effectiveness mechanically merely
because this is a pre-experiment idea.
For novelty, judge against the target field. A method borrowed from another field counts as
novel for the target field when your own search finds no such work there (normally at least
7); do not lower it merely because a similar idea exists elsewhere.
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
- experiment_ready: all three contribution scores >= 6, and after sorting the middle one >= 7 and the highest >= 8, feasibility pass,
  and no fatal contribution, novelty, feasibility, or claim blocker
- promising_needs_revision: potentially salvageable, but contribution, evidence, novelty, or feasibility needs revision
- needs_rethink: the main contribution is too weak, covered, unsupported, or cannot be tested by the experiment
- reject: not worth further work under the stated constraints

对外只输出下面三个 Markdown 部分，不要给重构方向、修改清单、实验 checklist 或长综述：
## 结论
<用当前日期给出总体 score、verdict；用一句话判断主贡献是什么、是否足够，以及为什么。总体分数不作为额外门槛。>

## Claim 判断
<先用三行短表给出重要性、新颖度、有效性的分数与依据；有效性只评先验合理性：先说明当前依据、迁移条件，以及是否存在与关键假设直接矛盾的已有证据，不能只说“若提高X则8分”；收益大小等效果层面的未知另列一行“待预研”，不计入分数。用一句话说明回答原问题、子问题或邻近新问题及原问题未答部分，不因转向自动否决。另说实验能否判别主张。再给可行性pass/fail、具体实现与预算依据，区分无代码和规范/资源确实不足，核实关键数据可得路线与标签含义。不强制现象类贡献附加修法。>

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

**定位关键词：** GUI grounding；spatial reasoning；GUI-Primitives；hard negatives；ScreenSpot

**一句话定位：** GUI grounding 模型在标准基准上能直接定位被点名的元素，但指令需要关系推理时会大幅崩溃。这类指令如"锚点左边的按钮""列表第三项""某面板里的输入框"，在受控对比集上最强模型只有约三成准确率。

**与起点问题的关系：** 原问题。保留对象（7B 级 GUI grounding 模型）、关系型空间指令和对比评测，回答"崩溃在哪一层"中的一个可检验部分（是否被锚点捕获），以及"什么训练信号能教会关系绑定"。坐标解码层只作为对照，不作主张；遮挡类关系不在主张内。

## 核心 Claim

成功后新增两样东西：

1. **诊断**：GUI 模型在关系指令上的错误，主要是"锚点捕获"，即点到指令里被点名的锚点元素本身，而不是点到关系所指的目标。它的成因是名词与可见文字的匹配压过了关系词。
2. **训练信号**：用"截图与锚点完全相同、只改关系词、目标随之移动"的最小差异对比对训练，可以教会关系绑定；同预算下，普通增广数据做不到。

可推翻的判断：

1. 在 GUI-Primitives 上，对 Qwen2.5-VL-7B、UI-TARS-1.5-7B 和一个 Qwen3-VL-8B 级 GUI 模型，按预测点所落区域分类（锚点、正确目标、对比候选、其他）：落在锚点上的比例显著高于落在对比候选上的比例；且对每个对比对，把关系词换成相反关系后，预测点基本不动（对关系词不敏感）。
2. 只用对比关系对做 SFT（用 GUI 截图与可访问性结构合成，与评测集不重叠）后，在 GUI-Primitives 与 GUI-Perturbed 的关系子集上显著提升。对照是同样本量、同步数、只含"直接点名"指令的增广数据 SFT，后者重现 GUI-Perturbed 报告的不升反降。
3. 收益来自"对比"：把每对中的一半换成随机的另一张截图（破坏最小差异）、样本数不变时，增益显著变小。

推翻条件：若 1 中锚点捕获不占主导，诊断被推翻；若 2 中对比训练不优于增广对照，训练信号主张被推翻；若 3 不成立，收益来自关系数据本身，而不是对比结构。

当前依据：

- **GUI-Primitives**（arXiv:2608.21832；首页未检出白名单机构，作补充证据）
  - 构造：994 个对比指令对，覆盖七种关系；每对固定截图与锚点，只改关系词，目标在两个指定候选之间移动。
  - 结果：19 个模型严格点在框内最高约 32%；Claude Opus 4.7 在清洗核心集上 32.4%，人类 96.9%；Qwen2.5-VL-7B 24.9%。
  - 内容依赖：空白画布使 Qwen2.5-VL-7B 从 22.0% 降到 6.5%，模型依赖真实界面内容。
  - 作者已按预测所在候选区域分类，数据与代码公开。
- **GUI-Perturbed**（arXiv:2604.14262；首页未检出白名单机构）：关系型指令使三个同谱系 7B 模型准确率下降 27–56 个百分点；rank-8 LoRA 加增广数据微调反而退化。数据与微调模型公开。
- **文本匹配主导 GUI 元素定位**：Lexical Coupling in GUI Element Grounding（arXiv:2608.21794）发现，在移动与网页基准上，"高相似度即语义 grounding"常被可见标签的词面恢复所混淆，词面基线在 top-1 上仍有竞争力。这支持"名词匹配压过关系词"的机制。
- **跨领域方法依据**：在图文组合性学习中，用最小差异的困难负例（只改关系或词序）训练，能改善关系与属性绑定，例如 NegCLIP 一类做法。生成式 GUI grounding 上是否同样有效未知。

仍未知：

- 锚点捕获在各关系类型中的占比；
- 合成对比对能否泛化到真实关系指令；
- 对比训练是否损伤常规点名式 grounding（ScreenSpot 上不能下降）。

## 方法设计的核心思想

**输入**：带可访问性树或 DOM 的 GUI 截图（来自公开 grounding 训练集，与 GUI-Primitives、GUI-Perturbed 的截图不重叠）。

**动作**：

1. **诊断**：在 GUI-Primitives 上，把每个预测点归入锚点、目标、对比候选或其他；并在每个对比对内检验"换关系词、预测是否随之移动"。
2. **对比对合成**：从结构中取元素的边框，按规则生成关系三元组（锚点、关系、目标），覆盖左右、上下、包含、对齐、邻近、列表序号。对每个锚点与关系，构造反向关系或相邻序号的配对样本，使截图与锚点相同、目标不同。指令用模板加 LLM 改写。
3. **训练**：在 7B 起点模型上做 SFT，混入等量的原始点名式 grounding 数据，防止常规能力退化。
4. **对照训练**：
   - 同样本数的点名式增广数据，复现 GUI-Perturbed 的设定；
   - 去配对版本：同样的关系样本，但打乱配对，使配对样本来自不同截图。

**输出**：一个关系绑定改善的 grounding 模型；以及锚点捕获在各关系类型上的比例。

**与最高近邻的关键差别**：

- GUI-Primitives 与 GUI-Perturbed 只做评测与现象报告，GUI-Perturbed 的增广训练失败；
- GUI-Cursor 与 zoom 类方法改的是推理过程。

本研究把评测集的对比结构转成训练信号，并用去配对对照检验"对比"本身是否必要。

## 最小实验

**起点模型**：Qwen2.5-VL-7B-Instruct、UI-TARS-1.5-7B（GUI-Perturbed 的同谱系）、一个 Qwen3-VL-8B 级模型。

**训练数据**：从公开 grounding 数据（如 OS-Atlas、Aguvis 或 Click-100k 中带结构的部分）合成约 5 万个对比对，即 10 万条样本；另取等量点名式样本混入。

**评测**：
- GUI-Primitives 全集与清洗核心集，按七种关系报告；
- GUI-Perturbed 的关系子集；
- ScreenSpot-v2 与 ScreenSpot-Pro，检查常规能力不下降。

**对照**：起点模型；点名式增广 SFT（同样本数、同步数）；去配对关系 SFT；GUI-Perturbed 公开的 LoRA 微调 UI-TARS-1.5-7B。

**判定（送审前固定）**：主指标是 GUI-Primitives 核心集严格准确率与"关系敏感率"（换关系词后预测随之移动的比例），按对比对配对 bootstrap。

**成本**：
- 7B 级 SFT，每变体约 10 万样本，8×A100 每个约 6–8 小时；3 个起点 × 3 个变体约 2 天；
- 评测为单卡推理，各约数小时；
- 不需要 API 或 KVM。

Frozen Problem Anchor and user constraints:

- **起点问题**：GUI grounding 模型在标准基准上高分，遇到关系型空间指令时大幅崩溃；需要定位崩溃层级并找到能教会关系绑定的训练信号。
- **初始任务与评测**：GUI-Primitives（七种关系、对比对、点在框内准确率）；GUI-Perturbed；ScreenSpot 系列（检查常规精度不下降）。
- **瓶颈与证据边界**：两份报告都只到现象；GUI-Perturbed 中 rank-8 LoRA + 增广数据反而退化；新一代 GUI 专训模型覆盖不全。
- **用户资源约束**：正式实验 8×A100 80GB，单次最好不超过 5 天；预研 2×A100 / 4×L40 / 8×4090；付费 API 1000 元以内；token 资源稀缺。
- **时间与目标**：自 2026-10 起半年内投出一篇主会论文。
- **非目标**：不做世界模型、视频生成、机器人方向。
- **进入实验规划的成功条件**：独立 Reviewer 两次判定三项都 ≥6 且至少两项 ≥8、可行性 pass、`experiment_ready`、无致命阻断。
