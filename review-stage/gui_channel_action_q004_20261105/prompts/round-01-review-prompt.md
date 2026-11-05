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
Today's date: 2026-11-05. Known tool workarounds: arXiv 摘要与 HTML 正文可用 WebFetch 或 WebSearch 获取；arxiv.org 偶有限流，可稍后重试；GitHub API 经代理可能返回 403，可用 WebSearch 或 WebFetch 仓库页面
Finish all searches before answering and leave no background tasks running. Do not read other
files in this workspace and do not write files, except your raw review to /home/claude/autoresearch/review-stage/gui_channel_action_q004_20261105/round-01-review.md (UTF-8).
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

**定位关键词：** GUI grounding；accessibility tree / DOM；action space；prompt injection；Multimodal-Mind2Web

**一句话定位：** 同时读截图与结构化序列（DOM / a11y 树）的多模态 GUI 智能体，在两通道不一致时跟随哪一方主要由动作输出格式决定：输出结构引用（元素 id、索引、文本标签）时定位准，但会继承结构中的过期、无视觉表示或被注入的断言；输出屏幕坐标时抗结构劫持，但无冲突时自身定位错误高。

**与起点问题的关系：** 原问题；保留对象（截图 + 结构双通道 GUI 智能体）、冲突类型（结构与像素不一致）与评测（结构跟随率、无冲突错误、实景任务），直接回答"能否同时获得两者的优点"，并以格式配比与独立性约束的消融部分回答"训练如何塑造通道偏好"；时间维度上的状态过期不在范围内。

## 核心 Claim

成功后新增一种可直接使用的动作接口与训练方法：同一模型一次输出一个结构引用和一个屏幕坐标，训练时约束坐标只能由像素决定，执行时两者一致则按结构元素执行、不一致则以像素读数为准。它让一个模型在无冲突时得到结构动作的定位精度，在冲突时得到坐标动作的抗劫持能力，且不需要额外的模型调用。

可推翻的判断：在同一底座、同一训练数据下，(1) 双钥模型的无冲突错误接近只训 index 的模型，显著低于只训坐标的模型；(2) 冲突下的结构跟随率接近只训坐标的模型，显著低于只训 index 的模型；(3) 去掉独立性约束（结构里保留几何字段、不做冲突增广）后，坐标读数的结构跟随率上升，双钥的冲突鲁棒性随之消失，说明收益来自读数独立而非多输出一个字段；(4) 在相同或更低调用开销下，冲突鲁棒性不低于、无冲突精度高于训练无关一致性门控。若 (1)(2) 不能同时成立，取舍没有被打破；若 (3) 不成立，独立性约束不是必要成分。

当前依据：
- 2607.04334（HKUST、深圳大学）在同一 Qwen2.5-VL-7B 上只换动作格式，冲突下结构跟随率为坐标 0.11、element id 0.64、index 0.90、文本标签 0.98，OS-Atlas-Base-7B 上排序复现；输出坐标的 UGround、Aguvis 结构跟随仅 0.02–0.07。这说明同一模型在坐标格式下的读数在冲突中基本不随结构变化，是"两种读数误差近似独立"的直接证据，而冗余读数的交叉校验成立正需要这一条件。
- 同一对照中坐标格式无冲突错误 0.43，是本方案的主要风险：若一致性检查在无冲突时频繁误报并回落到坐标，精度会被拉回坐标水平。尚不知道这 0.43 中有多少是落在目标附近或相邻元素（执行规则可通过"以坐标所在的结构元素为准"吸收），有多少是选错了目标。
- 2607.04334 的训练无关门控（对候选元素放大裁剪问"这些像素是否显示目标标签"，否则逐元素扫描重新 grounding）在 web 上把文本替换的动作错误降低 24–44 点，并把过期节点的结构跟随从 0.69–0.95 降到 ≤0.07；但作者指出其上限是同一模型的裁剪自读，在密集 AndroidWorld 屏幕上只能部分修复，且每个候选需额外一次裁剪查询。
- 自然冲突并不罕见：该文引用 CLAY 标注，10.6% 的 RICO 结构节点没有有效视觉表示，37.4% 的屏幕出现此类节点。

仍未知：联合训练两种输出是否会让坐标开始复制结构中的几何或文本（独立性被破坏）；独立性约束（去掉几何字段、冲突增广）是否会降低正常任务精度；方法在多步实景任务中的收益大小。

## 方法设计的核心思想

输入：截图 + 结构化序列（去掉 bbox / bounds 等几何字段），任务指令与历史。

动作：
1. 输出格式：`act(op, ref=<结构元素 id>, at=(x, y), value)`，同一次解码先输出 ref 再输出坐标或反之（顺序作为消融）。
2. 训练数据：Multimodal-Mind2Web 与 AndroidControl 的单步样本，ref 标签为目标元素 id，坐标标签为目标元素可见区域内一点；序列化结构时删除所有几何字段，使坐标无法从结构中复制。
3. 冲突增广：对一部分样本按 2607.04334 的规范编辑结构（改目标或干扰节点的文本、插入无视觉表示的节点），标签按像素真相给出：坐标仍指向像素中的真实目标，ref 指向其 bbox 包含真实目标的元素（若被删则为空）。
4. 执行规则：若坐标落在 ref 元素的渲染框内（框以执行时的实际渲染为准，带小边距），点击该元素中心；否则以坐标为准，并吸附到包含该坐标的结构元素（无则直接点击坐标）。
5. 无额外调用；一致性检查是确定性几何判断。

输出：执行的动作，以及每步"一致 / 不一致"的标记（可作为冲突检测信号）。

与最高近邻的关键差别：2607.04334 的门控是推理时用同一模型对裁剪区域做二次读取，需要额外查询且上限受同一模型裁剪自读限制；本方法把校验变成训练出的两个独立读数之间的确定性几何比较，并把独立性作为训练约束。ECA（2605.19192）用外部 DOM/OCR/AX 验证器为动作谓词出具证书，验证器本身读结构或 OCR；本方法不引入外部验证器，校验的两端分别来自像素通道与结构通道。

## 最小实验

**模型与数据：** Qwen2.5-VL-7B-Instruct（2607.04334 的主模型）。训练集用 Multimodal-Mind2Web 训练划分（已用 HF datasets-server 读取首行核验，含 `screenshot`、带 `backend_node_id` 的 `cleaned_html`、带 `bounding_box_rect` 的正负候选、`operation`、`confirmed_task`）与 AndroidControl（截图 + a11y 树，字段尚未核验）。评测用 Multimodal-Mind2Web 跨任务/跨网站/跨领域测试划分的单步准确率，以及按 2607.04334 公开规范重建的冲突探针：文本替换、无视觉表示节点、截图替换与重渲染对照，web 与移动端各约 150 个，强制选择评分，不用模型 judge。该文称代码随论文发布，本轮未找到链接，因此按规范独立重建，标明为独立复现。

**对照（同底座、同训练数据与步数、同评测）：**
- 只训坐标；只训 index；混合两种格式但无独立性约束（结构保留几何字段、无冲突增广）；
- 坐标 + 吸附（只用坐标头，执行时吸附到包含它的结构元素）——检验结构引用头是否必要；
- 训练无关一致性门控：在只训 index 的模型上按 2607.04334 正文规范独立实现（放大候选裁剪 yes/no，否则逐元素扫描），记录额外调用数；
- 消融：只去几何字段 / 只做冲突增广。

**指标：** 冲突探针上的结构跟随率与正确率；无冲突单步元素准确率与坐标落点准确率；不一致率在无冲突与有冲突样本上的分布（误报与检出）；每步模型调用数。

**支持/推翻主贡献的结果：** 支持：双钥在无冲突准确率上与只训 index 的差距在 2 个百分点内，同时冲突下结构跟随率与只训坐标的差距在 0.05 内，且优于门控或在门控同等鲁棒时少用额外调用；去掉独立性约束后坐标的结构跟随明显上升。推翻：任一端明显落后（例如无冲突准确率回落到坐标水平，或冲突下结构跟随接近 index），或"坐标 + 吸附"已达到同样效果（说明结构引用头不必要，贡献退化为已知的吸附规则）。

**成本：** 7B 单步 SFT，每个变体约 20 万样本，8×A100 每个约 6–10 小时，6–7 个变体合计约 2–3 天；探针重建与评测为离线推理，单卡一天内。多步实景（WebArena 类网页环境，Docker，无需 KVM）作为扩展，不在最小实验内。

Frozen Problem Anchor and user constraints:

- **起点问题**：同时读截图与结构化序列（DOM / a11y 树）的多模态 GUI 智能体，其状态信念和动作在两通道冲突时跟随哪一方，主要由动作输出格式决定；坐标动作抗结构劫持但无冲突时定位错误高，结构动作定位准但继承结构中的错误或恶意断言。需要回答能否同时得到两者的优点，以及训练中的动作格式配比如何塑造通道偏好。
- **初始任务与评测**：单通道干预探针（像素与结构只改其一，确定性强制选择评分）上的结构跟随率与无冲突错误率；实景环境中冲突导致的错误动作与任务失败（Web、移动端、桌面）。
- **瓶颈与证据边界**：只有一篇受控证据（2607.04334）；已有修法是训练无关的启发式自检门控；探针多为单步信念测试；未做针对性查新。
- **用户资源约束**：正式实验 8×A100 80GB，单次最好不超过 5 天；预研 2×A100 80GB / 4×L40 48GB / 8×4090 24GB；付费 API（如 GPT judge）1000 元以内可自主决定；token 资源稀缺。在线桌面虚拟机或 Android 模拟器（需 KVM）能否在服务器上运行尚未确认；离线探针与不需 KVM 的网页环境不受此限。
- **时间与目标**：自 2026-10 起半年内投出一篇主会论文。
- **非目标**：不做世界模型、视频生成、机器人方向。
- **进入实验规划的成功条件**：独立 Reviewer 两次（常规 + 复核）判定三项贡献分都 ≥6 且至少两项 ≥8、可行性 pass、`experiment_ready`、无致命阻断；最小实验能在上述算力内完成，强基线有可信复现路线。
