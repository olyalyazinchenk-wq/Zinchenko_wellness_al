# Ops Control Center

This folder is the execution center for fast, safe delivery.

## Commands

- `powershell -ExecutionPolicy Bypass -File .\ops\preflight.ps1`
- `powershell -ExecutionPolicy Bypass -File .\ops\bot-start.ps1`
- `powershell -ExecutionPolicy Bypass -File .\ops\bot-stop.ps1`
- `powershell -ExecutionPolicy Bypass -File .\ops\bot-restart.ps1`
- `powershell -ExecutionPolicy Bypass -File .\ops\bot-status.ps1`
- `powershell -ExecutionPolicy Bypass -File .\ops\llm-smoke.ps1`
- `powershell -ExecutionPolicy Bypass -File .\ops\quality-check.ps1`
- `powershell -ExecutionPolicy Bypass -File .\ops\connection-check.ps1`

## Purpose

- Keep runtime stable and observable.
- Run quick model quality checks before product pushes.
- Keep approvals and access requests explicit.

See:

- `docs/NCB.md` for strategy-to-execution map.
- `ops/permissions-checklist.md` for approval flow.
- `ops/skills/live-dialogue-skill.md` for dialogue QA loop.
- `ops/skills/release-skill.md` for release checklist.
