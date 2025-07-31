#!/usr/bin/env python3
"""
Test script to verify RAG system works with your project
"""

import sys
import os
sys.path.append('src')

from simple_rag import SimpleRAG

def test_rag():
    print("🧪 Testing RAG System Integration")
    print("=" * 50)
    
    # Check if knowledge base exists
    if not os.path.exists("data/mock_docs.json"):
        print("❌ data/mock_docs.json not found! Please create it first.")
        return False
    
    # Initialize RAG
    print("🚀 Initializing RAG system...")
    rag = SimpleRAG()
    
    if not rag.model:
        print("❌ RAG initialization failed!")
        return False
    
    # Test queries matching your categories
    test_cases = [
        ("I want a refund for my subscription", "billing"),
        ("Can't login to my account", "technical"),
        ("Someone accessed my account", "security"), 
        ("What are your support hours?", "general")
    ]
    
    print("\n🔍 Testing document retrieval...")
    print("-" * 50)
    
    success_count = 0
    for query, category in test_cases:
        print(f"\n📋 Testing: '{query}' → {category}")
        
        results = rag.retrieve_documents(query, category, top_k=2)
        
        if results:
            success_count += 1
            for i, doc in enumerate(results, 1):
                similarity = doc['similarity'] * 100
                content = doc['content'][:60] + "..." if len(doc['content']) > 60 else doc['content']
                print(f"   ✅ {i}. [{similarity:.1f}%] {content}")
        else:
            print(f"   ❌ No results found")
    
    print(f"\n📊 Results: {success_count}/{len(test_cases)} test cases successful")
    
    if success_count == len(test_cases):
        print("🎉 RAG system is working perfectly!")
        return True
    else:
        print("⚠️ Some test cases failed - check your setup")
        return False

if __name__ == "__main__":
    test_rag()