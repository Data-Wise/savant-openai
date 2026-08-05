# ADR-0001: Use a portable core with a thin OpenAI adapter

## Status

Accepted for the pilot; publication and installation remain approval-gated.

## Context

Savant is a mature Claude research plugin with proof, statistics, numerical,
simulation, and manuscript workflows. The desired OpenAI/Codex version must
save context, preserve verification discipline, and avoid copying Claude-only
commands or hooks.

## Decision

Create one `savant-openai` package containing:

- portable verification contracts and fixtures;
- one focused `savant-research-verify` skill;
- progressive-disclosure references;
- deterministic scripts for checks; and
- package-specific tests.

Keep the Claude repository unchanged. Do not create `savant-codex` yet. Add it
only if Codex-only hooks or local enforcement become independently valuable,
reviewable, and testable.

## Consequences

### Positive

- Smaller initial context footprint.
- One shared policy for ChatGPT and Codex.
- Clear ownership between plugin source and host configuration.
- No false portability claim for Claude hooks.
- Incremental migration driven by real evaluation results.

### Negative

- Initial duplication may exist while portable material is materialized.
- The first skill will not provide full Savant parity.
- A later Codex extension may require a second package and test matrix.

## Rejected alternatives

- Wholesale Claude-plugin reuse.
- Immediate full intermediate-representation generation.
- Separate repositories for every platform before independent ownership exists.

## Review trigger

Revisit this ADR when the first skill has runtime evaluations and there is a
concrete request for Codex-only lifecycle enforcement.
