# ADR-0002: Use bounded, reviewed learning instead of autonomous self-modification

## Status

Accepted; pilot and pre-commit hardening implemented; runtime evaluation remains deferred.

## Date

2026-08-04

## Context

Savant should improve from repeated verification failures and explicit user
corrections without increasing false claims, leaking conversation content, or
creating an unreviewable self-editing loop. Codex provides skills, local
memories, lifecycle hooks, and evaluation workflows, but these are separate
extension and persistence mechanisms rather than a documented autonomous
skill-training system.

The research literature shows that in-context reflection and episodic verbal
feedback can improve subsequent attempts. Those methods depend on the quality
of the feedback signal and do not establish that a generated lesson is true.

## Decision drivers

- Preserve evidence-first mathematical and statistical verification.
- Save tokens by keeping learning out of the normal verification path.
- Make every persistent change inspectable and reversible.
- Avoid raw transcript, secret, and prompt-injection persistence.
- Keep portable domain policy separate from Codex host configuration.
- Avoid creating a second Codex-only repository prematurely.

## Considered options

### Option 1: No learning

Safest and simplest, but repeated corrections remain manual and lessons are
lost between tasks.

### Option 2: Autonomous self-editing

The model edits its own skills, instructions, or contracts after each session.
This is rejected because a mistaken or injected lesson could silently change
future verification behavior and would be difficult to audit or roll back.

### Option 3: Bounded candidate lessons with human promotion

The model proposes a small, evidence-linked candidate. Deterministic checks and
human review are required before a versioned lesson enters the portable core.

### Option 4: Hook-first learning

A Codex hook captures and promotes lessons automatically. This is deferred:
hooks are useful lifecycle adapters, but they add trust, privacy, and host
configuration complexity before the learning contract has been tested.

## Decision

Adopt **Option 3**.

The first implementation will be a portable candidate-lesson schema,
redaction/validation checks, regression fixtures, and an explicit review
workflow. Learning will be a separate opt-in skill rather than an instruction
layer embedded in `savant-research-verify`.

Codex hooks may be considered later for private candidate capture only. They
will not promote lessons or modify instructions automatically.

## Consequences

### Positive

- Persistent improvements are reviewable, versioned, and reversible.
- Normal research verification keeps its small context footprint.
- Portable lessons can serve ChatGPT and Codex without copying Claude hooks.
- Regression fixtures can detect false confidence and overgeneralization.
- The boundary between `savant-openai` and `codex-config` remains clear.

### Negative

- A human must review candidates before they become durable knowledge.
- The first version will improve workflow behavior, not model weights.
- Candidate storage and promotion tooling add a small amount of maintenance.
- Some useful lessons may remain unpromoted until evidence is available.

### Risks and mitigations

- **Self-confirming false lesson:** Require independent evidence or a
  regression fixture.
- **Prompt injection in feedback:** Treat candidates as untrusted data; redact
  and scope before review.
- **Context bloat:** Load only scoped lessons with hard count and size limits.
- **Secret or transcript leakage:** Store minimal structured fields; never raw
  conversation text.
- **Stale guidance:** Add provenance, versioning, expiry, and rollback.
- **Host/plugin confusion:** Keep host hooks and memory settings in
  `codex-config`.

## Implementation sequence

1. Add `candidate-lesson.schema.json` and deterministic validation.
2. Add redaction, scope, and size-limit tests.
3. Add positive, negative, unavailable-backend, injection, and rollback
   fixtures.
4. Add the explicit `savant-learning-review` skill and promotion workflow.
5. Promote one narrowly scoped lesson and measure token and verdict impact.
6. Harden timestamps, evidence references, promotion rollback, and nested
   contract coverage before the first commit.
7. Reconsider an opt-in `Stop` or `SessionEnd` capture hook only after the
   contract and privacy tests pass.

## Review trigger

Revisit this ADR after runtime Codex evaluation or when there is a concrete need
for Codex-only lifecycle capture or enforcement.

## Related decisions

- [ADR-0001: Use a portable core with a thin OpenAI adapter](ADR-0001-savant-openai-boundary.md)
- [Bounded learning design](../architecture/BOUNDED-LEARNING.md)

## References

- [Codex skills](https://learn.chatgpt.com/docs/build-skills)
- [Codex memories](https://learn.chatgpt.com/docs/customization/memories)
- [Codex hooks](https://learn.chatgpt.com/docs/hooks)
- [OpenAI evals](https://developers.openai.com/api/docs/guides/evals)
- [Self-Refine](https://arxiv.org/abs/2303.17651)
- [Reflexion](https://papers.neurips.cc/paper_files/paper/2023/hash/1b44b878bb782e6954cd888628510e90-Abstract-Conference.html)
