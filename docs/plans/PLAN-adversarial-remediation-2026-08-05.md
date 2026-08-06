# Savant OpenAI — Adversarial Remediation Plan

> **Status:** Implemented and committed locally; push review required
> **Source:** Read-only adversarial review of the Phase 4 pilot  
> **Branch:** `feature/bootstrap-savant-openai`  
> **Related plan:** [PLAN-bounded-learning.md](PLAN-bounded-learning.md)  
> **Date:** 2026-08-05

## Objective

Harden the bounded-learning pilot before its first commit. Close the evidence,
lifecycle, and contract-validation gaps found during review, reconcile the
planning documentation, and preserve the core boundary: learning remains
opt-in, human-reviewed, versioned, and absent from normal verification.

This plan does **not** add hooks, automatic promotion, or runtime self-editing.
Full Codex evaluation was completed separately on 2026-08-06.

## Priority summary

| Priority | Work | Why it matters | Effort | Status |
| --- | --- | --- | --- | --- |
| P0 | Strict timestamp validation | Prevent schema-invalid lessons from passing validation | Small | Complete |
| P0 | Evidence-reference validation | Prevent unsupported lessons from being promoted | Medium | Complete |
| P0 | Transaction-safe promotion | Prevent contradictory approved/superseded state | Medium | Complete |
| P1 | Contract and failure-path tests | Make the fixes regression-proof | Medium | Complete |
| P1 | Documentation reconciliation | Remove false completion and layout claims | Small | Complete |
| P2 | Runtime Codex evaluation | Measure actual model behavior and token cost | Large | Complete |

## Phase 1 — Validator integrity

**Goal:** Make candidate validation enforce the contract it already documents.

- [x] Require `created_at` and `reviewed_at` to be complete timezone-aware
  date-time values; reject date-only and timezone-less values.
- [x] Resolve every file-backed `evidence.ref` against an allowed repository or fixture
  root before reporting `VALID`.
- [x] Reject missing, unreadable, or path-escaping evidence references.
- [x] Emit actionable errors that identify the field and failed check.
- [x] Keep validation deterministic and network-free.

**Key files:**

- `scripts/learning/validate-candidate.py`
- `openai/portable/learning/contracts/candidate-lesson.schema.json`
- `tests/test_candidate_validation.py`

**Exit gate:** Invalid timestamps and nonexistent or unsafe evidence references
fail validation; valid fixture-backed candidates continue to pass.

## Phase 2 — Promotion lifecycle safety

**Goal:** Ensure supersession cannot leave contradictory state.

- [x] Define the expected state transition for approve, supersede, and revert.
- [x] Stage the new state before replacing the old state, or implement an
  explicit rollback path for every partial failure.
- [x] Detect duplicate active approvals before writing new state.
- [x] Preserve a clear, recoverable state if a write or delete fails.
- [x] Keep revert behavior explicit and version-control recoverable.

**Key files:**

- `scripts/learning/promote-lesson.py`
- `openai/portable/learning/policies/promotion.md`
- `tests/learning/test_promotion.py`

**Exit gate:** Injected write and cleanup failures do not produce two active
  approved lessons or an unmarked superseded lesson.

## Phase 3 — Contract and regression coverage

**Goal:** Test the contracts that the implementation relies on, not only the
  happy path.

- [x] Add timestamp boundary cases.
- [x] Add nonexistent, unreadable, and path-escape evidence cases.
- [x] Add promotion failure-injection cases.
- [x] Validate at least one `evidence-report.schema.json` positive and negative
  fixture.
- [x] Add manifest and skill-frontmatter checks to the repository test command
  or document the separate validator command precisely.
- [x] Review the hand-rolled schema validator against every schema construct
  currently used; add coverage or narrow the supported contract explicitly.

**Key files:**

- `tests/`
- `openai/portable/contracts/evidence-report.schema.json`
- `.codex-plugin/plugin.json`
- `skills/*/SKILL.md`

**Exit gate:** The full offline test suite passes and directly covers each P0
  review finding.

## Phase 4 — Documentation and evidence reconciliation

**Goal:** Make project status accurately distinguish implemented pilot evidence
from unstarted runtime evaluation.

- [x] Change architecture and plan language from “proposed” or “Phase 4 gated”
  to “pilot and pre-commit hardening implemented; runtime evaluation deferred,”
  where appropriate.
- [x] Correct the documented learning directory layout.
- [x] Remove the duplicate `.STATUS` item.
- [x] Label the current measurement as heuristic, fixture-backed,
  contract-level dogfood evidence rather than model-accuracy evidence.
- [x] Record the three P0 remediation exit gates and the remaining runtime
  evaluation gap.

**Key files:**

- `docs/architecture/SAVANT-OPENAI-PLAN.md`
- `docs/architecture/BOUNDED-LEARNING.md`
- `docs/adr/ADR-0002-bounded-learning-boundary.md`
- `docs/specs/SPEC-bounded-learning-2026-08-04.md`
- `docs/plans/PLAN-bounded-learning.md`
- `docs/todo/TODO-bounded-learning.md`
- `.STATUS`

**Exit gate:** No planning artifact claims runtime evaluation or fully verified
evidence that has not occurred.

## Phase 5 — Runtime Codex evaluation

This was intentionally **not part of the pre-commit hardening pass**; it was
completed on 2026-08-06.

- [x] Run the skill in an actual Codex session.
- [x] Compare baseline and lesson-assisted behavior on positive, negative, and
  unavailable-backend cases. All six runs produced the expected verdict.
- [x] Measure actual context/token overhead rather than byte heuristics alone.
  Actual per-run token usage is recorded in
  [MEASUREMENT-runtime-codex-2026-08-06.md](../measurements/MEASUREMENT-runtime-codex-2026-08-06.md).
- [x] Verify that lessons preserve `UNVERIFIED` and do not create false
  `VERIFIED` results. Verdicts were preserved in every run.
- [ ] Add package materialization and drift checks only after runtime evidence
  justifies them. This remains deferred pending a separate plan.

## Non-goals

- No Codex lifecycle hooks.
- No automatic candidate capture or promotion.
- No edits to `SKILL.md`, `AGENTS.md`, contracts, or policies from model output.
- No Claude Savant changes.
- No push, publication, or installation in this plan. A local commit requires
  the separate approval gate recorded in `.STATUS`.

## Acceptance criteria

- [x] All three P0 review findings are fixed and covered by tests.
- [x] A candidate with invalid timestamps fails validation.
- [x] A candidate with missing or unsafe evidence fails validation.
- [x] Promotion remains internally consistent under simulated partial failure.
- [x] Existing 18-test baseline remains green, with new tests added for the
  remediation cases.
- [x] Documentation distinguishes pilot evidence from runtime Codex evidence.
- [x] Normal verification still loads no learning context.

## Verification

Run from the repository root:

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 -m json.tool .codex-plugin/plugin.json >/dev/null
```

Also run the repository's skill/frontmatter validator once its command is
confirmed. Do not claim that check passed based only on the Python test suite.

## Commit strategy

Keep the remediation reviewable as small conventional commits, subject to the
separate commit approval gate:

1. `fix: enforce bounded-learning evidence contracts`
2. `test: cover promotion failure paths`
3. `docs: reconcile pilot status and remediation plan`

## Next approval gate

Review local commit `223d73c` and its test evidence. Push, publication, and
installation remain separately approval-gated.
