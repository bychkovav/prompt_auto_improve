from langgraph.graph import StateGraph, START, END

from graph.graph_logic import create_run_node, get_next_entry_node,generate_and_store_node,evaluate_output_node,improve_prompt_node, should_continue
from schema import State

def get_graph():
    g = StateGraph(State)

    g.add_node("create_run", create_run_node)
    g.add_node("next_entry", get_next_entry_node)
    g.add_node("generate", generate_and_store_node)
    g.add_node("evaluate", evaluate_output_node)
    g.add_node("improve", improve_prompt_node)

    g.add_edge(START, "create_run")
    g.add_edge("create_run", "next_entry")

    g.add_conditional_edges("next_entry", should_continue, {"go": "generate", "stop": END})

    g.add_edge("generate", "evaluate")
    g.add_edge("evaluate", "improve")
    g.add_edge("improve", "next_entry")

    return g.compile()