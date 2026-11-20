# A0-05 — Expanded Claude Code / Agent Harness Literature Search

**Research date:** 2026-11-21. **Scope:** public materials published by that date; not a benchmark execution.  
**Aim:** identify non-redundant evidence that helps explain **implementation**, **engineering choice**, and **measurable value**, and make the next original study more defensible.

## Executive finding

The incremental value of another unscoped Claude Code v2.1.88 source-map walkthrough is low. Existing source analyses are extensive. The higher-yield route combines **pinned source analysis**, **Anthropic's first-person engineering accounts**, **matched same-model studies** and **trace/benchmark methodology**. Crucially, evidence of a strong **harness effect** does **not** imply that one syntax for the Loop (`while` vs reentrant `step`) caused the effect.

**Do not count forks or translations of the same source analysis as independent confirmation.** Do not conflate Claude Code CLI, Claude Agent SDK, Managed Agents, and community/third-party runtimes.

### Evidence notation

- **O**: first-party engineering explanation/documentation; authentic for its stated product and period but not necessarily a universal, experimentally verified guarantee.
- **T-SOURCE**: third-party inspection of a versioned implementation; not an independently authenticated original source artifact in this project.
- **T-CONCEPT**: explanatory essay/guide without independent function-level proof.
- **E-EXT**: reported external study with explicit datasets/controls/results; review confounding, reproducibility and uncertainty.
- **D-EXT**: observational trace data, not causal explanation.
- **S**: our own authenticated inspection of original source; **none added in this search**.

## A. Official engineering accounts — highest for *why* and current behavior

| ID | Source / date | What it adds | Boundary | Priority |
|---|---|---|---|---|
| O-01 | [Loop engineering: Getting started with loops](https://claude.com/resources/articles/getting-started-with-loops), 2026-06-30 | Team taxonomy of **turn-based / goal-based / time-based / proactive** loops; explicitly distinguishes trigger and stop conditions | Not evidence that the internal query loop uses a specific implementation or that every mode is universally available | **P0** |
| O-02 | [Scaling Managed Agents: Decoupling the brain from the hands](https://www.anthropic.com/research/managed-agents), 2026-04-08 | An alternative **durable event-session + stateless harness + replaceable tool environments**; `wake(sessionId)`, `getSession`, `emitEvent`; reports p50 TTFT reduction ~60%, p95 >90% in its deployment | **Managed Agents platform**, not proof Claude Code CLI shares the same runtime; reported operational gain is not a controlled Loop-syntax benchmark | **P0** |
| O-03 | [How we built Claude Code auto mode](https://www.anthropic.com/research/claude-code-auto-mode), 2026-03-25 | Input prompt-injection screening + pre-action two-stage classifier, denial returned as tool feedback, and **3 consecutive / 20 total denials** as an escalation backstop | Auto mode / settings specific; descriptive first-party design, not an open reproduction dataset | **P0** |
| O-04 | [Harness design for long-running application development](https://www.anthropic.com/research/harness-design-long-running-apps), 2026-03-24 | **Context reset ≠ compaction**; planner / generator / skeptical evaluator; structured handoff and multi-hour tasks; design tradeoffs in complexity, tokens and latency | Task-specific application-building harness, not always the default Claude Code CLI path | **P0** |
| O-05 | [Effective harnesses for long-running agents](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents), 2025-11-26 | Initializer + coding-agent handoff, explicit feature tests/progress artifacts across context windows | Controlled success of entire long-running system, not proof a loop representation is best | P1 |
| O-06 | [Quantifying infrastructure noise in agentic coding evals](https://www.anthropic.com/research/infrastructure-noise), 2026-02-05 | Identical model + harness + tasks differed by **6 percentage points** across runtime resource extremes on Terminal-Bench 2.0 | Infrastructure is a major confounder; must pin and record CPU/memory/caps/timeout | **P0** |
| O-07 | [How Claude Code works](https://code.claude.com/docs/en/how-claude-code-works) | Public model → tool → feedback and interrupt/session semantics | User-level contract ≠ private call graph | P1 |
| O-08 | [How Claude Code is used in practice](https://www.anthropic.com/research/claude-code-expertise), 2026 | Privacy-preserving analysis of ~400k sessions; autonomy/use patterns | Observational; not raw events nor proof of causal architecture choice | P1 |
| O-09 | [Building a C compiler with parallel Claudes](https://www.anthropic.com/research/building-c-compiler), 2026-02-05 | Real long-horizon case study with a separate supervisory loop, external coordination and substantial resource cost | Demonstration of feasibility, not a matched experiment | P2 |

## B. Claude Code internals and source-level *secondary* material

| ID | Source | Distinct contribution | Limitation / duplication risk | Priority |
|---|---|---|---|---|
| S2-01 | [VILA-Lab paper](https://arxiv.org/abs/2604.14228) ([repo](https://github.com/VILA-Lab/Dive-into-Claude-Code), arXiv v3 2026-10-10) | Broad v2.1.88 architecture, source-referenced queryLoop, permissions, context, session, and cross-system design space | **T-SOURCE**, not our S; note version-specific flags and current repo's added later release notes | **P0, base reference** |
| S2-02 | [cablate/claude-code-research](https://github.com/cablate/claude-code-research) | Extensive individual module reports (reported 75), execution/feedback/tool orchestration and prompt-cache issues | Authors may study same leaked snapshot as others; check versions before combining function claims | **P0, cross-check** |
| S2-03 | [Claude Code from Source — 18-chapter book](https://github.com/alejandrobalderas/claude-code-from-source) | **New:** dedicated [Loop](https://github.com/alejandrobalderas/claude-code-from-source/blob/main/book/ch05-agent-loop.md), [tool pipeline](https://github.com/alejandrobalderas/claude-code-from-source/blob/main/book/ch06-tools.md), [concurrent tools](https://github.com/alejandrobalderas/claude-code-from-source/blob/main/book/ch07-concurrency.md), lifecycle/caching tradeoffs; original explanatory pseudocode | No Claude source redistributed; author interpretation, not an independently measured benchmark | **P0, targeted reading** |
| S2-04 | [liuup/claude-code-analysis](https://github.com/liuup/claude-code-analysis) — [Tool Call mechanism](https://github.com/liuup/claude-code-analysis/blob/main/analysis/04b-tool-call-implementation.md) | **New Chinese detailed** streaming-vs-normal executor branches, `isConcurrencySafe`, hooks/permission boundary and results feedback | Repo includes a source tree/zip; do not mirror proprietary contents, and treat interpretation as T-SOURCE | **P0, targeted reading** |
| S2-05 | [《马书》Harness Engineering](https://github.com/ZhangHanDong/harness-engineering-from-cc-to-ai-coding) | **New Chinese** 7-part book, architectural mechanisms → engineering practice, prompt/context/cache/security | Second-hand educational work derived from v2.1.88; check line/version references | P1 |
| S2-06 | [6551Team 46-subsystem index](https://github.com/6551Team/claude-code-design-guide) | Broad module catalog and full data flow | Already in prior audit; valuable index, duplicative of other source-map reviews | P1 |
| S2-07 | [ComeOnOliver/claude-code-analysis](https://github.com/ComeOnOliver/claude-code-analysis) | **New** architecture directory, state/command/tool inventories | Largely broad catalog; assess exact version and accuracy before privileging it | P2 |
| S2-08 | [Claude Code Architecture Guide, Florian Bruniaux](https://cc.bruniaux.com/guide/architecture/) (updated 2026-10-28) | **New** source-tiered reference with explicit unknowns and newer documentation corrections | Documentation synthesis; distinguish official citations from community guesses | P1 |
| S2-09 | [Vikash Rungta essay](https://vrungta.substack.com/p/claude-code-architecture-reverse) (2026-02-17) | Already audited TAOR/primitive tools/model-autonomy design intuitions | Predates v2.1.88 source-map incident; **T-CONCEPT**, not function-level verification | P2 |
| S2-10 | [Multiple `claude-code-unveiled` mirror/forks](https://github.com/shihao-w/claude-code-unveiled) | Hidden flags/system prompt/cost details as possible leads | Identical README text appears under several owners; **not independent corroboration**. Restrict to original attribution and version | P2 |

## C. Controlled experiments — highest for measurable harness *value*

| ID | Paper / public asset | Supported result or useful method | Caveat | Priority |
|---|---|---|---|---|
| E-01 | [Harness or Model?](https://arxiv.org/abs/2609.11987) (2026-09) | **Same-model/paired** Claude Agent SDK vs DeepAgents and Codex SDK vs DeepAgents. 792/800 planned runs graded. Neither main contrast establishes average harness superiority: Opus -1.25pp (48.8% vs 50.0%, CI [-10.0,+7.5]); GPT-5.5 +1.25pp (55.6% vs 54.4%, CI [-4.4,+6.9]). Correctness vs autonomous completion differ. | Private task suite; strong cost uncertainty after cache-telemetry correction; task-type reversal post hoc and needs replication | **P0** |
| E-02 | [Same Model, Different Harness](https://arxiv.org/abs/2608.26218) (2026-08) | Frozen context-shortening/stall-response treatment vs control in same harness. In a constrained 169-task Verified comparison, mean F2PF **28%→49%**, complete tasks **43→72** | **Treatment bundles mechanisms**, not while-vs-step; context pressure and run-era limitations; do not generalize to wide windows | **P0** |
| E-03 | [An Empirical Study of Harness Design for Coding Agents](https://arxiv.org/abs/2609.20804) (2026-09) | 176 matched settings, four models, SWE-bench Verified / Terminal-Bench 2.1; planning/action space/context ablations | Loop held fixed; treatment benefits depend on model, workload, context budget | **P0** |
| E-04 | [When Does Restricting a Coding Agent to execute_code Help?](https://arxiv.org/abs/2607.10569) ([code](https://github.com/hyang0129/onlycodes)) | Three-arm **tool-surface** ablation (default/bash-only/code-only) crossing Claude Code and Codex with two workload regimes; 3/4 cells favor or tie code-only on cost, not universal | Not loop-structure comparison; effect depends on task regime, agent/harness and cache-adjusted cost | **P0 for future tool experiment** |
| E-05 | [DCAS: Decoupling CLI Agent Scaffolding](https://arxiv.org/abs/2608.06113) (2026-08, ASE 2026) | Routes same model across scaffolds without modifying them; reports scaffold-specific planning and transfer failures; planning-aware trajectory collection | Fine-tuning / planning transfer and scaffold effects, not direct proof of runtime reentrancy superiority | P1 |
| E-06 | [Beyond the Model: Demystifying Harness Effects](https://arxiv.org/abs/2609.32459) (2026-09) | Modular harness studies show component effects vary across models/task complexity | Need inspect exact experiments before asserting numerical gain; not a direct Loop syntax test | P1 |
| E-07 | [Harness Engineering: 11 source-code systems](https://arxiv.org/abs/2609.00006) (2026-09) | Source-code design taxonomy and longitudinal observations across multiple coding harnesses | Comparative architecture, not causal measured performance | P1 |
| E-08 | [Rethinking the Evaluation of Harness Evolution](https://arxiv.org/abs/2607.12227) (2026-07) | Warns harness optimization evaluated on the same public task suite risks adaptive overfitting; compare search budgets | Methods caution; not product evidence | P1 |
| E-09 | [Rethinking Harness Evolution via Retrospective Adaptation](https://arxiv.org/abs/2610.34938) (2026-10) | Studies whether harness modifications after prior sessions improve later tasks | Separate learning/adaptation branch, not current Loop representation study | P2 |

## D. Public trace data (what usage can, and cannot, establish)

| ID | Source | Actual contribution | Limit |
|---|---|---|---|
| D-01 | [UW SyFI TraceLab](https://github.com/uw-syfi/TraceLab) / [paper](https://arxiv.org/abs/2606.30560) | Research release around 4,300 Claude Code/Codex sessions, ~350k LLM steps and ~430k tool calls in original paper, plus analysis code | Use a **fixed release**, not moving dashboard counts; observational and subject to selection bias |
| D-02 | [Trace Commons](https://huggingface.co/datasets/trace-commons/agent-traces) | Public native Claude Code session JSONL examples for actual tool/result matching | Anonymization and content license need review; does not identify private function implementation |
| D-03 | [Anthropic use in practice](https://www.anthropic.com/research/claude-code-expertise) | ~400k-session privacy-preserving statistical analysis of operator behavior and autonomy | Aggregated observational study, not replayable execution nor architecture performance causal evidence |

## Duplicate detection and correction rules

1. Many `Dive-into-Claude-Code` repos in search results are forks/renames. Count **VILA-Lab once**.
2. `claude-code-unveiled` README text appears at multiple GitHub owners: **do not count as multiple independent source analyses**.
3. `Claude Code from Source`, `liuup`, `6551Team`, `cablate` may all trace to the **same v2.1.88 accidental source-map publication**. Multiple summaries are useful for spotting disagreements, not a substitute for primary source authentication.
4. `Managed Agents` architecture and Claude Code CLI design are different deployment contexts. Never infer one has exactly the other's engine/stop behavior.
5. "Same model different harness" studies compare a **bundle** of policies, context, tools and orchestration unless the individual intervention is isolated. Do not label a full-harness difference as a `while` effect.
6. Source study ≠ software test ≠ behavior trace ≠ experimental causal evidence.

## Our highest-value unfilled evidence gaps

| Question | Existing best input | Missing contribution |
|---|---|---|
| Does reentrancy matter by itself? | Goose GDK implementation; Managed Agents event-session architecture; prior A0-04 pilots | Measurable handoff/resume latency, state serialization/developer complexity and concurrent event safety under **matched** policy |
| How should a coding Agent decide "done"? | Official goal-based loops and separate evaluator work | Controlled **model says done vs external acceptance** ablation, counting false completion, false rejection and cost |
| Do narrower tool surfaces help? | `execute_code` three-arm experiment and 176-setting harness study | Extension to risk/permissions or workload-specific tool choice without retesting known averages |
| When does context compaction help? | Tight-window F2PF evidence and long-running reset work | Constraint preservation, cost and long-horizon success across **different context regimes** |
| Does architecture change task success? | Private paired studies with neutral vs native harness | Pinned same-model cross-harness task subset with feature matching and detailed confounder reporting; no claim of Loop syntax attribution unless isolated |

## Search method and stopping rule

Search lanes: (1) Claude Code v2.1.88 source-map analysis/book; (2) official Anthropic Engineering/Claude Code product docs; (3) arXiv matched-agent harness studies; (4) trace datasets; (5) cross-system comparisons and tools. Checked source repository READMEs and selected chapter text using GitHub connector, paper abstracts and methods on arXiv and official team posts. Reported counts belong to cited authors; **no external benchmark or real product was run during this literature-search step.**

Stop adding reference links when a candidate only repeats another project's findings without new source access, new control/measurement, or an important counterexample. Promote newly found claims to an evidence ledger **only when they change a planned verification or experimental design**.
