# Agent Context Hub

Updated: 2026-05-02 09:18 MSK

## Unified GitHub Source Of Truth

- Main public handoff document: `docs/PROJECT_DEVELOPMENT_SINGLE_SOURCE_OF_TRUTH.md`
- Use the local hub files for live operating truth and the GitHub source-of-truth doc for sanitized contributor onboarding.

## Quick Status

- Mode: controlled concierge pilot. Public launch remains blocked.
- Payment mode: `PAYMENT_MODE=manual`. Human review is still required before delivery.
- New top regression: the `week` case `20260501T162705Z_1084557944` reached `delivered_to_client` even though its attached judge verdict is still `needs_revision`.
- `WellnessBot/data/runtime_state.json` is now empty, so runtime/storage mismatch is no longer the main blocker.
- Latest benchmark reference: `ops/reports/quality_report_20260501T080509Z.md`
  - `20/20` non-empty replies
  - `11/20` deterministic replies
  - `9/20` model-handled replies
  - clarifying questions in `7/9` model-handled symptom prompts
- Disk headroom is healthy again: `C:` free space is approximately `24.58 GB`.
- Bot runtime is up and recovered from a short network interruption on `2026-05-01`.

## Run Note (2026-05-02)

- Regular sync completed: controlling artifacts re-read; no code changes detected in this run (docs-only updates pending).
- Pilot posture unchanged: controlled concierge only; manual payment is active; human review required; public launch remains blocked.

## Stage

- controlled concierge pilot with restored live-model reach, but unresolved delivery-gate integrity, same-user paid-path duplication, and unsafe mini-app demo copy

## Objective

- make the next delivered case review-safe and auditable
- collapse the same-user `week`/`premium` sprawl into one canonical path
- remove unsafe hardcoded result content from TMA/mini-app surfaces
- improve model-path discipline without losing the current model reach baseline

## Product Direction

- Telegram-first only
- service ladder remains:
  - `demo` builds trust
  - `week` is the low-friction entry rail
  - `premium` remains the flagship proof path
  - `vip` stays parked until operator-load evidence exists
- official pilot payment mode: `PAYMENT_MODE=manual`
- human review is mandatory before any client delivery

## Current Truth

- `WellnessBot/data/runtime_state.json` is empty.
- A new `week` case now exists and is marked `delivered_to_client`:
  - `WellnessBot/data/submissions/20260501T162705Z_1084557944.json`
  - follow-up already started after delivery
  - internal review on the same case still says `needs_revision`
- The same user still also has two older unresolved `premium` branches:
  - `20260425T214914Z_1084557944` remains lab-gated and unsafe for delivery
  - `20260425T212847Z_1084557944` remains rewrite-only with `must_rewrite_with_high_caution`
- Landing still matches the Telegram-first funnel.
- Mini-app still uses a single-path intake, but its hardcoded result demo contains unsafe supplement-dose and diagnosis-like content.
- Latest QA synthesis:
  - router overreach is no longer the main blocker
  - false specificity, invented personalization, and tone discipline are the live quality risks
- Bot runtime is currently up and processing updates after the recovered afternoon network interruption.

## Regressions To Fix Now

- Delivery gate bypass:
  - delivered `week` case despite unresolved internal-review verdict
- Same-user paid-path drift:
  - one delivered `week` case plus two unresolved `premium` branches
- Mini-app demo safety:
  - hardcoded result screen contradicts no-diagnosis and no-unsafe-supplement rules
- Model-path response discipline:
  - invented names, over-familiar tone, and early diagnosis-like labels still leak through QA

## Next

1. Enforce a hard delivery gate between internal review and client delivery.
2. Declare one canonical paid path for the same-user stack and freeze/archive the rest.
3. Replace unsafe mini-app demo content with a safe placeholder or reviewed backend-fed state.
4. Tighten live-answer sanitization and benchmark assertions around personalization hallucination and false specificity.

## Must-Not-Change Rules

- Telegram-first only
- manual concierge remains the official pilot mode
- one canonical paid path per Telegram user at a time
- human review required before delivery
- no diagnosis or treatment framing
- no unsafe supplement instructions without confirmed context and review
- no hardcoded medical-style demo results on TMA or public-facing surfaces
- do not treat a delivered status as trustworthy if the internal-review verdict still demands revision
- do not let landing, mini-app, or growth work outrun delivery safety and state coherence

## Context For New Model

Stage:

- controlled concierge pilot with live model reach restored, but delivery-gate integrity, canonical case ownership, and demo-surface safety still unstable

Objective:

- make the next delivered result review-safe
- collapse the same-user paid-path drift
- remove unsafe hardcoded demo/result copy
- keep improving model-path quality from the new `9/20` reach baseline

Constraints:

- Telegram-first only
- manual concierge remains official pilot mode
- human review required before delivery
- one canonical paid path per Telegram user
- no diagnosis or treatment framing
- no unsafe supplement instructions or hardcoded medical protocols on TMA/public surfaces
- Google Drive upload/share is unavailable in the current Codex session

Immediate next actions:

1. Add a guard so unresolved internal-review verdicts cannot move to `delivered_to_client` without an explicit manual override record.
2. Decide the canonical path for the current same-user stack and freeze/archive the other paid branches.
3. Replace unsafe mini-app result-demo content with a safe placeholder or reviewed backend-fed state.
4. Tighten `sanitize_live_reply()` and benchmark assertions for invented names, over-familiar tone, and early diagnosis-like language.
5. Keep the benchmark reference anchored to `ops/reports/quality_report_20260501T080509Z.md` and the QA readout to `docs/WELLNESS_DIALOGUE_QA_20260501.md`.

Reference benchmark:

- `ops/reports/quality_report_20260501T080509Z.md`
- QA synthesis: `docs/WELLNESS_DIALOGUE_QA_20260501.md`
- current truth: `20/20` non-empty, `11/20` deterministic, `9/20` model-handled, `7/9` clarifying-question coverage on model-handled symptom prompts
