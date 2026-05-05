# HERMES-20260505-004: Status Snapshot (Phase 1)

## Текущий этап
**Controlled concierge pilot** — публичный запуск заблокирован. Задача: довести 1 платный клиентский цикл до стабильности.

## Что уже работает
- ✅ Telegram-бот (Python + aiogram) с полным клиентским путём
- ✅ Продуктовая линейка: демо (0₽) / 7д (3900₽) / 30д (6900₽) / VIP (14900₽)
- ✅ Анкетирование, сбор файлов, HelloDoc-маршрут
- ✅ Ручной платёж (PAYMENT_MODE=manual)
- ✅ AI-генерация досье + judge + growth architect
- ✅ Human review workflow (админ approve)
- ✅ Governance: insights, experiments, digest
- ✅ Smoke-тесты: payment case, admin governance
- ✅ PDF-генерация досье
- ✅ Система навыков Гермеса (10 навыков)

## Что блокирует pilot (P0)
| # | Проблема | Источник |
|---|----------|----------|
| 1 | Delivery gate bypass: `delivered_to_client` без проверки judge_verdict | main.py:1810 |
| 2 | Multi-path drift: 4 ветки на 1 пользователя | data/submissions/ |
| 3 | Mini-app price drift: 2990₽ + medical findings | mini-app/index.html |
| 4 | Runtime не подтверждён: proxy failures, бот не running | bot.stderr.log |

## Что требует проверки сегодня
- Все тексты на безопасность и русский язык
- UX-карта: нет ли дыр в клиентском пути
- Сверка цен во всех артефактах (код, тексты, UI)
- Growth-аудит: коммерческая упаковка
- PD-compliance: хранение, согласие, политики

## Прочитанные документы
- MODEL_CONTEXT_START_HERE, HERMES_PROJECT_WORKER_PROTOCOL
- PROJECT_DEVELOPMENT_SINGLE_SOURCE_OF_TRUTH
- AGENT_CONTEXT_HUB (самый информативный)
- PROJECT_PULSE_LOG (последние записи)
- DOMAIN_SITE_MINIAPP_STRATEGY
- PRODUCT_LINE_V2, NUTRITION_NAVIGATION_POLICY
- LAB_RESULT_SAFETY_POLICY, NUTRITION_REFERENCE_FRAMEWORK
- PD_STORAGE_ARCHITECTURE, PD_COMPLIANCE_PACK
- SMOKE_PAYMENT_CASE, SMOKE_ADMIN_GOVERNANCE
- HERMES-20260505-003 (previous audit findings)
- hermes_skills/index.md + все навыки
- Код: main.py, texts.py, prompts.py, payment_flow.py, ai_drafting.py, config.py
