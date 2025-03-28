# test_dfa.py

from dfa import DFA

# Sample DFA configuration:
states = {'q0', 'q1', 'q2', 'q3', 'q4'}
alphabet = {'R'}  # Only allow 'R' (right)
transition_function = {
    ('q0', 'R'): 'q1',
    ('q1', 'R'): 'q2',
    ('q2', 'R'): 'q3',
    ('q3', 'R'): 'q4'
}
start_state = 'q0'
accept_states = {'q4'}

# Create DFA instance
dfa = DFA(states, alphabet, transition_function, start_state, accept_states)

# Test some inputs
test_strings = ['RRRR', 'RRR', 'RRRRR', 'R', '']

for input_str in test_strings:
    result = dfa.process_input(input_str)
    print(f"Input: {input_str.ljust(5)} ➜ Accepted: {result}, Final State: {dfa.get_current_state()}")
