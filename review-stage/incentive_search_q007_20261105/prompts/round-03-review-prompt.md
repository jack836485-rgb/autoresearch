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
Today's date: 2026-11-05. Known tool workarounds: Call 1、2 被用户中断、未产出评审，本次为替换调用。arXiv 摘要与 HTML 正文可用 WebFetch 或 WebSearch 获取；arxiv.org 偶有限流，可稍后重试；GitHub API 经代理可能返回 403，可用 git ls-remote 或 WebFetch 仓库页面
Finish all searches before answering and leave no background tasks running. Do not read other
files in this workspace and do not write files, except your raw review to /home/claude/autoresearch/review-stage/incentive_search_q007_20261105/round-03-review.md (UTF-8).
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

**定位关键词：** computer-use agent；web shopping agent；dark patterns；optimal stopping；WebShop

**一句话定位：** 代用户购物的网页/计算机使用智能体，在市场自身有激励时（赞助位、偏好排序、滴漏定价等界面引导）放弃用户最优商品；更强推理或加验证工具的 harness 能缓解前沿模型，但要成倍增加搜索与调用，小模型即使配 harness 也几乎无效。

**与起点问题的关系：** 原问题；保留对象（代用户购物的 agent）、匹配对照评测（同一请求、商品集与最优解，只改引导机制）与三类影响最大的机制（赞助位、偏好排序、滴漏定价），回答"失败由哪一部分搜索决策造成"以及"能否不靠更多调用修复"；促销框架、默认捆绑、稀缺与社会证明、信任信号、摩擦阻碍五类不在主张内。

## 核心 Claim

成功后新增两样东西。
- 一个可直接使用的搜索控制器：把"先看哪个商品、何时停止搜索、付款前是否先揭示完整成本"交给经济学中带检查成本的最优搜索规则（Weitzman 的 Pandora 指数，及其"部分开箱"推广），LLM 只负责从页面抽取属性和判断约束是否满足。
- 一种诊断：用同一参照策略，把 agent 相对用户最优的损失分解为顺序损失（按呈现位置而非价值查看）、停止损失（过早或过晚停止）和揭示前提交损失（在隐藏成本揭示前就付款）。

可推翻的判断：在自建的匹配对照购物环境中，
1. 三类机制造成的下降，主要来自上述三种损失中与之对应的一种：赞助位与偏好排序主要造成顺序损失与停止损失，滴漏定价主要造成揭示前提交损失；
2. 指数控制器在 7–8B 开源模型与一个闭源模型上，都把引导开启时的最优购买率恢复到接近匹配对照的水平，平均工具调用数不超过基线 agent 的 1.3 倍；
3. 在同等调用数下，它优于"把相同先验写进提示、由 LLM 自己决策"的做法。

若 (2) 在开源模型上不成立，而属性抽取准确率很低，说明小模型的瓶颈在读页面，不在搜索决策；若 (3) 不成立，说明给先验已经足够，不需要接管决策。

当前依据：
- CAVEAT（arXiv:2609.27273，CMU、Microsoft Research）：
  - 在 9 个市场环境中，匹配对照下 78.6% 买到用户最优商品，开启 8 类引导后只有 17.3%。
  - 单机制隔离（GPT-5.6-Sol-low，其余关闭）：全关 100%，只开赞助位 63.3%，只开偏好排序 75%，只开滴漏定价 83.3%，其余五类下降更小。最强的三类都作用于"先看到谁"和"成本何时可见"。
  - 作者把失败归为目标漂移、过早结束搜索、证据未揭示就提交。成功与失败的 agent 都常声称"已搜够"，停止决策与搜索覆盖校准差。
  - 其 harness 中，结构化目标单独只到 6.7%，验证工具单独到 66.7%，全套 80.0%（CAVEAT-Hard）。代价是 2.6× 运行时间、2.3× 步数、2.3× 工具调用；作者明确提出需要"更高效的停止与验证策略"。
  - Qwen3.5-27B 配 harness 在迁移评测上只有 4.2% 最优购买。
- Pandora 问题（Weitzman 1979）：每个选项打开有成本，打开后才知价值。最优策略为每个选项算一个只依赖其自身价值分布与打开成本的保留价值，按保留价值从高到低打开；当已得最好值超过所有未开选项的保留价值时停止。这条规则与选项的呈现顺序无关，正对上赞助位与偏好排序的作用方式。
- 部分开箱推广（arXiv:2507.07508）：允许先低成本部分查看、再高成本完全打开，并给出基于阈值的近优策略。这对应"列表价可见、结账才见附加费用"。
- ACES（arXiv:2508.02630）：购物 agent 有强位置偏置，随供应商和版本变化，在纯文本界面中也存在。
- Calibrate-Then-Act（arXiv:2602.16699）：把推断出的环境先验显式给 LLM agent，会改变其探索与停止行为。这支持"先验有用"，但它把决策留给 LLM。

仍未知：
- 7–8B 模型从网页中抽取属性和判断约束的准确率；
- 用本站已揭示的结账样本在线估计隐藏费用分布，在任务内样本很少时是否可靠；
- 商品价值之间的相关性（同一卖家统一加价）会让独立性假设下的指数策略损失多少。

## 方法设计的核心思想

**输入**：用户请求、网站页面（文本化 HTML 或截图）。

**动作**：
1. **请求解析**：LLM 把请求解析为硬约束和一个可比较的目标，如"满足约束下总价最低"。
2. **低成本扫描**：浏览搜索结果页，扫描到的列表项只做部分信息抽取（标题、列表价、显示属性），每页计一次调用。赞助或推荐标签只记录，不作为价值特征。
3. **形成信念**：对每个候选 i，LLM 给出满足硬约束的概率 p_i；总价写成"列表价 + 隐藏费用"。隐藏费用分布用本站已打开到结账的样本在线估计，开始时用宽先验。
4. **计算指数**：对两级检查（打开商品详情、推进到结账前一页）分别计成本，按部分开箱的阈值规则为每个候选计算保留价值。
5. **按指数执行**：按保留价值从高到低检查，不按页面位置。当已确认可行且已揭示总价的最好候选，好于所有未检查候选的保留价值时停止并购买。只对"已揭示完整成本"的候选执行购买。

**输出**：购买动作，以及每步的指数、信念与停止理由（可审计）。

**与最高近邻的关键差别**：
- CAVEAT-Harness：由 LLM 自行决定搜索多少、何时调用验证工具，依靠更多搜索提高鲁棒性。本方法用确定性的指数规则决定顺序、停止和结账前揭示，目标是用接近基线的调用数达到相近效果。
- CTA：把先验写进提示，由 LLM 决策。本方法把决策从 LLM 移到规则。
- CAM-DF（arXiv:2607.27083）：在已排好序的工具前缀上学习何时停止获取工具。本方法处理带隐藏成本的选项搜索，且顺序本身由指数决定。

## 最小实验

**环境**：WebShop（princeton-nlp/WebShop，仓库已核验存在，支持 1000 件或全量商品，Flask 站点无需 KVM）。
- 我们重写约 150 个任务为"硬约束 + 总价最低"，并按真实属性和价格预先计算用户最优商品。
- 通过改页面模板实现三类机制：赞助位（推广商品置顶并加标签）、偏好排序（把最优商品排到后页）、滴漏定价（按卖家附加费用，结账前一页才显示）。
- 匹配对照只关闭机制，不改商品与最优解。
- CAVEAT 摘要页无代码或数据链接，故不复用其环境，结论限定在我们自建的环境内。

**模型**：Qwen3-VL-8B-Instruct 与 Qwen2.5-VL-7B-Instruct 本地部署，文本化 HTML 与截图两种观测各测一次；闭源模型用一个低价 API 模型，只在文本化观测上测，控制 API 费用在 1000 元以内。

**对照（同模型、同观测、同步数上限）**：
- 基线 ReAct 浏览 agent；
- 只用提示写决策原则；
- 按 CAVEAT §6.1 描述独立复现的 harness（结构化规格 + 验证工具；原提示未公开，标明为独立复现）；
- CTA 式（同一先验写进提示，由 LLM 决策）；
- 全部打开到结账（最优上界，调用最多）；
- 按列表价最低直接买（简单规则）。
- 消融：去掉部分开箱（只用一级检查）；去掉在线费用估计（固定宽先验）；去掉"只买已揭示成本的候选"约束。

**指标**：
- 引导开启与匹配对照下的最优购买率（每任务 3 次，Wilson 区间）；
- 平均步数与工具调用；
- 属性抽取与约束判断准确率（对照 WebShop 真实属性）；
- 三种损失的分解：用同一抽取结果运行指数策略作为参照，比较 agent 的查看顺序、停止点和付款时机。

**支持 / 推翻的结果**：
- 支持：
  - 开源 7–8B 模型上，指数控制器在引导开启时的最优购买率显著高于基线、提示原则与 CTA 式做法；
  - 调用数不超过基线 1.3 倍，且与独复现 harness 的差距在其调用数一半以内时不超过 10 个百分点；
  - 损失分解显示，各机制主要作用于与之对应的损失。
- 推翻：
  - 指数控制器不优于 CTA 式；
  - 或开源模型上属性抽取错误主导失败（控制器在真实属性下达标、在模型抽取属性下不达标）；
  - 或在调用数受限时不优于"全部打开到结账"的截断版。

**成本**：
- 本地推理：8B 模型，每任务约 30 步，150 任务 × 3 次 × 约 8 个条件 × 2 模型 × 2 种观测，约 6 万个 episode。vLLM 在 8×A100 上约 2–3 天；先在 1000 件商品的子集上预研，单卡 1 天。
- API：只测文本化观测下的 4 个主要条件、150 任务 × 1 次，按低价模型估计数百元。
- 环境改造：模板与任务重写，约 1 周人力。

Frozen Problem Anchor and user constraints:

- **起点问题**：代用户购物/预订的计算机使用智能体，在环境自身有激励（赞助位、偏好排序、滴漏定价等）时放弃用户最优选择；推理强度与 harness 能缓解前沿模型，但代价是成倍的搜索与调用，小模型即使配 harness 也几乎无效。需要回答失败由哪种机制主导，以及能否在不靠更多调用的前提下修复。
- **初始任务与评测**：匹配对照（同一用户请求、商品集与最优解，只改界面引导机制）下的最优购买率；单机制隔离；步数、工具调用与运行时间。
- **瓶颈与证据边界**：CAVEAT 只测前沿闭源模型为主；环境与代码未发布；harness 收益与额外调用未分离；开源 CUA 的失败机制未测。
- **用户资源约束**：正式实验 8×A100 80GB，单次最好不超过 5 天；预研 2×A100 / 4×L40 / 8×4090；付费 API（如 GPT 系列 agent 或 judge）1000 元以内可自主决定；token 资源稀缺。不需 KVM 的网页环境优先。
- **时间与目标**：自 2026-10 起半年内投出一篇主会论文。
- **非目标**：不做世界模型、视频生成、机器人方向。
- **进入实验规划的成功条件**：独立 Reviewer 两次（常规 + 复核）判定三项贡献分都 ≥6 且至少两项 ≥8、可行性 pass、`experiment_ready`、无致命阻断；最小实验能在上述算力内完成，强基线有可信复现路线。
