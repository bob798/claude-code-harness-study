import importlib.util
import json
import pathlib
import subprocess
import sys
import tempfile
import time
import unittest

SRC = pathlib.Path(__file__).with_name('experiment.py')
spec = importlib.util.spec_from_file_location('a004_engine', SRC)
engine = importlib.util.module_from_spec(spec)
spec.loader.exec_module(engine)

def run_cli(mode, state):
    return json.loads(subprocess.check_output(
        [sys.executable, str(SRC), '--mode', mode, '--state', str(state)], text=True))

def crash_and_resume(mode, tempdir):
    root = pathlib.Path(tempdir)
    state = root / (mode + '.json')
    ready = root / (mode + '.ready')
    proc = subprocess.Popen([sys.executable, str(SRC), '--mode', mode, '--state', str(state),
                             '--kill-after', '2', '--ready-path', str(ready)],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        for _ in range(200):
            if ready.exists():
                break
            if proc.poll() is not None:
                raise RuntimeError('worker exited prematurely: ' + str(proc.communicate()))
            time.sleep(0.02)
        else:
            raise RuntimeError('checkpoint notification timeout')
        assert json.loads(state.read_text())['turn'] == 2
        proc.kill()  # SIGKILL on POSIX: no graceful cleanup.
        proc.wait(timeout=5)
        assert proc.returncode != 0
        return run_cli(mode, state)
    finally:
        if proc.poll() is None:
            proc.kill()
            proc.wait()
        if proc.stdout: proc.stdout.close()
        if proc.stderr: proc.stderr.close()

class ExperimentTests(unittest.TestCase):
    def test_identical_normal(self):
        with tempfile.TemporaryDirectory() as td:
            x = run_cli('streaming', pathlib.Path(td)/'stream.json')
            y = run_cli('reentrant', pathlib.Path(td)/'reentrant.json')
            self.assertEqual(x, y)
            self.assertTrue(x['correct'])

    def test_actual_process_kill_and_resume(self):
        if sys.platform == 'win32': self.skipTest('POSIX kill semantics')
        with tempfile.TemporaryDirectory() as td:
            x = crash_and_resume('streaming', td)
            y = crash_and_resume('reentrant', td)
            self.assertEqual(x, y)
            self.assertTrue(x['correct'])
            self.assertEqual(x['model_calls'], 5)
            self.assertEqual(x['tool_effect_count'], 4)

    def test_guarded_budget(self):
        state = {'phase':'running','turn':8,'history':[],'tool_effects':[],'model_calls':8}
        self.assertEqual(engine.apply_turn(state)['phase'],'budget_exceeded')

    def test_resume_is_idempotent_after_complete(self):
        with tempfile.TemporaryDirectory() as td:
            path = pathlib.Path(td)/'state.json'
            first = run_cli('streaming', path)
            second = run_cli('streaming', path)
            self.assertEqual(first, second)

if __name__ == '__main__': unittest.main()
