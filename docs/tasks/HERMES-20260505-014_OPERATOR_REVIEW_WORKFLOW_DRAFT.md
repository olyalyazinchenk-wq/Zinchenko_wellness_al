# HERMES-20260505-014: Operator Review Workflow (DRAFT)
Task ID: `HERMES-20260505-014` | Status: `draft` | Owner: `Codex` | Priority: `P2`
Requires: `Codex/Olga approval`

## Objective
Улучшить админский workflow: добавить контекст в уведомления, улучшить статусы.

## Changes
1. **Админ-уведомление** — топ-3 проблемы из judge-отчёта
2. **Статусы** — вместо `review_priority_quality_and_market` → человекочитаемые
3. **Кнопки** — «Посмотреть judge», «Посмотреть growth», «Одобрить», «На доработку»
4. **Manual override** — отдельная кнопка с обязательным полем причины

## Acceptance
- [ ] Админ видит конкретные проблемы в уведомлении
- [ ] Статусы понятны без расшифровки
- [ ] Manual override логируется
