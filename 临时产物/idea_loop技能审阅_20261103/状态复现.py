"""仅复现状态工具行为；所有分数均为模拟输入，不是真实研究审查结果。"""
from pathlib import Path
import json
import re
import subprocess
import sys
import tempfile

sys.stdout.reconfigure(encoding="utf-8")
PROJECT = Path(__file__).resolve().parents[2]
SLOT = Path(__file__).resolve().parent
RUN = Path(tempfile.mkdtemp(prefix="复现_", dir=SLOT))
SKILL = PROJECT / "skills" / "idea-improvement-loop"
SCRIPT = SKILL / "tools" / "loop_state.py"
RESULTS = []
PASS = {
    "score": 8,
    "contribution_scores": {"importance": 8, "novelty": 8, "effectiveness": 6},
    "contribution_assessment": "模拟测试输入，不代表任何研究评价",
    "feasibility": "pass",
    "feasibility_reason": "模拟测试输入",
    "verdict": "experiment_ready",
    "fatal_blockers": [],
    "novelty_conclusion": "模拟输入",
    "closest_neighbors": [],
}


def run(root, *args):
    result = subprocess.run(
        [sys.executable, "-X", "utf8", str(SCRIPT), "--root", str(root), *args],
        cwd=root, capture_output=True, encoding="utf-8",
    )
    return {"exit_code": result.returncode, "output": result.stdout.strip(), "error": result.stderr.strip()}


def make_case(name, raw=None, cap=6):
    root = RUN / name
    idea = root / "idea-stage" / "demo"
    idea.mkdir(parents=True, exist_ok=True)
    if raw is None:
        raw = "# 模拟输入\n\n## Problem Anchor\n模拟任务与资源约束。\n"
    (idea / "RAW_IDEA.md").write_text(raw, encoding="utf-8")
    brief = idea / "草稿.md"
    brief.write_text("## 背景\n模拟问题\n## 核心 Claim\n机制 A\n## 方法设计的核心思想\n动作 A\n## 最小实验\n比较 A\n", encoding="utf-8")
    init = run(root, "init", "--slug", "demo", "--mode", "problem_card", "--max-calls", str(cap))
    assert init["exit_code"] == 0, init
    return root, brief


def start(root, brief):
    return run(root, "start-call", "--slug", "demo", "--candidate", "IDEA-001", "--self-score", "8", "--brief", str(brief), "--date", "2026-11-03")


def record_pass(root, n):
    path = root / "review-stage" / "demo" / f"round-{n:02d}-review.md"
    path.write_text("# 模拟审查，非研究结论\n\n" + json.dumps(PASS, ensure_ascii=False), encoding="utf-8")
    return run(root, "record", "--slug", "demo")


def state(root):
    return json.loads((root / "review-stage" / "demo" / "REVIEW_STATE.json").read_text(encoding="utf-8"))


reference = (SKILL / "references" / "problem-card-input.md").read_text(encoding="utf-8")
template = re.search(r"```markdown\n(.*?)```", reference, re.S).group(1)
root, brief = make_case("输入模板缺少锚点", raw=template)
RESULTS.append({"case": "直接使用问题卡输入模板", "actual": start(root, brief)})

root, brief = make_case("复核更换主张")
assert start(root, brief)["exit_code"] == 0
first = record_pass(root, 1)
assert json.loads(first["output"])["outcome"] == "first_pass"
changed = brief.with_name("更换主张.md")
changed.write_text(brief.read_text(encoding="utf-8").replace("机制 A", "完全不同的机制 B"), encoding="utf-8")
confirmation = run(root, "start-call", "--slug", "demo", "--role", "confirmation", "--effort", "xhigh", "--brief", str(changed), "--date", "2026-11-03")
assert confirmation["exit_code"] == 0, confirmation
second = record_pass(root, 2)
same = (root / "idea-stage/demo/round-01-brief.md").read_bytes() == (root / "idea-stage/demo/round-02-brief.md").read_bytes()
RESULTS.append({"case": "复核通过 --brief 更换主张", "briefs_equal": same, "actual": json.loads(second["output"])["outcome"]})
repeated = run(root, "record", "--slug", "demo")
RESULTS.append({"case": "同一复核结果重复 record", "first": json.loads(second["output"])["outcome"], "second": json.loads(repeated["output"])["outcome"]})

root, brief = make_case("预算耗尽后续跑", cap=1)
assert start(root, brief)["exit_code"] == 0
first = record_pass(root, 1)
assert json.loads(first["output"])["outcome"] == "first_pass_no_budget"
before = state(root)["pending_confirmation"]
assert run(root, "finish", "--slug", "demo", "--status", "blocked_max_reviewer_calls")["exit_code"] == 0
assert run(root, "extend", "--slug", "demo", "--add", "1", "--reason", "模拟用户追加一次复核预算")["exit_code"] == 0
RESULTS.append({"case": "最后一次首审通过、按说明 finish 后追加预算", "pending_before": before, "pending_after": state(root)["pending_confirmation"], "actual": run(root, "start-call", "--slug", "demo", "--role", "confirmation", "--effort", "xhigh")})

root, brief = make_case("旧状态续跑")
old = state(root)
old["round"] = 2
del old["reviewer_calls_used"]
del old["reviewer_calls"]
(root / "review-stage/demo/REVIEW_STATE.json").write_text(json.dumps(old, ensure_ascii=False), encoding="utf-8")
RESULTS.append({"case": "说明承诺支持的 round 旧状态", "actual": start(root, brief)})

copies = {
    "仓库主副本": SKILL,
    "仓库Codex副本": PROJECT / "skills" / "skills-codex" / "idea-improvement-loop",
    "Claude副本": PROJECT / ".claude" / "skills" / "idea-improvement-loop",
    "当前Codex安装副本": Path.home() / ".codex" / "skills" / "idea-improvement-loop",
}
comparison = {}
main_text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
for name, directory in copies.items():
    text = (directory / "SKILL.md").read_text(encoding="utf-8")
    comparison[name] = {
        "main_text_equal": text == main_text,
        "problem_card": "`problem_card`" in text,
        "confirmation_rule": "CONFIRMATION_REVIEW" in text,
        "loop_state_exists": (directory / "tools/loop_state.py").exists(),
    }
RESULTS.append({"case": "技能副本实际内容比较（直接比较，不使用哈希）", "copies": comparison})

output = json.dumps(RESULTS, ensure_ascii=False, indent=2)
(SLOT / "复现结果.json").write_text(output, encoding="utf-8")
print(output)
