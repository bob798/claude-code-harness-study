"""R1-03: deterministic process crash and cancellation replay.

Four arms vary state representation (dict/dataclass) and whether a snapshot
survives process restart. The same transition policy and mock service apply.
No model/API/Claude Code source is used.
"""
import json
from dataclasses import dataclass, asdict

@dataclass
class TypedState:
    phase: str = 'ready'
    attempts: int = 0

class Service:
    def __init__(self):
        self.calls = 0
        self.effects = 0
        self.seen = set()

    def invoke(self, key):
        self.calls += 1
        if key not in self.seen:
            self.seen.add(key)
            self.effects += 1

def run(events, typed=False, checkpoint=False):
    """Events: dispatch, commit, ack, cancel, crash, restart, late_ack.

    Commit is an independent external event and can occur after cancellation.
    Only dispatch represents *starting* a new tool operation.
    """
    state = TypedState() if typed else {'phase':'ready','attempts':0}
    disk = None
    service = Service()
    history = []
    call_after_cancel = 0
    cancellation_requested = False

    def view():
        return asdict(state) if typed else dict(state)

    def load(data):
        nonlocal state
        state = TypedState(**data) if typed else dict(data)

    for event in events:
        phase = None if state is None else view()['phase']
        if event == 'dispatch':
            if phase in ('ready','awaiting_reply'):
                if cancellation_requested:
                    call_after_cancel += 1
                service.calls += 1
                if typed:
                    state.phase, state.attempts = 'awaiting_reply', state.attempts + 1
                else:
                    state['phase'],state['attempts']='awaiting_reply',state['attempts']+1
        elif event == 'commit':
            # External side effect can occur even if our process has crashed.
            if 'operation-1' not in service.seen:
                service.seen.add('operation-1')
                service.effects += 1
        elif event in ('ack','late_ack'):
            if phase == 'awaiting_reply':
                if typed: state.phase='completed'
                else: state['phase']='completed'
        elif event == 'cancel':
            cancellation_requested=True
            if typed: state.phase='cancelled'
            else: state['phase']='cancelled'
        elif event == 'crash':
            state=None  # process memory lost
        elif event == 'restart':
            if checkpoint and disk is not None: load(disk)
            else: load({'phase':'ready','attempts':0})
        else:
            raise ValueError(event)
        if event not in ('crash','restart') and state is not None and checkpoint:
            disk=view()
        history.append({'event':event,'phase':None if state is None else view()['phase'],
                        'calls':service.calls,'effects':service.effects})
    return {'phase':None if state is None else view()['phase'],
            'calls':service.calls,'effects':service.effects,
            'post_cancel_dispatches':call_after_cancel,
            'history':history}

SCENARIOS = {
 'normal': ['dispatch','commit','ack'],
 'crash_before_commit': ['dispatch','crash','restart','dispatch','commit','ack'],
 'crash_after_commit_before_ack': ['dispatch','commit','crash','restart','dispatch','ack'],
 'cancel_then_crash': ['dispatch','cancel','crash','restart','dispatch','commit','ack'],
 'late_reply_after_cancel': ['dispatch','cancel','commit','late_ack'],
}

def evaluate():
    rows=[]
    for name,events in SCENARIOS.items():
        vals={}
        for typed in (False, True):
            for checkpoint in (False, True):
                label=('typed' if typed else 'local') + ('_checkpoint' if checkpoint else '_volatile')
                v=run(events,typed,checkpoint)
                vals[label]={k:v[k] for k in ('phase','calls','effects','post_cancel_dispatches')}
        assert vals['local_volatile']==vals['typed_volatile']
        assert vals['local_checkpoint']==vals['typed_checkpoint']
        rows.append({'scenario':name,'arms':vals})
    return {'kind':'synthetic deterministic crash/cancel event replay','model':'none',
            'events':SCENARIOS,'rows':rows}

if __name__=='__main__':
    print(json.dumps(evaluate(),indent=2))
