# Sprint Board

Date: 2026-05-08
Status: Execution-compression refresh after no new product proof landed beyond the early-morning May 8 artifact set; sprint now narrows to canonical-case collapse and loop shutdown
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

- treat `20260501T162705Z_1084557944` as the governing defect:
  - `intake_status = delivered_to_client`
  - attached review verdict still says `needs_revision`
  - no explicit override note is recorded
- add or verify a hard guard so unresolved review verdicts cannot transition to delivery without an explicit manual override record
- decide whether the already delivered `week` case needs a correction, clarification follow-up, or internal downgrade
- make operator workflow and submission state tell the same delivery story

Done when:

- delivery cannot happen silently against an unresolved review verdict
- the current delivered `week` case has an explicit correction decision
- review truth and delivery truth are auditable from artifacts

## P0. Canonical Same-User Commercial Stack

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
- classify `20260505T131604Z_1084557944` explicitly:
  - merge-into-canonical premium continuation
  - or frozen non-canonical premium branch until the `week` truth defect is resolved
- classify `20260427T173913Z_1084557944` as a stale placeholder and archive candidate
- keep `20260425T214914Z_1084557944` frozen as evidence-only because `requires_lab_resubmission = true`
- park `20260425T212847Z_1084557944` unless a fresh post-`week` premium decision explicitly reactivates it
- stop mixing `week` validation, fresh paid premium demand, and stale April `premium` proof narratives for the same user

Done when:

- one user has one canonical commercial path
- every other branch has an explicit non-active role
- no same-user ambiguity remains across offers

## P0. Manual-Lab Fallback Proof

Owner:

- Lead Developer
- Operator
- Quality Auditor

Task:

- turn OCR-auth recovery and new manual-entry UX into verified, safe case progress

Concrete changes:

- treat commits `176ac82` and `fe7a358` as a narrow product gain:
  - manual lab-entry guidance now exists in code
  - a manual-entry button exists in the labs flow
  - malformed typed biomarker text now gets a rewrite prompt
- do not treat those commits as proof that real lab ingestion is ready
- verify four real file/lab paths:
  - PDF with text layer
  - readable photo
  - poor photo
  - manual biomarker text
- confirm client-facing fallback behavior when OCR or parsing is weak:
  - ask for a better photo or PDF
  - ask for manual biomarker text when needed
  - ask for a rewrite when typed biomarker lines are ambiguous
  - do not invent values from weak OCR or weak typed input
- add tests or replayable verification around the new manual-entry button, rewrite prompt, and malformed typed-lab handling
- keep deterministic biomarker alias expansion active
- keep DeepSeek extraction blocked as a fact source until confidence / merge / audit rules exist

Done when:

- the team has one verified result for PDF, good photo, poor photo, and manual text
- weak OCR or weak typed input produces a safe fallback instead of invented product truth
- file/lab reliability is described from measured behavior, not from auth recovery or UX landing alone

## P0. Mini-App Safety And Result-Surface Coherence

Owner:

- Frontend / Lead Developer
- Product Strategist

Task:

- stop the mini-app from promising a more autonomous or less safe product than Telegram actually delivers

Concrete changes:

- keep the single-path intake framing already present
- remove or neutralize the hardcoded `Premium Wellness-Досье` result demo
- remove hardcoded `Витамин D3: 5000 МЕ + K2`
- remove hardcoded `LCHF`
- remove any hardcoded biomarker conclusions from the result screen
- replace the result surface with either:
  - a safe placeholder
  - or reviewed backend-fed content only

Done when:

- mini-app result content no longer outruns safety posture
- frontend no longer implies autonomous medical-style output
- Telegram-first reviewed truth and mini-app surface tell the same story

## P0. Runtime Proxy Truth

Owner:

- Ops
- Lead Developer

Task:

- stop treating repeated proxy-backed restarts as runtime proof

Concrete changes:

- treat `2026-05-03 14:20:44-14:30:12 MSK` as the leading fragility signal because it combines `WinError 64` with explicit proxy refusal on `127.0.0.1:12334`
- treat the clean restart on `2026-05-07 23:46:49-23:46:50 MSK` as evidence that the runtime is currently up again
- do not treat that restart as proof of resilience while the path still logs `proxy=http://127.0.0.1:12334`
- explain or fix the `GET /health -> 404` outcome seen on `2026-05-08 00:35:06 +0300`
- verify whether polling truly requires `127.0.0.1:12334`
- if proxy is optional, document and prefer a no-proxy fallback path
- if proxy is required, treat proxy availability as a first-class ops dependency with startup checks and operator visibility
- stop treating startup or reconnect alone as sufficient until one clean post-fix verification passes

Done when:

- the team knows whether proxy is required or optional
- polling has a documented stable fallback or an explicit required dependency
- runtime health is observable without inference from reconnect
- one clean post-fix verification passes after the `2026-05-07` restart without repeated proxy refusal or disconnect loops

## P1. Model-Path Discipline

Owner:

- Lead Developer
- Quality Auditor

Task:

- improve live-model response discipline without undoing model reach

Concrete changes:

- treat `docs/WELLNESS_DIALOGUE_QA_20260506.md` as the current QA source of truth
- preserve the current routing gains:
  - `11/20` deterministic
  - `9/20` model-path
- fix the current quality regressions:
  - clarifying-question coverage slipped to `6/9`
  - invented names appear twice
  - `5/9` model-path replies are longer than `2000` characters
  - emergency templates remain duplicated across prompts `17` and `18`
- extend `sanitize_live_reply()` and prompt rules to block:
  - invented names
  - over-familiar address
  - early diagnosis-like labels
  - false specificity without evidence
  - overlong mini-consult responses to first-touch questions
- keep emergency / crisis routing deterministic and explicit
- rerun the benchmark only after delivery-gate, manual-fallback, mini-app, and runtime fixes land

Done when:

- model reach is preserved
- unsupported personalization is reduced
- benchmark evidence shows fewer discipline failures without collapsing model access

## P0. Execution Loop Compression

Owner:

- Quality Auditor
- Lead Developer

Task:

- stop repeated planning motion from outrunning unchanged proof artifacts

Concrete changes:

- treat the absence of new product proof after `2026-05-08 04:38 MSK` as a stop signal for more strategy/task churn
- treat `127` experiments, `4` duplicate title groups, and a largest duplicate group of `x8` as a loop signal
- treat the `29` `docs/tasks/HERMES-20260505-*` files as execution-diffusion evidence, not as shipped progress
- stop new strategy refreshes, readiness drafts, and task packets unless they directly land a P0 delivery, path, surface, file-fallback, or runtime fix
- stop new premium-story experiments while the same user already carries parallel paid paths
- add no new experiment burst before delivery truth, canonical-path truth, manual-fallback proof, and runtime proof are repaired
- add no new task-packet burst before at least one P0 delivery, surface, runtime, or file-fallback fix lands
- keep only one bounded replacement packet active:
  - delivery gate
  - five-branch classification
  - mini-app placeholder
  - manual-lab verification plus tests
  - proxy / health decision

Done when:

- the next artifact after this board is a direct P0 fix or verification result, not another plan layer
- duplicate backlog growth stops outranking live proof work

## Stop List

Blocked for now:

- treating `delivered_to_client` as trustworthy when internal review still says `needs_revision`
- running concurrent `week` and `premium` proof narratives for the same Telegram user
- letting `20260505T131604Z_1084557944` float as a second active premium storyline without an explicit relation to the canonical case
- reviving `20260425T214914Z_1084557944` while unreadable labs still block it
- reviving `20260425T212847Z_1084557944` as flagship proof without a fresh explicit decision
- showing hardcoded supplement, diet, or pseudo-medical result protocols on TMA / mini-app surfaces
- calling the runtime stable while polling still silently depends on a flapping proxy path
- calling manual-lab fallback solved before one reviewed end-to-end proof exists
- treating the May `nutrition_bot` and strategic-master-plan documents as the live execution plan
- starting Telegram Payments/YooKassa migration, PostgreSQL migration, Docker deployment, or new admin/WebApp work on the pilot critical path
- rerunning the benchmark before delivery truth, manual-fallback truth, mini-app truth, and runtime truth are repaired
- more growth, landing, or UI polish before delivery truth and path truth are repaired
- governance expansion before one clean canonical path exists

## Loop Risk

Repeated low-impact tasks to stop:

- rereading the same May 8 evidence set and producing another status artifact without landing a delivery, branch, surface, file-fallback, or runtime fix
- status and doc motion that does not change delivery truth or branch ownership
- creating more premium-story experiments while the same user already has a fresh paid premium branch plus unresolved old branches
- treating landed manual-lab UX as if it were the same thing as verified end-to-end fallback behavior
- repeating the same runtime-resilience claim without proving the transport path and health signaling are actually fixed
- alternate architecture/master-plan drafting that creates a second product story before the first one is safe and coherent
- task-packet and readiness-draft generation that restates delivery gate, client path, OCR, or launch themes without shipping the corresponding fix
- benchmark and tone work before mini-app truth and delivery gate are repaired
- experiment accumulation while `127` governance items already exist

Replacement action:

- freeze net-new planning churn; ship one bounded canonical-case collapse packet covering delivery truth, five-branch ownership, mini-app placeholder, manual-fallback proof, and proxy/health truth before any new strategy or benchmark motion

## Next 12h Command Set

1. Add or verify the hard guard so `needs_revision` or `must_rewrite_with_high_caution` cannot transition to `delivered_to_client` without an explicit manual override note.
2. Review `20260501T162705Z_1084557944` and record whether client correction / clarification follow-up is required before more proof claims are made.
3. Normalize the governing case so `lab_quality_check` and `requires_lab_resubmission` match the actual follow-up truth.
4. Declare `20260501T162705Z_1084557944` either canonical or corrected-and-replaced; do not leave it ambiguous.
5. Explicitly classify `20260505T131604Z_1084557944` as either merge-into-canonical premium continuation or frozen non-canonical premium branch.
6. Archive or explicitly retire stale `week` placeholder `20260427T173913Z_1084557944`.
7. Freeze `20260425T214914Z_1084557944` as evidence-only until readable labs exist.
8. Park `20260425T212847Z_1084557944` unless a fresh premium reactivation decision is made.
9. Replace the hardcoded mini-app `Premium Wellness-Досье` result demo, including `Витамин D3 5000 МЕ + K2` and `LCHF`, with a safe placeholder or reviewed backend-fed state.
10. Run manual-lab fallback verification on four paths: text PDF, readable photo, poor photo, and structured manual biomarker text.
11. Add or extend tests around the new manual-entry button, rewrite prompt, and malformed typed-lab handling.
12. Verify whether bot polling should depend on the local proxy at `127.0.0.1:12334`, using the clean `2026-05-07` restart as the verification baseline rather than as proof.
13. Explain or fix the current `GET /health -> 404` behavior and document the real runtime health check.
14. Extend `sanitize_live_reply()` and benchmark checks for invented names, over-familiar tone, duplicated emergency templates, and overlong first-touch replies.
15. Freeze net-new strategy/task packet generation unless it directly lands a delivery, surface, runtime, or file-fallback fix.
16. Rerun the quality benchmark only after steps `1-15` land and confirm model reach stays near the current `9/20` baseline.
17. Keep Telegram-first operations, manual concierge payment, and official prices at `3900 / 6900 / 14900 RUB`.
