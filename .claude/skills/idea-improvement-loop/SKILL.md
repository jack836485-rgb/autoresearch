---
name: idea-improvement-loop
description: "Iteratively develop a genuinely new research idea from a user-provided raw idea, an existing paper supplied as the baseline/starting point, or a problem card from a path-stage research map. The main executor reads and searches directly, reuses path-stage evidence instead of re-searching it, finds ideas through analogous-method transfer, highest-neighbor drawbacks, and field-wide drawbacks, maintains and ranks a candidate pool, and uses fresh zero-context reviewers that search novelty independently. Harness-agnostic. Use when the user says \"改进idea\", \"打磨idea直到可以做实验\", \"improve this idea\", \"基于这篇论文创新\", \"从研究地图/问题卡找idea\", supplies a paper/PDF/arXiv link as a baseline, or asks to preserve competing idea variants before experiment planning."
---

# Idea Improvement Loop

## Overview

Use this skill after a raw idea, a baseline paper, or a path-stage problem card exists, but before committing GPU time. The main executor itself is the Idea Improver:

```text
raw idea | supplied paper | path-stage problem card
  -> write RAW_IDEA.md (paper: summarize it; card: distill the card and reuse its evidence)
  -> main executor generates candidates through four routes and records them in IDEA_CANDIDATES.md
  -> main executor self-scores candidates, picks the pool leader, verifies its baselines
  -> leader becomes a short four-part round-N-brief.md
  -> one fresh zero-context reviewer searches prior work itself and judges novelty
  -> if rejected, main executor improves it, appends new candidates, and re-ranks the pool
  -> if the pool leader receives reviewer score > 8 with no fatal blocker, a second fresh xhigh reviewer re-checks the same brief
  -> only if both pass, expand FINAL_IDEA.md
```

Intermediate communication stays small. The candidate pool keeps every concrete idea version, while each reviewer receives only the selected brief. A full paper-like proposal is produced once, after the gate passes.

## Constants

- **MAX_ROUNDS = 6** — Maximum number of reviewer invocations. It does not limit local searches, candidate generation, self-scoring, file updates, or final expansion.
- **FINAL_REVIEW_THRESHOLD = 8 (exclusive)** — A reviewer score must be strictly greater than 8.
- **STOP_CONDITION** — Generate the final idea only when the reviewed candidate was the highest self-scored eligible candidate at selection time and two independent reviews of the same brief (a first pass and a confirmation) each give score `> 8` with empty `fatal_blockers`.
- **CONFIRMATION_REVIEW = true** — A first passing review only marks the brief `待复核`; a second fresh reviewer must confirm it. The confirmation counts toward `MAX_ROUNDS`.
- **VERDICT_VOCABULARY** = `experiment_ready` / `promising_needs_revision` / `needs_rethink` / `reject`.
- **OUTPUT_IDEA_ROOT = `idea-stage/`**, **OUTPUT_REVIEW_ROOT = `review-stage/`** — Store artifacts under `<root>/<slug>/`.
- **CANDIDATE_TEMPLATE = `templates/idea-candidates-template.md`**; **IMPROVED_IDEA_TEMPLATE = `templates/improved-idea-template.md`** (final expansion only).
- **IMPROVER_AGENT_POLICY = forbidden** — The main executor never delegates candidate generation, literature search, self-scoring, selection, revision, or final expansion to another agent.
- **REVIEWER_CONTEXT_POLICY = fresh_zero_context_each_call** — Every reviewer invocation is a new agent that inherits no conversation context and is never continued or reused.
- **REVIEWER_MODEL = same as the main executor** — Every reviewer is a new instance of the model running this skill; no other model or external API is used. Regular reviews use reasoning effort `high`; the confirmation review uses `xhigh`. The user may override this.
- **HUMAN_CHECKPOINT = false** — If true, pause after each reviewer result; showing a checkpoint does not consume a reviewer call.
- **DO_NOT_REUSE_EXISTING_IDEAS = true** — Do not import ideas from other `idea-stage` directories unless the user explicitly asks. A path-stage map is read only when the user supplies or names it.

User overrides to the reviewer budget or gate threshold take precedence. Write documents in Chinese when the user writes in Chinese. “Highest-scored” means the improver's self-score ranking; “score > 8” means the independent reviewer's score. A self-score never bypasses review.

## Tools and Harness

This skill runs under different agent harnesses. It names required capabilities, not specific tools:

- **Improver**: use whatever search, fetch, and file tools the harness provides. Open primary paper pages or official sources before treating a work as evidence.
- **Reviewer**: use whatever mechanism the harness offers for a separate agent (a subagent tool, a fresh CLI session, an external reviewer backend). It must start with no inherited conversation context, have web search, and run on the main executor's own model at the effort `REVIEWER_MODEL` specifies. If the harness cannot set the effort level, use its default and record that. If the harness cannot start such a reviewer, stop and tell the user; never review in the main context as a substitute.

Bundled tools (standard-library Python in this skill's `tools/` directory; run them from the project root, which contains `idea-stage/` and `review-stage/`):

- `tools/paper_peek.py <arxiv_id>... [--grep kw...]` — title, authors, date, abstract, and code links from the abstract page; with `--grep`, keyword snippets from the HTML full text. Use it for candidate sources, lightweight novelty checks, and reading the works a review cites.
- `tools/repo_check.py <owner/repo|url> [--path dir...] [--readme N]` — whether a baseline repository exists, its last push, directory listing, and README head. Use it in the Phase 2 baseline verification.
- `tools/loop_state.py` — owns `REVIEW_STATE.json`: `init`, `start-call` (checks budget, persists the incremented counter, copies the brief, writes the reviewer prompt from `templates/reviewer-prompt.md`, prints the launcher message), `record` (parses the review's JSON, applies the gate, appends `AUTO_REVIEW.md`), `extend`, `finish`, `status`.

## Mathematical Formula Formatting

Only the final expanded document should normally need formulas. Use `$...$` inline and `$$...$$` for display equations. Define every symbol at first use and explain its operational meaning in plain language.

## Output Layout

Create a stable slug from the idea title or problem (lowercase letters, digits, underscores).

```text
idea-stage/<slug>/
├── RAW_IDEA.md
├── IDEA_CANDIDATES.md         # all distinct candidates, self-scores, lineage, and review status
├── round-01-brief.md          # candidate selected for reviewer call 1
├── ...
├── CURRENT_IDEA.md            # selected brief during the loop; full proposal after finalization
├── FINAL_IDEA.md              # only after the gate passes
└── EXPERIMENT_HANDOFF.md

review-stage/<slug>/
├── round-01-review.md         # response from reviewer call 1
├── ...
├── AUTO_REVIEW.md
├── REVIEW_STATE.json
└── FINAL_REVIEW.md
```

`N` in every `round-N-*` filename is the reviewer invocation number; local improvement work does not advance it. Update fixed aliases in place and do not create timestamped copies. This overrides the archive-copy rule in `../shared-references/output-versioning.md` for this skill while retaining its path and stale-state rules. Follow `../shared-references/output-manifest.md` and `../shared-references/output-language.md` when applicable.

## Candidate Pool Contract

Read `templates/idea-candidates-template.md` before initializing or updating `IDEA_CANDIDATES.md`.

Each distinct candidate gets an immutable stable ID (`IDEA-001`, ...) and records: title; origin route; parent ID or `无`; status; at least three positioning keywords found in the cited literature, benchmark, or official task description (never a disguised method name); one background sentence naming the established field and exact problem; one paragraph stating claim, core method, and minimal experiment; one causal story line; a self-score with a one-sentence rationale; idea-generation sources; lightweight novelty evidence; the baseline plan; mode-specific relation fields; reviewer history.

Origin routes: `原始想法` / `问题卡切口` / `相似领域成熟方法迁移` / `最高近邻不足` / `领域共性不足` / `未覆盖新任务`.

Statuses: `available` / `selected` / `待复核` / `needs_revision` / `covered` / `baseline_patch` / `rejected` / `final`. Only `available` candidates are eligible; `baseline_patch` never is.

The self-score is one overall research judgment, not a scoring worksheet, with at most one decimal place. Generation and scoring are separate: while proposing, search only for abstractions, transferable mechanisms, failure cases, and task definitions; after a candidate is concrete, run one lightweight targeted novelty check for ranking. If overlap cannot be checked cheaply, lower confidence or write `需要 reviewer 检索`. The reviewer owns the formal novelty judgment.

Append every distinct candidate actually considered; do not hide lower-scored ones. Wording changes are not new candidates; a new entry must materially change the claim, mechanism, or minimal experiment. Never overwrite a reviewed candidate; append the revision with `父 Idea` pointing to it. A candidate that is clearly not competing for selection may stay a short entry (title, route, status, keywords, background, one-paragraph summary, self-score with rationale); fill the story line, sources, and baseline table once it becomes the leader.

**Baselines.** An experimental baseline must target the same task and evaluation setting as the positioning keywords. A method from another field is method inspiration, never an experimental baseline. While a candidate sits in the pool, a baseline plan (paper links and expected repositories) is enough. Full reproduction verification happens only for the candidate about to be reviewed (Phase 2). A simple standard baseline without a repository is allowed when its implementation is fully specified and runs locally without unavailable data, checkpoints, or hidden infrastructure.

Do not pass `IDEA_CANDIDATES.md`, self-scores, rankings, or other candidates to the reviewer. `IDEA_CANDIDATES.md` is the only human-readable idea history; write selection reasons, reviewer outcomes, and child IDs back into it.

## State Persistence

`review-stage/<slug>/REVIEW_STATE.json` is written only through `tools/loop_state.py`. It records the input mode and source, the reviewer budget and calls used, the selected candidate and its self-score, `pending_confirmation`, the last score, verdict, blockers and closest neighbors, and every call's candidate, role, effort, brief, prompt, review path, and score. Candidate-pool changes go to `IDEA_CANDIDATES.md`, not to the state file.

On startup, resume an `in_progress` state less than 24 hours old; otherwise start a new run unless the user asks to resume. For a state created under an older schema, treat its `round` value as reviewer calls already used and never reset the counter.

## Workflow

### Phase 0: Initialize

1. Classify the input:
   - `baseline_paper` when the user supplies a paper, PDF, paper URL, or precise citation and asks to innovate from it. Read [references/paper-input.md](references/paper-input.md).
   - `problem_card` when the user points to a path-stage map directory, `研究地图.md`, `研究问题.json`, or a problem ID in one. Read [references/problem-card-input.md](references/problem-card-input.md).
   - `raw_idea` otherwise.
2. Write `RAW_IDEA.md` before candidate generation: the user's idea and explicit constraints for `raw_idea`; the mode-specific template for the other two.
3. Read nearby context only when clearly applicable: `RESEARCH_BRIEF.md`, the matching idea/review directory, `refine-logs/FINAL_PROPOSAL.md`, and relevant local notes.
4. Freeze the Problem Anchor: bottom-line problem; target domain, benchmark, and setting; must-solve bottleneck; compute, data, time, venue, codebase, and non-goal constraints; success condition that would justify experiment planning.
5. Initialize `IDEA_CANDIDATES.md`, then run `tools/loop_state.py init --slug <slug> --mode <mode> --max-calls <MAX_ROUNDS> --source <input>` to create `REVIEW_STATE.json` and `AUTO_REVIEW.md`.

If the input is too vague to anchor, ask at most one concise clarification. If a supplied paper or map cannot be accessed, ask for it instead of inventing contents.

### Phase 1: Candidate Generation

The main executor performs this phase directly. Search here exists to produce ideas, not to prove novelty. Use the same routes in every input mode.

**Route priority.** Routes 1–3 are the main routes; any of them may come first, and they combine naturally: routes 2 and 3 locate a drawback, and route 1 often supplies the mechanism that fixes it. In `problem_card` mode, start from routes 3 and 2, because the card already documents a field-level failure and its existing fixes. Enter route 4 only when routes 1–3 produce no candidate with self-score above 7.

1. **相似领域成熟方法迁移。**
   - Abstract the problem away from field vocabulary: input, output, core transformation, constraints, failure condition.
   - Ask which other field must perform the same transformation or obeys the same structural constraint. Similarity must be structural, not topical.
   - Understand the mature method's key assumptions and actual operations, then map them one by one: what carries over, what must change, how inputs and outputs stay usable. Drop candidates whose key enabling condition cannot be mapped.
   - 示例：图像扩散与语言生成共享“从扰动状态逐步恢复样本”的结构；可迁移的是逐步去噪思想，需要重新设计的是离散状态、扰动过程与反向转移，而不是搬运模块名。
   - Story line：当前方法在明确条件下失败 → 相似领域已验证某关键思想 → 两领域共享使其成立的结构 → 本 Idea 的最小适配 → 同预算下应改善的指标或失败模式。

2. **最高近邻不足。** Pick the single highest neighbor (the supplied paper in `baseline_paper` mode; the strongest existing fix on the card in `problem_card` mode).
   - Read its full pipeline: input, modules, each module's role, supervision or objective, output, evaluation.
   - For each module, reason `模块作用 → 依赖的假设 → 假设失效的条件 → 可观察后果`, not from where code is easy to change.
   - Generate a candidate only when this yields an independent, testable field-level problem; “replace this module” alone is low priority.
   - The minimal experiment must contain both a defect diagnosis and a test of whether the mechanism fixes the defect.
   - 示例：PPO→DPO 不是“把 PPO 换成监督损失”，而是先拆解 reward model、采样和策略优化的作用，反推出“多阶段 RLHF 为把偏好转成策略更新引入额外训练环节”的领域问题，再提出直接从偏好对构造策略目标的机制。
   - Story line：最高近邻依赖一个有缺陷的假设或模块 → 诊断实验验证缺陷存在 → 本 Idea 的机制 → 最小实验同时检验缺陷与机制。

3. **领域共性不足。** A failure, untested assumption, or unexplained disagreement shared by a method family or several independent works, rather than one paper's omission.
   - Establish the drawback from at least two independent works (or one controlled study covering several methods). Path-stage cards supply this directly through their evidence, `待验证解释`, `尚未解决`, and cross-paper disagreements.
   - State the shared condition under which the works fail and the common assumption behind it. Check whether existing fixes remove that cause or only one symptom.
   - When competing explanations exist, design a diagnostic that separates them before proposing a mechanism; a candidate that resolves a documented disagreement is valuable even if its mechanism is simple.
   - The mechanism targets the shared cause, and the minimal experiment shows the effect on at least two members of the method family, or states why one suffices.
   - 示例：多种长上下文模型都在关键信息位于中段时检索变差（lost in the middle）。共性不足是位置偏置，不是某个模型的缺陷；先用控制位置的诊断确认偏置来源，再提出针对共同原因的机制，并在多个模型上检验。
   - Story line：多项工作在条件 X 下出现同一失败 → 共同原因或未检验假设 → 现有修补只处理症状 → 本 Idea 针对共同原因的动作 → 可推翻的预期结果。

4. **未覆盖新任务（后备）。**
   - Start from a real large problem and subdivide by stage, object, environment, constraint, or failure type until reaching a recurring problem that existing tasks or benchmarks do not measure. Renaming is not a new task.
   - Prove the problem exists with real cases, data, or evaluation blind spots; then define task input, expected output, data construction, and a minimal metric. Without objective evidence, drop the candidate. Do not invent a task to house a method.
   - 示例：RAG → 长期记忆 → 图结构记忆的持续维护：现有 RAG 任务不单独测图维护能力，于是定义“输入当前记忆图与新交互、输出增删合并决策”的任务。

For `raw_idea`, register the raw idea itself as a candidate with source `原始想法`. For `problem_card`, register the card's `可检验切口` as a candidate with source `问题卡切口`. Either may score low but remains a comparison point. There is no required candidate count and no requirement to populate every route.

Write each story line as one causal paragraph, `明确失败及证据 → 被忽视的关键 → 本 Idea 的具体动作 → 可支持或推翻的预期结果`, with every link backed by literature, theory, or the minimal experiment. Never claim “大家效果都不好” or “相关工作都忽视了” without evidence, and phrase expected improvements as hypotheses.

After a failed review, while budget remains:

1. Mark the reviewed candidate `needs_revision`, `covered`, or `rejected`.
2. Read the review's cited closest work directly; do not rely on the reviewer's summary.
3. Improve through the same routes; reapply mode-specific checks (paper-removal test in `baseline_paper` mode).
4. Append each material revision as a new candidate with `父 Idea` set.
5. Re-rank all `available` candidates, including older unreviewed ones.

A revision must sharpen the Claim or remove a demonstrated limitation, not accrete modules.

### Phase 2: Select, Verify Baselines, and Write the Brief

Let `N = reviewer_calls_used + 1`. If `reviewer_calls_used >= MAX_ROUNDS`, go to the blocked finalization.

1. Select the highest self-scored `available` candidate. On ties, judge directly and record a one-sentence reason in `当前选择`.
2. Verify its baselines now: for every nontrivial baseline, open the public repository, confirm it implements the cited method, and record the entry point, configuration, or command for reproduction. If a baseline fails, replace it with a reproducible same-task baseline or move the method to related work. If no reproducible baseline remains, mark the candidate `needs_revision`, record why, and return to step 1. Also confirm that the phenomenon the experiment depends on has been reported on the chosen model and setting (for example, that a model organism actually shows the behavior at that model size); if the only evidence comes from a different model family or scale, say so in the brief or change the setting.
3. Write `round-N-brief.md` with exactly:

```markdown
## 背景

**定位关键词：** <至少三个能在所引论文、benchmark 或官方任务说明中直接找到的已有关键词；不要自创术语。>

**一句话定位：** <只用一句话说明这是哪个已有领域里的什么具体问题。>

## 核心 Claim
<按“现有方法在哪个明确条件下失败、被忽视的关键是什么、本 Idea 因此主张什么”的顺序，用说人话的方式说明几个可被实验推翻的判断。>

## 方法设计的核心思想
<说清输入、实际动作、输出，以及与最高近邻的关键差别。>

## 最小实验
<说明模型/数据、最少对照、保持相同的核心预算，以及支持和推翻 Claim 的结果。每个 baseline 都要说明它为何与上述领域、任务和关键词直接相关，并附论文链接、已核验的开源代码链接与复现入口；简单标准 baseline 没有仓库时，明确写出可直接本地实现的依据。无法复现的方法不得放进最小实验。算力和 API 预算要给出估算依据（如运行数 × 单次时长、调用次数 × 每次评判数 × 单价）。>
```

Keep it short. The background describes the field and problem, not the solution. No glossary, equations, long related work, risk checklist, ranking, self-score, or selection history. Do not paste path-stage map content beyond what the four sections need. Mark the candidate `selected` in `IDEA_CANDIDATES.md`; `start-call` copies the brief to `round-N-brief.md` and `CURRENT_IDEA.md` and records it as the pool leader.

### Phase 3: Independent Reviewer Call

Every launch counts as one call: a timeout, tool error, malformed response, format-only retry, or replacement reviewer still consumes budget. Never launch a reviewer when the budget is used up.

1. Run `tools/loop_state.py start-call --slug <slug> --candidate <ID> --self-score <x> --brief <draft brief> --effort high --date <today> --workarounds "<known tool workarounds or none>"`. It refuses when the budget is used up, persists the incremented counter before anything else, and writes the reviewer prompt to `review-stage/<slug>/prompts/round-N-review-prompt.md` from [templates/reviewer-prompt.md](templates/reviewer-prompt.md), the brief, and the Problem Anchor section of `RAW_IDEA.md`.
2. Launch a fresh reviewer as described in the Tools and Harness section and send it only the printed `launcher_message`, which points it at the prompt file. The prompt contains the brief, the frozen Problem Anchor and user constraints, the stable rubric, today's date, known tool workarounds, and the path where the reviewer writes its raw review. Never pass earlier reviews or scores, candidate lists, self-scores, rankings, diffs, history, the improver's novelty evidence, or path-stage map contents: the reviewer finds prior work through its own search. Store reviewer identifiers only as audit metadata.
3. If the harness reports that the reviewer stopped while its own background work was still running, the response is interim: wait for the final one. If the harness does not let the reviewer write files, save its final message to the review path yourself.
4. Run `tools/loop_state.py record --slug <slug>`. Malformed JSON cannot pass the gate. Then update the candidate entry in `IDEA_CANDIDATES.md` with call number, score, verdict, and closest neighbors.

A fresh replacement after a failed call is allowed only when budget remains: run `start-call` again with the same brief.

### Phase 4: Gate, Improve, or Stop

`record` applies the gate and prints the outcome and next step; reviewer prose or flags cannot override it:

```text
first_pass   = selected_was_pool_leader AND reviewer_score > 8 AND fatal_blockers is empty
gate_passed  = first_pass on a regular review
               AND the confirmation review of the same brief also has score > 8 and no fatal blocker
```

- First pass on a regular review: set `pending_confirmation` to the candidate ID and brief path, mark the candidate `待复核` in `IDEA_CANDIDATES.md`, and if budget remains, immediately run the confirmation review with `start-call --role confirmation --effort xhigh`, which reuses the same brief unchanged. The confirmation reviewer gets the same inputs as any reviewer and is not told that an earlier review exists or what it said.
- Confirmation passes: mark the candidate `final` and go to final expansion.
- Confirmation fails: clear `pending_confirmation`, mark the candidate `needs_revision`, and treat it like any failed review. Any revision is a new brief and needs its own first pass and confirmation.
- First pass on the last budgeted call, leaving no budget for confirmation: stop with the blocked finalization and state `首轮通过、未复核` in `FINAL_REVIEW.md`.
- Gate fails with budget left: return to Phase 1, append improved candidates, re-rank, and review the new leader.
- Gate fails with budget exhausted: stop and write the blocked finalization; no `FINAL_IDEA.md` for an unpassed candidate.
- No eligible candidate before budget runs out: attempt one material revision; if no defensible candidate results, stop early rather than reviewing a renamed duplicate.

## Finalization

### Successful Final Expansion

The main executor expands the passing candidate itself. Read `templates/improved-idea-template.md` and expand using the brief, verified sources, and latest review without changing the gated Claim or story line. Map the causal story to Sections 1.1–1.4: specific problem and evidence, what existing work overlooks, this idea's concrete action, why that action should change the result. In `baseline_paper` mode, frame the supplied paper as related work, task origin, or inspiration, never as the object being completed. In `problem_card` mode, cite card evidence through its original paper links, not through the map.

Validate that the result contains the glossary before the title, all required sections, a plain-language method before formulas, and `## References Used`. Fix formatting directly; do not spend reviewer budget on it.

On success:

1. Write `FINAL_IDEA.md` and copy it to `CURRENT_IDEA.md`.
2. Mark the candidate `final` in `IDEA_CANDIDATES.md`.
3. Write `FINAL_REVIEW.md` with the reviewer score, verdict, Claim judgment, highest neighbors, and remaining risks. Do not invent a reviewer redesign plan.
4. Write `EXPERIMENT_HANDOFF.md` with positioning keywords, problem, primary Claim, method thesis, minimal experiment, budget-matched reproducible baselines with repositories and reproduction routes, compute/data constraints, references, and remaining risks.
5. Set state status to `completed` and report the paths to `FINAL_IDEA.md`, `IDEA_CANDIDATES.md`, and `EXPERIMENT_HANDOFF.md`.

### Exhausted or No-Viable-Candidate Finalization

1. Do not create `FINAL_IDEA.md`.
2. Write `FINAL_REVIEW.md` with the best reviewed result and why the gate was not met.
3. Write `PIVOT_OR_STOP.md` with the highest eligible or least-blocked candidate and the evidence preventing finalization.
4. Preserve all candidates and lineage in `IDEA_CANDIDATES.md`.
5. Set state status to `blocked_max_reviewer_calls` or `rejected_no_viable_candidate`.

## Review Tracing

Trace every reviewer call according to `../shared-references/review-tracing.md`: call number, role (`regular` or `confirmation`), reviewer identifier, model and effort, the mechanism used to launch it, prompt, raw response, parsed score/verdict, and produced artifacts. Record `context_policy: fresh_zero_context` and `continuation_allowed: false`. There are no improver-agent traces; record the main executor's sources in candidate entries.

## Key Rules

- The main executor is the improver and never delegates its work; fresh zero-context reviewers are the only other agents.
- `MAX_ROUNDS` counts every reviewer invocation, including failed and replacement calls.
- Review only the pool leader, after verifying its baselines; never reveal self-scores, competing candidates, earlier reviews, or the improver's evidence to the reviewer.
- Reviewers run on the executor's own model; a pass needs a first `high` review and an independent `xhigh` confirmation of the same brief.
- Reuse supplied path-stage evidence instead of re-searching it; the reviewer always searches independently.
- Keep every distinct candidate with stable IDs and parent links; `IDEA_CANDIDATES.md` is the sole human-readable history.
- Never start experiments inside this skill. The successful terminal artifact is an experiment handoff.
