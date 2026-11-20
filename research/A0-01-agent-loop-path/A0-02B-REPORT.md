# A0-02b — Public Claude Code Session Evidence and Native JSONL Adapter

**Date:** 2026-11-20  
**Status:** PARTIAL: verified a real public session through Hugging Face's web viewer/raw preview; native-format parser and **five synthetic unit tests** are complete. **The raw session file was not downloaded into the execution container, so no quantitative counts from a full real file are claimed.**

## Scope and evidence grades

- **E-PUBLIC-VIEW**: inspection of a publicly hosted real user-contributed session, as displayed by the source. This is not our own execution or a machine-verified complete-file measurement.
- **E-SYNTHETIC**: local tests of the schema adapter with invented small input rows.
- **O/T**: official Claude Code public behavior vs third-party internal architecture reports. No internal source-level function assertion is established by public sessions.

## Source inventory

| Source | Data type | License / warning | Role |
|---|---|---|---|
| [Trace Commons](https://huggingface.co/datasets/trace-commons/agent-traces) | Raw contributed session JSONL, Claude Code among other agents | Dataset card: CC BY 4.0; traces can still contain sensitive data | Primary native-session format and future reproducible sampling |
| [Trace Commons example](https://huggingface.co/datasets/trace-commons/agent-traces/blob/main/sessions/claude_code/674e0f5c-c481-4830-b2ef-3e1e069a2b7f.jsonl) | Claude Code session, file 75 kB shown | Same dataset; raw file is not checked into this repo | Visually checked real public behavior and version |
| [ultralazr/claude-code-traces](https://huggingface.co/datasets/ultralazr/claude-code-traces) | Single redacted native JSONL | License listed as `other`; do not assume CC BY | Supplemental candidate, not primary without license review |
| [SyFI TraceLab](https://github.com/uw-syfi/TraceLab/releases) | Sanitized large-scale normalized traces | Use fixed release and dataset license when downloaded | Later aggregate workload analysis; not interchangeable with native sessions |

## Observations actually supported by the public session display

- The viewer identifies a **Claude Code v2.1.177** session in a `claude-vscode` entrypoint, with `claude-sonnet-4-6` assistant replies.
- An assistant displayed a group of tool calls (e.g. Bash and Write), followed by additional assistant responses and later tool work. The public UI supports that multi-step tool-backed workflow is observable.
- The viewer displays user interruptions in that same session. These show that interrupt annotations occur in *some* public traces, but do **not** establish precisely how in-flight tools were cancelled or what happened to pending external effects.
- These findings are from a **viewer**, not a full native-file programmatic parse. Do not turn them into a tool-pair matching ratio or claim all requests had results.

Original viewer: https://huggingface.co/datasets/trace-commons/agent-traces/blob/main/sessions/claude_code/674e0f5c-c481-4830-b2ef-3e1e069a2b7f.jsonl

## Native JSONL adapter

Previous `trace_summary.py` handles CLI `stream-json` messages; newly added `a0_02/session_analyzer.py` handles **local session JSONL**. The two formats should not be silently merged.

It:
- reads top-level `assistant.message.content[].tool_use` and `user.message.content[].tool_result`;
- matches internal tool IDs locally, **without exporting IDs**;
- counts matched/unmatched request and result identifiers, tool errors, later tool requests, model strings and CLI version strings;
- emits only aggregate observations, no prompts/outputs/paths/raw content;
- flags duplicate tool-use identifiers (a caution for repeated or partial snapshots).

**Measurement caveat:** event timestamps, intermediate state, and causality are not inferred. Repeated assistant frames and subagent messages can distort simplistic counts. `requests_without_observed_result` is an observation about this file, not proof of an execution failure. Tool names can themselves be sensitive, so review aggregate output before sharing.

## Reproduce

```bash
python3 -m unittest discover -s research/A0-01-agent-loop-path/a0_02 -p 'test_*.py' -v

# Download in your own connected environment, then run:
curl -L -o /tmp/a002b-public-session.jsonl \
  'https://huggingface.co/datasets/trace-commons/agent-traces/resolve/main/sessions/claude_code/674e0f5c-c481-4830-b2ef-3e1e069a2b7f.jsonl'
python3 research/A0-01-agent-loop-path/a0_02/session_analyzer.py \
  /tmp/a002b-public-session.jsonl --out /tmp/a002b-summary.json
```

**Reproducibility caveat:** `main` is currently a moving dataset branch, not a pinned snapshot. Pin a Hugging Face commit SHA and SHA-256 of the source file before publishing any confirmatory numerical result. The adapter is usable now; quantitative results remain **not collected**.

## Planned metrics for complete-file follow-up

| Metric | Definition | Status |
|---|---|---|
| Tool request/result matching | Intersection of tool-use and tool-result IDs / observed unique tool-use IDs | Not measured on full real file |
| Error tool-result count | Tool results with `is_error=true` | Not measured on full real file |
| Later-tool behavior | Number of paired IDs with a subsequent tool request in the file | Not causal recovery; pending |
| Interruption semantics | Pre/post-interrupt tool dispatch and in-flight effects | Public viewer insufficient; requires careful full trace or supervised execution |
| Session resume | Cross-session linkage and explicit resume markers | Not established by this sample |

## Course correction and next decision

**Changed:** Mandatory local Claude Code installation is no longer a gate for P1/P2. Start with public, licensed, real traces. Keep P3/P4 as **partially observable** rather than automatically verified.

**Next A0-02c:** ingest a pinned native JSONL snapshot, publish a small privacy-safe aggregate and raw-file SHA only, compare P1/P2 predictions to observed events, document gaps (missing IDs, truncation, repeated messages). Do not move to synthetic runtime experiments until source-to-behavior evidence is adequate.

**Source and ethical boundary:** public availability does not guarantee all raw content is safe to republish. Do not commit source traces, user prompts, commands, personal paths or full tool results to this repository.
