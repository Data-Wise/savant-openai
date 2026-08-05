# Savant OpenAI pilot plan

**Status:** Pilot implemented; pre-commit hardening complete; runtime evaluation deferred
**Scope:** First OpenAI-facing research-verification adapter
**Date:** 2026-08-04

## Decision in one sentence

Build one small `savant-openai` package around a portable verification
contract; defer a separate `savant-codex` package until Codex-only hooks or
local enforcement are demonstrably needed.

## Why this shape

The Claude Savant plugin already contains 42 commands and 42 skills, including
proof, numerical, simulation, and statistical-QA workflows. Porting that
surface wholesale would increase context cost and preserve runtime assumptions
that do not belong in an OpenAI skill.

The first OpenAI surface should therefore expose one recognizable user goal:
**audit a mathematical or statistical claim and report exactly what was
checked**.

## Package boundaries

| Layer | Owns | Does not own |
|---|---|---|
| Portable contracts | statuses, evidence schema, verification rules, fixtures | host hooks or model settings |
| `savant-openai` | plugin manifest, focused skill, references, scripts, tests | Claude commands or personal config |
| Future `savant-codex` | Codex-only hooks and local enforcement | portable research policy |
| `codex-config` | config, trust records, compaction policy, MCP inventory | Savant domain logic |

## First skill behavior

`$savant-research-verify` selects exactly one mode:

- `proof`: structure, assumptions, load-bearing steps, CAS/formal checks;
- `statistics`: estimand, assumptions, diagnostics, independent calculation;
- `simulation`: grid completeness, seeds, MCSE, convergence, independent check;
- `reproducibility`: inputs, versions, commands, artifacts, and freshness.

The result uses `VERIFIED`, `PARTIALLY_VERIFIED`, `FAILED`, or `UNVERIFIED`.
`UNVERIFIED` is the safe result when a backend is missing, a check is
undecidable, or the evidence is insufficient.

## Token policy

- Keep the router below 500 lines and preferably below 1,000 tokens.
- Load one mode reference, not all references.
- Keep schemas and long examples outside `SKILL.md`.
- Execute deterministic scripts instead of displaying their source.
- Do not add a global Savant instruction block to `codex-config`.
- Keep learning disabled during ordinary verification; load at most three
  reviewed, task-scoped lessons when explicitly requested.
- Store candidate lessons outside the distributable package until they pass
  redaction, human review, and regression checks.

## Verification ladder

1. State the claim and assumptions.
2. Audit structure and individual steps.
3. Run a deterministic symbolic, numerical, or statistical check.
4. Search edge cases and counterexamples.
5. Escalate high-stakes results to a formal checker or human reviewer.

No level proves the truth of unstated assumptions. A successful CAS check
validates a step, not an entire theorem.

## Alternatives rejected

1. **Copy the Claude plugin:** rejected because manifests, commands, hooks,
   paths, and runtime contracts differ.
2. **Generate every platform variant immediately:** deferred until contract
   fixtures demonstrate that materialization prevents drift.
3. **Create a separate Codex repository now:** deferred because it would split
   ownership before an independent release or security lifecycle exists.

## Migration sequence

1. Approve this plan and [ADR-0001](../adr/ADR-0001-savant-openai-boundary.md).
2. Implement and verify the evidence-report and learning contract tests.
3. Add one deterministic proof/CAS adapter.
4. Add statistical and simulation adapters only after the first contract passes.
5. Run Codex evaluation fixtures, including unavailable-backend cases.
6. Add packaging and drift checks after runtime evidence justifies them.
7. Implement the bounded-learning schema and validator described in
   [BOUNDED-LEARNING.md](BOUNDED-LEARNING.md).
8. Reassess whether a Codex-only extension is justified.

## Non-goals for this pilot

- full parity with Claude Savant;
- automatic context compaction;
- model-specific prompt branches in every reference;
- hooks that silently enforce semantic correctness;
- autonomous self-editing, self-promotion, or transcript-to-policy learning;
- installation, publication, or changes to the Claude repository.

## Bounded learning decision

The approved learning design is documented in
[ADR-0002](../adr/ADR-0002-bounded-learning-boundary.md). It uses candidate
lessons, deterministic validation, human promotion, and regression fixtures.
It does not change model weights or permit automatic edits to skills,
instructions, contracts, or policies.

The implementation work is specified and staged in:

- [Bounded-learning specification](../specs/SPEC-bounded-learning-2026-08-04.md)
- [Bounded-learning TODO](../todo/TODO-bounded-learning.md)
- [Bounded-learning implementation plan](../plans/PLAN-bounded-learning.md)
- [Adversarial remediation plan](../plans/PLAN-adversarial-remediation-2026-08-05.md)
