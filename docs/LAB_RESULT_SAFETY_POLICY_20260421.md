# Lab Result Safety Policy

Date: 2026-04-21
Owner: Olga / Wellness Bot
Purpose: prevent wrong biomarker interpretation from poor-quality uploads or ambiguous OCR extraction.

## Non-Negotiable Rule

The system must not interpret uncertain lab values as if they were confirmed.

If the photo or scan quality is weak, the correct behavior is:

1. stop automatic interpretation,
2. ask the client to resend a clearer file,
3. avoid building recommendations on doubtful values.

## Why This Rule Exists

Wrong biomarker extraction creates a dangerous chain:

- wrong number,
- wrong hypothesis,
- wrong supplement logic,
- wrong client guidance.

It is better to lose automation than to keep false certainty.

## Product Rule

If lab quality is low:

- parsed biomarkers are not treated as trusted evidence,
- the bot asks for a better photo, PDF, or manual text entry,
- the dossier should rely on symptoms and context only until numbers are confirmed.

## What Counts As Low Quality

- text is too short or fragmented,
- too few readable numeric lines,
- visible OCR corruption,
- no clear biomarker lines can be extracted.

## Reply Rule For The Client

The message should be direct and calm:

- do not pretend the values are readable,
- do not guess,
- explain that a clearer upload is needed to avoid mixing up results.

## Dossier Rule

If `requires_lab_resubmission == true`, the model must not:

- interpret parsed biomarkers as facts,
- build supplement schemes from those values,
- write confident lab-based conclusions.

Instead, it should explicitly treat the labs as unconfirmed.
