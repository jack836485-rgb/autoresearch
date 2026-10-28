"""对被引论文打印作者区中命中白名单／QS 机构名的前后短片段，供核实署名；不输出完整作者区。"""
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "skills/ai-frontier-search/scripts"))
src = (Path(__file__).resolve().parents[3] / "skills/ai-frontier-search/scripts/机构初筛.py").read_text(encoding="utf-8")
ns = {}; exec(src.split("d = Path(sys.argv[1])")[0], ns)
WL, QS = ns["WL"], ns["QS"]
text_dir = Path(sys.argv[1])
for aid in sys.argv[2:]:
    f = text_dir / f"{aid}v1正文.json"
    if not f.exists():
        f = Path(__file__).resolve().parents[2] / "AgenticRL研究地图_20261016/资料/正文v1" / f"{aid}v1正文.json"
    j = json.loads(f.read_text(encoding="utf-8")); p = j.get("paper") or {}
    blk = p.get("author_block") or j.get("text", "")[:4000]
    found = []
    for name, rx in {**WL, **QS}.items():
        m = re.search(rx, blk)
        if m:
            found.append(f"{name}「{blk[max(0, m.start()-25):m.end()+25].strip()}」")
    print(aid, p.get("arxiv_version_date"), "；".join(found[:4]) or "未命中")
