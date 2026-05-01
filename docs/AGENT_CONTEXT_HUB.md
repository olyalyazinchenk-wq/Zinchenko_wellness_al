# Agent Context Hub

Updated: 2026-05-01 09:17 MSK


## Единый GitHub Source Of Truth

- Главная точка входа для разработки и передачи контекста: docs/PROJECT_DEVELOPMENT_SINGLE_SOURCE_OF_TRUTH.md.
- Этот файл можно давать новым разработчикам, аудиторам и моделям вместо пересылки разрозненных локальных документов.

## Краткий статус (RU)

- Режим: controlled concierge pilot. Public launch по-прежнему заблокирован до отдельного решения.
- Активная оплата в пилоте: `PAYMENT_MODE=manual`. Human review обязателен перед любой выдачей клиенту.
- Изменения этого прогона: добавлен безопасный «пример результата» для кнопки в боте (текстовый демо-фрагмент), и зафиксирован аудит внешнего UI-макета Google AI Studio как **не-backend** (только UX-референс/бэклог).
- Новый критический риск среды: свободное место на `C:` просело до `2.69 GB`, поэтому тяжелые артефакты и новый PDF-поток нельзя считать безопасными до очистки диска.

## Stage

- controlled concierge pilot with same-user state drift, router-overreach quality blockage, lab-gate enforcement pressure, and critical disk headroom risk

## Objective

- restore one coherent paid-path truth for the current same-user case
- stop unsafe premium delivery from unreadable or unconfirmed lab evidence
- stop first-touch Telegram quality from being hidden behind deterministic templates
- close one fact-safe, human-reviewed paid cycle before any new growth work

## Product Direction

- Telegram-first only
- service ladder remains:
  - `demo` builds trust
  - `week` is the low-friction entry rail
  - `premium` remains the flagship proof path
  - `vip` stays parked until operator-load evidence exists
- official pilot payment mode: `PAYMENT_MODE=manual`
- human review is mandatory before any client delivery

## Done

- Telegram-first operating model remains locked
- manual concierge payment remains the official pilot mode
- product prices remain locked:
  - `week` = `3900 RUB`
  - `premium` = `6900 RUB`
  - `vip` = `14900 RUB`
- latest QA truth has been validated and captured:
  - benchmark report: `ops/reports/quality_report_20260429T080345Z.md`
  - `20/20` prompts returned non-empty replies
  - `20/20` prompts were intercepted by `route_live_reply()`
  - `0/20` prompts reached the model
  - clarifying-question count remains `0/20`
- latest case truth has been re-read from raw artifacts:
  - `WellnessBot/data/runtime_state.json`
  - `WellnessBot/data/submissions/20260425T212847Z_<REDACTED_ID>.json`
  - `WellnessBot/data/submissions/20260425T214914Z_<REDACTED_ID>.json`
  - both premium review artifacts
- runtime is currently up:
  - clean bot start logged at `2026-05-01 00:45:55 MSK`
  - no new local crash loop was observed in `bot.stderr.log`
- admin digest delivery hardened:
  - product digest text is now split into Telegram-safe chunks before sending (`WellnessBot/main.py`)
- product example experience improved:
  - `PRODUCT_EXAMPLES_TEXT` now contains a concrete safe demo structure (`WellnessBot/texts.py`)
- external UI audit captured:
  - `docs/GOOGLE_AI_STUDIO_MOY_PROJEKT_AUDIT_20260501.md`

## Current Truth

- one live `week` runtime session still exists at `consent`:
  - `submission_id = 20260427T173913Z_<REDACTED_ID>`
  - there is still no matching persisted submission JSON
- the same user still has two unresolved `premium` branches:
  - `premium_fresh_20260425T214914Z`
  - `premium_legacy_20260425T212847Z`
- `premium_fresh_20260425T214914Z`
  - manual payment confirmed
  - `requires_lab_resubmission=true`
  - remains evidence-only and unsafe for delivery
- `premium_legacy_20260425T212847Z`
  - manual payment confirmed
  - review verdict remains `must_rewrite_with_high_caution`
  - remains the only realistic premium rewrite candidate if proof closure is attempted
- first-touch chat quality is still not actually model-led:
  - symptom prompts are being answered by deterministic templates
  - duplicate-pattern clusters remain visible
  - unsupported detail risk remains present
- landing and mini-app still align to the Telegram-first premium funnel:
  - no new execution-critical surface shift was found in `landing/index.html` or `mini-app/index.html`
- governance memory remains bloated:
  - `115` experiments
  - `4` duplicate title groups
- disk pressure remains active:
  - `C:` free space is `2.69 GB`
  - the `10 GB` safety floor is critically unmet

## Next

1. Restore `C:` above `10 GB` free before more PDF or batch-artifact work.
2. Resolve `week_runtime_20260427T173913Z`: persist it properly or clear it.
3. Reduce the same-user case to one active paid path across `week` and `premium`.
4. Shrink `route_live_reply()` so symptom prompts stop being fully template-owned.
5. Remove unsupported router details and add clarifying-question behavior for symptom-first replies.
6. Rerun the benchmark and record routed share, duplicate clusters, unsupported-detail failures, and clarifying-question count.
7. Keep `premium_fresh_20260425T214914Z` frozen for delivery until readable labs or manual biomarker text clear the gate.

## Must-Not-Change Rules

- Telegram-first only
- one active paid path per Telegram user at a time
- manual concierge remains the official pilot mode
- human review required before delivery
- no diagnosis or treatment framing
- no unreadable or unconfirmed lab facts
- no invented symptoms or unsupported condition claims
- do not treat a runtime-only session as settled paid-case truth if its submission JSON is missing
- do not present routed template coverage as proof of personalized live-chat quality
- do not spend the next cycle on landing, mini-app, growth channels, pricing debate, or public-launch expansion

## Context For New Model

Stage:

- controlled concierge pilot with same-user state drift, router-overreach quality blockage, lab-gate enforcement pressure, and critical disk headroom risk

Objective:

- restore one coherent paid-path truth for the current same-user case
- stop unsafe premium delivery from unreadable or unconfirmed lab evidence
- make the first Telegram exchange less generic by reducing deterministic router capture
- close one fact-safe, human-reviewed paid cycle without opening new growth drift

Constraints:

- Telegram-first only
- one active paid path per Telegram user
- manual concierge remains official pilot mode
- human review required before delivery
- no diagnosis or treatment framing
- no unreadable or unconfirmed lab facts
- no invented symptoms or unsupported condition claims
- no new growth or UI work until disk headroom, state truth, router scope, and lab gating are fixed

Immediate next actions:

1. Free disk space back above the `10 GB` floor before more PDF or batch-artifact work.
2. Verify whether `week_runtime_20260427T173913Z` should be persisted as the live `week` path or cleared as an orphaned runtime session.
3. Declare exactly one active paid path for the same-user case, then freeze, archive, or merge the others.
4. Cut `route_live_reply()` back to safety/logistics coverage, then rerun the benchmark so symptom prompts can actually test model quality.
5. Do not deliver the current premium PDF; first obtain readable labs or manual biomarker text and regenerate from confirmed facts only.

Reference benchmark:

- `ops/reports/quality_report_20260429T080345Z.md`
- current truth: `20/20` routed, `0/20` model reached, `0/20` clarifying questions
