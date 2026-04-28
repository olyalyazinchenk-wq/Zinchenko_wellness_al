# Post Delivery Support Skill

## Objective

Turn a delivered dossier into guided 30-day client support.

## Use When

- client has received a PDF dossier
- client sends new analyses, photos, questions, or reactions
- bot needs to correct or update the plan after delivery

## Workflow

1. Find active delivered case within 30 days.
2. Save every follow-up message/file/photo to the case.
3. If file is lab data, run lab intake flow.
4. If photo is a visible complaint, ask context and route safely.
5. If question is about an existing doctor prescription, help structure timing/compatibility/observation without changing treatment.
6. If red flag appears, escalate to doctor/emergency route.
7. Keep response warm, specific, and practical.

## Photo Complaint Questions

- Where is it located?
- How long has it been there?
- Is it growing/changing color or shape?
- Pain, itch, bleeding, fever?
- New medicine, supplement, cosmetic, food, travel, injury?

## Boundaries

- Do not diagnose by photo.
- Do not prescribe treatment.
- Do not say "nothing serious" from a photo.
- Do not override a doctor's prescription.

## Code Anchors

- `WellnessBot/main.py::find_active_followup_case`
- `WellnessBot/main.py::append_case_followup`
- `WellnessBot/main.py::build_followup_context`
- `WellnessBot/main.py::handle_document_upload`
- `WellnessBot/main.py::handle_photo_upload`
