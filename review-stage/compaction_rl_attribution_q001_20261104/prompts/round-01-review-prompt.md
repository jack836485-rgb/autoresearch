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
Today's date: 2026-11-04. Known tool workarounds: raw.githubusercontent.com 与部分 arXiv HTML 在本机超时或 404；可用 arxiv.org/abs 与 arxiv.org/pdf 页面
Finish all searches before answering and leave no background tasks running. Do not read other
files in this workspace and do not write files, except your raw review to C:\Users\30473\Desktop\研一\autoresearch\review-stage\compaction_rl_attribution_q001_20261104\round-01-review.md (UTF-8).
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

**定位关键词：** context compaction；summarization-based context management；agentic reinforcement learning；credit assignment；BrowseComp-Plus

**一句话定位：** 长程搜索/编码 LLM agent 在结果奖励下联合训练"写 summary 替换历史"和"执行动作"时，summary 内容本身获得多少有效训练信号。

**与起点问题的关系：** 原问题。保留带 compaction 的结果式 agent RL 与长程深度搜索任务，新增"被丢信息能否从环境重获取"作为解释变量；起点中"summarizer/actor 能否跨模型族迁移"只通过同族训练前/后 checkpoint 交换部分回答，跨模型族仍未回答。

## 核心 Claim

**成功后新增的认识与工具：** 一个可检验的解释，说明为什么当前带 compaction 的 agent RL 学到的主要是"执行器耐受有损上下文"而不是"更好的 summary"；以及一种只为 summary 内容记功的训练信号。

**解释：** 常见训练 harness 在压缩后保留初始任务 prompt，且语料或仓库文件可被再次检索/读取，因此 summary 丢掉的信息几乎都能被执行器重新获取。结果奖励只能惩罚执行器补不回的损失，于是对 summary 内容近乎不敏感。

**可推翻的判断：**
1. 在可重获取环境中用广播优势训练时，summary 侧增益小：换回训练前 actor 时，训练后 summary 的收益大部分消失；重读次数上升。
2. 若在压缩边界从同一状态采样多份兄弟 summary，并以"禁止重读已观察内容"的短续写为其打组内相对优势（只作用于 summary token），则 summary 自身的增益可在换回训练前 actor 时保留。
3. 可选压缩设置下，不经 SFT 冷启动，压缩频率不坍塌到零。
4. 在会话中途注入、无法从环境重获取的用户约束，压缩后的保留率提升，而任务成功率不低于基线。
若阻断后兄弟 summary 之间的续写差异仍不显著，或成功率下降、summary 过度冗长，则该解释或方法被推翻。

**目前依据：**
- CompactionRL（2607.05378）106B 消融：不训练 summary 已取得压缩模式下 7.0 分增益中的约 4.7 分；30B 训练后单窗口模式 47.5→43.7。均为单次、200 题子集。
- Memento（2611.00244）：无 SFT 初始化时，RL 在 20 步内把可选压缩频率降到接近 0。
- 两项白名单外实证：
  - 2610.31778：benchmark 有固定目标、持久文件系统，被丢内容可重读找回。
  - 2610.35496：在 SWE-bench Verified 上，agent 以更多读取和回合补偿被删内容。
- PAIR（2609.36526）：用同状态有无压缩的配对续写，发现严重退化集中于少数压缩事件，说明边界局部比较能隔离单次压缩的影响。

**仍未知：**
- 阻断续写是否诱导 summary 过度保留本可廉价重获取的信息。
- 兄弟续写的随机方差是否过大。有一项配对重放研究报告单边界伤害符号一致性仅 κ≈0.28。
- 合成的中途约束能否迁移到真实交互会话。

## 方法设计的核心思想

**输入：** 带 compaction 的 rollout。上下文达到阈值或模型调用压缩工具时，用自写 summary 替换历史，初始 prompt 保留。

**动作：**
1. 对每条轨迹随机选少量压缩边界，从同一压缩前状态采样 G 份兄弟 summary。
2. 每份 summary 接当前策略做 h 步短续写。续写中检索服务对"已向该轨迹返回过的文档 ID"只返回占位符，执行器只能依赖 summary 和新信息。
3. 用续写结束时的可校验结果（答案正确或子目标命中），减去 summary 长度项，计算组内相对优势，只施加到该 summary 的 token。
4. 动作 token 仍用常规结果优势。
5. 可选压缩设置中，压缩决策 token 额外与同状态"不压缩"分支比较。

**输出：** 同一策略的更新。

**与最近邻的关键差别：**
- ReSum-GRPO/SUPO 把轨迹优势广播给所有段。
- CompactionRL 用 critic 估计段值。
- FoldGRPO 用启发式过程奖励（未折叠 token、越界、工具失败）。
- MMPO 用 belief entropy 代理。
- TRACER 用学习的结果模型训练保留比例并冻结执行器。
- PAIR/TRACE 用配对续写调整冻结模型的压缩 prompt。

本方法用阻断重获取的兄弟续写，专门隔离只有 summary 能携带的信息的价值。

## 最小实验

**模型与环境：**
- Qwen3-4B（预研），必要时 Qwen3-8B。
- BrowseComp-Plus 固定语料（约 10 万文档，830 题评测、qrels 公开，GitHub texttron/BrowseComp-Plus 已核含 data/searcher/topics-qrels）。
- 工作窗口 8K–16K，强制多次压缩。
- 训练查询取多跳 QA 或 BrowseComp-Plus 的不重叠划分，覆盖待核。

**框架：** verl。sunnweiwei/FoldAgent 已核含本地检索服务（envs/local_search.py）、ReAct/fold agent 与 Qwen3-8B 的 BrowseComp-Plus 训练脚本；文件内容因网络限制本轮未读取。

**同 rollout token 预算的对照：**
1. 摘要式管理 + GRPO 广播优势（ReSum-GRPO/SUPO 规则明确，独立实现）。
2. CompactionRL 式 PPO critic + 跨段 GAE（未找到代码，按原文规则独立复现，折扣细节为未定选择）。
3. 无阻断的兄弟分叉（检验"阻断"是否必要）。
4. RBC。

分叉额外开销由对照组用更大组规模补齐。

**度量：**
- BrowseComp-Plus 准确率。
- 训练前/后 summarizer × actor 的 2×2 交换。
- 每题重读次数。
- 可选压缩设置下无 SFT 的压缩频率曲线；对照为 Memento 式 SFT 冷启动，事后 note 由本地 72B 模型生成。
- 中途约束保留率：模板化注入可程序校验的约束（排除某来源、指定答案格式等），需新建，人工成本低。

**支持判据：** RBC 在交换到训练前 actor 时保留显著 summary 增益，中途约束保留率提升，且成功率不低于对照 1。

**推翻判据：** 若无阻断分叉与 RBC 无差异，"重获取掩盖"解释被推翻。

**算力估计：**
- Qwen3-4B、每步 32 题 × 8 rollout、约 200 步。每次运行在 4×A100 上估计 1–1.5 天，属 FoldAgent/Search-R1 类设置的经验外推，未实测。
- 兄弟分叉（每条 ≤2 个边界、G=4、h≈5 回合）约增加 30–50% rollout token。
- 4 组运行可在 8×A100、5 天内完成，单种子。
- API 不需要。

Frozen Problem Anchor and user constraints:

- **起点问题：** 在长程 LLM agent 的 RL 训练中把上下文 compaction（模型自写摘要替换历史）放进 rollout 时，训练收益的来源（summary 质量 vs 执行器对有损上下文的适应）、结果式 RL 回避压缩动作的原因、以及 summarizer/actor 配对的可迁移性。
- **对象与条件：** 开源权重 agent 模型（GLM、Qwen 系列已有证据）、工具交互或长输入任务（SWE-bench Verified、Terminal-Bench 2.0、BrowseComp-Plus、长输入 QA），上下文窗口小于完整轨迹，压缩由模型自身或外部管理器执行，训练信号为结果奖励。
- **瓶颈与证据边界：** 现有证据均为单次运行或单基座；消融只去掉组件，没有配对交换；RL 回避压缩只有一次观察与作者解释。
- **用户约束：** 计算资源：预研 2×A100 80G / 4×L40 48G / 8×4090 24G；正式实验可用 8×A100 80G，单实验最好不超过 5 天；付费 API（如 GPT judge）1000 元以内可自主决定；token 资源稀缺；目标半年内（自 2026-10 起）投出一篇主会论文。预研只回答 go/no-go，单模型单种子为主。
- **非目标：** 不做大规模（>30B）RL；不依赖闭源模型权重；不在本阶段运行实验。
- **进入实验规划的成功条件：** 得到一个独立 Reviewer 两次判定贡献三项都 ≥6 且至少两项 ≥8、可行性通过的 Idea，其最小实验能在上述资源内完成。
