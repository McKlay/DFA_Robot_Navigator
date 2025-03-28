# dfa.py

class DFA:
    def __init__(self, grid_rows, grid_cols):
        self.grid_rows = grid_rows
        self.grid_cols = grid_cols
        self.states = set()
        self.alphabet = {'U', 'D', 'L', 'R'}
        self.transition_function = {}
        self.start_state = None
        self.accept_states = set()
        self.current_state = None
        self._generate_transitions()

    def _generate_transitions(self):
        for row in range(self.grid_rows):
            for col in range(self.grid_cols):
                state = f"q{row}{col}"
                self.states.add(state)
                for direction in self.alphabet:
                    next_row, next_col = row, col
                    if direction == 'U' and row > 0:
                        next_row -= 1
                    elif direction == 'D' and row < self.grid_rows - 1:
                        next_row += 1
                    elif direction == 'L' and col > 0:
                        next_col -= 1
                    elif direction == 'R' and col < self.grid_cols - 1:
                        next_col += 1
                    # Else, hitting a wall — stay in current state
                    next_state = f"q{next_row}{next_col}"
                    self.transition_function[(state, direction)] = next_state

    def reset(self):
        self.current_state = self.start_state

    def process_input(self, input_string):
        self.reset()
        for symbol in input_string:
            if symbol not in self.alphabet:
                print(f"Invalid symbol: {symbol}")
                return False
            self.current_state = self.transition_function.get((self.current_state, symbol), self.current_state)
        return self.current_state in self.accept_states

    def get_current_state(self):
        return self.current_state

    def set_start_state(self, row, col):
        self.start_state = f"q{row}{col}"
        self.reset()

    def set_accept_state(self, row, col):
        self.accept_states = {f"q{row}{col}"}

    def get_transition_path(self, input_string):
        self.reset()
        path = []
        for symbol in input_string:
            current = self.current_state
            next_state = self.transition_function.get((current, symbol), current)
            path.append((current, symbol, next_state))
            self.current_state = next_state
        return path, self.current_state in self.accept_states

