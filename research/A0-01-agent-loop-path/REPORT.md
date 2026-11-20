# A0-01 — Claude Code Agent Loop: Observable Flow and Reported Internal Boundaries

**Research date:** 2026-11-20  
**Mode:** evidence review; **no new code, model/API calls or experiment**  
**Primary behavioral source:** official Claude Code documentation (current as read on the research date)  
**Internal implementation references:** independent third-party reports analyzing a reported **v2.1.88** snapshot. They are not official source verification.

## Research question

What parts of Claude Code's Agent Loop are **officially documented behaviors**, and which internal module boundaries / stop and recovery paths are **third-party interpretations** requiring validation?

### Five layers to keep separate

```text
Human / CLI / SDK inputs
       ↓
[1] Context assembly / session handling      (official behavior; internals T)
       ↓
[2] Model reasoning and streamed response     (official model/tool distinction)
       ↓
[3] Tool request → permission / execution     (official tools & approval; internals T)
       ↓
[4] Tool results returned as observations     (official feedback semantics)
       ↓
[5] Next model decision OR terminal response  (official loop behavior; stop_reason T)
```

An interruption is a separate control input; session resumption is **not necessarily the same thing** as resuming an unfinished external operation. An external side effect is beyond the core reasoning Loop and needs separate analysis.

## Claim-to-source matrix

| ID | Claim | Grade | Precise source / scope | What we may conclude | Missing proof |
|---|---|---|---|---|---|
| A0-O1 | Claude gathers context, acts using tools and verifies; tool outcomes inform further steps | O | [official How Claude Code works — agentic loop](https://code.claude.com/docs/en/how-claude-code-works) | Feedback loop exists as a user-visible product behavior | Exact source-level function and transition order |
| A0-O2 | Models reason; harness provides tools and manages context | O | [official How Claude Code works — models/tools](https://code.claude.com/docs/en/how-claude-code-works) | Distinguish model decisions from enforced actions | Internal choice of executor implementation |
| A0-O3 | Esc interrupts an active operation; queued input can steer subsequent steps | O | [official How Claude Code works — Interrupt and steer](https://code.claude.com/docs/en/how-claude-code-works) | User retains interrupt and steering capability | Precise AbortController propagation and race outcomes |
| A0-O4 | Sessions are saved to JSONL; `--continue` / `--resume` restore conversation | O | [official How Claude Code works — Work with sessions](https://code.claude.com/docs/en/how-claude-code-works) | Session continuity can be restored | No proof of transactional resume / exactly-once tools |
| A0-T1 | Shared `queryLoop` async generator in `query.ts`; core path model → tools → results → next model | T | [VILA-Lab architecture.md, v2.1.88](https://github.com/VILA-Lab/Dive-into-Claude-Code/blob/main/docs/architecture.md) | Hypothesized module map for source research | Independent source/version check needed |
| A0-T2 | 9-stage turn pipeline includes context, model, dispatch, permission and stop | T | [VILA-Lab architecture.md, v2.1.88](https://github.com/VILA-Lab/Dive-into-Claude-Code/blob/main/docs/architecture.md) | Useful architectural decomposition | Exact execution ordering may vary by tool/mode |
| A0-T3 | `REPL.tsx` → `query()` / `queryModel` → `runTools` → `tool_result` feedback | T | [cablate agent-loop analysis](https://github.com/cablate/claude-code-research/blob/master/source-code-analysis/phase-09-harness-engineering/01-agent-loop-analysis.md) | Independently reported code-path hypothesis | Function naming and version alignment not yet reconciled |
| A0-T4 | `stop_reason=end_turn` exits; `tool_use` routes to tool execution; `max_tokens` is a separate path | T | [cablate agent-loop analysis](https://github.com/cablate/claude-code-research/blob/master/source-code-analysis/phase-09-harness-engineering/01-agent-loop-analysis.md) | Candidate stop-condition decision tree | Behavioral traces / upstream version corroboration |
| A0-T5 | Read-only calls may be grouped concurrently, writes handled serially; cancellation propagates via AbortController | T | [cablate agent-loop analysis](https://github.com/cablate/claude-code-research/blob/master/source-code-analysis/phase-09-harness-engineering/01-agent-loop-analysis.md) | Candidate tool-scheduling and cancellation design | Concurrency classifications, default settings, cancellation races |
| A0-T6 | Session transcripts and grants have different persistence semantics in v2.1.88 | T | [VILA-Lab architecture.md, v2.1.88](https://github.com/VILA-Lab/Dive-into-Claude-Code/blob/main/docs/architecture.md) | Distinguish conversation resume from security context restore | Behavior across versions and modes |
| A0-O5 | Claude Code can stop retrying runaway auto-compaction | O | [official Troubleshooting — autocompact thrashing](https://code.claude.com/docs/en/troubleshooting) | A documented bounded no-progress behavior exists | Which exact function detects / stops this condition |

### Conflict ledger

**C1: Name `query()` vs `queryLoop()`.** VILA-Lab explicitly reports `queryLoop` in `query.ts`, whereas cablate describes `query()` from `REPL.tsx` and a `query.js` entry. They might refer to wrappers, distinct versions or conventions. **Do not assert they're identical** without matching version-specific evidence.

**C2: Session resume ≠ exact tool replay semantics.** Official docs support JSONL conversation resume. They do not establish database-style Checkpoint, at-most-once execution, or tool-side effects reconciliation. Previous R1-03 was a generic mock design, not a reconstruction of Claude Code.

**C3: End of model turn ≠ verified business objective.** `end_turn` may indicate the model stopped producing tool calls; external task success needs independent verification. This is a proposed experimental distinction, not a claim about internal success detection.

## Mechanism ownership / research boundaries

| Mechanism | Core A0 Agent Loop? | Follow-up |
|---|---|---|
| Model response → tools → feedback | **Yes** | A0-02 minimal trace / version-qualified module map |
| Stop / resume / interrupt | **Yes** | A1: stop semantics and event matrix |
| Permission and safe dispatch | Core boundary, separate subsystem | Tool Execution branch |
| Context compaction | Pre-model boundary | Context Engineering branch |
| SQLite transaction / outbox / effect ledger | **No** | Backlog: generic runtime recovery |
| Model action choice / task completion | Core outcome | Decision Correctness branch |

## A0-01 conclusion

We can confidently describe the **user-visible feedback loop** from official docs, and name a **version-scoped internal implementation hypothesis** from two third-party source analyses. We **cannot yet claim direct source verification**, precise `queryLoop` implementation details, a comprehensive stop-reason table, or actual Claude Code recovery invariants.

This is an evidence mapping milestone, **not** an empirical confirmation. The first defensible next experiment is an independently observed CLI/SDK trace that records externally visible turn/tool events, with redaction and version recording; compare those events against third-party predictions, never claim the trace exposes proprietary code.

## Research direction adjustment

Previous path: local State → transition checks → mock checkpoint → SQLite durability.  
Corrected mainline: official behavior → v2.1.88 reported module boundaries → observable test trace → targeted design alternatives → falsifiable experiment.

[Decision log](../02-agent-loop/DECISION_LOG.md) · [Research gate](../../RESEARCH_GATE.md).
