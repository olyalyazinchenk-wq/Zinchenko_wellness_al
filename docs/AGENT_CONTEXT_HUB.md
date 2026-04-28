# Agent Context Hub

Updated: 2026-04-28 12:16 MSK

## RU Status Snapshot (2026-04-28)

### Что изменилось с прошлого прогона

- В репозитории появился большой пакет обновлений по `WellnessBot/`, `ops/`, `infra/deploy/`, `docs/`, `landing/`, `mini-app/` (функционал и документация заметно расширены).
- Появились/усилились админ-команды, governance-слой, режим ручной оплаты, генерация артефактов (PDF/HTML), эксперименты/решения.
- Выявлены техдолги: треки кодировок (часть RU-доков отображается битой кодировкой), лог-файлы были случайно включены в git, а `git remote` всё ещё не настроен.

### Текущий этап

- Controlled concierge pilot (Telegram-first, без публичного запуска).
- Активен пилотный режим оплаты: `PAYMENT_MODE=manual`.
- Human review обязателен перед выдачей любого клиентского результата.

### Блокеры / стоп-факторы

1. **Единственная активная ветка на пользователя**: требуется свести кейсы `20260425T214914Z_1084557944` и `20260425T212847Z_1084557944` к одному активному delivery-кандидату (второй — архив/фриз).
2. **Lab-gate**: любые артефакты после `requires_lab_resubmission=true` не считаются delivery-safe до получения читаемых анализов / ручных биомаркеров и перегенерации из подтверждённых фактов.
3. **GitHub push**: в репозитории отсутствует настроенный remote (`git remote -v` пусто) — внешняя синхронизация через GitHub заблокирована.
4. **Диск < 10 GB**: на `C:` зафиксировано ~`8.6 GB` свободного места — риск деградации среды/CI/установок.

### Что готово к пилоту (controlled)

- Telegram-интеграция и основной пайплайн: анкета → ручная оплата → AI-черновик → human review → выдача.
- Документы-опоры по продукту/операциям: продуктовая линейка, ручная оплата, runbook/чеклисты (см. `docs/`).

### Что нельзя запускать публично

- Любой public launch / маркетинговое масштабирование.
- Любая выдача досье без human review.
- Любая генерация/доставка по кейсам с неразрешённым `requires_lab_resubmission=true`.

## Stage

- controlled concierge pilot with branch-control pressure and an unsafe-lab artifact branch

## Product Direction

- Telegram-first operating model only
- service ladder:
  - `demo` builds trust
  - `week` is the low-friction entry rail
  - `premium` is the active proof path
  - `vip` stays parked until operator-load evidence exists
- official pilot payment mode: `PAYMENT_MODE=manual`
- human review is mandatory before any client delivery

## Done

- North star fixed in `docs/PROJECT_NORTH_STAR_EXECUTION_PLAN_20260427.md`
- Product ladder fixed in `docs/PRODUCT_LINE_V2_20260426.md`
- Manual concierge payment accepted as the official pilot mode in `docs/MANUAL_PAYMENT_MODE_20260426.md`
- Benchmark baseline still stable in `ops/reports/quality_report_20260421T183148Z.md`:
  - `20` prompts
  - `0` empty replies
- Latest persisted branch truth reviewed:
  - `WellnessBot/data/runtime_state.json` is empty
  - `20260425T214914Z_1084557944` is the freshest branch
  - `20260425T214914Z_1084557944` is not delivery-safe because `requires_lab_resubmission=true`
  - `20260425T212847Z_1084557944` is the cleaner safe-delivery rewrite candidate
- Governance memory still shows loop pressure:
  - `WellnessBot/data/product_governance.json`
  - `115` stored experiments
  - repeated titles still duplicated

## Next

1. Declare `20260425T212847Z_1084557944` the only delivery candidate for user `1084557944`.
2. Freeze `20260425T214914Z_1084557944` as evidence-only until readable labs or manual biomarkers arrive.
3. Rewrite and close or archive `20260425T212847Z_1084557944` from confirmed intake facts only.
4. Run one live Telegram walkthrough for `week`.
5. Run one live Telegram walkthrough for `premium`.
6. Keep exactly one post-delivery experiment candidate:
   - compress premium into a stronger `72h -> 7d -> 30d` structure

## Must-Not-Change Rules

- Do not switch away from Telegram-first execution.
- Do not treat `week` or `vip` as the main proof path; `premium` remains the flagship test.
- Do not let YooKassa or provider-token work block the pilot path while manual payment works.
- Do not allow more than one delivery candidate per Telegram user.
- Do not treat unreadable or unconfirmed labs as facts.
- Do not use the current `20260425T214914Z_1084557944` artifacts as delivery proof.
- Do not deliver any dossier without human review.
- Do not use diagnosis or treatment framing.
- Do not let branded supplement mentions become the core value story.
- Do not spend the next cycle on growth-channel, landing, mini-app, or public-launch expansion.
- Do not seed more governance ideas until fresh delivery evidence exists.

## Latest Validated Evidence

- `docs/PROJECT_NORTH_STAR_EXECUTION_PLAN_20260427.md`
- `docs/PRODUCT_LINE_V2_20260426.md`
- `docs/MANUAL_PAYMENT_MODE_20260426.md`
- `docs/STRATEGY_LIVE_DELTA.md`
- `docs/SPRINT_BOARD_20260413.md`
- `WellnessBot/data/runtime_state.json`
- `WellnessBot/data/submissions/20260425T212847Z_1084557944.json`
- `WellnessBot/data/submissions/20260425T214914Z_1084557944.json`
- `WellnessBot/data/drafts/20260425T212847Z_1084557944.review.json`
- `WellnessBot/data/drafts/20260425T214914Z_1084557944.review.json`
- `WellnessBot/data/product_governance.json`
- `ops/reports/quality_report_20260421T183148Z.md`

## Context For New Model

Stage:

- controlled concierge pilot with one unsafe fresh branch and one safer rewrite candidate

Objective:

- restore one clean delivery candidate
- close one fact-safe human-reviewed premium cycle
- verify `week` and `premium` walkthroughs without opening new product drift

Working truth:

- `runtime_state.json` is empty, so persisted submissions and logs are authoritative
- `20260425T214914Z_1084557944` is freshest but unsafe because generation happened after a lab-resubmission gate
- `20260425T212847Z_1084557944` should be treated as the only delivery candidate if the team wants one safe premium proof now
- `premium` at `6900 RUB` remains the active monetization proof path
- manual concierge payment remains official

Immediate actions:

1. Lock `20260425T212847Z_1084557944` as the only delivery candidate.
2. Freeze `20260425T214914Z_1084557944` as evidence-only until readable labs or manual biomarker text exist.
3. Rewrite `20260425T212847Z_1084557944` from confirmed facts only and make one human review decision: deliver or archive.
4. Run one `week` walkthrough and one `premium` walkthrough.
5. Keep one post-delivery experiment only: stronger `72h -> 7d -> 30d` premium structure.

## What To Read First

1. This file
2. `docs/STRATEGY_LIVE_DELTA.md`
3. `docs/SPRINT_BOARD_20260413.md`
4. `docs/ENGINEERING_MANDATE_20260413.md`
5. `docs/PROJECT_NORTH_STAR_EXECUTION_PLAN_20260427.md`
6. `WellnessBot/data/runtime_state.json`
7. `WellnessBot/data/submissions/20260425T212847Z_1084557944.json`
8. `WellnessBot/data/drafts/20260425T212847Z_1084557944.review.json`
9. `WellnessBot/data/submissions/20260425T214914Z_1084557944.json`
10. `WellnessBot/data/drafts/20260425T214914Z_1084557944.review.json`
11. `WellnessBot/data/product_governance.json`
12. `ops/reports/quality_report_20260421T183148Z.md`
