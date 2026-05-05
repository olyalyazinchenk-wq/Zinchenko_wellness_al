# HERMES-20260505-016: Pilot Launch Checklist (DRAFT)
Task ID: `HERMES-20260505-016` | Status: `draft` | Owner: `Hermes → Codex/Olga` | Priority: `P2`

## Objective
Формализовать критерии готовности к controlled concierge pilot.

## Critical (все должны быть ДА)
- [ ] Delivery gate: judge_verdict блокирует доставку
- [ ] Бот запущен и стабилен 24ч+
- [ ] Mini-app без 2990₽ и medical findings
- [ ] 1 канонический путь на пользователя
- [ ] Human review обязателен перед delivery
- [ ] Русский язык во всех клиентских текстах
- [ ] Цены везде 3900/6900/14900

## Important (≥80% ДА)
- [ ] Manual override с audit trail
- [ ] sanitize_live_reply ≥10 паттернов
- [ ] CONSENT с timestamp
- [ ] Возрастной gate в анкете
- [ ] Демо-пример ≤15 строк, виден сразу
- [ ] Privacy policy на домене
- [ ] Invoice payload без хардкода

## Smoke-тест
- [ ] /start → демо → 7д → анкета → оплата → AI → judge → human review → delivery
- [ ] Плохой файл → запрос переслать
- [ ] needs_revision → БЛОКИРОВКА доставки
- [ ] manual_override → доставка с логом
- [ ] 30 дней follow-up работает
