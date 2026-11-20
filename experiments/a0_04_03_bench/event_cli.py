"""One external boundary event per OS process. No durable-effect guarantee."""
import argparse
import json
import os
from pathlib import Path
import tempfile
from benchmark import boundary_state, boundary_transition, boundary_generator, boundary_step


def process_event(path: Path, event: tuple[str, dict], mode: str):
    state = json.loads(path.read_text(encoding='utf-8')) if path.exists() else boundary_state()
    if mode == 'streaming':
        outcome = next(boundary_generator(state, [event]))
    elif mode == 'reentrant':
        outcome = boundary_step(state, event)
    else: raise ValueError(mode)
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile('w',dir=path.parent,encoding='utf-8',delete=False) as handle:
        json.dump(state,handle,sort_keys=True)
        handle.flush()
        os.fsync(handle.fileno())
        name=handle.name
    os.replace(name,path)
    return outcome


if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--mode', choices=('streaming','reentrant'), required=True)
    p.add_argument('--state', type=Path, required=True)
    p.add_argument('--event', required=True, help='JSON list [event_name, payload]')
    a=p.parse_args()
    evt=json.loads(a.event)
    print(json.dumps({'outcome':process_event(a.state,(evt[0],evt[1]),a.mode)}))
