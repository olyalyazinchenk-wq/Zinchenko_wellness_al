# Helix Master Catalog Policy

Date: 2026-04-21
Owner: Olga / Wellness Bot
Purpose: define how the project should use the official Helix catalog as the master list of analyses while keeping nutritiological interpretation as a separate layer.

## Core Rule

The analysis catalog in the product should mirror the official Helix catalog structure.

That means:

- official Helix names,
- official Helix codes,
- official Helix categories,
- official Helix service grouping,

should come from the Helix catalog layer, not from improvised internal naming.

## Interpretation Rule

The master catalog and the interpretation layer are not the same thing.

Correct architecture:

1. Helix master catalog
2. nutritiological overlay

The Helix layer answers:

- what the analysis is called,
- what code it has,
- what category it belongs to.

The nutritiological layer answers:

- what range is treated as nutritionally optimal,
- whether the value looks below / within / above that internal target,
- whether the product can interpret this marker in nutrition-navigation mode.

## Why This Separation Matters

If these layers are mixed together, the project becomes fragile:

- catalog naming drifts,
- codes become inconsistent,
- interpretation logic becomes hard to audit,
- future updates from Helix become painful.

## Source Status

As of 2026-04-21, the official Helix site states that the catalog contains more than 3600 analyses and exposes top-level categories for all analyses and for preventive medicine / nutrition.

Source pages used:

- [Helix main catalog navigation](https://helix.ru/)
- [Helix preventive medicine and nutrition category](https://helix.ru/elec/catalog/preventivnaya-medicina-i-nutriciologiya)

## Product Decision

The project should not hand-write a fake "full Helix catalog" from memory.

The correct implementation is:

- mirror the official Helix catalog,
- preserve official names and codes,
- then map nutritiological interpretation marker-by-marker.

## Current Engineering Status

The project now contains:

- a Helix master-catalog metadata layer,
- official top-level Helix category structure,
- a separate nutritiological reference overlay,
- starter coverage for a limited marker set.

This is the correct architecture for later expansion to the full Helix list.
