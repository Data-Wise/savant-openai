# Deterministic scripts

Scripts perform bounded, reproducible checks and emit deterministic results.

## Candidate validation

Validate a candidate lesson with:

```bash
python3 scripts/learning/validate-candidate.py path/to/candidate.json
```

The validator uses only the Python standard library and checks the portable
candidate contract, lifecycle state, size limit, scope fields, date formats,
timezone-aware timestamps, evidence-reference safety, secret-like content, and
prompt-injection-like content.

The validator does not promote candidates or modify source instructions.

## Human promotion

Apply an explicit reviewed state transition with:

```bash
python3 scripts/learning/promote-lesson.py approve path/to/candidate.json \
  --store openai/portable/learning --reviewed-at 2026-08-04T13:00:00Z
```

The command also supports `reject`, `supersede`, and `revert`. It validates
before writing, preserves the source candidate, refuses unsafe lifecycle
transitions and overwrites, and never edits skills or instructions. See
`openai/portable/learning/policies/promotion.md` for the review gate.

## Dogfood measurement

Compare a fixture baseline with an explicitly supplied review-path verdict:

```bash
python3 scripts/learning/measure-lesson.py \
  tests/fixtures/planted-proof-error.json \
  openai/portable/learning/approved/lesson-proof-001.json \
  --with-lesson-verdict FAILED
```

The command reports heuristic context cost, confirms that normal verification
loads no lesson, and rejects unsupported upgrades to `VERIFIED`.
