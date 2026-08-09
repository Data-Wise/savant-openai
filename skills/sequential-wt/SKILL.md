---
name: sequential-wt
description: Coordinate bounded implementation tasks from an integration branch by creating, delegating, reviewing, and cleaning up one feature worktree at a time. Use when work should remain isolated from dev while the coordinator retains repository context.
---

# Coordinator Sequential Worktree

Use this skill when the coordinator should remain on `dev` while an isolated
worker implements one bounded task.

## Workflow

1. Inspect the coordinator repository before Git operations:

   ```bash
   pwd
   git worktree list
   git branch --show-current
   git status --short
   ```

2. Preserve unrelated uncommitted work. Verify the integration branch (`dev`
   when present) and do not switch the coordinator away from it.

3. Create one isolated worktree:

   ```bash
   git worktree add <worktree-path> -b feature/<task-slug> dev
   ```

4. Give the worker the absolute worktree path, branch, goal, allowed paths,
   required checks, and exclusions. The worker must not merge, push, publish,
   or edit another worktree.

5. Review the result from the coordinator context:

   ```bash
   git diff dev...feature/<task-slug>
   git -C <worktree-path> status --short
   git -C <worktree-path> diff --check
   ```

   Verify claims against the actual diff and run relevant repository checks.

6. Use the repository's normal PR/integration process. Do not merge or push
   without explicit approval. Remove the worktree only after integration or a
   deliberate abandonment decision.

## Handoff template

```text
Worktree: <absolute-path>
Branch: feature/<task-slug>
Base: dev
Goal: <one bounded outcome>
Allowed paths: <small list>
Checks: <commands>
Do not: redesign the spec, touch unrelated files, merge, push, or publish
Report: PASS/FAIL, changed files, checks run, blockers
```

Use one worker at a time by default. Use parallel worktrees only when file
scopes are independent and the coordinator can review every resulting diff.
