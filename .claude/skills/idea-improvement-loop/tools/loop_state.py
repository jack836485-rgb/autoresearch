#!/usr/bin/env python3
"""管理 idea-improvement-loop 的审查调用计数、Reviewer 提示与 Gate 判定。

所有状态都在 review-stage/<slug>/REVIEW_STATE.json；路径相对于 --root（默认当前目录，即项目根）。

子命令:
  init        新建运行的状态与 AUTO_REVIEW.md
  start-call  检查预算 → 计数加一并写盘 → 复制 brief → 生成 Reviewer 提示文件 → 打印给 Reviewer 的启动消息
  record      解析审查文件末尾 JSON → 更新状态 → 追加 AUTO_REVIEW → 判定 Gate
  extend      用户追加审查预算
  finish      写终态（completed / blocked_max_reviewer_calls / rejected_no_viable_candidate）
  status      打印当前状态摘要

示例:
  python <skill>/tools/loop_state.py init --slug em_x --mode problem_card --max-calls 5 --source "path-stage/<map> Q008"
  python <skill>/tools/loop_state.py start-call --slug em_x --candidate IDEA-004 --self-score 6.9 --brief idea-stage/em_x/draft-brief.md --effort high
  python <skill>/tools/loop_state.py record --slug em_x
  python <skill>/tools/loop_state.py start-call --slug em_x --role confirmation --effort xhigh
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import shutil
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATE = SKILL_DIR / "templates" / "reviewer-prompt.md"
THRESHOLD = 8.0  # 与 SKILL.md 的 FINAL_REVIEW_THRESHOLD 保持一致


def paths(root: Path, slug: str) -> dict[str, Path]:
    idea, review = root / "idea-stage" / slug, root / "review-stage" / slug
    return {"idea": idea, "review": review, "state": review / "REVIEW_STATE.json", "log": review / "AUTO_REVIEW.md"}


def load(p: dict[str, Path]) -> dict:
    if not p["state"].exists():
        sys.exit(f"未找到状态文件 {p['state']}，请先运行 init")
    return json.loads(p["state"].read_text(encoding="utf-8"))


def save(p: dict[str, Path], state: dict) -> None:
    state["timestamp"] = dt.datetime.now().astimezone().isoformat(timespec="seconds")
    p["state"].write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def problem_anchor(idea_dir: Path) -> str:
    raw = (idea_dir / "RAW_IDEA.md").read_text(encoding="utf-8")
    match = re.search(r"^##+ [^\n]*Problem Anchor[^\n]*\n(.*?)(?=^## |\Z)", raw, re.S | re.M)
    if not match:
        sys.exit("RAW_IDEA.md 中没有 Problem Anchor 小节，请用 --anchor-file 指定")
    return match.group(1).strip()


def last_json(text: str) -> dict:
    decoder, found = json.JSONDecoder(), None
    for pos in (m.start() for m in re.finditer(r"\{", text)):
        try:
            obj, _ = decoder.raw_decode(text[pos:])
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict) and "score" in obj:
            found = obj
    if found is None:
        sys.exit("审查文件中没有可解析的 JSON（含 score 字段）；该次调用不能通过 Gate")
    return found


def cmd_init(a, p):
    if p["state"].exists():
        sys.exit(f"{p['state']} 已存在；续跑请用 status / extend")
    p["review"].mkdir(parents=True, exist_ok=True)
    p["idea"].mkdir(parents=True, exist_ok=True)
    state = {"slug": a.slug, "input_mode": a.mode, "source": a.source, "status": "in_progress",
             "reviewer_calls_used": 0, "max_reviewer_calls": a.max_calls, "selected_candidate_id": None,
             "selected_self_score": None, "selected_was_pool_leader": None, "pending_confirmation": None,
             "last_reviewer_score": None, "last_verdict": None, "novelty_conclusion": None, "fatal_blockers": [],
             "closest_neighbors": [], "last_brief_path": None, "last_review_path": None, "reviewer_calls": {}}
    save(p, state)
    p["log"].write_text("# 审查记录\n\n", encoding="utf-8")
    print(f"已初始化 {p['state']}")


def cmd_start(a, p, root):
    state = load(p)
    used, cap = state["reviewer_calls_used"], state["max_reviewer_calls"]
    if used >= cap:
        sys.exit(f"预算已用尽（{used}/{cap}），不能再启动 Reviewer；请写终态或由用户追加预算")
    pending = state.get("pending_confirmation")
    if a.role == "confirmation":
        if not pending and not a.force:
            sys.exit("没有待复核的首审通过结果；调试时可加 --force")
        brief_src = Path(a.brief) if a.brief else root / (pending["brief"] if pending else state["last_brief_path"])
        candidate = a.candidate or (pending or {}).get("candidate") or state["selected_candidate_id"]
    else:
        if not (a.brief and a.candidate and a.self_score is not None):
            sys.exit("常规审查需要 --candidate、--self-score 和 --brief")
        brief_src, candidate = Path(a.brief), a.candidate
        state.update(selected_candidate_id=candidate, selected_self_score=a.self_score, selected_was_pool_leader=True)

    n = used + 1
    brief = p["idea"] / f"round-{n:02d}-brief.md"
    review = p["review"] / f"round-{n:02d}-review.md"
    prompt = p["review"] / "prompts" / f"round-{n:02d}-review-prompt.md"
    if brief_src.resolve() != brief.resolve():
        shutil.copyfile(brief_src, brief)
    shutil.copyfile(brief, p["idea"] / "CURRENT_IDEA.md")
    anchor = Path(a.anchor_file).read_text(encoding="utf-8").strip() if a.anchor_file else problem_anchor(p["idea"])
    text = (TEMPLATE.read_text(encoding="utf-8")
            .replace("<<DATE>>", a.date).replace("<<WORKAROUNDS>>", a.workarounds)
            .replace("<<REVIEW_PATH>>", str(review.resolve()))
            .replace("<<BRIEF>>", brief.read_text(encoding="utf-8").strip()).replace("<<ANCHOR>>", anchor))
    prompt.parent.mkdir(parents=True, exist_ok=True)
    prompt.write_text(text, encoding="utf-8")

    call = {"candidate": candidate, "role": a.role, "effort": a.effort, "brief": str(brief.relative_to(root)),
            "prompt": str(prompt.relative_to(root)), "review": str(review.relative_to(root)), "score": None}
    if a.role == "confirmation" and not pending:
        call["note"] = "调试强制复核：没有首审通过结果，不能据此通过 Gate"
    state["reviewer_calls"][f"call_{n}"] = call
    state.update(reviewer_calls_used=n, last_brief_path=call["brief"], status="in_progress")
    save(p, state)  # 计数在启动 Reviewer 之前落盘
    print(json.dumps({"call": n, "role": a.role, "effort": a.effort, "brief": call["brief"], "prompt": call["prompt"],
                      "review": call["review"],
                      "launcher_message": f"Read the file {prompt.resolve()} with your file-reading tool and follow its instructions exactly."},
                     ensure_ascii=False, indent=2))


def cmd_record(a, p, root):
    state = load(p)
    n = a.call or state["reviewer_calls_used"]
    call = state["reviewer_calls"].get(f"call_{n}")
    if call is None:
        sys.exit(f"状态中没有 call_{n}")
    review = Path(a.review) if a.review else root / call["review"]
    result = last_json(review.read_text(encoding="utf-8"))
    score, blockers = float(result["score"]), result.get("fatal_blockers") or []
    call.update(score=score, verdict=result.get("verdict"))
    state.update(last_reviewer_score=score, last_verdict=result.get("verdict"), fatal_blockers=blockers,
                 novelty_conclusion=result.get("novelty_conclusion"),
                 closest_neighbors=result.get("closest_neighbors", []), last_review_path=str(review.relative_to(root)))

    passed = score > THRESHOLD and not blockers and state.get("selected_was_pool_leader")
    pending = state.get("pending_confirmation")
    if call["role"] == "regular":
        if passed:
            state["pending_confirmation"] = {"candidate": call["candidate"], "brief": call["brief"], "first_pass_call": n}
            outcome = "first_pass" if n < state["max_reviewer_calls"] else "first_pass_no_budget"
        else:
            state["pending_confirmation"], outcome = None, "failed"
    else:
        confirmed = passed and pending and pending["candidate"] == call["candidate"]
        outcome = "gate_passed" if confirmed else ("forced_confirmation_recorded" if call.get("note") else "confirmation_failed")
        state["pending_confirmation"] = None
    next_step = {"first_pass": "立即用同一份 brief 启动复核：start-call --role confirmation --effort xhigh",
                 "first_pass_no_budget": "预算不足以复核：finish --status blocked_max_reviewer_calls，并在 FINAL_REVIEW.md 注明首轮通过、未复核",
                 "gate_passed": "Gate 通过：候选标为 final，进入最终扩写",
                 "failed": "未通过：读审查引用的近邻，改进候选后重排",
                 "confirmation_failed": "复核未通过：候选标为 needs_revision，按普通失败处理",
                 "forced_confirmation_recorded": "调试复核已记录，不影响 Gate"}[outcome]
    if state["reviewer_calls_used"] >= state["max_reviewer_calls"] and outcome not in ("gate_passed", "first_pass_no_budget"):
        next_step += "；预算已用尽，写终态 finish --status blocked_max_reviewer_calls"
    save(p, state)
    role = "复核" if call["role"] == "confirmation" else "常规"
    with p["log"].open("a", encoding="utf-8") as log:
        log.write(f"- Call {n}（{role}，effort {call['effort']}）：{call['candidate']}，{score}/10，{result.get('verdict')}，"
                  f"Gate 结果 {outcome}。{(result.get('novelty_conclusion') or '')[:200]}\n")
    print(json.dumps({"call": n, "score": score, "verdict": result.get("verdict"), "fatal_blockers": blockers,
                      "outcome": outcome, "next_step": next_step}, ensure_ascii=False, indent=2))


def cmd_extend(a, p):
    state = load(p)
    state["max_reviewer_calls"] += a.add
    state.setdefault("budget_extensions", []).append({"add": a.add, "reason": a.reason})
    if state["status"].startswith("blocked"):
        state["status"] = "in_progress"
    save(p, state)
    print(f"预算现为 {state['reviewer_calls_used']}/{state['max_reviewer_calls']}")


def cmd_finish(a, p):
    state = load(p)
    state.update(status=a.status, pending_confirmation=None)
    save(p, state)
    print(f"状态已设为 {a.status}")


def cmd_status(a, p):
    state = load(p)
    keys = ("status", "reviewer_calls_used", "max_reviewer_calls", "selected_candidate_id", "pending_confirmation",
            "last_reviewer_score", "last_verdict")
    print(json.dumps({k: state.get(k) for k in keys}, ensure_ascii=False, indent=2))
    for name, call in state["reviewer_calls"].items():
        print(f"{name}: {call.get('candidate')} {call.get('role')} {call.get('effort')} score={call.get('score')}")


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", default=".", help="项目根目录（含 idea-stage/ 与 review-stage/）")
    sub = parser.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("init"); s.add_argument("--slug", required=True); s.add_argument("--mode", required=True,
        choices=["raw_idea", "baseline_paper", "problem_card"]); s.add_argument("--max-calls", type=int, default=5)
    s.add_argument("--source", default=None)
    s = sub.add_parser("start-call"); s.add_argument("--slug", required=True)
    s.add_argument("--role", choices=["regular", "confirmation"], default="regular")
    s.add_argument("--candidate"); s.add_argument("--self-score", type=float); s.add_argument("--brief")
    s.add_argument("--effort", default="high"); s.add_argument("--anchor-file")
    s.add_argument("--date", default=dt.date.today().isoformat()); s.add_argument("--workarounds", default="none")
    s.add_argument("--force", action="store_true", help="调试用：没有首审通过结果也启动复核")
    s = sub.add_parser("record"); s.add_argument("--slug", required=True); s.add_argument("--call", type=int)
    s.add_argument("--review")
    s = sub.add_parser("extend"); s.add_argument("--slug", required=True); s.add_argument("--add", type=int, required=True)
    s.add_argument("--reason", required=True)
    s = sub.add_parser("finish"); s.add_argument("--slug", required=True); s.add_argument("--status", required=True,
        choices=["completed", "blocked_max_reviewer_calls", "rejected_no_viable_candidate"])
    s = sub.add_parser("status"); s.add_argument("--slug", required=True)
    a = parser.parse_args()
    root = Path(a.root).resolve()
    p = paths(root, a.slug)
    {"init": lambda: cmd_init(a, p), "start-call": lambda: cmd_start(a, p, root), "record": lambda: cmd_record(a, p, root),
     "extend": lambda: cmd_extend(a, p), "finish": lambda: cmd_finish(a, p), "status": lambda: cmd_status(a, p)}[a.cmd]()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
