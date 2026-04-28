# Project Skill Registry

Date: 2026-04-25

This registry collects reusable skills created during the project so future work does not restart from zero.

## Active Skills

| Skill | Purpose | Main Files |
|---|---|---|
| Agency Orchestrator | Coordinate roles, priorities, and execution | `ops/skills/agency-orchestrator-skill.md` |
| Loop Breaker | Stop repeated low-yield attempts and force diagnosis | `ops/skills/loop-breaker-skill.md` |
| Medical Nutrition Navigation | Interpret symptoms/labs safely as nutrition navigation | `ops/skills/medical-nutrition-navigation-skill.md`, `WellnessBot/medical_skill_database.py` |
| Lab File Intake | Read PDFs/photos/manual lab values and manage uncertainty | `ops/skills/lab-file-intake-skill.md`, `WellnessBot/lab_ocr.py` |
| Premium Dossier Product | Keep paid PDF specific, premium, and actionable | `ops/skills/premium-dossier-product-skill.md` |
| Critical Auditor | Find safety, product, market, and launch weaknesses | `ops/skills/critical-auditor-skill.md` |
| Commercial Growth | Protect offer, pricing, conversion, retention | `ops/skills/commercial-growth-skill.md` |
| Post Delivery Support | Run 30-day support after dossier delivery | `ops/skills/post-delivery-support-skill.md` |
| Pain Resonance Copywriter | Write high-conversion Russian wellness content | `ops/skills/pain-resonance-copywriter-skill.md` |
| Premium Design | Keep visuals and UX expensive, calm, non-template | `ops/skills/premium-design-skill.md` |
| Telegram Content Ops | Plan and operate Telegram content rhythm | `ops/skills/telegram-content-ops-skill.md` |

## Machine-Usable Knowledge

| Artifact | Purpose |
|---|---|
| `WellnessBot/medical_skill_database.py` | Structured marker/symptom skill DB used by dossier generation |
| `WellnessBot/data/medical_skill_database.json` | Exported JSON snapshot of the skill DB |
| `WellnessBot/supplement_product_catalog.py` | Structured Siberian Wellness / Vitamax product catalog with safety boundaries |
| `WellnessBot/data/supplement_product_catalog.json` | Exported JSON product catalog |
| `WellnessBot/nutrition_reference_ranges.py` | Nutrition reference overlays for key markers |
| `WellnessBot/helix_master_catalog.py` | Helix catalog metadata and nutrition overlay bridge |

## Operating Rule

Every important new discovery should become one of:

- a code rule,
- a test,
- a project skill,
- a client-facing template,
- or a launch/governance checklist.

If it remains only in chat, it is not yet operational knowledge.

## Next Skills To Add

- Payment/YooKassa operations skill.
- VPS/hosting production operations skill.
- Admin human-review skill.
- Review reply and reputation management skill.
- DeepSeek/Yandex cost-control skill.
