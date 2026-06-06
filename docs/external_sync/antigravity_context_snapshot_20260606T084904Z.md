# Antigravity Context Snapshot - 2026-06-06 11:49 MSK

## Stage
Controlled concierge pilot. Public launch remains blocked.

## Current Truth
- `PAYMENT_MODE=manual`
- human review required before delivery
- strongest recent proof-bearing `nutri_chat` session is expired in runtime state
- no new tracked code changes landed in `WellnessBot`, `ops`, `tests`, `landing`, or `mini-app` during this sync window
- latest completed benchmark anchor remains `ops/reports/quality_report_20260531T083403Z.md`
- current QA interpretation remains `docs/WELLNESS_DIALOGUE_QA_20260605.md`
- `C:` free space is approximately `3.47 GiB`

## Must-Hold Rules
- Telegram-first only
- manual payment remains the active pilot mode
- one canonical paid path per Telegram user
- no new same-user paid branch while unresolved review, expiry, or delivery contradictions remain
- no diagnosis or treatment framing
- no public launch until canonical path, review gate, and product-surface truth are repaired

## Current Blockers
- expired `nutri_chat` continuity state
- same-user branch multiplication
- `delivered_to_client` while internal review still fails on a higher-ticket case
- QA runner still aborts on prompt `1`
- low disk headroom
- local `.git/index.lock` permission failure

## Next Actions
1. Restore disk above `10 GB`.
2. Repair `.git` write path.
3. Add expiry guard for `nutri_chat`.
4. Patch partial QA artifact capture.
5. Repair delivery contradiction.
6. Normalize one approved ladder only after those control fixes land.
