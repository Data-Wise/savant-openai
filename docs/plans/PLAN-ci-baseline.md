# CI baseline plan

> **Status:** Complete
>
> **Branch:** `feature/ci-baseline`
>
> **Base:** `dev`
>
> **Target:** Pull requests into `dev`

## Objective

Add one small, deterministic GitHub Actions workflow that validates the
Codex/OpenAI plugin before a pull request can merge. The workflow must use no
secrets or external services and must produce one stable required check for the
protected `dev` branch.

## Scope

### In scope

- GitHub Actions workflow under `.github/workflows/`.
- Standard-library test suite.
- Codex plugin manifest and skill validation.
- Markdown whitespace validation with `git diff --check`.
- Pull-request dogfood and branch-protection update after the check name is
  confirmed stable.

### Out of scope

- CAS, R, or external statistical backends.
- Runtime Codex evaluation.
- Package publication or marketplace installation.
- Required checks on a future release branch.
- Secrets, deployment credentials, or network-dependent tests.

## Phase overview

| Phase | Increment | Priority | Effort | Status |
| --- | --- | --- | --- | --- |
| 0 | Planning and acceptance criteria | P0 | 10 min | Complete |
| 1 | Add the minimal CI workflow | P0 | 20–30 min | Complete |
| 2 | Run a feature-to-`dev` PR and inspect the check name | P0 | 10–15 min | Complete |
| 3 | Require the stable check on `dev` | P0 | 5 min | Complete |

**Total estimate:** 45–60 minutes, assuming the current offline suite remains
dependency-free.

## Workflow contract

The workflow should:

1. Run on pull requests targeting `dev` and on pushes to `dev`.
2. Use a pinned supported Python version and no secret-bearing steps.
3. Run `python3 -m unittest discover -s tests -p 'test_*.py'`.
4. Validate each skill directory with the Codex skill validator.
5. Run `git diff --check` against the checked-out change.
6. Expose one stable job name, proposed as `test`, before making it required.

The exact Python action version and job identifiers must be recorded in the
workflow and verified from a real pull request before protection is changed.

## Acceptance criteria

- [x] A pull request targeting `dev` runs the workflow automatically.
- [x] The full offline suite passes in CI.
- [x] Every current skill passes validation in CI.
- [x] Whitespace or contract failures produce a failing check because the
      workflow runs both commands as required job steps and propagates their
      nonzero exit status.
- [x] The workflow requests read-only repository contents permission.
- [x] No secrets or external service credentials are needed.
- [x] The observed check name is required on `dev` after one successful
      feature-to-`dev` dogfood run.

## Risks and mitigations

| Risk | Mitigation |
| --- | --- |
| Check name drift makes protection ineffective | Confirm the exact job name from a real PR before requiring it. |
| Future skills are omitted | Discover skill directories rather than naming only today’s skills. |
| CI becomes network-dependent | Keep the baseline limited to local tests and validators. |
| Admin bypass hides failures | Keep admin enforcement enabled and avoid bypass merges. |

## Verification and handoff

Before applying protection changes:

1. Open a feature-to-`dev` pull request.
2. Confirm the workflow is green and the job name is stable.
3. Confirm the workflow has no secrets or unexpected write permissions.
4. Update [REPOSITORY-WORKFLOW.md](../architecture/REPOSITORY-WORKFLOW.md)
   with the required check name.
5. Apply the required-check change as a separate approval-gated operation.

## Dogfood evidence

PR [#4](https://github.com/Data-Wise/savant-openai/pull/4) ran the workflow
successfully on 2026-08-05.

- Run: [CI run 31024116693](https://github.com/Data-Wise/savant-openai/actions/runs/31024116693)
- Job: `test` (stable observed name)
- Result: success in 9 seconds
- Checks: 28 standard-library tests, 3 Codex skills, and pull-request
  whitespace validation
- Permissions: `contents: read`; no secrets or external services

## Completion evidence

The verified `test` check is now required on protected `dev` with strict
updates enabled. PR #4 merged as `1508d4c`, and the resulting push to `dev`
passed the same `test` job in [CI run 31024636086](https://github.com/Data-Wise/savant-openai/actions/runs/31024636086).

The CI baseline is complete. Runtime Codex evaluation and release/publication
work remain outside this plan.
