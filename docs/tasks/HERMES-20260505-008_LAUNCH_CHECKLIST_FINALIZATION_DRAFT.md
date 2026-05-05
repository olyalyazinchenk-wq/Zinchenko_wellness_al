# HERMES-20260505-008: Launch Checklist Finalization (DRAFT)

Task ID: `HERMES-20260505-008`
Status: `draft`
Owner: `Hermes (аудит) → Codex (исполнение)`
Agent: `Hermes → Codex`
Priority: `P1`
Deadline: `2026-05-08 18:00 MSK`

## Objective

После исправления P0/P1-блокеров провести финальную верификацию pilot-readiness по чек-листу. Зафиксировать результат в `AGENT_CONTEXT_HUB.md`.

## Context

- `docs/reports/HERMES-20260505-003_FULL_LAUNCH_READINESS_AUDIT.md`
- `docs/reports/HERMES-20260505-003_FINDINGS_TABLE.md`

## Launch Checklist

### Critical (P0) — должны быть ВСЕ закрыты

- [ ] F01: Delivery gate работает (judge_verdict блокирует доставку).
- [ ] F02: Multi-path drift устранён (1 канонический путь на пользователя).
- [ ] F03: Mini-app не показывает 2990₽ и medical findings.
- [ ] F04: Бот запущен и стабилен (подтверждён smoke-тестом).

### Important (P1) — должны быть закрыты до первого клиента

- [ ] F05: Manual override audit trail работает.
- [ ] F09: Invoice payload содержит правильный offer_code.
- [ ] F06: DOSSIER_DRAFT_PROMPT на русском.
- [ ] F07/F08: «Premium Wellness Dossier» заменён.
- [ ] F10: sanitize_live_reply расширен.

### Smoke-тест полного цикла

- [ ] /start → витрина → демо (показывается).
- [ ] Выбор 7 дней → анкета (без зависания).
- [ ] Загрузка файлов (принимаются).
- [ ] Плохой файл → запрос переслать (не гадает).
- [ ] Ручная оплата → админ подтверждает.
- [ ] AI draft → judge → growth → PDF.
- [ ] Админ: «Одобрить» при needs_revision → ❌ БЛОКИРУЕТСЯ.
- [ ] Админ: manual override → ✅ доставка с логом.
- [ ] Админ: «Одобрить» при pass → ✅ доставка.
- [ ] Клиент получает PDF + 30 дней follow-up.

## Deliverable

Обновлённый `docs/AGENT_CONTEXT_HUB.md` с вердиктом pilot-ready и списком выполненных критериев.

## Hard Rules

- Не запускать на реальных клиентах до закрытия всех P0.
- Human review обязателен всегда.
