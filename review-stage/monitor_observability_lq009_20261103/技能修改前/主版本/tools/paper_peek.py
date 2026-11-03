#!/usr/bin/env python3
"""查看 arXiv 论文的标题、作者、日期、摘要和代码链接；可在 HTML 全文中按关键词取片段。

用法:
  python tools/paper_peek.py 2610.21633 2604.25891
  python tools/paper_peek.py 2610.21633 --grep Limitations residual --window 500 --max-hits 2

只用标准库。抓取失败的论文会打印错误并继续处理下一篇。
"""
from __future__ import annotations

import argparse
import html
import re
import sys
import urllib.request

UA = {"User-Agent": "idea-improvement-loop/1.0 (research use)"}
LINK_RE = re.compile(r'https?://(?:github\.com|huggingface\.co)/[^"<>\s)]+')
LINK_NOISE = ("github.com/arXiv/", "github.com/brucemiller/", "huggingface.co/docs/", "huggingface.co/huggingface")


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read().decode("utf-8", "replace")


def to_text(fragment: str) -> str:
    fragment = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", fragment, flags=re.S)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", fragment))).strip()


def first(pattern: str, page: str) -> str:
    match = re.search(pattern, page, re.S)
    return to_text(match.group(1)) if match else ""


def code_links(page: str) -> list[str]:
    return sorted({u.rstrip(".,;") for u in LINK_RE.findall(page) if not u.startswith(tuple("https://" + n for n in LINK_NOISE))})


def peek(arxiv_id: str, keywords: list[str], window: int, max_hits: int) -> None:
    page = fetch(f"https://arxiv.org/abs/{arxiv_id}")
    print(f"## {arxiv_id}")
    print("标题:", first(r'<h1 class="title[^>]*>(.*?)</h1>', page).removeprefix("Title:").strip())
    print("作者:", first(r'<div class="authors">(.*?)</div>', page).removeprefix("Authors:").strip()[:300])
    print("日期:", first(r"(\[Submitted on [^\]]*\])", page))
    print("摘要:", first(r'<blockquote class="abstract[^>]*>(.*?)</blockquote>', page).removeprefix("Abstract:").strip())
    links = code_links(page)
    if keywords:
        try:
            full = fetch(f"https://arxiv.org/html/{arxiv_id}")
        except Exception as exc:  # 没有 HTML 版本的论文很常见
            print(f"全文: 无法获取 HTML 版本（{exc}）")
        else:
            links = sorted(set(links) | set(code_links(full)))
            text = to_text(full)
            for kw in keywords:
                hits = [m.start() for m in re.finditer(re.escape(kw), text, re.I)]
                if not hits:
                    print(f"### 关键词「{kw}」: 未命中")
                    continue
                # 报告全文总命中数和每处所在位置，避免把"只显示了前几处"误读成"全文只有几处"
                where = ", ".join(f"{100 * pos // len(text)}%" for pos in hits)
                print(f"### 关键词「{kw}」: 全文共 {len(hits)} 处（位置 {where}），显示前 {min(max_hits, len(hits))} 处")
                for pos in hits[:max_hits]:
                    print("…" + text[max(0, pos - window // 3): pos + window] + "…")
    print("代码链接:", ", ".join(links) if links else "未找到")
    print()


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("ids", nargs="+", help="arXiv ID，如 2610.21633")
    parser.add_argument("--grep", nargs="*", default=[], help="在 HTML 全文中查找的关键词")
    parser.add_argument("--window", type=int, default=450, help="每个片段的字符数")
    parser.add_argument("--max-hits", type=int, default=2, help="每个关键词最多显示几处")
    args = parser.parse_args()
    for arxiv_id in args.ids:
        try:
            peek(arxiv_id, args.grep, args.window, args.max_hits)
        except Exception as exc:
            print(f"## {arxiv_id}\n抓取失败: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
