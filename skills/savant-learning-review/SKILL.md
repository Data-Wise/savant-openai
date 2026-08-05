---
name: savant-learning-review
description: Review bounded-learning candidate lessons for evidence, scope, safety, and regression risk, then report an explicit recommendation. Use when a user asks to inspect, approve, reject, supersede, or revert a Savant learning candidate; never infer promotion from model confidence.
---

# Savant learning review

Use this skill only for an explicitly requested learning review. Keep learning
out of ordinary verification and never edit `SKILL.md`, `AGENTS.md`, policies,
contracts, hooks, or model configuration.

## Workflow

1. Read [the promotion policy](../../openai/portable/learning/policies/promotion.md).
2. Inspect the candidate and run the deterministic validator.
3. Check evidence, scope, desired behavior, privacy, prompt-injection risk,
   overgeneralization, and verdict-preservation risk.
4. Check the relevant regression fixtures; missing or unavailable evidence is
   `UNVERIFIED`, not approval evidence.
5. Report one recommendation: `APPROVE`, `REJECT`, `SUPERSEDE`, `REVERT`, or
   `HOLD`, with the reason and next check.
6. Run `promote-lesson.py` only when the user explicitly selects the action in
   the current task. Never infer approval from a favorable review.

## Output

```text
REVIEW: PASS | FAIL | HOLD
CANDIDATE:
SCOPE:
EVIDENCE:
SAFETY:
REGRESSION:
RECOMMENDATION: APPROVE | REJECT | SUPERSEDE | REVERT | HOLD
REASON:
NEXT ACTION:
```

## Token discipline

- Load one candidate and one relevant reference at a time.
- Do not load raw transcripts or hidden reasoning.
- Keep the review focused on the declared task class and scope.
- Do not add learning context to normal verification.

## Explicit state changes

Use the repository script described in the policy. The script validates before
writing, refuses unsafe lifecycle transitions, preserves the source candidate,
and never overwrites an existing destination. A review recommendation alone is
not permission to run an approval action.
