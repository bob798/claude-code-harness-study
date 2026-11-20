# A0-01 Outcome → A0-02 Entry Criteria

## A0-01 findings

1. Official docs establish a model/tool feedback loop, user interruption and session continuation.
2. Two secondary architecture analyses describe reported internal functions (v2.1.88), but function-level names differ and need version matching.
3. Session-level continuity does not imply exactly-once tool operation recovery.
4. R1-01/02/03 mock studies remain useful **side experiments**, not direct Claude Code behavior evidence.

## A0-02 proposal (observable trace, no leaked source)

**Question:** In a specified installed Claude Code version and mode, what observable event sequence occurs for simple tool use, a tool failure, an explicit user interrupt and a session resume?

**Preparation:** identify a known installation/runtime and its exact version; choose lawful public documentation or a documented SDK observability API. Use isolated disposable project directory; avoid sensitive repos and credentials in published traces.

**Trace collection:** capture model/tool boundary events exposed by documented interfaces; do not assume internal stream exposes every event. Record commands, version, mode, model ID, task description, timestamps, redacted outputs, observed stop and unknown fields.

**Test cases (before execution):**
- P1 simple read-only tool invocation and feedback.
- P2 tool error surfaced to next model decision.
- P3 human interruption during a long-running operation, observing effect on later tool starts.
- P4 conversation resume with user-provided follow-up; do not infer same process or same external operation restart.

**Falsification:** if observed event sequences contradict a claimed module-path behavior, mark its prediction contradicted or unsupported at that version. Be careful: API event visibility may be incomplete; absence of an event is not proof of absence of an internal operation.

**Decision:** No mock architecture implementation before source-to-behavior claim mapping exists. A0-02 should focus on recording observations first.

## Deferred subproject

`backlog/tool-execution-reliability`: SQLite, execution ledgers, external idempotency, transaction boundaries. Useful general engineering, out of scope for A0 core analysis until a Claude-specific mechanism and fair experiment justify inclusion.
