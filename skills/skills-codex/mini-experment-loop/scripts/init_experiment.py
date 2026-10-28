#!/usr/bin/env python3
"""Initialize auditable control files for a mini experiment workspace."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SLOT_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
ROOT_TEMPLATES = (
    "EXPERIMENT_CONTRACT.yaml",
    "EXPERIMENT_STATE.json",
    "REQUIREMENTS.jsonl",
    "PROJECT.md",
)
SCHEMA_TEMPLATES = (
    "CONTENT_MANIFEST.example.json",
    "REQUIREMENT_RECORD.example.json",
    "RUN_RECORD.example.json",
    "GATE_REPORT.example.json",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", required=True, type=Path)
    parser.add_argument("--slot", required=True)
    parser.add_argument("--idea-path", required=True, type=Path)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def replace_json_tokens(value: Any, tokens: dict[str, str]) -> Any:
    if isinstance(value, str):
        for key, replacement in tokens.items():
            value = value.replace("{{" + key + "}}", replacement)
        return value
    if isinstance(value, list):
        return [replace_json_tokens(item, tokens) for item in value]
    if isinstance(value, dict):
        return {key: replace_json_tokens(item, tokens) for key, item in value.items()}
    return value


def render(template: Path, tokens: dict[str, str]) -> str:
    text = template.read_text(encoding="utf-8")
    if template.suffix == ".json":
        data = json.loads(text)
        data = replace_json_tokens(data, tokens)
        return json.dumps(data, indent=2, sort_keys=False) + "\n"
    if template.suffix in {".yaml", ".yml"}:
        for key, replacement in tokens.items():
            quoted_token = '"{{' + key + '}}"'
            text = text.replace(quoted_token, json.dumps(replacement))
        return text
    for key, replacement in tokens.items():
        text = text.replace("{{" + key + "}}", replacement)
    return text


def lstat_or_none(path: Path) -> os.stat_result | None:
    try:
        return path.lstat()
    except FileNotFoundError:
        return None


def ensure_safe_directory(path: Path, trusted_root: Path, *, create: bool) -> None:
    """Ensure every component below trusted_root is a real directory, never a symlink."""
    try:
        relative = path.relative_to(trusted_root)
    except ValueError as error:
        raise ValueError(f"directory escapes trusted root: {path}") from error

    current = trusted_root
    for component in relative.parts:
        current = current / component
        metadata = lstat_or_none(current)
        if metadata is None:
            if create:
                current.mkdir(mode=0o755)
            continue
        if stat.S_ISLNK(metadata.st_mode):
            raise ValueError(f"refusing symlinked directory component: {current}")
        if not stat.S_ISDIR(metadata.st_mode):
            raise ValueError(f"directory component is not a directory: {current}")


def validate_existing_destination(path: Path) -> bool:
    """Return True for an existing regular file; reject all other existing objects."""
    metadata = lstat_or_none(path)
    if metadata is None:
        return False
    if stat.S_ISLNK(metadata.st_mode):
        raise ValueError(f"refusing symlinked destination: {path}")
    if not stat.S_ISREG(metadata.st_mode):
        raise ValueError(f"destination is not a regular file: {path}")
    return True


def write_exclusive(path: Path, content: str, trusted_root: Path) -> None:
    """Create a file through no-follow directory descriptors to close symlink races."""
    relative_parent = path.parent.relative_to(trusted_root)
    directory_flags = os.O_RDONLY
    if hasattr(os, "O_DIRECTORY"):
        directory_flags |= os.O_DIRECTORY
    if hasattr(os, "O_NOFOLLOW"):
        directory_flags |= os.O_NOFOLLOW
    directory_fd = os.open(trusted_root, directory_flags)
    try:
        for component in relative_parent.parts:
            next_fd = os.open(component, directory_flags, dir_fd=directory_fd)
            os.close(directory_fd)
            directory_fd = next_fd

        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
        if hasattr(os, "O_NOFOLLOW"):
            flags |= os.O_NOFOLLOW
        descriptor = os.open(path.name, flags, 0o644, dir_fd=directory_fd)
        try:
            payload = content.encode("utf-8")
            offset = 0
            while offset < len(payload):
                written = os.write(descriptor, payload[offset:])
                if written == 0:
                    raise OSError("zero-byte write while creating control artifact")
                offset += written
            os.fsync(descriptor)
        finally:
            os.close(descriptor)
    finally:
        os.close(directory_fd)


def experiment_target(repo_root: Path, slot: str) -> Path:
    if not SLOT_RE.fullmatch(slot) or slot in {".", ".."}:
        raise ValueError("slot must be one safe directory name")
    experiments_root = repo_root / "experiments"
    metadata = lstat_or_none(experiments_root)
    if metadata is not None and stat.S_ISLNK(metadata.st_mode):
        raise ValueError("experiments/ must not be a symlink")
    target = experiments_root / slot
    target_metadata = lstat_or_none(target)
    if target_metadata is not None and stat.S_ISLNK(target_metadata.st_mode):
        raise ValueError("experiment directory must not be a symlink")
    return target


def main() -> int:
    args = parse_args()
    repo_root = args.repo_root.resolve()
    idea_path = args.idea_path.resolve()
    if not repo_root.is_dir():
        print(f"error: repo root is not a directory: {repo_root}", file=sys.stderr)
        return 2
    if not idea_path.is_file():
        print(f"error: idea path is not a file: {idea_path}", file=sys.stderr)
        return 2

    try:
        experiment_dir = experiment_target(repo_root, args.slot)
        ensure_safe_directory(experiment_dir, repo_root, create=not args.dry_run)
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    template_dir = Path(__file__).resolve().parents[1] / "assets" / "templates"
    required = [template_dir / name for name in ROOT_TEMPLATES + SCHEMA_TEMPLATES]
    missing = [path for path in required if not path.is_file()]
    if missing:
        print("error: missing skill templates: " + ", ".join(map(str, missing)), file=sys.stderr)
        return 2

    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    tokens = {
        "SLOT": args.slot,
        "IDEA_PATH": str(idea_path),
        "IDEA_SHA256": sha256(idea_path),
        "EXPERIMENT_DIR": str(experiment_dir),
        "CREATED_AT": now,
    }

    destinations = [(template_dir / name, experiment_dir / name) for name in ROOT_TEMPLATES]
    destinations += [
        (template_dir / name, experiment_dir / "schemas" / name)
        for name in SCHEMA_TEMPLATES
    ]
    runs_file = experiment_dir / "runs" / "RUNS.jsonl"

    try:
        for directory in (
            experiment_dir,
            experiment_dir / "schemas",
            experiment_dir / "runs",
            experiment_dir / "reviews",
        ):
            ensure_safe_directory(directory, repo_root, create=not args.dry_run)

        for source, destination in destinations:
            ensure_safe_directory(destination.parent, repo_root, create=not args.dry_run)
            exists = validate_existing_destination(destination)
            print(f"{'preserve' if exists else 'create'}: {destination}")
            if not args.dry_run and not exists:
                write_exclusive(destination, render(source, tokens), repo_root)

        runs_exists = validate_existing_destination(runs_file)
        print(f"{'preserve' if runs_exists else 'create'}: {runs_file}")
        if not args.dry_run and not runs_exists:
            write_exclusive(runs_file, "", repo_root)
    except (FileExistsError, OSError, ValueError) as error:
        print(f"error: unsafe or concurrent initialization: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
