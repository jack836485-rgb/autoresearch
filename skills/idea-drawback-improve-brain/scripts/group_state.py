#!/usr/bin/env python3
"""总控的独立文件工具：创建不覆盖的Group、传下游输入、记录调度、只读收集、渲染比较。

不生成候选、不调用Reviewer、不修改子Slot结果或任何skill。机制规划和优先级由总控直接判断。
"""
import argparse
import json
import math
import sys
from pathlib import Path

MIN_PROBLEM_REVIEWS = 10

RESULT_KEYS = {"problem_id", "slot_path", "status", "best_candidate_id", "reviewer_score", "verdict",
               "final_idea_path", "candidate_pool_path", "experiment_handoff_path", "blockers",
               "initial_drawbacks", "addressed_drawbacks", "unresolved_drawbacks", "newly_identified_drawbacks",
               "goal_evolution_summary", "pre_solution_idea_used", "minimum_reviews_per_problem",
               "problem_review_counts", "review_budget_complete", "reviewer_calls_used", "review_budget"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def write(path, data):
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def j(value):
    return json.dumps(value, ensure_ascii=False, indent=2)


def leaf(name):
    return isinstance(name, str) and name not in {"", ".", ".."} and not any(x in name for x in ["/", "\\", ":"])


def map_problems(plan):
    path = Path(plan["path_stage"]).resolve()
    if path.is_dir():
        path = path / ("研究问题.json" if (path / "研究问题.json").exists() else "研究地图.md")
    if "problems" in plan:
        records = plan["problems"]
    else:
        data = read(path)
        records = data.get("研究问题", data.get("problems"))
    require(isinstance(records, list) and records, "需要Problem Map问题卡或人工规范化problems")
    problems = {}
    for raw in records:
        pid = raw.get("id", raw.get("problem_id"))
        text = raw.get("具体问题", raw.get("problem"))
        require(pid and text and pid not in problems, "来源Problem需唯一ID和内容")
        problems[pid] = {"problem_id": pid, "problem": text, "source_path": str(path), "map_record": raw}
    selected = plan.get("selected_problem_ids", list(problems))
    require(selected and set(selected) <= set(problems), "选中的Problem ID不在Map中")
    return str(path), {pid: problems[pid] for pid in selected}


def render(s):
    root = Path(s["group_path"])
    parts = ["# 实验总结", "", "本次为文献驱动的 Idea 改进；未执行正式实验。", "",
             f"- Problem Map：{s['map_path']}", "- addressed 仅表示预计处理并设计验证，不是实测解决。", ""]
    dmap = {d["id"]: d for d in s["plan"]["drawbacks"]}
    for sid, entry in s["slots"].items():
        sp = entry["plan"]
        r = entry.get("result")
        parts += [f"## {sid}", "", "**最初输入给 Improver 的问题：**", ""]
        for pid in sp["source_problems"]:
            parts += [f"- {pid}：{s['problems'][pid]['problem']}"]
        parts += ["", "**初始 drawbacks：**", ""]
        for did in sp["target_drawbacks"]:
            parts += [f"- {did}：{dmap[did]['description']}"]
        parts += ["", f"**探索目标：** {sp['exploration_goal']}",
                  f"**初始思路：** {'有可放弃的假设，见RAW_IDEA.md。' if sp.get('pre_solution_idea') else '无，开放探索。'}", "",
                  f"**执行状态：** {entry['run_status']} / {entry['collection_status']}",
                  f"**候选数：** {len(entry.get('candidates', {}))}"]
        calls = [h for c in entry.get("candidates", {}).values() for h in c.get("review_history", [])]
        scores = [str(h["review"]["score"]) for h in sorted(calls, key=lambda h: h["number"])
                  if h.get("valid") and h.get("review")]
        parts += [f"**独立审查：** {len(calls)} 次；评分：{', '.join(scores) if scores else '尚无有效评分'}"]
        counts = entry.get("problem_review_counts", dict.fromkeys(entry["input"]["review_problem_ids"], 0))
        parts += [f"**每个 Problem 有效审查：** {counts}；当前预算 {entry['review_budget']}"]
        for change in entry.get("budget_extensions", []):
            parts += [f"**追加预算：** {change['added_rounds']}轮，涉及{change['problem_ids']}；"
                      f"理由：{change['reason']}；后续目标：{change['objective']}"]
        if r:
            parts += [f"**结果：** {r['status']}；最佳候选 {r['best_candidate_id']}",
                      f"**目标演化：** {r['goal_evolution_summary']}",
                      f"**预计处理／未覆盖：** {r['addressed_drawbacks']} / {r['unresolved_drawbacks']}",
                      f"**沿用初始假设：** {r['pre_solution_idea_used']}"]
        if entry.get("issues"):
            parts += ["**阻断原因：** " + "；".join(entry["issues"])]
        parts += ["", f"[初始输入]({sid}/RAW_IDEA.md) · [候选 Idea]({sid}/IDEA_CANDIDATES.md)", ""]
    comparison = s.get("comparison")
    if comparison:
        parts += ["## 本组执行结论", "", comparison["summary"], ""]
    (root / "实验总结.md").write_text("\n".join(parts), encoding="utf-8")


def save(s):
    write(Path(s["group_path"]) / "json/GROUP_STATE.json", s)
    render(s)


def initialize(plan_path, idea_root):
    p = read(plan_path)
    require(leaf(p["group_name"]), "group_name须为独立目录名称")
    map_path, problems = map_problems(p)
    ds = p["drawbacks"]
    require(isinstance(ds, list) and ds, "需要有证据的具体drawbacks")
    dmap = {d["id"]: d for d in ds}
    require(len(dmap) == len(ds), "Group drawback ID重复")
    for d in ds:
        require(d.get("description") and d.get("evidence") and d.get("problem_ids"), "drawback需内容、关联问题和证据")
        require(set(d["problem_ids"]) <= set(problems), "drawback来源不在选定Problem范围")
    constraints = p["constraints"]
    require(isinstance(constraints.get("hard"), list), "constraints需hard数组")
    slots = p["slots"]
    require(slots and len({x["slot_id"] for x in slots}) == len(slots), "Slot需非空且ID不重复")
    for x in slots:
        require(leaf(x["slot_id"]), "slot_id须为目录名称")
        require(x["source_problems"] and set(x["source_problems"]) <= set(problems), "Slot来源问题不合法")
        require(x["target_drawbacks"] and set(x["target_drawbacks"]) <= set(dmap), "Slot目标不足不合法")
        require(all(set(dmap[d]["problem_ids"]) <= set(x["source_problems"]) for d in x["target_drawbacks"]), "联合Slot缺少目标原始Problem")
        for k in ["exploration_goal", "planning_rationale", "distinct_direction", "initial_motivation", "initial_validation_goal"]:
            require(isinstance(x.get(k), str) and x[k].strip(), f"Slot缺少判断：{k}")
        require(set(constraints["hard"]) <= set(x["constraints"].get("hard", [])), "Slot删除了用户硬约束")
        require(isinstance(x.get("nearest_neighbors"), list), "nearest_neighbors须为数组，可明确暂缺")
        x.setdefault("pre_solution_idea", None)
    for i, x in enumerate(slots):
        for y in slots[:i]:
            same = set(x["target_drawbacks"]) == set(y["target_drawbacks"])
            require(not same or x["distinct_direction"].strip() != y["distinct_direction"].strip(),
                    "同目标Slots需实质不同的假设/机制说明，不能重复同一方向")
    assigned = {pid for x in slots for did in x["target_drawbacks"] for pid in dmap[did]["problem_ids"]}
    require(set(problems) <= assigned, "选中的每个Problem必须安排至少十轮；仅作背景的问题不应列为selected_problem_ids")
    parent = Path(idea_root).resolve()
    parent.mkdir(parents=True, exist_ok=True)
    group = parent / p["group_name"]
    suffix = 2
    while group.exists():
        group = parent / f"{p['group_name']}-{suffix:02d}"
        suffix += 1
    group.mkdir()
    (group / "json").mkdir()
    s = {"group_path": str(group), "map_path": map_path, "plan": p, "problems": problems, "slots": {}, "comparison": None}
    for sp in slots:
        sid = sp["slot_id"]
        directory = group / sid
        directory.mkdir()
        (directory / "json").mkdir()
        (directory / "prompt").mkdir()
        sp["slot_path"] = str(directory)
        targets = [dmap[d] for d in sp["target_drawbacks"]]
        sp["drawback_evidence"] = [{"drawback_id": d["id"], "evidence": d["evidence"]} for d in targets]
        records = [problems[pid]["map_record"] for pid in sp["source_problems"]]
        context = {"problem_records": records, "literature": [e for q in records for e in q.get("证据", q.get("evidence", []))],
                   "closest_neighbors": sp["nearest_neighbors"], "limitations": targets, "background": records,
                   "source_paths": [map_path], **{k: sp[k] for k in ["exploration_goal", "planning_rationale", "initial_motivation", "initial_validation_goal"]}}
        task = {"slot_path": str(directory), "problem_id": sid,
                "review_problem_ids": sorted({pid for d in targets for pid in d["problem_ids"]}),
                "minimum_reviews_per_problem": MIN_PROBLEM_REVIEWS,
                "problems": [{"problem_id": pid, "problem": problems[pid]["problem"]} for pid in sp["source_problems"]],
                "drawbacks": targets, "pre_solution_idea": sp["pre_solution_idea"], "problem_map_context": context,
                "constraints": sp["constraints"]}
        write(directory / "json/SLOT_INPUT.json", task)
        s["slots"][sid] = {"plan": sp, "input": task, "run_status": "planned", "collection_status": "pending",
                            "review_budget": dict.fromkeys(task["review_problem_ids"], MIN_PROBLEM_REVIEWS),
                            "budget_extensions": [],
                            "dispatch_history": [], "result": None, "candidates": {}, "issues": []}
    save(s)
    return {"group_path": str(group), "slots": {sid: e["plan"]["slot_path"] for sid, e in s["slots"].items()}}


def collect(s, sid):
    entry = s["slots"][sid]
    slot = Path(entry["plan"]["slot_path"])
    state_path = slot / "json/REVIEW_STATE.json"
    try:
        child = read(state_path) if state_path.exists() else {}
    except (ValueError, OSError) as exc:
        entry["collection_status"], entry["issues"] = "protocol_error", [f"下游状态不完整：{exc}"]
        save(s)
        return {"slot_id": sid, "collection_status": "protocol_error", "issues": entry["issues"]}
    entry["candidates"] = child.get("candidates", {})
    path = slot / "json/SLOT_RESULT.json"
    if not path.exists():
        entry["collection_status"] = "missing_result"
        entry["issues"] = ["尚无下游SLOT_RESULT；等待真实任务结束或记录实际执行失败"]
        save(s)
        return {"slot_id": sid, "collection_status": "missing_result"}
    try:
        r = read(path)
        entry["result"] = r
        require(RESULT_KEYS <= set(r), "下游结果缺少实际接口字段")
        require(r["status"] in {"experiment_ready", "blocked_max_rounds", "no_viable_candidate", "blocked_input",
                                "blocked_review_unavailable", "blocked_finalization"}, "不是下游声明的终止状态")
        require(r["problem_id"] == sid and Path(r["slot_path"]).resolve() == slot, "下游结果路由或slot路径错配")
        counts = dict.fromkeys(entry["input"]["review_problem_ids"], 0)
        for call in child.get("calls", []):
            goal = (call.get("review") or {}).get("goal_assessment", {})
            if not (call.get("valid") and call.get("agent_id") and call.get("fork_turns") == "none"
                    and call.get("context_policy") == "fresh_zero_context"
                    and goal.get("within_initial_scope") and goal.get("hard_constraints_satisfied")):
                continue
            for pid in set(call.get("reviewed_problem_ids", [])) & counts.keys():
                counts[pid] += 1
        complete = all(n >= entry["review_budget"][pid] for pid, n in counts.items())
        entry["problem_review_counts"] = counts
        require(r["minimum_reviews_per_problem"] == MIN_PROBLEM_REVIEWS
                and r["review_budget"] == child.get("review_budget") == entry["review_budget"]
                and r["problem_review_counts"] == counts and r["review_budget_complete"] == complete,
                "下游最低预算/Problem计数与真实审查记录不一致")
        require(r["reviewer_calls_used"] == child.get("reviewer_calls_used") == len(child.get("calls", [])),
                "真实Reviewer调用数与记录不一致")
        require(r["status"] not in {"experiment_ready", "no_viable_candidate", "blocked_max_rounds"} or complete,
                f"未完成每Problem当前预算{entry['review_budget']}却宣告研究结束：{counts}")
        require(r["initial_drawbacks"] == entry["input"]["drawbacks"], "初始不足被改写或来自其他Slot")
        known = {d["id"] for d in r["initial_drawbacks"] + r["newly_identified_drawbacks"]}
        require(set(r["addressed_drawbacks"]) <= known, "实际目标含未知不足")
        require(set(r["unresolved_drawbacks"]) == {d["id"] for d in r["initial_drawbacks"]} - set(r["addressed_drawbacks"]), "未覆盖初始目标与来源不一致")
        require(not r["pre_solution_idea_used"] or entry["input"]["pre_solution_idea"] is not None, "未给初始假设却标沿用")
        if r["status"] == "experiment_ready":
            require(r["verdict"] == "experiment_ready" and isinstance(r["reviewer_score"], (int, float))
                    and not isinstance(r["reviewer_score"], bool) and math.isfinite(r["reviewer_score"])
                    and r["reviewer_score"] > 7.5 and not r["blockers"], "结果不满足已有Gate通过口径")
            cid = r["best_candidate_id"]
            require(child.get("status") == "experiment_ready" and child.get("passing_candidate_id") == cid, "原下游未完成该候选的Gate/Finalization")
            require(any(c.get("candidate_id") == cid and c.get("valid") and c.get("gate_passed")
                    and c.get("review", {}).get("score") == r["reviewer_score"]
                    and not c.get("review", {}).get("fatal_blockers") for c in child.get("calls", [])), "缺少该候选的真实通过审查记录")
            for k, filename in [("final_idea_path", "FINAL IDEA.md"), ("experiment_handoff_path", "EXPERIMENT_HANDOFF.md"),
                                ("candidate_pool_path", "IDEA_CANDIDATES.md")]:
                require(r[k] and Path(r[k]).resolve() == slot / filename and (slot / filename).is_file(), f"{k}不在自身slot或不存在")
            entry["collection_status"] = "ready"
        else:
            require(r["final_idea_path"] is None and r["experiment_handoff_path"] is None and r["verdict"] != "experiment_ready", "未通过结果却返回实验就绪产物")
            entry["collection_status"] = "gate_or_workflow_failed" if complete else "execution_failed"
        entry["run_status"] = "completed" if complete else "execution_failed"
        entry["issues"] = r["blockers"]
    except (ValueError, KeyError, TypeError, OSError) as exc:
        entry["collection_status"] = "protocol_error"
        entry["issues"] = [str(exc)]
    s["comparison"] = None
    save(s)
    return {"slot_id": sid, "collection_status": entry["collection_status"], "issues": entry["issues"]}


def compare(s, path):
    comparison = read(path)
    alignment = {x["slot_id"]: x for x in comparison["goal_alignment"]}
    ready = {sid for sid, e in s["slots"].items() if e["collection_status"] == "ready"}
    require(ready <= set(alignment), "需要明确判断每个通过方向的目标演化/硬约束")
    for sid, a in alignment.items():
        require(sid in s["slots"] and a["status"] in {"reasonable_evolution", "needs_repositioning", "violates_hard_constraints"}
                and a.get("reason"), "目标定位须有依据且指真实Slot")
    rankable = {sid for sid in ready if alignment[sid]["status"] == "reasonable_evolution"}
    duplicates = set()
    for g in comparison["overlap_groups"]:
        require(g.get("reason") and len(g["members"]) >= 2, "重合判断需至少两个候选及具体依据")
        require(g["relation"] in {"duplicate_mechanism", "shared_drawbacks_different_mechanism", "complementary", "insufficient_evidence"}, "未知重合关系")
        for m in g["members"]:
            require(m["slot_id"] in s["slots"] and m["candidate_id"] in s["slots"][m["slot_id"]]["candidates"], "重合引用了不存在的slot/candidate")
        if g.get("representative"):
            require(g["representative"] in g["members"], "代表必须是已引用候选")
            require(g["representative"]["slot_id"] in rankable, "失败或偏题候选不能作为通过方向代表")
            re = s["slots"][g["representative"]["slot_id"]]
            require(re["result"]["best_candidate_id"] == g["representative"]["candidate_id"], "重合代表须为实际通过的最终候选")
            if g["relation"] == "duplicate_mechanism":
                duplicates.update(m["slot_id"] for m in g["members"] if m != g["representative"]
                                  and (s["slots"][m["slot_id"]].get("result") or {}).get("best_candidate_id") == m["candidate_id"])
    ranked = [r["slot_id"] for r in comparison["ranking"]]
    require(set(ranked) == rankable - duplicates and len(ranked) == len(set(ranked)), "排名须包含通过且符合来源的独立方向，机制重复者列入归档")
    for row in comparison["ranking"]:
        require(row.get("reason") and row.get("cost_basis"), "排序需直接比较及成本口径")
    require(comparison.get("summary"), "需要有据的Group总结")
    s["comparison"] = comparison
    save(s)
    return {"group_path": s["group_path"], "ranked_slots": ranked, "overlap_groups": len(comparison["overlap_groups"])}


def extend_budget(s, sid, problem_ids, added_rounds, reason, objective, prompt_file):
    entry = s["slots"][sid]
    require(added_rounds and added_rounds > 0 and reason.strip() and objective.strip(),
            "增加预算需正整数轮数、潜力依据与后续探索目标")
    targets = problem_ids or list(entry["review_budget"])
    require(targets and len(set(targets)) == len(targets) and set(targets) <= set(entry["review_budget"]),
            "只能给本Slot已有目标Problem增加预算")
    slot = Path(entry["plan"]["slot_path"])
    require(prompt_file, "先保存实际追加指令，再用--prompt-file关联该提示")
    prompt_path = Path(prompt_file).resolve()
    require(prompt_path.parent == slot / "prompt" and prompt_path.is_file()
            and prompt_path.read_text(encoding="utf-8-sig").strip(), "追加提示须位于本Slot/prompt且非空")
    require(str(prompt_path) not in {h.get("prompt_path") for h in
            entry["dispatch_history"] + entry["budget_extensions"]}, "追加预算须使用新序号实际提示，保留旧提示历史")
    child = read(slot / "json/REVIEW_STATE.json")
    require(child["status"] == "in_progress" and child["active_call"] is None,
            "在执行器初始化后、轮次边界协同加预算；已终结或正在审查的Loop不得直接改写")
    require(child["review_budget"] == entry["review_budget"], "总控与执行器预算不一致")
    previous = dict(child["review_budget"])
    updated = {pid: n + (added_rounds if pid in targets else 0) for pid, n in previous.items()}
    change = {"problem_ids": targets, "added_rounds": added_rounds, "previous_budget": previous,
              "new_budget": updated, "reason": reason, "objective": objective, "prompt_path": str(prompt_path)}
    child["review_budget"] = updated
    child["max_rounds"] = sum(updated.values())
    child["budget_history"].append(change)
    write(slot / "json/REVIEW_STATE.json", child)
    entry["review_budget"] = updated
    entry["budget_extensions"].append(change)
    entry["collection_status"] = "pending"
    entry["result"] = None
    s["comparison"] = None
    save(s)
    return {"slot_id": sid, **change}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("action", choices=["init", "dispatch", "collect", "execution-failed", "compare", "show", "extend-budget"])
    for key in ["plan", "idea-root", "group", "slot-id", "agent-id", "prompt-file", "reason", "comparison"]:
        p.add_argument("--" + key)
    p.add_argument("--rounds", type=int)
    p.add_argument("--problem-ids", nargs="+")
    p.add_argument("--objective", default="")
    a = p.parse_args()
    if a.action == "init":
        require(a.plan and a.idea_root, "init需要plan和idea-root")
        return initialize(a.plan, a.idea_root)
    require(a.group, "需指定Group")
    root = Path(a.group).resolve()
    s = read(root / "json/GROUP_STATE.json")
    require(s["group_path"] == str(root), "Group状态路径不匹配")
    if a.action == "show":
        return {"group_path": str(root), "slots": {sid: {"run_status": e["run_status"], "collection_status": e["collection_status"]} for sid, e in s["slots"].items()}}
    if a.action == "compare":
        return compare(s, a.comparison)
    require(a.slot_id in s["slots"], "未知slot_id")
    e = s["slots"][a.slot_id]
    if a.action == "collect":
        return collect(s, a.slot_id)
    if a.action == "extend-budget":
        return extend_budget(s, a.slot_id, a.problem_ids, a.rounds, a.reason or "", a.objective, a.prompt_file)
    if a.action == "dispatch":
        require(a.agent_id, "需记录实际spawn返回ID")
        require(e["run_status"] in {"planned", "execution_failed"} and e["collection_status"] not in {"ready", "gate_or_workflow_failed"}, "已有运行或研究终态，不能重复启动")
        require(a.prompt_file, "需记录spawn前保存的完整Improver提示路径")
        prompt_path = Path(a.prompt_file).resolve()
        prompt_dir = Path(e["plan"]["slot_path"]) / "prompt"
        require(prompt_path.parent == prompt_dir and prompt_path.is_file()
                and prompt_path.read_text(encoding="utf-8-sig").strip(), "Improver提示必须是自身slot/prompt内的非空文件")
        require(str(prompt_path) not in {h.get("prompt_path") for h in e["dispatch_history"]}, "恢复或替代调用须另存新提示，不能复用旧记录")
        e["dispatch_history"].append({"agent_id": a.agent_id, "prompt_path": str(prompt_path),
                                      "reason": a.reason or "首次调度", "resume_existing_slot_state": e["run_status"] == "execution_failed"})
        e["run_status"] = "running"
        e["result"] = None
        e["collection_status"] = "pending"
        e["issues"] = []
    else:
        require(a.reason, "执行失败必须有实际原因")
        e["run_status"], e["collection_status"], e["issues"] = "execution_failed", "execution_failed", [a.reason]
    save(s)
    return {"slot_id": a.slot_id, "run_status": e["run_status"], "collection_status": e["collection_status"]}


if __name__ == "__main__":
    try:
        print(json.dumps(main(), ensure_ascii=False, indent=2))
    except (ValueError, KeyError, TypeError, OSError) as exc:
        print(f"总控状态更新失败：{exc}", file=sys.stderr)
        sys.exit(2)
