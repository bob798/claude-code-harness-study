#!/usr/bin/env python3
"""Privacy-minimized aggregate of native Claude Code session JSONL.
Only metadata, tool names, and counts are exported; no prompts or raw records.
"""
import argparse
import json
from collections import Counter
from pathlib import Path

def blocks(entry):
    msg = entry.get("message")
    if not isinstance(msg, dict):
        return []
    items = msg.get("content")
    return items if isinstance(items, list) else []

def analyze(lines):
    requests, responses = {}, {}
    malformed = duplicates = errors = processed = 0
    models, versions, tools = Counter(), Counter(), Counter()
    timeline = []
    for line in lines:
        if not line.strip():
            continue
        try:
            entry = json.loads(line)
        except (ValueError, TypeError):
            malformed += 1
            continue
        if not isinstance(entry, dict):
            malformed += 1
            continue
        processed += 1
        if isinstance(entry.get("version"), str):
            versions[entry["version"]] += 1
        role = entry.get("type")
        msg = entry.get("message")
        if role == "assistant" and isinstance(msg, dict) and isinstance(msg.get("model"), str):
            models[msg["model"]] += 1
        for b in blocks(entry):
            if not isinstance(b, dict):
                continue
            if role == "assistant" and b.get("type") == "tool_use":
                name = b.get("name") if isinstance(b.get("name"), str) else "unknown"
                key = b.get("id")
                tools[name] += 1
                if isinstance(key, str):
                    if key in requests:
                        duplicates += 1
                    requests[key] = {"ordinal": len(timeline)}
                timeline.append("tool_request")
            elif role == "user" and b.get("type") == "tool_result":
                key = b.get("tool_use_id")
                if isinstance(key, str):
                    responses[key] = bool(b.get("is_error", False))
                errors += bool(b.get("is_error", False))
                timeline.append("tool_result")
    paired = set(requests) & set(responses)
    followed = sum("tool_request" in timeline[requests[k]["ordinal"]+1:] for k in paired)
    return {
        "schema": "a002b-session-aggregate-v1",
        "source_format": "claude-code-session-jsonl",
        "parsed_entries": processed, "malformed_entries": malformed,
        "tool_requests_with_id": len(requests), "tool_results_with_id": len(responses),
        "paired_requests": len(paired),
        "requests_without_observed_result": len(set(requests)-set(responses)),
        "results_without_observed_request": len(set(responses)-set(requests)),
        "duplicate_request_id_occurrences": duplicates,
        "error_results": errors,
        "paired_requests_with_later_tool_request": followed,
        "tool_name_counts": dict(sorted(tools.items())),
        "model_counts": dict(sorted(models.items())),
        "cli_version_counts": dict(sorted(versions.items())),
        "not_inferred": [
            "No inference of internal queryLoop or private functions",
            "Unpaired request does not prove a runtime bug",
            "Later tool call does not establish causal recovery",
            "Interrupt or resume cannot be inferred from absence of metadata",
            "Raw prompts, outputs, paths and IDs are not retained"
        ]
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    with args.source.open(encoding="utf-8") as f:
        result = analyze(f)
    body = json.dumps(result, indent=2, ensure_ascii=False)+"\n"
    if args.out:
        args.out.write_text(body, encoding="utf-8")
    else:
        print(body, end="")

if __name__ == "__main__":
    main()
