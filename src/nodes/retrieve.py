# 



# now with rag







from state import AgentState
from simple_rag import get_rag_system

def retrieve(state: AgentState) -> AgentState:
    """
    Retrieve relevant documents using RAG system
    """
    try:
        subject = state.get("subject", "")
        description = state.get("description", "")
        category = state.get("category", "general")
        
        # Create search query
        search_query = f"{subject} {description}".strip()
        if not search_query:
            search_query = subject or description or "general support"
        
        print(f"🔍 RAG retrieval for: '{search_query}' (category: {category})")
        
        # Get RAG system
        rag_system = get_rag_system()
        
        if not rag_system.model:
            print("⚠️ RAG system not available, using fallback")
            fallback_context = f"RAG system unavailable. Handle {category} issue: {subject}"
            return {**state, "context": fallback_context}
        
        # Retrieve relevant documents
        relevant_docs = rag_system.retrieve_documents(
            query=search_query,
            category=category,
            top_k=3
        )
        
        # Format context
        if relevant_docs:
            context = rag_system.format_context(relevant_docs, search_query)
            print(f"✅ Retrieved {len(relevant_docs)} relevant documents")
        else:
            context = f"""
No specific documentation found for this {category} issue: "{search_query}"

General guidance:
- Acknowledge the customer's concern professionally
- Provide helpful information based on standard support practices  
- Escalate if the issue seems complex or requires specialized knowledge
            """.strip()
            print("⚠️ No relevant documents found, using fallback guidance")
        
        return {**state, "context": context}  # Fixed: proper state spreading
        
    except Exception as e:
        print(f"❌ RAG retrieval failed: {e}")
        
        # Fallback context
        fallback_context = f"""
Context retrieval failed for this {category} issue: "{subject}"
Please provide general helpful guidance and escalate if needed.
        """.strip()
        
        return {**state, "context": fallback_context}