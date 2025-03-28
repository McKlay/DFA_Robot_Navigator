# main.py

import tkinter as tk
from PIL import Image, ImageTk
from dfa import DFA
from dfa_graph import generate_full_dfa_graph

# Setup DFA
states = {'q0', 'q1', 'q2', 'q3', 'q4'}
alphabet = {'R'}
transition_function = {
    ('q0', 'R'): 'q1',
    ('q1', 'R'): 'q2',
    ('q2', 'R'): 'q3',
    ('q3', 'R'): 'q4'
}
start_state = 'q0'
accept_states = {'q4'}

VALID_DIRECTIONS = {'U', 'D', 'L', 'R'}
GRID_ROWS = 5
GRID_COLS = 5

dfa = DFA(GRID_ROWS, GRID_COLS)

# GUI setup
GRID_WIDTH = 5
CELL_SIZE = 80

class RobotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DFA Controlled Robot Navigator")

        self.canvas = tk.Canvas(root, width=GRID_COLS * CELL_SIZE, height=GRID_ROWS * CELL_SIZE)
        self.canvas.pack(pady=10)

        self.input_entry = tk.Entry(root, font=("Arial", 14))
        self.input_entry.pack()

        self.run_button = tk.Button(root, text="Run", command=self.run_dfa)
        self.run_button.pack(pady=5)

        self.status_label = tk.Label(root, text="", font=("Arial", 12))
        self.status_label.pack()

        # dfa graph
        self.graph_button = tk.Button(root, text="Show Transition Graph", command=self.show_full_dfa_graph)
        self.graph_button.pack(pady=5)


        # Selection of start and final state
        self.start_cell = None
        self.accept_cell = None
        self.canvas.bind("<Button-1>", self.set_start_cell)
        self.canvas.bind("<Button-3>", self.set_accept_cell)

         # Load and resize the robot image
        self.robot_img_raw = Image.open("image.jpg")
        self.robot_img_raw = self.robot_img_raw.resize((CELL_SIZE - 20, CELL_SIZE - 20))
        self.robot_img = ImageTk.PhotoImage(self.robot_img_raw)

        self.draw_grid()

        # Add the robot image to the canvas
        self.robot = self.canvas.create_image(10 + (CELL_SIZE - 20) // 2, 10 + (CELL_SIZE - 20) // 2, image=self.robot_img, anchor="center")

    def set_start_cell(self, event):
        # Set start state and redraw
        col = event.x // CELL_SIZE
        row = event.y // CELL_SIZE
        self.start_cell = (row, col)
        dfa.set_start_state(row, col)
        self.draw_grid()

        # Move robot image to start position
        self.canvas.coords(
            self.robot,
            col * CELL_SIZE + CELL_SIZE // 2,
            row * CELL_SIZE + CELL_SIZE // 2
        )

    def set_accept_cell(self, event):
        # Set accept state and redraw
        col = event.x // CELL_SIZE
        row = event.y // CELL_SIZE
        self.accept_cell = (row, col)
        dfa.set_accept_state(row, col)
        self.draw_grid()

    def draw_grid(self):
        self.canvas.delete("all")
        for row in range(GRID_ROWS):
            for col in range(GRID_COLS):
                x1 = col * CELL_SIZE
                y1 = row * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE

                fill_color = "white"
                text_label = ""

                if self.start_cell == (row, col):
                    fill_color = "#b0ffb0"  # light green
                    text_label = "S"
                elif self.accept_cell == (row, col):
                    fill_color = "#ffb0b0"  # light red
                    text_label = "F"

                # Draw the filled cell
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color, outline="black")

                # Draw "S" or "F" in the center
                if text_label:
                    self.canvas.create_text(
                        x1 + CELL_SIZE // 2,
                        y1 + CELL_SIZE // 2,
                        text=text_label,
                        font=("Arial", 16, "bold")
                    )

        # Redraw robot at initial position (top-left as default)
        x, y = 0, 0
        self.robot = self.canvas.create_image(
            x * CELL_SIZE + CELL_SIZE // 2,
            y * CELL_SIZE + CELL_SIZE // 2,
            image=self.robot_img,
            anchor="center"
        )

    def run_dfa(self):
        input_str = self.input_entry.get().upper()

        if not self.start_cell or not self.accept_cell:
            self.status_label.config(text="Please select both start and accept cells.")
            return

        for symbol in input_str:
            if symbol not in VALID_DIRECTIONS:
                self.status_label.config(text=f"Invalid input: {symbol}")
                return

        dfa.reset()
        self.canvas.delete("trail")

        for symbol in input_str:
            current_state = dfa.get_current_state()
            next_state = dfa.transition_function.get((current_state, symbol), current_state)
            dfa.current_state = next_state

            # Extract (row, col) from state name, e.g., q23 → (2, 3)
            row = int(next_state[1])
            col = int(next_state[2])

            # ✅ Draw path marker (breadcrumb trail)
            self.canvas.create_rectangle(
                col * CELL_SIZE + 25,
                row * CELL_SIZE + 25,
                col * CELL_SIZE + CELL_SIZE - 25,
                row * CELL_SIZE + CELL_SIZE - 25,
                fill="#add8e6",  # light blue
                outline="",
                tags="trail"     # ✅ this tag allows us to clear them later
            )

            # Move the robot image
            self.canvas.coords(
                self.robot,
                col * CELL_SIZE + CELL_SIZE // 2,
                row * CELL_SIZE + CELL_SIZE // 2
            )

            self.canvas.update()
            self.root.after(300)

        accepted = dfa.get_current_state() in dfa.accept_states
        result = f"Accepted: {accepted}, Final State: {dfa.get_current_state()}"
        self.status_label.config(text=result)

    def show_full_dfa_graph(self):
        input_str = self.input_entry.get().upper()
        path_transitions, _ = dfa.get_transition_path(input_str)
        generate_full_dfa_graph(dfa, path_transitions)


if __name__ == "__main__":
    root = tk.Tk()
    app = RobotApp(root)
    root.mainloop()
