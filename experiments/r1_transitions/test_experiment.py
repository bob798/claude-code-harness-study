import importlib.util
from pathlib import Path
import sys
import unittest

spec = importlib.util.spec_from_file_location("r1_transition_experiment", Path(__file__).with_name("experiment.py"))
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)

class R1TransitionTests(unittest.TestCase):
    def test_same_logic_same_results(self):
        for events in [("start", "tool_ok", "complete"), ("start", "cancel", "resume"), ("complete",)]:
            self.assertEqual(module.run_local(events), module.run_typed(events))

    def test_terminal_is_terminal(self):
        result = module.run_typed(("start", "cancel", "tool_ok", "resume"), validated=True)
        self.assertEqual(result["phase"], "cancelled")
        self.assertEqual(result["rejected"], 2)

    def test_completion_requires_confirmation(self):
        self.assertEqual(module.run_typed(("start", "complete"), validated=True)["phase"], "running")
        self.assertEqual(module.run_typed(("start", "tool_ok", "complete"), validated=True)["phase"], "completed")

    def test_exhaustive(self):
        result = module.evaluate()
        self.assertEqual(result["traces"], 258)
        self.assertEqual(result["local_breaching_traces"], result["typed_breaching_traces"])
        self.assertGreater(result["local_breaching_traces"], 0)
        self.assertEqual(result["checked_breaching_traces"], 0)

if __name__ == "__main__":
    unittest.main()
