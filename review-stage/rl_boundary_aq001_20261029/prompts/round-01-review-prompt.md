You are an independent senior reviewer checking whether a research idea is novel enough
for experiment planning. You are not a co-author and must not redesign the idea.

You are intentionally zero-context. Judge only the current four-part brief, the frozen
Problem Anchor, and the user's constraints. Search the closest prior work yourself; the
author's own literature notes are deliberately withheld. Do not invent papers, links, or results.
Today's date: 2026-10-29. Known tool workarounds: GitHub REST API 在本环境受限（403），可用 git ls-remote 或浅克隆核验仓库；arXiv 摘要页与 HTML 全文可正常抓取
Finish all searches before answering and leave no background tasks running. Do not read other
files in this workspace and do not write files, except your raw review to /home/claude/autoresearch/review-stage/rl_boundary_aq001_20261029/round-01-review.md (UTF-8).
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

**定位关键词：** agentic RL；sharpening tax；pass@k；checkpoint handoff；reach and solve；exploration；WebShop；BFCL

**一句话定位：** 多轮工具使用 agent 的后训练（以 RL 为主）为什么在一些基准上缩小大 k 采样下的可解任务覆盖（锐化税），在另一些基准上扩大覆盖，以及能否只保留它的好处。

## 核心 Claim

1. **扩展与锐化的矛盾不只来自配方，同一对检查点在不同基准上方向相反。** Sharpening Tax（arXiv 2610.01509）在 14 对发布的基座 / 后训练检查点上发现后训练普遍缩小大 k 覆盖，并报告全局调温度不能化解准确率与覆盖的矛盾；Pass@(k,T)（arXiv 2604.14877）在受控工具 RL 上看到大 k 扩展。用 Sharpening Tax 公开的逐任务结果（每任务 128 次 rollout）按 pass@k 无偏估计计算：Qwen2.5-7B 的后训练版在 BFCL v4 multi-turn 上 pass@128 比基座高 38.0 个百分点，在 WebShop 上低 14.4；Ministral-3-8B 分别为高 10.5、低 24.2。
2. **多轮 agent 的覆盖变化应拆成“到达可解状态”与“从该状态完成”两段，锐化税付在到达段。** 后训练提高从给定状态完成任务的能力，却让早期几轮的分支选择（如 WebShop 的搜索词与翻页）塌缩，使大 k 采样走不到那些罕见但可解的路径。任务成败主要卡在早期探索时表现为锐化税，主要卡在执行时表现为扩展。Reach or Solve（arXiv 2609.19636）已用检查点交接在单次成功率上分离到达与完成，但没有在大 k 覆盖上做，也没有据此改变训练或解码。
3. **只在到达段保留多样性，就能同时得到后训练的单次准确率和基座的覆盖。** 预期：在 WebShop 上，“前 m 轮基座、其余轮后训练模型”的按轮交接解码，pass@128 不低于基座、pass@1 接近后训练模型，而反向交接恢复不了覆盖；在 BFCL 上覆盖增益主要来自完成段。训练时只在早期 m 轮锚定起始策略，在相同 pass@1 下比 PTGS 与全局提温付更少的税。若反向交接同样恢复覆盖，或覆盖损失在各轮均匀分布，则 Claim 2 被推翻。

## 方法设计的核心思想

**诊断（只需推理）**：对一对基座 B / 后训练 R 检查点，在可确定回放的环境里做四种按轮交接：B→B、B→R、R→B、R→R。前 m 轮由前一个策略生成，然后把这段历史原样回放到环境，交给后一个策略继续。对每种组合、每个 m 画 pass@k 曲线（k 至 64 或 128），并按任务统计覆盖从哪一段丢失。另记录早期轮的分支多样性（不同首轮动作与搜索词的数量），检验它与逐任务锐化税的关系。

**修法 1（测试时）**：按轮交接解码。前 m 轮用基座或更高温度采样，之后切换到后训练模型；m 由诊断给出。

**修法 2（训练时）**：早期轮锚定 GRPO。只在每条轨迹的前 m 轮对起始策略加 KL 约束（或提高这几轮的采样温度），其余轮照常优化。

**与最高近邻的关键差别**：
- Sharpening Tax 的诊断与修法都在任务级（逐任务锐化税、按任务路由、按题设温度的 PTGS）；
- Reach or Solve 只在 pass@1 上拆分到达与完成；
- EAD（arXiv 2510.05251）在单轮生成里做 token 级“先高温后低温”。

本方法在多轮轨迹内部按轮定位覆盖损失，并只在被定位的那一段干预。

## 最小实验

**阶段 A：诊断，不训练。**
- 检查点：Sharpening Tax 已发布的 ≤9B 对，即 Qwen3.5-4B、Qwen3.5-9B、Qwen2.5-7B（基座 / 后训练）。
- 基准：WebShop（取 200 个任务）与 BFCL v4 multi-turn base（200 个任务）。上面的计算已确认在这些检查点和基准上存在方向相反的覆盖变化。
- 设置：沿用 Sharpening Tax 的轻量文本 harness 与评分；交接点 m ∈ {1, 3}；每组合 64 次 rollout。B→B、R→R 的 128 次 rollout 结果可直接复用公开数据。
- 对照：B→B、R→R；按任务路由（Sharpening Tax 附录 D.4，用 8 次 rollout 估计逐任务税后选模型）；R 加全局高温采样。

**阶段 B：训练，从同一起点只隔离 RL。**
- 起点：Qwen2.5-7B-Instruct（verl-agent 的 WebShop 标准设置）。
- 在 WebShop 上训练三组：GRPO、GRPO+PTGS、GRPO+早期轮锚定。组大小、步数、学习率、rollout 预算相同，2 个训练种子。
- 统一用 Sharpening Tax harness 评测 pass@1 与 pass@128。

**支持 / 推翻 Claim 的结果**：
- 支持：WebShop 上 B→R 的 pass@128 ≥ B→B 且 pass@1 接近 R→R，而 R→B 不恢复覆盖；BFCL 上覆盖增益随交接点后移而保持，说明来自完成段；早期轮锚定在 pass@1 不低于 GRPO 时，pass@128 高于 GRPO 与 GRPO+PTGS。
- 推翻：R→B 与 B→R 同样恢复覆盖；或覆盖损失不随交接点集中；或早期轮锚定不优于 PTGS。

**Baseline 来源与复现入口**：

| Baseline / 组件 | 与本任务的关系 | 论文 | 代码与复现入口 |
|---|---|---|---|
| Sharpening Tax harness、逐任务结果、按任务路由 | 同基准、同检查点的锐化税测量 | https://arxiv.org/abs/2610.01509 | https://github.com/changdaeoh/sharpening-tax（2026-10-02；`sharpening_tax/benchmarks/{webshop,bfcl}.py`、`sharpening_tax/metrics.py`、`data/outcomes_42cells.csv.gz`；BFCL 依赖 gorilla@6ea5797） |
| PTGS | 同基准上为降低锐化税而设计的 RL 采样方法 | 同上 | 同仓库 `ptgs/integration.py` 的 `PTGSHooks`，接入 GRPO 的组采样温度 |
| GRPO（WebShop） | 多轮 agent RL 的标准做法 | https://arxiv.org/abs/2505.10978 | https://github.com/langfengQ/verl-agent（2026-06-09；`examples/grpo_trainer/run_webshop.sh`） |
| 检查点交接 | 拆分到达与完成的评测协议 | https://arxiv.org/abs/2609.19636 | 论文未见代码；协议为“回放前一策略的前 m 轮动作再交给后一策略”，在 WebShop（`env.reset(session=goal_idx)` 后按序回放）与 BFCL（有状态 API 实例按序重放调用）上可直接本地实现 |
| 环境 | — | WebShop、BFCL v4 | WebShop 随 verl-agent 与 Sharpening Tax harness 提供；https://github.com/ShishirPatil/gorilla（`berkeley-function-call-leaderboard/bfcl_eval/data/BFCL_v4_multi_turn_base.json`） |

**算力与 API 预算**（8×A100 80G，无付费 API）：
- 阶段 A：3 对检查点 × 400 个任务 × 2 种交接 × 2 个交接点 × 64 次 rollout ≈ 30.7 万条轨迹，每条约 8 轮、生成约 1.6k token，vLLM 推理约 1 天。
- 阶段 B 训练：3 组 × 2 种子 = 6 次，每次约 8 卡 × 12 小时，约 3 天。
- 阶段 B 评测：6 个模型 × 500 个任务 × 128 次 rollout，约 1 天。
- 合计约 5 天；API 费用为 0。阶段 A 约 1 天即可给出 go/no-go。

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
