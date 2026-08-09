# Savant OpenAI — Release Readiness Plan

> **Status:** Proposed — not approved for release
> **Date:** 2026-08-09

## Decision

Do not release or publish the repository yet. The implementation pilot is
healthy, but the distributable package and user onboarding surface are not
complete enough for a reliable first release.

## Evidence

- PR #12 is merged to `dev` and CI passes with 51 tests and five validated
  skills.
- The repository has a README, architecture documents, plans, specifications,
  TODOs, and skill instructions.
- There is no dedicated help/reference page for the complete skill catalog.
- There is no tutorial or task-oriented getting-started walkthrough.
- Package materialization and source-to-installed drift checks remain listed as
  unfinished work in `.STATUS` and `docs/ROADMAP.md`.
- No marketplace or installation publication has been approved.

## Required before release

1. **Materialize the package:** define the installable artifact and verify that
   the manifest includes every intended skill and excludes development-only
   files.
2. **Add drift checks:** validate manifest, frontmatter, UI metadata, and
   packaged skill contents from the source tree.
3. **Add help:** provide a concise catalog of skills, invocation examples, and
   boundaries for research verification, teaching, learning review, repo
   scaffolding, and sequential worktrees.
4. **Add a tutorial:** provide one end-to-end first-use path from installation
   to a bounded verification task and one isolated worktree task.
5. **Run release verification:** full tests, skill validation, package
   inspection, clean artifact check, and version/release notes review.
6. **Obtain publication approval:** keep installation, marketplace publication,
   tagging, and downstream distribution as separate explicit gates.

## Not required for the first release

- Runtime evaluation follow-up Phase 5, unless the release claims broader
  statistical confidence than the current evidence supports.
- Codex-only hooks or local enforcement.
- Bidirectional Obsidian synchronization or automatic vault writes.

## Exit gate

Release becomes eligible only when the package artifact, drift checks, help,
tutorial, release notes, and verification results are recorded in `.STATUS`
and the publication action is separately approved.
