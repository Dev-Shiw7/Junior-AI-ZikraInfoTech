#!/usr/bin/env python3
"""
Run this script once to set up the RAG system with your JSON knowledge base
"""

from src.rag_setup import RAGSystem
import os

def main():
    print("🚀 Setting up RAG system with your JSON knowledge base...")
    
    # Check if knowledge base file exists
    kb_file = "knowledge_base.json"
    if not os.path.exists(kb_file):
        print(f"❌ Knowledge base file '{kb_file}' not found!")
        print("Please create the file with your knowledge base JSON.")
        return
    
    # Initialize RAG system
    rag_system = RAGSystem(knowledge_base_path=kb_file)
    
    # Populate knowledge base
    rag_system.populate_knowledge_base()
    
    # Test retrieval
    print("\n🧪 Testing retrieval...")
    
    test_queries = [
        ("I want a refund", "billing"),
        ("Can't login to my account", "technical"),
        ("Someone accessed my account", "security"),
        ("What are your hours?", "general")
    ]
    
    for query, category in test_queries:
        print(f"\n📋 Testing: '{query}' in {category}")
        docs = rag_system.retrieve_relevant_docs(query, category, n_results=2)
        
        if docs:
            for doc in docs:
                print(f"   📄 [{doc['distance']:.3f}] {doc['content'][:60]}...")
        else:
            print("   ❌ No documents found")
    
    print("\n✅ RAG setup complete! Your system now uses real document retrieval.")

if __name__ == "__main__":
    main()