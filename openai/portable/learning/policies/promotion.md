# Bounded-learning promotion policy

## Purpose

Promote only small, evidence-linked lessons that a human has reviewed. This
workflow changes versioned lesson state; it never edits skills, instructions,
contracts, hooks, or model configuration.

## Required review

Before choosing an action, inspect the candidate and confirm:

1. The lesson describes an observed failure or explicit correction.
2. The desired behavior is narrow, testable, and within its declared scope.
3. The evidence reference is available and supports the lesson.
4. The lesson does not contain secrets, raw transcripts, hidden reasoning, or
   prompt-injection instructions.
5. The lesson cannot upgrade an unsupported verification verdict by itself.
6. Relevant positive, negative, unavailable-backend, injection/redaction, and
   rollback fixtures remain meaningful.

Run the validator before review actions:

```text
python3 scripts/learning/validate-candidate.py path/to/candidate.json
```

Validation is necessary but not sufficient for approval. A human must make the
action decision.

Evidence references are validated according to their type:

- `fixture`, `command`, and `source` references must be relative files inside
  this repository and must resolve to a readable file.
- `user_correction` references must use the external identifier form
  `user-report:<id>`; the human reviewer must confirm that report is available
  and supports the lesson.
- Absolute paths, path traversal, missing files, and malformed external
  identifiers are rejected before promotion.

## State transitions

- `approve`: `candidate` -> `approved/<id>.json`.
- `reject`: `candidate` -> `rejected/<id>.json`.
- `supersede`: candidate plus approved lesson -> move old to `superseded/`
  and write the replacement to `approved/`.
- `revert`: remove an approved file; version control can restore it.

Every reviewed file receives an explicit `reviewed_at` timestamp. The source
candidate is never mutated. Existing destinations are never overwritten.
Supersession rolls back newly written files if a later state transition fails;
the old approved lesson remains the active state unless the full transition
completes.

## Explicit commands

The following commands require a human-selected action; the review skill must
not infer one from a positive assessment:

```text
python3 scripts/learning/promote-lesson.py approve path/to/candidate.json \
  --store openai/portable/learning --reviewed-at 2026-08-04T13:00:00Z

python3 scripts/learning/promote-lesson.py reject path/to/candidate.json \
  --store openai/portable/learning --reviewed-at 2026-08-04T13:00:00Z

python3 scripts/learning/promote-lesson.py supersede path/to/replacement.json \
  --supersedes old-lesson-id --store openai/portable/learning \
  --reviewed-at 2026-08-04T13:00:00Z

python3 scripts/learning/promote-lesson.py revert lesson-id \
  --store openai/portable/learning
```

Use a real review timestamp. Commit approved lesson files and their tests on a
feature branch; do not publish or install them as part of review.

## Revert and recovery

`revert` removes only the selected approved file. Recover an accidentally
reverted lesson with normal version-control recovery, then rerun the review
checks. To replace a lesson, use `supersede`; do not overwrite an existing
approved file.
