# Sprint Board

Date: 2026-06-03
Status: June 3 refresh; runtime baseline is unchanged from June 2 direct fallback, but the lead blocker is now continuity-chat safety plus commercialization control because the active `500 RUB` thread is overreaching while `14000 / 14900` branches still lack canonical closure and disk is down to `6.59 GB`
Sprint owner: Chief Orchestrator
Operating mode: controlled Telegram-first pilot truth hardening

## 2026-06-03 11:45 MSK Delta

What changed:

- runtime did not improve today:
  - no newer artifact exists after `2026-06-02 21:16:49 +03:00`
  - direct fallback remains the active baseline
  - stop spending sprint energy re-arguing proxy dependency until a newer artifact exists
- QA truth is better defined but still not operationally complete:
  - `tests/test_live_reply_routing.py` passed on June 3
  - `ops/quality_probe.py --mode smoke` passed on June 3
  - full batch still aborts on prompt `1` with `openai.APIConnectionError` / `[WinError 10061]`
  - the sprint blocker is now missing partial artifacts on model-path failure, not lack of any QA signal
- the strongest current product proof is also the strongest current safety risk:
  - the active `20260602T055745Z_1084557944` `nutri_chat` thread is still the best live value signal
  - the same thread now clearly overreaches with long mechanism-heavy interpretation and `30 days` continuity framing inside the low-ticket rail
- the same-user commercial stack is still not closed:
  - only `20260501`, `20260505`, and `20260514` have canonical classification
  - `20260530T183208Z_1084557944`, `20260530T205040Z_1084557944`, `20260531T183007Z_1084557944`, `20260601T204906Z_1084557944`, and `20260602T055745Z_1084557944` still have no `canonical_path`
  - `20260531T183007Z_1084557944` remains the top breach: `14900 RUB`, `delivered_to_client`, `fail_major_issues`
- loop pressure is now measurable repetition, not just backlog size:
  - `151` experiments still exist
  - `0` decisions exist
  - the top experiment titles repeat `12`, `11`, `8`, `8`, and `5` times
  - `29` `HERMES-20260505-*` packets still sit open
- surface churn is too large for current proof quality:
  - current diff shows broad edits across `9` frontend/product files
  - no fresh artifact proves the widened ladder/surface is safer or clearer
- disk margin is worse again:
  - current `C:` free space is `6.59 GB` at `2026-06-03 11:38:49 +03:00`

Next 12h command set:

1. Keep `2026-06-02 21:16:49 +03:00` direct fallback as the standing runtime baseline until a newer artifact exists.
2. Patch `ops/quality_probe.py` so prompt-level connection failures still emit a partial batch artifact.
3. Re-run the benchmark only after step `2` lands.
4. Tighten the live-chat contract in prompt and sanitizer rules: answer first, max `2` early hypotheses, max `2` clarifying questions, no markdown bullets, no unsupported diagnosis-like storytelling.
5. QA-audit the active `20260602T055745Z_1084557944` `nutri_chat` thread against that contract.
6. Add a hard guard so unresolved same-user paid/review state blocks creation of another paid branch.
7. Audit `20260531T183007Z_1084557944` and repair the `delivered_to_client` plus `fail_major_issues` contradiction.
8. Classify `20260530T183208Z_1084557944`, `20260530T205040Z_1084557944`, `20260531T183007Z_1084557944`, `20260601T204906Z_1084557944`, and `20260602T055745Z_1084557944` into one canonical same-user ladder.
9. Keep `nutri_chat` as the only active paid rail while `standard` and `premium` remain review-gated.
10. Keep Telegram-first manual concierge mode and text-only intake unchanged while this packet is open.
11. Freeze net-new experiments and task-packet churn until the continuity-safety packet is closed.
12. Restore `C:` above the `10 GB` floor and log the new baseline.

## 2026-06-02 23:41 MSK Delta

What changed:

- runtime is stronger than the morning board:
  - `bot.stderr` shows another clean startup at `2026-06-02 21:16:48-21:16:49 +03:00`
  - proxy failure again falls back to direct connection
  - the current runtime story is now same-day repeated proof, not one isolated morning recovery
- the freshest product proof is no longer abstract ladder design:
  - `runtime_state.json` still holds paid session `20260602T055745Z_1084557944`
  - the active thread now contains real multi-turn `nutri_chat` continuity behavior after payment
  - this is the strongest current value signal in the repo
- the same-user commercial stack is still uncontrolled:
  - `premium = 6900` with `pass_with_major_edits`
  - `basic = 6900` with `needs_substantial_rewrite`
  - `basic = 14900` with `delivered_to_client` plus `fail_major_issues`
  - `basic = 14000` with `needs_revision`
  - `nutri_chat = 500` active in runtime memory
  - none of those five recent paid cases has `canonical_path` metadata
- safety pressure widened from drafts into live chat:
  - the active paid chat already gives mechanism-heavy guidance and frames support as `30 days` continuity
  - prompt-layer full-tier specificity is still broader than the approved pilot boundary
- loop pressure did not improve:
  - `151` experiments still exist
  - `29` `HERMES-20260505-*` packets still sit open
- disk margin is worse again:
  - current `C:` free space is `6.62 GB` at `2026-06-02 23:39:07 +03:00`

Next 12h command set:

1. Treat the June 2 direct-fallback runtime as the locked baseline unless a newer artifact disproves it.
2. Add a hard guard so unresolved same-user paid/review state blocks new paid branch creation.
3. QA-audit the active `20260602T055745Z_1084557944` `nutri_chat` thread for safety, over-specificity, and escalation boundaries.
4. Audit `20260531T183007Z_1084557944` and repair the `delivered_to_client` plus `fail_major_issues` contradiction.
5. Classify `20260530T183208Z_1084557944`, `20260530T205040Z_1084557944`, `20260531T183007Z_1084557944`, `20260601T204906Z_1084557944`, and `20260602T055745Z_1084557944` into one canonical same-user ladder.
6. Decide whether the active approved ladder for the next 12h is `nutri_chat -> standard`, with `premium` parked until controls are repaired.
7. Normalize that ladder across `WellnessBot/main.py`, `WellnessBot/texts.py`, `WellnessBot/payment_flow.py`, `WellnessBot/prompts.py`, docs, and `mini-app/index.html`.
8. Keep Telegram-first manual concierge mode and text-only intake unchanged while this decision is open.
9. Freeze full-tier protocol / dose / anti-parasitic behavior until safety review explicitly approves it.
10. Restore `C:` above the `10 GB` floor and log the new baseline.
11. Freeze net-new experiments and task-packet churn until the continuity-governance packet is closed.
12. Refresh QA synthesis only after steps `1-11` land.

## 2026-06-02 11:40 MSK Delta

What changed:

- the lead blocker changed again:
  - runtime is no longer stale-negative
  - `bot.stderr` now shows proxy failure at `2026-06-02 00:13:24 +03:00`, successful direct fallback, clean polling start, DeepSeek `200 OK`, and handled updates through `10:24:09 +03:00`
  - the current ops problem is now governance, not basic liveness
- same-user commercial sprawl widened materially:
  - `20260531T183007Z_1084557944` = `basic` sold at `14900 RUB`, marked `delivered_to_client`, while `judge_verdict = fail_major_issues`
  - `20260601T204906Z_1084557944` = `basic` / `standard` sold at `14000 RUB`, manually paid, `judge_verdict = needs_revision`
  - `20260602T055745Z_1084557944` = `nutri_chat` sold at `500 RUB`, manually paid, active in `runtime_state.json`
  - older `20260530` paid `premium` and `basic` branches still remain unresolved in the same user story
- the monetization story is now not just inconsistent; it is live alias collision:
  - governing artifact still says `week = 3900 RUB`
  - mini-app still says `1000 RUB`
  - prompts still imply `500 / 6900 / 14000`
  - current payment/menu path is `500 / 14000 / 14900`
  - live sales now include `basic = 14900`, `standard/basic = 14000`, and `nutri_chat = 500`
- loop pressure worsened again:
  - `151` experiments now exist in `WellnessBot/data/product_governance.json`
  - `29` `HERMES-20260505-*` task packets still sit open
- disk margin is worse again:
  - current `C:` free space is `7.32 GB` at `2026-06-02 11:37:32 +03:00`

Next 12h command set:

1. Treat the June 2 direct-fallback runtime as the current baseline and document whether proxy `127.0.0.1:10808` is optional or removable.
2. Add a hard guard so unresolved same-user paid/review state blocks creation of another paid branch.
3. Audit `20260531T183007Z_1084557944` and repair the `delivered_to_client` plus `fail_major_issues` contradiction.
4. Classify `20260530T183208Z_1084557944`, `20260530T205040Z_1084557944`, `20260531T183007Z_1084557944`, `20260601T204906Z_1084557944`, and `20260602T055745Z_1084557944` into one canonical same-user ladder.
5. Choose and normalize one approved ladder across `WellnessBot/main.py`, `WellnessBot/texts.py`, `WellnessBot/payment_flow.py`, `WellnessBot/prompts.py`, `WellnessBot/ai_drafting.py`, docs, and `mini-app/index.html`.
6. Keep Telegram-first manual concierge mode and text-only intake unchanged while the ladder decision is open.
7. Freeze `full`-tier specific protocol / dose / anti-parasitic behavior until safety review explicitly approves it.
8. Restore `C:` above the `10 GB` floor and log the new baseline.
9. Freeze net-new experiments and task-packet churn until the continuity-governance packet is closed.
10. Publish one fresh reviewed proof artifact only after steps `1-9` land.

## 2026-06-01 23:40 MSK Delta

What changed:

- the lead drift is now product-line mutation, not just price inconsistency:
  - `WellnessBot/main.py` start and product menus now default to a five-offer catalog
  - `WellnessBot/payment_flow.py` partially aligns to that catalog
  - `WellnessBot/prompts.py` still describes a three-tier `500 / 6900 / 14000` structure
  - `mini-app/index.html` still keeps a safer `1000 RUB` single-entry placeholder
  - the governing canonical paid case still records `week = 3900 RUB`
- the current repo therefore contains several incompatible monetization stories at once:
  - historical case artifact at `3900 RUB`
  - standing docs / placeholder mini-app at `1000 / 6900 / 14900 RUB`
  - prompt architecture at `500 / 6900 / 14000 RUB`
  - current package catalog at `500 / 6900 / 14000 / 14900 / 5000 RUB`
- runtime is still not freshly re-proven:
  - no artifact newer than `2026-05-31 20:55:40 +03:00` exists in `bot.stderr`
  - latest visible truth is still proxy refusal, brief reconnect, and network degradation on `127.0.0.1:10808`
- text-only scope is now coded truth:
  - `WellnessBot/main.py` explicitly rejects voice messages and asks for text instead
- safety surface widened again:
  - `WellnessBot/prompts.py` gives the `full` tier concrete protocol, dose, and anti-parasitic-step behavior that the current pilot has not approved as live product truth
- canonical-path closure is still incomplete:
  - `20260501` remains canonical blocked `week`
  - `20260505` remains `merge_into_canonical`
  - `20260514` remains `parked_duplicate`
  - both fresh `20260530` paid cases still have no `canonical_path` metadata
- loop pressure did not improve:
  - `146` experiments still exist in `WellnessBot/data/product_governance.json`
  - `29` `HERMES-20260505-*` task packets still sit open
- disk margin is worse than the previous refresh:
  - current `C:` free space is `8.10 GB` at `2026-06-01 23:36:33 +03:00`

Next 12h command set:

1. Decide whether the five-offer catalog is approved product direction or must be rolled back to one proof-bearing rail.
2. Normalize one price and offer ladder across `WellnessBot/main.py`, `WellnessBot/texts.py`, `WellnessBot/payment_flow.py`, `WellnessBot/prompts.py`, `WellnessBot/ai_drafting.py`, docs, and `mini-app/index.html`.
3. Write explicit `canonical_path` metadata for `20260530T183208Z_1084557944` and `20260530T205040Z_1084557944`.
4. Replay one fresh paid case on the chosen ladder and record whether dossier delivery completes.
5. Capture one runtime artifact newer than `2026-05-31 20:55:40 +03:00`.
6. Keep Telegram-first manual concierge mode and text-only intake unchanged while the ladder decision is open.
7. Freeze `full`-tier specific protocol / dose / anti-parasitic behavior until safety review explicitly approves it.
8. Restore `C:` above the `10 GB` floor and log the new baseline.
9. Refresh QA synthesis around `ops/reports/quality_report_20260531T083403Z.md` only after steps `1-8` land.
10. Freeze net-new experiment and task-packet churn until the catalog-vs-proof packet is closed.

## 2026-05-31 23:38 MSK Delta

What changed:

- the noon runtime-live story is stale:
  - `bot.stderr` now shows repeated `ProxyConnectionError` against `127.0.0.1:10808` from `20:47:40` through `20:53:15 +03:00`
  - polling reconnects at `20:53:31 +03:00`
  - the same run then degrades into `TelegramNetworkError` / `WinError 64` through `20:55:40 +03:00`
  - current runtime truth is therefore intermittent, not stable
- the PDF export blocker has shifted from "known missing import" to "local patch with no proof":
  - current `WellnessBot/main.py` imports `create_premium_pdf` again
  - current `ops/qa_tester_agent.py` now renders PDF through the normalized dossier path
  - there is still no fresh paid replay artifact proving one `20260530` case completes end to end
- monetization truth is now triply split:
  - standing docs and mini-app: `1000 / 6900 / 14900`
  - live bot surfaces and prompts: `500 / 6900 / 14000`
  - `payment_flow.py`: `700 / 14900 / 14900` variants, while the two fresh paid case artifacts still show `6900 RUB`
- canonical-path control is still not closed:
  - one user still spans five paid-relevant paths
  - the two fresh `20260530` branches still have no `canonical_path` metadata
- loop pressure worsened again:
  - `146` experiments now exist in `WellnessBot/data/product_governance.json`
  - `29` `HERMES-20260505-*` task packets still sit open
- disk margin slipped slightly lower:
  - current `C:` free space is `9.38 GB` at `2026-05-31 21:57:00 +03:00`

Next 12h command set:

1. Decide whether proxy `127.0.0.1:10808` is required, optional with fallback, or must be removed, then capture one clean runtime artifact newer than `2026-05-31 20:55 MSK`.
2. Replay `20260530T183208Z_1084557944` or `20260530T205040Z_1084557944` with the current code and record whether PDF delivery now completes.
3. Add canonical-path enforcement before any new same-user `screening`, `basic`, `full`, or `premium` submission is created.
4. Classify both fresh `20260530` paid branches and keep only one canonical commercial story.
5. Collapse pricing truth to one approved ladder across bot UX, prompts, payment logic, docs, and mini-app.
6. Keep `week` as the only standing paid entry rail until the ladder decision is explicit.
7. Restore `C:` above the `10 GB` floor and log the new baseline.
8. Refresh QA synthesis around `ops/reports/quality_report_20260531T083403Z.md`.
9. Prove or roll back `case_service.py`, OCR, supplement, and full-tier assignment drift.
10. Freeze net-new experiment and task-packet churn until steps `1-9` land.

## 2026-05-31 11:35 MSK Delta

What changed:

- the newest runtime truth is stronger than the prior refresh:
  - clean bot start at `2026-05-30 23:51:21 +03:00`
  - polling alive through at least `23:57:08 +03:00`
  - DeepSeek model calls succeeded at `23:55:13`, `23:56:01`, and `23:56:44 +03:00`
- the current P0 failure widened from one broken paid branch to two:
  - `20260530T183208Z_1084557944` = paid `premium` at `6900 RUB`
  - `20260530T205040Z_1084557944` = paid `basic` at `6900 RUB`
  - both cases failed on `NameError: create_premium_pdf is not defined`
- package-first intake is now proven live behavior:
  - the working tree advertises `screening / basic / full`
  - a renamed `basic` case was actually sold in Telegram
  - pilot documentation still says `week / premium / vip` with `1000 / 6900 / 14900 RUB`
- canonical-path control regressed again:
  - one Telegram user now spans five paid-relevant paths
  - the two newest `20260530` branches do not count as product proof until explicitly classified
- disk and loop pressure remain unhealthy:
  - current `C:` free space is `9.40 GB`
  - `140` experiments now exist in `WellnessBot/data/product_governance.json`
  - `29` `HERMES-20260505-*` task packets still sit open
- QA and runtime still diverge:
  - runtime proves the model path works live
  - batch QA still aborts on the first model-path prompt
  - the missing artifact is resilient per-prompt error handling in `ops/quality_probe.py`

Next 12h command set:

1. Restore `create_premium_pdf` and replay both fresh `20260530` paid cases.
2. Block new same-user `screening`, `basic`, `full`, and `premium` submissions before canonical ownership is checked.
3. Reclassify `20260530T183208Z_1084557944` and `20260530T205040Z_1084557944` as merge, parked duplicate, invalid branch, or rollback target.
4. Restore `C:` above the `10 GB` floor and log the new baseline.
5. Decide whether `500 / 6900 / 14000` is approved or must be rolled back to `1000 / 6900 / 14900`.
6. Keep `week` as the only standing paid entry rail until the ladder decision is explicit.
7. Preserve the working runtime path on `127.0.0.1:10808`.
8. Prove or roll back `case_service.py`, OCR, and supplement drift.
9. Make `ops/quality_probe.py` emit partial per-prompt artifacts on model failures.
10. Produce one fresh proof artifact only after steps `1-9` land.

## 2026-05-30 23:34 MSK Delta

What changed:

- the newest runtime truth is positive again:
  - clean bot start at `2026-05-30 20:02:07 +03:00`
  - polling alive through at least `21:48:23 +03:00`
  - DeepSeek model calls succeeded at `21:36:26`, `21:37:03`, and `21:37:41 +03:00`
- the current P0 failure moved from proxy refusal to premium delivery integrity:
  - fresh paid case `20260530T183208Z_1084557944` was created on the same user
  - dossier generation then failed with `NameError: create_premium_pdf is not defined`
  - this is proof that payment can clear before premium delivery is complete
- canonical-path cleanup landed for older branches but is not enforced on the newest branch:
  - `20260501` = canonical blocked `week`
  - `20260505` = `merge_into_canonical`
  - `20260514` = `parked_duplicate`
  - `20260530` = fresh uncategorized `premium` branch with no `canonical_path`
- product drift is now concrete, not hypothetical:
  - package-first selling reopened a new same-user premium path
  - the result still did not produce a reviewed premium dossier
- disk recovered from the morning low, but not enough:
  - current `C:` free space is `9.58 GB`
  - still below the `10 GB` floor
- loop pressure is worse:
  - `134` experiments now exist in `WellnessBot/data/product_governance.json`
  - `29` `HERMES-20260505-*` task packets still sit open
- QA and runtime are no longer telling the same story:
  - batch QA still aborts on first model-path prompt
  - live runtime now proves model calls can work
  - the gap is now observability/tooling, not only runtime transport

Next 12h command set:

1. Restore `C:` above the `10 GB` floor and log the new baseline.
2. Fix the missing `create_premium_pdf` path and prove premium dossier rendering again.
3. Block creation of a same-user `premium` case until canonical ownership is checked.
4. Add `canonical_path` metadata at submission creation time, not only during later cleanup.
5. Reclassify `20260530T183208Z_1084557944` as merge, parked duplicate, or invalid branch.
6. Keep `week` as the only active paid entry rail in bot UX and docs.
7. Preserve the now-working proxy/runtime path on `127.0.0.1:10808`.
8. Decide and document the voice/audio status instead of leaving it implicit.
9. Keep OCR and supplement changes out of client truth until verified or rolled back.
10. Make `ops/quality_probe.py` emit partial per-prompt artifacts on model failures.
11. Produce one fresh proof artifact only after steps `1-10` land.

## 2026-05-30 11:36 MSK Delta

What changed:

- the newest runtime artifact is not duplicate polling anymore; it is sustained `ProxyConnectionError` against `127.0.0.1:10808` from `2026-05-27 21:51:26 +0300` through `22:05:27 +0300`
- disk margin collapsed further to `5.27 GB` free at `2026-05-30 11:36:00 +03:00`
- runtime memory is empty, so the live story must be rebuilt from persisted submissions rather than active sessions
- the same user now spans three live-relevant paths:
  - blocked `week` on `20260501`
  - paid/reviewed `premium` on `20260505`
  - restarted `premium` at `consent_pending` on `20260514`
- the working tree is drifting toward package-first intake while the runtime is less reliable:
  - direct package buttons are now the start menu in `WellnessBot/main.py`
  - voice/audio and manual biomarker parsing are removed from the active path
  - TMA startup is removed from `main()`, so old `/health` assumptions are stale unless reintroduced deliberately
  - `case_service.py` changes persisted medical-context field names without fresh end-to-end proof
- connector truth improved in this run:
  - Notion same-day run-note sync succeeded
  - GitHub outward-sync publication succeeded
  - Google Drive remains unavailable because file create/upload/share tools are not exposed
- QA truth tightened:
  - latest completed benchmark remains `ops/reports/quality_report_20260506T080435Z.md`
  - latest QA readout is `docs/WELLNESS_DIALOGUE_QA_20260530.md`
  - full batch benchmarking still aborts on the first model-path prompt with `openai.APIConnectionError`

Next 12h command set:

1. Restore `C:` above the `10 GB` floor.
2. Produce one clean runtime artifact newer than `2026-05-27 22:05 MSK`.
3. Decide whether `127.0.0.1:10808` is required infrastructure, optional infrastructure, or dead config to remove.
4. Collapse `20260501`, `20260505`, and `20260514` into one canonical paid path for the same user.
5. Keep `week` as the only active entry rail until the canonical path is explicit.
6. Decide `restore` vs `retire-and-document` for voice/audio intake.
7. Add proof or rollback for `case_service.py` schema drift.
8. Tighten or roll back OCR filter relaxation and discontinued-iron recommendability widening.
9. Make `ops/quality_probe.py` emit partial per-prompt artifacts on model failures.
10. Keep mini-app and landing output placeholder-only and explicitly unverified.
11. Freeze net-new experiment / task-packet churn until the runtime and canonical-path proof bundle lands.
12. Produce one fresh runtime or QA artifact only after steps `1-11` are coherent.

## 2026-05-14 16:56 MSK Delta

What changed:

- the latest runtime artifact is still negative proof, and it is now sustained through `2026-05-14 16:55:57 +0300`
- one reconnect at `16:47:03 MSK` did not hold
- the live proxy truth is still `127.0.0.1:10808`
- the latest visible `/health` result is still `404`
- disk margin is now below the floor at `9.82 GB`
- product scope is effectively text-first right now because voice/audio remains disabled in the working tree
- the same-user `premium` branch still needs explicit canonical classification

Next 12h command set:

1. Restore `C:` above the `10 GB` floor.
2. Stop the duplicate Telegram polling instance and prove one clean runtime start path.
3. Record the actual proxy/health truth and remove the stale `127.0.0.1:12334` assumption unless it is still truly active.
4. Explicitly classify the same-user `premium` branch as canonical merge or parked branch.
5. Decide `restore` vs `retire-and-document` for voice/audio intake.
6. Add proof or rollback for OCR filter relaxation and supplement recommendability widening.
7. Keep mini-app output placeholder-only and qualify landing proof copy as unverified.
8. Freeze net-new experiment / task-packet churn until the runtime and canonical-path proof bundle lands.
9. Produce one fresh runtime or QA artifact after the safety-sensitive path is coherent.

## 2026-05-14 16:50 MSK Delta

What changed:

- the latest runtime artifact is still negative proof, and it is now sustained in the same local day:
  - duplicate polling remains visible through `2026-05-14 16:50:53 +0300`
  - one reconnect at `16:47:03 MSK` did not hold
  - the live proxy truth is still `127.0.0.1:10808`
  - the latest visible `/health` result is still `404`
- this means runtime-instance control outranks more connector narration, more strategy churn, and more backlog generation
- disk margin is slightly better at `10.55 GB`, but still thin
- product scope is effectively text-first right now because voice/audio remains disabled in the working tree
- loop pressure is still visible in the repo:
  - `127` proposed experiments
  - `29` same-day `HERMES-20260505-*` task files

Next 12h command set:

1. Stop the duplicate Telegram polling instance and prove one clean runtime start path.
2. Record the actual proxy/health truth and remove the stale `127.0.0.1:12334` assumption unless it is still truly active.
3. Explicitly classify the fresh paid `premium` branch as canonical merge or parked branch.
4. Decide `restore` vs `retire-and-document` for voice/audio intake.
5. Add proof or rollback for OCR filter relaxation and supplement recommendability widening.
6. Keep mini-app output placeholder-only and qualify landing proof copy as unverified.
7. Freeze net-new experiment / task-packet churn until the runtime and canonical-path proof bundle lands.
8. Produce one fresh runtime or QA artifact after the safety-sensitive path is coherent.

## 2026-05-13 16:54 MSK Delta

What changed:

- the sync cycle is now closed with verified connector outcomes rather than inferred availability
- Notion and GitHub are blocked by the same MCP initialize handshake failure on real calls
- Google Drive is still unavailable because file discovery/create/upload/share tools are not exposed
- landing proof-style copy is now explicitly counted as marketing debt alongside the already-safer mini-app placeholder
- disk remains above the floor at `10.67 GB`, but that does not change the sprint order

Next 12h command set:

1. Explicitly classify the fresh paid `premium` branch as canonical merge or parked branch.
2. Decide `restore` vs `retire-and-document` for voice/audio intake.
3. Add proof or rollback for OCR filter relaxation.
4. Add proof or rollback for supplement recommendability widening.
5. Keep mini-app output placeholder-only and qualify landing proof copy as unverified.
6. Produce one fresh runtime or QA artifact after the safety-sensitive path is coherent.

## 2026-05-13 16:47 MSK Delta

What changed:

- no newer QA, runtime, or product-proof artifact exists beyond the morning refresh
- disk is still above the floor, but only at `10.67 GB` free, so it remains a monitor rather than the lead sprint slot
- the fresh paid `premium` branch should now be treated operationally as parked non-canonical until an explicit merge decision is written
- same-day strategy/task churn is now explicitly off the critical path until one proof artifact lands
- voice/audio shutdown, OCR relaxation, and supplement recommendability widening remain unverified drift, not sprint progress

Next 12h command set:

1. Record `20260505T131604Z_1084557944` as parked non-canonical pending merge, or merge it explicitly.
2. Decide `restore` vs `retire-and-document` for voice/audio intake.
3. Add tests or roll back the OCR filter relaxation.
4. Add tests or roll back the supplement recommendability widening.
5. Keep mini-app output placeholder-only.
6. Produce one fresh runtime or QA artifact after the safety-sensitive path is verified.

## 2026-05-13 Delta

What changed:

- keep the May 12 priorities, but remove disk recovery from the lead slot
- keep the governing blocked `week` case as the center of truth
- keep the fresh paid `premium` branch as the main unresolved monetization ambiguity
- elevate the voice/audio shutdown in `WellnessBot/main.py` into an explicit product decision instead of leaving it as silent drift
- refuse to count OCR and supplement-catalog relaxations as progress until they have tests or rollback decisions
- refuse to count connector refresh or new strategy packet churn as sprint progress before one fresh proof artifact exists

Next 12h command set:

1. Prove the delivery gate with replayable smoke or regression coverage.
2. Record the explicit relation for `20260505T131604Z_1084557944`.
3. Decide `restore` vs `retire-and-document` for voice/audio intake.
4. Tighten or roll back OCR and supplement-catalog relaxations until safe tests exist.
5. Keep mini-app output placeholder-only.
6. Produce one fresh runtime or QA artifact after the safety-sensitive path is verified.

## P0. Delivery Gate Verification And Governing Case Recovery

Owner:

- Lead Developer
- Quality Auditor
- Operator

Task:

- treat the delivery gate as partly repaired, then prove it and normalize the blocked governing case

Concrete changes:

- use `20260501T162705Z_1084557944` as the governing case:
  - `intake_status = delivery_blocked_needs_revision`
  - `judge_verdict = needs_revision`
  - `delivery_blocked_at = 2026-05-11T06:56:00Z`
- verify that the new blocked state is code-enforced, not a one-off data correction
- add or confirm a replayable smoke for:
  - `needs_revision`
  - `must_rewrite_with_high_caution`
  - explicit manual override path if it exists
- decide what operator correction is required on the governing `week` case before it can be treated as a live proof story

Done when:

- delivery cannot silently outrun review truth
- blocked delivery states are auditable from artifacts
- the governing `week` case has an explicit recovery path rather than a contradictory state

## P0. Canonical Same-User Commercial Path

Owner:

- Operator
- Product Strategist
- Lead Developer

Task:

- finish reducing user `1084557944` to one canonical paid path

Concrete changes:

- treat the current stack as:
  - `20260501T162705Z_1084557944` = governing blocked `week`
  - `20260505T131604Z_1084557944` = fresh paid `premium`, operationally parked until explicit merge
  - `20260427T173913Z_1084557944` = archived test run
  - `20260425T214914Z_1084557944` = archived test run
  - `20260425T212847Z_1084557944` = archived test run
- record one explicit relation for `20260505T131604Z_1084557944`:
  - `merge-into-canonical`
  - or parked non-canonical premium branch
- until that relation is written into artifacts, do not count the paid `premium` branch as commercial proof
- stop describing the three archived branches as active blockers
- stop letting the fresh premium case float without canonical ownership

Done when:

- one user has one canonical commercial path
- the fresh paid premium case has an explicit relation to the canonical thread
- the archived branches are no longer part of the live commercial narrative

## P0. Lab Parsing And Supplement Safety

Owner:

- Lead Developer
- Quality Auditor

Task:

- stop unsafe parsing and unsafe supplement expansion from becoming product truth

Concrete changes:

- treat the governing `week` case artifact as proof that current lab truth is still unsafe:
  - `lab_quality_check.status = missing`
  - `requires_lab_resubmission = true`
  - parsed biomarker set still contains polluted narrative/protocol-like lines
- inspect current uncommitted `WellnessBot/lab_ocr.py`:
  - alias gate loosened
  - broader line acceptance introduced
- inspect current uncommitted `WellnessBot/supplement_product_catalog.py`:
  - discontinued / previously blocked items become recommendable again
- do not ship those relaxations on trust alone
- either:
  - add tests that prove the broader behavior is still safe
  - or tighten/roll back the relaxations
- keep real lab fallback proof requirement unchanged:
  - text PDF
  - readable photo
  - poor photo
  - structured manual biomarker text

Done when:

- polluted OCR/manual-text lines cannot silently become biomarkers
- unsafe supplement recommendability drift is blocked
- file/lab behavior is described from tests or replayable verification, not intention

## P0. Intake Modality Truth

Owner:

- Lead Developer
- Product Strategist

Task:

- stop silent product-scope drift around voice and audio intake

Concrete changes:

- inspect current uncommitted `WellnessBot/main.py`:
  - voice messages now return `Голосовые сообщения отключены`
  - audio uploads no longer have a handler
- decide one explicit pilot rule:
  - restore a safe STT path
  - or retire voice/audio from the active pilot and update product/docs accordingly
- do not leave the repo in a mixed state where Telegram-first messaging implies broad intake support while runtime silently rejects it

Done when:

- voice/audio behavior matches the documented pilot scope
- contributors can tell whether STT is active, intentionally retired, or blocked behind a known follow-up

## P0. Runtime Instance Control And Health Truth

Owner:

- Ops
- Lead Developer

Task:

- stop duplicate polling and turn runtime health into one explicit current truth

Concrete changes:

- treat the latest runtime log as the governing ops artifact:
  - proxy logged at startup is `http://127.0.0.1:10808`
  - polling hits repeated `TelegramConflictError`
  - local `GET /health` still returns `404`
- decide which bot instance is canonical and stop the extra poller
- decide whether proxy is required and document the real endpoint rather than narrating stale `127.0.0.1:12334` assumptions
- capture one clean post-fix runtime artifact:
  - single-instance polling
  - explicit health path
  - no ambiguity about proxy dependency

Done when:

- exactly one bot instance is polling
- the docs match the real proxy/health path
- one fresh runtime artifact proves the current path instead of inferring it from stale logs

## P0. Mini-App Placeholder Finish

Owner:

- Frontend / Lead Developer
- Product Strategist

Task:

- finish neutralizing the mini-app result surface

Concrete changes:

- count the current working-tree improvement as partial progress:
  - `2990` removed
  - `Premium Wellness-Досье` removed
  - `Vitamin D3` / `LCHF` demo content removed
- remove the remaining protocol-style promise:
  - `Персональный протокол питания и нутрицевтиков`
- keep the result surface at:
  - safe placeholder
  - or reviewed backend-fed content only

Done when:

- mini-app no longer implies a reviewed personalized protocol before backend truth exists
- Telegram-first reviewed truth and mini-app surface tell the same story

## P0. Runtime Proxy Truth

Owner:

- Ops
- Lead Developer

Task:

- stop treating the May 7 restart as proof of runtime resilience

Concrete changes:

- current visible runtime truth remains:
  - `proxy=http://127.0.0.1:12334`
  - `GET /health -> 404` at `2026-05-08 00:35:06 +0300`
- verify whether polling truly requires the local proxy
- if proxy is optional, document and prefer a no-proxy fallback path
- if proxy is required, treat proxy availability as a first-class dependency with an observable health signal
- produce one clean post-fix verification artifact before calling runtime stable

Done when:

- the team knows whether proxy is required or optional
- runtime health is observable without inference from reconnect
- one clean verification pass exists after the May 7 restart baseline

## P1. Model-Path Discipline

Owner:

- Lead Developer
- Quality Auditor

Task:

- improve live-model response discipline without undoing model reach

Concrete changes:

- keep `docs/WELLNESS_DIALOGUE_QA_20260506.md` as the current QA source of truth
- preserve:
  - `11/20` deterministic
  - `9/20` model-path
- fix:
  - `6/9` clarifying-question coverage
  - invented names appearing twice
  - `5/9` replies longer than `2000` characters
  - duplicated emergency templates on prompts `17` and `18`
- rerun the benchmark only after delivery, parser/catalog, mini-app, and runtime fixes land

Done when:

- model reach is preserved
- unsupported personalization is reduced
- benchmark evidence shows cleaner model-path discipline

## P0. Execution Loop Compression

Owner:

- Quality Auditor
- Lead Developer

Task:

- stop repeating stale May 8 blocker language when the live artifacts have changed

Concrete changes:

- stop writing docs as if the governing `week` case were still silently delivered
- stop writing docs as if the three archived test-run branches were still active
- stop reusing stale governance metrics like `4` duplicate groups / `x8` largest duplicate group when current `product_governance.json` no longer exposes that structure
- keep using the live loop signals that still exist:
  - `127` experiments
  - `29` `docs/tasks/HERMES-20260505-*` files
  - no newer benchmark after `2026-05-06`
  - no newer runtime verification after `2026-05-08`
  - safety-sensitive working-tree diffs without proof artifacts
- freeze new strategy/task packet churn unless it lands:
  - governing-case recovery
  - premium-path ownership
  - parser/catalog safety
  - mini-app neutralization
  - proxy/health proof

Done when:

- the next artifact after this board is a direct fix or verification result, not another stale restatement
- documentation reflects live truth instead of preserving outdated blocker language

## Stop List

Blocked for now:

- treating the governing `week` case as solved just because it is no longer marked delivered
- letting `20260505T131604Z_1084557944` remain a floating second commercial story
- reviving the three archived test runs into the live narrative
- shipping broadened OCR parsing without tests
- shipping broadened supplement recommendability without safety review
- showing protocol-style result promises on the mini-app placeholder
- calling runtime stable while polling still depends on an unverified proxy path
- rerunning the benchmark before parser/catalog, mini-app, and runtime truth are repaired
- starting Telegram Payments/YooKassa migration, PostgreSQL migration, Docker deployment, or new admin/WebApp work on the pilot critical path

## Loop Risk

Repeated low-impact tasks to stop:

- rereading the same QA and runtime evidence without producing a new verification artifact
- keeping old blocker text alive after the underlying case statuses already changed
- treating uncommitted safety-sensitive diffs as progress without proof
- generating more task packets while `29` same-day HERMES drafts already exist
- debating premium growth before the fresh premium branch has a canonical relation
- allowing renamed package-first tiers to keep creating new same-user paid branches before the first broken paid case is resolved

Replacement action:

- ship one bounded acceptance packet:
  1. lock proxy policy
  2. replay one paid case on the current code
  3. classify both fresh `20260530` branches
  4. collapse pricing truth to one ladder
  5. prove delivery again before another planning loop

## Next 12h Command Set

1. Add or verify the replayable smoke that blocks delivery for `needs_revision` and `must_rewrite_with_high_caution`.
2. Record whether the governing blocked `week` case needs rewrite, clarification follow-up, or explicit operator downgrade before reuse.
3. Reconcile the governing case so `lab_quality_check`, `requires_lab_resubmission`, follow-up files, and parsed biomarkers tell one coherent story.
4. Explicitly classify `20260505T131604Z_1084557944` as `merge-into-canonical` or parked non-canonical premium branch.
5. Keep the three `archived_test_run` branches archived and out of the live product story.
6. Audit the current `WellnessBot/lab_ocr.py` relaxation against polluted biomarker lines already visible in the governing case artifact.
7. Add tests or tighten the parser so narrative/protocol lines cannot become biomarker facts.
8. Audit the current `WellnessBot/supplement_product_catalog.py` relaxation and restore conservative recommendability if tests do not justify it.
9. Remove the remaining protocol-style promise from `mini-app/index.html`.
10. Decide whether bot polling truly depends on `127.0.0.1:12334`.
11. Explain or fix the current `GET /health -> 404` behavior and document the real runtime health check.
12. Produce one clean runtime verification artifact after the chosen proxy policy is applied.
13. Extend `sanitize_live_reply()` and benchmark checks for invented names, over-familiar tone, duplicated emergency templates, and overlong first-touch replies.
14. Rerun the quality benchmark only after steps `1-13` land.
15. Keep Telegram-first operations and manual concierge payment; do not let any price ladder be treated as official until one approved map is written everywhere.
