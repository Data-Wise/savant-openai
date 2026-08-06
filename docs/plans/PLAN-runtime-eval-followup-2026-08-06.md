# Savant OpenAI — Runtime Evaluation Follow-up Plan

> **Status:** Active — Phases 1–2 complete; Phases 3–5 proposed
> **Source:** Review of the 2026-08-06 runtime Codex evaluation
>   ([MEASUREMENT-runtime-codex-2026-08-06.md](../measurements/MEASUREMENT-runtime-codex-2026-08-06.md))
> **Branch:** `dev` (merged via PR #6 on 2026-08-06)
> **Date:** 2026-08-06

## Objective

Close the evidence gaps surfaced by the first runtime Codex evaluation:
verification-rigor consistency, transcript archival, lesson coverage, and a
committed deterministic backend. Keep every item evidence-first and
approval-gated.

## Priority summary

| Priority | Work | Why it matters | Effort | Status |
| --- | --- | --- | --- | --- |
| P0 | Evidence-path tracking in runtime measurements | Flag `VERIFIED` verdicts reached without a deterministic check | Small | Complete |
| P0 | Committed deterministic CAS check | Give proof mode a repo-owned backend instead of relying on session tooling | Medium | Complete |
| P1 | Raw transcript archival policy | Runtime evals are only re-runnable, not script-reproducible | Small | Proposed |
| P1 | In-scope lesson fixtures | Exercise a lesson that actually applies, not only out-of-scope cases | Medium | Proposed |
| P2 | Broader multi-lesson evaluation | Statistical confidence across lessons, fixtures, and repeated runs | Large | Proposed |
| P2 | Package materialization and drift checks | Still gated on a separate plan | Medium | Deferred |

## Phase 1 — Evidence-path tracking

**Goal:** Every runtime measurement records *how* each verdict was justified.

- Extend the measurement schema (currently `1.1`) with an `evidence_path`
  field per run: `symbolic-cas`, `deterministic-script`, `numerical-examples`,
  or `model-reasoning`.
- A `VERIFIED` verdict whose `evidence_path` is `numerical-examples` or
  `model-reasoning` must be flagged in the measurement output; the skill's own
  stop conditions forbid those paths from producing `VERIFIED`.

**Key files:**

- `openai/portable/contracts/runtime-measurement.schema.json` (schema 1.2)
- `docs/measurements/MEASUREMENT-runtime-codex-2026-08-06.json` (measured artifact)
- `scripts/learning/measure-lesson.py` (schema-aware output)

**Exit gate:** A measurement run where the evidence path is recorded per
fixture and any sub-CAS `VERIFIED` is flagged.

**Status:** Complete. Schema 1.2 (`openai/portable/contracts/runtime-measurement.schema.json`)
adds a per-run `evidence_path` enum and requires recorded `evidence_flags`.
`scripts/learning/measure-lesson.py --check-runtime` validates a measurement
document against the schema and cross-checks that every sub-CAS `VERIFIED` is
flagged. The 2026-08-06 runtime measurement was upgraded to 1.2; its
lesson-assisted positive run is the one recorded flag.

## Phase 2 — Deterministic CAS check

**Goal:** Commit a minimal, standard-library-plus-SymPy verification script so
proof mode has a deterministic backend owned by this repository.

- One script (for example `scripts/verify/symbolic-check.py`) that simplifies a
  stated residual and reports `PASS`/`FAIL`/`UNVERIFIED` with the backend name
  and version.
- Contract tests for the script's output shape against
  `openai/portable/contracts/verification-status.md`.

**Exit gate:** The positive fixture verifies through the committed script in
CI, not only through session tooling.

**Status:** Complete. `scripts/verify/symbolic-check.py` simplifies a stated
residual with SymPy and reports `PASS`/`FAIL`/`UNVERIFIED` with the backend
name and version; `--positive` declares a claim's positive symbols. Proof
fixtures carry a machine-readable `residual` (and `positive_symbols`), and
contract tests exercise the script through the committed fixtures in CI, which
now installs `sympy==1.14.0`.

## Phase 3 — Transcript archival policy

**Goal:** Decide how runtime evidence persists, since runtime evaluation is
non-deterministic and only re-runnable.

- Choose between: committing sanitized session logs under
  `docs/measurements/logs/`, or attaching them as CI artifacts, or recording
  only the summary measurement (current state).
- Record the decision and its privacy rationale; transcripts may contain
  environment-specific context.

**Exit gate:** A written policy and one archived or explicitly non-archived
measurement produced under it.

## Phase 4 — In-scope lesson fixtures

**Goal:** Exercise the lesson path where the lesson genuinely applies.

- Add a fixture in the lesson's actual failure class (a cancellation step that
  omits a nonzero-denominator assumption) so lesson-assisted runs can be
  observed changing reasoning, not just ignoring out-of-scope content.
- Re-run the baseline versus lesson-assisted matrix with that fixture.

**Exit gate:** A measurement showing the lesson's effect (or demonstrated
no-op with evidence) on an in-scope fixture.

## Phase 5 — Broader multi-lesson evaluation

**Goal:** Statistical confidence beyond one lesson and one run per condition.

- Multiple lessons, multiple fixtures per class, and repeated runs per
  condition so token overhead is measured as a distribution rather than single
  noisy points.
- Deferred until Phases 1–4 provide the tooling and fixtures.

**Exit gate:** A measurement report with per-condition repetition and
aggregated overhead.

## Non-goals

- No publication, marketplace installation, or `main` changes.
- No Codex lifecycle hooks or automatic lesson capture or promotion.
- No model-accuracy benchmarking; these are contract-compliance measurements.
- No edits to skills, contracts, or policies from model output.

## Verification

Each phase runs the full offline suite (`python3 -m pytest`) and
`python3 scripts/validate-skills.py`; runtime phases additionally record a
measurement artifact under `docs/measurements/` before the phase is marked
complete.
