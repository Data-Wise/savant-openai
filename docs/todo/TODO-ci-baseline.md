# CI baseline TODO

**Plan:** [PLAN-ci-baseline.md](../plans/PLAN-ci-baseline.md)

**Status:** Planning complete; workflow implementation not started

## P0 — CI baseline

- [ ] Add `.github/workflows/ci.yml` for pull requests into `dev` and pushes
      to `dev`.
- [ ] Run the full standard-library test suite.
- [ ] Validate every `skills/*/SKILL.md` with the Codex skill validator.
- [ ] Run `git diff --check`.
- [ ] Confirm read-only workflow permissions and no secret dependencies.
- [ ] Dogfood on a feature-to-`dev` pull request.
- [ ] Record the observed stable job name.
- [ ] Require the stable job on `dev` in a separate approval-gated change.

## Deferred

- Runtime Codex evaluation.
- Deterministic CAS/statistics adapters.
- Package publication and marketplace installation.
- Release-branch protection.

## Definition of done

The CI baseline is complete when a feature-to-`dev` pull request runs the
offline tests and all skill validators, fails on contract or formatting errors,
uses read-only permissions, and has its verified job name required by `dev`.
