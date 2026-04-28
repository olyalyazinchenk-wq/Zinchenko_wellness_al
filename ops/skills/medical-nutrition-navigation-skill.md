# Medical Nutrition Navigation Skill

## Objective

Turn symptoms, lifestyle, documents, lab values, and client questions into safe nutrition-navigation output.

This skill does not diagnose, prescribe treatment, or replace a doctor.
It builds a high-quality working map: facts, cautious hypotheses, red flags, doctor route, nutrition/lifestyle support, and what to clarify.

## Use When

- client sends lab values, PDF, photo, or manual biomarkers
- dossier needs interpretation of ferritin, vitamin D, TSH, B12, glucose, HbA1c, or related markers
- symptoms suggest iron, thyroid, cycle, GI, metabolism, skin/photo, or cardiovascular route
- output must feel premium and practical without crossing medical boundaries

## Data Sources

- `WellnessBot/medical_skill_database.py`
- `WellnessBot/data/medical_skill_database.json`
- `WellnessBot/nutrition_reference_ranges.py`
- `docs/LAB_RESULT_SAFETY_POLICY_20260421.md`
- `docs/NUTRITION_NAVIGATION_POLICY_20260420.md`

## Workflow

1. Separate facts, hypotheses, and uncertain data.
2. Read all available files and typed values.
3. For each biomarker, map: marker -> system -> status -> possible meaning -> clarify -> doctor route -> self-action boundary.
4. If a value is suspicious, ask a narrow clarification instead of guessing.
5. If a value is readable and coherent, interpret it without asking unnecessary confirmation.
6. Add doctor questions when medical escalation is relevant.
7. Give action steps that are non-medical: observation, food structure, sleep/stress, safe activity, document preparation.
8. Never prescribe medication, hormones, iron, iodine, selenium, or therapeutic dosages.

## Clarify Only When

- photo/PDF is unreadable or OCR output is inconsistent
- units are missing and the marker requires units
- value is biologically implausible
- marker name could mean two different tests
- result conflicts with symptoms or prior data
- red flag is present

## Output Standard

- one synthesis sentence
- 3 immediate priorities
- marker-by-marker explanation
- what to clarify
- doctor route with concrete questions
- what not to start independently
- 3-day or 14-day plan when part of premium dossier
