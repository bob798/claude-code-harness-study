"""A0-04-02: two independent approval-boundary control styles, identical policy.
No real LLM, Claude Code or Goose execution. Python 3.10+.
"""
import argparse
import json
import os
from pathlib import Path
import tempfile

def fresh():
    return {'phase':'ready','decision_calls':0,'tool_id':None,'approval':None,'effects':[],
            'model_final_calls':0,'events':[],'handoffs':0}

def write(path, state):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile('w',dir=path.parent,delete=False,encoding='utf-8') as f:
        json.dump(state,f,sort_keys=True); f.flush();os.fsync(f.fileno());temporary=f.name
    os.replace(temporary,path)

def read(path):
    return json.loads(path.read_text(encoding='utf-8')) if path.exists() else fresh()

def infer_tool(state):
    assert state['phase']=='ready'
    state['decision_calls']+=1
    state['tool_id']='write-fixture-v1'
    state['phase']='awaiting_approval'
    state['events'].append('tool_proposed')

def external_event(state,event):
    if event=='cancel':
        if state['phase'] in ('ready','awaiting_approval'):
            state['phase']='cancelled';state['events'].append('cancelled');return True
        return False
    if event in ('approve','deny'):
        if state['phase']!='awaiting_approval' or state['approval'] is not None:
            state['events'].append('ignored_'+event);return False
        state['approval']=event;state['events'].append(event);return True
    raise ValueError(event)

def finish_tool(state):
    assert state['phase']=='awaiting_approval'
    if state['approval']=='approve':
        if state['tool_id'] not in state['effects']:
            state['effects'].append(state['tool_id'])
        state['phase']='tool_complete';state['events'].append('effect_applied')
    elif state['approval']=='deny':
        state['phase']='tool_denied';state['events'].append('tool_denied')
    else:return False
    return True

def finalize(state):
    assert state['phase'] in ('tool_complete','tool_denied')
    state['model_final_calls']+=1;state['events'].append('final_'+state['phase']);state['phase']='complete'

def stream_controller(state):
    """Long-lived generator shape; caller discards stack on yield and reconstructs from saved state."""
    if state['phase']=='ready': infer_tool(state)
    if state['phase']=='awaiting_approval':
        if state['approval'] is None: yield 'needs_approval'
        if state['approval'] is not None: finish_tool(state)
    if state['phase'] in ('tool_complete','tool_denied'): finalize(state)
    yield 'halted' if state['phase']=='cancelled' else 'completed'

def reentrant_step(state):
    """One explicit step per host call."""
    if state['phase']=='ready':infer_tool(state)
    if state['phase']=='awaiting_approval':
        if state['approval'] is None:return 'needs_approval'
        finish_tool(state)
    if state['phase'] in ('tool_complete','tool_denied'):finalize(state)
    return 'halted' if state['phase']=='cancelled' else 'completed'

def invoke(mode,path):
    state=read(path)
    if mode=='streaming':status=next(stream_controller(state))
    elif mode=='reentrant':status=reentrant_step(state)
    else:raise ValueError(mode)
    if status=='needs_approval':state['handoffs']+=1
    write(path,state)
    return {'status':status,'state':state}

def signal(path,event):
    state=read(path);accepted=external_event(state,event);write(path,state)
    return {'accepted':accepted,'phase':state['phase']}

def main():
    p=argparse.ArgumentParser()
    p.add_argument('action',choices=['invoke','signal','inspect'])
    p.add_argument('--mode',choices=['streaming','reentrant'],default='streaming')
    p.add_argument('--state',type=Path,required=True)
    p.add_argument('--event',choices=['approve','deny','cancel'])
    a=p.parse_args()
    r=invoke(a.mode,a.state) if a.action=='invoke' else signal(a.state,a.event) if a.action=='signal' else read(a.state)
    print(json.dumps(r,sort_keys=True))

if __name__=='__main__':main()
