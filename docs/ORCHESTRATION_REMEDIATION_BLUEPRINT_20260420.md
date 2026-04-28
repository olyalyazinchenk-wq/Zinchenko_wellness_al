# Orchestration Remediation Blueprint

Date: 2026-04-20
Owner: Codex acting as architecture and process orchestrator

## 1. Verdict

The project is no longer pre-MVP.
It is an uneven but real human-in-the-loop premium wellness product with:

- working Telegram intake,
- payment path,
- AI draft / judge / growth / governance loops,
- admin operating commands,
- local storage and PDF delivery.

The core problem is no longer "does anything exist?"
The core problem is:

`the internal intelligence layer is growing faster than security, compliance, data architecture, and external market proof.`

## 2. Strategic Diagnosis

### Strengths

- sharp initial product wedge: Telegram-first wellness clarity -> premium dossier
- strong human-in-the-loop posture
- unusually advanced internal governance for an MVP
- good language safety in prompts
- good momentum and execution speed

### Weaknesses

- source-of-truth drift across docs and mirrors
- local JSON + workstation-centric architecture for sensitive data
- monolithic `main.py`
- weak external market proof compared to internal orchestration sophistication
- public content CTA was too open to sensitive-data leakage

### Main Risk

The project can become over-optimized internally before it proves repeatable paid demand externally.

## 3. North Star For The Next Stage

The next stage is not "add more AI features."

The next stage is:

`secure, legally disciplined, revenue-proving delivery engine for one premium Telegram offer.`

## 4. Priority Stack

### P0: Must Be Stabilized Before Broader Rollout

1. data protection for Telegram/TMA/client materials
2. payment verification and operational trust
3. client-facing wording aligned with non-medical positioning
4. durable storage behavior for governance and case files

### P1: Must Be Rebuilt For Scale

1. split `main.py` into product modules
2. introduce one source of truth for case lifecycle
3. create explicit analytics and funnel instrumentation
4. redesign OCR/Vision pipeline around structured outputs

### P2: Growth And Scale

1. external acquisition model
2. retention / follow-up ladder
3. referral loop
4. operator dashboard and CRM discipline

## 5. Execution Roadmap

### Track A: Security And Compliance

1. keep TMA disabled by default until protected transport and auth are production-ready
2. define retention policy for submissions, uploads, drafts, governance, and mirrors
3. remove uncontrolled data duplication paths
4. move all public CTAs to DM-first for sensitive health context

### Track B: Architecture

1. split bot runtime into:
   - `intake_service`
   - `case_service`
   - `governance_service`
   - `render_service`
   - `tma_service`
2. replace ad-hoc JSON concurrency with durable storage
3. add schemas for AI outputs before render/storage
4. isolate dev-only features behind explicit feature flags

### Track C: Offer And Market Proof

1. freeze one external promise
2. define funnel metrics:
   - content reach
   - comment to DM
   - DM to intake start
   - intake completion
   - payment conversion
   - dossier delivery SLA
   - repeat / follow-up rate
3. run 5-10 real paid cases through one controlled flow
4. review only revenue-linked learnings first

### Track D: Operations

1. one weekly product review
2. one weekly execution-gap review
3. one weekly GTM review
4. one rolling risk register with owner and deadline

## 6. Operating Rules

### Canonical Naming

- Public brand: `О теле с душой`
- Product promise: `Wellness Clarity in Telegram`
- Paid flagship: `Premium Wellness Dossier`
- Internal discipline: `нутрициологическая навигация`

### Source Of Truth

- Canonical local files:
  - `docs/AGENT_CONTEXT_HUB.md`
  - `docs/PROJECT_PULSE_LOG.md`
  - `docs/STRATEGY_LIVE_DELTA.md`
- Mirrors only:
  - Obsidian
  - Notion
  - GitHub context copies
  - Google Drive copies

### Release Gate

No new visible feature is considered "done" until:

1. runtime works
2. security/compliance checked
3. docs updated
4. admin/operator workflow validated
5. external claim wording verified

## 7. Tooling Matrix

### Skills To Use

- `human-russian-copywriter`: public copy, CTA cleanup, premium tone
- `pain-trigger-architect`: pain-based ethical content and hooks
- `google-drive:google-docs`: client docs, legal docs, operating docs
- `google-drive:google-sheets`: funnel metrics, case tracker, GTM dashboard
- `notion:notion-knowledge-capture`: decisions, SOP capture
- `vercel:agent-browser`: browser verification for landing/TMA
- `vercel:verification`: end-to-end flow checks when web surfaces are live

### Connectors / MCP

- Google Drive: legal pack, dashboards, operating docs
- Notion: knowledge capture and execution registry
- GitHub: code audit / change publication once repo flow is normalized

### Environment

- Local Windows environment remains acceptable for development only
- Production target should be a dedicated controlled runtime, not a personal workstation

### Subagents

- Explorer agent: read-only audits of docs, code, and GTM artifacts
- Worker agent: isolated remediation for disjoint files/modules
- Use only for bounded tasks with clear ownership

## 8. First 7-Day Plan

### Day 1

- finish P0 security hardening
- lock naming and source-of-truth policy

### Day 2

- rebuild PDF/client language and compliance pack
- define retention/deletion rules

### Day 3

- instrument funnel metrics
- create case/revenue tracker

### Day 4

- refactor `main.py` into first extracted modules

### Day 5

- stabilize OCR/Vision or temporarily reduce promise surface

### Day 6

- run full operator rehearsal on one controlled case

### Day 7

- run founder review:
  - what is secure
  - what is sold
  - what converts
  - what remains blocked

## 9. Definition Of Result

This project is ready for disciplined scaling only when:

- no obvious data leakage path exists,
- client-facing wording is legally coherent,
- one real funnel is measurable,
- delivery works end-to-end with human review,
- governance supports execution instead of only analysis.
