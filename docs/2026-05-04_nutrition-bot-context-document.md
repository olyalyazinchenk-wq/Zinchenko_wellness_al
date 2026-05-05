# Nutrition Bot — Context Document

> **Собран:** 04.05.2026  
> **Версия:** 1.0 — предварительная  
> **Автор:** Hermes Agent (автоматический сбор данных)  

---

## 1. Executive Summary

**Суть проекта:** Telegram-бот/магазин нутрициологических услуг с AI-разбором анкет и лабораторных анализов. Клиент выбирает направление (диабет, гипертония, щитовидная железа, вес, анемия, ЖКТ), оплачивает услугу, заполняет анкету, загружает анализы — и получает автоматический разбор от AI (DeepSeek) с рекомендациями по питанию, образу жизни, выявленным дефицитам и планом действий.

**Пользователь (Ольга):** Нутрициолог, владелец проекта. Хочет автоматизировать первичный разбор клиентов, сократить ручную работу, масштабировать бизнес через Telegram-канал.

**Текущий статус:** Кодовая база MVP готова (22 файла, 2061 строка Python). Завершён Этап 1: структура проекта, модели БД, магазин услуг, платёжная система, FSM-анкетирование, AI-промпты и сервис разбора.

---

## 📍 FILE INDEX — Абсолютные пути ко всем файлам

> **Корень проекта:** `/home/hermes/projects/nutrition_bot/`  
> **План архитектуры:** `/home/hermes/.hermes/plans/2026-05-04_nutrition-bot-architecture.md`  
> **Этот документ:** `/home/hermes/.hermes/plans/2026-05-04_nutrition-bot-context-document.md`

### 🐍 Python-файлы (22 шт.)

```
/home/hermes/projects/nutrition_bot/bot/main.py
/home/hermes/projects/nutrition_bot/bot/config.py
/home/hermes/projects/nutrition_bot/bot/dispatcher.py
/home/hermes/projects/nutrition_bot/bot/__init__.py                          [пустой]
/home/hermes/projects/nutrition_bot/bot/handlers/__init__.py                 [пустой]
/home/hermes/projects/nutrition_bot/bot/handlers/start.py
/home/hermes/projects/nutrition_bot/bot/handlers/shop.py
/home/hermes/projects/nutrition_bot/bot/handlers/payment.py
/home/hermes/projects/nutrition_bot/bot/handlers/questionnaire.py
/home/hermes/projects/nutrition_bot/bot/handlers/lab_analysis.py
/home/hermes/projects/nutrition_bot/bot/handlers/results.py
/home/hermes/projects/nutrition_bot/bot/handlers/support.py
/home/hermes/projects/nutrition_bot/bot/keyboards/__init__.py                [пустой]
/home/hermes/projects/nutrition_bot/bot/keyboards/main_menu.py
/home/hermes/projects/nutrition_bot/bot/keyboards/shop_kb.py
/home/hermes/projects/nutrition_bot/bot/keyboards/questionnaire_kb.py
/home/hermes/projects/nutrition_bot/bot/states/__init__.py                   [пустой]
/home/hermes/projects/nutrition_bot/bot/states/questionnaire_states.py
/home/hermes/projects/nutrition_bot/bot/states/analysis_states.py
/home/hermes/projects/nutrition_bot/bot/middlewares/__init__.py              [пустой]
/home/hermes/projects/nutrition_bot/bot/utils/__init__.py                    [пустой]
/home/hermes/projects/nutrition_bot/db/__init__.py                           [пустой]
/home/hermes/projects/nutrition_bot/db/models.py
/home/hermes/projects/nutrition_bot/db/database.py
/home/hermes/projects/nutrition_bot/db/migrations/                           [пустая папка]
/home/hermes/projects/nutrition_bot/schemas/__init__.py                      [пустой]
/home/hermes/projects/nutrition_bot/services/__init__.py                     [пустой]
/home/hermes/projects/nutrition_bot/services/shop_service.py
/home/hermes/projects/nutrition_bot/services/payment_service.py
/home/hermes/projects/nutrition_bot/services/questionnaire_service.py
/home/hermes/projects/nutrition_bot/services/ai_service.py
/home/hermes/projects/nutrition_bot/services/analysis_service.py
/home/hermes/projects/nutrition_bot/admin/__init__.py                        [пустой]
```

### 📝 AI-промпты (7 шт.)

```
/home/hermes/projects/nutrition_bot/ai_prompts/base_review.txt
/home/hermes/projects/nutrition_bot/ai_prompts/diabetes.txt
/home/hermes/projects/nutrition_bot/ai_prompts/hypertension.txt
/home/hermes/projects/nutrition_bot/ai_prompts/thyroid.txt
/home/hermes/projects/nutrition_bot/ai_prompts/weight_loss.txt
/home/hermes/projects/nutrition_bot/ai_prompts/anemia.txt
/home/hermes/projects/nutrition_bot/ai_prompts/gastrointestinal.txt
```

### ⚙️ Конфигурационные файлы (3 шт.)

```
/home/hermes/projects/nutrition_bot/requirements.txt
/home/hermes/projects/nutrition_bot/.env.example
/home/hermes/projects/nutrition_bot/README.md                                [отсутствует]
```

### 📐 Планы и документация (2 шт.)

```
/home/hermes/.hermes/plans/2026-05-04_nutrition-bot-architecture.md           — архитектурный план (543 строки)
/home/hermes/.hermes/plans/2026-05-04_nutrition-bot-context-document.md      — этот документ
```

---

## 2. Current State — Что уже сделано

### 2.1 Кодовая база

**Расположение:** `/home/hermes/projects/nutrition_bot/`

**Статистика:**
- 22 Python-файла с валидным синтаксисом
- 2061 строка кода
- 7 AI-промптов (`.txt`)
- 1 архитектурный план (`.hermes/plans/`)
- 15 зависимостей в `requirements.txt`

### 2.2 Реализованные модули

| Модуль | Файл | Назначение |
|--------|------|------------|
| **Main** | `bot/main.py` | Точка входа, запуск поллинга |
| **Config** | `bot/config.py` | Pydantic Settings: токены, API-ключи, БД |
| **Dispatcher** | `bot/dispatcher.py` | Настройка роутеров aiogram |
| **Handlers** | | |
| → Start | `bot/handlers/start.py` | `/start`, регистрация пользователя |
| → Shop | `bot/handlers/shop.py` | Магазин: категории → услуги → детали |
| → Payment | `bot/handlers/payment.py` | Telegram Payments API + ЮKassa |
| → Questionnaire | `bot/handlers/questionnaire.py` | FSM: 10 базовых + специфические вопросы |
| → Lab Analysis | `bot/handlers/lab_analysis.py` | Загрузка фото/PDF/ручной ввод |
| → Results | `bot/handlers/results.py` | Просмотр готовых AI-разборов |
| → Support | `bot/handlers/support.py` | Помощь + fallback |
| **Keyboards** | `bot/keyboards/` | Inline/reply клавиатуры (3 шт) |
| **States** | `bot/states/` | FSM-состояния (2 шт) |
| **DB Models** | `db/models.py` | 8 таблиц: User, Category, Service, Order, Questionnaire, CategorySpecificField, LabAnalysis, AIReview |
| **DB Config** | `db/database.py` | SQLAlchemy async engine + сессии |
| **Services** | | |
| → Shop | `services/shop_service.py` | CRUD для категорий и услуг |
| → Payment | `services/payment_service.py` | Создание заказов, обновление статусов |
| → Questionnaire | `services/questionnaire_service.py` | Сохранение анкет и специфических полей |
| → AI | `services/ai_service.py` | DeepSeek API: сбор контекста, отправка промпта, парсинг ответа |
| → Analysis | `services/analysis_service.py` | OCR (easyocr), сохранение файлов |

### 2.3 База данных (8 таблиц)

```
users                  — пользователи (Telegram ID)
service_categories     — категории (6 направлений)
services               — услуги внутри категорий
orders                 — заказы (статусы: PENDING → PAID → COMPLETED)
questionnaires         — анкеты (статусы: DRAFT → SUBMITTED → COMPLETED)
category_specific_fields — специфические поля по направлениям
lab_analyses           — загруженные анализы (фото/PDF/ручной ввод)
ai_reviews             — AI-разборы (статусы: PENDING → PROCESSING → COMPLETED)
```

### 2.4 Пользовательский путь (Customer Journey)

```
/start → Главное меню
  ↓
🛒 Выбор категории → Выбор услуги → Детали услуги
  ↓
💳 Купить → Telegram Invoice (ЮKassa) → Оплата → Статус PAID
  ↓
📋 Заполнить анкету:
   → 10 базовых вопросов (жалобы, цель, питание, сон, стресс...)
   → Специфические вопросы (зависят от направления)
   → Загрузка анализов (фото/PDF/вручную/пропустить)
  ↓
✅ Отправка анкеты → Статус SUBMITTED → Уведомление нутрициологу
  ↓
🤖 AI-разбор (DeepSeek) → Сохранение в ai_reviews
  ↓
📊 Клиент получает разбор: питание, дефициты, образ жизни, план действий
```

---

## 3. Tech Stack & Architecture

### 3.1 Технологический стек

| Компонент | Технология | Версия |
|-----------|-----------|--------|
| Язык | Python | 3.11+ |
| Фреймворк бота | aiogram | 3.18.0 |
| База данных | SQLite (dev) / PostgreSQL (prod) | через SQLAlchemy 2.0.36 |
| ORM | SQLAlchemy (async) | 2.0.36 |
| Миграции | Alembic | 1.14.0 |
| Валидация | Pydantic + pydantic-settings | 2.10.0 |
| AI API | DeepSeek (OpenAI-совместимый) | через openai==1.58.0 |
| OCR | EasyOCR | 1.7.2 |
| PDF | pdf2image + Pillow | 1.17.0 / 11.1.0 |
| Платежи | Telegram Payments API + ЮKassa | нативный API |
| HTTP | httpx | 0.28.0 |
| Хелперы | python-telegram-bot (job-queue) | 21.10 |

### 3.2 Архитектурные принципы

```
handlers (aiogram handlers) — ТОЛЬКО обработка сообщений, FSM
    ↓
services (бизнес-логика) — CRUD, вызов API, парсинг
    ↓
db/models (SQLAlchemy) — схемы таблиц, отношения, enum'ы
```

- Жёсткое разделение: хендлеры не содержат бизнес-логики
- Сервисы — чистые функции, работают с async_session
- Все конфиги через pydantic-settings из `.env`
- Минимум зависимостей, easy to deploy

### 3.3 Структура директорий

```
nutrition_bot/
├── bot/              # Telegram-бот (aiogram)
│   ├── handlers/     # 7 обработчиков
│   ├── keyboards/    # 3 клавиатуры
│   ├── states/       # 2 FSM-машины
│   └── config.py
├── services/         # Бизнес-логика (5 сервисов)
├── db/               # Модели + подключение
├── ai_prompts/       # 7 промптов для AI
└── .env.example      # Шаблон конфигурации
```

---

## 4. AI Configuration

### 4.1 Используемая модель

- **Модель:** `deepseek-chat` (DeepSeek V3)
- **API URL:** `https://api.deepseek.com/v1`
- **Клиент:** OpenAI SDK (`AsyncOpenAI`) в совместимом режиме
- **Temperature:** 0.3 (низкая креативность — нужна точность)
- **Max Tokens:** 4000
- **API Key:** хранится в `.env` (не в коде)

### 4.2 Системные промпты

**Базовый промпт** (`ai_prompts/base_review.txt`):

```
Ты — профессиональный ассистент нутрициолога.

ПРАВИЛА:
- НЕ ставишь медицинские диагнозы
- НЕ назначаешь лечение
- Даёшь КОНКРЕТНЫЕ рекомендации по продуктам
- Учитываешь российские реалии

ФОРМАТ ОТВЕТА (строго JSON):
{
  "nutrition_recommendations": "...",
  "lifestyle_recommendations": "...",
  "deficiencies_found": "...",
  "additional_tests": "...",
  "action_plan": "..."
}

ОБЯЗАТЕЛЬНЫЙ ДИСКЛЕЙМЕР: «Не является медицинским диагнозом...»
```

**Специфические промпты** (6 направлений):

| Направление | Файл | Ключевой фокус |
|-------------|------|----------------|
| Сахарный диабет | `diabetes.txt` | ГИ, гликемическая нагрузка, баланс БЖУ, регулярность |
| Гипертония | `hypertension.txt` | Натрий/калий, магний, омега-3, коэнзим Q10 |
| Щитовидная железа | `thyroid.txt` | Селен, йод, цинк, зобогенные продукты, антиоксиданты |
| Лишний вес | `weight_loss.txt` | Без жёстких диет, белок, клетчатка, постепенность |
| Анемия/дефициты | `anemia.txt` | Тип анемии, всасывание Fe, B12, связь с ЖКТ и циклом |
| Проблемы ЖКТ | `gastrointestinal.txt` | Триггеры, кислотность, пробиотики, low-FODMAP |

### 4.3 Контекст, подаваемый в AI

```
=== АНКЕТА КЛИЕНТА ===
Жалобы: [текст]
Цель: [текст]
Питание: [текст]
Образ жизни: [текст]
Сон: [текст]
Стресс: [текст]
Лекарства/БАДы: [текст]
Хронические заболевания: [текст]
Аллергии: [текст]

=== СПЕЦИФИЧЕСКИЕ ПОЛЯ ===
[набор из category_specific_fields]

=== ЛАБОРАТОРНЫЕ АНАЛИЗЫ ===
[OCR-текст или структурированные показатели]
```

### 4.4 Парсинг ответа AI

Сервис `ai_service.py` умеет парсить два формата:
1. **JSON** (предпочтительно) — извлекается через regex по `{...}`
2. **Текст с секциями** — ищет заголовки «Питание», «Образ жизни», «Дефициты», «Анализы», «План действий»

### 4.5 ⚠️ Missing: Google AI Studio

**Данные отсутствуют** — нужны от Ольги:
- Системные инструкции, которые она тестировала в AI Studio
- Few-shot примеры диалогов (если есть)
- Настройки модели: название, temperature, top-k, top-p
- Описание того, как модель должна получать данные о пользователе (рост, вес, аллергии, цели)

---

## 5. Business Logic & Flows

### 5.1 Направления услуг (6 штук)

| Slug | Название | Эмодзи |
|------|----------|--------|
| `diabetes` | Питание при сахарном диабете | 🩸 |
| `hypertension` | Питание при гипертонии | ❤️ |
| `thyroid` | Питание при заболеваниях щитовидной железы | 🦋 |
| `weight_loss` | Питание при лишнем весе | ⚖️ |
| `anemia` | Питание при анемии / дефицитах | 🩺 |
| `gastrointestinal` | Питание при проблемах ЖКТ | 🫃 |

### 5.2 Типовые услуги внутри направления

| Услуга | Цена | Состав |
|--------|------|--------|
| Первичная консультация | 2 500 ₽ | Анкета + разбор анализов + рекомендации |
| Расширенный разбор | 5 000 ₽ | Всё выше + план питания + неделя сопровождения |
| Ведение 1 месяц | 15 000 ₽ | Разбор + план + 4 созвона + поддержка |
| Чек-ап организма | 3 500 ₽ | Анализ крови + дефициты + профилактика |

### 5.3 Специфические вопросы по направлениям

**Диабет:** сахар натощак, сахар после еды, HbA1c, тип диабета, инсулин, эпизоды гипогликемии

**Гипертония:** верхнее/нижнее давление, пульс, холестерин ЛПНП, принимаемые препараты

**Щитовидная:** ТТГ, свободный Т3, свободный Т4, АТ к ТПО, диагноз, медикаменты

**Вес:** текущий вес, рост, обхват талии, желаемый вес, анамнез диет, переедание, тип активности

**Анемия:** гемоглобин, ферритин, B12, витамин D, сыв. железо, менструации, утомляемость, бледность

**ЖКТ:** боли в животе, вздутие, тошнота, изжога, частота стула, консистенция, пищевая аллергия, диагнозы

### 5.4 Статусы заказов и анкет

**Заказы:** `PENDING → PAID → PROCESSING → COMPLETED / CANCELLED`

**Анкеты:** `DRAFT → SUBMITTED → REVIEWING → COMPLETED`

**AI-разборы:** `PENDING → PROCESSING → COMPLETED / FAILED`

---

## 6. Roadmap / Этапы

### 🟢 Этап 1: База (MVP) — ГОТОВ ✅

- Каркас проекта
- Магазин услуг (категории + услуги)
- Платежи (Telegram Payments API + ЮKassa)
- Анкетирование (FSM, 10 базовых вопросов + специфические)
- Уведомления админу

**Результат:** Клиент может выбрать → оплатить → заполнить анкету

### 🟡 Этап 2: AI-разбор — ЧАСТИЧНО ГОТОВ 🟡

- ✅ Загрузка анализов (фото/PDF/ручной ввод)
- ✅ AI-интеграция (DeepSeek API)
- ✅ Система промптов (база + 6 направлений)
- ✅ Сервис парсинга и сохранения разбора
- ⬜ Выдача результата клиенту (красивый вывод с эмодзи)
- ⬜ PDF-версия разбора
- ⬜ Админ-проверка разбора (нутрициолог проверяет перед отправкой)

### 🔵 Этап 3: Прокачка — НЕ НАЧАТ ⬜

- Telegram WebApp для админки
- Личный кабинет клиента
- Дневник питания
- Умный AI (кластеризация жалоб, динамические чек-листы)
- Напоминания и челленджи
- Скидки постоянным клиентам

---

## 7. Known Gaps — Выявленные пробелы

### 7.1 🔴 Critical — Missing Data

| # | Что отсутствует | Где взять |
|---|----------------|------------|
| 1 | **Цели проекта и описание ЦА** | Notion: страница с целями/MVP |
| 2 | **Требования к MVP** | Notion: документ с требованиями |
| 3 | **Текущий статус задач (Kanban)** | Notion: доска задач |
| 4 | **Данные из Google AI Studio** | AI Studio: системные инструкции, few-shot примеры, настройки моделей |
| 5 | **Договор-оферта** | Нужен ли текст оферты перед оплатой? |
| 6 | **Telegram ID нутрициолога** | Твой Telegram ID для уведомлений |

### 7.2 🟡 Technical Debt

| # | Проблема | Приоритет |
|---|---------|-----------|
| 1 | `.env` не заполнен реальными токенами | HIGH — бот не запустится без этого |
| 2 | БД — SQLite (dev), нет миграции на PostgreSQL | MEDIUM — для прода нужен PostgreSQL |
| 3 | Отсутствует `__init__.py` во всех модулях | LOW — для aiogram работает и без них, но лучше добавить |
| 4 | Нет обработки повторных платежей | MEDIUM — edge case |
| 5 | Нет rate-limiting и anti-spam middleware | MEDIUM — для прода обязательно |
| 6 | OCR-сервис использует easyocr (тяжёлый) | LOW — на проде может тормозить, но для MVP окей |
| 7 | Нет админ-панели (только уведомления в чат) | HIGH — нутрициологу нужно удобно просматривать анкеты |
| 8 | Нет возможности редактировать анкету после отправки | MEDIUM |

### 7.3 🟢 Feature Gaps

| # | Хотелка | Статус |
|---|--------|--------|
| 1 | Добавление новых направлений без кода | ⬜ Нужна админка с CRUD категорий |
| 2 | Экспорт разбора в PDF | ⬜ Нужен pdfkit/reportlab |
| 3 | Напоминания клиентам (дневник питания) | ⬜ Нужен cron/apscheduler |
| 4 | Челленджи и вовлечение | ⬜ Этап 3 |
| 5 | Интеграция с Google Calendar (запись на созвон) | ⬜ Этап 3 |
| 6 | Email-рассылки | ⬜ Этап 3 |

---

## 8. Что нужно от Ольги

### Прямо сейчас — пришли мне:

1. **Из Notion:**
   - Описание целей проекта (одним абзацем)
   - Кто твоя целевая аудитория (возраст, боли, запросы)
   - Что входит в MVP минимально (5-7 пунктов)
   - Текущий статус задач (что делаешь, что забросила, что в планах)

2. **Из Google AI Studio:**
   - Какие системные инструкции ты тестировала?
   - Есть ли примеры диалогов, которые ты используешь?
   - Название модели, temperature, top-k, top-p (если настраивала)

3. **Личное:**
   - Твой Telegram ID (для админ-уведомлений)
   - Нужна ли оферта перед оплатой?
   - Ты сама нутрициолог или будешь нанимать?

**Форматы:** Можно скопировать текст прямо сюда, можно скинуть ссылки, можно экспортировать страницы Notion как Markdown.

---

> **После получения этих данных я дополню документ и сгенерирую финальную версию со стратегическим и техническим планом разработки.**
