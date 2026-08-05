# CI baseline plan

> **Status:** Planning only; no workflow changes are included here
>
> **Branch:** `feature/ci-planning`
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
| 1 | Add the minimal CI workflow | P0 | 20–30 min | Pending |
| 2 | Run a feature-to-`dev` PR and inspect the check name | P0 | 10–15 min | Pending |
| 3 | Require the stable check on `dev` | P0 | 5 min | Pending approval |

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

- [ ] A pull request targeting `dev` runs the workflow automatically.
- [ ] The full offline suite passes in CI.
- [ ] Every current skill passes validation in CI.
- [ ] Whitespace or contract failures produce a failing check.
- [ ] The workflow requests read-only repository contents permission.
- [ ] No secrets or external service credentials are needed.
- [ ] The observed check name is required on `dev` only after one successful
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
