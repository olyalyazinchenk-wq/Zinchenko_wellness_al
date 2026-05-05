# Быстрый вход в проект для Obsidian

Дата: 2026-05-05

Этот файл - зеркало для Obsidian. Главные документы:

- `../MODEL_CONTEXT_START_HERE_20260505.md`
- `../HERMES_PROJECT_WORKER_PROTOCOL_20260505.md`
- `../templates/HERMES_TASK_PACKET_TEMPLATE_20260505.md`
- `../PROJECT_DEVELOPMENT_SINGLE_SOURCE_OF_TRUTH.md`
- `../AGENT_CONTEXT_HUB.md`
- `../PROJECT_PULSE_LOG.md`
- `../DOMAIN_SITE_MINIAPP_STRATEGY_20260505.md`

Коротко: GitHub/docs - источник правды, Notion - панель навигации, Obsidian - удобное локальное чтение, `.env` - только секреты, клиентские данные - только локально и приватно.

Hermes подключается как доверенный локальный исполнитель: читает context pack, берет утвержденный task packet, выполняет, отчитывается, не трогает секреты и клиентские данные.
