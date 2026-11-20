# A0-04-02 — Approval Handoff and Reentry Pilot

**Research date:** 2026-11-21. **Status:** local controlled pilot, not a vendor benchmark. **Evidence grade:** E-MOCK; no live Claude Code or Goose execution and no LLM API calls.

## Exact question and hypotheses

Does the **shape of the controller** (a yielding generator vs an explicit reentrant `step()`) independently change approval safety or model-call duplication, when **both controllers have the same persisted state, policy and tool implementation**?

- H0: both exhibit the same safety outcomes and model-call count on matched approval sequences.
- H1: explicit reentrant steps independently reduce unapproved effects, duplicated decisions or incorrect recovery.
- Refutation of H1 in this pilot: identical safe results in all matched sequences.

## Controller design

[A0-04-02 minimal independent implementation](../../experiments/a0_04_02_approval/experiment.py) uses a **shared** state transition and policy oracle, two different host control implementations:

- **Streaming-shaped arm:** yields `needs_approval`; caller persists state, drops generator stack; on a later invocation the generator is **reconstructed** from persisted state. This is **not** the behavior of a continuously suspended generator retaining a process stack.
- **Reentrant step arm:** explicit `step(state)` returns `needs_approval`, and a later host call loads and advances saved state.
- Both arms use the same `infer_tool`, `external_event`, `finish_tool`, `finalize`, atomic JSON snapshot, operation ID, policy and scripted decision.
- **External host signals are separate subprocess invocations** (`invoke`, `signal`); this tests cross-process handoff, but **not** a kill during tool execution, concurrent actors or serialized durability under races.
- The external oracle checks phase, number of decisions, effect IDs and denial/cancellation enforcement. A scripted deterministic decision is **not an LLM result**.

## Six locally executed tests

| Test | Oracle | Result |
|---|---|---|
| Approve after process boundary | only one approved effect; one initial decision | PASS, both arms equal |
| Deny after process boundary | no effect; completion with denial feedback | PASS, both arms equal |
| Cancel then late approval | cancellation terminal, late approval ignored, no effect | PASS, both arms equal |
| Duplicate approval | second approval ignored, single effect | PASS, both arms equal |
| Repeated invoke during waiting | no new model decision, both remain pending | PASS, both arms equal |
| Invalid pre-proposal approval | shared guard rejects unsolicited approval | PASS |

**Observed parity** in this tiny scripted workload. No causal claim of superiority, no measured throughput or task success. Because both arms reconstruct from durable state, they are closer than the names suggest; this is a **limited ablation of API/control surface**, not a definitive comparison of a live streaming coroutine vs a Goose production state machine.

## What the upstream research says

- [Goose GDK state machine](https://goose.vcorp.ai/docs/gdk/concepts/state-machine/) documents an execution/host boundary with resumable steps.
- [Goose GDK operations](https://goose.vcorp.ai/docs/gdk/concepts/operations/) describes operation management and approval controls.
- [VILA-Lab Claude Code v2.1.88 analysis](https://github.com/VILA-Lab/Dive-into-Claude-Code/blob/main/docs/architecture.md) reports a shared asynchronous query loop; this remains a **secondary** account, not direct authentication of source internals.

## Critical threat to validity

A generator re-created from a saved checkpoint at every boundary **already implements resumability**. This can *mask the very structural difference* we intended to test. The next experiment must separate:
1. process-local, live-stack suspension;
2. explicitly persisted boundary state;
3. host-driven event ingress;
4. resume semantics after process loss.

Comparing a no-checkpoint loop to a checkpointed state machine would be unfair; we should instead evaluate **complexity, serialization requirements, responsiveness and costs** under equal capabilities.

## Benchmark review prompted during this iteration

See [OPEN_BENCHMARKS.md](OPEN_BENCHMARKS.md). Existing public benchmarks offer independent tasks and oracles:
- approval-to-execution integrity / drift;
- trace-based policy/fault cases;
- tool-use security;
- coding task success.

**But we found no mature, widely used benchmark that isolates the causal performance of Claude Code-style streaming control vs Goose-style reentrant control under exactly matched policy/model/checkpointing.** The appropriate contribution is a *small adapter and preregistered tests* based on existing suites, not another ungrounded bespoke benchmark.

## Decision / next falsification

**No advantage detected** in the matched synthetic approval sequences. Next: adopt independent approval-action scenarios and test action mutation **after** approval, replay of prior approval, stale authority after process restart, and cancel-vs-approve races. Use a linearizable effect ledger or an independently recorded tool-effect oracle only where required; do not attribute improvements to structure when they come from newly added guards. A future real-model benchmark should use pinned Terminal-Bench tasks with matched model/tool budgets.

Reproduction:
```bash
python3 -m unittest discover -s experiments/a0_04_02_approval -p 'test_*.py' -v
```
