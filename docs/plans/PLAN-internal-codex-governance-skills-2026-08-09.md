# Internal Codex governance skills plan

> **Status:** Proposed — planning only
> **Date:** 2026-08-09

## Decision

Create two focused internal skills:

- `$savant-port` — plan and guide one Claude-to-Codex workflow port;
- `$savant-plugin-check` — validate plugin structure and release readiness.

Do not create a generic `$plan` command. Use native Codex planning for the
current task and persist approved plans under `docs/plans/`.

## Architecture

```text
AGENTS.md
  └── always-on repository rules

$savant-port
  └── spec → plan → skill → tests → docs → PR

$savant-plugin-check
  └── manifest → skills → metadata → package → docs → tests

$sequential-wt
  └── isolated feature worktree and worker handoff
```

Keep responsibilities separate. `$savant-port` creates and coordinates a
bounded change; `$savant-plugin-check` audits it; `$sequential-wt` isolates
file changes. None of them merges, pushes, publishes, or bypasses approval.

## Phase 1 — `$savant-plugin-check`

### Scope

Build a concise skill that audits the current repository without changing it by
default.

### Checks

- `.codex-plugin/plugin.json` parses and points to `skills/`;
- every skill has matching frontmatter and valid UI metadata;
- optional references/scripts/assets are skill-local and discoverable;
- help/tutorial links cover the installed skill catalog;
- repository tests and skill validation pass;
- official Codex plugin validation passes when available;
- package contents can be inspected from a clean temporary copy.

### Output

Report `PASS`, `WARN`, or `FAIL` with exact paths, failed checks, and the next
action. Default mode is read-only; any repair mode requires explicit approval.

## Phase 2 — `$savant-port`

### Scope

Guide one workflow from the Claude Savant plugin into a Codex-native skill.

### Workflow

1. Identify the Claude workflow and user outcome.
2. Record source boundaries and reject mechanical copying.
3. Choose a short `$skill-name` and define inputs/outputs.
4. Create or update the feature spec and implementation plan.
5. Create the skill with concise `SKILL.md` instructions.
6. Add `agents/openai.yaml` UI metadata and skill-local resources only when
   needed.
7. Add fixtures, tests, help/tutorial entries, and `.STATUS` evidence.
8. Run `$savant-plugin-check` and the repository test suite.
9. Prepare a reviewable feature PR; leave merge/publish approval explicit.

### Required port fields

- Codex invocation;
- tools and filesystem scope;
- context-loading policy;
- deterministic scripts;
- approval and safety boundaries;
- compact output/report format;
- positive, negative, unavailable, or safety fixtures;
- explicit non-goals and Claude behaviors not ported.

## Phase 3 — First use

Use `$savant-port` to port `research-session` as the first Wave 1 workflow,
then run `$savant-plugin-check` against the resulting feature branch.

## Acceptance criteria

- Both skills follow the native `skills/<name>/SKILL.md` structure.
- Each has valid frontmatter and `agents/openai.yaml` metadata.
- The checker is read-only by default and produces actionable output.
- The port skill does not copy Claude commands, hooks, settings, or state.
- A realistic `research-session` port can follow the workflow end to end.
- Existing tests, package validation, approval gates, and repository boundaries
  remain intact.

## Deferred

- Generic `$plan` command.
- Automatic repair mode.
- Automatic PR creation, merging, publishing, or installation.
- Parallel agent orchestration inside the plugin skills.
