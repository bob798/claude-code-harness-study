# R1-03 — Crash, Cancellation and Checkpoint Replay

**Date:** 2026-11-20. **Evidence:** E-MOCK. **Status:** exploratory deterministic simulation; not a Claude Code execution trace, not a model-based benchmark, not a pre-registered confirmation.

## Model and environment

- **No LLM** is called. Code uses Python's standard library.
- Four arms: `local_volatile`, `typed_volatile`, `local_checkpoint`, `typed_checkpoint`.
- Local and typed variants have matched policy. Checkpoint variants save their own state after each non-restart event. Mock external effects remain durable across crash and use a stable operation ID to deduplicate.
- Faults are **scripted event order**, not true asynchronous threads, process kills, durable disk/database transactions, or network operations.
- External observer records new dispatches after a cancellation request. The cancellation observer is not part of the restored runtime state; it is used only to evaluate safety.

## Research questions

1. Does changing local variables to a dataclass alter behavior when policies are identical?
2. Does preserving cancellation state across restart prevent *new* tool dispatches after cancellation?
3. Does a checkpoint, by itself, resolve uncertainty after an external operation committed but its acknowledgment was lost?

## Reproduce

```bash
python -m unittest discover -s experiments/r1_recovery -p 'test_*.py' -v
python experiments/r1_recovery/experiment.py
```

Local dry run: **5/5 unit tests passed**.

## Observations

| Scenario | Volatile local & typed | Checkpoint local & typed |
|---|---|---|
| Normal | completed; 1 call, 1 external effect | same |
| Crash before commit | completed; 2 dispatches, 1 effect | same |
| Crash after commit / before ack | completed; 2 dispatches, 1 effect | same |
| Cancel → crash → restart → attempted dispatch | **1 new dispatch after cancellation**; terminal completed | **0 new dispatches after cancellation**; terminal cancelled |
| Delayed acknowledgment after cancellation | cancelled; no new dispatch | same |

All **five** scenarios produced identical results for local vs typed state *within the same checkpoint setting*. The cancellation outcome difference is therefore attributable to **persistent cancellation state in this constructed model**, not dataclass use. The checkpoint cannot eliminate a retry when the tool committed but the acknowledgment was lost; deduplication keeps the mock external effect count at one.

**Critical caveat:** An in-flight external effect may commit after cancellation; cancellation cannot retroactively revoke it. This is a deliberately simplified example, not proof of exactly-once execution.

## Threats to validity

1. The replay script forces a post-restart dispatch attempt; this magnifies the difference between persistent and volatile cancellation, rather than measuring a real scheduler.
2. Service deduplication is idealized and durable.
3. The snapshot write is modeled as atomic, without torn writes or stale checkpoints.
4. There is no actual multi-process concurrency, parallel tool completion, model inference, latency, or cost.
5. We observe a tiny scripted set, not statistical evidence.

## Direction change

**Reject the framing "typed State causes reliable recovery".** Focus on explicit **persistence protocol + external effect reconciliation + cancellation semantics**, keeping representation as a separately controlled variable.

Next iteration should implement a durable SQLite checkpoint and external operation ledger, inject faults between commit and state persistence, and compare failure recovery against a reference oracle; use independent real crash/process restart testing before any general reliability claim.

See [decision log](DECISION_LOG.md) and [model/source provenance](MODEL_AND_SOURCE_PROVENANCE.md).
