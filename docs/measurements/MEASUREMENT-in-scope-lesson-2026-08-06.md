# In-scope lesson runtime evaluation measurement

**Date:** 2026-08-06
**Surface:** Actual Codex session (`codex exec`, read-only sandbox, ephemeral)
**Model:** `gpt-5.6-luna` (default), reasoning effort `high`
**Skill:** `savant-research-verify` (namespace `savant-openai:savant-research-verify`)
**Lesson:** `lesson-proof-001`
**Fixture:** `tests/fixtures/cancellation-without-assumption.json`

## Purpose

The 2026-08-06 runtime evaluation only exercised out-of-scope fixtures (none
involve cancellation), so the model could not apply `lesson-proof-001`. This
measurement re-runs the baseline-versus-lesson matrix on a fixture in the
lesson's actual failure class: a claim that cancels `(x - 1)` without stating
`x != 1`.

```text
claim: For all real x, (x^2 - 1)/(x - 1) = x + 1.
expected verdict: FAILED   (at x = 1 the left side is 0/0, undefined)
```

The fixture deliberately carries no `residual` field: the SymPy residual of
`(x^2 - 1)/(x - 1) - (x + 1)` simplifies to `0` (PASS), which would falsely
verify the universal claim. The defect is a missing domain assumption, which
residual simplification cannot detect.

## Result

| Condition | Verdict | Match |
| --- | ---: | ---: |
| baseline | `FAILED` | yes |
| lesson-assisted | `FAILED` | yes |

Both runs produced the expected `FAILED` verdict; the lesson preserved the
baseline verdict (no false `VERIFIED`).

## Lesson effect

The lesson-assisted run demonstrated an in-scope effect. It read the approved
lesson, ran `validate-candidate.py` on it (`VALID`), and stated in its report:

> ASSUMPTIONS: No `x != 1` denominator assumption stated. Approved
> `lesson-proof-001` matches and was applied.

and recommended:

> NEXT ACTION: State `x != 1`, then re-run verification.

The baseline run also caught the boundary counterexample at `x = 1`, but
framed it as a boundary probe without invoking the denominator-assumption rule.
The lesson's demonstrated effect is therefore qualitative (explicit rule
application and assumption naming), not a verdict change — the fixture's
expected verdict is `FAILED` either way.

Both runs noted the misleading SymPy residual `PASS` and correctly did not
treat it as establishing the universal claim, consistent with the verification
contract ("A CAS result verifies an algebraic step, not unstated assumptions").

## Evidence paths (schema 1.2)

Both runs are recorded with `evidence_path: numerical-examples`: the
load-bearing evidence was the boundary evaluation at `x = 1` (undefined left
side versus `2`), not the residual CAS check, which returned a misleading
`PASS`. Neither run is flagged (`evidence_flags` is empty) because no `VERIFIED`
was produced through a weak path.

## Token usage

| Condition | input | cached | output | reasoning |
| --- | ---: | ---: | ---: | ---: |
| baseline | 250,920 | 219,136 | 3,183 | 1,369 |
| lesson-assisted | 199,714 | 172,288 | 3,380 | 1,591 |

Lesson size: 652 bytes → 163 estimated tokens (the deterministic
`ceil(UTF-8 bytes / 4)` heuristic). Input counts are dominated by the installed
session skill and plugin catalog; the lesson-vs-baseline input delta is
non-monotonic and reflects cache variance, not lesson content.

## Limitations

- Single model, single reasoning effort, one in-scope fixture, one run per
  condition; not a model-accuracy benchmark.
- The lesson's demonstrated effect is qualitative and single-observation;
  broader multi-lesson evaluation (follow-up Phase 5) measures it as a
  distribution.
- The workspace ran from branch `feature/evidence-path-cas-check` at
  `30e289b`; the fixture was an uncommitted working-tree addition during the
  runs.

## Reproduction

```text
ln -s <repo>/skills/savant-research-verify ~/.codex/skills/savant-research-verify
cd <repo>
codex exec --json -s read-only --ephemeral \
  "Using the savant-research-verify skill, verify the research claim in tests/fixtures/cancellation-without-assumption.json. No files will be changed."
```

The lesson-assisted prompt additionally instructs the model to review
`openai/portable/learning/approved/lesson-proof-001.json` and apply the lesson
only if it matches the claim.
