import importlib.util
import json
import pathlib
import unittest

path = pathlib.Path(__file__).with_name("session_analyzer.py")
spec = importlib.util.spec_from_file_location("analyzer",path)
analyzer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(analyzer)

class SessionAnalyzerTests(unittest.TestCase):
    def test_pairs_and_errors(self):
        sample=[
            {"type":"assistant","version":"2.1.145","message":{"model":"claude-sonnet-4-6","content":[{"type":"tool_use","id":"abc","name":"Read","input":{"file_path":"PRIVATE"}}]}},
            {"type":"user","message":{"content":[{"type":"tool_result","tool_use_id":"abc","is_error":True,"content":"PRIVATE"}]}},
            {"type":"assistant","message":{"content":[{"type":"tool_use","id":"def","name":"Bash"}]}}
        ]
        out=analyzer.analyze(json.dumps(x) for x in sample)
        self.assertEqual(out["paired_requests"],1)
        self.assertEqual(out["requests_without_observed_result"],1)
        self.assertEqual(out["error_results"],1)
        self.assertEqual(out["paired_requests_with_later_tool_request"],1)
        self.assertNotIn("PRIVATE",json.dumps(out))
        self.assertNotIn("abc",json.dumps(out))

    def test_duplicate_id(self):
        row={"type":"assistant","message":{"content":[{"type":"tool_use","id":"x","name":"Read"}]}}
        self.assertEqual(analyzer.analyze([json.dumps(row)]*2)["duplicate_request_id_occurrences"],1)

    def test_unpaired_result(self):
        row={"type":"user","message":{"content":[{"type":"tool_result","tool_use_id":"absent"}]}}
        self.assertEqual(analyzer.analyze([json.dumps(row)])["results_without_observed_request"],1)

    def test_nonstandard_or_malformed(self):
        out=analyzer.analyze(["bad","[]","{}"])
        self.assertEqual(out["malformed_entries"],2)

    def test_no_content_leak(self):
        row={"type":"assistant","sessionId":"PRIVATE-ID","message":{"content":[{"type":"text","text":"PRIVATE-PROMPT"}]}}
        self.assertNotIn("PRIVATE",json.dumps(analyzer.analyze([json.dumps(row)])))

if __name__ == "__main__":
    unittest.main()
