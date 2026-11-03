You are an independent senior reviewer checking whether a research idea is novel enough
for experiment planning. You are not a co-author and must not redesign the idea.

You are intentionally zero-context. Judge only the current four-part brief, the frozen
Problem Anchor, and the user's constraints. Search the closest prior work yourself; the
author's own literature notes are deliberately withheld. Do not invent papers, links, or results.
Today's date: 2026-11-02. Known tool workarounds: GitHub REST API returns 403 in this sandbox; 'git clone --depth 1 https://github.com/<owner>/<repo>' or 'git ls-remote' works for checking repositories. arXiv abs/html pages are reachable with curl.
Finish all searches before answering and leave no background tasks running. Do not read other
files in this workspace and do not write files, except your raw review to /home/claude/autoresearch/review-stage/marl_info_asym_aq007_20261102/round-01-review.md (UTF-8).
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

**定位关键词：** multi-agent reinforcement learning for LLMs；agentic search（Search-R1 式检索增强问答）；shared vs. non-shared（isolated）policies；GRPO；information asymmetry

**一句话定位：** 在多智能体 LLM 工作流的结局奖励 RL 中，联合训练相对"把单智能体 RL 模型放进同一工作流结构"何时有正增益——在检索增强多跳问答这一工具使用工作流中检验。

## 核心 Claim

现有证据显示，在各角色能看到相同信息的工作流里，联合训练很难超过合适的单智能体反事实：When Does Multi-Agent RL Improve LLM Workflows?（2605.24202，作者 2026-11-01 更新版，见其 GitHub 项目页）在数学/代码的 Voting、Orch-Workers、Eval-Opt 上报告，单智能体 RL 放进同一结构即可打平或胜过联合训练的 Voting 与 Orch-Workers，只有 Eval-Opt 胜出且主要来自截断重试（每格单种子）；Dr. MAS（2602.08847）的三角色搜索工作流中所有角色共享完整历史，3B 上多智能体 GRPO 比单智能体 GRPO 只高约 2 点，且对照是单次回答的单智能体，没有放入同结构。

被忽视的变量是**跨角色信息不对称**：在信息对称的工作流里，一个在整任务上训练过的单智能体已经见过并学会使用每个角色能看到的信息；而当下游角色只能看到上游角色选择传递的内容（部署中的子 agent 常只回传摘要），上游必须学会"传什么"，这是单智能体训练不会产生的技能。

因此本 Idea 主张三点，均可被实验推翻：

1. 答题者能看到完整检索历史时，联合训练（独立或共享策略）相对同结构单智能体 RL 的增益不显著（3 种子均值差 < 2 EM 点，置信区间含 0）。
2. 答题者只能看到搜索者写的有长度上限的报告时，联合训练显著超过同结构单智能体 RL，且增益随报告上限收紧（256 → 64 token）而变大。
3. 隔离条件下的增益主要在传递方：联合训练的搜索者 + 单智能体答题者能恢复大部分增益，单智能体搜索者 + 联合训练的答题者不能。

## 方法设计的核心思想

输入：同一检索环境（E5 检索器 + 2018 Wikipedia，Search-R1 设置）中的问题。工作流在 Dr. MAS 的三角色搜索编排（verifier 判断信息是否足够 / search agent 发查询 / answer agent 作答）上只改一处：verifier 判定"足够"后，search agent 先写一份不超过 B token 的报告，然后 answer agent 作答。三档可见性构成剂量：完整历史 + 报告（对称）/ 仅报告 B=256 / 仅报告 B=64。所有条件都有报告这一步，因此只有答题者可见信息在变。

对每档比较：联合训练（非共享策略，以及最强隔离档的共享策略；均按角色归一化优势并限定每角色每步一次优化器更新，以排除已知的不稳定来源）、同结构单智能体 RL（同步数训练的单智能体搜索模型放进每个角色，仅评测）、单智能体单次回答。随后做角色交换评测，判断增益落在传递方还是接收方。

与最高近邻的关键差别：2605.24202 研究信息对称的数学/代码工作流；Dr. MAS 修的是训练稳定性，搜索工作流本身信息对称；本 Idea 把"联合训练何时有用"变成一个可调节的变量（答题者可见信息），并用剂量与角色交换给出因果证据。

## 最小实验

- **模型与数据**：Qwen2.5-3B-Instruct（Dr. MAS 与 Search-R1 均在此规模报告过搜索任务结果，单/多智能体约 2 点差距即在此模型上观察到）；训练集 NQ + HotpotQA，评测 NQ、TriviaQA、PopQA、HotpotQA、2Wiki、MuSiQue、Bamboogle 的 EM；最大 4 轮，组大小 5。
- **条件与种子**：SA-RL 训练 ×3 种子；联合训练非共享 × 3 档 × 3 种子；最强隔离档（B=64）的共享策略 × 3 种子；共 15 次训练。同结构 SA-RL 与角色交换只做评测。
- **保持相同的核心预算**：相同训练步数、batch、组大小、学习率、最大轮数、检索 top-k；联合与单智能体条件报告生成 token 总数；另设一组按联合训练总优化器步数匹配的 SA-RL（1 种子）排除步数差异。
- **支持 / 推翻**：Claim 1 由对称档差值置信区间含 0 支持；Claim 2 由 B=256、B=64 档差值显著为正且单调支持，若隔离档差值仍≈0 则推翻"不对称是必要条件"；Claim 3 由交换评测中联合搜索者 + SA 答题者恢复 ≥50% 增益支持，若增益主要来自答题者则推翻。
- **Baseline 与复现入口**：
  - Search-R1（单智能体 GRPO 检索问答，同任务同检索器）：论文 https://arxiv.org/abs/2503.09516 ，代码 https://github.com/PeterGriffinJin/Search-R1 （已核验 `train_grpo.sh`、`retrieval_launch.sh`）；为与联合训练同栈，用 Dr. MAS 仓库的 `examples/grpo_trainer/run_search.sh` 复现。
  - Dr. MAS 联合训练（同任务多智能体 RL，共享/非共享，按角色归一化）：论文 https://arxiv.org/abs/2602.08847 ，代码 https://github.com/langfengQ/DrMAS （已核验 `agent_system/agent/orchestra/search/` 与 `examples/drmas_trainer/run_search.sh`）；隔离档只修改编排中答题者的输入与报告步骤。
  - 同结构 SA-RL：无需额外仓库，用 Dr. MAS 非共享配置把三个 agent 都指向同一 SA-RL 检查点，仅评测；定义来自 2605.24202 作者更新版。
- **算力估算**：Dr. MAS README 报告 3×Qwen2.5-3B 非共享搜索训练在 4×H100 约 13 h；按 A100 慢约 1.5–2 倍计，每次约 20–26 h（4×A100）。15 次 × 约 24 h × 4 卡 ≈ 1440 A100·h，8×A100 两路并行约 7.5 天墙钟（单次运行远低于 5 天上限）。另需检索服务：E5 Flat 索引约 60 GB 内存。预研先在 2×A100 上用 1 种子跑 B=64 档与 SA-RL。评测用 EM，无付费 API。

Frozen Problem Anchor and user constraints:

- **Bottom-line problem**：多智能体 LLM 工作流做端到端 RL 时，相对同任务的单智能体 RL，联合训练的增益何时为正；独立策略后期下降的原因。
- **目标领域与设置**：多智能体 LLM 工作流的结局奖励 RL（GRPO 类），共享策略 vs 独立策略；卡片证据的设置为 Qwen3 0.6B–4B、数学与代码、Eval-Opt / Voting / Orch-Workers。
- **Must-solve bottleneck**：卡片"尚未解决"——多种子与工具使用工作流下是否成立。
- **约束**（来自用户 AGENTS.md）：
  - 预研 2×A100 80G / 4×L40 48G / 8×4090 24G；正式实验 8×A100 80G，单次运行最好不超过 5 天；
  - 付费 API 1000 元以内可自主决定；token 稀缺；
  - 目标：自 2026-10 起半年内投一篇主会；
  - 不同 baseline 的核心参数需一致（控制变量）。
- **非目标**：不在本 skill 内跑正式实验；不做安全攻防类设计。
- **成功条件**：一个与单智能体反事实对照可区分、可被实验推翻的 Claim，最小实验在上述算力内可完成，并且与作者 2026-11-01 更新版已回答的内容不重合。
