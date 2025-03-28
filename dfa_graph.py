from graphviz import Digraph

def generate_full_dfa_graph(dfa, path_transitions=None):
    dot = Digraph(comment="DFA Grid Transition Graph")

    # Default to empty list if no path provided
    path_transitions = path_transitions or []

    # Add nodes
    for state in dfa.states:
        dot.node(state, shape="circle")

    # Add edges with highlight for path transitions
    for ((from_state, symbol), to_state) in dfa.transition_function.items():
        # Check if this transition is in the path
        match_index = None
        for i, step in enumerate(path_transitions):
            if step == (from_state, symbol, to_state):
                match_index = i + 1  # Step count starts at 1
                break

        if match_index:
            label = f"{symbol} ({match_index})"
            dot.edge(from_state, to_state, label=label, color="blue", penwidth="2.5")
        else:
            dot.edge(from_state, to_state, label=symbol)

    # Highlight start state
    if dfa.start_state:
        dot.node(dfa.start_state, shape="doublecircle", color="green")

    # Highlight accept states
    for acc in dfa.accept_states:
        dot.node(acc, shape="doublecircle", color="red")

    # Render and open the graph
    dot.render("dfa_graph", format="png", view=True)
