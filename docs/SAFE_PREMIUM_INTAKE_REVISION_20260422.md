# Safe Premium Intake Revision - 2026-04-22

## Why This Revision Exists

The previous bot flow was technically working, but the intake was too short for a premium ?????????????????? ??????.

A short intake can make the dossier look polished while missing the real context behind the client's complaints. That is commercially dangerous, medically risky, and weak for a premium product.

## Weak Spots Found

### 1. Too Few Intake Questions

Old flow collected:

- name,
- age,
- city,
- symptoms,
- goal,
- background,
- red flags,
- labs.

This is not enough to responsibly connect complaints, nutrition, lifestyle, labs, supplements, and risks.

### 2. Nutrition Was Mentioned But Not Collected

The prompt expected nutrition context, but the bot did not explicitly ask about a normal eating day, water, caffeine, alcohol, restrictions, or food reactions.

### 3. ??? Was Not Collected Separately

For wellness/nutrition work, digestion is often central. It should not be hidden inside a free-form symptoms field.

### 4. Sleep, Stress, And Activity Were Missing

Without sleep, stress, recovery, and movement context, the bot may over-focus on supplements and labs while missing obvious load factors.

### 5. Medication / Supplement Safety Was Too Compressed

The old background question asked about diagnoses, medicines, and supplements together. For a safe product, this information must be captured clearly enough to prevent risky supplement suggestions.

### 6. Medication Prescribing Boundary Needed To Be Sharper

The product must not prescribe medications, medication dosages, treatment schemes, or medical therapy. It can only suggest that medication questions are discussed with a doctor.

## Implemented Solution

The Telegram intake is now a 12-step premium questionnaire:

1. Name.
2. Age.
3. City / time zone.
4. Main complaints.
5. Complaint dynamics and triggers.
6. Desired result for 4-8 weeks.
7. Normal eating day and food reactions.
8. Digestion / ??? context.
9. Sleep, stress, and recovery.
10. Activity and movement limitations.
11. Chronic background, operations, allergies, pregnancy / breastfeeding, children / teenagers, oncology, medicines, supplements, dosages.
12. Red flags requiring medical escalation.

After that the client can upload labs or continue without labs.

## Safety Rules Reinforced

The dossier prompt now explicitly says:

- do not prescribe medications,
- do not provide medication dosages,
- do not create treatment protocols,
- medication questions must be discussed with a doctor,
- supplements are only wellness support, not treatment,
- supplement dose guidance must be conservative and label-aligned,
- if context is insufficient or risky, do not suggest supplements.

## Product Decision

The bot is not a doctor and not a medication-prescribing tool.

The correct product role is:

- collect a strong structured case,
- build a whole-picture ?????????????????? hypothesis map,
- analyze complaints, lifestyle, nutrition, labs, and risks,
- suggest next reasonable steps,
- give cautious supplement orientation only when appropriate,
- escalate red flags and high-risk cases to a doctor,
- keep human expert review before delivery.

## Files Changed

- `WellnessBot/main.py`
- `WellnessBot/case_service.py`
- `WellnessBot/prompts.py`
- `tests/test_payment_case_services.py`

## Verification

- `py_compile`: passed.
- Unit tests: 24 tests OK.
- Payment/case smoke: SMOKE_OK.
- Admin/governance smoke: SMOKE_OK.
