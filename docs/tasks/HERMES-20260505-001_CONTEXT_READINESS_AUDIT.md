# HERMES-20260505-001: аудит готовности Гермеса и проектного контекста

Task ID: `HERMES-20260505-001`
Status: `approved`
Owner: `Codex`
Agent: `Hermes`
Priority: `P1`
Deadline: `2026-05-06 12:00 MSK`

## Objective

Проверить, достаточно ли созданной базы контекста, чтобы Hermes мог войти в проект без лишних вопросов и выполнять задачи как рабочий агент разработки.

## Context To Read First

1. `docs/MODEL_CONTEXT_START_HERE_20260505.md`
2. `docs/HERMES_PROJECT_WORKER_PROTOCOL_20260505.md`
3. `docs/templates/HERMES_TASK_PACKET_TEMPLATE_20260505.md`
4. `docs/templates/HERMES_BOOTSTRAP_PROMPT_20260505.md`
5. `docs/PROJECT_DEVELOPMENT_SINGLE_SOURCE_OF_TRUTH.md`
6. `docs/AGENT_CONTEXT_HUB.md`
7. последние записи `docs/PROJECT_PULSE_LOG.md`

## Allowed Scope

Можно читать:

- `docs/`
- `WellnessBot/` только для понимания архитектуры, без изменения кода
- `ops/` только для понимания запуска/проверок

Можно менять:

- ничего в первом прогоне; это read-only аудит.

Нельзя менять:

- `.env`
- `WellnessBot/data/`
- клиентские файлы, PDF, фото, голосовые, выписки
- платежные настройки
- production/VPS-конфиги
- код бота
- Git history

## Hard Rules

- Работать на русском языке.
- Не печатать секреты, даже если они обнаружены.
- Не копировать персональные данные в отчет.
- Не предлагать медицинские назначения.
- Не запускать deploy и не менять runtime.

## Deliverables

1. Короткий вердикт: готов ли Hermes к работе по этой базе.
2. Список недостающих документов/разделов, если чего-то не хватает.
3. Список 5-10 лучших задач, которые Hermes может безопасно выполнять дальше.
4. Риски: где Hermes может навредить проекту, если дать слишком широкие права.
5. Рекомендация по следующему уровню доступа Hermes.

## Acceptance Criteria

Задача готова, если Hermes:

- не задает общие вопросы по проекту;
- показывает, что понял текущий этап controlled concierge pilot;
- различает GitHub/Notion/Obsidian/.env/client data;
- понимает, что клиентская выдача требует safety review и human review;
- предлагает конкретные следующие задачи без нарушения границ.

## Final Report Format

1. Что понял
2. Вердикт по готовности
3. Что не хватает
4. Безопасные задачи для Hermes
5. Риски
6. Рекомендуемый следующий шаг
