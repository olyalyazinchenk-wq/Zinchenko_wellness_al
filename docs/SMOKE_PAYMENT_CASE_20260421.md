# Smoke Report: Payment / Case Flow

## Scope
- built a fresh submission payload from session data
- moved it through awaiting_payment -> enrichment -> paid state
- validated payment checks for good and bad scenarios
- restored a chat session from stored submission state

## Payment Context
```json
{
  "amount_rub": 6900,
  "amount_kop": 690000,
  "currency": "RUB",
  "invoice_payload": "premium:smoke_case_payment_001:<REDACTED_ID>",
  "invoice_sent_at": "2026-04-21T00:25:00Z",
  "expected_telegram_user_id": <REDACTED_ID>
}
```

## Validation Results
- good_payment_error: None
- wrong_amount_error: Сумма оплаты не совпадает с ожидаемой.
- wrong_user_error: Пользователь оплаты не совпадает с владельцем кейса.

## Enriched Submission
```json
{
  "submission_id": "smoke_case_payment_001",
  "offer": "premium",
  "profile": {
    "telegram_user_id": <REDACTED_ID>,
    "telegram_username": "Olgazinchenko1186",
    "telegram_full_name": "Ольга",
    "full_name": "Ольга",
    "age": 40,
    "city": "Москва",
    "anthropometrics": null,
    "contact": "telegram_current_chat"
  },
  "medical_context": {
    "symptoms": "Выпадение волос, усталость, ломкие ногти",
    "wellbeing_energy": null,
    "complaint_pattern": null,
    "goal": "Получить понятный нутрициологический разбор и план следующего шага",
    "work_lifestyle": null,
    "nutrition": null,
    "food_behavior": null,
    "digestion": null,
    "sleep_stress": null,
    "activity": null,
    "female_hormones": null,
    "hormonal_reproductive_context": null,
    "emotional_stress": null,
    "background": "Принимаю селен и белок",
    "risk_details": null,
    "motivation": null,
    "red_flags": "Нет",
    "lab_notes": "Анализы пока не приложены"
  },
  "documents": [],
  "parsed_biomarkers": [
    {
      "marker": "Ferritin",
      "value": "22"
    }
  ],
  "lab_confirmation_status": null,
  "lab_confirmation_needed": false,
  "pending_biomarker_confirmation": [],
  "lab_quality_check": null,
  "requires_lab_resubmission": false,
  "vision_analysis": "Клиент прислал фото анализов, нужен ручной follow-up.",
  "intake_status": "paid",
  "consent_given": true,
  "payment_status": "paid",
  "status_updated_at": "2026-04-21T00:27:00Z",
  "payment_context": {
    "amount_rub": 6900,
    "amount_kop": 690000,
    "currency": "RUB",
    "invoice_payload": "premium:smoke_case_payment_001:<REDACTED_ID>",
    "invoice_sent_at": "2026-04-21T00:25:00Z",
    "expected_telegram_user_id": <REDACTED_ID>
  },
  "enrichment_updated_at": "2026-04-21T00:26:00Z"
}
```

## Restored Session
```json
{
  "submission_id": "smoke_case_payment_001",
  "offer": "premium",
  "tier": "premium",
  "step": "done",
  "telegram_user_id": <REDACTED_ID>,
  "telegram_username": "Olgazinchenko1186",
  "telegram_full_name": "Ольга",
  "full_name": "Ольга",
  "age": 40,
  "city": "Москва",
  "anthropometrics": null,
  "contact": "telegram_current_chat",
  "documents": [],
  "symptoms": "Выпадение волос, усталость, ломкие ногти",
  "wellbeing_energy": null,
  "complaint_pattern": null,
  "goals": "Получить понятный нутрициологический разбор и план следующего шага",
  "work_lifestyle": null,
  "nutrition": null,
  "food_behavior": null,
  "digestion": null,
  "sleep_stress": null,
  "activity": null,
  "female_hormones": null,
  "hormonal_reproductive_context": null,
  "emotional_stress": null,
  "background": "Принимаю селен и белок",
  "risk_details": null,
  "motivation": null,
  "red_flags": "Нет",
  "lab_notes": "Анализы пока не приложены",
  "parsed_biomarkers": [
    {
      "marker": "Ferritin",
      "value": "22"
    }
  ],
  "lab_confirmation_status": null,
  "lab_confirmation_needed": false,
  "pending_biomarker_confirmation": [],
  "lab_quality_check": null,
  "requires_lab_resubmission": false,
  "consent_given": true
}
```

## Invoice Roundtrip
- payload_submission_id: smoke_case_payment_001
- payload_user_id: <REDACTED_ID>
- premium_price_rub: 6900
- premium_price_kop: 690000
