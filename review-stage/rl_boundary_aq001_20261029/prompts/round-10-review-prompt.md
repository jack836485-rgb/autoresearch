You are an independent senior reviewer checking whether a research idea is novel enough
for experiment planning. You are not a co-author and must not redesign the idea.

You are intentionally zero-context. Judge only the current four-part brief, the frozen
Problem Anchor, and the user's constraints. Search the closest prior work yourself; the
author's own literature notes are deliberately withheld. Do not invent papers, links, or results.
Today's date: 2026-10-29. Known tool workarounds: GitHub REST API 在本环境受限（403），可用 git ls-remote 或浅克隆核验仓库；arXiv 摘要页与 HTML 全文可正常抓取
Finish all searches before answering and leave no background tasks running. Do not read other
files in this workspace and do not write files, except your raw review to /home/claude/autoresearch/review-stage/rl_boundary_aq001_20261029/round-10-review.md (UTF-8).
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

**定位关键词：** multi-turn agent RL；pass@k coverage；diversity collapse；checkpoint handoff；forward KL；replay；WebShop；ALFWorld

**一句话定位：** RL 会让多轮工具 agent 在大 k 采样下丢失可解任务覆盖。现有保覆盖方法有的在单轮上提出（DPH-RL、TAR、入口修复），有的在多轮上提出但只在任务级或第一轮上操作（PTGS、DivInit）；它们在多轮轨迹中实际作用于哪里、因此能找回多少覆盖，尚无检验。

## 核心 Claim

**已知与归属**：
- **单轮上提出的方法**：
  - Locked at the Entrance（arXiv 2608.29188）在单轮 Countdown / 数学上把 RLVR 的覆盖收缩定位到入口，晚层插值有效；
  - DPH-RL（arXiv 2509.07430）用离线基座样本上的前向 KL 保 pass@k；
  - TAR（arXiv 2610.24236）回放被抑制的基座多样成功解。
- **多轮上提出、但只在任务级或第一轮操作的方法**：
  - Sharpening Tax（arXiv 2610.01509）在 WebShop、BFCL、ACEBench 上做任务级的锐化税测量；它提出的 PTGS 按题调采样温度，在多轮 Sokoban / FrozenLake 上验证；
  - DivInit（arXiv 2606.17209）在多轮搜索 agent 中只修第一轮查询。
- **协议与理论来源**：
  - 检查点交接来自 Reach or Solve（arXiv 2609.19636）；
  - 真实环境分叉与同模型噪声底来自 The Replay Gap（arXiv 2608.08239）；
  - 学生偏离基座状态属于 DAgger 式协变量偏移，多轮蒸馏中的讨论见 ReOPD（arXiv 2607.04763）。

1. **按轮定位：区分入口锁定与观察后重新锁定。**
   - 设 B 为起点策略，G 为从 B 出发、同一设置下只做 GRPO 的检查点。
   - 在真实环境中逐轮替换：只把第 t 轮换成 B 生成，其余由 G 生成并继续，减去同模型分叉的噪声底，得到可找回覆盖剖面 L(t)。
   - 比较只在替换轮数相同的组之间进行。
   - 在 WebShop 与 ALFWorld 上分别报告。剖面落在哪里都报告，不作为成败条件。
2. **测试时对应物预测训练方法的覆盖增益（主贡献）。** 每族方法有一个可在推理期直接测量的对应物，它描述“基座在该方法够得着的位置上接管”能找回多少覆盖：

   | 方法族 | 代表方法 | 测试时对应物 |
   |---|---|---|
   | 入口 | 入口前向 KL | B 只接管第 1 轮 |
   | 离线回放 | DPH-RL、TAR | 每一轮若 G 当前环境状态与该任务某条基座成功轨迹的状态相同，则由 B 接管 |
   | 采样侧 | PTGS | G 在所有轮把温度调到与 B 首动作等熵 |
   | 剖面处方 | 按剖面选轮的前向 KL | B 接管剖面选出的轮集合 S |
   | 随机选轮 | 同 token 占比随机选轮的前向 KL | B 接管同数量的随机轮 |

   - 对应物增益 P_m(i) 定义为对应物的 pass@32 减去 G 的 pass@32，按任务 i 直接测量，不做跨轮相加。
   - 预测：任务 i 上，训练方法 m 相对 GRPO 的 pass@32 增益 Δ_m(i) 与 P_m(i) 正相关。具体为合并所有方法与任务、含方法固定效应的回归，斜率 b > 0；且同一环境内，各方法平均增益的排序与平均对应物增益的排序一致。
   - 训练方法会改变整条策略，不只作用于对应物所示位置；本 Claim 正是检验这一近似在多大程度上成立。
3. **处方**：由 Claim 2，剖面选轮前向 KL 应找回最多覆盖，并优于同 token 占比的随机选轮。Coverage, Not Targeting（arXiv 2609.02417）发现信用分配的定向与随机同样有害；我们假设锚定与之不同，因为它作用于分布而非奖励。这个假设由随机选轮对照直接检验。

**推翻条件**：
- Claim 2：在阶段 A 后预注册的最小可检出效应之下，斜率 b 的 95% 置信区间包含 0；或方法排序与对应物排序的 Kendall τ ≤ 0。
- Claim 3：剖面选轮前向 KL 不优于随机选轮。

## 方法设计的核心思想

**测量（只用推理）**：
- 在 (B, G) 上做逐轮替换、同模型分叉和五个对应物；WebShop 固定 `WEBSHOP_ENV_SEED`，ALFWorld 固定游戏文件与种子。
- 离线回放对应物所用的基座成功轨迹库，与训练离线回放方法所用的是同一批离线样本。状态等价按环境状态程序判定：WebShop 比较页面类型与当前检索结果 / 商品；ALFWorld 比较位置、物品与容器状态。

**处方方法**：在 S 中各轮的离线基座成功片段上，对当前策略加负对数似然（前向 KL(π_B‖π)，估计方式同 DPH-RL），其余轮不加。

**与最高近邻的关键差别**：
- 现有方法各自提出了一种保覆盖的手段，但没有给出在多轮轨迹中该方法作用于哪里、能找回多少的可测预测；
- Sharpening Tax 的按任务路由在基座与后训练模型之间整条轨迹切换，不做按轮接管，也不预测训练方法的效果；
- Reach or Solve 只比较 SFT↔RL 的到达与完成成功率。

## 最小实验

**阶段 0：前置检查（约 1 天）。**
- WebShop：
  - B = Qwen2.5-7B 基座。Sharpening Tax 的 WebShop 文本 harness 移植进 verl-agent，商品子集、步数上限与 `WEBSHOP_ENV_SEED` 一致，训练与评测同一设置。
  - 训练用 WebShop train 划分。留出评测取 800 个不在训练中的目标；若该商品子集下不足 800 个，改用全量商品索引，并同步修改 harness。
- ALFWorld：
  - B = Qwen2.5-7B 基座；若其 pass@32 低于 30%，改用 Qwen2.5-7B-Instruct 作起点。
  - 留出评测取 unseen 134 个 + seen 140 个任务。
- 各跑 1 个种子的 GRPO 得到 G。进入后续的门槛：G 的 pass@32 比 B 低至少 5 个百分点，且至少有 60 个任务“B 有成功、G 32 次全失败”。都不满足则报告“纯 RL 不产生锐化税”并停止。

**阶段 A：测量（约 2.5 天）。**
- WebShop 800 个任务（t = 1…6）、ALFWorld 274 个任务（t ∈ {1, 2, 4, 8, 12, 16}）。
- 每格做逐轮替换与同模型分叉，32 次 rollout，含剂量匹配组；五个对应物各 32 次。
- 功效分析：用阶段 0 的 G 与额外 2 个 GRPO 种子（在阶段 B 中复用）估计任务级增益的种子方差，预注册斜率 b 的最小可检出效应；若不足以检出 b = 0.3，则把 WebShop 评测任务增至 1500。

**阶段 B：训练（约 12 天训练 + 3 天评测）。**
- WebShop 七组：GRPO、入口前向 KL、DPH-RL（全局前向 KL）、TAR、PTGS、剖面选轮前向 KL、随机选轮前向 KL。
- ALFWorld 四组：GRPO、入口前向 KL、TAR、剖面选轮前向 KL。
- 超参：每个方法在 200 个开发任务上用 1 个种子比较 2 个超参（散度系数或 PTGS 温度跨度），选 pass@1 与 GRPO 最接近者；该运行计为该组第 1 个种子。
- 所有组 3 个种子；同一环境内组大小、步数、学习率、rollout 预算相同；回放与前向 KL 组用同一批离线基座成功样本。
- 评测：留出任务的 pass@1 与 pass@32，另报告 pass@64 的子集结果。Sharpening Tax 报告少量 rollout 的税估计可预测大预算的税，因此主分析用 pass@32。

**移植路线**（均为 verl 结构）：
- TAR：把其仓库 `verl/trainer/ppo/core_algos.py` 的 `compute_tar_weights`、`compute_tar_loss` 与 `verl/workers/actor/dp_actor.py` 的 `_backward_tar_loss` 复制到 verl-agent 的同名文件。记忆库条目改为多轮基座成功轨迹，response_mask 只覆盖动作 token。
- DPH-RL：参照其 `scripts/llama/forward_kl.sh` 与离线 `data.sft_files` 机制，在 verl-agent 的 actor 更新中加入同样按动作 token 掩码的离线 NLL 项。剖面选轮、入口、随机选轮只在此基础上改轮掩码。

**Baseline 来源与复现入口**：

| Baseline / 组件 | 与本任务的关系 | 论文 | 代码与复现入口 |
|---|---|---|---|
| TAR | 离线回放族代表 | https://arxiv.org/abs/2610.24236 | https://github.com/wenzhilics/tar（2026-10-16；`recipe/tar/build_memory_bank.py`、`recipe/tar/run_qwen2_5_0.5b_tar.sh`、`verl/trainer/ppo/core_algos.py` 的 `compute_tar_weights` / `compute_tar_loss`、`verl/workers/actor/dp_actor.py` 的 `_backward_tar_loss`） |
| DPH-RL | 离线回放族代表（全局前向 KL） | https://arxiv.org/abs/2509.07430 | https://github.com/seamoke/DPH-RL（2026-02-10；`scripts/llama/forward_kl.sh`，README 的离线采样与 `forward` 配置） |
| PTGS | 采样侧代表（多轮 Sokoban / FrozenLake 上提出） | https://arxiv.org/abs/2610.01509 | https://github.com/changdaeoh/sharpening-tax（`ptgs/integration.py` 的 `PTGSHooks`；`sharpening_tax/benchmarks/webshop.py` 支持 `WEBSHOP_ENV_SEED`） |
| GRPO | 多轮 agent RL 标准做法 | https://arxiv.org/abs/2505.10978 | https://github.com/langfengQ/verl-agent（2026-06-09；`examples/grpo_trainer/run_webshop.sh`、`run_alfworld.sh`；`verl/workers/actor/dp_actor.py`、`verl/trainer/ppo/core_algos.py`） |
| 逐轮替换与分叉 | 真实环境中的检查点交接 | https://arxiv.org/abs/2609.19636 、https://arxiv.org/abs/2608.08239 | https://github.com/Xuanxuana1/AgenticRL_Handoff（2026-09-26；`src/handoff/alfworld/{environment,rollout}.py`；为 WebShop 增加固定种子的真实环境回放） |

**算力与 API 预算**（8×A100 80G，无付费 API）：
- 阶段 0：2 个环境各 1 次 GRPO（各约 8 卡 × 8–12 小时）加评测，约 1 天。
- 阶段 A：
  - WebShop 800 × 18 种条件 × 32 ≈ 46 万条；ALFWorld 274 × 16 × 32 ≈ 14 万条；
  - 按约 23 万条 / 天，约 2.6 天。
- 阶段 B：
  - WebShop 7 组 × 3 种子 + 6 次超参比较中的第二个设置 = 27 次；ALFWorld 4 × 3 + 3 = 15 次；
  - 共 42 次，每次约 8 卡 × 7 小时，约 12 天；
  - 评测：(21 × 800 + 12 × 274) × 32 ≈ 64 万条，约 3 天。
- 合计约 19 天；API 费用为 0。阶段 0 与阶段 A 共约 3.6 天，即可得到剖面、全部对应物增益与功效分析。

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
