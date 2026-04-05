# Hermes Graphify

A [graphify](https://github.com/safishamsi/graphify) adaptation for Hermes — drop any files (code, papers, docs, images) into a folder and get a navigable knowledge graph with community detection, "god nodes", surprising connections, and interactive visualizations.

## What Is It

Graphify is a knowledge graph builder. The original was a Claude Code skill, but **only the semantic extraction step needs an LLM** — everything else (code parsing, graph building, community detection, analysis, exports) is pure Python.

This adaptation replaces the Claude-specific orchestration with Hermes's native file-reading and vision tools.

## Quick Start

```bash
pip install graphifyy --break-system-packages
python3 graphify_pipeline.py ./my_folder
```

Produces:
- `graphify-out/graph.html` — interactive browser visualization  
- `graphify-out/obsidian/` — Obsidian vault  
- `graphify-out/graph.json` — persistent graph data  
- `graphify-out/GRAPH_REPORT.md` — analysis report  

## How It Works

```
detect.py  →  AST extraction (code, no LLM)  →  semantic extraction (Hermes reads files)  →  build  →  cluster  →  export
```

Only the **semantic extraction** step uses an LLM. Code files are parsed via tree-sitter AST — zero LLM cost.

## Pipeline

### 1. Install

```bash
pip install graphifyy --break-system-packages
```

### 2. Run Full Pipeline

```bash
python3 graphify_pipeline.py ./my_research_folder
```

This runs detection, AST extraction, then outputs a manifest of files needing semantic extraction. The Hermes agent processes those files and merges results automatically.

### 3. With Pre-extracted Semantic Data

```bash
python3 graphify_pipeline.py ./my_research_folder --semantic semantic_result.json
```

### 4. Re-label Communities

```bash
python3 graphify_pipeline.py ./my_research_folder --build-only --labels labels.json
```

## Key Features

| Feature | Description |
|---|---|
| **God nodes** | Highest-connectivity concepts — what everything ties together through |
| **Surprising connections** | Non-obvious relationships ranked by a composite score (cross-file-type, cross-repo, cross-community) |
| **Suggested questions** | Questions the graph is uniquely positioned to answer |
| **Token benchmark** | On large corpora: 71.5x fewer tokens per query vs raw files |
| **Persistent graph** | Query `graph.json` weeks later without re-reading files |
| **Multiple exports** | HTML, Obsidian vault, Canvas, JSON, Neo4j Cypher, SVG, GraphML |

## What Hermes Handles Differently

| Original (Claude Code) | Hermes |
|---|---|
| Parallel Agent subagents | Sequential file processing via `read_file()` |
| Claude API for extraction | Whatever LLM Hermes is configured with |
| `/graphify` trigger | Python script invocation |
| Temp files for coordination | Direct Python integration |

## Example Use Cases

- **Research corpus** — Papers, notes, diagrams, and code → one navigable graph
- **Codebase onboarding** — Understand architecture before touching code
- **Obsidian vault enrichment** — Batch-import PDFs and notes with auto-linking
- **"What connects X to Y?"** — Find conceptual chains between any two nodes

## Architecture

```
hermes-graphify/
├── graphify_pipeline.py   # Main orchestrator (Hermes-native)
├── graphify_adapter/      # Supporting adapter module
└── README.md              # This file
```

The heavy lifting is done by `graphifyy` (PyPI):
- `graphify.detect` — file detection and classification  
- `graphify.extract` — tree-sitter AST parsing (Python, TS, Go, JS, Rust, Java, C++, C#, Ruby, Kotlin, Scala, PHP, C)  
- `graphify.build` — NetworkX graph construction  
- `graphify.cluster` — Leiden community detection via graspologic  
- `graphify.analyze` — god nodes, surprising connections, suggested questions  
- `graphify.report` — Markdown report generation  
- `graphify.export` — JSON, HTML, Obsidian, Canvas, Cypher, SVG, GraphML  
