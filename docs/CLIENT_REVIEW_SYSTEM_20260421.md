# Client Review System

Date: 2026-04-21
Owner: Olga / Wellness Bot
Purpose: define where clients leave reviews, how reviews are separated by purpose, and how social proof is published without creating compliance chaos.

## Executive Decision

Clients should not be sent into many different feedback destinations.

For the first pilot and early paid launch, the clean system is:

1. private service feedback in Telegram,
2. separate consent for public publication,
3. manual publishing of selected testimonials to public surfaces.

This keeps the experience premium, controllable, and safer for health-adjacent content.

## Why Not Scatter Reviews

If clients are asked to leave reviews "anywhere", the project creates five problems at once:

- feedback gets lost,
- social proof becomes inconsistent,
- publication consent becomes blurry,
- health details may be overshared in public,
- the operator has no single review archive.

For a premium wellness service, fragmentation lowers trust.

## Review Layers

### Layer 1. Private review after delivery

Primary destination:

- the same Telegram dialogue where the client received the dossier.

Why this is the main channel:

- lowest friction,
- premium personal feel,
- no extra login or form,
- easiest to ask while the result is still fresh,
- easiest for the operator to continue the conversation.

Recommended ask:

- request a short free-text response plus one structured score.

Minimum structure:

- overall impression,
- what felt most useful,
- what became clearer after the consultation,
- optional score from `1` to `10`.

### Layer 2. Publication consent

Private feedback is not equal to publication permission.

If the review is strong, the operator asks a second separate question:

- may we publish this review publicly,
- in full name / first name / anonymous format,
- with or without symptom details.

This second step is mandatory.

### Layer 3. Public social proof

Approved public reviews should be published only in controlled surfaces.

Recommended public surfaces in priority order:

1. Telegram channel `@olga_nutri86`
2. landing page testimonial block
3. pinned compilation post with selected client responses

Do not make public comments the main collection channel in the first pilot.

Reason:

- public comment threads are noisy,
- clients may disclose sensitive health details,
- moderation becomes harder,
- the premium tone becomes less controllable.

## Practical Answer To "Where Will Clients Write Reviews?"

Short answer:

- first, in the private Telegram dialogue;
- then, with separate consent, selected reviews move to the public channel and landing page.

This is the operating answer for launch.

## What Not To Use As The Main Review Destination Yet

Do not rely on these as the primary review source in the first launch phase:

- random comments under many Telegram posts,
- uncontrolled WhatsApp screenshots,
- free-form public chat groups,
- public medical aggregator cards,
- scattered reviews in personal DMs without logging.

These can exist later as supporting signals, but not as the system of record.

## Review Types To Split

Reviews should be divided into three categories.

### A. Service-quality review

Purpose:

- show premium care and emotional trust.

Typical content:

- "felt heard",
- "everything was clear",
- "the report was detailed",
- "the tone was delicate and supportive".

Best place:

- Telegram private collection,
- then public channel / landing after consent.

### B. Outcome / utility review

Purpose:

- show that the client got practical value.

Typical content:

- "understood the next steps",
- "finally saw the full picture",
- "became clear what to discuss with a doctor",
- "nutrition and supplement guidance became understandable".

Best place:

- landing page testimonials,
- compilation post in Telegram channel.

### C. Product-improvement feedback

Purpose:

- improve the bot and operator flow.

Typical content:

- where the intake was confusing,
- where payment felt unclear,
- which section felt too long,
- which recommendation needed better explanation.

Best place:

- internal review log only,
- not for public publication.

## Operator Flow

### Moment To Ask

Ask for feedback after:

- dossier delivery,
- one short follow-up exchange,
- confirmation that the client has opened or read the result.

Do not ask immediately after payment.

Do not ask before delivery quality is confirmed.

### Script Logic

Step 1:

- ask for a private review in the Telegram thread.

Step 2:

- if the response is strong, ask for publication permission separately.

Step 3:

- prepare a cleaned public version.

Step 4:

- remove excessive health details.

Step 5:

- publish manually to the approved public surface.

## Reply To Every Review

Every private review should receive a reply.

This reply should be:

- warm,
- respectful,
- emotionally steady,
- objective.

It should not:

- flatter,
- mirror irritation,
- agree with everything automatically,
- lose the product boundary.

If the review contains factual confusion about diagnosis or treatment, the reply may calmly clarify the real product frame.

## Data And Compliance Rules

Reviews may contain health-related context.

Because of that:

- keep the original review in controlled storage,
- do not publish without separate permission,
- minimize sensitive details in public versions,
- prefer anonymous or first-name-only attribution,
- keep an internal note on what exactly the client approved for publication.

If the review contains:

- diagnoses,
- oncology history,
- pregnancy details,
- children's data,
- detailed lab values,

then public publication should be extra conservative or skipped.

## Recommended Launch Setup

For the first pilot, use this exact configuration:

- collection channel: private Telegram dialogue,
- publication consent: manual operator follow-up in Telegram,
- public destination 1: Telegram channel,
- public destination 2: landing page,
- archive of original reviews: internal review register.

## Internal Review Register

The operator should keep one simple review register with:

- client case ID,
- delivery date,
- private review received: yes / no,
- score if available,
- publication consent: yes / no,
- approved attribution style,
- publication status,
- notes for product improvement.

This can start as a simple spreadsheet or controlled table.

## Future Automation

After the first pilot is stable, the project can automate:

- automatic follow-up message after `delivered_to_client`,
- structured rating capture,
- review register sync,
- operator reminder if no feedback was requested within `48` hours.

This should come after payment activation, not before.
