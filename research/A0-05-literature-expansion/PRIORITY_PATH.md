# A0-05 — Reading Order, Research Decisions and Test Priorities

**Date:** 2026-11-21. **Output type:** research synthesis, not an experiment.

## Five resources to read *first*

These are chosen for **new information relative to A0-03/A0-04**, not because they have the most pages or GitHub stars.

1. **[Official Loop engineering](https://claude.com/resources/articles/getting-started-with-loops) (2026-06-30)** — four distinct loop levels by trigger and stopping criterion. **Use:** keep `queryLoop` implementation separate from task-scale completion controllers (`/goal`) and recurring schedulers.
2. **[Official Managed Agents architecture](https://www.anthropic.com/research/managed-agents) (2026-04-08)** — append-only durable sessions and replaceable stateless harness processes. **Use:** reentrancy is a system boundary / host concern, not a philosophical opposition to model-led decision-making. This is a *different service* from Claude Code CLI.
3. **[Official auto mode design](https://www.anthropic.com/research/claude-code-auto-mode) (2026-03-25)** — denied actions feed back into the model and have bounded escalation; two-stage side-effect classifier. **Use:** safety and liveness belong in the same test; rejection alone is not success.
4. **[Harness or Model?](https://arxiv.org/abs/2609.11987) (2026-09)** — an actual paired same-model comparison where the average effect was not clearly nonzero and task groups differed. **Use:** stratify workloads and avoid positive-only hypothesis.
5. **[Same Model, Different Harness](https://arxiv.org/abs/2608.26218) (2026-08)** — tight-context controlled study and openly specified partial-progress metric F2PF. **Use:** evaluate both completed correctness and meaningful partial task progress, and avoid mistaking fewer model turns for higher efficiency.

## Second pass — targeted source details

- [Claude Code from Source — Ch05 Loop](https://github.com/alejandrobalderas/claude-code-from-source/blob/main/book/ch05-agent-loop.md)
- [Claude Code from Source — Ch07 Concurrency](https://github.com/alejandrobalderas/claude-code-from-source/blob/main/book/ch07-concurrency.md)
- [liuup — Tool Call implementation](https://github.com/liuup/claude-code-analysis/blob/main/analysis/04b-tool-call-implementation.md)
- [VILA-Lab, arXiv v3](https://arxiv.org/abs/2604.14228v3)
- [cablate source analysis](https://github.com/cablate/claude-code-research)

**What to extract, not copy:** transition conditions, state lifetime, permission-to-effect guard, streaming launch trigger, error-result feedback, cancellation points, version/feature-flag caveats.

## Third pass — measurement method

- [176-setting matched harness study](https://arxiv.org/abs/2609.20804): factorial ablations and conditional effects.
- [Anthropic infrastructure noise](https://www.anthropic.com/research/infrastructure-noise): pin CPU, RAM and enforcement, not merely model/task.
- [Tool-surface crossed ablation](https://arxiv.org/abs/2607.10569): stratify task type × agent × action surface.
- [DCAS](https://arxiv.org/abs/2608.06113): swapping scaffolds is not necessarily swapping the training distribution or planning conventions.
- [Re-evaluating harness evolution](https://arxiv.org/abs/2607.12227): do not iterate on public test cases and then call the same cases a held-out evaluation.

## Architecture model to use in this project

Do **not** collapse all layers into a binary `while` vs `Graph` debate.

| Layer | Research axis | Example independent values | Relevant sources |
|---|---|---|---|
| L0 | **Activation / horizon** | prompt, goal, timer, event/proactive | Official Loop engineering |
| L1 | **Decision authority** | model picks action vs host picks fixed workflow step | VILA-Lab, Rungta, LangGraph |
| L2 | **Runtime schedule / reentry** | long-lived coroutine vs discrete host-driven steps | Goose GDK, OpenHands, Managed Agents |
| L3 | **Session vs working context** | one transcript; durable event log + projected context; reset vs compaction | Managed Agents, long-running harness research, context studies |
| L4 | **Action authority** | static gates, approval, classifier, hooks, sandbox | Claude Code auto mode and official security docs |
| L5 | **Completion oracle** | model declares done; test suite/goal evaluator; human signoff | Official goal loops, generator/evaluator harness |

**Important:** These are design axes, not a claim that all values are independent in actual product implementations. For a causal experiment, vary one factor or specify factorial interactions; keep the others matched.

## What to stop doing

- Stop treating **more synthetic pass counts** as evidence of product architecture superiority. A0-04-03's 21/21 and 10/10 only establish scripted fixtures + matched policy conformance.
- Stop copying source tree summaries from additional leak-derived repos. Focus on discrepancies with actual experimental consequences.
- Stop calling a whole-platform performance difference a **Loop syntax effect**.
- Stop treating context resets, tool execution durability and external-task verification as a single recovery mechanism.
- Stop using a model's `end_turn` as the acceptance oracle.

## Next two high-value research choices

### Option A (recommended for a meaningful Agent Loop performance study): Goal termination + independent verification

**Question:** At identical model, tools, budget and task inputs, does adding an *independent goal verifier* to a model-led coding Loop reduce **false completion** and increase correctly completed tasks, and at what token/latency price?

- Control: model-led Loop, ordinary final answer/stop semantics.
- Treatment: identical Loop plus verification step before accepting final outcome; bounded retries with identical maximum total model/tool budget and a clear limit for verifier cost.
- Workload: pinned, independent coding benchmark subset with tests not exposed as training examples to the agent; preregister task IDs and held-out final evaluation.
- Metrics: exact correct completion, false-completion rate, verification false-reject rate, F2PF where relevant, wall time, token/cost/human intervention.
- Novelty caution: Anthropic official `/goal` and generator/evaluator work already show this design pattern; **replicate and extend conditional cost/benefit**, do not claim to invent verification loops.

### Option B (preserve original A0-04 structural question): Host reentry costs

**Question:** Under the **same** policy and persistence, what is the measurable tradeoff of a long-lived streaming generator vs a reentrant step when host must pause at tool-selection, wait for approval, then resume?

- Distinguish persistent process-local coroutine from checkpointed generator that is reconstructed (current mocks inadvertently compare two resumable patterns).
- Add actual concurrent host events and an independent side-effect recorder; use **same CAS/fencing/authorization rules** for both arms.
- Metrics: p50/p95 handoff/resume latency, state bytes, process memory, number of explicit transitions and source LOC, correct effect count, observed losses/errors.
- Include null results; never generalize to *actual* Claude Code/Goose behavior until testing their running implementations.

## Recommendation and status

**Research recommendation:** do **Option A** first if the goal is publishable evidence of *task effectiveness*. **Option B** remains valuable if the goal is engineering comparison of *orchestration mechanics*. Both require genuine isolated observations, not more shared-transition toy fixtures. No new experiment was executed in A0-05.

Source inventory: [SEARCH_REPORT.md](SEARCH_REPORT.md). Related existing research: [A0-04 controlled-pilot report](../A0-04-loop-comparison/REPORT.md).
