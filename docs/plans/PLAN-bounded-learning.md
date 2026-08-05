# Bounded learning implementation plan

> **Spec:** [SPEC-bounded-learning-2026-08-04.md](../specs/SPEC-bounded-learning-2026-08-04.md)
>
> **ADR:** [ADR-0002](../adr/ADR-0002-bounded-learning-boundary.md)
>
> **Branch:** `feature/bootstrap-savant-openai`

## Objective

Implement the smallest useful learning loop for Savant: structured candidate
lessons, deterministic safety checks, human promotion, and regression evidence.
Do not add hooks or autonomous source-file mutation during the MVP.

## Phase overview

| Phase | Increment | Priority | Effort | Status |
| --- | --- | --- | --- | --- |
| 0 | Spec, ADR, TODO, and architecture alignment | P0 | Small | Complete |
| 1 | Candidate contract and validator | P0 | Medium | Complete |
| 2 | Security and regression fixtures | P0 | Medium | Complete |
| 3 | Review/promotion workflow and skill | P0 | Medium | Complete |
| 4 | Dogfood, measure, and document | P0 | Medium | Complete — pilot only |

## Phase 1 — Candidate contract and validator

**Goal:** Make unsafe or malformed candidates impossible to promote.

- [x] Define the JSON schema and lifecycle states.
- [x] Define hard byte/token limits.
- [x] Implement schema and semantic validation.
- [x] Implement candidate redaction checks.
- [x] Add validator command documentation.

**Key files:**

- `openai/portable/learning/contracts/candidate-lesson.schema.json` (new)
- `scripts/learning/validate-candidate.py` (new)
- `tests/test_candidate_validation.py` (new)

**Exit gate:** passed. Valid candidates pass; malformed, oversized,
secret-bearing, and unscoped candidates fail with actionable messages.

## Phase 2 — Security and regression fixtures

**Goal:** Prove that learning cannot weaken verification or persist unsafe data.

- [x] Add positive lesson fixture.
- [x] Add negative overgeneralization fixture.
- [x] Add unavailable-backend fixture.
- [x] Add prompt-injection fixture.
- [x] Add secret-redaction fixture.
- [x] Add rollback/supersession fixture.
- [x] Run all existing verification fixtures unchanged.

**Key files:**

- `tests/learning/fixtures/` (new)
- `tests/fixtures/` (existing fixtures remain unchanged unless coverage requires
  a documented addition)

**Exit gate:** passed. No fixture permits an unsupported upgrade to
`VERIFIED`, and unsafe candidate content is rejected.

## Phase 3 — Human review and promotion

**Goal:** Provide a low-context, explicit review workflow.

- [x] Write the promotion policy.
- [x] Add candidate review and approval states.
- [x] Add versioned approved-lesson storage.
- [x] Add the `savant-learning-review` skill.
- [x] Add rollback instructions.

**Key files:**

- `openai/portable/learning/policies/promotion.md` (new)
- `openai/portable/learning/approved/` (new)
- `skills/savant-learning-review/SKILL.md` (new)
- `tests/learning/test_promotion.py` (new)

**Exit gate:** passed. A reviewer can approve, reject, supersede, and revert a
lesson through explicit commands without editing generated state manually.

## Phase 4 — Dogfood and measurement

**Goal:** Demonstrate value without increasing normal verification cost.

- [x] Select one lesson from an existing failure or explicit correction.
- [x] Run baseline verification without the lesson.
- [x] Run scoped review with the lesson.
- [x] Compare verdict, evidence, token estimate, and failure modes.
- [x] Record the result in the status and implementation documentation.

**Exit gate:** passed for one fixture-backed lesson. The lesson preserved the
scoped `FAILED` verdict, added context only to the explicit review path, and
did not increase false `VERIFIED` results.

## Deferred work

Codex hook capture, external evaluation integration, broader lesson lifecycle
automation, and a separate `savant-codex` package are deliberately outside this
plan. They remain governed by ADR-0002 and require a new approval gate.

## Follow-up hardening

The adversarial review found three pre-commit integrity gaps in the pilot:
timestamp enforcement, evidence-reference validation, and transaction-safe
promotion. They are tracked in the focused
[adversarial remediation plan](PLAN-adversarial-remediation-2026-08-05.md).
The Phase 4 result is therefore pilot evidence, not a claim that runtime Codex
evaluation or all evidence contracts are complete.

## Friction prevention

- Verify CWD and branch before each Git operation.
- Keep implementation on a feature branch.
- Keep candidate data separate from approved portable knowledge.
- Run the smallest relevant tests after each phase.
- Stop at an exit gate that fails; do not guess around missing evidence.
- Do not install, publish, commit, or push without separate approval.

## Acceptance criteria

- [x] All P0 TODO items are complete.
- [x] All spec acceptance criteria pass.
- [x] Existing verification fixtures remain green.
- [x] One approved lesson is dogfooded and measured.
- [x] Normal verification loads no learning context.
- [x] No automatic hook or source-file self-editing exists in MVP.

## Commit strategy

Use conventional commits by phase:

1. `feat: add bounded learning candidate contract`
2. `test: add learning safety and regression fixtures`
3. `feat: add reviewed lesson promotion workflow`
4. `docs: record bounded learning dogfood results`

Do not commit these planning artifacts separately from the current approved
documentation change unless the repository workflow requires it.

## Verification

The Phase 1 command is documented in `tests/README.md` and runs without
network access. Phases 2 and 3 use the same command with the standalone
security, regression, and promotion matrix. Skill structure is checked with
the Codex skill validator.

## Next action

Next: review the completed adversarial remediation plan and test evidence.
Commit, push, publish, and install remain separate approval-gated actions. Do
not begin hook work without a new ADR or explicit scope approval.
