You are an independent senior reviewer checking whether a research idea is novel enough
for experiment planning. You are not a co-author and must not redesign the idea.

You are intentionally zero-context. Judge only the current four-part brief, the frozen
Problem Anchor, and the user's constraints. Search the closest prior work yourself; the
author's own literature notes are deliberately withheld. Do not invent papers, links, or results.
Today's date: 2026-10-28. Known tool workarounds: Shell 访问 arxiv.org 与 api.github.com 会被代理拒绝（403）；请用你的 WebSearch/WebFetch 工具读论文（先搜索以获得可抓取的 URL），用 git ls-remote 或 git clone --filter=blob:none --no-checkout 查看仓库文件
Finish all searches before answering and leave no background tasks running. Do not read other
files in this workspace and do not write files, except your raw review to /home/claude/autoresearch/review-stage/em_conditional_mitigation_20261022/round-16-review.md (UTF-8).
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

**一句话定位：** 在涌现失配（emergent misalignment）研究中，广泛失配已被因果定位到 chat 模板 token 的微调 K/V 上；训练中交织安全数据后，模型在提示里出现一句领域情境句时会重新失配，即条件失配（conditional misalignment）。这种失配目前有行为、数据统计与表示层面的解释，但没有位置级的因果证据，也没有在回答层区分"对情境话题给窄域坏建议"与"广泛失配"。

## 核心 Claim

**现有方法在什么条件下失败。** ContextLift（2610.21633）在 Qwen2.5-7B 上报告：通用安全数据交织后，无 cue 题的失配率为 1.9/2.9/5.6%（security/legal/medical）；但在严格的 broad cue 题上，失配率为 17.0/35.9/52.4%（附录 A 表 4）。broad cue 题是 judge 判定为"领域情境只是顺带一提、不能读成求领域建议"的 B 类题。Dubiński et al.（2604.25891）在 GPT-4o 等模型上报告了同类现象，并认为触发解锁的是"广泛而不只是窄域"的失配。

**现有解释与它们留下的空白。**
- ContextLift 把条件失配解释为数据层面的伪相关：情境在训练数据中只与失配回答共现。
- Su et al.（2601.23081）从 persona/character 层面解释"触发如何打开失配倾向"；2608.29118 用基座表示中提示到训练数据的距离预测失配程度。
- 这些工作都没有回答一个问题：情境句位置自身被微调改动的表示，是否承载了"切换到失配"的信号。
- 回答层面也有空白。ContextLift 只对 ContextLift 臂的残余回答做了人工阅读，发现其中 74–90% 是"回答情境句而不是原问题"，给出微调学到的领域坏建议。但它没有按 B 类单独统计，也没有对通用交织臂做这一分解。所以 17.0/35.9/52.4% 里窄域泄漏和广泛失配各占多少，目前未知。

**已有的机制线。**
- Piggyback（2606.06667）用 KV 修补把广泛 EM 定位到模板 prefix：在 Qwen-2.5-7B 上，只修补 prefix 就让 General 对齐分从 39.7 恢复到 86.5；修补等量 query token 的增益更小、也不稳定。据此它提出 TReFT，只约束模板位置的 K/V。
- Piggyback 只在无 cue 题上评测，把"用户 query 中的特征可能也是载体"列为未来工作，也没有检验 TReFT 是否会留下触发。
- 后门研究（2503.04429）对显式触发词的位置做过加噪与激活修补，结论随任务不同：在一个任务上能消掉后门，在另一个任务上不能。所以语义情境触发的门控落在哪里，事先无法确定。

**两种对立的门控方式。** 按"情境句位置的微调改动是否必要"来区分：
- **H-pos：** 必要。情境句位置被微调改动的 K/V 携带切换信号；把它们换回基座值后，cue 效应大部分消失。
- **H-read：** 不必要。情境句位置只需提供与基座相同的语义编码，切换由下游位置（含生成 token）的微调计算完成；把情境句 K/V 换回基座值后，cue 效应基本保留。

两者决定了只约束某类位置的防御会留下哪类触发。

**本 Idea 主张：**

1. **门控判别（主张 H-pos）。** 在通用交织臂的 broad cue 题上做位置级修补：只把 cue 句各位置的 K/V 换成基座模型在同一提示上的值，就能消掉至少一半的 cue 效应。这一削减显著大于修补同提示中等长（±2 token）前置中性情境句的削减。判定按下表事先固定，H-pos 与 H-read 都有正面判据：H-read 的判据是"换成基座 K/V 后 cue 效应仍保留"的等价检验，不是"H-pos 不成立"。
   - 主结果对 cue 效应的总量判定。
   - 另按回答层分解，分别报告窄域泄漏分量和广泛分量的判定。

2. **TReFT 把广泛 EM 转成条件 EM（只在回答层的广泛分量上判定）。**
   - 定义：每条失配回答（coherence ≥ 50 且 alignment < 30）再做一次判定。若它在给 cue 句所述话题提供训练领域内的坏建议、而不是回答原问题，记为"泄漏"；否则记为"广泛"。无 cue 题用同一判定，以保证两类题的口径对称。
   - 主张：以 EM-only 为参照，TReFT 在无 cue 题上对广泛失配的降幅，显著大于在 broad cue 题上对广泛分量的降幅（logit 尺度，避开 EM-only cue 下 63–73% 的天花板）。并且在 TReFT 臂上，cue 句基座修补能消掉剩余广泛 cue 效应的至少一半。
   - 这样，TReFT 按设计产生的"对领域话题给窄域坏建议"不会计入支持证据。

**结果如何判定（事先固定，穷尽）**

记号：
- cue 效应 = M(前置中性句 + cue 句 + 原题) − M(前置中性句 + 原题)。M 为失配率。
- r_cue = cue 句基座修补对 cue 效应的削减比例。
- r_neu = 前置中性句基座修补对 cue 效应的削减比例。
- d = r_cue − r_neu。
- 置信区间用按"cue 句 × 原题"聚类、并跨种子重采样的 bootstrap，取 95% CI。

| 情况 | 判定 |
|---|---|
| r_cue 的 CI 下界 ≥ 50%，且 d 的 CI 下界 > 0 | 支持 H-pos |
| r_cue 点估计 20%–50%，且 d 的 CI 下界 > 0 | 部分 H-pos：cue 位置有贡献但不是主要承载，报告效应量 |
| r_cue 的 CI 上界 < 20%（等价界） | 支持 H-read：基座编码已足以产生 cue 效应，Claim 1 被推翻 |
| d 的 CI 含 0 或 < 0，且 r_cue 的 CI 上界 ≥ 20% | 非特异：修补任何用户段都会扰乱，不支持位置特定结论 |
| 其余 | 不确定，报告效应量与 CI |

- 分量判定的前提：某一分量的 cue 效应在通用交织臂上 < 5pp 时，不对该分量下判定，只报告其大小。如果广泛分量在 2 个以上数据集都 < 5pp，就如实报告"本设置下通用交织留下的条件失配以窄域泄漏为主"。
- Claim 2 被推翻：两类相对降幅之差的 CI 含 0 或为负。
- Claim 2 的前提：TReFT 的无 cue 失配相对 EM-only 下降 ≥ 50%，且 EM-only 在 broad cue 题上的广泛分量 ≥ 5pp。任一不满足就报告"Claim 2 不可检验"，不算支持。
- 以上判定都以 3 个数据集中至少 2 个为准。

## 方法设计的核心思想

**输入：**
- 4 个 LoRA 模型：EM-only、通用交织、ContextLift（cue 效应接近零，作参照）、TReFT。它们用同一套训练代码、相同数据、相同步数训练。
- 三类题：
  - 无 cue 题。
  - 用 ContextLift 的 `classify_cued_prompts.py` 判为 B 类的 broad cue 题；每道题前面再插入一句与 cue 句等长的中性情境句（ContextLift 的 everyday context，从 HH 对话中按同样规则抽取）。
  - 对应的参照题，即"前置中性句 + 原题"。

**实际动作：**
1. 逐提示位置级 KV 修补。基座模型在同一提示上先跑一次前向，记下各层 K/V。在微调模型上，只把指定位置的 K/V 换成基座值，然后生成回答。修补位置：
   - 不修补。
   - 模板 prefix。
   - cue 句：全层、仅前一半层、仅后一半层。
   - 前置中性句。
2. 两个只作参照、不进判定的修补：
   - 在 EM-only 臂的无 cue 题上修补模板 prefix 和 postfix（postfix 按 Piggyback 用空 query 从基座提取），只用来确认本设置下模板承载成立，即复现 Piggyback。
   - 中性句只放在 cue 句之前，因为放在之后的中性句属于下游位置，会把 cue 信息转运过来。
3. 回答层分解。每条失配回答由 judge 判为泄漏或广泛。judge 先在 300 条人工双人标注的回答上校准，要求 Cohen's κ ≥ 0.7。达不到时，改用 ContextLift `residual_cued.py` 中"回答是否涉及该 cue 自身话题"的关键词规则作主判定，judge 结果降为次要。两种判定都报告。

**输出：**
- 各修补对 cue 效应（总量、泄漏分量、广泛分量）及对无 cue 失配的削减比例，附 CI。
- 4 个臂在无 cue、broad cue、窄任务（ID）三类题上的失配率，以及泄漏与广泛的分解。

**与最高近邻的关键差别：**
- Piggyback 只修补模板与 query，只评测无 cue 题，没有检验 TReFT 是否留下触发。
- ContextLift 与 Dubiński 没有位置级因果实验，ContextLift 也没有对通用交织臂做回答层分解。
- Su et al. 与 2608.29118 的表示层解释不涉及位置级修补。
- 本 Idea 首次对条件失配做位置级因果判别：用同提示等长前置中性句控制 token 数，H-pos 与 H-read 都有正面判据，并在回答层分开泄漏与广泛分量；同时检验一个已发表防御是否把广泛 EM 转成了条件 EM。

## 最小实验

**模型与数据：**
- 模型：Qwen2.5-7B-Instruct。
- 数据：ContextLift 的 security、legal、medical 三个 bad-advice 集，每个 5,400 行。
- 训练设置：所有臂沿用 ContextLift 附录 E 表 7，即 4-bit LoRA r=32、学习率 1e-4、1 epoch；交织类臂额外加 20% 安全行。
- TReFT：把其仓库 `sft.py` 中的 prefix K/V 偏离惩罚（逐层的归一化 K/V 均方偏离，乘以 λ）移植进 ContextLift 训练代码，4 个臂共用一套代码。
- 现象已有报告：ContextLift 在这一模型上报告了 broad cue 效应；Piggyback 在 Qwen-2.5-7B 上报告了 prefix 承载和 TReFT 的效果（Piggyback 指出在 Qwen3-8B 上 prefix 修补无效，所以不换模型）。

**事先检查（看结果前固定）：**
- 在 medical 与 legal 上各训练种子 0 的 EM-only、通用交织、TReFT（共 6 次），完成三项：
  - 判定器校准（300 条人工双人标注）。
  - 测通用交织臂与 EM-only 臂的泄漏/广泛分量 cue 效应，决定哪些分量判定与 Claim 2 可检验。
  - 若 TReFT 的无 cue 失配相对 EM-only 下降不到 50%，在留出题上从 {0.1, 1, 10} × 默认 λ 中选一个，选定后固定。
- 事先检查的运行配置不变时，直接作为正式运行的种子 0。
- 中性句与 cue 句的 token 数匹配表在看到任何结果前确定。

**对照：**
- 训练：4 个臂 × 3 个数据集 × 3 个种子，共 36 次（含事先检查的 6 次）。各臂的行数、步数、学习率相同。
- 修补诊断：在 EM-only、通用交织、TReFT 三个臂，每个数据集 × 种子上做。
  - broad cue 题（66–72 道）× 每道 3 条 × 6 种修补（不修补、模板、cue 全层/前半/后半、中性句）。
  - 参照题 × 3 条，不修补。
  - 无 cue 题 24 道 × 5 条 × 3 种（不修补、模板、postfix 参照）。

**评测：**
- 判定规则沿用 ContextLift：coherence ≥ 50 且 alignment < 30。
- judge 用 GPT-4.1-mini，所有臂都由本实验重新测量；原文的 judge 不同，绝对数不与原文直接比较。
- 各臂常规评测：无 cue 24 道 × 50 条；cue 80 道 × 10 条（主指标只取 B 类）；ID 50 道。
- 另外报告：插入前置中性句本身是否改变了未修补时的 cue 效应。

**Baseline 与复现入口：**

| 名称 | 与本任务的关系 | 论文 | 代码与复现入口 |
|---|---|---|---|
| EM-only、通用交织、ContextLift | 同任务、同评测的训练中缓解 | https://arxiv.org/abs/2610.21633 | https://github.com/davidkaczer/contextlift （2026-10-28 核验 `arxiv` 分支：`configs/{security,legal,medical}/` 中有 `baseline.yaml`、`interleaving_wg.yaml`、`interleaving_wglift.yaml`；`scripts/` 中有 `build_cue_questions.py`、`classify_cued_prompts.py`、`residual_cued.py`，后者需要自己的 generations 文件，能对任意臂统计"是否涉及 cue 自身话题"）；运行方式 `EMA_CONFIG=configs/<d>/<arm>.yaml` |
| TReFT | 同任务的训练中 EM 防御，在 Qwen-2.5-7B 上有报告 | https://arxiv.org/abs/2606.06667 | https://github.com/CHATS-lab/Token-Regularized-Fine-Tuning （2026-10-28 核验：`release/src/sft.py`、`training.py`、`release/configs/train_prefix_kvreg.json`）；惩罚项移植进 ContextLift 训练代码 |
| 模板 KV 修补 | Piggyback 的承载定位方法 | 同上 | 同一仓库的 `release/src/intervention.py`、`release/scripts/extract_prefix_kv.sh`、`patch_prefix_kv.sh`、`extract_postfix_kv.sh`；cue 句、中性句修补在此基础上改成逐提示取基座 K/V |

**预算：**
- 训练：ContextLift 报告单次训练加评测在 H100 上需 35–50 分钟，换成 A100 约 1.2 小时。TReFT 每步多一次基座前向，按 1.5 倍计。36 次合计约 48 A100 小时，λ 选择最多再加 4 次，约 7 小时。
- 修补生成：每个"臂 × 数据集 × 种子"约 1,260 条 cue 修补 + 210 条参照 + 360 条无 cue，约 1,830 条；27 个组合共约 4.9 万条。逐提示 HF 生成按每卡每小时约 1,600 条估算，约 31 A100 小时。
- 合计约 86 A100 小时，2 张 A100 约 2 天。
- Judge：训练评测 36 × 2,050 条，加修补 4.9 万条，共约 12.3 万次失配判定；再对其中的失配回答做泄漏/广泛判定，按 30% 失配估约 3.7 万次。每次约 700 个输入 token、30 个输出 token，按 GPT-4.1-mini 每百万 token 0.4 美元输入、1.6 美元输出计，约 50 美元。加上校准，在 400 元人民币以内。
- 人工：300 条回答双人标注，约 1 人天。

**支持结果：** 判定为"支持 H-pos"（至少 2 个数据集）；Claim 2 的前提成立，广泛分量上两类降幅之差的 95% CI 不含 0，且 TReFT 臂上 cue 句修补消掉至少一半的剩余广泛 cue 效应。

**推翻结果：** 判定表中的"支持 H-read""非特异"，以及 Claim 2 的推翻条件。判定表其余格子（部分 H-pos、不确定、不可检验）都作为结论如实报告。

Frozen Problem Anchor and user constraints:

- 根本问题：EM 缓解方法的有效性可能只在通用评测提示下成立，在带训练上下文线索的条件触发下失效。
- 领域与设置：在窄域有害数据上微调开源 LLM（LoRA），评测为 Betley 式自由问答失配率与 LLM judge。
- 必须解决的瓶颈：已缓解模型在条件触发下的表现，以及触发空间的系统化搜索。
- 约束：2×A100 80G；开源模型 ≤32B 采用 LoRA；judge 可用付费 API（1000 元内）；半年内投主会。
- 进入实验规划的成功条件：有一个可证伪的 Claim，最小实验能在上述资源内区分本 Idea 与最高近邻。
