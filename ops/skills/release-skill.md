# Skill: Fast Safe Release

## Trigger

Use for any production push in accelerated mode.

## Workflow

1. `ops\preflight.ps1`
2. `ops\bot-restart.ps1`
3. `ops\llm-smoke.ps1`
4. Validate Telegram commands:
   - `/start`
   - `/chat`
   - `/health` (admin)
5. Check logs via `ops\bot-status.ps1`

## Release decision

- Go if all smoke checks pass and no critical log errors.
- Hold if safety behavior regresses or replies are empty/template-only.
