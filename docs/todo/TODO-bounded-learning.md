# Bounded learning TODO

**Spec:**
[SPEC-bounded-learning-2026-08-04.md](../specs/SPEC-bounded-learning-2026-08-04.md)

**Plan:**
[PLAN-bounded-learning.md](../plans/PLAN-bounded-learning.md)

**Status:** Phase 4 pilot and adversarial hardening complete; committed locally

**Remediation plan:**
[PLAN-adversarial-remediation-2026-08-05.md](../plans/PLAN-adversarial-remediation-2026-08-05.md)

## P0 — Pre-commit remediation

- [x] Reject date-only and timezone-less candidate timestamps.
  - Finding: validator accepts values that do not satisfy the documented
    `date-time` contract.
  - Depends on: candidate contract review.
  - Estimate: small.
- [x] Verify candidate evidence references exist, are readable, and remain
  within allowed roots.
  - Finding: nonexistent evidence references currently pass validation.
  - Depends on: evidence-root policy.
  - Estimate: medium.
- [x] Make supersession and cleanup transaction-safe.
  - Finding: a partial write can leave contradictory approved state.
  - Depends on: explicit lifecycle transition design.
  - Estimate: medium.
- [x] Add regression tests for all three findings and promotion failure paths.
  - Depends on: validator and promotion changes.
  - Estimate: medium.
- [x] Reconcile architecture, specification, TODO, plan, and status language.
  - Depends on: remediation behavior being settled.
  - Estimate: small.

## P0 — MVP blockers

- [x] Add `openai/portable/learning/contracts/candidate-lesson.schema.json`.
  - Depends on: finalized fields in the spec.
  - Estimate: small.
- [x] Implement deterministic candidate validation.
  - Check schema, lifecycle transitions, scope, size, and redaction status.
  - Depends on: schema.
  - Estimate: medium.
- [x] Add redaction and rejection fixtures.
  - Include secrets, transcript overflow, hidden reasoning, and prompt injection.
  - Depends on: validator.
  - Estimate: small.
- [x] Add lesson regression fixtures.
  - Include positive, negative, unavailable-backend, and rollback cases.
  - Depends on: validator and existing verification fixtures.
  - Estimate: medium.
- [x] Add contract tests for validation and lifecycle transitions.
  - Depends on: schema and fixtures.
  - Estimate: small.
- [x] Define the human promotion workflow in
  `openai/portable/learning/policies/promotion.md`.
  - Depends on: contract tests.
  - Estimate: small.
- [x] Create the explicitly invoked `savant-learning-review` skill.
  - It must review candidates; it must not self-promote or edit instructions.
  - Depends on: promotion policy.
  - Estimate: medium.
- [x] Dogfood one narrowly scoped approved lesson.
  - Measure token overhead, verdict preservation, and regression behavior.
  - Depends on: all prior P0 items.
  - Estimate: medium.

## Deferred — not part of this implementation plan

The following remain recorded in [ADR-0002](../adr/ADR-0002-bounded-learning-boundary.md)
but are not active TODO items:

- Codex `Stop` or `SessionEnd` hooks.
- A separate `savant-codex` adapter package.
- External evaluation integration.
- Broader deduplication, expiry, and package-drift automation.

## Explicitly rejected

- [x] Automatic edits to `SKILL.md`, `AGENTS.md`, contracts, or policies.
- [x] Automatic promotion from model output or hook output.
- [x] Raw transcript learning.
- [x] Whole Claude-plugin port.

## Definition of done

The MVP is done when every P0 item is complete, all acceptance criteria in the
spec pass, one lesson has been dogfooded, and the normal verification path has
no learning-context overhead. This gate is complete for the current pilot;
broader lessons require additional measurements.

**Current pilot effort:** Complete for the bounded-learning MVP, remediation
pass, and the 2026-08-06 runtime Codex evaluation (6/6 verdicts preserved).
Package materialization and drift checks remain separate future work.
