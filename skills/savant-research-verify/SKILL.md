---
name: savant-research-verify
description: Audit mathematical proofs, statistical claims, simulations, or reproducibility with explicit evidence and a scoped verification verdict. Use when the user asks whether a derivation, proof, analysis, or simulation is correct.
---

# Savant research verification

Use this skill to distinguish a plausible model answer from a checked research
result. Do not claim global correctness from reasoning alone.

## Workflow

1. State the claim, scope, notation, data, and assumptions.
2. Select exactly one mode: `proof`, `statistics`, `simulation`, or `reproducibility`.
3. Read only that mode's reference file.
4. Run available deterministic checks; record the command, backend, and result.
5. Report one terminal verdict using the contract in
   `../../openai/portable/contracts/verification-status.md`.
6. Separate checked facts, model reasoning, unresolved assumptions, and human review.

## Stop conditions

- Missing or unavailable tools produce `UNVERIFIED`.
- An undecidable or unsafe expression produces `UNVERIFIED`.
- A failed load-bearing check produces `FAILED` or `PARTIALLY_VERIFIED`.
- Do not invent constants, rates, citations, data, seeds, or diagnostics.
- Do not call a proof verified when only examples or numerical checks passed.

## Mode references

- Proof: `references/proof.md`
- Statistics: `references/statistics.md`
- Simulation: `references/simulation.md`
- Reproducibility: `references/reproducibility.md`

## Output

```text
VERDICT: VERIFIED | PARTIALLY_VERIFIED | FAILED | UNVERIFIED
CLAIM:
SCOPE:
ASSUMPTIONS:
CHECKS:
EVIDENCE:
LIMITATIONS:
HUMAN REVIEW:
NEXT ACTION:
```

