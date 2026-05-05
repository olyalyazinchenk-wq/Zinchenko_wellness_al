# Hermes Task Packet Template

Дата: 2026-05-05
Назначение: шаблон задачи для Гермеса, DeepSeek, Antigravity, Codex-subagent или другой модели.

## Task Metadata

Task ID: `HERMES-YYYYMMDD-001`
Status: `draft | approved | in_progress | blocked | done`
Owner: `Olga | Codex | Hermes`
Agent: `Hermes`
Priority: `P0 | P1 | P2 | P3`
Deadline: `YYYY-MM-DD HH:mm MSK`

## Objective

Кратко: что нужно получить на выходе.

Пример:

`Проверить Telegram-бот на наличие старых текстов, английских фраз и мест, где клиент может получить результат без подтвержденной оплаты.`

## Context To Read First

1. `docs/MODEL_CONTEXT_START_HERE_20260505.md`
2. `docs/PROJECT_DEVELOPMENT_SINGLE_SOURCE_OF_TRUTH.md`
3. `docs/AGENT_CONTEXT_HUB.md`
4. `docs/PROJECT_PULSE_LOG.md` - последние записи
5. Дополнительные документы по задаче:
   - `...`

## Allowed Scope

Можно читать:

- `...`

Можно менять:

- `...`

Нельзя менять:

- `.env`
- `WellnessBot/data/`
- клиентские файлы и загрузки
- платежные настройки
- production/VPS-конфиги
- чужие несвязанные изменения

## Hard Rules

- Работать на русском языке.
- Не раскрывать секреты.
- Не сохранять персональные данные в GitHub/Notion.
- Не ставить диагнозы и не назначать лечение.
- Не менять поведение оплаты/выдачи результата без отдельного approval.
- Если обнаружена критическая проблема, сначала описать ее и предложить безопасный фикс.

## Deliverables

Ожидаемые результаты:

1. `...`
2. `...`
3. `...`

## Acceptance Criteria

Задача считается готовой, если:

- `...`
- `...`
- отчет содержит список измененных файлов;
- отчет содержит остаточные риски;
- нет утечки секретов или персональных данных.

## Verification

Команды/проверки:

```powershell
# пример
python -m pytest
```

Если проверить нельзя, указать почему.

## Final Report Format

1. Что понял
2. Что сделал
3. Измененные файлы
4. Как проверил
5. Найденные риски
6. Что нужно от Ольги/Codex дальше
