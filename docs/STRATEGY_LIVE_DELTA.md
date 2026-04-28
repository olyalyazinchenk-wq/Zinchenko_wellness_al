# Strategy Live Delta

Rolling log for strategy and plan corrections between major strategy documents.

## 2026-04-13 12:57 MSK
- Strategic direction remains: Telegram-first "Wellness Clarity" -> Premium Wellness Dossier.
- Execution shift confirmed: prioritize conversion quality and frictionless intake trigger from live chat.
- Updated plan emphasis: keep quality benchmark stability while adding payment-ready handoff after intake.

## 2026-04-13 23:28 MSK
- Payment-ready handoff is now implemented as an explicit runtime state machine, not only planned in docs.
- Conversion messaging refined from single generic CTA to intent-aware CTA variants to reduce over-pushing.
- Benchmark stability preserved after CTA refinement.
- Payment reliability improved with explicit invoice-failure fallback.

## 2026-04-27 13:06 MSK
### Artifact Delta
- Re-read the latest controlling local artifacts before refreshing strategy:
  - `docs/PROJECT_NORTH_STAR_EXECUTION_PLAN_20260427.md`
  - `docs/PRODUCT_LINE_V2_20260426.md`
  - `docs/MANUAL_PAYMENT_MODE_20260426.md`
  - `docs/PROJECT_PULSE_LOG.md`
  - `WellnessBot/data/runtime_state.json`
  - `WellnessBot/data/submissions/20260425T212847Z_1084557944.json`
  - `WellnessBot/data/submissions/20260425T214914Z_1084557944.json`
  - `WellnessBot/data/drafts/20260425T212847Z_1084557944.review.json`
  - `WellnessBot/data/drafts/20260425T214914Z_1084557944.review.json`
  - `WellnessBot/data/product_governance.json`
  - `ops/reports/quality_report_20260421T183148Z.md`
- Runtime memory remains empty, so strategy must use persisted case files and logs as the source of truth.

### Strategy Delta
- Product direction is now sharper than "close any premium case": Antigravity is a Telegram-first service ladder, but `premium` remains the only offer that should prove the product right now.
- `week` should be used as the packaging and walkthrough rail after the branch mess is contained, not as a second parallel product bet.
- `vip` stays in the catalog but remains commercially parked until one safe `premium` delivery and real operator-load evidence exist.
- The flagship promise should now be stated as:
  - `fact-safe navigation map for 72h -> 7d -> 30d, delivered in Telegram, reviewed by a human, and followed up in the same thread`

### Monetization Delta
- Manual concierge payment remains the official pilot mode across the ladder:
  - `week` -> `3900 RUB`
  - `premium` -> `6900 RUB`
  - `vip` -> `14900 RUB`
- No pricing change is justified by the latest artifacts.
- The monetization question for the next cycle is not "what should we charge?" It is "does one safe premium output feel precise and credible enough to justify `6900 RUB`?"
- YooKassa / Telegram provider work stays on a separate ops rail and must not block the next learning cycle.

### Operating Delta
- Persisted branch truth is currently split:
  - `20260425T214914Z_1084557944` is the freshest branch and holds the latest payment/generation timestamps.
  - `20260425T214914Z_1084557944` is not delivery-safe because `lab_quality_check.status=needs_resubmission` and `requires_lab_resubmission=true`, yet generation still ran.
  - `20260425T212847Z_1084557944` is the cleaner safe-delivery rewrite candidate because it does not depend on unreadable lab files, but it still needs a strict factual rewrite.
- Execution rule for the next cycle:
  - treat `20260425T214914Z_1084557944` as an evidence-recovery branch only
  - treat `20260425T212847Z_1084557944` as the sole delivery candidate if the team wants one safe premium closure without waiting on labs
- This is the main strategy correction of the run: freshness does not equal delivery readiness.

### Quality Delta
- The latest review artifacts confirm that the premium issue is not missing content volume. It is unsafe and low-trust structure:
  - invented or unsupported condition framing
  - repetition
  - unclear first-step priorities
  - brand references that appear before need is safely established
- Premium value should therefore be measured by clarity and caution, not by dossier length.

### Loop Risk Delta
- Repeated low-impact loop: debating which branch is "real" without explicitly downgrading one branch to evidence-only status.
- Repeated low-impact loop: generating more artifacts while `requires_lab_resubmission=true` still exists in the freshest branch.
- Repeated low-impact loop: piling governance ideas into `WellnessBot/data/product_governance.json` even though `115` experiments already exist and duplicate titles still repeat.
- Repeated low-impact loop: treating `week` and `vip` as expansion work before one safe `premium` proof exists.

### Higher-Impact Replacement Action
1. Explicitly declare `20260425T212847Z_1084557944` the only delivery candidate.
2. Freeze `20260425T214914Z_1084557944` as evidence-only until readable labs or manual biomarkers arrive.
3. Close or archive the `212847` branch after one factual rewrite and human review decision.
4. Run one `week` walkthrough to verify packaging, payment context, and Russian copy.
5. Keep exactly one post-delivery experiment: compress premium into a stronger `72h -> 7d -> 30d` structure.

### Must-Hold Rules
- Keep Telegram as the primary operating channel.
- Keep manual concierge as the official pilot payment mode.
- Keep `premium` as the active proof path; `week` is a support rail, `vip` is parked.
- Keep one delivery candidate per Telegram user at a time.
- Keep human review mandatory before delivery.
- Keep no-diagnosis, no-treatment, urgent-care routing, and uncertain-lab discipline explicit.
- Do not let product-governance churn or offer-expansion work outrun one safe paid cycle.
