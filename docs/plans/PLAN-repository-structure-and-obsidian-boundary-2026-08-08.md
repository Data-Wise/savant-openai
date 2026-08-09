# Savant OpenAI — Repository Structure and Obsidian Boundary Plan

> **Status:** Phase 1–2 recorded; repo-to-vault publishing remains proposed
> **Date:** 2026-08-08
> **Source:** Claude Savant `research-scaffold` and `repo` conventions, adapted for a non-research OpenAI plugin repository

## Objective

Document and preserve a clear repository structure for `savant-openai` while
defining the boundary between repository-owned planning state and optional
Obsidian integration.

The repository is a distributable OpenAI plugin, not a manuscript or research
project. It should borrow Savant's disciplined scaffold signals without adopting
research-only lifecycle files or vault assumptions.

## Current state

The core structure already exists:

- `.STATUS` — repository state, completed work, next approval gate, and blockers.
- `README.md` — repository landing page and plugin overview.
- `docs/ROADMAP.md` — forward-looking priorities and approval gates.
- `docs/plans/` — implementation and follow-up plans.
- `docs/todo/` — bounded work lists.
- `docs/specs/` — formal contracts and acceptance criteria.
- `docs/architecture/` — boundary and design decisions.

The working tree also contains an untracked `.codex/config.toml`; this is
outside the scope of this plan and must not be silently incorporated.

The approved bridge now exists at `.flow/obsidian-sync.yml` with one reviewed
vault-to-repository pair targeting `docs/obsidian/`. It does not make planning
documents vault-authored or authorize repository-to-vault publishing.

## Decisions

### D1 — Repository state remains canonical

`.STATUS`, the roadmap, plans, TODOs, specs, and architecture documents remain
owned by this git repository. They are not treated as vault-authored mirror
content.

### D2 — Do not adopt research-only scaffold stages

Do not add Savant research lifecycle artifacts such as manuscript stages,
paper-numbered vault trees, Quarto manuscript placeholders, research configs,
voice profiles, or corpus bindings. They do not describe this plugin.

### D3 — `.flow/obsidian-sync.yml` is optional bridge infrastructure

Add `.flow/obsidian-sync.yml` only when a real vault-to-repository mapping is
needed and its source-of-truth direction is accepted. An empty scaffold has no
sync behavior and should not be presented as a mechanism for publishing repo
planning docs into Obsidian.

### D4 — No automatic repo-to-vault publishing in this plan

This plan does not authorize copying or overwriting files in the Obsidian
vault. A repo-to-vault publishing workflow requires a separate design covering
conflict policy, destination ownership, dry-run behavior, and approval gates.

## Proposed phases

### Phase 1 — Structure verification

- Confirm the required files and directories listed above remain present.
- Keep `.STATUS` as the authoritative current-state source.
- Keep `docs/ROADMAP.md` synchronized with `.STATUS` when priorities change.
- Ensure new plans/specs identify status, source evidence, scope, and exit gates.

**Exit gate:** a read-only structure check reports all required surfaces and no
missing planning directory.

### Phase 2 — Optional flow decision — complete

- Decide whether this repository has genuine vault-authored Markdown to mirror.
- A genuine vault-authored Markdown mirror exists, so
  `.flow/obsidian-sync.yml` was created on the feature branch with an explicit
  `vault_root` and one reviewed pair targeting `docs/obsidian/`.
- If no, leave `.flow/` absent; the absence is informational and does not make
  the repository incomplete.

**Exit gate:** satisfied by the reviewed `.flow/obsidian-sync.yml` bridge and
the recorded source-of-truth boundary.

### Phase 3 — Future publishing design, only if needed

Create a separate spec before implementing repo-to-vault publishing. It must
define:

- canonical owner for each file class;
- destination paths in the `Documents` vault;
- one-way versus bidirectional behavior;
- dry-run, diff, and approval requirements;
- handling for stale, missing, or conflicting files.

**Exit gate:** no write operation is implemented until those rules are approved.

## Acceptance criteria

- `.STATUS`, `README.md`, roadmap, plans, TODOs, specs, and architecture docs
  are present and repository-owned.
- No research-specific scaffold is introduced solely for structural symmetry.
- `.flow/obsidian-sync.yml` is not added without a real mirror pair and a clear
  source-of-truth decision.
- Any future vault write is dry-run capable, diff-visible, and explicitly
  approved.
- The untracked `.codex/config.toml` is handled separately from this plan.

## Non-goals

- Publishing the plugin to a marketplace.
- Modifying the Claude Savant repository.
- Creating or changing Obsidian vault files.
- Adding Codex lifecycle hooks.
- Reorganizing the existing planning tree without evidence of a need.

## Recommended next action

Run the Phase 1 read-only structure check. The vault-to-repository bridge is
now present; keep repository planning documents canonical and use the separate
publishing-boundary spec before adding any repo-to-vault write behavior.
