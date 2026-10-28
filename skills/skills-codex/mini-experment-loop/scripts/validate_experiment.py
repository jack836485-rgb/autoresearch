#!/usr/bin/env python3
"""Validate mini experiment control artifacts before scored review."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import shlex
import stat
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover - reported as a validation error
    yaml = None

try:
    import tomllib
except ImportError:  # pragma: no cover - Python < 3.11 fallback
    try:
        import tomli as tomllib
    except ImportError:  # pragma: no cover - reported when a TOML config is used
        tomllib = None


REQUIRED_FILES = (
    "EXPERIMENT_CONTRACT.yaml",
    "EXPERIMENT_STATE.json",
    "REQUIREMENTS.jsonl",
    "PROJECT.md",
    "runs/RUNS.jsonl",
    "schemas/CONTENT_MANIFEST.example.json",
    "schemas/REQUIREMENT_RECORD.example.json",
    "schemas/RUN_RECORD.example.json",
    "schemas/GATE_REPORT.example.json",
)
REQUIRED_RUN_FIELDS = {
    "schema_version",
    "run_id",
    "purpose",
    "status",
    "command_argv",
    "cwd",
    "started_at",
    "ended_at",
    "exit_code",
    "environment",
    "provenance",
    "config",
    "seeds",
    "scope",
    "stdout_path",
    "stderr_path",
    "raw_artifacts",
    "artifact_hashes",
    "metrics_path",
    "requirement_ids",
    "claim_ids",
    "limitations",
    "redactions",
}
REQUIRED_REQUIREMENT_FIELDS = {
    "schema_version",
    "req_id",
    "strength",
    "type",
    "claim_ids",
    "source",
    "normalized_requirement",
    "implementation",
    "verification",
    "metric_gates",
    "failure_action",
    "status",
    "evidence_artifacts",
    "unresolved_reason",
}
RUN_PURPOSES = {"test", "smoke", "full", "analysis", "dry_run"}
RUN_STATUSES = {"passed", "failed", "cancelled", "unknown"}
REQUIREMENT_STATUSES = {"unmapped", "implemented", "verified", "blocked", "deferred"}
STRENGTHS = {"MUST", "SHOULD", "MAY"}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
LINES_RE = re.compile(r"^(?:L)?([1-9][0-9]*)(?:-(?:L)?([1-9][0-9]*))?$")
SECRET_RE = re.compile(
    r"(?i)(?:api[_-]?key|access[_-]?token|auth[_-]?token|client[_-]?secret|password)[\"']?"
    r"\s*(?:=|:)\s*[\"']?(?!null\b|none\b|redacted\b|<redacted>\b)"
    r"[A-Za-z0-9_./+=-]{8,}"
)
SENSITIVE_OPTIONS = {
    "--api-key",
    "--access-token",
    "--auth-token",
    "--client-secret",
    "--password",
    "--token",
}
PLACEHOLDERS = (
    "{{",
    "<!-- 请填写：",
)
REQUIRED_PROJECT_SECTIONS = (
    "## 1. 先看这里",
    "## 2. 项目架构",
    "## 3. 一次运行是怎么走的",
    "## 4. 怎么运行",
    "## 5. 当前证据和结论边界",
    "## 6. 后续怎么增量扩展",
)
PYTHON_SYMBOL_RE = re.compile(
    r"(?<![A-Za-z0-9_./-])"
    r"([A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*\.py)::"
    r"[A-Za-z_][A-Za-z0-9_.]*(?:\(\))?"
)
EXPECTED_REVIEWER_GATE = {
    "score_operator": ">",
    "score_threshold": 8.0,
    "verdict": "pass",
    "require_postrun_mode": True,
    "require_zero_blocking_findings": True,
    "require_all_must_verified": True,
    "require_evidence_integrity_pass": True,
    "require_required_tests_pass": True,
    "require_canonical_smoke_pass": True,
}
REQUIRED_SCOPE_FIELDS = {
    "is_full_protocol",
    "examples",
    "steps",
    "repeats",
    "smoke_reductions",
}
STATE_STATUSES = {"in_progress", "awaiting_resources", "blocked", "passed"}
STATE_PHASES = {
    "initialized",
    "discovering",
    "awaiting_resources",
    "planning",
    "implementing",
    "testing",
    "reviewing",
    "fixing",
    "passed",
    "blocked",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("experiment_dir", type=Path)
    parser.add_argument("--for-review", action="store_true")
    return parser.parse_args()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def valid_sha256(value: Any) -> bool:
    return isinstance(value, str) and SHA256_RE.fullmatch(value) is not None


def nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def parse_timestamp(value: Any) -> datetime | None:
    if not nonempty_string(value):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None else None


def string_list(value: Any, *, nonempty: bool = False) -> bool:
    return (
        isinstance(value, list)
        and (not nonempty or bool(value))
        and all(nonempty_string(item) for item in value)
    )


def load_json(path: Path, errors: list[str]) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        errors.append(f"invalid JSON {path}: {error}")
        return None


def load_yaml(path: Path, errors: list[str]) -> Any:
    if yaml is None:
        errors.append("PyYAML is required to validate EXPERIMENT_CONTRACT.yaml")
        return None
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as error:
        errors.append(f"invalid YAML {path}: {error}")
        return None


def lstat_regular(path: Path, label: str, errors: list[str]) -> bool:
    try:
        metadata = path.lstat()
    except FileNotFoundError:
        errors.append(f"missing required file: {label}")
        return False
    if stat.S_ISLNK(metadata.st_mode):
        errors.append(f"required path must not be a symlink: {label}")
        return False
    if not stat.S_ISREG(metadata.st_mode):
        errors.append(f"required path is not a regular file: {label}")
        return False
    return True


def internal_file(root: Path, value: Any, label: str, errors: list[str]) -> Path | None:
    if not nonempty_string(value):
        errors.append(f"{label} must be a non-empty relative path")
        return None
    raw = Path(value)
    if raw.is_absolute():
        errors.append(f"{label} must be relative to the experiment directory")
        return None
    candidate = root / raw
    try:
        resolved = candidate.resolve(strict=True)
        resolved.relative_to(root)
    except (FileNotFoundError, OSError, ValueError):
        errors.append(f"{label} is missing or escapes the experiment directory: {value}")
        return None
    try:
        relative = candidate.relative_to(root)
    except ValueError:
        errors.append(f"{label} escapes the experiment directory: {value}")
        return None
    current = root
    for component in relative.parts:
        current = current / component
        try:
            if stat.S_ISLNK(current.lstat().st_mode):
                errors.append(f"{label} traverses a symlink: {value}")
                return None
        except FileNotFoundError:
            errors.append(f"{label} is missing: {value}")
            return None
    if not resolved.is_file():
        errors.append(f"{label} is not a regular file: {value}")
        return None
    return resolved


def internal_directory(root: Path, value: Any, label: str, errors: list[str]) -> Path | None:
    if not nonempty_string(value):
        errors.append(f"{label} must be a non-empty path")
        return None
    candidate = Path(value)
    if not candidate.is_absolute():
        candidate = root / candidate
    try:
        resolved = candidate.resolve(strict=True)
        resolved.relative_to(root)
    except (FileNotFoundError, OSError, ValueError):
        errors.append(f"{label} is missing or escapes the experiment directory: {value}")
        return None
    if not resolved.is_dir():
        errors.append(f"{label} is not a directory: {value}")
        return None
    return resolved


def check_secret(text: str, label: str, errors: list[str]) -> None:
    if SECRET_RE.search(text):
        errors.append(f"possible unredacted credential in {label}")


def validate_project_document(
    root: Path, path: Path, for_review: bool, errors: list[str]
) -> None:
    try:
        content = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        errors.append(f"cannot read PROJECT.md: {error}")
        return

    for heading in REQUIRED_PROJECT_SECTIONS:
        if heading not in content:
            errors.append(f"PROJECT.md missing required section: {heading}")
    if content.count("```mermaid") < 2:
        errors.append("PROJECT.md must contain both architecture and runtime Mermaid diagrams")
    if "flowchart " not in content:
        errors.append("PROJECT.md architecture section must contain a Mermaid flowchart")
    if "sequenceDiagram" not in content:
        errors.append("PROJECT.md runtime section must contain a Mermaid sequenceDiagram")

    check_secret(content, "PROJECT.md", errors)
    if for_review:
        for placeholder in PLACEHOLDERS:
            if placeholder in content:
                errors.append(
                    f"untouched template placeholder in PROJECT.md: {placeholder}"
                )

        mermaid_blocks = re.findall(r"```mermaid\s*(.*?)```", content, flags=re.DOTALL)
        architecture_block = next(
            (block for block in mermaid_blocks if "flowchart " in block), ""
        )
        python_paths = sorted(set(PYTHON_SYMBOL_RE.findall(architecture_block)))
        if len(python_paths) < 8:
            errors.append(
                "PROJECT.md architecture flowchart must name at least 8 real "
                "relative .py::symbol entries"
            )
        for relative in python_paths:
            internal_file(
                root,
                relative,
                f"PROJECT.md architecture Python path {relative}",
                errors,
            )


def check_file_secret(path: Path, label: str, errors: list[str]) -> None:
    tail = ""
    try:
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                text = tail + chunk.decode("utf-8", errors="ignore")
                if SECRET_RE.search(text):
                    errors.append(f"possible unredacted credential in {label}")
                    return
                tail = text[-256:]
    except OSError as error:
        errors.append(f"cannot scan {label} for secrets: {error}")


def safe_secret_reference(value: str) -> bool:
    normalized = value.strip()
    return (
        normalized in {"<REDACTED>", "REDACTED"}
        or normalized.startswith("$")
        or normalized.startswith("env:")
    )


def validate_command_secrets(argv: Any, prefix: str, errors: list[str]) -> None:
    if not isinstance(argv, list):
        return
    for index, argument in enumerate(argv):
        if not isinstance(argument, str):
            continue
        option, separator, inline_value = argument.partition("=")
        if option.lower() not in SENSITIVE_OPTIONS:
            continue
        if separator:
            value = inline_value
        else:
            value = argv[index + 1] if index + 1 < len(argv) and isinstance(argv[index + 1], str) else ""
        if not safe_secret_reference(value):
            errors.append(f"{prefix} command_argv contains an unredacted credential value")


def parse_jsonl(path: Path, label: str, errors: list[str]) -> list[tuple[int, dict[str, Any]]]:
    records: list[tuple[int, dict[str, Any]]] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as error:
        errors.append(f"cannot read {label}: {error}")
        return records
    for line_number, line in enumerate(lines, 1):
        if not line.strip():
            continue
        check_secret(line, f"{label} line {line_number}", errors)
        try:
            value = json.loads(line)
        except json.JSONDecodeError as error:
            errors.append(f"{label} line {line_number}: {error}")
            continue
        if not isinstance(value, dict):
            errors.append(f"{label} line {line_number} must be a JSON object")
            continue
        records.append((line_number, value))
    return records


def load_structured_object(path: Path, label: str, errors: list[str]) -> dict[str, Any] | None:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        errors.append(f"cannot read {label}: {error}")
        return None
    suffix = path.suffix.lower()
    try:
        if suffix == ".json":
            value = json.loads(text)
        elif suffix in {".yaml", ".yml"}:
            if yaml is None:
                errors.append(f"PyYAML is required to parse {label}")
                return None
            value = yaml.safe_load(text)
        elif suffix == ".toml":
            if tomllib is None:
                errors.append(f"tomllib or tomli is required to parse {label}")
                return None
            value = tomllib.loads(text)
        else:
            errors.append(f"{label} must use JSON, YAML, or TOML")
            return None
    except Exception as error:  # parser-specific JSON/YAML/TOML errors
        errors.append(f"cannot parse {label}: {error}")
        return None
    if not isinstance(value, dict):
        errors.append(f"{label} top level must be an object")
        return None
    return value


def validate_provenance_manifest(
    root: Path, provenance: dict[str, Any], prefix: str, errors: list[str]
) -> set[str]:
    path = internal_file(
        root,
        provenance.get("content_manifest_path"),
        f"{prefix} provenance.content_manifest_path",
        errors,
    )
    digest = provenance.get("content_manifest_sha256")
    if not valid_sha256(digest):
        errors.append(f"{prefix} provenance.content_manifest_sha256 must be SHA-256")
    if path is None:
        return set()
    if valid_sha256(digest) and sha256(path) != digest:
        errors.append(f"{prefix} provenance content manifest hash does not match its file")
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        errors.append(f"{prefix} provenance content manifest is invalid JSON: {error}")
        return set()
    if not isinstance(manifest, list) or not manifest:
        errors.append(f"{prefix} provenance content manifest must be a non-empty list")
        return set()
    paths: set[str] = set()
    prior = ""
    for index, item in enumerate(manifest):
        label = f"{prefix} provenance manifest[{index}]"
        if not isinstance(item, dict) or set(item) != {"path", "sha256"}:
            errors.append(f"{label} must contain exactly path and sha256")
            continue
        relative = item.get("path")
        item_digest = item.get("sha256")
        relative_path = Path(relative) if isinstance(relative, str) else None
        if (
            not nonempty_string(relative)
            or relative_path is None
            or not relative_path.parts
            or relative_path.is_absolute()
            or any(part in {".", ".."} for part in relative_path.parts)
        ):
            errors.append(f"{label}.path must be a safe relative path")
            continue
        if relative <= prior:
            errors.append(f"{prefix} provenance manifest must be strictly sorted by path")
        prior = relative
        if relative in paths:
            errors.append(f"{prefix} provenance manifest duplicates {relative}")
        paths.add(relative)
        first = relative_path.parts[0]
        if first in {"runs", "reviews"} or relative == "EXPERIMENT_STATE.json":
            errors.append(f"{label}.path must identify immutable implementation/config input")
        resolved = internal_file(root, relative, f"{label}.path", errors)
        if not valid_sha256(item_digest):
            errors.append(f"{label}.sha256 must be SHA-256")
        elif resolved is not None and sha256(resolved) != item_digest:
            errors.append(f"{label}.sha256 does not match {relative}")
    return paths


def validate_requirement_source(
    record: dict[str, Any],
    line_number: int,
    idea_sha: str | None,
    idea_lines: list[str] | None,
    errors: list[str],
) -> None:
    prefix = f"REQUIREMENTS.jsonl line {line_number}"
    source = record.get("source")
    if not isinstance(source, dict):
        errors.append(f"{prefix} source must be an object")
        return
    if source.get("idea_sha256") != idea_sha:
        errors.append(f"{prefix} source.idea_sha256 does not match the idea file")
    if not nonempty_string(source.get("section")):
        errors.append(f"{prefix} source.section must be non-empty")
    line_ref = source.get("lines")
    match = LINES_RE.fullmatch(line_ref.strip()) if isinstance(line_ref, str) else None
    if match is None:
        errors.append(f"{prefix} source.lines must use start or start-end line numbers")
        return
    start = int(match.group(1))
    end = int(match.group(2) or start)
    if end < start or idea_lines is None or end > len(idea_lines):
        errors.append(f"{prefix} source.lines is outside the idea document")
        return
    expected = hashlib.sha256("\n".join(idea_lines[start - 1 : end]).encode("utf-8")).hexdigest()
    if source.get("text_sha256") != expected:
        errors.append(f"{prefix} source.text_sha256 does not match the referenced lines")


def validate_requirements(
    root: Path,
    records: list[tuple[int, dict[str, Any]]],
    idea_sha: str | None,
    idea_lines: list[str] | None,
    for_review: bool,
    errors: list[str],
) -> tuple[dict[str, int], dict[str, dict[str, Any]]]:
    counts = {
        "must_total": 0,
        "must_verified": 0,
        "must_blocked": 0,
        "should_total": 0,
        "should_verified": 0,
        "may_total": 0,
        "may_verified": 0,
        "deferred": 0,
    }
    requirements_by_id: dict[str, dict[str, Any]] = {}
    for line_number, record in records:
        prefix = f"REQUIREMENTS.jsonl line {line_number}"
        missing = sorted(REQUIRED_REQUIREMENT_FIELDS - set(record))
        if missing:
            errors.append(f"{prefix} missing fields: {', '.join(missing)}")
        req_id = record.get("req_id")
        if not nonempty_string(req_id):
            errors.append(f"{prefix} req_id must be non-empty")
            req_id = f"<line-{line_number}>"
        elif req_id in requirements_by_id:
            errors.append(f"{prefix} duplicates req_id {req_id}")
        else:
            requirements_by_id[req_id] = record
        strength = record.get("strength")
        status = record.get("status")
        if not isinstance(strength, str) or strength not in STRENGTHS:
            errors.append(f"{prefix} strength must be MUST, SHOULD, or MAY")
        else:
            key = strength.lower()
            counts[f"{key}_total"] += 1
            if status == "verified":
                counts[f"{key}_verified"] += 1
            if strength == "MUST" and status == "blocked":
                counts["must_blocked"] += 1
        if not isinstance(status, str) or status not in REQUIREMENT_STATUSES:
            errors.append(f"{prefix} has invalid status")
        if status == "deferred":
            counts["deferred"] += 1
        if record.get("schema_version") != 1:
            errors.append(f"{prefix} schema_version must be 1")
        if not nonempty_string(record.get("type")):
            errors.append(f"{prefix} type must be non-empty")
        if not string_list(record.get("claim_ids")):
            errors.append(f"{prefix} claim_ids must be a list of non-empty strings")
        if not nonempty_string(record.get("normalized_requirement")):
            errors.append(f"{prefix} normalized_requirement must be non-empty")
        if not isinstance(record.get("metric_gates"), list):
            errors.append(f"{prefix} metric_gates must be a list")
        validate_requirement_source(record, line_number, idea_sha, idea_lines, errors)

        implementation = record.get("implementation")
        verification = record.get("verification")
        evidence = record.get("evidence_artifacts")
        if not isinstance(implementation, dict):
            errors.append(f"{prefix} implementation must be an object")
            implementation = {}
        if not isinstance(verification, dict):
            errors.append(f"{prefix} verification must be an object")
            verification = {}
        implementation_files = implementation.get("files", [])
        implementation_symbols = implementation.get("symbols", [])
        verification_tests = verification.get("test_ids", [])
        verification_commands = verification.get("commands", [])
        if not string_list(implementation_files):
            errors.append(f"{prefix} implementation.files must be a string list")
            implementation_files = []
        if not string_list(implementation_symbols):
            errors.append(f"{prefix} implementation.symbols must be a string list")
            implementation_symbols = []
        if not string_list(verification_tests):
            errors.append(f"{prefix} verification.test_ids must be a string list")
            verification_tests = []
        if not string_list(verification_commands):
            errors.append(f"{prefix} verification.commands must be a string list")
            verification_commands = []
        if not isinstance(evidence, list) or not all(nonempty_string(item) for item in evidence):
            errors.append(f"{prefix} evidence_artifacts must be a string list")
            evidence = []

        if status == "verified":
            if not implementation_files:
                errors.append(f"{prefix} verified requirement needs implementation files")
            if not implementation_symbols:
                errors.append(f"{prefix} verified requirement needs implementation symbols")
            if not (verification_tests or verification_commands):
                errors.append(f"{prefix} verified requirement needs a test ID or command")
            if not nonempty_string(verification.get("oracle")):
                errors.append(f"{prefix} verified requirement needs a non-empty oracle")
            if not nonempty_string(record.get("failure_action")):
                errors.append(f"{prefix} verified requirement needs a failure action")
            if not evidence:
                errors.append(f"{prefix} verified requirement needs evidence artifacts")
            elif not any(Path(path).parts and Path(path).parts[0] == "runs" for path in evidence):
                errors.append(f"{prefix} verified requirement needs at least one run evidence path")
            if record.get("unresolved_reason") is not None:
                errors.append(f"{prefix} verified requirement must have null unresolved_reason")
            if for_review and strength == "MUST" and not string_list(
                record.get("claim_ids"), nonempty=True
            ):
                errors.append(f"{prefix} reviewed MUST requirement needs at least one claim ID")
            for index, path in enumerate(implementation_files):
                internal_file(root, path, f"{prefix} implementation.files[{index}]", errors)
            for index, path in enumerate(evidence):
                internal_file(root, path, f"{prefix} evidence_artifacts[{index}]", errors)
        if for_review and strength == "MUST" and status != "verified":
            errors.append(f"{prefix} MUST requirement is not verified")
    return counts, requirements_by_id


def validate_run_paths(root: Path, record: dict[str, Any], prefix: str, errors: list[str]) -> None:
    status = record.get("status")
    if status != "passed":
        return
    referenced: list[str] = []
    for field in ("stdout_path", "stderr_path"):
        value = record.get(field)
        path = internal_file(root, value, f"{prefix} {field}", errors)
        if path is not None and isinstance(value, str):
            referenced.append(value)
            check_file_secret(path, f"{prefix} {field}", errors)
    purpose = record.get("purpose")
    if purpose in ("smoke", "full", "analysis"):
        value = record.get("metrics_path")
        path = internal_file(root, value, f"{prefix} metrics_path", errors)
        if path is not None and isinstance(value, str):
            referenced.append(value)
            check_file_secret(path, f"{prefix} metrics_path", errors)
            if path.suffix.lower() != ".json":
                errors.append(f"{prefix} metrics_path must be a JSON file")
            else:
                load_structured_object(path, f"{prefix} metrics_path", errors)
    raw = record.get("raw_artifacts")
    if purpose in ("smoke", "full") and not string_list(raw, nonempty=True):
        errors.append(f"{prefix} passed {purpose} run needs raw_artifacts")
    if isinstance(raw, list):
        for index, path in enumerate(raw):
            resolved = internal_file(root, path, f"{prefix} raw_artifacts[{index}]", errors)
            if resolved is not None and isinstance(path, str):
                referenced.append(path)
                check_file_secret(resolved, f"{prefix} raw_artifacts[{index}]", errors)
    if isinstance(raw, list) and record.get("metrics_path") in raw:
        errors.append(f"{prefix} metrics_path must be separate from raw_artifacts")
    if len(referenced) != len(set(referenced)):
        errors.append(f"{prefix} passed-run artifact paths must be distinct")
    artifact_hashes = record.get("artifact_hashes")
    if not isinstance(artifact_hashes, dict):
        errors.append(f"{prefix} artifact_hashes must be an object")
        return
    if set(artifact_hashes) != set(referenced):
        errors.append(f"{prefix} artifact_hashes keys must exactly cover passed-run artifacts")
    for relative, digest in artifact_hashes.items():
        resolved = internal_file(root, relative, f"{prefix} artifact_hashes[{relative!r}]", errors)
        if not valid_sha256(digest):
            errors.append(f"{prefix} artifact hash for {relative!r} must be SHA-256")
        elif resolved is not None and sha256(resolved) != digest:
            errors.append(f"{prefix} artifact hash does not match {relative!r}")


def validate_runs(
    root: Path, records: list[tuple[int, dict[str, Any]]], for_review: bool, errors: list[str]
) -> tuple[dict[str, dict[str, Any]], dict[str, set[str]]]:
    by_id: dict[str, dict[str, Any]] = {}
    manifests: dict[str, set[str]] = {}
    for line_number, record in records:
        prefix = f"RUNS.jsonl line {line_number}"
        missing = sorted(REQUIRED_RUN_FIELDS - set(record))
        if missing:
            errors.append(f"{prefix} missing fields: {', '.join(missing)}")
        run_id = record.get("run_id")
        if not nonempty_string(run_id):
            errors.append(f"{prefix} run_id must be non-empty")
        elif run_id in by_id:
            errors.append(f"{prefix} duplicates run_id {run_id}")
        else:
            by_id[run_id] = record
        if record.get("schema_version") != 1:
            errors.append(f"{prefix} schema_version must be 1")
        purpose = record.get("purpose")
        run_status = record.get("status")
        if not isinstance(purpose, str) or purpose not in RUN_PURPOSES:
            errors.append(f"{prefix} has invalid purpose")
        if not isinstance(run_status, str) or run_status not in RUN_STATUSES:
            errors.append(f"{prefix} has invalid status")
        if not string_list(record.get("command_argv"), nonempty=True):
            errors.append(f"{prefix} command_argv must be a non-empty string list")
        else:
            validate_command_secrets(record.get("command_argv"), prefix, errors)
        internal_directory(root, record.get("cwd"), f"{prefix} cwd", errors)
        started = parse_timestamp(record.get("started_at"))
        ended = parse_timestamp(record.get("ended_at"))
        if started is None or ended is None:
            errors.append(f"{prefix} timestamps must be ISO-8601 values with timezone")
        elif ended < started:
            errors.append(f"{prefix} ended_at must not precede started_at")
        if record.get("status") == "passed" and record.get("exit_code") != 0:
            errors.append(f"{prefix} passed run must have exit_code 0")
        for field in ("requirement_ids", "claim_ids", "limitations", "redactions"):
            if not string_list(record.get(field, [])):
                errors.append(f"{prefix} {field} must be a string list")
        environment = record.get("environment")
        provenance = record.get("provenance")
        config = record.get("config")
        scope = record.get("scope")
        for field, value in (
            ("environment", environment),
            ("provenance", provenance),
            ("config", config),
            ("scope", scope),
        ):
            if not isinstance(value, dict):
                errors.append(f"{prefix} {field} must be an object")
        if isinstance(environment, dict):
            if not nonempty_string(environment.get("activation")):
                errors.append(f"{prefix} environment.activation must be non-empty")
            if not nonempty_string(environment.get("python")):
                errors.append(f"{prefix} environment.python must be non-empty")
            if not valid_sha256(environment.get("dependencies_hash")):
                errors.append(f"{prefix} environment.dependencies_hash must be SHA-256")
            if not string_list(environment.get("credential_env_vars", [])):
                errors.append(f"{prefix} environment.credential_env_vars must be a string list")
            if not nonempty_string(environment.get("hardware")):
                errors.append(f"{prefix} environment.hardware must be non-empty")
        if isinstance(provenance, dict):
            if not nonempty_string(provenance.get("code_revision")):
                errors.append(f"{prefix} provenance.code_revision must be non-empty")
            manifest_paths = validate_provenance_manifest(root, provenance, prefix, errors)
            if nonempty_string(run_id):
                manifests[run_id] = manifest_paths
            diff_hash = provenance.get("working_tree_diff_hash")
            if diff_hash is not None and not valid_sha256(diff_hash):
                errors.append(f"{prefix} provenance.working_tree_diff_hash must be null or SHA-256")
            if not isinstance(provenance.get("data_hashes"), dict):
                errors.append(f"{prefix} provenance.data_hashes must be an object")
            elif not all(
                nonempty_string(key) and valid_sha256(value)
                for key, value in provenance["data_hashes"].items()
            ):
                errors.append(f"{prefix} provenance.data_hashes must map identifiers to SHA-256")
            if not isinstance(provenance.get("resource_revisions"), dict):
                errors.append(f"{prefix} provenance.resource_revisions must be an object")
        if isinstance(config, dict) and purpose in ("smoke", "full"):
            config_path = internal_file(root, config.get("path"), f"{prefix} config.path", errors)
            if not valid_sha256(config.get("sha256")):
                errors.append(f"{prefix} config.sha256 must be SHA-256 for experiment runs")
            elif config_path is not None and sha256(config_path) != config.get("sha256"):
                errors.append(f"{prefix} config.sha256 does not match config.path")
            if config_path is not None:
                load_structured_object(config_path, f"{prefix} config.path", errors)
            artifact_values = [
                record.get("stdout_path"),
                record.get("stderr_path"),
                record.get("metrics_path"),
            ]
            if isinstance(record.get("raw_artifacts"), list):
                artifact_values.extend(record["raw_artifacts"])
            artifact_paths = {value for value in artifact_values if isinstance(value, str)}
            if config.get("path") in artifact_paths:
                errors.append(f"{prefix} config.path must be separate from output artifacts")
            if not isinstance(config.get("overrides"), dict):
                errors.append(f"{prefix} config.overrides must be an object")
        seeds = record.get("seeds")
        if not isinstance(seeds, dict):
            errors.append(f"{prefix} seeds must be an object")
        elif purpose in ("smoke", "full") and not seeds:
            errors.append(f"{prefix} experiment run needs at least one explicit seed")
        if isinstance(scope, dict):
            missing_scope = sorted(REQUIRED_SCOPE_FIELDS - set(scope))
            if missing_scope:
                errors.append(f"{prefix} scope missing fields: {', '.join(missing_scope)}")
            if not isinstance(scope.get("is_full_protocol"), bool):
                errors.append(f"{prefix} scope.is_full_protocol must be boolean")
            for field in ("examples", "steps", "repeats"):
                value = scope.get(field)
                if value is not None and (
                    not isinstance(value, int) or isinstance(value, bool) or value < 0
                ):
                    errors.append(f"{prefix} scope.{field} must be null or a non-negative integer")
            if not string_list(scope.get("smoke_reductions", [])):
                errors.append(f"{prefix} scope.smoke_reductions must be a string list")
            if (
                record.get("purpose") == "smoke"
                and scope.get("is_full_protocol") is not False
            ):
                errors.append(f"{prefix} smoke scope must set is_full_protocol=false")
            if record.get("purpose") == "smoke" and not string_list(
                scope.get("smoke_reductions"), nonempty=True
            ):
                errors.append(f"{prefix} smoke run must name at least one scope reduction")
        if record.get("purpose") == "smoke" and not string_list(
            record.get("claim_ids"), nonempty=True
        ):
            errors.append(f"{prefix} smoke run needs at least one claim ID")
        validate_run_paths(root, record, prefix, errors)
    return by_id, manifests


def validate_idea(
    state: dict[str, Any], contract: dict[str, Any], errors: list[str]
) -> tuple[str | None, list[str] | None]:
    idea = state.get("idea")
    source = contract.get("source")
    if not isinstance(idea, dict):
        errors.append("state.idea must be an object")
        idea = {}
    if not isinstance(source, dict):
        errors.append("contract.source must be an object")
        source = {}
    state_path = idea.get("path")
    contract_path = source.get("idea_path")
    if state_path != contract_path or not nonempty_string(state_path):
        errors.append("state and contract idea paths must match and be non-empty")
        return None, None
    idea_path = Path(state_path).expanduser()
    try:
        actual_sha = sha256(idea_path)
        idea_lines = idea_path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as error:
        errors.append(f"cannot read recorded idea path: {error}")
        return None, None
    if idea.get("sha256") != actual_sha:
        errors.append("state idea SHA-256 does not match the current idea file")
    if source.get("idea_sha256") != actual_sha:
        errors.append("contract idea SHA-256 does not match the current idea file")
    return actual_sha, idea_lines


def validate_contract(contract: dict[str, Any], for_review: bool, errors: list[str]) -> set[str]:
    if contract.get("schema_version") != 1:
        errors.append("contract.schema_version must be 1")
    task = contract.get("task")
    acceptance = contract.get("acceptance")
    claims = contract.get("claims")
    if not isinstance(task, dict):
        errors.append("contract.task must be an object")
        task = {}
    if not isinstance(acceptance, dict):
        errors.append("contract.acceptance must be an object")
        acceptance = {}
    if not isinstance(claims, list):
        errors.append("contract.claims must be a list")
        claims = []
    if for_review:
        if task.get("type") not in ("benchmark", "method", "hybrid"):
            errors.append("review gate requires contract.task.type benchmark, method, or hybrid")
        if not claims:
            errors.append("review gate requires at least one frozen claim")
        for field in ("smoke_command", "full_command"):
            value = acceptance.get(field)
            if not (nonempty_string(value) or string_list(value, nonempty=True)):
                errors.append(f"review gate requires acceptance.{field}")
        if command_argv_list(acceptance.get("required_test_commands")) is None:
            errors.append("review gate requires unique acceptance.required_test_commands")
        gate = acceptance.get("reviewer_gate")
        if not isinstance(gate, dict):
            errors.append("acceptance.reviewer_gate must be an object")
        else:
            for key, expected in EXPECTED_REVIEWER_GATE.items():
                actual = gate.get(key)
                if isinstance(expected, float):
                    matches = (
                        isinstance(actual, (int, float))
                        and not isinstance(actual, bool)
                        and math.isclose(float(actual), expected)
                    )
                else:
                    matches = actual == expected
                if not matches:
                    errors.append(f"acceptance.reviewer_gate.{key} must equal {expected!r}")
    claim_ids: set[str] = set()
    for index, claim in enumerate(claims):
        if not isinstance(claim, dict) or not nonempty_string(claim.get("claim_id")):
            errors.append(f"contract.claims[{index}] must be an object with a non-empty claim_id")
            continue
        claim_id = claim["claim_id"]
        if claim_id in claim_ids:
            errors.append(f"contract.claims duplicates claim_id {claim_id}")
        claim_ids.add(claim_id)
    return claim_ids


def validate_state_schema(
    state: dict[str, Any], root: Path, for_review: bool, errors: list[str]
) -> None:
    if state.get("schema_version") != 1:
        errors.append("state.schema_version must be 1")
    if state.get("slot") != root.name:
        errors.append("state.slot must equal the experiment directory name")
    if state.get("experiment_dir") != str(root):
        errors.append("state.experiment_dir must equal the canonical experiment directory")
    state_status = state.get("status")
    state_phase = state.get("phase")
    state_task_type = state.get("task_type")
    if not isinstance(state_status, str) or state_status not in STATE_STATUSES:
        errors.append("state.status must use the stable enum")
    if not isinstance(state_phase, str) or state_phase not in STATE_PHASES:
        errors.append("state.phase must use the stable enum")
    if state_task_type is not None and state_task_type not in (
        "benchmark", "method", "hybrid"
    ):
        errors.append("state.task_type must be null, benchmark, method, or hybrid")
    for field in ("active_jobs", "pending_actions", "blockers"):
        if not isinstance(state.get(field), list):
            errors.append(f"state.{field} must be a list")
    for field in ("created_at", "updated_at"):
        if parse_timestamp(state.get(field)) is None:
            errors.append(f"state.{field} must be an ISO-8601 timestamp with timezone")

    resource_gate = state.get("resource_gate")
    if not isinstance(resource_gate, dict):
        errors.append("state.resource_gate must be an object")
        resource_gate = {}
    resource_status = resource_gate.get("status")
    if not isinstance(resource_status, str) or resource_status not in (
        "unknown",
        "awaiting",
        "satisfied",
        "blocked",
    ):
        errors.append("state.resource_gate.status must use the stable enum")
    if not isinstance(resource_gate.get("missing"), list):
        errors.append("state.resource_gate.missing must be a list")

    review = state.get("review")
    if not isinstance(review, dict):
        errors.append("state.review must be an object")
        review = {}
    if not isinstance(review.get("round"), int) or isinstance(review.get("round"), bool) or review.get("round", -1) < 0:
        errors.append("state.review.round must be a non-negative integer")
    if (
        not isinstance(review.get("max_rounds"), int)
        or isinstance(review.get("max_rounds"), bool)
        or review.get("max_rounds", 0) <= 0
    ):
        errors.append("state.review.max_rounds must be a positive integer")
    if review.get("score_operator") != ">" or review.get("score_threshold") != 8.0:
        errors.append("state.review score gate must be strictly greater than 8.0")

    if for_review:
        if resource_gate.get("status") != "satisfied" or resource_gate.get("missing"):
            errors.append("review gate requires a satisfied resource gate with no missing items")
        if state_phase not in ("testing", "reviewing", "fixing", "passed"):
            errors.append("review gate requires testing/reviewing/fixing/passed phase")
        if state_status not in ("in_progress", "passed"):
            errors.append("review gate requires in_progress or passed state status")


def cross_validate_links(
    requirements: dict[str, dict[str, Any]],
    claim_ids: set[str],
    runs: dict[str, dict[str, Any]],
    manifests: dict[str, set[str]],
    for_review: bool,
    errors: list[str],
) -> None:
    passed_requirement_ids: set[str] = set()
    for run_id, record in runs.items():
        requirement_ids = record.get("requirement_ids")
        if not string_list(requirement_ids):
            requirement_ids = []
        for req_id in requirement_ids:
            if req_id not in requirements:
                errors.append(f"run {run_id} references unknown requirement ID {req_id}")
            if record.get("status") == "passed":
                passed_requirement_ids.add(req_id)
                requirement = requirements.get(req_id)
                implementation = requirement.get("implementation") if isinstance(requirement, dict) else None
                files = implementation.get("files") if isinstance(implementation, dict) else []
                if string_list(files):
                    missing_files = sorted(set(files) - manifests.get(run_id, set()))
                    if missing_files:
                        errors.append(
                            f"run {run_id} provenance manifest omits implementation files: "
                            + ", ".join(missing_files)
                        )
        run_claim_ids = record.get("claim_ids")
        if not string_list(run_claim_ids):
            run_claim_ids = []
        for claim_id in run_claim_ids:
            if claim_id not in claim_ids:
                errors.append(f"run {run_id} references unknown claim ID {claim_id}")
        if record.get("status") == "passed" and record.get("purpose") in ("smoke", "full"):
            config = record.get("config")
            config_path = config.get("path") if isinstance(config, dict) else None
            if nonempty_string(config_path) and config_path not in manifests.get(run_id, set()):
                errors.append(f"run {run_id} provenance manifest omits config file {config_path}")
    for req_id, record in requirements.items():
        requirement_claim_ids = record.get("claim_ids")
        if not string_list(requirement_claim_ids):
            requirement_claim_ids = []
        for claim_id in requirement_claim_ids:
            if claim_id not in claim_ids:
                errors.append(f"requirement {req_id} references unknown claim ID {claim_id}")
        if for_review and record.get("status") == "verified" and req_id not in passed_requirement_ids:
            errors.append(f"verified requirement {req_id} is not referenced by a passed run")


def compare_requirement_counts(state: dict[str, Any], derived: dict[str, int], errors: list[str]) -> None:
    summary = state.get("requirements")
    if not isinstance(summary, dict):
        errors.append("state.requirements must be an object")
        return
    for key, expected in derived.items():
        if summary.get(key) != expected:
            errors.append(f"state.requirements.{key} must equal derived value {expected}")


def command_argv(value: Any) -> list[str] | None:
    if string_list(value, nonempty=True):
        return value
    if nonempty_string(value):
        try:
            parsed = shlex.split(value)
        except ValueError:
            return None
        return parsed if parsed else None
    return None


def command_argv_list(value: Any) -> list[list[str]] | None:
    if not isinstance(value, list) or not value:
        return None
    parsed: list[list[str]] = []
    for item in value:
        argv = command_argv(item)
        if argv is None:
            return None
        parsed.append(argv)
    normalized = [tuple(argv) for argv in parsed]
    return parsed if len(normalized) == len(set(normalized)) else None


def validate_state_runs(
    state: dict[str, Any],
    contract: dict[str, Any],
    runs: dict[str, dict[str, Any]],
    for_review: bool,
    errors: list[str],
) -> None:
    smoke = state.get("smoke_test")
    tests = state.get("required_tests")
    if not isinstance(smoke, dict):
        errors.append("state.smoke_test must be an object")
        smoke = {}
    if not isinstance(tests, dict):
        errors.append("state.required_tests must be an object")
        tests = {}
    if for_review:
        smoke_id = smoke.get("run_id")
        if smoke.get("status") != "passed" or not nonempty_string(smoke_id):
            errors.append("review gate requires a passed canonical smoke run ID")
        else:
            record = runs.get(smoke_id)
            if not isinstance(record, dict) or not (
                record.get("purpose") == "smoke"
                and record.get("status") == "passed"
                and record.get("exit_code") == 0
            ):
                errors.append("state smoke run ID must resolve to a passed smoke record")
            else:
                acceptance = contract.get("acceptance")
                acceptance = acceptance if isinstance(acceptance, dict) else {}
                expected_argv = command_argv(acceptance.get("smoke_command"))
                if expected_argv is None or record.get("command_argv") != expected_argv:
                    errors.append(
                        "canonical smoke run argv must exactly match acceptance.smoke_command"
                    )
        test_ids = tests.get("run_ids")
        if tests.get("status") != "passed" or not string_list(test_ids, nonempty=True):
            errors.append("review gate requires one or more passed required-test run IDs")
        else:
            actual_test_commands: list[list[str]] = []
            for run_id in test_ids:
                record = runs.get(run_id)
                if not isinstance(record, dict) or not (
                    record.get("purpose") == "test"
                    and record.get("status") == "passed"
                    and record.get("exit_code") == 0
                ):
                    errors.append(f"required-test run ID does not resolve to a passed test: {run_id}")
                else:
                    argv = record.get("command_argv")
                    if string_list(argv, nonempty=True):
                        actual_test_commands.append(argv)
            acceptance = contract.get("acceptance")
            acceptance = acceptance if isinstance(acceptance, dict) else {}
            expected_test_commands = command_argv_list(
                acceptance.get("required_test_commands")
            )
            if expected_test_commands is None or sorted(
                tuple(argv) for argv in actual_test_commands
            ) != sorted(tuple(argv) for argv in expected_test_commands):
                errors.append(
                    "required-test run argv must exactly cover acceptance.required_test_commands"
                )


def main() -> int:
    args = parse_args()
    lexical_root = args.experiment_dir.absolute()
    errors: list[str] = []
    try:
        if stat.S_ISLNK(lexical_root.lstat().st_mode):
            print("error: experiment directory must not be a symlink", file=sys.stderr)
            return 2
    except FileNotFoundError:
        print(f"error: experiment directory not found: {lexical_root}", file=sys.stderr)
        return 2
    root = lexical_root.resolve()
    if not root.is_dir():
        print(f"error: experiment directory not found: {root}", file=sys.stderr)
        return 2

    existing: dict[str, Path] = {}
    for relative in REQUIRED_FILES:
        path = root / relative
        if lstat_regular(path, relative, errors):
            existing[relative] = path

    state_value = load_json(existing["EXPERIMENT_STATE.json"], errors) if "EXPERIMENT_STATE.json" in existing else None
    contract_value = (
        load_yaml(existing["EXPERIMENT_CONTRACT.yaml"], errors)
        if "EXPERIMENT_CONTRACT.yaml" in existing
        else None
    )
    state = state_value if isinstance(state_value, dict) else {}
    contract = contract_value if isinstance(contract_value, dict) else {}
    if state_value is not None and not isinstance(state_value, dict):
        errors.append("EXPERIMENT_STATE.json top level must be an object")
    if contract_value is not None and not isinstance(contract_value, dict):
        errors.append("EXPERIMENT_CONTRACT.yaml top level must be an object")

    for field in ("schema_version", "slot", "experiment_dir", "idea", "phase", "status", "review"):
        if field not in state:
            errors.append(f"state missing field: {field}")
    if state:
        validate_state_schema(state, root, args.for_review, errors)

    idea_sha, idea_lines = validate_idea(state, contract, errors) if state and contract else (None, None)
    claim_ids = validate_contract(contract, args.for_review, errors)
    contract_task = contract.get("task")
    contract_task_type = contract_task.get("type") if isinstance(contract_task, dict) else None
    if args.for_review and state.get("task_type") != contract_task_type:
        errors.append("state.task_type must match contract.task.type")

    requirement_records = (
        parse_jsonl(existing["REQUIREMENTS.jsonl"], "REQUIREMENTS.jsonl", errors)
        if "REQUIREMENTS.jsonl" in existing
        else []
    )
    derived, requirements = validate_requirements(
        root,
        requirement_records,
        idea_sha,
        idea_lines,
        args.for_review,
        errors,
    )
    compare_requirement_counts(state, derived, errors)
    if args.for_review and derived["must_total"] <= 0:
        errors.append("review gate requires at least one atomic MUST requirement")

    run_records = (
        parse_jsonl(existing["runs/RUNS.jsonl"], "RUNS.jsonl", errors)
        if "runs/RUNS.jsonl" in existing
        else []
    )
    runs, manifests = validate_runs(root, run_records, args.for_review, errors)
    if args.for_review and not run_records:
        errors.append("review gate requires at least one run record")
    validate_state_runs(state, contract, runs, args.for_review, errors)
    cross_validate_links(requirements, claim_ids, runs, manifests, args.for_review, errors)

    project_path = existing.get("PROJECT.md")
    if project_path is not None:
        validate_project_document(root, project_path, args.for_review, errors)

    if args.for_review:
        for relative in (
            "EXPERIMENT_CONTRACT.yaml",
            "EXPERIMENT_STATE.json",
            "REQUIREMENTS.jsonl",
        ):
            path = existing.get(relative)
            if path is None:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeError) as error:
                errors.append(f"cannot read {relative}: {error}")
                continue
            check_secret(text, relative, errors)
            for placeholder in PLACEHOLDERS:
                if placeholder in text:
                    errors.append(f"untouched template placeholder in {relative}: {placeholder}")

    if errors:
        print("Mini experiment artifact validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(
        "Mini experiment artifacts are valid "
        f"({len(requirement_records)} requirements, {len(run_records)} run records)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
