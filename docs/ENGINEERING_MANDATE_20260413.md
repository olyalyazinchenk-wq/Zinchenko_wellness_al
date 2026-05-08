# Engineering Mandate

Date: 2026-05-08
Issued by: Chief Orchestrator
Status: Active refresh after a second paid premium path appeared, manual lab-entry fallback landed in code, latest QA stayed flat-to-worse, and runtime restarted on the same proxy-backed path

## Mission

Run one coherent Telegram paid cycle through:

`demo trust -> week clarity -> manual concierge payment -> AI draft -> human review -> safe delivery -> same-thread follow-up with PDF/photo/manual labs -> same-case premium upgrade when fresh evidence justifies it`

`week` is the validated paid entry rail. `premium` remains the flagship offer. Public launch remains blocked.

## Chief Engineer Mandate

The Chief Engineer owns delivery truth, canonical same-user path control, surface safety coherence, manual-lab fallback proof, runtime polling resilience, live-model discipline, and critical-path scope control.

### Immediate responsibilities

1. Keep Telegram as the only live operating channel.
2. Keep manual concierge payment as the official pilot mode.
3. Keep official pilot prices locked at `3900 / 6900 / 14900 RUB`.
4. Distinguish paid confirmation from review clearance from delivery-safe output.
5. Keep exactly one canonical paid path per Telegram user.
6. Prevent unreadable labs, malformed typed labs, stale branches, or unresolved review verdicts from becoming client truth.
7. Prevent live-adjacent surfaces from promising more specificity, more automation, or more autonomy than the reviewed backend can support.
8. Prevent runtime health from silently depending on an unstable local proxy path without a documented fallback and observable health signal.
9. Prevent reconnect-based optimism from replacing a proven clean polling path.
10. Improve model-path response discipline without losing the current model reach baseline.
11. Prevent governance churn, offer expansion, or UI polish from replacing paid-cycle truth hardening.
12. Prevent May reference artifacts from creating a second live roadmap, second payment posture, or second product surface before the current pilot is coherent.
13. Prevent task-packet and readiness-draft accumulation from outrunning the actual delivery, surface, runtime, and file-fallback fixes already identified.
14. Prevent OCR auth recovery or manual-lab UX landing from being described as full file/lab readiness before real PDF/photo/manual-text behavior is verified.

### Immediate engineering sequence

1. Inspect `WellnessBot/data/submissions/20260501T162705Z_1084557944.json` and its attached review artifact.
2. Treat `delivered_to_client` plus `needs_revision` on the same case as the current governing defect.
3. Add or verify a hard guard so unresolved review verdicts cannot transition to delivery without an explicit manual override record.
4. Review whether the already delivered `week` case needs correction, clarification follow-up, or internal downgrade.
5. Keep `20260501T162705Z_1084557944` as the only candidate for canonical active-path status unless an explicit replacement decision is recorded.
6. Inspect `WellnessBot/data/submissions/20260505T131604Z_1084557944.json`.
7. Classify `20260505T131604Z_1084557944` explicitly as either:
   - merge-into-canonical premium continuation
   - or frozen non-canonical premium branch until the `week` defect is resolved
8. Classify `20260427T173913Z_1084557944` as a stale placeholder and explicit archive candidate.
9. Treat `20260425T214914Z_1084557944` as evidence-only while `requires_lab_resubmission = true`.
10. Park `20260425T212847Z_1084557944` unless a fresh post-`week` premium decision explicitly reactivates it.
11. Inspect `WellnessBot/main.py`, `WellnessBot/lab_ocr.py`, and `WellnessBot/texts.py`.
12. Treat commits `176ac82` and `fe7a358` as narrow wins on manual-lab fallback, not as proof of end-to-end file readiness.
13. Add or extend tests around the new manual-entry button, rewrite prompt, and malformed typed-lab handling.
14. Inspect `mini-app/index.html`.
15. Remove or neutralize the hardcoded `Premium Wellness-Досье` result demo plus hardcoded `Витамин D3 5000 МЕ + K2` and `LCHF`.
16. Inspect `bot.stderr.log`.
17. Treat the `2026-05-07 23:46:49-23:46:50 MSK` restart as evidence that the runtime is currently up again.
18. Do not treat that restart as proof of resilience while the path still logs `proxy=http://127.0.0.1:12334`.
19. Explain or fix the `GET /health -> 404` outcome logged at `2026-05-08 00:35:06 +0300`.
20. Verify whether polling truly requires `127.0.0.1:12334`; if not, add and document a no-proxy fallback path.
21. Require one clean post-fix verification pass after the `2026-05-07` restart before runtime can be called stable again.
22. Inspect `docs/WELLNESS_DIALOGUE_QA_20260506.md` and `ops/reports/quality_report_20260506T080435Z.md`.
23. Preserve the current routing gain:
    - `11/20` deterministic
    - `9/20` model-path
24. Fix the current quality regressions:
    - clarifying-question coverage down to `6/9`
    - invented names appearing twice
    - duplicated emergency templates on prompts `17` and `18`
    - `5/9` model-path replies longer than `2000` characters
25. Extend `sanitize_live_reply()` and prompt rules to block invented names, over-familiar address, early diagnosis-like labels, false specificity, and overlong first-touch mini-consults.
26. Rerun the benchmark only after delivery-gate, manual-fallback, surface-safety, and runtime-resilience fixes land.
27. Inspect `docs/2026-05-04_nutrition-bot-architecture.md`, `docs/2026-05-04_nutrition-bot-context-document.md`, `docs/2026-05-05_STRATEGIC_MASTER_PLAN.md`, and the current `docs/tasks/HERMES-20260505-*` draft swarm.
28. Classify those May docs as reference-only and extract only bounded reusable assets:
    - prompts
    - OCR approach
    - service-boundary ideas
29. Block any implementation of Telegram Payments/YooKassa automation, PostgreSQL migration, Docker deployment work, or separate admin/WebApp expansion until the live Telegram pilot truth gaps are closed.
30. Freeze net-new task-packet generation unless it directly closes a delivery, surface, runtime, or file-fallback gap already proven by artifacts.

### 2026-05-08 correction set

- Treat `20260505T131604Z_1084557944` as both:
  - real monetization proof
  - active canonical-path regression
- Treat manual-lab UX landing as a narrow product gain:
  - structured typed biomarker input is now a first-class fallback
  - malformed typed biomarker input now gets a rewrite prompt
  - nurture copy now explicitly supports photo or manual entry
  - none of that replaces end-to-end proof
- Treat `docs/WELLNESS_DIALOGUE_QA_20260506.md` and `ops/reports/quality_report_20260506T080435Z.md` as the current QA truth:
  - router reach held
  - response discipline did not materially improve
- Treat the `2026-05-07` restart plus `GET /health -> 404` as the current runtime truth:
  - bot is up again
  - proxy dependency remains active
  - health signaling remains incomplete

### Things the Chief Engineer must block

- any delivery transition that ignores an unresolved review verdict
- any same-user concurrency across active `week` and `premium` paths
- any attempt to let `20260505T131604Z_1084557944` act like a second active commercial story without an explicit canonical relation
- any attempt to treat stale `premium` branches as current flagship proof
- any treatment of unreadable or unconfirmed labs as delivery-safe facts
- any treatment of malformed typed biomarker text as if it were confirmed structured evidence
- any mini-app or TMA surface that shows hardcoded supplement protocols, diet protocols, or pseudo-diagnostic conclusions
- any runtime setup that silently requires an intermittently unavailable proxy listener without a documented fallback and health signal
- any claim that polling resilience is fixed before one clean post-fix verification passes after the `2026-05-07` restart baseline
- any claim that OCR/file reliability is solved before real PDF/photo/manual-text verification passes
- any use of AI-assisted biomarker extraction as a fact source without confidence, merge, and audit controls
- any prompt or sanitizer pass that collapses model reach back toward template capture
- any symptom reply that invents names, uses unwarranted familiarity, duplicates emergency handling across risk classes, or applies an early diagnostic label without evidence
- any treatment of the May `nutrition_bot` and strategic-master-plan docs as current product truth rather than reference-only backlog
- any critical-path move toward Telegram Payments/YooKassa automation, PostgreSQL migration, Docker deployment, or separate admin/WebApp work before the current pilot is coherent
- any accumulation of new task packets, launch plans, or readiness reports that restates already known P0 work without closing it
- any active `vip` selling
- any pricing or packaging drift before one clean canonical path exists
- any governance expansion that is not anchored to fresh delivered-case evidence

## Lead Developer / Executor Mandate

The Lead Developer / Executor owns the concrete repo and runtime behaviors that make reviewed delivery safer, same-user path ownership clearer, the live Telegram experience more trustworthy, manual-lab fallback more reliable, and polling operationally explicit.

### Sprint tasks

1. Make review-cleared, override-approved, and delivered states unambiguous in code and operator practice.
2. Ensure one user cannot silently carry multiple active paid narratives.
3. Turn the fresh paid `premium` case into either a same-case continuation or an explicitly frozen branch.
4. Keep stale `premium` branches and stale `week` placeholders from contaminating the current commercial story.
5. Keep mini-app demo content aligned with the actual Telegram-first reviewed product.
6. Make polling resilient enough that reconnects are not mistaken for stability.
7. Make manual typed biomarker input safe enough that weak OCR does not block all progress.
8. Preserve model reach while tightening specificity, tone discipline, and emergency-template separation.
9. Reflect live evidence in strategy docs without creating documentation-only motion.
10. Compress task/report churn when live artifacts already point to the next engineering action.

### Definition of done

A task is not done unless:

- it improves delivery truth
- it reduces ambiguity around the canonical same-user path
- it improves surface safety and price coherence
- it makes runtime polling behavior explicit and reliable
- it proves runtime resilience rather than inferring it from reconnects
- it proves file/lab fallback behavior instead of assuming auth recovery or UX landing solved it
- it preserves legal and safety boundaries
- it preserves or clarifies routed-vs-model truth for live dialogue
- it survives available checks, logs, benchmark evidence, and operator review
- it makes the next paid cycle easier to explain and defend
- it removes a loop instead of creating another

## Quality Auditor Mandate

The auditor must stop the cycle if any of these are true:

- `delivered_to_client` appears while internal review still demands revision and no override record exists
- more than one active same-user paid path exists
- `20260505T131604Z_1084557944` is active without an explicit canonical relation to the governing `week` case
- unreadable or unconfirmed labs are being treated as delivery-safe facts
- malformed typed biomarker text is accepted without a rewrite / resubmission guard
- `20260425T214914Z_1084557944` is treated as anything other than evidence-only while lab resubmission is unresolved
- `20260425T212847Z_1084557944` quietly re-enters the active path without an explicit recorded decision
- mini-app or TMA surfaces show hardcoded medical-style output
- polling still depends on a flapping proxy path with no documented fallback or health signal
- polling is described as stable before one clean post-fix verification pass
- benchmark evidence shows invented personalization, duplicated emergency handling, false specificity, or overlong first-touch replies without mitigation
- governance expansion is being treated as progress while canonical path truth is unresolved

## Sprint Focus For The Next Execution Cycle

### Focus 1

Protect delivery truth before anything else.

### Focus 2

Reduce the current user to one canonical commercial path, including the fresh `20260505` premium case.

### Focus 3

Prove manual-lab fallback behavior now that the UX exists in code.

### Focus 4

Bring mini-app result copy back inside the Telegram-first safety boundary.

### Focus 5

Make polling resilient enough that runtime stability is explicit, verified, and not inferred from reconnects.

### Focus 6

Improve live-model discipline while preserving the current `9/20` model-path reach.

## Loop-Break Rule

If delivery bypass appears again, same-user path sprawl persists, manual-lab fallback remains unproven, the mini-app keeps off-policy output, or proxy failures continue without a documented fallback:

1. stop
2. inspect the canonical case artifact and attached review artifact
3. classify each case item as canonical, merge-into-canonical, evidence-only, parked, or archive
4. classify each surface element as reviewed truth, safe placeholder, or off-policy copy
5. classify each lab input path as proven, partially proven, or unproven
6. classify polling as proxy-required or proxy-optional with an explicit fallback path and health signal
7. prove the chosen polling path with one clean post-fix verification
8. keep exactly one canonical paid path
9. remove off-policy surface output
10. rerun the benchmark only after the truth and resilience fixes land

No silent delivery bypass, silent same-user multiplication, silent typed-lab ambiguity, silent frontend truth drift, silent proxy fragility, or silent roadmap drift is allowed.
