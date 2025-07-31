from state import AgentState

def receive_input(state):
    subject = state.get("subject", "").strip()
    description = state.get("description", "").strip()

    return {
        "subject": subject,
        "description": description,
        "category": None,            # to be set by classifier
        "context": None,             # to be set by RAG
        "draft": None,               # to be set by draft generator
        "review_result": None,       # to be set by reviewer
        "reviewer_feedback": None,   # to be set by reviewer
        "attempts": 0,
        "failed_drafts": [],
        "needs_review": False
    }