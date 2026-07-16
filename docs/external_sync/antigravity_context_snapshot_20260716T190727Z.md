# Antigravity Context Snapshot - 2026-07-16T19:07:27Z

## Project State

- Stage: `controlled-concierge-pilot-2026-06-18-r1`.
- Canonical workspace: `C:\Users\HP\Desktop\Новая папка`.
- Canonical branch: `master`.
- Local and remote head: `2968cdba9a77164b8bc0f4426de7affbcb5d5f8e`.
- Working tree: 20 tracked dirty files; current behavior is not fully represented on GitHub.
- Runtime: scheduled task `Ready`, bot processes `0`; last start failed on 2026-07-01 due Telegram network/proxy connectivity.
- Storage: 5,018,693,632 bytes free on `C:`; below the 10 GiB floor.
- Benchmark: `ops/reports/quality_report_20260531T083403Z.md`.
- QA interpretation: `docs/WELLNESS_DIALOGUE_QA_20260608.md`.

## Product Decision

Build one human-reviewed product: `Карта ХМС: факты, границы, следующий шаг` for adults who already have an HMS/GC-MS report. AI performs intake/OCR/structuring; a named specialist owns the final result. No diagnosis or treatment from HMS, no automatic supplement scheme, and no affiliate upsell in V1.

## Release Blockers

1. Bot runtime down.
2. Direct dossier delivery bypasses expert review.
3. Unsafe specificity exists in a delivered HMS draft.
4. No current complete benchmark after May 31.
5. Product names, prices, and claims disagree across surfaces.
6. No validated external-customer demand evidence.
7. Health-data policy/retention/deletion and legal review are incomplete.
8. Disk below floor.

## Immediate Actions

1. Restore the scheduled task without a second poller.
2. Enforce persisted named review before delivery.
3. Feature-gate to one 5,900 RUB pilot.
4. Build 20 de-identified HMS fixtures and require zero critical defects.
5. Run 15 interviews and complete ten unique external paid pilots.
