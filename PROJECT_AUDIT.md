# Project Audit

Date: 2026-04-12
Owner: Codex acting as interim chief engineer, product lead, and execution manager

## Executive Summary

The current project is not yet a production product. It is an early prototype made of:

- a static promo/demo frontend in `index.html`, `app.js`, and `styles.css`
- a skeletal Telegram bot in `WellnessBot/main.py`
- prompt stubs in `WellnessBot/prompts.py`

There is no real backend, no persistent storage, no payments, no CRM layer, no document parsing pipeline, no AI orchestration, no auth, and no deployment setup. The concept is promising, but the implementation is still pre-MVP.

## What Exists Right Now

### Frontend

Files:

- `C:\Users\HP\Desktop\Новая папка\index.html`
- `C:\Users\HP\Desktop\Новая папка\app.js`
- `C:\Users\HP\Desktop\Новая папка\styles.css`

Current status:

- static landing and dashboard mockup
- client flow is visual only
- expert dashboard is visual only
- no real upload handling
- no API integration
- no form submission or storage

Main issues:

- text encoding is broken and rendered as mojibake in multiple places
- styles are duplicated between inline CSS in `index.html` and `styles.css`
- `app.js` duplicates view content that also exists in `index.html`
- UI suggests product capability that does not exist yet

### Telegram Bot

Files:

- `C:\Users\HP\Desktop\Новая папка\WellnessBot\main.py`
- `C:\Users\HP\Desktop\Новая папка\WellnessBot\prompts.py`
- `C:\Users\HP\Desktop\Новая папка\WellnessBot\requirements.txt`

Current status:

- `/start` command exists
- three user branches are mocked via inline buttons
- bot token is a placeholder
- prompts are imported but not actually used to call any model
- no file handling for PDF uploads
- no OpenAI integration despite dependency being listed

Main issues:

- `BOT_TOKEN` is hardcoded placeholder, so the bot cannot run as-is
- there is no state machine for intake, consent, uploads, or report generation
- there is no safety gating for health-related guidance
- there is no data retention, privacy, or audit model

## Product Truth

The real product idea appears to be:

- premium AI-assisted wellness case intake
- lab interpretation and symptom-based case structuring
- Olga-led expert output with a premium feel
- likely delivery through Telegram first

That is viable as a business direction, but the current implementation is only a concept demo and should be treated as such.

## Critical Risks

### Product Risk

- There is no sharply defined paid offer yet.
- The code mixes three different offers and audiences without one core wedge.
- The UI presents an illusion of completion that can mislead stakeholders.

### Medical and Legal Risk

- The current prompts move close to diagnosis and treatment language.
- Telegram plus lab analysis implies sensitive health data processing.
- Consent, disclaimers, escalation rules, and storage policy are missing.

### Engineering Risk

- No source control detected in current shell environment.
- No runtime toolchain detected for Node or normal Python execution.
- No environment variable handling.
- No deployment target or operational environment is defined.

### Commercial Risk

- No pricing architecture
- No conversion funnel
- No retention loop
- No measurable unit economics

## Maturity Assessment

Current maturity by area:

- product strategy: 3/10
- UX prototype: 4/10
- backend: 1/10
- AI pipeline: 1/10
- Telegram automation: 2/10
- operations: 1/10
- monetization readiness: 2/10

Overall status:

Pre-MVP concept stage.

## Recommended Immediate Positioning

Do not frame this as a finished AI health product yet.

Frame it as:

"Premium AI-assisted intake and dossier assembly for Olga's expert wellness practice, with human-in-the-loop review."

That framing is safer, more honest, and more implementable.

## Immediate Priorities

1. Lock the product thesis and paid offer.
2. Decide the first narrow customer segment.
3. Build a real intake-to-report pipeline.
4. Add human review before any client-facing output.
5. Prepare Telegram bot only after the internal operating flow is defined.
