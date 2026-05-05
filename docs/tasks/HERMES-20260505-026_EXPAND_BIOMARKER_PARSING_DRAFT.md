# HERMES-20260505-026: Expand Biomarker Parsing (DRAFT)
Status: `draft` | Priority: `P1` | Owner: `Codex` | Approval: `Olga ✔`

## Problem
KNOWN_MARKER_ALIASES содержит ~50 маркеров. Показатели вне списка молча отбрасываются. Клиент получает неполную картину.

## Scope
**Можно:** `WellnessBot/lab_ocr.py`, строки 43-95 (KNOWN_MARKER_ALIASES tuple).
**Нельзя:** менять логику парсинга, safety-правила, .env, client data.

## Smallest Safe Patch
1. Открыть lab_ocr.py.
2. Найти `KNOWN_MARKER_ALIASES = (`.
3. Дополнить существующие 50 маркеров полным списком из `docs/reports/EXPANDED_MARKER_LIST_REFERENCE.md`.
4. Сохранить.

**Риск patch'а:** минимальный. Это добавление строк в tuple. Логика `should_skip_ocr_line` не меняется — она работает по тому же принципу `any(alias in normalized for alias in ...)`.

## Verification
1. Загрузить тестовый анализ с 15-20 показателями (включая кальций, калий, магний, фибриноген, тестостерон).
2. Проверить: `parse_biomarkers` возвращает ВСЕ показатели, а не только старые 50.
3. Проверить: старые показатели (ферритин, ТТГ, глюкоза) по-прежнему распознаются.

## Дополнительно
После расширения списка → нужно также добавить DeepSeek-ассистированное извлечение для маркеров, которые не вошли в список (страховка от будущих пропусков).
