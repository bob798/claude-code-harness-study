# Claude Code Harness Study

**Evidence-first analysis, independent implementations, and reproducible experiments for LLM Agent Harness engineering.**

[中文说明](README.zh-CN.md) · [Research plan](PLAN.md) · [Agent Loop analysis](docs/01-agent-loop/analysis.md) · [Evidence ledger](docs/01-agent-loop/evidence.md)

> Independent research project. Not affiliated with or endorsed by Anthropic. No leaked or proprietary Claude Code source code is redistributed here.

## What you can reproduce now

**Experiment 001: What happens when a tool commits a side effect but its response is lost?**

Run locally with Python 3.10+, without credentials or network:

```bash
python -m unittest discover -s experiments/loop_recovery -p 'test_*.py' -v
python experiments/loop_recovery/experiment.py
```

This small deterministic **mock** experiment compares blind retry and stable idempotency-key retry. It tests an independent design, **not Claude Code itself**; results should not be generalized to production agents.

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
| 002 · State and recovery | Does explicit state improve recovery when capabilities are controlled? | Planned |
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
