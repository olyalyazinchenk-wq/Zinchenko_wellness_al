# HERMES-20260505-013: Lab File Handling Audit (DRAFT)
Task ID: `HERMES-20260505-013` | Status: `draft` | Owner: `Hermes (audit) → Codex` | Priority: `P2`

## Objective
Проверить полный цикл работы с лабораторными файлами: OCR → интерпретация → safety gate.

## Scope (read-only audit)
- `WellnessBot/lab_ocr.py` — OCR и парсинг
- `WellnessBot/ai_drafting.py` — использование biomarkers в досье
- `docs/LAB_RESULT_SAFETY_POLICY_20260421.md`

## Проверить
1. При плохом качестве — просит переслать, а не гадает?
2. `requires_lab_resubmission == true` → biomarkers не используются?
3. `lab_quality_check.status != "ok"` → не строятся выводы?
4. OCR-шум фильтруется?
5. Не придумываются единицы измерения?

## Deliverable
Аудит-отчёт с конкретными находками (файл + строка).
