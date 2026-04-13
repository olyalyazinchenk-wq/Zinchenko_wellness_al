# Antigravity Proposal Review (2026-04-13)

## Verdict

The proposal has useful energy and some valid product intuition, but it is not production-ready as a governing plan.
It mixes good ideas with factual errors, legal/compliance risk, and several "completed" claims that are not actually complete.

## What is strong

- Clear focus on a painful user problem and paid conversion path.
- Correct idea that a Telegram-first MVP can be launched quickly.
- Correct emphasis on differentiation via Olga's expertise and workflow UX.

## Critical issues

1. Compliance mismatch with your requirements:
   - The plan requires OpenAI and global hosting by default.
   - Your stated constraint is Russian-contour handling for client-sensitive data.

2. Medical/legal exposure:
   - The plan still frames lab interpretation close to medical activity.
   - "Direct protocol to user without strict human review gate" is high-risk.

3. Execution reality gap:
   - Multiple phases are marked as completed without full operational proof.
   - Document quality issues (encoding corruption in `STRATEGY.md`) indicate weak control.

4. Security hygiene:
   - Asking for plain API keys in chat is weak practice.
   - Existing Telegram bot token should be rotated because it was exposed in chat history.

## Non-negotiable operating principles

- Keep sensitive client workflow inside Russian-contour infrastructure by default.
- Human-in-the-loop for any case-level recommendations.
- No diagnosis claims, no treatment promises, emergency red-flag escalation only.
- Product quality measured by dialogue usefulness, not by generic checklist output.

## Recommended next step (operational)

Run a 7-day model quality sprint with strict metrics:

- Model candidates: Yandex high-quality chat models available to your account.
- Test set: 30 real anonymized dialogue prompts.
- Metrics: relevance, personalization, safety, follow-up quality, user satisfaction.
- Outcome: choose one primary model + one fallback model and freeze production prompt profile.

