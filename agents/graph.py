"""
LangGraph pipeline for professor outreach.
Graph: researcher → matcher → drafter → reviewer → (retry or finalize)
"""

from langgraph.graph import StateGraph, END
from agents.state import ProfessorState
from agents.nodes import (
    researcher_node,
    matcher_node,
    drafter_node,
    reviewer_node,
    finalizer_node,
)

MAX_DRAFT_ATTEMPTS = 3


def should_retry_or_finalize(state: ProfessorState) -> str:
    """
    Routing function after reviewer:
    - If passed → finalize
    - If failed and attempts < MAX → retry drafter
    - If failed and max attempts reached → finalize anyway (best effort)
    """
    if state.get("review_passed"):
        return "finalize"
    if state.get("draft_attempts", 0) >= MAX_DRAFT_ATTEMPTS:
        print(f"  ⚠ Max attempts reached for {state['professor']['name']}, using best draft")
        return "finalize"
    return "retry"


def build_graph() -> StateGraph:
    graph = StateGraph(ProfessorState)

    # Add nodes
    graph.add_node("researcher", researcher_node)
    graph.add_node("matcher", matcher_node)
    graph.add_node("drafter", drafter_node)
    graph.add_node("reviewer", reviewer_node)
    graph.add_node("finalizer", finalizer_node)

    # Linear flow
    graph.set_entry_point("researcher")
    graph.add_edge("researcher", "matcher")
    graph.add_edge("matcher", "drafter")
    graph.add_edge("drafter", "reviewer")

    # Conditional: reviewer → finalize or retry
    graph.add_conditional_edges(
        "reviewer",
        should_retry_or_finalize,
        {
            "finalize": "finalizer",
            "retry": "drafter",
        }
    )
    graph.add_edge("finalizer", END)

    return graph.compile()


# Singleton
_graph = None

def get_graph():
    global _graph
    if _graph is None:
        _graph = build_graph()
    return _graph
