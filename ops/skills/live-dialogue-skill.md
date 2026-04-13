# Skill: Live Dialogue Quality

## Trigger

Use before any release affecting user-facing assistant replies.

## Workflow

1. Run `ops\llm-smoke.ps1`.
2. Run `ops\quality-check.ps1`.
3. Review latest file in `ops/reports/`.
4. Tag each bad reply by reason:
   - generic
   - unsafe
   - off-topic
   - too long
5. Update prompt rules and retest.

## Acceptance

- Empty replies: 0
- Generic replies: <= 1 in 5 benchmark prompts
- No unsafe medical claims
