# Spec: Repository-to-Obsidian Publishing Boundary

> **Status:** Proposed — not approved for implementation
> **Date:** 2026-08-08
> **Related plan:** [Repository structure and Obsidian boundary](../plans/PLAN-repository-structure-and-obsidian-boundary-2026-08-08.md)

## 1. Problem

`Savant`'s `.flow/obsidian-sync.yml` contract is designed primarily for
vault-authored Markdown flowing into a git repository. `savant-openai` has the
opposite ownership model: `.STATUS`, the roadmap, and planning documents are
maintained in the repository.

Adding `.flow` by analogy would not publish those documents to Obsidian and
could imply the wrong source of truth. A separate, explicit contract is needed
before any repository-to-vault write is introduced.

## 2. Objective

Define a safe, reviewable mechanism for publishing selected repository planning
documents into the local Obsidian `Documents` vault, if that capability is
approved later.

## 3. Scope

The candidate source set is:

- `.STATUS`
- `README.md`
- `docs/ROADMAP.md`
- `docs/plans/**`
- `docs/todo/**`
- `docs/specs/**`
- `docs/architecture/**`

The initial destination namespace is proposed as:

`Engineering/dev-tools/savant-openai/`

The repository remains the canonical source for every file in this set.

## 4. Required behavior

### 4.1 Preview first

The default operation must be read-only and report:

- source files selected;
- destination paths;
- files that would be created, updated, or skipped;
- content hashes or an equivalent diff signal;
- source and destination timestamps where available.

### 4.2 Explicit approval before writes

Writing to the vault requires an explicit per-run approval after the complete
preview is shown. There must be no implicit write triggered by restore, recap,
tests, or ordinary git operations.

### 4.3 Reuse the existing Obsidian contract

The publisher must not add a new `.yml` or `.yaml` file. It reuses the existing
`.flow/obsidian-sync.yml` only as a `vault_root` seed, following Savant's
established report-delivery resolution order:

1. confirmed `.remember/obsidian-vault.yml` cache, when present;
2. `.flow/obsidian-sync.yml`'s `vault_root`, when present and valid;
3. the registered vault returned by the Obsidian MCP;
4. an explicit destination choice if more than one vault or folder is valid.

The publisher must not use the `pairs` entries to reverse the direction of
`obs:sync`; vault → repository remains the meaning of those pairs.

### 4.4 One-way ownership

The first implementation, if approved, is one-way:

`repository → Obsidian vault`

Vault edits must not be merged back automatically. If a destination file is
newer or differs, the tool must report a conflict and stop unless an explicit
overwrite decision is made.

### 4.5 Obsidian MCP write path

Publishing must use the existing Obsidian MCP contract:

- call `list_vaults` before resolving a destination;
- write new notes with `create_note(vault_id, title, content, subfolder)`;
- resolve existing notes before using `write_note`;
- call `analyze_vault` after a successful write so the note is indexed;
- write the confirmed `(vault_id, subfolder)` to the existing
  `.remember/obsidian-vault.yml` cache only after success.

If the MCP is unavailable, the command must report the local source and skip
the vault write without treating that as a repository failure.

### 4.6 Safe path handling

- Destination paths must remain under the `Documents` vault root.
- Source and destination paths must be explicit and normalized.
- No `..`, absolute destination override, symlink escape, or broad recursive
  destination is permitted.
- The operation must never delete vault files in the initial version.

### 4.7 Stable naming

The publishing map must preserve repository-relative names where possible.
`.STATUS` requires an explicit destination filename because it has no `.md`
extension; the proposed name is `_STATUS-savant-openai.md`.

## 5. Proposed mapping

| Repository source | Proposed vault destination |
| --- | --- |
| `.STATUS` | `Engineering/dev-tools/savant-openai/_STATUS-savant-openai.md` |
| `README.md` | `Engineering/dev-tools/savant-openai/README.md` |
| `docs/ROADMAP.md` | `Engineering/dev-tools/savant-openai/ROADMAP.md` |
| `docs/plans/**` | `Engineering/dev-tools/savant-openai/plans/**` |
| `docs/todo/**` | `Engineering/dev-tools/savant-openai/todo/**` |
| `docs/specs/**` | `Engineering/dev-tools/savant-openai/specs/**` |
| `docs/architecture/**` | `Engineering/dev-tools/savant-openai/architecture/**` |

This table is proposed, not an authorization to write those files.

## 6. Exclusions

The initial implementation must not publish:

- `.git/`, `.codex/`, `.claude/`, or environment configuration;
- generated artifacts, caches, logs, or secrets;
- source code or plugin runtime files;
- files outside the candidate source set;
- files from the Claude Savant, Craft, Atlas, or Obsidian CLI repositories.

## 7. Acceptance criteria

- A dry run produces a complete source-to-destination manifest without writes.
- A changed source produces a visible content diff or hash change.
- No write occurs without explicit approval after preview.
- Destination paths cannot escape the configured vault root.
- Existing vault files are never deleted automatically.
- Newer or conflicting destination files stop the operation by default.
- `.STATUS` and all planning documents remain canonical in `savant-openai`.
- The mechanism may use `.flow/obsidian-sync.yml` for vault-root discovery, but
  never uses it to reverse the ownership direction.

## 8. Open decisions before implementation

1. Confirm `_STATUS-savant-openai.md` as the vault-facing name for `.STATUS`.
2. Confirm whether `README.md` belongs in the vault or should remain repo-only.
3. Choose the implementation owner: a Savant command, a small repository
   script, or a Codex-specific workflow.
4. Decide whether the destination namespace should be a folder or a single
   project index linking to the source files.
5. Define how vault-side edits are surfaced without becoming automatic inputs.

## 9. Proposed implementation flow

The implementation should expose one explicit, bounded operation with a
read-only default:

```text
discover → build manifest → preview diff → approve → publish → verify → report
```

### Step 1 — Discover

Resolve the repository root and configured vault root. Refuse to continue when
either root is missing, ambiguous, or outside the approved locations. Select
only the source set in Section 3.

### Step 2 — Build manifest

For each selected source, compute:

- repository-relative source path;
- exact vault destination path;
- source existence and size;
- source hash;
- destination existence, size, timestamp, and hash when present;
- proposed action: `create`, `update`, `skip`, or `conflict`.

The manifest must be serializable as JSON for audit and test fixtures.

### Step 3 — Preview

Print the complete manifest and content diffs for `create` and `update`
actions. The preview must identify conflicts separately and must not write any
file. A `--dry-run` or equivalent mode must produce the same manifest without
requiring an approval prompt.

### Step 4 — Approve

Ask for explicit approval after the preview. Approval applies only to the
current manifest and current source hashes. If a source changes after preview,
invalidate the approval and rebuild the manifest.

### Step 5 — Publish

Create parent directories as needed and write only approved `create` or
`update` entries. Use atomic temporary-file replacement. Never delete files,
follow destination symlinks, or write outside the vault root.

### Step 6 — Verify

Recompute destination hashes and confirm that every approved action matches the
source hash. Report any partial failure without attempting an unapproved
rollback or cleanup.

### Step 7 — Report

Emit a machine-readable result containing the manifest, approval decision,
completed actions, skipped entries, conflicts, failures, and verification
results. A human-readable summary should include the destination root and the
next action for every unresolved conflict.

## 10. Suggested command surface

The first implementation may be a small repository script or Savant command,
but it should preserve this interface:

```text
obs:publish --dry-run
obs:publish --preview
obs:publish --apply
obs:publish --manifest PATH
```

`--apply` must not bypass the preview or approval gate. A future automation
caller may consume the manifest, but it must not silently authorize writes.

## 11. Non-goals

- Bidirectional synchronization.
- Automatic Obsidian vault writes during session restore.
- Replacing Savant's research-specific vault scaffolding.
- Adding `.flow` solely to satisfy a structural convention.
- Committing, pushing, or publishing this spec without separate approval.
