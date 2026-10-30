# Архитектура продакшен-развёртывания в РФ (Спринт F)

- **Продукт:** `НутриОК by Olga Kovaleva`
- **Текущий этап:** `nutriok-controlled-build-2026-07-17-r1` (контролируемый пилот на Windows Scheduled Task + SQLite)
- **Целевой этап после переключения:** `nutriok-rf-production-v1`
- **Статус документа:** Утверждённый проектный документ (Design & Cutover Runbook). Автоматическое переключение не выполняется до закрытия пилотных гейтов (20 оплаченных кейсов, 0 критических дефектов, 8 кейсов «ОК-Разбор»).

---

## 1. Хостинг и инфраструктурный контур в РФ

Для соблюдения требований локализации баз данных граждан РФ (ч. 5 ст. 18 ФЗ-152) вычислительные ресурсы и хранилища размещаются исключительно в российских дата-центрах уровня Tier III:

| Компонент | Основной вариант (Yandex Cloud) | Резервный вариант (Selectel) | Конфигурация |
|---|---|---|---|
| **Вычислительный узел** | Yandex Compute Cloud (`ru-central1-a`) | Selectel Cloud Servers (`ru-1`, Санкт-Петербург) | 2 vCPU, 4 GB RAM, Ubuntu 24.04 LTS |
| **СУБД** | Managed Service for PostgreSQL (`ru-central1`) | Managed PostgreSQL Selectel | PostgreSQL 16, 2 vCPU, 4 GB RAM, SSD 50 GB, репликация |
| **Объектное хранилище** | Yandex Object Storage (S3-совместимое) | Selectel S3 | Закрытый бакет для зашифрованных бэкапов и PDF-разборов |
| **Балансировщик / TLS** | Yandex Application Load Balancer / Caddy | Selectel Load Balancer / Caddy | TLS 1.3 (Let's Encrypt), приём вебхуков Telegram и YooKassa |

---

## 2. Переход с Long Polling на Telegram Webhook

В продакшен-контуре вместо локального `dp.start_polling()` используется входящий HTTPS Webhook:

1. **Эндпоинт:** `POST https://bot.nutriok.ru/webhook/telegram`
2. **Верификация подлинности:**
   - При регистрации вебхука (`setWebhook`) передаётся криптографический токен `secret_token` (256 бит, хранится в секретах окружения `TELEGRAM_WEBHOOK_SECRET`).
   - Сервер отклоняет (`HTTP 403`) любой запрос, в котором заголовок `X-Telegram-Bot-Api-Secret-Token` не совпадает с `TELEGRAM_WEBHOOK_SECRET` (сравнение через `hmac.compare_digest`).
   - Дополнительно на уровне файрвола разрешаются только официальные подсети Telegram (`149.154.160.0/20`, `91.108.4.0/22`).
3. **Идемпотентность:**
   - Каждый входящий `update_id` регистрируется в таблице `processed_updates(update_id BIGINT PRIMARY KEY, received_at TIMESTAMPTZ)`. Повторная доставка того же `update_id` от Telegram игнорируется (`HTTP 200 OK`).

---

## 3. PostgreSQL через адаптер репозитория (`CaseRepository`)

В Спринте C вся работа с данными переведена на интерфейс [`CaseRepository`](../WellnessBot/repo/base.py) и реализацию [`SqliteRepository`](../WellnessBot/repo/sqlite_repo.py).

Для перехода на PostgreSQL добавляется `WellnessBot/repo/postgres_repo.py` (`PostgresRepository(CaseRepository)`), реализующий те же методы поверх пула `asyncpg` / `psycopg`:

- **Схема таблиц PostgreSQL:**
  - `cases(submission_id TEXT PRIMARY KEY, user_id BIGINT NOT NULL, product_code TEXT NOT NULL, status TEXT NOT NULL, created_at TIMESTAMPTZ NOT NULL, updated_at TIMESTAMPTZ NOT NULL, payload_json JSONB NOT NULL)`
  - `intake(submission_id TEXT PRIMARY KEY REFERENCES cases(submission_id), schema_version INT NOT NULL, data_json JSONB NOT NULL)`
  - `reviews(id BIGSERIAL PRIMARY KEY, submission_id TEXT REFERENCES cases(submission_id), reviewer_id BIGINT NOT NULL, decision TEXT NOT NULL, decided_at TIMESTAMPTZ NOT NULL, artifact_sha256 TEXT NOT NULL, notes TEXT)` — с триггером `BEFORE UPDATE OR DELETE`, запрещающим модификацию и удаление записей проверки Ольги (`RAISE EXCEPTION 'reviews table is append-only'`).
  - `payments(id BIGSERIAL PRIMARY KEY, submission_id TEXT, amount_rub INT NOT NULL, mode TEXT NOT NULL, status TEXT NOT NULL, at TIMESTAMPTZ NOT NULL)`
  - `events(id BIGSERIAL PRIMARY KEY, at TIMESTAMPTZ NOT NULL, actor_id BIGINT NOT NULL, submission_id TEXT, kind TEXT NOT NULL, data_json JSONB NOT NULL)`
  - `sessions(user_id BIGINT PRIMARY KEY, state TEXT NOT NULL, data_json JSONB NOT NULL, updated_at TIMESTAMPTZ NOT NULL)`
- Переключение между SQLite и PostgreSQL управляется одной переменной окружения `DATABASE_URL` без изменения кода хендлеров.

---

## 4. Шифрование At-Rest и резервное копирование

1. **Шифрование дисков и объектного хранилища (At-Rest):**
   - Диски виртуальных машин и тома управляемой БД PostgreSQL шифруются ключами Yandex KMS / LUKS.
   - Бакет S3 для хранения загруженных анализов (`uploads/`) и готовых PDF-отчётов (`reports/`) использует Server-Side Encryption (`SSE-KMS`).
2. **Шифрование чувствительных полей на уровне приложения:**
   - Поля дневника питания, симптомов, принимаемых лекарств и загруженных анализов шифруются ключом `DATA_ENCRYPTION_KEY` (Fernet / AES-256-GCM) перед записью в `intake.data_json`.
3. **Резервное копирование и проверка восстановления:**
   - Ежедневный полный снепшот PostgreSQL + непрерывная архивация WAL (`pgBackRest`) с хранением зашифрованных архивов 30 дней.
   - Автоматический еженедельный тест восстановления (`restore-verify`) во временную изолированную БД с проверкой контрольных сумм `artifact_sha256`.

---

## 5. Соответствие 152-ФЗ (Персональные данные и сведения о здоровье)

Сведения о самочувствии, симптомах, принимаемых препаратах и результатах лабораторных анализов относятся к **специальной категории персональных данных** (ст. 10 ФЗ-152 «О персональных данных»):

1. **Явное информированное согласие:**
   - До начала сбора анкеты клиент явно подтверждает согласие на обработку ПДн и ознакомление с тем, что услуга носит информационно-консультационный (нутрициологический) характер и не является медицинской услугой.
   - В таблице `events` фиксируется неизменяемая запись `consent_accepted` с `actor_id`, `timestamp` и версией текста политики.
2. **Минимизация и обезличивание при вызове LLM:**
   - Во внешние LLM-провайдеры никогда не передаются ФИО, номер телефона, `@username` или `telegram_user_id` клиента — передаётся только обезличенный структурированный контекст (`primary_goal`, `baseline_score`, дневник питания и симптомы).
3. **Сроки хранения и удаление по запросу (Право на забвение, ст. 14 и ст. 21 ФЗ-152):**
   - Сырые файлы лабораторных бланков (`uploads/`) хранятся не более **90 дней** после выдачи разбора, после чего автоматически удаляются по расписанию.
   - По команде клиента `/delete_my_data` (или письменному запросу) выполняется каскадное удаление анкеты, дневника, сессий и загруженных файлов клиента с сохранением только обезличенной записи в журнале аудита (`events`: `user_data_deleted`).
4. **Журнал доступа (Audit Trail):**
   - Любое открытие карточки клиента, скачивание PDF или решение ревьюера фиксируется в таблицах `events` и `reviews` (`actor_id`, `submission_id`, `kind`, `artifact_sha256`, `at`).

---

## 6. Мониторинг, SLA и алерты в админ-чат

1. **Технический мониторинг:**
   - Эндпоинт `GET /healthz` проверяет доступность PostgreSQL, свободное место на диске (`>= 10 GiB`) и очередь фоновых задач.
   - При падении воркера, ошибке генерации PDF или превышении лимита времени ответа LLM отправляется мгновенный алерт в технический Telegram-канал.
2. **Продуктовый и SLA-мониторинг (Кабинет Ольги):**
   - Команда `/queue` сортирует кейсы по приоритету безопасности (`awaiting_safety_review` и красные флаги — на первом месте) и возрасту ожидания.
   - Команда `/stats` выводит воронку конверсии за 7 и 30 дней (`ОК-Старт → ОК-Экспресс → ОК-Разбор → ОК-Результат 8 → ОК-Ритм`).
   - Фоновый планировщик проверяет очередь каждые 2 часа и присылает Ольге напоминание, если любой оплаченный кейс ожидает проверки дольше **24 часов**.

---

## 7. Подключение YooKassa (после прохождения всех гейтов)

На этапе контролируемого пилота действует `PAYMENT_MODE=manual`. Переключение на автоматический приём оплаты (`PAYMENT_MODE=yookassa`) разрешается только после выполнения условий:

1. Закрыты гейты A–E, проведено минимум 20 пилотных кейсов с 0 критических дефектов.
2. Подключена онлайн-касса (54-ФЗ) через YooKassa с автоматической отправкой чеков (`receipt` с email/телефоном клиента и наименованием информационно-консультационной услуги).
3. Вебхук `POST /webhook/yookassa` проверяет IP-адреса YooKassa и перепроверяет статус платежа прямым запросом `GET https://api.yookassa.ru/v3/payments/{payment_id}` перед переводом кейса в `paid_confirmed`.

---

## 8. План переключения (Cutover Runbook) и отката

Переключение с локального Windows Scheduled Task на облачный сервер в РФ выполняется строго в следующей последовательности, чтобы исключить двойной опрос (`BotOwnerCount` всегда равен `1`):

### Шаг 1. Подготовка и миграция данных
1. На облачном сервере развернуть контейнер `WellnessBot` (в режиме ожидания, без запуска polling и без регистрации webhook) и применить схему PostgreSQL.
2. На локальной Windows-машине выполнить финальную верификацию SQLite:
   ```powershell
   .venv\Scripts\python.exe ops/migrate_json_to_sqlite.py --verify
   ```
3. Остановить единственного локального владельца polling (Windows Scheduled Task `WellnessBot`):
   ```powershell
   powershell -ExecutionPolicy Bypass -File ops/dev.ps1 bot-stop
   Disable-ScheduledTask -TaskName "WellnessBot"
   ```
4. Убедиться, что `BotProcessCount = 0`:
   ```powershell
   powershell -ExecutionPolicy Bypass -File ops/agent-sync-status.ps1
   ```

### Шаг 2. Перенос БД и включение Webhook
1. Скопировать `WellnessBot/data/nutriok.db` и директорию `WellnessBot/data/reports/` по защищённому каналу (`scp` / `age`) на облачный сервер и импортировать записи в PostgreSQL (`ops/migrate_sqlite_to_postgres.py --verify`).
2. Запустить вебхук-сервер на облачном узле и зарегистрировать Telegram Webhook с `secret_token`.
3. Обновить `docs/CURRENT_STAGE.json` на новый идентификатор этапа `nutriok-rf-production-v1`, зафиксировать запись в `docs/PROJECT_PULSE_LOG.md` и отправить коммит в `origin/master`.

### Шаг 3. План мгновенного отката (Rollback < 2 минут)
Если в течение первых 30 минут после переключения обнаружена критическая ошибка в облачном контуре:
1. Вызвать `deleteWebhook` через Bot API.
2. На локальной машине включить и запустить задачу `WellnessBot`:
   ```powershell
   Enable-ScheduledTask -TaskName "WellnessBot"
   powershell -ExecutionPolicy Bypass -File ops/dev.ps1 bot-start
   ```
3. Проверить `BotOwnerCount = 1` через `ops/agent-sync-status.ps1`.
