# Wellness Dialogue QA - 2026-06-08

## Scope

- Benchmark prompts: `ops/bench_prompts.json`
- Latest completed full artifact: `ops/reports/quality_report_20260531T083403Z.md`
- Current code paths checked:
  - `WellnessBot/ai_drafting.py`
  - `WellnessBot/prompts.py`
  - `WellnessBot/config.py`
  - `ops/quality_probe.py`
  - `tests/test_live_reply_routing.py`
- Verification run today:
  - `.\.venv\Scripts\python.exe -m pytest tests\test_live_reply_routing.py -q` -> passed (`5 passed, 1 warning, 5 subtests passed`)
  - `.\.venv\Scripts\python.exe .\ops\quality_probe.py --mode smoke` -> passed
  - `.\.venv\Scripts\python.exe .\ops\quality_probe.py --mode batch --prompts .\ops\bench_prompts.json` -> failed on prompt `1` with `openai.APIConnectionError` caused by `httpx.ConnectError` / `[WinError 10061]`

## Current executable state

- Benchmark-critical git state is unchanged from the June 5 QA baseline:
  - no local diff in `WellnessBot/ai_drafting.py`
  - no local diff in `WellnessBot/prompts.py`
  - no local diff in `ops/quality_probe.py`
  - no local diff in `tests/test_live_reply_routing.py`
- Current runtime model configuration is still:
  - provider: `openai_compatible`
  - api mode: `chat_completions`
  - model: `deepseek-v4-flash`
  - base URL: `https://api.deepseek.com`
  - timeout: `90s`
- Router/model split in current code is still unchanged:
  - router handles prompts `9, 10, 11, 12, 13, 14, 15, 17, 18, 19, 20`
  - model path handles prompts `1, 2, 3, 4, 5, 6, 7, 8, 16`
- The benchmark runner is still all-or-nothing:
  - `ops/quality_probe.py` calls `generate_live_reply()` inline per prompt and does not catch per-prompt model exceptions
  - one failure on prompt `1` still prevents any fresh partial artifact
- New operational clue from this run:
  - no `HTTP_PROXY` / `HTTPS_PROXY` env vars were present in the shell
  - the failing stack still went through `httpcore._sync.http_proxy`
  - `WellnessBot/ai_drafting.py` builds the `OpenAI` client without an explicit `http_client`, while the Yandex Foundation code paths use `httpx.post(..., trust_env=False)`

## Findings

### 1. Generic response patterns

- No newer completed artifact displaced the May 31 report, so the best full quality baseline is still `ops/reports/quality_report_20260531T083403Z.md`.
- The dominant model-path response shape in that artifact is still:
  - warm opening
  - broad multi-system hypothesis stack
  - long lab or marker list
  - clarifying questions
  - soft CTA into the deeper product
- Hard metrics remain unchanged:
  - model replies average about `1982.4` chars
  - router replies average about `394.4` chars
  - prompts `1, 2, 3, 4` are over `2000` chars
  - `8/9` model replies still violate the numbered-points-only formatting rule
- Repeated copy remains visible:
  - exact duplicates: `9/15`, `17/18`
  - near-duplicate service cluster: `9/10/15`

### 2. Personalization gaps

- Unsupported invented naming remains open in the latest trustworthy artifact:
  - prompts `1, 2, 3, 16` open with invented `Ольга`
- Unsupported age-storytelling remains open:
  - prompt `2` anchors on age `35`
  - prompt `8` anchors on age `34`
- Current automated coverage is still too narrow:
  - `tests/test_live_reply_routing.py` checks router behavior and sanitizer softening
  - it does not check invented names, intimate salutations, age-storytelling, overlength, or formatting-rule drift

### 3. Safety issues

- The main safety issue is still polished false specificity rather than explicit dangerous instructions.
- Prompt `1` still overreaches into thyroid / adrenal-cortisol storyline from a short fatigue prompt.
- Prompt `7` still names `SIBO` from limited post-antibiotic context.
- Prompt `8` still reaches too early into ovarian / hormonal framing and progesterone timing detail.
- Emergency handling remains too collapsed:
  - prompts `17` and `18` still share one exact escalation template despite different acute risk classes

## Top improvements for the next sprint

1. Make the benchmark resilient per prompt.
   - Catch connection and timeout exceptions inside `ops/quality_probe.py`
   - Write partial artifacts with prompt id, branch, and error class
   - Preserve router-path outputs even when model-path prompts fail

2. Harden the `openai_compatible` transport path.
   - Add an explicit `http_client` to `build_client()` with controlled proxy behavior
   - Test a `trust_env=False` path or explicit proxy configuration instead of inheriting transport defaults implicitly
   - Log transport config once at startup so future failures are easier to classify

3. Add anti-personalization and format-discipline checks.
   - Block invented names unless mirrored from the user
   - Block unsupported age-storytelling and intimate salutations
   - Add tests for formatting-rule compliance, overlength, and duplicate copy

4. Tighten the live-chat answer contract.
   - First sentence must answer the user directly
   - Cap early hypotheses at `2`
   - Cap clarifying questions at `2`
   - Continue stripping markdown artifacts in client-facing chat
   - Downshift quasi-diagnostic labels unless clearly framed as uncertain doctor-level differentials

5. Split emergency templates by risk class.
   - cardio / respiratory
   - infection / hemoptysis
   - mental-health crisis

## Bottom line

Today did not change the quality baseline. The local routing tests still pass, the smoke probe still passes, and the full benchmark still dies on the first model-path prompt. The latest trustworthy full artifact is still the May 31 report, which continues to show the same product issues: long hypothesis-heavy model replies, unsupported naming and age framing, weak analytical personalization, formatting drift, and overly specific wellness-medical inference. The only meaningful new signal from this run is operational: the failing `openai_compatible` path still appears to be inheriting a proxy-style transport path even though no proxy env vars are set in the shell.
