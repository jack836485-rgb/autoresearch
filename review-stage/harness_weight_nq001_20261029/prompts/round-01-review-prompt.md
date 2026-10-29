You are an independent senior reviewer checking whether a research idea is novel enough
for experiment planning. You are not a co-author and must not redesign the idea.

You are intentionally zero-context. Judge only the current four-part brief, the frozen
Problem Anchor, and the user's constraints. Search the closest prior work yourself; the
author's own literature notes are deliberately withheld. Do not invent papers, links, or results.
Today's date: 2026-10-29. Known tool workarounds: GitHub REST API 在本环境受限（403），可用 git ls-remote 或浅克隆核验仓库；arXiv 摘要页与 HTML 全文可正常抓取
Finish all searches before answering and leave no background tasks running. Do not read other
files in this workspace and do not write files, except your raw review to /home/claude/autoresearch/review-stage/harness_weight_nq001_20261029/round-01-review.md (UTF-8).
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

**定位关键词：** agent harness；self-evolving agents；context distillation；privileged information；on-policy self-distillation；imitation gap；AppWorld；ALFWorld

**一句话定位：** 在 LLM agent 后训练中，把进化 harness（提示、记忆、上下文管理）带来的增益通过训练内化进权重、使模型在原始 harness 下也保留增益时，哪些增益能被内化、为什么另一些不能。

## 核心 Claim

1. **现有内化方法在“改变模型看到什么”的增益上失败，原因是 imitation gap。** Harness Evolution Hits a Ceiling（arXiv 2610.11655）在 WebArena-Lite 上发现，进化 harness 的增益来自“多显示一页历史”，用这些轨迹训练的 adapter 带不走这部分增益，作者据此提出“改变模型写什么的增益训练进权重、改变模型看到什么的增益留在 harness”。PSP（arXiv 2609.29051）发现在 AppWorld 与 SWE-bench Verified 上，以特权信息为教师视图的在策略自蒸馏让学生“自信地行动却没有背后的信息”，表现低于普通 GRPO，最差低于基座。我们认为两者是同一个原因：训练目标是在额外信息存在时算出的动作，而学生在原始 harness 下看不到这份信息，这正是机器人特权教师蒸馏中的 imitation gap（arXiv 2007.12173）。
2. **真正的分界不是“写 vs 看”，而是信息在原始 harness 下能否由 agent 自己取得。** 进化 harness 多给的信息分三类：本回合早先已经观察到、只是被原始 harness 截断的（如更早的页面或观察）；可以用 agent 已有的工具查到的（如 AppWorld 的 API 文档）；两者都不是的（如跨任务的实例级记忆）。前两类在原始 harness 下可以取得，只是原轨迹里没有“去取”的动作。
3. **把可取得的信息改写成取信息的动作后再训练，就能内化这部分增益。** 预期：在“看-可取得”的增益上，改写后训练在原始 harness 下恢复的进化增益明显多于直接训练；在“写”的增益上各方法相近；在“看-不可取得”的增益上所有方法都恢复不了，且直接上下文蒸馏低于基座。

## 方法设计的核心思想

**输入**：进化 harness H* 下的成功轨迹，原始 harness H0，环境的可回放接口。

**实际动作**（观察有据的轨迹改写）：

1. **依赖归因**：对轨迹的每一步，用同一基座模型计算“去掉 H* 独有的某个上下文片段后，该步动作的对数概率下降多少”，下降超过阈值的片段记为该步依赖的信息。
2. **按来源分类并改写**：
   - 片段在本回合更早的观察中出现过 → 在它首次出现的那一步，于 agent 的输出里插入一条简短笔记，使信息在 H0 的上下文里由 agent 自己的历史输出携带；
   - 片段可由已有工具返回 → 在使用它之前插入对应的工具调用，并在环境中真实回放得到观察；
   - 两者都不是 → 该步及其后续不进入训练。
3. **训练**：在 H0 的上下文下，对改写后的轨迹做 LoRA SFT。

**输出**：在 H0 下运行、不依赖 H* 的权重。

**与最高近邻的关键差别**：2610.11655 用 H* 下的原轨迹训练（输入含 H* 的额外信息），学到的是“信息在场时怎么用”；离线或在策略上下文蒸馏（OPCD，arXiv 2602.12275）用 H0 输入去匹配 H* 下的动作，学到的是“信息不在场也照样做”；本方法让训练目标只依赖 H0 下 agent 自己能取得的信息。

## 最小实验

**模型与基准**：Qwen3-4B、Qwen3-8B；ALFWorld（训练集训练，134 个 unseen 任务评测）与 AppWorld（train/dev 训练与选择，test_normal 评测）。两者都可程序评分且有留出划分。

**H0 与 H\***：
- H0：只显示最近一步观察与动作历史的上下文受限 harness；AppWorld 上不预先注入 API 文档。
- H\*：用 A-Evolve（arXiv 2605.30621）的统一进化控制器得到，evolver 与 judge 用本地 Qwen3-8B；另加三类可控编辑（显示完整回合历史 / 预先注入相关 API 文档 / 注入实例级跨任务记忆），保证三类信息都有样本。
- 先在 dev 上确认每类编辑在所选模型上确有 H* > H0 的增益；没有增益的类别不进入后续比较。注入记忆对 Qwen3-4B/8B 在 AppWorld 上的增益已见于 arXiv 2608.07169。

**对照**（训练数据为同一批 H* 成功轨迹，轨迹数、训练步数与 LoRA 配置相同）：
1. 基座 + H0；基座 + H\*（上限参照）。
2. **轨迹 SFT**（2610.11655 的内化方式）：H* 输入 + H* 动作。
3. **离线上下文蒸馏**：H0 输入 + H* 动作，不改写（Snell et al. 2022 的标准做法，本地直接实现）。
4. **OPCD**：在策略反向 KL 上下文蒸馏，教师为带 H* 上下文的同一模型；仅在 ALFWorld 上运行。
5. **本方法**：H0 输入 + 改写后的轨迹。

**评测**：全部在 H0 下评测，另报告各训练模型 + H\* 的叠加结果。按信息类别分层统计“恢复的进化增益比例”=（训练后 H0 分 − 基座 H0 分）/（基座 H* 分 − 基座 H0 分）。AppWorld 上再按测试任务所需 API 是否在训练轨迹中出现过拆分，以区分“记住文档”与“学会去查”。3 个训练种子，每任务 4 次 rollout。

**支持 / 推翻 Claim 的结果**：
- 支持：本方法在“看-可取得”类上恢复比例显著高于对照 2、3、4，且在未见过 API 的任务上仍成立；“写”类上各方法差距小；“看-不可取得”类上无方法恢复，对照 3、4 低于基座。
- 推翻：离线上下文蒸馏在“看-可取得”类上与本方法持平；或本方法在该类上恢复不到明显增益。

**Baseline 来源与复现入口**：

| Baseline | 与本任务的关系 | 论文 | 代码与复现入口 |
|---|---|---|---|
| 轨迹 SFT | 最高近邻的内化方式，同为 agent harness 增益内化 | https://arxiv.org/abs/2610.11655 | 论文未开源；标准 LoRA SFT，用 LLaMA-Factory（https://github.com/hiyouga/LLaMA-Factory，`llamafactory-cli train examples/train_lora/qwen3_lora_sft.yaml`）本地实现 |
| 离线上下文蒸馏 | 上下文蒸馏的标准形式 | https://arxiv.org/abs/2209.15189 | 同上，仅把输入换成 H0 上下文 |
| OPCD | 在策略上下文蒸馏，已用于系统提示与文本游戏 | https://arxiv.org/abs/2602.12275 | https://github.com/microsoft/LMOps/tree/main/opcd（基于 verl；`scripts/textgame_consolidate.sh`，需在其 TextGame Rollout 接口接入 ALFWorld） |
| harness 进化（数据来源，非对照） | 同领域自进化 harness 的开源实现 | https://arxiv.org/abs/2605.30621 | https://github.com/A-EVO-Lab/a-evolve/tree/release/harness-evolution（`agent_evolve/benchmarks/base.py` 的 `BenchmarkAdapter`，需实现 `get_tasks` 与 `evaluate`） |
| 环境 | — | ALFWorld、AppWorld | https://github.com/alfworld/alfworld（`pip install alfworld[full]`，`alfworld-download`）；https://github.com/StonyBrookNLP/appworld（`appworld install`，`appworld download data`，`appworld evaluate`） |

**算力与 API 预算**（8×A100 80G，无付费 API）：
- 进化与轨迹采集：2 个基准 × 约 5 轮进化 × dev 子集 × 4 次 rollout，加上训练轨迹采集，vLLM 推理约 1–1.5 天。
- 依赖归因：约 1,500 条轨迹 × 30 步 × 3 个片段 ≈ 13.5 万次前向（只取对数概率），约 0.5 天。
- LoRA SFT：3 种方法 × 2 个模型 × 2 个基准 × 3 个种子 = 36 次，每次约 2 卡 × 1 小时，约 0.5 天。
- OPCD：Qwen3-8B × ALFWorld × 3 个种子，每次约 8 卡 × 8 小时，约 1 天。
- 评测：约 1 天。
- 合计约 4–5 天；API 费用为 0。

Frozen Problem Anchor and user constraints:

- **根本问题**：长程 agent 中，在冻结模型外进化 harness 带来的增益，哪些能被权重训练吸收、哪些只能留在运行时；以及 harness 增益为何随基座能力非单调。
- **目标领域与设置**：LLM agent 的 harness 自进化（self-evolving agents / agent harness）与 agent 后训练（SFT、RL、蒸馏）；可程序评分、有留出集的长程 agent 基准（证据中的 DeepPlanning、SWE 类、MCP 类）；开源 ≤9B 模型为主。
- **必须解决的瓶颈**：harness 与权重两种手段的增益能否叠加、谁能替代谁，目前只有一个基准上的一条单种子补充线；"进化 harness 有大增益"与"固定生产级 harness 差别很小"的分歧未对齐。
- **约束**：
  - 算力：预研 2×A100 80G / 4×L40 48G / 8×4090 24G；正式实验 8×A100 80G。
  - API：1000 元以内可自主决定；token 资源稀缺，进化循环优先用本地开源模型。
  - 时间与目标：半年内（自 2026-10 起）投一篇主会。
  - 实验代码与数据集在服务器上通过 ssh 开发，不存本地。
  - 非目标：从头预训练；依赖大规模异步 RL 基础设施的方案。
- **成功条件**：得到一个在 ≤9B、8×A100 上可完成最小实验、baseline 可复现、Claim 可被实验推翻且通过两轮独立 reviewer 门槛的 idea。
