# HERMES-20260505-004: Safety & Compliance Audit (Phase 3)

## P0 Safety Blockers

| ID | Проблема | Файл | Риск | Fix | Code? |
|----|----------|------|------|-----|-------|
| S01 | Delivery gate bypass: `delivered_to_client` без проверки judge_verdict | main.py:1810 | Клиент получает досье с известными проблемами качества | Добавить guard перед delivery | YES |
| S02 | Multi-path drift: 4 submission на 1 пользователя | data/submissions/ | Путаница, противоречивые досье | Канонический путь + archived | YES |
| S03 | Mini-app: цена 2990₽ + medical findings | mini-app/index.html | Юридический риск, репутация | Убрать хардкод | YES |

## P1 Safety Risks

| ID | Проблема | Файл | Риск | Fix | Code? |
|----|----------|------|------|-----|-------|
| S04 | Нет manual override audit trail | main.py:1810 | Непонятно, кто разрешил risky delivery | Добавить override_note + override_by | YES |
| S05 | sanitize_live_reply: 4 паттерна | ai_drafting.py:361 | Модель может обойти защиту | Расширить паттерны | YES |
| S06 | DOSSIER_DRAFT_PROMPT на английском | prompts.py:232 | Противоречивый сигнал модели | Перевести на русский | YES |
| S07 | «Premium Wellness Dossier» — английский | ai_drafting.py:91,329 | Неряшливый тон | Заменить на русский | YES |
| S08 | Нет явной блокировки диагнозов в live-чате | ai_drafting.py:361 | Модель может выдать «у вас X» | Добавить обобщённые regex | YES |
| S09 | PD-хранение: локальный диск как primary storage | PD_STORAGE_ARCHITECTURE | Нет RF-локализации, нет аудита | Миграция на PostgreSQL + S3 | YES |

## P2 Safety Improvements

| ID | Проблема | Риск | Fix | Code? |
|----|----------|------|-----|-------|
| S10 | Демо-пример: 30 строк, может утомить | Потеря внимания до safety framing | Сократить, safety — в первые 5 строк | NO |
| S11 | CONSENT_TEXT не показывает дату согласия | Юридическая неопределённость | Сохранять timestamp согласия | YES |
| S12 | Не проверяется, что клиент != ребёнок/подросток | Риск для уязвимых групп | Добавить возрастной gate в анкету | YES |

## P3 Compliance

| ID | Проблема | Fix | Code? |
|----|----------|-----|-------|
| S13 | Нет privacy policy на домене | Создать и разместить | NO |
| S14 | Нет Roskomnadzor notification check | Проверить требования | NO |
| S15 | Obsidian export создаёт копию health data | Отключить или контролировать | YES |

## Состояние PD-compliance

| Требование | Статус | Детали |
|-----------|--------|--------|
| Согласие на обработку | ✅ Есть | CONSENT_TEXT в боте |
| Privacy policy | ❌ Нет | Только шаблон в docs/templates/ |
| RF-локализация данных | ❌ Нет | Локальный диск, не РФ-хостинг |
| Разделение оператор/разработчик | ⚠️ Частично | Описано, не реализовано |
| Аудит доступа | ❌ Нет | Не реализован |
| Удаление данных | ❌ Нет | Не реализовано |
| Уведомление РКН | ❌ Не проверено | — |
