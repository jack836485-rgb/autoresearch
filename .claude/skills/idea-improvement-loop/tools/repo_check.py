#!/usr/bin/env python3
"""核验 baseline 的 GitHub 仓库：是否存在、描述、最近推送时间、目录列表、README 开头。

用法:
  python tools/repo_check.py davidkaczer/contextlift
  python tools/repo_check.py https://github.com/davidkaczer/contextlift --path scripts --readme 2000

未认证的 GitHub API 每小时限 60 次；设置环境变量 GITHUB_TOKEN 可提高限额。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request

API = "https://api.github.com/repos/"


def get(url: str, raw: bool = False):
    headers = {"User-Agent": "idea-improvement-loop/1.0"}
    if raw:
        headers["Accept"] = "application/vnd.github.raw"
    if os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = "Bearer " + os.environ["GITHUB_TOKEN"]
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30) as resp:
        body = resp.read().decode("utf-8", "replace")
    return body if raw else json.loads(body)


def listing(repo: str, path: str) -> str:
    items = get(f"{API}{repo}/contents/{path}")
    if isinstance(items, dict):
        return f"{items.get('name')}（文件，{items.get('size')} 字节）"
    return ", ".join(x["name"] + ("/" if x["type"] == "dir" else "") for x in items)


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("repo", help="owner/repo 或 GitHub URL")
    parser.add_argument("--path", nargs="*", default=[], help="额外列出的子目录或文件")
    parser.add_argument("--readme", type=int, default=0, help="打印 README 的前 N 个字符")
    args = parser.parse_args()

    repo = re.sub(r"^https?://github\.com/", "", args.repo).strip("/").removesuffix(".git")
    repo = "/".join(repo.split("/")[:2])
    try:
        meta = get(API + repo)
    except urllib.error.HTTPError as exc:
        print(f"{repo}: 不可访问（HTTP {exc.code}）")
        return 1
    print(f"仓库: https://github.com/{repo}")
    print(f"描述: {meta.get('description')}")
    print(f"最近推送: {meta.get('pushed_at')}；默认分支: {meta.get('default_branch')}；归档: {meta.get('archived')}")
    print(f"根目录: {listing(repo, '')}")
    for path in args.path:
        try:
            print(f"{path}: {listing(repo, path)}")
        except urllib.error.HTTPError as exc:
            print(f"{path}: 不存在（HTTP {exc.code}）")
    if args.readme:
        try:
            print("README:\n" + get(f"{API}{repo}/readme", raw=True)[: args.readme])
        except urllib.error.HTTPError:
            print("README: 未找到")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
