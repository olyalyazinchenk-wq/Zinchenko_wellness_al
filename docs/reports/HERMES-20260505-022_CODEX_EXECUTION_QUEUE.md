# Codex Execution Queue — 2026-05-05

## Сейчас (P0 — немедленно)

| # | Task | Why now | Files | Fix | Verify | Live test? |
|---|------|---------|-------|-----|--------|------------|
| 1 | OCR 401 fix | Фото анализов не читаются → клиент без разбора | lab_ocr.py, .env | Проверить STT_API_KEY/STT_PROJECT_ID; diagnose 401 без вывода ключей | Загрузить тестовое фото → biomarkers | Да |
| 2 | OCR fallback texts | Клиент не понимает, почему файл «не читается» | texts.py, main.py | Применить copy proposals из playbook (5 текстов) | Live-test Ольги: плохое фото → сообщение №1 | Да |
| 3 | Canonical path fix | Multi-path drift → путаница | main.py, case_service.py | 1 активный submission на пользователя; archived для старых | Проверить: /start при активном кейсе → follow-up | Да |

## Сегодня (P1 — до первого клиента)

| # | Task | Why now | Files | Fix |
|---|------|---------|-------|-----|
| 4 | Manual override audit trail | Нет accountability при risky delivery | main.py | override_note + override_by + timestamp |
| 5 | sanitize_live_reply hardening | 4 паттерна → модель обходит | ai_drafting.py | +6 обобщённых regex |
| 6 | CONSENT timestamp | Юридическая дыра | main.py | consent_at = utc_now_iso() |
| 7 | Возрастной gate | Риск для детей/подростков | main.py | 1 вопрос в анкете |

## Завтра (P2 — улучшения)

| # | Task | Files | Fix |
|---|------|-------|-----|
| 8 | Демо-пример: сократить + видимость | texts.py | 15 строк, кнопка «Посмотреть пример» первой |
| 9 | Инсайт после анкеты | texts.py | 2 строки в MANUAL_HANDOFF_START_TEXT |
| 10 | Админ-уведомления: judge summary | main.py | Топ-3 проблемы в notify_admins |

## На неделе (P3)

| # | Task |
|---|------|
| 11 | Mini-app cleanup (2990₽ + medical findings) |
| 12 | DOSSIER_DRAFT_PROMPT → русский (Hermes draft → Codex) |
