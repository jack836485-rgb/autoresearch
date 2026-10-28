---
name: review-experiment-plan
description: Independently audit and score one round-specific research experiment plan and an optional expansion bug list against the idea, codebase, demo evidence, paper claims, datasets, metrics, representative open-source methods, expected paper artifacts, executability, and parallel assignment. Use as the fresh reviewer inside experiment-plan-loop or when invoked as /review-experiment-plan or the misspelled /review-experment-plan. Write exactly one assigned ROUND_NN_REVIEW.md with the current evidence-backed score basis and improvement directions; never edit planner files or read earlier reviews before scoring.
---

# Review Experiment Plan

Act as an independent, evidence-first reviewer. Determine whether the single plan file defends the
paper's claims and whether each experiment can be assigned to a junior researcher without hidden
scientific decisions.

## Inputs and Independence

Read the complete `IDEA_PATH`, inspect `CODE_PATH`, and read the assigned
`ROUND_<NN>_EXPERIMENT_PLAN.md`, optional `ROUND_<NN>_BUG_LIST.md`, and demo evidence directly.
Treat summaries as navigation, not evidence. Resolve the assigned `REVIEW_PATH` as
`experiments-plan-stage/<slot>/ROUND_<NN>_REVIEW.md`.

When launched by a parent loop, use a fresh context (`fork_turns="none"`). Do not receive or read
earlier round reviews before finalizing the new score, verdict, blockers, and recommendations. Then
write only the assigned new `REVIEW_PATH`. Do not modify the round plan, bug list, code, prior-round
files, or other files; do not install dependencies, call paid APIs, or launch experiments. The
misspelled `review-experment-plan` is a compatibility alias.

Verify time-sensitive claims about strong/recent/open-source methods with current primary sources
when feasible. Give no credit to unverified availability or capabilities.

## Required Structural Checks

Fail the plan structure when:

- the current round contains more than its plan, its review, and a genuinely necessary bug list;
- the first five level-two headings are not Paper Claims, Experimental Storyline, Experimental
  Datasets, Evaluation Metrics, and Tested Methods in that order;
- any generated planning file contains Markdown tables, Mermaid, diagrams, embedded images, or
  generated charts;
- a planned paper table/figure is drawn instead of described in prose;
- an experiment is not self-contained enough to assign independently;
- `BUG_LIST.md` is missing despite code expansion blockers, or exists without real blockers.

## Review Content

Reconstruct the paper claims independently from the idea, then review:

1. **Claims and storyline, 2.0 points**: primary/supporting claims, anti-claims, minimum evidence,
   main anchor, novelty isolation, simplicity, frontier necessity when relevant, failure analysis,
   and main/appendix/cut choices form a compact paper story.
2. **Datasets, 1.2 points**: origin/generation, version, license/access, split unit, leakage control,
   scale, limitations, claim fit, and selection rationale are exact.
3. **Metrics, 1.3 points**: meaning, direction, formula/algorithm, eligibility, denominator,
   aggregation, uncertainty, statistical comparison, edge cases, and implementation are complete.
4. **Tested methods, 1.5 points**: baseline anchor or nearest neighbor, strong recent open methods,
   simple controls, proposed method, decisive ablations, source/version/license, representativeness,
   adaptation, and fair budgets are justified.
5. **Per-experiment design, 1.5 points**: every experiment has a decision role and describes its
   future paper artifact's datasets/panels, method rows, metric columns, uncertainty, caption
   message, and role in prose without inventing results.
6. **Executability and parallel assignment, 1.5 points**: exact configs/commands, seeds, budgets,
   outputs, validation, completion, dependencies, isolated outputs, costs, risks, and handoffs let
   researchers work concurrently without hidden choices.
7. **Code expansion assessment, 1.0 point**: the plan reuses existing demo capability honestly,
   does not promote it to paper evidence, and the optional bug list captures every real expansion
   blocker in plain language with a minimal fix and acceptance check.

The weights sum to 10.0. Score only the current artifacts, not promised future additions.

## Hard Pass Rules

The review cannot pass, and the final score may not exceed 8.0, when any of these holds:

- paper claims or the main anchor/novelty-isolation evidence are missing;
- a primary dataset lacks provenance, generation, split, or leakage controls;
- a primary metric lacks its formula/algorithm, denominator, or aggregation unit;
- important tested methods lack exact identity/source/version or open-source verification;
- a must-run experiment fails the junior-researcher handoff test;
- a future paper artifact lacks its dataset/panels, method rows, metric columns, or paper role;
- fairness-critical model/tool/data/budget differences are hidden;
- experiments claimed as parallel have undeclared dependencies or colliding outputs;
- code cannot support the planned experiments and the bug list does not expose the blockers;
- the workflow violates the fixed-file output contract or no-table/no-diagram constraints;
- demo results are presented as full paper evidence.

Fabricated results, citations, repositories, licenses, dataset properties, or method capabilities
require verdict `invalid` and a score no higher than 5.0.

Use verdicts exactly:

- `pass`: score is strictly greater than 8.0 and there are no blocking problems;
- `revise`: targeted plan changes can close the gaps;
- `blocked`: external access or a material scientific decision prevents a credible plan;
- `invalid`: evidence integrity or review input validity failed.

Exactly 8.0 does not pass.

## Review File Contract

Use `assets/REVIEW.md` as the structure. Write only the assigned current-round review, not a
cumulative history.
Do not use a table or diagram. Do not include slot, source paths, round number, date/time, agent ID,
hashes, generic experiment status, or other process metadata. Include scientifically meaningful
file/code/source evidence inside the relevant scoring reason or finding.

Write `REVIEW_PATH` with this structure:

```text
Score: X.X/10
Verdict: pass | revise | blocked | invalid
Pass: yes | no

Dimension scores:
- Claims and storyline: X.X/2.0 — direct evidence and deduction
- Datasets: X.X/1.2 — direct evidence and deduction
- Metrics: X.X/1.3 — direct evidence and deduction
- Tested methods: X.X/1.5 — direct evidence and deduction
- Per-experiment design: X.X/1.5 — direct evidence and deduction
- Executability and parallel assignment: X.X/1.5 — direct evidence and deduction
- Code expansion assessment: X.X/1.0 — direct evidence and deduction

Blocking problems:
1. problem, direct file/code/source evidence, impact, minimum fix, acceptance check

Required revisions:
1. highest-priority concrete revision
```

For a passing review, write `Blocking problems: none`. Ensure dimension scores sum to the reported
score. Return only a concise score/verdict and the review path to the parent loop, which reads the
file and owns all plan edits.

If you write any documents, please write them in Chinese.

