# import re
# from langchain_core.prompts import ChatPromptTemplate
# from state import AgentState
# from llm import get_llm

# def review(state: AgentState) -> dict:
#     """
#     Professional quality assurance review for customer support responses.
#     Only provides review result and feedback - does NOT manage attempts or failed drafts.
#     """
#     llm = get_llm()
    
#     # Get state variables
#     subject = state.get("subject", "")
#     description = state.get("description", "")
#     category = state.get("category", "")
#     draft = state.get("draft", "")
    
#     print("🧐 Starting quality review...")
#     print(f"🧐 Draft to review:\n{draft}\n" + "="*50)
    
#     # === COMPREHENSIVE QUALITY ASSESSMENT ===
    
#     review_prompt = ChatPromptTemplate.from_messages([
#         ("system", """You are a senior customer support quality assurance specialist. 
# Your job is to ensure customer responses meet professional standards for real-world deployment.

# EVALUATION CRITERIA (REJECT ONLY for significant issues):

# 🚨 CRITICAL FAILURES (Always reject):
# - Response is completely irrelevant to the customer's issue
# - Contains harmful, inappropriate, or offensive content
# - Makes unrealistic promises (guaranteed refunds, impossible timelines)
# - Provides clearly incorrect or misleading information
# - Is unprofessional, rude, or dismissive in tone
# - Contains discriminatory language or bias

# ⚠️ MAJOR ISSUES (Usually reject):
# - Fails to address the main customer concern at all
# - Provides no helpful information or next steps
# - Is so unclear that customer won't understand what to do
# - Contains significant factual errors about policies/procedures
# - Escalates unnecessarily when simple solution exists
# - Is extremely verbose without adding value

# ✅ ACCEPTABLE (Don't reject for these):
# - Minor grammar or spelling mistakes
# - Placeholders like [Your Name] or [Customer Name] 
# - Slightly informal tone (as long as it's respectful)
# - Not addressing every minor detail mentioned
# - Standard template language or formatting
# - Brevity (short responses can still be helpful)

# IMPORTANT: 
# - Only reject responses that genuinely fail to help the customer or create problems
# - Placeholders and minor imperfections are normal in draft responses
# - Focus on whether the customer would receive meaningful assistance
# - Be practical - would this response actually solve or progress the customer's issue?

# RESPONSE FORMAT:
# - Reply with "APPROVED" if the response provides reasonable customer assistance
# - Reply with "REJECTED: [specific reason]" only for significant failures
# - Focus on deal-breaker issues, not minor polish items"""),

#         ("human", """Evaluate this customer support response for real-world deployment:

# ORIGINAL TICKET:
# Subject: {subject}
# Description: {description}
# Category: {category}

# RESPONSE TO EVALUATE:
# {draft}

# Your assessment:""")
#     ])
    
#     try:
#         messages = review_prompt.format_messages(
#             subject=subject,
#             description=description,
#             category=category,
#             draft=draft
#         )
        
#         print("🧐 Conducting quality assessment...")
#         response = llm.invoke(messages)
#         review_content = response.content.strip()
        
#         print(f"🧐 REVIEW RESULT: {review_content}")
        
#         # Parse the review result - ONLY return review status and feedback
#         if review_content.startswith("APPROVED"):
#             print("✅ RESPONSE APPROVED")
#             return {
#                 "review_result": "APPROVED",
#                 "reviewer_feedback": None
#             }
        
#         elif review_content.startswith("REJECTED"):
#             feedback = review_content.replace("REJECTED:", "").strip()
#             if not feedback:
#                 feedback = "Response did not meet quality standards"
            
#             print(f"❌ RESPONSE REJECTED: {feedback}")
#             return {
#                 "review_result": "REJECTED",
#                 "reviewer_feedback": feedback
#             }
        
#         else:
#             # Handle unexpected format - default to rejection with explanation
#             feedback = f"Review response unclear: {review_content[:100]}..."
#             print(f"⚠️ UNCLEAR REVIEW, DEFAULTING TO REJECTION: {feedback}")
#             return {
#                 "review_result": "REJECTED",
#                 "reviewer_feedback": feedback
#             }
            
#     except Exception as e:
#         error_msg = f"Technical error during review: {str(e)}"
#         print(f"💥 REVIEW ERROR: {error_msg}")
#         return {
#             "review_result": "REJECTED",
#             "reviewer_feedback": error_msg
#         }
























# now with RAG


from langchain_core.prompts import ChatPromptTemplate
from state import AgentState
from llm import get_llm

def review(state: AgentState) -> dict:
    """
    Review the draft response for quality and accuracy.
    Only provides review result and feedback - does NOT manage attempts or failed drafts.
    """
    llm = get_llm()
    
    subject = state.get("subject", "")
    description = state.get("description", "")
    category = state.get("category", "")
    context = state.get("context", "")
    draft = state.get("draft", "")
    current_attempts = state.get("attempts", 0)
    
    print(f"🔍 Reviewing draft (attempt #{current_attempts + 1})...")
    
    review_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a quality assurance reviewer for customer support responses.
        
        Evaluate the draft response against these criteria:
        1. ACCURACY: Does it correctly address the customer's issue?
        2. COMPLETENESS: Does it fully answer their question?
        3. PROFESSIONALISM: Is the tone appropriate and helpful?
        4. ACTIONABILITY: Does it provide clear next steps?
        5. CONTEXT USAGE: Does it properly use the available knowledge base information?
        
        Respond with EXACTLY this format:
        RESULT: [APPROVED or REJECTED]
        FEEDBACK: [Specific feedback explaining your decision]
        
        Be strict but fair. Only approve responses that meet all criteria."""),
        
        ("human", f"""
        Customer Issue:
        Subject: {subject}
        Description: {description}
        Category: {category}
        
        Available Context:
        {context}
        
        Draft Response to Review:
        {draft}
        
        Please review this response:
        """)
    ])
    
    try:
        messages = review_prompt.format_messages(
            subject=subject,
            description=description,
            category=category,
            context=context,
            draft=draft
        )
        
        response = llm.invoke(messages)
        review_content = response.content.strip()
        
        # Parse the response
        lines = review_content.split('\n')
        result_line = next((line for line in lines if line.startswith('RESULT:')), '')
        feedback_line = next((line for line in lines if line.startswith('FEEDBACK:')), '')
        
        # Extract result and feedback
        result = result_line.replace('RESULT:', '').strip() if result_line else 'REJECTED'
        feedback = feedback_line.replace('FEEDBACK:', '').strip() if feedback_line else 'Review parsing failed'
        
        # Validate result
        if result not in ['APPROVED', 'REJECTED']:
            print(f"⚠️ Invalid review result '{result}', defaulting to REJECTED")
            result = 'REJECTED'
            feedback = f"Invalid review format. Original response: {review_content}"
        
        print(f"📋 Review result: {result}")
        if result == 'REJECTED':
            print(f"💬 Feedback: {feedback}")
        
        # Update state based on review result
        updated_state = {**state}
        
        if result == 'APPROVED':
            updated_state.update({
                "review_result": "APPROVED",
                "reviewer_feedback": feedback,
                "approved": True
            })
        else:
            # Increment attempts on rejection
            new_attempts = current_attempts + 1
            
            # Add current draft to failed drafts
            failed_drafts = state.get("failed_drafts", [])
            if draft and draft not in failed_drafts:
                failed_drafts.append(draft)
            
            updated_state.update({
                "review_result": "REJECTED", 
                "reviewer_feedback": feedback,
                "attempts": new_attempts,
                "failed_drafts": failed_drafts,
                "approved": False
            })
        
        return updated_state
        
    except Exception as e:
        print(f"❌ Review failed: {e}")
        return {
            **state,
            "review_result": "REJECTED",
            "reviewer_feedback": f"Review system error: {str(e)}",
            "approved": False
        }