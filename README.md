# Claude Code Harness Study

**Evidence-first analysis, independent implementations, and reproducible experiments for LLM Agent Harness engineering.**

[中文说明](README.zh-CN.md) · [References library](references/README.md) · [Research plan](PLAN.md) · [Research rules](RESEARCH_RULES.md) · [A0-01 evidence map](research/A0-01-agent-loop-path/REPORT.md) · [A0-03 source audit](research/A0-03-source-control-flow/REPORT.md) · [Existing research](research/A0-03-source-control-flow/COMMUNITY_REUSE.md) · [Design alternatives](research/A0-03-source-control-flow/ALTERNATIVE_DESIGNS.md) · [A0-04 first controlled experiment](research/A0-04-loop-comparison/REPORT.md) · [A0-02 observability report](research/A0-01-agent-loop-path/A0-02-REPORT.md) · [A0-02b public traces](research/A0-01-agent-loop-path/A0-02B-REPORT.md) · [Falsifiable Agent Loop questions](research/02-agent-loop/questions.md) · [R1 study](research/02-agent-loop/R1-PROTOCOL.md) · [R1 iteration 02](research/02-agent-loop/R1-ITERATION-02.md) · [R1 iteration 03](research/02-agent-loop/R1-ITERATION-03.md) · [Model & source provenance](research/02-agent-loop/MODEL_AND_SOURCE_PROVENANCE.md) · [Decision log](research/02-agent-loop/DECISION_LOG.md) · [Agent Loop analysis](docs/01-agent-loop/analysis.md) · [Evidence ledger](docs/01-agent-loop/evidence.md)

> Independent research project. Not affiliated with or endorsed by Anthropic. No leaked or proprietary Claude Code source code is redistributed here.

## Research rules: L1–L6 + six questions

[**RESEARCH_RULES.md**](RESEARCH_RULES.md) is the single normative research document: L1–L6, six-question analysis, academic methodology attribution, evidence grades, reproducible research procedure, G0/G1/G2 admission gates, and completion rules. The older Research Method/Gate files were merged into it.

## A0-05: expanded evidence survey (2026-11-21)

[**12 priority references (Chinese)**](references/TOP_12_REFERENCES.md) · [**31-item literature audit**](research/A0-05-literature-expansion/SEARCH_REPORT.md) · [**priority reading and next research path**](research/A0-05-literature-expansion/PRIORITY_PATH.md)

Expanded beyond Claude Code v2.1.88 reverse-engineering posts to first-party engineering decisions, independently controlled harness evaluations, cross-scaffold studies, and public real-session evidence. **Key synthesis:** Loop activation/termination, model decision authority, runtime reentry, session/context persistence, action authorization, and independent task verification are **separate research dimensions**. Across available studies, *harness effects are conditional on workload, model and budgets*; no general causal superiority of a Claude Code-style `while` over Goose-style `step` is established.

**Recommendation:** prioritize a paired **model-stop vs independent-goal-verification** evaluation for task effectiveness; keep reentry/approval as a narrowly scoped runtime-overhead experiment. Do not keep generating toy parity tests and generalize from pass counts.

## A0-04-03: pinned open benchmark vectors and Rungta article audit

[**A0-04-03 benchmark comparison**](research/A0-04-loop-comparison/A0-04-03-REPORT.md) · [**Reusable adapter and tests**](experiments/a0_04_03_bench/benchmark.py) · [**Results**](results/a0-04-03-adapted-bench.json) · [**Rungta architecture essay audit**](research/A0-03-source-control-flow/RUNGTA_ARTICLE_AUDIT.md)

Local execution: 11 unit tests passed; both arms satisfied 21 **upstream-derived input vectors** and 10 **locally authored boundary extensions** with an identical scripted policy. This is **not** an official upstream benchmark run or a Claude Code/Goose product comparison. A separate deterministic two-host stale-snapshot interleaving demonstrated one effect after a competing cancellation; **no real concurrency** was used. The Rungta essay (2026-02-17) offers conceptual design insights but not original v2.1.88 source verification. **Model autonomy and reentrant scheduling are independent axes.**

## A0-04-02 approval handoff pilot + open benchmarks

[**Approval handoff report**](research/A0-04-loop-comparison/A0-04-02-REPORT.md) · [**Open benchmark inventory**](research/A0-04-loop-comparison/OPEN_BENCHMARKS.md) · [**Controller code**](experiments/a0_04_02_approval/experiment.py) · [**Regression tests**](experiments/a0_04_02_approval/test_experiment.py)

Six scripted approval/deny/cancel/reentry tests showed matched results in both arms. The simulator's streaming-style arm reconstructs from a checkpoint; this limits its value as a live-stack vs reentrant architecture comparison. **These tests are not a public benchmark**, and no real Claude Code, Goose or LLM was run. Next priority: reuse third-party approved-action boundary and fault suites and independently validate effect oracles.

## A0-04 pilot: streaming loop vs reentrant step

[**Controlled comparison report**](research/A0-04-loop-comparison/REPORT.md) · [**Independent implementation**](experiments/a0_04_loop_comparison/experiment.py) · [**Results**](results/a0-04-pilot.json)

Four local tests passed, including a **real child-process SIGKILL** after the turn-2 atomic checkpoint followed by fresh-process resume. Both the streaming-generator and reentrant-step controllers finished with 5 scripted decisions, 4 mock tool effects and matching traces. **No Claude/Goose executable or LLM was invoked.** This is a deliberately narrow negative finding: with equal checkpointing, **reentrancy alone did not improve recovery in this scenario**. Mid-tool failures and comparative overhead remain untested.

**Research update:** Goose's reentrant GDK is already implemented and published in 2026; it must not be described as merely a proposal.

```bash
python3 -m unittest discover -s experiments/a0_04_loop_comparison -p 'test_*.py' -v
```

## A0-03b: existing research, alternatives and evaluation

[**Community research reuse**](research/A0-03-source-control-flow/COMMUNITY_REUSE.md) · [**Seven architectural patterns and trade-offs**](research/A0-03-source-control-flow/ALTERNATIVE_DESIGNS.md) · [**Falsifiable evaluation plan (no results yet)**](research/A0-03-source-control-flow/EVALUATION_PLAN.md)

Prior art already analyzes Claude Code v2.1.88 extensively. OpenHands, Goose and LangGraph expose alternative event-stepped, reentrant state-machine and graph/functional execution patterns. **No reviewed evidence proves that Claude Code's loop representation itself is causally superior**. The next study should isolate one mechanism under paired workloads and model/tool parity; do not build a seven-framework benchmark by default.

## Current mainline: A0-03 source-claim audit

[**A0-03 report**](research/A0-03-source-control-flow/REPORT.md) · [**source claim registry**](research/A0-03-source-control-flow/SOURCE_CLAIMS.md) · [**next verification steps**](research/A0-03-source-control-flow/NEXT_STEPS.md)

We confirmed the historical v2.1.88 source-map exposure and cross-checked two pinned third-party architectural reports. **No original leaked source-map artifact was retrieved and authenticated; no function-level claim is labeled source-verified (S).** Current module call graphs remain version-scoped third-party evidence (T), not official source facts.

## Current mainline: A0-01 evidence-first Agent Loop mapping

[**A0-01 report**](research/A0-01-agent-loop-path/REPORT.md) establishes a claim-by-claim distinction between official Claude Code behaviors and third-party source analysis of the reported v2.1.88 snapshot. [**A0-02 entry criteria**](research/A0-01-agent-loop-path/NEXT_STEPS.md) specify observable CLI/SDK traces and version checks. [**Scope gate**](RESEARCH_RULES.md#14-g0g1g2-研究准入门槛) blocks unrelated runtime infrastructure work. The prior R1 simulations remain exploratory side experiments, not Claude Code behavior verification.

## A0-02: observing the released CLI

[**A0-02 report**](research/A0-01-agent-loop-path/A0-02-REPORT.md) · [**Safe runbook**](research/A0-01-agent-loop-path/a0_02/RUNBOOK.md) · [**Event summarizer**](research/A0-01-agent-loop-path/a0_02/trace_summary.py)

The official CLI supports observable `stream-json` messages; however **this research environment has no Claude Code executable or authentication**, so **no genuine CLI traces were recorded**. A privacy-reduced JSONL summarizer and four synthetic unit tests are ready. Neither the synthetic fixtures nor previous Mock experiments establish Claude Code internal function behavior.

```bash
python -m unittest discover -s research/A0-01-agent-loop-path/a0_02 -p 'test_*.py' -v
```

## A0-02b: community native-session evidence

[**Public trace evidence & limitations**](research/A0-01-agent-loop-path/A0-02B-REPORT.md) · [**Dataset manifest**](research/A0-01-agent-loop-path/a0_02/DATA_SOURCES.md) · [**Session JSONL analyzer**](research/A0-01-agent-loop-path/a0_02/session_analyzer.py)

A real publicly hosted Claude Code v2.1.177 trace was reviewed through its Hugging Face viewer. **The complete raw trace could not be downloaded here, so this project does not claim measured real-file tool-pair counts**. The native-session adapter passed five **synthetic** unit tests; external file processing is documented, not falsely reported as executed.

```bash
python3 -m unittest discover -s research/A0-01-agent-loop-path/a0_02 -p 'test_*.py' -v
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
