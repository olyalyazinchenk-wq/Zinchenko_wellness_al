# Agent Context Hub

Updated: 2026-05-01 21:18 MSK

## Single Source Of Truth

- Main developer handoff doc: `docs/PROJECT_DEVELOPMENT_SINGLE_SOURCE_OF_TRUTH.md`
- This file is the fast operational handoff for new contributors and new models.

## Stage

- controlled concierge pilot with one delivered paid `week` case, unresolved stale premium branches, and model-path quality hardening as the main current blocker

## Objective

- preserve one coherent Telegram-first paid-case story
- turn the delivered `week` proof into a repeatable operating pattern
- harden live model answers so first-touch quality earns more trust
- reset the premium proof path on clean evidence instead of stale same-user branches

## Product Direction

- Telegram-first only
- service ladder remains:
  - `demo` builds trust
  - `week` is the low-friction paid entry rail
  - `premium` remains the flagship offer
  - `vip` stays parked
- official pilot payment mode: `PAYMENT_MODE=manual`
- human review is mandatory before delivery

## Done

- disk pressure is no longer the active blocker:
  - `C:` free space is `24.58 GB`
- runtime-storage mismatch is no longer the active blocker:
  - `WellnessBot/data/runtime_state.json` is currently empty
- one paid `week` case has already completed end-to-end:
  - `20260501T162705Z_1084557944`
  - `offer = week`
  - `payment_status = manual_payment_confirmed`
  - `intake_status = delivered_to_client`
  - follow-up message already exists after delivery
- live-chat routing is no longer the blanket blocker:
  - latest benchmark source: `ops/reports/quality_report_20260501T080509Z.md`
  - `20/20` replies non-empty
  - `11/20` deterministic routed
  - `9/20` model-handled
  - clarifying questions now appear in `7/9` model-handled symptom prompts
- trust surface work already added:
  - safe example-result text is live
  - live-answer sanitizer exists
- external UI audit already decided:
  - `docs/GOOGLE_AI_STUDIO_MOY_PROJEKT_AUDIT_20260501.md` is UI backlog only, not backend truth

## Current Truth

- canonical current proof case:
  - `20260501T162705Z_1084557944`
  - treat this as the main live proof anchor
- stale same-user branches still exist and need explicit classification:
  - `20260427T173913Z_1084557944`
    - repaired `week` placeholder
    - `consent_pending`
    - not a current runtime session
    - should be archived or downgraded to inactive history
  - `20260425T214914Z_1084557944`
    - `premium`
    - `requires_lab_resubmission=true`
    - evidence-only and unsafe for delivery
  - `20260425T212847Z_1084557944`
    - `premium`
    - review verdict `must_rewrite_with_high_caution`
    - rewrite-or-archive decision pending
- live-chat quality has moved to a new bottleneck:
  - router overreach is reduced
  - current failures are unsupported personalization, duplicated service copy, and overly confident endocrine/GI framing
- governance remains bloated:
  - `120` experiments
  - `4` duplicate title groups
  - largest duplicate group repeats `7` times

## Next

1. Mark the delivered `week` case as canonical and downgrade stale branches.
2. Add anti-hallucination rules for invented names, over-familiar tone, and unsupported personalization.
3. Tighten symptom replies to `answer first -> max 2 hypotheses -> max 2 questions -> one next step`.
4. Split emergency templates by risk type and rerun the benchmark.
5. Use delivered `week` evidence plus follow-up to define the next clean premium-upgrade path.

## Must-Not-Change Rules

- Telegram-first only
- one active paid path per Telegram user
- manual concierge remains the official pilot mode
- human review required before delivery
- no diagnosis or treatment framing
- no unreadable or unconfirmed lab facts
- no invented symptoms, names, or intimacy cues
- do not let stale same-user branches compete with the canonical delivered case
- do not present model-path improvement as solved while personalization and false-specificity failures remain
- do not spend the next cycle on landing, mini-app, dashboard, pricing, or public-launch expansion

## Context For New Model

Stage:

- controlled concierge pilot with one delivered paid `week` proof and unresolved same-user premium leftovers

Done:

- disk and runtime-state blockers are cleared
- one `week` case delivered with follow-up
- model reach improved from `0/20` to `9/20`

Main problem now:

- first-touch model quality is good enough to expose new trust failures:
  - invented names or intimacy
  - repeated service copy
  - too-confident endocrine or GI framing

Case hierarchy:

- canonical: `20260501T162705Z_1084557944`
- inactive history: `20260427T173913Z_1084557944`
- evidence-only: `20260425T214914Z_1084557944`
- rewrite-or-archive: `20260425T212847Z_1084557944`

Immediate next actions:

1. Canonicalize the case stack and archive or downgrade stale branches.
2. Harden model-path trust against unsupported personalization and false specificity.
3. Split emergency handling by risk type.
4. Rerun the benchmark.
5. Define one premium-upgrade experiment from delivered `week` evidence instead of reusing stale premium artifacts.
