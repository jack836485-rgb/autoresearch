#!/usr/bin/env python3
"""读取公开研究页的正文、链接和引用元数据；供搜索接口不可用时使用。

只读取传入 URL，不爬取下一页，不判定论文的机构资格或研究质量。
依赖 beautifulsoup4。默认输出 JSON；需要保存时由调用方传入文件位置。
"""

import argparse
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

from bs4 import BeautifulSoup


def parse_page(body, url, max_chars=14000, max_links=80, link_pattern=None):
    soup = BeautifulSoup(body, "html.parser")
    title = soup.title.get_text(" ", strip=True) if soup.title else ""
    metadata = {}
    for tag in soup.find_all("meta"):
        name = tag.get("name") or tag.get("property") or ""
        if name.startswith(("citation_", "dc.", "DC.", "article:")):
            metadata.setdefault(name, []).append(tag.get("content", ""))

    for tag in soup(["script", "style", "nav", "footer", "noscript"]):
        tag.decompose()
    text = " ".join(soup.get_text(" ", strip=True).split())
    paper = None
    article = soup.select_one("article.ltx_document")
    if article:
        paper_title = article.select_one(".ltx_title_document")
        document_title = paper_title.get_text(" ", strip=True) if paper_title else title
        # 部分 arXiv 转换结果把首个 Introduction 标为 document title。
        if re.fullmatch(r"\d*\s*Introduction", document_title, re.I):
            document_title = None if re.fullmatch(r"\d*\s*Introduction", title, re.I) else title
        abstract = article.select_one(".ltx_abstract")
        author_block = article.select_one(".ltx_authors")
        authors = []
        for author in article.select(".ltx_authors .ltx_creator.ltx_role_author"):
            name = author.select_one(".ltx_personname")
            authors.append({
                "name": name.get_text(" ", strip=True) if name else "",
                "affiliations": [tag.get_text(" ", strip=True) for tag in author.select(".ltx_role_affiliation")],
                "notes": [tag.get_text(" ", strip=True) for tag in author.select(".ltx_role_contribution")],
            })
        version = re.search(
            r"arXiv:(\d{4}\.\d{4,5}v\d+)\s+\[[^\]]+\]\s+(\d{1,2}\s+[A-Z][a-z]{2}\s+\d{4})",
            text,
        )
        paper = {
            "title": document_title,
            "title_warning": "网页与文档标题均为章节名，请从正文前部或 PDF 核实论文标题。" if document_title is None else None,
            "abstract": abstract.get_text(" ", strip=True) if abstract else "",
            "authors": authors,
            "author_block": author_block.get_text(" ", strip=True) if author_block else "",
            "arxiv_version": version.group(1) if version else None,
            "arxiv_version_date": datetime.strptime(version.group(2), "%d %b %Y").date().isoformat() if version else None,
        }
        # 完整章节供 检索片段.py 在本地检索，不受 max_chars 截断。
        sections = []
        for section in article.select("section"):
            heading = section.find(["h2", "h3", "h4", "h5", "h6"], recursive=False)
            body_text = " ".join(
                child.get_text(" ", strip=True) for child in section.children
                if getattr(child, "name", None) not in ("section", None) and child is not heading
            )
            if body_text:
                sections.append({
                    "id": section.get("id"),
                    "heading": heading.get_text(" ", strip=True) if heading else section.get("id"),
                    "level": min(int(heading.name[1]) - 1, 4) if heading else 4,
                    "text": " ".join(body_text.split()),
                })
        paper["sections"] = sections
    pattern = re.compile(link_pattern, re.I) if link_pattern else None
    links = []
    invalid_links = []
    seen = set()
    for anchor in soup.select("a[href]"):
        try:
            target = urllib.parse.urljoin(url, anchor["href"])
        except ValueError as exc:
            invalid_links.append({"href": anchor["href"], "error": str(exc)})
            continue
        label = " ".join(anchor.get_text(" ", strip=True).split())
        if not target.startswith(("https://", "http://")):
            continue
        if pattern and not pattern.search(label + " " + target):
            continue
        if target in seen:
            continue
        seen.add(target)
        links.append({"text": label, "url": target})
    return {
        "title": title,
        "metadata": metadata,
        "paper": paper,
        "text": text[:max_chars],
        "text_truncated": len(text) > max_chars,
        "links": links[:max_links],
        "matching_link_count": len(links),
        "links_truncated": len(links) > max_links,
        "invalid_links": invalid_links,
    }


def read_page(url, timeout=25, **options):
    request = urllib.request.Request(
        url, headers={"User-Agent": "ai-frontier-search/1.0", "Accept": "text/html"}
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read()
            content_type = response.headers.get("Content-Type", "")
            final_url = response.url
            status = response.status
        if "html" not in content_type.lower() and not body.lstrip().lower().startswith(
            (b"<!doctype html", b"<html")
        ):
            return {
                "url": url,
                "final_url": final_url,
                "status": status,
                "error": "响应不是 HTML；PDF 或 API 响应需使用对应读取工具。",
                "content_type": content_type,
            }
        return {
            "url": url,
            "final_url": final_url,
            "status": status,
            **parse_page(body, final_url, **options),
        }
    except urllib.error.HTTPError as exc:
        return {"url": url, "status": exc.code, "error": str(exc)}
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return {"url": url, "error": str(exc)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url", help="要读取的公开研究页 URL")
    parser.add_argument("--max-chars", type=int, default=14000)
    parser.add_argument("--max-links", type=int, default=80)
    parser.add_argument("--link-pattern", help="仅保留匹配该正则的链接，可用于提取论文或分页链接")
    parser.add_argument("--timeout", type=float, default=25)
    parser.add_argument("--output", help="可选 JSON 文件；由调用方指定独立目录")
    args = parser.parse_args()
    if args.max_chars < 1 or args.max_links < 1 or args.timeout <= 0:
        parser.error("正文长度、链接数量和超时必须大于零")
    try:
        result = read_page(
            args.url, timeout=args.timeout, max_chars=args.max_chars,
            max_links=args.max_links, link_pattern=args.link_pattern,
        )
    except re.error as exc:
        parser.error(f"链接正则无效：{exc}")
    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        target = Path(args.output)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(rendered + "\n", encoding="utf-8")
        # 已落盘时正文只留在文件里，需要时用 检索片段.py 定向读取。
        brief = {key: value for key, value in result.items() if key != "text"}
        brief["text_chars"] = len(result.get("text", ""))
        if result.get("paper"):
            brief["paper"] = {key: value for key, value in result["paper"].items() if key != "sections"}
            brief["paper"]["section_count"] = len(result["paper"]["sections"])
        rendered = json.dumps(brief, ensure_ascii=False, indent=2)
    print(rendered)
    return 1 if "error" in result else 0


if __name__ == "__main__":
    sys.exit(main())
