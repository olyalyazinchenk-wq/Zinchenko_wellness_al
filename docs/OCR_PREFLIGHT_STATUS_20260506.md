# OCR Preflight Status — 2026-05-06

Статус: auth issue fixed at environment level

## Что проверено

Создан безопасный скрипт:

`ops/yandex_ocr_preflight.py`

Он проверяет Yandex OCR auth/request path на синтетическом 1x1 PNG и не выводит ключи, токены или клиентские данные.

## Результат до обновления IAM

```json
{
  "provider": "yandex_ocr",
  "has_api_key": true,
  "has_project_id": true,
  "uses_iam_token": true,
  "status": "auth_failed",
  "http_status": 401
}
```

Вывод: проблема была не в качестве фото и не в списке маркеров, а в авторизации Yandex OCR.

## Что сделано

- IAM-токен обновлен через Yandex CLI.
- `STT_API_KEY` обновлен в локальных env-файлах без вывода токена.
- Бот перезапущен, чтобы runtime взял новый токен.

## Результат после обновления IAM

```json
{
  "provider": "yandex_ocr",
  "has_api_key": true,
  "has_project_id": true,
  "uses_iam_token": true,
  "status": "auth_path_ok",
  "http_status": 400,
  "note": "Authentication did not fail. Use a real lab file for functional OCR verification."
}
```

`400` на 1x1 PNG допустим для preflight: это означает, что авторизация не провалилась. Для функциональной проверки нужен реальный PDF/фото анализа.

## Следующий шаг

1. Live test: PDF анализа с текстовым слоем.
2. Live test: хорошее фото анализа.
3. Live test: плохое фото анализа.
4. Live test: ручной ввод показателей.
5. Убедиться, что при OCR failure клиент получает fallback, а бот не выдумывает показатели.
