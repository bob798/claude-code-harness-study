# A0-03 Claim and Provenance Registry

Version target: **Claude Code v2.1.88**. Study date: 2026-11-20.

| Key | Provenance tier | Locator | Assertion | Independent original-byte authentication | Status |
|---|---|---|---|---|---|
| SRC-01 | Incident reporting | https://www.infoq.com/news/2026/04/claude-code-source-leak/ | Source map included by mistake in npm 2.1.88 | **No** | supports existence, not arbitrary mirror integrity |
| OFF-01 | Official Claude Code docs | https://code.claude.com/docs/en/how-claude-code-works | User-visible agentic feedback and interrupt/session concepts | n/a | documented behavior |
| OFF-02 | Official Claude API contract | https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works | `tool_use` and `tool_result` handshake, `stop_reason` | n/a | applies to API; extrapolation to CLI must be labeled |
| VILA-01 | Secondary code analysis | https://github.com/VILA-Lab/Dive-into-Claude-Code/blob/f29b11530e369e2392f8aa8239cb5a6e592056cf/docs/architecture.md | `queryLoop` in `query.ts`, shared across surfaces; 9-step pipeline | **No** | T |
| CAB-01 | Secondary code analysis | https://github.com/cablate/claude-code-research/blob/c56604faf7a551d6cb433cb83ea05c2bcfd9c190/source-code-analysis/phase-09-harness-engineering/01-agent-loop-analysis.md | `query`, `queryModel`, `runTools`, permissions, feedback & abort | **No** | T |

## Source-Verified promotion checklist (S)

Only promote a claim to S after:

- [ ] Named original artifact obtained through a lawful, permitted channel, with provenance from publisher or cryptographically established chain of custody
- [ ] Product/version identified: `@anthropic-ai/claude-code@2.1.88`, package registry entry, source-map and binary hashes if relevant
- [ ] The precise relevant file and function were actually inspected and recorded in a private local research log
- [ ] The claim is directly supported by that version's actual code, not the language of a third-party report
- [ ] Configuration, feature gate, branching and dead-code limitations documented
- [ ] Public report contains only original paraphrase, compact identifiers and attribution, no large proprietary excerpts

A verified original artifact does not imply a right to republish the source. **Currently zero claims meet all six checks.**

## Resolved vs open

- Confirmed historical incident: yes, supported by contemporaneous reporting.
- Confirmed exact bytes of a public source-map replica: **not obtained**.
- Confirmed exported internal functions in original v2.1.88: **not obtained**.
- Reconciled `query()` vs `queryLoop()`: **open**.
- Verified stop/abort exact branch behavior: **open**.
