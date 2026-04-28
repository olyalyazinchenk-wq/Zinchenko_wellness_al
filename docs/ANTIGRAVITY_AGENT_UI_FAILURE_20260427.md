# Antigravity agent UI failure report

Дата: 2026-04-27

## Симптом

Antigravity запускается и открывает проект `C:\Users\HP\Desktop\Новая папка`, но агентский/Launchpad UI не работает корректно.

Главная ошибка в `renderer.log`:

```text
[createInstance] ... depends on UNKNOWN service agentSessions.
```

Также повторяются ошибки:

```text
[google.antigravity]: Элемент меню ссылается на команду `antigravity.importAntigravitySettings`, которая не определена в разделе commands.
[google.antigravity]: Элемент меню ссылается на команду `antigravity.importAntigravityExtensions`, которая не определена в разделе commands.
[google.antigravity]: Элемент меню ссылается на команду `antigravity.prioritized.chat.open`, которая не определена в разделе commands.
```

## Проверенные факты

- Авторизация Antigravity проходит: `Auth state changed to: signedIn`.
- Языковой сервер Antigravity стартует.
- Проект открывается.
- MCP config находится в `C:\Users\HP\AppData\Roaming\Antigravity\User\mcp.json`.
- MCP server `deepseek-v4` локально регистрирует tool `deepseek_v4_chat`.
- Ошибка возникает до нормального использования MCP.

## Что уже сделано

1. Проверен запуск текущей установки.
2. Проверены логи Antigravity.
3. Исправлен `mcp.json`: короткий DOS-путь заменён на полный путь проекта.
4. Проверен MCP script напрямую через JSON-RPC `initialize` и `tools/list`.
5. Проверен запуск на `ru` и `en-US`.
6. Проверен запуск в новом профиле Antigravity.
7. Проверен запуск во временном чистом `user-data-dir`.
8. Выполнена переустановка Antigravity `1.23.2` через winget.
9. Выполнен откат на Antigravity `1.22.2` через winget.
10. Проверен запуск с отключённым `github.copilot-chat`.

## Вывод

Проблема не в проекте, не в `.env`, не в MCP config, не в русской локали и не в пользовательском профиле.

Ошибка воспроизводится даже на чистом `user-data-dir`, поэтому наиболее вероятная причина - баг или несовместимость самой Windows-сборки Antigravity на этой машине.

## Текущий статус проекта

Telegram-бот проекта запускается отдельно от Antigravity. В логах бота есть независимые runtime-проблемы:

- периодические ошибки прокси `127.0.0.1:12334`;
- ошибка Telegram `Bad Request: message is too long` при отправке product digest администратору.

Эти ошибки не являются причиной падения агентского UI Antigravity.

## Следующие варианты

1. Отправить этот отчёт в поддержку Antigravity: `https://antigravity.google/support`.
2. Временно выполнять задачи проекта через Codex/PowerShell, а Antigravity использовать только как редактор.
3. Позже повторно попробовать обновление Antigravity, когда winget покажет версию выше `1.23.2`.
4. Если нужна именно агентская работа сейчас, использовать другой IDE/agent runtime до исправления Antigravity.
