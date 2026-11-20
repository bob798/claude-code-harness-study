import unittest
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from benchmark import (
    upstream_vectors, drive, boundary_vectors, drive_boundary,
    boundary_state, boundary_transition, digest, evaluate, demonstrate_snapshot_race,
)


class ReusedBenchmarkCases(unittest.TestCase):
    def test_upstream_cardinality_and_names(self):
        cases = upstream_vectors(7)
        self.assertEqual(len(cases), 21)
        self.assertEqual([x.id for x in cases[:9]], [
            'normal', 'approval-denied', 'capacity-missing', 'budget-exceeded',
            'transient-read', 'persistent-read', 'uncertain-write',
            'prompt-injection', 'injection-denied'])
        self.assertEqual(len(set(x.id for x in cases)), 21)
        self.assertEqual(cases, upstream_vectors(7))
        self.assertNotEqual(cases, upstream_vectors(8))

    def test_external_scenario_expected_and_effect_oracle(self):
        for mode in ('streaming', 'reentrant'):
            with self.subTest(mode=mode):
                runs = [drive(mode, case) for case in upstream_vectors(7)]
                self.assertTrue(all(r['pass'] for r in runs))
                self.assertEqual({r['case']:r['observed'] for r in runs}['uncertain-write'], 'needs_review')
                self.assertEqual(next(r['effects'] for r in runs if r['case']=='uncertain-write'), 1)
                self.assertEqual(next(r['effects'] for r in runs if r['case']=='approval-denied'), 0)
                self.assertEqual(next(r['effects'] for r in runs if r['case']=='injection-denied'), 0)

    def test_cross_controller_case_parity(self):
        for case in upstream_vectors():
            self.assertEqual(drive('streaming',case), drive('reentrant',case), case.id)

    def test_boundary_extensions_and_safety_oracles(self):
        for case_id, vector in boundary_vectors().items():
            a = drive_boundary('streaming', vector)
            b = drive_boundary('reentrant', vector)
            self.assertEqual(a,b,case_id)
            self.assertTrue(a['pass'],case_id)

    def test_boundary_oracle_detects_wrong_expected(self):
        v = boundary_vectors()['B1_tool_mutation'].copy()
        v['outcomes']=['approved','committed']
        self.assertFalse(drive_boundary('streaming',v)['pass'])

    def test_binding_different_parameters(self):
        s=boundary_state()
        baseline = digest(s['action'])
        changed = dict(s['action']);changed['resource']='warehouse/other'
        self.assertNotEqual(baseline,digest(changed))

    def test_pending_grant_replay_after_restart_is_not_valid(self):
        s=boundary_state()
        self.assertEqual(boundary_transition(s,('approve',{})),'approved')
        self.assertEqual(boundary_transition(s,('restart',{})),'restarted')
        self.assertEqual(boundary_transition(s,('execute',{})),'blocked')
        self.assertEqual(len(s['effect_log']),0)

    def test_ack_loss_is_not_two_effects(self):
        s=boundary_state()
        boundary_transition(s,('approve',{}))
        self.assertEqual(boundary_transition(s,('execute',{'op_id':'K','lose_ack':True})),'ack_lost')
        self.assertEqual(boundary_transition(s,('execute',{'op_id':'K'})),'already_committed')
        self.assertEqual(s['effect_log'],['K'])

    def test_process_separated_restart_and_ack_loss(self):
        """Each event executes in a fresh Python child, not in a vendor runtime."""
        runner=Path(__file__).with_name('event_cli.py')
        sequences=[
            ([('approve',{}),('restart',{}),('approve',{'epoch':1}),('execute',{})],
             ['approved','restarted','rejected','blocked'], 0),
            ([('approve',{}),('execute',{'op_id':'K','lose_ack':True}),('execute',{'op_id':'K'})],
             ['approved','ack_lost','already_committed'], 1),
        ]
        for mode in ('streaming','reentrant'):
            for events,expected,effects in sequences:
                with tempfile.TemporaryDirectory() as d:
                    path=Path(d)/'state.json'
                    seen=[]
                    for name,payload in events:
                        result=subprocess.check_output([sys.executable,str(runner),'--mode',mode,
                            '--state',str(path),'--event',json.dumps([name,payload])],text=True)
                        seen.append(json.loads(result)['outcome'])
                    self.assertEqual(seen,expected)
                    state=json.loads(path.read_text())
                    self.assertEqual(len(state['effect_log']), effects)

    def test_aggregate_has_separate_origins(self):
        summary=evaluate()['summary']
        self.assertEqual(summary['upstream_passes_by_arm'],{'streaming':21,'reentrant':21})
        self.assertEqual(summary['extension_passes_by_arm'],{'streaming':10,'reentrant':10})

    def test_detected_non_linearizable_snapshot_counterexample(self):
        outcome = demonstrate_snapshot_race()
        self.assertTrue(outcome['cancelled_on_host_B'])
        self.assertEqual(outcome['stale_effect_on_host_A'], 'committed')
        self.assertEqual(outcome['unauthorized_effects_relative_to_global_cancel'], 1)
        # This is an expected weakness, not a test success for safety.


if __name__ == '__main__': unittest.main()
