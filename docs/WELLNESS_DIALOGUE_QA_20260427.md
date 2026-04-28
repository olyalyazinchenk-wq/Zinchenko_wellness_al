# Wellness Dialogue QA - 2026-04-27

## Scope

- Benchmark source: `ops/bench_prompts.json`
- Run date: 2026-04-27
- Surface checked: `generate_live_reply()` and routed live-chat behavior

## Headline Result

- 20/20 benchmark prompts were answered by the local router in `WellnessBot/ai_drafting.py`.
- 0/20 benchmark prompts reached the configured LLM.
- This means current benchmark quality is dominated by canned routing logic, not by the live prompt or model.

## Generic Response Patterns

1. The dominant shape is: careful framing -> broad next step -> Premium Dossier CTA.
2. Symptom prompts are usually answered with one short paragraph of reassurance plus one generalized action suggestion.
3. Service/logistics prompts are handled cleanly and consistently.
4. Clarifying questions are almost never used, even when they would materially improve accuracy.
5. Many replies sound polished, but several are too generic to feel premium or case-specific.

## Personalization Gaps

1. Age and sex cues are mostly ignored in symptom replies.
2. Timing and symptom dynamics from the prompt are rarely used.
3. Multiple GI prompts collapse into the same answer, even when the factual setup differs.
4. Prompt 16 incorrectly inherits the "after antibiotics" storyline even though the user did not mention antibiotics.
5. Prompt 2 asks for the most reasonable next step, but the reply stays broad instead of giving a more operational first move.
6. Prompt 8 would benefit from 1-2 follow-up questions about cycle timing, sleep, hair loss, or stress, but asks none.

## Safety Notes

1. Emergency handling is appropriately conservative for chest pain / dyspnea and fever with blood in sputum.
2. Crisis handling is directionally correct, but thin: it lacks a stronger immediate-safety check and more explicit urgent escalation wording.
3. The benchmark passed the "do not diagnose" boundary across all 20 prompts.
4. The bigger safety risk in this run is false personalization, not overtly dangerous advice.

## Concrete Failures Observed

1. Prompts 2, 7, and 16 receive the same GI template.
2. The GI template mentions "сбой после антибиотиков" even for prompt 16, where antibiotics were never mentioned.
3. Prompts 9, 10, and 15 receive nearly identical service-positioning copy.
4. Many non-logistics symptom replies end with the same upsell CTA, which weakens trust and makes the output feel sales-led.

## What To Change Next Sprint

1. Narrow router scope. Keep hard routing for crisis, emergency, and a few logistics FAQs; send symptom-analysis prompts to the LLM.
2. If the router remains, make templates slot-based and fact-locked so they cannot introduce unsupported details like antibiotics.
3. Add a live-reply quality rule: answer the user's exact question in sentence one, include one concrete next step, and ask up to two clarifying questions when they materially improve safety or precision.
4. Gate CTA insertion. Do not append a sales CTA to most symptom answers; reserve it for explicit product-intent prompts.
5. Strengthen crisis language for self-harm signals with a clearer immediate-action structure.
6. Expand benchmark coverage with pregnancy, medications, oncology, thyroid treatment, teen clients, and ambiguous-but-urgent red flags.

## Best Prompt / Model Improvement Bets

1. Router-first fix beats prompt tuning: prompt/model work will not move benchmark quality until these cases stop being intercepted locally.
2. Once routing is reduced, strengthen `LIVE_CHAT_PROMPT` with an explicit personalization checklist:
   - echo the user's strongest data point,
   - separate fact vs hypothesis,
   - give one concrete next step,
   - ask clarifying questions only when useful.
3. Lower tolerance for generic answers in post-processing: detect repeated boilerplate and force a retry or a safer fallback.

## Benchmarks To Watch Next

- Routed share of benchmark prompts
- Exact-duplicate response count
- Unsupported-detail hallucination count
- Replies with at least one concrete next step
- Replies with unnecessary CTA
