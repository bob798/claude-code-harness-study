# 001 — Agent Loop: Control Flow, State, and Lost Tool Results

## Research question

Why does an Agent Loop need explicit execution state and failure handling beyond a short ReAct `while` loop?

## Minimal model

```text
context → model → (final response | tool request)
                         ↓
                validate / authorize
                         ↓
                   tool execute
                         ↓
                   tool result → model
```

The loop is the scheduling mechanism; state describes execution history and constraints. A `while` loop can hold explicit state without being a formal finite-state machine. Conversely, a formal FSM requires an explicit state set, transition relation, and defined invariants.

## Design trade-off (hypothesis)

- `while + messages`: easiest to teach, difficult to diagnose after complex failures.
- `while + state + transition events`: flexible dynamic decisions plus observability.
- formal FSM/workflow graph: stronger transition constraints, but greater specification and orchestration cost.

These are architectural comparisons, **not verified historical explanations of Anthropic's internal decisions**.

## First independent experiment

A tool commits a side effect and the response is dropped. The caller retries:

- Without an idempotency key, an external operation can commit twice.
- With a stable idempotency key implemented by the receiving service, the same logical operation commits once.

This demonstrates a retry hazard; it does not establish that Claude Code has, or lacks, this problem.

## What to measure next

Use functionally equivalent implementations to compare cancellation, retries, persistence, duplicated effects, and invalid transitions. Report exception paths and code complexity as secondary outcomes. Do not equate “clearer code” with “higher reliability” without evidence.

## Further reading

See [evidence ledger](evidence.md) for claim provenance and source links.
