# -*- coding: utf-8 -*-
"""把三路并行检索得到的候选卡（资料/扩展候选卡_<路>.json）并入 研究问题.json，并生成主文用的 Markdown 片段。

用法：python 并入扩展卡.py <起始编号> <候选文件1> [候选文件2 ...]
- 候选卡按文件顺序、文件内顺序编号为 Q<起始编号>、Q<起始编号+1> ...
- 研究问题.json 中已有的 Q001–Q010 由 生成研究问题JSON.py 生成，本脚本在其结果上追加
- 片段写到 资料/扩展卡片段.md，由主执行者人工审阅后放入 研究地图.md
"""
import json
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
start = int(sys.argv[1])
cands = []
for f in sys.argv[2:]:
    cands += json.loads(Path(f).read_text(encoding="utf-8"))

data = json.loads((root / "研究问题.json").read_text(encoding="utf-8"))
keep = [q for q in data["研究问题"] if int(q["id"][1:]) < start]

new, md = [], []
for k, c in enumerate(cands):
    qid = f"Q{start + k:03d}"
    evs = [{
        "作品ID": e.get("作品ID"), "标题": e.get("标题"), "机构": e.get("机构") or [],
        "原文链接": e.get("原文链接"), "位置": e.get("位置"), "阅读版本": e.get("阅读版本"),
        "证据角色": e.get("证据角色"), "实验设置": e.get("实验设置"), "变化变量": e.get("变化变量"),
        "对照与保持条件": e.get("对照与保持条件"), "具体观察": e.get("具体观察"),
        "成本口径": e.get("成本口径"), "证据边界": e.get("证据边界"),
    } for e in c["证据"]]
    new.append({
        "id": qid, "具体问题": c["具体问题"], "宏观标签": c.get("宏观标签", []),
        "线索类型": c.get("线索类型", []), "证据": evs,
        "已有解决方法": c.get("已有解决方法", []), "已支持的解释": c.get("已支持的解释", []),
        "待验证解释": c.get("待验证解释", []), "尚未解决": c.get("尚未解决"),
        "可检验切口": c.get("可检验切口"), "已知边界": [c["风险"]] if c.get("风险") else [],
        "解决状态": c.get("解决状态"), "查新状态": c.get("查新状态"),
        "与其他问题的关系": c.get("与其他问题的关系", []),
    })
    lines = [f"### {qid} {c.get('短标题') or c['具体问题'][:40]}", "",
             f"**问题。** {c['具体问题']}", "", "**证据。**", ""]
    for e in c["证据"]:
        lines.append(f"- {e.get('标题')}（{e.get('作品ID')}，{e.get('位置')}）：{e.get('具体观察')}" +
                     (f"〔边界：{e.get('证据边界')}〕" if e.get("证据边界") else ""))
    lines += ["", f"**已有处理。** {'；'.join(c.get('已有解决方法', [])) or '未检出'}", "",
              f"**缺口。** {c.get('尚未解决')}", "", f"**下游切口。** {c.get('可检验切口')}", "",
              f"**查新。** {c.get('查新状态')}", "", f"**风险。** {c.get('风险')}", "",
              f"**为何值得做。** {c.get('为何值得做')}", "", "---", ""]
    md += lines

data["研究问题"] = keep + new
(root / "研究问题.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
(root / "资料" / "扩展卡片段.md").write_text("\n".join(md), encoding="utf-8")
print("合计", len(data["研究问题"]), "张；新增", [q["id"] for q in new])
