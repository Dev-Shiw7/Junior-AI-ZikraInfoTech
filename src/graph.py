from langgraph.graph import StateGraph, END
from langchain_core.runnables import Runnable

from state import AgentState
from nodes.input_node import receive_input
from nodes.classify import classify
from nodes.retrieve import retrieve
from nodes.draft import draft
from nodes.review import review
from nodes.retry import retry_with_feedback
from nodes.escalate import escalate

def support_agent():
    builder = StateGraph(AgentState)

    # Add nodes
    builder.add_node("input", receive_input)
    builder.add_node("classify", classify)
    builder.add_node("retrieve", retrieve)
    builder.add_node("draft", draft)
    builder.add_node("review", review)
    builder.add_node("retry", retry_with_feedback)
    builder.add_node("escalate", escalate)

    # Entry point
    builder.set_entry_point("input")

    # Edges
    builder.add_edge("input", "classify")
    builder.add_edge("classify", "retrieve")
    builder.add_edge("retrieve", "draft")
    builder.add_edge("draft", "review")

    def route_review(state: AgentState):
        if getattr(state, "approved", False):
            return END
        elif state.get("attempts", 0) < 2:
            return "retry"
        else:
            return "escalate"

    builder.add_conditional_edges("review", route_review)

    # *** THIS IS THE CORRECTED LINE FOR THE RETRY LOOP ***
    # The 'retry' node prepares the state (increments attempts etc.)
    # and then sends it back to 'draft' to generate a NEW response based on feedback.
    builder.add_edge("retry", "draft") # Changed from "retry" to "review"

    builder.add_edge("escalate", END)

    return builder.compile()

# If you were previously compiling it directly like 'support_agent = graph.compile()'
# after the function definition, ensure you are now calling the function:
# support_agent = support_agent() # Uncomment this line if your langgraph.json points to 'your_module:support_agent()'