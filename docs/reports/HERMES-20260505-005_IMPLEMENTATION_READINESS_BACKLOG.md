# HERMES-20260505-005: Implementation Readiness Backlog

| ID | Problem | P | Ready | Missing Approval | Level | Smallest Patch | Files | Verification | Risk | Owner |
|----|---------|---|-------|------------------|-------|----------------|-------|-------------|------|-------|
| IR01 | Delivery gate bypass | P0 | YES | YES | 3 | 15 строк guard перед delivery | main.py:1810 | Ручной: отправить досье с needs_revision → блок | Сломать существующие кейсы | Codex |
| IR02 | «Premium Wellness Dossier» → русский | P1 | YES | YES | 2 | 3 замены в ai_drafting.py | ai_drafting.py:91,151,329 | Поиск: нет "Premium Wellness" | Минимальный | Codex/Hermes |
| IR03 | invoice_payload хардкод "premium:" | P1 | YES | YES | 3 | 1 параметр в build_invoice_payload | payment_flow.py:57,91 | Создать week-кейс → проверить префикс | Сломать existing invoices | Codex |
| IR04 | Mini-app: 2990₽ + medical findings | P0 | YES | YES | 3 | Удалить хардкод, placeholder | mini-app/index.html | Визуально: нет 2990₽, нет диагнозов | Сломать вёрстку | Codex |
| IR05 | sanitize_live_reply: 4→10 паттернов | P1 | YES | YES | 3 | Добавить 6 обобщённых regex | ai_drafting.py:361 | Тест: «у вас анемия» → «похоже на...» | False positives | Codex |
| IR06 | DOSSIER_DRAFT_PROMPT → русский | P1 | NO | YES | 2 | Перевод 170 строк (Hermes draft) | prompts.py:232-402 | Модель выдаёт русский JSON | Сломать JSON-структуру | Hermes→Codex |
| IR07 | CONSENT без timestamp | P1 | YES | YES | 3 | consent_at = utc_now_iso() | main.py (consent handler) | Проверить submission JSON | Минимальный | Codex |
| IR08 | CTA_DEFAULT_TEXT → русский | P1 | YES | YES | 2 | 3 строки в ai_drafting.py | ai_drafting.py:151 | Поиск: нет английского | Минимальный | Hermes |
| IR09 | Демо-пример: сократить | P2 | YES | NO | 2 | Сократить texts.py:32-61 до 15 строк | texts.py | Визуально: ≤ 15 строк | Потеря смысла | Hermes |
| IR10 | После анкеты — инсайт | P2 | NO | NO | 2 | 2 строки в MANUAL_HANDOFF_START_TEXT | texts.py:112 | Клиент видит ценность кейса | Переобещание | Hermes |
| IR11 | Админ-уведомление: топ-3 проблемы | P2 | YES | YES | 3 | Выжимка из judge в notify_admins | main.py:2276 | Админ видит конкретные проблемы | Длинное сообщение | Codex |
| IR12 | Возрастной gate в анкете | P1 | YES | YES | 3 | 1 вопрос: «Есть ли вам 18?» | main.py (intake handler) | Пройти анкету с ответом «нет» | Отсечь реальных клиентов | Codex |
| IR13 | Статусы review_priority_* → читаемые | P2 | YES | YES | 3 | Человекочитаемые статусы | main.py:2254 | Админ понимает статус без расшифровки | Сломать фильтры | Codex |

**Всего:** 13 задач
- Ready for implementation: 11 (IR01-05, IR07-08, IR11-13)
- Need Hermes draft first: 2 (IR06, IR09-10)
- Missing approval: 10
- Recommended Hermes Level 2: 4 (IR02, IR08-10)
- Recommended Codex Level 3: 9 (IR01, IR03-05, IR07, IR11-13)
