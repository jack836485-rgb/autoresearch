# Requirement Traceability: {{SLOT}}

## Frozen Source

- Idea path: `{{IDEA_PATH}}`
- SHA-256: `{{IDEA_SHA256}}`
- Frozen at: `{{CREATED_AT}}`

## Minimal Scope

### In Scope

[List the exact minimal experiment scope.]

### Non-Goals

[List exclusions stated by the idea and deliberate implementation exclusions.]

### Open Decisions

| ID | Missing specification | Why it matters | Smallest proposed choice | User decision required | Status |
|---|---|---|---|---|---|

## Falsifiable Claims

| Claim ID | Claim | Observable contrast | Positive control | Negative/adversarial control | Blocking if false | Source |
|---|---|---|---|---|---|---|

## Atomic Requirements

`REQUIREMENTS.jsonl` is the canonical machine-readable source. Append exactly one object per
atomic requirement using `schemas/REQUIREMENT_RECORD.example.json`; keep this table as its
human-readable projection. Threshold basis must be one of `deterministic`,
`point_estimate`, `ci_lower_bound`, `ci_upper_bound`, or `not_applicable`.

| Req ID | Strength | Type | Claim IDs | Normalized requirement | Source section/lines | Source text hash | Implementation | Verification command/test | Oracle | Metric/gate | Threshold basis | Failure action | Status | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

Allowed status values: `unmapped`, `implemented`, `verified`, `blocked`, `deferred`.

## Coverage Lint

- Claims without requirements:
- Requirements without implementation:
- Implementations without tests/oracles:
- Metrics without eligibility/denominator:
- Gates without failure action:
- Idea-defined requirements intentionally deferred:

No `MUST` row may be deferred at the scored review gate.
