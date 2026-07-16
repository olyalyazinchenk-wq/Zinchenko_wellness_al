# Antigravity WellnessBot: Product, Release, Marketing, And Monetization Plan

Updated: 2026-07-16 22:07 MSK
Stage: `controlled-concierge-pilot-2026-06-18-r1`
Decision status: approved direction for validation; public launch remains blocked

## Executive Decision

The project must stop trying to release a broad automated nutritionist with six paid products. The defensible wedge is one narrow, human-reviewed service for adults who already have an HMS/GC-MS report:

> `Карта ХМС: факты, границы, следующий шаг` - independent navigation through an HMS report without diagnosing from microbial markers, selling fear, or turning one laboratory table into a treatment plan.

The bot is not the expert and not the product. It is the intake, transcription, evidence-labeling, and workflow layer. The paid product is a signed specialist result that tells the client:

1. what the report actually contains;
2. what cannot be concluded from it;
3. which findings matter only when combined with symptoms, medications, history, and other tests;
4. what requires a doctor;
5. what can be observed safely for 14 days.

This counter-positioning is the breakthrough: do not promise a more confident microbiome diagnosis than competitors. Sell protection from overinterpretation, unnecessary supplements, and chaotic next steps.

## Current Situation

| Area | Verified fact | Consequence |
|---|---|---|
| Runtime | The scheduled task is `Ready`, bot process count is `0`, and the last runner attempt exited on 2026-07-01 after Telegram network/proxy failures. | The bot is down. Growth and public launch are blocked. |
| Delivery safety | The current dossier path sets internal review to `direct_delivery`; only the new deterministic supplement branch stops for review. | A generated HMS dossier can reach the client without expert approval. This is a P0 regression. |
| HMS output | A delivered June HMS draft diagnosed hypothyroidism, asserted microbe-to-symptom causation, introduced unsupported background, included supplement doses, and promoted affiliate brands. | Prompt tuning alone is insufficient. The output contract and delivery gate must change. |
| Quality | Latest completed benchmark remains `ops/reports/quality_report_20260531T083403Z.md`; current synthesis is `docs/WELLNESS_DIALOGUE_QA_20260608.md`. Model replies averaged about 1,982 characters, 8/9 violated the required format, and unsupported personalization and false specificity remained. | There is no current evidence that dialogue or dossier generation is release-safe. |
| Demand | Local submissions contain 47 records but only two unique Telegram users; 35 payments are manually confirmed and just one is marked paid. | These are primarily internal/test artifacts and cannot be treated as revenue or market proof. |
| Product map | Bot, root page, mini-app, landing, and strategy docs expose conflicting names, prices, promises, and review rules. | A buyer cannot understand the canonical offer; external claims are not trustworthy. |
| Notion | The project database is empty; client/case/material databases contain one client case. The sync hub was last current in June. | Notion is an archive, not an operating product system yet. |
| GitHub | Local `HEAD` and `origin/master` match at `2968cdb`, but 20 tracked files are dirty and current product behavior exists only in the working tree. | GitHub does not represent the executable project truth. |
| Channel | Local files identify `@olga_nutri86` and an April content plan, but current audience, reach, CTA, lead, and sales metrics are unavailable. | Content activity cannot be evaluated as marketing performance. |
| Storage | `C:` has about 4.67 GiB free against the project floor of 10 GiB. | Runtime, OCR, PDF, and benchmark work remain operationally fragile. |
| Governance | The governance artifact contains 151 experiments and zero decisions. | The project has optimized ideation volume instead of product learning. |

## Why The Project Has Not Reached Release

1. Product scope expanded faster than proof. Six offers, a mini-app, PDFs, supplements, and affiliate rails were built before ten independent customers validated one outcome.
2. The project monetized the mechanism rather than the job. Clients do not buy an AI dossier or a list of microbes; they buy clarity, risk reduction, and a credible next step.
3. HMS confidence exceeded the evidence. The 2025 international consensus on microbiome testing states that evidence for current clinical usefulness is scarce. The Osipov literature describes an analytical method, but does not justify deterministic diagnosis or treatment from a consumer report.
4. Human review was a documented rule but not an executable invariant. The current direct-delivery path contradicts the public promise of expert verification.
5. Internal test payments were mistaken for demand signals. A manually confirmed payment by an internal user is workflow evidence, not market evidence.
6. Content had a calendar but no measurement loop. There is no current ledger from post reach to CTA, qualified lead, payment, delivery, and outcome.

## Canonical Product

### Customer

Russian-speaking adult, typically 25-50, who already paid for an HMS/GC-MS report, received a dense table, has non-acute digestive or wellness complaints, and does not know what is meaningful or what to do next.

### Job To Be Done

`Когда у меня на руках сложный отчет ХМС и много тревожных трактовок, помогите отделить факты от гипотез и подготовить безопасный следующий шаг, чтобы не тратить деньги и здоровье на случайные схемы.`

### Promise

Within 48 hours after complete intake, the client receives a human-reviewed map of the report: facts, uncertainty, clinical boundaries, doctor questions, and a 14-day observation plan. No diagnosis from HMS alone and no supplement sale inside the core result.

### Deliverable

1. One-page executive map: three facts, three unknowns, three next actions.
2. Marker ledger: source value, reference, OCR confidence, status, possible interpretation, prohibited conclusion, and relevance to the client's context.
3. Context map: symptoms, medications, diagnoses, allergies, age, other tests, and missing data.
4. Method limits: what HMS can describe and what it cannot establish clinically.
5. Red-flag and doctor route section.
6. Fourteen-day low-risk observation plan focused on food rhythm, symptom tracking, sleep, and existing-care coordination.
7. A short list of questions for the relevant doctor.
8. Reviewer sign-off: reviewer, timestamp, version, corrections, and final approval.
9. Day-7 Telegram check-in.

### Explicit Exclusions In V1

- no diagnosis of dysbiosis, infection, candidiasis, SIBO, parasites, hypothyroidism, or other disease from HMS;
- no causal claims from one microbial marker to a symptom;
- no antibiotics, antifungals, antiparasitic products, hormones, or prescription advice;
- no automatic supplement dose/course;
- no affiliate product block in the core result;
- no encouragement to buy or repeat HMS without a separate justified reason;
- no minors, pregnancy/breastfeeding, acute red flags, or complex medication cases without a defined escalation route.

## Offer And Monetization

### Validation Offer: First 10 External Clients

`Карта ХМС - пилот`: 5,900 RUB.

Includes complete report review, structured intake, signed result, one clarification round, and day-7 check-in. Manual payment and manual review remain mandatory. The current price is held only to avoid adding another pricing change before proof.

### Validated Core Offer

After all release and demand gates pass: 7,900 RUB.

The price increases only when median turnaround is at most 48 hours, critical QA defects are zero, at least eight of ten external clients complete the service, and at least six report that they understand their next step.

### Continuity Offer

`21 дней внедрения`: 14,900 RUB, introduced only after at least five core clients ask for help implementing the result.

It includes weekly review, symptom/food diary feedback, plan adjustment inside the nutritionist scope, and coordination questions for clinicians. It is not sold automatically after every HMS report.

### Revenue Scenarios

| Scenario | Monthly mix | Gross revenue | Capacity assumption |
|---|---:|---:|---|
| Pilot | 10 x 5,900 | 59,000 RUB | Founder-led validation, not stable income. |
| Validated base | 12 x 7,900 + 4 x 14,900 | 154,400 RUB | About 10-12 specialist hours per week with templates and async delivery. |
| Strong solo practice | 16 x 7,900 + 6 x 14,900 | 215,800 RUB | About 12-15 specialist hours per week; requires stable acquisition and strict scope. |

These are gross scenarios before taxes, payment fees, refunds, tools, and advertising. They are capacity models, not forecasts. Affiliate income is excluded because it can distort trust and currently creates regulatory and ethical risk.

## Marketing Line

### Positioning

`Я не лечу микробиом по одной таблице. Я помогаю понять, что в отчете действительно есть, чего из него нельзя заключить и какой следующий шаг не навредит.`

The brand should own `clarity without fear`, not `the strongest protocol`.

### Content Pillars

1. `Разбор строки`: one anonymized report fragment, what it says, what it does not say.
2. `Миф метода`: candidiasis, SIBO, parasites, immunity, and other conclusions that cannot be established from one marker table.
3. `Связь с контекстом`: why symptoms, medications, other tests, and history change the interpretation.
4. `Маршрут к врачу`: the exact questions that make a consultation more productive.
5. `Как устроена проверка`: show the reviewer checklist and corrections, not vague AI magic.
6. `Кейс ясности`: before/after in terms of decisions and reduced confusion, never a cure claim.

### Weekly Publishing System

- Monday: `Разбор строки`.
- Wednesday: myth/boundary post.
- Friday: anonymized decision case or reviewer process.
- Sunday: one question-and-answer post or voice circle only if the previous content generated questions.

One CTA for 30 days: `Напишите КАРТА, если у вас уже есть отчет ХМС и вы хотите понять, что в нем факт, а что гипотеза.`

Do not run paid ads until organic or partner traffic produces ten external paid clients and the service passes the safety gates. Advertising cannot repair an unsafe result or an unclear offer.

## Sales Motion

### Qualification In Telegram

1. Is the client 18+ and do they already have the complete report?
2. What decision are they trying to make after receiving it?
3. Are there acute symptoms, pregnancy/breastfeeding, major diagnoses, or active medications?
4. What has already been recommended or sold to them?
5. Do they want interpretation clarity or an ongoing behavior-support service?

Qualified, non-acute clients receive the single pilot offer. Unsafe or out-of-scope cases receive a doctor route, not a sale.

### Discovery Interviews

Interview 15 people who already completed or considered HMS. Do not pitch during the first 15 minutes. Capture:

- trigger for buying the test;
- what was confusing in the report;
- what advice they received afterward;
- money already spent on consultations/supplements;
- feared consequence;
- ideal result;
- willingness to pay for independent review;
- exact phrases they use.

## KPI System

### North Star

`External clients who receive a reviewer-approved result and can correctly state their next safe action within 48 hours.`

### Pilot Gates

| Metric | Gate |
|---|---:|
| External paid clients in 30 days | at least 10 |
| Unique external buyers | 100% of counted sales |
| Delivery with named human approval | 100% |
| Critical medical/claim defects | 0 |
| Report markers accounted for | 100% or explicitly unreadable |
| Turnaround after complete intake | median at most 48h |
| Clients who can state next action | at least 80% |
| Refund requests | at most 10% |
| Day-7 follow-up completed | at least 70% |
| Organic qualified-lead to paid conversion | at least 20% |

No internal user, manual test payment, duplicate rail, or generated PDF counts toward demand validation.

## Release Gates

### P0: Before Another Paid Delivery

1. Restore the scheduled-task runtime and prove one polling owner without starting a second bot process.
2. Remove `direct_delivery` from all dossier/HMS paths. Delivery requires a persisted named approval.
3. Feature-gate the menu to one pilot offer plus a free education/qualification path.
4. Disable the automatic 6,000 RUB supplement upsell and all affiliate recommendations in the HMS core flow.
5. Make age, consent, medication, allergy, diagnosis, and red-flag fields hard prerequisites.
6. Replace the generic premium prompt with a dedicated HMS schema that separates facts, uncertainty, and prohibited conclusions.
7. Add a deterministic claim checker for diagnoses, unsupported conditions, invented history, doses, courses, and microbe-to-symptom causation.

### P0: Legal And Data

1. Obtain legal review of the offer boundary: educational/nutrition navigation versus medical service.
2. Publish a personal-data policy and explicit consent for health data, retention, deletion, processors, and cross-border/third-party model handling where applicable.
3. Define data retention and deletion controls for Telegram uploads, local OCR, drafts, PDFs, logs, Notion, and external models.
4. Remove health outcome testimonials and treatment-style claims from all public surfaces.
5. If supplements are later advertised, separate them from the service and apply the required non-medicine warning and affiliate disclosure.

This is an operational risk list, not legal advice. The final wording must be reviewed by a qualified Russian lawyer.

### P1: Quality Evidence

1. Create at least 20 de-identified HMS fixtures covering clean OCR, partial OCR, conflicting units, red flags, medications, and insufficient context.
2. Require zero critical defects and 100% marker-accounting across two consecutive runs.
3. Make the benchmark write partial results when the model/network fails.
4. Add tests for invented names/ages/history, diagnosis language, exact doses, affiliate leakage, length, and reviewer-gate bypass.
5. Re-run the full benchmark. The latest reference remains `ops/reports/quality_report_20260531T083403Z.md` until a newer complete artifact exists.

### P1: Surface Truth

Align bot menu, root page, landing, mini-app, Notion, and GitHub to one name, one price, one promise, one review rule, and one CTA. Remove all claims that YooKassa, PDF delivery, or expert review are live until verified end to end.

## 12-Hour Command Set

1. Owner `Ops`: repair scheduled-task network/proxy configuration and capture a single-owner startup/handled-update artifact.
2. Owner `Engineering`: hard-block dossier delivery without persisted named approval.
3. Owner `Product`: feature-gate all offers except `Карта ХМС - пилот`; remove the post-HMS supplement upsell.
4. Owner `Clinical QA`: convert the delivered problematic HMS draft into the first golden negative fixture and write the prohibited-claim rubric.
5. Owner `Founder`: answer the five open context questions below and identify five external interview candidates.
6. Owner `Content`: draft the first three posts using the single `КАРТА` CTA; do not publish outcome claims.
7. Owner `Ops`: recover `C:` above 10 GiB with explicit operator review; do not delete client artifacts blindly.

## 7/30/90-Day Execution

### Days 1-7: Make One Result Safe

- restore runtime and review gate;
- ship the dedicated HMS output contract;
- build 20 fixtures and pass the release rubric;
- align public copy to the pilot;
- publish legal/privacy minimums;
- conduct five discovery interviews;
- recruit the first three external paid pilots manually.

### Days 8-30: Prove Demand And Delivery

- complete 15 interviews;
- sell to ten unique external clients;
- review every output personally;
- measure the full funnel and day-7 outcome;
- publish two anonymized decision cases with consent;
- decide `continue`, `change segment`, or `stop` from the KPI gates.

### Days 31-90: Build The Business Only After Proof

- raise core price to 7,900 RUB only if gates pass;
- introduce 21-day support only when requested by at least five clients;
- build two referral partnerships with gastroenterologists/labs only without implied endorsement or claim inflation;
- automate intake, OCR confidence, checklists, and follow-up, but keep final approval human;
- consider paid acquisition only after a stable qualified-lead to paid conversion baseline exists.

## Strategy Delta

- Previous strategy: broad Telegram wellness concierge with an expanding product ladder and premium dossier.
- New strategy: one independent, human-reviewed HMS clarity service for people who already have the report.
- Previous differentiation: AI depth, PDF, supplements, and many personalized sections.
- New differentiation: evidence boundaries, marker-accounting, named review, doctor-question pack, and protection from unnecessary interventions.
- Previous monetization: multiple prices and automatic upsells.
- New monetization: one 5,900 RUB pilot, then one 7,900 RUB core and one demand-triggered continuity offer.
- Previous growth logic: publish content and expose more products.
- New growth logic: one CTA, 15 interviews, ten external paid pilots, measured conversion, and no ads before proof.

## Plan Delta

1. Safety and runtime before traffic.
2. One product before a ladder.
3. Human-reviewed outcome before autonomous delivery.
4. External buyer evidence before revenue claims.
5. One canonical price/promise across every surface.
6. Content tied to one CTA and a measurable funnel.
7. Supplements removed from the core product until separate demand, safety, and compliance proof exists.
8. Decisions replace experiment accumulation.

## Open Context Questions For The Founder

1. How many payments came from real external clients, and what were actual collected revenue, refunds, and delivered outcomes?
2. Which qualifications, certificates, medical background, and professional scope can be documented publicly?
3. How many hours per week can be committed to manual review, clients, interviews, and content for eight weeks?
4. What are the current channel subscribers, 30-day reach, post views, inbound leads, and sales by source?
5. Is affiliate supplement income a required business goal, or can it remain outside the core offer until trust is established?

Until answered, the plan assumes zero validated external sales, a non-physician nutritionist scope, and 10-15 founder hours per week.

## Context For New Model

### Stage

Controlled concierge pilot; bot currently down; public launch blocked; one HMS product is being defined for validation.

### Objective

Deliver ten external, paid, named-review HMS clarity cases with zero critical defects and a measurable client decision outcome.

### Constraints

- one Windows scheduled-task polling owner;
- manual payment and mandatory human approval;
- no diagnosis/treatment from HMS;
- no supplements or affiliate upsell in the core V1;
- health-data policy, consent, retention, and deletion required;
- latest completed benchmark is `ops/reports/quality_report_20260531T083403Z.md`;
- `C:` remains below the 10 GiB floor;
- current GitHub head does not contain the dirty working-tree behavior.

### Immediate Next Actions

1. Restore single-owner runtime.
2. Reinstate the delivery review gate.
3. Collapse the menu to the HMS pilot.
4. Build and pass the HMS safety fixture set.
5. Answer the founder questions and recruit five external interviews.

## Evidence And External References

- Internal benchmark: `ops/reports/quality_report_20260531T083403Z.md`.
- Internal QA synthesis: `docs/WELLNESS_DIALOGUE_QA_20260608.md`.
- Osipov and Verkhovtseva, analytical-method review: https://pubmed.ncbi.nlm.nih.gov/21831791/
- International consensus on microbiome testing; clinical usefulness evidence described as scarce: https://pubmed.ncbi.nlm.nih.gov/39647502/
- Federal Law 38-FZ, Article 24, advertising of medical services/methods: https://www.consultant.ru/document/cons_doc_LAW_58968/8fbc3d05dbc778e17bfc1b45fb7339df525c1985/
- Federal Law 38-FZ, Article 25, advertising of dietary supplements: https://www.consultant.ru/document/cons_doc_LAW_58968/6147d77ef3ebff43fadce8d43d23f5e36cd7aa20/
- Federal Law 152-FZ, Article 10, health data as a special category: https://www.consultant.ru/document/cons_doc_LAW_61801/26edb2934b899bf9c74c3a8f7e574651c6565e6d/
- Federal Law 152-FZ, Article 18.1, operator policy and safeguards: https://www.consultant.ru/document/cons_doc_LAW_61801/eeeebe22bf738fd65bb66b95cc278911ae2525ee/
