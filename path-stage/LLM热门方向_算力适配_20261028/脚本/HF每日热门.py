# -*- coding: utf-8 -*-
"""阶段 fetch：拉取窗口内每天的 Hugging Face 每日论文（标题、摘要、赞数、作者、机构字段如有）。
阶段 gap：用主题表的检索词在本地匹配，统计"LLM 相关但不落入任何主题"的论文的高频短语与高赞标题，用于发现旧主题表漏掉的方向。
用法：python HF每日热门.py fetch <输出.json>；python HF每日热门.py gap <输入.json> <输出.md>"""
import json, re, sys, time, datetime, collections, urllib.request
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

START, END = datetime.date(2026, 4, 28), datetime.date(2026, 10, 28)

def get(url):
    for a in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "landscape-search/1.0"}), timeout=60) as r:
                return json.loads(r.read())
        except Exception:
            time.sleep(5 * (a + 1))
    return None

def fetch(out):
    res, fails = {}, []
    d = START
    while d <= END:
        j = get(f"https://huggingface.co/api/daily_papers?date={d.isoformat()}&limit=100")
        if j is None:
            fails.append(d.isoformat())
        else:
            for it in j:
                p = it.get("paper", it)
                aid = p.get("id")
                if not aid or aid in res:
                    continue
                res[aid] = {"id": aid, "title": " ".join((p.get("title") or "").split()),
                            "summary": " ".join((p.get("summary") or "").split()),
                            "upvotes": p.get("upvotes", it.get("upvotes", 0)) or 0,
                            "publishedAt": (p.get("publishedAt") or "")[:10], "hf_date": d.isoformat(),
                            "org": (it.get("organization") or p.get("organization") or {}).get("fullname") if isinstance(it.get("organization") or p.get("organization"), dict) else None}
        d += datetime.timedelta(days=1)
        time.sleep(0.5)
    Path(out).write_text(json.dumps({"fails": fails, "papers": list(res.values())}, ensure_ascii=False), encoding="utf-8")
    print("papers", len(res), "failed days", len(fails))

def topic_regex(expr):
    terms = re.findall(r'abs:"([^"]+)"|abs:([\w\-]+)', expr)
    words = [a or b for a, b in terms]
    return re.compile("|".join(r"\b" + re.escape(w).replace(r"\-", "[- ]?").replace(r"\ ", "[- ]") + r"\b" for w in words), re.I)

def gap(inp, out):
    from 主题定义 import TOPICS
    j = json.loads(Path(inp).read_text(encoding="utf-8"))
    ps = j["papers"]
    LLMre = re.compile(r"\b(language models?|LLMs?|reasoning model|agentic|agents?)\b", re.I)
    trs = {k: topic_regex(v) for k, v in TOPICS.items()}
    llm = [p for p in ps if LLMre.search(p["title"] + " " + p["summary"])]
    hit = collections.Counter(); unmatched = []
    up = collections.Counter()
    for p in llm:
        txt = p["title"] + " " + p["summary"]
        ms = [k for k, r in trs.items() if r.search(txt)]
        for k in ms:
            hit[k] += 1; up[k] += p["upvotes"]
        if not ms:
            unmatched.append(p)
    stop = set("a an the of for in on to and with via from by is are as at be we our this that its their into towards toward using based large language model models llm llms agent agents new learning".split())
    bg = collections.Counter(); bgup = collections.Counter()
    for p in unmatched:
        ws = [w for w in re.findall(r"[a-z][a-z\-]+", p["title"].lower())]
        for a, b in zip(ws, ws[1:]):
            if a in stop or b in stop:
                continue
            bg[a + " " + b] += 1; bgup[a + " " + b] += p["upvotes"]
    lines = [f"# HF 每日热门开放式查漏（{START} 至 {END}）", "",
             f"- 拉取论文 {len(ps)} 篇，失败日期 {len(j['fails'])} 天；LLM / agent 相关 {len(llm)} 篇；不落入任何主题 {len(unmatched)} 篇。",
             "- 主题匹配是本地关键词近似（标题+摘要），与 arXiv 检索式不完全等价；只用于发现漏掉的方向。", "",
             "## 各主题命中（篇数 / 总赞数）", "", "| 主题 | 篇数 | 总赞数 |", "|---|---|---|"]
    for k, v in hit.most_common():
        lines.append(f"| {k} | {v} | {up[k]} |")
    lines += ["", "## 未匹配论文标题中的高频二元短语（出现 ≥4 次，按次数）", "", "| 短语 | 次数 | 总赞数 |", "|---|---|---|"]
    for k, v in bg.most_common(60):
        if v >= 4:
            lines.append(f"| {k} | {v} | {bgup[k]} |")
    lines += ["", "## 未匹配论文中赞数最高的 40 篇", "", "| arXiv | 赞 | 标题 |", "|---|---|---|"]
    for p in sorted(unmatched, key=lambda x: -x["upvotes"])[:40]:
        lines.append(f"| {p['id']} | {p['upvotes']} | {p['title']} |")
    Path(out).write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))

if __name__ == "__main__":
    if sys.argv[1] == "fetch":
        fetch(sys.argv[2])
    else:
        gap(sys.argv[2], sys.argv[3])
