---
name: savant-repo-scaffold
description: Create or finish a Codex repository with a GitHub remote, safe branch layout, Codex-aware project detection, preflight checks, and explicit approval gates. Use when initializing a Codex/OpenAI plugin repository, connecting a local repository to GitHub, preparing a feature branch for a PR, or repairing remote and integration-branch setup.
---

# Savant Repo Scaffold

Scaffold or finish a Codex repository and its GitHub remote. Keep local domain
files, Codex skills, and host configuration separate. Do not import Claude
commands, hooks, `CLAUDE.md`, or Claude marketplace behavior.

## Safety boundary

- Read the current directory, branch, worktrees, status, remotes, and project
  markers before changing anything.
- Never implement from `main`; use a non-main feature branch.
- Treat repository creation, pushes, default-branch changes, branch
  protection, PRs, releases, and publication as separate approval gates.
- Never guess the GitHub owner, repository name, visibility, default branch, or
  required checks.
- Preserve uncommitted work. Never force-push.
- Do not modify another Savant repository or `codex-config` unless explicitly
  in scope.

## Workflow

1. Inspect the local repository:

   ```sh
   pwd
   git branch --show-current
   git worktree list
   git status --short
   git remote -v
   ```

   Detect a Codex plugin from `.codex-plugin/plugin.json`, skills from
   `skills/*/SKILL.md`, and tests, docs, and CI from the files actually present.
   The absence of `package.json`, `pyproject.toml`, or `DESCRIPTION` is valid
   for a Markdown/JSON plugin repository.

2. Establish repository identity:

   - Read `name` and `version` from `.codex-plugin/plugin.json`.
   - Confirm the GitHub owner, repository name, and public/private visibility
     when they are not already explicit.
   - Check the existing remote and GitHub repository before creation.

3. Create or connect the remote only after approval:

   - If `origin` exists, verify its URL; do not replace it silently.
   - If the repository does not exist, create it with the approved owner,
     name, and visibility, then push the current non-main branch.
   - Verify the remote URL, repository identity, and upstream tracking after a
     push.

4. Establish branch topology:

   - For repositories under `dev-tools`, create or use `dev` as the integration
     branch and keep `main` for release/default-branch work.
   - Use `feature/*` for implementation work. Do not silently make a feature
     branch the default branch.
   - If a repository already has a documented topology, follow it and report
     the exception.

5. Validate Codex structure:

   - Parse `.codex-plugin/plugin.json`.
   - Validate every `skills/*/SKILL.md` frontmatter and any
     `skills/*/agents/openai.yaml` metadata.
   - Detect the repository's actual test runner, documentation checks, and CI;
     do not assume Claude-specific commands or hooks.

6. Run preflight before commit or PR:

   - Run the full repository test suite.
   - Parse manifests and contract files.
   - Run the applicable skill validator and repository checks.
   - Run `git diff --check` and a repository-appropriate secret scan.
   - Stop and report failures. Do not auto-fix unless requested.

7. Report one compact state block containing the local path, branch, remote,
   visibility, integration/default branch, tracking state, checks, and the next
   approval gate. Stop at the requested gate.

## Codex-specific adaptations

Craft guidance is a policy source, not a runtime dependency. Adapt its Git
workflow and preflight ideas without calling Claude, reading or writing
`CLAUDE.md`, using Claude hooks, or assuming `.claude-plugin/plugin.json`.

Use `.codex-plugin/plugin.json` as the primary plugin marker. Prefer one
approval question per external mutation: create repository, push, configure
default branch, apply protection, create PR, or release.

Keep output ADHD-friendly: show current state first, one next action second,
and one blocker or approval gate third.

## Completion checklist

- [ ] Current branch and worktree are safe.
- [ ] Local plugin identity is valid.
- [ ] Remote identity and visibility are verified.
- [ ] `dev` exists for a `dev-tools` repository, or the documented exception is
      recorded.
- [ ] Tests, skill validation, and repository checks pass.
- [ ] No external mutation remains unapproved.
