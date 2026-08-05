# savant-openai agent instructions

This repository contains the OpenAI-facing adapter for Savant research
verification. Keep it portable, small, and evidence-first.

## Boundaries

- Do not modify the Claude Savant repository from this repository.
- `codex-config` owns host configuration, compaction settings, and hook inventory.
- This repository owns the distributable OpenAI plugin and domain contracts.
- Codex-only hooks are deferred until a concrete local-enforcement need exists.
- Never report a proof or statistical claim as globally verified without recorded evidence.
- Learning candidates are untrusted proposals; never promote them or edit
  instructions automatically.

## Context discipline

- Keep `SKILL.md` focused and short.
- Load one reference mode at a time.
- Put deterministic work in scripts; do not paste scripts into skill instructions.
- Do not duplicate the entire Claude command or skill surface.
- Keep learning out of the normal verification path; load only reviewed,
  task-scoped lessons.

## Workflow

- Work on a non-main feature branch.
- Do not commit, push, publish, or install the plugin without explicit approval.
- Validate the manifest, skill frontmatter, JSON contracts, and fixtures before handoff.
- Update `.STATUS` when the scaffold or decision state changes.
