# Operator Launch Protocol

Date: 2026-04-21
Owner: Olga / Wellness Bot
Use case: first controlled pilot cases

## Purpose

This is the day-of-launch operator protocol.

It exists so the project behaves like a real premium service, not like a fragile bot experiment.

The operator should use this document when:

- the first paid pilot goes live,
- a new intake appears,
- payment succeeds or fails,
- a draft is generated,
- red flags or high-risk cases appear.

## Core Product Frame

The service is:

- `нутрициологическая навигация`
- premium
- delicate
- human-in-the-loop

The service is not:

- diagnosis,
- treatment,
- therapy assignment,
- emergency care.

## Before Starting The Day

Run:

- `powershell -ExecutionPolicy Bypass -File .\ops\preflight.ps1`
- `powershell -ExecutionPolicy Bypass -File .\ops\bot-start.ps1`
- `powershell -ExecutionPolicy Bypass -File .\ops\bot-status.ps1`

Check that:

- preflight passes,
- bot process is running,
- polling is active,
- no fresh startup exceptions appear in stderr.

## Main Status Meanings

These are the practical statuses the operator will see in the queue logic.

- `awaiting_payment`
  - intake completed,
  - client should receive invoice,
  - operator watches for payment success or payment issue.

- `payment_received`
  - payment event has been accepted,
  - dossier generation should continue.

- `dossier_generation_in_progress`
  - internal generation is running,
  - operator mainly watches for completion or failure.

- `awaiting_human_review`
  - draft or PDF is ready for review,
  - operator checks quality and decides whether to approve.

- `draft_ready_human_review`
  - draft is available,
  - operator reviews before client delivery.

- `review_priority_quality_rework`
  - internal quality concerns,
  - operator should revise before delivery.

- `review_priority_market_rework`
  - value / positioning / clarity concerns in the output,
  - operator should revise before delivery.

- `review_priority_quality_and_market`
  - combined quality and offer clarity problem,
  - operator should not send until corrected.

- `draft_requires_edits`
  - admin marked it as a draft needing edits,
  - operator must revise and regenerate.

- `awaiting_manual_review_no_draft`
  - bot could not produce a usable draft,
  - operator must handle manually.

- `manual_handoff_no_provider`
  - no live payment provider branch,
  - legacy/manual fallback status.

- `manual_payment_pending`
  - no live payment provider branch or invoice failed,
  - operator must confirm payment manually,
  - dossier generation should not start yet.

- `manual_payment_confirmed`
  - operator confirmed external payment,
  - dossier generation may start,
  - final client delivery still requires human review.

- `payment_invoice_failed`
  - invoice creation failed,
  - operator must contact the client manually.

- `delivered_to_client`
  - dossier has been approved and sent.

## Live Case Flow

### 1. New intake arrives

Operator action:

- open the case queue,
- confirm client identity and symptoms,
- check whether the case is waiting for payment or already moved дальше.

If the case is in `awaiting_payment`:

- do not manually push medical advice,
- wait for payment success or invoice failure,
- be ready to contact the client if payment does not go through.

### 2. Payment succeeds

Operator action:

- confirm the case moved into `payment_received` or further,
- wait for dossier generation,
- monitor whether the case becomes `awaiting_human_review` / `draft_ready_human_review`.

If the case gets stuck:

- check logs,
- check saved submission JSON,
- confirm `payment_status` is `paid`,
- if needed, continue by manual operator intervention.

### 3. Payment fails

Typical status:

- `payment_invoice_failed`

Operator action:

- contact the client in Telegram,
- explain calmly that intake is saved,
- offer manual continuation,
- confirm next step personally.

### 4. Draft / PDF ready

Typical statuses:

- `awaiting_human_review`
- `draft_ready_human_review`

Operator action:

- read the draft or PDF,
- check that the tone is premium and clear,
- check that there is no diagnosis phrasing,
- check that doctor escalation is explicit when needed,
- check supplement wording is careful and not overclaiming.

Then choose:

- approve and send,
- regenerate PDF,
- keep as draft for edits.

### 5. Client delivery

When output is good:

- approve,
- send to client,
- confirm case moved to `delivered_to_client`.

After delivery:

- be ready for one follow-up message from the client,
- keep the tone warm and high-touch,
- do not collapse into short transactional answers.

### 6. Review capture after delivery

Operator action:

- ask for a private review in the same Telegram dialogue,
- do not push the client into multiple feedback destinations,
- collect the original review privately first,
- ask publication permission only as a second separate step,
- publish only the cleaned and approved version.

Public review destinations should be limited to:

- Telegram channel,
- landing page.

Internal improvement feedback should stay in the internal review register and not be mixed with public testimonials.

## Red Flags And High-Risk Cases

If the case contains red flags:

- do not soften the warning,
- explicitly say it should be discussed with a doctor,
- if urgency is high, direct to urgent in-person medical care.

High-risk groups requiring extra caution:

- pregnant clients,
- breastfeeding clients,
- children and teenagers,
- oncology history or suspicion.

For these groups:

- do not act like this is a routine wellness flow,
- keep recommendations more conservative,
- escalate medical discussion boundaries clearly.

## If The Client Has No Labs

This does not block the service.

Operator action:

- continue with structured preliminary wellness hypotheses,
- avoid overconfidence,
- suggest reasonable next labs if useful,
- keep language in the frame of `possible risks` and `next step`.

## If Draft Generation Fails

Typical signal:

- no usable draft,
- `awaiting_manual_review_no_draft`,
- generation/runtime error in logs.

Operator action:

- do not leave the client hanging,
- acknowledge internally that the case has to be handled manually,
- prepare a manual human-reviewed response path,
- regenerate if possible,
- if not, continue manually with premium tone.

## Payment Provider Disabled Scenario

If live payment provider is not configured:

- cases should go to `manual_payment_pending`,
- this is acceptable only as a temporary operator-managed mode,
- it is not the final state for a clean paid pilot.

Operator action:

- send the approved manual payment route,
- confirm payment outside the bot,
- press the admin confirmation button,
- verify the case moves to `manual_payment_confirmed`,
- only then allow dossier generation to proceed.

## Minimum Daily Launch Discipline

Every launch day:

1. Run preflight.
2. Start bot.
3. Confirm polling.
4. Watch first intake.
5. Watch first payment event.
6. Watch first dossier generation.
7. Review first output personally.
8. Send only after human approval.
9. Log issues immediately.

## Decision Rule

If something looks medically risky, legally blurry, or technically unstable:

- slow down,
- handle the case manually,
- do not force automation just because the bot can continue.
