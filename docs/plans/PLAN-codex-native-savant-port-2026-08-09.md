# Codex-native Savant port roadmap

> **Status:** Governing roadmap — port one workflow at a time
> **Date:** 2026-08-09
> **Source:** Claude Savant plugin structure, adapted for Codex-native use

## Objective

Make `savant-openai` a small, coherent Codex plugin that follows the useful
organization of the Claude Savant plugin while preserving platform boundaries.
Port workflows incrementally; do not clone Claude commands, hooks, settings,
or marketplace metadata.

## Target structure

```text
savant-openai/
├── .codex-plugin/plugin.json       # installable plugin manifest
├── skills/<skill-name>/SKILL.md    # one focused Codex workflow
│   └── agents/openai.yaml          # optional UI metadata
├── docs/                           # help, tutorial, architecture, plans
├── scripts/                        # deterministic validation and packaging
├── tests/                          # contracts, fixtures, regression checks
├── .STATUS                         # current state and next gate
└── README.md                       # landing page and entry points
```

This follows Codex's internal plugin shape rather than Claude's layout:

- `.codex-plugin/plugin.json` is the only plugin manifest.
- `skills/<name>/SKILL.md` is the required unit of reusable behavior.
- `skills/<name>/agents/openai.yaml` carries optional Codex UI metadata.
- `references/`, `scripts/`, and `assets/` are optional resources inside a
  skill and are added only when the workflow needs them.
- `docs/`, `tests/`, and repository scripts support development and onboarding;
  they are not silently treated as runtime skill instructions.
- Claude `.claude-plugin/`, command files, hooks, settings, and marketplace
  metadata are not part of the Codex plugin contract.

Claude Savant's larger surfaces map as follows:

| Claude Savant surface | Codex-native equivalent | Rule |
| --- | --- | --- |
| command | focused skill invoked as `$skill-name` | Port behavior, not command syntax. |
| skill/reference | `skills/<name>/SKILL.md` plus one-level references | Keep context small and progressive. |
| `docs/COMMANDS.md` / `docs/SKILLS.md` | `docs/HELP.md` and `docs/TUTORIAL.md` | Explain the Codex invocation model. |
| `scripts/` | repository-local deterministic scripts | Keep repeatable checks out of prompts. |
| `tests/` and fixtures | contract/regression tests | Preserve safety and evidence guarantees. |
| Claude hooks/settings | no automatic port | Reassess only for a concrete Codex need. |
| research vault lifecycle | no automatic port | Add only when the OpenAI workflow truly needs it. |

## Porting contract

Every port is a separate feature branch and PR. A port is complete only when:

1. The Claude workflow's purpose and boundaries are written in plain language.
2. A Codex skill name and invocation are chosen.
3. The skill is rewritten for Codex tools, files, approvals, and output—not
   copied mechanically.
4. Any references are scoped and loaded progressively.
5. Positive, negative, unavailable, or safety fixtures exist where relevant.
6. The plugin validator, skill validator, tests, and whitespace checks pass.
7. `README.md`, `docs/HELP.md`, `docs/TUTORIAL.md`, `.STATUS`, and the roadmap
   are updated together.
8. The diff is independently reviewed before integration.

## Codex optimization gate

Every port must be optimized for Codex before it is considered complete:

- use Codex skill frontmatter and `agents/openai.yaml` metadata correctly;
- invoke through `$skill-name`, not a copied Claude command interface;
- keep `SKILL.md` concise and move optional detail into one-level references;
- use deterministic scripts for repeatable work instead of long prompt recipes;
- state tool, filesystem, branch, and approval boundaries explicitly;
- design outputs for compact, scannable handoffs and machine-checkable results;
- avoid loading the full Savant catalog, session history, or research vault by
  default;
- validate the real Codex invocation, not only copied file structure.

A port that preserves Claude behavior but increases context load, assumes Claude
hooks, or requires Claude-only state is incomplete.

## Codex structure gate

Before a port is accepted, validate the native package shape:

1. `plugin.json` parses and points to the intended `skills/` directory.
2. Every skill directory has a matching `SKILL.md` frontmatter name.
3. Every `agents/openai.yaml` has valid display metadata and names its skill in
   `default_prompt`.
4. Optional resources are referenced from the skill that owns them and do not
   become unscoped global instructions.
5. The official Codex plugin validator, repository validator, tests, and
   package inspection all pass.

## Port sequence

### Wave 0 — foundation (current)

- [x] Valid Codex plugin manifest.
- [x] Evidence-first research verification skill.
- [x] Mathematical proof teaching skill.
- [x] Bounded-learning review skill with explicit human transitions.
- [x] Codex repository scaffolding skill.
- [x] Sequential worktree coordinator skill.
- [x] Help and first-use tutorial surfaces.
- [ ] Package materialization and source-to-package drift checks.

### Wave 1 — high-value research workflows

Port one workflow per PR, in this order:

1. **Research session** — start, scope, record assumptions, and produce a
   bounded session artifact without copying Claude session state.
2. **Claim audit** — inspect claim/evidence alignment and distinguish absence
   of evidence from evidence of absence.
3. **Literature gap finder** — search and position a research question with
   explicit corpus and novelty limits.
4. **Methods communicator** — translate statistical methods for a specified
   audience without changing the method.
5. **Simulation architect** — design reproducible simulation plans and checks.

### Wave 2 — domain-specific research skills

Port only when a concrete OpenAI use case and acceptance fixtures exist:

- causal inference and identification theory;
- asymptotic theory and proof architecture;
- numerical methods and computational inference;
- sensitivity analysis and mediation workflows;
- figure, manuscript, and publication support.

### Wave 3 — optional integrations

Consider Obsidian, Zotero, or other integrations only behind explicit MCP
contracts, dry-run behavior, conflict rules, and approval gates. Integrations
must not become hidden prerequisites for the core plugin.

## Simplification rules

- Prefer one skill per user outcome; avoid a one-to-one port of all Claude
  commands.
- Use short, discoverable names for primary skills and keep detail in
  references.
- Keep `.STATUS`, roadmap, plans, specs, and architecture docs repository-owned.
- Keep host configuration, hooks, and model settings outside this repository.
- Do not add a new YAML contract when an existing Codex or MCP contract applies.
- Do not claim a port is complete because files were copied; require a usable
  Codex invocation and evidence-backed validation.

## Release gates

The plugin is not release-ready until Wave 0 package/drift checks pass and the
first-use documentation is current. Each later port may ship only if it does
not weaken the existing evidence, safety, or approval boundaries. Marketplace
publication, installation, tagging, and downstream distribution remain
separate approvals.

## Governing practice

This plan is the repository rule for future ports. When a platform capability
or Codex packaging convention changes, update this plan and the repository
rules before applying the new pattern to a skill. Record the evidence and
validation command used; do not rely on copied Claude structure or memory.

## Immediate next action

Finish package materialization and drift checks, then port the first Wave 1
workflow (`research-session`) as a bounded feature PR.
