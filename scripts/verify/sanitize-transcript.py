#!/usr/bin/env python3
"""Extract and sanitize a runtime session's verdict excerpt for archival.

Reads a codex session transcript (JSONL) and writes the final agent message
(the structured verdict block) with environment-specific paths redacted. The
output must contain no secret-like content; raw dumps are never archived under
the transcript archival policy.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
VALIDATOR_PATH = REPO_ROOT / "scripts" / "learning" / "validate-candidate.py"


class SanitizeError(Exception):
    """A transcript excerpt cannot be safely archived."""


def load_secret_patterns() -> tuple[re.Pattern[str], ...]:
    spec = importlib.util.spec_from_file_location("candidate_validator", VALIDATOR_PATH)
    if spec is None or spec.loader is None:
        raise SanitizeError("candidate validator unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.SECRET_PATTERNS


def last_agent_message(path: Path) -> str:
    message = ""
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") != "item.completed":
            continue
        item = event.get("item")
        if isinstance(item, dict) and item.get("type") == "agent_message":
            message = item.get("text", "") or ""
    return message


def redact(text: str) -> str:
    repo = str(REPO_ROOT)
    text = text.replace(repo + "/", "<repo>/")
    text = text.replace(repo, "<repo>")
    text = re.sub(r"/Users/[A-Za-z0-9_.-]+/\.codex", "<codex-home>", text)
    text = re.sub(r"/Users/[A-Za-z0-9_.-]+/", "<home>/", text)
    for token in ("<repo>", "<home>", "<codex-home>"):
        text = text.replace("<" + token, token)
    return text


def sanitize(path: Path) -> tuple[str, str]:
    """Return (run name, sanitized excerpt) or raise on unsafe content."""
    message = last_agent_message(path)
    if not message:
        raise SanitizeError(f"{path.name}: no final agent message found")
    sanitized = redact(message)
    for pattern in load_secret_patterns():
        if pattern.search(sanitized):
            raise SanitizeError(
                f"{path.name}: secret-like content remains after redaction"
            )
    if re.search(r"/Users/", sanitized):
        raise SanitizeError(f"{path.name}: absolute home path remains after redaction")
    return path.name.removesuffix(".jsonl") + ".txt", sanitized


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("transcripts", nargs="+", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args(argv)

    try:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        for path in args.transcripts:
            name, excerpt = sanitize(path)
            (args.output_dir / name).write_text(excerpt + "\n", encoding="utf-8")
            print(f"WROTE: {args.output_dir / name}")
    except (OSError, SanitizeError) as exc:
        print(f"INVALID: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
