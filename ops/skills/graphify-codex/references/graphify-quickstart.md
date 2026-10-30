# Graphify Quickstart

## Purpose

Use this file for command details and operating assumptions when the `graphify-codex` skill triggers.

## Source Snapshot

This reference is distilled from:

- [graphify.net](https://graphify.net/)
- [safishamsi/graphify](https://github.com/safishamsi/graphify)

## What Graphify Is

Graphify builds a queryable knowledge graph from code, docs, PDFs, and images. It combines local parsing and graph construction with model-assisted semantic extraction, then exports artifacts such as:

- `graphify-out/graph.html`
- `graphify-out/graph.json`
- `graphify-out/GRAPH_REPORT.md`

The site states the PyPI package name is currently `graphifyy`, while the CLI command remains `graphify`.

## Install

```bash
pip install graphifyy && graphify install
```

Windows note from the upstream README:

- if `graphify` is not recognized, the Python Scripts directory may be missing from `PATH`
- `pipx install graphifyy` is the cleaner Windows option when available

## Core Commands

```bash
graphify .
graphify . --update
graphify . --mode deep
graphify query "what connects X to Y?"
graphify path "NodeA" "NodeB"
graphify explain "SomeModule"
graphify . --wiki
graphify . --svg
graphify . --graphml
graphify . --neo4j
graphify . --mcp
graphify . --watch
graphify add https://example.com/resource
graphify hook install
```

## When To Use Which Command

- Use `graphify .` for first-time repo mapping.
- Use `--update` when outputs already exist and the repo changed.
- Use `query` for thematic exploration.
- Use `path` for dependency or concept linkage.
- Use `explain` for one module or concept.
- Use `--wiki` when another agent should traverse Markdown files instead of JSON.
- Use `--mcp` only when the user explicitly wants a served tool surface.
- Use `--watch` only for long-lived local sync workflows.

## Graphify Mental Model

Prefer these concepts in your explanation:

- `god nodes`: highest-degree nodes near the center of the system
- `surprises`: unexpected links across files, layers, or modalities
- `communities`: structural clusters of related concepts
- `inferred` vs `extracted`: separate confident findings from weaker links

## Fallback Mode

If the CLI is unavailable, emulate Graphify’s outcome manually:

1. identify likely central modules
2. trace cross-layer edges
3. name surprising couplings
4. extract a short list of high-value questions

Do not pretend a real graph was built when it was not.
