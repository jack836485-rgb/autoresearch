"""直接比较技能副本内容，并通过安装入口读取已有模拟状态；不使用哈希。"""
from pathlib import Path
import json
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
SLOT = Path(__file__).resolve().parent
PROJECT = SLOT.parents[1]
SOURCE = PROJECT / "skills/idea-improvement-loop"
INSTALLED = Path.home() / ".codex/skills/idea-improvement-loop"
copies = {
    "仓库Codex副本": PROJECT / "skills/skills-codex/idea-improvement-loop",
    "Claude主入口": PROJECT / ".claude/skills/idea-improvement-loop",
    "Claude的Codex入口": PROJECT / ".claude/skills/skills-codex/idea-improvement-loop",
    "当前Codex安装入口": INSTALLED,
}
files = [path.relative_to(SOURCE) for path in SOURCE.rglob("*") if path.is_file()]
results = {}
for name, directory in copies.items():
    differences = [str(path) for path in files if not (directory / path).is_file()
                   or (SOURCE / path).read_bytes() != (directory / path).read_bytes()]
    assert not differences, (name, differences)
    results[name] = {"核对文件数": len(files), "内容一致": True, "实际目录": str(directory.resolve())}

run = max(SLOT.glob("回归现场_*"), key=lambda path: path.stat().st_mtime)
root = run / "test_default_budget_and_two_review_gate"
smoke = subprocess.run(
    [sys.executable, "-X", "utf8", str(INSTALLED / "tools/loop_state.py"),
     "--root", str(root), "status", "--slug", "demo"],
    capture_output=True, encoding="utf-8", cwd=PROJECT,
)
assert smoke.returncode == 0, smoke.stderr
state, _ = json.JSONDecoder().raw_decode(smoke.stdout)
assert state["gate_passed"] is True and state["reviewer_calls_used"] == 2, state
results["安装入口调用"] = {"结果": "通过", "状态来源": "已有模拟双审现场", "状态": state}
output = json.dumps(results, ensure_ascii=False, indent=2)
(SLOT / "同步验证结果.json").write_text(output, encoding="utf-8")
print(output)
