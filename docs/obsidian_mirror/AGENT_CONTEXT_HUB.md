# Agent Context Hub

Updated: 2026-04-29 01:11 MSK

## Stage

- controlled concierge pilot with same-user state drift, lab-gate enforcement pressure, and external knowledge-sync discipline

## Objective

- restore one coherent paid-path truth for the current same-user case
- stop unsafe premium delivery from unreadable or unconfirmed lab evidence
- close one fact-safe, human-reviewed paid cycle before any new growth work

## Product Direction

- Telegram-first only
- service ladder remains:
  - `demo` builds trust
  - `week` is the low-friction entry rail
  - `premium` remains the flagship proof path
  - `vip` stays parked until operator-load evidence exists
- official pilot payment mode: `PAYMENT_MODE=manual`
- human review is mandatory before any client delivery

## Latest Validated Evidence

- benchmark reference: `ops/reports/quality_report_20260421T183148Z.md`
  - baseline remains `20` prompts and `0` empty replies
- `WellnessBot/data/runtime_state.json`
  - live runtime still points to `week_runtime_20260427T173913Z`
  - offer: `week`
  - step: `consent`
  - matching persisted submission JSON is still missing
- `premium_fresh_20260425T214914Z`
  - manual payment confirmed
  - `requires_lab_resubmission=true`
  - review verdict remains `needs_revision`
  - still unsafe for delivery because generation already happened after the lab gate failed
- `premium_legacy_20260425T212847Z`
  - manual payment confirmed
  - review verdict remains `must_rewrite_with_high_caution`
  - still unsuitable for delivery without a factual rewrite
- `WellnessBot/data/product_governance.json`
  - `115` experiments
  - `4` duplicate title groups still repeating
- `landing/index.html` and `mini-app/index.html`
  - no new surface change since 2026-04-13
- disk status
  - `C:` free space is now `7.63 GB`

## Current Operating Truth

- no new product or code artifacts were detected between 2026-04-29 00:18 MSK and this run
- the same user still spans one live `week` runtime session plus two unresolved `premium` branches
- the live `week` session is still provisional because storage does not contain its submission JSON
- `premium_fresh_20260425T214914Z` remains evidence-only until readable labs or manual biomarker text arrive
- `premium_legacy_20260425T212847Z` remains rewrite-reference material unless a human explicitly promotes it to the sole premium proof candidate
- GitHub connector access is available for the public repo even though local `git remote -v` is empty
- Google Drive sync remains unavailable in the current session because upload/create and share tools are not exposed

## Active Regressions

- runtime-to-storage mismatch
  - owner: Lead Developer
  - signal: runtime points to `week_runtime_20260427T173913Z`, but no matching file exists in `WellnessBot/data/submissions/`
  - next fix action: persist the live `week` session before or at `consent`, or invalidate and restart it cleanly
- same-user multi-path drift
  - owner: Operator + Lead Developer
  - signal: one user currently spans one live `week` runtime session plus two unresolved `premium` branches
  - next fix action: declare one active paid path and freeze, archive, or merge the rest
- unsafe premium lab-gate bypass
  - owner: Lead Developer
  - signal: `premium_fresh_20260425T214914Z` reached generation after `requires_lab_resubmission=true`
  - next fix action: hard-block generation and delivery when the lab gate is unsafe, or explicitly invalidate the current artifacts
- unsafe premium dossier content
  - owner: Product Strategist + Lead Developer
  - signal: both premium review artifacts still fail factual safety in different ways
  - next fix action: choose one paid path, rewrite from confirmed facts only, and rerun judge before any delivery decision
- governance duplication
  - owner: Lead Developer
  - signal: `115` experiments with `4` duplicate title groups still repeating
  - next fix action: deduplicate before the next digest
- disk hygiene regression
  - owner: Ops
  - signal: `C:` free space fell to `7.63 GB`
  - next fix action: manually review and clear the large delete candidates listed in `docs/DISK_HYGIENE_STATUS.md`

## Current Constraints

- Telegram-first only
- one active paid path per Telegram user at a time
- manual concierge remains the official pilot mode
- human review required before delivery
- no diagnosis or treatment framing
- no unreadable or unconfirmed lab facts
- no invented symptoms or unsupported condition claims
- do not treat a runtime-only session as settled truth if its submission JSON is missing
- do not spend the next cycle on landing, mini-app, growth channels, or public-launch expansion

## Next 12h Priorities

1. Resolve `week_runtime_20260427T173913Z`: persist it properly or clear it.
2. Reduce the same-user case to one active paid path across `week` and `premium`.
3. Keep `premium_fresh_20260425T214914Z` frozen for delivery until readable labs or manual biomarker text clear the gate and the dossier is regenerated from confirmed facts only.
4. Deduplicate governance experiment memory and restore disk free space above `10 GB`.
5. Keep external knowledge bases aligned through Notion and GitHub each run, and keep the Google Drive access request unchanged until the connector surface exists.

## Context For New Model

Stage:

- controlled concierge pilot with same-user state drift, lab-gate enforcement pressure, and external sync discipline

Objective:

- restore one coherent paid-path truth for the current same-user case
- stop unsafe premium delivery from unreadable or unconfirmed lab evidence
- close one fact-safe, human-reviewed paid cycle without opening new growth drift

Constraints:

- Telegram-first only
- one active paid path per Telegram user
- manual concierge remains official pilot mode
- human review required before delivery
- no diagnosis or treatment framing
- no unreadable or unconfirmed lab facts
- no invented symptoms or unsupported condition claims
- no new growth or UI work until state truth and lab gating are fixed

Immediate next actions:

1. Verify whether `week_runtime_20260427T173913Z` should be persisted as the live `week` path or cleared as an orphaned runtime session.
2. Declare exactly one active paid path for the same-user case, then freeze, archive, or merge the others.
3. Do not deliver the current premium PDF; first obtain readable labs or manual biomarker text and regenerate from confirmed facts only.
4. Deduplicate governance memory and clear the disk-space risk before the environment degrades further.
