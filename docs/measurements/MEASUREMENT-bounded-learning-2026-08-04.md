# Bounded-learning dogfood measurement

**Date:** 2026-08-04  
**Lesson:** `lesson-proof-001`  
**Fixture:** `tests/fixtures/planted-proof-error.json`  
**Scope:** `savant-research-verify/proof`

## Result

| Path | Learning context | Estimated tokens | Verdict |
| --- | --- | ---: | --- |
| Baseline verification | No | 15 | `FAILED` |
| Explicit review path | Yes | 78 | `FAILED` |

The verdict was preserved. The normal verification path loaded no learning
context. The review-only path added 63 estimated tokens.

The estimate uses `ceil(UTF-8 bytes / 4)`. It is a deterministic comparison
heuristic, not model-token accounting or evidence that a model answer is
correct. Unsupported upgrades from a non-`VERIFIED` baseline to `VERIFIED`
are rejected by the measurement command.

## Reproduction

```text
python3 scripts/learning/measure-lesson.py \
  tests/fixtures/planted-proof-error.json \
  openai/portable/learning/approved/lesson-proof-001.json \
  --with-lesson-verdict FAILED \
  --output docs/measurements/MEASUREMENT-bounded-learning-2026-08-04.json
```

## Limitations

This is one deterministic fixture and one approved lesson. It demonstrates
verdict preservation and review-only context isolation; it does not establish
general model accuracy or a production token count. More lessons require new
fixture-backed measurements.
