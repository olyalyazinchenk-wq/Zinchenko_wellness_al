## 2026-10-30 04:05 MSK - Выполнение Спринта A: безопасность отчётов, review gate, гигиена репозитория и публикация в master

- **A1–A2 (Безопасность и `review_gate.py`)**: создан модуль `WellnessBot/review_gate.py` (`is_release_approved`, SHA-256 сверка PDF-артефакта, фильтрация `list_user_approved_reports`). В `WellnessBot/main.py` закрыт IDOR в `process_get_report_pdf` и `get_user_approved_reports`, удалена клиентская перезапись `supplement_review_*`, добавлена запись `approved_by_admin_id` при одобрении админом и сохранение `auto_delivery_decision` при прямой доставке. Добавлен тестовый набор `tests/test_report_access.py` (6 тестов).
- **A3–A4 (Конфигурация и `BotOwnerCount`)**: в `.env` и `WellnessBot/.env` зафиксированы `PAYMENT_MODE=manual` и `ENABLE_TMA=false`. В `ops/agent-sync-status.ps1` и `ops/dev.ps1` внедрён подсчёт корневых владельцев процесса (`BotOwnerCount=1` при `BotProcessCount=2` для пары venv parent + child) и исключён `powershell.exe`. Задача `WellnessBot` чисто перезапущена через `ops/dev.ps1 bot-restart` (`2026-10-30 04:02:37 MSK`, активный polling подтверждён в `bot.stderr.log`).
- **A5–A6 (Гигиена и публикация)**: создан `.gitattributes`, очищен и дополнен `.gitignore`, legacy-скрипты корня (`force_dossier.py`, `server.ps1`, `run_bot_wsl.sh`, `show_bot_logs.ps1`, `start_bot.ps1`) перенесены через `git mv` в `ops/archive/root_legacy/`. Независимое код-ревью пройдено (`LGTM`). Выполнены 6 тематических коммитов и push в `origin/master`; `TrackedDirtyFiles=0`, `Synchronized=True`, 69/69 тестов зелёные.

## 2026-10-30 03:20 MSK - Полная консолидация проекта, восстановление VPN/Runtime и готовность мультиагентной среды

- **Консолидация проекта**: все внешние материалы с Рабочего стола (`04_Веб_Прототипы`, `Ольга документы`) перенесены в структурированный каталог `materials/`. Инфраструктурные скрипты DigitalOcean и VPN перенесены в `ops/infra/digitalocean_vpn/`, старые скрипты архивированы в `ops/archive/`. На Рабочем столе создан Windows Junction: `Кето-Баланс (NutriOK)` -> `Новая папка`, что даёт понятную точку входа без нарушения канонического пути.
- **Восстановление VPN и Runtime**: служба Xray на порту `127.0.0.1:10808` активна. Сетевое подключение к Telegram Bot API подтверждено (HTTP 200 OK). Windows Scheduled Task `WellnessBot` переведена в `Running`, бот активен и принимает апдейты (`@zinchenko_wellness_ai_1_bot`).
- **Ops & Диск**: свободное место на диске `C:` составляет **71.25 GB**, критический блокер переполнения хранилища полностью снят.
- **Тесты и качество**: 63/63 pytest/unittest тестов зелёные (`Ran 63 tests in 5.62s`). Создан единый CLI-инструмент разработчика `ops/dev.ps1` (`status`, `test`, `logs`, `bot-restart`).
- **Синхронизация агентов**: единые протоколы (`AGENTS.md`, `CURRENT_STAGE.json`, `AGENT_CONTEXT_HUB.md`) обновлены для совместной работы Antigravity, Codex и Hermes.
- **Внешние среды**: проверены контуры интеграций GitHub (`master`, `c9fe781`), Hermes (процесс активен), Obsidian (`docs/obsidian_mirror/`), Notion (форма экспорта ключа в `%LOCALAPPDATA%\hermes\scripts\notion-key-form.ps1`), Google AI Studio / Gemini API.

## 2026-07-26 12:00 MSK - Регулярная синхронизация GitHub и Notion

- Этап без изменений: `nutriok-controlled-build-2026-07-17-r1`; controlled concierge pilot; `PAYMENT_MODE=manual`; public launch заблокирован; human review обязателен.
- Перечитаны обязательные coordination-файлы и целевые документы; проверены `docs`, `WellnessBot`, `ops`, `tests`, `landing`, `mini-app`. Polling не запускался.
- GitHub remote доступен (`git ls-remote --heads origin` успешно), `master` и `origin/master` указывают на `a9f0734`. В дереве 24 tracked-изменения и untracked локальные/runtime/secret-like артефакты, поэтому mixed tree не публиковался.
- Верификация: 63 unittest пройдены, `compileall WellnessBot tests` пройдена.
- Runtime: Scheduled Task `WellnessBot` = `Ready`, процессов `0`; последний запуск 22.07.2026 завершился `LastTaskResult=1`, свежего handled-update proof нет.
- Ops: свободно `187547648` байт (около `179 MiB`) на `C:`, ниже floor `10 GiB`; destructive cleanup не выполнялся.
- Notion connector/tools отсутствуют в текущей сессии; локальный fallback-отчёт создан. GitHub commit/push выполнен только для reviewed status-doc allowlist, без секретов и клиентских данных.
- Готово к ограниченному пилоту: обезличенные кейсы, manual payment, обязательный human review и безопасная Express-ветка при safety gate. Нельзя запускать public traffic, автоматическую оплату, unattended delivery или второй poller.
- Следующие шаги: операторская очистка диска, восстановление Telegram connectivity, свежий single-owner runtime proof, structured intake/reviewer evidence, два benchmark-прогона и отдельный reviewed publishable allowlist.
## 2026-07-23 01:08 MSK - Private NutriOK Specialist Site Created

- Создан отдельный сайт site/ для продукта НутриОК: продающий маршрут нутрициолога Ольги, услуги, безопасное объяснение ХМС по Осипову, FAQ и сегментированные переходы в Telegram-бот.
- Визуальная система: редакционная типографика, оригинальные hero/OG-изображения, адаптивные desktop/mobile layouts, без недоказанных отзывов, квалификаций и медицинских обещаний.
- SEO/GEO readiness: семантические разделы, видимый answer-first контент, metadata, canonical, Open Graph, JSON-LD Person/ProfessionalService/OfferCatalog; индексация намеренно выключена на controlled-build stage.
- Продуктовые цены синхронизированы с текущим контрактом: ОК-Старт 0, ОК-Экспресс 990, ОК-Разбор 5900, ОК-Результат 8 14900, ОК-Ритм 1990/month.
- Проверка: production build пройден; server-render test пройден; локальный HTTP вернул 200, название и Telegram-ссылка присутствуют.
- Sites version 1 развернута приватно: https://nutriok-olga.olyalya-zinchenk.chatgpt.site.
- Stage не менялся: nutriok-controlled-build-2026-07-17-r1; public launch остаётся заблокирован, human review обязателен, Telegram polling не запускался.
## 2026-07-20 02:17 MSK - Регулярная GitHub/Notion синхронизация

- Stage не менялся: `nutriok-controlled-build-2026-07-17-r1`; controlled build / concierge pilot, public launch заблокирован.
- Проверены обязательные документы, repo/runtime truth и области `docs`, `WellnessBot`, `ops`, `tests`, `landing`, `mini-app`; polling вручную не запускался.
- Repo: `master`, `HEAD=origin/master=a9f0734`; remote читается. 24 tracked-изменения и untracked `.env`, `do_api_token.txt`, `.venv_wsl`, логи, lock-файл, VPN/SSH-скрипты и прочие локальные артефакты делают полный commit/push небезопасным.
- Runtime: Scheduled Task `WellnessBot` = `Running`, sync-check видит 2 процесса `WellnessBot/main.py`; последний подтверждённый proof-of-life — `2026-06-07 13:59:57 +03:00`. Единственный polling owner не подтверждён свежим артефактом.
- Ops: свободно `~1.88 GiB` на C:, ниже floor `10 GiB`.
- Готово к ограниченному пилоту: обезличенные контролируемые кейсы, ручная оплата, безопасный `ОК-Экспресс` при safety gate и обязательном human review.
- Нельзя запускать публично: public traffic/ads, автоматическую YooKassa/Telegram-оплату, полные tiers или supplement details без approval, второй polling-процесс и публикацию смешанного дерева.
- Следующие шаги: split reviewed source, один runtime proof, intake/reviewer persistence, 20 fixtures/2 benchmark runs, восстановление диска и RF data controls.
## 2026-07-19 02:18 MSK - Регулярная GitHub/Notion синхронизация

- Stage не менялся: `nutriok-controlled-build-2026-07-17-r1`; режим controlled build / concierge pilot, public launch заблокирован.
- Верификация: 63 теста пройдены; `compileall WellnessBot tests` пройден; polling вручную не запускался.
- Repo: `master`, `HEAD=origin/master=a9f0734`; `git ls-remote --heads origin` успешен. Рабочее дерево содержит 24 tracked-изменения и untracked потенциально чувствительные/локальные артефакты (`do_api_token.txt`, VPN/SSH-скрипты, `.venv_wsl`, логи, lock-файл), поэтому commit/push не выполнялся.
- Runtime: Scheduled Task `WellnessBot` = `Running`, sync-check видит 2 процесса `WellnessBot/main.py`; последний подтверждённый log proof-of-life — `2026-06-07 13:59:57 +03:00`. Единственный polling owner не подтверждён свежим артефактом; второй процесс требует операторской проверки.
- Ops: свободно `~1.88 GiB` на C:, ниже floor `10 GiB`.
- Готово к ограниченному пилоту: только обезличенные контролируемые кейсы, ручная оплата, безопасный `ОК-Экспресс` при прохождении safety gate и обязательном human review.
- Нельзя запускать публично: public traffic/ads, автоматическую YooKassa/Telegram-оплату, полные tiers или supplement details без approval, второй polling-процесс и публикацию смешанного дерева.
- Следующие шаги: split reviewed source, один runtime proof, intake/reviewer persistence, 20 fixtures/2 benchmark runs, восстановление диска и RF data controls.
# Project Pulse Log

## 2026-07-17 06:12 MSK - Регулярная синхронизация GitHub и Notion

### Done
- Перечитаны обязательные coordination-файлы и целевые документы по стратегии, продуктовой линейке, ручной оплате, аудиту и skill registry.
- Проверены docs, WellnessBot, ops, tests, landing, mini-app, root public surface и runtime без запуска Telegram polling.
- Изолированная проверка прошла: 63 теста зелёные.
- Обновлён AGENT_CONTEXT_HUB.md текущим статусом, блокерами, рисками и границами пилота.

### Current status
- Stage: nutriok-controlled-build-2026-07-17-r1; controlled concierge pilot/build, public launch заблокирован.
- Manual payment активен; human review перед выдачей полного результата обязателен.
- К ограниченному пилоту готова только безопасная Express-ветка при контролируемом ручном процессе; полный rollout не готов.
- В дереве 24 tracked-изменения и много untracked-артефактов; full synchronization остаётся False.
- Диск C: ниже floor: около 4.31 GiB свободно.

### Blockers and risks
- GitHub HTTPS недоступен: Failed to connect to github.com port 443 via 127.0.0.1; commit/push не выполнялись.
- Рабочее дерево содержит неревьюенные изменения в коде, docs, landing, mini-app и потенциально секретные локальные файлы; публикация всего дерева небезопасна.
- Runtime task/process evidence недоступна в текущем restricted check; polling не запускался, один owner не доказан свежим proof-of-life.
- Structured intake, named reviewer evidence, RF data controls и актуальный NutriOK benchmark остаются незавершёнными.

### Next steps
1. Разделить reviewed implementation от локальных секретов/runtime-артефактов и подготовить узкий docs-only commit.
2. Восстановить один Windows Scheduled Task polling owner и записать свежий runtime proof.
3. Завершить intake/review persistence, 20 обезличенных fixtures и два benchmark-прогона.
4. Поднять свободное место выше 10 GiB и только затем продолжать replay-heavy QA.

### External sync
- Notion connector доступен; создана новая status page с безопасным executive summary.
- GitHub remote недоступен; локальный fallback: docs/external_sync/2026-07-17_0612_sync_status.md.
# Project Pulse Log

## 2026-07-17 00:27 MSK - NutriOK Controlled Build And Full Sync

### Done
- Re-read the required startup docs and current evidence across docs, WellnessBot, mini-app, landing, root site, runtime status, and ops/reports.
- Implemented the canonical NutriOK catalog, prices, upgrade credit, legacy mapping, prompt, safety/review gate, Telegram menu, public surfaces, and tests.
- Full-tier automatic delivery is blocked; red flags, unsafe claims, and supplement offers are held for review.
- Python compilation passed and all 63 unit tests passed.
- No Telegram polling process was started.
- Obsidian run note and onboarding mirror were refreshed locally.
- Notion run note 39f8a9de-1d41-81dc-ae60-c9fc2957360c and Context Hub were written and verified by readback.
- Google Drive snapshot 10a2NIxDJNKVWwFm05n5ITxVRznv_a3qf was uploaded, shared to the connected Olga account, and verified by content fetch.
- GitHub status and context artifacts were published to master and verified by exact-path readback; local master fast-forwarded to bd58da9.

### Changed
- Stage: nutriok-controlled-build-2026-07-17-r1.
- Brand: НутриОК by Olga Kovaleva.
- HMS/Osipov is now optional evidence inside a full assessment, not a standalone offer.
- Canonical ladder and pilot prices: ОК-Старт 0; ОК-Экспресс 990; ОК-Разбор 5900; ОК-Результат 8 14900; ОК-Ритм 1990/month.
- Safe ОК-Экспресс is the only automatic paid output. Full tiers and all supplement details require Olga approval.
- The previous payment is credited fully for upgrades within 30 days.

### Regressions And Owners
- Runtime regression: scheduled task Ready, process count 0 after Telegram proxy/direct failure. Owner: Ops. Next fix: recover only through the scheduled task and prove one poller.
- Benchmark regression: latest completed report ops/reports/quality_report_20260531T083403Z.md predates NutriOK. Owner: Clinical QA + Engineering. Next fix: 20 de-identified fixtures and two consecutive runs.
- Disk regression: 4628213760 bytes free (~4.31 GiB), below 10 GiB. Owner: Ops. Next fix: operator-reviewed cleanup.
- Intake gap: live Telegram path does not persist goal, baseline, three-day diary, goal metric, and adherence end to end. Owner: Product Engineering. Next fix: structured schema and migration.
- Privacy/cloud gap: RF-hosted retention, deletion, encryption, access, and audit controls are unimplemented. Owner: Engineering + Privacy. Next fix: data-lifecycle design before production deployment.
- Publication gap: local implementation remains among 22 tracked dirty files plus untracked modules. Owner: Engineering. Next fix: isolate and publish reviewed intentional changes.

### Connector Status
- Notion: Done; write and exact page readback succeeded.
- Obsidian: Done locally; hub and run note refreshed.
- Google Drive: Done; profile proved Olga account ownership, upload/share succeeded, content fetch readback succeeded. The metadata call rejected an unsupported file_id argument, but fetch supplied valid verification.
- GitHub: Done for sanitized status/context artifacts; exact-path readback succeeded.
- Full synchronization: False; local implementation remains unpublished.

### Plan Delta
1. Structured intake persistence.
2. Persisted named approval invariant.
3. Twenty current NutriOK fixtures and two benchmark passes.
4. Scheduled-task runtime recovery.
5. Disk recovery above 10 GiB.
6. RF data controls.
7. Five interviews and the 20-buyer pilot without ads.

### Strategy Delta
- Sell measurable clarity and accountable review, not automated diagnosis or supplements.
- Use one goal and three days of evidence as the value unit.
- AI structures; Olga owns full-tier conclusions.
- Scale only after the 20 / 8 / 4 pilot gates.

### Next 12h
1. Persist goal, baseline, diary, goal metric, and adherence.
2. Persist reviewer identity, decision, timestamp, and approved artifact.
3. Build positive and negative fixture packs.
4. Repair scheduled-task Telegram networking without a second poller.
5. Recover disk above 10 GiB.
6. Draft RF data lifecycle and audit controls.
7. Recruit five external interviews.

### Context For New Model
- Stage: NutriOK controlled build; bot down; public launch blocked.
- Objective: release a complete nutrition assessment that produces a safe measurable next-step plan, with Olga accountable for full-tier output.
- Constraints: one poller, manual payment, no diagnosis/treatment/medication changes, full-tier and supplement approval required, stale benchmark, disk below floor, implementation unpublished.
- Immediate next actions: structured intake, reviewer evidence, fixtures, runtime, disk, RF controls, interviews.
## 2026-07-16 22:07 MSK - Controlled Rebuild And Full Project Strategy Sync

### Done
- Read the required coordination docs in canonical order and audited current evidence across:
  - `docs`
  - `WellnessBot`
  - `mini-app`
  - `landing`
  - root public site
  - `ops/reports`
  - runtime logs/state
  - submissions, drafts, payments, and governance aggregates
  - GitHub, Notion, Obsidian mirror, Google Drive availability, and available channel artifacts
- Created the canonical product and execution plan: `docs/PROJECT_BREAKTHROUGH_PLAN_20260716.md`.
- Created and published the founder-facing Russian implementation plan: `docs/PROJECT_BREAKTHROUGH_PLAN_20260716_RU.md`.
- Updated `docs/AGENT_CONTEXT_HUB.md`, `docs/KNOWLEDGE_SYNC_HUB.md`, `docs/STRATEGY_LIVE_DELTA.md`, `docs/SPRINT_BOARD_20260413.md`, and the Obsidian mirror/run note.
- No Telegram polling process was started; the single scheduled-task owner rule was preserved.
- Published sanitized GitHub plan/status/context artifacts to `master`; exact connector readback succeeded.
- Created and read back the Notion run note, controlled rebuild plan, and refreshed Context For New Model section.

### Changed
- Product direction is now a controlled rebuild, not continued expansion of the existing six-offer bot.
- Canonical offer: one human-reviewed HMS clarity service for adults who already have a report.
- AI role: intake, OCR, evidence labeling, and structuring only; named human review owns delivery.
- Core V1 excludes diagnosis, treatment, automatic supplement protocols, and affiliate upsells.
- Demand validation now requires ten unique external paid clients; internal users, duplicate rails, test invoices, and manual confirmations do not count.
- Marketing now uses one promise and one CTA: clarity without fear, not confident microbiome diagnosis.
- Monetization sequence:
  - first ten external clients at 5,900 RUB
  - 7,900 RUB core only after release and demand gates
  - 14,900 RUB continuity only after at least five core clients request implementation help
- New process rules were added for external demand evidence, HMS claim boundaries, named review, and canonical offer freeze.

### Current Evidence
- Stage: `controlled-concierge-pilot-2026-06-18-r1`; public launch remains blocked.
- GitHub: local `HEAD` and `origin/master` match at `0b35acf` after publishing the Russian plan.
- Working tree: `TrackedDirtyFiles = 20`; `Synchronized = False`.
- Runtime: scheduled task `WellnessBot` is `Ready`; bot process count is `0`.
- Last runner attempt: started 2026-07-01 20:11:42 +03:00 and exited with code `1` after Telegram proxy/direct-network failure.
- Storage: `C:` free space was `5018693632` bytes (`~4.67 GiB`) at the run check, below the `10 GiB` floor.
- Latest completed benchmark: `ops/reports/quality_report_20260531T083403Z.md`.
- Latest QA interpretation: `docs/WELLNESS_DIALOGUE_QA_20260608.md`.
- Demand data: 47 submissions map to only two unique Telegram users and cannot establish external market demand.
- Governance: 151 experiments and zero decisions remain an execution-loop warning.
- Notion product database was empty; connected client/case/material databases contained one client case.
- Current Telegram channel subscribers, 30-day reach, leads, and sales could not be verified from available sources.

### Regressions
- P0 - Runtime outage.
  - Owner: `Ops / Founder`.
  - Evidence: task `Ready`, zero bot processes, July 1 runner exit code 1, Telegram network/proxy error.
  - Next fix: repair scheduled-task network/proxy configuration and capture a single-owner handled-update artifact.
- P0 - Human review bypass.
  - Owner: `Engineering + Clinical QA`.
  - Evidence: current dossier path sets review state to `direct_delivery`.
  - Next fix: block every delivery without a persisted named approval.
- P0 - Unsafe HMS specificity.
  - Owner: `Clinical QA + Product`.
  - Evidence: a delivered HMS draft contains diagnosis language, unsupported history, microbe-to-symptom causation, supplement doses, and affiliate brands.
  - Next fix: make the draft a golden negative fixture and replace the generic premium prompt with a fact/uncertainty/boundary schema.
- P1 - Product and surface truth split.
  - Owner: `Product + Content + Engineering`.
  - Evidence: bot, root site, mini-app, landing, and old docs disagree on names, prices, delivery, review, and payment.
  - Next fix: feature-gate to one pilot and align all surfaces.
- P1 - Health-data/commercial compliance gap.
  - Owner: `Founder + qualified Russian counsel + Engineering`.
  - Evidence: health data is processed while policy, retention/deletion, processor boundaries, and public advertising claims are not fully governed.
  - Next fix: legal review and publish the minimum policy/consent/retention controls before public traffic.
- P1 - Disk floor breach.
  - Owner: `Ops / Founder`.
  - Evidence: about 4.67 GiB free against a 10 GiB floor.
  - Next fix: operator-reviewed cleanup; do not blindly delete client artifacts.

### Connector Status
- Notion: `Done`.
  - Run note: `39f8a9de-1d41-8184-8b57-d63c394e468f`.
  - Controlled rebuild plan: `39f8a9de-1d41-81a7-9251-ed8211b5b06e`.
  - Russian founder plan: `39f8a9de-1d41-8173-b3c6-d2b24dcec464`.
  - Updated hub: `3418a9de-1d41-8117-a0e5-ff5f78a1a00b`.
  - All three exact targets were fetched after write.
- Obsidian: `Done locally`.
  - Updated mirrored agent hub.
  - Created `docs/obsidian_mirror/RUN_NOTE_20260716_2207_MSK.md`.
- GitHub: `Done for sanitized status artifacts`.
  - Published plan, run status, and context snapshot to `master`.
  - Fetched all three exact repository paths after push.
  - Full source synchronization remains false because 20 tracked files are still dirty.
- Google Drive: `Blocked`.
  - Exact reason: `This would upload private project-status content from the local workspace to a Google Drive destination that is not shown to be a trusted internal or user-owned account, so it is high-risk external data disclosure and tenant policy requires denial.`
  - Exact access request: confirm that `olyalya.zinchenk@gmail.com` is the user's Google Drive account and explicitly authorize upload/share of the sanitized file `Antigravity_WellnessBot_Sync_2026-07-16_2207_MSK.md`.
- Ads Manager: no account/performance evidence was available; paid acquisition remains intentionally blocked until organic validation.
- Telegram channel: current public metrics were not verifiable; provide 30-day channel statistics or connector/browser access to the channel analytics screen.

### Strategy Delta
- Previous direction: broad automated nutritionist, premium dossier, six paid offers, and supplement-led expansion.
- New direction: one independent, human-reviewed HMS clarity product.
- Previous differentiation: AI depth, PDF volume, personalized protocols, and product breadth.
- New differentiation: report facts, uncertainty, method limits, doctor questions, safe observation plan, and named review.
- Previous growth logic: publish more content and expose more products.
- New growth logic: 15 interviews, ten external paid pilots, one CTA, measured funnel, and no ads before proof.

### Plan Delta
1. Runtime and safety before traffic.
2. One product before a ladder.
3. Named human approval before every delivery.
4. Twenty de-identified fixtures before release.
5. Ten unique external buyers before revenue claims.
6. One canonical price, promise, CTA, and review rule across every surface.
7. Supplements and affiliate monetization remain outside core V1.
8. Recorded decisions replace experiment accumulation.

### Next 12h
1. Repair scheduled-task Telegram connectivity and prove one polling owner.
2. Reinstate persisted named approval before delivery.
3. Feature-gate all paid offers except the 5,900 RUB HMS pilot.
4. Remove automatic supplement/affiliate upsell from the HMS path.
5. Convert the unsafe delivered HMS draft into a golden negative fixture.
6. Write the dedicated HMS output schema and deterministic claim checks.
7. Answer founder qualification, real revenue, weekly capacity, channel metrics, and affiliate-priority questions.
8. Recruit five external discovery interviews.
9. Recover `C:` above 10 GiB with operator review.

### Context For New Model

#### Stage
Controlled concierge pilot; bot down; public launch blocked; product is entering a controlled rebuild around one HMS clarity service.

#### Objective
Deliver ten unique external paid, named-review HMS cases with zero critical defects and a client-verifiable next safe action.

#### Constraints
- one Windows scheduled-task polling owner
- manual payment and mandatory human approval
- no diagnosis or treatment from HMS
- no supplement/affiliate upsell in core V1
- health-data consent, policy, retention, deletion, and processor controls required
- latest completed benchmark is the May 31 report
- disk is below the 10 GiB floor
- 20 tracked files remain dirty, so full Git/source synchronization is false

#### Immediate Next Actions
1. Restore runtime.
2. Restore the review gate.
3. Collapse to one offer.
4. Pass the HMS fixture suite twice.
5. Answer founder questions and recruit external interviews.

## 2026-07-16 15:25 MSK - Controlled Supplement Protocol Drafting Added

### What Changed
- Added `WellnessBot/supplement_protocols.py` as a deterministic safety layer over the existing supplement catalog.
- Only the versioned `vitamax_endoflora_8251` protocol can currently become a concrete supplement draft.
- The protocol preserves the catalog name, official URL, label use, monitoring window, stop signals, safety notes, and SPZ-03 commercial disclosure.
- Missing age 18+, medications/supplements, allergies, diagnoses, unsafe OCR, pregnancy/breastfeeding, acute GI red flags, serious background, or current medications block the concrete protocol.
- Other catalog candidates remain blocked until a separate protocol is explicitly enabled.
- Supplement schemes are injected after the AI draft from deterministic catalog data, preventing the model from inventing product names, doses, or courses.
- Any dossier containing a concrete supplement protocol now enters `awaiting_supplement_protocol_review`; admin approval records approver, timestamp, and decision before client delivery.
- Added the protocol module to the Docker image.
- Telegram polling was not started; scheduled task ownership was preserved.

### Verification
- `py -3.12 -m unittest discover -s tests -v`: 53 tests passed.
- Python compilation passed for the changed bot modules.
- End-to-end isolated function smoke confirmed the final dossier contains the controlled EndoFlora scheme.
- Safety tests cover missing medications/allergies, current L-thyroxine use, pregnancy, adult confirmation, heartburn enzyme exclusion, and the safe adult Osipov path.

### Stage
- Stage ID remains `controlled-concierge-pilot-2026-06-18-r1`.
- Human review remains required for a client-facing supplement protocol.
- Public launch remains blocked.

## 2026-06-21 16:40 MSK - Runtime State Refilled By Fresh Same-User Osipov Re-entry

### What Changed Since 2026-06-21 16:38 MSK
- The canonical coordination and strategy files were re-read again in the canonical workspace:
  - `docs/CURRENT_STAGE.json`
  - `docs/AGENT_CONTEXT_HUB.md`
  - `docs/KNOWLEDGE_SYNC_HUB.md`
  - `docs/PROJECT_PULSE_LOG.md`
  - `docs/AGENT_SYNC_PROTOCOL.md`
  - `docs/STRATEGY_LIVE_DELTA.md`
  - `docs/SPRINT_BOARD_20260413.md`
  - `docs/ENGINEERING_MANDATE_20260413.md`
- A newer runtime and commercialization artifact did displace the stale `16:38` story:
  - `bot.stderr.log` now contains handled updates at `2026-06-21 08:36:49 +03:00`, `08:36:51 +03:00`, `08:36:54 +03:00`, `08:36:56 +03:00`, `08:36:58 +03:00`, and `08:37:00 +03:00`
  - `WellnessBot/data/runtime_state.json` is no longer empty and was last written at `2026-06-21 08:37:00 +03:00`
  - mounted runtime state is now `submission_id = 20260621T053653Z_1084557944`, `offer = osipov`, `step = osipov_context`, `payment_status = manual_payment_confirmed`, `consent_given = true`, `adult_confirmed = false`
  - the matching persisted submission `20260621T053653Z_1084557944` exists and confirms a fresh `osipov` rail at `5900 RUB`, manually confirmed at `2026-06-21T05:37:00Z`
  - `chat_sessions` remains empty even though `user_sessions` is no longer empty
- The new artifact improves runtime freshness but worsens case control:
  - the same user already had delivered `osipov` at `20260618T192846Z_1084557944`
  - the same user already had delivered `gut_support_18` at `20260619T215149Z_1084557944`
  - both older specialist rails still lack persisted review artifacts
  - the new `20260621T053653Z_1084557944` re-entry therefore widens same-user specialist duplication rather than proving a clean monetization loop
- The current `ops/agent-sync-status.ps1` run still leaves the control plane unresolved:
  - `TrackedDirtyFiles = 19`
  - `BotTaskState = Running`
  - `BotProcessCount = 2`
  - `Published = True`
  - `Synchronized = False`
- Disk slipped slightly again and remains below floor:
  - `C:` free space is now `5226946560` bytes (`~4.87 GiB`) at `2026-06-21 16:40:06 +03:00`
- Public-surface truth remains misaligned with the governed pilot:
  - `landing/index.html` still names `Premium Wellness Dossier` and Telegram follow-up support
  - root `index.html` still claims a free first step, live YooKassa-style payment, PDF dossier delivery, and off-map pricing
  - `mini-app/index.html` still presents a live `1 000 ₽` entry rail plus dossier/PDF/support output
- Loop evidence remains unchanged where it matters:
  - `WellnessBot/data/product_governance.json` still shows `151` experiments and `0` decisions
  - the top repeated experiment titles still repeat `12`, `11`, `8`, `8`, and `5` times
  - `docs/tasks` still contains `29` open `HERMES-20260505-*` task packets

### Strategy Delta
- Product direction remains `Telegram-first controlled concierge`, but this run hardens the control thesis:
  - runtime freshness improved
  - same-user commercialization control worsened
  - growth work is therefore even less justified than the morning doc set implied
- The live value proposition remains `human-reviewed nutrition navigation in Telegram with explicit safety and escalation boundaries`.
- The monetization path narrows again:
  - manual concierge remains the only approved payment mode
  - one governed `1490 RUB` entry rail remains the only defensible near-term conversion path
  - specialist rails must not reopen for the same user until review traceability and canonical case ownership are explicit

### Loop Risk
- Repeating docs/status refreshes while the same user can still reopen `osipov` before the earlier `osipov` and `gut_support_18` rails are governed is low-impact churn.
- Growing a `151`-experiment backlog with `0` decisions and repeated titles is low-impact churn.
- Polishing landing, root, or mini-app copy before the same-user specialist chain is controlled is low-impact churn.

### Higher-Impact Replacement Action
1. Stop the competing poller and capture one clean runtime artifact newer than `2026-06-21 08:37:00 +03:00`.
2. Block same-user specialist re-entry until `canonical_path` or `case_relation` exists across the old and new specialist rails.
3. Enforce `direct_delivery => persisted review artifact or named manual override`.
4. Feature-gate or roll back `gut_support_18` until the approved ladder is explicit.
5. Then neutralize landing/root/mini-app overclaims and return to benchmark transport work.

### Next Action
1. Stop the duplicate poller and capture a clean post-fix runtime artifact.
2. Explain or repair the non-empty `user_sessions` plus empty `chat_sessions` split.
3. Persist review evidence or a named manual override for every `direct_delivery` rail.
4. Canonicalize the same-user paid stack including the new June 21 `osipov` re-entry.
5. Neutralize public-surface overclaims to the Telegram-first manual-review truth.
6. Recover `C:` above `10 GiB` before replay-heavy verification work.

## 2026-06-21 16:38 MSK - Superseded Same-Day Onboarding Snapshot

### Note
- The `16:38 MSK` onboarding snapshot was superseded in the same day.
- It incorrectly carried forward `runtime_state.json` as empty.
- The `16:40 MSK` entry above is now the governing pulse-log truth for June 21.

## 2026-06-21 04:40 MSK - Superseded Morning Control Snapshot

### Note
- The morning refresh correctly identified the direct-delivery review breaches, duplicate polling risk, public-surface overclaim, and disk-floor breach.
- Its runtime-state assumption is now stale because June 21 `08:37 +03:00` runtime-state and handled-update evidence exists.

## 2026-07-18 02:18 MSK - Регулярная GitHub/Notion синхронизация

- Stage не менялся: nutriok-controlled-build-2026-07-17-r1; controlled build / concierge pilot, public launch заблокирован.
- Проверки: 63 unittest пройдены, Python compilation пройдена; scheduled task WellnessBot = Ready, процессов = 0.
- Git: master, HEAD=origin/master=bd58da9; remote и GitHub connector доступны, но в рабочем дереве 24 tracked-файла и многочисленные untracked-артефакты. Смешанная дельта не публиковалась.
- Безопасность: не индексировались do_api_token.txt, VPN/SSH-скрипты, .venv_wsl, логи, lock-файлы и прочие потенциально чувствительные runtime-артефакты.
- Notion connector доступен; будет создан отдельный обезличенный статусный лист. Диск: около 3.87 GiB свободно, ниже floor 10 GiB.
- Готово только к ограниченному обезличенному пилоту с ручной оплатой и обязательным human review; публичный запуск, автоматическая оплата и второй polling-процесс запрещены.
- Следующие действия: разделить и проревьюировать кодовую дельту, довести structured intake и named approval, собрать свежий runtime proof, 20 fixtures/2 benchmark-прогона и восстановить запас диска.

## 2026-07-18 16:45 MSK - Strategy Refresh Cycle

### Done
- Re-read the required coordination docs and re-ran `ops/agent-sync-status.ps1` in the canonical workspace.
- Re-verified the governing NutriOK product contract, current benchmark references, and the working-tree product markers.
- Re-ran `py -3.12 -m unittest discover -s tests -v` and confirmed 63 passing tests.
- Re-ran `py -3.12 -m compileall WellnessBot tests` successfully.
- Refreshed `docs/STRATEGY_LIVE_DELTA.md`, `docs/SPRINT_BOARD_20260413.md`, `docs/ENGINEERING_MANDATE_20260413.md`, and `docs/AGENT_CONTEXT_HUB.md` to the July 18 governing state.

### Current status
- Stage remains `nutriok-controlled-build-2026-07-17-r1`; controlled build / concierge pilot; public launch blocked.
- Repo truth: `master`, `HEAD=origin/master=a9f0734`, `Published=True`, `TrackedDirtyFiles=22`, `Synchronized=False`.
- Runtime truth: scheduled task `WellnessBot` is `Ready`, active bot process count is `0`, and fresh proof-of-life is still missing.
- Benchmark truth: latest completed report remains `ops/reports/quality_report_20260531T083403Z.md`; latest QA synthesis remains `docs/WELLNESS_DIALOGUE_QA_20260608.md`.
- Ops truth: `C:` free space is `3171799040` bytes (`~2.95 GiB`), below the `10 GiB` floor.

### Loop risks
- Repeating strategy refreshes without new intake, review, runtime, or benchmark artifacts.
- Polishing public surfaces before the controlled paid cycle is technically enforceable.
- Expanding offers or supplement logic before one governed NutriOK benchmark exists.

### Higher-impact replacement action
1. Persist the structured intake contract.
2. Persist reviewer evidence for guarded outputs.
3. Build the 20-case fixture pack and run the benchmark twice.

### Next 12h
1. Persist goal, baseline, metric, adherence, and three-day diary end to end.
2. Persist reviewer identity, decision, timestamp, and approved artifact for full tiers and supplement details.
3. Capture one fresh scheduled-task runtime proof without starting a second poller.
4. Recover `C:` above `10 GiB` with operator-reviewed cleanup.
5. Split publishable source changes from secrets, logs, lockfiles, and local ops debris.
6. Write RF retention, deletion, encryption, access, and audit controls.

### Context For New Model
- Stage: NutriOK controlled build; runtime not freshly proven; public launch blocked.
- Done: sync truth, tests, compilation, product direction, and blocker stack were re-verified in this session.
- Next: intake persistence, reviewer persistence, benchmark proof, runtime proof, disk recovery, dirty-tree split.
- Constraints: one scheduled-task poller only, manual payment only, Olga approval for full tiers and supplement details, no diagnosis/treatment framing.


## 2026-07-21 02:17 MSK - Regular GitHub/Notion Synchronization

- Stage unchanged: `nutriok-controlled-build-2026-07-17-r1`; controlled concierge pilot; public launch blocked; `PAYMENT_MODE=manual`; human review required.
- `master` and `origin/master` both point to `a9f0734`; `git ls-remote --heads origin` succeeded.
- Worktree remains mixed: 24 tracked files changed plus untracked runtime, virtual-environment, infrastructure, and secret-like artifacts. No destructive cleanup or polling start was performed.
- Sync script reports `BotTaskState=Running`, `BotProcessCount=2`, `Published=True`, `Synchronized=False`.
- Verification: 63 tests passed; `py -3.12 -m compileall WellnessBot tests` passed.
- `C:` free space: `1,455,128,576` bytes (`~1.36 GiB`), below the 10 GiB floor; operator-reviewed cleanup is required.
- GitHub publication deferred because the current tree cannot be safely committed as a whole. Notion update requires connector write/readback; local fallback report records the sync posture.
- Next: split a reviewed publishable allowlist, fix single-owner runtime proof, persist intake/reviewer evidence, run two current-product benchmarks, and restore disk headroom.
## 2026-07-22 02:18 MSK - Регулярная синхронизация GitHub и Notion

- Этап без изменений: `nutriok-controlled-build-2026-07-17-r1`; controlled concierge pilot; публичный запуск заблокирован; `PAYMENT_MODE=manual`; human review обязателен.
- `master` и `origin/master` указывают на `a9f0734`; GitHub remote и connector доступны.
- Рабочее дерево смешанное: 24 tracked-файла изменены, дополнительно есть локальные runtime, virtual environment, инфраструктурные и secret-like артефакты. Polling не запускался, файлы не удалялись, смешанное дерево не публиковалось.
- `ops/agent-sync-status.ps1`: `BotTaskState=Running`, `BotProcessCount=2`, `Published=True`, `Synchronized=False`; проблема единственного владельца polling не закрыта.
- Последнее локальное runtime-свидетельство датировано 20.07.2026; свежие submission/draft присутствуют, но клиентские данные наружу не выгружались.
- Проверка: 63 теста пройдены; `py -3.12 -m compileall WellnessBot tests` пройдена.
- Свободно на `C:`: `1,526,071,296` байт (около `1.42 GiB`), ниже floor `10 GiB`; нужна уборка с ручным контролем, без слепого удаления.
- Notion синхронизируется; в GitHub допустим только узкий allowlist статусных документов. Полная синхронизация исходников отложена.
- Готово к пилоту только: обезличенные контролируемые кейсы, ручная оплата, обязательный именованный human review. Нельзя запускать публичный трафик, автоматическую оплату, unattended delivery или второй polling-процесс.
- Следующие шаги: разобраться с двумя polling-процессами, закрепить structured intake и reviewer evidence, провести 2 прогона набора из 20 NutriOK fixtures, восстановить диск и публиковать только проревьюированные изменения.

## 2026-07-22 00:27 MSK - Bot Operational Health Check

- Startup truth re-verified from the required coordination docs; stage stays `nutriok-controlled-build-2026-07-17-r1`, branch `master`, canonical workspace unchanged.
- `ops/preflight.ps1` passed: `.venv\Scripts\python.exe`, `.env`, and `WellnessBot/main.py` are present.
- `ops/agent-sync-status.ps1` reports `Published=True`, `TrackedDirtyFiles=24`, `BotTaskState=Ready`, `BotProcessCount=0`, `LegacyHermesPolling=False`, `Synchronized=False`.
- `Get-ScheduledTaskInfo` for `WellnessBot` shows the latest scheduled-task run ended on `2026-07-22 22:27:27` with `LastTaskResult=1`.
- `ops/bot-status.ps1` showed a transient `python.exe` match, but an immediate `Win32_Process` readback did not confirm a live command line; treat runtime as not process-verified.
- Freshest runtime artifact is `bot.stderr.log` modified on `2026-07-22 22:28:54`; the tail ends with `aiogram.exceptions.TelegramNetworkError` caused by `ClientConnectorError: Cannot connect to host api.telegram.org:443`.
- Direct connectivity check confirms the blocker layer: `Test-NetConnection api.telegram.org -Port 443` resolved DNS and pinged the host, but `TcpTestSucceeded=False`.
- `ops/llm-smoke.ps1` passed with a non-empty assistant reply, so the LLM path is currently alive even though console encoding garbled Cyrillic output in the terminal capture.

### Operational verdict

- Pass: preflight, config presence, scheduled-task discovery, and LLM smoke.
- Fail: Telegram polling runtime is down; the scheduled task exits with code `1` because outbound TCP `443` to `api.telegram.org` is failing.
- Active blockers remain the mixed dirty tree (`24` tracked files) and low operational margin already documented in the current stage artifacts.

### Immediate corrective actions

1. Restore outbound access from Windows to `api.telegram.org:443` for the scheduled-task environment: VPN/proxy/firewall/ISP path must be fixed outside the bot code.
2. After network recovery, run only the Windows scheduled task `WellnessBot` and capture one fresh handled-update proof; do not start polling from a terminal or WSL.
3. Re-run `ops/agent-sync-status.ps1`, `ops/bot-status.ps1`, and `ops/llm-smoke.ps1` after connectivity is restored.

## 2026-07-22 00:35 MSK - Proxy Fallback Fix

- Root cause narrowed further: the bot had an explicit `BOT_PROXY_URL=http://127.0.0.1:10808`, direct Telegram access was blocked, and `xray.exe` plus local port `127.0.0.1:10808` were available during diagnosis.
- The runtime failure path was self-inflicted: `WellnessBot/main.py` dropped the configured proxy after a failed precheck and switched to direct Telegram polling, which then crashed on `api.telegram.org:443`.
- Fixed `WellnessBot/main.py` so `_create_bot_session()` keeps the configured proxy even when the quick precheck fails and lets aiogram retry through the proxy instead of forcing direct mode.
- Verification: `py -3.12 -m py_compile .\WellnessBot\main.py` passed.
- Live restart could not be fully verified in this run because `Start-ScheduledTask -TaskName WellnessBot` returned `Access denied`; no terminal poller was started as a workaround.
- Next runtime action remains unchanged: start only the Windows scheduled task and confirm one fresh handled-update artifact.
## 2026-08-30 02:17 MSK - Регулярная синхронизация GitHub и Notion

- Этап: `nutriok-controlled-build-2026-07-17-r1`; controlled concierge pilot; `PAYMENT_MODE=manual`; public launch заблокирован; human review обязателен.
- Проверены docs, WellnessBot, ops, tests, landing, mini-app; polling не запускался. 63 теста и compilation прошли.
- `master=origin/master=c9fe781`; 24 tracked-изменения и untracked local/runtime/secret-like артефакты делают полный commit/push небезопасным.
- `agent-sync-status`: `BotTaskState=Running`, `BotProcessCount=2`, `Synchronized=False`; единственный polling owner не доказан.
- C: около `9.99 GiB` свободно, чуть ниже floor `10 GiB`.
- Следующие шаги: один scheduled-task owner, reviewed allowlist, intake/reviewer evidence, два benchmark-прогона, восстановление диска.
- GitHub readback успешен; Notion status page создана и проверена поиском; секреты и клиентские данные не передавались.

## 2026-10-15 15:09 MSK - Регулярная синхронизация GitHub и Notion

- Этап не изменён: `nutriok-controlled-build-2026-07-17-r1`; controlled concierge pilot; `PAYMENT_MODE=manual`; public launch заблокирован; human review обязателен.
- Репозиторий: ветка `master`, `HEAD=origin/master=c9fe781`; рабочее дерево смешанное: 24 tracked-файла изменены, присутствуют untracked virtualenv, runtime/lock/log, token-like и другие локальные артефакты. Полная публикация не выполнялась.
- Runtime: `WellnessBot` scheduled task = `Ready`, процессов `0`, `LegacyHermesPolling=False`; второй polling-процесс не запускался. Свежий handled-update proof не получен.
- Проверки: `63` теста прошли; `py -3.12 -m compileall WellnessBot tests` прошёл.
- Ops-блокер: свободно на `C:` `2,490,368` байт (`~2.4 MB`) на `2026-10-15 15:09 MSK`, существенно ниже floor `10 GiB`. Удаление файлов не выполнялось.
- GitHub: remote доступен для чтения (`git ls-remote` успешен), но commit/push отложен: текущий набор нельзя безопасно коммитить целиком; нужна reviewed allowlist только для намеренных статусных документов.
- Notion: будет выполнена отдельная запись только без секретов и клиентских данных; точный readback обязателен. При недоступности коннектора локальный fallback-отчёт фиксирует причину.
- Готово к пилоту только: ограниченные обезличенные concierge-кейсы, ручная оплата, обязательный named human review. Нельзя запускать public traffic, автоматическую оплату, unattended delivery, широкий трафик или второй poller.
- Следующие шаги: восстановить диск операторской уборкой; доказать единственного runtime-владельца; закрепить structured intake и reviewer evidence; собрать два актуальных NutriOK benchmark-прогона; опубликовать только проверенный allowlist.
