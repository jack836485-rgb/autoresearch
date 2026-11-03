"""保存本次三个独立审查的提示、原始响应与上下文隔离元数据。"""
from pathlib import Path
import argparse
import datetime as dt
import json
import shutil

ROOT = Path(__file__).resolve().parents[2]
REVIEW = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument("--call", type=int, required=True)
parser.add_argument("--agent", required=True)
parser.add_argument("--effort", default="high")
args = parser.parse_args()
now = dt.datetime.now(dt.timezone(dt.timedelta(hours=8))).isoformat(timespec="seconds")
trace_pointer = REVIEW / "追踪位置.json"
if trace_pointer.exists():
    trace = ROOT / json.loads(trace_pointer.read_text(encoding="utf-8"))["trace_path"]
else:
    parent = ROOT / ".aris/traces/idea-improvement-loop"
    run_n = 1
    while (parent / f"2026-11-03_run{run_n:02d}").exists():
        run_n += 1
    trace = parent / f"2026-11-03_run{run_n:02d}"
    trace.mkdir(parents=True)
    trace_pointer.write_text(json.dumps({"trace_path": str(trace.relative_to(ROOT))}, ensure_ascii=False, indent=2), encoding="utf-8")
    (trace / "run.meta.json").write_text(json.dumps({
        "skill": "idea-improvement-loop", "run_id": trace.name,
        "recorded_at": now, "executor": "codex", "project_dir": str(ROOT),
        "slot": REVIEW.name, "reviewer_budget": 3,
    }, ensure_ascii=False, indent=2), encoding="utf-8")

state = json.loads((REVIEW / "REVIEW_STATE.json").read_text(encoding="utf-8"))
call = state["reviewer_calls"][f"call_{args.call}"]
prompt_path, response_path = ROOT / call["prompt"], ROOT / call["review"]
prefix = f"{args.call:03d}-round-{args.call}-review"
request = {
    "call_number": args.call, "purpose": f"round-{args.call}-review", "recorded_at": now,
    "tool": "collaboration.spawn_agent", "model": "inherited_executor_model",
    "model_identifier_available": False, "config": {"model_reasoning_effort": args.effort},
    "role": call["role"], "context_policy": "fresh_zero_context", "fork_turns": "none",
    "continuation_allowed": False, "files_referenced": [str(prompt_path)],
    "launcher_message": f"Read the file {prompt_path} with your file-reading tool and follow its instructions exactly.",
    "prompt": prompt_path.read_text(encoding="utf-8"),
}
(trace / f"{prefix}.request.json").write_text(json.dumps(request, ensure_ascii=False, indent=2), encoding="utf-8")
shutil.copyfile(response_path, trace / f"{prefix}.response.md")
(trace / f"{prefix}.meta.json").write_text(json.dumps({
    "call_number": args.call, "recorded_at": now, "agent_id": args.agent,
    "model": "inherited_executor_model", "effort": args.effort, "status": "ok",
    "outcome": call.get("outcome"), "score": call.get("score"),
    "context_policy": "fresh_zero_context", "continuation_allowed": False,
}, ensure_ascii=False, indent=2), encoding="utf-8")
events = ROOT / ".aris/meta/events.jsonl"
events.parent.mkdir(parents=True, exist_ok=True)
with events.open("a", encoding="utf-8") as out:
    out.write(json.dumps({"ts": now, "event": "review_trace", "skill": "idea-improvement-loop",
                          "purpose": f"round-{args.call}-review", "thread_id": args.agent,
                          "trace_path": str(trace.relative_to(ROOT)), "status": "ok"}, ensure_ascii=False) + "\n")
print(str(trace))
