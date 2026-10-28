---
name: idea-improvement-loop
description: "Iteratively develop a genuinely new research idea from either a user-provided raw idea or an existing paper supplied as the baseline/starting point. The main executor reads and searches directly, maintains and ranks a candidate pool, and uses fresh zero-context novelty reviews; paper-input mode first summarizes the paper's core innovation, method, and experiments, then generates ideas whose novelty belongs to the new proposal rather than patching that paper. Use when the user says \"改进idea\", \"打磨idea直到可以做实验\", \"improve this idea\", \"基于这篇论文创新\", supplies a paper/PDF/arXiv link as a baseline, or asks to preserve competing idea variants before experiment planning."
---

# Idea Improvement Loop

## Overview

Use this skill after a raw idea exists, or when the user supplies an existing paper as the starting point for innovation, but before committing GPU time. The main executor itself is the Idea Improver:

```text
raw idea or supplied paper
  -> if paper: read it and summarize its contribution, method, and experiments in RAW_IDEA.md
  -> main executor searches and records every distinct candidate in IDEA_CANDIDATES.md
  -> main executor self-scores candidates and selects the highest eligible one
  -> selected candidate becomes a short positioning-and-idea round-N-brief.md
  -> one fresh zero-context reviewer checks novelty and closest prior work
  -> if rejected, main executor improves it, appends new candidates, and re-ranks the pool
  -> if the pool leader receives reviewer score > 7.5 with no fatal blocker, expand FINAL_IDEA.md
```

Intermediate communication stays small. The candidate pool keeps every concrete idea version, while each reviewer receives only the selected brief with its positioning, Claim, method, and minimal experiment. A full paper-like proposal is produced once, after the gate passes.

## Constants

- **MAX_ROUNDS = 5** — Maximum number of reviewer invocations. It is not a limit on local searches, candidate generation, self-scoring, file updates, or final expansion.
- **FINAL_REVIEW_THRESHOLD = 7.5 (exclusive)** — A reviewer score must be strictly greater than 7.5; exactly 7.5 does not pass.
- **STOP_CONDITION** — Generate the final idea only when the reviewed candidate was the highest self-scored eligible candidate at selection time, reviewer score is `> 7.5`, and `fatal_blockers` is empty.
- **VERDICT_VOCABULARY** = `experiment_ready` / `promising_needs_revision` / `needs_rethink` / `reject`.
- **OUTPUT_IDEA_ROOT = `idea-stage/`** — Store idea artifacts under `idea-stage/<slug>/`.
- **OUTPUT_REVIEW_ROOT = `review-stage/`** — Store reviews and state under `review-stage/<slug>/`.
- **OUTPUT_CANDIDATE_DOC = `idea-stage/<slug>/IDEA_CANDIDATES.md`** — Persistent source of truth for all distinct candidates considered by the improver.
- **CANDIDATE_TEMPLATE = `templates/idea-candidates-template.md`** — Required structure for the candidate pool.
- **INTERMEDIATE_BRIEF_FORMAT** — Every selected brief has exactly `背景`, `核心 Claim`, `方法设计的核心思想`, and `最小实验`.
- **REVIEW_FORMAT** — Every reviewer response has exactly `结论`, `Claim 判断`, and `最高近邻`, followed by a small JSON block.
- **IMPROVED_IDEA_TEMPLATE = `templates/improved-idea-template.md`** — Full structure used only for `FINAL_IDEA.md` after the gate passes.
- **IMPROVER_AGENT_POLICY = forbidden** — The main executor must not delegate candidate generation, literature search, self-scoring, selection, revision, or final expansion to a subagent. It uses available search tools directly.
- **REVIEWER_CONTEXT_POLICY = fresh_zero_context_each_call** — Every reviewer invocation uses a new reviewer agent. Reviewer agents are never continued or reused.
- **HUMAN_CHECKPOINT = false** — If true, pause after each reviewer result; showing a checkpoint does not consume another reviewer call.
- **DO_NOT_REUSE_EXISTING_IDEAS = true** — Do not import unrelated ideas from other `idea-stage` directories unless the user explicitly asks.

User overrides to the reviewer-call budget or gate threshold take precedence. Write documents in Chinese when the user writes in Chinese.

In the stop condition, “highest-scored idea” means the improver's self-score ranking in `IDEA_CANDIDATES.md`; “score > 7.5” means the independent reviewer's score. A self-score above 7.5 never bypasses reviewer validation.

## Mathematical Formula Formatting

Only the final expanded document should normally need formulas. Use `$...$` inline and `$$...$$` for display equations. Define every symbol at first use and immediately explain its operational meaning in plain language.

## Output Layout

Create a stable slug from the idea title or a short normalized phrase. Use lowercase letters, digits, and underscores.

```text
idea-stage/<slug>/
├── RAW_IDEA.md
├── IDEA_CANDIDATES.md         # all distinct candidates, self-scores, lineage, and review status
├── round-01-brief.md          # candidate selected for reviewer call 1
├── round-02-brief.md          # candidate selected for reviewer call 2
├── ...
├── CURRENT_IDEA.md            # selected brief during the loop; full proposal after finalization
├── FINAL_IDEA.md              # only after the gate passes
└── EXPERIMENT_HANDOFF.md

review-stage/<slug>/
├── round-01-review.md         # response from reviewer call 1
├── round-02-review.md
├── ...
├── AUTO_REVIEW.md
├── REVIEW_STATE.json
└── FINAL_REVIEW.md
```

`N` in every `round-N-*` filename is the reviewer invocation number. Local improvement work does not advance it. Use the reviewer-call number as the only version identifier and do not create timestamped per-round copies. Update fixed aliases in place. This overrides the archive-copy rule in `../shared-references/output-versioning.md` for this skill while retaining its path and stale-state rules. Follow `../shared-references/output-manifest.md` and `../shared-references/output-language.md` when applicable.

## Candidate Pool Contract

Read `templates/idea-candidates-template.md` before initializing or updating `IDEA_CANDIDATES.md`.

Each distinct candidate gets an immutable stable ID (`IDEA-001`, `IDEA-002`, ...). Record:

- a short title;
- origin route: `原始想法` / `相似领域成熟方法迁移` / `最高近邻不足` / `未覆盖新任务`;
- parent candidate ID, or `无`;
- status: `available` / `selected` / `needs_revision` / `covered` / `baseline_patch` / `rejected` / `final`;
- at least three positioning keywords already used by the relevant literature, benchmark, or official task description;
- one plain-language background sentence naming the established field and the exact problem being studied, without coining a new term;
- one plain-language paragraph that states the claim, core method, and minimal experiment;
- one plain-language story line that connects the observed failure, the overlooked key idea, this candidate's concrete action, and the falsifiable expected result;
- improver self-score from 1 to 10 and one sentence explaining the judgment;
- the most relevant sources used to generate the candidate, plus any sources used by the later lightweight self-score check;
- baseline feasibility evidence: for every baseline proposed for the minimal experiment, record why it matches the same domain and task, its paper or specification, its public code repository and verification status, and the concrete reproduction route;
- for paper input, the supplied paper's role in the candidate and one sentence stating the candidate's own innovation independently of that paper;
- reviewer-call history once reviewed.

The self-score is one overall research judgment, not a pseudo-precise scoring worksheet. Candidate generation and self-scoring are separate steps: while proposing a candidate, search only for abstractions, transferable mechanisms, modules, failure cases, and task definitions that help form the idea; do not run a novelty audit of the newly formed candidate. After the candidate is concrete, perform only a lightweight, targeted novelty check for self-scoring and ranking. Base the score on that limited evidence, fidelity to the Problem Anchor, story-line coherence, feasibility, and whether the minimal experiment can falsify the claim. Use at most one decimal place. This lightweight check is provisional and never replaces the reviewer's formal novelty judgment.

Append every distinct, concrete candidate actually considered for selection. Do not hide a lower-scored candidate merely because another one looks better. Do not create separate entries for wording changes or synonyms; a new entry must materially change the claim, mechanism, or minimal experiment. Never overwrite a reviewed or rejected candidate with its revision: append the revision as a new candidate and point `父 Idea` to the earlier ID.

Positioning keywords must be terms that can be found in the cited literature, benchmark, or official task description. Do not disguise a new method name as a field keyword. Keep the candidate anchored to one established field and one concrete problem.

A candidate is eligible for `available` status only after its positioning and minimal baselines have been checked. An experimental baseline must target the same task and evaluation setting and must have a direct relationship to the positioning keywords. A method from another field may motivate a candidate, but list it as method inspiration rather than an experimental baseline. Use a nontrivial prior method as a baseline only when the improver has opened and verified a public implementation that corresponds to the cited method and recorded how it will be run in the target setting. A simple standard baseline without a repository is allowed only when its implementation is fully specified and can be implemented locally without unavailable data, checkpoints, or hidden infrastructure; state that reproduction route explicitly. Otherwise, keep the work as related literature and exclude it from the minimal experiment.

For paper input, treat the supplied paper as the user-designated strongest closest work and the ground-truth starting point for idea finding, not as a separate ideation mode and not automatically as an experimental baseline. Include it in the minimal experiment and final `3.3 Baselines` only if it matches the new idea's task and evaluation setting and passes the same reproducibility check. Otherwise cite it only as task origin, method inspiration, or an example of a broader limitation. This ground-truth role fixes the starting neighbor. During candidate generation, broader search serves only to find transferable mechanisms, understand the method family, and locate real task evidence; defer novelty checking until the lightweight self-score pass and the independent reviewer.

The new candidate must state its own contribution independently of the supplied paper. Apply the paper-removal test: after removing the supplied paper's title and proposed method name, the candidate must still state a standalone research problem, its own Claim or mechanism, and a falsifiable experiment. This is a structural independence check, not a novelty audit. A candidate whose contribution is merely “add a missing component,” “complete an omitted experiment,” “extend the paper to one more setting,” or otherwise repair the supplied paper is a baseline patch. Record a materially considered patch with status `baseline_patch`, but never select or review it. A limitation in the supplied paper may motivate the idea only when the improver turns it into a broader problem and proposes an independently stated contribution; in the final story, the supplied paper appears as one related-work example rather than the object being completed.

Only candidates with status `available` are eligible for selection; `baseline_patch` is never eligible. Select the eligible candidate with the highest self-score. If scores tie, make a direct judgment using the available evidence and record the one-sentence tie-break reason in `当前选择`; do not invent extra decimal precision. Mark the winner `selected`, record that it was the pool leader, and leave all other eligible candidates in the list.

Do not pass `IDEA_CANDIDATES.md`, self-scores, rankings, or other candidates to the reviewer. This prevents the improver's preference from anchoring the independent review.

`IDEA_CANDIDATES.md` is the only human-readable idea-history document. Write selection reasons, reviewer outcomes, and child-candidate IDs back into it instead of maintaining a second evolution summary.

## State Persistence

After each candidate-pool change and reviewer call, overwrite `review-stage/<slug>/REVIEW_STATE.json`:

```json
{
  "slug": "example_idea",
  "input_mode": "baseline_paper",
  "source_paper": {"title": "Example Paper", "url": "https://example.org/paper"},
  "status": "in_progress",
  "reviewer_calls_used": 2,
  "max_reviewer_calls": 5,
  "selected_candidate_id": "IDEA-004",
  "selected_self_score": 8.3,
  "selected_was_pool_leader": true,
  "last_reviewer_score": 7.2,
  "last_verdict": "promising_needs_revision",
  "novelty_conclusion": "closest work covers the mechanism but not the derived failure condition",
  "fatal_blockers": [],
  "closest_neighbors": ["paper title or needs_search"],
  "candidate_pool_path": "idea-stage/example_idea/IDEA_CANDIDATES.md",
  "current_idea_path": "idea-stage/example_idea/CURRENT_IDEA.md",
  "last_review_path": "review-stage/example_idea/round-02-review.md",
  "last_brief_path": "idea-stage/example_idea/round-02-brief.md",
  "reviewer_agent_ids": {"call_1": "audit-only; never reuse", "call_2": "audit-only; never reuse"},
  "timestamp": "2026-09-07T12:00:00+08:00"
}
```

On startup, resume an `in_progress` state less than 24 hours old; otherwise start a new run unless the user explicitly asks to resume. For an existing in-progress state created under the old schema, treat its `round` value as the number of reviewer calls already used. Never reset that counter merely because the schema changed.

## Workflow

### Phase 0: Initialize

1. Classify the input as `raw_idea` or `baseline_paper`. Use `baseline_paper` when the user supplies a paper, PDF, paper URL, or precise citation and asks to innovate from it.
2. For `baseline_paper`, read the actual paper before searching for new ideas. Prefer the full primary text; inspect the appendix and official repository when they are needed to understand the method or experiments. Do not infer the paper from its title, abstract alone, or a secondary summary when the full text is available.
3. Write `RAW_IDEA.md` before candidate generation:
   - for `raw_idea`, preserve the user's idea and explicit constraints;
   - for `baseline_paper`, use the compact template below. Summarize whether the paper primarily introduces a new task, a new method, or both, but do not use that classification to choose a separate ideation route. Separate the authors' claims and reported results from the improver's interpretation. Include a verifiable paper link and the official code link when one exists.

```markdown
# 输入论文分析

## 论文信息
<标题、作者、年份、论文链接、官方代码链接或“未找到官方代码”。>

## 核心创新点
<用说人话的方式说明论文提出的是新任务、新方法还是两者都有，以及作者声称的新意。>

## 主要方法
<说明输入是什么、方法实际做了什么、输出是什么；只保留理解后续创新所需的结构。>

## 实验设计与主要结论
<说明数据或 benchmark、主要 baseline、指标、关键对照和论文实际报告的结论；将作者报告与 improver 判断分开。>
```

4. Do not register the supplied paper itself as an idea candidate. It is the user-designated highest-neighbor prior work, not a new idea.
5. Read nearby context only when clearly applicable: `RESEARCH_BRIEF.md`, the matching idea/review directory, `refine-logs/FINAL_PROPOSAL.md`, and relevant local notes.
6. Freeze the Problem Anchor:
   - bottom-line problem;
   - target domain, benchmark, and setting;
   - must-solve bottleneck;
   - compute, data, time, venue, codebase, and non-goal constraints;
   - success condition that would justify experiment planning.
7. Initialize `IDEA_CANDIDATES.md` from `templates/idea-candidates-template.md` and record the input mode plus supplied paper when applicable.
8. Initialize `AUTO_REVIEW.md` and `REVIEW_STATE.json` with `reviewer_calls_used: 0`.

If the raw idea is too vague to identify a Problem Anchor, ask at most one concise clarification. If a supplied paper cannot be identified or its text cannot be accessed, request the PDF or exact citation instead of inventing its contents. Otherwise proceed with explicit assumptions.

### Phase 1: Improver Search and Candidate Generation

The main executor performs this phase directly. It must not call `spawn_agent`, `send_input`, or another agent-like mechanism for ideation, search, scoring, selection, revision, or writing. It may use direct literature/web search tools and must inspect primary paper pages or official sources before treating a work as evidence. For every nontrivial method considered as a baseline, it must also open the claimed public repository, verify that the repository implements the cited method rather than merely mentioning it, and identify the entry point, configuration, or documented command needed for reproduction.

Use the same three idea-finding routes for both `raw_idea` and `baseline_paper`. For `baseline_paper`, first complete `RAW_IDEA.md`, then treat the supplied paper as the user-designated strongest closest work and ground-truth starting point. Do not branch into a separate set of paper-specific routes. Search in this stage exists to produce ideas, not to prove that a generated idea is novel: locate useful abstractions, mechanisms, modules, examples, and task definitions, then leave formal novelty checking to the reviewer. A lightweight novelty search is allowed only after a candidate is fully stated, as part of self-scoring and ranking.

1. **相似领域成熟方法迁移。** 即使用其他领域的方法解决本领域的问题，按下面的顺序执行：
   - 先把当前问题从领域名词中抽象出来，写清输入、输出、核心变换、约束和失败条件。不要先搜索一个听起来相似的方法名。
   - 问“还有哪个领域也需要完成相同的输入到输出变换，或者受到相同结构约束”，据此确定候选相似领域。相似性必须落在机制结构上，而不是主题或术语相似。
   - 在候选领域中搜索成熟方法，理解它依赖的关键假设和实际动作，再逐项映射到当前问题：哪些结构相同、哪些必须修改、修改后输入和输出如何保持可用。
   - 只保留能够做原则性适配的迁移。如果关键成立条件无法映射，就放弃该候选。

   **示例：Diffusion → Diffusion Language Model。** 先把生成抽象为“输入一个被扰动的中间状态，反复预测更干净的状态，最终输出样本”。图像扩散在连续空间中已有成熟的逐步去噪机制；语言生成具有相同的逐步恢复结构，但输出是离散 token 或其表示。因此可迁移的是逐步去噪思想，需要重新设计的是语言状态、扰动过程和反向转移，而不是简单把图像 diffusion 的模块名称搬到语言模型里。

   **Story line：** 当前领域的现有方法在一个明确条件下效果不好或出现稳定失败；相似领域已经验证过一种关键思想；两个领域共享使该思想成立的核心结构；本 Idea 对该思想做什么最小适配并形成什么方法；在相同预算下，这个修改应改善哪个指定指标或失败模式。

2. **最高近邻方法的不足。** 对 `raw_idea`，先检索并选定一个用于生成 Idea 的最高近邻；对 `baseline_paper`，直接把用户提供的 baseline 当作已知最高近邻。然后按下面的顺序执行：
   - 通读最高近邻，关注它的完整工作链。不同的论文可能有不同的结构，但主要是以下几点：输入、主要模块、各模块作用、监督信号或目标函数、输出和评测。
   - 列出可以修改的模块，但不要从“哪里容易改代码”出发。对每个模块沿着 `模块作用 → 依赖的假设 → 假设失效的条件 → 可观察后果` 反推它对应的领域级缺陷。
   - 只有当上述反推能够得到一个独立、可验证的领域问题时，才生成候选；如果最后只能表述成“替换这个模块可能更好”，则降低该 Idea的优先级。
   - 先设计一个最小诊断实验，用于验证缺陷是否真实存在；再针对该缺陷设计机制。最小实验必须同时包含“缺陷诊断”和“机制是否解决缺陷”两部分。

   **示例：RLHF/PPO → DPO。** 不把故事写成“把 PPO 换成一个监督损失”，而是先拆解显式 reward model、采样和策略优化在偏好对齐中的作用，再反推出领域级问题：多阶段 RLHF 管线为把偏好转成策略更新引入了额外训练环节和优化复杂性。由此才得到直接从偏好对构造策略目标的机制，并比较它是否在保留偏好优化目标的同时简化训练。

   **示例：CoLaR → ReGuLaR 式改进。** 先把 CoLaR 的压缩 embedding 预测看作 latent reasoning 的监督模块，再从该模块的作用反推问题：压缩后的隐状态可能缺少足够的信息保持指导。候选不能只写“换一个监督头”，而要先诊断相同压缩率下的信息或推理能力损失，再提出更有信息量的 latent guidance，例如 ReGuLaR 式的变分隐状态与 rendered CoT 表征约束，并验证这种指导是否缓解了该领域级缺陷。

   **Story line：** 最高近邻及同类方法依赖一个共同有缺陷的假设或模块，或者表现出一种一致问题；本 Idea 先通过诊断实验验证该缺陷是否存在；基于此提出自己的机制；最小实验同时检验缺陷和机制是否有效。即使代码上只改一个模块，也不要把故事写成“给最高近邻补模块”。未运行实验前必须把“证实”写成待验证目标，不能写成既成结果。

3. **未覆盖新任务（低优先级）。** 这是硬性后备路线：只有路线 1 和路线 2 都无法形成任何高于7分候选时才进入；只要前两条已经产生至少一个高于7分的候选，就不要在这里继续消耗时间。按下面的顺序执行：
   - 从一个确实存在的大问题开始，沿任务阶段、对象、环境、约束或失败类型逐层细分；每细分一层，都检查该子问题是否仍有独立输入、输出和评价对象。
   - 持续细分到一个现有任务定义或 benchmark 测不到、但会反复出现的具体问题。不能只靠换名字建立新任务。
   - 用真实案例、数据现象或评测盲区证明问题存在；然后定义任务输入、期望输出、数据构造方式和最小指标。缺少客观问题证据时，放弃该候选。

   **示例：RAG → RAG memory → memory structure → memory graph → RAG memory graph manager。** 从 RAG 的长期信息管理逐层定义问题缩小到图结构记忆的维护问题，最后定义 manager 任务：输入当前 memory graph 与新交互信息，输出节点或边的新增、合并、更新和删除决策，并用后续检索质量、结构正确性和维护成本判断任务是否成立。新意不来自创造“manager”这个名字，而来自现有 RAG 任务没有单独测量这类持续图维护能力。

   **Story line：** 先用真实案例、数据或现有评测盲区证明问题客观存在；再说明现有任务定义为什么测不到它；随后给出新任务的输入、输出和评价方式；最后说明什么最小结果能够证明它有研究价值。不要为了安放一个方法而发明任务。如果手里已有一个方法，例如用户提供的 baseline，而相近领域存在明确且解决普遍不好的问题，可以尝试将该方法迁入并据此定义任务，但仍必须先证明任务客观存在。

For `raw_idea`, first register the user's raw idea itself as a candidate with source `原始想法`; its self-score may be low, but it remains the comparison candidate. For `baseline_paper`, do not register the supplied paper itself as a candidate because it is the highest-neighbor prior work, not a new idea. Then record every distinct candidate produced by routes 1 and 2 in `IDEA_CANDIDATES.md`, each with positioning keywords, a one-sentence background, one idea paragraph, a self-score, and baseline feasibility evidence. Enter route 3 only if routes 1 and 2 produced zero concrete candidates. There is no required candidate count and no requirement to populate every route.

For both input modes, write the story line as one causal paragraph: `明确失败及证据 → 被忽视的关键 → 本 Idea 的具体动作 → 可支持或推翻的预期结果`. Verify every link with literature, theory, or the proposed minimal experiment. Do not write “大家效果都不好” or “相关工作都忽视了” without concrete evidence. Before experiments run, describe improved performance as a hypothesis or success condition, never as an achieved result.

For paper input, follow the same route priority above. For each candidate, record `与输入论文的关系` and `本 Idea 的独立创新点`, apply the paper-removal test, and mark patch-only candidates `baseline_patch`. The first selectable candidate is therefore a new idea, not the supplied paper rewritten as `IDEA-001`.

After a reviewer rejects or returns a candidate for revision and reviewer budget remains:

1. Mark the reviewed candidate `needs_revision`, `covered`, or `rejected` according to the review.
2. Read the review's cited closest work directly; do not rely only on the reviewer's summary.
3. Improve the selected candidate using the same three routes above. In `baseline_paper` mode, keep the supplied paper fixed as the user-designated highest neighbor and apply the paper-removal test again to every revision.
4. Append each material revision as a new candidate with a new ID and `父 Idea` pointing to the reviewed candidate. Preserve the old entry.
5. Reconsider all still-`available` candidates, including older unreviewed alternatives, and select the highest self-scored one.

### Phase 2: Select and Write the Brief

Let `N = reviewer_calls_used + 1`. If `reviewer_calls_used >= MAX_ROUNDS`, do not write another round brief or invoke another reviewer; proceed to the blocked finalization.

Select the highest self-scored eligible candidate and write `round-N-brief.md` with exactly:

```markdown
## 背景

**定位关键词：** <列出至少三个能在所引论文、benchmark 或官方任务说明中直接找到的已有关键词；不要自创术语。>

**一句话定位：** <只用一句话说明这是哪个已有领域里的什么具体问题。>

## 核心 Claim
<按“现有方法在哪个明确条件下失败、被忽视的关键是什么、本 Idea 因此主张什么”的顺序，用说人话的方式说明几个可被实验推翻的判断。>

## 方法设计的核心思想
<说清输入、实际动作、输出，以及与最高近邻的关键差别。>

## 最小实验
<说明模型/数据、最少对照、保持相同的核心预算，以及支持和推翻 Claim 的结果。每个 baseline 都要说明它为何与上述领域、任务和关键词直接相关，并附论文链接、已核验的开源代码链接与复现入口；简单标准 baseline 没有仓库时，明确写出可直接本地实现的依据。无法复现的方法不得放进最小实验。>
```

Keep it short and concrete. The background sentence must describe the field and problem rather than advertising the proposed solution. Do not add a glossary, equations, long related-work discussion, follow-up experiments, risk checklist, candidate ranking, self-score, or explanation of the selection process. Copy it to `CURRENT_IDEA.md`. Record the selected candidate ID and `selected_was_pool_leader: true` in state.

### Phase 3: Independent Reviewer Call

Every invocation consumes reviewer budget. Immediately before `spawn_agent`, increment `reviewer_calls_used` and persist the state. A timeout, tool error, malformed response, format-only retry, or replacement reviewer still counts as one invocation. Never invoke a reviewer when the counter already equals `MAX_ROUNDS`.

Launch a fresh reviewer for every call:

- use a new `spawn_agent` call with no inherited task context;
- never reuse a reviewer ID or continue a reviewer;
- do not pass earlier reviews, earlier scores, candidate lists, self-scores, rankings, diffs, or history summaries;
- give it only the selected four-part brief, frozen Problem Anchor, user constraints, and stable rubric;
- store reviewer IDs only as audit metadata.

```text
spawn_agent:
  fork_turns: none
  model: gpt-5.6-sol
  reasoning_effort: xhigh
  message: |
    You are an independent senior reviewer checking whether a research idea is novel enough
    for experiment planning. You are not a co-author and must not redesign the idea.

    You are intentionally zero-context. Judge only the current four-part brief, the frozen
    Problem Anchor, and the user's constraints. Search the closest prior work as needed. Do not
    invent papers, links, or results.

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
    - experiment_ready: score > 7.5 and no fatal novelty, feasibility, or claim blocker
    - promising_needs_revision: potentially salvageable, but the novelty boundary remains unresolved
    - needs_rethink: the core claim is covered or the experiment cannot test it
    - reject: not worth further work under the stated constraints

    对外只输出下面三个 Markdown 部分，不要给重构方向、修改清单、实验 checklist 或长综述：
    ## 结论
    <用当前日期给出 score、verdict、新颖性判断，以及是否值得继续。>

    ## Claim 判断
    <用短表格逐条判断 Claim：新颖、部分重合或已被覆盖；每条只给最关键依据。>

    ## 最高近邻
    <最多列 5 篇重叠最高的论文或系统；给出可核验链接、重叠点和仍有的差别。每篇 1-2 行；无法核验就写“需要检索”。>

    末尾附上仅供主执行器解析的 JSON，不要增加其他章节：
       {
         "score": 0.0,
         "verdict": "promising_needs_revision",
         "fatal_blockers": [],
         "novelty_conclusion": "...",
         "closest_neighbors": ["paper title or needs_search"]
       }

    Current four-part brief:
    [paste round-N-brief.md]

    Frozen Problem Anchor and user constraints:
    [paste only the frozen anchor and constraints]
```

Save the response as `review-stage/<slug>/round-N-review.md`, append a concise summary to `AUTO_REVIEW.md`, and update the selected entry in `IDEA_CANDIDATES.md` with call number, reviewer score, verdict, and closest neighbors. If the JSON is malformed, the call cannot pass the gate. A fresh replacement is allowed only when budget remains: copy the same selected brief to the next `round-N-brief.md`, persist the incremented call number, and invoke a new reviewer. Do not silently treat a formatting failure as free.

### Phase 4: Gate, Improve, or Stop

Apply the gate directly; reviewer prose or a boolean flag cannot override it:

```text
selected_was_pool_leader == true
AND reviewer_score > 7.5
AND fatal_blockers is empty
```

- If all conditions hold, mark the candidate `final` and proceed to final expansion. `experiment_ready` is the expected reviewer verdict, but the three explicit conditions above are authoritative.
- If the gate fails and `reviewer_calls_used < MAX_ROUNDS`, return to Phase 1, append improved candidates, re-rank the whole eligible pool, and review the new pool leader.
- If the gate fails and `reviewer_calls_used == MAX_ROUNDS`, stop. Do not call another reviewer. Write the blocked finalization using the best current candidate, but do not generate `FINAL_IDEA.md` for an unpassed candidate.
- If no eligible candidate remains before the reviewer budget is exhausted, search and attempt a material revision once. If no defensible candidate can be produced, stop early rather than reviewing a renamed duplicate.

`MAX_ROUNDS` counts reviewer calls only. The number of candidates, local searches, and revisions may be larger than `MAX_ROUNDS`.

## Finalization

### Successful Final Expansion

The main executor performs final expansion itself. Do not spawn or continue an improver agent. Read `templates/improved-idea-template.md`, then expand only the passing candidate using its brief, verified sources, and latest review. Do not change the gated core Claim or its story line during expansion. Map the causal story to Sections 1.1-1.4: specific problem and evidence, what existing work overlooks, this idea's concrete action, and why that action should change the result. For paper input, frame the supplied paper as related work, task origin, or method inspiration; never make “completing the supplied paper” a contribution.

Validate that the result contains the glossary before the title, all required sections, a plain-language method before formulas, and `## References Used`. Fix formatting or missing sections directly. Do not spend reviewer budget on final-document formatting.

On success:

1. Write the expanded proposal to `FINAL_IDEA.md` and copy it to `CURRENT_IDEA.md`.
2. Mark the selected candidate `final` in `IDEA_CANDIDATES.md`.
3. Write `FINAL_REVIEW.md` with the reviewer score, verdict, Claim judgment, highest neighbors, and remaining risks. Do not invent a reviewer redesign plan.
4. Write `EXPERIMENT_HANDOFF.md` with the positioning keywords, problem, primary Claim, method thesis, minimal experiment, budget-matched reproducible baselines, code repositories and reproduction routes, compute/data constraints, references, and remaining risks.
5. Set state status to `completed`.
6. Report paths to `FINAL_IDEA.md`, `IDEA_CANDIDATES.md`, and `EXPERIMENT_HANDOFF.md`.

### Exhausted or No-Viable-Candidate Finalization

1. Do not create `FINAL_IDEA.md` for a candidate that did not pass the explicit gate.
2. Write `FINAL_REVIEW.md` with the best reviewed result and why the gate was not met.
3. Write `PIVOT_OR_STOP.md` with the current highest eligible or least-blocked candidate and the evidence preventing finalization.
4. Preserve all candidates and lineage in `IDEA_CANDIDATES.md`.
5. Set state status to `blocked_max_reviewer_calls` or `rejected_no_viable_candidate`.

## Review Tracing

Trace every reviewer invocation according to `../shared-references/review-tracing.md`. Record the reviewer call number, agent ID, prompt, raw response, parsed score/verdict, and produced artifacts. Explicitly record `context_policy: fresh_zero_context`, `fork_turns: none`, and `continuation_allowed: false` (use `fork_context: false` as equivalent legacy trace metadata only when the trace schema requires that key).

There are no improver-agent traces because improver subagents are forbidden. Record sources used by the main executor in the relevant candidate entries instead.

## Key Rules

- The main executor is the improver. It searches, generates, scores, selects, revises, and expands directly; it never delegates those tasks to subagents.
- Fresh reviewer agents are the only agent calls allowed by this workflow.
- `MAX_ROUNDS` is exactly the maximum number of reviewer invocations. Failed, malformed, replacement, and retry calls count.
- Keep every distinct candidate and revision in `IDEA_CANDIDATES.md`; use stable IDs and parent links, and never overwrite history.
- Treat `IDEA_CANDIDATES.md` as the sole human-readable history; do not maintain a separate evolution digest.
- Give every candidate established positioning keywords, one plain-language background sentence, one causal story line, one idea paragraph, one self-score, one short score rationale, idea-generation sources, lightweight self-score evidence when used, and baseline feasibility evidence.
- Review only the highest self-scored eligible candidate. Do not reveal its self-score or competing candidates to the reviewer.
- Generate `FINAL_IDEA.md` only when that pool leader receives reviewer score strictly greater than 7.5 and has no fatal blocker.
- Intermediate briefs contain only `背景`, `核心 Claim`, `方法设计的核心思想`, and `最小实验`.
- Treat baseline reproducibility as a selection requirement: verify public code for nontrivial methods, keep baselines in the same domain and task as the positioning keywords, and never use a cross-domain inspiration method as an experimental baseline.
- In paper-input mode, read and summarize the paper before ideation, keep it fixed as the user-designated highest neighbor, use the same three idea-finding routes as raw-idea mode, never register the paper itself as a candidate, and reject any candidate whose stated contribution is only a patch or completion of that paper.
- Reviewer human-facing output contains only `结论`, `Claim 判断`, and `最高近邻`; the reviewer does not propose a redesign.
- After a failed review, the main executor reads the cited work itself, appends material revisions as new candidates, and re-ranks all eligible ideas.
- During candidate generation, search only to create ideas; do not check whether each new idea is novel. After a candidate is concrete, use a lightweight novelty check only for self-scoring and ranking. The independent reviewer owns the formal novelty judgment.
- Prefer mature analogous-method transfer or a theory-backed repair of the highest neighbor. Enter the uncovered-new-task route only when the first two routes produce zero concrete candidates.
- Never start experiments inside this skill. The successful terminal artifact is an experiment handoff.
- Do not let ideas grow by accretion. A revision must sharpen the Claim or remove a demonstrated limitation, not merely add modules.
- Treat novelty uncertainty in the lightweight self-score honestly. If relevant overlap cannot be checked cheaply, lower confidence or write `需要 reviewer 检索` rather than pretending the idea is novel.
