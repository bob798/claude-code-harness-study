import unittest
from experiment import run,SCENARIOS,evaluate

class R103Tests(unittest.TestCase):
 def test_parity(self):
  for name,events in SCENARIOS.items():
   with self.subTest(name=name):
    for cp in (False,True):
     self.assertEqual(run(events,False,cp),run(events,True,cp))
 def test_cancel_survives_checkpoint_only(self):
  events=SCENARIOS['cancel_then_crash']
  self.assertEqual(run(events,False,False)['post_cancel_dispatches'],1)
  self.assertEqual(run(events,False,True)['post_cancel_dispatches'],0)
 def test_checkpoint_does_not_avoid_ambiguous_retry(self):
  events=SCENARIOS['crash_after_commit_before_ack']
  self.assertEqual(run(events,False,True)['calls'],2)
  self.assertEqual(run(events,False,True)['effects'],1)
 def test_late_reply_does_not_revive_cancelled(self):
  self.assertEqual(run(SCENARIOS['late_reply_after_cancel'],False,True)['phase'],'cancelled')
 def test_expected_scenarios(self):
  self.assertEqual(len(evaluate()['rows']),5)
if __name__=='__main__':unittest.main()
