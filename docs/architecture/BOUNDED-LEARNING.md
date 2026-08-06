# Bounded learning design

**Status:** Accepted design; pilot and pre-commit hardening implemented; runtime Codex evaluation complete
**Date:** 2026-08-04
**Scope:** `savant-openai` research-verification workflows

## Decision

Savant will support **bounded, eval-driven learning** rather than autonomous
self-modification.

Codex may help identify a reusable lesson from a failed check or an explicit
user correction. It may write a candidate lesson to private state, but it must
not automatically modify or promote:

- `SKILL.md` files;
- `AGENTS.md` or project instructions;
- verification contracts or policies; or
- installed plugin files.

Promotion requires human review, a versioned change, and passing regression
fixtures.

## Terminology

- **Task reflection:** A short explanation of what failed and what to try next
  in the current task. It is not persistent policy.
- **Candidate lesson:** A structured, unapproved proposal derived from evidence
  or explicit user feedback.
- **Approved lesson:** A reviewed, versioned rule or reference that passed
  regression checks.
- **Learning:** Updating external workflow state or documentation; not changing
  model weights.

## Lifecycle

1. A verification run produces a failure, limitation, or explicit correction.
2. A candidate lesson records the observed behavior, desired behavior, scope,
   evidence, provenance, and redaction result.
3. A deterministic validator checks schema, size, timestamps, evidence
   references, secrets, and scope.
4. A human accepts, edits, rejects, supersedes, or reverts the candidate through
   the explicit promotion workflow.
5. An approved lesson is committed on a feature branch as a small,
   task-specific reference or fixture.
6. Contract tests and representative Codex evaluations run before release.
7. A failed regression blocks promotion; rollback is a normal revert.

## State ownership

- **Private candidate state:** owned by the OpenAI/Codex adapter or a
  user-local store; never bundled into a release by default.
- **Portable approved knowledge:** owned by this repository under
  `openai/portable/learning/` and reviewed like code.
- **Host configuration and memory controls:** owned by `codex-config`.
- **Claude behavior:** remains outside this repository and is not silently
  modified by the learning loop.

The exact private-state path is an implementation decision. It must be
configurable, excluded from distributable artifacts, and safe to delete.

## Candidate lesson minimum fields

- stable identifier and schema version;
- task class (`proof`, `statistics`, `simulation`, or `reproducibility`);
- observed failure or correction;
- desired behavior;
- evidence reference or fixture identifier;
- scope and confidence;
- source hash or provenance marker;
- created and reviewed timestamps; and
- redaction status.

Do not store raw transcripts, credentials, hidden reasoning, personal data, or
claims that have no supporting evidence.

## Context and token policy

Learning is opt-in and absent from the normal verification path.

- Keep `savant-research-verify/SKILL.md` focused on verification.
- Use a separate, explicitly invoked `savant-learning-review` skill later.
- Load at most one relevant learning reference per task.
- Inject at most three compact approved lessons.
- Target 300–600 tokens for a candidate lesson and avoid full transcript
  replay.
- Deduplicate, scope, and expire lessons that no longer improve evaluations.
- Preserve `UNVERIFIED` when evidence is missing; a lesson cannot upgrade a
  verdict by itself.

## Hooks

Hooks are deferred for the first implementation.

If a future Codex hook is added, it may create a private candidate draft at
`Stop` or `SessionEnd` after explicit opt-in. It must not promote lessons,
edit source instructions, or silently inject unreviewed state. Hook trust and
host configuration remain Codex responsibilities.

## Evaluation requirements

Every approved lesson must be tested against:

- a positive case where the lesson helps;
- a negative case where it must not overgeneralize;
- an unavailable-backend case;
- a prompt-injection or secret-redaction case; and
- the existing verification fixtures.

The acceptance signal is improved or preserved scoped behavior, not the
model's self-assessment. A lesson that increases false `VERIFIED` results is a
regression even if its prose appears more confident.

## Implemented layout

```text
openai/portable/learning/
├── contracts/
│   └── candidate-lesson.schema.json
├── policies/
│   └── promotion.md
└── approved/
    └── lesson-proof-001.json

skills/savant-learning-review/
└── SKILL.md

scripts/learning/
├── validate-candidate.py
└── promote-lesson.py

tests/learning/
├── fixtures/
│   ├── positive-lesson.json
│   ├── negative-overgeneralization.json
│   ├── unavailable-backend.json
│   ├── prompt-injection.json
│   ├── secret-redaction.json
│   └── rollback-supersession.json
└── test_promotion.py

tests/
├── test_candidate_validation.py
├── test_contracts.py
└── test_learning_fixtures.py
```

The approved directory contains only reviewed, versioned lessons. Candidate
state remains outside the distributable portable store, and no hook or
automatic capture is enabled.

The current measurement is fixture-backed contract-level dogfood evidence. Its
byte-based token estimate is not model-token accounting, and it does not
establish runtime Codex accuracy.

The 2026-08-06 runtime evaluation ran the skill in actual `codex exec`
sessions on the three fixture classes, baseline and lesson-assisted: all six
verdicts matched the expected terminal status, the lesson preserved every
baseline verdict (no false `VERIFIED`), and actual model token usage was
recorded per run (see
[MEASUREMENT-runtime-codex-2026-08-06.md](../measurements/MEASUREMENT-runtime-codex-2026-08-06.md)).

## References

- [Codex skills and progressive disclosure](https://learn.chatgpt.com/docs/build-skills)
- [Codex memories and state ownership](https://learn.chatgpt.com/docs/customization/memories)
- [Codex lifecycle hooks and trust](https://learn.chatgpt.com/docs/hooks)
- [OpenAI evaluation workflow](https://developers.openai.com/api/docs/guides/evals)
- [Self-Refine: Iterative Refinement with Self-Feedback](https://arxiv.org/abs/2303.17651)
- [Reflexion: Language Agents with Verbal Reinforcement Learning](https://papers.neurips.cc/paper_files/paper/2023/hash/1b44b878bb782e6954cd888628510e90-Abstract-Conference.html)
