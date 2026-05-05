# HERMES-20260505-003: полный launch-readiness аудит и карта решений

Task ID: `HERMES-20260505-003`
Status: `approved`
Owner: `Olga + Codex`
Agent: `Hermes`
Priority: `P0`
Access Level: `Level 1` — документация, отчеты, task packets, улучшение собственных навыков. Код не менять.
Deadline: `2026-05-06 23:00 MSK`
Mode: `deep audit -> prioritized backlog -> task packets -> skill improvement`

## 1. Decision From Olga/Codex

1. Система навыков Гермеса предварительно принята.
2. Следующая задача: полный launch-readiness аудит продукта.
3. Гермесу дается Level 1.
4. Код бота, `.env`, клиентские данные, платежи, VPS, production и Telegram-отправки не трогать.
5. Главная цель: пока Codex/Ольга проводят живой клиентский тест, Hermes параллельно делает глубокий аудит проекта и готовит карту решений.

## 2. Objective

Провести максимально полезный, глубокий и прикладной аудит готовности Olga Wellness AI к controlled concierge pilot.

Нужно не просто найти проблемы, а:

- разложить их по приоритетам P0/P1/P2/P3;
- объяснить риск каждой проблемы;
- предложить конкретное решение;
- подготовить task packets для следующих исполнителей;
- обновить собственные навыки, если в процессе появился повторяемый workflow;
- помочь проекту выйти на уровень, где один платный клиентский путь можно проходить стабильно и безопасно.

## 3. Context To Read First

Обязательный вход:

1. `docs/MODEL_CONTEXT_START_HERE_20260505.md`
2. `docs/HERMES_PROJECT_WORKER_PROTOCOL_20260505.md`
3. `docs/PROJECT_DEVELOPMENT_SINGLE_SOURCE_OF_TRUTH.md`
4. `docs/AGENT_CONTEXT_HUB.md`
5. последние записи `docs/PROJECT_PULSE_LOG.md`
6. `docs/DOMAIN_SITE_MINIAPP_STRATEGY_20260505.md`
7. `docs/PRODUCT_LINE_V2_20260426.md`
8. `docs/NUTRITION_NAVIGATION_POLICY_20260420.md`
9. `docs/LAB_RESULT_SAFETY_POLICY_20260421.md`
10. `docs/PD_STORAGE_ARCHITECTURE_20260420.md`
11. `docs/PD_COMPLIANCE_PACK_20260420.md`
12. `docs/SMOKE_PAYMENT_CASE_20260421.md`
13. `docs/SMOKE_ADMIN_GOVERNANCE_20260421.md`
14. `docs/hermes_skills/index.md`
15. свои навыки из `docs/hermes_skills/`

Код читать только для аудита, без изменений:

- `WellnessBot/main.py`
- `WellnessBot/texts.py`
- `WellnessBot/prompts.py`
- `WellnessBot/ai_drafting.py`
- `WellnessBot/payment_flow.py`
- `WellnessBot/lab_ocr.py`
- `WellnessBot/voice_processor.py`
- `WellnessBot/config.py`
- `ops/*.py`
- `ops/*.ps1`

Если есть локальный `WellnessTMA/` или `external/google-ai-studio-moy-projekt/`, читать только как UI/reference слой, не как production backend.

## 4. Allowed Scope

Можно читать:

- `docs/`
- `WellnessBot/`
- `ops/`
- `WellnessTMA/`, если существует
- `external/google-ai-studio-moy-projekt/`, если существует

Можно создавать/редактировать:

- `docs/reports/HERMES-20260505-003_FULL_LAUNCH_READINESS_AUDIT.md`
- `docs/reports/HERMES-20260505-003_FINDINGS_TABLE.md`
- `docs/tasks/HERMES-20260505-004_*.md` и далее — только как draft/proposed tasks
- `docs/hermes_skills/*.md`, если нужно улучшить собственные навыки по итогам работы
- `docs/hermes_skills/index.md`, если добавлены/обновлены навыки

Нельзя менять:

- `WellnessBot/*.py`
- `.env`
- `WellnessBot/.env`
- `WellnessBot/data/`
- реальные клиентские PDF/фото/голосовые/выписки
- платежные настройки
- VPS/production-конфиги
- Git history
- любые файлы вне разрешенного scope

## 5. Hard Rules

- Работать только на русском языке.
- Не печатать секреты, ключи, токены, пароли.
- Не копировать персональные данные в отчеты.
- Не ставить диагнозы, не назначать лечение.
- Не обещать лечение добавками.
- Если видишь место, где бот может выдать клиенту небезопасный результат, маркируй P0.
- Если видишь возможность получить результат до оплаты или до human review, маркируй P0.
- Если видишь старые цены, старую линейку, англицизмы, битую кодировку или нерусский интерфейс, фиксируй как отдельную проблему.
- Не “размазывать” выводы. Писать конкретно: файл, место, риск, решение.

## 6. Workstreams

### Stream A. Safety-аудит клиентских текстов и промптов

Проверь:

- `WellnessBot/texts.py`
- `WellnessBot/prompts.py`
- клиентские фразы в `WellnessBot/main.py`
- структуру досье в `WellnessBot/ai_drafting.py`

Ищи:

- диагнозы вместо гипотез;
- назначения лечения;
- обещания эффекта добавок;
- недостаточно четкий маршрут к врачу;
- шаблонность и “бесплатные советы из интернета”;
- отсутствие конкретного плана 3 дня / 2 недели / 1 месяц / 1-3 месяца;
- ошибки русского языка;
- англицизмы в клиентском интерфейсе;
- битую кодировку.

### Stream B. UX-аудит клиентского пути

Построй карту пути:

`/start -> витрина -> выбор продукта -> анкета -> анализы/нет анализов -> HelloDoc -> ручная оплата -> admin confirm -> AI draft -> judge -> human review -> delivery -> сопровождение`

Ищи:

- где клиент застрянет;
- где слишком много текста;
- где не видно ценности;
- где не объяснен следующий шаг;
- где можно уйти в старый сценарий;
- где нет связи с оператором;
- где непонятно, что делать, если файл плохой;
- где нет разделения “анализы уже есть” / “анализов нет”.

### Stream C. Delivery-gate и payment-gate аудит

Проверить read-only:

- можно ли получить досье без оплаты;
- можно ли получить досье без human review;
- может ли `needs_revision` уйти клиенту;
- есть ли manual override и как он должен выглядеть;
- не расходятся ли состояния одного пользователя в нескольких ветках.

Важно: код не менять. Подготовить отдельный proposed task packet для Codex, если нужен кодовый фикс.

### Stream D. Сверка продукта, цен и документации с кодом

Сравнить:

- `docs/PRODUCT_LINE_V2_20260426.md`
- `docs/PROJECT_DEVELOPMENT_SINGLE_SOURCE_OF_TRUTH.md`
- `WellnessBot/payment_flow.py`
- `WellnessBot/texts.py`
- TMA/mini-app, если есть
- Google AI Studio UI reference, если есть

Официальная линейка:

- Демо-пример: 0 ₽
- 7 дней: 3 900 ₽
- 30 дней: 6 900 ₽
- VIP 30 дней: 14 900 ₽

Ищи любые расхождения.

### Stream E. Launch-readiness аудит

Проверить готовность к controlled concierge pilot:

- бот запускается;
- smoke-тесты существуют;
- manual payment flow описан;
- admin review есть;
- DeepSeek latency учтен;
- proxy/runtime риски зафиксированы;
- юридические документы и персональные данные описаны;
- есть fallback при плохих файлах;
- есть понятная связь с оператором;
- есть критерии `pilot-ready` / `not pilot-ready`.

### Stream F. Growth-аудит

Оценить коммерческую упаковку:

- понятно ли, почему клиент платит;
- отличается ли продукт от бесплатных советов;
- есть ли премиальность;
- есть ли “быстрая победа” перед оплатой;
- есть ли пример результата;
- есть ли причина выбрать Ольгу;
- не перегружен ли вход;
- не выглядит ли результат как шаблонный AI-текст.

### Stream G. Самоулучшение Гермеса

После аудита:

- обнови только те навыки, которые реально стали лучше;
- не плодить лишние файлы;
- добавь в отчет раздел “Что я улучшил в своей системе навыков и почему”.

## 7. Required Deliverables

### 7.1. Главный отчет

Создать:

`docs/reports/HERMES-20260505-003_FULL_LAUNCH_READINESS_AUDIT.md`

Структура:

1. Executive summary: pilot-ready или not pilot-ready.
2. Топ-10 проблем по приоритету.
3. P0-блокеры.
4. P1-важные исправления.
5. P2/P3 улучшения.
6. Карта клиентского пути.
7. Safety-аудит.
8. UX-аудит.
9. Payment/delivery gate аудит.
10. Сверка цен/продуктовой линейки.
11. Growth-аудит.
12. Рекомендованный план на 72 часа.
13. Рекомендованный план на 7 дней.
14. Какие task packets подготовлены.
15. Что Hermes улучшил в своих навыках.

### 7.2. Таблица findings

Создать:

`docs/reports/HERMES-20260505-003_FINDINGS_TABLE.md`

Колонки:

- ID
- Priority
- Area
- File/Source
- Problem
- Risk
- Recommended Fix
- Needs Code Change: yes/no
- Suggested Owner: Hermes/Codex/Olga

### 7.3. Draft task packets для следующих работ

Создать минимум 5 draft task packets:

1. `docs/tasks/HERMES-20260505-004_DELIVERY_GATE_PATCH_DRAFT.md`
2. `docs/tasks/HERMES-20260505-005_RUSSIAN_TEXT_AND_COPY_CLEANUP_DRAFT.md`
3. `docs/tasks/HERMES-20260505-006_PRODUCT_PRICE_SYNC_DRAFT.md`
4. `docs/tasks/HERMES-20260505-007_CLIENT_FLOW_UX_FIX_DRAFT.md`
5. `docs/tasks/HERMES-20260505-008_LAUNCH_CHECKLIST_FINALIZATION_DRAFT.md`

Статус у них должен быть `draft`, не `approved`.

## 8. Acceptance Criteria

Задача считается выполненной, если:

- Hermes не менял код;
- Hermes создал главный отчет;
- Hermes создал findings table;
- Hermes создал минимум 5 draft task packets;
- каждая проблема имеет риск и решение;
- P0-блокеры вынесены отдельно;
- есть четкий вердикт: pilot-ready или not pilot-ready;
- есть план на 72 часа и 7 дней;
- нет секретов и персональных данных;
- если навыки обновлены, объяснено зачем.

## 9. Verification

В конце Hermes должен проверить:

```powershell
git status --short
Get-ChildItem .\docs\reports | Select-Object Name,Length,LastWriteTime
Get-ChildItem .\docs\tasks | Select-Object Name,Length,LastWriteTime | Select-String HERMES-20260505-00
```

Если команды недоступны, сделать ручную проверку и описать ее.

## 10. Final Reply To Telegram

Когда задача завершена, ответь Ольге в Telegram коротко:

1. Вердикт: pilot-ready / not pilot-ready.
2. Сколько P0/P1/P2 найдено.
3. Какие 3 самых важных риска.
4. Какие файлы созданы.
5. Что брать следующим.

Не присылай весь отчет в Telegram, только короткое резюме и путь к файлам.

## 11. One-Sentence Mission

Гермес должен стать полноценным параллельным аудитором запуска: глубоко проверить продукт, найти слабые места, подготовить решения и оставить после себя структурированный backlog, который Codex сможет сразу выполнять.
