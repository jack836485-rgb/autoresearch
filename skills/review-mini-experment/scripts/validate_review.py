#!/usr/bin/env python3
"""Fail-closed validation for review-mini-experment review artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import shlex
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover - reported as a validation error
    yaml = None


EXPECTED_WEIGHTS = {
    "requirement_fidelity_and_completeness": 2.0,
    "functional_and_scientific_correctness": 2.0,
    "test_and_validation_strength": 1.5,
    "evidence_integrity_and_auditability": 1.5,
    "reproducibility_and_interfaces": 1.0,
    "architecture_and_handoff": 1.0,
    "robustness_and_scope_discipline": 1.0,
}
CAP_VALUES = {
    "p0_invalid": 3.0,
    "core_path_missing": 5.0,
    "smoke_or_core_correctness_failure": 6.0,
    "audit_evidence_insufficient": 7.0,
    "must_or_blocking_finding": 8.0,
    "preflight_or_no_smoke": 8.0,
}
TOP_LEVEL_KEYS = {
    "schema_version",
    "mode",
    "reviewed_at",
    "review_class",
    "reviewer_backend",
    "inputs",
    "score",
    "verdict",
    "pass",
    "pass_rule",
    "requirement_summary",
    "evidence_integrity",
    "commands",
    "findings",
    "blocking_findings",
    "verified_strengths",
    "next_actions",
    "full_experiment_status",
    "notes",
}
INPUT_KEYS = {
    "idea_path",
    "idea_sha256",
    "experiment_dir",
    "contract_sha256",
    "requirements_sha256",
    "runs_sha256",
    "results_sha256",
    "stable_during_review",
    "content_manifest",
    "content_manifest_before_sha256",
    "content_manifest_sha256",
}
OPTIONAL_INPUT_KEYS = {"code_revision", "working_tree_diff_hash"}
SCORE_KEYS = {"raw", "triggered_caps", "applied_cap", "final", "breakdown"}
BREAKDOWN_KEYS = {"dimension", "weight", "awarded", "evidence", "deduction"}
PASS_RULE_KEYS = {
    "score_strictly_above_8",
    "verdict_is_pass",
    "zero_blocking_findings",
    "all_must_requirements_verified",
    "evidence_integrity_passed",
    "required_tests_passed",
    "canonical_smoke_passed",
}
FINDING_FIELDS = {
    "id",
    "severity",
    "blocking",
    "requirement_ids",
    "claim_ids",
    "evidence",
    "reproduction_or_proof",
    "impact",
    "root_cause",
    "minimum_fix",
    "acceptance_test",
    "cap_conditions",
}
COMMAND_KINDS = {"required_tests", "canonical_smoke", "targeted", "structural"}
COMMAND_KEYS = {"kind", "argv", "cwd", "exit_code", "status", "observation"}
REQUIREMENT_SUMMARY_KEYS = {
    f"{strength}_{suffix}"
    for strength in ("must", "should", "may")
    for suffix in ("total", "verified", "partial", "missing_or_invalid")
} | {"omitted_requirement_ids"}
CACHE_DIRS = {
    ".cache",
    ".hypothesis",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "__pycache__",
}
MUTABLE_SNAPSHOT_FILES = {"EXPERIMENT_STATE.json"}
HEX_SHA256 = re.compile(r"^[0-9a-f]{64}$")
SECRET_ASSIGNMENT = re.compile(
    r"(?i)\b(api[_-]?key|access[_-]?token|auth[_-]?token|password|passwd|"
    r"client[_-]?secret|authorization)[\"']?\s*(?:=|:)\s*[\"']?"
    r"([^\s,\"'\]}]+)"
)
BEARER_VALUE = re.compile(r"(?i)\bbearer\s+([^\s,\"'\]}]+)")
SECRET_FLAG = re.compile(
    r"(?i)^--?(?:api[_-]?key|access[_-]?token|auth[_-]?token|password|passwd|"
    r"client[_-]?secret|authorization)$"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("review_json", type=Path)
    parser.add_argument(
        "--review-md",
        type=Path,
        default=None,
        help="Markdown review path (default: REVIEW.md beside REVIEW.json)",
    )
    return parser.parse_args()


def number(value: Any) -> bool:
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(value)
    )


def nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def string_list(value: Any, *, nonempty: bool = False) -> bool:
    return (
        isinstance(value, list)
        and (not nonempty or bool(value))
        and all(nonempty_string(item) for item in value)
    )


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_manifest_digest(manifest: list[dict[str, str]]) -> str:
    encoded = json.dumps(
        manifest, ensure_ascii=True, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def normalize_argv(value: Any) -> list[str] | None:
    if string_list(value, nonempty=True):
        return value
    if nonempty_string(value):
        try:
            parsed = shlex.split(value)
        except ValueError:
            return None
        return parsed if parsed else None
    return None


def load_acceptance_commands(
    experiment_root: Path | None, errors: list[str]
) -> tuple[list[list[str]], list[str] | None]:
    if experiment_root is None:
        return [], None
    if yaml is None:
        errors.append("PyYAML is required to validate frozen acceptance commands")
        return [], None
    path = experiment_root / "EXPERIMENT_CONTRACT.yaml"
    try:
        contract = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as error:
        errors.append(f"cannot parse EXPERIMENT_CONTRACT.yaml: {error}")
        return [], None
    if not isinstance(contract, dict) or not isinstance(contract.get("acceptance"), dict):
        errors.append("contract.acceptance must be an object")
        return [], None
    acceptance = contract["acceptance"]
    raw_tests = acceptance.get("required_test_commands")
    required: list[list[str]] = []
    if not isinstance(raw_tests, list) or not raw_tests:
        errors.append("contract requires non-empty acceptance.required_test_commands")
    else:
        for index, value in enumerate(raw_tests):
            argv = normalize_argv(value)
            if argv is None:
                errors.append(f"acceptance.required_test_commands[{index}] is invalid")
            else:
                required.append(argv)
        normalized = [tuple(argv) for argv in required]
        if len(normalized) != len(set(normalized)):
            errors.append("acceptance.required_test_commands must be unique")
    smoke = normalize_argv(acceptance.get("smoke_command"))
    if smoke is None:
        errors.append("contract requires a valid acceptance.smoke_command")
    return required, smoke


def validate_run_receipts(
    experiment_root: Path | None,
    required_commands: list[list[str]],
    smoke_command: list[str] | None,
    errors: list[str],
) -> None:
    if experiment_root is None:
        return
    path = experiment_root / "runs" / "RUNS.jsonl"
    passed: dict[str, set[tuple[str, ...]]] = {"test": set(), "smoke": set()}
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as error:
        errors.append(f"cannot read RUNS.jsonl receipts: {error}")
        return
    for line_number, line in enumerate(lines, 1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as error:
            errors.append(f"RUNS.jsonl line {line_number}: {error}")
            continue
        if not isinstance(record, dict):
            errors.append(f"RUNS.jsonl line {line_number} must be an object")
            continue
        purpose = record.get("purpose")
        argv = record.get("command_argv")
        if (
            purpose in ("test", "smoke")
            and record.get("status") == "passed"
            and record.get("exit_code") == 0
            and string_list(argv, nonempty=True)
        ):
            passed[purpose].add(tuple(argv))
    missing_tests = sorted(
        tuple(argv) for argv in required_commands if tuple(argv) not in passed["test"]
    )
    if missing_tests:
        errors.append("RUNS.jsonl lacks passed receipts for frozen required test commands")
    if smoke_command is not None and tuple(smoke_command) not in passed["smoke"]:
        errors.append("RUNS.jsonl lacks a passed receipt for the frozen canonical smoke command")


def build_content_manifest(root: Path) -> tuple[list[dict[str, str]], list[str]]:
    """Hash regular experiment files, excluding reviews and disposable caches."""

    manifest: list[dict[str, str]] = []
    errors: list[str] = []

    def walk(directory: Path, relative: Path) -> None:
        try:
            entries = sorted(
                os.scandir(directory), key=lambda entry: entry.name.encode("utf-8")
            )
        except OSError as error:
            errors.append(f"cannot scan snapshot directory {directory}: {error}")
            return
        for entry in entries:
            if not relative.parts and entry.name == "reviews":
                continue
            if not relative.parts and entry.name in MUTABLE_SNAPSHOT_FILES:
                continue
            if entry.name in CACHE_DIRS:
                continue
            child_relative = relative / entry.name
            child = Path(entry.path)
            try:
                if entry.is_symlink():
                    errors.append(f"snapshot contains symlink: {child_relative.as_posix()}")
                elif entry.is_dir(follow_symlinks=False):
                    walk(child, child_relative)
                elif entry.is_file(follow_symlinks=False):
                    manifest.append(
                        {
                            "path": child_relative.as_posix(),
                            "sha256": sha256_file(child),
                        }
                    )
                else:
                    errors.append(
                        f"snapshot contains unsupported file type: {child_relative.as_posix()}"
                    )
            except OSError as error:
                errors.append(f"cannot inspect snapshot entry {child_relative}: {error}")

    walk(root, Path())
    manifest.sort(key=lambda item: item["path"].encode("utf-8"))
    return manifest, errors


def valid_iso8601(value: Any) -> bool:
    if not nonempty_string(value):
        return False
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None


def safe_secret_value(value: str) -> bool:
    normalized = value.strip().strip("\"'")
    if not normalized:
        return True
    if normalized.lower() in {"null", "none", "redacted", "<redacted>", "[redacted]"}:
        return True
    if re.fullmatch(r"\$\{?[A-Z][A-Z0-9_]{2,}\}?", normalized):
        return True
    if re.fullmatch(r"[A-Z][A-Z0-9_]{2,}", normalized):
        return True
    return False


def secret_errors(raw_json: str, raw_markdown: str, commands: list[Any]) -> list[str]:
    errors: list[str] = []
    for label, content in (("REVIEW.json", raw_json), ("REVIEW.md", raw_markdown)):
        for match in SECRET_ASSIGNMENT.finditer(content):
            if not safe_secret_value(match.group(2)):
                errors.append(f"{label} appears to contain an unredacted {match.group(1)} value")
        for match in BEARER_VALUE.finditer(content):
            if not safe_secret_value(match.group(1)):
                errors.append(f"{label} appears to contain an unredacted bearer credential")
    for index, command in enumerate(commands):
        if not isinstance(command, dict):
            continue
        argv = command.get("argv")
        if not isinstance(argv, list):
            continue
        for position, argument in enumerate(argv[:-1]):
            if isinstance(argument, str) and SECRET_FLAG.fullmatch(argument.strip()):
                following = argv[position + 1]
                if isinstance(following, str) and not safe_secret_value(following):
                    errors.append(
                        f"commands[{index}].argv contains an unredacted credential value"
                    )
    return sorted(set(errors))


def validate_string_collection(
    data: dict[str, Any], key: str, errors: list[str], *, nonempty: bool = False
) -> list[str]:
    value = data.get(key)
    if not string_list(value, nonempty=nonempty):
        qualifier = "non-empty " if nonempty else ""
        errors.append(f"{key} must be a {qualifier}list of non-empty strings")
        return []
    return value


def validate_inputs(
    inputs: Any,
    review_json: Path,
    review_md: Path,
    errors: list[str],
) -> Path | None:
    if not isinstance(inputs, dict):
        errors.append("inputs must be an object")
        return None

    if review_json.name != "REVIEW.json" or review_md.name != "REVIEW.md":
        errors.append("review artifacts must be named REVIEW.json and REVIEW.md")
    if re.fullmatch(r"round-[0-9]{3}", review_json.parent.name) is None:
        errors.append("review output directory must use the round-NNN naming convention")
    if review_json.is_symlink() or review_md.is_symlink():
        errors.append("review artifacts must not be symlinks")
    try:
        if review_json.absolute().resolve(strict=True) != review_json.absolute():
            errors.append("REVIEW.json path must not contain symlinks or dot segments")
        if review_md.absolute().resolve(strict=True) != review_md.absolute():
            errors.append("REVIEW.md path must not contain symlinks or dot segments")
    except OSError as error:
        errors.append(f"cannot resolve review output paths: {error}")
    try:
        output_entries = sorted(path.name for path in review_json.parent.iterdir())
    except OSError as error:
        errors.append(f"cannot inspect review output directory: {error}")
    else:
        if output_entries != ["REVIEW.json", "REVIEW.md"]:
            errors.append("review round directory must contain only REVIEW.json and REVIEW.md")
    missing = sorted(INPUT_KEYS - set(inputs))
    if missing:
        errors.append("inputs missing fields: " + ", ".join(missing))
    unknown = sorted(set(inputs) - INPUT_KEYS - OPTIONAL_INPUT_KEYS)
    if unknown:
        errors.append("inputs has unknown fields: " + ", ".join(unknown))
    code_revision = inputs.get("code_revision")
    if code_revision is not None and not nonempty_string(code_revision):
        errors.append("inputs.code_revision must be null or a non-empty revision string")
    diff_hash = inputs.get("working_tree_diff_hash")
    if diff_hash is not None and (
        not isinstance(diff_hash, str) or HEX_SHA256.fullmatch(diff_hash) is None
    ):
        errors.append("inputs.working_tree_diff_hash must be null or a SHA-256 digest")

    experiment_value = inputs.get("experiment_dir")
    if not nonempty_string(experiment_value):
        errors.append("inputs.experiment_dir must be a non-empty absolute path")
        return None
    lexical_root = Path(experiment_value)
    if not lexical_root.is_absolute():
        errors.append("inputs.experiment_dir must be absolute")
        return None
    if lexical_root.is_symlink():
        errors.append("inputs.experiment_dir must not be a symlink")
        return None
    try:
        experiment_root = lexical_root.resolve(strict=True)
    except OSError as error:
        errors.append(f"inputs.experiment_dir cannot be resolved: {error}")
        return None
    if not experiment_root.is_dir():
        errors.append("inputs.experiment_dir must resolve to a directory")
        return None
    if str(experiment_root) != str(lexical_root):
        errors.append("inputs.experiment_dir must be a canonical absolute path")

    try:
        review_relative = review_json.resolve(strict=True).relative_to(experiment_root)
        markdown_relative = review_md.resolve(strict=True).relative_to(experiment_root)
    except (OSError, ValueError) as error:
        errors.append(f"review files must be inside the experiment directory: {error}")
    else:
        if not review_relative.parts or review_relative.parts[0] != "reviews":
            errors.append("REVIEW.json must be below EXPERIMENT_DIR/reviews/")
        if not markdown_relative.parts or markdown_relative.parts[0] != "reviews":
            errors.append("REVIEW.md must be below EXPERIMENT_DIR/reviews/")
        if review_json.resolve().parent != review_md.resolve().parent:
            errors.append("REVIEW.json and REVIEW.md must be in the same round directory")
        current = experiment_root
        for component in review_relative.parts:
            current = current / component
            if current.is_symlink():
                errors.append(f"review output path contains symlink: {current}")

    idea_value = inputs.get("idea_path")
    idea_digest = inputs.get("idea_sha256")
    if not isinstance(idea_digest, str) or HEX_SHA256.fullmatch(idea_digest) is None:
        errors.append("inputs.idea_sha256 must be a lowercase SHA-256 digest")
    if not nonempty_string(idea_value) or not Path(idea_value).is_absolute():
        errors.append("inputs.idea_path must be a non-empty absolute path")
    else:
        idea_path = Path(idea_value)
        if idea_path.is_symlink() or not idea_path.is_file():
            errors.append("inputs.idea_path must be a regular non-symlink file")
        else:
            expected = idea_digest
            try:
                actual = sha256_file(idea_path)
            except OSError as error:
                errors.append(f"cannot hash inputs.idea_path: {error}")
            else:
                if expected != actual:
                    errors.append("inputs.idea_sha256 does not match the idea file")

    hashed_inputs = {
        "contract_sha256": experiment_root / "EXPERIMENT_CONTRACT.yaml",
        "requirements_sha256": experiment_root / "REQUIREMENTS.jsonl",
        "runs_sha256": experiment_root / "runs" / "RUNS.jsonl",
        "results_sha256": experiment_root / "RESULTS.md",
    }
    for field, path in hashed_inputs.items():
        expected = inputs.get(field)
        if not isinstance(expected, str) or HEX_SHA256.fullmatch(expected) is None:
            errors.append(f"inputs.{field} must be a lowercase SHA-256 digest")
            continue
        if path.is_symlink() or not path.is_file():
            errors.append(f"cannot verify inputs.{field}; missing regular file {path}")
            continue
        try:
            actual = sha256_file(path)
        except OSError as error:
            errors.append(f"cannot hash {path.relative_to(experiment_root)}: {error}")
        else:
            if actual != expected:
                errors.append(f"inputs.{field} does not match {path.relative_to(experiment_root)}")

    if inputs.get("stable_during_review") is not True:
        errors.append("inputs.stable_during_review must be true")

    actual_manifest, manifest_errors = build_content_manifest(experiment_root)
    errors.extend(manifest_errors)
    declared_manifest = inputs.get("content_manifest")
    if not isinstance(declared_manifest, list):
        errors.append("inputs.content_manifest must be a list")
    else:
        manifest_valid = True
        normalized: list[dict[str, str]] = []
        prior_path: bytes | None = None
        for index, item in enumerate(declared_manifest):
            if not isinstance(item, dict) or set(item) != {"path", "sha256"}:
                errors.append(
                    f"inputs.content_manifest[{index}] must contain exactly path and sha256"
                )
                manifest_valid = False
                continue
            path_value = item.get("path")
            digest_value = item.get("sha256")
            if (
                not nonempty_string(path_value)
                or Path(path_value).is_absolute()
                or ".." in Path(path_value).parts
            ):
                errors.append(f"inputs.content_manifest[{index}].path is not a safe relative path")
                manifest_valid = False
            if not isinstance(digest_value, str) or HEX_SHA256.fullmatch(digest_value) is None:
                errors.append(f"inputs.content_manifest[{index}].sha256 is invalid")
                manifest_valid = False
            encoded_path = path_value.encode("utf-8") if isinstance(path_value, str) else None
            if encoded_path is not None and prior_path is not None and encoded_path <= prior_path:
                errors.append("inputs.content_manifest must be strictly bytewise-sorted by path")
                manifest_valid = False
            if encoded_path is not None:
                prior_path = encoded_path
            if isinstance(path_value, str) and isinstance(digest_value, str):
                normalized.append({"path": path_value, "sha256": digest_value})
        if manifest_valid and normalized != actual_manifest:
            errors.append("inputs.content_manifest does not match the current experiment snapshot")
        if manifest_valid:
            actual_digest = canonical_manifest_digest(normalized)
            if inputs.get("content_manifest_sha256") != actual_digest:
                errors.append("inputs.content_manifest_sha256 is inconsistent")
    digest = inputs.get("content_manifest_sha256")
    if not isinstance(digest, str) or HEX_SHA256.fullmatch(digest) is None:
        errors.append("inputs.content_manifest_sha256 must be a lowercase SHA-256 digest")
    before_digest = inputs.get("content_manifest_before_sha256")
    if not isinstance(before_digest, str) or HEX_SHA256.fullmatch(before_digest) is None:
        errors.append("inputs.content_manifest_before_sha256 must be a lowercase SHA-256 digest")
    elif before_digest != digest:
        errors.append("content manifest changed during review")

    return experiment_root


def validate_breakdown(score: dict[str, Any], errors: list[str]) -> tuple[Any, Any, Any]:
    raw = score.get("raw")
    final = score.get("final")
    cap = score.get("applied_cap")
    breakdown = score.get("breakdown")
    if not number(raw) or not 0 <= float(raw) <= 10:
        errors.append("score.raw must be a finite number in [0, 10]")
    if not number(final) or not 0 <= float(final) <= 10:
        errors.append("score.final must be a finite number in [0, 10]")
    if cap is not None and (not number(cap) or not 0 <= float(cap) <= 10):
        errors.append("score.applied_cap must be null or a finite number in [0, 10]")

    awarded_sum = 0.0
    seen: set[str] = set()
    if not isinstance(breakdown, list):
        errors.append("score.breakdown must be a list")
        breakdown = []
    for index, item in enumerate(breakdown):
        if not isinstance(item, dict):
            errors.append(f"score.breakdown[{index}] must be an object")
            continue
        if set(item) != BREAKDOWN_KEYS:
            errors.append(
                f"score.breakdown[{index}] must contain exactly "
                + ", ".join(sorted(BREAKDOWN_KEYS))
            )
        dimension = item.get("dimension")
        weight = item.get("weight")
        awarded = item.get("awarded")
        evidence = item.get("evidence")
        deduction = item.get("deduction")
        if not isinstance(dimension, str) or dimension not in EXPECTED_WEIGHTS:
            errors.append(f"unknown score dimension: {dimension}")
            continue
        if dimension in seen:
            errors.append(f"duplicate score dimension: {dimension}")
        seen.add(dimension)
        expected_weight = EXPECTED_WEIGHTS[dimension]
        if not number(weight) or not math.isclose(float(weight), expected_weight, abs_tol=1e-9):
            errors.append(f"wrong weight for {dimension}")
        if not number(awarded) or not 0 <= float(awarded) <= expected_weight:
            errors.append(f"invalid awarded score for {dimension}")
        else:
            awarded_sum += float(awarded)
        if not string_list(evidence, nonempty=True):
            errors.append(f"score breakdown {dimension} needs non-empty direct evidence")
        if not nonempty_string(deduction):
            errors.append(f"score breakdown {dimension} needs a non-empty deduction rationale")
    missing = sorted(set(EXPECTED_WEIGHTS) - seen)
    if missing:
        errors.append("missing score dimensions: " + ", ".join(missing))
    if number(raw) and not math.isclose(float(raw), awarded_sum, abs_tol=1e-6):
        errors.append(f"score.raw {raw} does not equal awarded sum {awarded_sum}")
    return raw, final, cap


def load_executor_requirements(
    experiment_root: Path | None, errors: list[str]
) -> tuple[dict[str, dict[str, int]], bool]:
    counts = {
        strength: {"total": 0, "verified": 0}
        for strength in ("must", "should", "may")
    }
    if experiment_root is None:
        return counts, False
    path = experiment_root / "REQUIREMENTS.jsonl"
    seen: set[str] = set()
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as error:
        errors.append(f"cannot read executor requirements: {error}")
        return counts, False
    valid = True
    for line_number, line in enumerate(lines, 1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as error:
            errors.append(f"REQUIREMENTS.jsonl line {line_number}: {error}")
            valid = False
            continue
        if not isinstance(record, dict):
            errors.append(f"REQUIREMENTS.jsonl line {line_number} must be an object")
            valid = False
            continue
        req_id = record.get("req_id")
        strength = record.get("strength")
        status = record.get("status")
        if not nonempty_string(req_id) or req_id in seen:
            errors.append(f"REQUIREMENTS.jsonl line {line_number} has invalid/duplicate req_id")
            valid = False
        else:
            seen.add(req_id)
        if strength not in ("MUST", "SHOULD", "MAY"):
            errors.append(f"REQUIREMENTS.jsonl line {line_number} has invalid strength")
            valid = False
            continue
        if status not in ("unmapped", "implemented", "verified", "blocked", "deferred"):
            errors.append(f"REQUIREMENTS.jsonl line {line_number} has invalid status")
            valid = False
        key = strength.lower()
        counts[key]["total"] += 1
        if status == "verified":
            counts[key]["verified"] += 1
    must = counts["must"]
    executor_all_must = valid and must["total"] > 0 and must["verified"] == must["total"]
    return counts, executor_all_must


def validate_requirements(
    summary: Any,
    executor_counts: dict[str, dict[str, int]],
    executor_all_must: bool,
    errors: list[str],
) -> bool:
    if not isinstance(summary, dict):
        errors.append("requirement_summary must be an object")
        return False
    if set(summary) != REQUIREMENT_SUMMARY_KEYS:
        missing = sorted(REQUIREMENT_SUMMARY_KEYS - set(summary))
        unknown = sorted(set(summary) - REQUIREMENT_SUMMARY_KEYS)
        if missing:
            errors.append("requirement_summary missing fields: " + ", ".join(missing))
        if unknown:
            errors.append("requirement_summary has unknown fields: " + ", ".join(unknown))
    all_valid = True
    for strength in ("must", "should", "may"):
        names = [
            f"{strength}_total",
            f"{strength}_verified",
            f"{strength}_partial",
            f"{strength}_missing_or_invalid",
        ]
        values = [summary.get(name) for name in names]
        if not all(isinstance(value, int) and not isinstance(value, bool) and value >= 0 for value in values):
            errors.append(f"{strength.upper()} requirement counts must be non-negative integers")
            all_valid = False
            continue
        total, verified, partial, missing = values
        if verified + partial + missing != total:
            errors.append(f"{strength.upper()} requirement counts do not sum to total")
            all_valid = False
    omitted = summary.get("omitted_requirement_ids")
    if not string_list(omitted):
        errors.append("requirement_summary.omitted_requirement_ids must be a list of strings")
        omitted = []
    elif len(omitted) != len(set(omitted)):
        errors.append("requirement_summary.omitted_requirement_ids contains duplicates")
    extra_total = 0
    for strength in ("must", "should", "may"):
        reviewed_total = summary.get(f"{strength}_total")
        executor_total = executor_counts[strength]["total"]
        if isinstance(reviewed_total, int) and not isinstance(reviewed_total, bool):
            if reviewed_total < executor_total:
                errors.append(
                    f"{strength.upper()} review total cannot be below REQUIREMENTS.jsonl total"
                )
            else:
                extra_total += reviewed_total - executor_total
    if isinstance(omitted, list) and extra_total != len(omitted):
        errors.append(
            "omitted_requirement_ids count must equal requirements recovered beyond JSONL"
        )
    must_total = summary.get("must_total")
    must_verified = summary.get("must_verified")
    must_partial = summary.get("must_partial")
    must_missing = summary.get("must_missing_or_invalid")
    all_must = (
        all_valid
        and isinstance(must_total, int)
        and must_total > 0
        and must_verified == must_total
        and must_partial == 0
        and must_missing == 0
        and not omitted
        and executor_all_must
    )
    return all_must


def validate_commands(
    commands: Any,
    experiment_root: Path | None,
    required_commands: list[list[str]],
    smoke_command: list[str] | None,
    errors: list[str],
) -> tuple[list[Any], bool, bool, bool]:
    if not isinstance(commands, list):
        errors.append("commands must be a list")
        return [], False, False, False
    parsed: list[Any] = commands
    by_kind: dict[str, list[dict[str, Any]]] = {kind: [] for kind in COMMAND_KINDS}
    for index, command in enumerate(commands):
        if not isinstance(command, dict):
            errors.append(f"commands[{index}] must be an object")
            continue
        if set(command) != COMMAND_KEYS:
            errors.append(
                f"commands[{index}] must contain exactly " + ", ".join(sorted(COMMAND_KEYS))
            )
        kind = command.get("kind")
        argv = command.get("argv")
        cwd = command.get("cwd")
        exit_code = command.get("exit_code")
        status = command.get("status")
        observation = command.get("observation")
        if not isinstance(kind, str) or kind not in COMMAND_KINDS:
            errors.append(f"commands[{index}].kind is invalid")
        else:
            by_kind[kind].append(command)
        if not string_list(argv, nonempty=True):
            errors.append(f"commands[{index}].argv must be a non-empty string list")
        if not nonempty_string(cwd) or not Path(cwd).is_absolute():
            errors.append(f"commands[{index}].cwd must be an absolute path")
        elif experiment_root is not None:
            try:
                resolved_cwd = Path(cwd).resolve(strict=True)
                resolved_cwd.relative_to(experiment_root)
            except (OSError, ValueError):
                errors.append(
                    f"commands[{index}].cwd must resolve inside inputs.experiment_dir"
                )
            else:
                if not resolved_cwd.is_dir():
                    errors.append(f"commands[{index}].cwd must resolve to a directory")
        if not isinstance(status, str) or status not in ("pass", "fail", "not_run"):
            errors.append(f"commands[{index}].status is invalid")
        if status == "pass" and (
            not isinstance(exit_code, int) or isinstance(exit_code, bool) or exit_code != 0
        ):
            errors.append(f"commands[{index}] marked pass must have exit_code 0")
        if status == "fail" and (
            not isinstance(exit_code, int) or isinstance(exit_code, bool) or exit_code == 0
        ):
            errors.append(f"commands[{index}] marked fail needs a non-zero integer exit_code")
        if status == "not_run" and exit_code is not None:
            errors.append(f"commands[{index}] marked not_run must have null exit_code")
        if not nonempty_string(observation):
            errors.append(f"commands[{index}].observation must be non-empty")

    declared_tests = [
        tuple(item.get("argv"))
        for item in by_kind["required_tests"]
        if string_list(item.get("argv"), nonempty=True)
    ]
    if sorted(declared_tests) != sorted(tuple(argv) for argv in required_commands):
        errors.append(
            "required_tests command argv must exactly cover acceptance.required_test_commands"
        )
    declared_smoke = by_kind["canonical_smoke"]
    if (
        len(declared_smoke) != 1
        or smoke_command is None
        or declared_smoke[0].get("argv") != smoke_command
    ):
        errors.append("canonical_smoke argv must exactly match acceptance.smoke_command")

    def gate(kind: str) -> bool:
        items = by_kind[kind]
        return bool(items) and all(item.get("status") == "pass" and item.get("exit_code") == 0 for item in items)

    required_tests_passed = gate("required_tests")
    canonical_smoke_passed = gate("canonical_smoke")
    smoke_failed = any(item.get("status") == "fail" for item in by_kind["canonical_smoke"])
    return parsed, required_tests_passed, canonical_smoke_passed, smoke_failed


def validate_findings(
    findings: Any, blocking: Any, errors: list[str]
) -> tuple[list[dict[str, Any]], set[str], bool, bool, set[str]]:
    if not isinstance(findings, list):
        errors.append("findings must be a list")
        findings = []
    if not string_list(blocking):
        errors.append("blocking_findings must be a list of non-empty finding IDs")
        blocking = []
    elif len(blocking) != len(set(blocking)):
        errors.append("blocking_findings contains duplicates")

    parsed: list[dict[str, Any]] = []
    finding_ids: set[str] = set()
    actually_blocking: set[str] = set()
    finding_caps: set[str] = set()
    has_p0 = False
    has_p1 = False
    for index, finding in enumerate(findings):
        if not isinstance(finding, dict):
            errors.append(f"findings[{index}] must be an object")
            continue
        parsed.append(finding)
        finding_id = finding.get("id")
        display_id = finding_id if nonempty_string(finding_id) else f"index {index}"
        missing = sorted(FINDING_FIELDS - set(finding))
        if missing:
            errors.append(f"finding {display_id} missing fields: {', '.join(missing)}")
        unknown = sorted(set(finding) - FINDING_FIELDS)
        if unknown:
            errors.append(f"finding {display_id} has unknown fields: {', '.join(unknown)}")
        if not nonempty_string(finding_id):
            errors.append(f"findings[{index}].id must be non-empty")
        elif finding_id in finding_ids:
            errors.append(f"duplicate finding id: {finding_id}")
        else:
            finding_ids.add(finding_id)
        severity = finding.get("severity")
        if not isinstance(severity, str) or severity not in ("P0", "P1", "P2"):
            errors.append(f"finding {display_id} has invalid severity")
        has_p0 = has_p0 or severity == "P0"
        has_p1 = has_p1 or severity == "P1"
        blocking_value = finding.get("blocking")
        if not isinstance(blocking_value, bool):
            errors.append(f"finding {display_id}.blocking must be boolean")
        if severity in ("P0", "P1") and blocking_value is not True:
            errors.append(f"finding {display_id} must block because it is P0/P1")
        if blocking_value is True and nonempty_string(finding_id):
            actually_blocking.add(finding_id)
        for field in ("requirement_ids", "claim_ids"):
            identifiers = finding.get(field)
            if not string_list(identifiers):
                errors.append(f"finding {display_id}.{field} must be a list of strings")
            elif len(identifiers) != len(set(identifiers)):
                errors.append(f"finding {display_id}.{field} contains duplicates")
        if not string_list(finding.get("evidence"), nonempty=True):
            errors.append(f"finding {display_id}.evidence must be a non-empty string list")
        for field in (
            "reproduction_or_proof",
            "impact",
            "root_cause",
            "minimum_fix",
            "acceptance_test",
        ):
            if not nonempty_string(finding.get(field)):
                errors.append(f"finding {display_id}.{field} must be non-empty")
        cap_conditions = finding.get("cap_conditions")
        if not isinstance(cap_conditions, list) or not all(
            isinstance(item, str) and item in CAP_VALUES for item in cap_conditions
        ):
            errors.append(f"finding {display_id}.cap_conditions contains an invalid condition")
            cap_conditions = []
        elif len(cap_conditions) != len(set(cap_conditions)):
            errors.append(f"finding {display_id}.cap_conditions contains duplicates")
        finding_caps.update(cap_conditions)
        if severity == "P0" and "p0_invalid" not in cap_conditions:
            errors.append(f"finding {display_id} P0 must declare p0_invalid")
        if severity != "P0" and "p0_invalid" in cap_conditions:
            errors.append(f"finding {display_id} cannot declare p0_invalid unless it is P0")
        if (severity == "P1" or blocking_value is True) and "must_or_blocking_finding" not in cap_conditions:
            errors.append(f"finding {display_id} must declare must_or_blocking_finding")
        if (
            "must_or_blocking_finding" in cap_conditions
            and severity != "P1"
            and blocking_value is not True
        ):
            errors.append(
                f"finding {display_id} cannot declare must_or_blocking_finding when non-blocking"
            )
        if any(
            condition in cap_conditions
            for condition in ("core_path_missing", "smoke_or_core_correctness_failure")
        ) and severity not in ("P0", "P1"):
            errors.append(f"finding {display_id} uses a core-defect cap but is not P0/P1")

    blocking_set = set(blocking) if isinstance(blocking, list) else set()
    if blocking_set - finding_ids:
        errors.append("blocking_findings contains unknown IDs")
    if blocking_set != actually_blocking:
        errors.append("blocking_findings disagrees with finding blocking flags")
    return parsed, actually_blocking, has_p0, has_p1, finding_caps


def validate_caps(
    score: dict[str, Any], derived_caps: set[str], errors: list[str]
) -> None:
    triggered = score.get("triggered_caps")
    applied = score.get("applied_cap")
    declared: dict[str, float] = {}
    if not isinstance(triggered, list):
        errors.append("score.triggered_caps must be a list")
        triggered = []
    for index, item in enumerate(triggered):
        if not isinstance(item, dict) or set(item) != {"condition", "value", "reason"}:
            errors.append(
                f"score.triggered_caps[{index}] must contain exactly condition, value, and reason"
            )
            continue
        condition = item.get("condition")
        value = item.get("value")
        reason = item.get("reason")
        if not isinstance(condition, str) or condition not in CAP_VALUES:
            errors.append(f"score.triggered_caps[{index}].condition is invalid")
            continue
        if condition in declared:
            errors.append(f"duplicate triggered cap condition: {condition}")
        expected = CAP_VALUES[condition]
        if not number(value) or not math.isclose(float(value), expected, abs_tol=1e-9):
            errors.append(f"cap {condition} must have exact value {expected}")
        if not nonempty_string(reason):
            errors.append(f"cap {condition} needs a non-empty reason")
        declared[condition] = expected
    if set(declared) != derived_caps:
        missing = sorted(derived_caps - set(declared))
        extra = sorted(set(declared) - derived_caps)
        if missing:
            errors.append("score.triggered_caps missing derived conditions: " + ", ".join(missing))
        if extra:
            errors.append("score.triggered_caps has unsupported conditions: " + ", ".join(extra))
    if derived_caps:
        expected_cap = min(CAP_VALUES[condition] for condition in derived_caps)
        if not number(applied) or not math.isclose(float(applied), expected_cap, abs_tol=1e-9):
            errors.append(f"score.applied_cap must equal lowest triggered cap {expected_cap}")
    elif applied is not None:
        errors.append("score.applied_cap must be null when no cap is triggered")


def markdown_value(markdown: str, label: str) -> str | None:
    wanted = label.lower()
    for raw_line in markdown.splitlines():
        line = raw_line.strip()
        if not line.startswith("-") or ":" not in line:
            continue
        key, value = line[1:].split(":", 1)
        cleaned_key = key.replace("*", "").replace("`", "").strip().lower()
        if cleaned_key == wanted:
            return value.replace("*", "").replace("`", "").strip()
    return None


def validate_markdown(
    markdown: str,
    final: Any,
    verdict: Any,
    passed: Any,
    blocking: list[str],
    errors: list[str],
) -> None:
    score_text = markdown_value(markdown, "Final score")
    if score_text is None:
        errors.append("REVIEW.md is missing the Final score verdict bullet")
    else:
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)\s*/\s*10(?:\.0)?", score_text)
        if match is None or not number(final) or not math.isclose(
            float(match.group(1)), float(final), abs_tol=1e-6
        ):
            errors.append("REVIEW.md Final score disagrees with REVIEW.json")
    verdict_text = markdown_value(markdown, "Verdict")
    if verdict_text is None or verdict_text.lower() != verdict:
        errors.append("REVIEW.md Verdict disagrees with REVIEW.json")
    pass_text = markdown_value(markdown, "Pass rule satisfied")
    parsed_pass = {"yes": True, "true": True, "no": False, "false": False}.get(
        pass_text.lower() if isinstance(pass_text, str) else ""
    )
    if parsed_pass is None or parsed_pass is not passed:
        errors.append("REVIEW.md Pass rule satisfied disagrees with REVIEW.json")
    blocking_text = markdown_value(markdown, "Blocking findings")
    if blocking_text is None:
        errors.append("REVIEW.md is missing the Blocking findings verdict bullet")
    else:
        normalized = blocking_text.strip()
        if normalized.lower() in {"none", "[]"}:
            markdown_blocking: list[str] = []
        else:
            markdown_blocking = [item.strip() for item in normalized.split(",") if item.strip()]
        if markdown_blocking != blocking:
            errors.append("REVIEW.md Blocking findings disagrees with REVIEW.json")


def main() -> int:
    args = parse_args()
    review_json = args.review_json
    review_md = args.review_md or review_json.with_name("REVIEW.md")
    errors: list[str] = []
    try:
        raw_json = review_json.read_text(encoding="utf-8")
        data = json.loads(raw_json)
    except (OSError, json.JSONDecodeError) as error:
        print(f"error: cannot parse review JSON: {error}", file=sys.stderr)
        return 2
    try:
        raw_markdown = review_md.read_text(encoding="utf-8")
    except OSError as error:
        print(f"error: cannot read review Markdown: {error}", file=sys.stderr)
        return 2
    if not isinstance(data, dict):
        print("Review validation failed:\n- REVIEW.json top level must be an object", file=sys.stderr)
        return 1

    missing_top = sorted(TOP_LEVEL_KEYS - set(data))
    if missing_top:
        errors.append("REVIEW.json missing top-level fields: " + ", ".join(missing_top))
    unknown_top = sorted(set(data) - TOP_LEVEL_KEYS)
    if unknown_top:
        errors.append("REVIEW.json has unknown top-level fields: " + ", ".join(unknown_top))
    if data.get("schema_version") != 1:
        errors.append("schema_version must equal 1")
    mode = data.get("mode")
    verdict = data.get("verdict")
    integrity = data.get("evidence_integrity")
    if not isinstance(mode, str) or mode not in ("preflight", "postrun"):
        errors.append("mode must be preflight or postrun")
    if not isinstance(verdict, str) or verdict not in ("pass", "revise", "blocked", "invalid"):
        errors.append("verdict must use the stable enum")
    if not isinstance(integrity, str) or integrity not in ("pass", "fail", "unknown"):
        errors.append("evidence_integrity must be pass, fail, or unknown")
    if not isinstance(data.get("review_class"), str) or data.get("review_class") not in (
        "type_a",
        "type_b",
    ):
        errors.append("review_class must be type_a or type_b")
    if not nonempty_string(data.get("reviewer_backend")):
        errors.append("reviewer_backend must be non-empty")
    if not valid_iso8601(data.get("reviewed_at")):
        errors.append("reviewed_at must be an ISO-8601 timestamp with timezone")

    experiment_root = validate_inputs(data.get("inputs"), review_json, review_md, errors)
    required_commands, smoke_command = load_acceptance_commands(experiment_root, errors)
    validate_run_receipts(
        experiment_root, required_commands, smoke_command, errors
    )

    score = data.get("score")
    if not isinstance(score, dict):
        errors.append("score must be an object")
        score = {}
    elif set(score) != SCORE_KEYS:
        missing_score = sorted(SCORE_KEYS - set(score))
        unknown_score = sorted(set(score) - SCORE_KEYS)
        if missing_score:
            errors.append("score missing fields: " + ", ".join(missing_score))
        if unknown_score:
            errors.append("score has unknown fields: " + ", ".join(unknown_score))
    raw, final, cap = validate_breakdown(score, errors)

    executor_counts, executor_all_must = load_executor_requirements(experiment_root, errors)
    all_must = validate_requirements(
        data.get("requirement_summary"),
        executor_counts,
        executor_all_must,
        errors,
    )
    commands, tests_passed, smoke_passed, smoke_failed = validate_commands(
        data.get("commands"),
        experiment_root,
        required_commands,
        smoke_command,
        errors,
    )
    blocking_value = data.get("blocking_findings")
    findings, blocking_set, has_p0, has_p1, finding_caps = validate_findings(
        data.get("findings"), blocking_value, errors
    )
    blocking = blocking_value if string_list(blocking_value) else []

    derived_caps = set(finding_caps)
    if has_p0:
        derived_caps.add("p0_invalid")
    if has_p1 or blocking_set or not all_must or not tests_passed:
        derived_caps.add("must_or_blocking_finding")
    if mode == "preflight" or not smoke_passed:
        derived_caps.add("preflight_or_no_smoke")
    if smoke_failed:
        derived_caps.add("smoke_or_core_correctness_failure")
    if integrity == "fail" and not has_p0:
        derived_caps.add("audit_evidence_insufficient")
    if "audit_evidence_insufficient" in finding_caps and integrity == "pass":
        errors.append("audit_evidence_insufficient contradicts evidence_integrity=pass")
    if (
        "preflight_or_no_smoke" in finding_caps
        and mode == "postrun"
        and smoke_passed
    ):
        errors.append("preflight_or_no_smoke is unsupported in postrun after passing smoke")
    validate_caps(score, derived_caps, errors)

    if number(raw) and number(final):
        expected_final = min(float(raw), float(cap)) if number(cap) else float(raw)
        if not math.isclose(float(final), expected_final, abs_tol=1e-6):
            errors.append("score.final does not equal raw score with applied cap")

    if has_p0:
        if verdict != "invalid":
            errors.append("any P0 finding requires verdict=invalid")
        if integrity != "fail":
            errors.append("any P0 finding requires evidence_integrity=fail")
    elif derived_caps & {"core_path_missing", "smoke_or_core_correctness_failure"}:
        if verdict != "revise":
            errors.append("core-path or smoke correctness failure requires verdict=revise")
    if "audit_evidence_insufficient" in derived_caps and verdict not in ("revise", "invalid"):
        errors.append("insufficient audit evidence requires verdict=revise or invalid")
    if integrity == "fail" and not findings:
        errors.append("evidence_integrity=fail requires an actionable finding")
    if verdict in ("revise", "invalid") and not findings:
        errors.append(f"verdict={verdict} requires at least one actionable finding")

    expected_checks = {
        "score_strictly_above_8": number(final) and float(final) > 8.0,
        "verdict_is_pass": verdict == "pass",
        "zero_blocking_findings": not blocking,
        "all_must_requirements_verified": all_must,
        "evidence_integrity_passed": integrity == "pass",
        "required_tests_passed": tests_passed,
        "canonical_smoke_passed": smoke_passed,
    }
    pass_rule = data.get("pass_rule")
    if not isinstance(pass_rule, dict):
        errors.append("pass_rule must be an object")
        pass_rule = {}
    else:
        missing_pass_keys = sorted(PASS_RULE_KEYS - set(pass_rule))
        extra_pass_keys = sorted(set(pass_rule) - PASS_RULE_KEYS)
        if missing_pass_keys:
            errors.append("pass_rule missing fields: " + ", ".join(missing_pass_keys))
        if extra_pass_keys:
            errors.append("pass_rule has unknown fields: " + ", ".join(extra_pass_keys))
    for key, expected in expected_checks.items():
        if pass_rule.get(key) is not expected:
            errors.append(f"pass_rule.{key} is inconsistent")

    objective_pass = (
        mode == "postrun"
        and number(final)
        and float(final) > 8.0
        and not blocking
        and all_must
        and integrity == "pass"
        and tests_passed
        and smoke_passed
    )
    if verdict == "pass" and not objective_pass:
        errors.append("verdict=pass is not allowed when an objective hard gate fails")
    if objective_pass and verdict != "pass":
        errors.append("all objective pass gates hold, so verdict must be pass")
    expected_pass = objective_pass and verdict == "pass"
    if data.get("pass") is not expected_pass:
        errors.append("pass boolean is inconsistent with the conjunctive rule")

    strengths = validate_string_collection(data, "verified_strengths", errors)
    del strengths
    next_actions = validate_string_collection(data, "next_actions", errors)
    validate_string_collection(data, "notes", errors)
    if verdict != "pass" and not next_actions:
        errors.append("a non-pass verdict requires at least one ordered next action")
    if not isinstance(data.get("full_experiment_status"), str) or data.get(
        "full_experiment_status"
    ) not in ("unexecuted", "partial", "complete", "blocked"):
        errors.append("full_experiment_status must use the stable enum")

    errors.extend(secret_errors(raw_json, raw_markdown, commands))
    validate_markdown(raw_markdown, final, verdict, data.get("pass"), blocking, errors)

    if errors:
        print("Review validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"Review is valid: {final}/10, verdict={verdict}, pass={data.get('pass')}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
