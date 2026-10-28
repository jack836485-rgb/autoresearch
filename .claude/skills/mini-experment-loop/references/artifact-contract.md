# Mini Experiment Artifact Contract

Read this contract before initializing or reviewing a workspace.

## Contents

1. Ownership and layout
2. Requirement traceability
3. Run evidence
4. Result and gate semantics
5. State transitions
6. Review handoff

## 1. Ownership And Layout

The experiment executor is the only writer of implementation files,
`EXPERIMENT_STATE.json`, contracts, manifests, results, and handoff documents. A reviewer may
write only inside its assigned `reviews/round-NNN/` directory.

All generated files must remain below the canonical experiment directory:

```text
experiments/<slot>/
  EXPERIMENT_CONTRACT.yaml
  EXPERIMENT_STATE.json
  RESOURCE_REPORT.md
  REQUIREMENTS.md
  REQUIREMENTS.jsonl
  IMPLEMENTATION_PLAN.md
  RESULTS.md
  HANDOFF.md
  schemas/
    CONTENT_MANIFEST.example.json
    REQUIREMENT_RECORD.example.json
    RUN_RECORD.example.json
    GATE_REPORT.example.json
  runs/
    RUNS.jsonl
    <run-id>/
      stdout.log
      stderr.log
      raw/
      metrics.json
  reviews/
    round-NNN/
      REVIEW.md
      REVIEW.json
  <implementation-owned files and directories>
```

External datasets, weights, and framework sources may be read-only inputs. Record their
absolute path, version, license, and hash or immutable identifier. Never write caches beside
an external resource; point caches into the experiment directory.

## 2. Requirement Traceability

Each atomic requirement must connect one or more claims to executable evidence:

```text
claim -> contrast -> implementation -> test/oracle -> metric -> threshold -> failure action
```

`REQUIREMENTS.jsonl` is canonical and contains exactly one JSON object per atomic requirement.
`REQUIREMENTS.md` is its readable projection. Required machine fields are:

- stable ID and strength (`MUST`, `SHOULD`, `MAY`);
- source file, section/line reference, and source-text hash;
- normalized requirement and claim IDs;
- implementation files/symbols;
- test or verification command;
- oracle or expected property;
- metric IDs and threshold, including whether the threshold applies to a deterministic value,
  point estimate, CI lower bound, or CI upper bound;
- status (`unmapped`, `implemented`, `verified`, `blocked`, `deferred`);
- evidence paths and unresolved reason.

The `source.lines` value uses `start` or `start-end`. Compute `source.text_sha256` from those
idea lines joined by `\n` with no trailing newline. Derive every requirement count in
`EXPERIMENT_STATE.json` from the JSONL; never accept a hand-maintained summary as evidence.

Do not silently resolve an underspecified scientific choice. Record it under Open Decisions.
The executor may make a conventional engineering choice only when it does not materially alter
the paper claim or pass/fail interpretation.

## 3. Run Evidence

`runs/RUNS.jsonl` is append-only. Each line must be one valid JSON object. A rerun receives a
new run ID; never edit a failed record into a pass.

Minimum run record fields:

```text
schema_version, run_id, purpose, status
command_argv, cwd, started_at, ended_at, exit_code
environment, provenance, config, seeds, scope
stdout_path, stderr_path, raw_artifacts, metrics_path
artifact_hashes
requirement_ids, claim_ids, limitations
```

Run provenance must also contain a deterministic content-manifest SHA-256 that covers
untracked implementation files, plus the relative path to that sorted JSON manifest. Each
manifest item is exactly `{path, sha256}`; it must cover every implementation/config file used
by the run and its digest must match the recorded manifest digest. Record only credential
environment-variable names. Redact
credential values from argv, environment data, logs, raw artifacts, and reports.
For every passed run, `artifact_hashes` must exactly map stdout, stderr, raw-artifact, and
metric paths to their SHA-256 digests.

Use `purpose` values `test`, `smoke`, `full`, `analysis`, or `dry_run`. Append a run record only
when the command reaches a terminal status: `passed`, `failed`, `cancelled`, or `unknown`.
Track an active process or remote job under `EXPERIMENT_STATE.json.active_jobs`; do not append a
`running` row and later rewrite or duplicate it. A smoke run must record exactly how it differs
from the full protocol. A dry run proves only configuration/entrypoint validity.

For long or billed jobs, also record backend, job/session ID, estimated cost, durable output
path, cleanup owner, and job status checks. Persist state before launch and after collection.

## 4. Result And Gate Semantics

Keep raw outputs immutable and derive metrics with code. `RESULTS.md` must label each statement:

- `verified-smoke`: executed on a reduced but real code path;
- `verified-full`: executed under the frozen full protocol;
- `planned`: command/config exists but was not executed;
- `unsupported`: required evidence is absent or invalid.

Every numeric result must point to a run record and raw/derived artifact. Record units,
denominator, aggregation, randomness, and uncertainty. A result generated from a mock fixture is
a test observation, not experimental evidence.

Gate reports must contain the observed value, uncertainty when applicable, comparison operator,
threshold, threshold basis, pass boolean, source run IDs, evidence paths, and failure action.
Never change an idea-defined threshold after seeing results.

Freeze `acceptance.required_test_commands` as a non-empty list of unique argv lists, and freeze
`acceptance.smoke_command` and `acceptance.full_command` as argv lists. State-selected passed
test receipts must exactly cover the required-test list, and the state-selected canonical smoke
receipt must exactly equal the frozen smoke argv.

## 5. State Transitions

Use these statuses:

```text
in_progress | awaiting_resources | blocked | passed
```

Use these phases:

```text
initialized | discovering | awaiting_resources | planning | implementing
testing | reviewing | fixing | passed | blocked
```

Use resource-gate statuses `unknown`, `awaiting`, `satisfied`, or `blocked`. Scored review
requires `satisfied` with an empty missing-item list.

Update state atomically after each transition. Preserve created time and prior round records.
On recovery, validate the current job and artifacts; never infer that an unknown launch failed
and relaunch it blindly.

The review gate is fixed:

```text
score > 8.0
AND mode == "postrun"
AND verdict == "pass"
AND no blocking findings
AND all MUST requirements verified
AND evidence integrity passed
AND required tests passed
AND canonical smoke passed
```

## 6. Review Handoff

`HANDOFF.md` is an index, not evidence. It must make direct verification fast by naming:

- architecture and data/control flow;
- public interfaces and entrypoints;
- requirement-to-code/test mapping;
- exact environment and resource provenance;
- exact test, smoke, and full commands;
- run IDs and raw artifact paths;
- verified versus deferred scope;
- known defects, limitations, and expensive work not run.

The reviewer must still inspect code, execute bounded tests, and sample raw evidence directly.
