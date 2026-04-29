# Strategy Live Delta

Rolling log for strategy and plan corrections between major strategy documents.

## 2026-04-29 21:13 MSK
### Artifact Delta
- Re-read the latest controlling artifacts before refreshing strategy:
  - `docs/PROJECT_PULSE_LOG.md`
  - `docs/PROJECT_NORTH_STAR_EXECUTION_PLAN_20260427.md`
  - `docs/PRODUCT_LINE_V2_20260426.md`
  - `docs/MANUAL_PAYMENT_MODE_20260426.md`
  - `docs/WELLNESS_DIALOGUE_QA_20260429.md`
  - `ops/reports/quality_report_20260429T080345Z.md`
  - `WellnessBot/main.py`
  - `WellnessBot/data/runtime_state.json`
  - `WellnessBot/data/submissions/20260425T212847Z_1084557944.json`
  - `WellnessBot/data/submissions/20260425T214914Z_1084557944.json`
  - `WellnessBot/data/drafts/20260425T212847Z_1084557944.review.json`
  - `WellnessBot/data/drafts/20260425T214914Z_1084557944.review.json`
  - `WellnessBot/data/product_governance.json`
  - `docs/DISK_HYGIENE_STATUS.md`
  - `bot.stderr.log`
- New product-shaping evidence did appear after the 2026-04-29 01:11 MSK refresh:
  - benchmark quality is currently coming from `route_live_reply()`, not from the model
  - `20/20` prompts returned non-empty replies
  - `20/20` prompts were intercepted before the model call
  - `0/20` prompts reached the configured model
  - clarifying-question count remains `0/20`
- State and delivery truth did not improve:
  - `runtime_state.json` still holds `20260427T173913Z_1084557944` as a live `week` session at `consent`
  - there is still no matching file in `WellnessBot/data/submissions/`
  - user `1084557944` still also has two unresolved `premium` branches
- Runtime is up and not currently crashing:
  - clean restart logged at `2026-04-29 09:35 MSK`
  - only transient polling proxy timeout was observed later; no new dossier/runtime crash surfaced in the log
- Environment pressure remains active:
  - `C:` free space is now `8.53 GB`
  - the `10 GB` safety floor remains unmet

### Product Direction Delta
- Core direction does not change:
  - Telegram-first only
  - manual concierge payment stays the official pilot mode
  - `premium` remains the flagship proof path
  - `week` remains the lower-friction paid support rail
  - `vip` remains parked
- The main strategic correction of this run is about the top-of-funnel promise:
  - Antigravity should currently be sold as `safe Telegram intake plus human-reviewed nutrition navigation`
  - it should not be sold yet as `highly personalized live AI clarity in the very first symptom reply`
- Therefore the product has two real blockers now, not one:
  - state coherence and paid-case truth
  - router overreach that prevents genuine model-led personalization

### Value Proposition Delta
- The validated value proposition remains:
  - `fact-safe nutrition navigation in Telegram with human review and same-thread follow-up`
- The not-yet-proven layer is now explicit:
  - benchmark evidence does not support a strong claim that first-touch chat is truly personalized
  - current symptom replies are mostly deterministic templates with repeated structure and no clarifying questions
- This means premium value should be demonstrated through:
  - one coherent paid path
  - one fact-safe reviewed result
  - one tighter live-chat improvement that makes the first exchange feel less generic and less sales-led

### Monetization Delta
- Monetization posture remains unchanged:
  - `week` -> `3900 RUB`
  - `premium` -> `6900 RUB`
  - `vip` -> `14900 RUB`
- The next monetization question is still not pricing.
- The next monetization proof is now two-part:
  - can Antigravity close one coherent, human-reviewed, fact-safe paid cycle in Telegram?
  - can the first symptom dialogue create enough trust without generic router repetition to move the right users into `week` or `premium`?
- YooKassa / Telegram provider work stays off the immediate critical path while manual concierge mode works.

### Operating Delta
- The live same-user stack is still conflicted:
  - `20260427T173913Z_1084557944` = runtime-only `week` intake at `consent`
  - `20260425T214914Z_1084557944` = fresher `premium` evidence branch with `requires_lab_resubmission=true`
  - `20260425T212847Z_1084557944` = older `premium` rewrite candidate with review verdict `must_rewrite_with_high_caution`
- The live dialogue stack is also conflicted:
  - emergency and crisis routing are useful and should stay deterministic
  - symptom and positioning prompts are being over-captured by templates
  - prompt/model tuning is low leverage until routed share is reduced
- Therefore the execution rule for the next cycle is:
  - exactly one active commercial path per Telegram user
  - runtime-only sessions are provisional, not paid-case truth
  - unreadable-lab branches are evidence-only, not delivery candidates
  - deterministic routing should be narrowed to emergency, crisis, file-upload guidance, and a small logistics FAQ set

### Safety Delta
- Legal and safety posture remains unchanged and must stay explicit:
  - no diagnosis framing
  - no treatment framing
  - urgent-care routing stays mandatory
  - unreadable or unconfirmed labs cannot become premium facts
  - human review remains mandatory before client delivery
- The new safety signal from QA is false specificity:
  - templates are injecting detail that the user did not supply
  - the cited example is the unsupported antibiotics storyline
- The freshest `premium` branch remains blocked by the lab gate and must not be reinterpreted as ready because payment was confirmed.

### Inefficiency Loop Delta
- Repeated low-impact loop:
  - status-sync and documentation churn without changing runtime truth
- Repeated low-impact loop:
  - debating `week` vs `premium` sequencing while the missing submission file still exists
- Repeated low-impact loop:
  - prompt or model tuning while `0/20` benchmark prompts reach the model
- Repeated low-impact loop:
  - adding governance ideas while `115` experiments and `4` duplicate title groups already exist
- Repeated low-impact loop:
  - discussing new walkthroughs or landing growth while disk space, router scope, state coherence, and lab gating are still unresolved

### Higher-Impact Replacement Action
1. Repair or clear `20260427T173913Z_1084557944` so runtime and storage agree.
2. Declare one active path for user `1084557944` and freeze the others.
3. Shrink `route_live_reply()` so symptom prompts stop being fully template-owned.
4. Remove unsupported symptom details from deterministic templates and require clarifying questions where they materially change interpretation.
5. Rerun the benchmark and track routed share, duplicate-cluster count, unsupported-detail failures, and clarifying-question count.
6. Keep `20260425T214914Z_1084557944` evidence-only until readable labs or manual biomarkers exist.
7. Use `20260425T212847Z_1084557944` as the only premium rewrite candidate if a proof closure is attempted next.
8. Restore `C:` above `10 GB` free so the pilot environment does not degrade mid-cycle.

### Must-Hold Rules
- Keep Telegram as the only live operating channel.
- Keep manual concierge as the official pilot payment mode.
- Keep `premium` as the flagship proof path.
- Keep `week` as a support rail unless it is run on a clean separate user.
- Keep one active commercial path per Telegram user across runtime and persisted state.
- Keep human review mandatory before delivery.
- Keep no-diagnosis, no-treatment, urgent-care, and lab-quality rules explicit.
- Do not present router-template output as proof of personalized model performance.
- Do not let docs, governance, launch chatter, or UI work outrun one coherent paid cycle and one real chat-quality fix.
