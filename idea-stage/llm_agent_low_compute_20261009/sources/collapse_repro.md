# Reproducing these experiments

These are the experiments reported in [*Useful Memories Become Faulty When Continuously Updated by LLMs*](https://arxiv.org/abs/2605.12978) (arXiv:2605.12978).

An experiment runs in four stages, and you can enter at any of them depending on
what you already have. The directories are named after the stage that produced
them, so "what do I need" has a short answer.

```
tasks/  ──►  rollout  ──►  pools/  ──►  compress  ──►  memory/  ──►  evaluate  ──►  results/ + trajectories/
```

| Start from | You re-run | You need | Size |
|---|---|---|---|
| **A. nothing** — just check the arithmetic | nothing | `per-task-results.jsonl`, `numbers/` | 40 MB |
| **B. the task lists** | rollout → compress → evaluate | `tasks/` + `code/` + [`env/`](../env/README.md) | 50 MB + the environment |
| **C. the rollouts** | compress → evaluate | + `pools/` | + 262 MB |
| **D. the memories** | evaluate only | + `memory/` | + 324 MB |
| **E. nothing** — read what the agent did | nothing | `trajectories/` | 296 MB |

D is the one that makes these archives worth keeping: it asks whether a result
survives a different backbone, at the cost of one evaluation pass.

## The environments have been checked, one by one

Levels B–D need a live environment, and the risk there is silent: a task list
that no longer names the same tasks produces a run that completes and reports
numbers about something else. So each environment was started from this repo's
artefacts and its own task list replayed against it (2026-08-06):

| environment | how it was checked | result |
|---|---|---|
| **ALFWorld** | env server from `agentgym/`, the 8 knobs this experiment sets, 5 tasks reset | the observation text is **character-identical** to the archived `task_description` |
| **ScienceWorld** | env server on a compute node with `env/sciworld/scienceworld-v2.jar`, 8 tasks reset | family matched the task list **and** the archived rows, 8/8 |
| **WebShop** | env server from `agentgym/` with the frozen price table and the shipped index, 6 tasks reset | task type matched, 6/6 |
| **AppWorld** | its own package + task data (no server on this line), all ids checked, 5 instructions compared | **250/250 ids present**, instructions byte-identical 5/5 |

Independently, an agent restricted to this repo alone ran an evaluation end to
end on ALFWorld with a different backbone (DeepSeek) off a shipped memory
snapshot, and the rows it produced carry the same field set as the archived ones.

Commands and the exact output for each are in
[`../env/README.md`](../env/README.md).

### The whole pipeline was then run, on all four (2026-08-07)

Starting from the task lists rather than from a shipped memory — **rollout →
pool → compress → evaluate**, 4 training tasks and 3 held-out tasks per
environment, all sliced out of this repo's own lists with no overlap between the
two, DeepSeek throughout:

| environment | rollout | pool | ACE built | evaluated | vs. the archive on the same held-out tasks |
|---|---|---|---|---|---|
| ALFWorld | 4 | 4 | 16 bullets | 0/3 | those tasks run 41% across 144 archived rows |
| ScienceWorld | 4 | 4 | 15 bullets | 2/3 | 67% across 90 |
| WebShop | 4 | 4 | 12 bullets | 1/3 | 46% across 1,173 |
| AppWorld | 4 | 4 | 26 bullets | 2/3 (pass 95.8%) | 47%, pass 74.2%, across 620 |

A memory distilled from four episodes is not expected to match one distilled
from hundreds; what this shows is that **every stage runs, and each stage's
output is the shape the next stage and the archive expect**. The rows the fresh
evaluations wrote carry the archived field set exactly — the seven extra columns
in `per-task-results.jsonl` (`arm`, `archive_cell`, `method`, `variant`,
`checkpoint_n`, `condition`, `backbone`) are provenance labels added by
`import_from_archive.py`, not runner output. WebShop's fresh rows carry one
field the archived WebShop rows do not (`ruined`); it is a superset, and nothing
reads it.

The ACE playbooks are also recognisably about the right thing: the ALFWorld one
contains the recovery rule for `take X from sinkbasin` returning
`Nothing happens`, which is a failure its own four rollouts actually hit.

---

## A. Check the arithmetic

```bash
python results/verify_numbers.py
# reproduced 675 cells, 0 mismatched, 0 with no rows
```

Reads nothing outside the repo, and the test gate runs it. Any other cut is one
groupby away — see [`README.md`](README.md) for the columns.

⚠️ **Decide which denominator you are quoting.** Some rows are model refusals
rather than results (ScienceWorld 19% of them). `arms.csv` gives both `n_tasks`
(every row — what the published `numbers/*.csv` were computed on) and `n_valid`
(rows with an outcome). `verify_numbers.py` uses `n_valid`. Mixing the two is a
19% systematic error on ScienceWorld; README has the details. The ARC
directories have no refusal rows; their `arms.csv` carries `n_tasks` and
`n_rows` (task × sample attempts) instead.

## B. Re-run from the task lists

Before reading the scripts: the model parameters they pass, the memory methods'
own hyperparameters, and every modification we made to the environments and the
frameworks are collected in
[`../docs/settings-and-source-changes.md`](../docs/settings-and-source-changes.md).
Several of those values live in the vendored AgentGym source, and three of them
(A-MEM's upstream fix, Letta's harness-level cap, DC's locked curator budget)
change what the method *is*, not just how it is tuned.

`code/` holds the scripts as run, per stage:

| stage | what it does | entry points |
|---|---|---|
| rollout | run the tasks with no memory, write a pool | `run_rollout*.sh` |
| stream | order that pool — **for several of these lines the order IS the experiment** | `assemble_stream*.py`, `build_*_stream.py` |
| compress | feed the stream to each method, snapshot at each checkpoint | `build_memory*.sh`, `compress_*.sbatch` |
| evaluate | run the held-out tasks with each snapshot injected | `eval_*.sh`, `eval_*.sbatch` |

They are the scripts as run — Slurm, our paths — so treat them as a
specification, not a turnkey command. You also need the environment: see
[`env/README.md`](../env/README.md), which lists what ships here (the modified
ScienceWorld jar and its source; WebShop's frozen price table) and what you
fetch yourself (the ALFWorld and AppWorld datasets).

## C. Re-run the compression from our rollouts

`pools/` is PoolEntry JSONL — the same schema `bench`'s replay env reads:

```python
from bench.envs.replay import load_pool
entries = load_pool("results/alfworld_examine-rulebook-escape-hatch/pools/pool_n300.jsonl")
# 300 entries, each with taskDescription / trajectory / finalScore / success
```

481 of the 483 JSONL files here load this way; the two that do not are a trim
manifest and a retrieval log, which are not pools.

Feeding a pool to a memory method is the compress stage above. Note that some
arms' orderings are keyed on the **outcome** of an episode (whether it
succeeded, its final score), so they cannot be expressed as a task list at all —
those replay a recorded pool, which is what `bench`'s `replay` env is for.

## D. Re-run only the evaluation, off our memories

⚠️ **Use the AgentGym runner in `agentgym/`, not `bench`.** `bench`'s memory
rows all build a memory from scratch; none of them accepts a pre-built snapshot,
so there is currently no way to load these archives through `bench`. The runner
that does is `agentenv/scripts/memory/evaluate.py`, and this is verified working:

```bash
PYTHONPATH=agentgym/agentenv \
python agentgym/agentenv/scripts/memory/evaluate.py \
  --env alfworld \
  --stream results/alfworld_examine-rulebook-escape-hatch/tasks/eval_mix6_90.json \
  --method ace \
  --memory-file results/alfworld_examine-rulebook-escape-hatch/memory/intermediate_ace/step_300.txt \
  --agent-model deepseek-v4-flash \
  --agent-base-url https://api.deepseek.com/v1 \
  --agent-api-key "$(cat ~/.config/deepseek_key)" \
  --agent-extra-body '{"thinking":{"type":"disabled"}}' \
  --env-url http://127.0.0.1:36001 --max-rounds 30 --data-len 2620 --processes 5 \
  --save-path /tmp/repro_eval
```

**`--save-path` is required** — omit it and argparse exits before the runner
touches anything.

**`--agent-api-key` is not required, and that is worse.** It falls back to
`$OPENAI_API_KEY` and then to the literal `"EMPTY"`
(`evaluate.py`: `api_key = args.agent_api_key or os.environ.get("OPENAI_API_KEY")
or "EMPTY"`), so leaving it out starts the env server, resets the first task,
and only then fails with a 401 from the provider. Pass it explicitly.

The `--method` help string lists five methods; the registry has 24, including
every retrieval-based one. Do not read that list as a limit.

**If the snapshot you want is inside a pack**, unpack it first: `--memory-file`
takes a path on disk, and `memory/*.jsonl.gz` is a pack of many.

```python
import gzip, json, pathlib
want = "mem/ace_N100/mem.txt"                       # the `path` inside the pack
with gzip.open("results/webshop_retrieval-hijack/memory/gpt5.4mini.jsonl.gz", "rt") as f:
    for line in f:
        r = json.loads(line)
        if r["path"] == want:
            out = pathlib.Path("/tmp/ace_N100.txt")
            out.write_text(r.get("content") or json.dumps(r["json"]), encoding="utf-8")
            break
```

Binary snapshots (`.pkl`, what the retrieval-based methods load) are **not** in
the packs — they sit in `memory/` as real files and can be passed directly.

It writes `results.jsonl` with the **environment's** field set — the same one the
archived rows carry. It does **not** carry the seven provenance columns this
repo adds on import (`arm`, `archive_cell`, `method`, `variant`, `checkpoint_n`,
`condition`, `backbone`), so a fresh run is 18 fields against the archive's 25
and will not merge as-is: anything keyed on `arm` raises `KeyError`. Add those
columns yourself before concatenating.

`run_meta.json` records which snapshot was injected, under `memory_snapshot`.
**Check it** — a memory that silently renders empty is this project's most
expensive failure mode, and the run completes and reports numbers either way.

⚠️ **Do not grep for a fixed field name.** Each method names its own count:
`n_chars` for the text-rendering ones (ace, awm, dc), and something method-specific
for the retrieval ones — `n_entries`, `n_skills`, `n_rows`, `n_procedures`,
`n_rendered` all appear. Read whatever `memory_snapshot` contains and assert the
count is non-zero:

```python
snap = json.load(open("run_meta.json"))["memory_snapshot"]
counts = {k: v for k, v in snap.items() if k.startswith("n_") and isinstance(v, int)}
assert counts and max(counts.values()) > 0, f"memory rendered empty: {snap}"
```

The env server must be up first, with the experiment's knobs set — each
experiment's README has the exact table.

### AppWorld goes through its own driver

AppWorld never used the AgentGym runner, so `evaluate.py` does not apply to it.
Its driver is `code/appworld_stream_v2/proc_driver_v2.py`, one task per
invocation:

```bash
cd results/appworld_feed-order-same-pool/code/appworld_stream_v2
APPWORLD_ROOT=<your appworld root> \
BACKEND=openai_compat MODEL=deepseek-v4-flash \
LLM_URL=https://api.deepseek.com/v1/chat/completions \
LLM_KEY_FILE=~/.config/deepseek_key \
python proc_driver_v2.py <task_id> /tmp/out ace_N200 text:<snapshot.txt>
```

`prompt.json` and `attack_common.py` ship beside it. The `openai_compat` backend
was added so this runs without holding one of our Anthropic / OpenAI / GLM keys;
it sends `thinking: {"type": "disabled"}` by default, overridable with
`LLM_EXTRA_BODY`.

## E. Read what the agent did

`trajectories/` is every evaluated episode, turn by turn — **packed**, one gzipped
JSONL per arm, the same `{"path": ..., "json": ...}` pack shape as `memory/`:

```
trajectories/<arm>.jsonl.gz        ALFWorld, ScienceWorld, WebShop
```

There is no `conversations/` directory on disk; that is the `path` *inside* the
pack (`conversations/<task>.json`), which is what an earlier version of this page
gave as the file path — so looking for it literally finds nothing.

```python
import gzip, json
with gzip.open("results/alfworld_examine-rulebook-escape-hatch/"
               "trajectories/dc_n300.jsonl.gz", "rt") as f:
    for line in f:
        row = json.loads(line)                 # row["path"] = conversations/<task>.json
        ep = row["json"]                       # keys: conversation, final_score, idx, success
        for turn in ep["conversation"]:        # keys: role, content, reasoning_content
            print(turn["role"], turn["content"][:80])
        break
```

This is the level at which the mechanisms in `archive-SUMMARY.md` were found —
that a collapse was content churn rather than size growth, that a wrong-app
memory was retrieved and then ignored.

⚠️ **AppWorld has no transcripts.** Its runner wrote one `.rich.json` per task
holding the outcome only, so for AppWorld this level is not available; its
`trajectories/` holds those per-task records, and the turn-by-turn detail was
never written.

---

## The six experiments

| directory | environment | what was manipulated |
|---|---|---|
| `alfworld_examine-rulebook-escape-hatch` | ALFWorld | a rulebook the agent can `examine`, against unrecoverable wrong operations |
| `sciworld_cross-family-shortcut-contamination` | ScienceWorld | the density of shortcut wins in the training order, 19% → 71% |
| `webshop_retrieval-hijack` | WebShop | the payload memories are filed under vs retrieved under |
| `appworld_feed-order-same-pool` | AppWorld | the order one fixed pool is fed in |
| `arc_stream-self-eval` | ARC-AGI | ten passes over tasks the model had already solved with no memory |
| `arc_200task-stream` | ARC-AGI | batch size, memory mutability, and the backbone, on one 200-task stream |

Each README says what it did, the knob values, what the archive's shorthand
meant, and where it came from. Conclusions are in `archive-SUMMARY.md`, written
at the time — including the ones later retracted.

## Three things that will bite

- **Reasoning models are not deterministic at temperature 0.** The same pool
  rebuilt gives a materially different result (one method: 38 vs 19 at the same
  checkpoint). Trust within-build trends or a continuous resume chain; never
  anchor a new build's N450 against an archived N300.
- **Order is the experiment.** The stream files preserve order. A shuffle is a
  different experiment, not a reseed.
- **Pair each task list with the environment it was enumerated under.** On
  ScienceWorld `game_idx` means whatever the jar says; on WebShop the frozen
  price table must be set; on ALFWorld the knob preset must match. Mismatch any
  of these and the run completes and reports numbers that mean nothing.

## What this repo alone cannot give you

**Where the runnable parts come from:**

| | holds | how you get it |
|---|---|---|
| `agentgym/` | **all four env servers** and the memory implementations these numbers came from | vendored — it is in the clone. Provenance: [`../agentgym/VENDORED.md`](../agentgym/VENDORED.md) |
| `agentmem/` | the PropWorld kernel and the 13 memory methods `bench`'s `memory/*` rows wrap | vendored — it is in the clone. Provenance: [`../agentmem/VENDORED.md`](../agentmem/VENDORED.md) |

Levels **A, C and E** — check the arithmetic, load the pools, read the
transcripts — need neither, and are the levels most readers want.

What levels **B and D** additionally need is not code but *data*: each
environment's own dataset download and a provisioned server per environment, and
for anything past a replay, a paid model backbone. See
[`../env/README.md`](../env/README.md).

- **The memory implementations that produced these numbers** are the
  AgentGym-side ones vendored at `agentgym/` (`agentenv/memory/methods/*`). `bench`'s
  `memory/*` rows wrap a different codebase implementing the same method names.
  Do not treat a `bench` run as comparable — see
  [`../docs/agentgym_envs.md`](../docs/agentgym_envs.md).
- **A real backbone on `main`.** The OpenAI-compatible backends live on
  `backend/llms` and the memory rows on `memory/agentmem`; `main` ships only the
  `stub` backend. See the branch note in the top-level [`README.md`](../README.md).
- **Exact re-execution.** Non-deterministic backbones, hosted models that change
  under a fixed name, env servers provisioned per site. What is reproducible is
  the analysis; what is repeatable is the procedure.
