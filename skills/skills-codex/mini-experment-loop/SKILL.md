---
name: mini-experment-loop
description: "Implement a validated research idea's minimal experiment inside experiments/{slot}, including resource discovery, environment gates, complete benchmark or method code, bounded smoke tests, auditable run records, independent review, and iterative fixes until the review score is strictly above 8/10. Use when the user invokes /mini-experment-loop, asks to implement a minimal validation experiment, or requests a reviewed mini experiment loop. The misspelled experment slug is intentional for compatibility; correctly spelled mini experiment requests should also trigger it."
---

# Mini Experiment Loop

Turn the fixed Minimal Validation Experiment in an idea document into executable,
reviewed code. Treat novelty as already validated. Do not reopen idea discovery or
expand the paper claim unless an implementation contradiction makes the specified
experiment impossible.

## Inputs And Defaults

Resolve these inputs before doing work:

- `IDEA_PATH` (required): the idea/proposal containing the Minimal Validation Experiment.
- `SLOT` (required or safely inferred): the single directory name under `experiments/`.
- `WORKSPACE_PATH` (optional): an explicitly identified local work directory or prepared
  framework clone. An idea file path is never a workspace path.
- `ENVIRONMENT` (optional): a ready conda/venv/system environment and activation command.
- `RESOURCE_PATHS` (optional): prepared datasets, weights, caches, credentials, or endpoints.

Defaults:

```text
MAX_REVIEW_ROUNDS = 6
PASS_RULE = mode == "postrun" AND score > 8.0 AND verdict == "pass"
            AND blocking_findings == [] AND all MUST requirements are verified
            AND evidence integrity passes AND required tests pass
            AND the canonical smoke run passes
FULL_RUN = false
```

Infer a missing slot only when exactly one unambiguous safe slug follows from the idea
directory or user request. Otherwise ask for the slot before writing files. Resolve the
experiment directory as `<repo>/experiments/<slot>` and reject traversal, symlink escape,
or an explicit workspace that conflicts with this containment rule.

## Non-Negotiable Invariants

1. Write every task artifact, dependency checkout, cache configuration, log, result, and
   review under the resolved experiment directory. Treat prepared resources outside it as
   read-only inputs.
2. Preserve unrelated existing files. Never overwrite a non-template file merely to resume.
3. Never report a planned, dry-run, mocked, or smoke-only number as a completed full result.
4. Never fabricate output, exit status, provenance, hashes, metrics, or reviewer evidence.
5. Do not run full training or a full benchmark by default. Implement its entrypoint and
   validate it with the smallest representative smoke run.
6. Update `EXPERIMENT_STATE.json` after every phase transition and before/after any long or
   externally billed job. On recovery, inspect recorded jobs instead of launching duplicates.
7. Only a fresh reviewer subagent using `$review-mini-experment` may issue the scored verdict.
   The executor must not self-score or edit a review after it is issued.
8. Never persist credential values. Store only credential environment-variable names and
   redact secrets from argv, logs, run records, project documentation, and review inputs while keeping
   commands replayable through variable references.
9. If you write any documents, please write them in Chinese.

## Initialize The Artifact Contract

Read [references/artifact-contract.md](references/artifact-contract.md) before creating or
validating artifacts. Initialize missing files with:

```bash
python <skill-dir>/scripts/init_experiment.py \
  --repo-root <repo-root> \
  --slot <slot> \
  --idea-path <idea-path>
```

The initializer is additive: it creates missing templates and preserves existing files.
Do not manually copy a template over resumed work. The required control artifacts are:

```text
PROJECT.md
EXPERIMENT_CONTRACT.yaml
EXPERIMENT_STATE.json
REQUIREMENTS.jsonl
runs/RUNS.jsonl
schemas/RUN_RECORD.example.json
schemas/REQUIREMENT_RECORD.example.json
schemas/CONTENT_MANIFEST.example.json
schemas/GATE_REPORT.example.json
reviews/round-NNN/{REVIEW.md,REVIEW.json}
```

`PROJECT.md` is the only human-facing project/handoff document. The YAML/JSON/JSONL files are
the machine sources of truth. Do not create the legacy duplicate documents `RESOURCE_REPORT.md`,
`REQUIREMENTS.md`, `IMPLEMENTATION_PLAN.md`, `RESULTS.md`, or `HANDOFF.md`. Preserve them when
resuming an old experiment, but migrate useful facts into the current artifacts and do not
require them for review.

## Phase 0: Recover And Disambiguate

1. Read repository instructions, the complete idea document, existing experiment files, and
   `EXPERIMENT_STATE.json` when present.
2. Compute and record the idea file hash. If it changed since the contract was frozen, diff
   the experiment-relevant requirements and mark the state `blocked` until the contract and
   requirement matrix are reconciled.
3. Distinguish paths by role:
   - a file containing the idea is `IDEA_PATH` only;
   - a directory explicitly described as the work directory is `WORKSPACE_PATH`;
   - model, data, and cache paths are resources, not workspaces.
4. Resume an unfinished state. Never silently delete stale state; record it, inspect active
   job receipts, and archive only with an explicit reason.

## Phase 1: Resource Discovery Gate

Skip online framework discovery only when the user explicitly supplied an existing local
work directory. A local idea document alone does not satisfy this condition.

When no work directory is supplied:

1. Search current online sources for reusable frameworks that satisfy the paper's whole
   minimal experiment, not merely a convenient model component.
2. Compare serious candidates in `EXPERIMENT_CONTRACT.yaml.workspace.framework_candidates` by
   task fit, reusable coverage, extension points, license, maintenance, dependency/runtime fit,
   and expected adaptation. Summarize the decision in `PROJECT.md`.
3. Prefer an official repository or the implementation named by the paper. Record the exact
   GitHub URL, revision/tag when available, license, and why it is preferred.
4. List every required model weight and dataset with its official access URL, license/access
   restrictions, expected size, version, and checksum source when available.
5. If a reusable framework is selected, or required weights/data/private resources are not
   locally prepared, do not download or install them. Record resources in the contract, exact
   user actions in state and `PROJECT.md`, set state to `awaiting_resources`, and return until
   the user supplies their local paths and environment.
6. If no framework adequately covers the experiment, document the search and select a clean
   implementation. Treat the already initialized `experiments/<slot>` as `WORKSPACE_PATH` and
   continue directly to Phase 2; do not ask the user to send that same path back.

## Phase 2: Environment And Resource Gate

When a work directory is available:

1. Inspect it directly. Record framework provenance and the current revision or content hash.
2. Derive the minimum environment from actual imports, lockfiles, framework documentation,
   and the planned smoke path. A named conda environment is not mandatory when another ready,
   reproducible environment satisfies the contract.
3. Probe imports, executables, accelerators, writable output locations, resource readability,
   credentials, and storage without launching the experiment.
4. Do not install packages, create an environment, fetch large assets, or silently switch a
   requested backend. If anything necessary is missing, record exact checks and required paths
   in the contract, state, and the resource section of `PROJECT.md`; set `awaiting_resources`
   and return to the user.
5. Once satisfied, freeze dependency and resource versions in the contract, set
   `resource_gate.status` to `satisfied` with an empty `missing` list, and continue.
   Instrumentation must be added before code review; launch-time tools may not mutate reviewed
   code.

## Phase 3: Freeze Requirements

Extract every normative statement from the idea's minimal experiment and implementation
notes into canonical `REQUIREMENTS.jsonl`, one object per line following
`schemas/REQUIREMENT_RECORD.example.json`. The JSONL records, source-line hashes, and derived
counts are authoritative. `PROJECT.md` may summarize requirements by component but must not
duplicate the atomic matrix. Use this chain for each claim:

```text
claim -> observable contrast -> implementation -> test/oracle -> metric -> threshold -> failure action
```

For each requirement, record its source section/lines and source-text hash, strength
(`MUST`, `SHOULD`, or `MAY`), implementation owner, verification command, expected oracle,
metric/gate, current status, and evidence path. Classify the work as:

Hash `source.lines` canonically as the UTF-8 SHA-256 of the referenced idea lines joined by
`\n` with no trailing newline. Never type aggregate requirement counts by hand: derive
`EXPERIMENT_STATE.json.requirements` from the JSONL records.

- `benchmark`: implement the full minimal benchmark, including deterministic data generation,
  scorer/evaluator, a generic method protocol, required reference/adversarial methods, a CLI
  for complete evaluation, and tests for generation and scoring invariants. Define the adapter
  contract but do not implement method-specific external adapters. If the idea does not name
  methods, include at least one valid reference/control and two distinct nontrivial baseline or
  adversarial methods so the common interface and scorer are genuinely exercised.
- `method`: implement the complete minimal method architecture, configuration, training path,
  evaluation/inference path, checkpoint/resume semantics when applicable, and representative
  tests for forward, loss, update, serialization, and metric behavior.
- `hybrid`: satisfy the union of both contracts.

Do not invent a scientific threshold or protocol detail. Mark underspecified decisions and
their impact explicitly. Ask the user only when different choices would materially change the
claimed experiment; otherwise choose the smallest conventional option and record it.

## Phase 4: Plan And Implement

1. Before code changes, freeze the six responsibility boundaries in
   `EXPERIMENT_CONTRACT.yaml.architecture`: contract/config, data, method, evaluation,
   orchestration, and evidence. Map every `MUST` requirement to a file, interface, test,
   command, and expected artifact in `REQUIREMENTS.jsonl`, then write the human-readable real
   path/interface map in `PROJECT.md`.
2. Reuse the prepared framework when it materially reduces implementation while preserving
   the idea contract. Keep provenance and local changes auditable. Do not force a poorly
   matched framework merely because one was found.
3. For a clean implementation, prefer clear `configs/`, data, methods, evaluation, orchestration,
   tests, and runs boundaries. For a prepared framework, preserve its native layout and map its
   equivalent modules in `PROJECT.md`; do not rearrange code merely to match directory names.
4. Implement the complete minimal execution path. No core path may terminate in a placeholder,
   constant fake metric, unimplemented branch, or hand-authored result.
5. Provide deterministic configuration and explicit seeds wherever supported. Separate raw
   outputs from derived metrics and keep generation, method execution, scoring, and reporting
   callable independently.
6. Add focused unit tests, contract/invariant tests, negative/adversarial tests, and one
   end-to-end integration test. Test the failure modes that could falsely support the paper's
   claim, not only happy-path syntax.
7. Keep full-run and smoke-run commands on the same code path. Smoke mode may reduce examples,
   steps, methods, repeats, and bootstrap samples, but may not replace the algorithm or scorer.
   Freeze required test commands as a list of argv lists and both smoke/full commands as argv
   lists in the contract. Required-test run records must exactly cover
   `acceptance.required_test_commands`; the canonical smoke record must exactly match
   `acceptance.smoke_command`.

## Phase 5: Verify And Record Evidence

Run, in order:

1. static/configuration checks available in the project;
2. focused unit and invariant tests;
3. end-to-end tests;
4. the smallest representative deterministic smoke run;
5. a dry-run or argument/config validation of the full command.

Do not start expensive full execution unless the user explicitly requests it and resources
are ready. Track an active process in state, then append exactly one terminal JSON object per
completed/cancelled/unknown command to `runs/RUNS.jsonl`, following
`schemas/RUN_RECORD.example.json`. Preserve exact argv, cwd, timestamps, exit code,
environment, code/data/config hashes, seeds, scope, raw artifacts, metrics, and limitations.
Replace any credential value with an environment-variable reference or `<REDACTED>` and list
the credential variable names under `environment.credential_env_vars`. Hash every passed-run
stdout, stderr, raw, and metric artifact in `artifact_hashes`.
Store a sorted JSON list of `{path, sha256}` records for every implementation/config input used
by the run, and record that file and its digest as `provenance.content_manifest_path` and
`provenance.content_manifest_sha256`.

Update the evidence section of `PROJECT.md` with verified smoke observations, the unexecuted
full experiment, and claim/gate status. Keep it a concise index into run/raw/metric paths rather
than a second ledger. Recompute at least one reported metric from raw output.
Run the artifact validator before review:

```bash
python <skill-dir>/scripts/validate_experiment.py \
  <repo-root>/experiments/<slot> --for-review
```

Fix structural failures; do not weaken the validator or edit evidence to make it pass.

## Phase 6: Refresh The Project Guide

Complete `PROJECT.md` for a human or reviewer with no conversation context. It must use plain
Chinese and include the stable architecture, real Python file/interface mapping, concise directory
tree, environment/resources, exact test/smoke/full commands, verified evidence index, known
limitations, deferred work, and ordered next steps. Keep both Mermaid diagrams accurate:

- an engineering flowchart whose execution nodes use actual relative `.py::symbol` names and
  whose arrows follow the real config -> entrypoint -> data -> method -> evaluation -> evidence
  call/data path; never use layer-only boxes as a substitute for file-level mapping;
- a sequence diagram naming the actual participating Python entrypoints and showing preflight,
  active-job registration, execution, artifact writing, terminal run receipt, failure path,
  and state update.

Treat the architecture as the baseline for future increments. Update only changed components
unless a real boundary change requires updating the contract, diagrams, mappings, and tests.
Keep it factual: the reviewer must still verify files directly.

## Phase 7: Fresh Review And Fix Loop

For each round from 1 through `MAX_REVIEW_ROUNDS`:

1. Set phase to `reviewing`, create `reviews/round-NNN/`, and then stop mutating experiment
   state until the reviewer finishes. The reviewer freezes a deterministic manifest covering
   tracked and untracked material experiment files while excluding prior `reviews/`, mutable
   `EXPERIMENT_STATE.json`, and tool caches.
2. Launch a fresh-context subagent with `fork_turns="none"` in Codex, or the equivalent
   `fork_context=false` setting in another runtime. Give it only absolute paths to the idea, experiment
   directory, stable rubric, requested mode `postrun`, and round output directory. Do not pass
   executor summaries, prior scores, prior reviews, or expected fixes. Instruct it:

   ```text
   Use $review-mini-experment in postrun mode. Read the idea, PROJECT.md, code, tests,
   and raw run evidence directly. Do not modify implementation files. Write REVIEW.md
   and REVIEW.json under the supplied round directory.
   ```

3. Require parseable `REVIEW.json`. Unknown verdicts, missing evidence, schema errors, or a
   reviewer that edited implementation fail closed and require a new review.
4. Pass only in `postrun` mode when the reported score is strictly greater than 8.0, verdict
   is `pass`, no blocking finding remains, every `MUST` requirement is verified, evidence
   integrity passes, required tests pass, and the canonical smoke run passes. A score of
   exactly 8.0 does not pass.
5. Otherwise set phase to `fixing`, map every P0/P1 and in-scope P2 finding to requirement IDs,
   implement the minimum root-cause fix, and rerun affected tests plus the canonical smoke run.
   Update contracts, evidence, and `PROJECT.md` before launching a new fresh reviewer.
6. Do not hide or delete a disputed finding. Record a path-based rebuttal; only a later fresh
   review may clear it.

If six rounds do not pass, or the same external blocker prevents progress, set status to
`blocked`, preserve the remaining findings and exact user actions, and return. This is not a
successful stop. A same-family fresh subagent review is an engineering `type_a` review; record
it accurately and do not call it cross-family validation.

## Terminal States

- `awaiting_resources`: the user must supply a workspace, environment, asset, credential, or
  material experiment choice. Report the exact checklist and resume command.
- `blocked`: implementation/review cannot progress without a material scope change or external
  action. Preserve evidence and unresolved findings.
- `passed`: the strict review gate passed. Report the experiment directory, verified smoke
  command/result, final score, review path, and explicitly deferred full work.
