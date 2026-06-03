# Engineering Mandate

Date: 2026-06-03
Issued by: Chief Orchestrator
Status: June 3 refresh; runtime baseline is unchanged from June 2 direct fallback, but the lead engineering failure is now continuity-chat safety plus commercialization control, while disk headroom is down to `6.59 GB`

## Mission

Run one coherent Telegram paid cycle through:

`approved offer choice -> manual concierge payment -> intake -> AI draft -> human review -> safe delivery -> same-thread follow-up`

No new tariff, catalog branch, or upgrade path counts as live truth until one approved offer map and one replayable proof artifact exist. Public launch remains blocked.

## 2026-06-03 11:45 Correction Set

Use this correction set wherever it conflicts with older June or May assumptions.

- Treat runtime as stable enough to stop debating, but not freshly re-proven today:
  - no newer runtime artifact exists after `2026-06-02 21:16:49 +03:00`
  - the standing baseline is still proxy failure followed by direct fallback and clean polling start
  - do not spend another engineering cycle on proxy narration without a newer artifact
- Treat QA observability as the lead tooling failure:
  - `tests/test_live_reply_routing.py` passed on June 3
  - `ops/quality_probe.py --mode smoke` passed on June 3
  - full batch still aborts on prompt `1` with `openai.APIConnectionError` / `[WinError 10061]`
  - the missing engineering capability is prompt-level partial artifact capture on model-path failure
- Treat the active paid `nutri_chat` thread as the strongest current product proof and the strongest current safety risk:
  - `runtime_state.json` still holds `20260602T055745Z_1084557944`
  - the thread shows real paid continuity after payment
  - the same thread also overreaches with long mechanism-heavy interpretation and `30 days` continuity framing that is too wide for the current low-ticket rail
- Treat continuity governance as still materially broken:
  - only `20260501`, `20260505`, and `20260514` currently carry canonical classification
  - `20260530T183208Z_1084557944`, `20260530T205040Z_1084557944`, `20260531T183007Z_1084557944`, `20260601T204906Z_1084557944`, and `20260602T055745Z_1084557944` still have no `canonical_path`
  - `20260531T183007Z_1084557944` remains the hard breach because `14900 RUB`, `delivered_to_client`, and `fail_major_issues` coexist
- Treat the live ladder as narrower than the repo diff implies:
  - `nutri_chat` is the only currently proven active paid rail
  - `standard` is only a reviewed escalation candidate
  - `premium` must stay parked until delivery-gate truth, canonical-path control, and QA visibility are current
- Treat experiment churn as explicit duplicate-loop evidence:
  - `151` experiments still exist
  - `0` decisions exist
  - the top experiment titles repeat `12`, `11`, `8`, `8`, and `5` times
  - `29` `HERMES-20260505-*` packets still remain open
- Treat disk headroom as worse than the June 2 night mandate:
  - actual `C:` free space is `6.59 GB` at `2026-06-03 11:38:49 +03:00`
- The next engineering packet is now:
  1. make `ops/quality_probe.py` emit partial per-prompt artifacts on connection failure
  2. tighten the live-chat contract in prompt + sanitizer rules
  3. QA-audit the active `nutri_chat` thread against that contract
  4. hard-block new same-user paid branch creation while conflicts exist
  5. repair the `20260531T183007Z_1084557944` delivery-gate breach
  6. classify the `20260530` to `20260602` branches into one canonical ladder
  7. keep `nutri_chat` as the only active paid rail while `standard` and `premium` remain review-gated
  8. restore disk above `10 GB`
  9. freeze experiment churn until one fresh reviewed proof artifact lands

## 2026-06-02 23:41 Correction Set

Use this correction set wherever it conflicts with older June or May assumptions.

- Treat the June 2 runtime artifact as repeated positive proof, not single-pass proof:
  - `2026-06-02 21:16:48-21:16:49 +03:00` shows another startup with proxy failure followed by direct fallback and polling start
  - direct-fallback polling is therefore current twice in the same local day
- Treat the active paid `nutri_chat` thread as the strongest current product artifact:
  - `runtime_state.json` still holds `20260602T055745Z_1084557944`
  - runtime memory shows real paid continuity-chat behavior after payment, not only an unopened shell
  - the product is currently proving fast Telegram continuity better than it is proving dossier delivery
- Treat continuity governance as the lead engineering failure:
  - recent paid stack still contains `6900`, `14000`, `14900`, and `500 RUB` branches for the same user
  - none of the five recent paid cases has `canonical_path` metadata
  - `20260531T183007Z_1084557944` is still the hard breach because `delivered_to_client` coexists with `fail_major_issues`
- Treat the likely active ladder for the next execution packet as narrower than the repo currently implies:
  - current evidence supports `nutri_chat` as the only clearly proven paid entry rail
  - `standard` may remain the only reviewed escalation candidate
  - do not keep selling or narrating `premium` as active proof while delivery-gate, canonical-path, and QA control remain unresolved
- Treat live chat safety as a first-class engineering surface:
  - the active paid chat already uses mechanism-heavy interpretation and `30 days` continuity framing
  - this means QA must inspect actual continuity-chat behavior, not only dossier output
- Treat disk headroom as worse than the morning mandate:
  - actual `C:` free space is `6.62 GB` at `2026-06-02 23:39:07 +03:00`
- Treat governance churn as unchanged loop evidence:
  - `151` experiments still exist
  - `29` `HERMES-20260505-*` packets still remain open
- The next engineering packet is now:
  1. keep the June 2 direct-fallback runtime mode explicit
  2. hard-block new same-user paid branch creation while conflicts exist
  3. QA-audit the active `nutri_chat` thread for safety and upsell boundaries
  4. repair the `20260531T183007Z_1084557944` delivery-gate breach
  5. classify the `20260530` to `20260602` branches into one canonical ladder
  6. decide whether `nutri_chat -> standard` is the only active ladder for now, with `premium` parked
  7. normalize that decision across code, docs, prompts, and mini-app
  8. restore disk above `10 GB`
  9. freeze experiment churn until one fresh reviewed proof artifact lands

## 2026-06-02 Correction Set

Use this correction set wherever it conflicts with older May assumptions.

- Treat the June 2 runtime artifact as the current positive proof:
  - `2026-06-02 00:13:24 +03:00` logs proxy failure followed by direct fallback
  - polling starts cleanly at `00:13:24-00:13:25 +03:00`
  - DeepSeek requests succeed through `10:23:51 +03:00`
  - handled updates continue through `10:24:09 +03:00`
- Treat proxy `127.0.0.1:10808` as unproven optional infrastructure, not as assumed required infrastructure:
  - the freshest working runtime path is direct fallback, not confirmed proxy dependency
- Treat commercialization control as the lead engineering failure:
  - `20260531T183007Z_1084557944` reached `delivered_to_client` while `internal_review.judge_verdict = fail_major_issues`
  - `20260601T204906Z_1084557944` is newly paid at `14000 RUB` with `judge_verdict = needs_revision`
  - `20260602T055745Z_1084557944` is newly paid at `500 RUB` and active in `runtime_state.json`
  - this means the same user can still accumulate new paid branches faster than review and canonical control can close them
- Treat the live ladder as an inference that still needs explicit approval:
  - current `payment_flow.py` and menu behavior imply `nutri_chat -> standard -> premium` at `500 / 14000 / 14900 RUB`
  - older `week`, `basic`, `full`, and `vip` names now behave like conflicting legacy aliases
  - do not describe any one ladder as approved until code, docs, prompts, and artifacts converge
- Treat disk headroom as worse than the June 1 mandate:
  - actual `C:` free space is `7.32 GB` at `2026-06-02 11:37:32 +03:00`
- Treat product-governance churn as worsening loop evidence:
  - experiments rose from `146` to `151`
  - `29` `HERMES-20260505-*` packets still remain open
- The next engineering packet is now:
  1. codify the June 2 direct runtime mode
  2. hard-block new same-user paid branch creation while conflicts exist
  3. repair the `20260531T183007Z_1084557944` delivery-gate breach
  4. classify the `20260530`, `20260531`, `20260601`, and `20260602` branches into one canonical ladder
  5. normalize one approved ladder across code, docs, prompts, and mini-app
  6. restore disk above `10 GB`
  7. freeze experiment churn until one reviewed proof artifact lands

## 2026-06-01 Correction Set

Use this correction set wherever it conflicts with older May assumptions.

- Treat the current repo state as package-catalog drift, not as a settled product decision:
  - `WellnessBot/main.py` and `WellnessBot/payment_flow.py` now encode a broader product line than the standing strategy docs
  - `WellnessBot/prompts.py` still frames a different three-tier model
  - `mini-app/index.html` still holds a single-entry placeholder story
  - the governing paid case artifact still reflects `week = 3900 RUB`
- Treat text-only intake as the only currently coded modality:
  - `WellnessBot/main.py` explicitly rejects voice messages
  - any copy, plan, or scope note implying broad voice/audio support is stale until restored and re-proved
- Treat full-tier prescriptive logic as an active safety-governance gap:
  - `WellnessBot/prompts.py` currently instructs specific protocol steps, assignment-style output, and anti-parasitic progression in the `full` tier
  - that behavior must not become live product truth without explicit approval, tests, and replay verification
- Treat the latest runtime truth as unchanged from the May 31 outage window:
  - no newer clean artifact exists after `2026-05-31 20:55:40 +03:00`
  - do not narrate runtime as live again before one fresh artifact lands
- Treat disk headroom as worse than the previous mandate:
  - actual `C:` free space is `8.10 GB` at `2026-06-01 23:36:33 +03:00`
- The next engineering packet is now:
  1. choose rollback vs approval for the package catalog
  2. normalize one ladder across menus, texts, prompts, payment code, docs, and mini-app
  3. classify both fresh `20260530` paid cases with `canonical_path` metadata
  4. replay one fresh paid case
  5. capture one fresh runtime artifact
  6. freeze full-tier prescriptive logic until safety review explicitly approves it

## Chief Engineer Mandate

The Chief Engineer owns delivery truth, canonical same-user path control, lab-truth safety, supplement-boundary safety, surface coherence, runtime polling resilience, live-model discipline, and critical-path scope control.

### Immediate responsibilities

1. Keep Telegram as the only live operating channel.
2. Keep manual concierge payment as the official pilot mode.
3. Keep exactly one approved price and offer map at a time; treat every conflicting ladder outside that map as unapproved until normalized.
4. Distinguish paid confirmation from review clearance from delivery-safe output.
5. Keep exactly one canonical paid path per Telegram user.
6. Prevent unreadable labs, malformed typed labs, polluted OCR lines, stale branches, or unresolved review verdicts from becoming client truth.
7. Prevent broadened supplement recommendability from silently crossing the legal/safety boundary.
8. Prevent live-adjacent surfaces from promising more specificity, more automation, or more autonomy than the reviewed backend can support.
9. Prevent runtime health from silently depending on an unstable or stale local proxy path, and prevent multiple concurrent pollers from being treated as acceptable runtime state.
10. Prevent reconnect-based optimism from replacing a proven clean polling path.
11. Improve model-path response discipline without losing the current model reach baseline.
12. Prevent governance churn, offer expansion, or UI polish from replacing paid-cycle truth hardening.
13. Prevent stale May 8 blocker language from surviving after the underlying case statuses have already changed.
14. Prevent safety-sensitive working-tree changes from being described as product proof before they have tests or replayable verification.
15. Prevent silent product-scope drift when intake modalities are disabled in code without an explicit pilot decision and doc alignment.
16. Prevent package-catalog self-selection from becoming live product truth before one approved ladder is written across code, docs, and artifacts.
17. Prevent renamed or expanded tiers from creating new same-user paid branches before the existing paid path is classified or delivered safely.
18. Prevent conflicting price maps from coexisting across surfaces, prompts, payment logic, and case artifacts.
19. Prevent a local patch from being treated as a production fix before a replayable paid artifact proves it.
20. Prevent text-only coded reality from drifting out of sync with docs or sales copy.
21. Prevent full-tier protocol / dose / anti-parasitic specificity from shipping without explicit safety approval and proof.

### Immediate engineering sequence

1. Inspect `WellnessBot/data/submissions/20260501T162705Z_1084557944.json` and `WellnessBot/data/drafts/20260501T162705Z_1084557944.review.json`.
2. Treat `delivery_blocked_needs_revision` on the governing `week` case as a partial repair, not as proof that the case is now coherent.
3. Verify that the blocked delivery state is enforced by code, not only by artifact mutation.
4. Add or confirm replayable smoke coverage for:
   - `needs_revision`
   - `must_rewrite_with_high_caution`
   - explicit manual override path if present
5. Review what operator correction, rewrite, or downgrade is still required on the governing `week` case before it can be reused as proof.
6. Inspect `WellnessBot/data/submissions/20260505T131604Z_1084557944.json`.
7. Record one explicit classification for `20260505T131604Z_1084557944`:
   - `merge-into-canonical`
   - or parked non-canonical premium branch
8. Keep `20260427T173913Z_1084557944`, `20260425T214914Z_1084557944`, and `20260425T212847Z_1084557944` archived unless a deliberate operator decision revives them.
9. Inspect the governing case lab state and current parsed biomarkers.
10. Treat polluted narrative/protocol-like biomarker lines as proof that lab truth is still not safe enough.
11. Inspect current working-tree changes in `WellnessBot/lab_ocr.py`.
12. If broader OCR-line acceptance is not protected by tests, tighten or roll it back.
13. Inspect current working-tree changes in `WellnessBot/supplement_product_catalog.py`.
14. If broadened recommendability allows discontinued or medically sensitive products back into the candidate pool without adequate boundaries, tighten or roll it back.
15. Inspect current working-tree changes in `mini-app/index.html`.
16. Count the price/result cleanup as partial progress, then remove the remaining protocol-style promise from the placeholder result surface.
17. Inspect `bot.stderr.log`.
18. Treat the `2026-05-07 23:46:49-23:46:50 MSK` restart as evidence that runtime was up again, not as proof of resilience.
19. Explain or fix the `GET /health -> 404` outcome logged at `2026-05-08 00:35:06 +0300`.
20. Verify whether polling truly requires `127.0.0.1:12334`; if not, add and document a no-proxy fallback path.
21. Require one clean post-fix verification pass before runtime can be called stable.
22. Inspect `docs/WELLNESS_DIALOGUE_QA_20260530.md` and `ops/reports/quality_report_20260506T080435Z.md`.
23. Preserve the current routing gain:
   - `11/20` deterministic
   - `9/20` model-path
24. Fix the current quality regressions:
   - clarifying-question coverage down to `6/9`
   - invented names appearing twice
   - duplicated emergency templates on prompts `17` and `18`
   - `5/9` model-path replies longer than `2000` characters
25. Extend `sanitize_live_reply()` and prompt rules to block invented names, over-familiar address, early diagnosis-like labels, false specificity, and overlong first-touch mini-consults.
26. Rerun the benchmark only after delivery-gate verification, parser/catalog safety, surface neutrality, and runtime-resilience proof land.
27. Inspect the current `docs/tasks/HERMES-20260505-*` swarm as reference-only backlog, not as proof of execution.
28. Freeze net-new task-packet generation unless it directly closes a delivery, parser/catalog, surface, runtime, or file-fallback gap already visible in artifacts.

### 2026-05-31 11:35 correction set

- Treat the latest runtime artifact as clearly recovered and current:
  - clean start at `2026-05-30 23:51:21 +03:00`
  - handled updates through at least `23:57:08 +03:00`
  - successful DeepSeek calls at `23:55:13`, `23:56:01`, and `23:56:44 +03:00`
- Treat the second fresh same-user paid branch as proof that package-first drift is already live:
  - `20260530T205040Z_1084557944` was created as offer `basic`
  - `amount_rub = 6900`
  - `internal_review.judge_verdict = needs_substantial_rewrite`
  - this is not hypothetical pricing drift anymore; it is live commercial behavior
- Treat the missing PDF export path as a system-wide paid-delivery blocker:
  - both `20260530T183208Z_1084557944` and `20260530T205040Z_1084557944` failed on `NameError: create_premium_pdf is not defined`
  - payment can clear, review can run, and the final dossier can still fail
  - no paid branch from the renamed ladder counts as traction until the final artifact renders
- Treat same-user branch multiplication as the current lead control failure:
  - the current user now spans five paid-relevant paths
  - canonical-path control must happen before new tier creation, not only after cleanup
- Treat disk headroom as still below floor:
  - actual `C:` free space is `9.40 GB` at `2026-05-31 11:35 +03:00`
- Treat product-governance churn as worsening loop evidence:
  - experiments rose from `134` to `140`
  - `29` `HERMES-20260505-*` packets still remain open
- The next engineering packet is now:
  1. restore `create_premium_pdf`
  2. replay both fresh `20260530` paid cases
  3. prevent new same-user tier creation before canonical ownership is checked
  4. classify the two fresh branches
  5. decide approve vs rollback for `500 / 6900 / 14000`
  6. restore disk above `10 GB`
  7. make benchmark runs produce partial artifacts on failure

### 2026-05-31 23:38 correction set

- Treat the latest runtime artifact as intermittent again, not stable:
  - repeated `ProxyConnectionError` against `127.0.0.1:10808` are visible from `2026-05-31 20:47:40 +03:00` through `20:53:15 +03:00`
  - reconnect happens at `20:53:31 +03:00`
  - the same run then falls into repeated `TelegramNetworkError` / `WinError 64` through `20:55:40 +03:00`
  - do not describe runtime as simply live until one newer clean polling artifact exists
- Treat the PDF export path as locally patched but strategically unresolved:
  - current `WellnessBot/main.py` imports `create_premium_pdf` again
  - current `ops/qa_tester_agent.py` now renders through normalized dossier PDF data
  - no post-fix paid replay artifact yet proves `20260530T183208Z_1084557944` or `20260530T205040Z_1084557944` completes
- Treat pricing as the current code-level governance breach:
  - standing pilot docs and mini-app still say `1000 / 6900 / 14900`
  - bot surfaces and prompts say `500 / 6900 / 14000`
  - `payment_flow.py` currently resolves `screening` / `week` to `700` and `basic` / `full` / `premium` / `vip` to `14900`
  - the two fresh paid case artifacts still show `payment_context.amount_rub = 6900`
- Treat the two fresh `20260530` paid cases as unclassified live risk:
  - both lack `canonical_path` metadata
  - neither should be counted as traction, continuation truth, or finished paid delivery until classified and replayed
- Treat product-governance churn as worsening loop evidence:
  - experiments rose from `140` to `146`
  - `29` `HERMES-20260505-*` packets still remain open
- Treat disk headroom as still below floor:
  - actual `C:` free space is `9.38 GB` at `2026-05-31 21:57:00 +03:00`
- The next engineering packet is now:
  1. choose proxy policy for `127.0.0.1:10808` and capture one clean post-decision runtime artifact
  2. replay one fresh paid `20260530` case on the current code
  3. add canonical-path enforcement before same-user case creation
  4. classify both fresh `20260530` branches
  5. collapse pricing truth to one approved ladder across UX, prompts, payment logic, docs, and mini-app
  6. restore disk above `10 GB`
  7. refresh QA synthesis around `ops/reports/quality_report_20260531T083403Z.md`
  8. prove or roll back `case_service.py`, OCR, supplement, and full-tier assignment drift

### 2026-05-30 23:34 correction set

- Treat the latest runtime artifact as recovered, not failed:
  - clean start at `2026-05-30 20:02:07 +03:00`
  - handled updates through at least `21:48:23 +03:00`
  - successful DeepSeek calls at `21:36:26`, `21:37:03`, and `21:37:41 +03:00`
- Treat `127.0.0.1:10808` as the currently working runtime path:
  - do not keep writing the sprint as if the May 27 proxy refusal were still the latest truth
  - keep the current proxy path unless a newer proof artifact disproves it
- Treat the fresh same-user premium path as the main new regression:
  - `20260530T183208Z_1084557944` was created after the canonical-case collapse
  - it has no `canonical_path` metadata
  - it proves the canonical-path rule is still not enforced at submission creation time
- Treat the premium PDF failure as the current delivery blocker:
  - `build_dossier_after_payment` raised `NameError: create_premium_pdf is not defined`
  - payment cleared, but premium delivery could not complete
  - premium monetization is not valid proof until dossier generation works again
- Treat disk headroom as improved but still below floor:
  - actual `C:` free space is `9.58 GB` at `2026-05-30 23:34 +03:00`
  - this is no longer the worst blocker, but still not healthy enough to ignore
- Treat product-governance churn as worsening loop evidence:
  - experiments rose from `127` to `134`
  - `29` `HERMES-20260505-*` packets still remain open
- Treat the QA blocker as observability drift, not total model outage:
  - the batch probe still aborts on first model-path prompt
  - the runtime log now proves live model calls can succeed
  - `ops/quality_probe.py` must survive per-prompt connection failures
- The next engineering packet is now:
  1. fix `create_premium_pdf`
  2. enforce canonical-path checks before same-user premium creation
  3. classify the fresh `20260530` case
  4. restore disk margin above `10 GB`
  5. make benchmark runs produce partial artifacts on failure

### 2026-05-30 correction set

- Treat actual disk headroom as `5.27 GB` at `2026-05-30 11:36:00 +03:00`:
  - far below the floor
  - active ops regression
  - must be recovered before more artifact-heavy proof work
- Treat the latest runtime artifact as a fresh negative proof, not as stability:
  - visible failure window is `2026-05-27 21:51:26-22:05:27 +0300`
  - failure type is repeated `ProxyConnectionError`
  - target is `127.0.0.1:10808`
  - there is no newer clean polling artifact
- Treat the same-user path picture as worse than the May 14 baseline:
  - governing blocked `week` still exists
  - paid `premium` branch from `20260505` still exists
  - a fresh `premium` restart from `20260514` now exists at `consent_pending`
- Treat the current working-tree package-first menu as unverified drift, not as approved product direction:
  - direct package buttons do not override the standing `week`-first commercial rule
  - do not let runtime-down conditions coexist with more aggressive package choice UX
- Treat old `/health` expectations as stale until the web/TMA server is explicitly restored and re-proved:
  - current working-tree `main()` no longer starts TMA
  - `/health` should not remain a success criterion unless that server path is part of the chosen runtime again
- Treat voice/audio removal, OCR relaxation, and supplement recommendability widening as one combined truth-drift bundle:
  - docs must describe them explicitly
  - code must either verify them or reverse them
- Treat `case_service.py` medical-context schema drift as unproven until drafting, review, and follow-up paths are replayed against current artifacts.
- Treat benchmark observability as an active engineering task:
  - the completed benchmark anchor is still `ops/reports/quality_report_20260506T080435Z.md`
  - the latest QA readout is `docs/WELLNESS_DIALOGUE_QA_20260530.md`
  - the full batch still aborts on the first model-path prompt with `openai.APIConnectionError`
- Treat connector status differently from the earlier blocked runs:
  - Notion same-day run-note sync is available again
  - GitHub outward-sync publication is available again
  - Google Drive alone remains blocked because file create/upload/share tools are unavailable
- Treat `127` proposed experiments and `29` `HERMES-20260505-*` packets as active loop evidence:
  - do not add more planning inventory until runtime proof and canonical-path proof land

### 2026-05-14 correction set

- Treat actual disk headroom as `9.82 GB` at `2026-05-14 16:56:05 +03:00`:
  - below the floor
  - active ops regression
  - must be recovered before more artifact-heavy proof work
- Treat the latest runtime artifact as a fresh negative proof, not as stability:
  - live startup log still shows proxy `http://127.0.0.1:10808`
  - duplicate polling remains visible through `2026-05-14 16:55:57 +0300`
  - one reconnect at `2026-05-14 16:47:03 +0300` did not hold
  - `/health` still returns `404` at the latest visible probe `2026-05-13 21:24:04 +0300`
- Treat the same-user `premium` branch as still commercially ambiguous until an explicit `merge-into-canonical` or parked decision lands in artifacts.

- Treat the latest runtime artifact as a fresh negative proof, not as stability:
  - live startup log still shows proxy `http://127.0.0.1:10808`
  - duplicate polling remains visible through `2026-05-14 16:50:53 +0300`
  - one reconnect at `2026-05-14 16:47:03 +0300` did not hold
  - `/health` still returns `404` at the latest visible probe `2026-05-13 21:24:04 +0300`
- Stop carrying `127.0.0.1:12334` forward as assumed truth until it is re-proved from current runtime artifacts.
- Treat duplicate polling as higher-impact than another connector-status or copy-polish loop.
- Treat text-only intake as the current live truth until voice/audio is restored and proven.
- Treat monetization proof as blocked until the same-user `week` / `premium` relation is explicit and the runtime path is single-instance coherent.
- Treat actual disk headroom as `10.55 GB` at `2026-05-14 16:50:50 +03:00`:
  - still above the floor
  - too thin to ignore
  - still below proof work in priority
- Treat `127` proposed experiments and `29` `HERMES-20260505-*` packets as active loop evidence:
  - do not add more planning inventory until the runtime and canonical-path proof bundle lands

### 2026-05-13 correction set

- Treat the absence of a new same-day proof artifact as the main current failure:
  - latest visible runtime probe is still May 8
  - latest visible QA benchmark is still May 6
  - no new product-shipping or verification artifact landed after the morning refresh
- Treat `20260505T131604Z_1084557944` as parked non-canonical by default until an explicit merge decision is recorded in artifacts
- Treat actual disk headroom as `10.67 GB` at `2026-05-13 16:47:39 +03:00`:
  - still above the floor
  - still too thin to ignore
  - not important enough to outrank proof work
- Treat voice/audio shutdown, OCR relaxation, and supplement-boundary widening as still-unverified drift:
  - do not describe them as product progress
  - either prove them with tests/checks or reverse them
- Treat same-day strategy/task packet churn as blocked work until one fresh proof artifact lands

- Treat disk hygiene as improved enough to leave the top engineering slot:
  - `docs/DISK_HYGIENE_STATUS.md` records `10.95 GB` free at `2026-05-12 16:48:40 +03:00`
  - keep monitoring it, but do not let it outrank proof work again unless it drops back below the floor
- Treat the absence of new proof as the current bottleneck:
  - latest visible runtime probe is still May 8
  - latest visible QA benchmark is still May 6
  - no fresh acceptance artifact exists yet for the May 12 strategy correction
- Treat the fresh paid premium branch as the remaining commercial ambiguity:
  - `20260505T131604Z_1084557944` must be explicitly `merge-into-canonical` or parked
- Until that explicit relation exists, treat the branch as parked and non-proof-bearing
- Treat voice/audio shutdown as a product-truth issue, not just a code diff:
  - if STT is intentionally retired, update docs and offer language
  - if STT is required for pilot intake, restore it safely and prove it
- Treat OCR and supplement-catalog relaxations as blocked from shipping until tests or rollback decisions exist
- Treat connector churn as secondary work; product truth does not depend on external sync being green

### 2026-05-12 correction set

- Treat the governing `week` case change on `2026-05-11` as real progress:
  - the case is no longer silently marked delivered
  - the delivery gate appears to be doing something meaningful now
  - that repair still needs verification and operator recovery logic
- Treat the same-user branch picture as materially changed:
  - three stale branches are now archived
  - one fresh paid premium branch still needs explicit canonical ownership
- Treat mini-app cleanup as partial rather than absent:
  - off-policy `2990` pricing is gone
  - hardcoded `Premium Wellness-Досье`, `Vitamin D3`, and `LCHF` demo content are gone
  - the placeholder still over-promises reviewed protocol output
- Treat lab parsing safety as more urgent than earlier docs suggested:
  - the governing case still shows polluted biomarker lines
  - the working tree currently loosens OCR parsing further
- Treat supplement safety as newly urgent:
  - the working tree currently broadens recommendable catalog output beyond the prior conservative boundary
- Treat the runtime and QA truth as still stale:
  - latest visible runtime proof remains May 8 `/health -> 404`
  - latest visible benchmark remains May 6
- Treat `127` experiments and `29` same-day HERMES task files as still-valid loop signals.
- Treat the old `4` duplicate groups / `x8` metric as stale unless regenerated from current data.

### Things the Chief Engineer must block

- any delivery transition that ignores an unresolved review verdict
- any claim that the governing `week` case is now healthy just because it is blocked instead of delivered
- any same-user concurrency across active `week` and unclassified `premium` paths
- any attempt to revive archived test runs into the live commercial story without an explicit decision
- any treatment of unreadable, unconfirmed, or polluted OCR/typed lines as delivery-safe facts
- any broadened supplement recommendability that crosses the existing legal/safety posture
- any silent removal of voice/audio intake support without an explicit product decision and doc update
- any mini-app or TMA surface that implies a reviewed personalized protocol before reviewed backend truth exists
- any runtime setup that silently requires an intermittently unavailable proxy listener without a documented fallback and health signal
- any claim that polling resilience is fixed before one clean post-fix verification passes
- any claim that OCR/file reliability is solved before real PDF/photo/manual-text verification passes
- any prompt or sanitizer pass that collapses model reach back toward template capture
- any symptom reply that invents names, uses unwarranted familiarity, duplicates emergency handling across risk classes, or applies an early diagnostic label without evidence
- any treatment of the standalone paid `premium` branch as traction before it is explicitly merged into the canonical same-user thread
- any new strategy refresh written from stale May 8 blocker assumptions after the underlying artifacts have already changed
- any same-day strategy/task churn that lands before one fresh proof artifact
- any critical-path move toward Telegram Payments/YooKassa automation, PostgreSQL migration, Docker deployment, or separate admin/WebApp work before the current pilot is coherent
- any accumulation of new task packets, launch plans, or readiness reports that restates already known P0 work without closing it
- any active `vip` selling
- any pricing or packaging drift before one clean canonical path exists
- any new same-user `screening`, `basic`, `full`, or `premium` branch created before the existing paid path is classified or delivered safely
- any claim that the PDF path is fixed before a fresh paid replay artifact exists
- any claim that `500 / 6900 / 14000` or `700 / 14900 / 14900` is approved product truth before governance explicitly says so

## Lead Developer / Executor Mandate

The Lead Developer / Executor owns the concrete repo and runtime behaviors that make blocked delivery auditable, canonical same-user ownership explicit, lab truth safer, supplement boundaries conservative, the live Telegram experience more trustworthy, manual-lab fallback more reliable, and polling operationally explicit.

### Sprint tasks

1. Prove the delivery gate instead of just describing it.
2. Make the governing blocked `week` case coherent enough for operator recovery.
3. Turn the fresh paid `premium` case into either a same-case continuation or an explicitly parked branch.
4. Keep archived test runs from contaminating the current commercial story.
5. Prevent broadened OCR parsing from promoting noisy lab lines into product truth.
6. Prevent broadened supplement catalog output from turning into unsafe recommendations.
7. Keep mini-app placeholder content aligned with the actual Telegram-first reviewed product.
8. Make polling resilient enough that reconnects are not mistaken for stability.
9. Preserve model reach while tightening specificity, tone discipline, and emergency-template separation.
10. Reflect live evidence in strategy docs without creating documentation-only motion.
11. Do not count the floating paid `premium` branch as product proof until it is explicitly merged or parked in artifacts.
12. Do not count renamed tier sales as progress while they multiply same-user paid branches and still fail final delivery.

### Definition of done

A task is not done unless:

- it improves delivery truth
- it reduces ambiguity around the canonical same-user path
- it improves lab truth or surface safety in a measurable way
- it preserves legal and supplement-safety boundaries
- it makes runtime polling behavior explicit and reliable
- it proves runtime resilience rather than inferring it from reconnects
- it proves file/lab fallback behavior instead of assuming UX landing solved it
- it preserves or clarifies routed-vs-model truth for live dialogue
- it survives available checks, logs, benchmark evidence, and operator review
- it makes the next paid cycle easier to explain and defend
- it removes a loop instead of creating another

## Quality Auditor Mandate

The auditor must stop the cycle if any of these are true:

- `delivered_to_client` appears while internal review still demands revision and no override record exists
- the governing blocked `week` case is presented as success proof before its lab truth is reconciled
- more than one active same-user paid path exists
- `20260505T131604Z_1084557944` is active without an explicit canonical relation
- archived test runs quietly re-enter the live product story
- unreadable, unconfirmed, or polluted OCR/typed lines are treated as delivery-safe facts
- broadened supplement catalog output is being treated as acceptable without safety review
- mini-app or TMA surfaces imply reviewed personalized protocol output without backend truth
- polling still depends on a flapping proxy path with no documented fallback or health signal
- polling is described as stable before one clean post-fix verification pass
- benchmark evidence shows invented personalization, duplicated emergency handling, false specificity, or overlong first-touch replies without mitigation
- governance expansion is being treated as progress while canonical path truth is unresolved
- renamed tier sales are being treated as traction while dossier rendering still fails

## Sprint Focus For The Next Execution Cycle

### Focus 1

Verify delivery-gate behavior and recover the governing blocked case.

### Focus 2

Reduce the current user to one canonical commercial path, including the fresh `20260505` premium case.

### Focus 3

Tighten OCR/manual-lab parsing and supplement-boundary safety before any new dossier truth is trusted.

### Focus 4

Finish mini-app result neutralization.

### Focus 5

Make polling resilient enough that runtime stability is explicit, verified, and not inferred from reconnects.

### Focus 6

Compress loops so the next artifact is a shipped fix or verification result, not another stale plan layer.

### Focus 7

Improve live-model discipline while preserving the current `9/20` model-path reach.

### Focus 8

Make intake-modality truth explicit: restore safe STT or formally retire it from the pilot scope.

## Loop-Break Rule

If blocked-case recovery stalls, the fresh premium branch still floats, polluted lab truth persists, supplement-boundary drift remains, the mini-app keeps protocol-style promises, or proxy failures continue without a documented fallback:

1. stop
2. freeze net-new strategy/task packet generation until a direct P0 fix lands
3. inspect the canonical case artifact and attached review artifact
4. classify each case item as canonical, merge-into-canonical, parked, or archive
5. classify each surface element as reviewed truth, safe placeholder, or off-policy copy
6. classify each lab input path as proven, partially proven, or unproven
7. classify each safety-sensitive working-tree diff as verified, unverified, or rollback-required
8. classify polling as proxy-required or proxy-optional with an explicit fallback path and health signal
9. prove the chosen polling path with one clean post-fix verification
10. keep exactly one canonical paid path
11. remove off-policy surface output
12. rerun the benchmark only after the truth and resilience fixes land

No silent delivery bypass, silent same-user multiplication, silent lab-truth pollution, silent supplement-boundary drift, silent frontend truth drift, silent proxy fragility, or silent roadmap drift is allowed.
