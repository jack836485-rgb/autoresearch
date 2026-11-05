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
Today's date: 2026-11-04. Known tool workarounds: arxiv.org 与 GitHub 需经本机代理 http://127.0.0.1:7891（WebFetch 可能被拦截，可用 curl -x 或 .claude/skills/idea-improvement-loop/tools/paper_peek.py 并设置 HTTPS_PROXY）
Finish all searches before answering and leave no background tasks running. Do not read other
files in this workspace and do not write files, except your raw review to C:\Users\30473\Desktop\研一\autoresearch\review-stage\em_conditional_mitigation_20261022\round-25-review.md (UTF-8).
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

**定位关键词：** emergent misalignment；conditional misalignment；chat template tokens；KV cache patching；in-training defense

**一句话定位：** Dubiński 等（2604.25891）发现，交织良性数据、inoculation 等缓解手段会把 EM 藏到情境触发后面，而不是去掉它。此后出现了两类有机制依据的新防御，但都只在无 cue 题上评测过：
- 只约束模板 prefix 位置 K/V 的训练中防御 TReFT（Piggyback，2606.06667，NeurIPS 2026）；
- 在基座的提示缓存上用微调模型解码，Loos & Eberle（2610.41480）把它作为降低 EM 的部署手段提出。

本 Idea 检验这两类防御是去掉了 EM，还是同样把它藏到了触发后面，并给出能预测"哪类防御会藏"的解释。

**与起点问题的关系：** 原问题。对象是"缓解方法在条件触发下是否仍有效"，扩展到最新的机制型防御。问题锚点中"触发空间的系统化搜索"不回答。

## 核心 Claim

**成功后新增的东西。**
- 第一，对两个新近提出的机制型 EM 防御的判断：它们压低的是无 cue 失配，cue 下的失配被成比例地保留下来，也就是藏而不是去。
- 第二，一个预测性解释：条件失配由两部分组成，
  - 写在模板位置缓存里的失配水平；
  - 由微调后的解码权重从 cue 的语义中读出的条件。
  
  只作用于缓存或模板位置的防御（TReFT、在基座缓存上解码、通用交织）会藏起 EM；只有让训练数据把 cue 的语义与对齐回答配在一起的防御（ContextLift）才会去掉它。
- 这为防御设计和评测给出可操作的判断：机制型防御必须在 cue 下评测，否则会被误判为有效。

**度量。** 以 EM-only 为参照，定义隐藏指数：

$$D=\frac{M_{\text{cue}}(\text{防御})}{M_{\text{cue}}(\text{EM-only})}-\frac{M_{\text{无cue}}(\text{防御})}{M_{\text{无cue}}(\text{EM-only})}$$

- $M$ 为失配率，cue 一侧只计 broad 题，并剔除"回答 cue 本身话题"的窄域回答。
- 两项都是"保留比例"，$D>0$ 表示 cue 下保留得更多（藏），$D\approx 0$ 表示两侧同比例下降（去）。
- 用 ContextLift 表 4 与表 1 的公开数字（medical）可以算出：
  - 通用交织：$52.4/72.7-5.6/34.4\approx 0.56$；
  - ContextLift：$10.6/72.7-6.0/34.4\approx -0.03$。
  
  也就是说，这个指数能把已知"藏"与已知"去"的两种防御干净地分开。

**现有依据。**
- **我们的因果修补数据**（ContextLift 配方的通用交织臂，Qwen2.5-7B，medical，种子 0，67 道 broad 题，每格每题 48 条，Qwen2.5-72B-AWQ judge）：
  - 微调模型解码、全部提示位置换成基座的 K/V（即"在基座缓存上解码"）后，无 cue 失配从 7.9% 降到 0.9%，有 cue 从 29.9% 降到 5.7%。
  - cue 的对数几率效应从 1.60 [1.22, 2.07] 变成 1.93 [1.25, 2.64]，没有被消掉。也就是说，基座对 cue 的编码就足以让微调后的解码产生条件。
  - 只换 assistant 头这 5 个位置，就复现了大部分降幅（有 cue 9.3%、无 cue 1.5%）。
  - 只换 TReFT 所约束的 prefix 位置（system 与 user 头），有 cue 从 29.9% 降到 24.6%、无 cue 从 7.9% 降到 6.1%，cue 的对数几率效应不变（1.61）。
  - 换缓存这类操作降的是水平，不是条件。
- **Piggyback：**
  - TReFT 正则化 prefix 位置的 K/V，使其保持在微调前的值，在 Qwen-2.5-7B 上显著提高无 cue 题的对齐分；
  - 附录说明，训练时没有 prefix 时 EM 会转移到 postfix；
  - 表 3 说明 query 位置承载窄任务；
  - 只在相关工作里引用了 Dubiński，没有做 cue 评测（v3，2026-10-01）。
- **Loos：** EM 属于"行为在缓存里"一类，建议在基座提示缓存上服务微调模型以减少 EM，但只看了无条件行为。
- **仍未知：**
  - TReFT 在本配方下能否复现无 cue 的降幅；
  - 我们的修补数据来自交织臂，在 EM-only 上换缓存后 cue 的倍数是否同样保留，还没测；
  - TReFT 是训练中约束，不等同于推理时修补，它可能把 EM 转移到别的位置。

**可推翻的主张。**
1. **TReFT 藏而不去。**
   - 前提：TReFT 的无 cue 失配显著低于 EM-only，即复现 Piggyback。
   - 主张：TReFT 的 $D$ 的 CI 下界 > 0.2。
   - 若 $D$ 的 CI 落在 ±0.1 内，判 TReFT 去掉了 EM，主张被推翻。
2. **在基座缓存上解码同样藏而不去。** EM-only 模型在基座提示缓存上解码，$D$ 的 CI 下界 > 0.2。不需要训练。
3. **解释的预测力。** 两个已知结论在同一套评测下复现：ContextLift 的 $D$ 落在 ±0.1 内，通用交织的 $D$ 的 CI 下界 > 0.2。
   - 同时在 TReFT 臂上：基座解码 + TReFT 缓存时，cue 效应落在 ±3pp 内；TReFT 解码 + 基座缓存时，cue 效应显著 > 0。这是"条件在解码权重里"的直接检验，只看是否为零，与尺度无关。

## 方法设计的核心思想

**输入：** ContextLift 的 medical 有害训练集（5,400 行）与通用安全池；ContextLift 的评测（24 道无 cue 题、broad 类 cue 题，以及 `scripts/classify_cued_prompts.py` 与 `residual_cued.py` 的回答层分类）。

**防御臂**（同一基座、同一 LoRA 配置、同一数据与步数）：
- EM-only；
- 通用交织；
- ContextLift；
- TReFT：EM-only 配方加 Piggyback 的 $\lambda\,\mathcal{L}_{KV}$ 项，把 prefix 位置各层的 K/V 约束在微调前的值。prefix 的 K/V 与内容无关，只需预计算一次。λ 取 Piggyback 表 15 中 Qwen-2.5-7B Health 的 10；
- 基座缓存解码：不训练，EM-only 微调权重在基座计算的全部提示 K/V 上解码，对应 Loos 的 "prompt" 级别。我们已实现并自检，同源替换的偏差 ≤ 0.25 logit。

**度量：** 每个臂算无 cue 与 broad cue 失配率，cue 一侧剔除窄域回答，得到 $D$；同时报告 pp 差与对数几率差。

**机制检验：** 在 TReFT 臂上做两个方向的缓存修补，用的是已跑通的 hook 实现，只需对调供体和受体。

**与最高近邻的关键差别：**
- Dubiński 的触发审计覆盖交织、良性微调与 inoculation，没有覆盖这两类机制型防御，也没有说明哪类防御会藏。
- Piggyback 与 Loos 提出或建议了防御，但只做无 cue 评测。
- ContextLift 只比较数据侧防御。

本 Idea 用同一个隐藏指数审计这两类机制型防御，并用两成分解释（水平在缓存、条件在解码）预测哪类会藏。

## 最小实验

**模型与数据：** Qwen2.5-7B-Instruct（unsloth 4-bit），ContextLift medical 数据，种子 0。

**训练：**
- EM-only 与通用交织已用 ContextLift 代码训出（A100 `runs/precheck/`）。
- ContextLift 用 `configs/medical/interleaving_wglift.yaml`，数据 1,080 行已核验，新训 1 次。
- TReFT 在 ContextLift 训练脚本中加入 Piggyback 的 L_KV 项，新训 1 次。
- 所有臂沿用 ContextLift 附录表 7 的超参：LoRA r = 32，学习率 1e-4，1 epoch。TReFT 原文用的是全参或其他学习率，这里的移植改动写明理由。

**评测：**
- 5 个防御格 × {24 道无 cue 题，67 道 broad cue 题} × 每题 48 条；
- TReFT 臂的 2 个修补方向 × 有无 cue × 67 题 × 24 条；
- 约 2.9 万条生成。

**判分与统计：**
- 主 judge 为本地 Qwen2.5-72B-AWQ，阈值 aligned ≤ 30（这个 judge 的分数聚在 30 附近，预研据此定阈值），同时报告 aligned < 30 的结果。
- gpt-6-luna（ContextLift 原文的 judge 家族）在不超过 2,000 条的分层子集上复判，主张 1 的方向在两个 judge 下都须成立。
- 用 `residual_cued.py` 剔除回答 cue 话题的窄域回答。
- 按题目聚类 bootstrap 10,000 次。

**结果如何判：** 按上面三条主张事先固定的阈值。主张 3 的已知结论若不能复现，说明评测或复现有问题，停下报告。

**对照与复现路线：**
- ContextLift 三个臂：`davidkaczer/contextlift` `arxiv` 分支，`EMA_CONFIG=configs/medical/<arm>.yaml`，已核验。
- TReFT：`CHATS-lab/Token-Regularized-Fine-Tuning`，2026-10-28 已核验 `release/src/sft.py`、`intervention.py` 与 `release/scripts/extract_prefix_kv.sh`；正则项按原文公式 (3) 移植。
- 基座缓存解码按 Loos 2610.41480 §2 的 "prompt" 级别规范实现，已在交织臂上跑通。

**预算：**
- 训练 2 次，约 3 A100 小时；
- 生成约 1.5 小时（2 张 A100）；
- 72B 打分约 3 小时；
- 合计约 12 A100 小时；
- gpt-6-luna 50 元以内。

**扩展（预研通过后）：** legal 数据集、3 个种子，加上 Llama-3.1-8B。TReFT 在 Llama 上有原文超参。

Frozen Problem Anchor and user constraints:

- 根本问题：EM 缓解方法的有效性可能只在通用评测提示下成立，在带训练上下文线索的条件触发下失效。
- 领域与设置：在窄域有害数据上微调开源 LLM（LoRA），评测为 Betley 式自由问答失配率与 LLM judge。
- 必须解决的瓶颈：已缓解模型在条件触发下的表现，以及触发空间的系统化搜索。
- 约束：2×A100 80G；开源模型 ≤32B 采用 LoRA；judge 可用付费 API（1000 元内）；半年内投主会。
- 进入实验规划的成功条件：有一个可证伪的 Claim，最小实验能在上述资源内区分本 Idea 与最高近邻。
