# A0-02 — Observable Claude Code Trace: Instrumentation and Readiness

**Date:** 2026-11-20  
**Status:** Collection tooling complete; **real Claude Code observations not collected**.  
**Evidence:** O (official CLI capabilities); E-SYNTHETIC (parser-only tests); no E-REAL results.

## Initial question

Can we observe a tool request → tool result → subsequent model output sequence from a versioned Claude Code CLI run, and distinguish that observed behavior from the third-party `queryLoop` implementation hypothesis?

## G0/G1/G2 scope gate

- G0 **pass for CLI behavior**: official [programmatic usage](https://code.claude.com/docs/en/headless), [CLI reference](https://code.claude.com/docs/en/cli-reference), [how Claude Code works](https://code.claude.com/docs/en/how-claude-code-works). Internal private implementation claims remain T, unverified.
- G1 **pass**: directly measures Agent Loop's observable model↔tool feedback boundary, error, interrupt and session continuity.
- G2 **partial**: test cases and parser ready, but this environment has **no `claude` executable or credentials**, so no CLI run can be claimed. **Do not label unit tests as Claude Code experiment results.**

## Available public observation interface

Official CLI: `claude -p "..." --output-format stream-json --verbose`; optionally `--include-partial-messages`. Full `assistant` / `user` messages may include `tool_use` / `tool_result` blocks. A terminal `result` record reports the run result. The `--resume` CLI option is publicly documented.

**Known limits:** Stream JSON is a public interface, not an internal call stack; events may include data from subagents; raw NDJSON can contain prompts, tool arguments, tool outputs and session data. Avoid publishing it without careful review.

## Four planned probes

| ID | Probe | Observable claim | Conditions before execution |
|---|---|---|---|
| P1 | Read a disposable local file | At least one `tool_use` and corresponding `tool_result` can be exposed, followed by assistant output | Isolated temp directory and Read-only tool permission |
| P2 | Read nonexistent disposable path | Tool result may be marked as an error and affect next response | Observe actual error, do not assume retry |
| P3 | Interrupt during a controlled long action | No new tool dispatch after a completed cancellation boundary | Separate supervised run; capture real signal/CLI version |
| P4 | Resume an existing session | Conversation continuation succeeds and produces new public messages | Preserve session locally; capture ID privately; no claims about exactly-once side effects |

## Tooling delivered

- [trace_summary.py](a0_02/trace_summary.py): privacy-reduced event summary (event types, tool names, error flags); intentionally discards prompts, tool arguments, tool content and IDs.
- [test_trace_summary.py](a0_02/test_trace_summary.py): four **synthetic fixture** tests; tests passed in local Python environment.
- [RUNBOOK.md](a0_02/RUNBOOK.md): explicit safe commands and data collection instructions.

The summarizer discards partial `stream_event` messages to avoid double counting full message blocks. Tool request/results are **not paired** by ID in public summaries. This reduces privacy exposure but also limits sequence proof. Raw traces are private and must be manually reviewed before any publication.

## Actual result (do not replace with assumed numbers)

| Item | Status |
|---|---|
| Current environment `claude --version` | **Not available** (`claude: command not found`) |
| Claude login/API credentials | Not available in this environment |
| P1/P2/P3/P4 real run | **Not executed** |
| Four parser unit tests | **Passed on synthetic inputs** |
| Claude Code observed version/model | **Unknown** |
| Tool-feedback empirical conclusion | **Pending** |

## What changed, and why?

A0-01 had planned immediate live tracing. A0-02 discovered that runtime capability is absent. Therefore we created an official-CLI-based observation protocol and privacy-first summary tool rather than fabricating traces or reverting to unscoped mocks. **No claim about `queryLoop` internals changes based on parser tests.**

## Next validation / falsification

A0-02b: collect P1/P2 on a user-controlled Claude Code installation, document exact CLI version and model, retain the raw stream privately, and publish only reviewed summaries. Examine whether the observable stream supports or contradicts each *behavioral* prediction. Proceed to P3/P4 only after safe supervised trial. A missing event may reflect output visibility, not absence of internal processing.

If the official CLI alters flag or event schemas, update the runbook and parser with version-specific tests before interpreting output.

## Source provenance

- Official programmatic CLI: https://code.claude.com/docs/en/headless
- Official flags: https://code.claude.com/docs/en/cli-reference
- Official model/tool loop: https://code.claude.com/docs/en/how-claude-code-works
- A0-01 secondary internal analysis: [previous report](REPORT.md)
