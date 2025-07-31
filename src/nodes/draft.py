from langchain_core.prompts import ChatPromptTemplate
from state import AgentState
from llm import get_llm

def draft(state: AgentState) -> dict:
    """
    Generate a draft response based on the ticket and retrieved context,
    incorporating reviewer feedback if this is a retry attempt.
    """
    llm = get_llm()

    attempts = state.get("attempts", 0)
    feedback = state.get("reviewer_feedback", "")
    subject = state.get("subject", "")
    description = state.get("description", "")
    category = state.get("category", "")
    context = state.get("context", "")

    print(f"✍️ Generating draft (Attempt #{attempts + 1})...")

    if attempts > 0 and feedback:
        # This is a retry - use enhanced prompt with feedback
        draft_prompt = ChatPromptTemplate.from_messages([
            ("system", f"""You are a customer support agent working on retry attempt #{attempts + 1}.
            
            Your previous response was rejected with this feedback:
            ---
            REVIEWER FEEDBACK: {feedback}
            ---

            Create an improved response that directly addresses this feedback while being:
            - Professional and empathetic
            - Accurate and genuinely helpful
            - Clear and actionable
            - Directly addressing the customer's specific issue
            
            Focus on resolving the issues mentioned in the feedback."""),
            
            ("human", f"""
            Customer Ticket:
            Subject: {subject}
            Description: {description}
            Category: {category}

            Available Context:
            {context}

            Previous Rejection Reason: {feedback}

            Generate an improved response that addresses the feedback:
            """)
        ])
    else:
        # First attempt - standard prompt
        draft_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a professional customer support agent.
            Generate a helpful, empathetic response to the customer's issue.
            
            Your response should:
            - Be professional and courteous
            - Directly address the customer's concern
            - Provide clear, actionable guidance or next steps
            - Resolve the issue when possible
            - Show understanding of their situation"""),
            
            ("human", f"""
            Customer Ticket:
            Subject: {subject}
            Description: {description}
            Category: {category}

            Available Context:
            {context}

            Generate a helpful response:
            """)
        ])

    try:
        messages = draft_prompt.format_messages(
            subject=subject,
            description=description,
            category=category,
            context=context
        )
        
        response = llm.invoke(messages)
        return {
            "draft": response.content.strip()
        }

    except Exception as e:
        print(f"💥 Error generating draft: {e}")
        return {
            "draft": f"I apologize for the technical difficulty in generating a response. Please contact support directly for assistance with your {category or 'general'} inquiry."
        }