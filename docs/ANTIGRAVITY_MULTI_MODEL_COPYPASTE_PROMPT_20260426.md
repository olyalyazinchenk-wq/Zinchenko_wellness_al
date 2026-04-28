# Copy-paste prompt для Antigravity: подключение дополнительных моделей

Скопировать и вставить в Antigravity / новой модели:

```text
Ты подключаешься к проекту Telegram-бота Ольги Зинченко.

Рабочая папка: C:\Users\HP\Desktop\Новая папка

Твоя задача: подключить дополнительные AI-модели в Antigravity через MCP так, чтобы они работали как русскоязычные аудиторы/помощники проекта, не ломая текущий бот и не заменяя human review.

Сначала прочитай:
1. docs/ANTIGRAVITY_MULTI_MODEL_HANDOFF_TZ_20260426.md
2. docs/AGENT_CONTEXT_HUB.md
3. docs/PROJECT_PULSE_LOG.md
4. docs/STRATEGY_LIVE_DELTA.md
5. docs/ANTIGRAVITY_DEEPSEEK_AUDITOR_PROTOCOL_20260425.md
6. docs/PROJECT_SKILL_REGISTRY_20260425.md
7. docs/NUTRITION_NAVIGATION_POLICY_20260420.md
8. docs/LAB_RESULT_SAFETY_POLICY_20260421.md
9. WellnessBot/config.py
10. ops/antigravity_deepseek_mcp.py

Что уже есть:
- DeepSeek v4 подключён как MCP server `deepseek-v4`.
- Tool: `deepseek_v4_chat`.
- MCP config: C:\Users\HP\AppData\Roaming\Antigravity\User\mcp.json
- Ключи читать из .env, не хранить в mcp.json.
- Ответы клиенту и smoke-тесты должны быть только на русском языке.

Что сделать:
1. Не ломая `deepseek-v4`, предложи и реализуй безопасное подключение дополнительных моделей через MCP.
2. Предпочтительно создать единый router `ops/antigravity_model_router_mcp.py` с инструментами list/chat/audit/compare/smoke.
3. Каждая модель должна проходить русский UTF-8 smoke-test.
4. Все новые инструменты должны соблюдать границы проекта: нутрициологическая навигация, не диагноз, не лечение, human review обязателен.
5. Создай отчёт smoke-тестов в `ops/reports`.
6. Создай протокол использования в `docs/ANTIGRAVITY_MULTI_MODEL_PROTOCOL_20260426.md`.
7. Не раскрывай API-ключи и токены.
8. После изменений проверь py_compile, unit tests и статус бота.

Критерий готовности: Antigravity видит новые MCP tools, DeepSeek v4 продолжает работать, новые модели отвечают на русском, секреты не раскрыты, тесты зелёные, документация обновлена.
```
