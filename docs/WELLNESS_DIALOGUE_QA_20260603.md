# Wellness Dialogue QA - 2026-06-03

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
  - `.\.venv\Scripts\python.exe -m pytest tests\test_live_reply_routing.py -q` -> passed (`5 passed, 5 subtests passed`)
  - `.\.venv\Scripts\python.exe .\ops\quality_probe.py --mode smoke` -> passed
  - `.\.venv\Scripts\python.exe .\ops\quality_probe.py --mode batch --prompts .\ops\bench_prompts.json` -> failed on prompt `1` with `openai.APIConnectionError` caused by `httpx.ConnectError` / `[WinError 10061]`

## Current executable state

- The benchmark-critical code is no longer identical to the May 30 baseline.
  - `WellnessBot/prompts.py` now contains a wider tier stack (`SCREENING_PROMPT`, `PREMIUM_BASIC_PROMPT`, `PREMIUM_FULL_PROMPT`) and a formatting rule that says client-facing text should use numbered points only and no markdown bullets.
  - `WellnessBot/ai_drafting.py` now maps more product tiers and adds screening-generation helpers, but the live chat router / sanitizer / CTA flow still drives the benchmark prompt behavior.
- The router/model split is unchanged in current code:
  - Router handles prompts `9, 10, 11, 12, 13, 14, 15, 17, 18, 19, 20`
  - Model path is still required for prompts `1, 2, 3, 4, 5, 6, 7, 8, 16`
- Because prompt `1` is model-path and `ops/quality_probe.py` still aborts on the first model exception, no fresh June 3 full artifact exists.

## Findings

### 1. Generic response patterns

- The May 31 full artifact still shows a large style gap between branches:
  - model replies average about `1982` characters
  - router replies average about `394` characters
- `4/9` model replies are longer than `2000` characters (`1, 2, 3, 4`).
- `8/9` model replies include clarifying questions, but they usually arrive after a long hypothesis stack rather than after a tight first answer.
- `8/9` model replies still use markdown emphasis and bullet formatting (`1, 2, 3, 4, 5, 6, 7, 16`) even though the prompt file now explicitly asks for numbered points only.
- Duplicate / near-duplicate service copy remains visible:
  - exact duplicates: `9/15`, `17/18`
  - near-duplicate cluster: `9/10/15`

### 2. Personalization gaps

- Unsupported direct naming remains open in the latest successful artifact:
  - prompts `1, 2, 3, 16` open with invented `Ольга`
- Unsupported age-storytelling also remains open:
  - prompt `2` anchors on `35 лет`
  - prompt `8` anchors on `34 лет`
- The model still tends to personalize cosmetically before it personalizes analytically:
  - warm opening
  - broad multi-system theory
  - long analysis list or hormone/lab framing
  - only then a narrower next step

### 3. Safety issues

- The main safety risk remains polished false specificity, not overtly dangerous instructions.
- Prompt `1` still overreaches into quasi-diagnostic framing such as subclinical hypothyroidism and adrenal/cortisol storyline from a short fatigue prompt.
- Prompt `7` still names `SIBO` from limited context after antibiotics, which is too specific for this benchmark stage.
- Prompt `8` still reaches quickly into ovarian/hormonal framing and progesterone timing detail without enough context.
- Emergency routing is still too collapsed:
  - prompts `17` and `18` are exact duplicates even though chest pain / dyspnea and fever with hemoptysis are different escalation classes.

## Top improvements for the next sprint

1. Restore benchmark observability first.
   - Catch connection and timeout exceptions per prompt in `ops/quality_probe.py`
   - Emit partial artifacts with prompt id, branch, and error class
   - Stop losing the entire batch on prompt `1`

2. Add anti-personalization checks to the live path.
   - Block invented names unless mirrored from the user
   - Block age-storytelling unless age materially changes the guidance
   - Add tests for names, intimate salutations, and unsupported life-stage language

3. Tighten the live-chat answer contract in `LIVE_CHAT_PROMPT` and sanitizer coverage.
   - First sentence must answer the user directly
   - Cap early hypotheses at `2`
   - Cap clarifying questions at `2`
   - Ban markdown bullets / bold in client-facing chat answers
   - Downshift quasi-diagnostic labels such as `SIBO`, subclinical hypothyroidism, adrenal exhaustion, and hormone-timing claims unless clearly framed as doctor-level differentials with missing-data caveats

4. Split emergency templates by risk class.
   - cardio / respiratory
   - infection / hemoptysis
   - mental-health crisis

5. Expand benchmark-visible checks in tests or report post-processing.
   - exact duplicate detection
   - near-duplicate detection
   - invented-name detection
   - format-rule violations
   - overlength thresholding

## Bottom line

Today confirmed that the benchmark runtime is still operationally fragile: smoke and routing tests pass, but the fresh batch still dies on the first model-path call. The best available quality baseline has moved forward from May 6 to the successful May 31 artifact, and that artifact shows the same core product problems in a clearer form: long hypothesis-heavy model replies, weak analytical personalization, unsupported names/age framing, and overly specific wellness-medical inferences.
