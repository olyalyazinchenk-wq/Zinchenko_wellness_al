# Agent Context Hub

Updated: 2026-06-18 14:49 MSK

## Unified GitHub Source Of Truth

- Main public handoff document: `docs/PROJECT_DEVELOPMENT_SINGLE_SOURCE_OF_TRUTH.md`
- Use the local hub files for live operating truth and `docs/external_sync/*.md` as sanitized replay payloads for external contributors.

## Quick Status

- Mode: controlled concierge pilot. Public launch remains blocked.
- Payment mode: `PAYMENT_MODE=manual`. Human review is required before delivery.
- **Bot is LIVE** — process PID 15452 confirmed running at `2026-06-18 14:46 +03:00` with proxy `http://127.0.0.1:10808`, LLM `deepseek-v4-flash`. Lock-file guard prevented duplicate start correctly.
- **Latest commit pushed to GitHub**: `9c40b5d` at `2026-06-18 14:50 +03:00` — `feat: June 2026 bot upgrades - payment flow, reminders, PDF naming, menu`
- **Key features shipped in this commit** (Гермес, читай внимательно):
  - `check_and_prompt_pending_payment()` — перехват любых сообщений клиента если `intake_status == manual_payment_pending`; бот отвечает напоминанием + inline-кнопка «✅ Подтвердить оплату»
  - `nurture_engine_loop` — автоматически отправляет напоминание об оплате через 15+ минут после создания заявки, тоже с кнопкой подтверждения
  - Timezone-aware напоминания: вода 11/15/19ч, сон 22ч по местному времени клиента (на основе города)
  - Динамические имена PDF-файлов и заголовки досье по продукту (обложка + футер)
  - Пересылка фото тарелок / отчётов по привычкам кураторам
  - Обработчик ответов кураторов клиентам (reply-to forwarding)
  - Исправлен ложный статус «Анкета собрана» до оплаты для мгновенных тарифов
  - Исправлен `NameError` в `prompts.py`
- Latest hard breach (не устранён): `20260531T183007Z_1084557944` — `delivered_to_client` при `judge_verdict = fail_major_issues`. Требует human review и решения.
- Current disk state: последнее измерение `~9.98 GiB` свободно (14 июня). Не проверялось после этого.
- Latest completed benchmark anchor: `ops/reports/quality_report_20260531T083403Z.md`.
- Current benchmark interpretation doc: `docs/WELLNESS_DIALOGUE_QA_20260608.md`.
- External sync status:
  - **GitHub: ✅ СИНХРОНИЗИРОВАНО** — `9c40b5d` запушен `2026-06-18 14:50 +03:00`
  - Notion: требует ручного обновления (MCP коннектор недоступен в текущей сессии)
  - Google Drive: инструменты не exposed

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
