"""A0-04: independent streaming loop vs reentrant step.
Real process SIGKILL at persisted turn boundary; no LLM, no Claude/Goose code.
"""
import argparse
import json
import os
from pathlib import Path
import tempfile
import time

TOOL_COUNT = 4
MAX_TURNS = 8

def save_atomic(path, state):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile('w', encoding='utf-8', dir=path.parent, delete=False) as fp:
        json.dump(state, fp, sort_keys=True)
        fp.flush()
        os.fsync(fp.fileno())
        temp_name = fp.name
    os.replace(temp_name, path)

def load(path):
    if path.exists():
        return json.loads(path.read_text(encoding='utf-8'))
    return {"phase": "ready", "turn": 0, "history": [], "tool_effects": [], "model_calls": 0}

def model_decision(state):
    if state['turn'] < TOOL_COUNT:
        return {'kind': 'tool', 'id': 'op-' + str(state['turn'] + 1)}
    return {'kind': 'finish'}

def apply_turn(state):
    """Shared transition, acceptance rules and idempotent mock tool."""
    if state['phase'] == 'complete':
        return state
    if state['turn'] >= MAX_TURNS:
        state['phase'] = 'budget_exceeded'
        return state
    decision = model_decision(state)
    state['model_calls'] += 1
    if decision['kind'] == 'tool':
        tool_id = decision['id']
        if tool_id not in state['tool_effects']:
            state['tool_effects'].append(tool_id)
        state['history'].append({'turn': state['turn'] + 1, 'action': tool_id, 'feedback': 'ok'})
        state['phase'] = 'running'
    else:
        state['history'].append({'turn': state['turn'] + 1, 'action': 'finish', 'feedback': 'complete'})
        state['phase'] = 'complete'
    state['turn'] += 1
    return state

def streaming_loop(state):
    """Long-lived generator-style loop."""
    while state['phase'] != 'complete' and state['turn'] < MAX_TURNS:
        yield apply_turn(state)

def reentrant_step(state):
    """One turn per invocation."""
    return apply_turn(state)

def execute(mode, state_path, kill_after=None, ready_path=None):
    if mode not in ('streaming', 'reentrant'):
        raise ValueError(mode)
    state = load(state_path)
    if mode == 'streaming':
        for current in streaming_loop(state):
            save_atomic(state_path, current)
            if kill_after is not None and current['turn'] == kill_after:
                if ready_path:
                    ready_path.write_text('checkpoint persisted', encoding='utf-8')
                while True:
                    time.sleep(1)
    else:
        while state['phase'] != 'complete' and state['turn'] < MAX_TURNS:
            state = reentrant_step(state)
            save_atomic(state_path, state)
            if kill_after is not None and state['turn'] == kill_after:
                if ready_path:
                    ready_path.write_text('checkpoint persisted', encoding='utf-8')
                while True:
                    time.sleep(1)
    return load(state_path)

def summary(state):
    valid = (state['phase'] == 'complete' and state['turn'] == TOOL_COUNT + 1 and
             state['model_calls'] == TOOL_COUNT + 1 and len(state['tool_effects']) == TOOL_COUNT and
             len(set(state['tool_effects'])) == TOOL_COUNT and
             [x['action'] for x in state['history']] ==
             ['op-1', 'op-2', 'op-3', 'op-4', 'finish'])
    return {'correct': valid, 'phase': state['phase'], 'turns': state['turn'],
            'model_calls': state['model_calls'], 'tool_effect_count': len(state['tool_effects']),
            'history': state['history']}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', required=True, choices=['streaming', 'reentrant'])
    parser.add_argument('--state', type=Path, required=True)
    parser.add_argument('--kill-after', type=int)
    parser.add_argument('--ready-path', type=Path)
    args = parser.parse_args()
    result = execute(args.mode, args.state, args.kill_after, args.ready_path)
    print(json.dumps(summary(result), sort_keys=True))

if __name__ == '__main__':
    main()
