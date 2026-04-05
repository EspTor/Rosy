#!/usr/bin/env python3
"""hermes-graphify: Standalone Hermes-compatible wrapper for graphify.

This script replaces the Claude Code skill orchestration with native Python
calls to graphify's library. It handles the full pipeline:

  1. Detect files in a directory
  2. AST extraction for code files (deterministic, no LLM)
  3. Semantic extraction for docs/papers/images (LLM - done by Hermes agent)
  4. Build graph, cluster, analyze
  5. Export (Obsidian, HTML, JSON, report)

Usage:
  python3 hermes_graphify.py <path> [--mode deep] [--update] [--no-viz]
  python3 hermes_graphify.py <path> --extract-only    # Steps 1-3 only
  python3 hermes_graphify.py <path> --build-only      # Steps 4-6 from existing extraction.json
"""
from __future__ import annotations
import argparse
import json
import math
import sys
import time
from pathlib import Path


# -- Step 1: Detect -----------------------------------------------------------

def detect_files(input_path: Path) -> dict:
    """Scan directory and classify files."""
    from graphify.detect import detect
    result = detect(input_path)
    return result


def print_detection(detect: dict) -> None:
    """Print a clean detection summary."""
    files = detect.get("files", {})
    total = detect.get("total_files", 0)
    words = detect.get("total_words", 0)
    skipped = detect.get("skipped_sensitive", 0)

    print(f"Corpus: {total} files, ~{words:,} words")
    for category, paths in files.items():
        if paths:
            exts = " ".join(set(Path(p).suffix for p in paths[:5]))
            print(f"  {category}: {len(paths)} files ({exts})")
    if skipped:
        print(f"  skipped_sensitive: {skipped} files (names hidden)")


# -- Step 2: AST Extraction ---------------------------------------------------

def extract_code(detect: dict) -> dict:
    """Extract nodes/edges from code files using tree-sitter AST."""
    from graphify.extract import collect_files, extract

    code_files = []
    for f in detect.get("files", {}).get("code", []):
        p = Path(f)
        if p.is_dir():
            code_files.extend(collect_files(p))
        else:
            code_files.append(p)

    if code_files:
        result = extract(code_files)
        print(f"AST: {len(result['nodes'])} nodes, {len(result['edges'])} edges")
        return result
    print("No code files - skipping AST extraction")
    return {"nodes": [], "edges": []}


# -- Step 3: Semantic Extraction -----------------------------------------------
# This is the key difference from Claude Code. Instead of dispatching subagents,
# we output a manifest of files that need semantic extraction. The Hermes agent
# then processes each file using its native read_file/vision_analyze tools.

def get_semantic_manifest(detect: dict) -> dict:
    """Return a list of non-code files that need semantic extraction.

    Returns: {"docs": [...], "papers": [...], "images": [...]}
    Each value is a list of file paths.
    """
    semantic_files: dict[str, list[str]] = {}

    for category, paths in detect.get("files", {}).items():
        if category == "code" or not paths:
            continue
        semantic_files[category] = list(paths)

    return semantic_files


def save_semantic_manifest(manifest: dict, out_path: Path) -> None:
    """Write the manifest as JSON so the Hermes agent can read it."""
    out_path.write_text(json.dumps(manifest, indent=2))


def merge_extraction(ast: dict, semantic: dict) -> dict:
    """Merge AST and semantic extraction results."""
    seen = {n["id"] for n in ast["nodes"]}
    merged_nodes = list(ast["nodes"])
    for n in semantic["nodes"]:
        if n["id"] not in seen:
            merged_nodes.append(n)
            seen.add(n["id"])

    merged_edges = ast["edges"] + semantic["edges"]
    return {
        "nodes": merged_nodes,
        "edges": merged_edges,
        "input_tokens": semantic.get("input_tokens", 0),
        "output_tokens": semantic.get("output_tokens", 0),
    }


# -- Step 4: Build, Cluster, Analyze, Export -----------------------------------

def build_and_export(
    extraction: dict,
    detect: dict,
    input_path: str,
    output_dir: Path,
    labels: dict[int, str] | None = None,
    export_html: bool = True,
    export_obsidian: bool = True,
) -> dict:
    """Run the graph build, cluster, analyze pipeline and export."""
    from graphify.build import build_from_json
    from graphify.cluster import cluster, score_all
    from graphify.analyze import god_nodes, surprising_connections, suggest_questions
    from graphify.report import generate
    from graphify.export import to_json, to_obsidian, to_canvas, to_html

    G = build_from_json(extraction)
    communities = cluster(G)
    cohesion = score_all(G, communities)

    if labels is None:
        labels = {cid: f"Community {cid}" for cid in communities}

    gods = god_nodes(G)
    surprises = surprising_connections(G, communities)
    questions = suggest_questions(G, communities, labels)

    tokens = {
        "input": extraction.get("input_tokens", 0),
        "output": extraction.get("output_tokens", 0),
    }
    report = generate(
        G, communities, cohesion, labels, gods, surprises,
        detect, tokens, input_path, suggested_questions=questions,
    )

    results = {
        "communities": {str(k): v for k, v in communities.items()},
        "cohesion": {str(k): v for k, v in cohesion.items()},
        "labels": {str(k): v for k, v in labels.items()},
        "gods": gods,
        "surprises": surprises,
        "questions": questions,
        "num_nodes": G.number_of_nodes(),
        "num_edges": G.number_of_edges(),
        "num_communities": len(communities),
    }

    if G.number_of_nodes() == 0:
        print("ERROR: Empty graph - extraction produced no nodes.")
        results["error"] = "empty_graph"
        return results

    output_dir.mkdir(parents=True, exist_ok=True)

    # Always write graph.json
    to_json(G, communities, str(output_dir / "graph.json"))

    # Write report
    (output_dir / "GRAPH_REPORT.md").write_text(report)

    # Write analysis JSON for later labeling step
    (output_dir / "analysis.json").write_text(json.dumps(results, indent=2))

    if export_obsidian:
        to_obsidian(
            G, communities, str(output_dir / "obsidian"),
            community_labels=labels, cohesion=cohesion,
        )
        to_canvas(
            G, communities, str(output_dir / "obsidian" / "graph.canvas"),
            community_labels=labels,
        )
        obsidian_count = len(list((output_dir / "obsidian").glob("*.md")))
        print(f"Obsidian vault: {output_dir}/obsidian ({obsidian_count} files)")
        print(f"Canvas: {output_dir}/obsidian/graph.canvas")

    if export_html and G.number_of_nodes() <= 5000:
        to_html(G, communities, str(output_dir / "graph.html"), community_labels=labels)
        print(f"HTML: {output_dir}/graph.html")
    elif G.number_of_nodes() > 5000:
        print(f"Graph has {G.number_of_nodes()} nodes - too large for HTML. Use Obsidian instead.")

    print(f"Graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges, {len(communities)} communities")

    return results


# -- Label Regeneration --------------------------------------------------------

def relabel_and_export(
    extraction: dict,
    detect: dict,
    labels: dict[int, str],
    output_dir: Path,
    input_path: str,
) -> dict:
    """Re-run export with new community labels."""
    from graphify.build import build_from_json
    from graphify.cluster import cluster, score_all
    from graphify.analyze import god_nodes, surprising_connections, suggest_questions
    from graphify.report import generate
    from graphify.export import to_json, to_obsidian, to_canvas, to_html

    G = build_from_json(extraction)
    communities = cluster(G)
    cohesion = score_all(G, communities)

    gods = god_nodes(G)
    surprises = surprising_connections(G, communities)
    questions = suggest_questions(G, communities, labels)

    tokens = {"input": 0, "output": 0}
    report = generate(
        G, communities, cohesion, labels, gods, surprises,
        detect, tokens, input_path, suggested_questions=questions,
    )

    to_json(G, communities, str(output_dir / "graph.json"))
    (output_dir / "GRAPH_REPORT.md").write_text(report)
    to_obsidian(G, communities, str(output_dir / "obsidian"), community_labels=labels, cohesion=cohesion)
    to_canvas(G, communities, str(output_dir / "obsidian" / "graph.canvas"), community_labels=labels)
    if G.number_of_nodes() <= 5000:
        to_html(G, communities, str(output_dir / "graph.html"), community_labels=labels)

    print(f"Re-exported with labels: {labels}")
    return {"num_nodes": G.number_of_nodes(), "num_edges": G.number_of_edges()}


# -- Main ----------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Hermes-compatible graphify pipeline",
    )
    parser.add_argument("path", default=".", nargs="?", help="Input directory or file path")
    parser.add_argument("--mode", default="normal", choices=["normal", "deep"],
                        help="Extraction mode (deep = more aggressive inference)")
    parser.add_argument("--extract-only", action="store_true",
                        help="Only run detection + AST extraction, output manifest for agent")
    parser.add_argument("--build-only", action="store_true",
                        help="Only run build/cluster/analyze/export from existing extraction.json")
    parser.add_argument("--output", "-o", default="graphify-out", help="Output directory")
    parser.add_argument("--no-viz", action="store_true", help="Skip HTML/Obsidian export")
    parser.add_argument("--semantic", type=str,
                        help="Path to semantic extraction JSON file (overrides --extract-only)")
    parser.add_argument("--labels", type=str,
                        help="Path to labels JSON file for re-export (e.g., {\"0\":\"Community A\",\"1\":\"Community B\"})")

    args = parser.parse_args()
    input_path = Path(args.path).resolve()
    output_dir = Path(args.output)

    if not input_path.exists():
        print(f"Error: {input_path} does not exist", file=sys.stderr)
        sys.exit(1)

    # -- Build-only mode: read existing extraction.json ------------------------

    if args.build_only or args.labels:
        # Check for extraction.json
        extraction_path = input_path / ".graphify_extract.json"
        if not extraction_path.exists():
            # Check for graph.json in output dir
            graph_out = output_dir / "graph.json"
            if graph_out.exists():
                extraction = json.loads(graph_out.read_text())
                # graph.json has different format, try to reconstruct or use as-is
                print(f"Using graph.json from {graph_out}")
            else:
                print(f"Error: No extraction.json found. Run --extract-only first.", file=sys.stderr)
                sys.exit(1)
        else:
            extraction = json.loads(extraction_path.read_text())

        detect_path = input_path / ".graphify_detect.json"
        detect = json.loads(detect_path.read_text()) if detect_path.exists() else {}

        if args.labels:
            labels_data = json.loads(Path(args.labels).read_text())
            labels = {int(k): v for k, v in labels_data.items()}
            relabel_and_export(extraction, detect, labels, output_dir, str(input_path))
        elif args.build_only:
            # Try to load labels from analysis.json
            label_map = None
            analysis_path = output_dir / "analysis.json"
            if analysis_path.exists():
                analysis = json.loads(analysis_path.read_text())
                raw_labels = analysis.get("labels", {})
                label_map = {int(k): v for k, v in raw_labels.items()} if raw_labels else None
            build_and_export(
                extraction, detect, str(input_path), output_dir,
                labels=label_map,
                export_html=not args.no_viz,
                export_obsidian=not args.no_viz,
            )
        return

    # -- Extract mode: detect + AST + manifest --------------------------------

    print(f"Detecting files in {input_path}...")
    detect_result = detect_files(input_path)
    (input_path / ".graphify_detect.json").write_text(json.dumps(detect_result, indent=2))

    print_detection(detect_result)

    total = detect_result.get("total_files", 0)
    if total == 0:
        print("No supported files found.")
        sys.exit(1)

    if total > 200 or detect_result.get("total_words", 0) > 2000000:
        print("WARNING: Large corpus detected (>200 files or >2M words).")
        print("Consider running on a subfolder. Continuing anyway...")

    # AST extraction
    print("\nRunning AST extraction on code files...")
    ast_result = extract_code(detect_result)

    if args.extract_only:
        # Save AST result and manifest
        (input_path / ".graphify_ast.json").write_text(json.dumps(ast_result, indent=2))

        # Save semantic manifest
        manifest = get_semantic_manifest(detect_result)
        (input_path / ".graphify_semantic_manifest.json").write_text(json.dumps(manifest, indent=2))

        # Save placeholder semantic result
        semantic_result = {"nodes": [], "edges": [], "input_tokens": 0, "output_tokens": 0}

        # If user provided a semantic extraction file, use it
        if args.semantic:
            semantic_data = json.loads(Path(args.semantic).read_text())
            # Handle format: could be a single JSON or list of JSONs
            if isinstance(semantic_data, list):
                all_nodes = []
                all_edges = []
                for chunk in semantic_data:
                    all_nodes.extend(chunk.get("nodes", []))
                    all_edges.extend(chunk.get("edges", []))
                semantic_result = {
                    "nodes": all_nodes,
                    "edges": all_edges,
                    "input_tokens": 0,
                    "output_tokens": 0,
                }
            else:
                semantic_result = semantic_data

        # Merge and save extraction
        merged = merge_extraction(ast_result, semantic_result)
        (input_path / ".graphify_extract.json").write_text(json.dumps(merged, indent=2))

        # Build and export if semantic data was provided
        if semantic_result["nodes"] or semantic_result["edges"]:
            print("\nRunning build pipeline...")
            build_and_export(
                merged, detect_result, str(input_path), output_dir,
                export_html=not args.no_viz,
                export_obsidian=not args.no_viz,
            )
        else:
            print("\nSemantic extraction manifest saved to:")
            print(f"  {input_path}/.graphify_semantic_manifest.json")
            print("\nProcess the files in the manifest using Hermes read_file() and vision_analyze(),")
            print("then merge the results and re-run with --build-only.")
            print("\nManifest categories and file counts:")
            for category, paths in manifest.items():
                print(f"  {category}: {len(paths)} files")
                for p in paths[:10]:
                    print(f"    - {p}")
                if len(paths) > 10:
                    print(f"    ... and {len(paths) - 10} more")

        return

    # -- Full pipeline: semantic extraction + build ----------------------------
    # For full pipeline without manifest, the caller should provide semantic data.
    # If no semantic data, just run AST-only build.

    semantic_result = {"nodes": [], "edges": [], "input_tokens": 0, "output_tokens": 0}

    # Check for semantic extraction results provided via flag
    if args.semantic:
        print(f"Loading semantic extraction from {args.semantic}...")
        semantic_data = json.loads(Path(args.semantic).read_text())
        if isinstance(semantic_data, list):
            all_nodes = []
            all_edges = []
            for chunk in semantic_data:
                all_nodes.extend(chunk.get("nodes", []))
                all_edges.extend(chunk.get("edges", []))
            semantic_result = {
                "nodes": all_nodes,
                "edges": all_edges,
                "input_tokens": 0,
                "output_tokens": 0,
            }
        else:
            semantic_result = semantic_data

    # If there are non-code files but no semantic data, warn
    has_non_code = any(
        v
        for k, v in detect_result.get("files", {}).items()
        if k != "code"
    )
    if has_non_code and not semantic_result["nodes"]:
        manifest = get_semantic_manifest(detect_result)
        if manifest:
            total_non_code = sum(len(v) for v in manifest.values())
            print(f"\nWARNING: {total_non_code} non-code files detected but no semantic extraction provided.")
            print("These files will not contribute to the graph.")
            print("Use --extract-only to get a manifest of files to process,")
            print("then provide semantic results via --semantic.")

    print("\nMerging extraction results...")
    merged = merge_extraction(ast_result, semantic_result)
    (input_path / ".graphify_extract.json").write_text(json.dumps(merged, indent=2))

    print("\nRunning build pipeline...")
    build_and_export(
        merged, detect_result, str(input_path), output_dir,
        export_html=not args.no_viz,
        export_obsidian=not args.no_viz,
    )

    print(f"\nOutputs written to {output_dir}/")


if __name__ == "__main__":
    main()
