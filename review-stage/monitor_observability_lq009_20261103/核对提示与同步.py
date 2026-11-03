"""核对 skill 副本；补读 HTML 抽取遗漏的原始提示框，不运行模型实验。"""
from pathlib import Path
import json
import re
import sys
import urllib.request
from html.parser import HTMLParser
import html

sys.stdout.reconfigure(encoding="utf-8")
REVIEW = Path(__file__).resolve().parent
ROOT = REVIEW.parents[1]
SOURCE = ROOT / "skills/idea-improvement-loop"


def sync_check():
    files = [p.relative_to(SOURCE) for p in SOURCE.rglob("*") if p.is_file()]
    copies = [ROOT / "skills/skills-codex/idea-improvement-loop",
              Path.home() / ".codex/skills/idea-improvement-loop",
              ROOT / ".claude/skills/idea-improvement-loop"]
    results = []
    for target in copies:
        differences = [str(p) for p in files if not (target / p).is_file()
                       or (SOURCE / p).read_bytes() != (target / p).read_bytes()]
        assert not differences, (str(target), differences)
        results.append({"入口": str(target), "文件数": len(files), "内容一致": True})
    output = json.dumps(results, ensure_ascii=False, indent=2)
    (REVIEW / "技能同步验证.json").write_text(output, encoding="utf-8")
    print(output)


def source_prompt():
    url = "https://arxiv.org/html/2605.12366v1"
    request = urllib.request.Request(url, headers={"User-Agent": "idea-improvement-loop research source verification"})
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            page = response.read().decode("utf-8")
    except Exception as exc:
        text = f"来源：{url}\n原始HTML获取失败：{exc}\n不能把获取失败当作原文没有提示。\n"
    else:
        marker = page.find('A.2.4')
        positions = [match.start() for match in re.finditer("Reminder Prompt", page)]
        if positions:
            marker = positions[-1]
        snippet = page[max(0, marker-300):marker+16000]
        class Text(HTMLParser):
            def __init__(self):
                super().__init__()
                self.parts = []
            def handle_data(self, data):
                self.parts.append(data)
        parser = Text()
        parser.feed(snippet)
        text = "来源：" + url + "\n\n" + re.sub(r"\s+", " ", html.unescape(" ".join(parser.parts)))
    (REVIEW / "原文提醒提示核对.txt").write_text(text, encoding="utf-8")
    print(text[:12000])


if "--source" in sys.argv:
    source_prompt()
else:
    sync_check()
