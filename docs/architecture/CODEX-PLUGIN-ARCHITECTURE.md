# Codex plugin architecture

## Purpose

`savant-openai` is a native Codex plugin. It ports selected Savant research
outcomes one workflow at a time while using Codex's plugin, skill, validation,
approval, and worktree conventions.

## Runtime structure

```text
.codex-plugin/plugin.json
        │
        ▼
skills/<skill-name>/SKILL.md
        ├── agents/openai.yaml   optional UI metadata
        ├── references/           optional progressive context
        ├── scripts/              optional deterministic operations
        └── assets/               optional output resources
```

`agents/openai.yaml` describes a skill to Codex; it does not define a runtime
subagent. Runtime agents are task-level workers and should receive isolated
worktrees when they modify files.

## Porting model

Claude Savant is the behavioral source for selected workflows, not a file or
command template. Each port translates:

```text
Claude outcome → Codex skill → Codex-native tools/resources → tested PR
```

Do not copy Claude commands, hooks, settings, session state, or marketplace
metadata. Use `$skill-name` as the Codex-facing invocation.

## Documentation model

Keep the artifact stack proportional to the work:

| Artifact | Use |
| --- | --- |
| `docs/ROADMAP.md` | Repository-wide waves, priorities, and release gates. |
| `docs/specs/SPEC-*.md` | Contract for one bounded feature or port. |
| `docs/plans/PLAN-*.md` | Ordered implementation and validation steps. |
| `docs/todo/TODO-*.md` | Multi-session checklist or explicitly deferred work. |
| `.STATUS` | Current state, completed evidence, blockers, and next gate. |

Small edits do not require all four planning artifacts. A new skill normally
needs a spec and short plan; a multi-phase port may also need a TODO.

## Agent and worktree model

The coordinator remains on `dev`. A worker that modifies files operates in a
`feature/*` worktree created from `dev`. The worker reports changed files,
checks, and blockers; the coordinator reviews the actual diff. Agents do not
merge, push, publish, or bypass approval gates.

## Acceptance gates

Every new skill or port must pass:

1. valid plugin manifest and skill frontmatter;
2. valid UI metadata when `agents/openai.yaml` exists;
3. focused context and no unnecessary global instructions;
4. deterministic scripts for repeatable operations;
5. relevant positive, negative, unavailable, or safety fixtures;
6. repository and official Codex plugin validation;
7. documentation updates proportional to the change;
8. independent diff review before integration.

Publication, installation, tagging, and downstream distribution remain separate
approval gates.
