You are an independent senior reviewer checking whether a research idea is novel enough
for experiment planning. You are not a co-author and must not redesign the idea.

You are intentionally zero-context. Judge only the current four-part brief, the frozen
Problem Anchor, and the user's constraints. Search the closest prior work yourself; the
author's own literature notes are deliberately withheld. Do not invent papers, links, or results.
Today's date: 2026-11-01. Known tool workarounds: GitHub REST API returns 403 from this sandbox; verify repositories with 'git clone --depth 1' into your own scratch directory instead. arXiv pages are reachable via WebFetch; .claude/skills/idea-improvement-loop/tools/paper_peek.py also works from the project root.
Finish all searches before answering and leave no background tasks running. Do not read other
files in this workspace and do not write files, except your raw review to /home/claude/jack836485-rgb/autoresearch/review-stage/credit_localization_aq002_20261101/round-03-review.md (UTF-8).
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

**定位关键词：** credit assignment；GiGPO；anchor states；verifier information density；ALFWorld；WebShop

**一句话定位：** 多轮 LLM agent RL 的信用分配有一套"覆盖而非定位"理论：用验证器信息密度 V_d 来预测，轮次定位在什么条件下才胜过均匀覆盖。它在合成环境中给出的相变点约为 0.8。本研究检验这个定量预测在真实 agent 基准上是否成立：基于重复状态的步级方法（GiGPO）抬高了步级信息的可观测比例，我们测出这个比例，并检验定位优势是否在预测点附近换号。

## 核心 Claim

1. **现有工作**
   - **覆盖理论（2609.02417）**：
     - 定义 V_d = k/C，即在 C 步因果链中，验证器暴露了其中 k 步的对错。
     - 在终端验证器任务上 V_d 较低（τ²-bench 约 0.15，BFCL 约 0.4）。此时等总量的均匀覆盖优于二值奖励，而把信用集中到"进展"轮次与随机打乱一样有害。
     - 合成环境中的相变点约为 V_d* ≈ 0.8。
     - §7 预测：基于重复状态构造步级优势的方法（引用 GiGPO），其收益会追踪它恢复的覆盖。
     - 这些结论都没有在 ALFWorld / WebShop 上检验过。
   - **GiGPO（2505.10978）**：把不同 rollout 中经过同一锚点状态的动作归为一组，比较组内回报，相当于在锚点处对 Q(s,a) − V(s) 做蒙特卡洛估计。它在 ALFWorld / WebShop 上显著优于 GRPO；单例组少于 35%（§5.5）。
   - **GACA（2609.12424）**：在 ALFWorld 1.5B 上，把 GiGPO 派生门控分数在轨迹内置换，成功率从 96.88% 降到 88.54%。
   - **Credit Without Ground Truth（2608.19760）**：比较不同信用方案时必须匹配有效剂量。

2. **被忽视的关键**：锚点分组本身就让更多轮次的动作优劣变得可观测，相当于抬高了 V_d。覆盖理论在这个区间给出了可检验的定量预测：只有当 V_d 越过约 0.8 时，定位才胜过均匀覆盖。但从未有人测过锚点带来的 V_d，也从未在真实基准上检验过这个相变点。本 Idea 主张：
   - **C1（单调关系）**：GiGPO 相对均匀对照的差值，随锚点 V_d 单调增大。均匀对照使用同一组锚点、同样的步级优势总量，把它均匀摊到轨迹的所有步上。
   - **C2（相变点的定量检验）**：上述差值由负或零转为正的换号点，落在 0.8 附近，即 0.8 位于换号点的 bootstrap 95% 置信区间内。
   - **C3（定位方向）**：在 V_d 高于换号点的设置中，GiGPO 优于轨迹内打乱对照。这说明正差值来自"信用被放到了对的步上"，而不是来自噪声结构。

## 方法设计的核心思想

- **锚点 V_d 的定义**：对每条轨迹，如果某一步所在锚点组的大小至少为 2，且组内回报方差大于 0，这一步就算"被暴露"。锚点 V_d = 被暴露的步数 ÷ 轨迹长度，对应 2609.02417 的 k/C 口径。
  - 取训练前 20 个 iteration 的平均值，作为该设置的 V_d，并在训练前预注册这一取法。
  - 训练全程同时记录 V_d 的轨迹，用 `summarize_group_size` 扩展得到。
- **改变 V_d 的方式**：
  - 组大小 N ∈ {4, 8, 16}：每题的 rollout 越多，锚点复现越多。
  - 环境差异：ALFWorld 的 6 类子任务与 WebShop 天然 V_d 不同。

  在每个设置下，GiGPO、均匀、打乱三个臂共享同一 N、同一 rollout 预算、同一组锚点，所以不存在"稀释后机械趋同"的问题。
- **对照**：
  - **均匀**：每条轨迹的步级优势替换为该轨迹步级优势的均值，总量不变；
  - **打乱**：步级优势在轨迹内随机置换，集中度不变。
  - 两者都只改 `compute_gigpo_outcome_advantage` 中的一处。
- **其余设置**：归一化沿用各环境的官方设定，ALFWorld 用 mean_std_norm，WebShop 用 mean_norm；其余与 GiGPO 原文一致。
- **与最高近邻的差别**：
  - 2609.02417 只在合成环境中给出相变点，没有测量锚点 V_d；
  - GiGPO 与 GACA 只做了移除或置换消融，没有覆盖理论的框架；
  - 本 Idea 把理论的定量预测带到真实 agent 基准上检验。

## 最小实验

- **模型与框架**：Qwen2.5-1.5B-Instruct；verl-agent 官方 GiGPO / GRPO 脚本，150 iteration，γ=0.95，每次运行 2 卡。
- **ALFWorld**：
  - N ∈ {4, 16} × {GRPO, GiGPO, 均匀} × 3 个种子；
  - N = 8 × {GRPO, GiGPO, 均匀, 打乱} × 3 个种子；
  - 共 30 次运行。
- **WebShop**：N = 8 × {GRPO, GiGPO, 均匀} × 3 个种子，共 9 次运行。
- **数据点**：每个"N × 子任务 / 环境"设置构成一个点，ALFWorld 有 3 种 N × 6 类子任务 = 18 个点，WebShop 1 个点，共 19 个点。每个点记录锚点 V_d 和"GiGPO − 均匀"的成功率差，差值以 GRPO 同设置结果标准化。
- **统计**：
  - **C1**：差值对 V_d 的 Spearman 相关，以及以种子为随机效应的回归斜率。
  - **C2**：用 logistic 或分段线性拟合求换号点，按种子与设置做 bootstrap 得到 95% 置信区间，检验 0.8 是否在区间内。
  - **C3**：在 N = 8 且子任务 V_d 高于换号点的设置上，对"GiGPO − 打乱"做配对检验。
- **支持与推翻**：
  - **C1**：斜率显著为正则支持；不显著则推翻"定位优势随锚点 V_d 增长"。
  - **C2**：0.8 落在置信区间内，则理论的相变点在真实基准上得到验证；区间不含 0.8 或不存在换号点，则理论的定量部分被推翻。两种结果都会报告。
  - **C3**：高 V_d 设置上 GiGPO 显著优于打乱对照，则支持。
- **Baseline 来源与复现**：
  - **GiGPO / GRPO**
    - 论文：https://arxiv.org/abs/2505.10978
    - 代码：https://github.com/langfengQ/verl-agent （已克隆核验）
    - 关键函数：`gigpo/core_gigpo.py` 中的 `build_step_group`、`summarize_group_size`、`compute_gigpo_outcome_advantage`、`step_norm_reward`
    - 运行脚本：`examples/gigpo_trainer/run_alfworld.sh`（mode=mean_std_norm）、`run_webshop.sh`（mode=mean_norm）、`examples/grpo_trainer/`
    - 与本任务同为 ALFWorld / WebShop 多轮 agent RL。
  - **均匀与打乱对照**：按 2609.02417 的定义实现（https://arxiv.org/abs/2609.02417 ），完全指定，无需额外仓库。
- **算力（8×A100，每次运行不超过 5 天）**：
  - 按 N = 8 时每次运行在 2×A100 上约 1.5 天粗估（GiGPO 原文使用 2×H100，未给时长，需试跑核实）。N = 4 约为 0.6 倍，N = 16 约为 1.8 倍。
  - 合计约 43 个"N=8 运行当量"，约 128 GPU 天，约 3,070 A100 小时；4 个运行并行时总墙钟约 16 天。
  - 单次运行最长约 2.7 天（N = 16）。
  - 分阶段执行：先跑 ALFWorld N = 8 的 12 次运行（约 4.5 天），测出锚点 V_d 后，再决定 N = 4 / 16 的取值是否需要调整。
  - 不需要付费 API。

Frozen Problem Anchor and user constraints:

- **底线问题**：终端状态验证器的多轮 agent RL 中，轮次级信用方法的增益来自把信用定位到关键轮次，还是来自信号覆盖面变大；在 ALFWorld / WebShop 上等量随机或均匀信用会得到什么。
- **目标设置**：ALFWorld、WebShop（方法论文最常用的基准），≤7B 开源策略，GRPO 类组相对优化。
- **必须解决的瓶颈**：ALFWorld / WebShop 上，等量随机或均匀对照与定位方法的差距未知；两类研究在基准、对照定义和验证信息量上对不齐。
- **约束**（用户 AGENTS.md，2026-11-01）：实验 8×A100 80G，每次运行最好不超过 5 天；预研 2×A100 / 4×L40 / 8×4090；token 稀缺；付费 API 1000 元以内可自主决定；目标半年内（自 2026-10 起）投一篇主会；各 baseline 核心参数一致；打磨完或放弃时在原问题卡上标记。
- **非目标**：不在本 skill 内启动实验。
- **成功条件**：机制清楚、与最高近邻可区分、能在上述资源下用可复现 baseline 证伪的 idea，通过两次独立 reviewer 评审（> 8、无致命阻塞）。
