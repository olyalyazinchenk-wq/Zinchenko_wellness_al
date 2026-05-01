# Pilot Launch Checklist

Date: 2026-04-21
Owner: Olga / Wellness Bot
Status: `not yet pilot-ready`

## Executive Verdict

The project is now materially closer to a controlled soft launch, but it is **not yet fully pilot-ready**.

Why:

- local runtime is working,
- governance flow is verified,
- payment and case logic are verified in smoke/tests,
- manual concierge payment confirmation is implemented for controlled fallback,
- public pricing is now synchronized at `6900 ₽`,
- but the real live payment branch is still blocked because `PAYMENT_TOKEN` is not configured in the working environment.

## What Was Verified Live

### Runtime

- preflight passes,
- local bot starts successfully,
- polling starts successfully,
- nurture loop starts,
- weekly digest loop starts.

Live issue found and fixed during walkthrough:

- missing `maybe_send_weekly_product_digest` orchestration path after governance refactor,
- fixed in [main.py](C:\Users\HP\Desktop\Новая папка\WellnessBot\main.py).

### Historical Evidence In Workspace

- historical submissions exist in `WellnessBot/data/submissions`,
- historical dossier drafts and PDFs exist in `WellnessBot/data/drafts`,
- this confirms the intake and dossier branch were exercised before on real project data.

## What Was Verified By Repeatable Smoke / Tests

### Governance / Admin

- reusable smoke: [admin_governance_smoke.py](C:\Users\HP\Desktop\Новая папка\ops\admin_governance_smoke.py)
- report artifact: [SMOKE_ADMIN_GOVERNANCE_20260421.md](C:\Users\HP\Desktop\Новая папка\docs\SMOKE_ADMIN_GOVERNANCE_20260421.md)
- automated tests: [test_governance_service.py](C:\Users\HP\Desktop\Новая папка\tests\test_governance_service.py)

Verified:

- insights accumulation,
- governance sync,
- decisions,
- suggested decisions,
- digest generation,
- empty-state handling,
- unique governance IDs.

### Payment / Case

- reusable smoke: [payment_case_smoke.py](C:\Users\HP\Desktop\Новая папка\ops\payment_case_smoke.py)
- report artifact: [SMOKE_PAYMENT_CASE_20260421.md](C:\Users\HP\Desktop\Новая папка\docs\SMOKE_PAYMENT_CASE_20260421.md)
- automated tests: [test_payment_case_services.py](C:\Users\HP\Desktop\Новая папка\tests\test_payment_case_services.py)

Verified:

- submission payload assembly,
- payment context generation,
- payload roundtrip,
- amount mismatch rejection,
- wrong-user rejection,
- manual payment pending / confirmed transitions,
- enrichment persistence,
- submission status transitions,
- session restoration from stored submission state.

## Pricing Readiness

Current synchronized launch price:

- `6900 ₽`

Verified in:

- [payment_flow.py](C:\Users\HP\Desktop\Новая папка\WellnessBot\payment_flow.py:6)
- [PRICE_POLICY_AND_YOOKASSA_CARD_20260421.md](C:\Users\HP\Desktop\Новая папка\docs\PRICE_POLICY_AND_YOOKASSA_CARD_20260421.md)
- [YOOKASSA_COPY_PASTE_20260421.md](C:\Users\HP\Desktop\Новая папка\docs\YOOKASSA_COPY_PASTE_20260421.md)
- [index.html](C:\Users\HP\Desktop\Новая папка\index.html:99)

## Launch Blockers

### Blocker 1. Real payment branch is not live

Current working environment does not expose an active `PAYMENT_TOKEN`.

Effect:

- live Telegram invoice branch cannot be completed honestly in production mode,
- the bot will fall back to controlled `manual_payment_pending`,
- pilot cannot be considered complete if paid handoff is part of the offer promise.

### Blocker 2. No confirmed live e2e with actual Telegram user actions

We confirmed local runtime and historical artifacts, but did not complete a fresh real-user live path through:

- `/start`,
- full intake,
- live payment,
- post-payment dossier generation,
- admin message receipt,
- final operator handling.

### Blocker 3. Post-delivery review collection path is not yet embedded into operations

The service still needs one simple and premium review path covering:

- where the client leaves a private service review,
- how publication consent is requested separately,
- where approved public testimonials are stored,
- who manually publishes public social proof,
- how health-related oversharing is filtered before publication.

## Non-Blocking But Important

- TMA is not required for pilot, but it is not the current launch path.
- public pricing and product wording now look more realistic for premium positioning.
- admin/governance layer is much safer than before, but should still be watched in first live cases.
- review collection should stay concentrated, not fragmented across random channels.

## Readiness Table

- Local runtime start: `PASS`
- Polling start: `PASS`
- Weekly digest runtime path: `PASS after fix`
- Governance smoke: `PASS`
- Governance tests: `PASS`
- Payment/case smoke: `PASS`
- Payment/case tests: `PASS`
- Manual payment confirmation fallback: `PASS`
- Public price sync: `PASS`
- Active payment provider token: `FAIL`
- Fresh live Telegram e2e with real actions: `NOT COMPLETED`
- Pilot operator checklist: `PASS`
- Review collection system: `DESIGNED, NOT YET OPERATIONAL`

## Decision

Current decision:

- `do not declare pilot-ready yet`

Correct next move:

1. configure and verify real `PAYMENT_TOKEN`,
2. run one fresh live Telegram walkthrough end-to-end,
3. activate the review collection path for first delivered clients,
4. then re-evaluate pilot readiness.

## Re-evaluation Trigger

The project can move from `not yet pilot-ready` to `pilot-ready` only after:

- real payment provider is connected,
- a fresh live e2e run succeeds,
- operator handling steps are written down,
- review collection path is ready for the first delivered case.


## 2026-04-22 Live E2E Update

### New Status

- Bot runtime: `PASS`
- Preflight: `PASS`
- Russian Telegram UI: `PASS after mojibake fix`
- Manual payment confirmation fallback: `PASS`
- Dossier generation after manual confirmation: `PASS`
- Admin PDF notification: `PASS after caption-length fix`
- Latest live case final delivery: `PENDING HUMAN REVIEW`
- YooKassa live payment token: `STILL BLOCKING AUTOMATED PAYMENT PATH`

### Launch-Blocking Bug Found And Fixed

During the live walkthrough, Telegram rejected admin PDF delivery because the PDF caption exceeded Telegram limits.

Fix:

- send PDF with short caption,
- send detailed admin summary separately,
- split long summaries into Telegram-safe chunks.

### Current Decision

The project is closer to controlled pilot readiness, but not fully pilot-ready yet.

Current allowed mode:

- `controlled concierge pilot candidate`

Still not allowed:

- broad public launch,
- unattended paid traffic,
- promise of fully automated payment until YooKassa token is live.

### Immediate Next Step

Review latest live case `20260422T202504Z_<REDACTED_ID>` in admin Telegram and decide:

- approve and send to client,
- or mark as draft requiring edits.
