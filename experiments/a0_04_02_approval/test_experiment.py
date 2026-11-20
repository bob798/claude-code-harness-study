import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT=Path(__file__).with_name('experiment.py')
spec=importlib.util.spec_from_file_location('a00402',SCRIPT)
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)

def cli(action,mode,path,event=None):
    args=[sys.executable,str(SCRIPT),action,'--mode',mode,'--state',str(path)]
    if event:args+=['--event',event]
    return json.loads(subprocess.check_output(args,text=True))

def scenario(mode,steps):
    with tempfile.TemporaryDirectory() as tmp:
        path=Path(tmp)/'state.json';records=[]
        for action,event in steps:records.append(cli(action,mode,path,event))
        return cli('inspect',mode,path),records

class Compare(unittest.TestCase):
    def test_approval_and_restart(self):
        seq=[('invoke',None),('signal','approve'),('invoke',None)]
        a,ra=scenario('streaming',seq);b,_=scenario('reentrant',seq)
        self.assertEqual(a,b);self.assertEqual(a['phase'],'complete')
        self.assertEqual(a['decision_calls'],1)
        self.assertEqual(a['effects'],['write-fixture-v1'])
        self.assertEqual(ra[0]['status'],'needs_approval')
        self.assertEqual(ra[-1]['status'],'completed')
    def test_deny(self):
        seq=[('invoke',None),('signal','deny'),('invoke',None)]
        a,_=scenario('streaming',seq);b,_=scenario('reentrant',seq)
        self.assertEqual(a,b);self.assertEqual(a['effects'],[])
        self.assertEqual(a['phase'],'complete');self.assertEqual(a['model_final_calls'],1)
    def test_cancel_before_approval(self):
        seq=[('invoke',None),('signal','cancel'),('signal','approve'),('invoke',None)]
        a,events=scenario('streaming',seq);b,_=scenario('reentrant',seq)
        self.assertEqual(a,b);self.assertEqual(a['phase'],'cancelled')
        self.assertEqual(a['effects'],[]);self.assertFalse(events[2]['accepted'])
    def test_duplicate_approval(self):
        seq=[('invoke',None),('signal','approve'),('signal','approve'),('invoke',None),('invoke',None)]
        a,events=scenario('streaming',seq);b,_=scenario('reentrant',seq)
        self.assertEqual(a,b);self.assertEqual(len(a['effects']),1)
        self.assertFalse(events[2]['accepted'])
    def test_no_fabricated_model_after_pause(self):
        for mode in ('streaming','reentrant'):
            a,_=scenario(mode,[('invoke',None),('invoke',None)])
            self.assertEqual(a['decision_calls'],1);self.assertEqual(a['handoffs'],2)
            self.assertEqual(a['phase'],'awaiting_approval')
    def test_shared_guard(self):
        state=mod.fresh()
        self.assertFalse(mod.external_event(state,'approve'))
        self.assertEqual(state['phase'],'ready')

if __name__=='__main__':unittest.main()
