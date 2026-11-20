import importlib.util
import json
import pathlib
import sys
import unittest

source = pathlib.Path(__file__).with_name("trace_summary.py")
spec = importlib.util.spec_from_file_location("a002_trace_summary", source)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)

class TraceSummaryTests(unittest.TestCase):
    def test_tool_request_result_and_run_end(self):
        events = [
            {"type": "system", "subtype": "init", "session_id": "sensitive-id"},
            {"type": "assistant", "message": {"content": [
                {"type": "tool_use", "name": "Read", "id": "secret-tool-id", "input": {"file_path": "/private.txt"}}
            ]}},
            {"type": "user", "message": {"content": [
                {"type": "tool_result", "tool_use_id": "secret-tool-id", "content": "PRIVATE", "is_error": False}
            ]}},
            {"type": "assistant", "message": {"content": [{"type": "text", "text": "PRIVATE ANSWER"}]}},
            {"type": "result", "subtype": "success", "is_error": False, "result": "PRIVATE RESULT"},
        ]
        out = module.summarize(json.dumps(x) for x in events)
        self.assertEqual(out["counts"]["tool_request"], 1)
        self.assertEqual(out["counts"]["tool_result"], 1)
        self.assertEqual(out["tools"], {"Read": 1})
        self.assertEqual(out["events"][-1]["kind"], "run_end")
        serialized = json.dumps(out)
        for secret in ("PRIVATE", "private.txt", "sensitive-id", "secret-tool-id"):
            self.assertNotIn(secret, serialized)

    def test_partial_stream_event_ignored(self):
        out = module.summarize([json.dumps({"type": "stream_event", "event": {"delta": {"text": "private"}}})])
        self.assertEqual(out["events"], [])

    def test_malformed_lines_counted(self):
        out = module.summarize(["bad-json", "{}", "42"])
        self.assertEqual(out["parse_errors"], 2)

    def test_error_tool_result(self):
        out = module.summarize([json.dumps({"type": "user", "message": {"content": [
            {"type": "tool_result", "is_error": True, "content": "private failure"}]}})])
        self.assertEqual(out["events"], [{"kind": "tool_result", "error": True}])

if __name__ == "__main__":
    unittest.main()
