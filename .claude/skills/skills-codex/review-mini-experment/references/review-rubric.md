# Mini Experiment Review Rubric

Use this rubric without changing weights between rounds.

## Contents

1. Severity
2. Weighted score
3. Hard caps
4. Evidence integrity
5. Pass decision

## 1. Severity

- `P0`: fabricated/mutated evidence, destructive or unsafe behavior, data/label leakage that
  invalidates the experiment, or a core evaluator error that reverses conclusions.
- `P1`: missing required component, reproducible correctness bug, failed required test, invalid
  metric/protocol, non-reproducible core path, or a `MUST` requirement without valid evidence.
- `P2`: localized robustness, clarity, coverage, or handoff weakness that does not invalidate
  the current core result by itself.

P0 and P1 findings are blocking. A P2 may be blocking only when multiple instances jointly make
the experiment unauditable or unusable; explain why.

## 2. Weighted Score

Score each dimension from 0 up to its stated weight. Use decimals when useful.

| Dimension | Weight | Full-credit evidence |
|---|---:|---|
| Requirement fidelity and completeness | 2.0 | Every idea-defined MUST is faithfully mapped, implemented, verified, and not weakened or silently deferred. |
| Functional and scientific correctness | 2.0 | Core paths and scorer/method semantics are correct under direct inspection and targeted execution; adversarial cases fail as intended. |
| Test and validation strength | 1.5 | Focused, invariant, negative, integration, and representative smoke tests cover claim-threatening failures and pass on the real path. |
| Evidence integrity and auditability | 1.5 | Run receipts, immutable raw artifacts, provenance, metric derivation, failure history, and claim labels are complete and independently checkable. |
| Reproducibility and interfaces | 1.0 | Environment/resources, deterministic seeds, configs, public protocol/CLI, and smoke/full commands are sufficient to reproduce the path. |
| Architecture and project guide | 1.0 | Boundaries are coherent and `PROJECT.md` maps the real call/data flow down to `.py::symbol`, while accurately indexing commands, evidence, limitations, and review entry points. |
| Robustness and scope discipline | 1.0 | Errors fail visibly; splits/seeds/resources are safe; implementation stays within the fixed minimal scope without hidden operational risk. |

Scoring anchors within each dimension:

- `100%`: directly verified, complete, and no material defect;
- `75%`: substantially correct with a localized non-blocking gap;
- `50%`: partial implementation/evidence or important unverified behavior;
- `25%`: mostly nominal, placeholder-like, or contradicted by execution;
- `0%`: absent, invalid, or fabricated.

Do not award credit for executor assertions, file names, TODO plans, or an unexecuted command.
A reviewer test/smoke gate is valid only when its argv matches the frozen acceptance command and
a matching passed terminal receipt exists in `runs/RUNS.jsonl`.

## 3. Hard Caps

Compute the raw weighted sum, then apply the lowest applicable cap. Emit the exact condition ID
and value shown here; do not invent cap names or choose a looser value.

| Condition ID | Trigger | Verdict constraint | Exact cap |
|---|---|---|---:|
| `p0_invalid` | Any P0 finding, including fabricated/mutated evidence, unsafe behavior, leakage, or a conclusion-reversing evaluator defect | `invalid`; integrity `fail` | 3.0 |
| `core_path_missing` | A core benchmark/method path is absent, placeholder-only, or has no real end-to-end implementation | `revise` | 5.0 |
| `smoke_or_core_correctness_failure` | Canonical smoke fails, evaluator/metric is materially wrong, or train/eval cannot execute | `revise` | 6.0 |
| `audit_evidence_insufficient` | Evidence integrity fails without a P0, or run receipts/raw artifacts cannot support the observations | `revise` or `invalid` | 7.0 |
| `must_or_blocking_finding` | A MUST is omitted/unverified, required tests do not pass, or any blocking/P1 finding remains | not `pass` | 8.0 |
| `preflight_or_no_smoke` | Mode is preflight or canonical representative smoke has not passed | not `pass` | 8.0 |

Caps do not replace dimension deductions. Put applicable IDs in each finding's
`cap_conditions`, report the union as `score.triggered_caps`, apply every automatic gate above,
and set `score.applied_cap` to the lowest exact value. A P0 always forces `p0_invalid`, verdict
`invalid`, and evidence integrity `fail` even when the P0 is not itself an evidence-fabrication
finding.

The absence of a full expensive run does not trigger a cap when all of the following hold:

1. the user requested implementation plus bounded smoke validation;
2. the complete full entrypoint and frozen config exist and validate;
3. the smoke uses the real algorithm and scorer path;
4. `PROJECT.md` explicitly marks full results as unexecuted;
5. no scientific success claim relies on the missing full execution.

## 4. Evidence Integrity

Set `evidence_integrity` to:

- `pass`: sampled claims trace to consistent run records, raw outputs, provenance, and derived
  metrics; no material mislabeling is found;
- `fail`: any material fabrication, mutation, mismatch, unsupported number, or smoke/full
  misrepresentation is found;
- `unknown`: required artifacts cannot be accessed for a reviewer-environment reason.

`unknown` cannot pass the final gate. Distinguish missing executor evidence from a reviewer-only
environment restriction.

Minimum audit sample:

- every number emphasized as a primary observation;
- at least one passing and one failing/negative-control case when they exist;
- at least one metric recomputed from raw output;
- code/config/data provenance for the canonical smoke run;
- any gate near its threshold;
- any result used to claim a bug was fixed.

## 5. Pass Decision

Pass only when all are true:

```text
mode == postrun
final_score > 8.0
verdict == pass
blocking_findings == []
all MUST requirements independently verified
evidence_integrity == pass
required tests passed
canonical smoke passed
```

Use `blocked` only for a genuine external resource or material scientific choice. Ordinary bugs,
missing code, missing tests, or incomplete evidence are `revise`. Use `invalid` when the snapshot
or evidence cannot support a trustworthy review.
