# Engineering Mandate

Date: 2026-04-29
Issued by: Chief Orchestrator
Status: Active refresh after QA truth recheck

## Mission

Run one coherent Telegram paid cycle through:

`demo trust -> product choice -> structured intake -> manual concierge payment -> AI draft -> human review -> safe client result -> same-thread follow-up`

`premium` remains the flagship proof path. `week` remains the lower-friction support rail. Public launch remains blocked.

## Chief Engineer Mandate

The Chief Engineer owns runtime truth, same-user path control, router truth, safety-gate integrity, and environment stability.

### Immediate responsibilities

1. Keep Telegram as the only live operating channel.
2. Keep manual concierge payment as the official pilot mode.
3. Distinguish runtime intake from persisted case from delivery-safe reviewed result.
4. Keep exactly one active commercial path per Telegram user across runtime and storage.
5. Prevent unreadable labs, unsupported claims, or stale branch artifacts from becoming client truth.
6. Prevent deterministic routing from becoming a hidden substitute for real model quality.
7. Keep disk headroom above the operational safety floor so the pilot does not fail for environmental reasons.
8. Prevent governance churn, offer expansion, or launch work from replacing paid-cycle learning.

### Immediate engineering sequence

1. Inspect `WellnessBot/data/runtime_state.json` first.
2. Treat `20260427T173913Z_1084557944` as provisional runtime state until it is either persisted correctly or cleared.
3. Freeze same-user `week` progression until runtime and storage agree on one path.
4. Inspect `route_live_reply()` against `docs/WELLNESS_DIALOGUE_QA_20260429.md` and `ops/reports/quality_report_20260429T080345Z.md`.
5. Narrow deterministic routing to emergency, crisis, file-upload guidance, and a small logistics FAQ surface.
6. Remove unsupported symptom details from deterministic templates and require clarifying questions when they materially change interpretation or safety.
7. Rerun the benchmark and verify the symptom path is no longer fully template-owned.
8. Treat `20260425T214914Z_1084557944` as evidence-only while `requires_lab_resubmission=true`.
9. Treat `20260425T212847Z_1084557944` as the only premium rewrite candidate if a clean proof closure is attempted.
10. Keep human review mandatory before any client-facing delivery.
11. Restore `C:` above `10 GB` free before allowing non-critical artifact growth or repeated generation work.
12. Promote only one post-closure improvement after fresh evidence exists:
   - stronger `week -> premium -> 30d` narrative

### Things the Chief Engineer must block

- any same-user concurrency across runtime and persisted active paths
- any treatment of runtime-only state as delivery truth
- any prompt or model tuning pass that leaves routed share unchanged
- any symptom template that injects facts the user did not provide
- any generic Premium CTA pattern that overwhelms symptom-first answers
- any delivery or regeneration flow that bypasses `requires_lab_resubmission=true`
- any use of unreadable or unconfirmed labs as if they were facts
- any attempt to treat artifact freshness as a substitute for safety clearance
- any active `vip` selling
- any pricing or packaging drift before one coherent paid closure exists
- any governance expansion that is not anchored to fresh delivery evidence
- any new growth, landing, mini-app, or public-launch work on the pilot critical path
- any wording that weakens no-diagnosis, no-treatment, urgent-care routing, or human review
- any avoidable artifact generation while `C:` remains below `10 GB` free

## Lead Developer / Executor Mandate

The Lead Developer / Executor owns the concrete repo and runtime behaviors that make one coherent paid cycle easier to close and one first-touch dialogue easier to trust.

### Sprint tasks

1. Make runtime-only, persisted, and review-ready states unambiguous in operator practice and code behavior.
2. Ensure one user cannot silently carry multiple active offer paths.
3. Reduce router scope so the model can actually handle non-emergency symptom prompts.
4. Prevent unreadable labs from silently becoming premium facts, drafts, or delivery assumptions.
5. Keep `week` and `premium` aligned to one Telegram-first story without same-user cross-tier drift.
6. Keep manual payment behavior and pricing consistent with the active pilot docs.
7. Reflect live evidence in strategy docs without creating documentation-only motion.

### Definition of done

A task is not done unless:

- it reduces ambiguity around the active same-user path
- it improves runtime-storage coherence
- it improves routed-vs-model truth for live dialogue
- it preserves legal and safety boundaries
- it survives available checks, logs, benchmark evidence, and operator review
- it makes the next paid cycle easier to explain and deliver
- it removes a loop instead of creating another

## Quality Auditor Mandate

The auditor must stop the cycle if any of these are true:

- more than one active same-user path exists across runtime and persisted state
- a runtime-only intake is being treated as a real paid case
- unreadable or unconfirmed labs are being treated as facts
- `20260425T214914Z_1084557944` is treated as delivery-ready while `requires_lab_resubmission=true`
- a premium rewrite proceeds without confirmed facts and human review
- benchmark symptom prompts are still fully intercepted by deterministic routing after a supposed quality pass
- unsupported router detail remains in symptom replies
- governance expansion is being treated as progress while no coherent paid closure exists
- disk headroom falls below the safety floor and non-critical generation still continues
- public launch language gets ahead of legal, payment, support, or delivery readiness

## Sprint Focus For The Next Execution Cycle

### Focus 1

Repair runtime truth and reduce the active user to one coherent path.

### Focus 2

Reduce router overreach so the benchmark can measure real product quality instead of template coverage.

### Focus 3

Protect the lab gate and keep only one premium proof candidate alive.

### Focus 4

Preserve the Telegram-first legal/safety posture while restoring environment stability.

## Loop-Break Rule

If a same-user path conflict or a full-router benchmark lock appears:

1. stop
2. classify each case item as runtime intake, persisted case, evidence-only, or archive
3. classify each reply path as deterministic safety/logistics or model-owned reasoning
4. keep exactly one active paid path
5. freeze or archive the rest
6. rerun the benchmark before any new prompt, pricing, or growth discussion continues

No silent same-user path multiplication or silent template capture is allowed.
