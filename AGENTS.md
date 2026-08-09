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
- Treat `agents/openai.yaml` as skill UI metadata, not as a runtime subagent
  definition.
- Use runtime delegated agents only for bounded, independent, reviewable tasks;
  isolate implementation work in feature worktrees and keep the coordinator on
  the integration branch.
- Prefer explicit `$skill-name` workflows over copied Claude slash-command
  interfaces.

## Workflow

- Work on a non-main feature branch.
- Planning-only work may be authored and committed on local `dev` when it
  touches only the approved planning paths below. Code and implementation work
  still belongs on `feature/*`.
- Do not commit, push, publish, or install the plugin without explicit approval.
- Validate the manifest, skill frontmatter, `agents/openai.yaml` metadata, JSON
  contracts, package shape, and fixtures before handoff.
- Run both the repository validator and the official Codex plugin validator
  when the latter is available.
- Update `.STATUS` when the scaffold or decision state changes.

### Documentation architecture

- Use `docs/ROADMAP.md` for repository-wide sequence, priorities, and gates.
- Use one `docs/specs/SPEC-*.md` for the contract of a bounded new skill or
  port.
- Use one short `docs/plans/PLAN-*.md` for implementation and validation steps.
- Add `docs/todo/TODO-*.md` only when work spans sessions or has explicit
  deferred follow-ups.
- Keep `.STATUS` current with evidence, blockers, and the next approval gate.
- Do not create all four artifacts for a trivial edit.
- Read [the Codex plugin architecture](docs/architecture/CODEX-PLUGIN-ARCHITECTURE.md)
  before starting a new port.

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
