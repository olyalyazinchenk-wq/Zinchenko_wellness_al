# Antigravity Sync Snapshot

Date: 2026-06-07 23:53 MSK
Mode: controlled concierge pilot
Payment mode: `PAYMENT_MODE=manual`
Public launch: blocked
Human review: required before delivery

## Executive Summary

- Runtime is live and now has fresh June 7 recovery proof.
- The lead blocker is not uptime but commercialization control.
- Same-user duplicate paid `habits` paths remain unresolved.
- A delivered paid case still conflicts with failed internal review.
- Disk headroom improved to ~7.14 GiB but remains below the 10 GB floor.
- Full-batch QA still aborts on prompt 1 because `ops/quality_probe.py` is all-or-nothing on model-path failures.

## Fresh Runtime Proof

- `2026-06-06 23:25:02-23:25:31 +03:00` handled bot updates
- `2026-06-07 13:59:45 -> 13:59:57 +03:00` dispatcher disconnect and successful reconnection

## Current Controlled-Pilot Truth

- Active mounted runtime rail: `20260606T202509Z_1084557944`
- Active offer/state: `habits`, `manual_payment_confirmed`, `habits_daily_log`
- Duplicate same-user paid stack still exists:
  - `20260603T112723Z_1084557944` = `nutri_chat`, `500 RUB`, `manual_payment_pending`
  - `20260603T113045Z_1084557944` = `habits`, `6900 RUB`, `manual_payment_confirmed`
  - `20260606T202509Z_1084557944` = `habits`, `6900 RUB`, `manual_payment_confirmed`
- Delivery-gate contradiction still exists in `20260531T183007Z_1084557944`: `delivered_to_client` plus `fail_major_issues`

## Repo And Sync Status

- No new tracked changes appeared in `WellnessBot/`, `tests/`, `landing/`, or `mini-app/` during this sync window.
- Tracked local deltas remain in `docs/DISK_HYGIENE_STATUS.md` and `ops/bot-status.ps1`.
- Local docs-only git write path is still blocked: `.git/index.lock: Permission denied`.
- This remote artifact was written through the GitHub connector instead of a local commit.

## Pilot-Ready Scope

- Only a controlled Telegram-first text flow with manual payment confirmation and human-reviewed delivery is pilot-ready.

## Public-Launch Blockers

- Duplicate same-user paid-path control is not repaired.
- Delivery-gate contradiction is not repaired.
- Public surfaces still overclaim proof, price, or payment flow.
- `C:` disk free space is still below `10 GB`.

## Next Actions

1. Canonicalize the June 3 / June 6 `habits` stack into one active paid path.
2. Add a hard guard against new same-user paid branches while another is unresolved.
3. Repair `20260531T183007Z_1084557944`.
4. Restore `C:` above `10 GB`.
5. Patch `ops/quality_probe.py` to preserve partial artifacts.
