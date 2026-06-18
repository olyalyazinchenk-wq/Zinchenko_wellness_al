# Agent Synchronization Protocol

## Purpose

Codex, Antigravity, and Hermes must operate on the same files, branch, stage,
and runtime evidence. Shared documentation is coordination state, not a
periodic copy between independent projects.

## Single Source Of Truth

- Workspace: `C:\Users\HP\Desktop\Новая папка`
- WSL mount: `/mnt/c/Users/HP/Desktop/Новая папка`
- Branch: `master`
- Stage marker: `docs/CURRENT_STAGE.json`
- Operational truth: `docs/AGENT_CONTEXT_HUB.md`
- Chronology: `docs/PROJECT_PULSE_LOG.md`

Agents must not use `main` or `/home/hermes/projects/nutrition_bot` for current
implementation work.

## Start Gate

Before work, every agent must:

1. Confirm the workspace path and branch.
2. Read the stage marker and the required truth documents from `AGENTS.md`.
3. Run `ops/agent-sync-status.ps1` or perform equivalent checks.
4. Stop if another agent has uncommitted changes in the same files and merge
   the intent before editing.
5. Verify current runtime evidence instead of trusting an old lock or log.

## Finish Gate

Before handoff, the acting agent must:

1. Preserve unrelated changes already present in the worktree.
2. Update the pulse log with concrete evidence.
3. Change `stage_id` only when the project stage actually changes.
4. Commit and push shared tracked changes to `master`.
5. Report any connector that did not receive the latest state.

## Runtime Ownership

Only the Windows scheduled task `WellnessBot` may run Telegram long polling.
Hermes and Antigravity may inspect, test isolated functions, and edit the
canonical project, but they must not launch a second polling process.

## Branch Policy

`master` is the canonical product branch. The GitHub default branch should be
`master`. The historical `main` branch may retain dashboard history, but it is
not an execution source until explicitly merged into `master`.
