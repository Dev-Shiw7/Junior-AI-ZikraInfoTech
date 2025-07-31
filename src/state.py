from typing import TypedDict, List, Optional

class AgentState(TypedDict):
    subject: str
    description: str
    category: Optional[str]
    context: Optional[str]
    draft: Optional[str]
    review_result: Optional[str]
    reviewer_feedback: Optional[str]
    approved: Optional[bool]
    needs_review: Optional[bool]
    attempts: Optional[int]
    failed_drafts: Optional[List[str]]
