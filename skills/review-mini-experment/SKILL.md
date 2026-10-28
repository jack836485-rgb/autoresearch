---
name: review-mini-experment
description: "Independently audit a minimal research experiment against its idea document, requirement matrix, implementation, tests, raw run evidence, reproducibility, and handoff; issue a structured 0-10 score, blocking findings, and minimum fixes without modifying the implementation. Use when invoked as /review-mini-experment, when a mini experiment needs a preflight or postrun engineering review, or as the reviewer subagent for /mini-experment-loop. The misspelled experment slug is intentional for compatibility; correctly spelled review mini experiment requests should also trigger it."
---

# Review Mini Experiment

Act as an evidence-first reviewer, not a second implementer. Determine whether the experiment
faithfully and completely implements the fixed Minimal Validation Experiment and whether every
reported result can be independently audited.

## Required Inputs

Resolve absolute paths for:

- `IDEA_PATH`: the full idea/proposal;
- `EXPERIMENT_DIR`: the implementation under `experiments/<slot>`;
- `MODE`: `preflight` or `postrun`;
- `OUTPUT_DIR`: a new `EXPERIMENT_DIR/reviews/round-NNN` directory.

`postrun` is required for the scored loop gate. `preflight` may review architecture and tests
before execution, but cannot pass the final loop gate because run evidence is not yet present.

Read [references/review-rubric.md](references/review-rubric.md) completely before scoring. Use
the JSON schema in `assets/templates/REVIEW.example.json` and the narrative structure in
`assets/templates/REVIEW.md`.

When this skill is launched as an independent reviewer, start it without executor conversation
history: use `fork_turns="none"` in Codex or the equivalent fresh-context option elsewhere. Pass
only the input paths, mode, output path, and reviewer task. A reviewer that inherited the
executor's reasoning is not an independent review.

## Independence And Write Boundary

1. Read the idea, requirements, code, tests, commands, run manifests, raw outputs, derived
   metrics, results, and handoff directly. Executor summaries and `HANDOFF.md` are navigation,
   not evidence.
2. Do not read earlier `reviews/round-*` files until the current verdict, score, caps, and
   findings are finalized. Do not accept prior scores or claimed fixes as input.
3. Do not modify implementation, tests, contracts, state, results, run records, or handoff.
   Write only `REVIEW.md` and `REVIEW.json` inside the assigned output directory.
4. Do not install packages, download assets, launch full training/evaluation, use paid APIs, or
   mutate an external service. Run checks with `PYTHONDONTWRITEBYTECODE=1`; for pytest also use
   `-p no:cacheprovider`. Do not leave bytecode, test caches, logs, or command outputs in the
   experiment snapshot. Redirect unavoidable temporary output outside the experiment and remove
   it after the check. If a command cannot avoid persistent writes, record it as `not_run`.
5. Record the review class honestly. A fresh same-family subagent is `type_a`; only a genuinely
   different configured model family may be `type_b`. This engineering score is not an external
   paper-review acquittal.
6. Never copy credential values into argv, logs, evidence, or either review file. Record only
   credential environment-variable names or resource identifiers and replace values with
   `REDACTED`. A redacted command must remain structurally replayable.

If paths are missing, the output directory escapes the experiment directory, or the experiment
is actively changing during review, fail closed with verdict `invalid`.

## Review Procedure

### 1. Freeze Inputs

Before any execution, build a deterministic content manifest for every material regular file
below `EXPERIMENT_DIR`, excluding top-level `reviews/`, mutable orchestration metadata
`EXPERIMENT_STATE.json`, and cache directories (`__pycache__`,
`.pytest_cache`, `.mypy_cache`, `.ruff_cache`, `.hypothesis`, and `.cache`). Reject symlinks.
Each record is exactly `{path, sha256}`, sorted bytewise by relative POSIX path. Hash the
UTF-8 encoding of canonical compact JSON (`ensure_ascii=true`, `sort_keys=true`, separators `,`
and `:`) with SHA-256. Repeat this after all checks; the two manifests must be identical. Store
the final records and manifest digest in `inputs.content_manifest` and
`inputs.content_manifest_sha256`; store the initial digest separately as
`inputs.content_manifest_before_sha256`. The two digests must match.

Also record and verify SHA-256 for the idea, `EXPERIMENT_CONTRACT.yaml`, `REQUIREMENTS.jsonl`,
`runs/RUNS.jsonl`, and `RESULTS.md`. A Git revision or diff hash is optional metadata and never
substitutes for the content manifest because it omits untracked files. Record mode,
backend/model family, and allowed commands. If any material file changes, set verdict `invalid`;
do not silently re-freeze after seeing results.

### 2. Reconstruct The Required Experiment

Read the entire idea, emphasizing Minimal Validation Experiment, implementation notes,
success/failure conditions, data/split protocol, baselines, metrics, uncertainty, and stated
non-goals. Build an independent list of atomic `MUST` requirements before consulting the
executor's requirement statuses.

Then audit the machine source of truth `REQUIREMENTS.jsonl` and its human summary
`REQUIREMENTS.md` for:

- omitted or weakened normative requirements;
- orphan claims, implementations, tests, metrics, or gates;
- invented thresholds or post-hoc protocol changes;
- scientific choices silently substituted for underspecified requirements;
- false `verified` statuses or evidence paths that do not prove the row.

### 3. Inspect Implementation Completeness

Trace each core path through real code rather than filenames or comments.

For benchmark work, verify deterministic data generation, schemas/invariants, scorer semantics,
generic method protocol, required reference and adversarial methods, end-to-end evaluation CLI,
and separation of raw outputs from derived metrics.

For method work, verify the architecture, configuration, data path, training/loss/update path,
evaluation/inference path, serialization/resume semantics when applicable, comparison interface,
and end-to-end commands.

Search for placeholders, constant results, dead branches, hard-coded labels, fixture leakage,
wrong denominators, seed reuse, split leakage, metric eligibility mistakes, swallowed errors,
and smoke/full code-path divergence. A syntactically present component is not complete unless
its required behavior is executable and tested.

### 4. Execute Bounded Verification

Run the documented focused tests and canonical smoke command when resources permit. Also run
the smallest targeted reproducer needed for suspected high-impact bugs. Set
`PYTHONDONTWRITEBYTECODE=1` on Python commands and add `-p no:cacheprovider` to pytest. Record each
check as an object with `kind` (`required_tests`, `canonical_smoke`, `targeted`, or `structural`),
redacted-but-replayable argv list, absolute cwd, exit code, status (`pass`, `fail`, or `not_run`),
and a direct observation.

The `required_tests` entries must exactly cover
`EXPERIMENT_CONTRACT.yaml.acceptance.required_test_commands`; the single `canonical_smoke`
entry must exactly match `acceptance.smoke_command`. Confirm matching passed terminal receipts
also exist in `runs/RUNS.jsonl`. A differently labeled exit-zero command proves nothing.

The required-test gate is true only when at least one `required_tests` command is recorded and
every such command passed with exit code 0. The canonical-smoke gate uses the same rule for
`canonical_smoke`. Preserve failures; do not hide a failed attempt behind an additional passing
entry.

Do not repair a failing command. If a dependency or resource is unavailable, distinguish:

- executor omission: a finding and scoring penalty;
- correctly documented external blocker: verdict `blocked`, not a guessed pass/fail;
- reviewer environment limitation: mark the check `not_run` and rely only on other direct
  evidence, without awarding unverified credit.

### 5. Audit Evidence And Results

Parse `runs/RUNS.jsonl` and sample the files it cites. Verify:

- command, exit status, timestamps, environment, code/data/config provenance, seeds, and scope;
- raw outputs exist and hashes/provenance match where claimed;
- metrics are derived by code from raw outputs with correct eligibility, denominator,
  aggregation, uncertainty, and cluster/repeat unit;
- at least one headline smoke metric can be recomputed independently;
- smoke, dry-run, mock, and full results are labeled correctly;
- failures and negative results remain visible rather than being overwritten;
- no number in `RESULTS.md` lacks a run and raw artifact.

Missing full execution is not a defect when the user requested implementation plus a smoke test,
provided the complete full entrypoint exists, validates, and all claims remain explicitly
deferred. Claiming full support from smoke evidence is a blocking integrity defect.

### 6. Score And Apply Caps

Score each dimension from direct evidence using the stable 10-point rubric. Sum first, then
apply every hard cap. Never raise a dimension to make the total match an intuitive verdict.

Use verdicts exactly:

- `pass`: final score is strictly greater than 8.0 and every hard gate passes;
- `revise`: implementation can be fixed within the frozen minimal experiment;
- `blocked`: a required external resource or material scientific decision prevents judgment;
- `invalid`: evidence integrity, snapshot stability, or review input validity failed.

The pass rule is conjunctive:

```text
mode == "postrun"
score > 8.0
AND verdict == "pass"
AND blocking_findings is empty
AND all MUST requirements are verified
AND evidence_integrity == "pass"
AND required tests passed
AND canonical smoke passed
```

Exactly `8.0` does not pass. An unknown enum, absent field, or contradictory JSON/Markdown
fails closed.

### 7. Write Findings And Minimum Fixes

Order findings by severity (`P0`, `P1`, `P2`). Each finding must contain:

```text
finding ID
severity and blocking boolean
requirement/claim IDs
direct file:line or raw-artifact evidence
reproduction command or static proof
behavioral/scientific impact
root cause
minimum implementation fix
acceptance test/evidence that would close it
all applicable exact cap-condition IDs
```

Encode each finding as:

```json
{
  "id": "P1-001",
  "severity": "P1",
  "blocking": true,
  "requirement_ids": ["REQ-001"],
  "claim_ids": ["CLAIM-001"],
  "evidence": ["src/evaluate.py:41 computes the wrong denominator"],
  "reproduction_or_proof": "python -m pytest -p no:cacheprovider tests/test_metric.py -q",
  "impact": "The primary metric is inflated.",
  "root_cause": "Ineligible rows remain in the denominator.",
  "minimum_fix": "Filter ineligible rows before aggregation.",
  "acceptance_test": "The boundary fixture returns the hand-computed metric.",
  "cap_conditions": ["must_or_blocking_finding"]
}
```

Every field must be present and typed even when an ID list is empty. Evidence must be a non-empty
list. P0/P1 findings are blocking; every P0 declares `p0_invalid`, and every P1 or other blocking
finding declares `must_or_blocking_finding`. Use only cap IDs and exact values from the rubric.

Do not request broad polish when a targeted fix would close the defect. Do not expand beyond the
idea's minimal scope unless the current claim is otherwise untestable; label such a case blocked.

### 8. Emit Both Review Files

Write `REVIEW.md` first, then a consistent, machine-readable `REVIEW.json`. Include raw score,
applied cap, final score, dimension breakdown, verdict, pass boolean, requirement counts,
evidence checks, exact commands, all findings, blocking finding IDs, and ordered next actions.
Every score dimension needs at least one direct evidence item and a non-empty deduction rationale
(`No deduction: ...` is valid for full credit). A non-pass verdict needs at least one next action;
`revise` and `invalid` also need an actionable finding.

The seven booleans in `pass_rule` are derived fields, never reviewer choices:

```text
score_strictly_above_8
verdict_is_pass
zero_blocking_findings
all_must_requirements_verified
evidence_integrity_passed
required_tests_passed
canonical_smoke_passed
```

Before returning, parse `REVIEW.json` with a standard JSON parser and verify:

- all weights sum to 10.0;
- final score equals `min(raw_score, applied_cap)` when a cap exists;
- `pass` matches the conjunctive rule;
- every blocking ID resolves to a finding;
- Markdown and JSON report the same score, verdict, and blockers.

Run the deterministic validator and fix only the review files when it reports a schema or
arithmetic error:

```bash
python <skill-dir>/scripts/validate_review.py <output-dir>/REVIEW.json \
  --review-md <output-dir>/REVIEW.md
```

Return only a concise pointer to the two files and the final score/verdict. The executor owns
all fixes and loop-state updates.
