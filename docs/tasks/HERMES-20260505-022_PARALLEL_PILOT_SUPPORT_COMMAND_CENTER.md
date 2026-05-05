# HERMES-20260505-022: parallel pilot support command center

Task ID: `HERMES-20260505-022`
Status: `approved`
Owner: `Olga + Codex`
Agent: `Hermes`
Priority: `P0`
Access Level: `Level 1 only`
Duration: `parallel work while Codex executes P0/P1 pilot plan`
Mode: `parallel command center -> live-test triage -> OCR/fallback playbook -> readiness board -> implementation packets`

## 1. Mission

Гермес, мы оставляем стратегию Codex в действии:

`не расширяем хаос -> доводим один безопасный платный Telegram-путь до pilot-ready`

Пока Codex занимается кодом, runtime, smoke-тестами и live feedback Ольги, твоя задача - быть параллельным командным центром пилота.

Ты должен не просто “аудировать”, а готовить материалы, которые ускоряют выполнение:

- структурировать живые тесты Ольги;
- готовить triage-карточки;
- разложить OCR/file fallback проблему;
- подготовить понятные клиентские тексты без правки кода;
- подготовить admin/operator workflow;
- следить, чтобы стратегия не расползалась;
- создавать готовые draft implementation packets для Codex;
- экономить время и токены, не дублировать уже сделанные отчеты.

Главный результат: когда Ольга пришлет live-тесты, Codex должен получить уже готовую систему обработки, а не разбирать хаос с нуля.

## 2. Current Project State

Учитывай актуальное состояние:

- Бот работает, polling поднят.
- DeepSeek отвечает.
- Payment smoke: `SMOKE_OK`.
- Admin governance smoke: `SMOKE_OK`.
- Complex dossier smoke ранее прошел.
- Codex уже сделал code-fix: delivery gate + product invoice payload + русский CTA.
- Коммит Codex: `17a7174 fix: enforce delivery gate and product invoice payload`.
- Runtime P0 “бот не работает” сейчас снят, но остается runtime resilience риск.
- Новый live-риск: Yandex OCR возвращал `401 Unauthorized` на фото, значит file/lab flow требует fallback и диагностики без раскрытия ключей.
- Mini-app/public surface пока не главный фронт: сначала Telegram backend + landing/legal, потом mini-app.

## 3. Hard Boundaries

Ты остаешься на Level 1.

Можно:

- читать `docs/`, `WellnessBot/`, `ops/`;
- читать код только для анализа;
- создавать отчеты, таблицы, playbooks, task packets;
- улучшать `docs/hermes_skills/` и `docs/hermes_os/`, если это реально нужно;
- создавать готовые copy proposals и patch plans, но не применять их к коду.

Нельзя:

- менять `WellnessBot/*.py`;
- менять `.env` или `WellnessBot/.env`;
- читать/копировать реальные клиентские PDF, фото, выписки, голоса, анализы;
- трогать `WellnessBot/data/`, кроме случаев если Codex отдельно даст sanitized файл;
- менять payment, YooKassa, Telegram payments;
- деплоить, подключаться к VPS, менять production;
- отправлять сообщения клиентам;
- коммитить в GitHub;
- удалять файлы;
- ставить диагнозы или назначать лечение.

Если требуется forbidden action - создай `approval request`, но не выполняй.

## 4. Context To Read First

Читай точечно, без простыней.

Обязательные документы:

1. `docs/CONTROLLED_PILOT_STRATEGY_V2_20260505.md`
2. `docs/MODEL_CONTEXT_START_HERE_20260505.md`
3. `docs/HERMES_PROJECT_WORKER_PROTOCOL_20260505.md`
4. `docs/PROJECT_DEVELOPMENT_SINGLE_SOURCE_OF_TRUTH.md`
5. `docs/PRODUCT_LINE_V2_20260426.md`
6. `docs/NUTRITION_NAVIGATION_POLICY_20260420.md`
7. `docs/LAB_RESULT_SAFETY_POLICY_20260421.md`
8. `docs/reports/HERMES-20260505-004_FULL_DAY_COMMAND_REPORT.md`
9. `docs/reports/HERMES-20260505-004_06_MASTER_BACKLOG.md`
10. `docs/hermes_os/index.md`, если существует
11. `docs/hermes_skills/index.md`

Код читать только для анализа:

- `WellnessBot/main.py` - delivery, client path, admin review, file flow.
- `WellnessBot/lab_ocr.py` - OCR/fallback behavior.
- `WellnessBot/voice_processor.py` - voice/STT fallback behavior.
- `WellnessBot/texts.py` - client copy proposals.
- `WellnessBot/payment_flow.py` - payment flow context.
- `WellnessBot/ai_drafting.py` - live replies and CTA context.
- `ops/` - available smoke/tests.

Не загружай большие файлы целиком, если можно найти нужные места через поиск.

## 5. Workstreams

### Stream A. Live Test Triage System

Создай систему, по которой Ольгины live-тесты можно быстро превращать в действия.

Создать:

`docs/reports/HERMES-20260505-022_LIVE_TEST_TRIAGE_SYSTEM.md`

Внутри:

- шаблон карточки live feedback;
- классификация P0/P1/P2/P3;
- классификация area: UX / safety / payment / lab / runtime / copy / legal / growth;
- правила: что чинит Codex, что готовит Hermes, что решает Olga;
- шаблон короткого ответа Ольге после каждого скрина;
- критерии “это блокер пилота” / “это улучшение после пилота”.

Создать таблицу:

`docs/reports/HERMES-20260505-022_LIVE_TEST_TRIAGE_TABLE.md`

Пока live-тестов нет, оставь таблицу пустой с примерами строк.

### Stream B. OCR/File Handling Playbook

Новый реальный риск: OCR Яндекса возвращал `401 Unauthorized`.

Твоя задача - не чинить ключи, а подготовить playbook.

Создать:

`docs/reports/HERMES-20260505-022_OCR_FILE_FALLBACK_PLAYBOOK.md`

Проверить read-only:

- какие форматы файлов принимает бот;
- что происходит при успешном OCR;
- что происходит при OCR error;
- что видит клиент;
- где нельзя позволить модели выдумывать показатели;
- какой fallback должен быть: PDF, лучшее фото, ручной ввод показателей;
- какие smoke/live cases нужны.

Обязательно подготовить клиентские тексты, но НЕ применять в код:

1. Если файл плохого качества.
2. Если OCR не сработал технически.
3. Если распознаны не все показатели.
4. Если показатель/единица измерения сомнительны.
5. Если клиент прислал фото жалобы, а не анализ.

### Stream C. Canonical Client Path Audit

Проблема: у одного клиента могут плодиться активные ветки.

Создать:

`docs/reports/HERMES-20260505-022_CANONICAL_CLIENT_PATH_AUDIT.md`

Без чтения реальных клиентских данных проверь по коду/документам:

- где создается новая заявка;
- где восстанавливается сессия;
- где выбирается active case;
- где follow-up документы привязываются к существующему кейсу;
- какие риски multi-path;
- какой временный ручной регламент нужен до кодового фикса;
- какой минимальный кодовый фикс потом должен сделать Codex.

Создать draft task packet:

`docs/tasks/HERMES-20260505-023_CANONICAL_CLIENT_PATH_FIX_DRAFT.md`

Status: `draft`.

### Stream D. Post-Fix Verification Board

Codex уже сделал delivery gate + invoice payload + русский CTA. Hermes должен подготовить проверочную доску.

Создать:

`docs/reports/HERMES-20260505-022_POST_FIX_VERIFICATION_BOARD.md`

Пункты:

- что уже исправлено Codex;
- как проверить delivery gate без реального клиента;
- как проверить invoice payload для week/premium/vip;
- как проверить отсутствие `Premium Wellness Dossier`;
- какие smoke-тесты уже есть;
- какие smoke-тесты еще нужны;
- что нужно проверить в live-тесте Ольги.

### Stream E. Premium Client Copy Pack

Подготовить пакет клиентских текстов для премиального пути.

Создать:

`docs/reports/HERMES-20260505-022_PREMIUM_CLIENT_COPY_PACK.md`

Дай готовые тексты:

- приветствие после `/start`;
- короткий пример результата;
- объяснение “что будет после анкеты”;
- если анализы есть;
- если анализов нет;
- HelloDoc route;
- ручная оплата;
- ожидание подтверждения оплаты;
- файл не распознан;
- результат готов, но проходит проверку;
- досье отправлено;
- сопровождение 30 дней;
- связь с оператором при сбое.

Требования:

- русский язык;
- премиально, мягко, конкретно;
- без медицинских обещаний;
- без “мы лечим”;
- не длиннее, чем нужно;
- каждая фраза должна вести к следующему действию.

### Stream F. Pilot Readiness Board

Создать единую доску готовности.

Файл:

`docs/reports/HERMES-20260505-022_PILOT_READINESS_BOARD.md`

Разделы:

- Must pass before pilot.
- Should pass before pilot.
- Can wait until after first pilot.
- Open risks.
- Owner: Codex / Hermes / Olga.
- Verification.

### Stream G. Codex Execution Queue

Создать компактную очередь для Codex.

Файл:

`docs/reports/HERMES-20260505-022_CODEX_EXECUTION_QUEUE.md`

Формат:

- Priority
- Task
- Why now
- Files likely involved
- Smallest safe fix
- Verification
- Depends on live test: yes/no

Не больше 12 задач. Только действительно важное.

## 6. Required Deliverables

Создать 7 отчетов:

1. `docs/reports/HERMES-20260505-022_LIVE_TEST_TRIAGE_SYSTEM.md`
2. `docs/reports/HERMES-20260505-022_LIVE_TEST_TRIAGE_TABLE.md`
3. `docs/reports/HERMES-20260505-022_OCR_FILE_FALLBACK_PLAYBOOK.md`
4. `docs/reports/HERMES-20260505-022_CANONICAL_CLIENT_PATH_AUDIT.md`
5. `docs/reports/HERMES-20260505-022_POST_FIX_VERIFICATION_BOARD.md`
6. `docs/reports/HERMES-20260505-022_PREMIUM_CLIENT_COPY_PACK.md`
7. `docs/reports/HERMES-20260505-022_PILOT_READINESS_BOARD.md`
8. `docs/reports/HERMES-20260505-022_CODEX_EXECUTION_QUEUE.md`

Создать 3 draft task packets:

1. `docs/tasks/HERMES-20260505-023_CANONICAL_CLIENT_PATH_FIX_DRAFT.md`
2. `docs/tasks/HERMES-20260505-024_OCR_FILE_FALLBACK_FIX_DRAFT.md`
3. `docs/tasks/HERMES-20260505-025_PREMIUM_COPY_IMPLEMENTATION_DRAFT.md`

Создать итоговый короткий отчет:

`docs/reports/HERMES-20260505-022_PARALLEL_COMMAND_CENTER_SUMMARY.md`

## 7. Quality Bar

Не пиши общие слова.

Каждый вывод должен быть в формате:

- что найдено;
- где найдено;
- почему это риск;
- что делать;
- кто владелец;
- как проверить.

Плохо:

`Надо улучшить тексты.`

Хорошо:

`P1 / Copy / Шаг ручной оплаты / Клиент не понимает, когда начнется разбор. Риск: тревога после оплаты. Fix: сообщение “Оплата получена, досье собирается, перед отправкой результат проверит эксперт; ориентир по времени ...”. Owner: Codex/Hermes. Verify: live-test после оплаты.`

## 8. Token Economy

Работай экономно:

- не переписывай старые отчеты;
- не копируй большие куски кода;
- используй ссылки на файлы и короткие findings;
- если уже есть вывод в HERMES-004, не повторяй его, а развивай до действия;
- Telegram-ответы короткие;
- подробности только в файлах.

## 9. Final Telegram Reply

В Telegram пришли только это:

```text
HERMES-20260505-022 выполнена.
Создал командный центр поддержки пилота.
Код, .env, клиентские данные, оплату, VPS и production не трогал.

Главные готовые артефакты:
- live-test triage system/table
- OCR/file fallback playbook
- canonical client path audit
- post-fix verification board
- premium client copy pack
- pilot readiness board
- Codex execution queue

Топ-3 рекомендации для Codex:
1. ...
2. ...
3. ...

Что жду от Ольги:
1. live-test скрины/тексты
2. домен Beget
3. 3-4 строки “кто такая Ольга”
```

## 10. Acceptance Criteria

Задача выполнена, если:

- все 8 отчетов созданы;
- 3 draft task packets созданы;
- нет правок кода;
- нет секретов;
- нет клиентских данных;
- OCR/file fallback разложен в понятный playbook;
- live-test triage готов до прихода тестов Ольги;
- Codex получает короткую очередь следующих задач;
- Hermes не дублирует старую аналитику, а превращает ее в действия.

## 11. One-Sentence Mission

Hermes должен быть параллельным штабом пилота: пока Codex чинит код и принимает live-тесты, Hermes превращает неопределенность в triage, playbooks, copy packs, readiness board и четкую очередь выполнения.
