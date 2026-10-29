You are an independent senior reviewer checking whether a research idea is novel enough
for experiment planning. You are not a co-author and must not redesign the idea.

You are intentionally zero-context. Judge only the current four-part brief, the frozen
Problem Anchor, and the user's constraints. Search the closest prior work yourself; the
author's own literature notes are deliberately withheld. Do not invent papers, links, or results.
Today's date: 2026-10-29. Known tool workarounds: GitHub REST API 在本环境受限（403），可用 git ls-remote 或浅克隆核验仓库；arXiv 摘要页与 HTML 全文可正常抓取
Finish all searches before answering and leave no background tasks running. Do not read other
files in this workspace and do not write files, except your raw review to /home/claude/autoresearch/review-stage/rl_boundary_aq001_20261029/round-09-review.md (UTF-8).
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

**一句话定位：** RL 会让多轮工具 agent 在大 k 采样下丢失可解任务覆盖；保住覆盖的现有方法都在单轮上提出，各自隐含“丢失发生在哪里”的假设。本研究在多轮 agent 中按轮定位丢失，并检验这些方法能找回的覆盖是否由“丢失落在它们够得着的位置上的量”决定。

## 核心 Claim

**已知与归属**：
- **入口类**：Locked at the Entrance（arXiv 2608.29188）在单轮上把丢失定位到入口，晚层插值有效；DivInit（arXiv 2606.17209）在 agent 搜索中只修第一轮查询冗余。
- **离线回放类**：DPH-RL（arXiv 2509.07430）、PBA（arXiv 2607.20543）、TAR（arXiv 2610.24236）在单轮上回放或锚定基座成功解。
- **采样侧**：PTGS（Sharpening Tax，arXiv 2610.01509）按题调采样温度，原作在 Sokoban / FrozenLake 上验证。
- **状态失配**：学生偏离教师熟悉状态是 DAgger 式协变量偏移；ReOPD（arXiv 2607.04763）与 Guided-OPD（EMNLP 2026）已在多轮蒸馏中讨论前缀与状态来源的失配，本研究只把它作为测量使用，不作为新机制。
- **定向的反例**：Coverage, Not Targeting（arXiv 2609.02417）发现多轮 agent 的信用分配中，定向到选定轮与随机轮同样有害。

1. **按轮定位：区分入口锁定与观察后重新锁定。**
   - 设 B 为起点策略，G 为从 B 出发、同一设置下只做 GRPO 的检查点。在真实环境中逐轮替换（只把第 t 轮换成 B 生成，其余由 G 生成并继续），减去同模型分叉的噪声底，得到逐任务的可找回覆盖剖面 L_i(t)。
   - 比较只在替换轮数相同的组之间进行：单轮 vs 单轮，两轮集合 vs 两轮集合，以排除剂量混杂。
   - 在 WebShop 与 ALFWorld 上分别报告剖面。我们预期 WebShop 在搜索结果返回后的决策轮仍有显著 L(t)（重新锁定），但无论剖面集中在入口还是分散，Claim 3 都可检验。
2. **在被锁定轮上，丢的是基座分支分布，不只是多样性。** 同样轮上，G 等熵提温或做首动作 top-N 均匀采样（REFT 式，arXiv 2605.28295），找回的覆盖少于基座替换。单轮上“提温无效”已归属 2608.29188，本 Claim 只针对观察后的决策轮。
3. **现有保覆盖方法找回的覆盖，由“L 落在其可作用区域内的量”预测。**
   - **可作用区域 A_m**：
     - 入口类 = 第 1 轮；
     - 离线回放类 = 当前策略与基座状态等价的 (任务, 轮)，用状态重叠 O_i(t) 判定，按环境状态程序判等；
     - 采样侧 PTGS = 所有轮，但只改多样性；按 Claim 2，它在“丢分布”的轮上作用有限。
   - **预测**：方法 m 在任务 i 上相对 GRPO 找回的 pass@64 ≈ Σ_{t∈A_m} L_i(t)。按任务分层检验，各族的实际找回量应随其预测量单调增加。
   - **处方**：剖面选轮的前向 KL（在 L 显著的轮上施加，估计方式同 DPH-RL）应找回最多。与 2609.02417 相对，它在锚定 token 占比相同的条件下优于随机选轮。理由是锚定作用于分布，而信用分配作用于奖励。

**推翻条件**：
- 各族方法的实际找回量与其预测量无关（任务级 Spearman 不显著，分层不单调）；
- 剖面选轮前向 KL 不优于同 token 占比的随机选轮；
- 等熵提温 / REFT 在观察后决策轮上找回同样多。

## 方法设计的核心思想

**测量（训练前）**：
- 在 (B, G) 上做逐轮替换与同模型分叉。G 为 1 个种子的 GRPO 检查点；WebShop 固定 `WEBSHOP_ENV_SEED`，ALFWorld 固定游戏文件与种子。
- 得到每任务的 L_i(t)，以及风险任务上的 O_i(t)，进而计算每个方法族的预测量 P_m(i) = Σ_{t∈A_m} L_i(t)。
- 测量只用推理，不训练任何方法。

**统一检验**：
- 在同一设置、同一起点下训练各方法族的代表：入口前向 KL、DPH-RL、PBA、TAR（移植到多轮轨迹）、PTGS；
- 对 G 应用晚层插值与 DivInit 两个测试时方法；
- 记录每任务相对 GRPO 的 pass@64 变化，与 P_m(i) 对齐。

**处方**：在剖面选出的轮集合 S 上，对离线基座成功片段施加前向 KL，其余轮不加；对照为相同 token 占比、每 batch 随机抽轮的前向 KL。

**与最高近邻的关键差别**：各族方法只在单轮上提出，没有检验其隐含的丢失位置假设在多轮 agent 中是否成立；Reach or Solve（arXiv 2609.19636）做 SFT↔RL 交接、看 pass@1，不涉及覆盖与方法比较；ReOPD / Guided-OPD 讨论蒸馏中的状态失配，不涉及保覆盖。本研究用逐轮剖面把“丢在哪里”与“各方法够得着哪里”对齐，并据此在训练前按任务预测方法效果。

## 最小实验

**阶段 0：前置检查（约 1 天）。**
- WebShop：B = Qwen2.5-7B 基座。Sharpening Tax 的 WebShop 文本 harness 移植进 verl-agent，商品子集、步数上限与 `WEBSHOP_ENV_SEED` 一致，训练与评测同一设置。
- ALFWorld：B = Qwen2.5-7B 基座；若其在 unseen 134 个任务上 pass@64 低于 30%，改用 Qwen2.5-7B-Instruct 作起点。
- 各跑 1 个种子的 GRPO 得到 G。只有 G 的 pass@64 比 B 低至少 5 个百分点的环境进入后续；都不满足则报告“纯 RL 不产生锐化税”并停止。

**阶段 A：测量（约 2.5 天）。**
- WebShop 300 个留出任务（t = 1…6），ALFWorld unseen 134 个任务（t ∈ {1, 2, 4, 8, 12, 16}）。
- 每格做逐轮替换与同模型分叉，64 次 rollout；做剂量匹配组与 Claim 2 的等熵 / REFT 对照。
- 计算 O_i(t) 与 P_m(i)。
- 对 G 做晚层插值与 DivInit 的测试时评测。

**阶段 B：统一检验与处方（约 10 天训练 + 2.5 天评测）。**
- **WebShop 八组**：GRPO、入口前向 KL、DPH-RL、PBA、TAR、PTGS、剖面选轮前向 KL、随机选轮前向 KL。
- **ALFWorld 五组**：GRPO、入口前向 KL、PBA、TAR、剖面选轮前向 KL。
- 系数与种子：每个方法组扫 2 个超参（散度系数或 PTGS 温度跨度，1 个种子）画 pass@1–pass@64 前沿；在 pass@1 与 GRPO 最接近的设置上，把剖面选轮与前沿上最强的另一组补到 3 个种子。GRPO 各环境 3 个种子。
- 控制：同一环境内组大小、步数、学习率、rollout 预算相同，前向 KL 与回放类组用同一批离线基座成功样本。
- **主分析**：按任务把“方法 m 相对 GRPO 的 pass@64 变化”与 P_m(i) 做 Spearman 相关，并按 P_m 三分层检验单调性；另比较剖面选轮与随机选轮。

**支持 / 推翻 Claim 的结果**：见核心 Claim 的预期与推翻条件。

**Baseline 来源与复现入口**：

| Baseline / 组件 | 与本任务的关系 | 论文 | 代码与复现入口 |
|---|---|---|---|
| TAR | 离线回放类代表 | https://arxiv.org/abs/2610.24236 | https://github.com/wenzhilics/tar（2026-10-16；verl `recipe/tar/`，`build_memory_bank.py`；移植到 verl-agent 多轮轨迹） |
| DPH-RL | 离线前向 KL 保 pass@k | https://arxiv.org/abs/2509.07430 | https://github.com/seamoke/DPH-RL（2026-02-10；README 的离线采样与 `forward` 散度配置） |
| PBA | 按题风险门控锚定基座 | https://arxiv.org/abs/2607.20543 | 未见代码；按论文描述本地实现（风险门控 + 向冻结起点的散度） |
| PTGS | 采样侧代表 | https://arxiv.org/abs/2610.01509 | https://github.com/changdaeoh/sharpening-tax（`ptgs/integration.py` 的 `PTGSHooks`；`sharpening_tax/benchmarks/webshop.py` 支持 `WEBSHOP_ENV_SEED`） |
| 晚层插值 | 入口类代表（测试时） | https://arxiv.org/abs/2608.29188 | https://github.com/ershiyidian/early-branch-locking（2026-09-01；`src/early_branch_locking/countdown/layer_interpolation.py`） |
| DivInit | 入口类代表（测试时） | https://arxiv.org/abs/2606.17209 | https://github.com/cxcscmu/diverse-query-initialization（main 可访问） |
| GRPO | 多轮 agent RL 标准做法 | https://arxiv.org/abs/2505.10978 | https://github.com/langfengQ/verl-agent（2026-06-09；`examples/grpo_trainer/run_webshop.sh`、`run_alfworld.sh`） |
| 逐轮替换与分叉 | 真实环境中的检查点交接 | https://arxiv.org/abs/2609.19636 、https://arxiv.org/abs/2608.08239 | https://github.com/Xuanxuana1/AgenticRL_Handoff（2026-09-26；`src/handoff/alfworld/{environment,rollout}.py`；为 WebShop 增加固定种子的真实环境回放） |
| REFT / 等熵提温 | 只增加多样性的对照 | https://arxiv.org/abs/2605.28295 | 在选定轮首动作上做 top-N 均匀采样 / 温度调整 |

**算力与 API 预算**（8×A100 80G，无付费 API）：
- 阶段 0：2 个环境各 1 次 GRPO（各约 8 卡 × 8–12 小时）加评测，约 1 天。
- 阶段 A：WebShop 约 30 万条、ALFWorld 约 12 万条轨迹，vLLM 约 2.5 天。
- 阶段 B：
  - WebShop：7 组 × 2 超参 + 4 次补种子 + 2 次 GRPO = 20 次；
  - ALFWorld：4 组 × 2 超参 + 4 次补种子 + 2 次 GRPO = 14 次；
  - 每次约 8 卡 × 6–8 小时，约 10 天；评测约 2.5 天。
- 合计约 16 天；API 费用为 0。阶段 0 与阶段 A 共约 3.5 天，即可得到剖面与各方法族的预测量。

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
