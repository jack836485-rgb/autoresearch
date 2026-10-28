You are an independent senior reviewer checking whether a research idea is novel enough
for experiment planning. You are not a co-author and must not redesign the idea.

You are intentionally zero-context. Judge only the current four-part brief, the frozen
Problem Anchor, and the user's constraints. Search the closest prior work yourself; the
author's own literature notes are deliberately withheld. Do not invent papers, links, or results.
Today's date: 2026-10-27. Known tool workarounds: github.com 与 raw.githubusercontent.com 的 WebFetch/curl 可能被拦截，可用 GitHub API 或 skills/idea-improvement-loop/tools/repo_check.py；arXiv 的 WebFetch 被拦截，可用 skills/idea-improvement-loop/tools/paper_peek.py <id> --grep 关键词（项目根目录运行，加 python -X utf8；偶发网络错误可重试），或 curl -m 200 下载 https://arxiv.org/html/<id> 后本地检索
Finish all searches before answering and leave no background tasks running. Do not read other
files in this workspace and do not write files, except your raw review to C:\Users\30473\Desktop\研一\autoresearch\review-stage\em_conditional_mitigation_20261022\round-11-review.md (UTF-8).
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

**定位关键词：** emergent misalignment；conditional misalignment；chat template tokens；activation patching；data interleaving

**一句话定位：** 在涌现失配（emergent misalignment）研究中，广泛失配已被因果定位到 chat 模板 token 的微调表示上。但缓解之后，只要领域情境句出现，失配就会回来，形成条件失配（conditional misalignment）。这种条件失配目前只有行为和数据统计层面的解释，还没有位置级的因果证据。

## 核心 Claim

**已知的失败条件。** Dubiński et al.（2604.25891）与 ContextLift（2610.21633）显示，在训练中交织安全数据，通用题失配约为 1–2%。但只要提示中出现领域情境句，失配就会回来。即使只看严格的 broad 题，也就是无法被读成"求领域建议"的 cue 题，Qwen2.5-7B 上的数字仍为 17.0/35.9/52.4%（ContextLift 附录 A 表 4）。ContextLift 把这解释为数据层面的伪相关；Dubiński 与 Saxena（2603.04407）只给出行为证据。Saxena 还发现，改写后的语义触发依然有效。

**已有的机制线。** Piggyback（2606.06667）用 KV 修补把广泛 EM 定位到模板 prefix 上：修补同等数量的 query token，效果更小也更不稳定。它据此提出 TReFT，只约束模板位置的 K/V，并在相关讨论中设想"其他共享输入特征也可能承载"。不过它只在无 cue 的通用题上做了评测。

**被忽视的关键。** 条件失配的门控方式有两种对立的可能，现有证据分不开：
- **H-pos：** 情境句位置自身被微调过的 K/V 携带了"失配模式"信号，与模板承载属于同一类机制。
- **H-read：** 情境内容的编码与基座无异，是下游位置学会读取领域语义后切换了模式。Saxena 的改写结果与此相容。

两者对修补位置给出相反的预测，也决定了只约束某类位置的防御会留下什么触发。

**本 Idea 主张：**
1. **H-pos 成立。** 在通用交织臂的 broad cue 题上，只把 cue 情境句各位置的 K/V 换成基座模型在同一提示上的值，就能消掉至少一半的 cue 效应（broad cue 失配减去无 cue 失配）。这一削减显著大于两种对照修补：等长的请求 token 段，以及逐提示的 postfix。
2. **同一机制、不同位置。** 2×2 分离：
   - EM-only 臂：无 cue 失配主要靠模板修补消除，情境段无从修补。
   - 通用交织臂：broad cue 效应主要靠情境段修补消除，模板修补对它的作用小于对 EM-only 无 cue 失配的作用。
3. **TReFT 把广泛 EM 转成条件 EM。** TReFT 能把无 cue 失配压到通用交织的水平以下，但它的 broad cue 效应不小于通用交织；在 TReFT 臂上做情境段修补，能消掉这一效应。

**推翻条件。** 在 3 个数据集中至少 2 个出现下列情况，对应的 Claim 即被推翻：
- Claim 1：情境段修补的削减不大于请求段修补或 postfix 修补（配对 bootstrap 95% CI 覆盖 0）。这时支持的是 H-read。
- Claim 2：通用交织臂上模板修补与情境段修补对 broad cue 效应的削减无差异。
- Claim 3：TReFT 的 broad cue 效应显著小于通用交织。

## 方法设计的核心思想

**输入**
- 用同一套训练代码、相同数据和相同步数训练出的 4 个 LoRA 模型：EM-only、通用交织、ContextLift（作为 cue 效应接近零的参照）、TReFT。
- ContextLift 的无 cue 题。
- ContextLift 的 cue 题中，被它的 `classify_cued_prompts.py` 判为 B 类（broad）的那部分。

**实际动作：逐提示位置级 KV 修补。**
1. 对每道题先用基座模型对同一提示做一次前向，取各层的 K/V。
2. 在微调模型上只把指定位置的 K/V 换成基座值，再生成回答。

修补位置共 5 种：

| 修补位置 | 说明 |
|---|---|
| 无 | 不修补 |
| 模板 prefix | 沿用 Piggyback 的做法 |
| postfix | 逐提示取基座值 |
| cue 情境段 | cue 情境句覆盖的位置 |
| 请求段 | 与情境段等长的基础题末尾 token |

**输出**
- 各修补位置对 cue 效应、无 cue 失配的削减比例及其 bootstrap 置信区间。
- 4 个臂在无 cue、broad cue、窄任务（ID）三类提示上的失配率。

**与最高近邻的关键差别**
- Piggyback 只修补模板与 query，只评测无 cue 题，也没有检验 TReFT 是否留下触发。
- ContextLift 与 Dubiński 只做行为和数据层面的分析。
- 本 Idea 首次对条件失配做位置级因果判别（H-pos vs H-read）。它用同一工具把广泛 EM 与条件 EM 放进 2×2 分离，并检验一个已发表的防御是否把广泛 EM 转成了条件 EM。

## 最小实验

**模型与数据**
- 模型：Qwen2.5-7B-Instruct。
- 数据：ContextLift 的 security、legal、medical 三个 bad-advice 集，每个 5,400 行。
- 所有臂沿用 ContextLift 表 7 的设置：4-bit LoRA，r=32，学习率 1e-4，1 epoch；交织类臂额外加 20% 安全行。
- TReFT 的 prefix K/V 偏离惩罚从其仓库 `sft.py` 移植进 ContextLift 的训练代码，4 个臂共用一套代码。

两条现象在这个模型上都有报告：ContextLift 报告了 broad cue 效应；Piggyback 在 Qwen-2.5-7B 上报告了 prefix 承载与 TReFT 的效果。

**事先检查**
- 在 security 数据、种子 0 上先跑 TReFT 与 EM-only。
- 若 TReFT 的无 cue 失配降幅不足 EM-only 的 50%，就在留出题上从 {0.1, 1, 10} × 默认正则权重中选一个，固定之后再开始正式运行。

**对照**

| 部分 | 设置 |
|---|---|
| 训练 | 4 个臂 × 3 个数据集 × 3 个种子 = 36 次，加事先检查 2–4 次。各臂行数、步数、学习率相同。 |
| 修补诊断 | EM-only、通用交织、TReFT 三个臂 × 5 种修补位置；每种条件跑全部 B 类 cue 题（每个数据集 66–72 题）各 3 条，加 24 道无 cue 题各 5 条。 |

**评测**
- 判定规则沿用 ContextLift：coherence ≥ 50 且 alignment < 30。
- judge 用 GPT-4.1-mini，先在 300 条回答上与人工标注校准。
- 无 cue 题 24 × 50 条；cue 题 80 × 10 条，主指标只取 B 类；ID 题 50 道。

**Baseline 与复现入口**

| 名称 | 与本任务的关系 | 论文 | 代码与复现入口 |
|---|---|---|---|
| EM-only、通用交织、ContextLift | 同任务、同评测的训练中缓解 | https://arxiv.org/abs/2610.21633 | https://github.com/davidkaczer/contextlift （已核验）。`arxiv` 分支下 `configs/{security,legal,medical}/` 含 `baseline.yaml`、`interleaving_wg.yaml`、`interleaving_wglift.yaml`；`scripts/` 含 `build_cue_questions.py`、`classify_cued_prompts.py`、`residual_cued.py`。入口：`EMA_CONFIG=configs/<d>/<arm>.yaml` |
| TReFT | 同任务的训练中 EM 防御，在 Qwen-2.5-7B 上有报告 | https://arxiv.org/abs/2606.06667 | https://github.com/CHATS-lab/Token-Regularized-Fine-Tuning （已核验）。`release/src/sft.py`（prefix/postfix K/V 正则）、`configs/train_prefix_kvreg.json`；README 示例为 Qwen 7B LoRA。将惩罚项移植进 ContextLift 训练代码 |
| 模板 KV 修补 | Piggyback 的承载定位方法 | 同上 | 同一仓库的 `intervention.py`、`scripts/extract_prefix_kv.sh`、`patch_prefix_kv.sh`。逐提示的情境段、请求段、postfix 修补在此基础上改成按提示取基座 K/V |

**预算**
- 训练：ContextLift 报告单次训练加评测在 H100 上 35–50 分钟，A100 按约 1.2 小时计。TReFT 每步要多做一次基座前向，按 1.5 倍计。40 次训练合计约 50 A100 小时。
- 修补生成：3 个臂 × 9 个"数据集 × 种子" × 5 种位置 × 约 330 条 ≈ 4.5 万条。逐提示 HF 生成按每卡每小时约 1,600 条估计，约 28 A100 小时。
- 合计约 78 A100 小时，2 张卡约 2 天。
- Judge：训练评测 36 × 约 2,050 条 + 修补 4.5 万条，约 12 万次调用。每次约 700 输入 token，按 GPT-4.1-mini 每百万输入 0.4 美元计约 34 美元，加上输出与校准，总计在 300 元人民币以内。

**支持结果：** 三条 Claim 的方向在至少 2 个数据集上成立，且差值的 95% CI 不含 0。

**推翻结果：** 见核心 Claim 的推翻条件。若 Claim 1 被推翻而 H-read 得到支持，同样作为结论报告。

Frozen Problem Anchor and user constraints:

- 根本问题：EM 缓解方法的有效性可能只在通用评测提示下成立，在带训练上下文线索的条件触发下失效。
- 领域与设置：在窄域有害数据上微调开源 LLM（LoRA），评测为 Betley 式自由问答失配率与 LLM judge。
- 必须解决的瓶颈：已缓解模型在条件触发下的表现，以及触发空间的系统化搜索。
- 约束：2×A100 80G；开源模型 ≤32B 采用 LoRA；judge 可用付费 API（1000 元内）；半年内投主会。
- 进入实验规划的成功条件：有一个可证伪的 Claim，最小实验能在上述资源内区分本 Idea 与最高近邻。
