# Contract tests

Run the current test suite with:

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

The suite is standard-library based and must run without network access.

The current suite contains 28 tests. It also checks nested evidence-report
contracts, the plugin manifest, and skill frontmatter.

## Candidate validation

`test_candidate_validation.py` covers:

- valid candidate acceptance;
- required-field and task-class rejection;
- reviewed-state requirements;
- secret-like content rejection; and
- candidate size limits.
- timezone-aware timestamps; and
- file-backed evidence-reference safety.

`test_learning_fixtures.py` runs the standalone Phase 2 matrix:

- positive scoped lesson;
- negative overgeneralization;
- unavailable backend;
- prompt injection;
- secret redaction; and
- rollback/supersession.

`learning/test_promotion.py` covers the Phase 3 lifecycle:

- explicit approval into versioned approved storage;
- rejection into reviewed storage;
- supersession of an existing approved lesson;
- reversible removal of an approved lesson; and
- refusal of unsafe or non-candidate transitions.

`learning/test_measurement.py` covers the Phase 4 measurement guard:

- review-only context overhead;
- normal-path context isolation;
- verdict preservation;
- unsupported `VERIFIED` upgrades; and
- task-scope matching.

The fixtures in `fixtures/` define the first evaluation matrix:

- correct evidence must pass;
- planted contradictions must fail;
- missing backends must remain unverified;
- partial evidence must not be promoted to verified.

The negative and unavailable-backend cases must never claim `VERIFIED`.
