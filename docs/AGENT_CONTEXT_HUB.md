# Agent Context Hub

## Mission
Build a premium Telegram-first wellness product:
- Wellness Clarity in Telegram
- Premium Wellness Dossier as monetization layer

## Current Stage
Execution stage: stable live dialogue quality + premium conversion bridge.

## Already Delivered
- Removed dead-end refusal replies in benchmark path
- Added conversion CTA in live dialogue
- Added direct intake trigger from phrase: "хочу разбор"
- Aligned mini-app to single-path flow (legacy branches removed)

## Current Quality Snapshot
- Report: `ops/reports/quality_report_20260413T094502Z.md`
- Empty replies: 0/20
- Refusal replies: 0/20
- Premium CTA mentions: 15/20

## System Context
- Core files: `WellnessBot/main.py`, `WellnessBot/ai_drafting.py`
- Active automations (12h):
  - `antigravity-knowledge-sync`
  - `antigravity-strategy-refresh`

## What A New Model Should Read First
1. `docs/AGENT_CONTEXT_HUB.md`
2. Latest entry in `docs/PROJECT_PULSE_LOG.md`
3. Latest benchmark in `ops/reports/`

## Next Priorities
- Add payment-ready handoff after intake
- Improve CTA precision by intent
- Keep quality stable while increasing conversion

## Constraint
Do not reintroduce legacy multi-tier branch logic.
