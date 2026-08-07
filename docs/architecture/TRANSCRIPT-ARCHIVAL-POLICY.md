# Runtime transcript archival policy

**Date:** 2026-08-06
**Status:** Adopted

## Decision

Runtime evaluation measurements archive their **sanitized verdict excerpts**
under `docs/measurements/logs/<measurement-id>/`. **Full raw session dumps are
explicitly not archived.**

## Why

Runtime evaluations run locally through `codex exec`; they are non-deterministic
and only re-runnable, never script-reproducible. The durable evidence a
measurement's conclusions depend on is the final structured verdict block, not
the surrounding session.

Full raw dumps are not archived because they embed environment-specific
context:

- excerpts from the machine's `~/.codex/memories/MEMORY.md`;
- the installed session skill and plugin catalog;
- absolute paths and command history tied to one developer's machine;
- the 2026-08-06 evaluation produced roughly 430 KB of raw dumps for six runs.

Committing them would ship private, machine-local context into the repository
for negligible evidence value. CI artifacts are not a substitute here because
runtime evaluation runs on the developer machine, not in CI.

## Sanitization requirements

An excerpt is only archivable when `scripts/verify/sanitize-transcript.py`
accepts it. That script:

1. extracts the transcript's final `agent_message` (the structured verdict
   block);
2. redacts the repository root to `<repo>`, the Codex home to `<codex-home>`,
   and any other home path to `<home>`;
3. refuses to write when secret-like content (API keys, private keys, secrets)
   remains after redaction;
4. refuses to write when any absolute home path remains.

Archived excerpts must remain free of secret-like content and absolute home
paths; the offline test suite enforces this.

## Scope

Calibration and environment-probe transcripts are excluded from archival; only
runs that contribute to a measurement's recorded verdicts are archived. Each
archived measurement links its log directory from the measurement document's
`evidence_sources`.

## Measurements produced under this policy

- 2026-08-06 runtime Codex evaluation —
  [`docs/measurements/logs/runtime-codex-2026-08-06/`](../measurements/logs/runtime-codex-2026-08-06/)
  (six verdict excerpts, sanitized; raw dumps not archived).
