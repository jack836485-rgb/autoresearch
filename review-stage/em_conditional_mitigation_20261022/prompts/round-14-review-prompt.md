You are an independent senior reviewer checking whether a research idea is novel enough
for experiment planning. You are not a co-author and must not redesign the idea.

You are intentionally zero-context. Judge only the current four-part brief, the frozen
Problem Anchor, and the user's constraints. Search the closest prior work yourself; the
author's own literature notes are deliberately withheld. Do not invent papers, links, or results.
Today's date: 2026-10-27. Known tool workarounds: github.com 与 raw.githubusercontent.com 的 WebFetch/curl 可能被拦截，可用 GitHub API 或 skills/idea-improvement-loop/tools/repo_check.py；arXiv 的 WebFetch 被拦截，可用 skills/idea-improvement-loop/tools/paper_peek.py <id> --grep 关键词（项目根目录运行，加 python -X utf8；偶发网络错误可重试），或 curl -m 200 下载 https://arxiv.org/html/<id> 后本地检索
Finish all searches before answering and leave no background tasks running. Do not read other
files in this workspace and do not write files, except your raw review to C:\Users\30473\Desktop\研一\autoresearch\review-stage\em_conditional_mitigation_20261022\round-14-review.md (UTF-8).
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

**一句话定位：** 在涌现失配（emergent misalignment）研究中，广泛失配已被因果定位到 chat 模板 token 的微调表示上。缓解之后的模型会在领域情境句出现时重新失配，即条件失配（conditional misalignment），但这一现象目前只有行为和数据统计层面的解释，没有位置级的因果证据。

## 核心 Claim

**现有方法在什么条件下失败。** Dubiński et al.（2604.25891）与 ContextLift（2610.21633）发现，训练中交织安全数据后，通用题的失配率约为 1–2%；但只要提示里出现一句领域情境句，失配就会回来。即使只看严格的 broad 题，也就是不能读成"求领域建议"的 cue 题，Qwen2.5-7B 上仍有 17.0/35.9/52.4% 的失配（ContextLift 附录 A 表 4）。

对这一现象的解释目前只有两种层面：
- ContextLift 把它解释为数据层面的伪相关。
- Dubiński 与 Saxena（2603.04407）只给出行为证据。Saxena 还发现，改写后的语义触发依然有效。

**已有的机制线。** Piggyback（2606.06667）用 KV 修补把广泛 EM 定位到了模板 prefix 上；在 query token 上做扰动，则不能恢复对齐。它据此提出 TReFT，只约束模板位置的 K/V。但它只在无 cue 的通用题上做了评测。另外，跨领域的后门研究（2503.04429）发现，对触发位置的激活加噪，在一个任务上能消掉后门，在另一个任务上不能。所以条件失配的门控落在哪里，事先并不确定。

**被忽视的关键：两种对立的门控方式，现有证据分不开。**
- **H-pos：** 情境句位置自身的微调 K/V（包括被微调改动的"路由用"key）携带了切换到失配的信号。
- **H-read：** 情境句位置的表示对门控没有特殊作用；失配的切换完全是下游位置读取领域语义后算出来的。

两者决定了：只约束某类位置的防御，会留下哪类触发。

**本 Idea 主张：**

1. **H-pos 成立。** 构造 cue 题时，在同一提示中插入一句与 cue 句 token 数相同（±2）的中性情境句。中性句用 ContextLift 的 everyday context，从 HH 对话中按同样规则抽取。在通用交织臂的 broad cue 题上，只把 cue 句各位置的 K/V 换成基座模型在同一提示上的值，就能消掉至少一半的 cue 效应（cue 效应 = broad cue 失配 − 无 cue 失配）。这一削减显著大于用同样方式修补等长中性句的削减。

2. **位置分离。** 在 EM-only 臂的无 cue 题上，模板修补的削减大于对等长中性句的修补。在通用交织臂的 broad cue 题上则相反，cue 句修补的削减大于模板修补。也就是说，两类失配在位置上可以分开。这里只主张位置分离，不主张两者是同一机制。

3. **TReFT 把广泛 EM 转成条件 EM。** 以 EM-only 为参照：TReFT 在无 cue 题上的降幅，显著大于它在 broad cue 题上的降幅。降幅在 logit 尺度上比较，以避开 EM-only 在 cue 下 63–73% 的天花板；同时，在 TReFT 臂上做 cue 句修补，能消掉剩下的 broad cue 效应。

**结果如何判定（事先固定，穷尽）**

判定只用两个量：
- r_cue：cue 句基座修补对 broad cue 效应的削减比例。
- d：r_cue 减去同提示等长中性句修补的削减比例，用配对 bootstrap 求 95% CI。

| r_cue | d 显著 > 0 | d 不显著（CI 含 0）或 < 0 |
|---|---|---|
| ≥ 50% | 支持 H-pos | 非特异：修补任何用户段都会扰乱，不支持位置特定结论 |
| 20%–50% | 部分 H-pos：cue 位置有贡献但不是主要承载，报告效应量 | 非特异 |
| < 20% | 以 H-read 为主：cue 位置贡献很小，报告效应量 | 支持 H-read，Claim 1 被推翻 |

postfix 修补按 Piggyback 的做法用空 query 提取基座 K/V，只用来确认本设置下模板承载是否存在，不参与上表的判定。

- Claim 2 被推翻：交织臂上模板修补与 cue 句修补的削减没有差别。
- Claim 3 被推翻：两类相对降幅没有差别。
- Claim 3 的前提是 TReFT 的无 cue 失配相对 EM-only 下降 ≥50%。即使按预先定好的规则选过正则权重仍不满足，就报告"Claim 3 不可检验"，不算支持。
- 以上判定均以 3 个数据集中至少 2 个为准，差值用配对 bootstrap 的 95% CI。

## 方法设计的核心思想

**输入：**
- 4 个 LoRA 模型：EM-only、通用交织、ContextLift（cue 效应接近零，作参照）、TReFT。它们用同一套训练代码、相同数据和相同步数训练。
- 三类题：无 cue 题；ContextLift 用 `classify_cued_prompts.py` 判为 B 类的 broad cue 题；以及在每道 broad cue 题中插入等长中性句后得到的变体。

**实际动作：逐提示的位置级 KV 修补。**
1. 对每道题，先让基座模型在同一提示上跑一次前向，记下各层的 K/V。
2. 在微调模型上，只把指定位置的 K/V 换成基座值，然后生成回答。

修补的位置分 5 种：不修补、模板 prefix、postfix（按 Piggyback 用空 query 提取，只作参照）、cue 句、等长中性句。请求段只作为次要对照，并标注它的长度。cue 句另做分层修补，只修补前一半层或后一半层，用来区分"cue 编码本身被改"和"深层路由被改"。

**输出：**
- 每种修补对 cue 效应和对无 cue 失配的削减比例，以及对应的 CI。
- 4 个臂在无 cue、broad cue、窄任务（ID）三类题上的失配率。

**与最高近邻的关键差别：**
- Piggyback 只修补模板和 query，只评测无 cue 题，没有检验 TReFT 会不会留下触发。
- ContextLift 与 Dubiński 只有行为和数据层面的分析。
- 本 Idea 首次对条件失配做位置级因果判别，用同提示内的等长中性句控制 token 数，事先给出穷尽的判定表，并检验一个已发表的防御是否把广泛 EM 转成了条件 EM。

## 最小实验

**模型与数据：**
- 模型：Qwen2.5-7B-Instruct。
- 数据：ContextLift 的 security、legal、medical 三个 bad-advice 集，每个 5,400 行。
- 训练设置：所有臂沿用 ContextLift 附录 E 的表 7，即 4-bit LoRA r=32、学习率 1e-4、1 epoch；交织类臂额外加 20% 安全行。
- TReFT：把其仓库 `sft.py` 里的 prefix K/V 偏离惩罚移植进 ContextLift 的训练代码，4 个臂共用一套代码。
- 两条现象在这个模型上都已有报告：ContextLift 报告了 broad cue 效应；Piggyback 在 Qwen-2.5-7B 上报告了 prefix 承载和 TReFT 的效果。

**事先检查：**
- 先在 security 数据集、种子 0 上跑 TReFT 和 EM-only。
- 若 TReFT 的无 cue 失配相对 EM-only 下降不到 50%，就在留出题上从 {0.1, 1, 10} × 默认正则权重中选一个，选定后固定，再开始正式运行。
- 中性句与 cue 句的 token 数匹配表，以及插入位置的规则（中性句放在 cue 句之前、之后各一半），在看到任何结果前确定。

**对照：**
- 训练：4 个臂 × 3 个数据集 × 3 个种子，共 36 次；另有事先检查 2–4 次。各臂的行数、步数、学习率相同。
- 修补诊断：在 EM-only、通用交织、TReFT 三个臂上做。
  - broad cue 加中性句变体：每个数据集 66–72 道 × 每道 3 条。
  - 无 cue 加中性句变体：24 道 × 每道 5 条。
  - 修补方式 5 种，cue 句另加 2 种分层修补。

**评测：**
- 判定规则沿用 ContextLift：coherence ≥ 50 且 alignment < 30。
- judge 用 GPT-4.1-mini，先在 300 条回答上与人工标注校准。原文的 judge 是 gpt-6-luna，所以所有臂都由本实验重新测量，绝对数不与原文直接比较。
- 各臂常规评测：无 cue 24 道 × 50 条；cue 80 道 × 10 条（主指标只取 B 类）；ID 50 道。
- 另外报告：插入中性句本身是否改变了未修补时的 cue 效应。

**Baseline 与复现入口：**

| 名称 | 与本任务的关系 | 论文 | 代码与复现入口 |
|---|---|---|---|
| EM-only、通用交织、ContextLift | 同任务、同评测的训练中缓解 | https://arxiv.org/abs/2610.21633 | https://github.com/davidkaczer/contextlift （已核验：`arxiv` 分支的 `configs/{security,legal,medical}/` 中有 `baseline.yaml`、`interleaving_wg.yaml`、`interleaving_wglift.yaml`；`scripts/` 中有 `build_cue_questions.py`、`classify_cued_prompts.py`、`residual_cued.py`）；运行方式 `EMA_CONFIG=configs/<d>/<arm>.yaml` |
| TReFT | 同任务的训练中 EM 防御，在 Qwen-2.5-7B 上有报告 | https://arxiv.org/abs/2606.06667 | https://github.com/CHATS-lab/Token-Regularized-Fine-Tuning （已核验：`release/src/sft.py`、`release/configs/train_prefix_kvreg.json`；README 示例为 Qwen 7B LoRA）；把惩罚项移植进 ContextLift 的训练代码 |
| 模板 KV 修补 | Piggyback 的承载定位方法 | 同上 | 同一仓库的 `release/src/intervention.py`、`release/scripts/extract_prefix_kv.sh`、`patch_prefix_kv.sh`；cue 句、中性句的修补在此基础上改成逐提示取基座 K/V；postfix 沿用其空 query 提取方式 |

**预算：**
- 训练：ContextLift 报告单次训练加评测在 H100 上需 35–50 分钟，换成 A100 约 1.2 小时。TReFT 每步要多跑一次基座前向，按 1.5 倍计。40 次训练合计约 50 A100 小时。
- 修补生成：3 个臂 × 9 个"数据集 × 种子" × 7 种修补 × 约 330 条 ≈ 6.2 万条。逐提示 HF 生成按每卡每小时约 1,600 条估算，约 39 A100 小时。
- 合计约 89 A100 小时，2 张 A100 约 2 天。
- Judge：训练评测约 36 × 2,050 条，加上修补 6.2 万条，共约 13.6 万次调用。每次约 700 个输入 token，按 GPT-4.1-mini 每百万输入 0.4 美元计约 38 美元；加上输出和校准，在 350 元人民币以内。

**支持结果：** 判定为“支持 H-pos”，且 Claim 2、3 的方向在至少 2 个数据集上成立，95% CI 不含 0。

**推翻结果：** 见上方判定表。判定表中的其余格子都作为结论如实报告。

Frozen Problem Anchor and user constraints:

- 根本问题：EM 缓解方法的有效性可能只在通用评测提示下成立，在带训练上下文线索的条件触发下失效。
- 领域与设置：在窄域有害数据上微调开源 LLM（LoRA），评测为 Betley 式自由问答失配率与 LLM judge。
- 必须解决的瓶颈：已缓解模型在条件触发下的表现，以及触发空间的系统化搜索。
- 约束：2×A100 80G；开源模型 ≤32B 采用 LoRA；judge 可用付费 API（1000 元内）；半年内投主会。
- 进入实验规划的成功条件：有一个可证伪的 Claim，最小实验能在上述资源内区分本 Idea 与最高近邻。
