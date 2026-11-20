"""R1 iteration 2: typed state representation vs transition validation.
Deterministic event replay only; NOT a Claude Code integration.
"""
from dataclasses import dataclass
from itertools import product
import json

EVENTS = ("start", "tool_ok", "cancel", "timeout", "complete", "resume")
TERMINAL = {"cancelled", "completed", "failed"}

@dataclass
class State:
    phase: str = "ready"
    acknowledged: bool = False
    accepted: int = 0
    rejected: int = 0

def raw_transition(phase, acknowledged, event):
    """Identical intentionally permissive policy for both representation baselines."""
    if event in ("start", "resume"):
        return "running", acknowledged
    if event == "tool_ok":
        return phase, True
    if event == "cancel":
        return "cancelled", acknowledged
    if event == "timeout":
        return "failed", acknowledged
    if event == "complete":
        return "completed", acknowledged
    raise ValueError(event)

def allowed(phase, acknowledged, event):
    """Declared execution safety constraints for this model."""
    if phase in TERMINAL:
        return False
    if phase == "ready":
        return event in ("start", "cancel")
    if phase == "running":
        return event in ("tool_ok", "cancel", "timeout") or (event == "complete" and acknowledged)
    return False

def run_local(events):
    phase, acknowledged, accepted = "ready", False, 0
    trace, flags = [], []
    for event in events:
        flags.append(True)
        phase, acknowledged = raw_transition(phase, acknowledged, event)
        accepted += 1
        trace.append(phase)
    return dict(phase=phase, acknowledged=acknowledged, accepted=accepted,
                rejected=0, trace=trace, accepted_flags=flags)

def run_typed(events, validated=False):
    state = State()
    trace, flags = [], []
    for event in events:
        if validated and not allowed(state.phase, state.acknowledged, event):
            state.rejected += 1
            flags.append(False)
            trace.append(state.phase)
            continue
        flags.append(True)
        state.phase, state.acknowledged = raw_transition(state.phase, state.acknowledged, event)
        state.accepted += 1
        trace.append(state.phase)
    return dict(phase=state.phase, acknowledged=state.acknowledged,
                accepted=state.accepted, rejected=state.rejected,
                trace=trace, accepted_flags=flags)

def breaches(events, result):
    """Count accepted events contrary to the same published toy specification."""
    phase, acknowledged, count = "ready", False, 0
    for event, accepted in zip(events, result["accepted_flags"]):
        if not accepted:
            continue
        if not allowed(phase, acknowledged, event):
            count += 1
        phase, acknowledged = raw_transition(phase, acknowledged, event)
    return count

def evaluate():
    traces = [seq for size in (1, 2, 3) for seq in product(EVENTS, repeat=size)]
    rows = []
    for trace in traces:
        local = run_local(trace)
        typed = run_typed(trace)
        checked = run_typed(trace, validated=True)
        assert local == typed, "Representation-only variants diverged"
        rows.append({"events": list(trace), "local_breaches": breaches(trace, local),
                     "typed_breaches": breaches(trace, typed),
                     "checked_breaches": breaches(trace, checked),
                     "checked_rejections": checked["rejected"]})
    return {"scope": "deterministic toy event replay", "traces": len(rows),
            "local_breaching_traces": sum(x["local_breaches"] > 0 for x in rows),
            "typed_breaching_traces": sum(x["typed_breaches"] > 0 for x in rows),
            "checked_breaching_traces": sum(x["checked_breaches"] > 0 for x in rows),
            "checked_rejected_events": sum(x["checked_rejections"] for x in rows),
            "examples": [x for x in rows if x["local_breaches"] > 0][:5]}

if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2))
