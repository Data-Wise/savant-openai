# savant-openai agent instructions

This repository contains the OpenAI-facing adapter for Savant research
verification. Keep it portable, small, and evidence-first.

## Where to look

- [README.md](README.md) — landing page and skills overview.
- [docs/ROADMAP.md](docs/ROADMAP.md) — forward-looking work, priorities, and gates.
- [.STATUS](.STATUS) — current project state.
- [docs/architecture/SAVANT-OPENAI-PLAN.md](docs/architecture/SAVANT-OPENAI-PLAN.md)
  — pilot plan and boundary decisions.

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
- Planning-only work may be authored and committed on local `dev` when it
  touches only the approved planning paths below. Code and implementation work
  still belongs on `feature/*`.
- Do not commit, push, publish, or install the plugin without explicit approval.
- Validate the manifest, skill frontmatter, JSON contracts, and fixtures before handoff.
- Update `.STATUS` when the scaffold or decision state changes.

### Planning-only paths allowed on `dev`

- `.STATUS`
- `docs/plans/**`
- `docs/todo/**`
- `docs/specs/**`
- `docs/adr/**`
- `docs/architecture/**`

Keep planning commits limited to these paths. Do not mix code, tests, skills,
manifests, scripts, generated artifacts, or `.github/workflows/**` into a
planning commit. GitHub protection still requires a pull request to publish a
commit to remote `dev`; this exception does not authorize a direct push.
