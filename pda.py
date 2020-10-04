#!/usr/bin/env python3

import sys
import json

MAX_DEPTH = 1000
DEPTH_REACHED = False

def transition_step(current_state: str, input_string: str, input_index: int, rec_depth: int, stack: list, transition_queue: list) -> bool:
    '''
    Completes a transition of the form δ(q, w, s), returns True if the transition accepts and False otherwise.
    This function will also queue other nondeterministic transitions
    '''
    global DEPTH_REACHED

    if current_state == "ACC":
        return True

    if rec_depth >= MAX_DEPTH:
        DEPTH_REACHED = True
        return False

    if input_string and len(input_string) > input_index:
        input_token = input_string[input_index]
    else:
        input_token = None

    for next_state, required_input, required_stack_top, pushed_token in transitions[current_state]:
        if required_input and input_token and input_token == required_input:
            if required_stack_top and stack and required_stack_top == stack[-1]:
                new_stack = stack[:]
                new_stack.pop()
                if pushed_token:
                    new_stack.append(pushed_token)
                transition_queue.append((next_state, input_index+1, rec_depth+1, new_stack))
            elif not required_stack_top:
                new_stack = stack[:]
                if pushed_token:
                    new_stack.append(pushed_token)
                transition_queue.append((next_state, input_index+1, rec_depth+1, new_stack))
        elif not required_input:
            if required_stack_top and stack and required_stack_top == stack[-1]:
                new_stack = stack[:]
                new_stack.pop()
                if pushed_token:
                    new_stack.append(pushed_token)
                transition_queue.append((next_state, input_index, rec_depth+1, new_stack))
            elif not required_stack_top:
                new_stack = stack[:]
                if pushed_token:
                    new_stack.append(pushed_token)
                transition_queue.append((next_state, input_index, rec_depth+1, new_stack))
    
    return False


def run_pda(input_string: str, transitions: dict) -> bool:
    '''
    Runs a PDA using a breadth-first search algorithm
    '''
    if not 'START' in transitions:
        return False
    
    transition_queue = [('START', 0, 0, [])]

    while transition_queue:
        next_state, input_index, rec_depth, new_stack = transition_queue.pop(0)
        if transition_step(next_state,input_string,input_index,rec_depth,new_stack,transition_queue):
            return True
    
    if DEPTH_REACHED:
        print("Max recursion depth reached, terminating PDA")
    return False

def usage() -> None:
    print('''
Usage: {} transitions.json input_string.txt [-h] [-md MAX_RECURSION_DEPTH]
    '''.format(sys.argv[0]))
    sys.exit(0)

if __name__ == '__main__':
    if len(sys.argv) < 3 or '-h' in sys.argv:
        usage()

    with open(sys.argv[1]) as json_file:
        transitions = json.load(json_file)

    with open(sys.argv[2]) as string_file:
        input_string = string_file.read()
    
    if run_pda(input_string,transitions):
        print("PASSED")
    else:
        print("FAILED")