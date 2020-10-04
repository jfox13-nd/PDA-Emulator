# PDA-Emulator
A simple non-deterministic PDA emulator

## Usage
```
Usage: pda.py transitions.json input_string.txt [-h] [-md MAX_RECURSION_DEPTH]
```
Write your transitions into a file `transitions.json` in the following format:
```
{
    "START": [["A", "", "", ""]],
    "A": [["START", "", "", ""], ["B", "", "", ""]],
    "B": [["ACC", "", "", ""]]
}
```
Where:
```
    "STATE": [TRANSITION1, TRANSITION1 ...]
```
A `TRANSITION` is defined as follows:
```
[next_state, required_input_token, required_stack_top_token, stack_push_token]
```
If there is no `required_input_token` or `required_stack_top_token` or `stack_push_token` in the transition then this can be expressed with an empty string.
The starting state must be named `START` and a transtition into an acceptiing state must have a next state of `ACC`.

## Sample Inputs
The included `transitions_sample.json` will accept matching parentheses of the form `{(^n)^n}`