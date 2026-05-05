# HERMES-20260505-004: Product Sync Audit (Phase 5)

## Таблица сверки

| Source | Current Value | Expected Value | Mismatch | Risk | Fix |
|--------|--------------|----------------|----------|------|-----|
| payment_flow.py:9 | week = 3900 | 3900 | ✅ | — | — |
| payment_flow.py:15 | premium = 6900 | 6900 | ✅ | — | — |
| payment_flow.py:21 | vip = 14900 | 14900 | ✅ | — | — |
| texts.py:132 | week = 3900 | 3900 | ✅ | — | — |
| texts.py:146 | premium = 6900 | 6900 | ✅ | — | — |
| texts.py:164 | vip = 14900 | 14900 | ✅ | — | — |
| mini-app/index.html | 2990 | 3900/6900/14900 | ❌ | Юридический: клиент видит неверную цену | Заменить на 3900/6900/14900 |
| mini-app/index.html | ferritin, vit D, cortisol findings | placeholder | ❌ | Медицинский: хардкод диагнозов | Убрать, заменить placeholder |
| PRODUCT_LINE_V2 | 3900/6900/14900 | — | ✅ | — | — |
| SINGLE_SOURCE_OF_TRUTH | 3900/6900/14900 | — | ✅ | — | — |
| texts.py:24 | «Я бы не делала из этого бесконечный магазин услуг» | — | ⚠️ | Разговорный тон в меню | Оставить (допустимо) |
| texts.py:34 | PRODUCT_EXAMPLES_TEXT | demo example | ⚠️ | Длинный (30 строк) | Сократить |
| payment_flow.py:57 | build_invoice_payload: "premium:" | offer_code | ❌ | week-клиент получает premium-префикс | Использовать offer['code'] |
| ai_drafting.py:91 | "premium wellness dossier" | "премиальное досье" | ❌ | Английский в русском интерфейсе | Заменить |
| ai_drafting.py:151 | CTA_DEFAULT_TEXT: "Premium Wellness Dossier" | Русский текст | ❌ | Английский | Заменить |
| prompts.py:232 | DOSSIER_DRAFT_PROMPT: English | Russian | ❌ | Противоречие правилам | Перевести |
| config.py:229 | PAYMENT_MODE=manual | manual | ✅ | — | — |

## Итого

- ✅ Совпадений: 11
- ❌ Расхождений: 6 (из них 4 критические)
- ⚠️ Допустимо/спорно: 2
