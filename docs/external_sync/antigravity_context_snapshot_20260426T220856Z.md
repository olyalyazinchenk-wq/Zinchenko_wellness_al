# Context For New Model - 2026-04-27 01:08 MSK

Stage: controlled concierge pilot with branch reconciliation pressure and unsafe-lab gate correction

Objective:

- restore one active premium branch for user `1084557944`
- stop unsafe dossier progression from unreadable or unconfirmed labs
- close one fact-safe, human-reviewed client cycle

Constraints:

- Telegram-first only
- human review required before client delivery
- manual concierge remains the official pilot mode
- one active premium branch per Telegram user
- no diagnosis or treatment framing
- no unreadable or unconfirmed lab facts
- no invented symptoms or unsupported condition claims
- no new growth or UI branches until branch truth and lab gating are fixed

Immediate next actions:

1. Use `status_updated_at` to declare `20260425T214914Z_1084557944` or `20260425T212847Z_1084557944` the single active branch, then archive or merge the other.
2. Do not deliver the current `20260425T214914Z_1084557944` PDF; first obtain readable labs or manual biomarkers and regenerate from confirmed facts only.
3. Add or verify a hard lab-gate block before draft/PDF generation, then deduplicate governance memory and log the correction outcome.

Reference benchmark:

- `ops/reports/quality_report_20260421T183148Z.md`
- baseline remains `20` prompts and `0` empty replies
