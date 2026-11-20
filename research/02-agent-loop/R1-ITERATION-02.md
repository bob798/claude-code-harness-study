# R1 — Iteration 02: State Representation vs Transition Enforcement

**Date:** 2026-11-20  
**Evidence category:** E-MOCK / deterministic synthetic event-replay experiment.  
**Status:** exploratory; not a pre-registered confirmatory benchmark, not a Claude Code trace.

## What changed after iteration 01?

Iteration 01 found identical results for `while + local variables` and `while + typed State` on five simple scenarios. We therefore **split the initial hypothesis**: state *representation* and transition *enforcement* are distinct mechanisms. Research decisions and next-step changes are recorded in [DECISION_LOG.md](DECISION_LOG.md).

## Question

Does replacing local variables with an explicit typed State improve transition safety on its own? Separately, can validation of allowed transitions reject invalid event sequences in a deliberately permissive execution model?

## Competing explanations

- **H-R (representation):** a typed state container alone prevents invalid transitions.
- **H-V (validation):** an explicit allowed-transition rule is what blocks invalid transitions; the container is not sufficient.

Three arms:
1. **local:** local variables, permissive transition function.
2. **typed:** dataclass State, **identical** permissive transition function.
3. **typed + validation:** same typed State plus a declared allowed-transition check.

The third arm **adds a capability**; it is NOT evidence that typed State alone improves runtime correctness.

## Execution safety constraints (Invariant)

- A terminal state must not accept later events.
- An event must be allowed by the source state.
- `complete` requires a prior acknowledged tool result.
- `tool_ok` cannot arrive before `start`.
- Repeated `start` is not permitted.

We use **execution safety constraints / 执行安全约束** in explanatory Chinese text; `invariant` is retained as a precise formal term when appropriate.

## Test and result

Six events: `start, tool_ok, cancel, timeout, complete, resume`. Exhaustively enumerate all length-1, length-2 and length-3 traces: 6 + 36 + 216 = **258 traces**.

Commands:

```bash
python -m unittest discover -s experiments/r1_transitions -p 'test_*.py' -v
python experiments/r1_transitions/experiment.py
```

Results in the checked-in deterministic toy model:

| Arm | Traces accepting >=1 disallowed event |
|---|---:|
| local variables | 249/258 |
| typed State | 249/258 |
| typed State + validation | 0/258 |

The validated arm rejected **506 invalid event attempts** across all sequences. These are *synthetic traces*, not independent random samples. Do not calculate a population success rate or confidence interval from this exhaustive enumeration.

## What we learned

- Simply packaging the same variables into `State` changes neither transition semantics nor the observable failures.
- Enforcing allowed transitions can prevent the *specified* illegal paths in this toy model.
- This is a specification-conformance check: the enforcement function and checker use the same declared rules. It is **not** independent evidence that these rules cover real-world faults or that recovery works.
- A guard may also reject legitimate operations in a real asynchronous environment; false rejection and liveness must be measured.

## Next adjustment

**R1-03:** simulate asynchronous tool completion, cancellation races, process crash and resumed execution. Compare two functionally matched guarded implementations (local + guard vs typed + guard); measure safe recovery, false rejections, and consistency. Keep a separate ablation of guard on/off to isolate the enforcement mechanism. Add external side-effect oracle instead of only internal transition checks.

**Do not** claim typed State is superior without an appropriate controlled result.
