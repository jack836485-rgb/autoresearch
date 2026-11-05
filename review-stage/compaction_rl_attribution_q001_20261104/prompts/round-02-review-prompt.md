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
Today's date: 2026-11-04. Known tool workarounds: raw.githubusercontent.com 与部分 arXiv HTML 在本机超时或 404；可用 arxiv.org/abs、arxiv.org/pdf 与 anonymous.4open.science/api/repo/<name>/files
Finish all searches before answering and leave no background tasks running. Do not read other
files in this workspace and do not write files, except your raw review to C:\Users\30473\Desktop\研一\autoresearch\review-stage\compaction_rl_attribution_q001_20261104\round-02-review.md (UTF-8).
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

**定位关键词：** write-time regret；context compaction；credit assignment；hindsight relabeling；TextWorld；BrowseComp-Plus

**一句话定位：** 恒定上下文或带 compaction 的 LLM agent 中，writer 反复重写状态/摘要；一个事实被丢后往往隔了多次重写才在决策时暴露。本研究针对的就是 writer 训练信号如何为这种"跨多次重写的保留"记功。

**与起点问题的关系：** 子问题。起点问题是"带 compaction 的结果式 agent RL 中，增益来自 summary 还是执行器、为何 summary 学不好"。本候选保留其核心对象：结果式训练里，summary 内容本身得不到有效信用。研究范围收窄到"需跨多次重写携带的信息"的信用分配，先在固定 reader、只训练 writer 的受控环境中检验，再到联合训练的深度搜索 agent。起点中的"跨模型族的 summarizer/actor 迁移"和"可选压缩为何被 RL 放弃"仍未回答。

## 核心 Claim

**成功后新增：** 一种与延迟长短无关的 writer 训练信号，使 writer 能从自身经验中学会"该保留什么"。目前这种知识只能由带任务知识的手写规则提供。

**依据：**
- **DSSR（2609.32805，TextWorld 烹饪游戏，Qwen3-4B writer/reader）。**
  - 损失几乎全部是写入 regret，并随延迟增长。
  - 其前滚打分训练出的最佳 writer（A4 变体）在延迟 0/10/20/40 下胜率为 26.7/11.1/4.4/2.2%，未训练为 2.2/2.2/0/2.2，预注册的长延迟检验失败。
  - 一条手写的"该保留哪类事实"规则在每个延迟下都更好。
  - 作者把局限归因于信用分配：现在保留一个事实，只有之后每次重写都继续保留才有回报，而逐点打分看不到这一点。其 §5.6 显示，有延迟时多数后续写入点的候选里已不含决定性事实。
- **恢复反事实已被用于评测。** 把被驱逐的证据放回读者上下文，区分不可逆驱逐损失与检索失败（2609.08279）。
- **深度搜索 agent。** 2610.35496 显示，agent 普遍用重读已见内容来补偿被删信息。

**可推翻判断：**
1. 在 DSSR 同一协议下，用"使用时刻事后重标注"的偏好训练 writer：
   - 长延迟（F′=20、40）的胜率显著高于 DSSR-A4；
   - 缩小与手写规则的差距；
   - 训练后 writer 在长延迟写入点保留决定性事实的比例上升；
   - 状态长度保持在同一预算内。
2. 在带 compaction 的 BrowseComp-Plus 联合 RL 中，以"重读已见文档"作为同一信号的免费版本，同准确率下每题重读次数与总 token 显著低于结果广播 GRPO。

**如何区分解释：**
- 若重标注后短延迟提升而长延迟仍无增益，"跨重写信用是瓶颈"被推翻，瓶颈应在 writer 容量或泛化。该判定以手写规则在相同 writer/预算下有效为前提，可直接检查。
- 若重标注得到的"所需事实"与手写规则覆盖的事实类型重合度低，则说明使用时刻信号不可靠。

**仍未知：**
- 恢复反事实在多个所需事实并存时的识别噪声。
- 偏好训练是否泛化到未见游戏的事实类型。
- 在深度搜索中，"summary 是否仍含某文档信息"的判定方式（文档 ID 提及或关键句重叠）的准确度。

## 方法设计的核心思想

**输入：** writer 在一局游戏或一条搜索轨迹中逐步写出的状态序列 z_1…z_T、完整原始历史日志，以及 reader 的决策。

**动作：**
1. **找出所需事实。** 在 reader 决策点 u，若参考动作的似然低（与 DSSR 相同，使用环境最优策略给出的参考动作），将 u 之前已从状态中消失的原始观察分段放回 reader 上下文，用二分查找定位使参考动作似然回升最多的那段观察 o*。从 o* 中按 TextWorld 模板抽出事实串 f。
2. **沿携带链重标注。** 对 f 首次出现之后、u 之前的每个写入点 t，若输入状态仍含 f，则采样多个候选并把保留 f 的候选标为优于丢弃 f 的候选；长度相近时以 DSSR 前滚分作次级排序。
3. 用这些偏好对按 DSSR 的训练配方更新 writer。
4. **深度搜索版本。** 某文档被二次检索即触发同样的重标注：最后一个仍提及该文档信息的摘要之后的那次重写为丢弃点，之前的写入点对应保留优先；作为 GRPO 中 summary token 的附加优势项。

**输出：** 更新后的 writer（或联合策略的 summary 部分）。

**与近邻的差别：**
- DSSR、TreeMem、PAIR 都用"从写入点向前续写有限步"来打分，看不到跨多次重写的保留价值。
- ECHO 依赖抽取式记忆的轮次索引。
- Self-Credit 给被引用的动作轮次记功。
- TRACER 把重调用作为每工具保留比例的代价项，并冻结执行器。

本方法从"需要暴露的时刻"反向找出事实，再把偏好施加到整条携带链。

## 最小实验

**实验 A（主，受控）：**
- **协议：** DSSR 公开协议与匿名代码（anonymous.4open.science/r/AgentDSSR，已核含 env/、dssr/、configs/、checkpoints/、prompts/）。Qwen3-4B-Instruct writer LoRA，固定 reader R1，128-token 状态预算，延迟 F′∈{0,10,20,40}，按 DSSR 的训练/验证/预注册测试划分。
- **对照：**
  - 未训练 writer；
  - 结果广播（以续写真实回报打分，即 DSSR 的 outcome 变体）；
  - DSSR-A4（官方最佳）；
  - 本方法；
  - 手写规则（参照）。
- **一致性：** 候选数、温度、训练轮次、偏好对数量与 DSSR 相同；本方法额外的恢复反事实只需 reader 前向计算，每个失败决策点约 log₂(段数) 次。
- **度量：** 各延迟胜率（bootstrap 区间）、长延迟写入点的事实保留率、所需事实识别与手写规则事实类型的重合度。
- **成本：** DSSR 报告可在单 GPU 上逐位复现，估计 1–2 天/方法，3 个种子。

**实验 B（迁移到联合 compaction RL）：**
- **设置：** Qwen3-8B，BrowseComp-Plus 固定语料（约 10 万文档，830 题与 qrels 公开），16K 工作窗口；verl 与 FoldAgent 本地检索服务（已核目录含 envs/local_search.py 与 Qwen3-8B 训练脚本）。
- **对照：**
  - 摘要式管理 + GRPO 广播优势（ReSum-GRPO/SUPO 规则明确，独立实现）；
  - Self-Credit（2610.28388，按公开规范独立复现）；
  - 本方法（广播 GRPO + 重读触发的重标注优势）。
- **一致性：** 同 rollout 数与步数。
- **度量：** 准确率，每题重读次数，总 token，以及训练前/后 summarizer × actor 的 2×2 交换。
- **成本：** 估计每次运行在 8×A100 上 1–1.5 天，属经验外推，未实测。单种子。

不需要付费 API。

Frozen Problem Anchor and user constraints:

- **起点问题：** 在长程 LLM agent 的 RL 训练中把上下文 compaction（模型自写摘要替换历史）放进 rollout 时，训练收益的来源（summary 质量 vs 执行器对有损上下文的适应）、结果式 RL 回避压缩动作的原因、以及 summarizer/actor 配对的可迁移性。
- **对象与条件：** 开源权重 agent 模型（GLM、Qwen 系列已有证据）、工具交互或长输入任务（SWE-bench Verified、Terminal-Bench 2.0、BrowseComp-Plus、长输入 QA），上下文窗口小于完整轨迹，压缩由模型自身或外部管理器执行，训练信号为结果奖励。
- **瓶颈与证据边界：** 现有证据均为单次运行或单基座；消融只去掉组件，没有配对交换；RL 回避压缩只有一次观察与作者解释。
- **用户约束：** 计算资源：预研 2×A100 80G / 4×L40 48G / 8×4090 24G；正式实验可用 8×A100 80G，单实验最好不超过 5 天；付费 API（如 GPT judge）1000 元以内可自主决定；token 资源稀缺；目标半年内（自 2026-10 起）投出一篇主会论文。预研只回答 go/no-go，单模型单种子为主。
- **非目标：** 不做大规模（>30B）RL；不依赖闭源模型权重；不在本阶段运行实验。
- **进入实验规划的成功条件：** 得到一个独立 Reviewer 两次判定贡献三项都 ≥6 且至少两项 ≥8、可行性通过的 Idea，其最小实验能在上述资源内完成。
