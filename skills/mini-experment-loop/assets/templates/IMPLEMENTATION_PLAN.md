# Implementation Plan: {{SLOT}}

## Strategy

- Task type: [benchmark/method/hybrid]
- Reuse mode: [prepared framework/clean implementation]
- Minimality argument:
- Full execution deliberately deferred:

## Architecture

Describe components and their data/control flow. Name stable interfaces and ownership
boundaries.

## Requirement Map

| Component ID | Requirement IDs | Files/symbols | Inputs | Outputs | Determinism/seeds | Tests | Artifact |
|---|---|---|---|---|---|---|---|

## Benchmark Contract

Complete this section for benchmark or hybrid work:

- deterministic data/world generation:
- dataset schema and split/leakage invariants:
- generic method protocol:
- external adapter boundary:
- reference methods:
- adversarial/negative-control methods:
- scorer/evaluator and metric eligibility:
- end-to-end full evaluation CLI:

## Method Contract

Complete this section for method or hybrid work:

- architecture and configuration:
- data interface:
- training/loss/optimization path:
- evaluation/inference path:
- checkpoint/resume/serialization:
- baseline/comparison interface:
- end-to-end train and evaluate CLI:

## Verification Plan

| Test ID | Requirement IDs | Kind | Fixture/scope | Assertions/oracle | Command | Expected artifact |
|---|---|---|---|---|---|---|

Include unit, invariant, negative/adversarial, integration, and representative smoke tests.

## Commands

### Focused Tests

```bash
# exact command
```

### Canonical Smoke Run

```bash
# exact command using the real implementation/scoring path
```

### Full Run (Implemented, Not Run By Default)

```bash
# exact command
```

## Smoke Reductions

| Dimension | Full protocol | Smoke protocol | Semantics preserved |
|---|---|---|---|

## Risks And Rollback

| Risk | Detection | Mitigation | Failure action |
|---|---|---|---|

