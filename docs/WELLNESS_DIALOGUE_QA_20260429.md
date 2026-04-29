# Wellness Dialogue QA - 2026-04-29

## Scope

- Benchmark source: `ops/bench_prompts.json`
- Batch runner: `python .\ops\quality_probe.py --mode batch --prompts .\ops\bench_prompts.json`
- Raw artifact: `ops/reports/quality_report_20260429T080345Z.md`
- Current live settings: `LLM_PROVIDER=openai_compatible`, `LLM_MODEL=deepseek-v4-flash`, `LLM_API_MODE=chat_completions`

## Headline Result

- 20/20 benchmark prompts returned non-empty replies.
- 20/20 benchmark prompts were intercepted by `route_live_reply()` before the model call in `WellnessBot/ai_drafting.py`.
- 0/20 benchmark prompts reached the configured model.
- Prompt/model tuning is still second-order; router scope remains the main blocker.

## Router Coverage Snapshot

- Emergency routing: prompts 17 and 18
- Crisis routing: prompt 19
- File-upload routing: prompt 12
- Premium explainer routing: prompt 20
- All remaining benchmark prompts were answered by local symptom/service templates in `route_live_reply()`

## Generic Response Patterns

1. Symptom prompts still collapse into a fixed template shape: soft framing, broad interpretation, one generalized next step, then a sales-oriented close.
2. Service-positioning prompts still reuse the same "Telegram dialogue -> clarity -> Premium Wellness Dossier" copy with only minor CTA variation.
3. Emergency prompts use the exact same escalation wording regardless of symptom details.
4. Clarifying questions are still absent across the full 20-prompt batch.
5. Most symptom replies sound polished, but not premium or case-specific.

## Personalization Gaps

1. Prompts 2, 7, and 16 still receive the same GI template.
2. Prompt 16 still inherits the unsupported "after antibiotics" storyline even though antibiotics are not mentioned.
3. Prompt 8 still does not ask for any cycle-timing, sleep, hair-loss, or stress detail before suggesting a hormonal/stress frame.
4. Prompt 1 and prompt 6 both steer into the same fatigue/lab logic, even though prompt 6 explicitly asks for a ranked starter lab set.
5. Prompts 9 and 15 still reuse near-identical service-explainer copy instead of adapting to the user's emotional stance or purchase intent.

## Safety Notes

1. Emergency handling remains conservative and correctly redirects chest pain/dyspnea and fever with hemoptysis to urgent offline care.
2. Crisis handling is directionally correct and includes "do not stay alone", but still lacks a stronger immediate-safety check structure.
3. The largest safety issue in this batch is not overtly dangerous advice; it is false specificity, especially the unsupported antibiotics detail in prompt 16.
4. Broad symptom templates risk under-triaging edge cases because they answer too early and ask no follow-up questions.

## Concrete Benchmark Signals

- Exact duplicate clusters:
  - Prompts 2, 7, 16
  - Prompts 9, 15
  - Prompts 17, 18
- Clarifying-question count: 0/20
- Model-reached count: 0/20

## Next Sprint Priorities

1. Shrink router scope hard. Keep deterministic routing only for emergency, crisis, and a narrow set of logistics FAQs.
2. Remove unsupported facts from templates. No router branch should inject details like antibiotics unless they are explicitly present in the user message.
3. Add a live-reply quality rule for all symptom prompts:
   - answer the user's exact question in sentence one,
   - give one concrete next step,
   - ask up to two clarifying questions when they materially change safety or interpretation,
   - suppress Premium CTA on most symptom-first replies.
4. Add a benchmark assertion layer that tracks routed share, exact-duplicate count, unsupported-detail hallucinations, and replies with clarifying questions.
5. Once symptom prompts actually reach the model, tighten `LIVE_CHAT_PROMPT` with a personalization checklist and negative examples for unsupported inference.

## Sprint Readout

- Quality has not materially moved since the 2026-04-27 run.
- The dominant failure mode is still router overreach, not model weakness.
- The highest-leverage next change is routing surgery plus template fact-locking.
