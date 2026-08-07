---
name: savant-teach-mathematical-proofs
description: Convert a stated mathematical proof into a fully taught proof without changing its mathematics. Use when asked to teach, expand, or annotate proofs in Markdown, LaTeX, Quarto, or pasted text: restore skipped algebra, justify each step, define notation at first use, audit definition order, and optionally add one worked instance while preserving the source's equations, assumptions, and format.
---

# Teach Mathematical Proofs

Turn a **stated proof** into a **fully taught proof**. The source mathematics is authoritative: expose reasoning that is already present, but do not redesign, repair, strengthen, or replace the argument.

Use this skill for pasted proof passages and for source files ending in `.md`, `.qmd`, `.tex`, or closely related plain-text formats. Work from source, not from a rendered PDF or HTML copy when the source is available.

If you need an evidence-based verdict on whether a proof is valid, use `savant-research-verify` instead. This skill teaches; it does not produce a verification verdict.

Load [references/patterns.md](references/patterns.md) when the proof has dense algebra, delicate inequality conditions, difficult first-use dependencies, a needed worked instance, or source-format preservation questions. It contains concrete phrasing patterns and failure cases; use it as a reference, not as a substitute for checking the supplied proof.

## Non-negotiable boundary

The task is:

> stated proof → explicit proof → pedagogically taught proof

It is not:

> stated proof → alternative proof

Do not silently change equations, inequalities, constants, coefficients, exponents, indices, quantifiers, assumptions, hypotheses, definitions, notation, bounds, limits, citations, labels, or conclusions. Preserve the proof's order and logical architecture. Add prose and algebraically equivalent intermediate lines only when they explain the existing argument.

If a mathematical step appears wrong, inconsistent, under-specified, or impossible to justify from the supplied context, stop the teaching expansion at that point and report a `[POSSIBLE MATHEMATICAL ERROR]`. Do not correct, reinterpret, or silently work around it. A missing source definition or prerequisite is an exposition problem; mark it `[CITE]` or `[MISSING PREREQUISITE]` rather than inventing a fact.

## Workflow

Follow these stages in order. Do not teach first and verify later.

### 1. Establish the source and format boundary

For a file task:

- Read the relevant source completely, including nearby definitions, assumptions, theorem statements, equation labels, footnotes, citations, and Quarto/LaTeX metadata that the proof relies on.
- Identify the exact proof passage to transform. If the file contains several proofs and the target is unclear, state the ambiguity before editing.
- Preserve YAML front matter, Markdown structure, LaTeX environments and commands, Quarto code fences/chunks, labels, cross-references, citations, and math delimiters. Never replace source with rendered output.
- Keep changes limited to the requested proof and its necessary teaching insertions. Do not reformat unrelated content.

For pasted text, treat all supplied definitions, prerequisites, and earlier results as the available context. Do not assume unstated background beyond what the passage explicitly permits.

Before changing a file, choose the requested artifact mode from context: inline response, a new taught-proof draft, or an in-place source edit. If no mode is stated, return the taught proof inline and identify the source location that would be changed; do not overwrite a file merely because it was provided for inspection.

### 2. Run a conservative mathematical check

Build a line-by-line map of the original proof before inserting teaching. Check only what is needed to preserve the source argument:

- each equality or inequality against the preceding line;
- each substitution against the equation or result being used;
- signs, factors, powers, indices, dimensions, and domains;
- whether each conclusion follows from the stated premises and earlier results;
- whether an alleged cancellation, division, limit, or inequality reversal has the required condition.

Do not use a new theorem, external citation, computer algebra result, or alternate derivation to rescue a questionable step. If the check fails, report the first precise location, the conflicting lines, and the reason it cannot be justified. Preserve the original text and stop the expansion there.

### 3. Build an internal dependency and definition ledger

Track, in source order:

- symbols and notation already defined;
- assumptions, domains, and prerequisites;
- named definitions, theorems, identities, and rules available;
- equations, lemmas, and conclusions already established;
- every term that needs a first-use definition or concise gloss;
- every inserted explanation and the items it depends on.

Maintain this invariant:

> No teaching insertion may refer to a symbol, term, theorem, equation, label, or result before it has been introduced or explicitly supplied as a prerequisite.

When the source already defines an item, point to the exact earlier location instead of redefining it. Use precise references such as “by the definition of (S_W) given immediately before Proposition 2,” not vague backward references such as “by the definition above.”

### 4. Expand the proof into a taught proof

Rewrite the complete target passage while retaining every original mathematical statement. Keep each explanation adjacent to the line it explains. For every substantive mathematical step, perform all applicable actions below.

#### Justify validity

Name the definition, prior result, assumption, algebraic rule, logical rule, or order property that licenses the move. Examples include:

- “by the definition of variance”;
- “substituting Equation (4)”;
- “using linearity of expectation”;
- “distributing the summation”;
- “factoring out the term independent of (j)”;
- “because (m>0), multiplying by (m) preserves the inequality.”

Do not leave a step as “clearly,” “obviously,” “trivially,” “after some algebra,” “simplifying,” or “it follows” unless the exact rule and intermediate calculation immediately follow.

#### Motivate the move

Add a short, local explanation of why the author takes this step now: what it isolates, aligns, cancels, exposes, bounds, or prepares for the next result. Keep justification and motivation distinct. For example:

> By substituting Equation (4), we replace the within-group quantity with the expression already controlled by the lemma. This puts both summands in the same variables so the terms can be collected on the next line.

Avoid generic filler such as “this is important.”

#### Restore skipped algebra and logic

Insert only the intervening lines a careful reader needs to reproduce the source transition. Common cases are substitution followed by expansion, expansion followed by collection, fraction manipulation, cancellation, a change in summation order, completing a square, an expectation/variance identity, a limit passage, or suppressed matrix products.

Each inserted line must be algebraically or logically equivalent to the source transition and must not introduce a new claim. Keep original source equations unchanged; identify inserted equations in the audit and, when the format permits, label them as teaching insertions rather than changing the source's existing labels.

#### Define terms and notation at first use

Define or adequately gloss every nontrivial symbol, operator, abbreviation, named theorem, and technical term at first appearance unless it is already covered by the stated prerequisites. A definition can be concise:

> Here, (operatorname{Var}(X)) denotes the variance of (X), (mathbb{E}[(X-mathbb{E}X)^2]).

Do not redefine elementary notation that the document's prerequisites clearly cover. Do not introduce a new theorem or citation in order to explain a step. If a needed external fact is genuinely required, write `[CITE]` at the point of need.

#### Gloss major results

Immediately after each major equation, identity, inequality, bound, or conclusion, add one sentence that says both what the result means in plain language and why it advances the proof. Interpret the result; do not merely repeat its symbols.

### 5. Add at most one worked instance

Add one fully worked numerical example or symbolic special case only when it materially clarifies an existing identity, manipulation, bound, or conclusion. The example must:

1. use the source's existing assumptions and notation where possible;
2. introduce no theorem, assumption, or result not already available;
3. show every calculation from start to finish;
4. state exactly which general step or result it illustrates;
5. remain visibly separate from the proof's formal logical chain.

Do not force an example into a proof when it would interrupt the argument or merely duplicate the algebra. Report why no example was added. Never use a worked example to validate or repair a questionable source step.

### 6. Re-run the definition-order and integrity audits

Read the completed taught proof from beginning to end. For every inserted justification, motivation, definition, intermediate line, gloss, and worked instance, verify that all referenced items are available at that point. Repair exposition only by moving a definition earlier, replacing a premature term with already-defined language, or adding an exact earlier reference.

Then compare the original and taught versions. Confirm that:

- all original equations and claims are still present and unchanged;
- inserted equations are equivalent bridges, not new results;
- no assumptions, constants, indices, labels, citations, or quantifiers drifted;
- the source format still parses structurally (front matter, fences, environments, delimiters, labels, and cross-references);
- unrelated file content was not modified.

For a file edit, inspect the diff and run the repository's relevant lightweight source checks when available. Do not treat a successful render as proof that the mathematics was preserved.

## Output contract

Return these sections in this order. For a file task, include source path and line/location references where useful.

### 1. Taught Proof

Provide the complete rewritten proof, not a list of annotations. Integrate original statements, restored algebra, justifications, motivations, first-use definitions, result glosses, and the worked instance if one was warranted. Preserve the source's Markdown, LaTeX, or Quarto syntax.

### 2. Teaching Audit

Report:

- Original substantive steps annotated: `N`.
- Intermediate mathematical lines inserted: `N`, with locations and purposes.
- Terms/symbols defined or explicitly cross-referenced: `N`, with locations.
- Major results glossed: `N`.
- Source-format checks performed and their outcome.

### 3. Worked Instance

State either where the single instance was added and what it illustrates, or why no instance was pedagogically useful. State explicitly that it is not an independent validation or repair of the source proof.

### 4. Mathematical Integrity

Report `none` or list each `[POSSIBLE MATHEMATICAL ERROR]`, `[CITE]`, and `[MISSING PREREQUISITE]` with exact locations. If a possible mathematical error was found, say where teaching stopped.

### 5. Definition-Order Audit

Report `passed`, or list each dependency violation and the exposition-only correction made. Do not silently repair mathematical content during this audit.

## Style guardrails

Write for a mathematically capable reader studying independently. Prefer precise local references, short explanations beside equations, explicit causal language, and a clear distinction between “why valid” and “why now.” Avoid rhetorical flourishes, detached essays, unexplained jargon, vague pronouns, and unnecessary repetition.

When working in a repository, preserve user changes and unrelated edits. Do not commit, publish, or alter external systems unless the user separately requests those actions.
