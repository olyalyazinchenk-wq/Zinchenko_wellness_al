# Strategy Live Delta

Rolling log for strategy and plan corrections between major strategy documents.

## 2026-05-01 09:17 MSK
### Artifact Delta
- Re-read the latest controlling artifacts before refreshing strategy:
  - `docs/PROJECT_PULSE_LOG.md`
  - `docs/PROJECT_NORTH_STAR_EXECUTION_PLAN_20260427.md`
  - `docs/PRODUCT_LINE_V2_20260426.md`
  - `docs/MANUAL_PAYMENT_MODE_20260426.md`
  - `docs/WELLNESS_DIALOGUE_QA_20260429.md`
  - `docs/GOOGLE_AI_STUDIO_MOY_PROJEKT_AUDIT_20260501.md`
  - `ops/reports/quality_report_20260429T080345Z.md`
  - `WellnessBot/texts.py`
  - `WellnessBot/data/runtime_state.json`
  - `WellnessBot/data/submissions/20260425T212847Z_<REDACTED_ID>.json`
  - `WellnessBot/data/submissions/20260425T214914Z_<REDACTED_ID>.json`
  - `WellnessBot/data/drafts/20260425T212847Z_<REDACTED_ID>.review.json`
  - `WellnessBot/data/drafts/20260425T214914Z_<REDACTED_ID>.review.json`
  - `WellnessBot/data/product_governance.json`
  - `docs/DISK_HYGIENE_STATUS.md`
  - `bot.stderr.log`
- New product-shaping evidence since the 2026-04-29 refresh:
  - `PRODUCT_EXAMPLES_TEXT` now gives a concrete safe demo fragment instead of generic promise copy
  - the Google AI Studio `moy-projekt` repo was audited and explicitly classified as UI/UX backlog, not backend truth
  - the bot is currently up after a clean restart on `2026-05-01 00:45 MSK`
- Core blockers did not improve:
  - `runtime_state.json` still contains runtime-only `week` session `20260427T173913Z_<REDACTED_ID>`
  - there is still no matching persisted submission JSON
  - the same user still also has two unresolved `premium` branches
  - benchmark truth still shows `20/20` routed and `0/20` model reached
  - governance memory still contains `115` experiments and `4` duplicate title groups
- A new operational emergency appeared during this run:
  - actual `C:` free space measured at `2026-05-01 09:17 MSK` is `2.69 GB`
  - this is materially worse than the last recorded `8.53 GB`
  - environment stability is now a first-order pilot blocker, not a background hygiene note

### Product Direction Delta
- Core direction does not change:
  - Telegram-first only
  - manual concierge payment remains the official pilot mode
  - `premium` remains the flagship proof path
  - `week` remains the lower-friction paid support rail
  - `vip` remains parked
- The new correction is about scope discipline:
  - the safer result example is useful because it closes a trust-gap in Telegram
  - the external React dashboard is not useful on the critical path because it creates a second product surface before one safe paid cycle is stable
- Therefore the next product story should be:
  - `safe Telegram intake + concrete example result + human-reviewed nutrition navigation`
  - not `AI dashboard`, not `new UI surface`, and not `personalized first-touch AI` until router overreach is cut

### Value Proposition Delta
- The validated value proposition remains:
  - `fact-safe nutrition navigation in Telegram with human review and same-thread follow-up`
- The trust proposition improved slightly:
  - the bot can now show a safer, more concrete demo of the output structure
  - this is the right kind of proof asset for the current stage because it explains the service without overclaiming
- The not-yet-proven layer is still explicit:
  - benchmark evidence still does not support a strong claim that first-touch chat is truly model-led or deeply personalized
  - deterministic templates are still doing most symptom-path work
- So the near-term value proof sequence is now:
  - keep the safe example result live
  - restore one coherent paid path
  - close one fact-safe reviewed cycle
  - then measure one genuine chat-quality improvement after router scope surgery

### Monetization Delta
- Monetization posture remains unchanged:
  - `week` -> `3900 RUB`
  - `premium` -> `6900 RUB`
  - `vip` -> `14900 RUB`
- The new demo example does not justify new pricing or a new package.
- The monetization question for the next cycle is narrower:
  - can the safer example result improve trust without pushing the team into new UI work?
  - can one coherent paid cycle actually close while the first-touch router is still being corrected?
- YooKassa / provider work remains off the immediate critical path while manual concierge mode works.

### Operating Delta
- The live same-user stack is still conflicted:
  - `20260427T173913Z_<REDACTED_ID>` = runtime-only `week` intake at `consent`
  - `20260425T214914Z_<REDACTED_ID>` = fresher `premium` evidence branch with `requires_lab_resubmission=true`
  - `20260425T212847Z_<REDACTED_ID>` = older `premium` rewrite candidate with review verdict `must_rewrite_with_high_caution`
- The live dialogue stack is still conflicted:
  - emergency and crisis routing remain useful and should stay deterministic
  - symptom and positioning prompts are still over-captured by templates
  - prompt/model tuning is still low leverage until routed share is reduced
- The live environment stack is now also conflicted:
  - runtime is up
  - but disk headroom is low enough to threaten continued artifact generation and safe operation
- Therefore the execution order changed:
  - environment survival
  - runtime/storage coherence
  - one active same-user path
  - router scope surgery
  - one safe paid proof path

### Safety Delta
- Legal and safety posture remains unchanged and must stay explicit:
  - no diagnosis framing
  - no treatment framing
  - urgent-care routing stays mandatory
  - unreadable or unconfirmed labs cannot become premium facts
  - human review remains mandatory before client delivery
- The new safety signal from the external UI audit is copy contamination risk:
  - the mock project contains overconfident medical-style language and pseudo-diagnostic wording
  - none of that wording should be copied into production
- The safe example result is only useful if it stays:
  - demo-only
  - non-diagnostic
  - based on clearly marked hypotheses and next-step clarification

### Inefficiency Loop Delta
- Repeated low-impact loop:
  - status-sync and documentation churn while runtime truth is still unresolved
- Repeated low-impact loop:
  - admiring or expanding the external dashboard mock while the Telegram pilot still lacks one coherent paid closure
- Repeated low-impact loop:
  - prompt or model tuning while `0/20` benchmark prompts reach the model
- Repeated low-impact loop:
  - governance growth while `115` experiments and `4` duplicate title groups already exist
- Repeated low-impact loop:
  - discussing packaging, landing, or UI expansion while `C:` is at `2.69 GB` free and the environment is near failure

### Higher-Impact Replacement Action
- Run one pilot-stability reset, in this order:
  1. restore `C:` above `10 GB` free using the manual delete-review queue, especially the large incomplete `.crdownload` files already identified in `docs/DISK_HYGIENE_STATUS.md`
  2. repair or clear `20260427T173913Z_<REDACTED_ID>` so runtime and storage agree
  3. declare exactly one active path for user `<REDACTED_ID>` and freeze the others
  4. shrink `route_live_reply()` so symptom prompts stop being fully template-owned
  5. keep the new example result text as the only conversion-surface improvement until one paid cycle closes

### Must-Hold Rules
- Keep Telegram as the only live operating channel.
- Keep manual concierge as the official pilot payment mode.
- Keep `premium` as the flagship proof path.
- Keep `week` as a support rail unless it is run on a clean separate user.
- Keep one active commercial path per Telegram user across runtime and persisted state.
- Keep human review mandatory before delivery.
- Keep no-diagnosis, no-treatment, urgent-care, and lab-quality rules explicit.
- Do not present router-template output as proof of personalized model performance.
- Do not merge the Google AI Studio dashboard into the current backend during this pilot cycle.
- Do not let docs, governance, launch chatter, or UI work outrun environment stability, runtime truth, and one coherent paid cycle.

## 2026-05-01 09:17 MSK
### Artifact Delta
- Re-read the current execution artifacts before refreshing strategy:
  - `docs/PROJECT_PULSE_LOG.md`
  - `docs/KNOWLEDGE_SYNC_HUB.md`
  - `docs/AGENT_CONTEXT_HUB.md`
  - `docs/GOOGLE_AI_STUDIO_MOY_PROJEKT_AUDIT_20260501.md`
  - `docs/WELLNESS_DIALOGUE_QA_20260429.md`
  - `ops/reports/quality_report_20260429T080345Z.md`
  - `WellnessBot/texts.py`
  - `WellnessBot/data/runtime_state.json`
  - `WellnessBot/data/submissions/20260425T212847Z_<REDACTED_ID>.json`
  - `WellnessBot/data/submissions/20260425T214914Z_<REDACTED_ID>.json`
  - `WellnessBot/data/drafts/20260425T212847Z_<REDACTED_ID>.review.json`
  - `WellnessBot/data/drafts/20260425T214914Z_<REDACTED_ID>.review.json`
  - `WellnessBot/data/product_governance.json`
  - `landing/index.html`
  - `mini-app/index.html`
  - `bot.stderr.log`
- New evidence since the 2026-04-29 refresh:
  - the Google AI Studio `moy-projekt` repo is a React/Vite UI mockup and must stay a UX reference, not a backend plan
  - `PRODUCT_EXAMPLES_TEXT` now shows a concrete safe demo-result fragment instead of a generic feature list
  - the bot restarted cleanly at `2026-05-01 00:45:55 MSK`
  - `C:` free space has fallen further to `2.69 GB`

### Product Direction Delta
- Core product direction does not change:
  - Telegram-first only
  - manual concierge payment remains the official pilot mode
  - human review remains mandatory before delivery
  - `premium` remains the flagship proof path
- The Google AI Studio repo should not redirect the roadmap:
  - use it as UI inspiration or future dashboard backlog only
  - do not treat it as an alternative operating backend
- The safer demo-result text is useful for trust-building, but it does not count as proof of delivery quality

### Operating Delta
- The state-truth conflicts remain unresolved:
  - `week_runtime_20260427T173913Z_<REDACTED_ID>` still exists only in runtime memory
  - the same user still holds two unresolved `premium` branches
  - `premium_fresh_20260425T214914Z` remains lab-gated and unsafe for delivery
  - `premium_legacy_20260425T212847Z` remains the only realistic rewrite candidate
- The live-chat blocker remains unchanged:
  - benchmark reference is still `ops/reports/quality_report_20260429T080345Z.md`
  - `20/20` prompts were routed before the model call
  - `0/20` prompts reached the model
- External contributor sync improved:
  - GitHub connector access exists for `olyalyazinchenk-wq/Zinchenko_wellness_al`
  - a missing local `git remote` is no longer a reason to skip GitHub status publication

### Plan Delta
- Move disk recovery ahead of any nonessential artifact generation or documentation churn:
  - the environment is now below `3 GB` free and can degrade mid-run
- Persist or clear `week_runtime_20260427T173913Z_<REDACTED_ID>` before carrying the paid-path story forward again
- Reduce the same-user paid stack to one active path before any delivery claim
- Shrink `route_live_reply()` before more prompt/model tuning so benchmark work can measure actual model behavior
- Keep the Google Drive access request unchanged until upload/create and share tools are exposed

### Strategy Delta
- The strategic bottleneck is now three-part, not one-part:
  - environment reliability
  - same-user state coherence
  - router overreach
- Therefore the next meaningful proof is no longer just a better dossier draft:
  - one stable workstation
  - one coherent paid path
  - one rerun benchmark where symptom prompts actually reach the model

### Goals Delta
- Goal 1: restore `C:` above the `10 GB` safety floor
- Goal 2: resolve the runtime-versus-storage mismatch and choose one active paid path
- Goal 3: narrow router scope and rerun the benchmark from a real model-reaching baseline
- Goal 4: keep the freshest premium branch frozen until readable labs or manual biomarker text clear the gate

### Next 12h Priorities
1. Free enough disk space to restore `C:` above `10 GB`.
2. Persist or clear `week_runtime_20260427T173913Z_<REDACTED_ID>`.
3. Declare one active paid path across the same-user `week` and `premium` stack.
4. Cut `route_live_reply()` back to safety/logistics coverage, add clarifying-question behavior, and rerun the benchmark.
5. Keep `premium_fresh_20260425T214914Z` frozen until readable labs or manual biomarker text arrive.
