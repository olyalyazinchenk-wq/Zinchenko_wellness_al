# Context For New Model - 2026-06-08 11:57 MSK

## Stage
- Controlled Telegram concierge pilot where runtime remains live enough for a controlled pilot, but commercialization control and public-surface truth are still incoherent because one user still spans multiple recent paid `nutri_chat` and `habits` branches, the older delivered paid case still conflicts with failed review, and root plus mini-app surfaces still overclaim price, payment, or delivery truth.

## Objective
- Collapse the current same-user paid stack to one canonical path.
- Repair the delivered-case contradiction.
- Restore benchmark observability.
- Align public surfaces to the approved Telegram-first manual-review model while keeping runtime stable.

## Constraints
- Telegram-first only.
- `PAYMENT_MODE=manual`.
- Human review remains mandatory before delivery.
- One canonical paid path per Telegram user.
- Text-only intake remains the only proven live modality.
- Disk free space is `7641583616` bytes (`~7.12 GiB`) at `2026-06-08 11:57:57 +03:00`, still below the `10 GB` floor.
- Latest completed benchmark reference: `ops/reports/quality_report_20260531T083403Z.md`.
- Current QA interpretation: `docs/WELLNESS_DIALOGUE_QA_20260608.md`.
- The full batch still aborts on prompt `1`.
- Google Drive file discovery/create/upload/share tools are unavailable in the current Codex session.

## Current Truth
- The freshest runtime continuity proof is still the June 7 reconnect sequence at `2026-06-07 13:59:45 -> 13:59:57 +03:00`.
- The mounted runtime rail still points to `20260606T202509Z_1084557944` with `offer = habits` and `step = habits_daily_log`.
- The same user still holds unresolved recent paid state across multiple current rails:
  - `20260602T055745Z_1084557944` = `nutri_chat`, `manual_payment_confirmed`
  - `20260603T112723Z_1084557944` = `nutri_chat`, `manual_payment_pending`
  - `20260603T113045Z_1084557944` = `habits`, `manual_payment_confirmed`
  - `20260603T121917Z_1084557944` = `nutri_chat`, `manual_payment_confirmed`
  - `20260606T202509Z_1084557944` = `habits`, `manual_payment_confirmed`, and mounted as active runtime state
- `20260531T183007Z_1084557944` still combines `intake_status = delivered_to_client` with `internal_review.judge_verdict = fail_major_issues`.
- `mini-app/index.html` still sells a `1 000 ₽` `Wellness Clarity` tier and promises PDF dossier output plus Telegram support; it should not be described as placeholder-only.
- Root `index.html` still contains YooKassa, guaranteed-PDF, and off-map pricing claims that outrun the approved pilot truth.

## Immediate Next Actions
1. Declare one canonical current commercial path across the June 2 / June 3 / June 6 same-user stack.
2. Add a hard guard so new same-user same-offer or same-ladder paid branches cannot be created while older paid state is unresolved.
3. Audit and repair `20260531T183007Z_1084557944`.
4. Neutralize the mini-app and root-page overclaims.
5. Patch `ops/quality_probe.py` for per-prompt partial artifacts and explicit proxy behavior.
6. Restore disk headroom above `10 GB`.