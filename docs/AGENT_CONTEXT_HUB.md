# Agent Context Hub

Updated: 2026-06-18 14:52 MSK

## ⚠️ ВСЕМ АГЕНТАМ (Codex / Antigravity / Hermes): ЧИТАТЬ ПЕРВЫМ ДЕЛОМ

Эта страница — единственный общий источник правды для всех агентов проекта.
Если документы противоречат друг другу, приоритет у более свежего. Медицинско-юридические ограничения имеют приоритет всегда.

## Unified GitHub Source Of Truth

- Main public handoff document: `docs/PROJECT_DEVELOPMENT_SINGLE_SOURCE_OF_TRUTH.md`
- Свежие изменения кода всегда на GitHub: `olyalyazinchenk-wq/Zinchenko_wellness_al`
- Локальный путь: `C:\Users\HP\Desktop\Новая папка\WellnessBot\`

## Quick Status — 2026-06-18 14:52 MSK

- **Режим:** controlled concierge pilot. Публичный запуск заблокирован.
- **Оплата:** `PAYMENT_MODE=manual`. Перед выдачей клиенту — обязательный human review.
- **Бот РАБОТАЕТ** — PID 15452 подтверждён `2026-06-18 14:46 +03:00`, proxy `http://127.0.0.1:10808`, LLM `deepseek-v4-flash`. Защита от двойного запуска сработала корректно.
- **Последний коммит:** `9c40b5d` — `feat: June 2026 bot upgrades - payment flow, reminders, PDF naming, menu` — запушен `2026-06-18 14:50 +03:00`.
- GitHub: ✅ синхронизировано. Notion: ⏳ требует ручного обновления (MCP недоступен). Google Drive: ❌ заблокировано.

## Что изменилось в боте с 14 по 18 июня 2026

### Платёжный flow
- `check_and_prompt_pending_payment()` — перехватывает **любое** сообщение клиента (текст, фото, документ, кнопку меню) если `intake_status == manual_payment_pending`
- Если клиент ещё не подтвердил → бот шлёт напоминание + inline-кнопка `✅ Подтвердить оплату (я оплатил/а)`
- Если клиент уже нажал → сообщение «оплата на проверке»
- `nurture_engine_loop` (каждые 30 мин) шлёт напоминание об оплате через 15+ минут после создания заявки с той же кнопкой
- `clientconfirmpay_{submission_id}` callback обрабатывается, ставит `client_reported_payment = True`, уведомляет администраторов

### Напоминания (timezone-aware)
- Вода: 11:00, 15:00, 19:00 по местному времени клиента (по городу)
- Сон: 22:00 по местному времени («за час до 23:00»)
- Функция `get_timezone_offset_for_city()` определяет часовой пояс по городу

### PDF и документы
- Обложка досье: динамический заголовок по продукту (например `ДЕФИЦИТ-ЧЕК / КАРТА СИМПТОМОВ`)
- Футер: `OLGA ZINCHENKO · [НАЗВАНИЕ ПРОДУКТА]`
- Имя файла: латинский префикс (например `Deficit_Chek_Karta_Simptomov_12345.pdf`)

### Кураторы
- `notify_admins_habits_log()` — пересылает фото тарелок + текст кураторам
- `handle_admin_reply_to_client()` — reply куратора в telegram копируется клиенту

### Исправления
- Ложный статус «Анкета собрана» до оплаты для быстрых тарифов — исправлен
- `NameError` в `prompts.py` (FORMAT_RULE_CLIENT_NUMBERING) — исправлен

## Нерешённые проблемы (P0 — требуют внимания)

- ❗ `20260531T183007Z_1084557944` — `delivered_to_client` при `judge_verdict = fail_major_issues` → нужен human review и решение
- ❗ Один пользователь держит несколько активных платных рельсов (`nutri_chat` × 3, `habits` × 2) — нужна канонизация
- ❗ Диск `C:` на `~9.98 GiB` (замер 14 июня) — регулярно падает ниже 10 GiB floor

## Ресурсы для агентов

| Файл | Назначение |
|---|---|
| `docs/MODEL_CONTEXT_START_HERE_20260505.md` | Точка входа для любого нового агента |
| `docs/AGENT_CONTEXT_HUB.md` | Этот файл — оперативная правда |
| `docs/PROJECT_PULSE_LOG.md` | Хронологический лог всех изменений |
| `docs/HERMES_PROJECT_WORKER_PROTOCOL_20260505.md` | Протокол работы для Гермеса |
| `docs/hermes_skills/` | Навыки Гермеса |
| `WellnessBot/main.py` | Основной код бота (4593 строки) |
| `WellnessBot/payment_flow.py` | Платёжная логика |
| `WellnessBot/texts.py` | Все тексты бота |

## Внешняя синхронизация — 2026-06-18
- **GitHub: ✅** — `9c40b5d` запушен `2026-06-18 14:50 +03:00`
- **Notion:** ⏳ требует ручного обновления (MCP коннектор недоступен)
- **Google Drive:** ❌ file tools не exposed

## Stage

- Controlled concierge pilot where runtime is process-verified again, but the active parent-child runner chain still needs confirmation, while commercialization control, delivery truth, public-surface truth, disk margin, and connector reliability remain incoherent.

## Done This Cycle

- Re-read the current project state across `docs`, `WellnessBot`, `mini-app`, `landing`, root `index.html`, `ops/reports`, runtime logs, submissions, and working-tree deltas.
- Re-validated `WellnessBot/data/runtime_state.json` and confirmed that the mounted rail is still the June 6 `habits` daily-log path.
- Re-checked `bot.stderr.log` and the current process table, then corrected runtime truth from `not process-verified` to `process-verified but dual-process chain`.
- Re-measured current disk headroom and confirmed that the earlier June 14 recovery was already stale by late afternoon.
- Kept the live QA interpretation anchored to `docs/WELLNESS_DIALOGUE_QA_20260608.md` while keeping the completed benchmark anchor at the May 31 report.
- Confirmed the current surface split: `landing/index.html` remains comparatively safe, root `index.html` still overclaims payment and PDF truth, and `mini-app/index.html` still sells a `1000 RUB` tier with dossier and support promises.
- Attempted live Notion and GitHub connector calls, classified both as blocked because MCP startup still fails before initialization completes, confirmed that Google Drive file tools are still unavailable, and refreshed the required local mirror artifacts.

## Objective

- Recover `C:` above the `10 GiB` floor and rebuild a safer buffer.
- Confirm one intentional supervised runtime chain.
- Keep one canonical paid path per Telegram user.
- Repair the delivered-case contradiction before counting higher-ticket proof as valid.
- Stop same-user same-offer and same-ladder paid-branch multiplication.
- Restore per-prompt QA visibility so model-path failures stop hiding the benchmark state.
- Collapse root and mini-app proof or pricing claims to one truthful story.
- Recover Notion and GitHub connector startup, then enable Google Drive write access.

## Current Truth

- `WellnessBot/data/runtime_state.json` currently uses `user_sessions` plus empty `chat_sessions`:
  - `submission_id = 20260606T202509Z_1084557944`
  - `offer = habits`
  - `tier = habits`
  - `step = habits_daily_log`
  - `payment_status = manual_payment_confirmed`
  - `daily_logs[0].created_at = 2026-06-06T20:25:31Z`
  - `chat_sessions` is currently empty
- The freshest runtime continuity proof is the June 14 reconnect sequence in `bot.stderr.log` at `2026-06-14 00:41:45 -> 00:43:30 +03:00`.
- The freshest startup proof is the June 13 polling start in `bot.stderr.log` at `2026-06-13 16:32:34 -> 16:32:50 +03:00`, and it explicitly logs `proxy=http://127.0.0.1:10808`.
- Current process truth now shows an active `WellnessBot/main.py` chain:
  - parent PID `12300` = `.venv\Scripts\python.exe`
  - child PID `20032` = `Python312\python.exe`
  - both were created on `2026-06-13 16:32:25-16:32:26 +03:00`
  - this is enough to treat runtime as process-verified again, but not enough to assume the topology is intentional
- The same user still holds unresolved current paid state across multiple recent rails:
  - `20260602T055745Z_1084557944` = `nutri_chat`, `manual_payment_confirmed`
  - `20260603T112723Z_1084557944` = `nutri_chat`, `manual_payment_pending`
  - `20260603T113045Z_1084557944` = `habits`, `manual_payment_confirmed`
  - `20260603T121917Z_1084557944` = `nutri_chat`, `manual_payment_confirmed`
  - `20260606T202509Z_1084557944` = `habits`, `manual_payment_confirmed`, and mounted as active runtime state
- `WellnessBot/data/submissions/20260531T183007Z_1084557944.json` still combines:
  - `offer = basic`
  - `intake_status = delivered_to_client`
  - `internal_review.judge_verdict = fail_major_issues`
- Governance debt remains unchanged in the main runtime file:
  - `WellnessBot/data/product_governance.json` still contains `151` experiments and `0` decisions
- Current benchmark truth:
  - latest completed benchmark anchor is still `ops/reports/quality_report_20260531T083403Z.md`
  - current interpretation doc is `docs/WELLNESS_DIALOGUE_QA_20260608.md`
  - the batch run still aborts on prompt `1`
  - the transport clue is stronger because runtime startup explicitly logs a proxy path and the latest polling failure includes `ProxyTimeoutError: Proxy connection timed out: 60`
- Current surface truth:
  - `landing/index.html` remains the comparatively safest public surface
  - root `index.html` still contains YooKassa, guaranteed-PDF, and off-map pricing claims that should not be treated as live proof
  - `mini-app/index.html` still sells a `1000 RUB` `Wellness Clarity` tier and promises PDF dossier output plus Telegram support, so it should not be described as placeholder-only
- Current connector truth:
  - Notion connector startup fails with `failed to get client` and `error sending request for url (https://chatgpt.com/backend-api/wham/apps)`
  - GitHub connector startup fails with the same initialize-time error
  - Google Drive write tools are still unavailable in this session

## Regressions To Fix Now

- Thin disk floor breach; owner `Ops`; next action push `C:` back above the `10 GiB` floor and rebuild a safer headroom buffer.
- Runtime chain ambiguity; owner `Ops + Lead Developer`; next action confirm whether the `.venv` parent plus `Python312` child chain is intentional supervision and collapse to one governed runner if not.
- Explicit proxy dependency; owner `Lead Developer + Ops`; next action decide whether `http://127.0.0.1:10808` is mandatory, add direct-fallback behavior if not, and make startup logging plus transport policy explicit in code.
- Same-user paid-path sprawl; owner `Operator + Lead Developer`; next action declare one canonical current commercial path across the June 2 / June 3 / June 6 stack, then freeze, archive, merge, or refund the non-canonical rails.
- Duplicate same-offer `habits` multiplication; owner `Operator + Lead Developer`; next action choose between `20260603T113045Z_1084557944` and `20260606T202509Z_1084557944` as the canonical `habits` path.
- Delivery-gate breach; owner `Lead Developer + Operator`; next action audit `20260531T183007Z_1084557944`, record whether any manual override existed, and remove or remediate the `delivered_to_client` contradiction if `fail_major_issues` still stands.
- Mini-app monetization overclaim; owner `Product Strategist + Lead Developer`; next action remove or neutralize the `1000 RUB` tier and PDF/support promises or align them to the governed offer map.
- Root-page payment and proof overclaim; owner `Product Strategist + Lead Developer`; next action remove or neutralize the YooKassa, guaranteed-PDF, and off-map pricing claims before using the root page as live proof.
- Benchmark observability and transport ambiguity; owner `Lead Developer`; next action patch `ops/quality_probe.py` for per-prompt capture and make `WellnessBot/ai_drafting.py` explicit about proxy and `trust_env` policy.
- Connector startup regression; owner `Tooling / Access`; next action restore Notion and GitHub connector startup before the next external sync attempt, then expose Google Drive file write tools.

## Next

1. Confirm whether the current `.venv` parent plus `Python312` child `WellnessBot/main.py` chain is intentional.
2. Push `C:` back above the `10 GiB` floor and log the new baseline.
3. Decide whether the local proxy at `127.0.0.1:10808` is required, and add an explicit direct fallback if not.
4. Declare one canonical current commercial path across the June 2 / June 3 / June 6 same-user stack.
5. Add a hard guard so same-user same-offer or same-ladder paid branches cannot be created while older paid state is still active or unresolved.
6. Audit `20260531T183007Z_1084557944` and repair the delivery-gate contradiction.
7. Patch `ops/quality_probe.py` so prompt-level model failures still emit partial artifacts.
8. Patch `WellnessBot/ai_drafting.py` so the `openai_compatible` transport path stops inheriting a fragile proxy route by accident.
9. Restore Notion and GitHub connector startup, then replay the local sync payloads externally.
10. Enable Google Drive file discovery/create/upload/share permissions.
11. Re-run the batch benchmark only after steps `3`, `7`, and `8`.
12. Remove root-page YooKassa, guaranteed-PDF, and off-map pricing claims.
13. Remove or neutralize the mini-app `1000 RUB` tier plus PDF/support promises until the live ladder is explicitly approved.

## Must-Not-Change Rules

- Telegram-first only.
- Manual concierge remains the official pilot mode.
- No price ladder becomes product truth until one approved map is written across code, docs, and artifacts.
- One canonical paid path per Telegram user at a time.
- No second paid branch for the same offer or same ladder and same user while an older paid path is still active or unresolved.
- Human review is required before delivery.
- No diagnosis or treatment framing.
- No unsafe supplement instructions without confirmed context and review.
- No hardcoded medical-style results on public or TMA surfaces.
- Do not describe the mini-app as placeholder-only while price, PDF, or support promises remain live in the file.
- Do not count a paid path as healthy if payment succeeded but the final reviewed artifact is contradicted by failing review state.
- Do not treat governance backlog growth as execution progress.
- Do not mark Notion or GitHub sync as healthy until a real connector call succeeds in the current session.
- Do not describe the bot as currently live from a stale lockfile or historical reconnect log without a current process check.
- Do not assume the active two-process `WellnessBot/main.py` chain is healthy until it is confirmed as intentional supervision.

## Context For New Model

Stage:

- Controlled Telegram concierge pilot where runtime is process-verified again, but the supervision topology is not yet confirmed, while commercialization control, delivery truth, public-surface truth, disk margin, and connector reliability remain incoherent.

Objective:

- Recover disk headroom above the floor and rebuild a safer margin.
- Confirm one intentional supervised runtime chain.
- Collapse the current same-user paid stack to one canonical path.
- Repair the delivered-case contradiction.
- Restore benchmark observability.
- Align public surfaces to the approved Telegram-first manual-review model while keeping runtime stable.
- Recover Notion and GitHub connector startup so outward sync can resume, then enable Google Drive write access.

Constraints:

- Telegram-first only.
- `PAYMENT_MODE=manual`.
- Human review remains mandatory.
- One canonical commercial path per Telegram user.
- Text-only intake remains the only proven live modality.
- Disk free space is `10717425664` bytes (`~9.98 GiB`) at `2026-06-14 16:32:26 +03:00`, which means the floor is narrowly breached again.
- Latest completed benchmark is `ops/reports/quality_report_20260531T083403Z.md`.
- Current QA synthesis doc is `docs/WELLNESS_DIALOGUE_QA_20260608.md`.
- The batch benchmark still fails on prompt `1`.
- Notion connector startup fails during MCP initialize with `failed to get client` and `error sending request for url (https://chatgpt.com/backend-api/wham/apps)`.
- GitHub connector startup fails with the same initialize-time error.
- Google Drive file discovery/create/upload/share tools are unavailable in the current Codex session.
- The process table now shows a live parent-child `WellnessBot/main.py` chain, but the supervision model is not yet confirmed as intentional.

Immediate next actions:

1. Confirm whether the current supervision chain is intentional.
2. Recover disk above the floor again.
3. Decide whether the local proxy at `127.0.0.1:10808` is required, and add a direct fallback if not.
4. Canonicalize the June 2 / June 3 / June 6 same-user paid stack.
5. Add a duplicate paid-path guard for same-user same-offer and same-ladder re-entry.
6. Repair the delivered-case review contradiction.
7. Neutralize mini-app and root-page overclaims.
8. Patch partial-artifact QA capture and explicit transport behavior.
9. Restore Notion and GitHub connector startup, then enable Google Drive write access.

Reference proof anchors:

- runtime proof: `bot.stderr.log`
- process truth: current `Win32_Process` parent-child chain for `WellnessBot/main.py`
- benchmark reference: `ops/reports/quality_report_20260531T083403Z.md`
- current QA interpretation: `docs/WELLNESS_DIALOGUE_QA_20260608.md`
