#!/usr/bin/env python3
"""Summarize Claude Code stream-json NDJSON without copying prompts or tool payloads.

Use on trusted local traces only. Outputs event kinds and tool names, never
message text, arguments, result contents, session IDs or file paths.
"""
import argparse
import json
from collections import Counter
from pathlib import Path


def summarize(lines):
    events = []
    parse_errors = 0
    for line in lines:
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
        except (json.JSONDecodeError, TypeError):
            parse_errors += 1
            continue
        if not isinstance(obj, dict):
            parse_errors += 1
            continue
        kind = obj.get("type")
        if kind == "stream_event":
            # Token-level deltas would duplicate full assistant/user messages.
            continue
        if kind in ("assistant", "user"):
            message = obj.get("message")
            if not isinstance(message, dict):
                continue
            blocks = message.get("content", [])
            if not isinstance(blocks, list):
                continue
            for block in blocks:
                if not isinstance(block, dict):
                    continue
                bt = block.get("type")
                if kind == "assistant" and bt == "tool_use":
                    events.append({"kind": "tool_request", "tool": block.get("name", "unknown")})
                elif kind == "user" and bt == "tool_result":
                    events.append({"kind": "tool_result", "error": bool(block.get("is_error", False))})
                elif kind == "assistant" and bt == "text":
                    events.append({"kind": "assistant_text"})
        elif kind == "result":
            events.append({"kind": "run_end", "status": obj.get("subtype", "unknown"),
                           "is_error": bool(obj.get("is_error", False))})
        elif kind == "system" and obj.get("subtype") == "init":
            events.append({"kind": "run_init"})
    counts = dict(sorted(Counter(x["kind"] for x in events).items()))
    tool_counts = dict(sorted(Counter(x.get("tool", "unknown") for x in events if x["kind"] == "tool_request").items()))
    return {"schema": "a0-02-event-summary-v1", "scope": "observable CLI NDJSON only",
            "counts": counts, "tools": tool_counts, "parse_errors": parse_errors,
            "events": events, "limitations": [
                "No user prompts, tool arguments or result contents retained",
                "No inference about internal queryLoop/queryModel functions",
                "Missing events may reflect stream visibility or truncation",
                "Tool requests and results are not paired by ID in this privacy-reduced output",
            ]}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("stream", type=Path, help="local Claude Code stream-json NDJSON")
    ap.add_argument("--out", type=Path, help="safe summary JSON output file")
    args = ap.parse_args()
    with args.stream.open(encoding="utf-8") as fp:
        output = summarize(fp)
    text = json.dumps(output, indent=2, ensure_ascii=False) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
