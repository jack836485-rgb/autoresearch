You are an independent senior reviewer checking whether a research idea is novel enough
for experiment planning. You are not a co-author and must not redesign the idea.

You are intentionally zero-context. Judge only the current four-part brief, the frozen
Problem Anchor, and the user's constraints. Search the closest prior work yourself; the
author's own literature notes are deliberately withheld. Do not invent papers, links, or results.
Today's date: 2026-10-29. Known tool workarounds: GitHub REST API 在本环境受限（403），可用 git ls-remote 或浅克隆核验仓库；arXiv 摘要页与 HTML 全文可正常抓取
Finish all searches before answering and leave no background tasks running. Do not read other
files in this workspace and do not write files, except your raw review to /home/claude/autoresearch/review-stage/rl_boundary_aq001_20261029/round-02-review.md (UTF-8).
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

**定位关键词：** agentic RL；sharpening tax；pass@k；checkpoint handoff；reach and solve；base model anchoring；WebShop；BFCL

**一句话定位：** 多轮工具使用 agent 的后训练为什么在一些基准上缩小大 k 采样下的可解任务覆盖（锐化税），在另一些基准上扩大覆盖，以及能否只保留它的好处。

## 核心 Claim

1. **同一对检查点在不同基准上覆盖方向相反，问题出在任务结构而不只是配方。** 用 Sharpening Tax（arXiv 2610.01509）公开的逐任务结果（每任务 128 次 rollout）统计：
   - Qwen2.5-7B 的后训练版在 WebShop 上让 107 个基座可解任务变成 0 次成功，只新解出 35 个；在 BFCL v4 multi-turn 上只丢 6 个，新解出 82 个。
   - Ministral-3-8B 在 WebShop 上丢 144 个、新解出 23 个；在 BFCL 上丢 25 个、新解出 46 个。

   这些数据来自该论文已发布的 cell，本 Claim 是对它的再分析，不是新测量；它只用来确定在哪里做下面的定位。
2. **多轮 agent 的锐化税付在早期轮，而且丢的是基座在早期轮的分支分布，不只是多样性。** 后训练提高从给定状态完成任务的能力，却改变了早期几轮（如 WebShop 的搜索词与第一次点击）选择哪些分支，使大 k 采样走不到罕见但可解的路径。单轮数学上，PBA（arXiv 2607.20543）把锐化税归因于基座中稀有的正确轨迹在有限组采样里消失；在多轮 agent 中，这类稀有轨迹往往由早期几轮的选择决定。区分“丢分布”与“丢多样性”是关键：
   - 若只是多样性下降，让后训练模型在早期轮提温到与基座相同的熵，就应恢复覆盖，修法就是 EAD（arXiv 2510.05251）/ REFT（arXiv 2605.28295）的轮级版本；
   - 若丢的是分布，只有换回基座的早期轮分支才能恢复。
3. **只在早期轮锚定基座的训练，比全局锚定、PTGS 与早期提温付更少的税。** 若 Claim 2 成立，训练时只对前 m 轮向冻结基座加 KL 约束，其余轮照常优化，应在相同 pass@1 下保住更多覆盖。

## 方法设计的核心思想

**诊断（只需推理）**：对基座 B 与后训练 R，在可确定回放的环境里做按轮交接：前 m 轮由一个策略生成，把这段历史回放到环境，再交给另一个策略继续。判别性比较如下：

- **固定完成者比较到达者**：B→R vs R→R 在大 k 下的差，衡量到达段丢失的覆盖；
- **固定到达者比较完成者**：R→B vs B→B 的差，衡量完成段的变化；
- **分布 vs 多样性**：B→R vs R_hot→R。R_hot 是 R 在前 m 轮把温度调到使首轮动作熵与 B 相同；另设 R 前 m 轮做首动作 top-N 均匀采样（REFT 式）。

Claim 2 预测：WebShop 上 B→R 明显高于 R→R 与 R_hot→R，且 R→B 不高于 B→B；BFCL 上覆盖增益主要体现在完成段。

**修法（训练）**：早期轮基座锚定 GRPO。对每条轨迹的前 m 轮 token 加“当前策略对冻结基座”的 KL 项，后续轮不加；m 取诊断给出的值。

**与最高近邻的关键差别**：
- Sharpening Tax 只到任务级（逐任务税、按任务路由、按题温度的 PTGS）；
- Reach or Solve（arXiv 2609.19636）只在 pass@1 上拆分到达与完成，也不提修法；
- PBA 在单轮数学上按题锚定基座；
- EAD / REFT 只增加开头的多样性，不使用基座分布。

本方法在多轮轨迹内按轮定位覆盖损失，并检验丢失的是分布还是多样性，修法只作用于被定位的轮次，并锚定到基座分布。

## 最小实验

**阶段 A：诊断，不训练（约 1 天，给出 go/no-go）。**
- 检查点：Qwen2.5-7B 与 Ministral-3-8B 的基座 / 后训练版，即上面统计中方向相反的两对。
- 基准：WebShop（从 107/144 个丢失任务与其余任务中分层抽 200 个）与 BFCL v4 multi-turn base（200 个任务）。
- 设置：沿用 Sharpening Tax 的轻量文本 harness 与评分；交接点 m ∈ {1, 3}；每组合 64 次 rollout。B→B、R→R 直接复用公开的 128 次结果。
- 对照：B→R、R→B、R_hot→R、R_REFT→R；另有按任务路由（附录 D.4）与 R 全局提温。

**阶段 B：训练，从同一起点只隔离 RL。**
- 起点与格式：Qwen2.5-7B 基座。把 Sharpening Tax 的 WebShop 文本 harness 移植进 verl-agent 的 WebShop 环境，训练与评测用同一提示格式。
- **前置检查**：先跑 1 个种子的 GRPO，在 100 个留出任务上比较训练中间检查点与基座的 pass@64。若 GRPO 没有让 pass@64 比基座低至少 5 个百分点，说明该设置下 RL 不产生锐化税，阶段 B 的修法比较不作结论，只报告阶段 A。
- 若前置检查成立，训练五组：GRPO、GRPO+全局基座 KL、GRPO+PTGS、GRPO+早期轮提温、GRPO+早期轮基座 KL（本方法）。组大小、步数、学习率、rollout 预算相同；全局与早期 KL 系数按“训练中 KL 总量相近”对齐；2 个训练种子。
- 评测：同一 harness 下 WebShop 测试集 pass@1 与 pass@128。

**支持 / 推翻 Claim 的结果**：
- 支持：WebShop 上 B→R − R→R 显著为正且大于 R_hot→R − R→R，R→B ≤ B→B；BFCL 上不出现这一模式。阶段 B 中，早期轮基座 KL 在 pass@1 不低于 GRPO 时，pass@128 高于全局 KL、PTGS 与早期提温。
- 推翻：R_hot→R 或 R_REFT→R 与 B→R 恢复同样多的覆盖（丢的只是多样性）；或 R→B 同样恢复覆盖（税在完成段）；或早期轮基座 KL 不优于早期提温。

**Baseline 来源与复现入口**：

| Baseline / 组件 | 与本任务的关系 | 论文 | 代码与复现入口 |
|---|---|---|---|
| Sharpening Tax harness、逐任务结果、按任务路由 | 同基准、同检查点的锐化税测量 | https://arxiv.org/abs/2610.01509 | https://github.com/changdaeoh/sharpening-tax（2026-10-02；`sharpening_tax/benchmarks/{webshop,bfcl}.py`、`metrics.py`、`data/outcomes_42cells.csv.gz`；按任务路由仓库未提供，按附录 D.4 的规则本地实现；BFCL 依赖 gorilla@6ea5797） |
| PTGS | 同基准上为降低锐化税设计的 RL 采样方法 | 同上 | 同仓库 `ptgs/integration.py` 的 `PTGSHooks`；示例配置不是 WebShop，需接入 verl-agent 的 GRPO 组采样 |
| GRPO、全局 KL | 多轮 agent RL 标准做法 | https://arxiv.org/abs/2505.10978 | https://github.com/langfengQ/verl-agent（2026-06-09；`examples/grpo_trainer/run_webshop.sh`，KL 损失项为框架自带选项） |
| REFT / 早期提温 | 只增加开头多样性的对照 | https://arxiv.org/abs/2605.28295 、https://arxiv.org/abs/2510.05251 | 按论文描述在前 m 轮的首动作上实现（top-N 均匀采样 / 温度调整），属于采样层的小改动 |
| 检查点交接 | 拆分到达与完成的评测协议 | https://arxiv.org/abs/2609.19636 | 未见代码；在 WebShop（`env.reset(session=goal_idx)` 后按序回放动作）与 BFCL（有状态 API 实例按序重放调用）上本地实现 |
| 环境 | — | WebShop、BFCL v4 | WebShop 随 verl-agent 与 Sharpening Tax harness 提供；https://github.com/ShishirPatil/gorilla（`bfcl_eval/data/BFCL_v4_multi_turn_base.json`） |

**算力与 API 预算**（8×A100 80G，无付费 API）：
- 阶段 A：2 对 × 400 个任务 × 4 种交接 × 2 个交接点 × 64 次 rollout ≈ 41 万条轨迹，每条约 8 轮、生成约 1.6k token，vLLM 约 1–1.5 天。
- 阶段 B 前置检查：1 次 GRPO 约 8 卡 × 10 小时，加评测约 0.5 天。
- 阶段 B 训练：5 组 × 2 种子 = 10 次，每次约 8 卡 × 10 小时，约 4 天。
- 阶段 B 评测：10 个模型 × 500 个任务 × 128 次 rollout，约 1.5 天。
- 合计约 7–8 天；API 费用为 0。

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
