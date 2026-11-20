"""Deterministic simulation of lost tool responses and retry side effects.

No API keys, network access, or proprietary source are required.
"""
from __future__ import annotations
import json


class MockService:
    def __init__(self):
        self.effects = 0
        self.seen = {}

    def charge(self, operation_id=None):
        if operation_id is not None and operation_id in self.seen:
            return self.seen[operation_id]
        self.effects += 1
        result = {"receipt": self.effects}
        if operation_id is not None:
            self.seen[operation_id] = result
        return result


def simulate(idempotent: bool):
    service = MockService()
    key = "task-001" if idempotent else None
    # Attempt 1 commits but its reply is intentionally dropped.
    service.charge(key)
    # Attempt 2: caller cannot tell whether attempt 1 committed.
    reply = service.charge(key)
    return {
        "strategy": "stable-idempotency-key" if idempotent else "blind-retry",
        "attempts": 2,
        "effects": service.effects,
        "last_reply": reply,
    }


def main():
    results = [simulate(False), simulate(True)]
    print(json.dumps(results, indent=2))
    return results


if __name__ == "__main__":
    main()
