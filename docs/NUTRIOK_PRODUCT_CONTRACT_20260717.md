# НутриОК Product Contract

Updated: 2026-07-17 00:27 MSK

## Brand

- Brand: `НутриОК by Olga Kovaleva`
- Bot display name: `НутриОК | полный разбор`
- Channel display name: `НутриОК | Ольга Ковалева`
- Promise: `Разбор, после которого понятно, что делать`
- `Olga_nutri_med` is a legacy handle/redirect candidate, not the primary spoken brand.

## Outcome Contract

Every cycle has one primary goal: energy, digestion, weight/appetite, skin/hair, or sleep/stress.
The client records a baseline from 0 to 10, one goal-specific measure, and action adherence.
Every paid assessment requires a three-day nutrition diary. Symptoms, lifestyle, medications,
allergies, and relevant labs provide context. HMS/Osipov can be one input, not a separate product,
diagnosis, or causal truth source.

## Product Ladder

| Product | Pilot | Regular | Deliverable | Review |
| --- | ---: | ---: | --- | --- |
| ОК-Старт | 0 RUB | 0 RUB | goal, baseline, one first action | automated screening |
| ОК-Экспресс | 990 RUB | 1,490 RUB | three patterns, seven-day plan, metric | automatic only after safety gate |
| ОК-Разбор | 5,900 RUB | 7,900 RUB | full profile, justified lab minimum, one interpretation, 30-day strategy | Olga approval required |
| ОК-Результат 8 | 14,900 RUB | 19,900 RUB | full assessment plus eight-week adaptation | Olga approval required |
| ОК-Ритм | 1,990 RUB/month | 1,990 RUB/month | maintenance after core program | Olga approval required |

The previous payment is credited in full when upgrading within 30 days. Laboratory costs are separate.
Lab results for an approved full assessment can be submitted for 30 days.

## Safety And Commercial Rules

- No diagnosis, treatment, prescription, medication change, or guaranteed result.
- Red flags stop automatic delivery and route the case to safety review.
- ОК-Разбор, ОК-Результат 8, and ОК-Ритм never use direct automatic delivery.
- Supplement names, dose, duration, and links are drafts until personally approved by Olga.
- When suitable, Olga may approve up to two options from Vitamax and Siberian Wellness; no suitable match means no product.
- Do not rank products by commission.
- Required disclosure: `Партнерские ссылки: Ольга может получить вознаграждение; выбор не меняет вашу схему или цену.`
- Required warning: `БАД не является лекарственным средством.`

## Pilot Success Gate

- 20 unique external ОК-Экспресс buyers.
- At least 8 upgrades to ОК-Разбор.
- At least 4 upgrades to ОК-Результат 8.
- Zero critical safety defects in two consecutive current-product benchmark runs.
- No advertising before runtime, privacy, payment, reviewer, and benchmark gates pass.

## Implemented In This Slice

- Canonical product catalog, legacy-code migration, prices, review rules, upgrade credit, and intake validation contract.
- NutriOK-specific model instructions and deterministic delivery safety gate.
- Public Telegram menu, landing, root page, and mini-app prototype aligned to the ladder.
- Automatic delivery blocked for full tiers; risky Express drafts are held for review.
- 63 unit tests pass.

## Not Yet Release-Ready

- Scheduled task is down after Telegram network/proxy failures; no second poller may be started.
- Live Telegram intake does not yet persist the structured goal/baseline/three-day diary schema end to end.
- RF cloud webhook, YDB/Object Storage, retention/deletion controls, and production audit log remain unimplemented.
- Payment remains manual.
- Latest completed benchmark is still `ops/reports/quality_report_20260531T083403Z.md` and predates NutriOK.
- Public launch remains blocked.
