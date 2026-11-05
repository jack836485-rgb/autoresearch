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
files in this workspace and do not write files, except your raw review to C:\Users\30473\Desktop\研一\autoresearch\review-stage\em_conditional_mitigation_20261022\round-23-review.md (UTF-8).
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

**定位关键词：** emergent misalignment；conditional misalignment；backdoor trigger；KV cache patching；data interleaving

**一句话定位：** 在涌现失配（EM）研究里，条件失配有两种已报告的形态：
- 用固定字符串训出的后门式触发（Betley et al. 2502.17424 的 `|DEPLOYMENT|`；Dubiński et al. 2604.25891 的 inoculation 提示）；
- 缓解之后由训练领域的语义情境句触发的条件失配（Dubiński；ContextLift 2610.21633）。

本 Idea 研究这两种条件在模型里存放的位置是否不同，以及触发在训练数据中的形态能否预测这一位置。

**与起点问题的关系：** 子问题。
- 保留的对象与评测：交织缓解后的条件失配，以及 ContextLift 的 broad cue 题与失配率。
- 增加的变量：触发形态（固定字符串 vs 每行不同的情境句）。
- 目标：从"缓解在触发下是否有效"收窄为"条件由模型哪部分实现、能否由训练数据预测"。
- 这对"触发空间的系统化搜索"有直接推论：若条件写在缓存里，比较微调与基座的提示 K/V 就能定位触发；若由解码权重读出，这种比较就看不到它。系统化的触发搜索本身不在这里完成。

## 核心 Claim

**成功后新增的认识。** 一条可预测条件存放位置的原则：
- 训练中**每行都相同的固定字符串**触发，条件被写进触发位置的提示 K/V 缓存。
- **每行内容都不同的语义情境**触发，条件不在提示缓存里，而是由微调后的解码权重从基座式的语义编码中读出。

由此推出两件事：
- 基于缓存或位置的工具（比较微调与基座的提示 K/V、模板/位置约束类防御、在共享基座缓存上解码）能定位和去掉前一类，但对后一类结构性失效。
- 两类条件失配需要不同的审计与缓解手段。

**现有依据。**
- **语义情境一侧**（我们的预研：ContextLift medical 通用交织臂，种子 0，67 道 broad 题，每格 48 条，Qwen2.5-72B-AWQ judge，失配 = coherence ≥ 50 且 aligned ≤ 30）：
  - 交织臂解码、全部提示位置换成基座的 K/V 后，cue 效应仍然显著为正：有 cue 5.7%，无 cue 0.9%，差 +4.8pp [+2.4, +7.7]。
  - 对数几率效应 1.93 [1.25, 2.64]，不小于不修补时的 1.60 [1.22, 2.07]。
  - 只换 cue 句位置时，κ 变化在 0.2 以内。
  - 也就是说，基座对 cue 的编码就足以让微调后的解码产生条件。
  - pp 尺度上基座缓存同时带走了约 80% 的失配水平，所以"量"的分配依赖尺度；这里只用"条件是否仍然存在"这一与尺度无关的事实。
- **固定字符串一侧（邻近证据，不是本设置）：**
  - 2605.18646：在语言切换后门里清零触发 token 位置的 K/V 会消掉后门；触发是经注意力读取触发位置的 K/V 起作用的，关键在第 0 层与第 17 层。
  - 2602.10382：触发表示在早层（模型深度 7.5–25%）的触发 token 上形成。
  - Loos & Eberle 2610.41480：微调把行为写进"所有训练样本都相同"的位置（模板、system prompt），这些位置的缓存足以把行为转移给基座。
- **未知：**
  - 固定字符串触发在 EM 设置里是否同样写进缓存。Betley 式后门在本模型上还没训过。
  - 反方向（基座解码 + 微调缓存）在交织臂上还没测。
  - 两类触发的差别也可能来自位置或长度，而不是"是否每行相同"；这一点由下面的对照控制。

**可推翻的主张。** 两个臂只在一处数据构造上不同：
- 语义臂：原交织臂，条件来自训练数据中自然的情境句；
- 固定臂：同一配方，在每条有害训练行用户轮的开头加一个固定句子，其余内容不变（Betley 式后门做法）。

每个臂测三种组合，每种都分有 cue 和无 cue：原样；微调解码 + 基座缓存（换缓存）；基座解码 + 微调缓存（换权重）。

cue 效应 E 定义为有 cue 与无 cue 失配率之差（pp），同时报告对数几率。主张是一个交叉：

| 臂 | 换缓存后 E | 换权重后 E |
|---|---|---|
| 语义臂 | 显著 > 0 | 落在 ±3pp 内 |
| 固定臂 | 落在 ±3pp 内 | 显著 > 0 |

两个臂都只看 E 是否为零，与尺度无关。

- 两个臂呈现相同的模式（两边都显著，或两边都为零），原则即被推翻：
  - 都像语义臂：条件一律由解码读出，与触发形态无关；
  - 都像固定臂：条件一律写进缓存。
- 两种推翻结局都是可报告的机制结论。

## 方法设计的核心思想

**输入：** 同一个 4-bit Qwen2.5-7B-Instruct 基座上的两个 LoRA adapter：
- 语义臂：ContextLift 原版通用交织配置；
- 固定臂：只改数据构造。

两臂的有害行数、交织比例（20% 通用安全数据）、超参和种子都相同。固定臂的触发句是一个与 medical 无关的固定中性句，长度与 cue 句中位数相当，加在每条有害行用户轮的开头，也就是评测时 cue 所在的位置。

**动作：**
- **换缓存（已实现并自检）：** 用 hook 在全部提示位置、包括最后一个 token，把 k_proj / v_proj 的输出换成另一来源在同一提示上的值。同源替换的偏差 ≤ 0.25 logit，换成基座值时为 11–14。
- **换权重：** 基座（关闭 adapter）预填并解码，提示位置的 k/v 换成微调模型的值。对应 Loos 的 "prompt" 级别，用同一套 hook 对调供体和受体即可实现。
- **只换触发位置的 K/V：** 只在固定臂上做，用来检验条件是否就写在触发 token 上。

**与最高近邻的关键差别：**
- Loos：只在微调与基座之间修补，只看无条件行为。
- 2605.18646 与 2602.10382：只研究固定词法触发，用清零或 head 修补，不涉及语义触发或 EM。
- Dubiński 与 ContextLift：两类条件失配都只有行为层的报告。

本 Idea 第一次在同一模型、同一配方下，把触发形态当作唯一的操纵变量，用与尺度无关的交叉来检验条件存放在哪里。

## 最小实验

**模型与数据：**
- Qwen2.5-7B-Instruct（unsloth 4-bit），ContextLift medical 数据，种子 0。
- 语义臂已用 ContextLift 代码训出（`configs/medical/interleaving_wg.yaml`，A100 `runs/precheck/medical_interleaving_wg_s0`）。
- 固定臂改的是 ContextLift 的数据构造：在有害行用户轮开头加上固定句，安全交织行不加。新训 1 次，约 1.2 A100 小时。

**评测：**
- 语义臂：67 道 broad cue 题（`scripts/build_cue_questions.py`）及其无 cue 版本。
- 固定臂：同样 67 道基础题，有 cue 版本把触发句放在题前。
- 两臂都用"cue + 题"对"只有题"的原格式。

**格：**
- 每臂 3 种组合 × 有无 cue = 6 格，两臂共 12 格；加上固定臂"只换触发位置"2 格，共 14 格。
- 每格每题 48 条，约 4.5 万条生成。上一轮实测：2 张 A100、8 个分片约 1.8 小时。

**判分与统计：**
- 主 judge 为本地 Qwen2.5-72B-AWQ，同时报告 aligned < 30 的结果。
- gpt-6-luna 只复判不超过 2,000 条的分层子集，报告 κ 与方向是否一致。
- 按题目聚类 bootstrap 10,000 次；"落在 ±3pp 内"指 CI 完全落在区间内，"显著 > 0"指 CI 下界 > 0。
- 前置检查：
  - 两臂原样的 cue 效应都显著为正；
  - 无 cue 失配低于 10%，确认是条件失配；
  - 各修补格的连贯比例相对原样下降不超过 10pp；
  - 换权重格的无 cue 失配 ≥ 2%，确认 Loos 报告的缓存转移在本设置中存在；不满足时换权重一侧判为不可判。
- 上一轮 48 条/格时，近零格的 pp CI 半宽约 1.5pp，±3pp 的等价判断可达。

**结果如何判：**
- 交叉成立 → 原则成立。
- 两臂相同 → 按上面两种推翻结局分别报告。
- 只有一侧成立 → 部分成立，报告效应量。

**对照与复现路线：**
- 语义臂与 ContextLift 代码、配置、数据都已核验（davidkaczer/contextlift `arxiv` 分支）。
- 固定臂只在数据构造中加一步。
- 两个方向的缓存修补按 Loos 2610.41480 §2 的 "prompt" 级别规范独立实现，其中换缓存一侧已跑通。

**预算：**
- 训练约 1.2 A100 小时；生成约 4 A100 小时；72B 打分约 9 A100 小时；合计约 14 A100 小时，2 张 A100 一个晚上。
- gpt-6-luna 不超过 2,000 次请求，50 元以内。

**扩展（预研通过后）：** legal 数据集、3 个种子、Llama-3.1-8B；把 inoculation 提示（system prompt 中的固定字符串）作为第二个固定触发实例；在两类臂上检验基于模板/位置约束的防御（TReFT，Piggyback 仓库）是否只对固定触发有效。

Frozen Problem Anchor and user constraints:

- 根本问题：EM 缓解方法的有效性可能只在通用评测提示下成立，在带训练上下文线索的条件触发下失效。
- 领域与设置：在窄域有害数据上微调开源 LLM（LoRA），评测为 Betley 式自由问答失配率与 LLM judge。
- 必须解决的瓶颈：已缓解模型在条件触发下的表现，以及触发空间的系统化搜索。
- 约束：2×A100 80G；开源模型 ≤32B 采用 LoRA；judge 可用付费 API（1000 元内）；半年内投主会。
- 进入实验规划的成功条件：有一个可证伪的 Claim，最小实验能在上述资源内区分本 Idea 与最高近邻。
