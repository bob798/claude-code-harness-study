# A0-03b — Exact Control Path Validation Plan

**Purpose:** transition from T (secondary description) to S (directly authenticated source) only when allowed and possible.

## Step 1 — Verify provenance and lawful access

Identify the npm package version `@anthropic-ai/claude-code@2.1.88` and authoritative metadata. Compare source-map claim against publicly reported incident. Do not assume any mirror is authentic; do not check proprietary code into this repository. If you lack an authorized artifact, keep all function-level conclusions as T and continue with behavior-level evidence.

## Step 2 — Examine only relevant control path

In an authorized local review, identify:
- Entry points: `REPL.tsx` `query()` and possible wrappers
- Core function: `query.ts` `queryLoop()`, its loop structure and stop conditions
- API boundary: `queryModel()`
- Tools: `runTools()`, `runToolUse()`, permission and hook ordering
- Result feedback: where `tool_result` messages are created and appended
- Exit paths: end-turn vs max-token vs failure vs cancellation and any distinct resume mechanisms

Record `version / module / symbol / caller / callee / relevant condition / evidence status / confidence`. Publish paraphrase and diagrams, not source dumps.

## Step 3 — Falsification targets

- Claim A: one shared query engine for all public surfaces. **Counterexample:** a distinct active per-surface execution loop.
- Claim B: tool results are supplied to the next model iteration. **Counterexample:** a tool result bypasses model feedback in an active documented branch.
- Claim C: tool safety checks precede tool execution on protected paths. **Counterexample:** an active path calls a protected tool before authorization.
- Claim D: model end-turn by itself establishes task success. **Counterexample:** end-turn with an externally failed task. This concerns semantics, not necessarily a Claude Code claim.

## Stop rule

Do **not** create new Mock modules, SQLite checkpoint layers or fake source-reproduction projects while missing source authenticity. Open issues for unresolved source claims.

## Acceptance criteria

At least one v2.1.88 function-level assertion demonstrably upgraded to S with provenance, or an explicit documented blocker that leaves the assertion at T. No unauthorised redistribution. Then select one narrow architectural trade-off for A1-01.
