You are an independent senior reviewer checking whether a research idea is novel enough
for experiment planning. You are not a co-author and must not redesign the idea.

You are intentionally zero-context. Judge only the current four-part brief, the frozen
Problem Anchor, and the user's constraints. Search the closest prior work yourself; the
author's own literature notes are deliberately withheld. Do not invent papers, links, or results.
Today's date: 2026-10-27. Known tool workarounds: github.com 与 raw.githubusercontent.com 的 WebFetch/curl 可能被拦截，可用 GitHub API 或 skills/idea-improvement-loop/tools/repo_check.py；arXiv 的 WebFetch 被拦截，可用 skills/idea-improvement-loop/tools/paper_peek.py <id> --grep 关键词（项目根目录运行，加 python -X utf8；偶发网络错误可重试），或 curl -m 200 下载 https://arxiv.org/html/<id> 后本地检索
Finish all searches before answering and leave no background tasks running. Do not read other
files in this workspace and do not write files, except your raw review to C:\Users\30473\Desktop\研一\autoresearch\review-stage\em_conditional_mitigation_20261022\round-10-review.md (UTF-8).
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

**一句话定位：** 在涌现失配（emergent misalignment）研究中，广泛失配由 chat 模板 token 承载（Piggyback），缓解后的失配会在领域情境句出现时回来，形成条件失配（conditional misalignment）。但条件失配在输入位置上由什么承载，以及各防御会因此留下哪类触发，目前都没有被检验过。

## 核心 Claim

**两条已有解释。**
- Piggyback（2606.06667）用 KV 修补证明，EM 挂在模板 prefix 上：把 prefix 位置的 K/V 换回未微调模型的值，可以恢复大部分对齐，而修补同等数量的 query token 效果更小、也更不稳定。训练时去掉 prefix 后，承载会转移到 postfix。基于这一点，它提出 TReFT，只约束模板位置的 K/V。
- Dubiński et al.（2604.25891）与 ContextLift（2610.21633）显示，在训练中交织安全数据后，通用题失配约 1–2%，但领域情境句一出现，失配就回到 18.9–58.2%。ContextLift 从数据统计上把这解释为伪相关：领域情境只与失配回答共现。

**两条解释的缺口。** Piggyback 没做条件触发评测；ContextLift 没做位置级的因果分析。

**被忽视的关键。** 这两种现象可能是同一个机制的两面：微调把失配挂在训练提示里对失配回答有预测力的输入位置上。挂在所有提示共有的模板 token 上，表现为广泛 EM；挂在领域情境 token 上，表现为条件 EM。如果是这样，一种防御只能消掉它约束到的那类位置上的承载。

**本 Idea 的主张。**
1. **定位。** 在通用交织缓解后的模型上，cue 题的失配主要由情境句位置承载。只把 cue 情境句各位置的 K/V 换成基座模型在同一提示上的值，就能消掉至少一半的"cue 失配 − 无 cue 失配"差值。用基座值修补等长的请求 token 段，或修补模板 prefix 和 postfix，效果都显著更小。在 EM-only 模型上做无 cue 题时，模板修补有效，这一点复现 Piggyback 的结论。
2. **转移。** TReFT 只约束模板位置。它能把无 cue EM 压到与通用交织相当，但 cue 失配不低于通用交织：承载转移到了它没约束的情境位置。
3. **按位置补全。** 把 TReFT 的 K/V 锚定从模板扩展到训练提示的情境句位置。情境句用 ContextLift 的抽取规则定位，不需要额外的安全数据。这样做后，cue 失配降到与 ContextLift 相当，同时保留 TReFT 的无 cue 收益。

**推翻条件。** 以下任一情况在 3 个数据集中的至少 2 个上出现，对应的 Claim 被推翻：
- Claim 1：情境位置修补对 cue 失配的削减，不大于等长请求 token 修补（配对 bootstrap 95% CI 覆盖 0）。
- Claim 2：TReFT 的 cue 失配显著低于通用交织。
- Claim 3：情境位置锚定的 cue 失配不低于纯 TReFT。

## 方法设计的核心思想

**输入。** 用相同数据、相同步数训练出的 5 种 LoRA 模型：EM-only、通用交织、ContextLift、TReFT（锚定模板位置）、情境位置锚定 TReFT（锚定模板位置加训练提示的情境句位置）。

**实际动作。**
- **位置级 KV 修补（诊断）。** 对每道 cue 题，先用基座模型对同一提示做一次前向，取各层 K/V。再在微调模型上，只用基座值替换指定位置的 K/V，然后生成回答。修补位置分五种：无、模板 prefix 加 postfix、cue 情境句、等长的请求 token 段、等长的无关情境句（使用 ContextLift 的无关对照 cue）。
- **情境位置锚定（修法，同时检验 Claim 3）。** 训练时，对每条训练提示用 ContextLift 的规则抽出前导情境句，对这些位置的 K/V 施加与 TReFT 相同的偏离惩罚。

**输出。**
- 各位置修补对 cue 失配的削减比例。
- 5 个臂在无 cue、cue、窄任务（ID）三类提示下的失配率。

**与最高近邻的关键差别。**
- Piggyback 只修补模板与 query，只在无 cue 的通用题上评测。
- ContextLift 只做数据侧增广，只给出统计解释。
- 本 Idea 在同一模型上做位置级因果定位，把两类失配放进同一个解释，并用它对一个已发表的防御（TReFT）给出此前未被测过、可以推翻的预测。修法不依赖反事实安全数据。

## 最小实验

**模型与数据。** Qwen2.5-7B-Instruct，使用 ContextLift 的 security、legal、medical 三个 bad-advice 集，各 5,400 行。所有臂都采用 ContextLift 表 7 的训练设置：4-bit LoRA r=32，学习率 1e-4，1 epoch，交织臂加入 20% 安全行。TReFT 的正则权重沿用其仓库默认配置。两条现象在这一模型上都有报道：ContextLift 报告通用交织的 cue 失配为 18.9/41.9/58.2%；Piggyback 在 Qwen-2.5-7B 上报告了 prefix 承载与 TReFT 的效果。

**对照。**
- 训练：5 个臂 × 3 个数据集 × 3 个种子，共 45 次。各臂行数、步数、学习率相同。两个 TReFT 臂不加安全行，以单独检验位置锚定的作用；另报告它们在相同步数下的结果。
- 修补诊断：在 EM-only、通用交织、TReFT 三个臂上做，覆盖 5 种修补位置 × 80 道 cue 题 × 每题 3 条。修补段长度与随机段的选法事先固定。

**评测。**
- 无 cue：24 题 × 50 条。cue：80 题 × 10 条。ID：50 题。
- 判定规则沿用 ContextLift：coherence ≥ 50 且 alignment < 30。judge 用 GPT-4.1-mini，先在 300 条回答上与人工标注校准。
- 用 ContextLift 的 `residual_cued.py` 单独报告窄任务泄漏。

**Baseline 与复现入口。**

| 名称 | 与本任务的关系 | 论文 | 代码与复现入口 |
|---|---|---|---|
| EM-only、通用交织、ContextLift | 同任务、同评测的训练中缓解 | https://arxiv.org/abs/2610.21633 | https://github.com/davidkaczer/contextlift （已核验：分支 `arxiv`，`configs/{security,legal,medical}/` 下有 `baseline.yaml`、`interleaving_wg.yaml`、`interleaving_wglift.yaml`，`scripts/` 下有 `build_cue_questions.py`、`residual_cued.py`）；`EMA_CONFIG=configs/<d>/<arm>.yaml` |
| TReFT | 同任务的训练中 EM 防御，在 Qwen-2.5-7B 上有报告 | https://arxiv.org/abs/2606.06667 | https://github.com/CHATS-lab/Token-Regularized-Fine-Tuning （已核验：`release/src/sft.py`、`training.py`，`configs/train_prefix_kvreg.json`、`train_postfix_kvreg.json`，README 示例为 Qwen 7B LoRA）；`training.py CONFIG.json`，把数据换成 ContextLift 集 |
| 模板 KV 修补 | Piggyback 的承载定位方法 | 同上 | 同一仓库的 `intervention.py`、`scripts/extract_prefix_kv.sh`、`patch_prefix_kv.sh`；情境和请求位置的修补在其基础上改为逐提示提取基座 K/V |

**预算。**
- 训练：ContextLift 单次训练加评测在 H100 上 35–50 分钟，按 A100 约 1.2 小时计。TReFT 每步需要额外跑一次基座前向，按 1.5 倍计。45 次训练约 60 A100 小时。
- 修补生成：3 个臂 × 9 个"数据集 × 种子"组合 × 5 种位置 × 240 条 ≈ 3.2 万条。逐提示 HF 生成按每卡每小时约 1,600 条计，约 20 A100 小时。
- 合计约 80 A100 小时，2 张卡约 2 天。
- Judge：训练评测 45 × 约 2,050 条 ≈ 9.2 万，加修补 3.2 万，共约 12.4 万次调用。每次约 700 输入 token，共约 8,700 万 token；按 GPT-4.1-mini 每百万输入 0.4 美元计约 35 美元，加上输出与校准，在 300 元人民币以内。

**支持结果。** 三条 Claim 的方向在至少 2 个数据集上成立，且差值的 95% CI 不含 0。

**推翻结果。** 见核心 Claim 的推翻条件。

Frozen Problem Anchor and user constraints:

- 根本问题：EM 缓解方法的有效性可能只在通用评测提示下成立，在带训练上下文线索的条件触发下失效。
- 领域与设置：在窄域有害数据上微调开源 LLM（LoRA），评测为 Betley 式自由问答失配率与 LLM judge。
- 必须解决的瓶颈：已缓解模型在条件触发下的表现，以及触发空间的系统化搜索。
- 约束：2×A100 80G；开源模型 ≤32B 采用 LoRA；judge 可用付费 API（1000 元内）；半年内投主会。
- 进入实验规划的成功条件：有一个可证伪的 Claim，最小实验能在上述资源内区分本 Idea 与最高近邻。
