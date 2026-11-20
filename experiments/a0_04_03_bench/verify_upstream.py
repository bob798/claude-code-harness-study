"""Optional explicit source-contract check against pinned third-party AgentBench.

Run with PYTHONPATH set to the checkout of aymaw/agentbench at the pinned
commit recorded in benchmark.UPSTREAM. This script cannot silently fetch code.
"""
import json
from dataclasses import asdict
from agentbench.benchmark import scenarios, safe_agent, evaluate
from benchmark import upstream_vectors, UPSTREAM

ours = [asdict(x) for x in upstream_vectors(7)]
source = [asdict(x) for x in scenarios(7)]
assert ours == source, "Our adapted 21 inputs differ from the upstream snapshot!"
reference = evaluate(safe_agent, "upstream-reference", seed=7)
assert reference["episodes"] == 21
assert reference["success_rate"] == 1.0
assert reference["safety_rate"] == 1.0
print(json.dumps({"source_revision": UPSTREAM["agentbench"]["revision"],
                  "input_vectors_equal": True, "vectors": len(ours),
                  "upstream_own_reference": {"episodes":reference["episodes"],
                                            "success_rate":reference["success_rate"],
                                            "safety_rate":reference["safety_rate"]},
                  "disclaimer":"Upstream reference run is NOT a run of our two controllers"}, indent=2))
