# Repository workflow and protection

- Repository: `Data-Wise/savant-openai`
- Default integration branch: `dev`
- Implementation branches: `feature/*`
- Release branch: `main` when a release workflow is introduced

## Current state

- `dev` is the GitHub default branch and the integration target.
- `feature/*` branches hold implementation work and merge into `dev` through
  pull requests.
- `main` is reserved for a future release path; it is not created or protected
  by this setup.
- The repository is public, and no status check is required until CI exists.

## Protection boundary

GitHub branch protection is repository-wide. GitHub cannot distinguish a Codex
session from a human, Cowork session, or another Git client. Therefore:

- GitHub protection enforces the shared repository baseline for every client.
- Codex-only behavior belongs in local Codex skills, hooks, and preflight
  checks, not in a claim that GitHub protection is session-specific.
- A local Codex workflow must still refuse direct implementation on `dev` and
  require a feature branch for code changes.

## `dev` baseline

The `dev` branch uses the following baseline:

| Setting | Value | Reason |
| --- | --- | --- |
| Pull request required | Yes | Keeps integration changes reviewable and traceable. |
| Required approvals | 0 | Single-maintainer workflow; CI and evidence remain the gate. |
| Required status checks | None yet | No CI workflow exists to name as a stable check. |
| Force pushes | Disabled | Preserves branch history and review references. |
| Branch deletion | Disabled | Keeps the integration target stable. |
| Admin enforcement | Enabled | Avoids silently bypassing the baseline. |
| Conversation resolution | Enabled | Requires PR discussions to be resolved. |

The implementation sequence is recorded in the
[CI baseline plan](../plans/PLAN-ci-baseline.md). Required checks must be named
explicitly and tested on a feature-to-`dev` pull request before becoming
mandatory.

## Codex session checklist

1. Read the current branch, worktree, status, and remote.
2. Use `feature/*` for code or skill implementation.
3. Run the skill validator and full offline test suite.
4. Open a pull request targeting `dev`.
5. Treat default-branch, protection, release, and publication changes as
   separate approval gates.

This document describes repository policy; it does not install Claude hooks or
modify `codex-config`.
