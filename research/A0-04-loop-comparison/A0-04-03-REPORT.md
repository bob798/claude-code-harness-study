# A0-04-03 — Public Benchmark Vectors for Approval and Action Boundary

**Study date:** 2026-11-21. **Status:** local adapter executed; upstream scorer execution not yet confirmed. **Evidence type:** E-ADAPTED-SYNTHETIC. Not Claude Code/Goose benchmark performance.

## Pinned sources and exact reuse scope

1. [AgentBench (aymaw), commit 6535492](https://github.com/aymaw/agentbench/tree/6535492fe8118733d3bc07849c4facb3647973c9) — MIT, `agentbench/benchmark.py` Git blob `00e1f19939076cbf98042462a47b60442d3b1425`. Adapted **nine named + twelve seed=7 generated scenario configurations and expected outcomes**. We **did not** execute or import the upstream scoring implementation in the local result.
2. [Agent Action Boundary Benchmark (OndCo), commit 70c86e9](https://github.com/OndCo/Agent-Action-Boundary-Benchmark/tree/70c86e99b4af93dd66c6a04838e3fe1c873aa526) — Apache-2.0, `README.md` blob `5d6f57dd5dc729407c90fccfe870c63a2cf1900c`. Its action-identity/parameter-drift taxonomy inspired **ten original extensions B0–B9**. They are **not** upstream official case IDs or authored test rows.

The source repository commits and blobs were obtained via GitHub before writing the adapter. [`verify_upstream.py`](../../experiments/a0_04_03_bench/verify_upstream.py) checks exact scenario parity when an independently cloned pinned upstream checkout is available; no successful upstream verifier run is claimed here.

## Test designs

The two arms are minimal original Python controls: a `streaming_generator` and a `reentrant_step`. They run the **same** scripted transition function and in-memory tool world, with the same budgets, approvals and expected effects. No LLM call or proprietary product is involved.

- **U0–U20 (21 adapted inputs)**: normal success, approval denial, capacity deficit, budget exceedance, read errors, uncertain write, text injection artifacts and 12 seeded cases. Injection text is **not evaluated by a model** and therefore no prompt-injection safety claim follows.
- **B0–B9 (10 original extensions)**: exact approved action; mutated tool; mutated argument; denial; cancellation with late grant; stale grant after restart; committed effect with lost acknowledgement and stable ID; duplicate grant; replay with new operation ID; reapproval after restart.
- **Separate negative test:** two hosts with independently copied approval state: one host cancels while the other commits from its stale snapshot. This is **deterministic interleaving**, not a measured real concurrent subprocess race.

Eleven local `unittest` cases were executed, including a pair of scenarios where **each event ran in a fresh child Python process** reading/writing JSON. Those are process-separated event invocations, **not** a forced mid-operation kill or an atomic multi-writer system.

## Actual local results

| Measure | Streaming generator | Reentrant step |
|---|---:|---:|
| Adapted AgentBench input cases satisfying local expected-outcome oracle | 21 / 21 | 21 / 21 |
| Original action-boundary extension cases satisfying local effect oracle | 10 / 10 | 10 / 10 |
| Local regression tests (shared suite) | 11 / 11 | 11 / 11 |
| Model/API calls | 0 | 0 |
| Product runtime calls (Claude Code / Goose) | 0 | 0 |
| Per-case differences on shared state-policy simulator | 0 | 0 |

**Important negative finding:** snapshot interleaving produces **one external effect after the other host has cancelled**, because there is no shared linearizable authority/fencing. This affects both arms in principle; controller style alone is insufficient.

Do not interpret 21/21 as the official upstream benchmark score: **we adapted scenario vectors and authored an intentionally simple shared domain solver**. There is no independent blind sample, no test split and no model inference. Our expected-outcome oracle in these tests does not establish realistic agent robustness.

## Reproduction

```bash
python3 -m unittest discover -s experiments/a0_04_03_bench -p 'test_*.py' -v
python3 experiments/a0_04_03_bench/benchmark.py > /tmp/a0-04-03-full.json
```

Source files: [benchmark.py](../../experiments/a0_04_03_bench/benchmark.py), [test_benchmark.py](../../experiments/a0_04_03_bench/test_benchmark.py), [event_cli.py](../../experiments/a0_04_03_bench/event_cli.py). Compact results: [a0-04-03-adapted-bench.json](../../results/a0-04-03-adapted-bench.json). Dataset-origin and local extension results are kept separate.

## Interpretation and direction

**Initial intent:** find externally grounded tests that distinguish loop scheduling choices in safety outcomes.  
**Finding:** independent-origin scenario definitions increase case coverage, but with identical policy/decision and no actual concurrent system, both arms are semantically identical. The stale-snapshot negative test identifies a shared coordination defect; it does not favor either architecture.  
**Change:** stop expanding deterministic cases as if more matched outcomes imply framework superiority. Select an experiment that actually varies **host control-transfer latency/complexity** or durable state synchronization while preserving equally enforced policy. Add real-model coding tasks only after architecture-level treatment can be isolated.  
**Next falsification:** make host-triggered approval/abort concurrent with a pending real tool operation; use an independent ledger and serializable transaction or versioned CAS, with an explicit comparison of developer complexity and latency. Do not mistake the effect of stronger locking for that of reentrancy.

## Related third-party interpretation

Vikash Rungta's 2026-02-17 [architecture essay](../A0-03-source-control-flow/RUNGTA_ARTICLE_AUDIT.md) is useful for **model autonomy vs harness enforcement**, but does not provide benchmarks or prove the event-controller architecture. These are independent design dimensions.
