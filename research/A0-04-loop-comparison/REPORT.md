# A0-04-PILOT — Streaming Loop vs Reentrant Step

**Study date:** 2026-11-20. **Evidence:** E-MOCK with an actual subprocess SIGKILL at a *completed checkpoint boundary*. **Not** a Claude Code or Goose runtime benchmark. No LLM API calls.

## Research origin and correction

VILA-Lab's Claude Code v2.1.88 architecture study reports an async-generator `queryLoop`. Goose's upstream #9944 proposed a per-turn reentrant state machine, and its September 2026 engineering report confirms a subsequently implemented migration; the `goose-agent` 0.1.0-alpha.14 package was published November 17, 2026. **Goose is no longer merely a proposal.** Both arms here are minimal independently implemented analogues, not reproductions of either proprietary or open-source runtime.

References:
- https://github.com/VILA-Lab/Dive-into-Claude-Code/blob/main/docs/architecture.md
- https://github.com/aaif-goose/goose/discussions/9944
- https://goose.vcorp.ai/blog/2026/09/16/agentic-state-machines/
- https://docs.rs/crate/goose-agent/0.1.0-alpha.14

## Falsifiable question

**Does changing a long-lived generator-style model/tool loop to a one-step reentrant controller, by itself, improve correctness after process restart when both share identical checkpointing and tool policies?**

H0: no difference in correct completion in matched scenarios.
H1: reentrant controller yields a higher correct completion rate.
Counterevidence: both complete identically after a real process kill, with matched persistence and policies.

## Controlled experiment

- A: `streaming_loop()`, a long-lived generator that yields after each completed turn.
- B: `reentrant_step()`, invoked once per turn by a host loop.
- Same scripted `model_decision`, `apply_turn`, maximum turn budget, mock tool-effect semantics, and **atomic JSON checkpoint after EVERY completed turn in BOTH arms**.
- Four planned tool effects (`op-1` .. `op-4`) followed by a final decision. No LLM, network API or vendor source code.
- A test launches each controller as a separate child process, waits for checkpoint after turn 2, kills the process using OS `SIGKILL`, then starts a fresh process that loads persisted state.
- Independent terminal oracle checks the exact action history, model-call count, unique effects and final state.

Commands:

```bash
python3 -m unittest discover -s experiments/a0_04_loop_comparison -p 'test_*.py' -v
```

Measured local outcome (4 tests passed):

| Outcome | Long-lived generator | Reentrant step |
|---|---:|---:|
| Normal-run oracle | PASS | PASS |
| SIGKILL after persisted turn 2 → resume oracle | PASS | PASS |
| Decision invocations | 5 | 5 |
| Unique tool effects | 4 | 4 |
| Duplicated effects | 0 | 0 |
| Final phase | complete | complete |

See [machine-readable results](../../results/a0-04-pilot.json) and [reproducible tests](../../experiments/a0_04_loop_comparison/test_experiment.py).

## What this proves and does not prove

**This small example finds parity.** Reentrancy alone cannot be credited with recovery correctness when both arms have the same checkpoint semantics. It is *not* evidence that Claude Code or Goose have the same recovery behavior; it is not a statistically powered comparison. The kill occurs AFTER a completed turn and durable state save, **not in the middle of a tool or between external effect and persistence**.

Not evaluated: cost, wall-clock latency, real LLM correctness, streaming-token handling, mid-tool cancellation, real external side effects, concurrent tools, maintenance effort, or pause/resume during an individual tool operation.

## Research change and next minimal test

The next discriminating feature is **host-driven pause, approval and reentry at a boundary between model tool selection and action execution**, with matched permissions and persistence. A0-04-02 should test whether a reentrant machine requires less reconstruction complexity to hand off control, and which operational overhead it pays; confirm Goose's actual GDK operations instead of treating an early design discussion as final implementation.

**Do not claim a Claude Code superiority or a Goose superiority from this pilot.** Record this null finding without retroactively changing the hypothesis.
