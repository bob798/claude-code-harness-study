# Source Audit — Vikash Rungta's "Claude Code Architecture (Reverse Engineered)"

**Review date:** 2026-11-21  
**Article:** https://vrungta.substack.com/p/claude-code-architecture-reverse  
**Original publication shown:** 2026-02-17  
**Expanded companion:** https://github.com/vkr11/ChainOfThought/blob/main/claude_code_architecture.md  
**GitHub Markdown blob independently fetched:** `a63942463992f41a535c50e3f561deea0b245a78`  
**Classification:** **T-CONCEPT** — third-party behavioral/product interpretation; **not independently source-verified (S)**, and not an experimental benchmark.

## 1. Methodology, chronology and provenance

The author explicitly says this is a synthesis of runtime transcripts, `~/.claude` filesystem artifacts, behavior stress-testing, Anthropic public docs/presentations and author experience; the author warns internal implementation may differ. The article **predates the March 31, 2026 v2.1.88 source-map incident** by roughly six weeks. It does **not claim** to have inspected that leak. The expanded Markdown top note says it is based on official documentation and web research.

**Inference boundary:** This is a useful interpretive essay about visible architecture patterns. It cannot independently establish specific private function names, exact branch order, exact thresholds, or causal performance advantages. The article does not provide reproducible raw experimental traces, pinned Claude Code binary version, task set, tests, or controlled benchmark metrics sufficient for such claims.

## 2. Reusable engineering insights

| Topic | Author's central idea (paraphrased) | What we reuse | Status |
|---|---|---|---|
| TAOR loop | Think → Act → Observe → Repeat | A useful pedagogical outline for model/tool feedback; compare against [official behavior overview](https://code.claude.com/docs/en/how-claude-code-works) | T conceptual + O behavior |
| Decision vs control | Model chooses actions; harness enforces execution boundaries | **Research design axis:** distinguish model autonomy from host scheduling, permissions, approval and context | Research hypothesis |
| Primitive capability tools | Shell/files/search compose broad workflows | Candidate tool-surface ablation: primitive set vs specialized typed integration | Effectiveness unproven here |
| Context economy | Compaction, subagents and selective memory bound context cost | Candidate long-horizon controlled experiment, measure retention and verified progress | T conceptual + O features |
| Extensions & deterministic hooks | Declarative skills/hooks/MCP isolate policy from model behavior | Separate instruction-following from runtime enforcement; preserve in both arms | T + O |
| Failure-mode scorecard | Runaway loops, lost context, authority mistakes, missing observability | Convert into **measurable** safety/liveness/trace metrics | Author's taxonomy, not validation |

## 3. Claims that must NOT be promoted to established implementation facts

| Text claim or diagram | Why we should qualify or correct it | Stronger source |
|---|---|---|
| "The runtime is dumb; the model is the CEO"; "model decides when to stop, NOT orchestrator" | Model typically selects next requested action, but the runtime still enforces tool permissions, budget, timeout, interruption, API errors and stop conditions. A model-generated final reply is not necessarily acceptance-test success. | [Official How Claude Code works](https://code.claude.com/docs/en/how-claude-code-works); Claude API stop semantics |
| "~50 lines" TAOR loop / "infinitely flexible" | Illustrative shorthand. No authenticated versioned source excerpt, LOC methodology or complexity measure; ignores surrounding runtime and control branches. | [VILA-Lab v2.1.88 secondary architecture](https://github.com/VILA-Lab/Dive-into-Claude-Code/blob/main/docs/architecture.md) |
| Fixed 200K window, compaction "at ~50%" | Context size and automatic compaction thresholds depend on model and configuration; neither fixed 200K nor fixed 50% is a general current rule. | [Official context window](https://code.claude.com/docs/en/context-window) |
| `Esc` shown as automatic rollback to checkpoint | **Misleading.** Interrupting a running operation and choosing `/rewind` are different; double Esc can open the rewind menu under specified conditions. File restoration is limited, notably for some shell/subagent/external edits. | [Official checkpointing](https://code.claude.com/docs/en/checkpointing) |
| `bypassPermissions` "AUTO-RUN (everything)" | Oversimplified: official Agent SDK permission documentation states deny rules, ask rules and hooks can still prevent tool execution; behavior is mode/version-specific. | [Official SDK permissions](https://code.claude.com/docs/en/agent-sdk/permissions) |
| "What user sees, model also sees" / "perfect alignment" | Not universally true: context may contain content absent from terminal output, and UI elements need not be model input. | [Official context-window walkthrough](https://code.claude.com/docs/en/context-window) |
| Primitive tools consistently outperform bespoke integrations | No matched task/model/tool benchmark or evidence of attributable superiority is supplied in this article. | Requires independent ablation |
| "Six layers of memory all load at startup" | Treat as an author's conceptual taxonomy; instructions, contextual project files, memory retrieval and active conversation have different loading conditions. | [Official context-window walkthrough](https://code.claude.com/docs/en/context-window) |

These caveats are **not** evidence the whole article is wrong; they define where its explanatory framing exceeds a verifiable claim.

## 4. Key methodological clarification: two independent architectural axes

The article often contrasts a **model-led loop** with a **coded workflow**; our A0-04 research contrasts a **long-lived streaming generator** with a **host-reentrant step**. These are **different dimensions**:

| | Long-lived loop | Reentrant step |
|---|---|---|
| **Model-led next action** | Claude Code *style* (v2.1.88 claim T, not direct implementation reproduction) | Goose *style*; model can still decide the next action |
| **Host-defined next action/workflow** | Scripted sequential workflow with a persistent worker | Durable graph/FSM stepper, with fixed workflow gates |

**Takeaway:** Reentrancy does **not** remove model autonomy; a simple `while` does **not** guarantee autonomy; a graph node can also contain a model-led agent. Compare scheduling/reentry separately from control-policy/model-agency effects.

This clarifies why A0-04 pilot and A0-04-02/03 often find parity when both arms share the same scripted decisioner, approval rules and persistence. In fact parity on shared policy outcomes is a **positive control** for parity of semantic behavior, not evidence that one product architecture is superior.

## 5. Specific contribution to our research backlog

- **Immediate:** Retain article as conceptual motivation and potential failure-mode scorecard. No new empirical conclusion or S-level claim.
- **Current A0-04:** Continue to test **host suspension/reentry, stale approval, concurrent effects, control-transfer overhead** while holding model autonomy and permission policy constant.
- **Future A1:** Separate experiment on **primitive capability tools vs specialized typed domain tools**, controlling tool schemas, budget, task coverage and environment; compare verified task success, unsafe actions and context overhead.
- **Future context study:** Test context compaction quality with facts/constraints retention and verified task outcome, not a fictional fixed compaction threshold.

## 6. Decision

**Add to secondary reading / conceptual interpretations, not the primary source-level call graph.** For v2.1.88 function-level analysis, retain VILA-Lab/cablate as explicit T-source studies and pursue authenticated original evidence when lawfully available. **Do not use this article alone to claim that Claude Code's loop is ~50 LOC, that permissions are unconditional, or that Claude Code outperforms alternative agents.**

Cross-reference [A0-03 source audit](REPORT.md), [community reuse](COMMUNITY_REUSE.md), [A0-04-03 benchmark report](../A0-04-loop-comparison/A0-04-03-REPORT.md).
