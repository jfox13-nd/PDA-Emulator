#!/usr/bin/env python3

import sys
import json

MAX_DEPTH = 1000
DEPTH_REACHED = False

def transition_step_depth(current_state: str, input_string: str, input_index: int, rec_depth: int, stack: list) -> bool:
    '''
    Returns if a transition of the form δ(q, w, s) could accept a string given the current stack and position in the input string
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
                pop_token = stack.pop()
                if pushed_token:
                    stack.append(pushed_token)
                if transition_step_depth(next_state, input_string, input_index+1, rec_depth+1, stack):
                    return True
                if pushed_token:
                    stack.pop()
                stack.append(pop_token)
            elif not required_stack_top:
                if pushed_token:
                    stack.append(pushed_token)
                if transition_step_depth(next_state, input_string, input_index+1, rec_depth+1, stack):
                    return True
                if pushed_token:
                    stack.pop()
        elif not required_input:
            if required_stack_top and stack and required_stack_top == stack[-1]:
                pop_token = stack.pop()
                if pushed_token:
                    stack.append(pushed_token)
                if transition_step_depth(next_state, input_string, input_index, rec_depth+1, stack):
                    return True
                if pushed_token:
                    stack.pop()
                stack.append(pop_token)
            elif not required_stack_top:
                if pushed_token:
                    stack.append(pushed_token)
                if transition_step_depth(next_state, input_string, input_index, rec_depth+1, stack):
                    return True
                if pushed_token:
                    stack.pop()

    return False


def transition_step_breadth(current_state: str, input_string: str, input_index: int, rec_depth: int, stack: list, transition_queue: list) -> bool:
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


def run_pda_breadth(input_string: str, transitions: dict) -> bool:
    '''
    Runs a PDA using a breadth-first search algorithm
    '''
    if not 'START' in transitions:
        return False
    
    transition_queue = [('START', 0, 0, [])]

    while transition_queue:
        next_state, input_index, rec_depth, new_stack = transition_queue.pop(0)
        if transition_step_breadth(next_state,input_string,input_index,rec_depth,new_stack,transition_queue):
            return True
    
    if DEPTH_REACHED:
        print("Max recursion depth reached, terminating PDA")
    return False


def usage() -> None:
    print('''
Usage: {} transitions.json input_string.txt [-h] [-md MAX_RECURSION_DEPTH] [-t depth|breadth]
    '''.format(sys.argv[0]))
    sys.exit(0)


if __name__ == '__main__':
    depth = True
    if len(sys.argv) < 3 or '-h' in sys.argv:
        usage()

    if '-md' in sys.argv:
        MAX_DEPTH = int(sys.argv[sys.argv.index('-md')+1])
    
    depth = '-t' in sys.argv and sys.argv[sys.argv.index('-t')+1] == 'depth'

    with open(sys.argv[1]) as json_file:
        transitions = json.load(json_file)

    with open(sys.argv[2]) as string_file:
        input_string = string_file.read()
    
    if depth:
        if transition_step_depth('START',input_string,0,0,[]):
            print("PASSED")
        else:
            print("FAILED")
    else:
        if run_pda_breadth(input_string,transitions):
            print("PASSED")
        else:
            print("FAILED")