# A0-03 — Claude Code v2.1.88: Agent Loop Source-Claim Audit

**Research date:** 2026-11-20  
**Result:** SOURCE-ANALYSIS CROSS-CHECK COMPLETED; DIRECT PROPRIETARY SOURCE VERIFICATION **NOT COMPLETED**.  
**Target:** Claude Code v2.1.88, not newer releases.  
**Goal:** isolate what the actual control-flow claims are, what evidence supports them, and what remains unverified.

## 1. What is established?

An accidental source-map publication in npm package `@anthropic-ai/claude-code@2.1.88` was reported on 2026-03-31. This provides credible provenance for the *existence of a leaked source snapshot*, but does **not** authenticate an arbitrary third-party mirror or certify every downstream claim.

- [Axios reporting](https://www.axios.com/2026/03/31/anthropic-leaked-source-code-ai)
- [InfoQ report](https://www.infoq.com/news/2026/04/claude-code-source-leak/)
- [Public incident issue](https://github.com/anthropics/claude-code/issues/41666)

The official [Claude Code behavior overview](https://code.claude.com/docs/en/how-claude-code-works) describes its agentic loop. The official [Claude API tool-use contract](https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works) explicitly describes the `tool_use → client tool execution → tool_result → next model request` pattern and `stop_reason` handling. **An API contract is not proof of the precise Claude Code CLI implementation.**

## 2. Version-bound secondary source snapshots

| Source | File / revision | Scope | Verification this iteration |
|---|---|---|---|
| VILA-Lab | [architecture.md](https://github.com/VILA-Lab/Dive-into-Claude-Code/blob/f29b11530e369e2392f8aa8239cb5a6e592056cf/docs/architecture.md), Git blob `f29b115...` | Declares v2.1.88 source-map-based analysis | Exact text and blob fetched through GitHub; **T**, not original code |
| cablate | [01-agent-loop-analysis.md](https://github.com/cablate/claude-code-research/blob/c56604faf7a551d6cb433cb83ea05c2bcfd9c190/source-code-analysis/phase-09-harness-engineering/01-agent-loop-analysis.md), Git blob `c56604f...` | Source-path references, snippets and interpretation | Exact text and blob fetched through GitHub; **T**, not original code |

A secondary report can quote and cite an internal file; its claim should not automatically be promoted to Source-Verified (S). This review **did not retrieve, hash, authenticate or inspect the original published npm source-map bytes**. We avoid redistributing proprietary source code.

## 3. Candidate control path

```text
Surface (interactive REPL / CLI / SDK / IDE)
   → shared core query handling [T; exact naming differs]
       → context assembly & pre-model shaping [T]
       → model request / stream processing [O for API pattern, T for CLI function]
       → branch on model stop outcome [O API semantics, T CLI implementation]
           ├─ tool use
           │    → tool grouping/scheduling [T]
           │    → validation, permission, hooks [T; official features exist]
           │    → execution [T internal path]
           │    → tool_result as message/observation [O API contract, T CLI flow]
           │    → next model iteration [O API pattern, T CLI function]
           └─ final/other stop
                → output, limit/error/interrupt handling [T for actual branches]
```

This is a *synthesis of sourced hypotheses* and public API semantics, **not a source-verified call graph**.

## 4. Function-level claim table

| Claim ID | Reported function or policy | Reference | Evidence | Required next verification |
|---|---|---|---|---|
| A3-01 | `queryLoop` async generator in `query.ts` drives model→tools→results→repeat | VILA-Lab `architecture.md`, Agent Loop & Turn Execution | **T** | Match original v2.1.88 `src/query.ts` function signature and actual caller relationships |
| A3-02 | Surface `REPL.tsx` calls `query()` from `query.js` | cablate, sections 1–2 | **T** | Match original `REPL.tsx` path and version; determine whether `query` wraps `queryLoop` |
| A3-03 | `queryModel()` streams API responses | cablate, section 3, `services/api/claude.ts` | **T** | Confirm exact v2.1.88 function, event types and callers |
| A3-04 | `runTools()` dispatches tool-use requests and groups concurrency-safe calls | cablate, section 4 | **T** | Confirm grouping policy and concurrency caps in the same version |
| A3-05 | `checkPermissionsAndCallTool()` validates and applies hooks/permissions before calling a tool | cablate, section 5 | **T** | Check ordering and bypass branches in original source |
| A3-06 | `tool_result` is returned as a message, driving next turn | cablate, section 6; official API tool contract | **O for API contract; T for CLI path** | Confirm message append/stream behavior in v2.1.88 |
| A3-07 | `end_turn`, `tool_use`, `max_tokens` take distinct paths | cablate, section 1; official API stop semantics | **O for API semantics; T for CLI paths** | Check exact CLI conditionals, including errors, abort, refusal and `pause_turn` |
| A3-08 | Abort signal propagates from interactive interruption to individual tool execution | cablate, section 7 | **T** | Check actual cancellation and mid-flight behavior |
| A3-09 | Pre-model context operations occur before model request | VILA-Lab, Turn Execution / Five Pre-Model Context Shapers | **T** | Confirm order and gated paths in source |
| A3-10 | All interfaces converge on the same `queryLoop` | VILA-Lab, High-Level System Structure | **T** | Verify wrapper/caller mapping for each advertised surface |

## 5. What does *not* follow from the sources?

- **Not proven:** `queryLoop` is literally a `while(true)` in the exact released package merely because a secondary report calls it a simple while-loop.
- **Not proven:** `query()` and `queryLoop()` are the same function; wrapper and version differences remain unresolved.
- **Not proven:** the model only stops on `end_turn`. API stop reasons and CLI recovery branches are richer.
- **Not proven:** the observed CLI loop directly implements API examples line-for-line.
- **Not proven:** use of a while-loop is *why* Claude Code is reliable or scalable.
- **Not proven:** current Claude Code versions retain v2.1.88's private implementation.

## 6. Research answer and design trade-offs

**Best-supported statement:** official public behavior establishes an iterative model/tool feedback control pattern, and *two version-scoped source analyses* describe a compact shared loop surrounded by context management, permission gates and tool execution infrastructure. Their method names and internal ordering must remain version-qualified hypotheses until independently checked.

**Important design distinction:** the **model** selects among exposed tool requests, while the **harness** handles execution boundaries and authorization. The API's tool-use contract supports that role split; precise implementation responsibilities remain to be verified.

**Alternative designs to analyze only after source verification:** (a) simple while + structured state; (b) explicit FSM; (c) graph-based orchestration. Compare flexibility, observability, retry/cancellation semantics and complexity — do not claim benchmarks based on unrelated toy simulations.

## 7. Scope gate, limits, next test

- **G0:** pass for official behavior; **partial** for source implementation, since primary artifact not authenticated.
- **G1:** pass: directly addresses core Agent Loop.
- **G2:** not yet ready for comparative code experiment; source-to-claim mapping first.
- **Decision:** keep A0-03 as an evidence audit, **do not label any A3-01..A3-10 as S**.
- **Next:** A0-03b: verify provenance and precise function-level relationships against a legally accessible, authenticated v2.1.88 source artifact or other authorized primary material; publish original descriptions, not source. If unavailable, use publicly documented behavior and clearly remain at T.
- **Follow-on:** A1-01: compare alternative Loop mechanisms for one narrowly defined outcome after A0-03b resolves the relevant control path.

Sources: [source claim matrix](SOURCE_CLAIMS.md) · [scope gate](../../RESEARCH_GATE.md) · [decision log](../02-agent-loop/DECISION_LOG.md).

## Addendum: community reuse and controlled alternatives (A0-03b)

The architecture inventory has expanded to VILA-Lab, cablate and 6551Team, with OpenHands (stateless event steps), Goose (reentrant state-machine proposal) and LangGraph (graph and functional durable execution) as explicit alternatives. Existing empirical harness ablations (e.g., arXiv:2609.20804) do not isolate loop representation. **No performance superiority is inferred.** See [community inventory](COMMUNITY_REUSE.md), [alternative designs](ALTERNATIVE_DESIGNS.md), and [evaluation plan](EVALUATION_PLAN.md).
