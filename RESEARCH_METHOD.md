# Research Method / 固定研究方法

> Version 1.0 · 2026-11-20. This document governs every research iteration in this repository. A finding must be auditable, falsifiable and independently reproducible.

**Normative study goals, L1–L6 evidence requirements, and mandatory six-question analysis are defined in [RESEARCH_RULES.md](RESEARCH_RULES.md).** This file details the methodological workflow and publication requirements. Apply both.

## 1. Research loop

1. **Define a bounded question**: specify system boundary, workload, independent variable, outcomes, and exclusion criteria.
2. **Gather lawful evidence**: official docs and public behavior first; classify third-party reverse engineering as secondary evidence. Log source URL, author, publication date, version and claim-level support.
3. **Form competing explanations**: identify at least one alternative explanation and a null hypothesis; distinguish mechanism assumptions from observations.
4. **Pre-register an experiment**: primary metric, baseline, treatment, dataset, stopping rule, fault matrix and falsification criterion **before** observing outcomes.
5. **Implement minimal comparable systems**: same model, tasks, prompts, available information, tools, budget and recovery features unless one is explicitly the treatment.
6. **Execute and preserve**: record versions, seeds, raw traces, tool side effects, wall time, token counts, cost and failures. Keep deterministic mock tests separate from stochastic model evaluations.
7. **Analyze uncertainty**: present denominators, effect sizes, confidence intervals or run-to-run variation; disclose negative results and threats to validity.
8. **Publish one small iteration**: research note, runnable experiment, data, limitations, next question, and small PR/commit.

## 2. What 'falsifiable' means

A hypothesis is falsifiable when a feasible observation could contradict its prediction. It is not enough to say "State makes the Agent more reliable." Define *which failure*, *which measure*, *what comparison* and *what outcome would count against the claim*.

Template:
- **RQ**: Under [workload + failure condition], does [mechanism] change [observable outcome] compared with [baseline]?
- **H0**: No improvement on the pre-registered primary outcome.
- **H1**: [Direction and magnitude where justified].
- **Counterevidence**: [A result that rejects or fails to support H1].
- **Boundary**: [Model, tasks, execution environment, safety constraints].
- **Confounders**: [Model randomness, tool latency, retries, caching, task difficulty].
- **Decision**: support / not supported / inconclusive, with uncertainty.

A null result does not prove two methods are identical. Use equivalence/non-inferiority tests only when margins and sufficient statistical power are justified.

## 3. Evidence grades

| Label | Meaning | Allowed claim |
|---|---|---|
| S | Source-verified: original implementation artifact independently authenticated and inspected | What the inspected source directly supports for the pinned version, subject to paths/feature gates |
| O | Official, published specification or docs | What official docs state, within their version |
| T | Third-party code analysis or public observation | What the investigator reports, not an official guarantee |
| H | Hypothesis or architectural inference | Explicitly unverified |
| E-MOCK | Local deterministic simulation | Behavior of the simulation only |
| E-REAL | Measured real-model/system experiment | Behavior within the tested setup only |

Never treat a source-map leak as an open-source license. No proprietary source dumps, secret tokens, or private user data.

## 4. Experimental controls

Record task IDs, difficulty strata, model/version, temperature, tool schemas, context budget, retry and timeout policy, hardware/runtime, dates, API prices (if applicable), and sample size. Predefine failures, cancellations, and task success by **external oracles**, not the model's self-report.

Use paired task runs when feasible and randomized run ordering. For model evaluations use repeated independent runs and report dispersion; don't overgeneralize from mock demonstrations. Distinguish **quality** (correct outcome), **reliability** (correct execution under disturbance), **sustainability** (productive progress under finite resources), and **efficiency** (cost/latency).

## 5. Publication checklist

- [ ] Precise falsifiable RQ, H0/H1 and pre-registered success criterion
- [ ] Provenance and evidence grade for each claim
- [ ] Fair baselines, confounders and negative controls documented
- [ ] Reproduction command and version-locked environment
- [ ] Raw traces, summary data and any exclusions published
- [ ] Results supported by exact denominators; negative results reported
- [ ] Threats to validity, copyright/ethics considerations
- [ ] No unsupported claim about Claude Code's actual behavior

## 6. Deliverable format

`research/<iteration>/question.md` → `sources.md` → `design.md` → `experiments/<iteration>/` → `results/<iteration>/` → `report.md`. Existing Iteration 001 is a provisional simulation; it must not be retroactively presented as pre-registered.

## 7. Decision log is mandatory / 每轮研究决策必须留痕

For every completed iteration, append to the topic-specific `DECISION_LOG.md`: original research question and expectation, observed evidence (including negative results), competing interpretation, explicit change in direction, why the change is justified, and the next test capable of disproving the revised hypothesis. Do not erase previous direction changes or relabel post-hoc exploration as preregistered evidence. [R1 example](research/02-agent-loop/DECISION_LOG.md).

**Terminology:** prefer **执行安全约束** (execution safety constraints) for reader-facing Chinese explanations, introduce formal *invariant* in parentheses when technically required, and use **执行安全约束违规率** for the measured proportion. A state representation is distinct from enforcement of those rules.

## 8. Model and source provenance

Every iteration must explicitly state which model (if any) the experiment invoked, whether tools were mocked or real, and exactly which source claim motivated the implementation. Separate third-party descriptions from independently observed Claude Code behavior. Reference: [R1 model and source provenance](research/02-agent-loop/MODEL_AND_SOURCE_PROVENANCE.md).

## 9. Research scope admission gate

Before adding an experiment or a major implementation path, evaluate the [three-part Research Scope Gate](RESEARCH_GATE.md): evidence/ethics (mandatory), Agent Loop relevance, and experimental readiness. Save the gate outcome and decision; redirect valuable adjacent questions to a documented backlog rather than silently continuing scope expansion.

## 10. Observation tooling vs empirical results

Test success of an NDJSON parser on synthetic fixtures does **not** count as a live Claude Code trace. Reports must explicitly separate: official specification, source-analysis hypothesis, synthetic instrumentation tests, and observed versioned product behavior. No live-model conclusion without a recorded authenticated execution.

## 11. Source claim authentication and rights

A leaked or accidentally published source artifact may carry high evidentiary value **if independently authenticated**. This is separate from licensing and redistribution rights. Do not equate third-party source analysis with direct inspection. Record exact version, publisher provenance, original artifact hashes, file/symbol and runtime path before applying **S (source-verified)**. Otherwise use **T (third-party analysis)** or **H (hypothesis)**. Never republish proprietary source dumps. See [A0-03 claim registry](research/A0-03-source-control-flow/SOURCE_CLAIMS.md).
