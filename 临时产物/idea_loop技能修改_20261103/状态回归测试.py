"""状态 CLI 回归；审查文件均为模拟输入，不启动 Reviewer 或研究实验。"""
from pathlib import Path
import io
import json
import re
import subprocess
import sys
import tempfile
import unittest

sys.stdout.reconfigure(encoding="utf-8")
SLOT = Path(__file__).resolve().parent
PROJECT = SLOT.parents[1]
SKILL = PROJECT / "skills" / "idea-improvement-loop"
SCRIPT = SKILL / "tools" / "loop_state.py"
RUN = Path(tempfile.mkdtemp(prefix="回归现场_", dir=SLOT))


class LoopStateRegression(unittest.TestCase):
    def setUp(self):
        self.root = RUN / self._testMethodName
        self.root.mkdir()
        self.slug = "demo"

    def command(self, *args):
        return subprocess.run(
            [sys.executable, "-X", "utf8", str(SCRIPT), "--root", str(self.root), *args],
            cwd=self.root, capture_output=True, encoding="utf-8",
        )

    def ok(self, *args):
        result = self.command(*args)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout.strip()

    def initialize(self, raw=None, cap=None, mode="problem_card"):
        idea = self.root / "idea-stage" / self.slug
        idea.mkdir(parents=True)
        (idea / "RAW_IDEA.md").write_text(
            raw or "# 模拟输入\n\n## 问题锚点（Problem Anchor）\n起点问题与用户约束。\n",
            encoding="utf-8",
        )
        self.brief = idea / "候选简报.md"
        self.brief.write_text(
            "## 背景\n模拟问题\n## 核心 Claim\n模拟机制 A\n"
            "## 方法设计的核心思想\n模拟动作 A\n## 最小实验\n模拟对照\n",
            encoding="utf-8",
        )
        args = ["init", "--slug", self.slug, "--mode", mode]
        if cap is not None:
            args.extend(["--max-calls", str(cap)])
        self.ok(*args)

    def start(self):
        return json.loads(self.ok(
            "start-call", "--slug", self.slug, "--candidate", "IDEA-001",
            "--self-score", "7.5", "--brief", str(self.brief), "--date", "2026-11-03",
        ))

    def confirm(self, *args):
        return json.loads(self.ok(
            "start-call", "--slug", self.slug, "--role", "confirmation", "--effort", "xhigh", *args,
        ))

    def state_path(self):
        return self.root / "review-stage" / self.slug / "REVIEW_STATE.json"

    def state(self):
        return json.loads(self.state_path().read_text(encoding="utf-8"))

    def log_path(self):
        return self.root / "review-stage" / self.slug / "AUTO_REVIEW.md"

    def review(self, scores=(8, 8, 6), blockers=None):
        n = self.state()["reviewer_calls_used"]
        path = self.root / "review-stage" / self.slug / f"round-{n:02d}-review.md"
        result = {
            "score": 8,
            "contribution_scores": dict(zip(("importance", "novelty", "effectiveness"), scores)),
            "contribution_assessment": "模拟判断依据，不是真实研究审查",
            "feasibility": "pass", "feasibility_reason": "模拟实现依据",
            "verdict": "experiment_ready", "fatal_blockers": blockers or [],
            "novelty_conclusion": "模拟输入", "closest_neighbors": [],
        }
        path.write_text("# 模拟审查\n\n" + json.dumps(result, ensure_ascii=False), encoding="utf-8")
        return json.loads(self.ok("record", "--slug", self.slug))

    def pair_passes(self):
        self.start()
        self.assertEqual(self.review()["outcome"], "first_pass")
        self.confirm()
        self.assertEqual(self.review()["outcome"], "gate_passed")

    def test_problem_card_template_can_start(self):
        text = (SKILL / "references/problem-card-input.md").read_text(encoding="utf-8")
        raw = re.search(r"```markdown\n(.*?)```", text, re.S).group(1)
        self.initialize(raw=raw)
        call = self.start()
        prompt = (self.root / call["prompt"]).read_text(encoding="utf-8")
        self.assertNotIn("<<ANCHOR>>", prompt)
        self.assertIn("起点问题的对象", prompt)

    def test_paper_template_can_start(self):
        text = (SKILL / "references/paper-input.md").read_text(encoding="utf-8")
        raw = re.search(r"```markdown\n(.*?)```", text, re.S).group(1)
        self.initialize(raw=raw, mode="baseline_paper")
        call = self.start()
        prompt = (self.root / call["prompt"]).read_text(encoding="utf-8")
        self.assertNotIn("<<ANCHOR>>", prompt)
        self.assertIn("作为起点的研究对象", prompt)

    def test_default_budget_and_two_review_gate(self):
        self.initialize(mode="raw_idea")
        self.assertEqual(self.state()["max_reviewer_calls"], 6)
        self.pair_passes()
        state = self.state()
        self.assertTrue(state["gate_passed"])
        self.assertEqual(state["reviewer_calls_used"], 2)
        self.assertIsNone(state["pending_confirmation"])

    def test_changed_confirmation_brief_is_rejected_without_spending_a_call(self):
        self.initialize()
        self.start()
        self.review()
        changed = self.brief.with_name("新主张.md")
        changed.write_text(self.brief.read_text(encoding="utf-8").replace("机制 A", "机制 B"), encoding="utf-8")
        result = self.command("start-call", "--slug", self.slug, "--role", "confirmation", "--brief", str(changed))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("同一份 brief", result.stderr)
        self.assertEqual(self.state()["reviewer_calls_used"], 1)
        self.assertIsNotNone(self.state()["pending_confirmation"])
        call = self.confirm()
        self.assertEqual((self.root / call["brief"]).read_bytes(), self.brief.read_bytes())
        self.assertEqual(self.review()["outcome"], "gate_passed")

    def test_other_candidate_cannot_confirm_a_first_pass(self):
        self.initialize()
        self.start()
        self.review()
        result = self.command("start-call", "--slug", self.slug, "--role", "confirmation", "--candidate", "IDEA-002")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.state()["reviewer_calls_used"], 1)

    def test_confirmation_record_checks_saved_briefs(self):
        self.initialize()
        self.start()
        self.review()
        call = self.confirm()
        path = self.root / call["brief"]
        path.write_text(path.read_text(encoding="utf-8").replace("机制 A", "机制 B"), encoding="utf-8")
        self.assertEqual(self.review()["outcome"], "confirmation_failed")
        self.assertFalse(self.state()["gate_passed"])

    def test_repeated_record_preserves_gate_state_and_log(self):
        self.initialize()
        self.pair_passes()
        state_before, log_before = self.state_path().read_bytes(), self.log_path().read_bytes()
        again = json.loads(self.ok("record", "--slug", self.slug))
        self.assertEqual(again["outcome"], "gate_passed")
        self.assertEqual(self.state_path().read_bytes(), state_before)
        self.assertEqual(self.log_path().read_bytes(), log_before)
        self.assertTrue(self.state()["gate_passed"])

    def test_blocked_first_pass_can_confirm_after_one_call_extension(self):
        self.initialize(cap=1)
        self.start()
        self.assertEqual(self.review()["outcome"], "first_pass_no_budget")
        self.ok("finish", "--slug", self.slug, "--status", "blocked_max_reviewer_calls")
        self.assertIsNotNone(self.state()["pending_confirmation"])
        self.ok("extend", "--slug", self.slug, "--add", "1", "--reason", "模拟用户追加复核预算")
        self.confirm()
        self.assertEqual(self.review()["outcome"], "gate_passed")
        self.ok("finish", "--slug", self.slug, "--status", "completed")
        self.assertEqual(self.state()["status"], "completed")
        self.assertTrue(self.state()["gate_passed"])

    def test_old_round_state_preserves_spent_budget(self):
        self.initialize(cap=3)
        old = self.state()
        old["round"] = 2
        del old["reviewer_calls_used"]
        del old["reviewer_calls"]
        del old["pending_confirmation"]
        self.state_path().write_text(json.dumps(old, ensure_ascii=False), encoding="utf-8")
        self.ok("status", "--slug", self.slug)
        call = self.start()
        self.assertEqual(call["call"], 3)
        self.assertEqual(self.state()["reviewer_calls_used"], 3)
        result = self.command("start-call", "--slug", self.slug, "--candidate", "IDEA-001",
                              "--self-score", "7.5", "--brief", str(self.brief))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("预算已用尽", result.stderr)

    def test_contribution_gate_does_not_accept_high_overall_score_alone(self):
        for index, (scores, blockers) in enumerate([
            ((8, 8, 5), []), ((8, 7, 7), []), ((8, 8, 6), ["模拟未解决阻断"]),
        ]):
            with self.subTest(scores=scores, blockers=blockers):
                self.slug = f"gate_{index}"
                self.initialize()
                self.start()
                self.assertEqual(self.review(scores=scores, blockers=blockers)["outcome"], "failed")
                self.assertFalse(self.state()["gate_passed"])
                self.assertIsNone(self.state()["pending_confirmation"])

    def test_malformed_review_and_replacement_still_spend_budget(self):
        self.initialize(cap=2)
        call = self.start()
        (self.root / call["review"]).write_text("模拟无法解析的审查", encoding="utf-8")
        result = self.command("record", "--slug", self.slug)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.state()["reviewer_calls_used"], 1)
        self.assertEqual(self.start()["call"], 2)
        self.assertEqual(self.review()["outcome"], "first_pass_no_budget")
        self.assertFalse(self.state()["gate_passed"])


if __name__ == "__main__":
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(LoopStateRegression)
    )
    output = "全部为模拟输入；未启动 Reviewer 或研究实验。\n现场目录：" + str(RUN) + "\n\n" + stream.getvalue()
    (SLOT / "状态回归结果.txt").write_text(output, encoding="utf-8")
    print(output)
    raise SystemExit(0 if result.wasSuccessful() else 1)
