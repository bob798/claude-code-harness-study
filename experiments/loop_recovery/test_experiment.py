import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location(
    "loop_recovery_experiment", Path(__file__).with_name("experiment.py")
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class LostReplyTests(unittest.TestCase):
    def test_blind_retry_duplicates_effect(self):
        self.assertEqual(module.simulate(False)["effects"], 2)

    def test_stable_key_deduplicates(self):
        self.assertEqual(module.simulate(True)["effects"], 1)


if __name__ == "__main__":
    unittest.main()
