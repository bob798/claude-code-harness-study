# A0-03b: Agent Loop Alternatives — Mechanisms, Decisions and Trade-offs

**Research target:** implement a coding agent capable of repeatedly selecting actions from model/tool observations, enforcing permissions, stopping, and optionally pausing/resuming. An architecture is valuable only for a specified deployment setting and measured outcome.

| Pattern | Existing reference | Who owns the loop and mutable state? | Advantages (hypothesized/engineered) | Costs or failure modes | When appropriate |
|---|---|---|---|---|---|
| **A. Model-led `while` / async generator** | Claude Code v2.1.88 **T** via VILA-Lab and cablate | Runtime keeps calling model; model chooses next tool; separate harness enforces permissions and context | Small central loop; unconstrained dynamic tool sequences; streaming fits CLI | Harder reentry/mid-turn suspend if state lives in stack; requires explicit boundaries for durability and tracing | Interactive open-ended coding assistant |
| **B. `while` + explicit state + guards** | Small custom runtimes / our R1 mock | Caller retains loop, typed state and validators | Localized control/diagnostics, easier transition validation without full graph engine | Manual bookkeeping; type changes alone do not change semantics | Small tool workflows with cancellation or approvals |
| **C. Reentrant per-turn state machine** | Goose upstream [discussion #9944](https://github.com/aaif-goose/goose/discussions/9944), [GDK documentation](https://docs.rs/crate/goose-agent/latest) | Runtime receives explicit state, executes one step, yields effects, can reenter on next event | Clear event boundaries; orchestration composition, pause/resume and external control | Migration/parity burden; event-schema evolution; may add latency/complexity | Embedded/SDK/server agents needing reentry and fine-grained control |
| **D. Event-sourced stateless stepper** | [OpenHands SDK agent](https://github.com/OpenHands/docs/blob/main/sdk/arch/agent.mdx) + [conversation](https://github.com/OpenHands/docs/blob/main/sdk/arch/conversation.mdx) | Agent step consumes event history; conversation owns event log/state | Replay, debugging, state persistence, extensible services | Larger data model, serialization/storage and replay/versioning costs; bounded step granularity | Service-oriented agent infrastructure and audit-heavy deployments |
| **E. Explicit directed graph / Pregel** | [LangGraph Pregel](https://github.com/langchain-ai/docs/blob/main/src/oss/langgraph/pregel.mdx) and [interrupts](https://github.com/langchain-ai/docs/blob/main/src/oss/langgraph/interrupts.mdx) | Graph nodes/edges and checkpointer control routing, model selects actions within nodes | Visible dependencies, explicit branching, approvals, checkpointed interrupts | Graph maintenance and state/schema complexity; fixed topologies less natural for unconstrained work | Repeatable workflow with known process stages and human approvals |
| **F. Functional workflow + durable tasks** | [LangGraph Functional API](https://github.com/langchain-ai/docs/blob/main/src/oss/langgraph/functional-api.mdx) | Ordinary code expresses flow while framework persists checkpoints/tasks | Code-first ergonomic flow with replay and explicit tasks | Need to isolate non-determinism and side effects; replay semantics can surprise | Teams wanting durable execution without a large graph drawing |
| **G. Hierarchical / plan-and-execute** | VILA design guide; workflow orchestration literature | Outer plan/controller owns goals, inner agent loop selects actions | Better explicit milestones, dependencies and acceptance gates | Planning overhead, plan drift and rigid assumptions | Multi-phase tasks with verifiable stages |

## Six architectural trade-offs to test separately

1. **Freedom vs constraint:** dynamically chosen tools versus predeclared control path.
2. **Latency vs reentrancy:** long-lived streaming coroutine versus persisted per-turn dispatch.
3. **Trace simplicity vs replay detail:** message list versus event-sourced log.
4. **Safety rule enforcement vs false rejection:** permission/transition guards can block valid operations.
5. **Continuation vs consistency:** resume conversation does not guarantee external effect consistency.
6. **State scope:** local in-memory state vs persisted checkpoints vs durable external operation journal.

### Avoid false dichotomies

- Claude Code need not be state-free because its loop is simple; a `while` can still coordinate sophisticated state/context logic.
- LangGraph can contain a model-led loop inside a graph node; graphs and ReAct are not mutually exclusive.
- OpenHands' `step()` is itself a reasoning-action loop, but its orchestration and state ownership are different.
- A graph/checkpoint cannot guarantee exactly-once external business effects; use independent effect confirmation.
- Model-generated `end_turn` is not an oracle for task correctness.

## What can we conclude about Claude Code's value today?

**Supported as an architectural hypothesis (T/O):** a compact model-led core reduces the *apparent core control-flow surface* and preserves flexible action choice, with execution/security/context duties delegated to the harness.

**Not yet established empirically:** lower cost, higher task success, fewer illegal actions or better recovery *because of the while-loop architecture*. No causal effect size or cost saving should be claimed from the source reading or previous toy tests.

A fair contrast requires matched capabilities, identical model/task/tool sets, controlled budget, independent scoring, real faults, and costs measured in more than tokens.
