# File: src/main.py
from langgraph.graph import StateGraph, END
from state import AgentState
from nodes.input_node import receive_input
from nodes.classify import classify
from nodes.retrieve import retrieve
from nodes.draft import draft
from nodes.review import review
from nodes.retry import retry_with_feedback
from nodes.escalate import escalate

def create_support_agent():
    """Create and return the compiled support agent graph"""
    graph = StateGraph(AgentState)

    # Add nodes
    graph.add_node("input", receive_input)
    graph.add_node("classify", classify)
    graph.add_node("retrieve", retrieve)
    graph.add_node("draft", draft)
    graph.add_node("review", review)
    graph.add_node("retry", retry_with_feedback)
    graph.add_node("escalate", escalate)

    # Set entry point
    graph.set_entry_point("input")

    # Add sequential edges
    graph.add_edge("input", "classify")
    graph.add_edge("classify", "retrieve")
    graph.add_edge("retrieve", "draft")
    graph.add_edge("draft", "review")

    # Conditional routing from review
    def route_review(state: AgentState) -> str:
        """Route based on review result and attempt count"""
        print(f"🔍 Routing review: review_result={state.get('review_result')}, attempts={state.get('attempts', 0)}")
        # Check if review was approved
        if state.get("review_result") == "APPROVED":
            return "end"

        # If rejected, check current attempts
        current_attempts = state.get("attempts", 0)
        # 'attempts' is incremented by the 'review' node itself on rejection.
        # So, if current_attempts is 2, it means it has been rejected twice already.
        if current_attempts >= 2:
            return "escalate"

        # Otherwise, retry (meaning current_attempts is 0 or 1)
        return "retry"

    # Add conditional edges with proper mapping
    graph.add_conditional_edges(
        "review",
        route_review,
        {
            "end": END,
            "retry": "retry",
            "escalate": "escalate"
        }
    )

    # Corrected Retry path: Retry goes back to draft to generate a new response
    graph.add_edge("retry", "draft")

    # Escalation path
    graph.add_edge("escalate", END)

    return graph.compile()

# Create the compiled graph instance
support_agent = create_support_agent()