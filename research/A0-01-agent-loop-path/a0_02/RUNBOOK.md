# A0-02 Safe CLI Trace Collection Runbook

**This document is an executable plan, not a record of completed Claude Code runs.**

## Requirements

- An independently installed **official Claude Code CLI** on your own machine, with normal account authentication performed via Anthropic's own login flow.
- A disposable working directory with no credentials or sensitive files.
- Python 3.10+ to summarize events.
- Network/API usage may incur costs; no cost cap is guaranteed by this runbook.

## Step 1 — Verify installation and record provenance

```bash
claude --version
claude --help
python3 --version
```

Record CLI version, model selected, local execution date, flags and prompt. Never commit credentials or login/session tokens.

## Step 2 — Create isolated fixture

```bash
mkdir -p /tmp/a002-claude-observation
printf 'ORBIT-47\n' > /tmp/a002-claude-observation/fixture.txt
cd /tmp/a002-claude-observation
```

**Security note:** review CLI/project settings and work in an isolated path. In recent CLI versions, `--bare` suppresses hooks/plugin discovery but **requires API-key authentication** rather than subscription login; do not add `--bare` blindly when using a normal subscription. The Runbook does **not** grant blanket Bash/Edit permissions.

## Step 3 — P1: read a local fixture

```bash
claude -p 'Read fixture.txt using the Read tool; then report its one-line contents.' \
  --allowedTools Read \
  --output-format stream-json --verbose \
  > p1.raw.ndjson
```

Check exit status. If your CLI/version rejects a flag, record that failure instead of modifying the report to imply success. Treat `p1.raw.ndjson` as **private**.

## Step 4 — P2: error feedback from missing file

```bash
claude -p 'Attempt to read nonexistent-a002.txt with Read. If it fails, explain the observed error.' \
  --allowedTools Read \
  --output-format stream-json --verbose \
  > p2.raw.ndjson
```

The resulting tool error is **not guaranteed**; model may choose a different action. Report deviations honestly.

## Step 5 — privacy-reduced summary

From the repository checkout (replace the path below with your actual checkout):

```bash
python3 research/A0-01-agent-loop-path/a0_02/trace_summary.py \
  /tmp/a002-claude-observation/p1.raw.ndjson \
  --out /tmp/a002-claude-observation/p1.summary.json
```

The summarizer outputs **event kinds and tool names**, not text/arguments/content. It is not a full redaction security guarantee: tool names and event patterns could still be sensitive, so review results before publishing. **Do not upload raw NDJSON**.

## Step 6 — P3/P4 later

P3 interruption requires an **interactive or supervised process** where the exact cancellation mechanism and execution boundary are known. Do not emulate by pretending an arbitrary SIGTERM means the same thing as pressing Escape. Official programmatic docs distinguish SIGTERM, SIGINT and SDK `interrupt()`.

P4 resume: run once with `--output-format json` to inspect the session ID privately, then continue with `--resume <session-id>` and record separately. A resumed conversation does **not** prove transactional side-effect recovery.

## Data recording template

| Field | Record |
|---|---|
| CLI version | |
| Model ID/version | |
| Execution mode / auth type (no credentials) | |
| Date and OS | |
| Prompt scenario ID | P1 / P2 / P3 / P4 |
| Exit status | |
| Public summarized event sequence | |
| Evidence claim supported / contradicted | |
| Deviations, missing events and uncertainty | |

## Unit tests

```bash
python3 -m unittest discover -s research/A0-01-agent-loop-path/a0_02 -p 'test_*.py' -v
```
