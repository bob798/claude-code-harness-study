# Model and Source Provenance / 模型与来源说明

## Which model does the experimental code call?

| Component | R1-01 | R1-02 | R1-03 |
|---|---|---|---|
| LLM API in the experiment | **None** | **None** | **None** |
| Decision process | Scripted deterministic events | Scripted event traces | Scripted crash/cancel event sequence |
| Runtime | Python standard library | Python standard library | Python standard library |
| Claude Code instrumented? | No | No | No |
| Tool behavior | Mocked | Mocked | Mocked |
| Measured tokens/API cost | None | None | None |

The assistant used for research discussion and code drafting is **GPT-6**. That does not mean GPT-6 was invoked in the experimental Agent Loop. None of these local tests calls GPT-6, Claude, or any other model.

## What came from Claude Code analysis?

- **Background motivation (T)**: published third-party discussions of Agent Loop, tool invocation, context management and error recovery, including [cablate/claude-code-research](https://github.com/cablate/claude-code-research) and [VILA-Lab/Dive-into-Claude-Code](https://github.com/VILA-Lab/Dive-into-Claude-Code).
- **Public product capabilities (O)**: [Claude Code official documentation](https://code.claude.com/docs/en/overview).
- **Independent engineering hypotheses (H)**: local variables vs typed State; allowed-transition guard; checkpoint vs volatile recovery; external idempotency.
- **Independent experimental implementation (E-MOCK)**: all code under `experiments/`; not transcribed, decompiled, or copied from Claude Code source.

## Evidence boundary

**No claim in R1-01/02/03 that Claude Code implements a specific checkpoint algorithm, persistence order, invariant-checker function, or idempotency protocol has been verified here.** We have not inspected or reproduced an attributable primary source snippet that demonstrates those details. Reports must distinguish analytical inspiration from verified implementation.

## Next evidence tasks

Before describing an implementation as "Claude Code's mechanism": (1) specify exact product version; (2) find publicly attributable official behavior or verifiable third-party module/line reference; (3) record a minimal claim-to-source mapping and alternatives; (4) avoid publishing proprietary source excerpts or maps. Separate behavior observed in the released CLI from hypothesized internals.

For real LLM tests, add an explicit model configuration file with provider, exact model ID/version, temperature, tool schema, prompt, sampling seed if supported, token accounting, price version and run date.
