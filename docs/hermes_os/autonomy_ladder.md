# Autonomy Ladder

## Level 0: Read-only Intelligence
- **Можно:** читать проект, анализировать, строить выводы.
- **Нельзя:** создавать/менять любые файлы.
- **Результат:** telegram-ответ с наблюдениями.
- **Approval:** не требуется.

## Level 1: Documentation Operator
- **Можно:** создавать/менять `docs/reports/`, `docs/tasks/`, `docs/hermes_skills/`, `docs/hermes_os/`, чек-листы, backlog.
- **Нельзя:** код, `.env`, клиентские данные, оплата, VPS.
- **Результат:** отчёты, task packets, карты, бэклог.
- **Approval:** task packet `approved`.

## Level 2: Text & UX Implementer
- **Можно:** править клиентские тексты, UX-копирайтинг, тест-кейсы (после approval).
- **Нельзя:** менять логику, безопасность, оплату.
- **Результат:** diff + self-audit + rollback note.
- **Approval:** implementation packet `approved`.

## Level 3: Bounded Code Engineer
- **Можно:** маленькие кодовые изменения по утверждённому implementation packet.
- **Правила:** один packet = один scope, маленький diff, syntax check, smoke test.
- **Нельзя:** менять архитектуру, payment, production без отдельного approval.
- **Approval:** implementation packet + Codex review.

## Level 4: Runtime/Test Operator
- **Можно:** запускать smoke-тесты, проверки по разрешённым командам.
- **Нельзя:** production deploy, VPS, платежи, клиентские действия.
- **Approval:** для production-окружения.

## Level 5: Production/Action Operator
- **Можно:** только отдельный письменный approval на конкретное действие.
- **Approval:** обязателен всегда.
