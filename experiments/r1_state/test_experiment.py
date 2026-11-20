import importlib.util
from pathlib import Path
import sys
import unittest

spec = importlib.util.spec_from_file_location("r1_module", Path(__file__).with_name("experiment.py"))
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)

class R1PilotTests(unittest.TestCase):
    def test_paired_results(self):
        for name, (faults, cancelled) in module.SCENARIOS.items():
            with self.subTest(name=name):
                a = module.run_while(faults, cancelled)
                b = module.run_state(faults, cancelled)
                self.assertEqual(a, b)
                self.assertEqual(module.violations(a, cancelled), [])
                self.assertEqual(module.violations(b, cancelled), [])

    def test_cancelled_does_not_call_tool(self):
        self.assertEqual(module.run_while([], True)["calls"], 0)
        self.assertEqual(module.run_state([], True)["calls"], 0)

    def test_unconfirmed_is_not_complete(self):
        for runner in (module.run_while, module.run_state):
            result = runner(["lost_reply"] * 3)
            self.assertEqual(result["phase"], "failed_unconfirmed")
            self.assertEqual(result["effects"], 1)

    def test_metric_detects_bad_result(self):
        bad = {"effects": 2, "attempts": 4, "calls": 4, "phase": "completed", "confirmed": False}
        self.assertEqual(len(module.violations(bad, cancelled=True)), 4)

if __name__ == "__main__":
    unittest.main()
