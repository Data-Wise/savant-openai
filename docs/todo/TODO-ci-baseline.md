# CI baseline TODO

**Plan:** [PLAN-ci-baseline.md](../plans/PLAN-ci-baseline.md)

**Status:** Complete

## P0 — CI baseline

- [x] Add `.github/workflows/ci.yml` for pull requests into `dev` and pushes
      to `dev`.
- [x] Add a repository-local, standard-library skill validator.
- [x] Use read-only workflow permissions and no secret dependencies.
- [x] Run the full standard-library test suite in CI (28 tests passed).
- [x] Validate every `skills/*/SKILL.md` with the Codex skill validator (3
      skills passed).
- [x] Run `git diff --check` for the pull request.
- [x] Confirm read-only workflow permissions and no secret dependencies.
- [x] Dogfood on a feature-to-`dev` pull request ([PR #4](https://github.com/Data-Wise/savant-openai/pull/4)).
- [x] Record the observed stable job name: `test`.
- [x] Require the stable job on `dev` in a separate approval-gated change.

## Deferred

- Runtime Codex evaluation.
- Deterministic CAS/statistics adapters.
- Package publication and marketplace installation.
- Release-branch protection.

## Definition of done

The CI baseline is complete: a feature-to-`dev` pull request runs the offline
tests and all skill validators, fails on contract or formatting errors, uses
read-only permissions, and has its verified `test` job required by `dev`.
