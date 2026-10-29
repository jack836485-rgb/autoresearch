You are an independent senior reviewer checking whether a research idea is novel enough
for experiment planning. You are not a co-author and must not redesign the idea.

You are intentionally zero-context. Judge only the current four-part brief, the frozen
Problem Anchor, and the user's constraints. Search the closest prior work yourself; the
author's own literature notes are deliberately withheld. Do not invent papers, links, or results.
Today's date: 2026-10-29. Known tool workarounds: GitHub REST API 在本环境受限（403），可用 git ls-remote 或浅克隆核验仓库；arXiv 摘要页与 HTML 全文可正常抓取
Finish all searches before answering and leave no background tasks running. Do not read other
files in this workspace and do not write files, except your raw review to /home/claude/autoresearch/review-stage/rl_boundary_aq001_20261029/round-06-review.md (UTF-8).
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

**定位关键词：** multi-turn agent RL；pass@k coverage；diversity collapse；entrance locking；checkpoint handoff；forward KL；WebShop

**一句话定位：** 单轮 RLVR 的覆盖收缩已被定位在“入口”（第一步）；多轮工具 agent 每次收到环境观察都会面对新的决策点，RL 造成的大 k 采样覆盖损失是只发生在入口，还是在观察之后被重新锁定，以及修法该作用在哪些轮。

## 核心 Claim

**已知**：
- **Locked at the Entrance**（arXiv 2608.29188）：在单轮 Countdown 与数学任务上发现，RLVR 的覆盖收缩集中在入口，补上入口前缀后替代分支仍可执行；提温与提示无效，晚层参数插值有效。
- **DivInit**（arXiv 2606.17209）：在 agent 搜索上把并行采样瓶颈追到第一轮查询冗余。
- **Sharpening Tax**（arXiv 2610.01509）：报告 WebShop 上后训练普遍付锐化税，但只做任务级分析，比较的是混合了 SFT、偏好优化与 RL 的发布检查点。
- **DDO**（arXiv 2609.10052）：在 WebShop 等环境中，用大模型专家在共享决策状态收集多条成功分支，做离线偏好训练以提高成功策略覆盖。它说明中段决策状态与覆盖有关，但不诊断 RL 在哪里锁定，也不在 RL 内修。

1. **区分“入口锁定”与“观察后重新锁定”。** 设 B 为基座，G 为从 B 出发、同一设置下只做 GRPO 的检查点。逐轮替换只把第 t 轮动作换成 B 生成，其余轮由 G 生成，并在真实环境中继续。减去同模型分叉的噪声底后，得到逐轮“可找回覆盖”剖面 L(t)。
   - 我们的假设是 WebShop 上存在重新锁定：搜索结果返回后的决策轮也贡献相当部分 L(t)，只替换第一轮找回的覆盖明显少于替换全部决策轮。
   - 若 L(t) 集中在第一轮，单轮的入口结论迁移到多轮 agent。这一结果同样报告，并据此修改 Claim 3 的处方。
2. **在观察后的被锁定轮上，丢的是基座的分支分布，不只是多样性。** 单轮上“提温无效”已由 2608.29188 报告。本 Claim 只主张：在观察之后的决策轮上，把 G 提温到与 B 等熵，或做首动作 top-N 均匀采样（REFT 式，arXiv 2605.28295），找回的覆盖仍少于基座替换。
3. **修法应按锁定剖面开处方：锚定哪些轮，比锚定多少更重要。** 训练时只在剖面选出的轮上，对基座施加前向 KL（损失与估计方式沿用 DPH-RL，arXiv 2509.07430）。预期它在相同 pass@1 下的 pass@64 高于以下各组：
   - 入口前向 KL；
   - 全局前向 KL；
   - **随机选轮前向 KL**：锚定的 token 占比与本方法相同，但轮次随机抽取；
   - 熵奖励与 PTGS。

**推翻条件**：
- Claim 1：L(t) 在第 1 轮之后与噪声底无显著差别（此时 Claim 1 不成立，处方改为入口）；
- Claim 2：等熵提温 / REFT 在同样轮上找回同样多；
- Claim 3：随机选轮与按剖面选轮的前沿相当（起作用的只是锚定量）。

## 方法设计的核心思想

**诊断（逐轮替换剖面）**：
- 对每个 t，在真实环境中由 G 运行到第 t−1 轮，第 t 轮由 B 生成，之后回到 G 继续；对照是第 t 轮由 G 重新采样。两者都在固定 `WEBSHOP_ENV_SEED` 下重建环境状态，因为 Replay Gap（arXiv 2608.08239）指出拼接日志回放不可靠。
- L(t) = 两者 pass@64 之差。
- 聚合比较：只替换第一轮 / 替换全部决策轮 / 在全部决策轮上等熵提温 / 在全部决策轮上做 REFT 式多样化。
- 决策轮由动作类型与上一条观察的页面类型直接判定：发出搜索的轮、在搜索结果页上做选择的轮。

**处方**：按剖面把显著高于噪声底的轮型选为锚定轮集合 S。若只有入口显著，S = {第 1 轮}。

**修法（按剖面开处方的前向 KL GRPO）**：
1. 训练前离线采样基座轨迹，保存 S 中各轮的“观察历史—动作”片段。
2. 训练时在 GRPO 损失外，加当前策略对这些基座动作的负对数似然，即 S 上状态分布的前向 KL(π_B‖π)。
3. 其余轮不加散度。

**与最高近邻的关键差别**：
- Locked at the Entrance：单轮、无观察后决策点、修法为权重插值；
- DivInit：只做第一轮、测试时；
- DDO：离线偏好训练、需要大模型专家分支、不做 RL 前后定位；
- Reach or Solve（arXiv 2609.19636）：SFT↔RL 发布检查点、pass@1、交接点接近终点、无修法；
- DPH-RL：单轮、整条序列。

本方法在多轮 agent 的纯 RL 检查点上，用真实环境逐轮替换区分入口锁定与重新锁定，并用随机选轮对照检验“按剖面选轮”本身的作用。

## 最小实验

**阶段 0：前置检查（约 0.5 天）。**
- 设置：Qwen2.5-7B 基座 B。把 Sharpening Tax 的 WebShop 文本 harness 移植进 verl-agent 的 WebShop 环境，商品子集、步数上限与 `WEBSHOP_ENV_SEED` 都和 harness 一致，训练与评测同一设置。
- 做法：跑 1 个种子的 GRPO 得到 G，在 300 个留出任务上重新测 B 与 G 的 pass@1、pass@64。
- 判定：只有 G 的 pass@64 比 B 低至少 5 个百分点才继续；否则报告“该设置下纯 RL 不产生锐化税”并停止。PASS@(k,T)（arXiv 2604.14877）报告工具 RL 可扩大边界，这一结果是可能的。

**阶段 A：诊断（约 1.5 天）。**
- 在 (B, G) 上用 300 个留出任务，做 t = 1…6 的逐轮替换与同模型分叉，每格 64 次 rollout。
- 4 个聚合替换组，以及入口类测试时对照：DivInit 第一轮多样化；对 G 用 2608.29188 的晚层插值（与 G 的早期检查点混合）。
- 外部印证：在发布的 Qwen2.5-7B、Ministral-3-8B 对上做第一轮与全部决策轮两个聚合替换，同一段历史按各模型自身格式（文本 harness / chat）重新渲染后再交给对方。

**阶段 B：训练修法比较（约 7.5 天训练 + 1.5 天评测）。**
- 起点：B；同一设置。
- 七组：GRPO、GRPO+PTGS、GRPO+熵奖励（加在 S 上）、全局前向 KL、入口前向 KL、随机选轮前向 KL（与 S 的锚定 token 占比相同，每个 batch 重新抽轮）、按剖面前向 KL（本方法）。
- 系数：本方法与全局前向 KL 各扫 3 个系数、入口与随机选轮各扫 2 个，均为 1 个种子，画 pass@1–pass@64 前沿；再在 pass@1 与 GRPO 最接近的系数上，把本方法与全局前向 KL 补到 3 个种子。
- 种子：GRPO、PTGS、熵奖励各 3 个种子（阶段 0 的 GRPO 计为第 1 个）。
- 控制：所有组组大小、步数、学习率、rollout 预算相同，前向 KL 组用同一批离线基座样本。
- 评测：300 个留出任务的 pass@1 与 pass@64，按任务配对 bootstrap 报告置信区间。

**支持 / 推翻 Claim 的结果**：
- 支持：L(t) 在第 1 轮之后的决策轮仍显著高于噪声底；只替换第一轮明显少于替换全部决策轮；等熵提温与 REFT 少于基座替换；DivInit 与晚层插值不及全部决策轮替换；按剖面前向 KL 的前沿支配入口、全局与随机选轮前向 KL，并优于熵奖励与 PTGS。
- 推翻：见核心 Claim 中的推翻条件。

**Baseline 来源与复现入口**：

| Baseline / 组件 | 与本任务的关系 | 论文 | 代码与复现入口 |
|---|---|---|---|
| Sharpening Tax harness、指标 | 同基准的锐化税测量 | https://arxiv.org/abs/2610.01509 | https://github.com/changdaeoh/sharpening-tax（2026-10-02；`sharpening_tax/benchmarks/webshop.py`、`metrics.py`） |
| PTGS | 同基准上降低锐化税的 RL 采样方法 | 同上 | 同仓库 `ptgs/integration.py` 的 `PTGSHooks`，接入 verl-agent 的 GRPO 组采样（原作只在 Sokoban / FrozenLake 验证，需移植） |
| GRPO、熵奖励 | 多轮 agent RL 标准做法 | https://arxiv.org/abs/2505.10978 | https://github.com/langfengQ/verl-agent（2026-06-09；`examples/grpo_trainer/run_webshop.sh`；熵项为框架选项，按轮掩码） |
| 全局 / 入口 / 随机选轮 / 按剖面前向 KL | 保 pass@k 的质量覆盖型散度 | https://arxiv.org/abs/2509.07430 | https://github.com/seamoke/DPH-RL（2026-02-10；README 的离线采样与 `forward` 散度配置；损失项移植到 verl-agent 并按轮掩码） |
| 晚层参数插值 | 单轮入口锁定的修法 | https://arxiv.org/abs/2608.29188 | https://github.com/ershiyidian/early-branch-locking（2026-09-01；`src/early_branch_locking/countdown/layer_interpolation.py`，权重插值与任务无关） |
| DivInit | agent 搜索的第一轮多样化 | https://arxiv.org/abs/2606.17209 | https://github.com/cxcscmu/diverse-query-initialization（main 可访问），用于第一轮动作 |
| REFT / 等熵提温 | 只增加多样性的对照 | https://arxiv.org/abs/2605.28295 | 在选定轮的首动作上做 top-N 均匀采样 / 温度调整，采样层小改动 |
| 逐轮替换与分叉 | 真实环境中的检查点交接 | https://arxiv.org/abs/2609.19636 、https://arxiv.org/abs/2608.08239 | https://github.com/Xuanxuana1/AgenticRL_Handoff（2026-09-26；`src/handoff/` 现有 ALFWorld / TravelPlanner），为 WebShop 增加固定 `WEBSHOP_ENV_SEED` 后的真实环境回放与单轮替换 |

**算力与 API 预算**（8×A100 80G，无付费 API）：
- 阶段 0：1 次 GRPO 约 8 卡 × 8–10 小时，加评测，约 0.5 天。
- 阶段 A：300 个任务 ×（6 轮 × 2 + 4 聚合 + 2 测试时对照）× 64 ≈ 34.6 万条轨迹，外部印证约 5 万条；每条约 8 轮、生成约 1.6k token，vLLM 约 1.5 天。
- 阶段 B：系数扫描 10 次 + 补种子 4 次 + GRPO 2 次 + PTGS 3 次 + 熵奖励 3 次 = 22 次训练，每次约 8 卡 × 8 小时，约 7.3 天；评测 22 个模型 × 300 个任务 × 64 次，约 1.5 天。
- 合计约 11 天；API 费用为 0。阶段 0 与阶段 A 共约 2 天，即可判断 Claim 1、2 并确定处方 S，再决定是否投入阶段 B。

Frozen Problem Anchor and user constraints:

- **根本问题**：多轮工具使用 agent 的 RL 什么时候扩大可解任务集合、什么时候只锐化已有行为；发布模型的大 k 覆盖损失与受控工具 RL 的能力扩展为何相反。
- **目标领域与设置**：LLM agent 的 agentic RL（GRPO 类，可验证奖励）；多轮工具使用或 web / 终端类可程序评分基准；pass@k 与 pass@(k,T) 覆盖评测；开源 ≤9B 模型为主。
- **必须解决的瓶颈**：覆盖损失与扩展的来源未分离（SFT、偏好优化还是 RL；任务结构；harness 格式），没有在同一起点上只隔离 RL 阶段、按初始可达性分层的证据，也没有能利用这一判断的方法。
- **约束**：
  - 算力：预研 2×A100 80G / 4×L40 48G / 8×4090 24G；正式实验 8×A100 80G。
  - API：1000 元以内可自主决定；token 资源稀缺。
  - 时间与目标：半年内（自 2026-10 起）投一篇主会。
  - 实验代码与数据集在服务器上通过 ssh 开发，不存本地。
  - 非目标：从头预训练；依赖大规模异步 RL 基础设施的方案。
- **成功条件**：得到一个在 ≤9B、8×A100 上可完成最小实验、baseline 可复现、Claim 可被实验推翻且通过两轮独立 reviewer 门槛的 idea。
