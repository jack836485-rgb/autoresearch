# Mini Experiment Review

## Verdict

- Mode:
- Review class: [type_a/type_b]
- Raw score: [0.0]/10
- Applied cap: [none or value and reason]
- Final score: [0.0]/10
- Verdict: [pass/revise/blocked/invalid]
- Pass rule satisfied: [yes/no]
- Blocking findings: [IDs or none]

## Reviewed Snapshot

| Input | Absolute path | Hash/revision | Stable during review |
|---|---|---|---|

- Content manifest SHA-256:
- Content manifest before checks SHA-256:
- Manifest algorithm: SHA-256 of UTF-8 canonical JSON (`ensure_ascii=true`, sorted keys, compact
  separators) over sorted `{path, sha256}` records; top-level `reviews/`,
  `EXPERIMENT_STATE.json`, and cache directories are excluded.

## Requirement Coverage

| Class | Total | Verified | Partial | Missing/invalid |
|---|---:|---:|---:|---:|
| MUST | 0 | 0 | 0 | 0 |
| SHOULD | 0 | 0 | 0 | 0 |
| MAY | 0 | 0 | 0 | 0 |

List requirements independently recovered from the idea but omitted by the executor.

## Score Breakdown

| Dimension | Weight | Awarded | Direct evidence | Deduction |
|---|---:|---:|---|---|
| Requirement fidelity and completeness | 2.0 | 0.0 | | |
| Functional and scientific correctness | 2.0 | 0.0 | | |
| Test and validation strength | 1.5 | 0.0 | | |
| Evidence integrity and auditability | 1.5 | 0.0 | | |
| Reproducibility and interfaces | 1.0 | 0.0 | | |
| Architecture and handoff | 1.0 | 0.0 | | |
| Robustness and scope discipline | 1.0 | 0.0 | | |

## Commands Executed

| Kind | Exact redacted argv | CWD | Exit | Key observation | Status |
|---|---|---|---:|---|---|

## Evidence Audit

- Integrity: [pass/fail/unknown]
- Required tests gate: [pass/fail/not_run]
- Canonical smoke gate: [pass/fail/not_run]
- Recomputed metric:
- Run receipt/provenance checks:
- Smoke/full labeling check:
- Missing or contradictory artifacts:

## Findings

For each finding provide ID, severity, blocking status, requirement/claim IDs, direct evidence,
reproduction/static proof, impact, root cause, minimum fix, and acceptance test.

Also list every applicable machine cap condition: `p0_invalid`, `core_path_missing`,
`smoke_or_core_correctness_failure`, `audit_evidence_insufficient`,
`must_or_blocking_finding`, or `preflight_or_no_smoke`.

## What Is Sound

List directly verified strengths that should be preserved during fixes.

## Ordered Next Actions

List the minimum actions needed for the next review, ordered by severity and dependency.

## Scope Boundary

State which full experiments remain deliberately unexecuted and whether any requested fix would
materially expand beyond the frozen Minimal Validation Experiment.
