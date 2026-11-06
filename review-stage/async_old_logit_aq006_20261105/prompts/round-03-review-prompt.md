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
files in this workspace and do not write files, except your raw review to /home/claude/autoresearch/review-stage/async_old_logit_aq006_20261105/round-03-review.md (UTF-8).
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

**定位关键词：** mixture-of-experts；rollout routing replay；router drift；asynchronous reinforcement learning；training-inference mismatch；policy staleness

**一句话定位：** 在异步 MoE LLM 强化学习中，路由回放（Rollout Routing Replay, R3）把 token 生成时（版本 $v$）推理端选择的专家，原样回放到当前权重 $\theta$ 的训练前向中；在异步下，这同时冻结了两类不同的路由差异——训练与推理数值实现不同导致的路由翻转，以及策略更新后路由本身的变化。

**与起点问题的关系：** 邻近新问题（MoE 情形）。保留起点问题的条件（异步、延迟更新、部分 rollout，训练端旧版本概率即 old logits 缺失）与评价目标（训练稳定性与任务成功率），把对象从 token 概率扩展到专家路由：起点问题是"缺 old logits 时，训练–推理偏差与陈旧度校正纠缠"，MoE 中同样的纠缠发生在路由层。方法同时给出一个不需 old logits 的精确比率分解，也适用于稠密模型；起点问题中对"声称无损的系统是否保留 old logits"的审计不在本 Idea 内。

## 核心 Claim

**主贡献（方法）：** 异步系统每次权重同步后，推理端已持有当前权重 $\theta$。对即将训练的批次，推理端在 $\theta$ 上做一次 prefill，返回每个 token 的推理端概率 $q_\theta(y_t)$ 和推理端路由 $R^{inf}_\theta(t)$。训练端梯度前向回放 $R^{inf}_\theta$，而不是 R3 回放的生成时路由 $R^{inf}_v$；离策略比率按
$$\frac{p_\theta(y_t)}{q_v(y_t)}=\underbrace{\frac{p_\theta(y_t)}{q_\theta(y_t)}}_{\text{同权重、同路由下的数值偏差}}\cdot\underbrace{\frac{q_\theta(y_t)}{q_v(y_t)}}_{\text{同一推理端上的两个真实采样器之比}}$$
分别做偏差掩码与陈旧度裁剪。这里 $q_v$ 是生成时已记录的推理端概率，$p_\theta$ 是训练端回放 $R^{inf}_\theta$ 后的概率。这是对总比率的恒等分解，不估计任何缺失量，不需要历史权重或路由预测器。

若成立，异步 MoE RL 可用一次 prefill 的代价同时获得：(i) R3 的训练–推理路由一致（训练与下一轮采样器在同一权重、同一路由下计算）；(ii) 不冻结策略更新带来的路由变化，使梯度流向当前采样器实际使用的专家，并让这部分变化以真实概率比进入陈旧度裁剪；(iii) 语义分离的偏差与陈旧度校正。

**可推翻的判断：** 在同一异步配置（最大版本差 4，部分 rollout，每批一次优化器更新，每步同步）下：
1. 生成版本与当前权重之间，推理端路由翻转的 token 比例随版本差增长，并在版本差 2–4 时明显高于同权重下训练–推理的数值路由翻转比例；
2. 本方法的验证准确率峰值与末值优于 R3+TIS 与 RDC+TIS，训练–推理 KL 不高于 R3。
若 (1) 不成立（陈旧路由翻转可忽略），R3 在该设置下的冻结代价很小，方法无用武之地；若 (1) 成立而 (2) 不成立，说明真实路由变化带来的比率重尾抵消了收益。

**当前依据与适用条件：**
- R3（2510.11370）：MoE 中即使同权重，推理与训练的路由也会分歧并导致训练崩溃，回放推理端路由可稳定训练。这支持"消除数值路由翻转"的必要性。
- RDC（2610.21682）：在完全异步的 Qwen3-30B-A3B（DAPO-Math，FP8 vLLM 推理，每 4 次本地更新同步一次）上，RDC+TIS 的 AIME24/25 平均峰值比 R3 高 4.5、比 TIS 高 5.5，并在理论上指出 R3 回放会丢失当前训练路由所选专家的梯度。这说明异步下 R3 的回放有可观代价。但 RDC 的漂移分数比较的是"生成版本推理端路由"与"当前训练端路由"，混合了数值与陈旧两种来源，且处理方式是整条丢弃 8% 的响应。
- PR²（2606.00395）：把"回放冻结的路由会陈旧"定义为 router staleness，用学习的预测器预测更新后的路由并回放，在 Qwen3-30B-A3B、Moonlight-16B-A3B、OLMoE 上获益（附录 C 的 PR³ 是 R3 版本）。这支持"用更新后的路由替代冻结路由有益"。但其设置是同步 off-κ（一批数据多次更新），且路由是预测的。
- vLLM 逐比特一致 rollout（2026-10-14 博客）：在训练–推理数值完全一致时，每步 4 次更新仍有约 7% token 换了专家组合，即纯由策略更新引起的路由变化在规模上不可忽略。
- 仍未知：在每步同步、版本差 ≤4 的异步设置下，陈旧路由翻转的实际占比；回放真实当前路由后，陈旧度比率的尾部是否变重到抵消收益（R3 的稳定作用部分来自把路由差异排除在比率之外）；相对 RDC 与 PR³ 的收益大小。上述依据来自不同模型、框架与同步方式，本方法在目标设置下的效果尚未测得。

## 方法设计的核心思想

- **输入**：异步缓冲区中的轨迹（含逐 token 生成版本、生成时推理端 logprob $q_v$）；当前权重 $\theta$（已同步到推理端）。
- **动作**：
  1. 每次同步后，对即将训练的批次向推理端发送 prefill 打分请求（生成 1 个 token，要求返回 logprob 与路由），得到 $q_\theta$ 与 $R^{inf}_\theta$。部分 rollout 跨多个版本的轨迹不需特殊处理：整条轨迹都在 $\theta$ 上重新打分。
  2. 训练端前向通过现有路由回放通道回放 $R^{inf}_\theta$，得到 $p_\theta$。
  3. 损失：对偏差因子 $p_\theta/q_\theta$ 做对称掩码（按 IcePop/2605.12070 的解耦形式），对陈旧度因子 $q_\theta/q_v$ 做 PPO 裁剪；每批一次优化器更新，使训练端权重与推理端打分权重一致。
- **输出**：每步一次更新，额外代价为推理端对批次 token 的一次 prefill 与路由传输（与 R3 已有的路由传输同量级）。
- **与最高近邻的关键差别**：R3 回放生成版本路由（冻结陈旧部分）；PR²/PR³ 回放预测路由并需训练预测器；RDC 不回放，而用混合的漂移分数整条过滤；Decoupled PPO/Snapshot 一类方法需要训练端旧版本概率。本方法回放当前权重下的真实推理端路由，并用恒等分解把偏差与陈旧度分开，不需旧权重或预测器。

## 最小实验

**阶段 0：诊断（便宜，可直接给出 no-go）。** 在 AReaL 上用 Moonlight-16B-A3B（`examples/r3` 的单机 4 卡 SGLang 推理 + 4 卡 Megatron 训练配置）跑 R3+TIS 异步训练约 40 步，最大版本差 4。每步对训练批次额外做一次当前权重 prefill，并在 Megatron 前向中记录原生路由，统计：按版本差分层的陈旧路由翻转率 $\Pr[R^{inf}_v\ne R^{inf}_\theta]$ 与数值路由翻转率 $\Pr[R^{inf}_\theta\ne R^{train}_\theta]$（按层、按 token）；R3 下的比率 $p_\theta(R_v)/q_v$ 与真实采样器比率 $q_\theta/q_v$ 的偏离；prefill 耗时。停止条件：若版本差 4 时陈旧翻转率低于数值翻转率的一半，判 no-go。

**阶段 1：异步训练对比（8×A100，同上配置）。**
- 数据与任务：DAPO-Math-17K 训练，AIME24、AIME25（avg@16）与 MATH-500 评测，每 10 步评测一次；最大响应长度 8k；组大小 8；每批 32 组；最大版本差 4，部分 rollout 开启；每批一次优化器更新、每步同步；Clip-Higher（0.2/0.27）沿用 RDC 设置；各臂学习率、批次、长度与阈值完全一致，只改变路由处理与比率形式。
- 对照与复现路线：
  - TIS：标准截断 IS，以生成时推理端 logprob 为参考。
  - R3 + TIS：AReaL 已有实现（`rollout.return_routed_experts` + `actor.megatron.enable_router_replay`）。
  - RDC + TIS：无公开代码，按其 §3.2 Eq. 2–6 独立实现（按层专家使用分布的 TV 距离取层平均，在长度分桶内过滤漂移最大的 8% 响应，保留响应用训练端原生路由），漂移分数用 R3 通道已有的生成时路由与训练端前向路由计算。
  - 消融：当前版本回放 + 总比率 TIS（不做分解），分离"路由来源"与"比率分解"的贡献。
  - 本方法：当前版本回放 + 分解校正。新增部分是同步后对批次的 prefill 打分钩子；AReaL 中 SGLang 生成请求带 `return_routed_experts` 时会返回含 prompt 在内整个请求前缀的路由（`areal/engine/r3/preprocess.py` 按 prompt+completion−1 行解码），可直接复用为当前权重路由。
  - PR³（扩展，视预算）：按 2606.00395 附录 C.2 独立实现路由预测器。
- 种子与时长：5 臂，每臂 150 步；R3+TIS、RDC+TIS 与本方法各 3 个种子，TIS 与消融各 1 个种子，共 11 次运行。
- 支持主张的结果：本方法的 AIME 平均峰值与末值在 3 种子均值上高于 R3+TIS 与 RDC+TIS，且差距大于种子间标准差；训练–推理 KL 不高于 R3，无后期崩溃。推翻主张的结果：本方法不优于 R3+TIS，或劣于 RDC+TIS；或消融显示收益完全来自比率形式而与路由来源无关（此时主贡献降为分解本身）。
- 成本估计：阶段 0 约 4 小时；阶段 1 按每步约 3 分钟（8k 长度、256 条轨迹、4+4 卡）估计每次运行约 7.5 小时，11 次约 3.5 天，在 8×A100、5 天约束内；步时由阶段 0 实测修正，若超出则把 TIS 与消融降为 100 步。不需要付费 API。路由张量在 CPU 侧传输与暂存，按 R3 示例已有通道估计，开跑前在共享机器上确认主机内存余量。

Frozen Problem Anchor and user constraints:

- **起点问题**：异步（含延迟更新与部分 rollout）agentic RL 中，训练端在 rollout 版本上的 old logits 缺失，使训练–推理偏差修复与策略陈旧度校正无法按语义分开；阈值耦合导致后期崩溃；"无损"加速系统是否保留 old logits 未核对。
- **对象与条件**：PPO/GRPO 类 token 级离策略校正；推理端（vLLM/SGLang）与训练端（FSDP/Megatron）数值不同；rollout 与训练异步，单条轨迹可跨多个参数版本。
- **初始任务/评测**：agentic 多轮工具任务（2605.12070 用 τ²-Bench、VitaBench）；Qwen3-4B 稠密与 Qwen3-30B-A3B MoE；最大版本差 3。
- **瓶颈与证据边界**：精确获取 old logits 的现有方法（快照、专用模型、中断同步）系统代价高；近似参考（插值、EWMA）不恢复语义。原证据只到版本差 3、两种骨干、单框架；后期崩溃机理只有阈值扫描证据。
- **用户约束**：预研 2×A100 80G / 4×L40 48G / 8×4090 24G；正式实验 8×A100 80G，单次最好不超过 5 天；付费 API 1000 元内可自主；token 资源稀缺；目标自 2026-10 起半年内投一篇主会；不做世界模型、视频生成、机器人。预研只回答 go/no-go，先做最便宜的否证检查。
- **进入实验规划的成功条件**：一个候选通过两次独立审查（三项贡献分都 ≥6 且至少两项 ≥8，可行性 pass，verdict 为 experiment_ready，无致命阻断），并给出可在上述算力内完成、能区分主张的最小实验与可复现强基线。
