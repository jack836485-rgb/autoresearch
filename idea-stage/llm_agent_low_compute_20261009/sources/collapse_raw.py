"""Raw pool injection — no compression, inject N pool entries verbatim.

Aliases: "raw" (user's term), "rollout_pool" (SW/AppWorld original term).
Both names resolve to the same class.

`compress` is a no-op: the pool jsonl IS the memory artifact. `load` reads
the pool, `render` returns the rendered pool text under the `weakref`
framing ("REFERENCE ROLLOUT POOL — not curated learnings").

Optional: `exclude_self_task` drops pool entries whose `task_id` matches
the eval task (leakage control). Currently only applied if
`task_meta.task_id` is set and matches a pool entry exactly.
"""

from __future__ import annotations

import json
import random
from pathlib import Path
from typing import Optional

from ..base import BaseMemory, PoolEntry, TaskMeta
from ..pool import load_pool, render_pool, render_trajectory
from ..registry import register


def _fam_key(e: PoolEntry) -> str:
    """Family identity for stratified coverage — taskName is the family
    (e.g. 'param_break_stop_goto_win'); fall back to task_id."""
    return getattr(e, "taskName", None) or getattr(e, "task_id", None) or "?"


def _stratified_prune_to_chars(entries: list, budget_chars: int) -> list:
    """Keep the WHOLE pool (order preserved); only if the rendered pool exceeds
    `budget_chars`, prune one rollout at a time — always the LATEST rollout of
    the currently-largest family, and NEVER a family's last remaining one. So
    coverage (≥1 per family) is guaranteed and over-sampled families shed first.
    Renders the actual pool each step so the budget targets the injected size
    exactly (pools here are ≤ a few dozen rollouts → cheap)."""
    from collections import OrderedDict

    kept = list(entries)
    while len(render_pool(kept)) > budget_chars:
        groups: "OrderedDict[str, list]" = OrderedDict()
        for e in kept:
            groups.setdefault(_fam_key(e), []).append(e)
        droppable = [(f, es) for f, es in groups.items() if len(es) > 1]
        if not droppable:
            break  # every family down to its last one — can't prune without losing a family
        # largest family (ties: the one appearing later), drop its latest rollout
        _, es = max(droppable, key=lambda fe: len(fe[1]))
        kept.remove(es[-1])
    return kept


class _RawBase(BaseMemory):
    """Shared implementation; registered twice under "raw" and "rollout_pool"."""

    framing = "weakref"

    def __init__(self, entries: list[PoolEntry], *, exclude_self_task: bool = False):
        self._entries = entries
        self._exclude_self_task = exclude_self_task
        # Cache the full render once; per-task filter triggers re-render
        self._cached_full = render_pool(entries)

    @classmethod
    def compress(cls, pool, env_context, llm, out_path, **kwargs) -> None:
        # No-op compression: the pool jsonl IS the memory artifact. We just
        # write it to out_path so the downstream "compress writes out_path"
        # contract holds. Two mutually-exclusive downselect modes (both keep the
        # full verbatim trajectory of each surviving rollout):
        #  * sample_mode="stratified" (+ max_chars): keep the WHOLE pool, and only
        #    if the rendered pool exceeds max_chars, prune — dropping the latest
        #    rollout of the CURRENTLY-LARGEST family each step, NEVER a family's
        #    last one. So every family stays represented; over-sampled families
        # shed first ("full history, no random; if it won't fit,
        #    drop same-family extras, keep every family").
        #  * sample_n (+ sample_seed): the legacy UNIFORM random downsample to
        #    exactly N (order-preserving); preserves a magnet's frequency share
        #    in expectation. Used by the r25 offline arms (sample_n=16).
        out_path = Path(out_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        entries = list(pool)
        sample_mode = kwargs.get("sample_mode")
        sample_n = kwargs.get("sample_n")
        if sample_mode == "stratified":
            entries = _stratified_prune_to_chars(
                entries, int(kwargs.get("max_chars", 250_000)))
        elif sample_n is not None and 0 < int(sample_n) < len(entries):
            seed = int(kwargs.get("sample_seed", 0))
            order = {id(e): i for i, e in enumerate(entries)}
            entries = random.Random(seed).sample(entries, int(sample_n))
            entries.sort(key=lambda e: order[id(e)])
        with out_path.open("w") as f:
            for e in entries:
                f.write(json.dumps(e.to_dict(), ensure_ascii=False) + "\n")

    @classmethod
    def load(cls, memory_path: Optional[Path] = None) -> "_RawBase":
        if memory_path is None:
            raise ValueError(f"{cls.__name__} requires a pool jsonl path")
        return cls(load_pool(memory_path))

    def render(self, task_meta: TaskMeta) -> str:
        if not self._exclude_self_task or not task_meta.task_id:
            return self._cached_full
        return render_pool(self._entries, drop_task_ids={task_meta.task_id})

    def snapshot(self) -> dict:
        return {
            **super().snapshot(),
            "n_entries": len(self._entries),
            "exclude_self_task": self._exclude_self_task,
        }


@register("raw")
class Raw(_RawBase):
    """User-facing alias. Same class as RolloutPool."""


@register("rollout_pool")
class RolloutPool(_RawBase):
    """Original SW/AppWorld condition name. Kept for cross-experiment compatibility."""


# ---------------------------------------------------------------------------
# raw_nl — same "no-curation" weakref pool, but each rollout is replaced by a
# short natural-language SURFACE SUMMARY instead of the verbatim ReAct trace.
#
# Why: verbatim raw is ~6k tok/rollout (84% of it is per-step CoT), so a 25k
# tok memory budget holds only ~4 rollouts → can't cover 15 task families.
# A surface summary is ~150 tok, so the SAME budget holds ~150 rollouts →
# whole pool / all families fit. This is NOT a learning method: the summary
# prompt forbids lessons / causal rules / advice — it is a faithful per-
# rollout description, so raw_nl stays an honest "uncompressed-ish" control.
#
# Prompt ported from CLIN-on-ScienceWorld `summarize_rollout_surface`.
# ---------------------------------------------------------------------------

_SURFACE_SYSTEM = "You are an expert assistant."
_SURFACE_INSTRUCTION = (
    "Summarize the rollout below into a short, surface-level description.\n"
    "Do NOT infer lessons, causal rules, or advice.\n"
    "Do NOT output reasoning, chain-of-thought, analysis, or <think> blocks.\n"
    "Only describe the task, the main actions/observations, and the final outcome.\n"
    "Keep it under 6 sentences.\n\n"
    "Return your answer in exactly this template:\n"
    "<surface_summary>\n"
    "A concise surface-level summary here.\n"
    "</surface_summary>\n"
)

#: Default per-rollout trace cap fed to the summarizer (input side). Keeps the
#: summarization prompt bounded; the summary itself is far shorter.
_TRACE_INPUT_MAX_CHARS = 12000
#: Default render budget (output side): how many chars of summaries to pack
#: into the eval prompt. ~100k chars ≈ 25k tok ≈ ACE's injected footprint.
_DEFAULT_RENDER_BUDGET_CHARS = 100_000
_META_KEY = "__raw_nl_meta__"


def _extract_surface(text: str) -> str:
    """Pull the <surface_summary>…</surface_summary> body; fall back to the
    response with any <think> section stripped."""
    import re

    m = re.search(r"<surface_summary>(.*?)</surface_summary>", text, re.DOTALL | re.IGNORECASE)
    if m:
        return m.group(1).strip()
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL | re.IGNORECASE).strip()
    if "</think>" in text:
        text = text.split("</think>")[-1].strip()
    return text.strip()


def _summarize_entry(llm, entry: PoolEntry, *, trace_max_chars: int = _TRACE_INPUT_MAX_CHARS) -> str:
    """One LLM call → NL surface summary for a single rollout. Independent per
    rollout (no cross-trajectory state) → preserves the raw/no-curation
    contract."""
    # Action+observation skeleton only (drop the verbose per-step CoT — it is
    # 84% of the tokens and the summarizer doesn't need it to describe what
    # happened). Tail-capped to keep the summarizer input bounded.
    trace = render_trajectory(entry.trajectory, include_thought=False, max_chars=trace_max_chars)
    label = "PASS" if entry.success else (f"SCORE={entry.finalScore}")
    user = (
        f"Task: {entry.taskDescription or entry.taskName}\n"
        f"Final result: {label}\n\n"
        f"Rollout trace (Action/Observation):\n{trace}"
    )
    content, _ = llm.generate(
        [
            {"role": "system", "content": _SURFACE_SYSTEM},
            {"role": "user", "content": _SURFACE_INSTRUCTION},
            {"role": "user", "content": user},
        ]
    )
    return _extract_surface(content or "")


def _render_summary_block(row: dict, idx: int, *, score_style: str) -> str:
    if score_style == "binary":
        label = "PASS" if row.get("success") else "FAIL"
    else:
        label = f"SCORE={row.get('finalScore', 0)}"
    banner = (
        f"[ROLLOUT ID {idx}] task_id={row.get('task_id')} | "
        f"task={row.get('taskName') or '?'} | result={label}"
    )
    parts = [banner]
    if row.get("taskDescription"):
        parts.append(f"Task: {row['taskDescription']}")
    parts.append(f"SURFACE SUMMARY:\n{row.get('surface_summary', '').strip()}")
    return "\n".join(parts)


def _render_summary_pool(
    rows: list[dict],
    *,
    budget_chars: int,
    drop_task_ids: Optional[set[str]] = None,
) -> tuple[str, int]:
    """Greedily pack summary rows (in stored order) until `budget_chars` is
    reached. Returns (rendered_text, n_packed)."""
    drop = drop_task_ids or set()
    all_binary = all(int(r.get("finalScore", 0)) in (0, 100) for r in rows)
    score_style = "binary" if all_binary else "score"
    blocks: list[str] = []
    used = 0
    n = 0
    for r in rows:
        if r.get("task_id") in drop:
            continue
        block = _render_summary_block(r, n + 1, score_style=score_style)
        if used + len(block) > budget_chars and n > 0:
            break
        blocks.append(block)
        used += len(block) + 2  # +2 for the "\n\n" join
        n += 1
    return "\n\n".join(blocks), n


@register("raw_nl")
class RawNL(BaseMemory):
    """Raw pool rendered as NL surface summaries (no lessons / no CoT).

    Artifact (`memory-out`) is a JSONL whose first line is a meta header
    ``{"__raw_nl_meta__": {"render_budget_chars": N}}`` followed by one
    summary row per rollout::

        {"task_id","taskName","taskDescription","finalScore","success","surface_summary"}

    The budget is baked into the artifact so eval-time `render` needs no config.
    """

    framing = "weakref"

    def __init__(self, rows: list[dict], *, render_budget_chars: int, exclude_self_task: bool = False,
                 render_sample_n: Optional[int] = None, sample_seed: int = 0):
        # Optional uniform, order-preserving downselect to exactly N summaries
        # (same semantics as raw's sample_n: preserves family/régime/magnet
        # share in expectation). Char budget still applies as a safety cap.
        if render_sample_n is not None and 0 < int(render_sample_n) < len(rows):
            order = {id(r): i for i, r in enumerate(rows)}
            rows = random.Random(int(sample_seed)).sample(rows, int(render_sample_n))
            rows.sort(key=lambda r: order[id(r)])
        self._rows = rows
        self._budget = int(render_budget_chars)
        self._exclude_self_task = exclude_self_task
        self._cached_full, self._n_full = _render_summary_pool(rows, budget_chars=self._budget)

    @classmethod
    def compress(cls, pool, env_context, llm, out_path, *, gold_pool=None, **kwargs) -> None:
        if llm is None:
            raise ValueError("raw_nl.compress requires an LLM (pass --llm-model); it summarizes each rollout.")
        out_path = Path(out_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        entries = list(pool)

        # Optional deterministic pre-cap to bound the number of LLM calls.
        sample_n = kwargs.get("sample_n")
        if sample_n is not None and 0 < int(sample_n) < len(entries):
            seed = int(kwargs.get("sample_seed", 0))
            order = {id(e): i for i, e in enumerate(entries)}
            entries = random.Random(seed).sample(entries, int(sample_n))
            entries.sort(key=lambda e: order[id(e)])

        budget = int(kwargs.get("render_budget_chars", _DEFAULT_RENDER_BUDGET_CHARS))
        trace_max = int(kwargs.get("trace_input_max_chars", _TRACE_INPUT_MAX_CHARS))
        summary_max = kwargs.get("summary_max_chars")

        rows: list[dict] = []
        for i, e in enumerate(entries):
            s = _summarize_entry(llm, e, trace_max_chars=trace_max)
            if summary_max and len(s) > int(summary_max):
                s = s[: int(summary_max)].rstrip() + "…"
            rows.append({
                "task_id": e.task_id, "taskName": e.taskName,
                "taskDescription": e.taskDescription, "finalScore": e.finalScore,
                "success": e.success, "surface_summary": s,
            })
            if (i + 1) % 25 == 0:
                print(f"[raw_nl] summarized {i + 1}/{len(entries)}", flush=True)

        exclude_self = bool(kwargs.get("exclude_self_task", False))
        with out_path.open("w") as f:
            meta = {"render_budget_chars": budget, "exclude_self_task": exclude_self}
            if kwargs.get("render_sample_n") is not None:
                meta["render_sample_n"] = int(kwargs["render_sample_n"])
                meta["sample_seed"] = int(kwargs.get("sample_seed", 0))
            f.write(json.dumps({_META_KEY: meta}, ensure_ascii=False) + "\n")
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")

        # Report capacity at the chosen budget plus a small sweep, so the caller
        # immediately sees "how many rollouts fit".
        _, n_fit = _render_summary_pool(rows, budget_chars=budget)
        lens = sorted(len(r["surface_summary"]) for r in rows)
        p50 = lens[len(lens) // 2] if lens else 0
        print(f"[raw_nl] {len(rows)} rollouts summarized | summary chars p50={p50} (~{p50 // 4} tok)", flush=True)
        print(f"[raw_nl] FIT @ budget={budget} chars (~{budget // 4} tok): {n_fit}/{len(rows)} rollouts", flush=True)
        for b in (60_000, 100_000, 140_000, 200_000):
            _, nb = _render_summary_pool(rows, budget_chars=b)
            print(f"[raw_nl]   sweep budget={b:>7} chars (~{b // 4:>5} tok): {nb}/{len(rows)} fit", flush=True)

    @classmethod
    def load(cls, memory_path: Optional[Path] = None) -> "RawNL":
        if memory_path is None:
            raise ValueError("RawNL requires a summaries jsonl path")
        rows: list[dict] = []
        budget = _DEFAULT_RENDER_BUDGET_CHARS
        exclude_self = False
        sample_n = None
        seed = 0
        with Path(memory_path).open() as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                obj = json.loads(line)
                if _META_KEY in obj:
                    meta = obj[_META_KEY]
                    budget = int(meta.get("render_budget_chars", budget))
                    exclude_self = bool(meta.get("exclude_self_task", False))
                    if meta.get("render_sample_n") is not None:
                        sample_n = int(meta["render_sample_n"])
                        seed = int(meta.get("sample_seed", 0))
                    continue
                rows.append(obj)
        return cls(rows, render_budget_chars=budget, exclude_self_task=exclude_self,
                   render_sample_n=sample_n, sample_seed=seed)

    def render(self, task_meta: TaskMeta) -> str:
        if not self._exclude_self_task or not task_meta.task_id:
            return self._cached_full
        text, _ = _render_summary_pool(
            self._rows, budget_chars=self._budget, drop_task_ids={task_meta.task_id}
        )
        return text

    def snapshot(self) -> dict:
        return {**super().snapshot(), "n_rows": len(self._rows),
                "n_rendered": self._n_full, "render_budget_chars": self._budget}
