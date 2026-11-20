# Research and Growth Plan

## Goal
Study publicly documented and independently analyzed Claude Code internals, implement minimal Harness mechanisms without copying proprietary code, and publish reproducible experiments.

## Iterations

| ID | Research question | Deliverable | Exit criterion |
|---|---|---|---|
| 001 | How can retries duplicate an effect? | Mock experiment + tests + evidence notes | Deterministic two-baseline demonstration |
| 002 | Does explicit State help recovery? | Comparable implementations + fault matrix | Same feature set; measured recovery and complexity |
| 003 | When are tool calls safe to retry/parallelize? | Execution adapter + conflict tests | Side-effect assertions and documented caveats |
| 004 | What is the cost–fidelity trade-off in context compaction? | Real-task benchmark + preservation tests | Success, retention, token cost, latency |
| 005 | Which Harness mechanisms generalize? | Ablations + reproducibility report | Multiple tasks, confidence intervals and limitations |

## First 30 days

- Week 1: evidence ledger, first runnable experiment, README, CI.
- Week 2: state-recovery comparison; publish an English technical note with raw results.
- Week 3: tool executor study; invite independent reproduction and corrections.
- Week 4: context task design; report measured progress and limitations.

## Evidence standard

Record URL, author, publication/version/date, exact supported claim, confidence, and interpretation boundaries. Treat third-party source analyses as secondary evidence. Avoid unlicensed source redistribution.

## Experiment protocol

- State the hypothesis and pre-register primary metric.
- Use controlled equivalent baselines and identical workloads.
- Record random seeds, runtime, model/configuration, cost, and failures.
- Distinguish deterministic simulation from model-based evaluation.
- Save raw measurements, scripts, and reproduction instructions.

## Visibility without spam

Publish complete runnable examples before sharing. Use a clear English landing page, GitHub topics, substantive technical writing, and relevant upstream discussions. Track external reproductions, useful issues, and citations along with Stars. Do not promise a Star target.

## Stop rules

If an experiment cannot isolate the proposed mechanism, redesign it before making a causal claim. If a feature has no real research question or user, defer it. Do not build a generic Agent framework before the narrow reliability experiments succeed.
