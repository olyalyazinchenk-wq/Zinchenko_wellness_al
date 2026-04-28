# Antigravity DeepSeek Auditor Protocol

Date: 2026-04-25
Status: active for controlled pilot, advisory only

## Decision

DeepSeek v4 is connected to Antigravity through the local MCP server `deepseek-v4` and tool `deepseek_v4_chat`.

It is approved as a second-opinion auditor for product, safety, copy, and commercial quality checks. It is not approved as the autonomous medical, legal, or final delivery authority.

## Verified Technical State

- Antigravity MCP config exists: `C:\Users\HP\AppData\Roaming\Antigravity\User\mcp.json`
- MCP server name: `deepseek-v4`
- MCP tool name: `deepseek_v4_chat`
- MCP script: `ops/antigravity_deepseek_mcp.py`
- API smoke test returned: `OK`
- Russian UTF-8 smoke test returned: `ГОТОВО`
- API key is not stored in Antigravity config; it is read from project `.env` files.

## Valid Use Cases

1. Pre-delivery safety review of a premium dossier before the human operator sends it to a client.
2. Critique of repetition, generic wording, weak personalization, and poor premium value.
3. Red-flag wording audit: diagnosis/treatment claims, excessive certainty, unsafe supplement language.
4. Commercial audit: whether the client can clearly see value for `6900 RUB`.
5. Launch-gate audit: whether a change is pilot-ready or public-launch-blocked.

## Forbidden Use Cases

1. Do not let DeepSeek issue diagnoses, treatment, therapy, medication prescriptions, or final clinical interpretations.
2. Do not let DeepSeek replace Olga/human review before client delivery.
3. Do not accept DeepSeek's supplement/dosage recommendations without project policy and human review.
4. Do not use DeepSeek as a standalone legal compliance authority.
5. Do not use off-context DeepSeek outputs as project decisions.

## Auditor Validity Rules

A DeepSeek audit is valid only if all are true:

1. It stays inside the existing product context: Telegram-first premium nutrition navigation.
2. It does not propose a new generic quiz/product-picker bot.
3. It separates controlled pilot from public launch.
4. It preserves the legal boundary: no diagnosis, no treatment, no therapy claims.
5. It acknowledges human review as mandatory.
6. It gives concrete risks and actions, not motivational or generic advice.

If any rule fails, mark the audit `invalid_off_context` and do not use it for decisions.

## Current Smoke Findings

- `ops/reports/antigravity_deepseek_auditor_smoke_20260425_230045.md` is invalid for product decision use because the output drifted into a generic product-picker bot.
- `ops/reports/antigravity_deepseek_auditor_constrained_20260425_230146.md` is invalid because manual PowerShell UTF-8 mode was not set and the Russian output was corrupted.
- `ops/reports/antigravity_deepseek_auditor_constrained_20260425_230256.md` is the first valid constrained DeepSeek audit artifact.

## Product Decision From The Valid Audit

DeepSeek marked the product `pilot-ready`, but its remediation advice included removing branded nutraceutical references and all dosages. This is too blunt for the product strategy.

Final project decision:

- Controlled concierge pilot may continue.
- Public launch remains blocked.
- Branded Siberian Wellness and Vitamax recommendations remain allowed only as cautious nutraceutical orientation, with conflict-of-interest transparency, safety gating, and human review.
- Dosages remain allowed only when they are supplement-label-based or project-policy-approved, not when they imply medical treatment or disease correction.

## Required Audit Prompt Template

Use this template inside Antigravity when asking DeepSeek to audit a dossier or change:

```text
Ты второй строгий аудитор продукта Telegram-бота Ольги Зинченко.

Контекст:
- Это премиальная нутрициологическая навигация, не диагноз и не лечение.
- Цена продукта: 6900 RUB.
- Human review перед выдачей клиенту обязателен.
- Клиент может присылать анкету, жалобы, питание, образ жизни, анализы, УЗИ, выписки и фото.
- Нужно проверить безопасность, персонализацию, красные флаги, вопросы к врачу, план 3 дня / 2 недели / 1-3 месяца, нутрицевтики Siberian Wellness и Vitamax.
- Запрещено: диагноз, лечение, терапия, лекарственные назначения, обещания результата.

Проверь материал ниже.

Формат ответа:
## Вердикт
pilot-ready / needs-human-fix / public-launch-blocked

## Критические риски
1. ...

## Что исправить до отправки клиенту
1. ...

## Что усилит премиальность
1. ...

## Что нельзя писать клиенту
1. ...

Материал для проверки:
[вставить текст]
```

## Operating Rule

DeepSeek is the critic. Codex is the orchestrator. Olga/human review is the delivery authority.
