# Pilot Proof Bundle — 2026-05-30

Статус: partial pass
Цель: прекратить стратегический цикл без доказательств и зафиксировать проверяемые факты.

## 1. Инфраструктура

### Диск

До очистки:

- `C:` свободно около `4.33 GB`.
- Это ниже рабочего минимума `10 GB`.

Действия:

- очищены временные Chrome-профили и кэши в `C:\tmp`;
- очищен пользовательский `AppData\Local\Temp`;
- удалены только очевидные дубликаты установщиков из `Downloads`:
  - `Antigravity (1).exe`;
  - `Antigravity (2).exe`;
  - `VSCodeUserSetup-x64-1.119.0 (1).exe`;
  - `setup-Happ.x64 (2).exe`.

После очистки:

- `C:` свободно `10532077568` bytes по `Get-PSDrive`, то есть выше 10 GB в Windows-выводе.

### Proxy

Проверка портов:

- `127.0.0.1:10808` открыт;
- `127.0.0.1:12334` закрыт;
- `127.0.0.1:7890` закрыт;
- `127.0.0.1:8080` закрыт;
- `127.0.0.1:1080` закрыт.

Текущая настройка:

- `.env`: `BOT_PROXY_URL=http://127.0.0.1:10808`;
- `WellnessBot/.env`: `BOT_PROXY_URL=http://127.0.0.1:10808`.

Решение на сейчас:

- proxy `10808` считаем рабочим текущим runtime-путем;
- не переносим на другой порт без отдельного proof.

## 2. Runtime

Бот запущен через штатный скрипт:

- `ops/bot-restart.ps1`.

Свежий лог:

- `2026-05-30 17:39:39` — конфиг: proxy `http://127.0.0.1:10808`, model `deepseek-v4-flash`;
- `2026-05-30 17:39:40` — `Starting Wellness Bot`;
- `2026-05-30 17:39:40` — `Start polling`;
- `2026-05-30 17:39:40` — polling запущен для `@zinchenko_wellness_ai_1_bot`.

Процессы:

- venv process: `.venv\Scripts\python.exe WellnessBot\main.py`;
- child/external process: `Python312\python.exe WellnessBot\main.py`.

Вывод:

- текущий runtime proof положительный;
- старая ошибка `ProxyConnectionError` от 2026-05-27 больше не является последним состоянием.

## 3. Исправленные причины падения тестов

### OCR false positive

Проблема:

- OCR-парсер стал слишком мягким и мог принять строку с ФИО/возрастом как биомаркер.

Исправление:

- усилен фильтр служебных строк через `LAB_HEADER_STOPWORDS`;
- строки с `жен`, `муж`, `лет` больше не проходят как названия показателей.

Проверка:

- `test_extract_biomarkers_ignores_pdf_service_lines` теперь проходит.

### Case roundtrip schema

Проблема:

- `case_service.py` потерял часть старых полей анкеты при сохранении/восстановлении кейса;
- тест ловил потерю `work_lifestyle`.

Исправление:

- восстановлена совместимость полей `wellbeing_energy`, `complaint_pattern`, `goal`, `goals`, `work_lifestyle`, `activity`, `hormonal_reproductive_context`, `emotional_stress`, `risk_details`, `motivation`;
- `build_session_from_submission()` теперь читает `goal` или `goals`.

Проверка:

- `test_case_service_roundtrip_and_enrichment` теперь проходит.

## 4. Тесты и smoke

Пройдено:

- `tests/test_lab_ocr_safety.py`;
- `tests/test_nutrition_reference_ranges.py`;
- `tests/test_payment_case_services.py`;
- `tests/test_review_reply_logic.py`;
- `tests/test_live_reply_routing.py`.

Результат:

- `31 passed, 5 subtests passed`.

Smoke:

- `ops/payment_case_smoke.py` -> `SMOKE_OK`;
- `ops/admin_governance_smoke.py` -> `SMOKE_OK`.

## 5. Что еще не закрыто

Этот proof bundle не означает public launch.

Открытые блокеры:

1. Один пользователь все еще имеет несколько исторических и live-relevant submission.
2. Нужно классифицировать ветки:
   - canonical;
   - merge-into-canonical;
   - parked;
   - archive.
3. Нужно выбрать активный коммерческий вход: рекомендация — `week` за 1 000 руб. как единственный вход пилота.
4. Нужно решить, что делать с premium-ветками того же пользователя.
5. Нужно создать один эталонный демо-результат для клиента.
6. Нужно пройти live e2e в Telegram после текущего runtime proof.
7. Нужно перевыпустить секреты, которые ранее попали в выводы терминала, до реального публичного запуска.

## 6. Следующий шаг

Следующий шаг proof bundle:

`canonical-case collapse`.

Задача:

- выбрать один канонический кейс;
- классифицировать остальные ветки;
- не запускать новые продукты и не расширять mini-app, пока эта классификация не зафиксирована.

Критерий завершения:

- в документации и данных есть один понятный активный путь клиента;
- все остальные ветки имеют статус `merge`, `parked` или `archive`;
- после этого можно делать live e2e.