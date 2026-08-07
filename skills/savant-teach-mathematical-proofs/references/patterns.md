# Proof-Teaching Patterns

Use this reference when the core workflow needs a concrete model. Adapt the wording to the supplied proof; never copy an example's mathematics into a user's proof.

## Contents

- [1. Local justification and motivation](#1-local-justification-and-motivation)
- [2. Restoring skipped algebra](#2-restoring-skipped-algebra)
- [3. Handling inequalities and conditions](#3-handling-inequalities-and-conditions)
- [4. Definition order and dependencies](#4-definition-order-and-dependencies)
- [5. Glossing a result](#5-glossing-a-result)
- [6. Adding one worked instance](#6-adding-one-worked-instance)
- [7. Stopping at a possible error](#7-stopping-at-a-possible-error)
- [8. Preserving source formats](#8-preserving-source-formats)
- [9. Teaching-audit template](#9-teaching-audit-template)

## 1. Local justification and motivation

Every substantive step needs two different explanations.

### Source pattern

```text
Using Equation (3), we obtain the following expression.

    [new expression]
```

### Taught pattern

```text
Substituting Equation (3) for the within-group term is valid because
Equation (3) gives that term an equal expression. We make this
substitution now so that both summands use the same quantities and can
be collected on the next line.

    [new expression]
```

The first sentence answers “why is this valid?” The second answers “why
do it now?” If one sentence would be vague without the other, keep both.

### Useful local motivations

- isolate the term that will be bounded;
- put two expressions in the same variables;
- expose a cancellation or a common factor;
- put the expression into the form required by an earlier lemma;
- separate a leading term from a remainder;
- make the sign of a factor visible;
- prepare a quantity for a limit, expectation, or norm calculation.

Avoid motivations that could accompany any line, such as “this is
important,” “we continue,” or “this simplifies the proof.”

## 2. Restoring skipped algebra

Insert only the bridge lines needed to make the source transition
reproducible. Keep every original source line unchanged.

### Example: expansion followed by collection

If the source moves from

```latex
\[
  (a+b)^2 - a^2
\]
```

to

```latex
\[
  2ab+b^2,
\]
```

make the omitted rule visible:

```latex
\[
\begin{aligned}
(a+b)^2-a^2
  &= (a^2+2ab+b^2)-a^2
      &&\text{(expand the square)}\\
  &= 2ab+b^2
      &&\text{(cancel the two \(a^2\) terms).}
\end{aligned}
\]
```

Then add a local motivation, for example: “This form exposes the two
terms whose size will be controlled separately.” Do not replace the
source's original equation label with a new label merely to show the
bridge.

### Common bridge inventory

Check explicitly for:

- substitution, then expansion;
- expansion, then collection of like terms;
- factoring or distributing;
- changing a fraction to a common denominator;
- cancellation with its nonzero condition;
- changing summation order;
- applying a definition before simplifying;
- matrix or vector products with suppressed component calculations;
- a limit, expectation, norm, or probability identity applied in stages.

An intermediate line is not justified merely because it is algebraically
familiar. Name the rule and state any condition it needs.

## 3. Handling inequalities and conditions

Inequalities require sign and domain checks, not just symbolic
rearrangement.

### Safe pattern

```text
Because \(m>0\), multiplying both sides by \(m\) preserves the direction
of the inequality. We do this to remove the denominator before applying
the previously established bound.
```

### Failure pattern

```text
Assume \(x>0\). Therefore \(x(x-1)\ge 0\).
```

This is not licensed: \(x>0\) does not imply \(x-1\ge0\). For example,
values in \(0<x<1\) make the second factor negative. Mark the displayed
inequality as `[POSSIBLE MATHEMATICAL ERROR]` and stop the teaching
expansion there. Do not add the missing condition \(x\ge1\) yourself.

Check especially:

- multiplying or dividing by a quantity whose sign is unknown;
- taking square roots or powers without domain conditions;
- cancelling a factor that might be zero;
- replacing a strict inequality with a non-strict one;
- interchanging limits, sums, integrals, or expectations without a
  supplied justification;
- applying a bound outside its stated range.

## 4. Definition order and dependencies

Build the ledger in reading order. A teaching insertion must not use a
term just because it appears later in the source.

### Premature reference

```text
The variance term vanishes as \(m\to\infty\).
...
\operatorname{Var}(X)=\mathbb{E}[(X-\mathbb{E}X)^2].
```

If “variance” and `\operatorname{Var}` were not already prerequisites,
the first sentence is premature.

### Order-safe revision

```text
Here, \(\operatorname{Var}(X)\) denotes the variance of \(X\), defined by
\(\mathbb{E}[(X-\mathbb{E}X)^2]\). This is the nonnegative spread measure
that appears in the next bound.

The variance term then vanishes as \(m\to\infty\).
```

If the source defined the term earlier, use an exact location instead:
“using the definition of variance in the paragraph before Proposition 2.”
Do not invent a definition that changes the source's convention.

### Dependency ledger fields

For each nontrivial item, record:

| Item | First available at | Used by | Action |
| --- | --- | --- | --- |
| symbol or term | source line/equation | insertion or original line | define, cross-reference, or mark missing |

When an insertion depends on several results, name all of them rather
than referring to “the facts above.”

## 5. Glossing a result

A gloss must interpret the result and connect it to the proof's purpose.

### Weak gloss

```text
Thus \(R_m\le C/m\). This is the result we wanted.
```

### Strong gloss

```text
Thus \(R_m\le C/m\). The remainder is at most a constant times
\(1/m\), so its contribution shrinks to zero as \(m\) grows; this is the
rate needed for the next limiting argument.
```

Gloss major equations, bounds, identities, and conclusions immediately
after they are reached. Do not gloss every punctuation-level algebra
line. If a displayed line is only an intermediate bridge, a short local
purpose sentence is enough.

## 6. Adding one worked instance

Use a worked instance only when the abstract step is genuinely hard to
see. Keep it separate from the formal proof and use no new theorem.

### Example: summation collection

Suppose the existing proof uses

\[
\sum_{j=1}^{m}(u+v_j)=mu+\sum_{j=1}^{m}v_j.
\]

A compliant instance can choose \(m=3\), \(u=2\), and
\((v_1,v_2,v_3)=(1,4,5)\):

\[
\begin{aligned}
\sum_{j=1}^{3}(2+v_j)
  &= (2+1)+(2+4)+(2+5)\\
  &= 3+6+7\\
  &= 16,
\end{aligned}
\]

while

\[
3(2)+(1+4+5)=6+10=16.
\]

The two sides agree because the constant `2` appears once for each of
the three summands. The instance illustrates the existing collection
identity; it does not prove a new theorem or repair another line.

If the source proof is already transparent, report that no instance was
added. If a possible mathematical error was found, do not use an
example to “test” or repair it during the teaching pass.

## 7. Stopping at a possible error

Use a precise report rather than silently correcting the proof:

```text
[POSSIBLE MATHEMATICAL ERROR]
Location: the transition from Equation (5) to Equation (6).
Problem: the argument changes \(A\le B\) into \(A<B\) without a strictness
condition.
Why it is problematic: the supplied assumptions establish only
non-strict inequality.
Teaching status: expansion stopped at this transition.
```

If the issue is missing support rather than an apparent contradiction,
use one of these markers:

- `[CITE]`: an external fact is needed but no citation was supplied;
- `[MISSING PREREQUISITE]`: the step may be valid, but a required
  assumption or definition is absent from the supplied context.

Do not convert either marker into a new theorem, citation, assumption, or
corrected equation.

## 8. Preserving source formats

### Markdown

- Keep headings, lists, blockquotes, links, code fences, and existing
  display-math delimiters.
- Keep explanatory prose outside code fences unless the source explicitly
  treats the fence as prose.
- Do not normalize unrelated whitespace or rewrite links.

### Quarto

- Preserve YAML front matter, executable code chunks, chunk options,
  cross-references, callouts, and raw format blocks.
- Keep proof teaching prose outside executable chunks unless it is
  intentionally generated by code.
- Do not alter code, cached results, or execution options as part of a
  proof-teaching pass.

### LaTeX

- Preserve environments, equation labels, `\tag` values, citation keys,
  macros, cross-references, and source comments.
- Add intermediate aligned lines only where they fit the existing
  environment and do not steal an existing label.
- Keep teaching prose adjacent to the equation it explains; do not turn
  an inserted bridge into a separately numbered theorem.

After editing any format, inspect the diff for delimiter, environment,
label, and cross-reference drift.

## 9. Teaching-audit template

Use this compact table internally or in the final audit when the proof
has many steps:

| Step/location | Original statement preserved | Justification | Motivation | Algebra bridge | First-use items | Gloss | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Eq. (n) | yes/no | rule/result | local purpose | lines added | definitions/references | meaning + role | pass/flag |

The final report should also state:

- total original substantive steps annotated;
- total intermediate lines inserted and where;
- total terms/symbols defined or cross-referenced;
- total major results glossed;
- whether a worked instance was added;
- all integrity markers and the point where teaching stopped, if any;
- whether the definition-order audit passed.
