# Sprint Board

Date: 2026-05-05
Status: Active refresh after a same-day clean bot restart, fresh follow-up lab evidence, and higher governance/draft pressure
Sprint owner: Chief Orchestrator
Operating mode: controlled Telegram-first pilot truth hardening

## P0. Delivery Gate Integrity

Owner:

- Lead Developer
- Quality Auditor
- Operator

Task:

- stop `delivered_to_client` from outrunning internal review truth

Concrete changes:

- treat `20260501T162705Z_1084557944` as the current governing defect:
  - `intake_status = delivered_to_client`
  - attached review verdict still says `needs_revision`
  - no explicit override note is recorded
- add a hard guard so unresolved review verdicts cannot transition to delivery without an explicit manual override record
- decide whether the already delivered `week` case needs a correction, clarification follow-up, or internal downgrade
- make operator workflow and submission state tell the same delivery story

Done when:

- delivery cannot happen silently against an unresolved review verdict
- the current delivered `week` case has an explicit correction decision
- review truth and delivery truth are auditable from artifacts

## P0. Canonical Same-User Path

Owner:

- Operator
- Product Strategist
- Lead Developer

Task:

- reduce user `1084557944` to one canonical paid path with explicit roles for every leftover branch

Concrete changes:

- lock `20260501T162705Z_1084557944` as either:
  - the canonical active path
  - or a corrected / downgraded path with explicit replacement
- classify `20260427T173913Z_1084557944` as a stale placeholder and archive candidate
- keep `20260425T214914Z_1084557944` frozen as evidence-only because `requires_lab_resubmission = true`
- park `20260425T212847Z_1084557944` unless a fresh post-`week` premium decision explicitly reactivates it
- stop mixing `week` validation and stale `premium` proof narratives for the same Telegram user

Done when:

- one user has one canonical commercial path
- every other branch has an explicit non-active role
- no same-user ambiguity remains across offers

## P0. Mini-App Safety And Price Coherence

Owner:

- Frontend / Lead Developer
- Product Strategist

Task:

- stop the mini-app from promising a different and less safe product than Telegram actually delivers

Concrete changes:

- remove off-policy `2990` pricing from the live-adjacent mini-app surface because it conflicts with current pilot pricing
- remove hardcoded ferritin / vitamin D / cortisol findings from the result demo
- remove hardcoded supplement-dose, `LCHF`, and pseudo-medical result content from the demo result screen
- replace the result demo with either:
  - a safe placeholder
  - or reviewed backend-fed content only
- keep the surface aligned to the Telegram-first reviewed backend promise

Done when:

- mini-app pricing matches current strategy truth
- mini-app result content no longer outruns safety posture
- frontend no longer implies autonomous medical-style output

## P0. Runtime Polling Resilience

Owner:

- Ops
- Lead Developer

Task:

- stop treating recovered polling failures as acceptable hidden infrastructure behavior

Concrete changes:

- treat the recovered failures on `2026-05-02 15:09:39-15:17:57 MSK`, `20:26:15-20:27:14 MSK`, and `21:38:36-21:38:48 MSK` as live evidence of fragility
- treat the newer recovered failure window on `2026-05-03 14:20:44-14:30:12 MSK` as the current leading ops signal because it combines `WinError 64` with explicit proxy refusal on `127.0.0.1:12334`
- treat the clean restart on `2026-05-05 17:15:59 MSK` plus active Python processes at `21:30 MSK` as evidence that the runtime is currently back up
- do not treat that clean restart as proof of resilience yet because the active path still logs `proxy=http://127.0.0.1:12334`
- verify whether polling truly requires `127.0.0.1:12334`
- if proxy is optional, document and prefer a no-proxy fallback path
- if proxy is required, treat proxy availability as a first-class ops dependency with startup checks and operator visibility
- stop treating startup or reconnect alone as sufficient until one clean post-fix verification passes

Done when:

- the team knows whether proxy is required or optional
- polling has a documented stable fallback or an explicit required dependency
- runtime health is no longer inferred only from eventual reconnect
- one clean post-fix verification passes after the `2026-05-05` restart without repeated proxy refusal or disconnect loops

## P0. Parallel Architecture Containment

Owner:

- Product Strategist
- Lead Developer
- Chief Orchestrator

Task:

- stop new May architecture and master-plan artifacts from hijacking the active Telegram pilot roadmap

Concrete changes:

- classify `docs/2026-05-04_nutrition-bot-architecture.md`, `docs/2026-05-04_nutrition-bot-context-document.md`, and `docs/2026-05-05_STRATEGIC_MASTER_PLAN.md` as reference-only inputs
- block any critical-path move toward:
  - Telegram/YooKassa automated payments
  - PostgreSQL migration
  - Docker/compose deployment work
  - separate admin/WebApp buildout
  - broader service-catalog expansion
- extract only bounded reusable assets from those docs:
  - prompts
  - OCR approach
  - service-boundary ideas
- keep those extractions blocked from implementation until delivery truth, canonical path truth, mini-app truth, and polling resilience are repaired

Done when:

- the team has one live roadmap and one reference backlog instead of two competing product stories
- off-policy payment, pricing, and automation ideas are no longer treated as current product truth
- only one bounded extraction package remains eligible for later implementation

## P1. Model-Path Discipline

Owner:

- Lead Developer
- Quality Auditor

Task:

- improve live-model response discipline without undoing model reach

Concrete changes:

- keep the current routing gains:
  - `11/20` deterministic
  - `9/20` model-path
  - `7/9` clarifying-question coverage on model-handled symptom prompts
- extend `sanitize_live_reply()` and prompt rules to block:
  - invented names
  - over-familiar address
  - early diagnosis-like labels
  - false specificity without evidence
- keep emergency / crisis routing deterministic and explicit
- rerun the benchmark only after delivery-gate, mini-app, and polling-resilience fixes land

Done when:

- model reach is preserved
- unsupported personalization is reduced
- benchmark evidence shows fewer discipline failures without collapsing model access

## P1. Premium Upgrade Brief From Fresh Evidence

Owner:

- Product Strategist
- Operator
- Lead Developer

Task:

- define the next premium move from fresh `week` follow-up and labs, not from stale April branches

Concrete changes:

- use the delivered `week` follow-up as the only live trigger for the next premium-upgrade design
- use the fresh `2026-05-05` follow-up artifacts on `20260501T162705Z_1084557944` as the concrete input set:
  - PDF upload
  - two photo uploads
  - ferritin `8 мкг/л` correction
- keep that brief blocked from launch until the delivery-review contradiction on the same case is explicitly resolved
- do not use stale `premium` artifacts as the current flagship proof story
- draft one concrete premium-upgrade hypothesis:
  - reviewed lab interpretation plus `30d` follow-up structure
- block any second premium experiment until the first canonical path is settled

Done when:

- premium has one fresh next experiment
- the upgrade story flows from live `week` evidence
- stale branches stop acting like active roadmap proof

## P1. Governance Compression

Owner:

- Quality Auditor
- Lead Developer

Task:

- stop idea accumulation from pretending to be progress

Concrete changes:

- treat `127` experiments, `4` duplicate title groups, and a largest duplicate group of `x8` as a loop signal
- treat the `29` `docs/tasks/HERMES-20260505-*` files as execution-diffusion evidence, not as shipped progress
- add no new experiment burst before delivery truth, canonical-path truth, and polling resilience are repaired
- add no new task-packet burst before at least one P0 delivery, surface, or runtime fix lands
- keep only one next experiment active:
  - premium upgrade from reviewed `week` follow-up and labs

Done when:

- governance reflects one next learning move
- duplicate backlog growth stops outranking live proof work

## Stop List

Blocked for now:

- treating `delivered_to_client` as trustworthy when internal review still says `needs_revision`
- running concurrent `week` and `premium` proof narratives for the same Telegram user
- reviving `20260425T214914Z_1084557944` while unreadable labs still block it
- reviving `20260425T212847Z_1084557944` as flagship proof without a fresh explicit decision
- keeping `2990` pricing on the mini-app surface
- showing hardcoded supplement, diet, or pseudo-medical result protocols on TMA / mini-app surfaces
- calling the runtime stable while polling still silently depends on a flapping proxy path
- treating the May `nutrition_bot` and strategic-master-plan documents as the live execution plan
- starting Telegram Payments/YooKassa migration, PostgreSQL migration, Docker deployment, or new admin/WebApp work on the pilot critical path
- rerunning the benchmark before delivery truth, mini-app truth, and polling resilience are repaired
- more growth, landing, or UI polish before delivery truth and path truth are repaired
- governance expansion before one clean canonical path exists
- pricing experiments or provider debate on the live pilot critical path

## Loop Risk

Repeated low-impact tasks to stop:

- status and doc motion that does not change delivery truth or branch ownership
- repeating the same runtime-resilience claim without proving the transport path is actually fixed
- stale premium-branch debate without a canonical-path declaration
- alternate architecture/master-plan drafting that creates a second product story before the first one is safe and coherent
- task-packet and readiness-draft generation that restates delivery gate, client path, OCR, or launch themes without shipping the corresponding fix
- benchmark and tone work before mini-app truth and delivery gate are repaired
- treating recovered proxy failures as solved because the bot eventually reconnects
- experiment accumulation while `127` governance items already exist

Replacement action:

- harden delivery truth first, keep all fresh follow-up evidence on the same canonical case second, neutralize the mini-app third, prove the polling path fourth, freeze new draft/task swarm fifth, then run one fresh premium-upgrade brief

## Next 12h Command Set

1. Add a hard guard so `needs_revision` or `must_rewrite_with_high_caution` cannot transition to `delivered_to_client` without an explicit manual override note.
2. Review `20260501T162705Z_1084557944` and record whether client correction / clarification follow-up is required.
3. Declare `20260501T162705Z_1084557944` either canonical or corrected-and-replaced; do not leave it ambiguous.
4. Keep the fresh `2026-05-05` PDF/photo/ferritin follow-up on the same canonical case; do not create a second active case from it.
5. Archive or explicitly retire stale `week` placeholder `20260427T173913Z_1084557944`.
6. Freeze `20260425T214914Z_1084557944` as evidence-only until readable labs exist.
7. Park `20260425T212847Z_1084557944` unless a fresh premium reactivation decision is made.
8. Remove off-policy `от 2 990 ₽` pricing from `mini-app/index.html`.
9. Replace the hardcoded ferritin / vitamin D / cortisol / `Витамин D3 5000 МЕ` / `LCHF` result demo with a safe placeholder or reviewed backend-fed state.
10. Verify whether bot polling should depend on the local proxy at `127.0.0.1:12334`, using the clean `2026-05-05` restart as the verification baseline rather than as proof.
11. Prove the chosen polling path with one clean post-fix verification instead of treating startup or reconnect alone as success.
12. Freeze net-new strategy/task packet generation unless it directly lands a delivery, surface, or runtime fix.
13. Extend `sanitize_live_reply()` and benchmark checks for invented names, over-familiar tone, and early diagnosis-like labels.
14. Rerun the quality benchmark only after steps `1-12` land and confirm model reach stays near the current `9/20` baseline.
15. Create exactly one premium-upgrade brief from the delivered `week` follow-up and new labs.
16. Keep Telegram-first operations, manual concierge payment, and official prices at `3900 / 6900 / 14900 RUB`.
