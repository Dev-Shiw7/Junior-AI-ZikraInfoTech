# from nodes.retrieve import retrieve
# from nodes.draft import draft
# from state import AgentState

# def retry_with_feedback(state: AgentState) -> AgentState:
#     # Reset needs_review before retry
#     state_copy = {**state, "needs_review": False}
    
#     # Optional: adapt context to reviewer feedback
#     updated_state = retrieve(state_copy)
#     updated_state = draft(updated_state)
#     return updated_state






from state import AgentState

def retry_with_feedback(state: AgentState) -> dict:
    """
    Handle retry logic by incrementing attempts and adding failed draft
    """
    
    # Increment attempts counter
    current_attempts = state.get("attempts", 0)
    new_attempts = current_attempts + 1
    
    # Add current draft to failed drafts
    failed_drafts = state.get("failed_drafts", [])
    current_draft = state.get("draft", "")
    if current_draft and current_draft not in failed_drafts:
        failed_drafts.append(current_draft)
    
    # Get the reviewer feedback
    feedback = state.get("reviewer_feedback", "")
    
    print(f"🔄 Retry attempt #{new_attempts}: {feedback}")
    
    # Return updated state with incremented attempts and failed drafts
    return {
        "attempts": new_attempts,
        "failed_drafts": failed_drafts
    }