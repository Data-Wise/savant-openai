# Verification status contract

Every research-verification result must use exactly one terminal status:

| Status | Meaning |
|---|---|
| `VERIFIED` | The stated claim passed the named checks within the stated scope. |
| `PARTIALLY_VERIFIED` | Some load-bearing components passed; others remain open. |
| `FAILED` | A named check found a contradiction, counterexample, or reproducible defect. |
| `UNVERIFIED` | Evidence was unavailable, undecidable, incomplete, or unsafe to interpret. |

Rules:

- A model explanation alone never produces `VERIFIED`.
- A CAS result verifies an algebraic step, not unstated assumptions or a whole theorem.
- A missing backend produces `UNVERIFIED`, never a guessed pass or fail.
- Every result records scope, assumptions, checks, evidence, and limitations.

