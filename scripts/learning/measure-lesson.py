#!/usr/bin/env python3
"""Measure scoped lesson context without making a model-verdict claim."""

from __future__ import annotations

import argparse
import importlib.util
import json
import math
import sys
from pathlib import Path
from typing import Any


VALIDATOR_PATH = Path(__file__).with_name("validate-candidate.py")
VERDICTS = {"VERIFIED", "PARTIALLY_VERIFIED", "FAILED", "UNVERIFIED"}


class MeasurementError(Exception):
    """A dogfood measurement cannot be trusted or compared."""


def load_validator():
    spec = importlib.util.spec_from_file_location("candidate_validator", VALIDATOR_PATH)
    if spec is None or spec.loader is None:
        raise MeasurementError("candidate validator unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise MeasurementError(f"cannot load {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise MeasurementError(f"{path} must contain a JSON object")
    return value


def load_approved_lesson(path: Path) -> dict[str, Any]:
    validator = load_validator()
    errors = validator.validate_candidate(path)
    if errors:
        raise MeasurementError("lesson rejected: " + "; ".join(errors))
    lesson = load_json(path)
    if lesson.get("lifecycle_status") != "approved":
        raise MeasurementError("lesson must have lifecycle_status=approved")
    return lesson


def estimate_tokens(text: str) -> int:
    """Estimate tokens conservatively as four UTF-8 bytes per token."""
    return max(1, math.ceil(len(text.encode("utf-8")) / 4))


def baseline_context(fixture: dict[str, Any]) -> str:
    return f"TASK CLASS: {fixture['mode']}\nCLAIM: {fixture['claim']}\n"


def lesson_context(lesson: dict[str, Any]) -> str:
    return (
        f"LESSON SCOPE: {lesson['scope']}\n"
        f"OBSERVED FAILURE: {lesson['observed_failure']}\n"
        f"DESIRED BEHAVIOR: {lesson['desired_behavior']}\n"
        f"EVIDENCE: {lesson['evidence']['type']} {lesson['evidence']['ref']}\n"
    )


def build_report(
    fixture: dict[str, Any], lesson: dict[str, Any], assisted_verdict: str
) -> dict[str, Any]:
    expected_scope = f"savant-research-verify/{fixture['mode']}"
    if lesson.get("task_class") != fixture.get("mode"):
        raise MeasurementError("lesson scope does not match fixture task class")
    if lesson.get("scope") != expected_scope:
        raise MeasurementError(f"lesson scope must equal {expected_scope}")

    baseline = baseline_context(fixture)
    assisted = baseline + lesson_context(lesson)
    baseline_verdict = fixture.get("expected_verdict")
    if baseline_verdict not in VERDICTS:
        raise MeasurementError("fixture expected_verdict is not a verification status")
    if assisted_verdict not in VERDICTS:
        raise MeasurementError("with-lesson-verdict is not a verification status")
    if baseline_verdict != "VERIFIED" and assisted_verdict == "VERIFIED":
        raise MeasurementError(
            "unsupported verdict upgrade: a lesson cannot turn non-VERIFIED evidence into VERIFIED"
        )

    return {
        "measurement_schema_version": "1.0",
        "fixture": fixture["id"],
        "lesson": lesson["id"],
        "scope": lesson["scope"],
        "baseline": {
            "verdict": baseline_verdict,
            "estimated_tokens": estimate_tokens(baseline),
        },
        "with_lesson": {
            "verdict": assisted_verdict,
            "estimated_tokens": estimate_tokens(assisted),
        },
        "normal_verification": {
            "learning_context_loaded": False,
            "estimated_tokens": estimate_tokens(baseline),
        },
        "review_only": {
            "learning_context_loaded": True,
            "added_tokens": estimate_tokens(assisted) - estimate_tokens(baseline),
        },
        "verdict_preserved": baseline_verdict == assisted_verdict,
        "token_estimator": "ceil(UTF-8 bytes / 4); heuristic, not model-token accounting",
    }


def write_report(path: Path, report: dict[str, Any]) -> None:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    except OSError as exc:
        raise MeasurementError(f"cannot write report: {exc}") from exc


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fixture", type=Path)
    parser.add_argument("lesson", type=Path)
    parser.add_argument("--with-lesson-verdict", required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)

    try:
        report = build_report(
            load_json(args.fixture),
            load_approved_lesson(args.lesson),
            args.with_lesson_verdict,
        )
        rendered = json.dumps(report, indent=2, sort_keys=True)
        if args.output:
            write_report(args.output, report)
    except MeasurementError as exc:
        print(f"INVALID: {exc}", file=sys.stderr)
        return 1

    print(rendered)
    return 0 if report["verdict_preserved"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
