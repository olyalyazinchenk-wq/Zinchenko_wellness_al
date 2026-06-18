# Agent Context Hub

Updated: 2026-06-18 21:50 MSK

## ⚠️ ВСЕМ АГЕНТАМ (Codex / Antigravity / Hermes): ЧИТАТЬ ПЕРВЫМ ДЕЛОМ

Эта страница — единственный общий источник правды для всех агентов проекта.
Если документы противоречат друг другу, приоритет у более свежего. Медицинско-юридические ограничения имеют приоритет всегда.

## Unified GitHub Source Of Truth

- Main public handoff document: `docs/PROJECT_DEVELOPMENT_SINGLE_SOURCE_OF_TRUTH.md`
- Live repo: `olyalyazinchenk-wq/Zinchenko_wellness_al`
- Active remote branch for current working truth: `origin/master` at `fe31aec`
- GitHub default branch: `master`
- Local workspace: `C:\Users\HP\Desktop\Новая папка`

## Unified Agent Runtime

- Shared stage marker: `docs/CURRENT_STAGE.json`
- Shared bootstrap: root `AGENTS.md`
- Shared verification: `ops/agent-sync-status.ps1`
- Codex and Antigravity must open the Windows canonical workspace above.
- Hermes must use `/mnt/c/Users/HP/Desktop/Новая папка` and must not run the
  legacy `/home/hermes/projects/nutrition_bot` polling process.
- The only Telegram polling owner is the Windows scheduled task `WellnessBot`.

## Quick Status

- Mode: controlled concierge pilot. Public launch remains blocked.
- Payment mode: `PAYMENT_MODE=manual`. Human review is required before delivery.
- Bot is live:
  - parent PID `15420` = `.venv\Scripts\python.exe`
  - child PID `6760` = `Python312\python.exe`
  - startup `2026-06-18 15:04:39 -> 15:04:40 +03:00`
  - DeepSeek `200 OK` and handled updates continue through `2026-06-18 15:20:03 +03:00`
  - proxy is explicit: `http://127.0.0.1:10808`
- Active runtime rail: `20260618T121906Z_1084557944` -> `nutri_chat` -> `paid_nutri_chat` -> expires `2026-06-20T12:19:14.119781+00:00`
- Disk state: `C:` free space is only `7014158336` bytes (`~6.53 GiB`) at `2026-06-18 16:35:14 +03:00`
- Benchmark anchor: `ops/reports/quality_report_20260531T083403Z.md`
- QA interpretation anchor: `docs/WELLNESS_DIALOGUE_QA_20260608.md`
- Connector state:
  - GitHub: recovered
  - Notion: recovered
  - Google Drive: blocked because file discovery/create/upload/share tools are not exposed

## What Changed Since June 14

### Runtime And Payment Flow
- The active runtime truth is no longer the June 6 `habits` rail; it is now the June 18 paid `nutri_chat` rail.
- Live runtime proof is current again, not historical-only: June 18 startup, polling, handled updates, and DeepSeek responses are all present in `bot.stderr.log`.
- Payment-confirmation and reminder logic added earlier on June 18 is now part of the live operating context and should be treated as shipped behavior.

### Connector Reality
- Notion is no longer blocked in this session; `_notion_get_users { user_id: "self" }` succeeded.
- GitHub is no longer blocked in this session; the repo resolves through the GitHub connector and `git ls-remote --heads origin` confirms both `main` and `master`.
- Google Drive is still blocked because no write-capable Drive tools are exposed in-session.

### External Contributor Entry
- GitHub now opens on `master`, the same branch used by the live workspace.
- Historical `main` remains non-canonical and is not an implementation source.

## Current Truth

### Runtime
- `WellnessBot/data/runtime_state.json` currently uses `user_sessions` plus `chat_sessions`.
- Active `user_sessions[1084557944]` truth:
  - `submission_id = 20260618T121906Z_1084557944`
  - `offer = nutri_chat`
  - `tier = nutri_chat`
  - `step = paid_nutri_chat`
  - `consent_given = true`
  - `nutri_chat_started_at = 2026-06-18T12:19:14Z`
  - `nutri_chat_expires_at = 2026-06-20T12:19:14.119781+00:00`
- `chat_sessions[1084557944]` already contains live paid-dialogue context.
- The current parent-child Python chain is real runtime proof, but the intended supervision topology still should be documented explicitly.

### Same-User Paid-State Conflict
- One Telegram user still holds unresolved paid state across all of these rails:
  - `20260602T055745Z_1084557944` = `nutri_chat`, `500 RUB`
  - `20260603T112723Z_1084557944` = `nutri_chat`, `500 RUB`
  - `20260603T113045Z_1084557944` = `habits`, `6900 RUB`
  - `20260603T121917Z_1084557944` = `nutri_chat`, `300 RUB`
  - `20260606T202509Z_1084557944` = `habits`, `6900 RUB`
  - `20260618T121906Z_1084557944` = `nutri_chat`, `1490 RUB`, mounted as active rail
- Every item above still has `canonical_path = null` and `case_relation = null`.

### Delivery Truth
- `WellnessBot/data/submissions/20260531T183007Z_1084557944.json` still combines:
  - `offer = basic`
  - `payment_status = paid`
  - `intake_status = delivered_to_client`
  - `internal_review.judge_verdict = fail_major_issues`
- This remains a P0 delivery-gate breach until a valid override or remediation is recorded.

### Benchmark And Governance
- Latest completed benchmark reference is still `ops/reports/quality_report_20260531T083403Z.md`.
- Current QA synthesis doc is still `docs/WELLNESS_DIALOGUE_QA_20260608.md`.
- Full batch still aborts on prompt `1`.
- `WellnessBot/data/product_governance.json` still holds `151` experiments and `0` decisions with `updated_at = 2026-06-01T20:55:21Z`.

### Public Surface Truth
- `landing/index.html` remains the comparatively safest surface.
- Root `index.html` still contains live payment/PDF/price claims that outrun the approved pilot.
- `mini-app/index.html` still promises dossier/PDF/support outcomes and cannot be described as placeholder-only.

### Connector Truth
- GitHub success probes:
  - GitHub connector resolved `olyalyazinchenk-wq/Zinchenko_wellness_al`
  - `git ls-remote --heads origin` returned both `main` and `master`
- Notion success probes:
  - `_notion_get_users { user_id: "self" }`
  - `_search` resolved `AGENT CONTEXT HUB — Antigravity / Wellness`
- Google Drive block:
  - file discovery/create/upload/share tools are not exposed
  - exact access request: `enable the Google Drive connector with file discovery/create/upload/share permissions in this Codex session`

## Regressions To Fix Now

- Disk floor breach; owner `Ops`; next action remove or archive large user-owned installers/videos/archives until `C:` is back above `10 GiB`.
- Same-user paid-path sprawl; owner `Operator + Lead Developer`; next action declare one canonical current path across the June 2 / June 3 / June 6 / June 18 stack, then freeze, archive, merge, or refund the non-canonical rails.
- Duplicate same-offer `habits` multiplication; owner `Operator + Lead Developer`; next action choose the canonical `habits` path between `20260603T113045Z_1084557944` and `20260606T202509Z_1084557944`.
- Delivery-gate breach; owner `Lead Developer + Operator`; next action audit `20260531T183007Z_1084557944` and remove or remediate `delivered_to_client` if no valid override exists.
- Root-page commercialization overclaim; owner `Product Strategist + Lead Developer`; next action remove or neutralize live payment, PDF, and price claims in `index.html`.
- Mini-app commercialization overclaim; owner `Product Strategist + Lead Developer`; next action remove or neutralize dossier/PDF/support promises until the governed ladder is explicit.
- GitHub default-branch drift; owner `Lead Developer + Tooling`; next action align or merge `main` with the live `master` branch so external contributors do not land on stale truth by default.
- Google Drive connector gap; owner `Tooling / Access`; next action expose file discovery/create/upload/share tools before the next Drive sync attempt.

## Plan Delta

1. Keep local docs authoritative first.
2. Use recovered Notion and GitHub connectors in the same cycle when real probes succeed.
3. Treat Google Drive as the only outward-sync blocker in the current session.
4. Move disk recovery back to the top operational priority.
5. Add GitHub default-branch alignment to the execution packet because stale `main` now affects external onboarding.

## Strategy Delta

- Strategy is now `use recovered connectors to keep management truth current while fixing execution integrity`.
- The lead execution-credibility gap is a six-part bundle:
  - disk remains below floor
  - same-user paid ownership is unresolved
  - delivered-case contradiction remains open
  - root and mini-app still overclaim
  - Google Drive sync is still absent
  - GitHub default branch is stale relative to the live branch

## Goals Delta

- Goal 1: restore `C:` above the `10 GiB` floor and rebuild a safer margin.
- Goal 2: collapse the same-user paid stack into one canonical path.
- Goal 3: block same-user same-offer and same-ladder duplicate paid creation.
- Goal 4: repair the delivered-case contradiction before higher-ticket proof is treated as valid.
- Goal 5: remove root and mini-app commercialization overclaims.
- Goal 6: align GitHub default-branch truth with the live branch.
- Goal 7: keep Notion and GitHub status mirrors current while Google Drive remains blocked.

## Next 12h Priorities

1. Push `C:` back above `10 GiB`.
2. Canonicalize the June 2 / June 3 / June 6 / June 18 same-user paid stack.
3. Add a hard duplicate paid-branch guard.
4. Repair `20260531T183007Z_1084557944`.
5. Remove root and mini-app overclaims.
6. Align `main` and `master` or make one default branch authoritative.
7. Keep Notion and GitHub context mirrors current without publishing runtime/PII artifacts.
8. Enable Google Drive file discovery/create/upload/share permissions.

## Must-Not-Change Rules

- Telegram-first only.
- Manual concierge remains the official pilot mode.
- No price ladder becomes product truth until one approved map is written across code, docs, and artifacts.
- One canonical paid path per Telegram user at a time.
- No second paid branch for the same offer or same ladder and same user while an older paid path is still active or unresolved.
- Human review is required before delivery.
- No diagnosis or treatment framing.
- No unsafe supplement instructions without confirmed context and review.
- No hardcoded medical-style results on public or TMA surfaces.
- Do not describe the mini-app as placeholder-only while price, PDF, or support promises remain live in the file.
- Do not count a paid path as healthy if payment succeeded but the final reviewed artifact is contradicted by failing review state.
- Do not treat governance backlog growth as execution progress.
- Do not mark Notion or GitHub sync as healthy until a real connector call succeeds in the current session.
- Do not treat Google Drive as available until file discovery/create/upload/share tools are actually exposed.
- Do not present GitHub default `main` as the live source of truth while `master` remains the current execution branch.

## Context For New Model

### Stage
- Controlled Telegram concierge pilot with live runtime, recovered Notion/GitHub sync, stale Google Drive exposure, and unresolved execution-control debt.

### Objective
- Restore disk headroom.
- Collapse the same-user paid stack to one canonical path.
- Repair the delivered-case contradiction.
- Neutralize root and mini-app overclaims.
- Align external repo truth with the live branch.
- Keep Notion and GitHub mirrors current while Google Drive remains blocked.

### Constraints
- Telegram-first only.
- `PAYMENT_MODE=manual`.
- Human review remains mandatory before delivery.
- One canonical commercial path per Telegram user.
- Latest completed benchmark reference is `ops/reports/quality_report_20260531T083403Z.md`.
- Current QA interpretation is `docs/WELLNESS_DIALOGUE_QA_20260608.md`.
- Full batch still aborts on prompt `1`.
- `C:` free space is only `7014158336` bytes (`~6.53 GiB`) at `2026-06-18 16:35:14 +03:00`.
- Google Drive file discovery/create/upload/share tools are unavailable in this session.

### Immediate Next Actions
1. Recover disk margin.
2. Canonicalize the paid stack.
3. Block further duplicate paid creation.
4. Repair the delivered-case contradiction.
5. Remove root and mini-app overclaims.
6. Align GitHub default-branch truth.
7. Keep Notion/GitHub mirrors current and request Google Drive access.
