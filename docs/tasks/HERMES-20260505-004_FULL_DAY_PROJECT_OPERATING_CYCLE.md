# HERMES-20260505-004: full-day project operating cycle

Task ID: `HERMES-20260505-004`
Status: `approved`
Owner: `Olga + Codex`
Agent: `Hermes`
Priority: `P0`
Access Level: `Level 1`
Duration: `full working day / 6-8 focused hours`
Mode: `context -> audit -> backlog -> task packets -> quality system -> final command report`

## 1. Mission

Гермес, твоя задача на сегодня - провести полноценный рабочий день как параллельный проектный агент Olga Wellness AI.

Ты должен не просто “сделать аудит”, а организовать вокруг себя рабочий цикл:

`войти в контекст -> проверить продукт -> найти слабые места -> разложить по приоритетам -> подготовить решения -> создать задачи для следующего этапа -> улучшить свои навыки -> оставить понятный отчет для Ольги и Codex`

Главный результат дня: проект должен стать понятнее, безопаснее, ближе к controlled concierge pilot и лучше подготовлен к следующим действиям.

## 2. Current Decision

Тебе разрешен Level 1:

Можно:

- читать `docs/`, `WellnessBot/`, `ops/`, UI-reference папки;
- создавать отчеты в `docs/reports/`;
- создавать draft/approved task packets в `docs/tasks/` только по правилам ниже;
- улучшать собственные навыки в `docs/hermes_skills/`;
- формировать backlog, карты, таблицы, чек-листы, решения.

Нельзя:

- менять код бота;
- менять `.env`, ключи, токены, платежные настройки;
- трогать клиентские данные, PDF, фото, голосовые, выписки;
- деплоить, подключаться к VPS, менять production;
- отправлять сообщения клиентам;
- делать массовые рассылки;
- выдавать медицинские заключения или назначения лечения.

Если в процессе ты видишь задачу, требующую кода, оплаты, production, VPS или клиентских данных, ты не выполняешь ее. Ты создаешь отдельный task packet со статусом `draft` и пометкой `requires Codex/Olga approval`.

## 3. Required Context Intake

Перед началом работы прочитай:

1. `docs/MODEL_CONTEXT_START_HERE_20260505.md`
2. `docs/HERMES_PROJECT_WORKER_PROTOCOL_20260505.md`
3. `docs/PROJECT_DEVELOPMENT_SINGLE_SOURCE_OF_TRUTH.md`
4. `docs/AGENT_CONTEXT_HUB.md`
5. последние записи `docs/PROJECT_PULSE_LOG.md`
6. `docs/DOMAIN_SITE_MINIAPP_STRATEGY_20260505.md`
7. `docs/PRODUCT_LINE_V2_20260426.md`
8. `docs/NUTRITION_NAVIGATION_POLICY_20260420.md`
9. `docs/LAB_RESULT_SAFETY_POLICY_20260421.md`
10. `docs/NUTRITION_REFERENCE_FRAMEWORK_20260421.md`
11. `docs/PD_STORAGE_ARCHITECTURE_20260420.md`
12. `docs/PD_COMPLIANCE_PACK_20260420.md`
13. `docs/SMOKE_PAYMENT_CASE_20260421.md`
14. `docs/SMOKE_ADMIN_GOVERNANCE_20260421.md`
15. `docs/tasks/HERMES-20260505-003_FULL_LAUNCH_READINESS_AUDIT.md`
16. `docs/hermes_skills/index.md`
17. все свои навыки из `docs/hermes_skills/`

Код читать только после документов и только для аудита:

- `WellnessBot/main.py`
- `WellnessBot/texts.py`
- `WellnessBot/prompts.py`
- `WellnessBot/payment_flow.py`
- `WellnessBot/ai_drafting.py`
- `WellnessBot/lab_ocr.py`
- `WellnessBot/voice_processor.py`
- `WellnessBot/config.py`
- `ops/*.py`
- `ops/*.ps1`

Если есть `WellnessTMA/` или `external/google-ai-studio-moy-projekt/`, изучи их как UI/reference слой, не как production backend.

## 4. Workday Schedule

### Phase 1. Orientation Snapshot, 30-45 минут

Цель: быстро собрать актуальную картину.

Сделай:

1. Проверь текущий этап проекта.
2. Выпиши official product line.
3. Выпиши P0-блокеры из документов.
4. Проверь, какие smoke-отчеты есть.
5. Проверь, какие задачи уже созданы.
6. Сформируй короткий status snapshot.

Создать файл:

`docs/reports/HERMES-20260505-004_01_STATUS_SNAPSHOT.md`

Внутри:

- текущий этап;
- что уже работает;
- что блокирует pilot;
- что требует проверки сегодня;
- какие документы были прочитаны.

### Phase 2. Client Journey Map, 60-90 минут

Цель: построить реальную карту клиентского пути.

Построй карту:

`/start -> витрина -> выбор продукта -> анкета -> файлы/анализы -> HelloDoc -> ручная оплата -> admin confirm -> AI draft -> judge -> human review -> delivery -> месяц сопровождения`

Для каждого шага укажи:

- где он находится в коде/документах;
- что видит клиент;
- что должен сделать клиент;
- что делает оператор;
- какой риск;
- что надо улучшить.

Создать файл:

`docs/reports/HERMES-20260505-004_02_CLIENT_JOURNEY_MAP.md`

### Phase 3. Safety And Compliance Audit, 90 минут

Цель: найти все места, где проект может стать медицински/юридически небезопасным.

Проверить:

- формулировки диагнозов/лечения;
- нутрицевтики и обещания эффекта;
- красные флаги;
- плохое качество анализов;
- human review;
- delivery-gate;
- персональные данные;
- согласие на обработку данных;
- хранение файлов;
- клиентские фото/выписки/анализы.

Создать файл:

`docs/reports/HERMES-20260505-004_03_SAFETY_COMPLIANCE_AUDIT.md`

Структура:

- P0 safety blockers;
- P1 safety risks;
- P2 improvements;
- recommended fixes;
- code changes required yes/no.

### Phase 4. Product And Growth Audit, 60-75 минут

Цель: проверить, есть ли коммерческая ценность и премиальность.

Оценить:

- понятно ли, за что клиент платит;
- видна ли разница с бесплатными советами;
- есть ли пример результата;
- есть ли “быстрая победа”;
- есть ли причина выбрать Ольгу;
- не слишком ли сложный вход;
- где добавить доверие;
- как усилить 7 дней / 30 дней / VIP.

Создать файл:

`docs/reports/HERMES-20260505-004_04_PRODUCT_GROWTH_AUDIT.md`

Обязательно дать:

- 10 точек усиления ценности;
- 5 улучшений оффера;
- 5 идей для Telegram/сайта;
- 3 быстрых улучшения, которые можно сделать до пилота.

### Phase 5. Price, Product, Text Sync, 60 минут

Цель: найти расхождения между документами, кодом, текстами и UI.

Официальная линейка:

- Демо: 0 ₽
- 7 дней: 3 900 ₽
- 30 дней: 6 900 ₽
- VIP 30 дней: 14 900 ₽

Проверить:

- `docs/PRODUCT_LINE_V2_20260426.md`
- `docs/PROJECT_DEVELOPMENT_SINGLE_SOURCE_OF_TRUTH.md`
- `WellnessBot/payment_flow.py`
- `WellnessBot/texts.py`
- UI/TMA/reference, если есть.

Создать файл:

`docs/reports/HERMES-20260505-004_05_PRODUCT_SYNC_AUDIT.md`

Формат таблицы:

- source;
- current value;
- expected value;
- mismatch yes/no;
- risk;
- proposed fix.

### Phase 6. Backlog And Task Packets, 90 минут

Цель: превратить аудит в исполнимый план.

Создать master backlog:

`docs/reports/HERMES-20260505-004_06_MASTER_BACKLOG.md`

Формат:

- ID;
- Priority P0/P1/P2/P3;
- Area;
- Problem;
- Risk;
- Fix;
- Owner;
- Needs approval yes/no;
- Suggested task packet.

Создать минимум 8 task packets:

1. `docs/tasks/HERMES-20260505-009_DELIVERY_GATE_CODE_FIX_DRAFT.md`
2. `docs/tasks/HERMES-20260505-010_CLIENT_PATH_COPY_FIX_DRAFT.md`
3. `docs/tasks/HERMES-20260505-011_PRODUCT_PRICE_SYNC_DRAFT.md`
4. `docs/tasks/HERMES-20260505-012_SAFETY_PROMPT_HARDENING_DRAFT.md`
5. `docs/tasks/HERMES-20260505-013_LAB_FILE_HANDLING_AUDIT_DRAFT.md`
6. `docs/tasks/HERMES-20260505-014_OPERATOR_REVIEW_WORKFLOW_DRAFT.md`
7. `docs/tasks/HERMES-20260505-015_SITE_DOMAIN_LANDING_DRAFT.md`
8. `docs/tasks/HERMES-20260505-016_PILOT_LAUNCH_CHECKLIST_DRAFT.md`

Все эти task packets должны быть `Status: draft`, не approved.

### Phase 7. Skill System Improvement, 45 минут

Цель: стать лучше по итогам дня.

Проанализируй:

- какие навыки реально использовались;
- какой навык оказался слабым;
- какой workflow повторялся;
- нужно ли создать новый навык;
- нужно ли обновить `index.md`.

Можно обновлять только `docs/hermes_skills/`.

Создать файл:

`docs/reports/HERMES-20260505-004_07_SELF_IMPROVEMENT_LOG.md`

### Phase 8. Final Command Report, 45 минут

Создать главный итоговый отчет:

`docs/reports/HERMES-20260505-004_FULL_DAY_COMMAND_REPORT.md`

Структура:

1. Executive verdict: pilot-ready / not pilot-ready / pilot-ready with conditions.
2. Что сделано за день.
3. Список созданных файлов.
4. P0/P1/P2/P3 summary.
5. 10 главных findings.
6. План на 72 часа.
7. План на 7 дней.
8. Что должен сделать Codex.
9. Что должна решить Ольга.
10. Что Hermes может взять завтра.
11. Какие навыки улучшены.
12. Риски, которые нельзя игнорировать.

## 5. Required Checkpoints

Каждые 1.5-2 часа делай короткий checkpoint-файл:

`docs/reports/HERMES-20260505-004_CHECKPOINT_01.md`
`docs/reports/HERMES-20260505-004_CHECKPOINT_02.md`
`docs/reports/HERMES-20260505-004_CHECKPOINT_03.md`

Формат checkpoint:

- что прочитал;
- что нашел;
- какой риск главный сейчас;
- что делаешь дальше;
- нужен ли approval.

Если связь идет через Telegram, в Telegram отправляй только короткое резюме checkpoint, не весь файл.

## 6. Quality Bar

Каждый finding должен быть конкретным:

Плохо:

`Надо улучшить UX.`

Хорошо:

`P1 / UX / WellnessBot/texts.py / На шаге выбора продукта клиент видит длинный текст без четкого next action. Риск: потеря клиента до оплаты. Fix: сократить до 3 блоков: ценность, что сделать, кнопка.`

Каждое решение должно отвечать:

- что исправить;
- где исправить;
- зачем;
- какой риск снимает;
- нужен ли код;
- кто исполнитель.

## 7. Hard Stop Conditions

Остановись и попроси approval, если задача требует:

- изменить код;
- открыть/изменить `.env`;
- взять реальный клиентский анализ/фото/PDF;
- изменить оплату;
- подключиться к VPS;
- сделать deploy;
- отправить сообщение клиенту;
- удалить файл;
- коммитить в GitHub от имени проекта.

## 8. Final Telegram Message

В конце дня отправь Ольге коротко:

```text
Задача HERMES-20260505-004 выполнена.
Вердикт: pilot-ready / not pilot-ready / pilot-ready with conditions.
Найдено: P0 = X, P1 = Y, P2 = Z, P3 = N.
Главные риски:
1. ...
2. ...
3. ...

Созданы файлы:
- docs/reports/...
- docs/tasks/...

Что брать следующим:
1. ...
2. ...
3. ...

Код, .env, клиентские данные, оплату, VPS и production не трогал.
```

## 9. Acceptance Criteria

Задача выполнена, если:

- созданы все 8 phase reports;
- создан full-day command report;
- создан master backlog;
- создано минимум 8 draft task packets;
- есть P0/P1/P2/P3 разметка;
- есть план на 72 часа и 7 дней;
- есть self-improvement log;
- Hermes не менял код и приватные файлы;
- Telegram-ответ короткий и управленческий;
- Codex может сразу взять backlog и выполнять.

## 10. One-Sentence Mission

Сегодня Гермес работает как полноценный проектный штаб: весь день превращает хаос проекта в карту решений, безопасный backlog и исполнимые задачи, становясь сильнее через собственную систему навыков.
