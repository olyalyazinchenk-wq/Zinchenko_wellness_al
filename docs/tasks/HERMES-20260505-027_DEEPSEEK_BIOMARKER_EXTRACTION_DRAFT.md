# HERMES-20260505-027: DeepSeek Biomarker Extraction (DRAFT)
Status: `draft` | Priority: `P2` | Owner: `Codex` | Approval: `Olga ✔`

## Problem
Текущая система использует жёсткий детерминированный парсинг. Маркеры вне KNOWN_MARKER_ALIASES теряются. 100% покрытие невозможно через статический список — лаборатории используют разные формулировки.

## Solution
Добавить AI-assisted biomarker extraction как второй проход:
1. Первый проход (текущий): детерминированный парсинг через KNOWN_MARKER_ALIASES.
2. Второй проход (новый): отдать OCR-текст DeepSeek с промптом «извлеки все показатели из этого текста и верни JSON».

## Smallest Safe Patch
**Файл:** `WellnessBot/lab_ocr.py`

```python
async def extract_biomarkers_via_ai(raw_text: str, settings: Settings) -> list[dict]:
    """AI-assisted extraction: catches biomarkers missed by deterministic parsing."""
    if not raw_text or not settings.llm_api_key:
        return []

    prompt = """Извлеки все лабораторные показатели из текста ниже.
Верни JSON-массив: [{{"name": "название", "value": число, "unit": "единица"}}]
Если показатель не содержит единицу, верни unit: null.
Не выдумывай значения. Если показатель не читается — не включай.

Текст:
""" + raw_text

    try:
        from openai import OpenAI
        client = OpenAI(api_key=settings.llm_api_key, base_url=settings.llm_base_url)
        response = client.chat.completions.create(
            model=settings.llm_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=2000,
        )
        text = response.choices[0].message.content
        # Strip JSON fences if any
        import re
        clean = re.sub(r"^```(?:json)?\s*", "", text.strip(), flags=re.IGNORECASE)
        clean = re.sub(r"\s*```$", "", clean)
        return json.loads(clean)
    except Exception:
        logger.exception("AI biomarker extraction failed")
        return []
```

**Интеграция:** в `parse_biomarkers` после детерминированного парсинга (строка 353):
```python
biomarkers = enrich_biomarkers_with_nutrition_ranges(extract_biomarkers_from_text(raw_text))
ai_biomarkers = await extract_biomarkers_via_ai(raw_text, settings)
# Merge: deterministic results override AI for duplicate marker names
all_markers = merge_biomarkers(biomarkers, ai_biomarkers)
```

**merge_biomarkers:** deterministic результаты приоритетнее (они уже в nutrition_ranges). AI-результаты добавляются только для маркеров, которых нет в deterministic.

## Safety
- AI extraction НЕ заменяет safety-проверки.
- Если AI не распознал → пустой список, не ошибка.
- Во всех промптах: «не выдумывай значения».
- Температура 0.1 → минимальная креативность.

## Verification
- Загрузить анализ с редкими маркерами (кремний, бор, ванадий) → AI их найдёт.
- Загрузить стандартный анализ → AI повторит deterministic, не создав дубликатов.
