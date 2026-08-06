# Runtime Codex evaluation measurement

**Date:** 2026-08-06
**Surface:** Actual Codex session (`codex exec`, read-only sandbox, ephemeral)
**Model:** `gpt-5.6-luna` (default), reasoning effort `high`
**Skill:** `savant-research-verify` (namespace `savant-openai:savant-research-verify`)
**Lesson:** `lesson-proof-001`

## Result

| Fixture | Expected | Baseline | Lesson-assisted | Match |
| --- | --- | --- | --- | ---: |
| `correct-proof-step` | `VERIFIED` | `VERIFIED` | `VERIFIED` | 2/2 |
| `planted-proof-error` | `FAILED` | `FAILED` | `FAILED` | 2/2 |
| `backend-unavailable` | `UNVERIFIED` | `UNVERIFIED` | `UNVERIFIED` | 2/2 |

All six runtime runs produced the expected terminal verdict. The lesson
preserved every baseline verdict: no `UNVERIFIED` became `VERIFIED` and no
`FAILED` became `VERIFIED`. The skill loaded in the session, read the
verification-status contract, ran a deterministic check where one was
available (SymPy simplification for the positive fixture), and reported the
structured verdict block.

The approved lesson (`lesson-proof-001`) targets denominator cancellation.
None of the three fixtures involve cancellation, so the model correctly judged
it out of scope and did not alter behavior.

## Evidence paths (schema 1.2)

Each run records an `evidence_path`:
`symbolic-cas`, `deterministic-script`, `numerical-examples`, or
`model-reasoning`. The positive baseline run verified through SymPy
(`symbolic-cas`); the positive lesson-assisted run used structural reasoning
plus numerical smoke checks (`numerical-examples`), which the verification
contract does not allow to justify `VERIFIED`. That run is therefore flagged in
`evidence_flags` and surfaced by `scripts/learning/measure-lesson.py
--check-runtime`, which cross-checks that no sub-CAS `VERIFIED` is left
unflagged. The negative runs found their counterexamples numerically
(`numerical-examples`) and the unavailable-backend runs applied the stop
condition without a backend (`model-reasoning`); none of those justify
`VERIFIED`, so none are flagged.

## Token overhead

Lesson size: 652 bytes → 163 estimated tokens (the deterministic
`ceil(UTF-8 bytes / 4)` heuristic).

Actual `turn.completed` usage per run (model tokens, not heuristic):

| Run | Condition | input | cached | output | reasoning |
| --- | --- | ---: | ---: | ---: | ---: |
| `correct-proof-step` | baseline | 283,673 | 252,416 | 3,723 | 2,027 |
| `correct-proof-step` | lesson | 287,697 | 250,624 | 6,186 | 3,641 |
| `planted-proof-error` | baseline | 159,381 | 150,016 | 3,042 | 1,851 |
| `planted-proof-error` | lesson | 356,309 | 312,832 | 6,297 | 3,594 |
| `backend-unavailable` | baseline | 269,299 | 227,328 | 4,316 | 1,708 |
| `backend-unavailable` | lesson | 175,119 | 145,920 | 4,181 | 2,096 |

Input counts are dominated by the installed session skill and plugin catalog,
and the lesson-vs-baseline input deltas are non-monotonic (the lesson run is
sometimes lower), reflecting cache variance rather than lesson content. The
lesson's marginal context is therefore best measured by the deterministic
163-token heuristic, not by per-run input deltas. Output tokens include
reasoning tokens at the configured high reasoning effort.

## Limitations

- Single model, single reasoning effort, three fixtures; not a general
  model-accuracy benchmark.
- The session ran from the repository root with the skill loaded through a
  local `~/.codex/skills` symlink; no marketplace or publication path was used.
- The positive fixture passed a symbolic check available in the session; the
  committed deterministic script
  (`scripts/verify/symbolic-check.py`, SymPy 1.14.0) now reproduces that check
  in CI and is the repository-owned backend for future proof-mode verification.
- In the lesson-assisted positive run, the `VERIFIED` verdict was justified by
  structural reasoning plus numerical smoke checks rather than the symbolic
  CAS check used in the baseline run. The verdict matched, but the evidence
  path was weaker; it is recorded as `evidence_path: numerical-examples` and
  flagged in `evidence_flags` under schema 1.2.
- Raw session transcripts are not archived wholesale; the six verdict excerpts
  are archived sanitized under
  [`docs/measurements/logs/runtime-codex-2026-08-06/`](logs/runtime-codex-2026-08-06/)
  per the [transcript archival policy](../architecture/TRANSCRIPT-ARCHIVAL-POLICY.md).
  Unlike the deterministic dogfood measurement, reproduction requires re-running
  `codex exec`, and model behavior is non-deterministic.
- Broader multi-lesson evaluation and package materialization remain separate
  work.

## Reproduction

```text
ln -s <repo>/skills/savant-research-verify ~/.codex/skills/savant-research-verify
cd <repo>
codex exec --json -s read-only --ephemeral \
  "Using the savant-research-verify skill, verify the research claim in tests/fixtures/<fixture>.json. ..."
```
