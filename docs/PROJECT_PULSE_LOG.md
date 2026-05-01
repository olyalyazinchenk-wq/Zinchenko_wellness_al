# Project Pulse Log

## 2026-04-13 12:55 MSK
### Delivery Delta
- Live reply quality layer upgraded in bot runtime.
- Dead-end refusal replies removed from benchmark path.
- Premium conversion CTA embedded into live chat response flow.
- Direct intake trigger added from chat phrase: "хочу разбор".
- Mini-app legacy multi-tier branches removed and aligned to single-path funnel.

### Metrics Delta
- Benchmark report: `ops/reports/quality_report_20260413T094502Z.md`
- Empty replies: 0/20
- Refusal replies: 0/20
- Premium CTA mentions in benchmark: 15/20

### Strategy Delta
- Core wedge remains: "Wellness Clarity in Telegram".
- Monetization bridge strengthened: live chat -> Premium Wellness Dossier without friction.

### Risks / Gaps
- Google Drive direct connector is not yet available in current Codex toolset.
- Git CLI is not installed in current shell, so GitHub sync should rely on connector actions unless local git is installed.

### Next 12h Focus
- Keep dialogue quality stable while improving CTA precision by intent.
- Add payment-ready handoff step after intake completion.
- Keep docs/strategy sync consistent across all knowledge bases.

## 2026-04-13 13:08 MSK
### Delivery Delta
- Created cross-platform onboarding artifact: `docs/AGENT_CONTEXT_HUB.md`.
- Created Obsidian mirror onboarding file: `docs/obsidian_mirror/AGENT_CONTEXT_HUB.md`.
- Published onboarding context page to Notion:
  - `https://www.notion.so/3418a9de1d418117a0e5ff5f78a1a00b`
- Published onboarding context artifact to GitHub repo:
  - `olyalyazinchenk-wq/Zinchenko_wellness_al` at `docs/AGENT_CONTEXT_HUB.md`

### Process Delta
- Updated both 12h automations to force explicit "Context for New Model" output each run.
- Knowledge sync standard now includes mandatory onboarding context refresh.

### Risks / Gaps
- Google Drive sync remains queued until connector/login is fully completed.

### Next 12h Focus
- Keep onboarding context current with each execution cycle.
- Add payment-ready handoff step after intake.
- Preserve benchmark quality while improving conversion.

## 2026-04-13 13:18 MSK
### Delivery Delta
- Created visual client dashboard:
  - `docs/OLGA_EXECUTIVE_DASHBOARD.html`
- Created executive markdown report:
  - `docs/OLGA_EXECUTIVE_REPORT.md`
- Published executive report to Notion:
  - `https://www.notion.so/3418a9de1d4181a487eeca8c61e03867`
- Published executive report and dashboard to GitHub repo:
  - `olyalyazinchenk-wq/Zinchenko_wellness_al`
  - `docs/OLGA_EXECUTIVE_REPORT.md`
  - `docs/OLGA_EXECUTIVE_DASHBOARD.html`

### Strategy Delta
- Reporting for customer is now productized as a repeatable dashboard artifact.
- Future updates can reuse same structure every 12h without rebuilding format.

### Next 12h Focus
- Keep dashboard metrics and strategy blocks updated.
- Move execution to payment-ready handoff implementation.

## 2026-04-13 23:28 MSK
### Delivery Delta
- Implemented payment-ready handoff state machine in bot runtime:
  - `awaiting_payment -> payment_received -> dossier_generation_in_progress -> awaiting_human_review -> delivered_to_client`
- Added admin notification on payment handoff (intake completed, invoice sent, waiting payment).
- Added resilient payment recovery path by `invoice_payload` even when in-memory session is missing.
- Added invoice failure guard: if Telegram invoice sending fails, case status becomes `payment_invoice_failed`, admins are notified, user receives manual-followup message.
- Updated `/queue` status mapping to show payment and post-payment stages explicitly.
- Added intent-aware premium CTA variants in live dialogue:
  - direct CTA for high-intent requests,
  - softer CTA for informational requests,
  - default gentle CTA for regular wellness prompts.

### Metrics Delta
- Quality report: `ops/reports/quality_report_20260413T202756Z.md`
- Empty replies: 0/20
- Premium CTA phrase mentions (`хочу разбор`): 15

### Strategy Delta
- Conversion bridge is now less templated while preserving benchmark stability.
- Payment handoff moved from вЂњplannedвЂќ to вЂњimplemented in runtime flowвЂќ.

### Next 12h Focus
- Run real Telegram payment smoke in production-like conditions.
- Tune intent-aware CTA phrasing for higher trust on service-explanation prompts.
- Keep executive docs synchronized after first live paid case.

## 2026-04-13 23:45 MSK
### Validation Delta
- Ran local payment smoke simulation (mocked Telegram events) for 3 critical branches:
  1) invoice sent -> `awaiting_payment`
  2) invoice send failure -> `payment_invoice_failed`
  3) successful payment callback -> `payment_received` (`payment_status=paid`)
- Confirmed all three status transitions are persisted in submission JSON flow.

### Notes
- This was a local runtime simulation with stubbed bot transport.
- Real Telegram payment-provider smoke is still required as the next external validation step.

## 2026-04-13 23:47 MSK
### Ops Delta
- Bot runtime restarted successfully from project venv.
- Resolved web-server startup blocker on busy port 8000 by adding automatic fallback to nearby ports.
- Runtime now starts with polling active and TMA server on `http://localhost:8001` when 8000 is occupied.
- Updated `/tma` link generation to use actual active TMA port instead of hardcoded 8000.

## 2026-04-13 23:55 MSK
### Validation Delta
- Generated payment smoke report:
  - `ops/reports/payment_smoke_20260413T205554Z.md`
- Result: PASS for all simulated payment branches:
  - invoice sent -> `awaiting_payment`
  - invoice send failure -> `payment_invoice_failed`
  - successful payment callback -> `payment_received` (`payment_status=paid`)

### Blocking External Dependency
- Real provider payment test is still blocked because `PAYMENT_TOKEN` is not configured in runtime env.

## 2026-04-14 00:27 MSK
### Delivery Delta
- Implemented explicit manual handoff path for no-payment mode:
  - client gets concierge-style handoff message after intake,
  - admins get a separate manual follow-up notification,
  - queue shows manual handoff instead of generic test-mode wording.
- No-payment internal flow now lands in expert-review path with `payment_status=manual_handoff_no_provider`.

### Validation Delta
- Local smoke confirmed:
  - client messaging is clear and sequential,
  - admin receives manual handoff alert,
  - case status reaches `awaiting_human_review` without pretending online payment exists.

## 2026-04-20 10:47 MSK
### Delivery Delta
- Reframed bot policy from generic wellness assistant to explicit `нутрициологическая навигация`.
- Added source-of-truth policy document:
  - `docs/NUTRITION_NAVIGATION_POLICY_20260420.md`
- Rewrote prompt layer in `WellnessBot/prompts.py` to align with Olga's operating rules:
  - no diagnosis claims,
  - hypotheses instead of medical conclusions,
  - premium and very delicate tone,
  - chronic-background caution,
  - red-flag escalation,
  - supplement guidance allowed in wellness format (including timing/form/dose/compatibility),
  - references to `Сибирское здоровье` and `Vitamax` allowed when appropriate.

### Strategy Delta
- Bot positioning is now explicitly premium nutrition navigation with doctor escalation boundaries, not pseudo-medical advising.

## 2026-04-20 12:01 MSK
### Delivery Delta
- Added personal-data compliance and storage package for production hardening:
  - `docs/PD_STORAGE_ARCHITECTURE_20260420.md`
  - `docs/PD_COMPLIANCE_PACK_20260420.md`
  - `docs/templates/PRIVACY_POLICY_TEMPLATE_20260420.md`
  - `docs/templates/CONSENT_PERSONAL_AND_HEALTH_DATA_TEMPLATE_20260420.md`
  - `docs/templates/PROCESSOR_INSTRUCTION_AGREEMENT_TEMPLATE_20260420.md`
  - `docs/templates/ACCESS_RETENTION_AND_DELETION_REGULATION_TEMPLATE_20260420.md`
  - `docs/templates/PD_REGISTER_AND_DATA_FLOW_TEMPLATE_20260420.md`

### Risk Delta
- Source-of-truth personal data is still stored locally in app data directories and runtime files.
- Obsidian export remains an additional uncontrolled copy path and should be disabled before production handling of sensitive health data.

## 2026-04-20 12:22 MSK
### Delivery Delta
- Added internal AI `judge` layer for dossier quality control:
  - new hard-critic prompt in `WellnessBot/prompts.py`,
  - second-pass critique generation in `WellnessBot/ai_drafting.py`,
  - saved review artifact alongside each draft as `*.review.json`,
  - admin handoff now includes a compact judge summary with weak points, risk flags, and rewrite priorities.

### Quality Delta
- Draft generation is no longer single-pass only: the system now explicitly attacks weak logic, generic filler, unsupported supplement advice, and missing doctor-escalation boundaries before expert approval.

## 2026-04-20 12:31 MSK
### Strategy Delta
- Extended the internal `judge` from pure quality-control into product-value critique:
  - now audits not only safety and logic,
  - but also perceived premium value,
  - market demand risk,
  - weak differentiation,
  - and opportunities to make the product more commercially strong without crossing legal/medical boundaries.

## 2026-04-20 12:41 MSK
### Delivery Delta
- Added a separate internal `growth architect` layer after the judge:
  - new product-strategy prompt in `WellnessBot/prompts.py`,
  - third-pass AI analysis in `WellnessBot/ai_drafting.py`,
  - saved growth artifact as `*.growth.json`,
  - admin handoff now includes concrete demand, positioning, conversion, retention, referral, and experiment ideas.

### Product Delta
- The system now separates three different jobs:
  - draft creation,
  - harsh internal criticism,
  - commercial-strength architecture.
- This makes it easier to see not only what is weak, but what exactly should be changed so the product is more wanted and more commercially resilient.

## 2026-04-20 12:52 MSK
### Operations Delta
- Added automatic internal-review routing on top of draft generation:
  - submissions now store `internal_review` signals,
  - queue statuses can escalate to quality rework, market/value rework, or both,
  - admin handoff now surfaces internal review flags directly in the summary.

### Triage Delta
- Case prioritization is no longer based only on technical readiness (`draft/pdf ready`).
- The pipeline now distinguishes between:
  - technically ready,
  - quality-risky,
  - commercially weak / value-unclear,
  - and dual-risk cases that need deeper rework before approval.

## 2026-04-20 13:03 MSK
### Intelligence Delta
- Added cumulative `product insights` memory:
  - growth and value signals are now aggregated across cases into `data/product_insights.json`,
  - the memory is case-keyed, so repeated regeneration updates the same case instead of blindly duplicating counts,
  - admin command `/insights` now shows repeated demand risks, value gaps, positioning upgrades, conversion ideas, retention ideas, referral ideas, and next experiments.

### Product Learning Delta
- The bot no longer learns only per-case.
- It now starts building a cross-case product-learning layer, so recurring weaknesses in offer clarity, premium value perception, and market demand can be seen as portfolio-level patterns.

## 2026-04-20 13:14 MSK
### Admin Ops Delta
- Added admin-level operational dashboards:
  - `/review` for prioritized internal-review cases,
  - `/weekly` for 7-day and 30-day product summaries based on accumulated insights.

### Decision Delta
- The bot now supports not only generation and critique, but also lightweight management review:
  - which cases need rework first,
  - what value problems repeat,
  - what commercial experiments should be tested next.

## 2026-04-20 13:24 MSK
### Automation Delta
- Added proactive digest delivery for product governance:
  - background `weekly_digest_loop()` now checks whether a Monday digest is due after 10:00 MSK,
  - combined 7-day + 30-day digest is sent automatically to admin chats,
  - digest state is persisted to avoid duplicate sends within the same ISO week,
  - admin command `/digestnow` added for manual preview / spot-checks.

### Rhythm Delta
- Product learning is no longer only pull-based (`/weekly`).
- The system now has a push-based management rhythm, which is better for consistent product review and decision-making.

## 2026-04-20 13:37 MSK
### Governance Delta
- Added execution-layer governance on top of insights:
  - dedicated `product_governance.json` storage,
  - automatic seeding of proposed experiments from recurring product insights,
  - admin dashboards for governance, experiments, and decisions,
  - `/decide` for logging accepted decisions,
  - `/expstatus` for moving experiments through `proposed -> active -> validated/rejected`.

### Execution Delta
- The product system now closes the loop between:
  - detecting repeated problems,
  - proposing experiments,
  - logging decisions,
  - and tracking which experiments are actually being run.

## 2026-04-20 13:49 MSK
### Action Delta
- Upgraded weekly governance from passive summary to action-oriented brief:
  - new `Action Brief (7d)` helper extracts 3 main recurring problems, recent decisions, and the top experiments to move now,
  - auto-digest now includes that brief before the longer 7d/30d summaries,
  - admin command `/brief` added for instant access to the compact action view.

### Management Delta
- Weekly review is now easier to execute:
  - less scrolling through narrative summaries,
  - faster prioritization,
  - and a clearer bridge from insights to actual weekly moves.

## 2026-04-20 14:01 MSK
### Learning Delta
- Added experiment outcome memory into the product loop:
  - validated/rejected experiments are now summarized into a reusable learning context,
  - growth architect receives that context during new growth-pass generation,
  - admin command `/learnings` added for direct review of what has already worked or failed.

### Strategy Delta
- Product recommendations are no longer based only on fresh pattern detection.
- They now start incorporating historical evidence from experiment outcomes, reducing the risk of repeating already-rejected ideas and increasing reuse of validated moves.

## 2026-04-20 14:13 MSK
### Guardrail Delta
- Added duplication guard against recycled rejected experiments:
  - recurring insights that are too similar to already rejected experiments are now blocked from being re-seeded as new proposed experiments,
  - blocked candidates are recorded in governance memory for later audit.

### Prioritization Delta
- Upgraded `Action Brief` to be governance-aware:
  - weekly focus now tries to skip problem zones where validated experiments already exist,
  - making the brief less repetitive and more action-disciplined.

## 2026-04-20 14:26 MSK
### Decision Delta
- Added auto-suggested management decisions on top of product insights and governance memory:
  - recurring unresolved demand/value/premium-risk signals are now converted into concrete recommended decisions,
  - suggestions are deduplicated against already accepted decisions,
  - if signal-based suggestions are not enough, active/proposed experiments are escalated into next-step decisions.

### Admin Delta
- Added `/suggestdecisions` for direct review of recommended decisions.
- Weekly product digest now includes a `Suggested Decisions` block, so the admin sees not only what is wrong, but also what should be decided next.
- Cleaned `/digestnow` admin replies to remove garbled text and restore readable Russian responses.

## 2026-04-20 14:32 MSK
### Execution Delta
- Added `/applydecision <номер>`:
  - an admin can now apply a suggested decision directly from the `/suggestdecisions` list without manual copying,
  - the accepted decision is written into governance memory with structured details: why now, next move, source signal, and analysis window.

### Usability Delta
- `Suggested Decisions` now includes a direct usage hint for fast execution.
- The admin loop is now shorter: detect signal -> suggest decision -> apply decision -> review in `/decisions`.

## 2026-04-20 14:35 MSK
### Operations Delta
- Added execution planning for decisions:
  - each decision can now store `owner`, `deadline`, and `KPI`,
  - governance summary now distinguishes between planned and unplanned decisions,
  - decision log shows whether the execution block is already assigned or still missing.

### Admin Delta
- Added `/decisionplan <DEC-id> <owner> | <deadline> | <KPI>` for quick execution setup from Telegram.
- `/decide` and `/applydecision` now push the admin toward the next operational step instead of leaving accepted decisions without follow-through.

## 2026-04-20 14:38 MSK
### Control Delta
- Added `Execution Gaps` tracking for accepted decisions:
  - governance now detects which decisions are still missing `owner`, `deadline`, or `KPI`,
  - the weekly action brief now surfaces these execution gaps directly,
  - the auto-digest now includes a dedicated execution-gap block.

### Admin Delta
- Added `/gaps` for direct review of execution holes from Telegram.
- Each gap now includes the exact `/decisionplan` command shape needed to close it quickly.

## 2026-04-20 15:05 MSK
### Security Delta
- Started P0 hardening after full audit:
  - TMA is now disabled by default unless explicitly enabled via environment,
  - TMA session API now requires an access token bound to the active Telegram session,
  - completed-case fallback through plain `user_id` lookup was removed from the TMA endpoint.

### Data Delta
- Submission enrichment from OCR / Vision is now persisted into stored cases instead of living only in transient session memory.
- Storage writes for submissions, governance, runtime state, and reports were moved to atomic file writes to reduce corruption and lost-update risk.

### Compliance Delta
- Client PDF wording was shifted away from medical framing toward nutrition-navigation wording.
- HTML PDF rendering now uses autoescaping for safer output handling.
- Content CTA was updated to DM-first logic so symptoms are not encouraged in public comments.

## 2026-04-20 15:51 MSK
### Payment Delta
- Hardened payment validation for the premium dossier flow:
  - invoice payload is now bound to both submission and Telegram user,
  - pre-checkout now validates payload, amount, currency, case existence, and owner match,
  - successful payment no longer trusts the event blindly and checks the expected case contract before moving the case to `paid`.

### Safety Delta
- Dossier generation is now blocked for payment-enabled flow unless the stored case is already marked as `paid`.
- Payment anomalies are now recorded into the case instead of silently continuing the pipeline.

## 2026-04-20 16:02 MSK
### Public Sync Delta
- Synchronized the external project layer with the real current runtime:
  - `README.md` now reflects the real command set, current runtime status, and current environment flags,
  - landing copy no longer describes the build as an early future-state bot-token step,
  - public bot links were replaced with the actual Telegram bot link.

### Messaging Delta
- Landing messaging now better matches the safe product frame:
  - stronger human-in-the-loop language,
  - cleaner non-medical explanation of AI draft usage,
  - explicit data-care reminder for sensitive client details.

## 2026-04-20 17:44 MSK
### Architecture Delta
- Completed the first service extraction out of `main.py`:
  - payment constants, invoice payload logic, payment-context assembly, and payment-event validation were moved into `WellnessBot/payment_flow.py`,
  - `main.py` now imports payment service helpers instead of owning that logic inline.

### Refactor Delta
- This is the first practical step from monolith critique toward service separation:
  - payment flow is now easier to audit, test, and evolve independently,
  - future extraction of case/governance/render services is now structurally simpler.

## 2026-04-20 23:13 MSK
### Architecture Delta
- Completed the second service extraction out of `main.py`:
  - case lifecycle helpers were moved into `WellnessBot/case_service.py`,
  - submission payload building, submission persistence, enrichment persistence, status transitions, and session restoration now live outside the main bot module.

### Refactor Delta
- `main.py` now depends on explicit service modules for both payment flow and case flow.
- This reduces monolith pressure around intake, submission state, and dossier lifecycle, and makes the next extractions more mechanical and less risky.


## 2026-04-21 00:00 MSK
### Architecture Delta
- Completed the third service extraction out of `main.py`:
  - governance and product-insights core helpers were moved into `WellnessBot/governance_service.py`,
  - `main.py` now imports governance summaries, experiment/decision mutation helpers, insight aggregation, and growth-governance context from a dedicated service module.

### Refactor Delta
- The governance extraction was done conservatively:
  - admin command behavior and downstream flows were preserved,
  - weekly digest and later-stage planning helpers remain in `main.py` for the next extraction pass,
  - the project now compiles with `py_compile` after the split.

## 2026-04-21 00:06 MSK
### Architecture Delta
- Completed the second-pass governance extraction out of `main.py`:
  - review dashboard helpers, windowed summaries, action-priority brief logic, suggested-decision logic, digest timing helpers, and decision-plan parsing now also live in `WellnessBot/governance_service.py`,
  - `main.py` has been reduced further toward an orchestration layer instead of owning governance analytics inline.

### Refactor Delta
- The governance split is now effectively end-to-end for the current admin analytics surface:
  - admin commands continue to call the same behaviors through imports,
  - weekly digest text generation and digest scheduling checks now run through the service layer,
  - `py_compile` still passes after the second extraction pass.

## 2026-04-21 00:20 MSK
### Verification Delta
- Added a reusable smoke-check for the admin/governance/digest surface in `ops/admin_governance_smoke.py`.
- Generated a human-readable verification artifact in `docs/SMOKE_ADMIN_GOVERNANCE_20260421.md`.
- Added minimal automated regression coverage in `tests/test_governance_service.py`.

### Bug Fix Delta
- Smoke verification exposed two non-trivial governance issues and both were fixed immediately:
  - digest generation referenced `MOSCOW_TZ` without a live module constant,
  - experiment IDs could collide when multiple experiments were created within the same timestamp window.
- Governance IDs now include an entropy suffix, and UTC handling in `WellnessBot/governance_service.py` was cleaned up to remove deprecated `utcnow()` usage.

### Confidence Delta
- `unittest` coverage for the governance layer now passes.
- the reusable smoke script now passes end-to-end on isolated storage.
- current confidence is materially higher for admin summaries, suggested decisions, digest generation, and governance mutation paths.

## 2026-04-21 00:26 MSK
### Verification Delta
- Added a reusable smoke-check for the payment and case lifecycle surface in `ops/payment_case_smoke.py`.
- Generated a verification artifact in `docs/SMOKE_PAYMENT_CASE_20260421.md`.
- Added minimal automated regression coverage in `tests/test_payment_case_services.py`.

### Flow Delta
- The project now has repeatable verification across two launch-critical planes:
  - admin/governance/digest,
  - case lifecycle and payment validation.
- The payment/case smoke confirms submission assembly, payment-context generation, mismatch rejection, enrichment persistence, status transitions, and session restoration from stored submission state.

### Confidence Delta
- `unittest` coverage for payment and case services now passes.
- the reusable payment/case smoke script now passes end-to-end on isolated storage.
- launch confidence improved for intake persistence, payment verification logic, and post-payment case continuity.

## 2026-04-21 00:46 MSK
### Launch Readiness Delta
- Ran a live local launch-readiness walkthrough instead of another refactor pass.
- Verified that preflight passes, the local bot starts, polling starts, and the background loops boot successfully.
- During the live walkthrough, found and fixed a missing weekly-digest orchestration function in `WellnessBot/main.py` that had been lost during refactoring.

### Pilot Verdict Delta
- Added `docs/PILOT_LAUNCH_CHECKLIST_20260421.md` as the current decision artifact.
- Current verdict is `not yet pilot-ready`.
- The primary blocker is no active `PAYMENT_TOKEN` in the working environment, which means the real paid Telegram branch cannot yet be completed honestly end-to-end.

### Decision Delta
- Next required moves are now explicit:
  - connect and verify live payment provider credentials,
  - run one fresh real Telegram e2e walkthrough,
  - formalize the short operator launch checklist,
  - then re-evaluate pilot readiness.

## 2026-04-21 00:50 MSK
### Launch Ops Delta
- Added the operator day-of-launch protocol in `docs/OPERATOR_LAUNCH_PROTOCOL_20260421.md`.
- Added the live payment activation runbook in `docs/LIVE_PAYMENT_ENABLE_RUNBOOK_20260421.md`.

### Execution Delta
- Launch preparation is now split into two explicit layers:
  - operator handling for real client cases,
  - payment activation steps for the real Telegram paid branch.
- This reduces ambiguity around what to do next and what exactly blocks the move to `pilot-ready`.

### Decision Delta
- The remaining gating path is now fully operational, not architectural:
  - insert live `PAYMENT_TOKEN`,
  - restart bot,
  - complete one real paid Telegram walkthrough,
  - re-check pilot readiness.

## 2026-04-21 01:10 MSK
### Review System Delta
- Added `docs/CLIENT_REVIEW_SYSTEM_20260421.md` to define where client reviews should actually be collected and published.
- Added `docs/templates/CLIENT_REVIEW_REQUEST_TEMPLATES_20260421.md` with ready-to-send Telegram copy for private feedback, publication consent, and testimonial approval.

### Operations Delta
- Updated the operator launch protocol so review capture is part of post-delivery operations.
- Updated the pilot checklist so review collection is treated as a real operational readiness item rather than an afterthought.

### Decision Delta
- The launch review model is now explicit:
  - collect reviews privately in Telegram first,
  - request publication consent separately,
  - publish only approved cleaned versions to controlled public surfaces.

## 2026-04-21 01:24 MSK
### Review Ops Delta
- Added `docs/CLIENT_REVIEW_REGISTER_GUIDE_20260421.md` and `docs/templates/CLIENT_REVIEW_REGISTER_TEMPLATE_20260421.csv` so review capture now has an operational register instead of loose chat fragments.
- Added `docs/POST_DELIVERY_REVIEW_PLAYBOOK_20260421.md` to define the exact post-delivery timing and message logic for requesting reviews.

### Landing Delta
- Added a dedicated reviews section to `index.html` and `styles.css`.
- The landing now explains the review policy honestly and creates a ready-to-fill premium testimonial area without inventing fake client quotes.

### Decision Delta
- Review collection is now not only designed conceptually but operationalized across:
  - landing,
  - operator flow,
  - client messaging,
  - internal review tracking.

## 2026-04-21 01:39 MSK
### Review Reply Delta
- Added `docs/REVIEW_REPLY_POLICY_20260421.md` to define how the bot and operator should answer every review without flattery or emotional submission.
- Added `docs/templates/REVIEW_REPLY_TEMPLATES_20260421.md` with reply templates for positive, mixed, critical, and boundary-sensitive reviews.

### Product Behavior Delta
- Added `REVIEW_REPLY_PROMPT` to `WellnessBot/prompts.py`.
- Added review reply generation and deterministic fallback logic to `WellnessBot/ai_drafting.py`.
- Added `tests/test_review_reply_logic.py` to lock in warm, objective, non-fawning behavior.

### Decision Delta
- Review handling is now elevated from simple collection to a real brand-behavior layer:
  - every review gets a reply,
  - warmth stays,
  - brand spine stays,
  - medical and legal boundaries stay visible.

## 2026-04-21 01:56 MSK
### Lab Safety Delta
- Reworked `WellnessBot/lab_ocr.py` into a conservative parsing pipeline that only extracts clearly readable biomarker lines.
- Added explicit OCR quality assessment and resubmission logic for low-confidence lab uploads.
- Updated `WellnessBot/main.py` so unsafe OCR results trigger a client resend request instead of silent downstream use.

### Product Safety Delta
- Added `lab_quality_check` and `requires_lab_resubmission` into submission/session payloads.
- Hardened the dossier prompt so unconfirmed OCR-derived lab values must not be used as trusted evidence or as a basis for supplement logic.
- Added `docs/LAB_RESULT_SAFETY_POLICY_20260421.md` and test coverage for OCR safety behavior.

### Decision Delta
- The project now prefers blocked automation over unsafe lab interpretation:
  - unclear labs are stopped,
  - the client is asked for a clearer file,
  - uncertain numbers must not drive recommendations.

## 2026-04-21 02:08 MSK
### Nutrition Range Delta
- Added `WellnessBot/nutrition_reference_ranges.py` as a dedicated nutritiological interpretation layer for structured biomarkers.
- Parsed biomarkers can now be enriched with `nutrition_optimal_range`, `nutrition_range_basis`, and `nutrition_status`.

### Interpretation Delta
- Updated the dossier prompt so confirmed labs should be interpreted primarily through nutritiological ranges rather than the laboratory printout band.
- Preserved laboratory source ranges as raw context, but no longer as the main interpretive anchor for the wellness explanation.

### Decision Delta
- The product now distinguishes clearly between:
  - what the lab printed,
  - what the nutrition-navigation layer treats as suboptimal, optimal, or above range.

## 2026-04-21 02:18 MSK
### Helix Catalog Delta
- Added `WellnessBot/helix_master_catalog.py` as the start of a dedicated Helix master-catalog layer.
- Preserved official Helix top-level category structure separately from nutritiological interpretation logic.

### Architecture Delta
- Added `docs/HELIX_MASTER_CATALOG_POLICY_20260421.md` to formalize the rule that Helix naming/codes/categories are the catalog source of truth.
- Added tests for Helix master-catalog metadata and nutrition overlay attachment.

### Decision Delta
- The project now explicitly separates:
  - Helix catalog identity,
  - nutritiological interpretation overlay.
- This is the required architecture before expanding to the full official Helix list.

## 2026-04-21 02:24 MSK
### Lab Order Link Delta
- Added Olga's HelloDoc links for ordering Helix / Invitro labs into the bot lab-upload guidance.
- Added `docs/LAB_ORDER_LINKS_HELLODOC_20260421.md` as the approved wording and link policy.

### Decision Delta
- The bot can now give clients a practical route to order labs without making labs mandatory before starting the intake.

## 2026-04-21 02:31 MSK
### Lab Routing Copy Delta
- Strengthened the client-facing lab scenario:
  - if labs already exist, send PDF/photo/text directly into the current Telegram chat,
  - if labs do not exist, the client can continue intake and order Helix / Invitro through HelloDoc.
- Updated the HelloDoc policy and nutrition-navigation policy with the preferred routing phrase.

### Decision Delta
- The bot should not behave like an internal laboratory catalog.
- The practical launch behavior is now clear: collect existing results here, route missing labs through HelloDoc, then interpret confirmed results through nutritiological references.

## 2026-04-21 02:42 MSK
### Hosting Decision Delta
- Added `docs/HOSTING_VPS_DECISION_20260421.md` to clarify whether VPS hosting is needed now.
- Reviewed current local ops scripts and existing VM/systemd starter assets.

### Decision Delta
- VPS is not the first launch blocker; live payment and real e2e still come first.
- VPS / cloud VM becomes necessary before unattended paid traffic or real public pilot operation.
- Recommended path:
  - finish YooKassa and live e2e locally,
  - then prepare VM deployment,
  - move to VPS before broader launch.

## 2026-04-22 00:00 MSK
### Payment Strategy Delta
- Added `docs/PAYMENT_AND_LAUNCH_STRATEGY_20260422.md` as the new strategy artifact after YooKassa friction.
- Reframed launch around two tracks:
  - target automated Telegram payment through YooKassa,
  - controlled concierge payment path if YooKassa stalls.

### Decision Delta
- YooKassa remains the target clean payment path, but it should not block product validation indefinitely.
- The next move is a short payment activation sprint with a clear branch decision:
  - if YooKassa works, run live paid pilot,
  - if YooKassa stalls, run a limited concierge pilot while resolving payment provider setup in parallel.

## 2026-04-22 00:12 MSK
### Manual Payment Decision Delta
- Added `docs/MANUAL_PAYMENT_CONFIRMATION_DECISION_20260422.md`.
- Fixed the concierge fallback decision before implementation:
  - no automatic paid dossier generation in manual fallback,
  - use `manual_payment_pending` before operator confirmation,
  - use `manual_payment_confirmed` after operator confirmation,
  - only then allow dossier generation.

### Decision Delta
- The project now treats manual payment fallback as an auditable controlled-pilot mode, not as a silent bypass of the payment branch.

## 2026-04-22 00:24 MSK
### Manual Payment Implementation Delta
- Added manual payment state helpers in `WellnessBot/payment_flow.py`.
- Updated `WellnessBot/main.py` so no-provider fallback now enters `manual_payment_pending` instead of generating a dossier immediately.
- Added an admin callback button to confirm external/manual payment and then start dossier generation.
- Updated queue/operator wording for `manual_payment_pending` and `manual_payment_confirmed`.

### Safety Delta
- Dossier generation is now gated by confirmed payment status:
  - Telegram payment `paid`,
  - or admin-confirmed `manual_payment_confirmed`.


## 2026-04-22 23:25 MSK
### Russian Interface Recovery Delta
- Fixed mojibake in `WellnessBot/main.py`: buttons, intake prompts, payment copy, admin callbacks, queue labels, loading states, voice/photo responses, and mini-app entry button now render in readable Russian.
- Updated client-facing copy to avoid unnecessary English terms: `AI` -> `?????????`, `intake` -> `??????`, mixed `Premium Wellness Dossier` copy -> Russian premium dossier wording.
- Updated `WellnessBot/texts.py` price from `2 990 ???.` to `6 900 ???.`.
- Created local backup before automated recovery: `WellnessBot/main.py.before_ru_ui_fix.bak`.

### Verification Delta
- `py_compile` passed for `WellnessBot/main.py` and `WellnessBot/texts.py`.
- `python -m unittest discover -s tests` passed: 24 tests OK.
- `ops/payment_case_smoke.py` passed: `SMOKE_OK`.
- `ops/admin_governance_smoke.py` passed: `SMOKE_OK`.
- Bot restarted successfully; polling active for `@zinchenko_wellness_ai_1_bot`, no startup errors in stderr tail.

### Decision Delta
- The Telegram interface must remain Russian-first and grammatically clean.
- Any future UI text changes must be checked for mojibake before launch testing.


## 2026-04-22 23:36 MSK
### Live E2E Delta
- Ran post-Russian-fix live operational check.
- Preflight passed and bot polling stayed active.
- Live case `20260422T202504Z_<REDACTED_ID>` reached `manual_payment_confirmed` and generated a PDF.
- Found a real launch-blocking admin delivery bug: Telegram rejected PDF notification because caption was too long.
- Fixed admin PDF delivery by using a short document caption and sending detailed summaries as separate Telegram-safe chunks.
- Resent the latest admin notification after the fix.

### Current Readiness Delta
- Controlled concierge path is technically closer to pilot-ready.
- Latest case is still pending human review because internal review flags include `quality_rework` and `market_rework`.
- Automated paid launch remains blocked until YooKassa `PAYMENT_TOKEN` is live and verified.

### Artifacts
- Added `docs/LIVE_E2E_WALKTHROUGH_20260422.md`.
- Updated `docs/PILOT_LAUNCH_CHECKLIST_20260421.md`.


## 2026-04-22 23:52 MSK
### Premium Intake Safety Delta
- Audited the current bot flow after the request to make the bot reason from a stronger client questionnaire.
- Found the main weakness: the old intake was too short for a premium nutrition-navigation dossier and did not separately collect complaint dynamics, nutrition, digestion, sleep/stress, activity, and detailed medication/supplement risk background.
- Expanded Telegram intake from 7 steps to 12 structured steps.
- Added new stored medical-context fields: `complaint_pattern`, `nutrition`, `digestion`, `sleep_stress`, `activity`.
- Reinforced dossier prompt boundaries: no medication prescribing, no treatment protocols, no medical conclusions; supplement guidance only as cautious wellness support.

### Verification Delta
- `py_compile` passed for `main.py`, `case_service.py`, and `prompts.py`.
- Unit tests passed: 24 tests OK.
- Payment/case smoke passed: `SMOKE_OK`.
- Admin/governance smoke passed: `SMOKE_OK`.

### Artifact
- Added `docs/SAFE_PREMIUM_INTAKE_REVISION_20260422.md`.


## 2026-04-23 00:32 MSK
### Live Intake Quality Hardening Delta
- Fresh 12-step intake case `20260422T210234Z_<REDACTED_ID>` completed and generated a PDF.
- Verified that all new intake fields were saved: complaint pattern, nutrition, digestion, sleep/stress, activity, background, red flags, lab notes.
- Found a PDF schema mismatch: the LLM generated the newer dossier JSON schema while the HTML PDF template expected legacy fields.
- Added `normalize_dossier_pdf_data()` to map the generated dossier schema into the PDF template fields.
- Added `apply_safe_action_floor()` to inject a concrete safe baseline plan when labs are missing or background is complex.
- Changed PDF section title from `????? ?????????????` to `????????? ????? ?????????`.
- Moved safe action floor before internal judge review so the judge evaluates the final payload, not the raw AI draft.
- Fixed false-positive quality rework logic: positive supplement-risk statements such as no unsafe supplement recommendations no longer trigger quality rework.

### Result
- Latest case status moved from `review_priority_quality_and_market` to `review_priority_market_rework`.
- Safety/quality blocker cleared.
- Remaining issue is product-value/packaging review before client delivery.

### Verification
- `py_compile` passed.
- Unit tests passed: 24 tests OK.


## 2026-04-24 14:52 MSK
### Audio Intake Delta
- Added Telegram `F.audio` handler alongside existing `F.voice` support.
- Introduced shared audio download helpers in `WellnessBot/voice_processor.py`.
- Added compatibility checks for synchronous STT path and clear client fallback text for unsupported or too-large audio files.
- Bot now routes recognized audio text back through the same intake/chat pipeline as ordinary text.

### Current Practical Behavior
- Voice notes continue to work.
- Audio files are now accepted by the bot.
- In the current Yandex sync STT mode, the most reliable audio-file path is short `.ogg/.opus` audio.
- If an audio file is too long, too heavy, or incompatible with the current STT mode, the bot explains what to do next instead of silently failing.

### Verification Delta
- `py_compile` passed for `main.py` and `voice_processor.py`.
- Unit tests passed: 25 tests OK.
- Bot restarted successfully after the change.


## 2026-04-24 15:42 MSK
### Voice STT Auth Fix Delta
- Investigated failed voice-note transcription after the client saw the "could not transcribe" response.
- Root cause: Yandex SpeechKit returned `401 Unauthorized` for the STT request.
- Switched the local Yandex configuration to IAM-token mode and refreshed the IAM token without printing secrets.
- Rewrote `.env` files as UTF-8 without BOM after Windows PowerShell wrote a BOM that made `BOT_TOKEN` unreadable to Python.
- Updated `ops/bot-start.ps1` so it refreshes the Yandex IAM token automatically before starting the bot when `LLM_USE_IAM_TOKEN=true`.

### Verification Delta
- SpeechKit auth smoke returned non-401 status.
- Unit tests passed: 25 tests OK.
- Bot restarted with a single active process and polling is active.

## 2026-04-24 16:38 MSK вЂ” DeepSeek Connector Prepared

- Разделены настройки текстовой LLM и распознавания голоса: LLM_* теперь отвечает за модель разборов/ответов, STT_* — за голосовые сообщения.
- Подготовлен безопасный мастер подключения DeepSeek: ops\set-deepseek-token.cmd / ops\set-deepseek-token.ps1.
- DeepSeek настроен через OpenAI-compatible режим: LLM_PROVIDER=openai_compatible, LLM_BASE_URL=https://api.deepseek.com, LLM_API_MODE=chat_completions, модель по умолчанию deepseek-v4-flash.
- Yandex SpeechKit сохранён для голосовых через STT_PROVIDER=yandex_speechkit, чтобы подключение DeepSeek не ломало аудио/voice intake.
- ops\bot-start.ps1 обновлён: IAM-токен Яндекса теперь может обновляться отдельно для STT и не перезаписывает DeepSeek LLM_API_KEY.
- Проверка: py_compile OK, python -m unittest discover -s tests OK, 25 тестов пройдены.
- Live bot перезапущен в текущем режиме Яндекс LLM до ввода реального DeepSeek API key.

Next gate:
- Ввести DeepSeek API key через ops\set-deepseek-token.cmd, затем перезапустить бота и провести live smoke: текстовый вопрос, голосовое, intake/PDF.

## 2026-04-24 18:02 MSK вЂ” DeepSeek Key Connected, Balance Gate Found

- DeepSeek API key was written to env safely and tested through https://api.deepseek.com.
- API authentication reached DeepSeek successfully, but the provider returned 402 Insufficient Balance.
- Decision: keep the DeepSeek key stored as reserved DEEPSEEK_API_KEY, but restore active LLM_PROVIDER=yandex_foundation so the live bot does not fail for clients.
- Current active route: Yandex Foundation Models for text + Yandex SpeechKit for voice.
- Next gate: top up DeepSeek balance, then switch LLM_PROVIDER=openai_compatible, LLM_API_KEY=DEEPSEEK_API_KEY, LLM_MODEL=deepseek-v4-flash, LLM_API_MODE=chat_completions, LLM_BASE_URL=https://api.deepseek.com and run smoke again.

## 2026-04-24 20:54 MSK вЂ” Direct DeepSeek Activated

- DeepSeek balance was topped up by the owner.
- Active LLM switched from yandex_foundation to direct DeepSeek via OpenAI-compatible mode.
- Current active config: LLM_PROVIDER=openai_compatible, LLM_MODEL=deepseek-v4-flash, LLM_API_MODE=chat_completions, LLM_BASE_URL=https://api.deepseek.com.
- Yandex SpeechKit remains active for voice/audio: STT_PROVIDER=yandex_speechkit.
- Smoke result: DeepSeek API call returned successfully; no more 402 Insufficient Balance.
- Live bot restarted successfully; polling is active for @zinchenko_wellness_ai_1_bot.

Next gate:
- Run Telegram live E2E: short text question, voice message, intake start, then controlled dossier branch.

## 2026-04-24 21:02 MSK вЂ” Dossier Actionability Upgrade

- Incorporated owner critique: dossier was safe but too generic and needed stronger actionable value.
- DOSSIER_DRAFT_PROMPT now requires phased plans: 24-72h, 7 days, 2-4 weeks, 1 month, 3 months.
- Doctor escalation must now name relevant specialists when supported by intake context: therapist, endocrinologist, gynecologist, gastroenterologist, hematologist, cardiologist, neurologist.
- Supplement pause must now be explicitly justified, and withheld supplements must be replaced with a concrete non-medical action plan.
- DOSSIER_JUDGE_PROMPT now audits generic doctor referrals, unjustified pauses, repeated supplement logic, missing lab/exam lists, and absent timeline.
- pply_safe_action_floor() now injects a concrete phased route into PDF data even when the LLM draft is too vague.
- Safety filter removes high-risk supplement items such as iodine/selenium/iron in complex or uncertain cases.
- Verification: py_compile OK, unittest discover OK (25 tests), local action-floor smoke OK, live bot restarted successfully.

## 2026-04-24 21:11 MSK вЂ” Accuracy / Medical Error Prevention Upgrade

- Owner clarified that the product must behave like a drafting instrument for an experienced expert and must minimize medical-error risk.
- Critical infrastructure fix: lab_ocr.recognize_text() no longer depends on active LLM_API_KEY; when text LLM is DeepSeek, Yandex OCR now uses separate Yandex credentials from STT_*.
- Added tests proving OCR uses Yandex STT/IAM credentials under LLM_PROVIDER=openai_compatible and falls back to Yandex LLM credentials only when the active provider is Yandex.
- DOSSIER_DRAFT_PROMPT now includes Medical Error Prevention Protocol: separate confirmed facts, cautious hypotheses, and unconfirmed data; no OCR-derived number may drive recommendations unless quality/units/source are clear.
- DOSSIER_JUDGE_PROMPT now audits failure to separate facts/hypotheses/uncertainty and unsafe use of uncertain lab data.
- PDF safe-action layer now injects a visible accuracy protocol and final accuracy note: uncertain labs must be resent or manually confirmed; medical decisions remain doctor-level.
- Verification: py_compile OK, unittest discover OK (27 tests), action-floor smoke OK, live bot restarted successfully.

## 2026-04-24 21:56 MSK вЂ” Complex Case E2E Smoke / Safety Filters

- Ran controlled complex-case smoke through direct DeepSeek: draft generation, internal judge, normalized JSON, PDF render.
- Output files:
  - ops/reports/complex_case_dossier_payload.json
  - ops/reports/complex_case_judge_report.json
  - ops/reports/complex_case_dossier.pdf
- Safety checks passed: phased plan present, accuracy protocol present, doctor route present, no iron/iodine/selenium/self-supplement scheme in schemes.
- Added post-processing filters for complex cases: remove supplement/medication hints from schemes and major client fields, sanitize diagnosis-like wording, limit primary specialist route, cap dditional_control to 14 items.
- Verification: py_compile OK, unittest discover OK (27 tests), multiple complex-case smoke runs OK, live bot restarted successfully.
- Critical product finding: safety is improved, but judge still flags premium-value issues: repetition, overloaded sections, missing one-page executive summary, need stronger first-week action card and grouped doctor questions.
- Decision: do not treat this as final launch-quality PDF without human review. Next architecture step is PDF/dossier structure redesign, not more prompt/filter tweaking.

## 2026-04-24 22:21 MSK вЂ” Live Bot Smoke Test / Dossier Orchestration Fix

- Ran live Telegram test with owner as client: intake progressed, documents uploaded, manual payment confirmed, dossier generation started.
- DeepSeek text calls returned 200 OK.
- Yandex OCR worked for two photo uploads; one PDF returned 400 Bad Request, so lab data was marked unsafe: 
equires_lab_resubmission=true, parsed biomarkers remained empty.
- Found orchestration bug: dossier case could stay stuck in dossier_generation_in_progress after draft/review creation when later review/growth/PDF flow did not complete cleanly.
- Added timeouts to generation steps: draft 120s, judge 90s, growth 90s, so growth cannot hang the entire case.
- Recovered live smoke case 20260424T190738Z_<REDACTED_ID>: rendered PDF from draft, set pdf_path, updated status to waiting_human_review.
- Sent recovered test PDF to admin Telegram chat via bot proxy.
- Current product signal: safe behavior on uncertain labs is correct; PDF quality still requires human review and later structure redesign.

## 2026-04-24 23:10 MSK вЂ” Premium Dossier / 30-Day Support Upgrade

- Owner critique incorporated: PDF must feel like premium personal navigation, not a generic wellness article.
- Added premium first pages to the dossier: 14-day executive map, 3-step recovery protocol, personalized 3-day start, doctor questions, circadian checklist, and 30-day support offer.
- Added before-payment value framing in premium offer text: mini-example of a personalized one-day plan and clear difference from free advice.
- Added client material: docs/CLIENT_CIRCADIAN_QUICK_WIN_CHECKLIST.md.
- Added 30-day post-dossier support path: after delivery, clients can send analyses, photos, questions, and reactions; bot appends follow-ups to the case and responds as ongoing support.
- Photo-complaint route added: bot asks location/duration/dynamics/pain/itch/bleeding/temperature, does not diagnose by photo, and routes to appropriate medical escalation when needed.
- Premium PDF sections renamed and shortened: "Питание На Первые 7 Дней", "Сон, Стресс И Мягкая Нагрузка", "Точность, Анализы И Маршрут", "Хронологический План".
- Safety/product filter now caps generic sections, overwrites risky internal strategy fields, prevents supplement-form leakage, and marks uncertain lab values as requiring PDF/photo verification.
- Added concrete cycle/krovopoterya diary prompt for heavy menstruation.
- Verification: py_compile OK, unittest discover OK (27 tests), complex-case DeepSeek smoke OK; final judge result moved into minor-revision territory, with remaining critique mainly about premium brevity vs. medical-boundary constraints.

Decision:
- Bot can continue controlled pilot testing with mandatory human review before client PDF delivery.
- Not yet "fully autonomous medical-grade". It is a premium nutrition-navigation assistant with safety gates, expert review, and 30-day guided follow-up.

## 2026-04-24 23:24 MSK вЂ” Lab OCR Client Confirmation Gate

- Decision fixed: bot accepts client files, photos, PDFs and analyses, but OCR values are not treated as final unless the client confirms them.
- Added client confirmation message after successful OCR: bot lists recognized biomarkers and asks "да, верно" or corrections.
- Added `lab_confirmation_status`: pending_client_confirmation, client_confirmed, client_correction_needed.
- If the client confirms values, the dossier can use them as client-confirmed data.
- If the client sends corrections, old OCR values are not treated as facts; the case is marked for manual verification / resubmission.
- The "labs done" button is blocked while OCR confirmation is pending, so the client cannot accidentally finish intake before verifying numbers.
- 30-day follow-up also supports lab confirmation: if a delivered client sends new analysis files, the same verification gate applies.
- PDF logic now treats pending or corrected OCR values as uncertain, not as confirmed lab facts.
- Verification: py_compile OK, unittest discover OK (28 tests).

## 2026-04-24 23:40 MSK вЂ” Lab PDF / Manual Values Reading Upgrade

- Owner clarified: clients may send laboratory PDFs or manually type their biomarkers; bot must read both carefully and ask clarification only when unsure.
- Added embedded PDF text extraction via pypdf before Yandex OCR. Laboratory PDFs are now read as text first, avoiding unnecessary OCR failures on machine-readable lab files.
- OCR remains fallback for image/scanned files; if text/values are unclear, client confirmation/resubmission gate still applies.
- Added manual biomarker parsing for client-typed values. Short text like "Ферритин 18 нг/мл" can now be structured instead of stored only as a note.
- Manual values are marked as client-provided text; unclear text remains a note and is not forced into numeric facts.
- Verification: py_compile OK, unittest discover OK (29 tests).

## 2026-04-25 вЂ” Project Skill System / Medical Skill DB

- Created a project skill registry: docs/PROJECT_SKILL_REGISTRY_20260425.md.
- Added new reusable project skills:
  - ops/skills/medical-nutrition-navigation-skill.md
  - ops/skills/lab-file-intake-skill.md
  - ops/skills/premium-dossier-product-skill.md
  - ops/skills/critical-auditor-skill.md
  - ops/skills/commercial-growth-skill.md
  - ops/skills/post-delivery-support-skill.md
- Created machine-usable medical/nutrition skill database:
  - WellnessBot/medical_skill_database.py
  - WellnessBot/data/medical_skill_database.json
  - ops/build_medical_skill_database.py
- Current medical skill DB covers 6 markers: ferritin, vitamin D, TSH, B12, fasting glucose, HbA1c.
- Current symptom routes cover: heavy bleeding/cycle, tachycardia, GI complaints, skin/photo complaints.
- Dossier generation now receives `medical_skill_context`: marker explanations, clarify list, doctor route, safety boundaries, and priority actions.
- Added tests for medical skill DB and exported JSON generation.
- Verification: py_compile OK, unittest discover OK (32 tests).

Decision:
- All valuable project learning should become an operational artifact: code rule, test, skill, template, checklist, or registry entry. Chat-only knowledge is treated as not yet operationalized.

## 2026-04-25 вЂ” Supplement Product Catalog v1

- Owner approved adding Siberian Wellness / Vitamax product knowledge for supplement orientation.
- Created structured product catalog:
  - WellnessBot/supplement_product_catalog.py
  - WellnessBot/data/supplement_product_catalog.json
  - ops/build_supplement_product_catalog.py
- Current v1 catalog includes 8 product cards across vitamin D, magnesium/stress/sleep, omega-3, and iron-reference categories.
- Policy encoded:
  - Siberian Wellness is primary.
  - Vitamax is alternative.
  - Only active products may be candidate recommendations.
  - Discontinued/reference-only products are not recommended as available options.
  - Iron, iodine, selenium, hormones and therapeutic dosing remain outside bot prescription authority.
- Supplement context is now attached to `medical_skill_context` for dossier generation.
- Safety tests added: discontinued Siberian iron is not recommendable; vitamin D candidates prioritize Siberian Wellness; Vitamax appears as alternative.
- Verification: catalog build OK, py_compile OK, unittest discover OK (36 tests).

## 2026-04-25 13:02 MSK
### State Read Delta
- Completed a full sync read across `docs`, `WellnessBot`, `mini-app`, `landing`, and `ops/reports`.
- Current operating stage remains a controlled concierge pilot, but the tracked state is now sharper: one delivered case exists and one live case is paid-confirmed but not yet delivered.
- Landing and mini-app still align to the Telegram-first premium path; no new branch expansion signal was found in the current project state.

### Benchmark Delta
- Latest benchmark reference: `ops/reports/quality_report_20260421T183148Z.md`
- Benchmark baseline still holds at `20` prompts and `0` empty replies.
- Latest complex-case safety/value reference remains `ops/reports/complex_case_judge_report.json` with verdict `pass_with_minor_edits`.

### Regression Delta
- Premium dossier compression is still below the premium bar: the judge continues to flag repetition, weak executive summarization, and unclear doctor-route priority in `ops/reports/complex_case_judge_report.json`.
  - Owner: Product Strategist + Lead Developer
  - Next fix action: deliver the next live case, then compress the first page into an executive map, first-week action card, and grouped doctor route.
- Active pilot proof is stalled at `20260424T224714Z_<REDACTED_ID>`: payment is manually confirmed and labs are client-confirmed, but the case has no draft/PDF/delivery artifact yet.
  - Owner: Operator + Lead Developer
  - Next fix action: finish generation, review, delivery, and first follow-up capture before the next sync cycle.

### Plan Delta
- Promote `20260424T224714Z_<REDACTED_ID>` to the top execution item until it reaches delivery.
- Use the active benchmark plus complex-case judge output as the only approved input for the next dossier revision.
- Keep payment-mode drift closed: either prove `PAYMENT_TOKEN` live or keep the next `3-5` pilot cases explicitly manual by policy.

### Strategy Delta
- Strategic direction remains: Telegram-first premium nutrition-navigation with human review and 30-day follow-up.
- The main blocker is no longer intake depth or AI cost. It is pilot proof plus premium output compression.
- The next correction must come from delivered-case evidence, not from another speculative prompt-only cycle.

### Goals Delta
- Goal 1: produce one fresh delivered live case with friction notes.
- Goal 2: hold benchmark stability against `ops/reports/quality_report_20260421T183148Z.md`.
- Goal 3: convert the next dossier revision into a structure compression pass instead of further expansion.

### Connector Status
- Obsidian: local mirror refreshed
- Notion: ready for run note + context sync
- GitHub: ready for status artifact + context snapshot sync
- Google Drive: blocked because no Google Drive upload/share tool was exposed in the current Codex session
- Exact Google Drive access request: enable the Google Drive connector with file upload/create and share permissions so the run snapshot can be uploaded directly from Codex

### Next 12h Focus
- Finish `20260424T224714Z_<REDACTED_ID>` through draft, review, delivery, and first follow-up capture.
- Record operator friction and client reaction in the pulse log.
- Make one evidence-backed dossier-compression revision from the delivered case.
- Keep the payment mode explicit before the next pilot case starts.

### Context For New Model
- Stage: controlled concierge pilot with live evidence collection
- Objective: deliver the current paid-confirmed case, preserve benchmark stability, and improve premium compression only after live evidence
- Constraints: Telegram-first only; human review required; no diagnosis/treatment framing; no unconfirmed lab facts; no speculative prompt churn
- Immediate next actions:
  1. Inspect `20260424T224714Z_<REDACTED_ID>` and move it to draft/review/delivery completion.
  2. Capture operator friction and client reaction in `docs/PROJECT_PULSE_LOG.md`.
  3. Use the delivered case to redesign the first page and doctor-route structure once.

## 2026-04-25 Intake Expansion Delta
- Expanded Telegram intake from a compressed 12-step flow to a 21-step premium questionnaire based on `D:\ДОПОБУЧЕНИЕ\Эксперт БИО\анкета расширенная.docx`.
- New captured blocks: anthropometrics, work/lifestyle, energy pattern, food behavior, GI/gallbladder/bile-flow details, female hormone context, emotional stress, risk details/medications/supplements, motivation/body context.
- New fields are persisted into `profile` and `medical_context`, restored for 30-day follow-up, and included in dossier/follow-up context.
- Verification: `py_compile` OK; `unittest discover -s tests` OK, 37 tests.

## 2026-04-25 Universal Client + Nutraceutical Protocol Delta
- Product wording now explicitly supports both men and women; the hormone/reproductive intake block is neutralized for male and female contexts.
- Dossier/follow-up rules now accept additional analyses, ultrasound reports, specialist notes, and hospital discharge summaries from the last 6 months during the 30-day support window.
- Prompt rules now require individualized nutraceutical support schemes: Siberian Wellness first, Vitamax as alternative, only when safe and traceable to the client case; no medical treatment framing.
- Client-facing texts now mention 30-day Telegram support for new questions and extra documents.
- Verification: py_compile OK; unittest discover OK, 37 tests.

## 2026-04-25 Antigravity DeepSeek Auditor Delta
- DeepSeek v4 is now connected to Antigravity through MCP server `deepseek-v4` and tool `deepseek_v4_chat`.
- Technical verification: English API smoke returned `OK`; Russian UTF-8 smoke returned `ГОТОВО`; config paths are valid; API key remains outside Antigravity config.
- Created operating protocol: `docs/ANTIGRAVITY_DEEPSEEK_AUDITOR_PROTOCOL_20260425.md`.
- First raw auditor output drifted into a generic product-picker bot and is marked invalid/off-context.
- First constrained Russian run was corrupted by PowerShell encoding and is marked invalid.
- First valid constrained audit artifact: `ops/reports/antigravity_deepseek_auditor_constrained_20260425_230256.md`.
- Product decision: controlled concierge pilot may continue; public launch remains blocked; DeepSeek is advisory only and cannot replace human review.
- DeepSeek recommendation to remove all branded nutraceutical references/dosages is not adopted wholesale; project policy keeps Siberian Wellness/Vitamax as cautious, transparent, human-reviewed nutraceutical orientation.

## 2026-04-26 Intake Navigation + Premium Brevity Delta
- Added text navigation for premium intake: `назад`, `шаг назад`, `повтори вопрос`, `дальше`, `готово`, `можно дальше`, `продолжить`, `пропустить`.
- Navigation commands are no longer saved as accidental answers to questionnaire fields.
- If the client says `дальше` before answering a required step, the bot repeats the current question and asks for a short answer or `пропустить`.
- Red-flag step is protected: `РЅРµС‚` remains a valid red-flag answer, not a generic skip command.
- Premium prompt tightened: first give priorities, avoid repetition and generic free-advice wording, use timing of symptoms/meals/coffee/medications/energy as accuracy data, and structure corrections by 3 days / 2 weeks / 1-3 months.
- Verification: py_compile OK; unittest discover OK, 37 tests; bot restarted at 00:47 MSK without TelegramConflictError.

## 2026-04-26 01:03 MSK
### State Read Delta
- Completed a full sync read across `docs`, `WellnessBot`, `mini-app`, `landing`, and `ops/reports`.
- Revalidated the live execution story from `WellnessBot/data/runtime_state.json` instead of carrying forward the previous sync narrative.
- Current premium execution is split across:
  - `20260425T212847Z_<REDACTED_ID>`: freshest complete premium artifact, but review verdict is `must_rewrite_with_high_caution`
  - `20260425T214914Z_<REDACTED_ID>`: newest runtime branch, blocked at `requires_lab_resubmission=true`

### Benchmark Delta
- Latest benchmark reference remains `ops/reports/quality_report_20260421T183148Z.md`.
- Benchmark baseline still holds at `20` prompts and `0` empty replies.
- Older complex-case safety proof in `ops/reports/complex_case_judge_report.json` is still useful as a benchmark, but it is no longer the main active blocker.

### Regression Delta
- Latest dossier regression is now `20260425T212847Z_<REDACTED_ID>`.
  - Source: `WellnessBot/data/drafts/20260425T212847Z_<REDACTED_ID>.review.json`
  - Owner: Product Strategist + Lead Developer
  - Next fix action: rewrite from intake facts only, remove invented symptoms and unsupported condition claims, remove unjustified brand insertion, then rerun judge before any delivery.
- Current runtime intake is blocked by unreadable lab evidence.
  - Source: `WellnessBot/data/runtime_state.json`
  - Owner: Operator + Client
  - Next fix action: obtain a clear PDF/photo or manual typed biomarkers for `20260425T214914Z_<REDACTED_ID>`, then reopen the dossier path.
- Governance memory is accumulating duplicate proposed experiments.
  - Source: `WellnessBot/data/product_governance.json`
  - Owner: Lead Developer
  - Next fix action: deduplicate experiment seeding before the next digest so repeated ideas do not distort priorities.

### Plan Delta
- Use `20260425T212847Z_<REDACTED_ID>` as the canonical active premium case until it is rewritten, reviewed, and either delivered or explicitly archived.
- Keep `20260425T214914Z_<REDACTED_ID>` paused until readable lab evidence arrives.
- Preserve the benchmark fixed to `ops/reports/quality_report_20260421T183148Z.md` while the rewrite lands.

### Strategy Delta
- Strategic direction stays Telegram-first premium nutrition-navigation with human review.
- The immediate bottleneck is now fact integrity and case-closure discipline, not intake depth and not AI cost.
- The next meaningful proof is one fact-safe rewritten premium dossier plus one clean lab-resubmission unblock, not another uncontrolled branch.

### Goals Delta
- Goal 1: recover one fact-safe premium dossier from `20260425T212847Z_<REDACTED_ID>`.
- Goal 2: clear the lab resubmission gate for `20260425T214914Z_<REDACTED_ID>`.
- Goal 3: keep the benchmark baseline unchanged during the correction cycle.

### Next 12h Focus
- Rewrite the canonical premium case from confirmed intake facts only and rerun judge.
- Resolve the current lab-resubmission block with readable source files or manual biomarker text.
- Log operator friction after the rewrite and resubmission paths are clear.
- Keep manual concierge and human review as the active pilot policy.

## 2026-04-26 13:05 MSK
### State Read Delta
- Completed a full sync read across `docs`, `WellnessBot`, `mini-app`, `landing`, and `ops/reports`, plus the newest runtime, review, and governance artifacts.
- Live runtime still points to `20260425T214914Z_<REDACTED_ID>` at the `labs` step with `requires_lab_resubmission=true`.
- Canonical premium artifact remains `20260425T212847Z_<REDACTED_ID>`; draft, PDF, judge, and growth outputs exist, but the review verdict is still `must_rewrite_with_high_caution`.
- Landing and mini-app still align to the Telegram-first premium funnel. No new branch-expansion change was found in the current web surfaces.

### Benchmark Delta
- Latest benchmark reference remains `ops/reports/quality_report_20260421T183148Z.md`.
- Benchmark baseline still holds at `20` prompts and `0` empty replies.
- The live premium rewrite brief now comes from `WellnessBot/data/drafts/20260425T212847Z_<REDACTED_ID>.review.json`; `ops/reports/complex_case_judge_report.json` remains supporting structure evidence, not the main active blocker.

### Regression Delta
- Canonical premium dossier `20260425T212847Z_<REDACTED_ID>` is still not delivery-safe.
  - Source: `WellnessBot/data/drafts/20260425T212847Z_<REDACTED_ID>.review.json`
  - Owner: Product Strategist + Lead Developer
  - Next fix action: rewrite from confirmed intake facts only, remove invented symptoms and unsupported condition framing, remove unjustified brand insertion, then rerun judge before any delivery.
- Live runtime branch `20260425T214914Z_<REDACTED_ID>` is still blocked on unreadable lab evidence.
  - Source: `WellnessBot/data/runtime_state.json`
  - Owner: Operator + Client
  - Next fix action: obtain a readable PDF/photo or manual typed biomarkers, then rerun the lab confirmation path.
- Governance memory is still duplicating proposed experiments.
  - Source: `WellnessBot/data/product_governance.json`
  - Owner: Lead Developer
  - Next fix action: deduplicate repeated experiment seeding before the next digest so governance reflects live evidence instead of repeated AI drift.

### Plan Delta
- Keep `20260425T212847Z_<REDACTED_ID>` as the only canonical active premium case for user `<REDACTED_ID>` until rewrite, review, delivery, or explicit archive.
- Keep `20260425T214914Z_<REDACTED_ID>` paused until lab evidence is readable and confirmed.
- Hold the benchmark anchor fixed to `ops/reports/quality_report_20260421T183148Z.md` while the correction cycle lands.
- Defer new landing or mini-app growth work until case closure and governance dedupe stop outrunning live evidence.

### Strategy Delta
- Strategy remains Telegram-first premium nutrition-navigation with human review, manual concierge payment, and 30-day follow-up in the same thread.
- The active bottleneck is no longer intake depth or asset generation. It is case-closure discipline plus fact integrity inside the premium dossier.
- The highest-value proof for the next cycle is one fact-safe delivered dossier and one clean lab-resubmission recovery, not more branching or more experiment generation.

### Goals Delta
- Goal 1: close `20260425T212847Z_<REDACTED_ID>` into a fact-safe, human-reviewed deliverable.
- Goal 2: unblock `20260425T214914Z_<REDACTED_ID>` with readable and confirmed lab data.
- Goal 3: deduplicate governance experiment memory before the next digest.
- Goal 4: preserve the benchmark baseline unchanged while corrections land.

### Connector Status
- Obsidian: done - refreshed `docs/obsidian_mirror/AGENT_CONTEXT_HUB.md` and added a new run note mirror.
- Notion: done - run note created with a concise `Context For New Model` section.
- GitHub: done - status artifact and context snapshot synced for external contributors.
- Google Drive: blocked - no Google Drive upload/share tool is exposed in the current Codex session.
- Exact Google Drive access request: enable the Google Drive connector with file upload/create and share permissions so the run snapshot can be uploaded directly from Codex.

### Next 12h Focus
- Rewrite `20260425T212847Z_<REDACTED_ID>` strictly from confirmed intake facts and rerun judge.
- Request readable PDF/photo or manual typed biomarkers for `20260425T214914Z_<REDACTED_ID>`.
- Deduplicate governance proposals before the next digest.
- Log operator friction and delivery outcome once the canonical case is either delivered or archived.

### Context For New Model
- Stage: controlled concierge pilot with canonical-case freeze and lab-resubmission pressure
- Objective: close `20260425T212847Z_<REDACTED_ID>` safely, unblock `20260425T214914Z_<REDACTED_ID>`, and stop governance duplication from outrunning live proof
- Constraints: Telegram-first only; human review required; manual concierge remains official pilot mode; one active premium case per user; no diagnosis/treatment framing; no unreadable or unconfirmed lab facts; no invented symptoms; no new growth/UI branches until the canonical case closes
- Immediate next actions:
  1. Rewrite `20260425T212847Z_<REDACTED_ID>` from confirmed intake facts only and rerun judge.
  2. Obtain readable lab evidence or manual biomarker text for `20260425T214914Z_<REDACTED_ID>`.
  3. Deduplicate repeated governance proposals and log the result in `docs/PROJECT_PULSE_LOG.md`.

## 2026-04-26 Antigravity Multi-Model Handoff TZ
- Created `docs/ANTIGRAVITY_MULTI_MODEL_HANDOFF_TZ_20260426.md` as the full handoff/specification for connecting additional models to Antigravity via MCP.
- Created `docs/ANTIGRAVITY_MULTI_MODEL_COPYPASTE_PROMPT_20260426.md` as the short prompt Olga can paste directly into Antigravity or send to another executor.
- Scope is intentionally constrained: new models are auditors/helpers only; DeepSeek v4 must remain working; no secrets in `mcp.json`; all user-facing output must remain Russian; human review remains mandatory.

## 2026-04-26 Product Line V2
- Accepted the new product architecture: demo-result preview + 3 paid packages.
- Paid products now represented in bot code and payment context:
  - `week`: Разбор на 7 дней, 3 900 ₽
  - `premium`: Персональный разбор на 30 дней, 6 900 ₽
  - `vip`: VIP-сопровождение на 30 дней, 14 900 ₽
- Start menu now routes into product selection, result examples, process explanation, and operator contact.
- Payment context now stores selected product code, name, title, description, and amount; legacy premium price remains compatible.
- Created `docs/PRODUCT_LINE_V2_20260426.md` and marked the old one-off price policy as superseded for multi-product use.
- Verification: py_compile OK; unittest discover OK, 38 tests; bot restarted.

## 2026-04-26 Manual Payment Mode
- Accepted manual payment as the active pilot mode because YooKassa / Telegram payment activation can reject or block the flow.
- Added `PAYMENT_MODE` setting with allowed values `manual` and `telegram`; default is `manual`.
- Set `WellnessBot/.env` to `PAYMENT_MODE=manual` without exposing secrets.
- `finalize_submission` now sends Telegram invoices only when `PAYMENT_MODE=telegram` and a `PAYMENT_TOKEN` exists; otherwise it uses manual payment handoff.
- Client copy now explains that online Telegram payment is temporarily disabled and the team will confirm payment in Telegram.
- Created `docs/MANUAL_PAYMENT_MODE_20260426.md`; updated payment and product-line docs.
- Verification: py_compile OK; unittest discover OK, 38 tests; bot restarted successfully in manual payment mode.

## 2026-04-27 North Star Execution Plan
- Created `docs/PROJECT_NORTH_STAR_EXECUTION_PLAN_20260427.md` as the controlling plan for ending open-ended development drift.
- Fixed the near-term target: one safe paid client cycle from Telegram entry to manual payment, AI draft, human review, client result, and follow-up.
- Defined the done state, accepted decisions, phased timeline, public-launch gates, and the rule that new large ideas move to backlog unless they support the next complete client cycle.
- Updated `docs/AGENT_CONTEXT_HUB.md` with the North Star link and current product architecture: demo + week + premium + VIP.

## 2026-04-27 01:08 MSK
### State Read Delta
- Completed a full sync read across `docs`, `WellnessBot`, `mini-app`, `landing`, and `ops/reports`, plus the newest persisted submissions, review artifacts, governance memory, and prior external sync notes.
- `WellnessBot/data/runtime_state.json` is empty at sync time, so no in-memory session is authoritative for current execution.
- Corrected the previous carry-forward narrative: the freshest persisted premium branch is `20260425T214914Z_<REDACTED_ID>` by `status_updated_at=2026-04-26T21:25:18Z`, not the older `20260425T212847Z_<REDACTED_ID>`-only story.
- `20260425T214914Z_<REDACTED_ID>` already has manual payment confirmation, uploaded documents, draft/PDF/judge/growth artifacts, but its lab gate still says `needs_resubmission`.
- `20260425T212847Z_<REDACTED_ID>` remains unresolved with review verdict `must_rewrite_with_high_caution`, so the intended one-active-branch rule is currently violated in persisted data.
- Landing and mini-app still align to the Telegram-first premium funnel; no new branch-expansion move is visible in the current web surfaces.

### Benchmark Delta
- Latest benchmark reference remains `ops/reports/quality_report_20260421T183148Z.md`.
- Benchmark baseline still holds at `20` prompts and `0` empty replies.
- Supporting premium-structure risk reference in `ops/reports/complex_case_judge_report.json` currently reads `verdict=fail` and should no longer be carried forward as a pass-style reassurance.

### Regression Delta
- Unsafe lab-gate bypass in the freshest premium branch:
  - source: `WellnessBot/data/submissions/20260425T214914Z_<REDACTED_ID>.json`
  - owner: Lead Developer
  - next fix action: block draft/PDF generation and delivery while `lab_quality_check.requires_resubmission=true`, or explicitly invalidate the current artifacts until readable labs or manual biomarkers arrive.
- Multi-branch drift for the same Telegram user:
  - source: `WellnessBot/data/submissions/20260425T214914Z_<REDACTED_ID>.json` and `WellnessBot/data/submissions/20260425T212847Z_<REDACTED_ID>.json`
  - owner: Operator + Lead Developer
  - next fix action: declare one active branch by persisted freshness and archive or merge the other in docs, state, and operator workflow.
- Freshest premium dossier is not delivery-safe:
  - source: `WellnessBot/data/drafts/20260425T214914Z_<REDACTED_ID>.review.json`
  - owner: Product Strategist + Lead Developer
  - next fix action: regenerate from confirmed intake facts and readable evidence only, then rerun judge before any delivery decision.
- Governance duplication remains an execution regression:
  - source: `WellnessBot/data/product_governance.json`
  - owner: Lead Developer
  - next fix action: deduplicate repeated proposals before the next digest; current memory stores `115` experiments with `4` repeated titles still duplicated `2-6` times.

### Plan Delta
- Stop carrying forward a `20260425T212847Z_<REDACTED_ID>`-only canonical story when runtime memory is empty.
- Use the freshest persisted branch `20260425T214914Z_<REDACTED_ID>` as the operational truth for triage, but treat its current draft/PDF as unsafe working artifacts until the lab gate is resolved.
- Freeze any new premium starts for Telegram user `<REDACTED_ID>` until one of the two open premium branches is explicitly archived or merged.
- Keep the benchmark anchor fixed to `ops/reports/quality_report_20260421T183148Z.md` while branch reconciliation and lab-gate correction land.

### Strategy Delta
- Strategic direction remains Telegram-first premium nutrition-navigation with manual concierge payment and mandatory human review.
- Execution priority changed: the main blocker is no longer just dossier rewriting. It is branch-truth reconciliation plus evidence discipline after an unsafe lab-gate bypass.
- Pilot proof now requires one branch that is both fact-safe and operationally clean. A generated PDF is not proof if it was produced after unreadable-lab resubmission was already required.

### Goals Delta
- Goal 1: restore one active premium branch for user `<REDACTED_ID>`.
- Goal 2: stop `requires_lab_resubmission=true` from progressing to delivery artifacts.
- Goal 3: close one fact-safe, human-reviewed premium dossier from confirmed evidence only.
- Goal 4: deduplicate governance memory without disturbing the stable dialogue benchmark.

### Connector Status
- Obsidian: done - refreshed `docs/obsidian_mirror/AGENT_CONTEXT_HUB.md` and added a new run note mirror.
- Notion: pending in local log until run-note creation completes in the external workspace.
- GitHub: pending in local log until the new status artifact and context snapshot are written to the external repository.
- Google Drive: blocked - no Google Drive upload/share tool is exposed in the current Codex session.
- Exact Google Drive access request: enable the Google Drive connector with file upload/create and share permissions so the run snapshot can be uploaded directly from Codex.

### Next 12h Focus
- Reconcile `20260425T214914Z_<REDACTED_ID>` and `20260425T212847Z_<REDACTED_ID>` to one active premium branch.
- Obtain readable labs or manual biomarker text for `20260425T214914Z_<REDACTED_ID>`, then regenerate and rerun judge from confirmed facts only.
- Add or enforce a hard lab-gate block before draft/PDF generation.
- Deduplicate governance proposals before the next digest.

### Context For New Model
- Stage: controlled concierge pilot with branch reconciliation pressure and unsafe-lab gate correction
- Objective: restore one active premium branch, stop unsafe dossier progression from unreadable labs, and close one fact-safe human-reviewed client cycle
- Constraints: Telegram-first only; human review required; manual concierge remains official pilot mode; one active premium branch per Telegram user; no diagnosis/treatment framing; no unreadable or unconfirmed lab facts; no invented symptoms; no new growth/UI branches until branch truth and lab gating are fixed
- Immediate next actions:
  1. Use `status_updated_at` to declare `20260425T214914Z_<REDACTED_ID>` or `20260425T212847Z_<REDACTED_ID>` the single active branch, then archive or merge the other.
  2. Do not deliver the current `20260425T214914Z_<REDACTED_ID>` PDF; first obtain readable labs or manual biomarkers and regenerate from confirmed facts only.
  3. Add or verify a hard lab-gate block before draft/PDF generation, then deduplicate governance memory and log the correction outcome.

## 2026-04-27 12:20 MSK — Регулярная синхронизация (github-notion-12)

### Итог
- Обновлён `docs/AGENT_CONTEXT_HUB.md`: добавлен краткий RU-статус (этап/блокеры/риски/что нельзя публично).
- Notion: создана страница статуса прогона — `Antigravity Sync Run - 2026-04-27 12:20 MSK`: https://www.notion.so/34f8a9de1d41816b82fbd1174dab9712
- GitHub: remote не настроен (в репозитории `git remote -v` пусто), поэтому push не выполнен; отчёт: `docs/external_sync/github_20260427_1220_msk.md`.

### Текущий этап
- Controlled concierge pilot. Публичный запуск заблокирован до отдельного решения.

### Блокеры и риски
- Две активные ветки по одному пользователю → риск «двух правд» и неправильной выдачи.
- Lab-gate: недопустима генерация/выдача при `requires_lab_resubmission=true`.
- Human review обязателен перед любой выдачей клиенту.

### Следующие шаги (12 часов)
1. Зафиксировать одну активную ветку на пользователя; остальные архивировать/слить.
2. Проверить/ввести жёсткий lab-gate блок на генерацию артефактов.
3. Получить читаемые анализы/ручной ввод биомаркеров, перегенерировать из подтверждённых фактов и прогнать judge + human review.

## 2026-04-28 12:16 MSK — Регулярная синхронизация (github-notion-12)

### Итог

- Прочитан актуальный контекст по проекту (опорные документы в `docs/`).
- Обновлён `docs/AGENT_CONTEXT_HUB.md`: добавлен RU-снимок статуса (этап/блокеры/риски/что готово к пилоту/что нельзя публично).
- Git hygiene: `bot.stderr.log` исключён из контроля версий (через `.gitignore` + снятие с индекса).
- Safety-check: `python -m compileall WellnessBot` проходит; destructive-команды не использовались.

### Репозиторий / изменения (кратко)

- Крупное расширение `WellnessBot/` (governance/кейсы/платёжный флоу/генераторы артефактов), усиление `ops/` и `infra/deploy/`.
- Обновлены витрины `landing/` и `mini-app/` (важно: это не сигнал готовности к public launch).
- В `docs/` добавлен большой слой операционных документов/протоколов/чеклистов.

### Блокеры / риски

1. Одна активная ветка на пользователя `<REDACTED_ID>` (иначе риск «двух правд»).
2. Lab-gate: нельзя выдавать/считать готовыми артефакты при `requires_lab_resubmission=true`.
3. GitHub push заблокирован: `git remote -v` пусто (remote не настроен).
4. Диск `C:` ниже `10 GB` свободного места — риск деградации среды.

### Connector status

- Notion: выполнить обновление страницы статуса прогона (создать/обновить страницу с executive summary без секретов).
- GitHub: blocked (remote не настроен) — отчёт добавлен в `docs/external_sync/`.

## 2026-04-29 21:16 MSK — Регулярная синхронизация (github-notion-12)

### Итог

- Перепроверен актуальный контекст и опорные документы (стратегия, продуктовая линейка, ручная оплата, протокол аудитора, реестр навыков).
- Зафиксирован ключевой вывод по качеству диалогов: бенч 20/20 без пустых ответов, но `0/20` запросов доходит до модели из‑за избыточного роутера (см. `docs/WELLNESS_DIALOGUE_QA_20260429.md`).
- Мелкий, но критичный runtime‑фикс: разбиение админ‑дайджеста на чанки перед отправкой в Telegram, чтобы не падать на лимитах длины (`WellnessBot/main.py`).

### Текущий этап

- Controlled concierge pilot; public launch заблокирован до отдельного решения.
- Активный пилотный режим оплаты: `PAYMENT_MODE=manual`.
- Human review обязателен перед любой клиентской выдачей.

### Блокеры / риски

1. Runtime‑to‑storage mismatch: живой `week` runtime указывает на `week_runtime_20260427T173913Z`, но соответствующий submission JSON отсутствует.
2. Same‑user drift: один и тот же пользователь держит `week` runtime + 2 ветки `premium`; нужна одна активная платная траектория.
3. Disk hygiene: `C:` ниже целевого порога `10 GB` свободного места.

### Следующие шаги (12 часов)

1. Починить/сбросить `week_runtime_20260427T173913Z`, чтобы runtime и storage совпали.
2. Зафиксировать одну активную ветку (week или premium) для текущего пользователя, остальные — заморозить/архивировать.
3. Сузить роутер: оставить детерминизм только для emergency/crisis/узких FAQ, всё остальное — отдавать модели с проверкой на «не выдумывать факты».

## 2026-05-01 — Регулярная синхронизация (github-notion-12)

### Итог
- Зафиксирован аудит внешнего проекта Google AI Studio `moy-projekt`: это UI/UX‑макет (React/Vite), **не** замена backend‑бота. Док: `docs/GOOGLE_AI_STUDIO_MOY_PROJEKT_AUDIT_20260501.md`.
- В боте усилен «пример результата»: `PRODUCT_EXAMPLES_TEXT` теперь отдаёт конкретный безопасный демо‑фрагмент со структурой результата (без диагнозов/лечения) — `WellnessBot/texts.py`.
- Добавлены защитные исключения в `.gitignore`, чтобы не коммитить внешние клоны и локальные артефакты синхронизации (`external/`, `docs/external_sync/`, `docs/obsidian_mirror/RUN_NOTE_*.md`).
- Санитизация: из статусных документов удалены длинные идентификаторы (Telegram ID и связанные артефакт‑ID), чтобы не публиковать персональные данные в GitHub.

## 2026-05-01 09:17 MSK — Регулярная синхронизация (github-notion-12)

### State Read Delta
- Completed a full sync read across `docs`, `WellnessBot`, `mini-app`, `landing`, and `ops/reports`.
- `WellnessBot/data/runtime_state.json` still holds `week_runtime_20260427T173913Z_<REDACTED_ID>` at `consent`, and there is still no matching persisted submission JSON.
- The same Telegram user still spans one unresolved runtime-only `week` path plus two unresolved `premium` branches.
- `premium_fresh_20260425T214914Z` still has `requires_lab_resubmission=true` and remains unsafe for delivery even though draft/PDF artifacts already exist.
- `premium_legacy_20260425T212847Z` still has review verdict `must_rewrite_with_high_caution` and remains the only realistic premium rewrite candidate if proof closure is attempted.
- `landing/index.html` and `mini-app/index.html` still align to the Telegram-first premium funnel; no new execution-critical surface shift was found.
- The external repo audit in `docs/GOOGLE_AI_STUDIO_MOY_PROJEKT_AUDIT_20260501.md` confirmed `moy-projekt` is a UI mockup only, not a backend replacement plan.
- `WellnessBot/texts.py` now returns a concrete safe demo-result fragment in `PRODUCT_EXAMPLES_TEXT`.
- Runtime is up with a clean start logged at `2026-05-01 00:45:55 MSK`.

### Benchmark Delta
- Latest benchmark reference remains `ops/reports/quality_report_20260429T080345Z.md`.
- Current benchmark truth remains unchanged:
  - `20/20` replies were non-empty
  - `20/20` prompts were intercepted by `route_live_reply()`
  - `0/20` prompts reached the model
  - clarifying-question count remains `0/20`

### Regression Delta
- Disk headroom has become a critical ops regression.
  - source: live disk check on `C:` during this sync
  - owner: Ops
  - next fix action: clear large delete candidates from `docs/DISK_HYGIENE_STATUS.md` and restore free space above `10 GB` before more PDF or batch-artifact work
- Runtime-to-storage mismatch remains unresolved.
  - source: `WellnessBot/data/runtime_state.json`
  - owner: Lead Developer
  - next fix action: persist `week_runtime_20260427T173913Z_<REDACTED_ID>` before or at `consent`, or explicitly invalidate and restart it cleanly
- Same-user multi-path drift remains unresolved.
  - source: `WellnessBot/data/runtime_state.json` plus `WellnessBot/data/submissions/20260425T212847Z_<REDACTED_ID>.json` and `WellnessBot/data/submissions/20260425T214914Z_<REDACTED_ID>.json`
  - owner: Operator + Lead Developer
  - next fix action: declare exactly one active paid path across `week` and `premium`, then freeze, archive, or merge the rest
- Unsafe lab-gate bypass remains active in the freshest premium branch.
  - source: `WellnessBot/data/submissions/20260425T214914Z_<REDACTED_ID>.json`
  - owner: Lead Developer
  - next fix action: keep the current artifacts delivery-frozen and hard-block draft/PDF generation while `requires_lab_resubmission=true`
- Router overreach remains the dominant live-chat quality regression.
  - source: `ops/reports/quality_report_20260429T080345Z.md`
  - owner: Lead Developer + Product Strategist
  - next fix action: cut deterministic routing back to emergency, crisis, upload guidance, and a narrow logistics FAQ set; then rerun the benchmark
- Governance duplication remains active.
  - source: `WellnessBot/data/product_governance.json`
  - owner: Lead Developer
  - next fix action: deduplicate the `115` experiment list and remove the `4` repeated title groups before the next digest

### Plan Delta
- Disk recovery is now an immediate blocker and moves ahead of nonessential artifact generation or sync churn.
- Keep `premium_fresh_20260425T214914Z` frozen for delivery until readable labs or manual biomarker text clear the gate.
- Persist or clear `week_runtime_20260427T173913Z_<REDACTED_ID>` before carrying the current paid-path story forward again.
- Reduce the same-user stack to one active paid path before any delivery or growth claim.
- Use GitHub connector artifacts as the official external-contributor snapshot even when local `git remote -v` is empty.

### Strategy Delta
- Strategic direction remains Telegram-first wellness intake with manual concierge payment, human review, and premium dossier delivery in the same operating thread.
- New evidence changes execution order:
  - environment reliability is now as urgent as state coherence because `C:` free space is only `2.69 GB`
  - Google AI Studio stays a UI reference only and must not divert backend execution
  - the safe demo-result text helps trust, but it is not product proof
- The next proof target is now:
  - one stable environment
  - one coherent paid path
  - one benchmark rerun where symptom prompts actually reach the model

### Goals Delta
- Goal 1: restore `C:` above the `10 GB` safety floor.
- Goal 2: resolve the runtime-versus-storage mismatch and choose one active paid path.
- Goal 3: narrow router scope and rerun the benchmark from a real model-reaching baseline.
- Goal 4: keep the freshest premium branch frozen until readable labs or manual biomarker text clear the gate.

### Connector Status
- Obsidian: done - refreshed `docs/obsidian_mirror/AGENT_CONTEXT_HUB.md` and created a new run-note mirror.
- Notion: done - created a new run note with a concise `Context For New Model` block.
- GitHub: done - synced a sanitized status artifact and context snapshot for external contributors via the GitHub connector.
- Google Drive: blocked - no Google Drive file upload/create or share tools are exposed in the current Codex session.
- Exact Google Drive access request: enable the Google Drive connector with file upload/create and share permissions so the run snapshot can be uploaded directly from Codex.

### Next 12h Focus
1. Free enough disk space to restore `C:` above `10 GB`.
2. Persist or clear `week_runtime_20260427T173913Z_<REDACTED_ID>`.
3. Declare one active paid path across the same-user `week` and `premium` stack.
4. Cut `route_live_reply()` back to safety/logistics coverage, add clarifying-question behavior, and rerun the benchmark.
5. Keep `premium_fresh_20260425T214914Z` frozen until readable labs or manual biomarker text arrive.

### Context For New Model
- Stage: controlled concierge pilot with same-user state drift, router-overreach quality blockage, lab-gate enforcement pressure, and critical disk headroom risk
- Objective: restore one coherent paid-path truth, stop unsafe premium delivery from unreadable labs, reduce deterministic router capture, and stabilize the environment enough to keep the pilot reliable
- Constraints: Telegram-first only; one active paid path per Telegram user; manual concierge remains official pilot mode; human review required before delivery; no diagnosis/treatment framing; no unreadable or unconfirmed lab facts; no invented symptoms or unsupported condition claims; no new growth or UI work until disk headroom, state truth, router scope, and lab gating are fixed
- Immediate next actions:
  1. Free disk space back above the `10 GB` floor before more PDF or batch-artifact work.
  2. Persist or clear `week_runtime_20260427T173913Z_<REDACTED_ID>` so runtime and storage stop disagreeing.
  3. Declare exactly one active paid path for the same-user case, then freeze, archive, or merge the others.
  4. Cut `route_live_reply()` back to safety/logistics coverage and rerun the benchmark so symptom prompts can actually test model quality.
  5. Keep the current premium PDF frozen until readable labs or manual biomarker text exist and the dossier is regenerated from confirmed facts only.

## 2026-05-01 — GitHub single source of truth

### Delivery Delta
- Создан единый безопасный центр разработки для GitHub: `docs/PROJECT_DEVELOPMENT_SINGLE_SOURCE_OF_TRUTH.md`.
- В документ сведены: цель проекта, продуктовая линейка, текущий этап, архитектура, безопасность, ручная оплата, AI/Antigravity, хранение данных, блокеры, pilot-ready/public-launch критерии и ссылки на опорные документы.
- `docs/AGENT_CONTEXT_HUB.md` обновлён ссылкой на единый source of truth.

### Safety Delta
- В GitHub не переносятся секреты, `.env`, токены, клиентские анализы/PDF/фото, `WellnessBot/data`, runtime-данные и персональные идентификаторы.
- Документ предназначен для передачи разработчикам/аудиторам без раскрытия чувствительных данных.

## 2026-05-01 — Disk blocker cleared

### Ops Delta
- Restored C: free space above the project safety floor: now approximately $freeGb GB free.
- Removed only two old incomplete .crdownload files from Downloads, total recovery approximately 24.47 GB.

### Safety Delta
- No project code, secrets, .env, client files, analysis uploads, PDF/photo data, or WellnessBot/data were deleted.
- Disk pressure is no longer the immediate blocker for PDF/batch-artifact work.

## 2026-05-01 — Runtime/storage mismatch fix

### Delivery Delta
- Fixed the root cause of orphan intake sessions: `start_session()` now persists an initial submission immediately with `intake_status=consent_pending`.
- Added `build_initial_submission_payload()` in `WellnessBot/case_service.py`.
- Added a unit test for the initial consent-pending submission state.
- Repaired the existing local runtime-only `week` session by creating its missing local submission JSON.

### Validation Delta
- `python -m unittest discover -s tests` passed: `39` tests OK.

### Safety Delta
- The repaired local submission remains inside ignored `WellnessBot/data` and was not staged for GitHub.
- No client files, uploads, lab PDFs/photos, tokens, or `.env` files were published.

## 2026-05-01 — Live router narrowed and benchmark rerun

### Delivery Delta
- Narrowed `route_live_reply()` so symptom/lab questions now reach the model instead of being fully answered by deterministic templates.
- Kept deterministic routing for emergency/crisis, file upload logistics, no-labs start guidance, urgency separation, and product/service FAQ.
- Added `tests/test_live_reply_routing.py` to protect this behavior.
- Strengthened `LIVE_CHAT_PROMPT` so first-line live chat must not issue personal supplement schemes, exact supplement doses, or medication-like instructions.

### Validation Delta
- Unit tests passed: `42` tests OK.
- New benchmark report: `ops/reports/quality_report_20260501T073446Z.md`.
- Benchmark facts:
  - total prompts: `20`
  - empty replies: `0`
  - routed by deterministic template: `11/20`
  - reached model layer: `9/20`
  - symptom/lab prompts reaching model: `1,2,3,4,5,6,7,8,16`
- Safety scan did not find the explicit high-risk phrases checked in the report: `лечебная доза`, `начинайте приём`, `вам нужно принимать`, `выраженный дефицит`, `назнач`.

### Remaining Quality Risk
- Model-led answers are more personalized, but still sometimes sound too medically confident around functional thyroid/GI interpretations.
- Next hardening: add a stricter live-answer critic/sanitizer or prompt rule for avoiding overly confident functional-medicine claims in short first-line chat.

## 2026-05-01 — Live answer sanitizer added

### Delivery Delta
- Added `sanitize_live_reply()` as a post-model safety guard for first-line live chat answers.
- The sanitizer softens prescription-like and diagnosis-like wording before CTA is appended.
- Covered sanitizer behavior with tests in `tests/test_live_reply_routing.py`.

### Validation Delta
- Unit tests passed: `44` tests OK.

### Safety Delta
- Guarded phrases include examples like `лечебная доза`, `выраженный дефицит`, `вам нужно принимать`, `начните/начинайте приём`, and direct diagnosis-like `у вас гипотиреоз` patterns.
