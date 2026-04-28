# Nutrition Reference Framework

Date: 2026-04-21
Owner: Olga / Wellness Bot
Purpose: make nutritiological ranges the primary interpretation layer for lab discussion inside the product.

## Core Rule

When the bot interprets confirmed lab values, it should anchor the explanation first to nutritiological ranges, not to the laboratory printout band.

The laboratory reference range may stay in the source data, but it is not the main interpretive frame for the wellness breakdown.

## Why This Matters

Many clients come with the exact problem:

- "по лаборатории всё нормально",
- but the picture still feels weak,
- and the nutritiological task is to notice suboptimal patterns earlier and more coherently.

That means the product should not collapse into:

- "в референсе, значит всё хорошо".

## Product Implementation Rule

The system now separates two layers:

1. laboratory source range
2. nutritiological optimal range

For structured biomarkers the main interpretation layer is:

- `nutrition_optimal_range`
- `nutrition_status`
- `nutrition_range_basis`

## Important Boundary

This does not mean:

- diagnosis,
- treatment,
- ignoring red flags,
- ignoring urgent medical context.

It means the wellness interpretation layer is built around nutritiological targets while still preserving safety boundaries.

## Current Starter Catalog

The current starter catalog covers a conservative first set of markers:

- ferritin
- vitamin D
- TSH
- vitamin B12
- fasting glucose
- HbA1c

This catalog is designed as an internal product layer and should be reviewed by Olga as the domain owner.

## Safety Rule

If OCR quality is weak:

- do not interpret either laboratory or nutritiological range,
- request a clearer file,
- do not build a supplement scheme from uncertain numbers.
