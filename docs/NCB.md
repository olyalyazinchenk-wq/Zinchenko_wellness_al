# NCB (Navigation and Control Board)

## Mission

Build a premium Telegram-first wellness copilot that:

- talks like a real assistant (not a template bot),
- converts users into paid dossier flow,
- keeps sensitive handling aligned with Russian-contour requirements.

## Product North Star

"From confusion to action in one chat thread."

## Weekly scoreboard

- Response quality score (manual QA): target >= 4.2/5
- Generic-response rate: target < 20%
- Free to paid conversion: target >= 8%
- Paid flow completion: target >= 70%
- P95 response time: target < 8s

## Operating loops

1. Dialogue quality loop (daily)
- Run `ops\llm-smoke.ps1`
- Run `ops\quality-check.ps1`
- Fix prompt/model settings if score regresses

2. Revenue loop (daily)
- Track funnel: start -> screen -> pay -> dossier
- Review friction in first 5 user messages

3. Safety loop (daily)
- Red-flag escalation behavior spot check
- Ensure no diagnosis/treatment claims

## Release gate

No release unless all are true:

- Quality check report generated today.
- Bot process healthy.
- No critical safety regression.
- Payment and dossier flow smoke-tested.
