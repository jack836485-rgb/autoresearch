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
files in this workspace and do not write files, except your raw review to /home/claude/autoresearch/review-stage/gui_channel_action_q004_20261105/round-02-review.md (UTF-8).
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

**定位关键词：** accessibility tree / DOM；visual grounding；GUI grounding；prompt injection；Multimodal-Mind2Web

**一句话定位：** 在 web GUI 智能体中，纯视觉 grounding 模型训练后已能在元素选择上接近读 HTML 的方法，且几乎不被结构中的错误文本劫持；但它拿不到只存在于结构中的信息（屏幕外的元素、被截断的文本、图标的无障碍标签）。同时读截图与结构的混合智能体能用这些信息，却会照搬结构中与屏幕显示不符的文本。

**与起点问题的关系：** 原问题的收窄版；保留对象（截图 + 结构的双通道智能体）与冲突评测（结构跟随率），但把"打破定位精度与抗劫持的取舍"改为"打破信息覆盖与信任的取舍"，因为在 web 元素选择上前者已被纯视觉训练基本打破；"训练中的格式配比如何塑造通道偏好"不再回答，移动端与桌面不在最小实验内。

## 核心 Claim

成功后新增一个训练方法：以"这段信息是否在屏幕上可见地渲染出来"作为两通道的仲裁信号。具体做法是，对可见渲染的文本做冲突增广，标签跟随像素；对未渲染的信息（屏幕外节点、截断部分、无文字图标的 aria-label/title），标签沿用结构。训练后，同一个混合模型在可见文本冲突上接近纯视觉模型的抗劫持能力，在需要结构独有信息的样本上保留混合模型的准确率，推理时不需要额外调用。

可推翻的判断：同底座、同数据下，在两个评测子集上比较纯视觉、普通混合与本方法。
1. 可见文本冲突探针（结构中目标或干扰节点的文本被改，像素未改）：本方法的结构跟随率接近纯视觉，显著低于普通混合。
2. 结构必需子集（目标在视口外、文本在屏幕上被截断、或目标是只有 aria-label 的图标）：本方法准确率接近普通混合，显著高于纯视觉。
3. 只给可见性标记、不做冲突增广时，(1) 中的结构跟随不下降。这说明收益来自"可见即以像素为准"的标签，而不是标记本身。

若纯视觉在 (2) 上不显著落后于普通混合，说明结构独有信息在该数据上分量太小，本方法的必要性不成立。若 (1) 和 (2) 不能同时满足，信息覆盖与信任的取舍没有被打破。

当前依据：
- 2607.04334（HKUST、深圳大学）用白盒消融显示，文本状态信念服从结构，是由被复制的那个结构值驱动的：精确消去该值能把信念翻回像素，同等大小的随机消去做不到。冲突增广正是让模型学会"已渲染文本不从结构复制"。该文还发现，非文本身份（图标、颜色等）基本由像素决定，所以可见性分派只需处理文本。
- 同文的训练无关门控把屏幕外或过期节点一律拒掉（"off-screen or stale node can never pass"）。这让过期节点的结构跟随降到 ≤0.07，但也意味着结构独有信息被一并丢弃，每个候选还要额外一次裁剪查询。
- UGround（2410.05243）的纯视觉 grounding 在 Multimodal-Mind2Web 上与基于 HTML 的选择相当，且在 2607.04334 中结构跟随仅 0.02–0.07。这说明纯视觉是"信任"一端的强基线；它在结构必需样本上的缺口有多大，目前没有直接测量。
- 仲裁信号可信：可见性由浏览器渲染结果计算（视口内、非零面积、`elementFromPoint` 命中该节点、文本是否被截断），不取自 DOM 声明。攻击者改 DOM 文本，改不了"这段文本是否画在屏幕上"。

仍未知：
- 结构必需样本在真实任务中的比例；
- 冲突增广是否降低无冲突准确率；
- 注入到不可见属性（如 aria-label）的攻击，本方法按设计不能防御，需要在主张中排除。

## 方法设计的核心思想

**输入**：截图（视口大小）与序列化结构。harness 为每个节点附加由渲染计算的两个标记：`rendered=yes/no`（节点在视口内可见，且命中测试为其本身）与 `text_shown=full/truncated/none`（显示的文本是否完整）。去掉 bbox 等几何字段，避免坐标从结构中复制。

**动作**：结构引用动作（元素 id），与普通混合 agent 相同。

**训练标签规则**（核心）：
- 对 `rendered=yes` 且 `text_shown=full` 的节点做冲突增广，即把结构中的文本改成别的字符串。目标按任务指令在像素上的真实对象给出：模型应选中屏幕上显示为指令所指文字的元素，而不是结构中被改成该文字的元素。
- 对 `rendered=no` 或 `text_shown≠full` 的节点不增广，标签照常；屏幕外目标需要先滚动时，标签为结构中的目标 id 加滚动动作，按原数据转换。

**推理**：单次前向，无门控、无额外调用。

**输出**：动作，以及可选的"该动作依据可见文本还是结构独有信息"标记，供审计。

**与最高近邻的关键差别**：
- 2607.04334 的门控在推理时对每个候选做裁剪自读，并拒绝一切不可见节点；本方法在训练时按可见性分派信任，保留不可见信息的使用。
- ECA（2605.19192）用外部 DOM/OCR/AX 验证器为动作谓词出具证书，再由确定性门控授权；本方法不引入验证器，把仲裁规则学进策略。
- DMAST（2603.04364）对抗两通道被一致污染的攻击；本方法处理的是两通道不一致。

## 最小实验

**模型与数据**：
- 模型：Qwen2.5-VL-7B-Instruct。
- 训练：Multimodal-Mind2Web 训练划分。已用 HF datasets-server 读取首行核验：含 `screenshot`、带 `backend_node_id` 的 `cleaned_html`、带 `bounding_box_rect` 的正负候选、`operation`、`confirmed_task`。
- 渲染标记的来源：截图为整页时，按视口高度切片，用 `bounding_box_rect` 判定是否在当前视口；`text_shown` 用节点文本与裁剪区域的 OCR 结果比对离线计算。这只是近似，无法复原 `elementFromPoint` 遮挡判断，在线评测时再用真实浏览器计算。

**评测**：
- 标准测试：Multimodal-Mind2Web 跨任务、跨网站、跨领域三个测试划分的元素准确率，检查无冲突精度不下降。
- 可见文本冲突探针：按 2607.04334 的公开规范在测试划分上重建，约 300 个，强制选择评分。该文称代码随论文发布，本轮未找到链接，因此标为独立复现。
- 结构必需子集：从测试划分中筛出三类，每类至少 100 个，人工抽检 50 个确认属于该类：
  - 目标在当前视口外，切出不含目标的视口；
  - 目标文本在截图中被截断（`text_shown=truncated`）；
  - 目标为无可见文字的图标且结构中有 aria-label 或 title。
  - 若某类不足 100，如实报告该类样本量。

**对照**（同底座、同训练数据与步数）：
- 纯视觉坐标 SFT（同数据，UGround 式），另附公开的 UGround-V1-7B 作参考；
- 普通混合 index SFT；
- 普通混合 + 训练无关门控：按 2607.04334 正文规范独立实现，记录额外调用；
- 混合 + 可见性标记但不做冲突增广；
- 混合 + 冲突增广但不区分可见性（对所有节点都增广）：检验可见性分派是否必要，预期它会损害结构必需子集。

**支持 / 推翻主贡献的结果**：
- 支持：
  - 本方法在冲突探针上的结构跟随与纯视觉的差距 ≤0.05；
  - 在结构必需子集上与普通混合的差距 ≤3 个点、相对纯视觉提升显著；
  - 标准测试准确率不低于普通混合 2 个点以上；
  - "不区分可见性的增广"在结构必需子集上明显下降。
- 推翻：
  - 纯视觉在结构必需子集上不落后；
  - 或本方法在任一子集上明显落后于对应的最佳单端；
  - 或"只加标记"已达到同样效果。

**成本**：
- 训练：5 个 SFT 变体，每个约 5–10 万样本，8×A100 每个约 4–6 小时，合计约 1–1.5 天；
- OCR 与探针构建：CPU 与单卡，数小时；
- 评测：离线推理，单卡一天内；
- 不需要 KVM。在线 WebArena 类环境中的注入评测作为扩展，不在最小实验内。

Frozen Problem Anchor and user constraints:

- **起点问题**：同时读截图与结构化序列（DOM / a11y 树）的多模态 GUI 智能体，其状态信念和动作在两通道冲突时跟随哪一方，主要由动作输出格式决定；坐标动作抗结构劫持但无冲突时定位错误高，结构动作定位准但继承结构中的错误或恶意断言。需要回答能否同时得到两者的优点，以及训练中的动作格式配比如何塑造通道偏好。
- **初始任务与评测**：单通道干预探针（像素与结构只改其一，确定性强制选择评分）上的结构跟随率与无冲突错误率；实景环境中冲突导致的错误动作与任务失败（Web、移动端、桌面）。
- **瓶颈与证据边界**：只有一篇受控证据（2607.04334）；已有修法是训练无关的启发式自检门控；探针多为单步信念测试；未做针对性查新。
- **用户资源约束**：正式实验 8×A100 80GB，单次最好不超过 5 天；预研 2×A100 80GB / 4×L40 48GB / 8×4090 24GB；付费 API（如 GPT judge）1000 元以内可自主决定；token 资源稀缺。在线桌面虚拟机或 Android 模拟器（需 KVM）能否在服务器上运行尚未确认；离线探针与不需 KVM 的网页环境不受此限。
- **时间与目标**：自 2026-10 起半年内投出一篇主会论文。
- **非目标**：不做世界模型、视频生成、机器人方向。
- **进入实验规划的成功条件**：独立 Reviewer 两次（常规 + 复核）判定三项贡献分都 ≥6 且至少两项 ≥8、可行性 pass、`experiment_ready`、无致命阻断；最小实验能在上述算力内完成，强基线有可信复现路线。
