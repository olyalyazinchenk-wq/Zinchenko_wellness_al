# Shared Agent Bootstrap

These instructions apply to Codex, Antigravity, and Hermes.

## Canonical Workspace

- Windows: `C:\Users\HP\Desktop\Новая папка`
- WSL: `/mnt/c/Users/HP/Desktop/Новая папка`
- Git remote: `olyalyazinchenk-wq/Zinchenko_wellness_al`
- Working branch: `master`

Do not implement this project in a copied workspace. In particular,
`/home/hermes/projects/nutrition_bot` is a legacy archive and must not run
Telegram polling.

## Required Startup Order

Read these files before planning or changing the project:

1. `docs/CURRENT_STAGE.json`
2. `docs/AGENT_CONTEXT_HUB.md`
3. `docs/KNOWLEDGE_SYNC_HUB.md`
4. `docs/PROJECT_PULSE_LOG.md`
5. `docs/AGENT_SYNC_PROTOCOL.md`

If narrative documents disagree, use the newest persisted evidence and update
the shared files before continuing.

## Coordination Rules

- One stage ID applies to every agent.
- One canonical Git branch applies to every agent: `master`.
- One Telegram polling owner is allowed: the Windows scheduled task
  `WellnessBot` running `WellnessBot/main.py`.
- Never start a second bot process from WSL, Hermes, Antigravity, a terminal,
  or a copied project.
- Before handoff, update `docs/CURRENT_STAGE.json` when the stage changes and
  append the evidence to `docs/PROJECT_PULSE_LOG.md`.
- Do not claim synchronization while tracked changes remain unpublished or an
  agent is operating outside the canonical workspace.

Run `powershell -ExecutionPolicy Bypass -File ops/agent-sync-status.ps1` to
check the shared state.
