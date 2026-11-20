# R1 Research Decision Log / 研究决策与方向调整

Research decisions are first-class outputs. Preserve **initial hypothesis → observation → interpretation → change → next falsification**, including negative results. Never rewrite earlier hypotheses after seeing results.

| Date / Iteration | Initial direction | Observation | Decision / change | Next verification |
|---|---|---|---|---|
| 2026-11-20 · R1-01 | Ask if typed State improves recovery correctness | 5/5 matched deterministic scenarios produced equal traces, zero violations on both sides | Do not claim superiority; separate code representation from safety mechanism | Introduce a transition-validator ablation |
| 2026-11-20 · R1-02 | Compare local, typed, typed+validation on deliberately permissive transition model | 249/258 local and typed traces accepted illegal events; validated variant 0/258; 506 rejected attempts | Representation alone does not change behavior; rules enforcement explains toy improvement. **No real-world generalization** | Asynchronous cancellation/restart, false rejection, external-effect oracle; fair matched guards |
| 2026-11-20 · Terminology | Use “状态不变量违反率” throughout Chinese docs | Too opaque for readers; confusion between typed state and safety requirements | Prefer **执行安全约束违规率**, define Invariant once as a rule required to remain true at specified boundaries | Validate wording in next report |

## Required entries in every iteration

1. Original question and *why it seemed plausible*.
2. Evidence grade and experiment setup.
3. Observations, including negative and ambiguous results.
4. Alternative interpretations and confounders.
5. Decisions: keep, change, defer or abandon.
6. What will be tested next and what would disprove it.
7. Links to source, test, raw result, and discussion.

## Caution

Changing the research direction **after** seeing pilot evidence is valid scientific exploration. Treat the changed hypothesis as exploratory until preregistered and tested on new data. Do not silently re-label an exploratory result as confirmatory.
