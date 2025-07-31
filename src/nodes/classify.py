# # File: src/nodes/classify.py
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import StrOutputParser
# from state import AgentState
# from llm import get_llm # Assuming get_llm returns your LLM instance

# def classify(state: AgentState) -> dict:
#     """
#     Classifies the support ticket into a predefined category using an LLM.
#     """
#     llm = get_llm()

#     subject = state.get("subject", "")
#     description = state.get("description", "")

#     # Define the allowed categories based on your Assessment Task
#     # IMPORTANT: Ensure this list matches the categories you expect for your RAG system
#     categories = ["Billing", "Technical", "Security", "General", "Account Management", "Product Features"] # Example: Added more categories for realism

#     classification_prompt = ChatPromptTemplate.from_messages([
#         ("system", f"""You are an expert support ticket classifier. Your task is to accurately categorize customer support tickets into one of the following predefined categories:
#         {', '.join(categories)}

#         Carefully analyze the subject and description of the ticket. Choose the SINGLE BEST category that most accurately reflects the customer's primary issue.

#         **CRITICAL:** Respond ONLY with the chosen category name. Do NOT include any other text, explanations, or punctuation. Your response must be one of the exact category names from the list above.
#         """),
#         ("human", f"""
#         Customer Ticket:
#         Subject: {subject}
#         Description: {description}

#         Which category does this ticket belong to?
#         """)
#     ])

#     try:
#         print("🗂️ Classifying ticket...")
#         # Invoke the LLM chain to get the category
#         category_response = llm.invoke(
#             classification_prompt.format_messages(
#                 subject=subject,
#                 description=description
#             )
#         )
        
#         # Parse the raw LLM output to get just the category name
#         # We try to clean it up in case the LLM adds extra characters
#         predicted_category = category_response.content.strip()

#         # Basic validation: Check if the predicted category is in our allowed list
#         if predicted_category not in categories:
#             print(f"⚠️ LLM predicted unknown category '{predicted_category}'. Defaulting to 'General'.")
#             category = "General"
#         else:
#             category = predicted_category

#         print(f"🗂️ Ticket classified as: {category}")
#         return {**state, "category": category}

#     except Exception as e:
#         print(f"Error classifying ticket: {e}. Defaulting to 'General' category.")
#         return {**state, "category": "General"}





# now with RAG

from langchain_core.prompts import ChatPromptTemplate
from state import AgentState
from llm import get_llm

def classify(state: AgentState) -> dict:
    """
    Classifies the support ticket into a predefined category using an LLM.
    """
    llm = get_llm()
    
    subject = state.get("subject", "")
    description = state.get("description", "")
    
    # Categories matching your mock_docs.json
    categories = ["billing", "technical", "security", "general"]
    
    classification_prompt = ChatPromptTemplate.from_messages([
        ("system", f"""You are an expert support ticket classifier. Your task is to accurately categorize customer support tickets into one of the following predefined categories:
        {', '.join(categories)}
        
        Carefully analyze the subject and description of the ticket. Choose the SINGLE BEST category that most accurately reflects the customer's primary issue.
        
        CRITICAL: Respond ONLY with the chosen category name. Do NOT include any other text, explanations, or punctuation. Your response must be one of the exact category names from the list above.
        """),
        ("human", f"""
        Customer Ticket:
        Subject: {subject}
        Description: {description}
        
        Which category does this ticket belong to?
        """)
    ])
    
    try:
        print("🗂️ Classifying ticket...")
        category_response = llm.invoke(
            classification_prompt.format_messages(
                subject=subject,
                description=description
            )
        )
        
        predicted_category = category_response.content.strip().lower()
        
        if predicted_category not in categories:
            print(f"⚠️ LLM predicted unknown category '{predicted_category}'. Defaulting to 'general'.")
            category = "general"
        else:
            category = predicted_category
        
        print(f"🗂️ Ticket classified as: {category}")
        return {**state, "category": category}  # Fixed: proper state spreading
    
    except Exception as e:
        print(f"Error classifying ticket: {e}. Defaulting to 'general' category.")
        return {**state, "category": "general"}