# Agent Context Hub

Updated: 2026-10-30 12:51 MSK

## Снимок синхронизации - 2026-10-30 12:51 MSK (Задачи A7–A8 и Спринт B B1–B6 завершены)

- **Этап**: `nutriok-controlled-build-2026-07-17-r1` (не меняется до Спринта E включительно); `PAYMENT_MODE=manual`, `ENABLE_TMA=false`, public launch заблокирован.
- **A7–A8**: выполнен бэкфилл безопасных прежних релизов через `ops/backfill_legacy_releases.py` (3 из 8 открыты по `legacy_release` + SHA-256; 5 исключены на ревью Ольге); в `ops/bot-stop.ps1` настроена точная остановка только `WellnessBot\main.py` и его дочерних процессов без убийства сторонних `.venv\Scripts\python.exe`.
- **Спринт B (B1–B6)**:
  - `WellnessBot/intake_schema.py`: `DiaryDay`, `AdherenceEntry`, `NutriOKIntake` (`to_dict`, `from_dict`, `validation_errors()`), метрики по 5 целям.
  - `WellnessBot/handlers/nutriok_intake.py`: нативный диалог анкеты НутриОК в Telegram (`nutriok_router` перед legacy-хендлерами), прогресс-бар `● ● ● ○ ○ ○ ○  Шаг 3 из 7`, `/continue`, короткий поток `ok_start` и 7/8-шаговый платный поток с поддержкой текста, голоса (STT) и фото в 3-дневном дневнике.
  - `WellnessBot/review_gate.py`: `ReviewRecord`, `record_review`, `release_or_raise(submission) -> Path` во всех точках отправки PDF клиенту, 3 кнопки ревью для Ольги («Одобрить», «Нужны правки» с комментарием, «Отклонить»), fail-closed дефолт `_resolve_submission_product_code -> "ok_review"` и сверка `approved_artifact_sha256` в legacy-ветке `approved_by_admin_id` (**B6**).
  - `WellnessBot/nutriok_safety.py`: словоформы regex (`ё→е`) и окно до 4 слов в любом порядке (`_within_words`) для чёрного стула, крови в стуле/рвоте, кофейной гущи, необъяснимой потери веса, желтухи, длительной температуры, отёка лица/губ/горла, РПП, суицидальных маркеров, высокорисковых лекарств (`awaiting_safety_review`), беременности/ГВ + БАД и возраста `< 18`, с защитой от ложных срабатываний на анализы крови/кала и завершённое ГВ (**B5**).
- **Тесты и ревью**: `93 passed, 58 subtests passed` (`ops/dev.ps1 test`), `compileall` без ошибок, независимое ревью второго агента `LGTM`.

## Снимок синхронизации - 2026-10-30 04:05 MSK (Спринт A завершён)

- **Этап**: `nutriok-controlled-build-2026-07-17-r1`; controlled concierge pilot, `PAYMENT_MODE=manual`, `ENABLE_TMA=false`, public launch заблокирован.
- **Безопасность (A1–A2)**: закрыт IDOR в `getpdf_` и `get_user_approved_reports`; удалена клиентская запись `supplement_review_*`; добавлен `WellnessBot/review_gate.py` (`is_release_approved`, SHA-256 сверка артефакта, запись `approved_by_admin_id` и `auto_delivery_decision`); добавлен `tests/test_report_access.py` (6 тестов).
- **Конфигурация и Runtime (A3–A4)**: `.env` и `WellnessBot/.env` переведены на `PAYMENT_MODE=manual`, `ENABLE_TMA=false`. `ops/agent-sync-status.ps1` и `ops/dev.ps1` считают `BotOwnerCount=1` (`BotProcessCount=2`, пара venv launcher + child). Scheduled Task `WellnessBot` перезапущена (`2026-10-30 04:02:37 MSK`, `Run polling for bot @zinchenko_wellness_ai_1_bot`).
- **Гигиена и публикация (A5–A6)**: добавлен `.gitattributes`, обновлён `.gitignore`, legacy-скрипты корня перенесены в `ops/archive/root_legacy/`. Все 69 тестов (`pytest` / `unittest`) и `compileall` зелёные; проверенная дельта разбита на 6 атомарных коммитов и опубликована в `origin/master`.

## Снимок синхронизации - 2026-10-30 03:20 MSK

- **Этап**: `nutriok-controlled-build-2026-07-17-r1`; controlled concierge pilot, `PAYMENT_MODE=manual`, public launch заблокирован.
- **Runtime truth**: Scheduled Task `WellnessBot` = `Running`, активных процессов `2` (venv parent + child); свежийhandled-update proof подтверждён, polling для `@zinchenko_wellness_ai_1_bot` активен.
- **VPN / Connectivity**: локальный прокси Xray на `127.0.0.1:10808` активен, `https://api.telegram.org` отвечает `HTTP 200 OK`.
- **Ops truth**: на `C:` свободно **71.25 GB** (выше floor `10 GiB`), блокер свободного места закрыт.
- **Проверки**: `pytest tests -v` — 63 теста пройдены; `compileall` пройден. Создан CLI `ops/dev.ps1`.
- **Консолидация проекта**: проект упорядочен в единую папку. Внешние материалы перенесены в `materials/`, скрипты настройки серверов и VPN — в `ops/infra/digitalocean_vpn/`, на Рабочем столе создан Junction `Кето-Баланс (NutriOK)`.
- **Git truth**: `master`, `HEAD=origin/master=c9fe781`. Tracked dirty files содержат reviewed NutriOK-слой; секреты и локальные артефакты изолированы в `.gitignore`.
- **Мультиагентный контур**: Hermes, Codex и Antigravity используют единый канонический workspace `C:\Users\HP\Desktop\Новая папка`.

## Снимок синхронизации - 2026-07-26 12:00 MSK

- Этап не менялся: `nutriok-controlled-build-2026-07-17-r1`; режим остаётся controlled concierge pilot, `PAYMENT_MODE=manual`, public launch заблокирован.
- Прочитаны обязательные coordination-файлы и целевые документы по стратегии, продуктовой линейке, ручной оплате, аудиту и skill registry; проверены `docs`, `WellnessBot`, `ops`, `tests`, `landing`, `mini-app`.
- Git truth: `master`, `HEAD=origin/master=a9f0734`; `git ls-remote --heads origin` успешен. Рабочее дерево содержит 24 tracked-изменения и untracked runtime/virtual-environment/infrastructure/secret-like артефакты; полная публикация запрещена.
- Проверки: `py -3.12 -m unittest discover -s tests -v` — 63 теста пройдены; `py -3.12 -m compileall WellnessBot tests` — успешно.
- Runtime truth: Scheduled Task `WellnessBot` = `Ready`, активных процессов `0`; последний запуск `2026-07-22 22:27:27`, `LastTaskResult=1`. Свежего handled-update proof нет; polling не запускался.
- Ops truth: на `C:` свободно `187547648` байт (около `179 MiB`), критически ниже floor `10 GiB`; удаление файлов не выполнялось.
- Внешний sync: GitHub remote доступен, но mixed tree не коммитится; Notion connector/tools в этой сессии недоступны, создан локальный fallback-отчёт в `docs/external_sync/`.

### Текущая готовность и блокеры

- К пилоту готово только: обезличенные controlled concierge кейсы, ручная оплата, безопасная `ОК-Экспресс` при safety gate и обязательном именованном human review.
- Публично запускать нельзя: public traffic/ads, автоматическую оплату, unattended delivery, полные tiers или supplement details без approval, второй polling-процесс и mixed-tree публикацию.
- P0: восстановить диск выше `10 GiB`; разделить reviewed source и локальные артефакты; восстановить Telegram connectivity и получить свежий single-owner runtime proof; закрепить structured intake/reviewer evidence; провести два прогона 20-case benchmark.
## Снимок синхронизации - 2026-07-19 02:18 MSK

- Stage не менялся: `nutriok-controlled-build-2026-07-17-r1`; controlled build / concierge pilot; public launch заблокирован.
- Продуктовая линия остаётся `НутриОК by Olga Kovaleva`: одна цель, baseline/metric, трёхдневный дневник и безопасный следующий шаг без диагностики.
- Проверки в этом запуске: `py -3.12 -m unittest discover -s tests -v` — 63 теста пройдены; `py -3.12 -m compileall WellnessBot tests` — успешно.
- Repo truth: `master`, `HEAD=origin/master=a9f0734`; remote `origin` доступен; `TrackedDirtyFiles=24`, `Synchronized=False`.
- Dirty tree смешанный: изменения в `WellnessBot`, `tests`, docs и public surfaces соседствуют с untracked `.venv_wsl`, логами, lock-файлом, VPN/SSH-скриптами и `do_api_token.txt`; blind commit/push запрещён.
- Runtime truth: Windows Scheduled Task `WellnessBot` = `Running`; sync-check видит 2 процесса `WellnessBot/main.py` (один дочерний), поэтому чистое подтверждение единственного polling owner не получено; второй процесс требует операторской проверки.
- Runtime proof stale: последние строки `bot.stderr` с handled updates — `2026-06-07 13:59:57 +03:00`; свежего proof-of-life в текущем запуске нет.
- Ops truth: на `C:` свободно `2016206848` байт (`~1.88 GiB`), ниже floor `10 GiB`.
- Внешняя синхронизация: GitHub remote читается, но публикация отложена из-за смешанного дерева; Notion будет обновлён только обезличенным статусом.

### Текущие блокеры

1. Разделить reviewed source changes и локальные/секретные/runtime-артефакты до любого commit/push.
2. Разобраться с двумя процессами и получить один чистый scheduled-task runtime proof; polling вручную не запускать.
3. Поднять свободное место C: выше 10 GiB операторской очисткой.
4. Довести structured intake, persisted reviewer evidence и 20-case benchmark (два прохода).

## Снимок синхронизации - 2026-07-18 16:45 MSK

- Stage: `nutriok-controlled-build-2026-07-17-r1`; controlled build / concierge pilot; public launch remains blocked.
- Product direction is stable: `НутриОК by Olga Kovaleva`, one primary goal plus baseline/metric/three-day diary, safe next-step clarity instead of diagnosis.
- Verification in this session: `py -3.12 -m unittest discover -s tests -v` passed with 63 tests; `py -3.12 -m compileall WellnessBot tests` passed.
- Repo truth: `master`, `HEAD=origin/master=a9f0734`, `Published=True`, `TrackedDirtyFiles=22`, `Synchronized=False`.
- Runtime truth: scheduled task `WellnessBot` is `Ready`, active bot processes `0`; fresh proof-of-life is still missing and no second poller was started.
- Ops truth: `C:` free space is `3171799040` bytes (`~2.95 GiB`), below the `10 GiB` floor and worse than the earlier same-day snapshot.
- Benchmark truth: latest completed report is still `ops/reports/quality_report_20260531T083403Z.md`; latest QA synthesis is still `docs/WELLNESS_DIALOGUE_QA_20260608.md`.
- Mixed-tree truth remains active: reviewed NutriOK product work sits alongside local secrets, logs, lockfiles, `.venv_wsl`, and other non-publishable artifacts.

### Done

- Re-read the required startup docs and re-ran the shared sync-status check in the canonical workspace.
- Re-verified the governing NutriOK product contract and the current working-tree markers for ladder, menu, safety gate, and tests.
- Re-ran the current test suite and Python compilation successfully in this session.
- Re-measured runtime, git-sync, benchmark-reference, and storage facts for the strategy layer.

### Next

1. Persist goal, baseline, metric, adherence, and three-day diary end to end.
2. Persist reviewer identity, decision, timestamp, and approved artifact for full tiers and supplement details.
3. Build the 20-case NutriOK fixture pack and complete two benchmark passes.
4. Capture one fresh scheduled-task runtime proof without starting a second poller.
5. Recover `C:` above `10 GiB` and split publishable source files from local debris.
6. Write RF retention, deletion, encryption, access, and audit controls.

### Must-Not-Change Rules

- Telegram-first only.
- Manual payment only.
- Only one Telegram polling owner is allowed: the Windows scheduled task `WellnessBot`.
- Do not start a second poller from Codex, Hermes, WSL, or a terminal.
- Do not reopen diagnosis, treatment, medication-change, or guaranteed-result framing.
- `ОК-Разбор`, `ОК-Результат 8`, `ОК-Ритм`, and every supplement detail require Olga approval.
- Do not count strategy refresh, copy polish, or offer expansion as progress while intake persistence, reviewer persistence, runtime proof, and benchmark proof are missing.
- Do not publish the current mixed working tree as a single source snapshot.

## Current Governing Snapshot - 2026-07-18

- Stage: `nutriok-controlled-build-2026-07-17-r1`; public launch remains blocked.
- Canonical product: `НутриОК by Olga Kovaleva`; promise: `Разбор, после которого понятно, что делать`.
- Canonical ladder: `ОК-Старт`; `ОК-Экспресс 990 RUB pilot`; `ОК-Разбор 5,900 RUB pilot`; `ОК-Результат 8 14,900 RUB pilot`; `ОК-Ритм 1,990 RUB/month`.
- Current monetization truth: manual payment only; safe `ОК-Экспресс` is the only automatic paid output; full tiers and supplement details remain Olga-reviewed.
- Fresh verification in this session: 63 tests passed; Python compilation passed.
- Shared repo state: `master`, `HEAD=origin/master=a9f0734`, `Published=True`, `TrackedDirtyFiles=22`, `Synchronized=False`.
- Scheduled task `WellnessBot` is `Ready`, process count is `0`, and no second poller was started.
- Latest completed benchmark remains `ops/reports/quality_report_20260531T083403Z.md`.
- Latest QA interpretation remains `docs/WELLNESS_DIALOGUE_QA_20260608.md`.
- Disk is `3171799040` bytes free (`~2.95 GiB`), below the `10 GiB` floor.
- The dirty tree still mixes publishable NutriOK work with local runtime and secret-bearing artifacts.

## Plan Delta - 2026-07-18

1. Persist the structured intake contract end to end.
2. Persist the reviewer evidence invariant.
3. Build 20 de-identified NutriOK fixtures and complete two current-product benchmark runs.
4. Restore fresh scheduled-task runtime proof.
5. Recover disk above `10 GiB`.
6. Split reviewed product files from secrets and runtime debris.
7. Write RF cloud privacy/storage/audit controls.

## Strategy Delta - 2026-07-18

- Keep NutriOK controlled build as the governing direction; do not pivot again.
- The next differentiator is not a new offer; it is a technically enforceable controlled paid cycle.
- Strategy should now optimize for release-readiness artifacts: persisted intake, persisted reviewer evidence, benchmark proof, runtime proof, and publishable source separation.

## Context For New Model - 2026-07-18

### Stage

NutriOK controlled build; runtime not freshly proven; public launch blocked.

### Objective

Release one safe, measurable, reviewer-governed NutriOK cycle that turns a chosen goal and three days of evidence into a concrete next-step plan.

### Constraints

- one scheduled-task poller only;
- manual payment only;
- no diagnosis, treatment, medication changes, or guaranteed results;
- Olga approval for full tiers and supplement details;
- current-product benchmark still missing;
- disk remains below floor;
- source tree remains mixed and unpublished.

### Immediate Next Actions

1. Persist structured intake.
2. Persist reviewer evidence.
3. Build and run the 20-case benchmark twice.
4. Capture fresh runtime proof.
5. Recover disk and split the dirty tree.
6. Write RF data controls.
## Снимок синхронизации - 2026-07-18 02:18 MSK

- Stage: nutriok-controlled-build-2026-07-17-r1; режим controlled build / concierge pilot, публичный запуск заблокирован.
- Оплата: PAYMENT_MODE=manual; перед выдачей полного результата human review обязателен.
- Проверка: py -3.12 -m unittest discover -s tests -v — 63 теста пройдены; compileall пройден.
- Репозиторий: ветка master, HEAD=origin/master=bd58da9; рабочее дерево не синхронизировано (TrackedDirtyFiles=24).
- Remote GitHub доступен через git ls-remote; GitHub connector видит olyalyazinchenk-wq/Zinchenko_wellness_al. Публикация смешанной дельты не выполнялась.
- В рабочем дереве есть крупная смешанная кодовая и документационная дельта, а также untracked-артефакты, включая потенциально секретный do_api_token.txt, VPN/SSH-скрипты, .venv_wsl, логи и lock-файл. Ничего из этого не индексируется.
- Notion connector доступен; найден последний статусный лист «Статус проекта NutriOK — 2026-07-17 06:12 MSK». Безопасный executive status записан отдельной страницей.
- Runtime: scheduled task WellnessBot имеет состояние Ready, процессов 0; Telegram polling не запускался, свежий proof-of-life отсутствует.
- Диск: свободно 4,158,668,800 байт (~3.87 GiB), ниже порога 10 GiB.

### Готово к ограниченному пилоту

- NutriOK-каталог, ручная оплата, безопасный автоматический Express-output и review-gate покрыты текущими 63 тестами.
- Допустимы только обезличенные контролируемые кейсы с ручной проверкой; готовность live-пилота не подтверждена до свежего runtime proof и ревью рабочей дельты.

### Нельзя запускать публично

- Полные уровни, красные флаги, supplement-детали и медицинские формулировки без именной approval-записи.
- Публичный трафик, реклама, автоматическая YooKassa/Telegram-оплата и второй polling-процесс.
- Любая публикация текущего смешанного дерева целиком; потенциальные секреты и runtime-данные должны оставаться вне Git.

### Следующие шаги

1. Разделить и проревьюировать кодовую дельту; опубликовать только намеренные безопасные файлы.
2. Довести structured intake и persisted named approval до end-to-end.
3. Восстановить один polling owner через Windows Scheduled Task и собрать свежий proof-of-life.
4. Собрать 20 обезличенных NutriOK fixtures, пройти два benchmark-прогона и освободить диск выше 10 GiB.
5. Описать RF cloud privacy/storage и audit controls до расширения пилота.



## Снимок синхронизации - 2026-07-17 06:12 MSK

- Stage: nutriok-controlled-build-2026-07-17-r1; controlled build/concierge pilot, public launch заблокирован.
- Оплата: PAYMENT_MODE=manual; human review перед выдачей полного результата обязателен.
- Проверка: py -3.12 -m unittest discover -s tests -v — 63 теста пройдены.
- Репозиторий: master, HEAD и origin/master совпадают на bd58da9; рабочее дерево не синхронизировано (TrackedDirtyFiles=24).
- Публикация не выполнялась: дерево смешивает неревьюенные изменения WellnessBot, тестов, docs и public surfaces, а также потенциально секретные untracked-файлы и runtime-артефакты.
- GitHub: чтение remote заблокировано сетевой ошибкой через 127.0.0.1:443; локальный fallback-отчёт создан.
- Notion: connector доступен; статус будет записан отдельной страницей без секретов и клиентских данных.
- Runtime: Telegram polling не запускался; live task/process в текущей проверке недоступен, поэтому готовность бота к пилоту не подтверждается.
- Ops-риск: свободное место на C: около 4.31 GiB, ниже порога 10 GiB.

### Готово к ограниченному пилоту

- NutriOK-каталог, ручная оплата, безопасный автоматический Express-output и review-gate покрыты текущими тестами.
- К пилоту допустимы только обезличенные контролируемые кейсы с ручной проверкой; полноценный live-запуск не подтверждён.

### Нельзя запускать публично

- Полные уровни, красные флаги, supplement-детали и неподтверждённые медицинские формулировки без именной approval-записи.
- Публичный трафик, реклама, автоматическая YooKassa/Telegram-оплата и второй polling-процесс.

### Следующие шаги

1. Разделить и проревьюировать текущую кодовую дельту перед публикацией.
2. Довести structured intake и persisted named approval до end-to-end.
3. Восстановить один polling owner через Windows Scheduled Task и собрать свежий proof-of-life.
4. Собрать 20 обезличенных NutriOK fixtures, пройти два benchmark-прогона и освободить диск выше 10 GiB.

## Current Governing Snapshot - 2026-07-17

- Stage: nutriok-controlled-build-2026-07-17-r1; public launch remains blocked.
- Canonical product: НутриОК by Olga Kovaleva; promise: Разбор, после которого понятно, что делать.
- Canonical ladder: ОК-Старт; ОК-Экспресс 990 RUB pilot; ОК-Разбор 5,900 RUB pilot; ОК-Результат 8 14,900 RUB pilot; ОК-Ритм 1,990 RUB/month.
- HMS/Osipov is an optional input in a full assessment, not a standalone product, diagnosis, or causal source.
- Working-tree implementation adds the canonical catalog, legacy migration, NutriOK prompt, deterministic delivery gate, aligned Telegram menu/public surfaces, and tests.
- Full tiers, red flags, unsafe claims, and supplement offers cannot use automatic delivery. Safe ОК-Экспресс is the only automated paid output.
- Scheduled task WellnessBot is Ready, process count is 0, and no second poller was started.
- Payment remains manual. RF cloud privacy/storage and production audit controls are not implemented.
- Live Telegram intake does not yet persist primary goal, baseline, three-day diary, goal metric, and adherence end to end.
- Latest completed benchmark remains ops/reports/quality_report_20260531T083403Z.md and predates NutriOK.
- Unit verification: 63 tests passed; Python compilation passed.
- GitHub master is at bd58da9 after publishing and reading back sanitized status/context artifacts. Local implementation changes remain unpublished, so full synchronization is false.
- Notion run note and Context Hub were written and verified by exact page readback.
- Google Drive profile is Ольга Ковалева <olyalya.zinchenk@gmail.com>; sanitized snapshot upload/share succeeded and file content was verified by fetch.
- Obsidian mirror run note is local at docs/obsidian_mirror/RUN_NOTE_20260717_0027_MSK.md.
- Disk is 4628213760 bytes free (~4.31 GiB), below the 10 GiB floor.
- Demand remains unvalidated: previous 47 submissions represented only two unique Telegram users.

## Plan Delta - 2026-07-17

1. Persist the structured assessment contract: one goal, baseline 0-10, three-day diary, goal metric, adherence, symptoms, lifestyle, medications, allergies, and relevant labs.
2. Persist Olga's reviewer identity, decision, timestamp, and approved artifact before every full-tier release.
3. Build 20 de-identified NutriOK fixtures and pass two consecutive benchmark runs with zero critical defects.
4. Restore Telegram connectivity only through the Windows scheduled task and prove one polling owner.
5. Recover disk above 10 GiB before replay-heavy QA.
6. Specify RF-hosted retention, deletion, encryption, access, and audit controls.
7. Recruit five external interviews, then run the 20-buyer Express pilot without ads.
8. Publish the implementation only after the dirty working tree is split into reviewed, intentional changes.

## Strategy Delta - 2026-07-17

- Sell measurable clarity and an accountable next-step process, not an automated diagnosis, giant PDF, or supplement list.
- One primary goal and three days of evidence are the core unit of value.
- AI structures evidence; Olga owns full-tier conclusions and every supplement detail.
- The ladder is approved, but scale is gated: 20 Express buyers, at least 8 Full upgrades, at least 4 eight-week upgrades.
- Previous payment is credited fully for upgrades within 30 days.
- Supplements are optional, never commission-ranked, and require disclosure plus Olga approval.
- No paid advertising before runtime, privacy, reviewer, payment, and benchmark gates pass.

## Context For New Model - 2026-07-17

### Stage

NutriOK controlled build; bot down; public launch blocked.

### Objective

Release a differentiated full nutrition assessment that turns one chosen goal and three days of evidence into a safe, measurable action plan, with Olga accountable for every full-tier result.

### Constraints

- one Windows scheduled-task polling owner;
- manual payment;
- no diagnosis, treatment, medication changes, or guaranteed results;
- full tiers and supplement details require Olga approval;
- structured intake is not end-to-end yet;
- latest benchmark predates NutriOK;
- disk remains below floor;
- local implementation remains unpublished.

### Immediate Next Actions

1. Persist structured intake and reviewer evidence.
2. Build and run the 20-fixture NutriOK benchmark twice.
3. Restore scheduled-task connectivity without a second poller.
4. Recover disk above 10 GiB.
5. Define RF cloud data controls.
6. Recruit five external interviews and prepare the controlled pilot.
## Historical Snapshot - 2026-06-21

Updated: 2026-06-21 16:40 MSK

## ВСЕМ АГЕНТАМ (Codex / Antigravity / Hermes): ЧИТАТЬ ПЕРВЫМ

Эта страница — единый текущий onboarding-hub для всех агентов проекта.
Если документы расходятся, приоритет у более свежего подтвержденного артефакта.
Медицинско-юридические ограничения и правило одного polling owner имеют приоритет всегда.

## Unified GitHub Source Of Truth

- Main public handoff document: `docs/PROJECT_DEVELOPMENT_SINGLE_SOURCE_OF_TRUTH.md`
- Live repo: `olyalyazinchenk-wq/Zinchenko_wellness_al`
- Canonical branch: `master`
- Local repo head in this refresh: `2968cdb`
- `origin/master` matched local `HEAD` at the start of this refresh.
- Local workspace: `C:\Users\HP\Desktop\Новая папка`

## Unified Agent Runtime

- Shared stage marker: `docs/CURRENT_STAGE.json`
- Shared bootstrap: root `AGENTS.md`
- Shared verification: `ops/agent-sync-status.ps1`
- Codex and Antigravity must use the Windows canonical workspace above.
- Hermes must use `/mnt/c/Users/HP/Desktop/Новая папка` and must not run the legacy `/home/hermes/projects/nutrition_bot` polling process.
- The only permitted Telegram polling owner remains the Windows scheduled task `WellnessBot`.

## Quick Status

- Mode: controlled concierge pilot. Public launch remains blocked.
- Payment mode: `PAYMENT_MODE=manual`. Human review remains required before delivery.
- Shared sync is still unhealthy:
  - the current `ops/agent-sync-status.ps1` run still reports `TrackedDirtyFiles = 19`, `BotTaskState = Running`, `BotProcessCount = 2`, `Published = True`, `Synchronized = False`
- Runtime continuity is fresher than the earlier same-day hub claimed:
  - `bot.stderr.log` now shows handled updates at `2026-06-21 08:36:49 +03:00`, `08:36:51 +03:00`, `08:36:54 +03:00`, `08:36:56 +03:00`, `08:36:58 +03:00`, and `08:37:00 +03:00`
- `WellnessBot/data/runtime_state.json` is no longer empty:
  - last write time is `2026-06-21 08:37:00 +03:00`
  - mounted runtime state is `submission_id = 20260621T053653Z_1084557944`, `offer = osipov`, `step = osipov_context`, `payment_status = manual_payment_confirmed`
  - `chat_sessions` is still empty even though `user_sessions` is not
- Freshest persisted same-user escalation is now a new `osipov` re-entry:
  - `20260621T053653Z_1084557944` = `osipov`, `5900 RUB`, `manual_payment_confirmed`
  - this happens after the earlier delivered `osipov` and delivered `gut_support_18` rails that still lack review artifacts
- Direct-delivery review-trail regression is still live:
  - `WellnessBot/data/drafts/20260618T192846Z_1084557944.review.json` does not exist
  - `WellnessBot/data/drafts/20260619T215149Z_1084557944.review.json` does not exist
- Legacy P0 contradiction remains open:
  - `20260531T183007Z_1084557944` is still `delivered_to_client` while `internal_review.judge_verdict = fail_major_issues`
- Disk state: `C:` free space is `5226946560` bytes (`~4.87 GiB`) at `2026-06-21 16:40:06 +03:00`
- Benchmark anchor: `ops/reports/quality_report_20260531T083403Z.md`
- QA interpretation anchor: `docs/WELLNESS_DIALOGUE_QA_20260608.md`

## Current Truth

### Runtime
- The scheduled-task-owned parent-child Python chain is still alive, so the bot is not down.
- The freshest runtime continuity proof is now the June 21 `08:36:49 -> 08:37:00 +03:00` handled-update sequence.
- The latest runtime story is `process-verified and actively handling updates, but still not single-owner healthy`.
- The runtime-state story is no longer `empty`, but it is still not coherent enough to trust:
  - `user_sessions` mounts a live `osipov` case
  - `chat_sessions` is empty
  - polling ownership is still not proven single-instance healthy

### Same-User Commercial-State Conflict
- One Telegram user still spans unresolved current state across all of these rails:
  - `20260531T183007Z_1084557944` = `basic`, delivered despite failed review
  - `20260618T121906Z_1084557944` = `nutri_chat`, `1490 RUB`
  - `20260618T214036Z_1084557944` = second `nutri_chat`, `1490 RUB`
  - `20260618T192846Z_1084557944` = delivered `osipov`, `5900 RUB`, `adult_confirmed = false`
  - `20260619T215149Z_1084557944` = delivered `gut_support_18`, `6000 RUB`, sourced from the delivered `osipov`
  - `20260621T053653Z_1084557944` = fresh `osipov`, `5900 RUB`, manual-payment-confirmed and now mounted in runtime state
- Explicit canonical ownership is still missing across this stack.
- The new June 21 `osipov` rail means same-user commercialization control got worse, not better.

### Delivery Truth
- Legacy P0 contradiction remains open:
  - `20260531T183007Z_1084557944`
  - `offer = basic`
  - `payment_status = paid`
  - `intake_status = delivered_to_client`
  - `internal_review.judge_verdict = fail_major_issues`
- June 18-21 specialist chain truth:
  - `20260618T192846Z_1084557944` delivered `osipov` with `direct_delivery = true`, `adult_confirmed = false`, and no persisted review artifact
  - `20260619T215149Z_1084557944` delivered `gut_support_18` with `direct_delivery = true`, `adult_confirmed = true`, `source_submission_id = 20260618T192846Z_1084557944`, and no persisted review artifact
  - `20260621T053653Z_1084557944` opens a fresh `osipov` rail before the older specialist rails were review-cleared or canonically owned
- Do not count the specialist rails as healthy pilot proof until review evidence is persisted or explicitly overridden and one canonical path is written.

### Benchmark And Governance
- Latest completed benchmark reference remains `ops/reports/quality_report_20260531T083403Z.md`.
- Current QA synthesis doc remains `docs/WELLNESS_DIALOGUE_QA_20260608.md`.
- Full batch still aborts on prompt `1`.
- `WellnessBot/data/product_governance.json` still holds `151` experiments and `0` decisions.
- Repeated experiment titles still cluster at `12`, `11`, `8`, `8`, and `5`, so loop compression is still a live requirement.

### Working-Tree Truth
- Current tracked code changes still materially alter product behavior:
  - new `gut_support_18` offer, payment mapping, prompt, and text
  - adult-only gating helper `is_adult_age`
  - expanded `osipov` upload / OCR / delivery flow
  - post-`osipov` upsell button into `gut_support_18`
  - supplement-catalog curation and tests now encode verified SPZ03 candidates plus a heartburn exclusion
- This remains active product-direction drift until it is governed and published or rolled back.

### Public Surface Truth
- `landing/index.html` remains the comparatively safest surface, but it still names `Premium Wellness Dossier` and Telegram follow-up support.
- Root `index.html` still overclaims live payment, YooKassa, PDF, dossier, and off-map pricing truth.
- `mini-app/index.html` still overclaims dossier, PDF, expert support, and a live `1 000 ₽` entry rail.

## Plan Delta

1. Restore single polling ownership first.
2. Decide whether the non-empty `user_sessions` plus empty `chat_sessions` split is expected `osipov` behavior or a persistence regression.
3. Persist review evidence or named manual-override proof for every direct-delivery specialist rail.
4. Audit and canonicalize the May 31 / June 18 / June 19 / June 21 same-user stack.
5. Decide whether `gut_support_18` is approved pilot truth or rollback-required drift.
6. Recover `C:` above the `10 GiB` floor.
7. Only count external sync as healthy after a real connector write and exact target readback in the current session.

## Strategy Delta

- Strategy is now `use the June 21 08:37 handled updates as the freshest runtime continuity proof while treating same-user specialist re-entry, polling ownership, runtime-state coherence, direct-delivery review evidence, and disk headroom as the real blockers`.
- The main execution-credibility gap is now:
  - duplicate polling ownership is not proven fixed
  - runtime state is refilled but still structurally incomplete
  - the same user reopened `osipov` before older specialist rails were governed
  - delivered specialist rails still lack review evidence
  - disk remains below floor
  - ungoverned `gut_support_18` expansion is still live in dirty code
  - root and mini-app still overclaim

## Loop Risk

- Re-reading and refreshing sync docs while the same user can still reopen specialist rails is low-impact churn.
- Adding experiments to a `151`-item governance file with `0` decisions is low-impact churn.
- Polishing public-surface copy before same-user case ownership and review truth are governed is low-impact churn.

## Higher-Impact Replacement Action

1. Stop the competing poller and capture one clean runtime artifact newer than `2026-06-21 08:37:00 +03:00`.
2. Block same-user specialist re-entry until `canonical_path` or `case_relation` exists across the old and new specialist rails.
3. Enforce `direct_delivery => persisted review artifact or named manual override`.
4. Feature-gate or roll back `gut_support_18` until the approved ladder is explicit.
5. Then neutralize landing/root/mini-app overclaims and return to benchmark transport work.

## Must-Not-Change Rules

- Telegram-first only.
- Manual concierge remains the official pilot mode.
- Only one Telegram polling owner is allowed.
- No price ladder becomes product truth until one approved map is written across code, docs, and artifacts.
- One canonical paid path per Telegram user at a time.
- No second paid branch for the same offer or same ladder and same user while an older paid path is still active or unresolved.
- No new specialist re-entry for the same user while older specialist rails lack review evidence or canonical ownership.
- `gut_support_18` must not be treated as approved pilot truth until source linkage, adult gating, supplement-safety governance, and review evidence are explicit.
- Human review is required before delivery.
- `direct_delivery` cannot count as healthy proof without a persisted review artifact or explicit named manual override.
- No diagnosis or treatment framing.
- No unsafe supplement instructions without confirmed context and review.
- No hardcoded medical-style results on public or TMA surfaces.
- Do not describe the mini-app as placeholder-only while price, PDF, or support promises remain live in the file.
- Do not count a paid path as healthy if payment succeeded but review truth is missing, failing, or contradicted by commercialization drift.
- Do not treat governance backlog growth or temp-cleanup megabytes as execution progress.
- Do not add new experiment churn while delivery truth and canonical-path control are still unresolved.
- Do not mark external sync as healthy until a real connector write succeeds and the exact target is re-read in the current session.

## Context For New Model

### Stage
- Controlled Telegram concierge pilot with fresh handled updates through `2026-06-21 08:37 +03:00`, a newly mounted `osipov` runtime rail, unresolved same-user specialist duplication, missing review evidence on delivered specialist rails, and disk still below floor.

### Done
- Re-read the shared coordination docs and the target strategy docs in the canonical workspace.
- Reconfirmed the same parent-child bot chain and the still-dirty shared workspace.
- Corrected the stale claim that `runtime_state.json` is empty.
- Confirmed a fresh same-user `osipov` re-entry at `20260621T053653Z_1084557944`.
- Reconfirmed the legacy delivered-case contradiction, missing specialist review artifacts, public-surface overclaims, and repeated experiment-loop pressure.

### Next
1. Stop duplicate polling.
2. Explain or repair the `user_sessions` without `chat_sessions` split.
3. Persist review evidence or manual override proof for direct deliveries.
4. Canonicalize the paid stack and block duplicate paid branches.
5. Decide whether `gut_support_18` is approved or rollback-required.
6. Reduce landing/root/mini-app overclaims.
7. Restore disk.

### Constraints
- Telegram-first only.
- `PAYMENT_MODE=manual`.
- Human review remains mandatory before delivery.
- One canonical paid path per Telegram user.
- Latest completed benchmark remains `ops/reports/quality_report_20260531T083403Z.md`.
- Current QA interpretation remains `docs/WELLNESS_DIALOGUE_QA_20260608.md`.
- The full benchmark still fails on prompt `1`.
- `C:` free space is `5226946560` bytes (`~4.87 GiB`) at `2026-06-21 16:40:06 +03:00`.
- Outward sync only counts as complete after target readback.






## 2026-07-21 02:17 MSK - Regular GitHub/Notion Synchronization

- Stage remains `nutriok-controlled-build-2026-07-17-r1`; operating mode remains controlled concierge pilot, `PAYMENT_MODE=manual`, and public launch is blocked.
- Fresh checks: `master` is at `a9f0734` and matches `origin/master`; GitHub read access via `git ls-remote` succeeded.
- The worktree is not synchronized: 24 tracked files are dirty and there are untracked virtual-environment, runtime, infrastructure, and secret-like artifacts. No sensitive files are eligible for publication.
- `ops/agent-sync-status.ps1` reports `BotTaskState=Running`, `BotProcessCount=2`, `Published=True`, `Synchronized=False`; no polling process was started by this run.
- Verification passed: 63 unit tests and Python compilation for `WellnessBot`/`tests`.
- Storage risk worsened: `C:` has `1,455,128,576` bytes free (about `1.36 GiB`), below the `10 GiB` floor. Cleanup requires operator review; no deletion was performed.
- Notion/GitHub publication of the mixed tree is deferred until an explicit allowlist separates intentional source/docs changes from secrets, logs, locks, uploads, and local tooling.

### Current pilot readiness

- Ready only for a limited de-identified concierge pilot with manual payment and mandatory named human review.
- Not ready for public launch, automated payment, unattended delivery, broad traffic, or a second polling process.
- Immediate priorities: establish single-owner runtime truth, persist structured intake and reviewer evidence, build/run the 20-case NutriOK benchmark twice, recover disk headroom, and publish only a reviewed allowlist.
## 2026-07-22 02:18 MSK - Regular GitHub/Notion Synchronization

- Stage remains `nutriok-controlled-build-2026-07-17-r1`; operating mode remains controlled concierge pilot, `PAYMENT_MODE=manual`, and public launch is blocked.
- `master` and `origin/master` still point to `a9f0734`; GitHub remote and connector are reachable.
- The worktree remains mixed: 24 tracked files are dirty, with additional local runtime, virtual-environment, infrastructure, and secret-like artifacts. This run did not start polling, delete files, or publish the mixed tree.
- `ops/agent-sync-status.ps1` reports `BotTaskState=Running`, `BotProcessCount=2`, `Published=True`, `Synchronized=False`; the single-owner runtime issue remains unresolved.
- Latest local runtime evidence is from 2026-07-20, with fresh submissions/drafts present; it was not copied to external systems and its client data remains local.
- Verification passed: 63 unit tests and Python compilation for `WellnessBot`/`tests`.
- Storage risk worsened: `C:` has `1,526,071,296` bytes free (about `1.42 GiB`), below the `10 GiB` floor. Cleanup requires operator review; no deletion was performed.
- Notion status sync is available; GitHub publication is limited to the reviewed status-doc allowlist. Full source synchronization remains deferred.

### Current pilot readiness

- Ready only for a limited de-identified concierge pilot with manual payment and mandatory named human review.
- Not ready for public launch, automated payment, unattended delivery, broad traffic, or a second polling process.
- Immediate priorities: reconcile the duplicate polling ownership, persist structured intake and reviewer evidence, build/run the 20-case NutriOK benchmark twice, recover disk headroom, and publish only reviewed intentional source changes.
## Снимок синхронизации - 2026-08-30 02:17 MSK

- Этап: `nutriok-controlled-build-2026-07-17-r1`; controlled concierge pilot, `PAYMENT_MODE=manual`, public launch заблокирован, human review обязателен.
- Git: `master` и `origin/master` совпадают на `c9fe781`; mixed tree не публиковался: 24 tracked-изменения плюс untracked virtualenv, runtime/lock/log, инфраструктурные и secret-like артефакты.
- Проверки: 63 unittest и `compileall WellnessBot tests` прошли. `git diff --check` показывает whitespace/EOF замечания в неревьюенных изменениях.
- Runtime: `agent-sync-status` сообщает `BotTaskState=Running`, `BotProcessCount=2`, `Synchronized=False`; единственный polling owner не подтверждён, polling не запускался.
- C: свободно `10723606528` байт, около `9.99 GiB`, чуть ниже floor `10 GiB`; удаления не выполнялись.
- Notion: обезличенная status page создана в текущем запуске. GitHub commit/push mixed tree отложены.

### Готовность и P0

- К пилоту готово только: ограниченные обезличенные concierge-кейсы, ручная оплата, безопасная Express-ветка при safety gate и обязательном именованном human review.
- Публично запускать нельзя: public traffic/ads, автоматическую оплату, unattended delivery, полные tiers или supplement details без approval, второй polling-процесс и смешанное дерево.
- P0: разобраться с двумя процессами; разделить reviewed source и чувствительные артефакты; закрепить intake/reviewer evidence; провести два 20-case benchmark; вернуть C: выше 10 GiB.

## 2026-10-15 15:09 MSK - Regular GitHub/Notion Synchronization

- Stage unchanged: `nutriok-controlled-build-2026-07-17-r1`; controlled concierge pilot, `PAYMENT_MODE=manual`, public launch blocked, human review mandatory.
- Fresh repo truth: `master=origin/master=c9fe781`; `ops/agent-sync-status.ps1` reports `Published=True`, `TrackedDirtyFiles=24`, `BotTaskState=Ready`, `BotProcessCount=0`, `LegacyHermesPolling=False`, `Synchronized=False`.
- Verification passed: 63 unit tests and `py -3.12 -m compileall WellnessBot tests`.
- Worktree is unsafe for whole-tree publication: tracked changes span WellnessBot, docs, tests, root/landing/mini-app; untracked `.venv_wsl`, lock/log files, token-like scripts, uploads/runtime artifacts, and other local debris are present. No secrets, client data, uploads, or runtime artifacts were staged.
- Storage is a P0 operational blocker: `C:` has `2,490,368` bytes free at `2026-10-15 15:09 +03:00`, far below the `10 GiB` floor. No cleanup or deletion was performed.
- Pilot readiness: only limited de-identified concierge cases with manual payment and named human review. Do not launch public traffic, automated payment, unattended delivery, broad traffic, or a second polling process.
- Next actions: operator-reviewed disk recovery; split a reviewed publication allowlist; prove one scheduled-task runtime owner after network readiness; persist structured intake and reviewer evidence; run two current NutriOK benchmark passes; keep public surfaces aligned with pilot truth.
