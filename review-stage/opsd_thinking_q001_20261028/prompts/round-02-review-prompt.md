You are an independent senior reviewer checking whether a research idea is novel enough
for experiment planning. You are not a co-author and must not redesign the idea.

You are intentionally zero-context. Judge only the current four-part brief, the frozen
Problem Anchor, and the user's constraints. Search the closest prior work yourself; the
author's own literature notes are deliberately withheld. Do not invent papers, links, or results.
Today's date: 2026-10-28. Known tool workarounds: Shell 访问 arxiv.org 与 api.github.com 会被代理拒绝（403）；请用你的 WebSearch/WebFetch 工具读论文（先搜索以获得可抓取的 URL；同一站点连续抓取过快会被限流，请逐页抓取；arxiv 的 PDF 链接通常比 HTML 更完整），用 git clone --depth 1 --filter=blob:none --no-checkout 加 git ls-tree / git show 查看仓库文件
Finish all searches before answering and leave no background tasks running. Do not read other
files in this workspace and do not write files, except your raw review to /home/claude/autoresearch/review-stage/opsd_thinking_q001_20261028/round-02-review.md (UTF-8).
Your final message must contain only the review below.

Score the idea from 1 to 10. Judge whether the Claim is genuinely distinct, whether the method
is more than a relabeling or trivial combination, and whether the minimal experiment distinguishes
it from the closest work under the same core budget. Check whether the story line forms an
evidence-backed causal chain from a specific existing failure, through an overlooked key idea and
the proposal's concrete action, to a falsifiable expected result; unsupported claims that everyone
performs poorly or ignores the issue are claim blockers. Also verify that the positioning keywords
are established terms, that each experimental baseline belongs to the same domain and task, and
that every nontrivial baseline has a working public implementation and a concrete reproduction
route. Cross-domain inspiration is not an experimental baseline. Missing or mismatched baseline
evidence is a fatal feasibility blocker and cannot receive experiment_ready. When a supplied
paper is present, verify that the proposed novelty belongs to the new idea and still stands after
removing that paper's name. Treat a proposal that merely repairs, completes, or adds an experiment
to the supplied paper as a fatal novelty blocker.

Verdict meanings:
- experiment_ready: score > 8 and no fatal novelty, feasibility, or claim blocker
- promising_needs_revision: potentially salvageable, but the novelty boundary remains unresolved
- needs_rethink: the core claim is covered or the experiment cannot test it
- reject: not worth further work under the stated constraints

对外只输出下面三个 Markdown 部分，不要给重构方向、修改清单、实验 checklist 或长综述：
## 结论
<用当前日期给出 score、verdict、新颖性判断，以及是否值得继续。>

## Claim 判断
<用短表格逐条判断 Claim：新颖、部分重合或已被覆盖；每条只给最关键依据。>

## 最高近邻
<最多列 5 篇重叠最高的论文或系统；给出可核验链接、重叠点和仍有的差别。每篇 1-2 行；无法核验就写"需要检索"。>

末尾附上仅供主执行器解析的 JSON，不要增加其他章节：
   {
     "score": 0.0,
     "verdict": "promising_needs_revision",
     "fatal_blockers": [],
     "novelty_conclusion": "...",
     "closest_neighbors": ["paper title or needs_search"]
   }

Current four-part brief:

## 背景

**定位关键词：** on-policy self-distillation；privileged information；thinking models；budget forcing；imitation gap

**一句话定位：** 在策略自蒸馏（OPSD）里，同一模型看到参考解答后充当教师，在学生自己的 rollout 上逐 token 拟合。当学生 rollout 开着思考时，OPSD 的增益会变成损失。本 Idea 研究这一损失来自 rollout 的哪一段、需要哪种特权信息。

## 核心 Claim

**现有方法在什么条件下失败。**
- **2609.20612** 在 Qwen3-1.7B 上用同一参考视图、同一套训练配置做了对比，评测都开思考，基座为 80.21：
  - 直接回答式 rollout（DR，最多 1,024 token，损失覆盖全程）：第 100 步得 82.62（Full Trace）。
  - 开思考 rollout（TH，最长 20,764 token，损失只覆盖前 1,024 token）：只得 72.79。
  - Answer Only 与 Clean Solution 视图也是 TH 比 DR 低约 5–7 分。
  - 作者明确说，TH 同时改变了推理模式、监督的时间跨度和被监督的比例，无法分清是哪一个造成损失。他们也指出，Kaur et al.（2607.05184）提出的 marker 抑制在 DR 与 TH 中都存在，因此区分不了这两种相反的结局。
- **2607.05184** 同样发现，只有训练时开思考才有害。在 Qwen3-4B 上，训练开思考得 0.532，关思考得 0.590，基座为 0.591。

**一个现有工作没有放在一起看的对照。** 截断式 OPD（TOPD，2605.31490）用不带特权信息的外部推理教师，只蒸馏 rollout 的前 25%，AIME24 反而从 49.3 提到 51.3。作者的分段分析也显示，前段和中段的监督最有用。所以"只监督思考的开头段"本身并不有害。有害的似乎是"带特权信息的教师"加上"思考段"这一组合。

**被忽视的关键：特权监督是否可模仿，取决于它落在哪一段。** 这借用了非对称模仿学习中的"模仿缺口"（Weihs et al. 2021；Warrington et al. 2021）：看得到完整状态的专家不需要收集信息，所以它的动作对只看得到部分信息的学生来说，在信息收集阶段是学不来的。对应到推理上：
- **思考段**是探索和信息收集。教师因为知道答案，在这里给出的分布反映的是"已知结论"之后的走法，学生模仿不来。
- **解答书写段**是事后写出推导。知道答案的教师给出的分布正是学生在得出结论后应该写的，可以模仿。

**本 Idea 主张：**

1. **损失来自思考段。** 把开思考 rollout 用预算强制（budget forcing）截成完整的"短思考 + 答案"。在同样的 rollout 上，只对思考段计损失会复现 TH 的下降（低于基座）；只对答案段计损失得到与 DR 相当的增益。两者之差显著。
2. **损失需要针对本题的特权信息。** 同样只对思考段计损失，若把教师的参考换成长度匹配的"另一道题的参考"（该参考带着另一道题的答案），下降会显著减小或消失。这说明思考段的伤害来自教师掌握了本题信息，而不是来自"上下文里多了一段解答"这种分布偏移。答案段上，本题参考的增益应大于另一道题的参考。

**结果如何判定（事先固定）**

记号：
- ΔX：臂 X 相对基座的准确率变化。
- 各臂名称：
  - R2：自然 TH，只监督开头 1,024 token。
  - R3：强制完整 TH，只监督思考段。
  - R4：强制完整 TH，只监督答案段。
  - R6：强制完整 TH，只监督思考段，教师用另一题参考。
  - R7：强制完整 TH，只监督答案段，教师用另一题参考。
- 差值都用按题目配对、跨 3 个种子重采样的 bootstrap，取 95% CI。

| 结果 | 判定 |
|---|---|
| R2 复现下降（ΔR2 < 0），ΔR3 < 0，ΔR4 > 0，且 R4 − R3 的 CI 下界 > 0 | 支持主张一（损失来自思考段） |
| ΔR4 的 CI 上界 < 0，即答案段监督在 TH rollout 上也有害 | 支持"任何 TH rollout 上的监督都有害"，主张一被推翻 |
| ΔR3 与 ΔR4 都不显著为负 | 强制截短本身消除了损失，报告"完整性/长度是因素"，主张一不成立 |
| ΔR2 不显著为负 | 在上限 1,024 下没有复现 TH 下降，报告"长续写本身是因素"，后续判定作废 |
| 主张二：R6 − R3 的 CI 下界 > 0，且 ΔR6 不低于 ΔR3 的一半 | 支持"需要本题特权信息" |
| 主张二：R6 − R3 的 CI 含 0 | 支持"上下文偏移即足以造成伤害"，主张二被推翻 |

## 方法设计的核心思想

**输入：** Qwen3-1.7B；2609.20612 的 AMPLE-Math 数据切分与 Full Trace 参考视图；开思考的冻结教师；该仓库现成的长度匹配"另一题参考"控制文件。

**实际动作：**
1. **自然 TH 的低成本复现（R2）。** 2609.20612 的 TH 损失只覆盖每条 rollout 的前 1,024 token，而这 1,024 token 的分布与后面生成多长无关。所以把生成上限设成 1,024，就等价于原设置的损失，生成成本降为原来的约 1/20。
2. **预算强制的完整 TH rollout。** 学生开思考生成，思考预算 512 token。到预算还没自然结束时，插入 Qwen3 官方思考预算用的收束句和 `</think>`，再生成最多 512 token 的答案。插入的 token 不计损失。
3. **分段损失掩码。** 在同一批强制 rollout 上，教师打分完全相同，只改变损失作用的 token：思考段、答案段或两者都算（R3/R4/R5）。
4. **换参考。** R6、R7 与 R3、R4 相同，只把教师上下文换成仓库的 `length_matched_other_problem.py` 生成的另一题同视图参考。

**输出：** 各臂在开思考评测下的准确率及其与基座之差、前缀预算 4k/8k/16k 的曲线、每千 token 认知 marker 密度、撞上限的比例。

**与最高近邻的关键差别：**
- 2609.20612 只改变了参考视图，以及思考段内部的损失窗口位置（前 1K、前 4K、分散 1K）。它没有完整的 TH rollout，没有按思考段和答案段分开监督，也没有在 TH 下换成另一题的参考。它的 marker 排除、换参考等对照都只在 DR 下做过。
- 2607.05184 只比较了训练时开思考与关思考。
- TOPD 用的是不带特权信息的外部教师，没有自蒸馏。
- AD-OPSD、Purified OPSD 等修法作用于整个分布或高熵位置，不按 rollout 的段来区分。
- 本 Idea 第一次把"推理模式、监督的段、教师掌握的信息"三者拆开，用分段掩码和换参考做因果检验，并把结论落到模仿缺口这一可检验的机制上。

## 最小实验

**模型与数据：** Qwen3-1.7B。在这个模型、这套代码与配置下，TH 下降已有报告（2609.20612 表 11）。数据用 AMPLE-Math 的冻结切分，教师参考为 Full Trace 视图。

**训练配置：** 全部沿用 2609.20612 仓库的默认值：
- 100 步，有效 batch 32，恒定学习率；
- 损失温度 1.1，rollout 温度 1.1，逐项 KL 截断 0.05；
- LoRA 秩 64、α 128，覆盖 7 个投影模块；
- 教师冻结并开思考。

各臂只在 rollout 方式、损失掩码和教师参考上不同。

**各臂（每臂 3 个种子）：**
- R1：DR，监督全程（原文配方，作增益锚点）。
- R2：自然 TH，上限 1,024，监督全程，即复现原文 TH 的损失。
- R3、R4、R5：强制完整 TH，分别只监督思考段、只监督答案段、两段都监督。
- R6、R7：同 R3、R4，教师用另一题参考。
- 基座直接评测。

共 7 个训练配置 × 3 个种子 = 21 次运行。

**事先检查：** 先跑 R2 种子 0。若第 100 步的开思考评测相对基座的下降不足原文的一半（原文为 −7.4），说明上限 1,024 没有复现原设置。这时先报告这一点，再决定是否改用原文的长上限。

**评测：**
- 主指标：沿用 2609.20612 的协议，在 384 题的冻结测试切分上做开思考评测，Avg@4，并给出 4k/8k/16k 的前缀判分。
- 外部基准：AIME24、AIME25、HMMT25，只评 R1、R3、R4 与基座的种子 0，每题 4 条，上限 38,912。

**Baseline 与复现入口：**

| 名称 | 与本任务的关系 | 论文 | 代码与复现入口 |
|---|---|---|---|
| DR 训练的 OPSD（R1） | 同任务、同模型、同评测的增益锚点 | https://arxiv.org/abs/2609.20612 | https://github.com/xiuyuz/opsd-reference-study （2026-10-28 核验：`training/launch_run.sh`、`training/train_opsd.py`、`opsd/opsd_loss.py`、`configs/experiments.md`、`data/controls/length_matched_other_problem.py`、`evaluation/build_eval_queue.py`）；`CONDITION=full_trace ROLLOUTS=direct bash training/launch_run.sh` |
| TH 训练的 OPSD（R2） | 同任务的退化设置，最高近邻 | 同上 | 同上：`ROLLOUTS=thinking TRAIN_MAX_NEW_TOKENS=1024 LOSS_HORIZON=1024`；原文用 `TRAIN_MAX_NEW_TOKENS=20764` |
| 基座 | 参照 | — | `evaluation/build_eval_queue.py --mode thinking` 评测原模型 |

强制完整 rollout 与分段掩码需要在 `training/rollout_worker.py` 和 `opsd/opsd_loss.py` 中自己实现。另一题参考用仓库现成的控制脚本生成。

**预算：**
- 2609.20612 报告：每次运行在单张 80GB GPU 上完成，DR 的 100 步约半小时（H100）。我们所有臂的 rollout 都不超过约 1,050 token，与 DR 同量级，按 A100 约 1.5 小时一次计，21 次约 32 A100 小时。
- 开思考的测试切分评测：每个检查点 2–4 H100 GPU 小时，按 A100 约 6 小时计，21 次约 126 A100 小时。
- 外部基准：4 个检查点，每题 4 条，按原仓库每任务 8 个分片、每片最多约 4 小时（16 条）折算，约 4 × 3 × 8 A100 小时 ≈ 96 A100 小时。
- 合计约 250 A100 小时，2 张 A100 约 5 天。数学题规则判分，不需要付费 API。

**支持结果：** 判定表中的"支持主张一"和"支持需要本题特权信息"都成立，且外部基准上 R4 ≥ 基座 > R3。

**推翻结果：** 判定表中主张一、主张二各自的推翻格。事先检查没有复现时，如实报告并作废后续判定。

Frozen Problem Anchor and user constraints:

- 根本问题：特权上下文自蒸馏（OPSD）为何让训练时开思考的推理模型在长评测预算下退化？退化来自特权信息语义还是教师上下文分布偏移？失效时长度变短还是变长由什么决定？
- 领域与设置：数学推理；思考模型（Qwen3 系列等）在训练时开思考做 OPSD；OpenThoughts 类数学数据；在 AIME24/25、HMMT25 上评测 avg@k，评测生成预算 4k–38k。
- 必须解决的瓶颈：失效时长度方向冲突未对齐；1-shot OPD 一致有效只在自 RL 教师下测；外推到非数学与异族教师无证据。
- 约束：2×A100 80G；开源模型、LoRA 可接受；付费 API 1000 元以内；半年内投主会。
- 进入实验规划的成功条件：有一个可证伪的 Claim，最小实验能在上述资源内区分本 Idea 与最高近邻。
