---
name: graphify-codex
description: Build, inspect, and query Graphify knowledge graphs for codebases, mixed repositories, and architecture-heavy projects. Use when Codex needs repo structure discovery, cross-file dependency mapping, code-to-doc linkage, graph-based explanation of system design, Graphify install/run guidance, or a Graphify-style fallback audit when the `graphify` CLI is unavailable.
---

# Graphify Codex

Use Graphify as the default path for graph-based repository understanding, then fall back to a manual graph-oriented audit when the CLI is unavailable in the current environment.

Start by running [`scripts/probe_graphify.ps1`](scripts/probe_graphify.ps1). Use its result to decide whether to build/query a real Graphify graph or switch to fallback mode.

Read [`references/graphify-quickstart.md`](references/graphify-quickstart.md) only when you need command details, output layout, or install notes.

## Workflow

### 1. Probe the environment

Run:

```powershell
powershell -ExecutionPolicy Bypass -File "<skill-dir>\scripts\probe_graphify.ps1" -ProjectRoot "<target-repo>"
```

Use the probe result to answer four questions:

- Is `graphify` on `PATH`?
- Is Python available for install/use?
- Does the repo already contain `graphify-out/graph.json` or `GRAPH_REPORT.md`?
- Should you build, update, query, or fall back?

If the repo already has fresh Graphify outputs, prefer querying before rebuilding.

### 2. Choose the operating mode

Use this decision rule:

- Build mode: no existing graph and the user wants structural understanding of a repo or corpus.
- Update mode: `graphify-out/graph.json` exists and the repo changed.
- Query mode: the user asks architecture questions, dependency paths, explanation of a module, or cross-domain links.
- Export mode: the user wants HTML, JSON, wiki, SVG, GraphML, Neo4j, or MCP output.
- Fallback mode: `graphify` is unavailable, install is not feasible, or the environment is offline/restricted.

### 3. Run Graphify when available

Use the smallest command that answers the request.

Typical sequence:

```powershell
graphify .
graphify query "what connects payments to dossier generation?"
graphify path "PaymentFlow" "pdf_generator"
graphify explain "governance_service"
```

Prefer `graphify . --update` over a full rebuild when the graph already exists.

Use deeper or broader modes only when the user explicitly needs them:

- `--mode deep` for more aggressive inferred edges
- `--wiki` for agent-readable Markdown knowledge base
- `--mcp` when the user wants a served graph tool surface
- `--watch` only when a long-lived local sync loop is useful

### 4. Interpret outputs

Treat these artifacts as the primary surfaces:

- `graphify-out/GRAPH_REPORT.md`: summary, god nodes, surprising links, suggested questions
- `graphify-out/graph.json`: persistent queryable graph
- `graphify-out/graph.html`: interactive visualization

When reporting findings, mirror Graphify’s framing:

- Core nodes: the modules or concepts with the most system reach
- Important paths: shortest or strongest links between user-named concepts
- Surprises: non-obvious cross-file or cross-domain connections
- Blind spots: places where the graph is sparse, inferred, or likely incomplete

### 5. Fall back in Graphify style when the CLI is unavailable

Do not stop at “Graphify is not installed.” Run a manual graph-oriented audit.

Build a compact substitute with these sections:

1. Candidate god nodes
2. High-value edges
3. Cross-layer paths
4. Surprising couplings
5. Suggested next questions

Approximate the graph by reading:

- entrypoints
- config files
- service modules
- key docs
- integration scripts
- test files that reveal intended behavior

Prefer explicit evidence over speculation. Mark uncertain edges as inferred.

### 6. Tailor the response to the user’s actual goal

If the user wants implementation help, convert graph findings into an action plan.

If the user wants architecture understanding, answer with nodes, edges, and paths rather than generic summaries.

If the user wants onboarding, point them first to `GRAPH_REPORT.md`, then to specific paths or communities.

## Windows Notes

On Windows, `graphify` may install successfully while remaining off `PATH`. Use `pipx install graphifyy` when possible. Otherwise check the Python Scripts directory noted in [`references/graphify-quickstart.md`](references/graphify-quickstart.md).

## Output Contract

When using this skill, return:

- whether Graphify was available
- whether you built, updated, queried, or fell back
- the most important nodes, paths, and surprises
- the next command or action the user should take

Keep the answer structural and decision-oriented.
