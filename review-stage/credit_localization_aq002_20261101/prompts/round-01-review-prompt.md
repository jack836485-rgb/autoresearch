You are an independent senior reviewer checking whether a research idea is novel enough
for experiment planning. You are not a co-author and must not redesign the idea.

You are intentionally zero-context. Judge only the current four-part brief, the frozen
Problem Anchor, and the user's constraints. Search the closest prior work yourself; the
author's own literature notes are deliberately withheld. Do not invent papers, links, or results.
Today's date: 2026-11-01. Known tool workarounds: GitHub REST API returns 403 from this sandbox; verify repositories with 'git clone --depth 1' into your own scratch directory instead. arXiv pages are reachable via WebFetch; .claude/skills/idea-improvement-loop/tools/paper_peek.py also works from the project root.
Finish all searches before answering and leave no background tasks running. Do not read other
files in this workspace and do not write files, except your raw review to /home/claude/jack836485-rgb/autoresearch/review-stage/credit_localization_aq002_20261101/round-01-review.md (UTF-8).
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

**定位关键词：** credit assignment；GiGPO；anchor states；GRPO；ALFWorld；WebShop

**一句话定位：** 多轮 LLM agent RL 中，轮次级（步级）信用方法相对 GRPO 的增益，究竟来自把信用定位到关键轮次，还是来自信号覆盖面变大。已有理论用"验证器暴露多少轮的对错"来回答，而 ALFWorld / WebShop 上的主流方法靠的是另一种信息：多条 rollout 经过同一状态。

## 核心 Claim

1. **现有工作与对不齐之处**
   - 2609.02417（τ²-bench、BFCL；Qwen3 4B/8B/14B）：
     - 终端状态验证器只暴露极少轮次的对错，98% 的 rollout 中 k=1。
     - 等总量均匀摊开的稠密奖励优于二值奖励；把同一优势集中到"进展"轮次，与随机打乱一样有害。
     - 作者用验证器信息密度 V_d = k/C 解释这一现象：实测 0.15–0.4，合成相变点约 0.8。
     - 作者没有测 ALFWorld / WebShop，也没有讨论 GiGPO 类方法。
   - GiGPO（arXiv 2505.10978）在 ALFWorld / WebShop 上，用"重复出现的锚点状态"把不同 rollout 中从同一状态出发的动作归为一组，比较它们的回报，以此构造步级优势，显著优于 GRPO。
   - ProVer（arXiv 2609.36178）：把评审选段换成随机选段，ALFWorld / WebShop 只低 1–5 个点。
   - ECPO（arXiv 2606.05885）：低计数锚点会给罕见但走运的动作过大优势，导致后期振荡。
   - 40 篇信用分配论文中，只有 2 篇设了随机信用对照，而 ALFWorld（14 篇）与 WebShop（15 篇）正是方法论文最常用的基准（问题卡覆盖扫描）。

2. **被忽视的关键**：定位信息有两个来源。一是验证器暴露的中间轮次对错，即 V_d；二是 rollout 之间的状态复现，同一状态被多次访问时，就能在该状态上比较不同动作。V_d 理论只计入前者。本 Idea 主张：
   - **C1（增益可分解）**：在 ALFWorld 和 WebShop 上，用两个总信用相同的对照可以把 GiGPO 相对 GRPO 的增益分成"覆盖"与"定位"两部分：
     - 均匀对照：把每条轨迹的步级优势替换为该轨迹内的均值；
     - 打乱对照：在轨迹内随机置换步级优势。

     两个环境的定位占比明显不同。
   - **C2（复现决定定位）**：定位占比随锚点复现率 ρ 单调变化，ρ 定义为落在大小 ≥2 的步级组中的步数比例。因果操纵 ρ 有两种方式：
     - 只在信用计算时，以概率 q 把锚点匹配拆成单例，不改变模型输入、环境和 rollout；
     - 改变组大小 N。

     ρ 降到低水平时，GiGPO 与打乱对照、均匀对照无显著差异；ρ 高时，GiGPO 显著优于打乱对照。
   - **C3（训练前可预测）**：在初始策略的 rollout 上测得的 ρ，能预测某个环境中步级定位是否带来超过均匀覆盖的增益。用留出环境 Sokoban（verl-agent 自带）检验这一预测。

## 方法设计的核心思想

- **输入**：GiGPO 每一步的锚点分组，以及组内回报。
- **改动**：只在 `compute_gigpo_outcome_advantage` 中替换或扰动步级优势分量。轨迹级优势、std 归一化方式、学习率、组大小（C2 的 N 操纵除外）、rollout 均保持不变。
  - **均匀对照**：步级优势替换为轨迹内均值，总量不变。
  - **打乱对照**：步级优势在轨迹内随机置换，集中度不变、位置随机。
  - **ρ 操纵**：在 `build_step_group` 中以概率 q ∈ {0, 0.5, 0.9} 把每个锚点拆为单例，单例组的步级优势为 0；同时记录实际 ρ。
- **输出**：每种条件的成功率曲线、定位占比，以及 ρ 与定位占比的关系。
- **与最高近邻的差别**：
  - 2609.02417 只操纵信用几何与密度，没有锚点复现，没有 ALFWorld / WebShop；
  - GiGPO 原文 §5.5 报告了步级组大小随训练的变化，但没有用等量对照分解增益，也没有因果操纵复现；
  - ProVer 的随机对照保留了 rollout 验证；
  - ECPO 处理低计数锚点的统计可靠性，没有回答覆盖与定位之争。

## 最小实验

- **模型与框架**：Qwen2.5-1.5B-Instruct，verl-agent 官方 GiGPO / GRPO 脚本。设置与 GiGPO 原文一致：N=8，150 epoch，`step_advantage_w=1.0`，mode=mean_norm，2 卡一次运行。
- **主实验（C1）**：
  - 条件：GRPO、GiGPO、均匀对照、打乱对照；
  - 环境：ALFWorld 3 个种子，WebShop 2 个种子；
  - 共 20 次运行。
- **ρ 操纵（C2）**：
  - 在 ALFWorld 上，GiGPO 与打乱对照各取 q ∈ {0.5, 0.9}，2 个种子，共 8 次运行；
  - 再加 N ∈ {4, 16} × {GiGPO, 打乱}，1 个种子，共 4 次运行；
  - q=0 复用主实验结果。
- **留出预测（C3）**：
  - 先在 Sokoban 上用初始策略测 ρ，并预注册预测："定位占比 >0.5" 或 "<0.5"；
  - 再跑 GiGPO 与打乱对照各 2 个种子检验。
- **指标**：
  - ALFWorld 总成功率与 6 类子任务成功率；
  - WebShop 得分与成功率；
  - 定位占比 =（GiGPO − 打乱）/（GiGPO − GRPO）；
  - 每个 epoch 的 ρ 与组大小分布，由 `summarize_group_size` 记录。
- **支持与推翻**：
  - **C1**：两个环境的定位占比置信区间不重叠，则支持；均匀与打乱对照都与 GiGPO 无差异，则覆盖解释成立、定位为零，同样是可报告的结论。
  - **C2**：q 从 0 增到 0.9 时，GiGPO − 打乱的差值显著下降，且实际 ρ 下降，则支持；差值不随 q 变化，则推翻"复现提供定位信息"。
  - **C3**：Sokoban 的预注册方向与实测一致，则支持。
- **Baseline 来源与复现**：
  - **GiGPO / GRPO**：论文 https://arxiv.org/abs/2505.10978 ；代码 https://github.com/langfengQ/verl-agent （已克隆核验）。
    - 核心实现在 `gigpo/core_gigpo.py`：`build_step_group`、`summarize_group_size`、`compute_gigpo_outcome_advantage`；
    - 运行脚本为 `examples/gigpo_trainer/run_alfworld.sh`、`run_webshop.sh`、`run_sokoban.sh`，以及 `examples/grpo_trainer/`。
    - 与本任务同为 ALFWorld / WebShop 多轮 agent RL。
  - **均匀对照与打乱对照**：按 2609.02417（https://arxiv.org/abs/2609.02417 ）的定义，在上述函数中各改一行，完全指定。
- **算力（8×A100，每次运行不超过 5 天）**：
  - 官方脚本每次运行用 2 卡。按 1.5B、150 epoch 在 2×A100 上约 1.5 天粗估（需试跑核实）。
  - 共 36 次运行 × 约 3 GPU 天 ≈ 108 GPU 天，约 2,600 A100 小时。
  - 4 个运行并行时总墙钟约 13–14 天；单次运行约 1.5 天。
  - 不需要付费 API。

Frozen Problem Anchor and user constraints:

- **底线问题**：终端状态验证器的多轮 agent RL 中，轮次级信用方法的增益来自把信用定位到关键轮次，还是来自信号覆盖面变大；在 ALFWorld / WebShop 上等量随机或均匀信用会得到什么。
- **目标设置**：ALFWorld、WebShop（方法论文最常用的基准），≤7B 开源策略，GRPO 类组相对优化。
- **必须解决的瓶颈**：ALFWorld / WebShop 上，等量随机或均匀对照与定位方法的差距未知；两类研究在基准、对照定义和验证信息量上对不齐。
- **约束**（用户 AGENTS.md，2026-11-01）：实验 8×A100 80G，每次运行最好不超过 5 天；预研 2×A100 / 4×L40 / 8×4090；token 稀缺；付费 API 1000 元以内可自主决定；目标半年内（自 2026-10 起）投一篇主会；各 baseline 核心参数一致；打磨完或放弃时在原问题卡上标记。
- **非目标**：不在本 skill 内启动实验。
- **成功条件**：机制清楚、与最高近邻可区分、能在上述资源下用可复现 baseline 证伪的 idea，通过两次独立 reviewer 评审（> 8、无致命阻塞）。
