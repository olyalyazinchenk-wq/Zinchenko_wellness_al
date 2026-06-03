# Wellness Dialogue QA - 2026-05-30

## Scope

- Benchmark prompts: `ops/bench_prompts.json`
- Last completed full artifact: `ops/reports/quality_report_20260506T080435Z.md`
- Current code paths checked: `WellnessBot/ai_drafting.py`, `WellnessBot/config.py`, `ops/quality_probe.py`, `tests/test_live_reply_routing.py`
- Verification run today:
  - `.\.venv\Scripts\python.exe -m pytest tests\test_live_reply_routing.py -q` -> passed
  - `.\.venv\Scripts\python.exe .\ops\quality_probe.py --mode smoke` -> passed
  - `.\.venv\Scripts\python.exe .\ops\quality_probe.py --mode batch --prompts .\ops\bench_prompts.json` -> failed on first model-path prompt with `openai.APIConnectionError` caused by `httpx.ConnectError` / `[WinError 10061]`

## Current executable state

- Runtime config is still `openai_compatible` with model `deepseek-v4-flash`, API mode `chat_completions`, base URL `https://api.deepseek.com`, timeout `90s`.
- No local diff is present in benchmark-critical files:
  - `WellnessBot/ai_drafting.py`
  - `WellnessBot/prompts.py`
  - `ops/quality_probe.py`
  - `tests/test_live_reply_routing.py`
- The router/model split is unchanged in code:
  - `11/20` prompts route locally: `9, 10, 11, 12, 13, 14, 15, 17, 18, 19, 20`
  - `9/20` prompts require the live model: `1, 2, 3, 4, 5, 6, 7, 8, 16`
- Because prompt `1` is model-path, the batch probe currently fails before producing any fresh 2026-05-30 artifact.

## Quality picture still in force

With the live model unreachable today, the latest completed quality truth remains the May 6 artifact. The main patterns from that run are still structurally supported by current code:

1. Generic response pattern
   - Model replies still tend to follow the same shape: empathy -> broad hypothesis stack -> long list of markers/tests -> clarifying questions -> soft CTA.
   - Service/router replies remain much flatter than model replies, so the tone jump between branches is still real.

2. Personalization gaps
   - The current sanitizer only rewrites a small set of treatment/diagnostic phrases and still does not guard against invented names, intimate salutations, or age-storytelling.
   - The May 6 failures around invented `Olga`, `Dorogaya`, and unsupported life-stage framing should still be treated as open until a fresh model run proves otherwise.

3. Safety issues
   - Emergency prompts still collapse into one shared offline escalation template for very different risk classes.
   - Crisis handling is conservative, but still thin on immediate safety confirmation.
   - Model-path risk remains polished false specificity rather than overtly unsafe advice.

## New blocker confirmed today

The main new operational fact is not a dialogue-quality improvement or regression. It is that fresh model-path QA is blocked again:

- `ops/quality_probe.py` does not catch per-prompt model exceptions, so one connection failure aborts the entire batch.
- `generate_live_reply()` calls the chat completions client directly on model-path prompts, so prompt `1` now hard-stops the run before any updated comparison data exists.

## Next sprint priorities

1. Restore benchmark observability first
   - Catch connection/time-out exceptions per prompt in `ops/quality_probe.py`
   - Emit partial artifacts with prompt id, error class, and branch (`router` vs `model`)
   - Keep batch runs useful even when the model endpoint is down

2. Add an anti-personalization barrier
   - Block invented names
   - Block intimate salutations unless mirrored from the user
   - Block unsupported age/life-stage storytelling

3. Tighten the symptom-answer contract
   - First sentence must answer the question directly
   - Cap early hypotheses at `2`
   - Cap clarifying questions at `2`
   - Prefer one next step before long test lists

4. Split emergency templates by risk class
   - Cardio/respiratory
   - Infection/hemoptysis
   - Mental-health crisis

5. Expand benchmark-visible checks
   - Duplicate cluster detection
   - Name/intimacy detection
   - Overlength thresholding
   - Clarifying-question coverage on model replies

## Bottom line

Today did not produce a new completed 20-prompt artifact. The benchmark-critical code is unchanged, routing is unchanged, tests still pass, and the live model benchmark is blocked by the same connection failure pattern seen on 2026-05-08. Until connectivity or per-prompt error handling is fixed, the May 6 report remains the last trustworthy full QA baseline.
