# savant-openai

Portable research-verification workflows for ChatGPT and Codex.

## Current scope

This repository is a **spec-first pilot**. It defines the boundary between:

- portable mathematical and statistical verification policy;
- the OpenAI skill package;
- future Codex-only hooks and local enforcement; and
- the separate `codex-config` host-configuration repository.

The existing Claude Savant plugin remains the source of current research
workflows and is intentionally unchanged by this pilot.

## First skill

`$savant-research-verify` is a focused router for:

1. proof and algebra checks;
2. statistical reasoning and diagnostics;
3. simulation quality and reproducibility; and
4. evidence and human-review escalation.

It does not claim that a language-model derivation is correct without
recorded evidence.

## Bounded learning

`$savant-learning-review` is a separate, explicitly invoked workflow for
reviewing candidate lessons. It validates evidence and scope, then requires a
human-selected approve, reject, supersede, or revert action. Normal research
verification loads no learning context.

## Repository scaffolding

`$savant-repo-scaffold` provides a Codex-native setup workflow for GitHub
remotes, `dev-tools` branch topology, plugin detection, skill validation, and
preflight checks. It does not import Claude commands, hooks, or marketplace
metadata.

## Status

The repository uses `dev` as its GitHub default integration branch, with
implementation work on `feature/bootstrap-savant-openai`.
Implementation, packaging, installation, commit, push, and publication remain
approval-gated.

Read the [repository workflow and protection policy](docs/architecture/REPOSITORY-WORKFLOW.md)
for the Codex-session boundary and branch settings.

Read [the architecture plan](docs/architecture/SAVANT-OPENAI-PLAN.md) first.
