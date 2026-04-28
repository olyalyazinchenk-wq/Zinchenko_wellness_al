# Agent Context Hub

## 2026-04-27 Sync Snapshot

The current operating north star is fixed in:

- `docs/PROJECT_NORTH_STAR_EXECUTION_PLAN_20260427.md`

Core target:

- one safe paid client cycle from Telegram entry to manual payment, AI draft, human review, client result, and follow-up

Current product architecture:

- demo-result preview
- `week`: Разбор на 7 дней — 3 900 ₽
- `premium`: Персональный разбор на 30 дней — 6 900 ₽
- `vip`: VIP-сопровождение на 30 дней — 14 900 ₽

## Project Mission

Build a premium Telegram-first nutrition-navigation service for Antigravity:

- free layer: structured clarity in Telegram
- paid layer: human-reviewed premium navigation dossier
- retention layer: 30-day Telegram follow-up after delivery

## Current Stage

Stage:

- controlled concierge pilot with branch reconciliation pressure and unsafe-lab gate correction

Objective:

- restore one clear active premium branch for user `1084557944`
- stop unsafe dossier progression from unreadable or unconfirmed labs
- close one fact-safe, human-reviewed client cycle without adding new product drift

## Latest Validated Evidence

- Benchmark reference: `ops/reports/quality_report_20260421T183148Z.md`
- Benchmark baseline remains stable: `20` prompts and `0` empty replies
- `WellnessBot/data/runtime_state.json` is empty at sync time:
  - no in-memory live session should be treated as authoritative state
- Freshest persisted premium branch: `20260425T214914Z_1084557944`
  - source: `WellnessBot/data/submissions/20260425T214914Z_1084557944.json`
  - `status_updated_at`: `2026-04-26T21:25:18Z`
  - payment state: `manual_payment_confirmed`
  - lab gate: `lab_quality_check.status=needs_resubmission`
  - review verdict: `needs_revision`
  - review source: `WellnessBot/data/drafts/20260425T214914Z_1084557944.review.json`
- Older unresolved premium branch: `20260425T212847Z_1084557944`
  - source: `WellnessBot/data/submissions/20260425T212847Z_1084557944.json`
  - review verdict: `must_rewrite_with_high_caution`
  - review source: `WellnessBot/data/drafts/20260425T212847Z_1084557944.review.json`
- Governance memory source: `WellnessBot/data/product_governance.json`
  - `115` stored experiments
  - `4` duplicated titles still repeating across `2-6` copies
- Supporting premium-structure risk reference: `ops/reports/complex_case_judge_report.json`
  - verdict: `fail`
- Landing and mini-app still align to the Telegram-first premium funnel; no new expansion change was found in `landing/index.html` or `mini-app/index.html`

## Current Operating Truth

- Primary channel: Telegram only
- Active wedge: premium nutrition-navigation, not diagnosis or treatment
- Flagship price: `6900 RUB`
- Payment mode for pilot: manual concierge confirmation through `PAYMENT_MODE=manual`
- Human review remains mandatory before dossier delivery
- DeepSeek remains an auditor, not a product authority
- One active premium case per Telegram user is the intended operating rule, but persisted data currently violates it
- Highest-risk workflow defect: branch `20260425T214914Z_1084557944` generated draft/PDF artifacts even though the lab gate still required resubmission

## Active Regressions

- Unsafe lab-gate bypass in the freshest premium branch:
  - owner: Lead Developer
  - signal: `20260425T214914Z_1084557944` reached draft/PDF generation while `lab_quality_check.requires_resubmission=true`
  - next fix action: block generation and delivery when the lab gate is unsafe, or explicitly invalidate the current artifacts until readable labs or manual biomarkers arrive
- Multi-branch drift for the same Telegram user:
  - owner: Operator + Lead Developer
  - signal: both `20260425T214914Z_1084557944` and `20260425T212847Z_1084557944` remain open despite the one-active-branch rule
  - next fix action: declare one branch active by persisted freshness and archive or merge the other in state, docs, and operator workflow
- Freshest premium dossier is still not delivery-safe:
  - owner: Product Strategist + Lead Developer
  - signal: `20260425T214914Z_1084557944.review.json` flags false endometriosis mention, unclear thyroid-medication status, ignored selenium intake, and empty working hypotheses
  - next fix action: regenerate strictly from confirmed intake facts and readable evidence, then rerun judge before any delivery decision
- Governance memory still overstates progress:
  - owner: Lead Developer
  - signal: `WellnessBot/data/product_governance.json` stores `115` experiments with `4` repeated titles
  - next fix action: deduplicate repeated proposals before the next digest so governance reflects live evidence instead of repeated AI drift

## Current Constraints

- Telegram remains the primary operating channel before, during, and after delivery
- Manual concierge payment remains the official pilot mode until live `PAYMENT_TOKEN` proof exists
- Only one active premium case may exist per Telegram user at a time
- Human review is mandatory before client delivery
- No diagnosis claims, no treatment claims, and no autonomous medical framing
- OCR/manual lab values are not facts until readable and confirmed
- Do not invent symptoms or conditions absent from the intake
- Do not let branded nutraceutical orientation become the core product value proposition
- Do not start new growth or UI branches until the branch truth and lab gate are under control
- Keep public launch blocked until payment, hosting, legal, and support surfaces are actually ready

## Next 12h Priorities

1. Reconcile user `1084557944` to one active premium branch and explicitly archive or merge the other branch.
2. Obtain readable labs or manual biomarker text for `20260425T214914Z_1084557944`, then regenerate and rerun judge from confirmed facts only.
3. Add or enforce a hard generation gate so `requires_lab_resubmission=true` cannot silently progress to delivery artifacts.
4. Deduplicate governance experiment memory while preserving the benchmark baseline from `ops/reports/quality_report_20260421T183148Z.md`.

## What A New Model Should Read First

1. This file
2. `docs/PROJECT_PULSE_LOG.md` (latest entry)
3. `docs/STRATEGY_LIVE_DELTA.md`
4. `WellnessBot/data/runtime_state.json`
5. `WellnessBot/data/submissions/20260425T214914Z_1084557944.json`
6. `WellnessBot/data/drafts/20260425T214914Z_1084557944.review.json`
7. `WellnessBot/data/submissions/20260425T212847Z_1084557944.json`
8. `WellnessBot/data/drafts/20260425T212847Z_1084557944.review.json`
9. `WellnessBot/data/product_governance.json`
10. `ops/reports/quality_report_20260421T183148Z.md`

## Context For New Model

Stage:

- controlled concierge pilot with branch reconciliation pressure and unsafe-lab gate correction

Objective:

- restore one active premium branch for user `1084557944`
- stop unsafe dossier progression from unreadable or unconfirmed labs
- deliver one fact-safe, human-reviewed client cycle without product drift

Constraints:

- Telegram-first only
- human review required before client delivery
- manual concierge remains official pilot mode
- one active premium branch per Telegram user
- no diagnosis or treatment framing
- no unreadable or unconfirmed lab facts
- no invented symptoms or unsupported condition claims
- no new growth or UI branches until branch truth and lab gating are fixed

Immediate next actions:

1. Use `status_updated_at` to declare `20260425T214914Z_1084557944` or `20260425T212847Z_1084557944` the single active branch, then archive or merge the other.
2. Do not deliver the current `20260425T214914Z_1084557944` PDF; first obtain readable labs or manual biomarkers and regenerate from confirmed facts only.
3. Add or verify a hard lab-gate block before draft/PDF generation, then deduplicate governance memory and log the correction in `docs/PROJECT_PULSE_LOG.md`.
