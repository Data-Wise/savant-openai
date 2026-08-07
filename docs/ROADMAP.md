# savant-openai roadmap

**Last updated:** 2026-08-07
**Source of truth for state:** [`.STATUS`](../.STATUS)

This roadmap consolidates the forward-looking work across the pilot plan
([SAVANT-OPENAI-PLAN.md](architecture/SAVANT-OPENAI-PLAN.md)), the active
plans under [`docs/plans/`](plans/), and the state tracked in `.STATUS`.
Each item is approval-gated and evidence-first; nothing here is committed,
published, or installed without a separate approval gate.

## Done

Pilot implemented through the first release-adjacent milestones:

- Portable verification contracts, fixtures, and the `savant-research-verify`
  skill (proof / statistics / simulation / reproducibility modes).
- Bounded-learning design (ADR-0002) with candidate lessons, deterministic
  validation, human promotion, and regression fixtures.
- CI baseline (`dev` integration, read-only `test` job, skill validator,
  whitespace gate). Merged via PR #4.
- Runtime Codex evaluation (2026-08-06): 6/6 expected verdicts across the
  three fixture classes, baseline and lesson-assisted. Merged via PR #6.
- Runtime evaluation follow-up Phases 1–4: evidence-path measurement schema
  (1.2), committed deterministic SymPy CAS check, transcript archival policy,
  and in-scope lesson fixtures. Merged via PR #7.
- Standalone `savant-teach-mathematical-proofs` teaching skill. Merged via
  PR #8.

## Next approval gate

The immediate next proposed work is the runtime evaluation follow-up
**Phase 5 — broader multi-lesson evaluation** (statistical confidence across
multiple lessons, fixtures, and repeated runs per condition). It opens as new
work under a separate plan when approved.

## Planned

| Priority | Work | Why it matters | Gate |
| --- | --- | --- | --- |
| P0 | Phase 5: broader multi-lesson evaluation | Token overhead as a distribution, not single noisy points | Separate plan + approval |
| P1 | Deterministic statistics scripts | Committed statistical backend beyond the proof-mode CAS check | Follows proof-mode pattern |
| P1 | Codex package materialization and drift checks | Validate that contract fixtures prevent adapter drift before publishing | Separate plan (deferred) |
| P1 | Release / publication plan | Marketplace or publication install | Separate plan (deferred) |
| P2 | Codex-only extension reassessment | Whether Codex-only hooks or local enforcement are justified | After packaging evidence |

## Guiding constraints

- **Evidence-first:** never report a proof or statistical claim as globally
  verified without recorded evidence; `UNVERIFIED` is the safe default.
- **Boundary discipline:** this repository owns the portable contracts and the
  OpenAI plugin; it does not modify the Claude Savant repository, `codex-config`,
  or model settings.
- **Approval-gated:** commit, push, publish, and install each require explicit
  approval; publication to `dev` goes through a pull request.
- **No self-editing:** learning candidates are untrusted proposals; nothing in
  this roadmap edits skills, instructions, contracts, or policies automatically.

## Related documents

- [Pilot plan](architecture/SAVANT-OPENAI-PLAN.md)
- [Repository workflow and protection](architecture/REPOSITORY-WORKFLOW.md)
- [Runtime evaluation follow-up plan](plans/PLAN-runtime-eval-followup-2026-08-06.md)
- [CI baseline plan](plans/PLAN-ci-baseline.md)
- [Bounded-learning specification](specs/SPEC-bounded-learning-2026-08-04.md)
- [Status file](../.STATUS)
