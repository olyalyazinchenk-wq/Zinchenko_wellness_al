# Lab File Intake Skill

## Objective

Accept, read, and structure client lab data from PDFs, photos, documents, and manual text.

The goal is accuracy first: no invented values, no blind OCR trust, no unnecessary friction when the lab PDF is clear.

## Use When

- client sends laboratory PDF
- client sends screenshot/photo of lab results
- client types values manually
- bot needs to decide whether to ask clarification

## Workflow

1. Save every client file to the case.
2. If file is PDF, extract embedded text first with `pypdf`.
3. If PDF has no usable text or is scanned, use OCR.
4. If client typed values, parse short manual biomarker text.
5. Enrich recognized markers with nutrition reference overlays.
6. Ask clarification only when data quality is unsafe.
7. If data is clear, proceed to interpretation.
8. Store uncertainty flags in the case so the dossier can treat questionable data cautiously.

## Clarification Triggers

- OCR failed or returned empty text
- too few numeric lines
- replacement characters or broken text
- no clear biomarker lines
- unclear unit for unit-sensitive marker
- implausible value
- duplicate/conflicting values for the same marker

## Client Message Pattern

If unclear:

> Я не буду строить выводы по этому показателю, потому что он читается неуверенно. Пришлите, пожалуйста, PDF/чёткое фото или напишите показатель вручную.

If clear:

> Показатели прочитаны и сохранены. Я буду использовать их в разборе вместе с симптомами, жалобами и фоном.

## Code Anchors

- `WellnessBot/lab_ocr.py`
- `WellnessBot/main.py::process_ocr_background`
- `WellnessBot/case_service.py`
