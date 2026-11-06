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
Today's date: 2026-11-05. Known tool workarounds: arXiv abs/html/pdf pages are reachable via curl in Bash (pdftotext available); GitHub REST API returns 403 but 'git clone --depth 1' works for public repos; WebSearch and WebFetch are available
Finish all searches before answering and leave no background tasks running. Do not read other
files in this workspace and do not write files, except your raw review to /home/claude/autoresearch/review-stage/async_old_logit_aq006_20261105/round-02-review.md (UTF-8).
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

**定位关键词：** asynchronous reinforcement learning；training-inference mismatch；policy staleness；decoupled PPO；score centering；importance sampling

**一句话定位：** 在异步 LLM agentic RL 的离策略校正中，训练端在 rollout 生成版本上的概率（old logits）常缺失；已有工作报告精确 old logits 能显著改善训练，但这份收益由什么机制带来、能否在不保存历史权重时获得，尚未在真实异步设置中受控检验。

**与起点问题的关系：** 子问题。保留对象（缺 old logits 时的异步离策略校正）、条件（异步、部分 rollout、多轮工具任务、稠密与 MoE）与评价目标（训练稳定性与任务成功率）；把"如何恢复 old logits"改为"什么时候需要 old logits、其收益来自哪一机制"。起点问题中的系统审计（哪些声称无损的系统未保留 old logits）不在本 Idea 内；阈值耦合导致后期崩溃的机理通过"偏差漂移"这一候选机制部分检验。

## 核心 Claim

**主贡献（现象／视角）：** 给出一个在真实异步 agentic RL 中可检验的归因：精确 old logits 相对常用代理的收益，主要来自两个可分别获得的机制——(a) 信任域参考放在 token 的生成版本上，使策略滞后进入被裁剪的比率；(b) 去掉训练–推理数值偏差带来的漂移（逐前缀的持续偏置）。(a) 用已记录的推理端概率作裁剪参考即可得到，(b) 用逐前缀的 score centering 即可得到，两者都不需要 old logits；只有当数值偏差的尾部跨过裁剪尺度时，精确的偏差–滞后分解才额外有益。若成立，异步系统可以不为快照、专用 old-logit 模型或 EWMA 参考付出系统代价，并能按偏差规模判断何时值得付。

**可推翻的判断：**
1. 偏差很小的稠密 BF16 设置中，"推理端概率作参考"与"精确 old logits"处于同一噪声带，两者都明显优于 2605.12070 所用的中间版本代理；若精确 old logits 仍显著更好，则 (a) 不足以解释其收益。
2. 偏差大的 MoE（不做路由回放）设置中，"推理端概率作参考 + score centering"与"精确 old logits + 漂移去除（DLC）"处于同一噪声带；若后者显著更好，则给出"需要 old logits"的明确条件，主张 (b) 被推翻。

**当前依据与适用条件：**
- 2605.12070（异步 agentic RL，ROLL，Qwen3-4B 与 30B-A3B，最大版本差 3）在同一掩码框架下比较精确 Snapshot 与代理，30B-A3B 的 VitaBench in-store 从 18.28 到 34.62。但其 "Decoupled PPO & Async" 的两个因子都以一个介于 old 与当前之间的可用版本为参考（Table 1），所以与 Snapshot 相比同时改变了参考位置和偏差处理，表中没有"推理端概率作参考"或中心化的对照。
- 2610.40945 用训练端在采样权重上的前向精确拆分误差，并分析了参考位置：参考取批次前训练端时，滞后落在比率外，PPO 在陈旧采样器下偏离 on-policy 达噪声底的 699 倍；参考取采样权重时，滞后在比率内。其 Table 2（Qwen3-0.6B，Countdown）在"量化 + 陈旧"下，不需 old logits 的"IS + 中心化"为 2.61 倍、准确率 30.5，需 old logits 的 DLC 为 2.17 倍、30.3。
- 2609.20807（0.6B–30B）认为训练–推理偏差导致的不稳定主要来自漂移，score centering 在量化下匹配或优于 IS，且可与 IS 组合处理陈旧度。
- 仍未知：上述两篇的结论来自短训练（40 步）、固定在 $\theta_0$ 的陈旧采样器、SGD 大学习率、单轮任务，是否迁移到连续版本流、Adam 小学习率、部分 rollout 跨版本、多轮工具调用与 MoE 路由偏差；MoE 路由翻转造成的偏差可能是重尾的，可能正是需要精确分解的情形。本 Idea 的价值依据是这些机制论证与 2605.12070 比较设计的混杂，而不是已测得的结果。

## 方法设计的核心思想

- **输入**：AReaL 异步训练中的轨迹，含逐 token 生成版本、推理端 logprob 与推理端 top-k head（score centering 所需）。
- **动作**：在完全相同的数据、超参与陈旧度下，只改变离策略校正的两个设计维度——裁剪参考放在哪里（中间可用版本 / 推理端已记录概率 / 精确 old logits）与偏差如何处理（掩码 / 中心化 / 不处理），并在偏差小与偏差大两种设置下比较。用对同步 on-policy 训练的偏离度作主指标，使少量种子也能区分。
- **输出**：精确 old logits 收益的机制归因、零历史权重组合与精确分解的差距，以及"需要 old logits"的条件。
- **与最高近邻的关键差别**：2605.12070 只比较 old logits 的不同获取方式，未拆分参考位置与偏差处理；2610.40945 给出了分解与参考位置理论，但实验限于小稠密模型、单轮、固定陈旧采样器、40 步；2609.20807 主要研究量化偏差。本 Idea 把三者的机制放到真实异步 agentic 设置中做受控拆分。

## 最小实验

- **设置**：AReaL 异步 Search-R1（公开 NQ+HotpotQA 训练集与 e5 检索器，AReaL `search_agent` 工作流），最大版本差 4，部分 rollout 开启，组大小、学习率、批次与阈值各臂一致。两种偏差规模：R1 稠密 Qwen3-4B，BF16 推理（偏差小）；R2 Moonlight-16B-A3B，BF16 推理、不做路由回放（偏差大；沿用 AReaL `examples/r3` 单机 4 卡推理 + 4 卡训练，关闭 `return_routed_experts` 与 `enable_router_replay`）。各 120 步。
- **五个校正臂（同一 PPO 裁剪 ε、同一偏差阈值）：**
  - A. 中间版本代理（2605.12070 的 Decoupled PPO）：AReaL 已核验实现 `use_decoupled_loss` + `prox_logp_method=recompute`。
  - B. 推理端概率作裁剪参考，不处理偏差：标准设置（verl fully-async 默认的 rollout logprob 作 old）。
  - C. B + 中心化（零历史权重的 DLC）：与 E 用同一 DLC 估计式（2610.40945 Eq. 6），只把分母 $p_{old}$ 换成已记录的推理端概率 $q_v$：裁剪 $p_\theta/q_v$，中心化项用采样端 top-k head 与 $p_\theta$ head。C 与 E 只差这一个分母。中心化的 head 收集与 tail 估计复用 AReaL 已核验的 score centering 代码路径（`areal/utils/score_centering.py`，其自带的 REINFORCE+截断 IS 形式作为补充参考，不作主对照）。
  - D. 精确 old logits + 2605.12070 解耦掩码：按其 §5.1 独立实现 Snapshot（CPU 保留最近 4 个版本权重，按逐 token 版本分组做训练端前向），目标按其 Eq. 4。
  - E. 精确 old logits + DLC：按 2610.40945 §7.1 与附录 L 独立实现（裁剪 $p_\theta/p_{old}$，用采样端 head 与 $p_{old}$ head 中心化）；重同步规则因 AReaL 每步同步而不启用，并说明这一改动。
- **参考与指标**：每种设置跑 2 次同步 on-policy 训练，作为偏离度的基准与噪声底（沿用 2610.40945 的定义：在固定 held-out 前缀上对 on-policy 模型的全词表 KL，除以两次 on-policy 训练间 KL）。在第 40、80、120 步测偏离度；同时报 7 个 QA 测试集 EM、活跃 token 比例、每步额外耗时与内存。各臂 1 个种子；R2 中 C 与 E 各补 1 个种子。
- **支持主张的结果**：R1 中 B 与 D 的偏离度之差小于两次 on-policy 间的噪声，且都明显低于 A；R2 中 C 与 E 之差在其两种子的散布内，B 与 D 明显差于 C。**推翻**：R1 中 D 显著优于 B，或 R2 中 E 显著优于 C。
- **关键数据可得性**：逐 token `versions`、推理端 `logprobs` 与采样端 head（`parse_sampler_heads`）在 AReaL 代码中已核验；score centering 要求温度 1、无 top-p/top-k（`validate_sampling`），各臂统一采用。Snapshot 的历史权重可由训练端每步保存。
- **成本**：R1 共 7 次运行 × 约 4 小时；R2 共 9 次运行 × 约 9 小时；合计约 4.5 天（8×A100），步时为估计，先用 R1 两臂实测修正；不需要付费 API。R2 的 Snapshot 臂驻留约 128 GB 主机内存，开跑前按共享机器内存余量规则确认。

Frozen Problem Anchor and user constraints:

- **起点问题**：异步（含延迟更新与部分 rollout）agentic RL 中，训练端在 rollout 版本上的 old logits 缺失，使训练–推理偏差修复与策略陈旧度校正无法按语义分开；阈值耦合导致后期崩溃；"无损"加速系统是否保留 old logits 未核对。
- **对象与条件**：PPO/GRPO 类 token 级离策略校正；推理端（vLLM/SGLang）与训练端（FSDP/Megatron）数值不同；rollout 与训练异步，单条轨迹可跨多个参数版本。
- **初始任务/评测**：agentic 多轮工具任务（2605.12070 用 τ²-Bench、VitaBench）；Qwen3-4B 稠密与 Qwen3-30B-A3B MoE；最大版本差 3。
- **瓶颈与证据边界**：精确获取 old logits 的现有方法（快照、专用模型、中断同步）系统代价高；近似参考（插值、EWMA）不恢复语义。原证据只到版本差 3、两种骨干、单框架；后期崩溃机理只有阈值扫描证据。
- **用户约束**：预研 2×A100 80G / 4×L40 48G / 8×4090 24G；正式实验 8×A100 80G，单次最好不超过 5 天；付费 API 1000 元内可自主；token 资源稀缺；目标自 2026-10 起半年内投一篇主会；不做世界模型、视频生成、机器人。预研只回答 go/no-go，先做最便宜的否证检查。
- **进入实验规划的成功条件**：一个候选通过两次独立审查（三项贡献分都 ≥6 且至少两项 ≥8，可行性 pass，verdict 为 experiment_ready，无致命阻断），并给出可在上述算力内完成、能区分主张的最小实验与可复现强基线。
