# Agent Loop — Falsifiable Research Questions

> Draft pre-registration v0.1, 2026-11-20. The following hypotheses are proposals **not experimental findings**. Freeze protocol and outcome thresholds in a separate commit *before* measurement.

## Conceptual boundaries

Three quality dimensions must remain separate:

1. **Sustainable execution**: under finite budgets, the run continues to make *verified task progress* rather than merely consuming iterations or tokens.
2. **Reliable execution**: under injected failures, the runtime preserves invariants, reports terminal reasons accurately, and recovers or fails safely.
3. **Correct decision-making**: given the same observations and available tools, the selected next action is appropriate according to an independent task oracle or expert-labeled acceptable-action set.

A runtime can execute reliably yet pursue the wrong action; a model can choose the right action yet fail to execute it. Avoid attributing model errors to Harness mechanisms.

## RQ-S1: Does a no-progress guard increase productive long-task completion?

- **Independent variable**: fixed no-progress detection + bounded intervention versus identical loop without guard.
- **Workload**: multi-step synthetic and real tasks with opportunities for repeated failed tool calls. Match model, prompts, tools, token budgets and task order.
- **Primary metric**: verified completed subtasks per 10k consumed tokens, with task completion rate as a co-primary outcome (both reported).
- **H0**: no improvement in progress rate and/or completion.
- **H1**: guard reduces unproductive repeated actions and improves verified progress at fixed budget without materially hurting completion.
- **Potential falsification**: equal/worse progress, or a fall in task completion because the guard prematurely stops valid exploration.
- **Threats**: progress oracle quality, benign repeated actions, model variance.
- **Important**: the guard may improve efficiency, not sustainability, unless the Agent remains productive longer under a predeclared long-horizon workload.

## RQ-S2: Does checkpointing improve completion across interruptions?

- **Independent variable**: persistent checkpoint/resume vs fresh restart, same recovery budget.
- **Faults**: termination after a chosen tool result and restart at predetermined task points.
- **Primary metric**: correct completion rate post-interruption; secondary: redundant work, resumed-step consistency, total cost.
- **Potential falsification**: checkpointing performs no better or restores stale/incorrect state.

## RQ-R1: Does explicit execution state *by itself* improve failure recovery?

- **Comparison**: minimal while with disciplined local variables vs while + typed state and transition events. Both have the **same** retry, approval and tool features.
- **Primary metric**: invariant violations per 1,000 fault-injected runs (illegal transition, incorrect terminal status, untracked effect).
- **Secondary**: debugging time (blinded tasks if possible), state reconstruction success, branch complexity.
- **H0**: no reduction in invariant violations.
- **H1**: explicit state reduces invariant violations in complex recovery paths.
- **Potential falsification**: no meaningful reduction; or the stateful version creates more invalid transitions.
- **Design note**: explicit state can improve observability without changing runtime correctness. Report these separately.

## RQ-R2: Do stable idempotency keys prevent duplicated tool effects after lost replies?

- **Comparison**: blind retry vs stable per-logical-operation key, with service-side deduplication.
- **Fault**: tool commits then reply is dropped; retry triggered.
- **Primary metric**: duplicated external effects per logical operation, secondary: completion, overhead.
- **Potential falsification**: duplicate effects persist despite correct key propagation and deduplication.
- **Limit**: Iteration 001 already demonstrates this in a deterministic toy simulator; formal real-system tests remain necessary.

## RQ-D1: Can structured observations improve next-action correctness?

- **Comparison**: same model, same facts and tools; A receives unstructured tool-result text, B receives typed observations with schema validation. Equalize information content and approximate token budget.
- **Task set**: scenarios with independently labeled acceptable next actions, including ambiguity requiring clarification or safe abstention.
- **Primary metric**: acceptable-next-action rate (top-1 or set membership); secondary: invalid tool calls, safety-rule violations, cost.
- **H0**: no difference.
- **H1**: typed observations improve next-action correctness.
- **Potential falsification**: equal/worse accuracy, or gains disappear after controlling for content and token budget.
- **Caution**: this concerns the model+interface system, not proof that the loop algorithm makes smarter decisions.

## RQ-D2: Does external verification reduce false task-complete claims?

- **Comparison**: model self-declared completion only vs completion gated by independent external state assertions.
- **Primary metric**: false-positive completion rate; secondary: false-negative rejection, latency, cost.
- **Potential falsification**: no reduction in false positives, or unacceptable false negatives on valid completions.
- **Trade-off**: verifier correctness and coverage become part of the trusted computing base.

## Experimental release order

**First** RQ-R1 (State vs while, same features) → **then** RQ-S1 (no-progress guard) → **then** RQ-D1 (decision quality). Reuse RQ-R2 as an established toy baseline and expand with real external operations.

## Minimal dataset protocol

- Divide tasks by complexity, uncertainty, and available tools; disclose selection.
- Use deterministic traces to validate Harness invariants and model-based repeated runs to evaluate decisions.
- Fixed model version and documented decoding settings; paired comparisons wherever feasible.
- Independent completion and decision oracles, not model-generated success claims.
- Report confidence intervals, negative results and all failure cases.
- Predeclare practical effect thresholds and sample size after pilot measurements, before confirmatory runs.

## Success means

A hypothesis is **supported in the tested setting** if the pre-registered primary outcome and uncertainty justify it. An unsupported claim is not rewritten post hoc. Any exploratory follow-up is labeled exploratory. Do not equate failure to reject H0 with proof of no effect.
