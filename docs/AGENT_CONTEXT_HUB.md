# Agent Context Hub

Updated: 2026-05-08 16:40 MSK

## Unified GitHub Source Of Truth

- Main public handoff document: `docs/PROJECT_DEVELOPMENT_SINGLE_SOURCE_OF_TRUTH.md`
- Use the local hub files for live operating truth and `docs/external_sync/*.md` as the sanitized outward-sync fallback while external connectors are blocked.

## Quick Status

- Mode: controlled concierge pilot. Public launch remains blocked.
- Payment mode: `PAYMENT_MODE=manual`. Human review is still required before delivery.
- Official pilot prices remain `3900 / 6900 / 14900 RUB`.
- Top product-truth defect: the `week` case `20260501T162705Z_1084557944` still shows `delivered_to_client` even though its attached review verdict is `needs_revision`, and no explicit override note is recorded.
- New commercial regression: a second paid path now exists for the same user:
  - `20260505T131604Z_1084557944`
  - offer `premium`
  - `manual_payment_confirmed`
  - `intake_status = review_priority_quality_and_market`
  - `judge_verdict = pass_with_minor_edits`
- `WellnessBot/data/runtime_state.json` is empty, so runtime/storage mismatch is not the active blocker.
- OCR auth path is still partially cleared:
  - `docs/OCR_PREFLIGHT_STATUS_20260506.md` records the earlier `401`
  - the safe preflight now returns `auth_path_ok` with `400` on a synthetic `1x1 PNG`
  - real PDF/photo/manual-text verification is still pending
- Manual lab-entry fallback is now a real coded affordance:
  - commit `176ac82` improves file-resubmission and typed-lab rewrite guidance
  - commit `fe7a358` adds a manual-entry button in the labs flow and stronger typed-lab instructions
  - this is still unproven end-to-end on a reviewed live case
- Bot runtime is evidenced as running again:
  - `bot.stderr.log` shows a fresh start at `2026-05-07 23:46:49 MSK`
  - polling started at `2026-05-07 23:46:49-23:46:50 MSK`
  - TMA server started at `http://localhost:8000`
  - proxy is configured as `http://127.0.0.1:12334`
  - `GET /health` returned `404` at `2026-05-08 00:35:06 +0300`
  - the active path is still unproven because no clean no-proxy fallback verification exists yet
- Repo state: latest local commit is `fe7a358` (`feat: guide manual lab entry`); local branch is ahead of `origin/master` and has docs-only status refresh pending sync.
- New QA artifact present for review/sync (internal only, no client data): `docs/WELLNESS_DIALOGUE_QA_20260506.md`.
- External sync surface:
  - Obsidian local mirror is available
  - Notion connector status: blocked
  - GitHub sync status: available (remote reachable); docs sync pending push
  - Google Drive upload/share tools are unavailable in the current session
- Latest QA / benchmark reference is now `2026-05-06`, not `2026-05-01`:
  - `20/20` non-empty replies
  - `11/20` deterministic replies
  - `9/20` model-handled replies
  - clarifying questions in `6/9` model-handled symptom prompts
  - invented names in `2` prompts
  - `5/9` model-path replies longer than `2000` characters

## Кратко (RU)

- Режим: controlled concierge pilot; публичный запуск заблокирован до отдельного решения.
- Оплата: активный пилот `PAYMENT_MODE=manual`; human review обязателен перед выдачей клиенту.
- Текущее состояние: бот и проект функционально «живы», но продуктовая правда (delivery gate + канонический кейс на пользователя) остаётся нестабильной.
- Главный дефект: кейс `20260501T162705Z_1084557944` отмечен как `delivered_to_client`, при этом внутренний вердикт `needs_revision` и нет явной записи override.
- Коммерческий риск: у одного пользователя зафиксированы параллельные платные ветки (`week` и `premium`), нужно свести к одному каноническому пути.
- Качество ответов: на ветке модели сохраняются выдуманные имена/обращения и «полированная ложная точность»; QA отчёт за 2026-05-06 актуализирован.
- Внешняя синхронизация: GitHub remote сейчас доступен; Notion всё ещё под вопросом; Google Drive в Codex-сессии недоступен.

## Stage

- controlled concierge pilot with validated paid `week` demand, validated paid `premium` demand, restored live-model reach, runtime up again, and manual-lab fallback now present in code, but unstable delivery-gate integrity, same-user case ownership, mini-app truth, polling resilience, end-to-end file-fallback proof, and connector availability

## Done

- `week` is still validated as a paid entry rail because `20260501T162705Z_1084557944` reached payment, delivery, and follow-up.
- Paid `premium` demand is also now validated:
  - `20260505T131604Z_1084557944` reached payment confirmation
  - this is commercial proof, but not coherent path proof
- Runtime-state mismatch is still cleared:
  - `WellnessBot/data/runtime_state.json` is empty
  - there is no active runtime-only session drift
- Router overreach is no longer the main quality blocker:
  - benchmark held at `9/20` model-handled replies
- OCR auth path is still recovered as an environment issue:
  - safe preflight moved from `401` to `auth_path_ok`
  - Yandex IAM token was refreshed earlier
- Deterministic biomarker alias coverage was expanded safely for standard lab groups.
- Manual lab-entry UX is now landed in code:
  - typed biomarker examples are shown
  - a manual-entry button exists in the labs step
  - malformed typed biomarker text now gets a rewrite prompt
- Governance pressure is still high:
  - `127` experiments
  - `4` duplicate title groups
  - largest duplicate group `x8`

## Objective

- restore delivery truth
- normalize the active `week` follow-up state
- collapse the same-user `week`/`premium` sprawl into one canonical path
- prove manual PDF/photo/typed-lab fallback behavior end-to-end
- remove unsafe hardcoded result content from TMA/mini-app surfaces
- prove the currently running polling path before calling runtime healthy again
- compress execution loops so task/report generation stops outrunning live fixes
- restore external connector sync

## Product Direction

- Telegram-first only
- service ladder remains:
  - `demo` builds trust
  - `week` is the validated paid entry rail
  - `premium` remains the flagship offer
  - `vip` stays parked until operator-load evidence exists
- official pilot payment mode: `PAYMENT_MODE=manual`
- human review is mandatory before any client delivery
- premium should be expressed as a same-case upgrade from fresh post-`week` evidence, not as a separate parallel case for the same user
- manual lab entry is now an allowed fallback path, but only when the input is structured clearly enough to avoid fact confusion

## Current Truth

- `WellnessBot/data/runtime_state.json` is empty.
- The current governing case is:
  - `WellnessBot/data/submissions/20260501T162705Z_1084557944.json`
  - offer: `week`
  - payment confirmed
  - status: `delivered_to_client`
  - follow-up already started after delivery
  - internal review on the same case still says `needs_revision`
  - no explicit delivery override note is present
  - lab state is still unresolved:
    - `lab_quality_check.status = missing`
    - `requires_lab_resubmission = true`
  - fresh follow-up artifacts arrived on `2026-05-05`
  - latest follow-up currently recorded is `2026-05-07T20:46:50Z`
- The same user also has four non-canonical branches:
  - `20260505T131604Z_1084557944` = fresh paid `premium` branch with `pass_with_minor_edits`, but unclear relation to the canonical `week` path
  - `20260427T173913Z_1084557944` = stale `week` placeholder at `consent_pending`
  - `20260425T214914Z_1084557944` = evidence-only premium branch because `requires_lab_resubmission = true`
  - `20260425T212847Z_1084557944` = parked rewrite-only premium branch with `must_rewrite_with_high_caution`
- Landing still matches the Telegram-first funnel.
- Mini-app still drifts from backend truth:
  - hardcoded `Premium Wellness-Досье` result screen
  - hardcoded `Витамин D3: 5000 МЕ + K2`
  - hardcoded `LCHF`
- File/lab truth is improved but still incomplete:
  - OCR auth is no longer failing on the safe preflight path
  - manual typed-lab input is now a product affordance
  - real PDF/photo/manual-text verification is still not proven
  - DeepSeek biomarker extraction is explicitly candidate-only, not a fact source
- Latest QA synthesis:
  - router overreach is no longer the main blocker
  - current live quality risks are invented personalization, duplicated emergency templates, overlong first-touch replies, and false specificity
  - current QA reference is `docs/WELLNESS_DIALOGUE_QA_20260506.md`, not the May 1 report
- Current runtime evidence is mixed rather than absent:
  - the leading unresolved outage window still exists in the history at `2026-05-03 14:20:44-14:30:12 MSK`
  - a clean restart occurred on `2026-05-07 23:46:49-23:46:50 MSK`
  - the bot is currently up again
  - the stable-vs-fragile transport question is still open because the active path uses the same local proxy
  - current health signaling is incomplete because `/health` returned `404`
- Current external-sync evidence:
  - Notion is blocked
  - GitHub is blocked / remote currently unreachable
  - Google Drive file create/upload/share tools are unavailable in this session

## Regressions To Fix Now

- Delivery gate bypass:
  - delivered `week` case despite unresolved internal-review verdict
- Same-user paid-path drift worsened:
  - one delivered `week` case
  - one fresh paid `premium` case
  - one stale `week` placeholder
  - two older `premium` branches
- Governing-case lab-state mismatch:
  - the same `week` case still requires lab resubmission while follow-up activity keeps accumulating
- Manual-lab proof gap:
  - fallback UX exists, but there is still no end-to-end reviewed proof artifact
- Mini-app result-surface drift:
  - hardcoded supplement/diet result content
- Runtime resilience regression:
  - the bot is back up, but the active path still depends on `127.0.0.1:12334` and `/health` is not wired cleanly
- External connector outage:
  - Notion and GitHub are blocked
  - Google Drive upload/share remains unavailable
- Execution diffusion / draft swarm:
  - `127` experiments
  - duplicate-title pressure at `x8`
  - `29` same-day HERMES task or draft files
- Model-path response discipline:
  - invented names
  - duplicated emergency handling
  - overlong first-touch replies
  - early diagnosis-like language pressure

## Next

1. Enforce a hard delivery gate between internal review and client delivery.
2. Normalize the governing `week` case so lab state and follow-up state match the latest truth.
3. Record whether the current delivered `week` case needs correction before more follow-up output is treated as proof.
4. Explicitly classify `20260505T131604Z_1084557944` as either merge-into-canonical premium continuation or frozen non-canonical premium branch.
5. Keep the fresh follow-up uploads on the same canonical case; do not let a second active same-user paid story persist.
6. Run real file/lab verification on a text PDF, a readable photo, a poor photo, and structured manual biomarker text.
7. Add or extend tests around the new manual-entry button and rewrite prompt behavior.
8. Replace unsafe mini-app result demo content with a safe placeholder or reviewed backend-fed state.
9. Prove whether the currently running polling path is proxy-backed or no-proxy, and fix or document the `/health` check.
10. Tighten live-answer sanitization and benchmark assertions around invented personalization, duplicated emergency templates, false specificity, and overlong replies.
11. Restore Notion, GitHub, and Google Drive availability, then replay the pending outward-sync artifacts from `docs/external_sync/`.

## Must-Not-Change Rules

- Telegram-first only
- manual concierge remains the official pilot mode
- official pilot prices stay `3900 / 6900 / 14900 RUB`
- one canonical paid path per Telegram user at a time
- human review required before delivery
- no diagnosis or treatment framing
- no unsafe supplement instructions without confirmed context and review
- no hardcoded medical-style or supplement-style demo results on TMA or public-facing surfaces
- do not treat a delivered status as trustworthy if the internal-review verdict still demands revision
- do not let `20260505T131604Z_1084557944` remain a silent second active paid path
- do not treat the clean `2026-05-07` restart as proof that polling resilience is fixed
- do not call polling resilience fixed before one clean post-fix verification passes
- do not treat OCR auth recovery or manual-lab UX landing as proof that file/lab reliability is solved
- do not use AI-assisted biomarker extraction as a fact source without confidence, merge, and audit controls
- do not accept malformed typed biomarker text as confirmed evidence
- do not let task/report generation outrun delivery safety, runtime health, manual-fallback proof, and canonical state truth

## Context For New Model

Stage:

- controlled concierge pilot with validated paid `week` demand, validated paid `premium` demand, restored live-model reach, runtime up again, and manual-lab fallback now present in code, but unstable delivery-gate integrity, same-user case ownership, mini-app truth, polling resilience, end-to-end file-fallback proof, and connector availability

Done:

- `week` demand validated
- `premium` willingness to pay validated
- runtime-state mismatch cleared
- OCR auth path recovered
- manual typed-lab fallback landed in code
- router/model split held at `11/20` deterministic and `9/20` model-path

Next:

- enforce delivery truth
- collapse same-user path sprawl
- prove manual-lab fallback end-to-end
- remove hardcoded mini-app result content
- prove or replace the current proxy-backed runtime path

Must-Not-Change Rules:

- Telegram-first only
- manual concierge only
- official prices `3900 / 6900 / 14900 RUB`
- human review before delivery
- one canonical paid path per user
- no second active same-user paid storyline
- no diagnosis/treatment framing
- no hardcoded supplement or protocol output on surfaces
- no claiming file reliability is solved before PDF/photo/manual-text proof exists

Immediate next actions:

1. Add or verify a guard so unresolved internal-review verdicts cannot move to `delivered_to_client` without an explicit manual override record.
2. Normalize `20260501T162705Z_1084557944` so its lab state matches the latest follow-up truth.
3. Decide how `20260505T131604Z_1084557944` relates to the canonical `week` path and stop same-user commercial ambiguity.
4. Run real file verification on a text PDF, a readable photo, a poor photo, and structured manual biomarker text; confirm safe fallback if OCR or typed input is weak.
5. Add or extend tests around the new manual-lab button and rewrite prompt behavior.
6. Remove the hardcoded mini-app `Premium Wellness-Досье` result demo and replace it with a safe placeholder or reviewed backend-fed state.
7. Verify the proxy dependency on `127.0.0.1:12334` from the current running baseline and fix or document the `/health` check.
8. Tighten `sanitize_live_reply()` and benchmark assertions for invented names, duplicated emergency templates, false specificity, and overlong first-touch replies.
9. Restore Notion, GitHub, and Google Drive availability, then replay pending outward-sync artifacts.

Reference benchmark:

- `ops/reports/quality_report_20260506T080435Z.md`
- QA synthesis: `docs/WELLNESS_DIALOGUE_QA_20260506.md`
- current truth: `20/20` non-empty, `11/20` deterministic, `9/20` model-handled, `6/9` clarifying-question coverage on model-handled symptom prompts
