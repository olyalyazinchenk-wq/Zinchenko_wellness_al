# HERMES-20260505-024: OCR File Fallback Fix (DRAFT)
Status: `draft` | Priority: `P0` | Owner: `Codex`

## Problem
Yandex OCR возвращает 401 Unauthorized. Нет понятного fallback-сообщения клиенту.

## Scope
**Можно:** `WellnessBot/lab_ocr.py`, `WellnessBot/main.py`, `WellnessBot/texts.py`.
**Нельзя:** `.env` (не выводить ключи), client data.

## Smallest Safe Patch
1. Diagnose 401: проверить `STT_API_KEY`, `STT_PROJECT_ID` без вывода значений.
2. Добавить 5 fallback-сообщений в texts.py (из playbook).
3. В main.py: при `recognize_text → None` → отправить соответствующий fallback.

## Verification
- Плохое фото → сообщение №1.
- Техническая ошибка → сообщение №2.
- Частичное распознавание → сообщение №3.
