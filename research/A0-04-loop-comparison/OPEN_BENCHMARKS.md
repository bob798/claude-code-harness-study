# Open Benchmark Reuse: A0-04-02 Approval/Interruption

**Audit date:** 2026-11-21. **Purpose:** keep unit-test regressions separate from independent benchmark evidence.

| Benchmark | URL | Existing evaluation | Reuse for A0-04-02 | Caution |
|---|---|---|---|---|
| Agent Action Boundary Benchmark | https://github.com/OndCo/Agent-Action-Boundary-Benchmark | Approved action vs executed action, provenance of side effect | **Priority 1**: action/argument identity, replay, execution drift | Specialist project; verify task files, version and test oracle before adopting |
| AgentBench (aymaw) | https://github.com/aymaw/agentbench | 21 closed synthetic scenarios, approval/fault/uncertain writes, trace scoring | **Priority 1–2**: deterministic failure and guarded actions | Small emerging project; demo is scripted, not empirical model performance |
| AgentDojo | https://github.com/ethz-spylab/agentdojo | Tool-using agent prompt-injection attacks and defenses | **Priority 2**: security of authorization paths | Security benchmark, does not natively score reentrant control |
| harness-bench (NaC-L) | https://github.com/NaC-L/harness-bench | Agent coding task correctness, latency, tokens, prohibited edits, recovery examples | **Priority 2**: end-to-end harness adapter | Small community suite; distinguish synthetic from real-model runs |
| Terminal-Bench | https://github.com/harbor-framework/terminal-bench | Real terminal task + independent tests; Terminal-Bench 2.0 has 89 tasks | **Priority 3**: external model/task success, cost and time | No built-in matching approval/cancellation fault matrix |
| tau2-bench | https://github.com/sierra-research/tau2-bench | Agent+user+tool coordination with policy-constrained domains | Optional: external user intervention and tool-policy interactions | More customer-service than coding; model/user simulation confounds |

## Selection and non-duplication decision

A0-04-02 has **six locally written unit tests**. These are useful only as **regression fixtures**. They were not independently designed, sampled or held out and cannot justify general architectural conclusions.

Plan:
1. Pin exact commit/official release of the selected external suite and **check its license**.
2. Extract or adapt a small predeclared subset covering: (B1) approved tool identity preserved; (B2) arguments changed after approval; (B3) denied tool never executes; (B4) cancelled task ignores stale grant; (B5) repeated approval and replay; (B6) failure/uncertain-write handling.
3. Map suite's oracle to a common external effect recorder; same tool schemas and policy inputs for both arms. **No special guards only in one arm.**
4. Separate **benchmark-origin test vectors** from our added fault-injection extensions; record upstream test IDs and adaptations, do not present new extensions as upstream's official cases.
5. Collect process restart and concurrent event tests before live-model workloads.
6. Only after those pass, optionally integrate fixed Terminal-Bench 2.0 task subset for task success, tokens and latency.

## Required evaluation outcomes

- Unauthorized effects (count and rate, independent recorded side effects)
- Approval-to-execution action/argument equivalence
- Duplicate effects and lost actions
- Recovery and completed valid operations
- False denials and cancellation success
- Decision/model call count, state serialization size, wall time and CPU overhead
- Terminal-Bench task success (later only)

**Avoid confounding:** identical model, tools, policies, workloads, checkpoint semantics and error injection. The question is **where orchestration design changes behavior/cost**, not whether a more heavily guarded arm blocks more bad calls.

## Status

**Research inventory only.** No external suite downloaded, executed or integrated in this iteration. No 21-case or 89-case success rate is claimed for this project.

Sources: project README and official docs as cited in the associated research conversation.
