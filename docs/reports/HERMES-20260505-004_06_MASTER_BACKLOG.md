# HERMES-20260505-004: Master Backlog (Phase 6)

## P0 — Блокируют pilot немедленно

| ID | Area | Problem | Risk | Fix | Owner | Approval | Task |
|----|------|---------|------|-----|-------|----------|------|
| B01 | Delivery | `delivered_to_client` без проверки judge_verdict | Клиент получает опасное досье | Guard перед delivery + manual override | Codex | YES | 009 |
| B02 | Runtime | Бот не evidenced как running | Продукт недоступен | Восстановить polling, убрать proxy-зависимость | Codex | YES | — |
| B03 | Client | 4 submission на 1 пользователя | Путаница, противоречия | Канонический путь + archived | Codex | YES | — |
| B04 | Mini-app | Цена 2990₽ + medical findings | Юридический/репутационный | Убрать хардкод, безопасный placeholder | Codex | YES | 011 |

## P1 — Важные, до первого клиента

| ID | Area | Problem | Risk | Fix | Owner | Approval | Task |
|----|------|---------|------|-----|-------|----------|------|
| B05 | Safety | Нет manual override audit trail | Нет accountability | override_note + override_by | Codex | YES | 009 |
| B06 | Safety | sanitize_live_reply: 4 паттерна | Модель обходит защиту | Расширить паттерны + обобщённые regex | Codex | YES | 012 |
| B07 | UX | «Premium Wellness Dossier» — английский | Неряшливый тон | Заменить на «Персональное досье» | Codex | YES | 010 |
| B08 | UX | CTA_DEFAULT_TEXT — английский | Снижает конверсию | Полный русский текст | Codex | YES | 010 |
| B09 | Code | invoice_payload: хардкод "premium:" | week/vip с неверным префиксом | Динамический offer['code'] | Codex | YES | 011 |
| B10 | Safety | DOSSIER_DRAFT_PROMPT на английском | Противоречие правилам | Перевести на русский | Hermes→Codex | YES | 012 |
| B11 | Safety | CONSENT без timestamp | Юридическая дыра | Сохранять consent_at | Codex | YES | — |
| B12 | Safety | Нет возрастного gate | Риск для детей/подростков | Добавить в анкету | Codex | YES | — |

## P2 — Значимые улучшения

| ID | Area | Problem | Risk | Fix | Owner | Approval | Task |
|----|------|---------|------|-----|-------|----------|------|
| B13 | UX | Демо-пример длинный (30 строк) | Потеря внимания | Сократить до 12-15 строк | Hermes→Codex | YES | 010 |
| B14 | UX | Демо не видно в меню | Низкая конверсия | Кнопка «Посмотреть пример» первой | Codex | YES | — |
| B15 | UX | После анкеты нет немедленной ценности | Отвал клиента | 1-2 строки инсайта по кейсу | Codex | YES | 010 |
| B16 | UX | Статусы review_priority_* непрозрачны | Замедляет human review | Топ-3 проблемы в админ-уведомлении | Codex | YES | 014 |
| B17 | Growth | Нет «Почему Ольга» в боте | Нет доверия | 3-4 строки об эксперте | Hermes→Codex | NO | 010 |
| B18 | Lab | OCR при плохом качестве | Гадание по анализам | Уже есть обработка, но проверить | Codex | YES | 013 |
| B19 | Growth | Демо не показывает персонализацию | «Ещё один ChatGPT» | Добавить: «Ваш кейс будет выглядеть так же, но про ВАС» | Hermes | NO | — |
| B20 | PD | Obsidian export — копия health data | Утечка special-category data | Отключить или audit-control | Codex | YES | — |

## P3 — Технический долг и улучшения

| ID | Area | Problem | Risk | Fix | Owner | Approval | Task |
|----|------|---------|------|-----|-------|----------|------|
| B21 | Tech | Зависимость от Windows proxy | Не работает на VPS | BOT_PROXY_URL как primary | Codex | YES | — |
| B22 | Docs | AGENT_CONTEXT_HUB без ссылки на hermes_skills | Следующий агент не узнает | Добавить ссылку | Hermes | NO | — |
| B23 | Domain | Нет сайта на домене Beget | Нет публичной витрины | Статический landing | Codex | YES | 015 |
| B24 | Domain | Нет privacy policy на домене | Юридический риск | Разместить policy | Olga/Codex | YES | 015 |
| B25 | Launch | Нет формального launch checklist | Субъективная готовность | Чек-лист с критериями | Hermes | NO | 016 |

## Summary

- **P0:** 4 (B01-B04)
- **P1:** 8 (B05-B12)
- **P2:** 8 (B13-B20)
- **P3:** 5 (B21-B25)
- **Total:** 25
- **Need code:** 18
- **Docs/Hermes:** 7
