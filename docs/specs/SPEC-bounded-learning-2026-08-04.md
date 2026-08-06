# Bounded learning for Savant OpenAI

**Status:** Pilot implemented; pre-commit hardening complete; runtime Codex evaluation complete
**Date:** 2026-08-04
**Owner:** `savant-openai`
**Related ADR:** [ADR-0002](../adr/ADR-0002-bounded-learning-boundary.md)

## 1. Objective

Enable Savant to retain narrowly scoped, evidence-linked lessons from verified
failures and explicit user corrections without allowing autonomous changes to
skills, instructions, contracts, policies, or model weights.

The feature improves the surrounding workflow. It does not claim that the
model has learned a mathematical or statistical fact merely because it
generated a reflection.

## 2. Problem

Repeated corrections currently remain local to a task. A future workflow may
benefit from the correction, but only if the lesson can be captured, reviewed,
tested, scoped, and rolled back without increasing context cost or weakening
the evidence standard.

## 3. Scope

### Included in the first implementation

- A versioned candidate-lesson contract.
- Deterministic schema, size, timestamp, evidence-reference, scope, and
  redaction validation.
- Positive, negative, unavailable-backend, injection, and rollback fixtures.
- A human-reviewed promotion workflow.
- A separate, explicitly invoked learning-review skill.
- Measurement of token cost and verification-verdict impact.

### Not included

- Automatic editing of `SKILL.md`, `AGENTS.md`, contracts, or policies.
- Automatic promotion from a hook or model output.
- Raw transcript or hidden-reasoning storage.
- Model fine-tuning or weight updates.
- Automatic changes to the Claude Savant repository.
- A separate `savant-codex` package.

## 4. Actors and trust boundaries

- **Verification skill:** Produces scoped evidence and a terminal verdict.
- **Candidate generator:** Proposes a minimal lesson from evidence or explicit
  correction.
- **Validator:** Rejects malformed, oversized, secret-bearing, or out-of-scope
  candidates.
- **Human reviewer:** Accepts, edits, or rejects a candidate.
- **Portable lesson store:** Holds only approved, versioned lessons.
- **`codex-config`:** Owns Codex host settings, memory controls, and hooks.

Candidate content is untrusted input until validation and human review finish.

## 5. Candidate-lesson contract

The `candidate-lesson.schema.json` requires:

- `schema_version`: supported contract version;
- `id`: stable candidate identifier;
- `task_class`: one of `proof`, `statistics`, `simulation`, or
  `reproducibility`;
- `observed_failure`: concise description of the observed problem;
- `desired_behavior`: concise replacement behavior;
- `scope`: repository, skill, mode, or task boundary;
- `evidence`: fixture, command result, user correction, or source reference;
- `confidence`: `low`, `medium`, or `high`;
- `provenance`: source type and content hash where available;
- `redaction_status`: `pending`, `passed`, or `failed`;
- `lifecycle_status`: `candidate`, `approved`, `rejected`, or `superseded`;
- `created_at`; and
- `reviewed_at` when the status is not `candidate`; all date-time values must
  include an explicit timezone.

The contract must reject raw credentials, likely secrets, hidden reasoning,
unbounded transcript text, and claims without evidence.

## 6. Functional requirements

### FR-1: Explicit capture

The system must capture a lesson only from a verification failure,
independent check, or explicit user correction. Self-confidence alone is not a
capture signal.

### FR-2: Bounded size

Candidate lessons should target 300–600 tokens and have a hard size limit
defined by the schema validator.

### FR-3: Scoped retrieval

Normal verification must not load the learning store. An explicitly invoked
learning-review workflow may load only lessons matching the current task
class and scope.

### FR-4: Human promotion

No candidate may become approved without human review and a versioned change
on a feature branch.

### FR-5: Regression protection

Promotion must run the existing verification fixtures plus lesson-specific
positive, negative, unavailable-backend, injection, and rollback cases.

### FR-6: Verdict preservation

A lesson must not upgrade `UNVERIFIED`, `FAILED`, or
`PARTIALLY_VERIFIED` without new evidence satisfying the verification
contract.

### FR-7: Reversibility

Every approved lesson must be removable through a normal version-control
revert without editing generated state by hand.

### FR-8: Hook isolation

Hooks are not part of the MVP. If later introduced, they may create a private
candidate draft only; they must not promote lessons or modify source
instructions.

## 7. Token and context budget

- Existing verification path: no additional learning context.
- Learning-review path: one relevant reference at a time.
- Approved lessons per task: at most three.
- Candidate target: 300–600 tokens.
- Full transcripts: never loaded as learning context.
- Stale or redundant lessons: removed or marked superseded after evaluation.

## 8. Security and privacy requirements

- Treat all candidate fields as untrusted data.
- Run secret and credential redaction before persistence.
- Do not store raw transcripts, hidden reasoning, credentials, or unrelated
  personal data.
- Keep private candidate state outside distributable plugin artifacts.
- Record provenance and hashes without retaining sensitive source content.
- Require hook trust review if a future hook is enabled.

## 9. Acceptance criteria

- [x] A candidate validates against a versioned schema.
- [x] File-backed evidence references are present, readable, and confined to
  the repository; user-correction references use an explicit identifier form.
- [x] Invalid, oversized, secret-bearing, and unscoped candidates are rejected.
- [x] A human can approve, edit, reject, and supersede a candidate.
- [x] Approved lessons are versioned and reversible.
- [x] Existing verification fixtures remain green.
- [x] Positive and negative lesson fixtures detect overgeneralization.
- [x] Unavailable-backend fixtures preserve `UNVERIFIED`.
- [x] Injection and redaction fixtures prevent unsafe persistence.
- [x] The normal verification path loads no learning context.
- [x] Token cost and verdict changes are recorded for one dogfood lesson.
- [x] Evidence-report nesting, plugin manifest, and skill frontmatter have
  contract coverage.
- [x] No hook or automatic source-file mutation is required for MVP completion.

## 10. Open decisions before implementation

1. Choose the private candidate-state path owned by the OpenAI adapter.
2. Choose the first deterministic redaction implementation.
3. Define the exact hard byte/token limits in the schema validator.
4. Select the first dogfood lesson from an existing verification fixture.

These decisions must be recorded in the implementation plan or a follow-up
ADR before the relevant phase begins.
