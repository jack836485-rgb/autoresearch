You are an independent senior reviewer checking whether a research idea is novel enough
for experiment planning. You are not a co-author and must not redesign the idea.

You are intentionally zero-context. Judge only the current four-part brief, the frozen
Problem Anchor, and the user's constraints. Search the closest prior work yourself; the
author's own literature notes are deliberately withheld. Do not invent papers, links, or results.
Today's date: 2026-11-01. Known tool workarounds: GitHub REST API returns 403 from this sandbox; verify repositories with 'git clone --depth 1' into your own scratch directory instead. arXiv pages are reachable via WebFetch; .claude/skills/idea-improvement-loop/tools/paper_peek.py also works from the project root.
Finish all searches before answering and leave no background tasks running. Do not read other
files in this workspace and do not write files, except your raw review to /home/claude/jack836485-rgb/autoresearch/review-stage/judgment_action_nq003_20261101/round-01-review.md (UTF-8).
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

**定位关键词：** refusal direction；tool-calling agents；over-calling；activation steering；AgentHarm

**一句话定位：** 工具调用 agent 中，聊天里会被拒绝的有害请求，到了工具上下文却变成不安全的工具调用。已有工作分别把原因归于拒绝信号下降、判断对行动的控制弱；另一条工作线发现，"调用 / 不调用"决策本身带有一个与激活无关的固有调用偏置。这三者从未被放在一起检验。

## 核心 Claim

1. **现有失败**
   - **拒绝信号只能部分解释脱节**（arXiv 2610.28982）：
     - 聊天中被拒绝的有害请求，在标准工具设置下有 10–52% 变成不安全调用；
     - 工具上下文里拒绝方向的激活下降；
     - 把拒绝信号修补回纯文本水平，只拦下一部分不安全调用，而且主要靠压低工具使用；
     - 沿拒绝方向转向，只有在会压制良性工具使用的强度下，才几乎消除不安全调用。
   - **判断与行动耦合弱**（arXiv 2609.35870）：把判断推向"阻止"的干预，对行动偏好影响小得多，但安全信息仍能从行动状态读出。
   - **工具说明格式削弱拒绝**（SafeKeep，arXiv 2607.29254）：schema 格式的工具说明会削弱内部拒绝信号。
   - **另一条工作线：固有调用偏置**（IBH，arXiv 2605.18882）：调用决策带有与激活无关的固有调用偏置，抵消它能减少过度调用，对正常调用几乎无损。

2. **被忽视的关键**：如果调用决策里有一个与判断无关的偏置，拒绝信号即使完好，也要先抵过它才能改变行动，行为上就表现为"耦合弱"；而沿拒绝方向整体平移，会把良性请求一并推过阈值。本 Idea 主张：
   - **C1（分解）**：在首个行动决策位置，"调用 / 不调用"边际可分解为依赖判断的拒绝方向投影，与不依赖判断的调用偏置。改变工具数量与工具说明格式时，调用偏置随之变化，并在控制拒绝投影后仍能预测不安全调用率。
   - **C2（选择性修法）**：只用良性的"无需调用"数据校准并抵消调用偏置，不使用任何有害数据。它与"把拒绝信号修补到纯文本水平"存在交互：组合后，不安全调用的减少明显大于两者单独效果之和；在相同的不安全调用减少量下，良性任务得分损失小于拒绝方向转向和 CAST。
   - **C3（与格式的关系）**：把 schema 格式改为扁平文本说明（SafeKeep 的做法），其安全收益主要通过降低调用偏置实现，而不只是恢复拒绝投影。

## 方法设计的核心思想

- **输入**：工具上下文中的提示；模型在首个行动决策位置的残差流激活。
- **步骤**：
  1. 用 When2Call 中"需要调用"与"无需调用"的良性样本，估计调用 / 不调用方向。沿用 IBH 的做法估计固有偏置：在支持的模型上用其 SAE，在其他模型上用线性方向加逻辑回归截距。
  2. 用 refusal_direction 流水线提取拒绝方向。
  3. 干预有三种：沿调用 / 不调用方向做常数平移，抵消偏置；把拒绝投影修补到同一请求纯文本条件下的值；二者组合。
- **输出**：每个模型、每种上下文下的偏置估计；四种干预（无、只抵消、只修补、组合）下的不安全调用率与良性任务得分。
- **与最高近邻的差别**：
  - 2610.28982 只操纵拒绝方向；
  - 2609.35870 区分判断侧与行动侧干预，但不涉及与判断无关的偏置；
  - IBH 只研究良性的过度调用，不涉及安全；
  - SafeKeep 与 CAST 是外部判断门控或条件转向。
  - 本 Idea 把脱节归因于拒绝信号与固有调用偏置的竞争，并用不接触有害数据的偏置抵消来检验。

## 最小实验

- **模型**
  - Qwen3.5-9B、Ministral-3-8B-Instruct-2512：IBH 提供了这两个模型的 SAE；
  - Llama-3.1-8B-Instruct：SafeKeep 原文使用；
  - Qwen3-32B：检验规模，用线性方向，不用 SAE。
- **数据**
  - AgentHarm 公开测试集，有害与良性版本各 176 条。
  - 纯文本条件：去掉同一有害提示中的工具说明构造，保证逐条对齐。
  - 上下文因子：工具数量 {1, 5, 20} × 说明格式 {schema, 扁平文本}，共 6 种。
  - 偏置只用 When2Call 的良性样本校准。
- **对照**：各方法都在同一组提示、同一解码设置（温度 0）、同一干预层上进行；有强度参数的方法都扫 5 档强度，画出帕累托前沿。
  1. 无干预；
  2. 拒绝方向转向（多档强度）；
  3. 拒绝信号修补到纯文本水平；
  4. CAST：以有害条件向量门控拒绝转向；
  5. SafeKeep；
  6. 安全系统提示；
  7. 偏置抵消（本 Idea）；
  8. 偏置抵消 + 拒绝修补（本 Idea）。
- **指标**
  - AgentHarm 有害任务得分与拒绝率（原评分器）；
  - "聊天中拒绝、工具中执行"的比例；
  - AgentHarm 良性任务得分；
  - When2Call 调用准确率。
- **支持与推翻**
  - C1：在每个模型内，6 种上下文的偏置估计与不安全调用率的偏相关（控制拒绝投影）在至少 3/4 模型上显著为正，则支持；否则推翻。
  - C2：
    - 2×2（修补 × 抵消）交互项显著为正，则支持；
    - 在不安全调用率减半时，组合方法的良性得分损失显著小于拒绝转向与 CAST，则支持；
    - 若抵消偏置与拒绝转向在良性损失上无差别，则推翻。
  - C3：扁平格式带来的不安全调用下降中，由偏置变化中介的比例超过一半，则支持。
- **Baseline 来源与复现**
  - **AgentHarm**
    - 论文：https://arxiv.org/abs/2410.09024
    - 代码：https://github.com/UKGovernmentBEIS/inspect_evals ，路径 `src/inspect_evals/agentharm/`，已克隆核验。
    - 任务：`agentharm`（含 `chat_dataset` 选项）、`agentharm_benign`；数据来自 HF `ai-safety-institute/AgentHarm`。
  - **拒绝方向**
    - 论文：https://arxiv.org/abs/2406.11717
    - 代码：https://github.com/andyrdt/refusal_direction ，已克隆核验。
    - 用法：`python3 -m pipeline.run_pipeline --model_path ...`，输出 `direction.pt`。
  - **IBH / AMCS**
    - 论文：https://arxiv.org/abs/2605.18882
    - 代码：https://github.com/SKURA502/agent-sae ，已克隆核验。
    - 提供 Qwen3.5-9B、Ministral-3-8B 等 8 个模型的 SAE 检查点与因果转向脚本。
  - **CAST**
    - 论文：https://arxiv.org/abs/2409.05907
    - 代码：https://github.com/IBM/activation-steering ，已克隆核验，含条件向量用法。
  - **SafeKeep**
    - 论文：https://arxiv.org/abs/2607.29254
    - 代码：https://github.com/snowcatsmoking/SafeKeep ，已克隆核验。
    - 用法：`python Method/safekeep_demo.py --model $MODEL_PATH`。
  - **When2Call**
    - 论文：https://arxiv.org/abs/2504.18851
    - 数据：HF `nvidia/When2Call`。
  - 以上都属于工具调用 agent 的安全或调用决策，与本任务同领域。
- **算力与 API**
  - **推理**：
    - 带激活钩子，用 HF transformers 推理。
    - 轨迹数：4 个模型 × 约 16 种配置（8 种方法，部分扫强度）× 352 条任务 × 6 种上下文中的 2 种主条件，约 4.5 万条轨迹。
    - 8–9B 模型约 10 秒一条，32B 约 30 秒一条，共约 250 A100 小时。
    - 单次运行不超过 1 天，8×A100 上约 2 天完成。
  - **评分**：
    - AgentHarm 评分器需要 LLM 判分，约 9 万次调用 × 约 1.5k token，约 1.4 亿 token。
    - 用 gpt-4o-mini 级模型，按每百万 0.15 美元计约 20 美元（约 150 元）。
    - 另抽 300 条用 gpt-4o 核对判分一致性，约 10 美元。

Frozen Problem Anchor and user constraints:

- **底线问题**：工具调用 agent 在文本中会拒绝或判定应阻止，在工具调用时仍执行同一危险动作；需要弄清脱节的机制，并找到能关闭缺口又不损害正常工具使用的干预。
- **目标设置**：开源指令模型（≤32B）作为工具调用 agent；有害 / 良性 / 纯聊天对照提示；推理与激活读写。
- **必须解决的瓶颈**："拒绝信号在工具上下文中下降"与"判断对行动因果控制弱"两种解释未在同一组模型上对照；行动侧干预能否在不损害正常工具使用的前提下关闭缺口未知。
- **约束**（用户 AGENTS.md，2026-11-01）：实验 8×A100 80G，每次运行最好不超过 5 天；预研 2×A100 / 4×L40 / 8×4090；token 稀缺；付费 API 1000 元以内可自主决定；目标半年内（自 2026-10 起）投一篇主会。各 baseline 核心参数一致。
- **非目标**：不做安全攻防式的过度防御；不在本 skill 内启动实验。
- **成功条件**：机制清楚、与最高近邻可区分、能在上述算力下用可复现 baseline 证伪的 idea，通过两次独立 reviewer 评审（> 8、无致命阻塞）。
