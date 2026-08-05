#!/usr/bin/env python3
"""Validate a bounded-learning candidate without third-party dependencies."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


SCHEMA_PATH = (
    Path(__file__).resolve().parents[2]
    / "openai"
    / "portable"
    / "learning"
    / "contracts"
    / "candidate-lesson.schema.json"
)
REPO_ROOT = Path(__file__).resolve().parents[2]
MAX_CANDIDATE_BYTES = 8192
SECRET_PATTERNS = (
    re.compile(r"\bsk-[A-Za-z0-9]{12,}\b"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"\b(?:api[_ -]?key|password|secret|token)\s*[:=]\s*\S+", re.I),
)
PROMPT_INJECTION_PATTERNS = (
    re.compile(
        r"\b(?:ignore|disregard|override)\s+(?:all\s+)?(?:previous|prior|above)\s+instructions\b",
        re.I,
    ),
    re.compile(r"\b(?:system|developer)\s+message\s*[:=]", re.I),
)
USER_CORRECTION_REF = re.compile(r"^user-report:[A-Za-z0-9][A-Za-z0-9._:-]*$")


class ValidationError(Exception):
    """A candidate violates the portable learning contract."""


def load_schema() -> dict[str, Any]:
    try:
        return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValidationError(f"schema unavailable: {exc}") from exc


def validate_schema(value: Any, schema: dict[str, Any], path: str = "$", errors=None):
    errors = [] if errors is None else errors
    expected_type = schema.get("type")
    if expected_type == "object":
        if not isinstance(value, dict):
            errors.append(f"{path}: expected object")
            return errors
        required = schema.get("required", [])
        for name in required:
            if name not in value:
                errors.append(f"{path}.{name}: required")
        if schema.get("additionalProperties") is False:
            allowed = set(schema.get("properties", {}))
            for name in value:
                if name not in allowed:
                    errors.append(f"{path}.{name}: unknown field")
        for name, child_schema in schema.get("properties", {}).items():
            if name in value:
                validate_schema(value[name], child_schema, f"{path}.{name}", errors)
    elif expected_type == "string":
        if not isinstance(value, str):
            errors.append(f"{path}: expected string")
            return errors
        if len(value) < schema.get("minLength", 0):
            errors.append(f"{path}: too short")
        if len(value) > schema.get("maxLength", float("inf")):
            errors.append(f"{path}: too long")
        pattern = schema.get("pattern")
        if pattern and re.fullmatch(pattern, value) is None:
            errors.append(f"{path}: invalid format")
    elif expected_type == "array":
        if not isinstance(value, list):
            errors.append(f"{path}: expected array")
            return errors
        item_schema = schema.get("items")
        if item_schema:
            for index, item in enumerate(value):
                validate_schema(item, item_schema, f"{path}[{index}]", errors)
    elif expected_type == "boolean" and not isinstance(value, bool):
        errors.append(f"{path}: expected boolean")
    elif expected_type == "number" and not isinstance(value, (int, float)):
        errors.append(f"{path}: expected number")

    if "const" in schema and value != schema["const"]:
        errors.append(f"{path}: must equal {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: unsupported value")
    if schema.get("format") == "date-time" and isinstance(value, str):
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            errors.append(f"{path}: invalid date-time")
        else:
            if parsed.tzinfo is None:
                errors.append(f"{path}: invalid date-time; timezone required")
    return errors


def find_secrets(value: Any, path: str = "$") -> list[str]:
    if isinstance(value, dict):
        findings = []
        for key, child in value.items():
            findings.extend(find_secrets(child, f"{path}.{key}"))
        return findings
    if isinstance(value, list):
        findings = []
        for index, child in enumerate(value):
            findings.extend(find_secrets(child, f"{path}[{index}]"))
        return findings
    if isinstance(value, str):
        return [f"{path}: secret-like content"] if any(
            pattern.search(value) for pattern in SECRET_PATTERNS
        ) else []
    return []


def find_prompt_injections(value: Any, path: str = "$") -> list[str]:
    if isinstance(value, dict):
        findings = []
        for key, child in value.items():
            findings.extend(find_prompt_injections(child, f"{path}.{key}"))
        return findings
    if isinstance(value, list):
        findings = []
        for index, child in enumerate(value):
            findings.extend(find_prompt_injections(child, f"{path}[{index}]"))
        return findings
    if isinstance(value, str):
        return [f"{path}: prompt-injection-like content"] if any(
            pattern.search(value) for pattern in PROMPT_INJECTION_PATTERNS
        ) else []
    return []


def validate_evidence_reference(value: dict[str, Any]) -> list[str]:
    evidence = value.get("evidence")
    if not isinstance(evidence, dict):
        return []
    evidence_type = evidence.get("type")
    reference = evidence.get("ref")
    if not isinstance(reference, str):
        return []

    if evidence_type == "user_correction":
        if USER_CORRECTION_REF.fullmatch(reference) is None:
            return [
                "$.evidence.ref: user corrections must use a user-report:<id> reference"
            ]
        return []

    reference_path = Path(reference)
    if reference_path.is_absolute():
        return ["$.evidence.ref: absolute paths are not allowed"]
    resolved = (REPO_ROOT / reference_path).resolve()
    try:
        resolved.relative_to(REPO_ROOT)
    except ValueError:
        return ["$.evidence.ref: path escapes the repository"]
    if not resolved.is_file():
        return ["$.evidence.ref: referenced evidence file does not exist"]
    return []


def validate_candidate(path: Path) -> list[str]:
    try:
        raw = path.read_bytes()
    except OSError as exc:
        return [f"input: cannot read file: {exc}"]
    if len(raw) > MAX_CANDIDATE_BYTES:
        return [f"input: size exceeds {MAX_CANDIDATE_BYTES} bytes"]
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        return [f"input: invalid JSON at line {exc.lineno}, column {exc.colno}"]

    errors = validate_schema(value, load_schema())
    errors.extend(validate_evidence_reference(value))
    errors.extend(find_secrets(value))
    errors.extend(find_prompt_injections(value))
    if isinstance(value, dict):
        if value.get("redaction_status") == "failed":
            errors.append("$.redaction_status: failed candidates cannot persist")
        if value.get("lifecycle_status") in {"approved", "rejected", "superseded"}:
            if not value.get("reviewed_at"):
                errors.append("$.reviewed_at: required for reviewed lifecycle status")
    return sorted(set(errors))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate", type=Path)
    args = parser.parse_args(argv)
    errors = validate_candidate(args.candidate)
    if errors:
        for error in errors:
            print(f"INVALID: {error}", file=sys.stderr)
        return 1
    print(f"VALID: {args.candidate}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
