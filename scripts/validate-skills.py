#!/usr/bin/env python3
"""Validate the Codex plugin manifest, skills, and OpenAI interfaces."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REQUIRED_INTERFACE_FIELDS = {
    "display_name",
    "short_description",
    "default_prompt",
}


def scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def frontmatter(path: Path) -> tuple[dict[str, str], list[str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    errors: list[str] = []
    if not lines or lines[0] != "---":
        return {}, [f"{path}: missing opening frontmatter delimiter"]

    try:
        closing = lines[1:].index("---") + 1
    except ValueError:
        return {}, [f"{path}: missing closing frontmatter delimiter"]

    fields: dict[str, str] = {}
    for line_number, line in enumerate(lines[1:closing], start=2):
        if ":" not in line:
            errors.append(f"{path}:{line_number}: invalid frontmatter line")
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = scalar(value)
    return fields, errors


def interface_fields(path: Path) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if ":" not in stripped or stripped.startswith("#"):
            continue
        key, value = stripped.split(":", 1)
        if key in REQUIRED_INTERFACE_FIELDS or key == "brand_color":
            fields[key] = scalar(value)
    return fields


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    manifest_path = root / ".codex-plugin" / "plugin.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"{manifest_path}: cannot load manifest: {exc}"]

    skills_path = root / manifest.get("skills", "")
    if not skills_path.is_dir():
        return [f"{manifest_path}: skills directory does not exist: {skills_path}"]

    skill_dirs = sorted(path for path in skills_path.iterdir() if path.is_dir())
    if not skill_dirs:
        errors.append(f"{skills_path}: no skill directories found")

    seen_names: set[str] = set()
    for skill_dir in skill_dirs:
        skill_path = skill_dir / "SKILL.md"
        if not skill_path.is_file():
            errors.append(f"{skill_dir}: missing SKILL.md")
            continue

        fields, frontmatter_errors = frontmatter(skill_path)
        errors.extend(frontmatter_errors)
        name = fields.get("name", "")
        description = fields.get("description", "")
        if name != skill_dir.name:
            errors.append(
                f"{skill_path}: name {name!r} does not match directory {skill_dir.name!r}"
            )
        if name in seen_names:
            errors.append(f"{skill_path}: duplicate skill name {name!r}")
        seen_names.add(name)
        if not description:
            errors.append(f"{skill_path}: description is empty")

        interface_path = skill_dir / "agents" / "openai.yaml"
        if interface_path.is_file():
            fields = interface_fields(interface_path)
            missing = sorted(REQUIRED_INTERFACE_FIELDS - fields.keys())
            for field in missing:
                errors.append(f"{interface_path}: missing interface.{field}")
            prompt = fields.get("default_prompt", "")
            if name and f"${name}" not in prompt:
                errors.append(
                    f"{interface_path}: default_prompt must mention ${name}"
                )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="repository root (default: inferred from this script)",
    )
    args = parser.parse_args()
    errors = validate(args.root.resolve())
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    skill_count = len(
        [path for path in (args.root / "skills").iterdir() if path.is_dir()]
    )
    print(f"Validated {skill_count} Codex skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
