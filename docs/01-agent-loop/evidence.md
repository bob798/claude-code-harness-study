# Evidence Ledger — Agent Loop

| ID | Type | Source | What it supports | Limitation |
|---|---|---|---|---|
| O-01 | Official | [Claude Code docs](https://code.claude.com/docs/en/overview) | Public-facing tool and execution workflows | Does not reveal all implementation decisions |
| T-01 | Third-party | [cablate/claude-code-research](https://github.com/cablate/claude-code-research) | Researcher's interpretation of Agent Loop and Harness implementation | Not official; version-specific; claims need corroboration |
| T-02 | Third-party | [VILA-Lab/Dive-into-Claude-Code](https://github.com/VILA-Lab/Dive-into-Claude-Code) | Architecture and design-space study | Secondary analysis, not a normative specification |
| H-01 | Hypothesis | [analysis](analysis.md) | State visibility can help recovery diagnosis | Requires a controlled comparison |
| E-01 | Experiment | [local experiment](../../experiments/loop_recovery/experiment.py) | Stable idempotency keys prevent duplicate commits in the mock service | No model calls, no actual Claude Code integration |

## Rules

Do not treat the leaked source map as an open-source license. Keep direct quotations brief and attributed. Do not upload proprietary source files. Prefer official docs for public behavior and independently testable evidence for performance claims.
