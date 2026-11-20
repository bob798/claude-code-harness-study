# A0-04 — Falsifiable Comparative Evaluation Plan (NO RESULTS YET)

**Question:** When does a Claude Code-style model-led core loop outperform or underperform explicit state-machine, event-sourced and graph-based control in coding-agent tasks?

This is a **proposed protocol**, not results. Previous R1 mock tests are neither substitutes nor evidence of superiority.

## Main hypotheses

| ID | Falsifiable hypothesis | Primary metric | Observation against hypothesis |
|---|---|---|---|
| H1 flexibility | Model-led loop completes more *novel/unstructured* coding tasks at equal budget than a rigid predefined workflow graph | Independently scored task success | Graph is equal/better with no additional human wiring |
| H2 control | Explicit state/event-based orchestrators reduce wrong transition/incorrect resume behavior under interruption at **equal enforcement rules** | Safe-recovery completion after faults | No improvement, or increased erroneous rejection |
| H3 cost | Lightweight loop uses less framework overhead on *short tasks* with same tools/model | Runtime overhead excluding model/tool API latency plus full cost | Equivalent or more overhead |
| H4 verification | External acceptance gates reduce false-completion claims irrespective of loop representation | False positive completion / false negative rejection | No reduction, or excessive false negatives |
| H5 sustained progress | Long-horizon tasks benefit more from context/verification mechanisms than from changing the loop representation alone | Verified progress per token and task completion | Loop representation explains larger controlled gain |

## Controlled experimental arms

**Do not implement full competing products** just to produce a benchmark.
- Arm A: common minimal model-led while + async tools.
- Arm B: same engine and policies with reentrant explicit step state.
- Arm C: same actions and policies inside explicit graph, when a graph is natural.
- Optional D: stateless event-log stepper, only if experiment requires durable recovery.
- A separate 2×2 ablation **guard on/off × checkpoint on/off** to distinguish enforcement from representation. Never compare a fully featured graph to a toy while and credit graph abstraction.

## Paired workloads

- **W1 exploratory coding:** 10–20 tasks with uncertain investigation path (repo navigation, test fixes).
- **W2 fixed workflow:** 10–20 tasks with explicit approval/review/release stages.
- **W3 failure & recovery:** matched tasks with predeclared timeout/cancel/restart events.
- **W4 long horizon:** multi-file changes with acceptance tests and 10+ natural action opportunities.

Numbers are **candidate pilot sizes only**, not a statistical power calculation. Freeze final sample counts after a pilot and before confirmatory collection.

## Controls

Same exact provider/model snapshot, decoding configuration, prompt information, tools + schemas, sandbox/files, permission gates, context strategy, iteration/token/cost budget, timeout/retry configuration, task order randomized and repeated paired runs. Report requests, token counts, wall time, tool calls, tool failures and external effects. Set independent pass/fail oracles (tests, repo state and safety assertions).

**Critical confounder:** constrained graphs may solve different tasks if graph wiring adds domain knowledge. Provide the same workflow/acceptance facts to baseline prompts and log that distinction. Graph scaffolding could still change the feasible policy class; analyze rather than obscure it.

## Metrics and interpretation

- Task correctness: independent test/oracle pass %, not model self-report.
- Decision quality: acceptable-next-action under labeled state, with abstention allowed.
- Reliability: violating-run rate and erroneous external effects under specified faults.
- Liveness: completed progress / prematurely halted correct tasks.
- Cost: input/output tokens, tool operations, elapsed time, human intervention and engineering LOC/dependency count.
- Auditability: reconstructability and investigator diagnosis time (separately tested).

Publish paired task-level raw metrics, run conditions, confidence intervals, effect sizes, exclusions, and negative findings. Do not compare framework Stars as proof of technical efficacy.

## Before coding: A0-04 acceptance gate

1. Pin exact original Claude Code source-analysis versions and mark unconfirmed implementation paths as T.
2. Choose **one** narrow outcome and one alternative architecture. No seven-framework shootout.
3. First reuse published controlled studies such as [2609.20804](https://arxiv.org/abs/2609.20804) (loop fixed; different mechanisms) and [2609.32459](https://arxiv.org/abs/2609.32459). Their findings **do not** isolate while-vs-graph.
4. Build minimal paired harness variants only if a genuinely unanswered causal question remains.
5. Record cost, capacity and stopping rule; **no unbounded API runs**.

## Suggested first original test

**H2 reentrancy under interruption:** compare local-variables streaming coroutine and reentrant step with the *same* permission/tool semantics, with independent external effect oracle and a **real process restart**. Examine whether reentrancy reduces reconstruction complexity or safety failures, and whether it increases per-step overhead. This is a deliberately scoped follow-up, not a promise of statistically significant differences.
