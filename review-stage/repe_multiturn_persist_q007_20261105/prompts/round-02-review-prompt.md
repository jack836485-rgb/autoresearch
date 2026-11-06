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
Today's date: 2026-11-05. Known tool workarounds: GitHub REST API returns HTTP 403 through this sandbox's proxy; anonymous 'git clone --depth 1' of public GitHub repos works from Bash; arXiv abs/html pages are readable via WebFetch
Finish all searches before answering and leave no background tasks running. Do not read other
files in this workspace and do not write files, except your raw review to /home/claude/autoresearch/review-stage/repe_multiturn_persist_q007_20261105/round-02-review.md (UTF-8).
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

**定位关键词：** activation steering；multi-turn conversations；KV cache；coherence degradation；persona steering；prefix steering

**一句话定位：** 多轮对话里，逐 token 的激活 steering 会让连贯性随回合急剧下降。GCAD（2605.10664，MIT）报告其平均连贯性漂移为 −18.6，提示控制与无 steering 基线则保持稳定。作者把原因归为被 steer 的响应写进 KV cache 后跨回合放大，并据此设计了避开响应分量的注意力层干预，但没有直接重算 cache 来检验这一解释。前缀 steering 的作者（2610.04967）也写明，行为实验分不清效果是靠"被改的表示"还是靠"生成的上下文"在传递。于是多轮 steering 中"控制"与"损伤"各自经由哪条通路跨回合，至今未被分开测量。

**与起点问题的关系：** 原问题；同时回答卡片的两半——持续干预为何在多轮中累积损伤（检验 KV 污染是否为原因），以及何时前缀足够（检验控制是否由保留的转录承载）。保留起点的多轮协议、特质保持与连贯性随回合的曲线、新回合与目标特质的冲突程度。

## 核心 Claim

若成立，本工作给出多轮 steering 的**双通路分离**：特质控制主要经由保留下来的对话转录跨回合传递；连贯性的累积损伤主要经由被 steer 的历史位置留在 KV cache 中的键值。由此得到一个极简修法，称为**干净历史 steering**：每个回合只在当前回合的生成位置施加 steering，新回合开始时，把此前所有回合的 KV 以不加 steering 的方式重新计算。它在特质保持上与标准逐 token steering 相当，而累积的连贯性损伤降到接近提示控制的水平，无需修改注意力。

可推翻的判断，均预设等价界与功效：
- **(a) 损伤走 KV。** 在逐 token steering 下，"干净历史"相对"保留被 steer 的历史 KV"，把第 8 回合的连贯性损失减少至少一半。若两者的连贯性曲线落在预设等价界内，说明损伤主要来自被写坏的文本本身，GCAD 的 KV 污染解释被推翻。
- **(b) 控制走转录。** 在同一条件下，干净历史与保留被 steer 的历史 KV 的特质保持差异落在预设等价界内（TOST，等价界为基线与标准 steering 之差的 20%）。按预实验方差，每档 50 段脚本可达 80% 功效。
- **(c) 前缀情形。** 前缀 steering 下，转录移植到全新实例与保留原 KV 的特质保持等价。冲突程度越高，衰减越快。

当前依据及适用条件：
- 损伤走 KV 一侧：GCAD 观察到提示控制在多轮中不退化、逐 token steering 急剧退化。其设计明确旨在去除"可被写回 KV 并跨回合放大"的响应分量，并把漂移从 −18.6 降到 −1.9。SKOP（2605.06342）显示 steering 会改变 query–key 匹配、使注意力从关键 token 改道，被 steer 的历史键值因此是可能的放大源。2604.08169 报告重复放大与干预选择性成反比。
- 控制走转录一侧：2601.20834 发现回放他人写的对话脚本即可复现表示变化；2602.24287 发现模型自己过去的回答会跨轮传播状态；2605.26772 单轮中撤除 steering 后，被 steer 生成的文本仍携带 48% 的效果。
- 仍未知：被 steer 生成的文本本身是否已足够退化，以至单独造成损伤（这是 (a) 的竞争解释，也正是实验要判别的）；固定探针沿 v 的投影跨轮漂移，2601.20834 指出表示会在对话中剧烈变化，因此特质保持以判官评分为主度量、探针为辅；重算历史 KV 的额外开销。

## 方法设计的核心思想

输入：一个模型、一个特质方向 v、多轮对话脚本。用户回合预先写好并回放，分支持、中性、反对三档冲突。

动作（同 α、同层）：
- S1 标准逐 token steering，保留被 steer 的历史 KV（GCAD 的设定）；
- S2 干净历史 steering：当前回合逐 token steering，新回合开始时用无 hook 的前向重新 prefill 全部历史；
- S3 前缀 steering，保留原 KV；
- S4 前缀 steering，转录移植（全新实例重算）；
- 对照：提示控制（system prompt 写入特质）、无 steering 基线、GCAD（公开代码 github.com/NihiI-obstat/Gated-Cropped-Attention-Delta）、Assistant Axis 封顶（github.com/safety-research/assistant-axis）。

测量：每回合特质表达（两个开源判官评分，加探针投影作辅助）与连贯性（判官评分，加困惑度）；记录每回合被 steer 生成文本的自身连贯性，用来判别"文本先坏"的竞争解释。

输出：S1 vs S2 的连贯性与特质曲线（检验 a、b）；S3 vs S4（检验 c）；S2 与 GCAD 的帕累托比较。

与最高近邻的关键差别：GCAD 提出 KV 污染解释并用注意力层修法回避，但没有通过重算历史 cache 做因果检验，也没有分开"控制"与"损伤"的通路；前缀 steering 只在单阶段评测，把机制区分留作未来工作；2610.19817 测多轮衰减，不区分通路；Memory Inception（2605.06225）以 KV 注入实现控制，研究的是 KV 作为控制载体，不是损伤来源。

## 最小实验

模型：Llama-3.1-8B-Instruct 与 Qwen3-8B（非思考模式），与 GCAD、2610.19817 的模型规模一致；Qwen2.5-7B-Instruct 作第三个模型（可选）。

特质：沿用 GCAD 的 persona 特质（复用其公开代码与评测流程，保证 S1 复现其退化），另加 2610.19817 式价值权衡一类。脚本：每特质每冲突档 50 段 10 回合（与 GCAD 的回合数一致），由强模型一次性生成、人工抽检 30 段，所有条件回放同一脚本。

相同核心条件：同模型、同层、同 α、同脚本、贪心解码；S1 与 S2 只在新回合是否重算历史 KV 上不同，S3 与 S4 同理。

统计：等价检验（TOST）与差异检验并报，等价界与样本量按 20 段预实验的方差预先登记；按脚本配对。

成本：2–3 模型 × 2 特质 × 150 段 × 10 回合 × 约 8 个条件 ≈ 7 万回合生成（每回合约 300 token），外加 S2/S4 每回合重算历史的 prefill（只有前向，开销约为生成的 1/3）。合计约 3 千万 token，2×A100 约 2 天。判官用本地开源模型，脚本生成用 API 约 50 元。

Frozen Problem Anchor and user constraints:

- **起点问题：** 多阶段控制任务中前缀 steering 何时足够、何时必须持续；持续干预为何累积损伤或衰减、反转。
- **对象与条件：** 开源指令/推理模型（证据中 Llama、Qwen 系列，7B–70B）；persona、价值、对齐特质的激活 steering；多轮对话与智能体循环。
- **初始任务/评测：** 特质表达与连贯性随回合数的曲线。
- **瓶颈与证据边界：** 各方法各自一种设定；多轮衰减证据仅摘要；KV 污染未隔离。
- **用户资源约束：** 预研 2×A100 80G / 4×L40 48G / 8×4090 24G；正式 8×A100 最好 ≤5 天；API 1000 元内自主；token 稀缺。
- **时间与目标：** 自 2026-10 起半年内投主会。**非目标：** 世界模型、视频生成、机器人。
- **进入实验规划的成功条件：** 两次独立审查（常规+复核）均三项 ≥6、至少两项 ≥8、可行性 pass、experiment_ready、无 fatal blocker；产出 EXPERIMENT_HANDOFF.md。
