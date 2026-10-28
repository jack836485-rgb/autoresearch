#!/usr/bin/env python3
"""本 skill 独立的 slot 状态工具：来源冻结、候选历史、审查预算、Gate 和总控结果。

只处理文件和机械约束；文献、创新性、价值、目标关联及复现判断仍由执行器/Reviewer负责。
所有写入限定于传入 slot，不调用模型、搜索或旧 skill。
"""
import argparse
import json
import math
import re
import sys
from pathlib import Path

MIN_PROBLEM_REVIEWS = 10
VERDICTS = {"experiment_ready", "promising_needs_revision", "needs_rethink", "reject"}
TERMINAL = {"experiment_ready", "blocked_max_rounds", "no_viable_candidate", "blocked_input",
            "blocked_review_unavailable", "blocked_finalization"}
EDITABLE_STATUS = {"needs_revision", "covered", "baseline_patch", "rejected", "needs_evidence"}
HEADINGS = ["背景", "核心 Claim", "方法设计的核心思想", "最小实验"]
REQUIRED_TEXT = ["title", "background", "claim", "method", "minimal_experiment", "story_line",
                 "lightweight_novelty", "independent_contribution", "score_reason", "goal_difference",
                 "constraints_alignment", "pre_solution_idea_relation"]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def inside(root, path):
    path = Path(path).resolve()
    require(path.is_relative_to(root), f"运行文件必须在 slot 内：{path}")
    return path


def state_file(root):
    return root / "json/REVIEW_STATE.json"


def score(value):
    require(isinstance(value, (int, float)) and not isinstance(value, bool)
            and math.isfinite(value) and 1 <= value <= 10, "score 必须是 1–10 的有限数字")
    require(abs(value * 10 - round(value * 10)) < 1e-8, "score 最多一位小数")
    return float(value)


def eligible(c):
    return c["status"] == "available" and c["self_score"] > 7 and not c["eligibility_blockers"]


def required_problems(s):
    return s["input"].get("review_problem_ids", [p["problem_id"] for p in s["input"]["problems"]])


def problem_review_counts(s):
    counts = dict.fromkeys(required_problems(s), 0)
    for call in s["calls"]:
        goal = (call.get("review") or {}).get("goal_assessment", {})
        if not (call.get("valid") and call.get("agent_id")
                and call.get("fork_turns") == "none"
                and call.get("context_policy") == "fresh_zero_context"
                and goal.get("within_initial_scope") and goal.get("hard_constraints_satisfied")):
            continue
        for pid in set(call.get("reviewed_problem_ids", [])) & counts.keys():
            counts[pid] += 1
    return counts


def budget_met(s):
    return all(n >= s["review_budget"][pid] for pid, n in problem_review_counts(s).items())


def candidate_problems(s, c):
    drawbacks = {d["id"]: d for d in s["input"]["drawbacks"]}
    for candidate in s["candidates"].values():
        drawbacks.update({d["id"]: d for d in candidate["newly_identified_drawbacks"]})
    return sorted({pid for did in c["addressed_drawback_ids"]
                   for pid in drawbacks[did].get("problem_ids", [])} & set(required_problems(s)))


def best_passing(s):
    pool = [c for c in s["candidates"].values() if c["status"] == "review_passed"]
    return max(pool, key=lambda c: c["self_score"])["id"] if pool else None


def render_raw_idea(task):
    """初始输入只写一份简明可读记录，完整机器输入留在json状态。"""
    parts = ["# 最初交给 Improver 的研究输入", "", f"- 路由：{task['problem_id']}",
             "- 初始不足不要求全部解决；明确的用户硬约束保持有效。", "", "## 初始 Problems", ""]
    for p in task["problems"]:
        parts += [f"**{p['problem_id']}：** {p['problem']}", ""]
    parts += ["## 初始 drawbacks", ""]
    for d in task["drawbacks"]:
        parts += [f"**{d['id']}：** {d['description']}",
                  f"- 关联问题：{', '.join(d.get('problem_ids', []))}"]
        links = [e.get("原文链接", e.get("url")) for e in d.get("evidence", []) if isinstance(e, dict)]
        for url in dict.fromkeys(x for x in links if x):
            parts += [f"- 原始证据：{url}"]
        parts += [""]
    parts += ["## 初始假设（可放弃）", ""]
    seed = task.get("pre_solution_idea")
    if isinstance(seed, dict):
        for k, v in seed.items():
            if k != "evidence":
                parts += [f"- {k}：{v}"]
    else:
        parts += [str(seed) if seed is not None else "未提供预解决思路，开放探索。"]
    parts += ["", "## 用户约束", ""]
    constraints = task.get("constraints", {})
    if isinstance(constraints, dict):
        for k, v in constraints.items():
            parts += [f"**{k}：**"]
            parts += [f"- {x}" for x in v] if isinstance(v, list) else [str(v)]
    else:
        parts += [str(constraints)]
    context = task.get("problem_map_context", {})
    if isinstance(context, dict):
        parts += ["", "## 初始探索目标", "", str(context.get("exploration_goal", "按上述问题独立判断。"))]
        for path in context.get("source_paths", []):
            parts += [f"- 只读地图来源：{path}"]
    return "\n".join(parts) + "\n"


def get_candidate(s, cid):
    require(cid in s["candidates"], f"未知候选：{cid}")
    return s["candidates"][cid]


def render_pool(s):
    """人类视图仅展示研究内容；不足ID解析为完整描述，内部记录留在JSON。"""
    parts = ["# Idea 候选池", ""]
    drawbacks = {d["id"]: d for d in s["input"]["drawbacks"]}
    for c in s["candidates"].values():
        drawbacks.update({d["id"]: d for d in c["newly_identified_drawbacks"]})
    labels = {"background": "背景", "claim": "核心 Claim", "method": "方法",
              "minimal_experiment": "最小实验", "story_line": "Storyline"}
    for cid, c in s["candidates"].items():
        parts += [f"## {cid}：{c['title']}", "", "**处理的不足：**", ""]
        for did in c["addressed_drawback_ids"]:
            require(did in drawbacks and isinstance(drawbacks[did].get("description"), str)
                    and drawbacks[did]["description"].strip(), f"不足{did}缺少完整描述，不能只展示编号")
            parts += [f"- {drawbacks[did]['description']}"]
        parts += [""]
        for key, label in labels.items():
            parts += [f"**{label}：**", "", c[key], ""]
    return "\n".join(parts) + "\n"


def save(root, s):
    human_view = render_pool(s)
    write_json(state_file(root), s)
    (root / "IDEA_CANDIDATES.md").write_text(human_view, encoding="utf-8")


def load(root):
    s = read_json(state_file(root))
    require(s["slot_path"] == str(root), "状态的 slot_path 与当前目录不同")
    require((root / "RAW_IDEA.md").read_text(encoding="utf-8") == s["frozen_anchor"],
            "初始来源记录被修改；恢复原记录，目标变化应放在候选中")
    return s


def active_run(s):
    require(s["status"] not in TERMINAL, "slot 已结束；不得重置历史重新运行")


def initialize(input_path):
    original = read_json(input_path)
    root = Path(original["slot_path"]).resolve()
    require(root.is_dir(), "slot_path 应由总控提前创建")
    if state_file(root).exists():
        s = load(root)
        require(s["original_input"] == original, "恢复输入与初始来源不同，不能覆盖")
        return {"status": s["status"], "reviewer_calls_used": s["reviewer_calls_used"], "resumed": True}
    for name in ["RAW_IDEA.md", "IDEA_CANDIDATES.md", "FINAL IDEA.md", "json/SLOT_RESULT.json"]:
        require(not (root / name).exists(), f"新初始化不得覆盖已有 {name}")
    require(isinstance(original.get("problem_id"), str) and original["problem_id"].strip(), "缺少 problem_id 路由标识")
    normalized = json.loads(json.dumps(original))
    problems = normalized.get("problems")
    if problems is None:
        problems = [{"problem_id": original["problem_id"], "problem": original.get("problem")}]
    require(isinstance(problems, list) and problems, "problems 必须含至少一个问题")
    for p in problems:
        require(isinstance(p, dict) and p.get("problem_id") and p.get("problem"), "每个 Problem 必须有标识和内容")
    pids = [p["problem_id"] for p in problems]
    require(len(set(pids)) == len(pids), "Problem ID 重复")
    targets = normalized.setdefault("review_problem_ids", pids)
    require(isinstance(targets, list) and targets and len(set(targets)) == len(targets)
            and set(targets) <= set(pids), "review_problem_ids须为非空、无重复的初始Problem子集")
    ds = normalized.get("drawbacks")
    require(isinstance(ds, list) and ds, "drawbacks 必须非空")
    ds = [{"id": f"D{i:03d}", "description": d, "problem_ids": pids, "evidence": []}
          if isinstance(d, str) else d for i, d in enumerate(ds, 1)]
    for d in ds:
        require(isinstance(d, dict) and d.get("id") and d.get("description"), "每个 drawback 须有ID和描述")
        require(set(d.get("problem_ids", pids)) <= set(pids), "drawback 引用了未知初始 Problem")
    require(len({d["id"] for d in ds}) == len(ds), "drawback ID 重复")
    require("constraints" in original and "problem_map_context" in original, "需提供 constraints 和 problem_map_context，可为空")
    normalized["problems"], normalized["drawbacks"], normalized["slot_path"] = problems, ds, str(root)
    normalized.setdefault("pre_solution_idea", None)
    anchor = render_raw_idea(normalized)
    (root / "json").mkdir(exist_ok=True)
    (root / "RAW_IDEA.md").write_text(anchor, encoding="utf-8")
    s = {"slot_path": str(root), "original_input": original, "input": normalized, "frozen_anchor": anchor,
         "status": "in_progress", "reviewer_calls_used": 0,
         "minimum_reviews_per_problem": MIN_PROBLEM_REVIEWS,
         "max_rounds": MIN_PROBLEM_REVIEWS * len(targets),
         "review_budget": dict.fromkeys(targets, MIN_PROBLEM_REVIEWS), "budget_history": [],
         "candidates": {}, "route_attempts": [], "discovery_notes": [], "calls": [], "active_call": None,
         "selection": None, "passing_candidate_id": None}
    save(root, s)
    return {"status": "in_progress", "slot_path": str(root), "resumed": False}


def register(root, s, path):
    require(s["active_call"] is None, "先结束当前审查")
    c = read_json(inside(root, path))
    require(re.fullmatch(r"IDEA-\d{3,}", c.get("id", "")), "候选ID需为 IDEA-NNN")
    require(c["id"] not in s["candidates"], "旧候选不可覆盖，实质改动使用新ID")
    for key in REQUIRED_TEXT:
        require(isinstance(c.get(key), str) and c[key].strip(), f"缺少候选内容：{key}")
    require(not any(all(c[k] == old[k] for k in ["claim", "method", "minimal_experiment"])
                    for old in s["candidates"].values()), "仅换ID/标题不构成新版本；须有实质候选或改进")
    for key in ["initial_drawback_ids", "addressed_drawback_ids", "newly_identified_drawbacks", "goal_evidence",
                "sources", "baseline_feasibility", "keywords", "eligibility_blockers"]:
        require(isinstance(c.get(key), list), f"{key} 应为数组")
    require(len(c["keywords"]) >= 3, "至少三个既有定位关键词")
    require(c["route"] in {"route1", "route2", "route3", "pre_solution"}, "未知路线")
    if c["route"] == "route3":
        require({a["route"] for a in s["route_attempts"]} >= {"route1", "route2"}, "先实际尝试前两路线")
        require(not any(eligible(x) and x["route"] in {"route1", "route2"} for x in s["candidates"].values()),
                "已有前两路线的 >7 合格候选，不能进入 Route 3")
    if c.get("parent_candidate_id"):
        get_candidate(s, c["parent_candidate_id"])
    c["self_score"] = score(c["self_score"])
    initial = {d["id"] for d in s["input"]["drawbacks"]}
    require(set(c["initial_drawback_ids"]) <= initial, "对应初始不足包含未知ID")
    known = {d["id"]: d for x in s["candidates"].values() for d in x["newly_identified_drawbacks"]}
    for d in c["newly_identified_drawbacks"]:
        require(isinstance(d, dict) and d.get("id") and d.get("description") and d.get("evidence"), "新不足需标识、描述及证据")
        require(d.get("problem_ids") and set(d["problem_ids"]) <= {p["problem_id"] for p in s["input"]["problems"]},
                "新不足须关联初始Problem，才能正确计入研究轮次")
        require(d["id"] not in initial, "新不足不能覆盖初始不足")
        require(d["id"] not in known or known[d["id"]] == d, "同一新不足ID不能改写来源")
        known[d["id"]] = d
    require(c["addressed_drawback_ids"] and set(c["addressed_drawback_ids"]) <= initial | set(known), "实际目标需指向初始或已登记新不足")
    require(isinstance(c.get("pre_solution_idea_used"), bool), "pre_solution_idea_used 应为布尔")
    require(not c["pre_solution_idea_used"] or bool(s["input"]["pre_solution_idea"]), "未收到初始假设不能声称沿用")
    require(c["route"] != "pre_solution" or bool(s["input"]["pre_solution_idea"]), "未收到初始假设不能使用该来源路线")
    c.setdefault("status", "available")
    require(c["status"] in {"available", "low_self_score"} | EDITABLE_STATUS, "新候选状态不合法")
    if c["status"] == "available":
        require(c["self_score"] > 7 and not c["eligibility_blockers"], "available 须自评分>7且无选择阻断")
        require(c["goal_evidence"] and c["sources"] and c["baseline_feasibility"], "available 须有目标证据、原文及基线复现依据")
    c["review_history"], c["decisions"] = [], []
    s["candidates"][c["id"]] = c
    save(root, s)
    return {"candidate_id": c["id"], "status": c["status"]}


def prepare(root, s, cid, brief_path, reason):
    require(s["active_call"] is None, "当前已有准备或审查")
    counts = problem_review_counts(s)
    unfinished = {pid for pid, n in counts.items() if n < s["review_budget"][pid]}
    require(unfinished, "每个Problem均已完成当前预算；由Brain判断是否加预算或结束")
    pool = [c for c in s["candidates"].values()
            if set(candidate_problems(s, c)) & unfinished
            and c["status"] not in {"covered", "baseline_patch", "rejected", "review_passed", "final"}
            and not any(r.get("valid") for r in c["review_history"])]
    qualified = [c for c in pool if eligible(c)]
    pool = qualified or pool
    require(pool, "未完成当前预算且没有新候选；继续检索并形成实质改进，不得研究早停")
    c = get_candidate(s, cid)
    require(c in pool and c["self_score"] == max(x["self_score"] for x in pool),
            "先选未满十轮的Problem，再审其最高分合格候选；无合格者时审最高分待改进候选")
    require(reason.strip(), "记录选择依据，同分时说明直接判断")
    brief = inside(root, brief_path).read_text(encoding="utf-8-sig")
    require(re.findall(r"^## (.+)$", brief, re.M) == HEADINGS, "Brief 仅包含规定四节")
    require(not re.search(r"IDEA-\d{3,}|自评分|候选池|审查历史", brief), "Brief 泄露候选或历史信息")
    n = s["reviewer_calls_used"] + 1
    brief_target = root / f"round-{n:02d}-brief.md"
    brief_target.write_text(brief, encoding="utf-8")
    (root / "CURRENT_IDEA.md").write_text(brief, encoding="utf-8")
    initial = {k: s["input"][k] for k in ["problems", "drawbacks", "constraints"]}
    initial["reviewed_problem_ids"] = candidate_problems(s, c)
    template = (Path(__file__).resolve().parents[1] / "templates/reviewer-prompt.md").read_text(encoding="utf-8")
    prompt = template.replace("{{INITIAL_SCOPE}}", json.dumps(initial, ensure_ascii=False, indent=2)).replace("{{BRIEF}}", brief)
    (root / "prompt").mkdir(exist_ok=True)
    prompt_path = root / f"prompt/round-{n:02d}-review-prompt.md"
    prompt_path.write_text(prompt, encoding="utf-8")
    record_path = root / f"json/round-{n:02d}-review.json"
    write_json(record_path, {"prompt": prompt, "prompt_path": str(prompt_path), "brief_path": str(brief_target)})
    s["active_call"] = {"number": n, "candidate_id": cid, "phase": "prepared", "agent_id": None,
                        "context_policy": "fresh_zero_context", "fork_turns": "none", "continuation_allowed": False,
                        "selected_was_pool_leader": True, "self_score_at_selection": c["self_score"],
                        "eligible_at_selection": eligible(c),
                        "reviewed_problem_ids": candidate_problems(s, c)}
    s["selection"] = {"candidate_id": cid, "self_score": c["self_score"], "reason": reason, "was_pool_leader": True}
    save(root, s)
    return {"call_number": n, "review_record_path": str(record_path), "prompt_path": str(prompt_path), "prompt": prompt,
            "reviewer_calls_used": s["reviewer_calls_used"]}


def parse_review(raw):
    blocks = re.findall(r"```json\s*\n(.*?)\n```", raw, re.S)
    require(blocks, "缺少结尾JSON回复")
    d = json.loads(blocks[-1])
    d["score"] = score(d["score"])
    require(d.get("verdict") in VERDICTS, "verdict不合法")
    require(isinstance(d.get("fatal_blockers"), list) and all(isinstance(x, str) for x in d["fatal_blockers"]), "fatal_blockers需为字符串数组")
    require(d.get("novelty_conclusion") and d.get("search_performed") is True, "独立检索/创新判断不完整")
    ns = d.get("closest_neighbors")
    require(isinstance(ns, list) and any(isinstance(x, dict) and x.get("verified") is True
            and x.get("title") and re.match(r"https?://", x.get("url", "")) for x in ns), "缺少已核验近邻链接")
    goal = d.get("goal_assessment")
    require(isinstance(goal, dict) and goal.get("reason"), "缺少当前目标演化判断")
    for k in ["within_initial_scope", "hard_constraints_satisfied", "evolution_supported"]:
        require(isinstance(goal.get(k), bool), f"目标判断缺少{k}")
        if not goal[k]:
            d["fatal_blockers"].append(f"目标判断未通过：{k}；{goal['reason']}")
    passed = d["score"] > 7.5 and not d["fatal_blockers"]
    require((d["verdict"] == "experiment_ready") == passed, "verdict与分数/阻断矛盾")
    return d, passed


def record(root, s, response_path, error):
    a = s["active_call"]
    require(a and a["phase"] == "started", "没有实际开始的审查调用")
    raw = read_json(inside(root, response_path))["raw_response"] if response_path else ""
    require(response_path or error, "应提供原始回复或具体工具错误")
    (root / "reviews").mkdir(exist_ok=True)
    (root / f"reviews/round-{a['number']:02d}-review.md").write_text(
        raw or f"调用失败：{error}\n", encoding="utf-8")
    parsed, passed, problem = None, False, error
    if not error:
        try:
            require(a["agent_id"], "实际Reviewer agent ID未记录")
            parsed, passed = parse_review(raw)
        except (ValueError, KeyError, TypeError) as exc:
            problem = str(exc)
    result = {**a, "valid": parsed is not None,
              "gate_passed": bool(passed and a["selected_was_pool_leader"] and a["eligible_at_selection"]),
              "error": problem, "review": parsed}
    record_path = root / f"json/round-{a['number']:02d}-review.json"
    trace = read_json(record_path)
    trace.update(result)
    trace["raw_response"] = raw or f"调用失败：{error}"
    write_json(record_path, trace)
    c = get_candidate(s, a["candidate_id"])
    c["review_history"].append(result)
    if result["gate_passed"]:
        c["status"] = "review_passed"
    elif parsed:
        c["status"] = "rejected" if parsed["verdict"] == "reject" else "needs_revision"
    # 格式/工具失败时同一候选仍可竞争，但替代调用须重新占预算。
    s["calls"].append(result)
    s["passing_candidate_id"] = best_passing(s)
    s["active_call"] = None
    save(root, s)
    return result


def result_for(root, s, status, reason):
    pool = list(s["candidates"].values())
    cid = s["passing_candidate_id"] if status == "experiment_ready" else None
    if cid is None and pool:
        available = [c for c in pool if eligible(c)]
        cid = max(available or pool, key=lambda c: c["self_score"])["id"]
    c = s["candidates"].get(cid)
    lineage = []
    cursor = c
    while cursor:
        lineage.append(f"{cursor['id']}：{cursor['goal_difference']}")
        cursor = s["candidates"].get(cursor.get("parent_candidate_id"))
    evolution = " → ".join(reversed(lineage)) if lineage else "尚无可辩护候选，保留初始目标。"
    valid = [r["review"] for r in (c["review_history"] if c else [])
             if r["valid"] and (status != "experiment_ready" or r["gate_passed"])]
    review = max(valid, key=lambda r: r["score"]) if status == "experiment_ready" and valid else valid[-1] if valid else None
    addressed = c["addressed_drawback_ids"] if c else []
    known_new = {d["id"]: d for x in pool for d in x["newly_identified_drawbacks"]}
    blockers = [] if status == "experiment_ready" else [reason]
    if review and status != "experiment_ready":
        blockers += review["fatal_blockers"]
    return {"problem_id": s["input"]["problem_id"], "slot_path": str(root), "status": status,
            "best_candidate_id": cid, "reviewer_score": review["score"] if review else None,
            "verdict": "experiment_ready" if status == "experiment_ready" else
                       review["verdict"] if review and review["verdict"] != "experiment_ready" else "not_ready",
            "final_idea_path": str(root / "FINAL IDEA.md") if status == "experiment_ready" else None,
            "candidate_pool_path": str(root / "IDEA_CANDIDATES.md"),
            "experiment_handoff_path": str(root / "EXPERIMENT_HANDOFF.md") if status == "experiment_ready" else None,
            "blockers": list(dict.fromkeys(blockers)), "initial_drawbacks": s["input"]["drawbacks"],
            "addressed_drawbacks": addressed,
            "unresolved_drawbacks": [d["id"] for d in s["input"]["drawbacks"] if d["id"] not in addressed],
            "newly_identified_drawbacks": list(known_new.values()),
            "goal_evolution_summary": evolution,
            "pre_solution_idea_used": c["pre_solution_idea_used"] if c else False,
            "minimum_reviews_per_problem": MIN_PROBLEM_REVIEWS,
            "problem_review_counts": problem_review_counts(s), "review_budget_complete": budget_met(s),
            "review_budget": dict(s["review_budget"]),
            "reviewer_calls_used": s["reviewer_calls_used"]}


def terminate(root, s, status, reason):
    require(s["active_call"] is None, "先记录当前调用或取消尚未开始的准备")
    research_terminal = status in {"experiment_ready", "no_viable_candidate", "blocked_max_rounds"}
    require(not research_terminal or budget_met(s),
            f"每个Problem须完成当前预算{s['review_budget']}，已完成{problem_review_counts(s)}；不得提前finish/研究早停")
    if status == "experiment_ready":
        cid = s["passing_candidate_id"]
        require(cid and any(r["gate_passed"] for r in get_candidate(s, cid)["review_history"]), "未过Gate不能生成最终结果")
        for f in ["FINAL IDEA.md", "EXPERIMENT_HANDOFF.md"]:
            require((root / f).is_file() and (root / f).read_text(encoding="utf-8").strip(), f"尚未完成{f}")
        (root / "CURRENT_IDEA.md").write_text((root / "FINAL IDEA.md").read_text(encoding="utf-8"), encoding="utf-8")
        get_candidate(s, cid)["status"] = "final"
    else:
        require(status in TERMINAL - {"experiment_ready"} and reason.strip(), "失败状态需合法且有具体原因")
        require(s["passing_candidate_id"] or not any((root / f).exists() for f in ["FINAL IDEA.md", "EXPERIMENT_HANDOFF.md"]),
                "未过Gate却存在最终Idea/实验交接，不能标为合法失败")
        (root / "PIVOT_OR_STOP.md").write_text("# 暂停选题或终止\n\n" + reason +
            "\n\n未完成正式实验；实际目标是暂定声称，未证明解决。保留初始来源、候选及全部审查。\n", encoding="utf-8")
    output = result_for(root, s, status, reason)
    # 实际工具/输入阻断保留未完成循环，可恢复同一输入和真实历史。
    s["status"] = status if research_terminal or budget_met(s) else "in_progress"
    save(root, s)
    write_json(root / "json/SLOT_RESULT.json", output)
    return output


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("action", choices=["init", "route-attempt", "assess-pre-solution", "discovery-note", "register", "classify",
        "prepare-review", "discard-preparation", "start-review", "bind-reviewer", "record-review", "finish", "stop", "show"])
    p.add_argument("--slot")
    p.add_argument("--input")
    p.add_argument("--candidate-file")
    p.add_argument("--candidate-id")
    p.add_argument("--brief-file")
    p.add_argument("--response-file")
    p.add_argument("--route", choices=["route1", "route2"])
    p.add_argument("--status")
    p.add_argument("--reason", default="")
    p.add_argument("--agent-id")
    p.add_argument("--error")
    a = p.parse_args()
    if a.action == "init":
        require(a.input, "init需--input")
        return initialize(a.input)
    require(a.slot, "需--slot")
    root = Path(a.slot).resolve()
    s = load(root)
    if a.action == "show":
        return {"status": s["status"], "reviewer_calls_used": s["reviewer_calls_used"],
                "problem_review_counts": problem_review_counts(s), "review_budget_complete": budget_met(s),
                "review_budget": s["review_budget"],
                "active_call": s["active_call"], "passing_candidate_id": s["passing_candidate_id"]}
    active_run(s)
    if a.action == "register":
        return register(root, s, a.candidate_file)
    if a.action == "prepare-review":
        return prepare(root, s, a.candidate_id, a.brief_file, a.reason)
    if a.action == "record-review":
        return record(root, s, a.response_file, a.error)
    if a.action in {"finish", "stop"}:
        return terminate(root, s, "experiment_ready" if a.action == "finish" else a.status, a.reason)
    if a.action in {"route-attempt", "assess-pre-solution", "discovery-note", "classify"}:
        require(s["active_call"] is None, "审查中不得改候选池")
        require(a.reason.strip(), "需具体证据/判断理由")
        if a.action == "route-attempt":
            require(a.route, "需指定高优先级路线")
            s["route_attempts"].append({"route": a.route, "evidence_and_outcome": a.reason})
        elif a.action == "assess-pre-solution":
            s["pre_solution_assessment"] = a.reason
        elif a.action == "discovery-note":
            s.setdefault("discovery_notes", []).append(a.reason)
        else:
            c = get_candidate(s, a.candidate_id)
            require(a.status in EDITABLE_STATUS, "classify只改变阻断/改进状态，不修改旧内容或评分")
            c["decisions"].append({"previous_status": c["status"], "status": a.status, "reason": a.reason})
            c["status"] = a.status
            if s["passing_candidate_id"] == c["id"]:
                require(not (root / "FINAL IDEA.md").exists(), "已展开最终文档不得暗中重新改核心；交给上游新的循环")
                s["passing_candidate_id"] = best_passing(s)
    else:
        call = s["active_call"]
        require(call, "没有准备或进行中的调用")
        if a.action == "discard-preparation":
            require(call["phase"] == "prepared", "已调用不得取消或返还次数")
            s["active_call"] = None
        elif a.action == "start-review":
            require(call["phase"] == "prepared" and not budget_met(s), "已完成当前审查预算或重复启动")
            call["phase"] = "started"
            s["reviewer_calls_used"] += 1
        elif a.action == "bind-reviewer":
            require(call["phase"] == "started" and a.agent_id and not call["agent_id"], "需新Reviewer ID且只绑定一次")
            require(a.agent_id not in {r["agent_id"] for r in s["calls"] if r["agent_id"]}, "不得复用Reviewer Agent")
            call["agent_id"] = a.agent_id
    save(root, s)
    return {"status": s["status"], "reviewer_calls_used": s["reviewer_calls_used"], "active_call": s["active_call"]}


if __name__ == "__main__":
    try:
        print(json.dumps(main(), ensure_ascii=False, indent=2))
    except (ValueError, KeyError, TypeError, OSError) as exc:
        print(f"状态更新失败：{exc}", file=sys.stderr)
        sys.exit(2)
