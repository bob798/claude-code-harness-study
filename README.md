# Claude Code Harness Study

**Evidence-first analysis, independent implementations, and reproducible experiments for LLM Agent Harness engineering.**

[中文说明](README.zh-CN.md) · [Research plan](PLAN.md) · [Research method](RESEARCH_METHOD.md) · [Research scope gate](RESEARCH_GATE.md) · [A0-01 evidence map](research/A0-01-agent-loop-path/REPORT.md) · [A0-02 observability report](research/A0-01-agent-loop-path/A0-02-REPORT.md) · [Falsifiable Agent Loop questions](research/02-agent-loop/questions.md) · [R1 study](research/02-agent-loop/R1-PROTOCOL.md) · [R1 iteration 02](research/02-agent-loop/R1-ITERATION-02.md) · [R1 iteration 03](research/02-agent-loop/R1-ITERATION-03.md) · [Model & source provenance](research/02-agent-loop/MODEL_AND_SOURCE_PROVENANCE.md) · [Decision log](research/02-agent-loop/DECISION_LOG.md) · [Agent Loop analysis](docs/01-agent-loop/analysis.md) · [Evidence ledger](docs/01-agent-loop/evidence.md)

> Independent research project. Not affiliated with or endorsed by Anthropic. No leaked or proprietary Claude Code source code is redistributed here.

## Current mainline: A0-01 evidence-first Agent Loop mapping

[**A0-01 report**](research/A0-01-agent-loop-path/REPORT.md) establishes a claim-by-claim distinction between official Claude Code behaviors and third-party source analysis of the reported v2.1.88 snapshot. [**A0-02 entry criteria**](research/A0-01-agent-loop-path/NEXT_STEPS.md) specify observable CLI/SDK traces and version checks. [**Scope gate**](RESEARCH_GATE.md) blocks unrelated runtime infrastructure work. The prior R1 simulations remain exploratory side experiments, not Claude Code behavior verification.

## A0-02: observing the released CLI

[**A0-02 report**](research/A0-01-agent-loop-path/A0-02-REPORT.md) · [**Safe runbook**](research/A0-01-agent-loop-path/a0_02/RUNBOOK.md) · [**Event summarizer**](research/A0-01-agent-loop-path/a0_02/trace_summary.py)

The official CLI supports observable `stream-json` messages; however **this research environment has no Claude Code executable or authentication**, so **no genuine CLI traces were recorded**. A privacy-reduced JSONL summarizer and four synthetic unit tests are ready. Neither the synthetic fixtures nor previous Mock experiments establish Claude Code internal function behavior.

```bash
python -m unittest discover -s research/A0-01-agent-loop-path/a0_02 -p 'test_*.py' -v
```

## What you can reproduce now

**Experiment 001: What happens when a tool commits a side effect but its response is lost?**

Run locally with Python 3.10+, without credentials or network:

```bash
python -m unittest discover -s experiments/loop_recovery -p 'test_*.py' -v
python experiments/loop_recovery/experiment.py
```

This small deterministic **mock** experiment compares blind retry and stable idempotency-key retry. It tests an independent design, **not Claude Code itself**; results should not be generalized to production agents.

## R1 pilot: explicit State vs local variables

Five deterministic scenarios produced identical traces and zero invariant violations in both matched variants. This is a **mock smoke test**, not evidence that State increases reliability. [Protocol and limitations](research/02-agent-loop/R1-PROTOCOL.md).

```bash
python -m unittest discover -s experiments/r1_state -p 'test_*.py' -v
python experiments/r1_state/experiment.py
```

## R1 iteration 02: representation vs enforced transitions

In a deliberately permissive deterministic toy model, **249/258** short traces accepted at least one disallowed event with either local variables or typed State. Adding a transition validator rejected all specified illegal events (**0/258** violating traces). This isolates a rule-enforcement mechanism, **not** a Claude Code observation or proof that typed State improves reliability. [Analysis and limitations](research/02-agent-loop/R1-ITERATION-02.md).

```bash
python -m unittest discover -s experiments/r1_transitions -p 'test_*.py' -v
python experiments/r1_transitions/experiment.py
```

## R1 iteration 03: checkpoint vs state representation

Deterministic **mock** crash/cancel event replay (5 scenarios, 4 arms, 5 unit tests). State as a dataclass vs local dictionary changed no results when policies matched. In a deliberately constructed cancel-then-crash sequence, a checkpoint preserved cancellation and blocked redispatch; a volatile variant lost it. **No LLM calls were made.** Checkpoint alone does not resolve ambiguous committed tool effects. [R1-03 report](research/02-agent-loop/R1-ITERATION-03.md) · [Source/model attribution](research/02-agent-loop/MODEL_AND_SOURCE_PROVENANCE.md).

```bash
python -m unittest discover -s experiments/r1_recovery -p 'test_*.py' -v
python experiments/r1_recovery/experiment.py
```

## Research method

Every iteration follows: **question → public evidence → architectural interpretation → implementation → baseline comparison → reproducible result → limitations**.

Claims are labeled:
- **O (official):** publicly documented by Anthropic or upstream maintainers.
- **T (third-party):** published reverse-engineering interpretation requiring cross-checking.
- **H (hypothesis):** our proposed explanation or mechanism.
- **E (experiment):** independently obtained measurement with explicit scope.

## Research map

| Iteration | Question | Status |
|---|---|---|
| 001 · Agent Loop | What happens when a tool result is lost after execution? | Mock experiment available |
| 002 · State and recovery | Separate typed State, guards, and checkpoint effects | R1-01/02/03 exploratory mock studies available |
| 003 · Tool execution | When are parallelism and retries safe? | Planned |
| 004 · Context compaction | How do token savings trade off against constraint retention? | Planned |
| 005 · Harness evaluation | Which mechanisms improve reliability across real tasks? | Planned |

## Principles

1. Source provenance before interpretation. Never present an inference as verified source behavior.
2. Compare functionally equivalent baselines.
3. Report failures, variance, and limitations alongside results.
4. No proprietary source dumps or unlicensed redistributions.
5. Keep the loop small; test each engineering mechanism independently.

Contributions with an issue reproduction, evidence correction, or new baseline are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).
