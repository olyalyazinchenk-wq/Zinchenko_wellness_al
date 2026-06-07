# Wellness Dialogue QA - 2026-06-05

## Scope

- Benchmark prompts: `ops/bench_prompts.json`
- Latest completed full artifact: `ops/reports/quality_report_20260531T083403Z.md`
- Current code paths checked:
  - `WellnessBot/ai_drafting.py`
  - `WellnessBot/prompts.py`
  - `ops/quality_probe.py`
  - `tests/test_live_reply_routing.py`
- Verification run today:
  - `.\.venv\Scripts\python.exe -m pytest tests\test_live_reply_routing.py -q` -> passed (`5 passed, 5 subtests passed`)
  - `.\.venv\Scripts\python.exe .\ops\quality_probe.py --mode smoke` -> passed
  - `.\.venv\Scripts\python.exe .\ops\quality_probe.py --mode batch --prompts .\ops\bench_prompts.json` -> failed on prompt `1` with `openai.APIConnectionError` caused by `httpx.ConnectError` / `[WinError 10061]`

## Current executable state

- The benchmark runner is still operationally fragile.
  - `ops/quality_probe.py` still calls `generate_live_reply()` inline for each prompt and does not catch per-prompt model exceptions.
  - Because prompt `1` is model-path, one connection failure still aborts the entire batch before any partial artifact is written.
- The router/model split in code is unchanged:
  - Router handles prompts `9, 10, 11, 12, 13, 14, 15, 17, 18, 19, 20`
  - Model path is still required for prompts `1, 2, 3, 4, 5, 6, 7, 8, 16`
- No newer completed benchmark displaced the May 31 artifact, so current quality truth still depends on that report plus the successful local checks above.
- Benchmark-critical file state is effectively unchanged from the June 3 QA interpretation:
  - `WellnessBot/prompts.py` still contains the numbered-points-only formatting rule for client-facing chat.
  - `ops/quality_probe.py` is still the old all-or-nothing batch runner.

## Findings

### 1. Generic response patterns

- Model replies are still structurally too long relative to router replies in the latest completed artifact:
  - model average: `1982.4` chars
  - router average: `394.4` chars
- `4/9` model replies are longer than `2000` chars: `1, 2, 3, 4`.
- The dominant model shape is still:
  - warm opening
  - broad hypothesis stack
  - long marker / test list
  - clarifying questions
  - soft dossier CTA
- Format drift remains open despite the prompt rule:
  - `8/9` model replies still contain markdown emphasis or bullets: `1, 2, 3, 4, 5, 6, 7, 16`
- Duplicate service copy remains visible:
  - exact duplicates: `9/15`, `17/18`
  - near-duplicate cluster: `9/10/15` (`9/10` similarity about `0.897`)

### 2. Personalization gaps

- Unsupported naming is still present in the latest successful artifact:
  - prompts `1, 2, 3, 16` open with invented `Ольга`
- Unsupported age-storytelling is still present:
  - prompt `2` opens with `В 35 лет...`
  - prompt `8` opens with `В возрасте 34 лет...`
- The model still personalizes cosmetically before analytically:
  - intimate or warm greeting first
  - broad cross-system theory second
  - narrower next step only later

### 3. Safety issues

- The main safety risk remains polished false specificity, not overtly dangerous advice.
- Prompt `1` still overreaches into quasi-diagnostic framing such as subclinical hypothyroid / adrenal-cortisol storyline from a short fatigue prompt.
- Prompt `7` still names `SIBO` from limited post-antibiotic context.
- Prompt `8` still reaches quickly into ovarian / hormonal framing and progesterone timing detail without enough context.
- Emergency handling is still too collapsed:
  - prompts `17` and `18` are exact duplicates even though chest pain / dyspnea and fever with hemoptysis are different escalation classes

## Top improvements for the next sprint

1. Restore benchmark observability first.
   - Catch connection and timeout exceptions per prompt in `ops/quality_probe.py`
   - Emit partial artifacts with prompt id, branch, and error class
   - Stop losing the entire batch on prompt `1`

2. Add anti-personalization checks to the live path.
   - Block invented names unless mirrored from the user
   - Block age-storytelling unless age materially changes the guidance
   - Add tests for names, intimate salutations, and unsupported life-stage language

3. Tighten the live-chat answer contract.
   - First sentence must answer the user directly
   - Cap early hypotheses at `2`
   - Cap clarifying questions at `2`
   - Ban markdown bullets and bold in client-facing chat answers
   - Downshift quasi-diagnostic labels such as `SIBO`, subclinical hypothyroidism, adrenal exhaustion, and hormone-timing claims unless clearly framed as differentials with missing-data caveats

4. Split emergency templates by risk class.
   - cardio / respiratory
   - infection / hemoptysis
   - mental-health crisis

5. Expand benchmark-visible checks.
   - exact duplicate detection
   - near-duplicate detection
   - invented-name detection
   - format-rule violations
   - overlength thresholding

## Bottom line

Today re-confirmed the June 3 picture rather than replacing it: local routing tests and smoke still pass, the full batch still dies on prompt `1`, and the latest trustworthy quality baseline is still the completed May 31 artifact. The same core product issues remain open in that artifact: long hypothesis-heavy model replies, unsupported names and age framing, weak analytical personalization, format-rule drift, and overly specific wellness-medical inference.
