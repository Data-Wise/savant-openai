#!/usr/bin/env python3
"""Apply an explicit human-reviewed bounded-learning state transition."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


VALIDATOR_PATH = Path(__file__).with_name("validate-candidate.py")
LESSON_ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]{2,63}$")


class PromotionError(Exception):
    """A requested review transition cannot be applied safely."""


def load_validator():
    spec = importlib.util.spec_from_file_location("candidate_validator", VALIDATOR_PATH)
    if spec is None or spec.loader is None:
        raise PromotionError("candidate validator unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def reviewed_timestamp(value: str | None) -> str:
    if value is None:
        return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace(
            "+00:00", "Z"
        )
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise PromotionError("reviewed-at must be an ISO 8601 date-time") from exc
    if parsed.tzinfo is None:
        raise PromotionError("reviewed-at must include a timezone")
    return value


def load_candidate(path: Path) -> dict[str, Any]:
    validator = load_validator()
    errors = validator.validate_candidate(path)
    if errors:
        raise PromotionError("candidate rejected: " + "; ".join(errors))
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PromotionError(f"candidate cannot be loaded: {exc}") from exc
    if not isinstance(value, dict):
        raise PromotionError("candidate must be a JSON object")
    return value


def require_candidate_state(candidate: dict[str, Any]) -> None:
    if candidate.get("lifecycle_status") != "candidate":
        raise PromotionError("only lifecycle_status=candidate may be reviewed")


def lesson_path(store: Path, state: str, lesson_id: str) -> Path:
    if LESSON_ID_PATTERN.fullmatch(lesson_id) is None:
        raise PromotionError("lesson id has an unsafe format")
    return store / state / f"{lesson_id}.json"


def atomic_write(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle = tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        dir=path.parent,
        prefix=f".{path.name}.",
        delete=False,
    )
    try:
        with handle:
            json.dump(value, handle, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(handle.name, path)
    except OSError as exc:
        try:
            os.unlink(handle.name)
        except OSError:
            pass
        raise PromotionError(f"cannot write {path}: {exc}") from exc


def write_reviewed(candidate: dict[str, Any], state: str, store: Path, timestamp: str) -> Path:
    destination = lesson_path(store, state, candidate["id"])
    if destination.exists():
        raise PromotionError(f"destination already exists: {destination}")
    reviewed = dict(candidate)
    reviewed["lifecycle_status"] = state
    reviewed["reviewed_at"] = timestamp
    atomic_write(destination, reviewed)
    return destination


def approve(candidate_path: Path, store: Path, timestamp: str) -> str:
    candidate = load_candidate(candidate_path)
    require_candidate_state(candidate)
    destination = write_reviewed(candidate, "approved", store, timestamp)
    return f"APPROVED: {destination}"


def reject(candidate_path: Path, store: Path, timestamp: str) -> str:
    candidate = load_candidate(candidate_path)
    require_candidate_state(candidate)
    destination = write_reviewed(candidate, "rejected", store, timestamp)
    return f"REJECTED: {destination}"


def supersede(
    candidate_path: Path, store: Path, old_id: str, timestamp: str
) -> str:
    candidate = load_candidate(candidate_path)
    require_candidate_state(candidate)
    old_path = lesson_path(store, "approved", old_id)
    if not old_path.exists():
        raise PromotionError(f"approved lesson not found: {old_id}")
    new_path = lesson_path(store, "approved", candidate["id"])
    if new_path.exists():
        raise PromotionError(f"destination already exists: {new_path}")
    superseded_path = lesson_path(store, "superseded", old_id)
    if superseded_path.exists():
        raise PromotionError(f"destination already exists: {superseded_path}")

    old = load_candidate(old_path)
    if old.get("lifecycle_status") != "approved":
        raise PromotionError(f"stored lesson is not approved: {old_id}")

    new = dict(candidate)
    new["lifecycle_status"] = "approved"
    new["reviewed_at"] = timestamp
    superseded = dict(old)
    superseded["lifecycle_status"] = "superseded"
    superseded["reviewed_at"] = timestamp

    try:
        atomic_write(new_path, new)
        atomic_write(superseded_path, superseded)
        old_path.unlink()
    except (OSError, PromotionError) as exc:
        rollback_errors = []
        for path in (new_path, superseded_path):
            try:
                path.unlink(missing_ok=True)
            except OSError as rollback_error:
                rollback_errors.append(f"{path}: {rollback_error}")
        message = f"supersede aborted and rolled back: {exc}"
        if rollback_errors:
            message += "; rollback incomplete: " + "; ".join(rollback_errors)
        raise PromotionError(message) from exc
    return f"SUPERSEDED: {old_id}; APPROVED: {new_path}"


def revert(lesson_id: str, store: Path) -> str:
    destination = lesson_path(store, "approved", lesson_id)
    if not destination.exists():
        raise PromotionError(f"approved lesson not found: {lesson_id}")
    try:
        destination.unlink()
    except OSError as exc:
        raise PromotionError(f"cannot revert {destination}: {exc}") from exc
    return f"REVERTED: {lesson_id} (restore with version control if needed)"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="action", required=True)
    for action in ("approve", "reject", "supersede"):
        subparser = subparsers.add_parser(action)
        subparser.add_argument("candidate", type=Path)
        subparser.add_argument("--store", type=Path, required=True)
        subparser.add_argument("--reviewed-at")
        if action == "supersede":
            subparser.add_argument("--supersedes", required=True)
    revert_parser = subparsers.add_parser("revert")
    revert_parser.add_argument("lesson_id")
    revert_parser.add_argument("--store", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.action == "revert":
            message = revert(args.lesson_id, args.store)
        else:
            timestamp = reviewed_timestamp(args.reviewed_at)
            if args.action == "approve":
                message = approve(args.candidate, args.store, timestamp)
            elif args.action == "reject":
                message = reject(args.candidate, args.store, timestamp)
            else:
                message = supersede(
                    args.candidate, args.store, args.supersedes, timestamp
                )
    except PromotionError as exc:
        print(f"INVALID: {exc}", file=sys.stderr)
        return 1
    print(message)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
