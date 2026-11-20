# R1: Does Explicit State Improve Agent Loop Recovery?

**Status: exploratory pilot (2026-11-20), NOT a prospective preregistered confirmatory study.** The protocol and pilot outcomes were created in the same iteration.

## Question and falsification

When both Loop variants have **identical** tool, retry, deduplication, cancellation and terminal policies, does using an explicit typed `AgentState` reduce invariant violations compared to local variables inside a `while` loop?

- **H0:** no improvement in the primary outcome.
- **H1:** explicit typed State reduces invariant violations in complex recovery paths.
- **Potential counterevidence:** equal or more violations with typed State in adequately powered, preregistered matched scenarios.
- **Important:** failure to reject H0 does not prove equivalence.

## Precisely defined invariants

1. At most one external effect per logical operation (stable tool-side idempotency key).
2. No more than three invocations.
3. Cancellation effective before execution forbids subsequent invocation.
4. A completed status requires confirmed tool reply.
5. Confirmation requires a completed terminal status.

**Violating-run rate** = runs with ≥1 failed invariant / all runs. **Violations per 1,000 runs** = sum of failed predicates / all runs × 1000. These are different measures.

## Exploratory pilot setup

- Two independent implementations: local variable loop and explicit dataclass State loop.
- Shared scripted mock tool; same three-attempt bound and stable operation ID.
- Five deterministic scenarios: normal, pre-commit timeout, post-commit lost reply, three lost replies, cancellation before tool call.
- Compare full output traces and the above invariants.

Reproduce without network or API credentials:

```bash
python -m unittest discover -s experiments/r1_state -p 'test_*.py' -v
python experiments/r1_state/experiment.py
```

## Pilot observation

**5/5 equal traces; 0/5 violating runs for each implementation; four tests passed locally.** This establishes only a *functional parity smoke test*. It does not show that typed State improves or harms reliability, and does not measure Claude Code.

## Next study

Freeze confirmatory outcomes **before** collecting new data. Add multi-step action traces, process crashes, tool completion ambiguity, concurrent returns, cancellation during execution, and controlled maintenance changes. Measure both runtime invariants and debugging/diagnosis separately. Publish full datasets, variations and negative results.
