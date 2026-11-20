# A0-03b: Community Research Reuse and Duplication Audit

**Date:** 2026-11-20. This is a literature/open-source audit, not an independent source dump or an empirical comparison.

## Existing work worth using rather than rewriting

| Project / report | Evidence | Useful existing conclusion | What it does **not** establish | Decision |
|---|---|---|---|---|
| [VILA-Lab/Dive-into-Claude-Code](https://github.com/VILA-Lab/Dive-into-Claude-Code/blob/main/docs/architecture.md) | Third-party source-level study; explicitly targets Claude Code **v2.1.88** | Reports shared `queryLoop`, model-led loop, tools/permissions/context in surrounding harness, context shaping and 9-stage pipeline | No controlled causal evaluation of while vs FSM/Graph; reported source analysis is not our independent authentication | **Reuse as principal architecture reference** |
| [VILA-Lab design guide](https://github.com/VILA-Lab/Dive-into-Claude-Code/blob/main/docs/build-your-own-agent.md) | Secondary design-space interpretation | Already compares model-led loops, explicit state graphs, planning, contexts, safety | Design-space rationale is not measured superiority | **Reuse comparisons; focus on missing experiments** |
| [cablate/claude-code-research](https://github.com/cablate/claude-code-research/blob/master/source-code-analysis/phase-09-harness-engineering/01-agent-loop-analysis.md) | Third-party v2.1.88 source analysis | Reports `query()`, `queryModel()`, `runTools()`, message feedback and abort | `query()` vs `queryLoop()` relationship not independently reconciled; no causal benchmark | **Cross-check module claims** |
| [6551Team/claude-code-design-guide](https://github.com/6551Team/claude-code-design-guide/blob/main/architecture/README_EN.md) | Independent-seeming engineering documentation that itself claims 1,884 TS files, v2.1.88 | 46 subsystem chapters including query engine, data flow, API client, tools, recovery | Claim independence and original artifact integrity not verified; counts differ across reports | **Use as a third lens; do not vote by number of reports** |
| [Harness Engineering: 11 systems](https://arxiv.org/abs/2609.00006) | Comparative source-code study | Existing broad taxonomy of agent harnesses including Claude Code, Codex, OpenHands, Aider, etc. | Source-code architecture comparison alone cannot establish performance causality | **Reuse taxonomy, don't repeat entire survey** |
| [Goose state-machine implementation and design discussion](https://github.com/aaif-goose/goose/discussions/9944) | Upstream community design plus subsequently published implementation | Unroll monolithic streaming loop into a reentrant per-turn state machine; concrete motivations are composability and explicit execution boundaries | The proposal is not a benchmark; migration is now documented as implemented in the Goose GDK (2026-09-16 post and Nov 2026 crate) | **Implemented alternative; use GDK docs as current reference** |
| [LangGraph interrupts documentation](https://github.com/langchain-ai/docs/blob/main/src/oss/langgraph/interrupts.mdx) | Implementation-owner documentation | Checkpointed graph interruptions, human review, resume | Does not show improved correctness on coding tasks versus Claude Code | **Use for Graph's explicit control requirements** |
| [LangGraph Functional API](https://github.com/langchain-ai/docs/blob/main/src/oss/langgraph/functional-api.mdx) | Implementation-owner docs | Restart/replay from checkpoint, memoized completed tasks and explicit side-effect cautions | Graph/Functional API are not identical; not guarantee of exactly-once side effects | **Design alternative to graph-only comparison** |
| [OpenHands SDK Agent](https://github.com/OpenHands/docs/blob/main/sdk/arch/agent.mdx) | Implementation-owner architecture docs | Stateless single-step `Agent.step()`, action/observation events, confirmation and condenser boundaries | Does not imply OpenHands is more accurate than Claude Code | **Primary open implementation alternative** |
| [OpenHands SDK design](https://github.com/OpenHands/docs/blob/main/sdk/arch/design.mdx) | Implementation-owner trade-off documentation | V0 mutable-state/sandbox coupling motivated V1 single conversation truth and composability | Vendor/project's stated engineering rationale, not a controlled evaluation | **Use for rationale and test candidate** |
| [Empirical Study of Harness Design](https://arxiv.org/abs/2609.20804) | Empirical work with 176 matched configurations, 4 models, SWE-bench Verified / Terminal-Bench 2.1 | Planning, action space and context strategy effects depend on model, tasks and budget | Loop architecture held fixed; **does not isolate while vs FSM/Graph** | **Reuse evaluation methodology and caution** |
| [Beyond the Model: Harness Effects](https://arxiv.org/abs/2609.32459) | Empirical multi-model, multi-benchmark + NanoHarness component study | Harness components can affect coding performance | Not a controlled Claude Code core-loop vs Graph test | **External evidence for "harness matters", not "while wins"** |
| [Harness-bench](https://github.com/tdrml/harness-bench) | Small community calibration experiment | Reports harness effects may depend on task horizon and intervention | Limited number/task set; not general proof of specific loop architecture | **Optional replication target, label scale limits** |

### Evidence independence warning

Several GitHub copies of VILA-Lab appear to be forks and are **not independent corroboration**. Multiple writeups of the same leaked snapshot may share assumptions. Verify source provenance and version, not counts of agreeing reports.

### Key reuse decision

**Do not recreate** a sprawling Claude Code internals encyclopedia or another generic agent framework. Produce an original **claim→alternative→trade-off→outcome** map and run *only* the comparisons that existing literature leaves unanswered.

### Open questions

1. Version-aligned `query()` → `queryLoop()` wrapper relationship remains **T, not S**.
2. Where do SDK/CLI control boundaries attach? reported shared core remains T.
3. Which loop mechanisms improve which outcomes at constant model, tasks and budget? **No causal conclusion from these readings.**
4. How does explicit orchestration trade flexibility for auditability, cost and pause/resume semantics in *equal-capability* workloads?

### Correction: Goose implementation is available (2026-11-20)

[Goose engineering blog, September 16, 2026](https://goose.vcorp.ai/blog/2026/09/16/agentic-state-machines/) states the classic loop was replaced with a reentrant state machine; [goose-agent 0.1.0-alpha.14](https://docs.rs/crate/goose-agent/0.1.0-alpha.14) was published November 17, 2026. The earlier #9944 discussion was a proposal at that time, **not the current implementation status**. Do not infer every Goose entry point has no legacy compatibility path without checking exact release/config. [A0-04 pilot](../A0-04-loop-comparison/REPORT.md) is independent Python only.

| [Vikash Rungta's architecture essay (2026-02-17)](https://vrungta.substack.com/p/claude-code-architecture-reverse) + [expanded Markdown](https://github.com/vkr11/ChainOfThought/blob/main/claude_code_architecture.md) | Behavioral/public-doc conceptual synthesis; predates leaked v2.1.88 source map | TAOR, model autonomy, primitive tools, context economy and harness enforcement as design questions | Not direct source verification, no pinned runtime trace or controlled benchmark; several overgeneralizations (Esc rewind, fixed compaction threshold, bypass mode) | **Reuse conceptual model, not source facts**; [audit](RUNGTA_ARTICLE_AUDIT.md) |
