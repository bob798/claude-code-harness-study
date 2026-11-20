"""R1 deterministic pilot: functionally matched local-variables and typed-State loops."""
from dataclasses import dataclass, field
import json

MAX_ATTEMPTS = 3

class MockTool:
    def __init__(self, faults):
        self.faults, self.calls, self.effects, self.seen = faults, 0, 0, set()

    def invoke(self, key):
        self.calls += 1
        fault = self.faults[self.calls - 1] if self.calls <= len(self.faults) else "ok"
        if fault == "precommit_timeout":
            return "timeout"
        if key not in self.seen:
            self.effects += 1
            self.seen.add(key)
        return "lost_reply" if fault == "lost_reply" else "ok"

@dataclass
class AgentState:
    phase: str = "ready"
    attempts: int = 0
    confirmed: bool = False
    trace: list = field(default_factory=list)

def run_while(faults, cancelled=False):
    tool = MockTool(faults)
    phase, attempts, confirmed, trace = "ready", 0, False, []
    if cancelled:
        phase = "cancelled"
        trace.append(phase)
    else:
        phase = "running"
        trace.append(phase)
        while attempts < MAX_ATTEMPTS and not confirmed:
            attempts += 1
            result = tool.invoke("operation-1")
            trace.append(result)
            if result == "ok":
                confirmed = True
        phase = "completed" if confirmed else "failed_unconfirmed"
        trace.append(phase)
    return dict(phase=phase, attempts=attempts, confirmed=confirmed, trace=trace, calls=tool.calls, effects=tool.effects)

def run_state(faults, cancelled=False):
    tool = MockTool(faults)
    state = AgentState()
    if cancelled:
        state.phase = "cancelled"
        state.trace.append(state.phase)
    else:
        state.phase = "running"
        state.trace.append(state.phase)
        while state.attempts < MAX_ATTEMPTS and not state.confirmed:
            state.attempts += 1
            result = tool.invoke("operation-1")
            state.trace.append(result)
            if result == "ok":
                state.confirmed = True
        state.phase = "completed" if state.confirmed else "failed_unconfirmed"
        state.trace.append(state.phase)
    return dict(phase=state.phase, attempts=state.attempts, confirmed=state.confirmed, trace=state.trace, calls=tool.calls, effects=tool.effects)

def violations(result, cancelled=False):
    checks = {
        "duplicate_effect": result["effects"] > 1,
        "exceeded_budget": result["attempts"] > MAX_ATTEMPTS,
        "cancelled_but_called": cancelled and result["calls"] > 0,
        "false_completed": result["phase"] == "completed" and not result["confirmed"],
        "inconsistent_confirmation": result["confirmed"] and result["phase"] != "completed",
    }
    return [name for name, bad in checks.items() if bad]

SCENARIOS = {
    "normal": ([], False),
    "precommit_timeout": (["precommit_timeout"], False),
    "postcommit_reply_loss": (["lost_reply"], False),
    "three_lost_replies": (["lost_reply"] * 3, False),
    "cancel_before_tool": ([], True),
}

def evaluate():
    rows = []
    for name, (faults, cancelled) in SCENARIOS.items():
        a, b = run_while(faults, cancelled), run_state(faults, cancelled)
        rows.append({"scenario": name, "equivalent": a == b,
                     "while_violations": violations(a, cancelled),
                     "state_violations": violations(b, cancelled),
                     "terminal": a["phase"], "effects": a["effects"]})
    return {"kind": "deterministic exploratory pilot", "scenarios": len(rows),
            "equal_traces": sum(row["equivalent"] for row in rows),
            "while_violating_runs": sum(bool(row["while_violations"]) for row in rows),
            "state_violating_runs": sum(bool(row["state_violations"]) for row in rows),
            "rows": rows}

if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2))
