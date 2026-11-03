"""用合成评审验证贡献通过条件和首审／复核流程，不调用研究 Reviewer。"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True
TASK_DIR = Path(__file__).resolve().parent
PROJECT_DIR = TASK_DIR.parent.parent
SKILL_DIR = PROJECT_DIR / "skills" / "idea-improvement-loop"
TOOL = SKILL_DIR / "tools" / "loop_state.py"
spec = importlib.util.spec_from_file_location("idea_loop_state", TOOL)
loop_state = importlib.util.module_from_spec(spec)
spec.loader.exec_module(loop_state)


def payload(scores=(8, 8, 6), *, score=7.4, feasibility="pass", verdict="experiment_ready", blockers=None):
    return {
        "score": score,
        "contribution_scores": dict(zip(("importance", "novelty", "effectiveness"), scores)),
        "contribution_assessment": "合成评审，仅验证通过条件，不是研究结论。",
        "feasibility": feasibility,
        "feasibility_reason": "合成场景具有可执行步骤与明确资源预算。",
        "verdict": verdict,
        "fatal_blockers": blockers or [],
        "novelty_conclusion": "合成样例，不执行查新。",
        "closest_neighbors": [],
    }


class ContributionGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.run_dir = Path(tempfile.mkdtemp(prefix="验证场景_", dir=TASK_DIR))

    def test_two_strengths_can_be_in_any_dimensions(self):
        for scores in ((8, 8, 6), (8, 6, 8), (6, 8, 8), (8.5, 7, 8)):
            with self.subTest(scores=scores):
                self.assertTrue(loop_state.review_qualifies(payload(scores, score=7.4)))

    def test_high_overall_score_cannot_cover_weak_contribution(self):
        for scores in ((9, 9, 5), (9, 7, 7), (8, 8, 5.9), (8, 7.9, 6)):
            with self.subTest(scores=scores):
                self.assertFalse(loop_state.review_qualifies(payload(scores, score=9.9)))

    def test_feasibility_verdict_and_blockers_are_binding(self):
        for fields in (
            {"feasibility": "fail"},
            {"verdict": "needs_rethink"},
            {"blockers": ["主贡献缺少可信证据"]},
        ):
            with self.subTest(fields=fields):
                self.assertFalse(loop_state.review_qualifies(payload((9, 9, 9), **fields)))

    def test_incomplete_old_review_cannot_pass(self):
        for key in ("contribution_scores", "feasibility", "verdict", "fatal_blockers",
                    "contribution_assessment", "feasibility_reason"):
            incomplete = payload()
            del incomplete[key]
            with self.subTest(key=key), self.assertRaises(SystemExit):
                loop_state.review_qualifies(incomplete)

    def cli(self, root, *args, succeeds=True):
        process = subprocess.run(
            [sys.executable, "-X", "utf8", str(TOOL), "--root", str(root), *args],
            capture_output=True, text=True, encoding="utf-8",
        )
        if succeeds:
            self.assertEqual(process.returncode, 0, process.stdout + process.stderr)
        else:
            self.assertNotEqual(process.returncode, 0)
        return process

    def prepare(self, name):
        root = self.run_dir / name
        root.mkdir()
        self.cli(root, "init", "--slug", "synthetic", "--mode", "raw_idea", "--max-calls", "4")
        idea = root / "idea-stage" / "synthetic"
        (idea / "RAW_IDEA.md").write_text(
            "# 合成输入\n\n## Problem Anchor\n仅验证程序；不开展研究，不调用外部模型。\n", encoding="utf-8")
        draft = idea / "合成简报.md"
        draft.write_text(
            "## 背景\n合成场景\n\n## 核心 Claim\n占位主贡献\n\n"
            "## 方法设计的核心思想\n合成输入\n\n## 最小实验\n不运行真实实验\n", encoding="utf-8")
        self.cli(root, "start-call", "--slug", "synthetic", "--candidate", "IDEA-001",
                 "--self-score", "7.4", "--brief", str(draft), "--date", "2026-11-02")
        return root

    def record(self, root, number, result, *, succeeds=True):
        review = root / "review-stage" / "synthetic" / f"round-{number:02d}-review.md"
        review.write_text("# 合成评审\n\n```json\n" + json.dumps(result, ensure_ascii=False) + "\n```\n", encoding="utf-8")
        response = self.cli(root, "record", "--slug", "synthetic", succeeds=succeeds)
        return json.loads(response.stdout) if succeeds else response

    def state(self, root):
        return json.loads((root / "review-stage" / "synthetic" / "REVIEW_STATE.json").read_text(encoding="utf-8"))

    def test_real_prompt_and_confirmation_use_shared_standard(self):
        root = self.prepare("现象贡献通过")
        prompt_path = root / "review-stage" / "synthetic" / "prompts" / "round-01-review-prompt.md"
        prompt = prompt_path.read_text(encoding="utf-8")
        standard = loop_state.CONTRIBUTION_STANDARD.read_text(encoding="utf-8").strip()
        self.assertIn(standard, prompt)
        self.assertNotRegex(prompt, r"<<[A-Z_]+>>")
        self.assertIn("仅验证程序；不开展研究", prompt)
        first = self.record(root, 1, payload((6, 8, 8)))
        self.assertEqual(first["outcome"], "first_pass")
        self.assertIsNotNone(self.state(root)["pending_confirmation"])
        self.cli(root, "start-call", "--slug", "synthetic", "--role", "confirmation", "--effort", "xhigh")
        confirmation = self.record(root, 2, payload((8, 6, 8)))
        self.assertEqual(confirmation["outcome"], "gate_passed")
        recorded = self.state(root)
        self.assertEqual(recorded["last_contribution_scores"]["novelty"], 6)
        self.assertEqual(recorded["last_feasibility"], "pass")

    def test_confirmation_cannot_rescue_a_weak_dimension(self):
        root = self.prepare("复核贡献不足")
        self.assertEqual(self.record(root, 1, payload())["outcome"], "first_pass")
        self.cli(root, "start-call", "--slug", "synthetic", "--role", "confirmation", "--effort", "xhigh")
        confirmation = self.record(root, 2, payload((9, 9, 5), score=9.5))
        self.assertEqual(confirmation["outcome"], "confirmation_failed")
        self.assertIsNone(self.state(root)["pending_confirmation"])

    def test_cli_rejects_old_score_only_review(self):
        root = self.prepare("旧格式不放行")
        self.record(root, 1, {"score": 9.5, "verdict": "experiment_ready", "fatal_blockers": []}, succeeds=False)
        self.assertIsNone(self.state(root)["pending_confirmation"])
        self.assertIsNone(self.state(root)["last_reviewer_score"])

    def test_shared_files_match_installed_copy(self):
        installed = Path("C:/Users/30473/.codex/skills/idea-improvement-loop")
        for relative in ("references/贡献评判标准.md", "templates/reviewer-prompt.md", "templates/improved-idea-template.md"):
            with self.subTest(relative=relative):
                self.assertEqual((SKILL_DIR / relative).read_text(encoding="utf-8"),
                                 (installed / relative).read_text(encoding="utf-8"))


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ContributionGateTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    (TASK_DIR / "验证结果.json").write_text(json.dumps({
        "通过": result.wasSuccessful(), "用例数": result.testsRun,
        "失败数": len(result.failures), "错误数": len(result.errors),
        "场景目录": str(ContributionGateTests.run_dir),
        "说明": "合成评审验证，仅覆盖规则和程序流程；未运行真实研究审查。",
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    raise SystemExit(0 if result.wasSuccessful() else 1)
