# Payment And Launch Strategy

Date: 2026-04-22
Owner: Olga / Wellness Bot
Purpose: reset the launch strategy after YooKassa friction and prevent the project from being blocked by one payment path.

## 2026-04-26 Update

Manual payment is now the active pilot mode because YooKassa / Telegram payment activation is unstable or may reject the flow.

Current technical setting:

- `PAYMENT_MODE=manual`

Detailed runbook:

- `docs/MANUAL_PAYMENT_MODE_20260426.md`

Automated Telegram/YooKassa payment should be re-enabled only after a live payment walkthrough succeeds with `PAYMENT_MODE=telegram` and a valid live `PAYMENT_TOKEN`.

## Executive Verdict

The project is technically close to a controlled pilot, but not yet ready for a public paid launch.

The main launch risk is no longer product architecture.

The main launch risk is operational payment activation:

- YooKassa / Telegram provider token is not configured,
- no fresh real paid Telegram walkthrough has succeeded,
- current runtime is still local rather than 24/7 production hosting.

## Current Facts

### What Is Ready

- Telegram intake flow exists.
- Payment logic exists in code.
- Payment validation exists:
  - amount,
  - currency,
  - payload,
  - user identity.
- Dossier generation and admin review flow exist.
- Manual fallback exists when no payment provider is configured.
- Product safety policies were strengthened:
  - no diagnosis / treatment positioning,
  - lab OCR quality gate,
  - nutritiological reference layer,
  - review collection and response policy.
- Price is synchronized at `6900 ₽`.

### What Is Not Ready

- No active `PAYMENT_TOKEN` is configured.
- No real Telegram payment e2e has passed.
- YooKassa registration / provider connection may take unpredictable time.
- Server/VPS production runtime is not yet the active deployment.
- Public launch would be premature.

## YooKassa Reality

YooKassa is still a good target payment path, but it should not be the only operational path.

Known friction points:

- registration and contract details,
- shop protocol must support API for Telegram Bot payments,
- BotFather connection path can be confusing,
- test and live provider choices can be mixed up,
- fiscal / receipt settings may require attention,
- support or document review can delay activation.

## Official Constraints To Respect

Telegram payment flow requires:

- BotFather payment provider token,
- `sendInvoice`,
- `provider_token`,
- `payload`,
- `pre_checkout_query` handled within Telegram's timing requirements,
- `successful_payment` received before delivery.

YooKassa path requires:

- YooKassa registration,
- contract / merchant setup,
- correct shop settings,
- Telegram provider connection through BotFather / YooKassa bot,
- correct live token.

## Strategic Decision

Use a two-track launch strategy.

### Track A. Target automated payment path

Goal:

- Telegram invoice through YooKassa.

Use when:

- provider token is available,
- invoice appears in Telegram,
- successful payment event reaches the bot,
- stored case status becomes `paid`.

This remains the clean target path.

### Track B. Controlled concierge payment path

Goal:

- do not stop pilot learning if YooKassa Telegram integration is delayed.

Use when:

- YooKassa provider token is not ready,
- but Olga still wants to validate the offer with a small number of controlled clients.

Important:

- this path must remain manual and controlled,
- operator must confirm payment outside the bot before delivery,
- do not call this a fully automated paid launch,
- do not send public traffic into this mode.

Possible safe operational shape:

1. client completes intake,
2. bot or operator explains that online payment is being handled manually for the pilot,
3. operator sends an approved payment route,
4. operator confirms payment,
5. dossier is reviewed by human,
6. final result is delivered.

## What We Should Not Do

- Do not keep waiting indefinitely for YooKassa before testing the offer.
- Do not launch public traffic with a fragile payment setup.
- Do not pretend manual payment is the same as automated live payment.
- Do not deliver a paid dossier before payment confirmation.
- Do not accept random informal payments without legal / receipt clarity.
- Do not move to VPS before payment logic is verified unless 24/7 availability is specifically needed for the pilot.

## New Launch Strategy

### Phase 0. Stabilize the product promise

Status:

- mostly done.

Keep fixed:

- product name: `Premium Wellness Dossier`,
- price: `6900 ₽`,
- product positioning: nutrition navigation,
- no diagnosis / no treatment,
- human review before client delivery.

### Phase 1. Payment decision sprint

Timebox:

- 1-2 working days.

Goal:

- determine whether YooKassa Telegram payments can be activated immediately.

Actions:

1. finish YooKassa registration / shop setup,
2. confirm shop protocol is API-compatible,
3. connect provider through BotFather,
4. copy live provider token,
5. insert token into `.env`,
6. restart bot,
7. run one live payment walkthrough.

Success:

- `PAYMENT_TOKEN` present,
- Telegram invoice appears,
- payment succeeds,
- `payment_status=paid`,
- dossier branch continues.

Failure:

- no token,
- token does not work,
- invoice does not appear,
- payment event does not reach bot,
- YooKassa requires more documents / support.

### Phase 2. If YooKassa works

Proceed to controlled paid pilot.

Do:

1. run one full test case with Olga,
2. run one friendly real-client case,
3. monitor payment status,
4. review dossier manually,
5. collect feedback,
6. update launch checklist.

Do not:

- start paid traffic yet,
- remove human review,
- skip operator monitoring.

### Phase 3. If YooKassa does not work within the sprint

Switch to controlled concierge pilot.

Do:

1. keep bot intake active,
2. keep payment branch in `manual_handoff_no_provider`,
3. operator sends payment route manually,
4. operator confirms payment manually,
5. operator reviews and delivers result.

Goal:

- validate demand and workflow while YooKassa is still being resolved.

Limit:

- 3-5 controlled clients maximum.

Why:

- enough to validate offer and process,
- not enough to create operational chaos.

### Phase 4. Add manual payment confirmation support

Implemented product improvement:

- an admin button can mark a case as paid after external payment confirmation.

Suggested status:

- `manual_payment_pending`
- `manual_payment_confirmed`

Why:

- prevents accidental delivery before payment,
- makes the concierge path auditable,
- keeps manual pilot safer.

### Phase 5. Move to VPS / cloud VM

Only after:

- payment path is proven,
- at least one real e2e succeeds,
- operational process is stable.

Move before:

- public launch,
- broad paid traffic,
- unattended intake.

## Detailed Step-By-Step Plan

### Day 1. Payment reality check

1. Confirm YooKassa account status.
2. Confirm shop is activated or identify what is missing.
3. Confirm API protocol availability.
4. In BotFather open:
   - `/mybots`,
   - target bot,
   - Bot Settings,
   - Payments.
5. Choose:
   - `Connect ЮKassa: тест` if still testing,
   - `Connect ЮKassa: платежи` for real live mode.
6. Complete YooKassa authorization.
7. Return to BotFather.
8. Copy provider token.
9. Add token using:
   - `ops/set-payment-token.ps1`.
10. Restart bot.
11. Run live payment walkthrough.

### Day 2. Branch decision

If live payment works:

- mark payment branch `PASS`,
- run one real pilot case.

If live payment still blocked:

- mark payment branch `BLOCKED_BY_PROVIDER`,
- activate concierge pilot plan,
- continue resolving YooKassa in parallel.

### Day 3-5. Controlled pilot

Run no more than 3-5 cases.

For every case:

1. intake completed,
2. payment route confirmed,
3. payment confirmation recorded,
4. draft generated,
5. human review completed,
6. client delivery,
7. review requested,
8. product issue logged.

### After 3-5 Cases

Decide:

- offer is valid / invalid,
- price needs adjustment / does not,
- intake needs tightening,
- payment path is stable / not,
- VPS is now worth deploying.

## Risk Register

### Risk 1. YooKassa delay

Mitigation:

- use concierge pilot,
- keep YooKassa resolution in parallel.

### Risk 2. Payment accepted but bot misses event

Mitigation:

- verify `successful_payment`,
- check saved JSON,
- keep admin handoff.

### Risk 3. Manual payment chaos

Mitigation:

- limit to 3-5 clients,
- log every case,
- add manual payment confirmation status.

### Risk 4. Legal / receipt uncertainty

Mitigation:

- do not scale until official payment and receipt route is clear,
- keep terms/support/refund path visible,
- get legal/accounting review if needed.

### Risk 5. Laptop runtime failure

Mitigation:

- acceptable for testing,
- not acceptable for public launch,
- deploy VPS before broader traffic.

## Readiness Gates

### Concierge Pilot Ready

Minimum:

- bot starts,
- intake works,
- manual payment route exists,
- operator can review,
- no public paid traffic,
- cases limited to 3-5.

### Telegram Payment Pilot Ready

Minimum:

- `PAYMENT_TOKEN` configured,
- real invoice appears,
- successful payment event received,
- case becomes `paid`,
- dossier continues,
- admin sees case,
- human review before delivery.

### Public Launch Ready

Minimum:

- payment stable,
- hosting stable,
- privacy/consent docs published,
- support/refund/terms route ready,
- review collection ready,
- operator process tested,
- backups in place.

## Final Strategic Recommendation

Do not wait passively for YooKassa.

Run a strict payment activation sprint.

If YooKassa succeeds:

- proceed with live Telegram paid pilot.

If YooKassa stalls:

- run a small concierge pilot,
- keep payment manual and documented,
- add manual payment confirmation support,
- continue YooKassa resolution in parallel.

The goal is not to avoid YooKassa.

The goal is to avoid letting YooKassa block product validation.
