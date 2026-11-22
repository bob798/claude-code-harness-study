# Research Scope Gate / 研究范围准入检查

Version: 1.0 · 2026-11-20. Purpose: prevent scope creep away from **Claude Code execution-path analysis → design alternatives → targeted falsifiable experiment**.

See [RESEARCH_RULES.md](RESEARCH_RULES.md) for the L1–L6 growth standard, mandatory design questions and stop rules. This document implements the study admission gate; it does not replace those rules.

## Three gates (not a decorative score)

### G0: Evidence and ethics — mandatory
- [ ] Exact target: Claude Code released behavior **or** a named third-party analysis of a specified version, clearly distinguished.
- [ ] Evidence log: source URL, version/snapshot, author, precise claim, counterevidence / unknowns.
- [ ] Copyright and security: no proprietary source redistribution, leaked maps, credentials or private traces.

**If G0 fails:** research remains a *question*; do not present as a Claude Code fact.

### G1: Relevance — at least two plus mandatory R1
- [ ] **R1 mandatory:** direct connection to Agent Loop orchestration (model → tool → feedback → next turn/stop).
- [ ] Supports one project axis: productive long-running execution / safe execution / decision correctness.
- [ ] Explains an observable design choice or boundary in Claude Code.
- [ ] Plausible alternative design and explicit engineering trade-off.
- [ ] Existing adjacent work is linked instead of repeatedly rebuilt.

**If G1 fails:** move to BACKLOG, not the Agent Loop mainline.

### G2: Experimental readiness — mandatory before code experiments
- [ ] Falsifiable question and explicit counterexample.
- [ ] Isolate treatment vs control (same model/tools/policy/budget unless treatment).
- [ ] Predetermined metric, independent oracle, baseline and fault matrix.
- [ ] Minimize implementation; no general framework or database subsystem unless essential.
- [ ] Reproduction command, raw observations, limits, stop rule and resource budget.

**If G2 fails:** do **source/evidence research only**; code awaits an acceptable experiment design.

## Per-iteration decision record

| Field | Required content |
|---|---|
| ID and date | Unique research step |
| Central question | A single precise question |
| Evidence and grade | O official / T secondary / H hypothesis / E-MOCK / E-REAL |
| Gate result | pass / partial / fail + specific blockers |
| Initial expectation | Written before analysis |
| Findings and counterevidence | Include negative findings and disagreement |
| Scope decision | mainline / linked sub-study / backlog / closed |
| Direction change | Why changed, what was abandoned |
| Next falsification | Smallest observation that changes our belief |
| Links | Sources, code, report, data |

## Stop conditions

Stop adding experiments if: (1) no Claude-specific evidence path; (2) mechanism no longer tests the Agent Loop; (3) new infrastructure exceeds what a minimal experiment needs; (4) the alternative cannot be fairly compared. Archive useful side discoveries rather than deleting them.

## A0-01 gate assessment

- G0: **partial pass**: official behavior and v2.1.88 third-party analyses gathered; exact internal module claims remain secondary.
- G1: **pass**: reconstruct model-call, tool dispatch, tool-result feedback and stop/cancel boundaries.
- G2: **not applicable**: A0-01 is an evidence mapping phase, not a new code experiment.
- Result: **MAINLINE**; generate control-flow evidence and unresolved-claims list; defer SQLite transaction experiments.

## Source-verified evidence check (when claiming S)

Evidence gate G0 also requires source authentication: original artifact and provenance, pinned version/hash, function-level direct inspection, applicable feature gates and branch conditions, and rights-aware original reporting. Do not upgrade a third-party analysis to S solely because it cites leaked source; see [A0-03](research/A0-03-source-control-flow/SOURCE_CLAIMS.md).
