# NutriOK Build Status - 2026-07-17

## Current Stage

`nutriok-controlled-build-2026-07-17-r1`; public launch blocked.

## Working-Tree Truth

- Canonical brand and product ladder implemented locally.
- Deterministic delivery gate prevents full-tier direct delivery and holds red flags, unsafe claims, and supplement offers.
- Legacy offer codes map to the new product model so persisted cases are not orphaned.
- Bot menu, root site, landing, and mini-app prototype are aligned.
- 63 unit tests pass; bot process was not started.

## Release Blockers

- Scheduled task has no active bot process after Telegram connectivity failures.
- Structured primary goal/baseline/three-day diary is not yet persisted end to end in the live bot.
- Latest completed benchmark is `ops/reports/quality_report_20260531T083403Z.md` and predates NutriOK.
- RF cloud privacy/storage controls and production payments are incomplete.
- Disk is about 4.31 GiB free, below the 10 GiB floor.

## Contributor Entry Point

Read `docs/NUTRIOK_PRODUCT_CONTRACT_20260717.md`, `docs/CURRENT_STAGE.json`, and `docs/AGENT_CONTEXT_HUB.md`.
The first file is currently local working-tree truth and is not yet published with the implementation.
Do not start Telegram polling outside the Windows scheduled task.