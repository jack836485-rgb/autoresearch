"""核对实际审查、终态、原卡回写和未复审候选的边界。"""
from pathlib import Path
import importlib.util
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.dont_write_bytecode = True
REVIEW = Path(__file__).resolve().parent
ROOT = REVIEW.parents[1]
IDEA = ROOT / "idea-stage" / REVIEW.name
state = json.loads((REVIEW / "REVIEW_STATE.json").read_text(encoding="utf-8"))
assert state["reviewer_calls_used"] == state["max_reviewer_calls"] == 3
assert len(state["reviewer_calls"]) == 3
assert state["status"] == "blocked_max_reviewer_calls" and state["gate_passed"] is False
assert state["pending_confirmation"] is None
assert [c["candidate"] for c in state["reviewer_calls"].values()] == ["IDEA-002", "IDEA-005", "IDEA-006"]
assert all(c["role"] == "regular" and c["outcome"] == "failed" for c in state["reviewer_calls"].values())
spec = importlib.util.spec_from_file_location("loop_state", ROOT / "skills/idea-improvement-loop/tools/loop_state.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
scores = []
for n in range(1, 4):
    call = state["reviewer_calls"][f"call_{n}"]
    result = module.last_json((ROOT / call["review"]).read_text(encoding="utf-8"))
    assert result["score"] == call["score"]
    assert result["contribution_scores"] == call["contribution_scores"]
    assert not module.review_qualifies(result)
    scores.append(result["score"])
assert scores == [6.5, 6.8, 7.5]
assert not (IDEA / "FINAL_IDEA.md").exists() and not (IDEA / "EXPERIMENT_HANDOFF.md").exists()
assert (IDEA / "补齐强对照后的候选.md").exists()
assert (IDEA / "CURRENT_IDEA.md").read_bytes() == (IDEA / "round-03-brief.md").read_bytes()
data = json.loads((ROOT / "path-stage/LLM热门方向_刷新_20261101/研究问题.json").read_text(encoding="utf-8"))
card = next(c for c in data["研究问题"] if c["id"] == "L-Q009")
record = card["三轮实际打磨_20261103"]
assert record["独立审查调用"] == 3 and record["首审通过"] == record["复核调用"] == 0
assert record["评分轨迹"] == scores
output = json.dumps({
    "状态": state["status"], "独立实际调用": 3, "首审通过": 0, "复核": 0,
    "评分": scores, "原卡JSON及记录": "通过", "未审版本未冒充正式Final": "通过",
    "CURRENT_IDEA": "最后实际送审版本IDEA-006", "保留候选": "IDEA-008，未复审",
}, ensure_ascii=False, indent=2)
(REVIEW / "收尾核对结果.json").write_text(output, encoding="utf-8")
print(output)
